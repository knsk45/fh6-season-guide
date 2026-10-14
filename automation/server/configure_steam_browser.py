"""Verify existing Steam editors and save disabled browser configuration.

No form filling/submission, approval creation, cookie access, or timer activation.
"""
import copy
import fcntl
import json
import os
from pathlib import Path
import pwd
import re
import subprocess
import sys
import time
from urllib.parse import parse_qs, urlsplit

ROOT = Path('/opt/fh6/repo')
STORE = Path('/var/lib/fh6')
CONFIG = Path('/etc/fh6/steam-browser.json')
GUIDE_ID = '3787739730'
SECTION_IDS = {'ru': '9235220', 'en': '9330926'}
SAVE = 'a.btn_green_white_innerfade[href*="ValidateEditSubSectionForm"]'


def candidate(current, project):
    if current.get('publishEnabled') is not False:
        raise ValueError('Publication must remain disabled')
    guide = project['steamGuide']
    if (current['cdp'] != 'http://127.0.0.1:9222'
            or current['publicUrl'] != guide['url']
            or parse_qs(urlsplit(guide['url']).query).get('id') != [GUIDE_ID]):
        raise ValueError('Unexpected dedicated browser or guide')
    result = copy.deepcopy(current)
    for lang, section_id in SECTION_IDS.items():
        section = result['sections'][lang]
        url = urlsplit(section['editUrl'])
        if (url.scheme != 'https' or url.netloc != 'steamcommunity.com'
                or url.path != '/sharedfiles/editguidesubsection/'
                or parse_qs(url.query) != {'id': [GUIDE_ID], 'sectionid': [section_id]}
                or section['titleText'] != guide['sections'][lang]['title']
                or section['publicText'] != f'[id="{section_id}"] > .subSectionDesc'):
            raise ValueError('Unexpected existing section mapping')
        section.update(title='input#title[name="title"]',
                       textarea='textarea#description[name="description"]', save=SAVE)
    # Semantic challenge fields only classify blockers. Every successful editor
    # still requires its exact URL, authenticated header, title and Save handler.
    result.update(loginSelector='input[type="password"]:visible',
                  guardSelector='input[autocomplete="one-time-code"]:visible',
                  publishEnabled=False, selectorsVerified=False)
    return result


def probe(config):
    sys.path.insert(0, str(ROOT / 'automation/server'))
    import steam_publish as worker
    from steam_consent import state
    from playwright.sync_api import sync_playwright
    result = {'sections': {}}
    desired = worker.texts(ROOT)
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(config['cdp'], timeout=15000)
        adapter = worker.SteamBrowser(browser, config)
        try:
            for lang in SECTION_IDS:
                adapter.ready(lang)  # navigation and DOM checks only
                header = adapter.page.locator('#account_pulldown')
                if header.count() != 1 or not header.is_visible():
                    raise ValueError('Authenticated header unavailable')
                save = adapter.page.locator(config['sections'][lang]['save'])
                callback = save.evaluate(r'''e =>
                    /^\s*javascript:\s*(?:return\s+)?ValidateEditSubSectionForm\s*\(/.test(e.getAttribute("href") || "")''')
                if not callback:
                    raise ValueError('Unexpected save handler')
                if not desired[lang].strip() or len(desired[lang]) > 4800:
                    raise ValueError('Invalid generated text')
                result['sections'][lang] = dict(editorVerified=True, saveVerified=True,
                    publicMatchesCurrent=adapter.matches(lang, desired[lang]),
                    generatedCharacters=len(desired[lang]))
        finally:
            adapter.page.close()
            adapter.public.close()
        # Playwright disconnects at context-manager exit; never close the
        # owner's browser or its persistent default authentication context.
    result.update(freshAuditAccepted=bool(worker.fresh_audit(ROOT)),
                  consentEnabled=bool(state(STORE)['enabled']))
    return result


def verified(result):
    sections = result.get('sections', {})
    for lang in SECTION_IDS:
        value = sections.get(lang, {})
        if value.get('editorVerified') is not True or value.get('saveVerified') is not True:
            raise ValueError('Both existing editors must pass')
        if type(value.get('publicMatchesCurrent')) is not bool:
            raise ValueError('Public verification unavailable')
        count = value.get('generatedCharacters')
        if type(count) is not int or not 0 < count <= 4800:
            raise ValueError('Invalid text length')


def atomic(path, data, gid):
    tmp = path.with_name(path.name + '.setup-tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o640)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
            os.fchown(stream.fileno(), 0, gid); os.fchmod(stream.fileno(), 0o640)
        os.replace(tmp, path)
        parent = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(parent)
        finally: os.close(parent)
    finally:
        tmp.unlink(missing_ok=True)


def main():
    if sys.argv[1:] == ['--probe']:
        if os.geteuid() != pwd.getpwnam('fh6').pw_uid:
            raise ValueError('Probe requires publisher user')
        print(json.dumps(probe(json.load(sys.stdin)), separators=(',', ':')))
        return
    if sys.argv[1:] or os.geteuid() != 0:
        raise ValueError('Configuration requires root without arguments')
    source = Path(__file__).absolute()
    if source.is_symlink() or source.stat().st_uid != 0 or source.stat().st_mode & 0o022:
        raise ValueError('Setup source must be root-owned and protected')
    if CONFIG.is_symlink() or CONFIG.stat().st_uid != 0 or CONFIG.stat().st_mode & 0o022:
        raise ValueError('Unexpected configuration ownership')
    for unit in ('fh6-steam-publish.service', 'fh6-steam-publish.timer'):
        if subprocess.run(['systemctl', 'is-active', '--quiet', unit]).returncode == 0:
            raise ValueError('Publication units must be inactive')
    if subprocess.run(['systemctl', 'is-enabled', '--quiet', 'fh6-steam-publish.timer']).returncode == 0:
        raise ValueError('Publication timer must remain disabled')
    if (STORE / 'runner.lock').is_symlink():
        raise ValueError('Unexpected runner lock')
    with (STORE / 'runner.lock').open('rb') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        old = CONFIG.read_bytes()
        project = json.loads((ROOT / 'data/project.json').read_text(encoding='utf-8-sig'))
        config = candidate(json.loads(old), project)
        child = subprocess.run(['runuser', '-u', 'fh6', '--', '/opt/fh6/venv/bin/python',
                                str(source), '--probe'], input=json.dumps(config),
                               text=True, capture_output=True, timeout=180)
        if child.returncode != 0:
            raise RuntimeError('Read-only browser verification failed; configuration unchanged')
        result = json.loads(child.stdout)
        verified(result)
        backup = STORE / 'repairs' / ('steam-browser-config-' + str(time.time_ns()))
        backup.mkdir(mode=0o700, parents=True)
        original = backup / 'steam-browser.json'
        original.write_bytes(old); original.chmod(0o600)
        config.update(selectorsVerified=True, verifiedAt=time.time())
        try:
            atomic(CONFIG, json.dumps(config, ensure_ascii=False, indent=2).encode(),
                   pwd.getpwnam('fh6').pw_gid)
        except Exception:
            atomic(CONFIG, old, pwd.getpwnam('fh6').pw_gid)
            raise
    print('STEAM_BROWSER_CONFIGURED publication=disabled; no form filled or submitted')
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    print('BACKUP=' + str(backup))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Browser errors may include private details; never echo them or stderr.
        print('STEAM_BROWSER_SETUP_FAILED type=' + type(error).__name__)
        raise SystemExit(1)
