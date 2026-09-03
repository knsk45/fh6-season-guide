"""Project-owned FH6 portable compatibility builder, NOT the retired plugin validator.

Python standard library + the existing Node renderer. Validation and a reopened
ZIP package must succeed before the public HTML is replaced. Receipts bind the
state, artifact, renderer, validator, HTML and every packaged local asset.
"""
import argparse
import base64
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit, parse_qsl
import zipfile

PROVIDER = 'fh6-portable/1.0.0'
CHAIN = ['automation/build_portable_report.py', 'reports/build_artifact.ps1',
         'reports/enhance_portable_html.mjs', 'automation/validate_season.ps1']

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def safe_path(root, name):
    require(isinstance(name, str) and name and '\\' not in name and not Path(name).is_absolute(), 'Invalid relative package path')
    path = (root / name).resolve()
    require(path.is_relative_to(root.resolve()) and '..' not in Path(name).parts, 'Path escapes project: ' + name)
    require(path.is_file(), 'Missing file: ' + name)
    return path

def replace_retry(source, target):
    for attempt in range(12):
        try:
            os.replace(source, target)
            return
        except PermissionError:
            if attempt == 11:
                raise
            time.sleep(min(.1 * (attempt + 1), .5))

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    replace_retry(temp, path)

def runtime(name):
    bundled = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies'
    fallback = bundled / ('node/bin/node.exe' if name == 'node' else 'native/powershell/pwsh.exe')
    found = shutil.which(name) or str(fallback)
    require(Path(found).is_file(), 'Missing runtime: ' + name)
    return found

def preflight(root):
    for name in CHAIN:
        safe_path(root, name)
    for name in ['node', 'pwsh']:
        subprocess.run([runtime(name), '--version'], check=True, capture_output=True, timeout=15)
    return {name: sha(root / name) for name in CHAIN}

class Node:
    def __init__(self, tag='', attrs=None):
        self.tag, self.attrs, self.children = tag, dict(attrs or []), []
    def all(self, tag=None, cls=None):
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if (tag is None or child.tag == tag) and (cls is None or cls in child.attrs.get('class', '').split()):
                    found.append(child)
                found.extend(child.all(tag, cls))
        return found
    def text(self):
        if self.tag in {'style', 'script'}:
            return ''
        value = ''.join(c.text() if isinstance(c, Node) else c for c in self.children)
        return '\n' + value + '\n' if self.tag in {'p','div','li','ol','ul','h2','section','article','br'} else value

class Document(HTMLParser):
    VOID = {'img', 'br', 'hr', 'meta', 'link', 'input', 'source', 'wbr', 'area', 'base', 'embed', 'param', 'track', 'col'}
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node(); self.stack = [self.root]
        self.feed(html); self.close()
    def handle_starttag(self, tag, attrs):
        require(len(attrs) == len(dict(attrs)), 'Duplicate HTML attribute')
        node = Node(tag, attrs); self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def normalized(html):
    text = Document(html).root.text()
    text = re.sub(r'(?<!\w)(S1|S2|[DCBARX])\s*([0-9]{3})(?![0-9])', r'\1\2', text, flags=re.I)
    return ' '.join(text.split())

def safe_link(url):
    parts = urlsplit(url or '')
    require(parts.scheme == 'https' and parts.hostname and not parts.username and not parts.password, 'Unsafe source URL')
    require(not any(re.search(r'token|secret|password|signature|api[_-]?key', key, re.I) for key, _ in parse_qsl(parts.query)), 'Secret-bearing source URL')

def links(nodes):
    result = []
    for a in nodes:
        safe_link(a.attrs.get('href'))
        require(a.attrs.get('target') == '_blank' and {'noopener', 'noreferrer'} <= set(a.attrs.get('rel', '').split()), 'Unsafe card link attributes')
        result.append((a.attrs['href'], ' '.join(a.text().split())))
    return result

def validate_artifact(root, state, artifact):
    season, manifest, snapshot = state['season'], artifact['manifest'], artifact['snapshot']
    require(artifact['surface'] == manifest['surface'] == 'dashboard', 'Unsupported portable surface')
    require(manifest['version'] == snapshot['version'] == 1, 'Unsupported manifest/snapshot version')
    require(manifest['title'] == season['reportTitle'], 'Artifact title mismatch')
    from datetime import datetime
    stamps = [manifest['generatedAt'], snapshot['generatedAt'], artifact['package_info']['generated_at']]
    require(all(datetime.fromisoformat(s) == datetime.fromisoformat(state['lastContentUpdate']) for s in stamps), 'Artifact timestamp mismatch')
    require(snapshot['accessIssues'] == state['openItems'], 'Lost unresolved evidence')
    require(snapshot['status'] == ('partial' if state['openItems'] else 'ready'), 'Incorrect evidence status')
    require(snapshot['datasets'] == {} and manifest['charts'] == [] and manifest['sources'] == [] and artifact['sources'] == [], 'Unsupported legacy artifact extension; add explicit support before use')
    cards = state['activities']; blocks = manifest['blocks']
    require(len(cards) == season['expectedCardCount'] and [c['id'] for c in cards] == [b['id'] for b in blocks], 'Artifact activity count/order mismatch')
    for card, block in zip(cards, blocks):
        require(block['type'] == 'html' and block['layout'] == 'full', 'Unsupported block type/layout')
        doc = Document(block['body']).root
        require(len(doc.all('article', 'card')) == 1 and len(doc.all('style')) == 1, 'Invalid card envelope')
        require(len(doc.all('h2')) == 1 and normalized(doc.all('h2')[0].text()) == normalized(card['title']), 'Card title mismatch')
        require(len(doc.all('span','number')) == 1 and doc.all('span','number')[0].text() == str(card['number']), 'Card number mismatch')
        require(len(doc.all('span','points')) == 1 and doc.all('span','points')[0].text() == str(card['points']), 'Card points mismatch')
        require(len(doc.all('div','eyebrow')) == 1 and normalized(doc.all('div','eyebrow')[0].text()) == normalized(str(card['kind']) + str(card['points'])), 'Card kind mismatch')
        allowed = {'style','article','div','img','span','h2','p','ol','ul','li','strong','code','a','em','b','br'}
        for node in doc.all():
            require(node.tag in allowed and not any(k.lower().startswith('on') for k in node.attrs), 'Active/unsupported HTML in card')
        require(not re.search(r'@import|url\s*\(|expression\s*\(', block['body'], re.I), 'External/active CSS in card')
        paragraphs = doc.all('p')
        require(len(paragraphs) == 3, 'Expected condition, how-to and tune paragraphs')
        for node, key, label in zip(paragraphs, ['conditionHtml','howHtml','tuneHtml'], ['Условие:', 'Как выполнить:', 'Автомобиль и тюнинг:']):
            require(normalized(node.text()) == normalized(label + ' ' + card[key]), 'Artifact content differs from state: ' + key)
        expected_links = links(Document(card['sourceHtml']).root.all('a'))
        expected_links.append((card['visual'].get('sourceUrl') or season['fandomUrl'], card['visual'].get('sourceLabel') or 'изображение и иконка: Forza Wiki'))
        require(links(doc.all('a')) == expected_links, 'Artifact source links differ from state')
        images = doc.all('img')
        require(len(images) == 2, 'Each card needs image and icon')
        for image, key in zip(images, ['image','icon']):
            name = season['assetsDirectory'] + '/' + card['visual'][key]
            asset = safe_path(root, name)
            require(name.startswith('reports/assets/'), 'Asset outside reports/assets')
            require(image.attrs.get('data-local-src') == name.removeprefix('reports/'), 'Image references wrong season asset')
            match = re.fullmatch(r'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)', image.attrs.get('src',''))
            require(match and base64.b64decode(match[2], validate=True) == asset.read_bytes(), 'Embedded image differs from local asset')
    return blocks

def validate_html(root, html, state, artifact, project):
    require(len(html.encode()) <= state['season']['maxPublicHtmlBytes'], 'HTML exceeds size budget')
    require(not re.search(r'<iframe\b|data:image/|data-analytics-portable-reader', html, re.I), 'Heavy/embedded runtime in public HTML')
    doc = Document(html).root
    sections = [n for n in doc.all('section') if 'data-activity-block' in n.attrs]
    require([n.attrs.get('id') for n in sections] == [c['id'] for c in state['activities']], 'Public card order mismatch')
    for section, block in zip(sections, artifact['manifest']['blocks']):
        require(normalized(section.text()) == normalized(block['body']), 'Public card lost or changed content')
        require(links(section.all('a')) == links(Document(block['body']).root.all('a')), 'Public card lost links')
    times = [n for n in doc.all('time') if 'updated' in n.attrs.get('class','').split()]
    require(len(times) == 1 and times[0].attrs.get('datetime') == artifact['snapshot']['generatedAt'], 'Public freshness timestamp mismatch')
    scripts = doc.all('script')
    require(len(scripts) == 1 and 'src' not in scripts[0].attrs and state['season']['endAt'] in html, 'Unexpected script or deadline')
    support = [n for n in doc.all('section') if 'data-support-block' in n.attrs]
    require(len(support) == 1 and len(support[0].all('div','visit-stats')) == 1, 'Support/analytics block missing')
    require(html.index('data-support-block') > html.rindex('data-activity-block'), 'Support must follow all activities')
    require(project['support']['title'] in support[0].text(), 'Support title mismatch')
    require(sum(a.attrs.get('href') == project['support']['url'] for a in support[0].all('a')) == 2, 'Support links mismatch')
    for rel, key in [('icon','faviconPng'),('apple-touch-icon','appleTouchIcon')]:
        assets = [n.attrs.get('href') for n in doc.all('link') if n.attrs.get('rel') == rel]
        require(assets == [project['branding'][key].removeprefix('reports/')], 'Branding mismatch')
    files = {}
    counters = 0
    for node in doc.all('img') + doc.all('link'):
        attr = 'src' if node.tag == 'img' else 'href'
        name = node.attrs.get(attr, '')
        if name == project['analytics']['counterImageUrl'] and node.tag == 'img':
            counters += 1
            continue
        require(name.startswith('assets/'), 'Unexpected external asset: ' + name)
        asset = safe_path(root / 'reports', name)
        files[name] = sha(asset)
    require(counters == 1, 'Expected exactly the configured visit counter')
    require(project['support']['qrAsset'].removeprefix('reports/') in files, 'QR asset missing')
    return files

def validate_zip(package, files):
    with zipfile.ZipFile(package) as archive:
        require(sorted(archive.namelist()) == sorted(files), 'Package entries mismatch')
        require(archive.testzip() is None, 'Package CRC failed')
        for name, expected in files.items():
            require(hashlib.sha256(archive.read(name)).hexdigest() == expected, 'Package bytes differ: ' + name)

def verify_receipt(root, path):
    receipt = read(path)
    require(receipt['schemaVersion'] == 1 and receipt['provider'] == PROVIDER and receipt['validation'] == receipt['package'] == 'passed', 'No compatible successful receipt')
    for name, expected in receipt['inputs'].items():
        require(sha(safe_path(root, name)) == expected, 'Build input changed: ' + name)
    required = set(CHAIN + ['data/current-season.json','data/project.json','reports/artifact.json'])
    require(set(receipt['inputs']) == required, 'Receipt input coverage incomplete')
    state, project, artifact = read(root/'data/current-season.json'), read(root/'data/project.json'), read(root/'reports/artifact.json')
    validate_artifact(root, state, artifact)
    current = validate_html(root, (root/'reports/current-week.html').read_text(encoding='utf-8'), state, artifact, project)
    current['current-week.html'] = sha(root/'reports/current-week.html')
    require(current == receipt['files'], 'Published package file set changed')
    for name, expected in current.items():
        require(sha(safe_path(root/'reports', name)) == expected, 'Packaged file changed: ' + name)
    package = safe_path(root, receipt['zipPath'])
    require(sha(package) == receipt['zipSha256'], 'Package hash mismatch')
    validate_zip(package, current)
    return receipt

def build(root, receipt_path):
    preflight(root)
    state, project, artifact = read(root/'data/current-season.json'), read(root/'data/project.json'), read(root/'reports/artifact.json')
    validate_artifact(root, state, artifact)
    checked = subprocess.run([runtime('pwsh'), '-NoProfile', '-File', str(root/'automation/validate_season.ps1'), '-SkipOutputs'], capture_output=True, text=True, encoding='utf-8', timeout=60)
    require(checked.returncode == 0 and 'STRUCTURE_OK' in checked.stdout, 'State validation failed: ' + checked.stdout + checked.stderr)
    inputs = {name: sha(root/name) for name in CHAIN + ['data/current-season.json','data/project.json','reports/artifact.json']}
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='portable-', dir=receipt_path.parent) as directory:
        candidate = Path(directory)/'current-week.html'
        subprocess.run([runtime('node'), str(root/'reports/enhance_portable_html.mjs'), '--root', str(root), '--output', str(candidate)], check=True, timeout=60)
        files = validate_html(root, candidate.read_text(encoding='utf-8'), state, artifact, project)
        files['current-week.html'] = sha(candidate)
        package = receipt_path.with_suffix('.zip')
        temporary_zip = Path(directory)/'report.zip'
        with zipfile.ZipFile(temporary_zip, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for name in sorted(files):
                archive.write(candidate if name == 'current-week.html' else root/'reports'/name, name)
        validate_zip(temporary_zip, files)
        require(all(sha(root/name) == value for name, value in inputs.items()), 'Build inputs changed during execution')
        replace_retry(temporary_zip, package)
        receipt = {'schemaVersion':1, 'provider':PROVIDER, 'validation':'passed', 'package':'passed',
                   'verification':'structural_only', 'inputs':inputs, 'files':files,
                   'zipPath':package.relative_to(root).as_posix(), 'zipSha256':sha(package),
                   'generatedAt':artifact['snapshot']['generatedAt'], 'cards':len(state['activities'])}
        replace_retry(candidate, root/'reports/current-week.html')
        atomic_json(receipt_path, receipt)
        atomic_json(root/'automation/runs/current-portable-receipt.json', receipt)
    verify_receipt(root, receipt_path)
    print('PORTABLE_PROVIDER=' + PROVIDER + '\nPORTABLE_VALIDATION=passed\nPORTABLE_PACKAGE=passed\nPORTABLE_RECEIPT=' + str(receipt_path))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['preflight','build','verify'])
    p.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    p.add_argument('--receipt')
    a = p.parse_args(); root = Path(a.root).resolve()
    receipt = Path(a.receipt).resolve() if a.receipt else root/'automation/runs/current-portable-receipt.json'
    require(receipt.is_relative_to(root/'automation/runs'), 'Receipt must stay in local automation/runs')
    if a.action == 'preflight':
        preflight(root); print('PORTABLE_PREFLIGHT=OK\nPORTABLE_PROVIDER=' + PROVIDER)
    elif a.action == 'build':
        build(root, receipt)
    else:
        verify_receipt(root, receipt); print('PORTABLE_RECEIPT_VERIFIED=OK')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('PORTABLE_BUILD_FAILED=' + str(error), file=sys.stderr)
        sys.exit(1)
