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
import subprocess
import sys
import tempfile
import time
import urllib.request
from urllib.parse import urlsplit, urlunsplit
from phone_tasks import save,read

PAGE='https://forza.labsgg.com/series/details'
PREFIX='/images/jr6fd40q/production/'
MAX_IMAGE=8*1024*1024
MAX_TOTAL=48*1024*1024
MAX_CANDIDATES=24


class HandoffError(RuntimeError):
    pass


HANDOFF_CHECK=r'''
import hashlib,json,re,sys
from pathlib import Path
folder=Path(sys.argv[1]);index=json.loads((folder/'index.json').read_text())
assert index['section']==sys.argv[2] and isinstance(index['entries'],list)
for row in index['entries']:
    name=row['path']
    assert re.fullmatch(r'[a-f0-9]{64}\.(png|jpg|webp)',name)
    file=folder/name
    assert not file.is_symlink() and file.is_file() and file.stat().st_size<=8*1024*1024
    raw=file.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']==name.split('.')[0]
print(len(index['entries']))
'''


def verify_handoff(folder,section,user='fh6-editor'):
    command=[sys.executable,'-c',HANDOFF_CHECK,str(folder),section]
    if user:command=['runuser','-u',user,'--',*command]
    try:result=subprocess.run(command,capture_output=True,text=True,timeout=30)
    except (OSError,subprocess.TimeoutExpired):
        raise HandoffError('Image handoff reader did not complete') from None
    if result.returncode or not result.stdout.strip().isdigit():
        raise HandoffError('Downloaded image handoff failed integrity/readability checks')
    return int(result.stdout.strip())


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


def cached_entry(cache,candidate,previous):
    receipt=cache/('source-'+hashlib.sha256(candidate['url'].encode()).hexdigest()+'.json')
    # A damaged receipt must not hide a valid index entry or prevent re-download.
    for entry in (read(receipt),previous.get(candidate['url'],{})):
        try:
            if not isinstance(entry,dict) or entry.get('url')!=candidate['url']:continue
            name=entry.get('path','')
            if not re.fullmatch(r'[a-f0-9]{64}\.(?:png|jpg|webp)',name):continue
            file=cache/name
            if file.is_symlink() or not file.is_file() or file.stat().st_size>MAX_IMAGE:continue
            raw=file.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=entry.get('sha256'):continue
            extension(raw,'image/verified-cache')
            return dict(entry,label=candidate['label'],bytes=len(raw),reused=True)
        except (OSError,ValueError,TypeError):continue
    return None


def download(url,limit):
    for attempt in range(2):
        try:return fetch(url,limit)
        except OSError:
            if attempt:raise
            time.sleep(1)


def collect(root,store,state):
    key=section_key(state)
    cache=Path(store)/'tile-image-cache'/key
    for parent in (cache.parent,cache):
        if parent.is_symlink():raise ValueError('Unexpected cache symlink')
        parent.mkdir(mode=0o750,parents=True,exist_ok=True)
        if os.geteuid()==0:shutil.chown(parent,group='fh6')
    manifest=dict(section=key,pageUrl=PAGE,checkedAt=datetime.now().astimezone().isoformat(),
                  status='UNAVAILABLE',entries=[],errors=[])
    old_index=read(cache/'index.json')
    old_rows=old_index.get('entries',[]) if isinstance(old_index,dict) else []
    previous={row['url']:row for row in old_rows if isinstance(row,dict) and isinstance(row.get('url'),str)} if isinstance(old_rows,list) else {}
    try:
        page,mime=download(PAGE,4*1024*1024)
        if mime!='text/html':raise ValueError('Not a source page')
        parser=Images(key);parser.feed(page.decode('utf-8'))
        manifest['pageSha256']=hashlib.sha256(page).hexdigest()
        if not parser.found:
            manifest['status']='NO_CURRENT_SECTION'
        else:
            total=0
            for candidate in parser.items[:MAX_CANDIDATES]:
                try:
                    cached=cached_entry(cache,candidate,previous)
                    if cached and total+cached['bytes']<=MAX_TOTAL:
                        total+=cached['bytes'];manifest['entries'].append(cached)
                        save(cache/('source-'+hashlib.sha256(candidate['url'].encode()).hexdigest()+'.json'),cached)
                        continue
                    raw,mime=download(candidate['url'],min(MAX_IMAGE,MAX_TOTAL-total))
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
                    entry=dict(candidate,path=name,sha256=sha,bytes=len(raw))
                    save(cache/('source-'+hashlib.sha256(candidate['url'].encode()).hexdigest()+'.json'),entry)
                    manifest['entries'].append(entry)
                except Exception as exc:
                    manifest['errors'].append(dict(url=candidate['url'],error=type(exc).__name__))
                if total>=MAX_TOTAL:break
            manifest['status']=('PARTIAL' if manifest['errors'] else 'AVAILABLE') if manifest['entries'] else 'UNAVAILABLE'
    except Exception as exc:manifest['errors'].append(dict(error=type(exc).__name__))
    save(cache/'index.json',manifest)
    return cache,manifest
