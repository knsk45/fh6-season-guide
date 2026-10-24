"""Download bounded current-season image evidence before the offline editor runs.

Only the configured public ForzaLabs page and its fixed image CDN are allowed.
Downloads are candidates, never proof of a matching tile or publication consent.
"""
from datetime import datetime
import hashlib
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
import tempfile
import urllib.request
from urllib.parse import urlsplit, urlunsplit
from phone_tasks import save

PAGE='https://forza.labsgg.com/series/details'
PREFIX='/images/jr6fd40q/production/'
MAX_IMAGE=8*1024*1024
MAX_TOTAL=48*1024*1024
MAX_CANDIDATES=24


def section_key(state):
    season=state['season']
    name=season['season']
    if name not in {'summer','autumn','winter','spring'}:raise ValueError('Unknown season')
    day=datetime.fromisoformat(season['startAt']).date().isoformat()
    return name+'-'+day


def original_url(value):
    url=urlsplit(value)
    if (url.scheme!='https' or url.netloc!='cdn.sanity.io' or
            not re.fullmatch(re.escape(PREFIX)+r'[a-f0-9]{40}-[0-9]{2,5}x[0-9]{2,5}\.(?:png|jpg|jpeg|webp)',url.path)):
        raise ValueError('Unexpected image origin/path')
    # Download untouched originals, not transformed/resized CDN variants.
    return urlunsplit(('https','cdn.sanity.io',url.path,'',''))


class Images(HTMLParser):
    def __init__(self,section):
        super().__init__();self.section=section;self.depth=0;self.items=[];self.found=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='article':
            if self.depth:self.depth+=1
            elif attrs.get('id')==self.section:self.depth=1;self.found=True
        if tag=='img' and self.depth:
            try:url=original_url(attrs.get('src',''))
            except ValueError:return
            if url not in {v['url'] for v in self.items}:
                self.items.append(dict(url=url,label=attrs.get('alt','')[:250]))
    def handle_endtag(self,tag):
        if tag=='article' and self.depth:self.depth-=1


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise ValueError('Redirect outside the fixed download request is not accepted')


def fetch(url,limit):
    opener=urllib.request.build_opener(NoRedirect())
    request=urllib.request.Request(url,headers={'User-Agent':'FH6-evidence-collector/1.0'})
    with opener.open(request,timeout=20) as response:
        raw=response.read(limit+1)
        if len(raw)>limit:raise ValueError('Download exceeds byte limit')
        return raw,response.headers.get_content_type()


def extension(raw,mime):
    if not mime.startswith('image/'):raise ValueError('Not an image response')
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):return '.png'
    if raw.startswith(b'\xff\xd8\xff'):return '.jpg'
    if raw[:4]==b'RIFF' and raw[8:12]==b'WEBP':return '.webp'
    raise ValueError('Unsupported image bytes')


def collect(root,store,state):
    key=section_key(state)
    cache=Path(store)/'tile-image-cache'/key
    for parent in (cache.parent,cache):
        if parent.is_symlink():raise ValueError('Unexpected cache symlink')
        parent.mkdir(mode=0o750,parents=True,exist_ok=True)
        if os.geteuid()==0:shutil.chown(parent,group='fh6')
    manifest=dict(section=key,pageUrl=PAGE,checkedAt=datetime.now().astimezone().isoformat(),
                  status='UNAVAILABLE',entries=[],errors=[])
    try:
        page,mime=fetch(PAGE,4*1024*1024)
        if mime!='text/html':raise ValueError('Not a source page')
        parser=Images(key);parser.feed(page.decode('utf-8'))
        manifest['pageSha256']=hashlib.sha256(page).hexdigest()
        if not parser.found:
            manifest['status']='NO_CURRENT_SECTION'
        else:
            total=0
            for candidate in parser.items[:MAX_CANDIDATES]:
                try:
                    raw,mime=fetch(candidate['url'],min(MAX_IMAGE,MAX_TOTAL-total))
                    suffix=extension(raw,mime);total+=len(raw)
                    sha=hashlib.sha256(raw).hexdigest();name=sha+suffix
                    target=cache/name
                    if target.is_symlink():raise ValueError('Unexpected image symlink')
                    fd,temp=tempfile.mkstemp(dir=cache,prefix='.image-')
                    try:
                        with os.fdopen(fd,'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
                        os.chmod(temp,0o640)
                        if os.geteuid()==0:shutil.chown(temp,group='fh6')
                        os.replace(temp,target)
                    finally:Path(temp).unlink(missing_ok=True)
                    manifest['entries'].append(dict(candidate,path=name,sha256=sha,bytes=len(raw)))
                except Exception as exc:
                    manifest['errors'].append(dict(url=candidate['url'],error=type(exc).__name__))
                if total>=MAX_TOTAL:break
            manifest['status']='AVAILABLE' if manifest['entries'] else 'UNAVAILABLE'
    except Exception as exc:manifest['errors'].append(dict(error=type(exc).__name__))
    save(cache/'index.json',manifest)
    return cache,manifest
