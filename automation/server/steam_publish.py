"""Owner-approved two-section publication. No credentials or browser profiles read."""
import argparse
import fcntl
import hashlib
import json
import re
import time
import os
import sys
from datetime import datetime
from pathlib import Path

FILES = {'ru': 'steam-guide-current.txt', 'en': 'steam-guide-current-en.txt'}
MESSAGES = {
    'NEEDS_SETUP': 'Нужно настроить и проверить серверный браузер Steam.',
    'NEEDS_APPROVAL': 'Разрешение отсутствует или отозвано. Проверьте тумблер в панели.',
    'AUDIT_REQUIRED': 'Нужна свежая полная проверка сезона перед публикацией.',
    'COMPLETE': 'Оба раздела публично проверены.',
    'NEEDS_LOGIN': 'Войдите в Steam в выделенном браузере и повторите запуск.',
    'STEAM_GUARD': 'Подтвердите Steam Guard самостоятельно в браузере и повторите запуск.',
    'UNCERTAIN': 'Отправка могла пройти. Нужна публичная проверка; повторная отправка запрещена.',
    'BLOCKED': 'Проверка недоступна или структура Steam изменилась. Публикация остановлена.',
    'STALE_APPROVAL': 'Тексты изменились. Прочитайте обе версии в панели и разрешите заново.',
}


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    with tmp.open('w',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2)
        stream.flush();os.fsync(stream.fileno());os.fchmod(stream.fileno(),0o640)
    tmp.replace(path)
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def fresh_audit(root):
    sys.path.insert(0,str(root/'automation'))
    try:
        from refresh_guard import Guard
        active=json.loads((root/'automation/runs/refresh/active.json').read_text())
        return active.get('status') in {'PENDING_CONFIRMATION','COMPLETED','AWAITING_DELIVERY'} and Guard(root).audit_valid(active)
    except (ImportError,OSError,ValueError,KeyError,TypeError):return False

def approved(approval,key,store):
    if (approval.get('action')!='replace-current-ru-en' or approval.get('sha256')!=key
            or approval.get('status')!='AWAITING_BROWSER_PUBLICATION'
            or type(approval.get('approvedAt')) not in {int,float}
            or not 0<=time.time()-approval['approvedAt']<=86400):return False
    if approval.get('automatic'):
        from steam_consent import state
        policy=state(store)
        return policy['enabled'] and approval.get('standingConsentAt')==policy['updatedAt']
    return True


def texts(root):
    return {lang: (root/'reports'/name).read_text(encoding='utf-8-sig') for lang, name in FILES.items()}


def combined(values):
    return digest('\n'.join(values[lang] for lang in FILES))


def substantive(text):
    text = re.sub(r'(?m)^\[b\]Последняя проверка данных:\[/b\][^\r\n]*(\r?\n)?', '', text)
    return digest(text.replace('\r\n', '\n').strip())


def publish(root, store, approval, browser):
    """Caller holds exclusive lock. Every submit is durably recorded first."""
    desired = texts(root)
    key = combined(desired)
    state_path = store/'steam-publication'/f'{key}.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {'sections': {}}

    def save(status):
        state.update(status=status, message=MESSAGES.get(status, status), sha256=key, updatedAt=time.time())
        atomic(state_path, state)
        atomic(store/'steam-status.json', state)
        return state

    if not approved(approval,key,store):
        return save('STALE_APPROVAL')
    if not fresh_audit(root):return save('AUDIT_REQUIRED')
    if any(not value.strip() or len(value) > 4800 for value in desired.values()):
        return save('BLOCKED')
    try:
        for lang in FILES:
            # Always inspect public section first, even after a crash/timeout.
            if browser.matches(lang, desired[lang]):
                state['sections'][lang] = 'VERIFIED'
                save('VERIFYING')
                continue
            if state['sections'].get(lang) in {'SUBMITTING', 'VERIFIED'}:
                return save('UNCERTAIN')
            browser.ready(lang)
            def before_save():
                if texts(root)!=desired:raise Stop('STALE_APPROVAL')
                if not approved(approval,key,store):raise Stop('NEEDS_APPROVAL')
                if not fresh_audit(root):raise Stop('AUDIT_REQUIRED')
                state['sections'][lang]='SUBMITTING'
                save('PUBLISHING')
            browser.replace(lang, desired[lang],before_save)
            if not browser.matches(lang, desired[lang]):
                return save('UNCERTAIN')
            state['sections'][lang] = 'VERIFIED'
            save('VERIFYING')
        if texts(root) != desired:
            return save('STALE_APPROVAL')
        if not all(browser.matches(lang, desired[lang]) for lang in FILES):
            return save('UNCERTAIN')
        project = json.loads((root/'data/project.json').read_text(encoding='utf-8-sig'))['steamGuide']
        audit = json.loads((root/'data/current-season.json').read_text(encoding='utf-8-sig'))['lastContentUpdate']
        # Baselines only follow the final fresh public verification of BOTH locales.
        targets={}
        for lang in FILES:
            section = project['sections'][lang]
            target = (root/section['publicationStatePath']).resolve()
            if not target.is_relative_to((root/'automation/runs').resolve()):
                return save('BLOCKED')
            targets[lang]=target
        for lang in FILES:
            section=project['sections'][lang];target=targets[lang]
            atomic(target, dict(schemaVersion=1, contentHash=substantive(desired[lang]),
                   publishedAt=datetime.now().astimezone().isoformat(), sourceAuditAt=audit, steamGuideUrl=project['url'],
                   language=lang, sectionTitle=section['title'], evidence='Both public sections verified; approval '+key))
        return save('COMPLETE')
    except Stop as exc:
        return save(str(exc))
    except Exception:
        # Never persist browser exceptions (may contain private URLs/session details).
        return save('UNCERTAIN' if 'SUBMITTING' in state['sections'].values() else 'BLOCKED')


class Stop(Exception):
    pass


class SteamBrowser:
    """Connect to an operator-opened browser. Selectors require installation review.

    publicText must select the full visible body of exactly one existing section.
    Expected visible text strips only the mirror's supported BBCode vocabulary.
    """
    def __init__(self, browser, config):
        self.browser, self.config = browser, config
        if len(browser.contexts)!=1:raise Stop('NEEDS_SETUP')
        self.context = browser.contexts[0]
        self.public = browser.new_context()  # no cookies: public verification
        self.page = self.context.new_page()
        self.viewer = self.public.new_page()
        self.page.set_default_timeout(15000);self.viewer.set_default_timeout(15000)

    def matches(self, lang, text):
        cfg = self.config['sections'][lang]
        self.viewer.goto(self.config['publicUrl'], wait_until='domcontentloaded')
        node = self.viewer.locator(cfg['publicText'])
        if node.count() != 1 or not node.is_visible():
            raise Stop('BLOCKED')
        # Renderer accepts only the small BBCode vocabulary used by the mirrors.
        expected = re.sub(r'\[/?(?:b|i|u|h[1-6])\]', '', text)
        if re.search(r'\[/?[a-z]', expected, re.I):
            raise Stop('BLOCKED')
        normalize = lambda value: ' '.join(value.replace('\u00a0', ' ').split())
        return normalize(node.inner_text()) == normalize(expected)

    def ready(self, lang):
        cfg = self.config['sections'][lang]
        self.page.goto(cfg['editUrl'], wait_until='domcontentloaded')
        if self.page.locator(self.config['guardSelector']).count():
            raise Stop('STEAM_GUARD')
        if '/login' in self.page.url or self.page.locator(self.config['loginSelector']).count():
            raise Stop('NEEDS_LOGIN')
        if self.page.url!=cfg['editUrl']:raise Stop('BLOCKED')
        for name in ['title', 'textarea', 'save']:
            node=self.page.locator(cfg[name])
            if node.count()!=1 or not node.is_visible() or not node.is_enabled():
                raise Stop('BLOCKED')
        if self.page.locator(cfg['title']).input_value() != cfg['titleText']:
            raise Stop('BLOCKED')

    def replace(self, lang, text,before_save):
        cfg = self.config['sections'][lang]
        self.page.locator(cfg['textarea']).fill(text)
        before_save()
        self.page.locator(cfg['save']).click()  # never create/delete a section


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    args = parser.parse_args()
    args.store.mkdir(parents=True, exist_ok=True)
    with (args.store/'runner.lock').open('rb') as runner_lock,(args.store/'steam-publisher.lock').open('a+b') as lock:
        fcntl.flock(runner_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        config = json.loads(args.config.read_text())
        if config.get('publishEnabled') is not True or config.get('selectorsVerified') is not True:
            atomic(args.store/'steam-status.json',dict(status='NEEDS_SETUP',message=MESSAGES['NEEDS_SETUP']))
            return
        if config['cdp'] != 'http://127.0.0.1:9222':
            raise ValueError('Only loopback CDP allowed')
        project = json.loads((args.root/'data/project.json').read_text(encoding='utf-8-sig'))['steamGuide']
        if config['publicUrl'] != project['url']:
            raise ValueError('Guide mismatch')
        from urllib.parse import urlsplit, parse_qs
        ids = []
        for lang in FILES:
            cfg = config['sections'][lang]
            url = urlsplit(cfg['editUrl'])
            query = parse_qs(url.query)
            if (url.scheme != 'https' or url.netloc != 'steamcommunity.com'
                    or url.path != '/sharedfiles/editguidesubsection/'
                    or query.get('id') != parse_qs(urlsplit(project['url']).query).get('id')
                    or not re.fullmatch(r'\d+', query.get('sectionid', [''])[0])
                    or cfg['titleText'] != project['sections'][lang]['title']):
                raise ValueError('Existing section mapping required')
            ids.append(query['sectionid'][0])
        if len(set(ids)) != 2:
            raise ValueError('Distinct sections required')
        approvals=[]
        for p in args.store.glob('steam-approval-*.json'):
            if p.is_symlink():continue
            try:approvals.append(json.loads(p.read_text()))
            except (OSError,ValueError):continue
        key=combined(texts(args.root))
        approvals = [a for a in approvals if approved(a,key,args.store)]
        if not approvals:
            atomic(args.store/'steam-status.json', dict(status='NEEDS_APPROVAL', message=MESSAGES['NEEDS_APPROVAL']))
            return
        from playwright.sync_api import sync_playwright
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.connect_over_cdp(config['cdp'])
                adapter = SteamBrowser(browser, config)
                try:
                    publish(args.root, args.store, max(approvals, key=lambda a: a.get('approvedAt', 0)), adapter)
                finally:
                    adapter.page.close()
                    adapter.public.close()
        except Exception:
            atomic(args.store/'steam-status.json', dict(status='NEEDS_LOGIN', message=MESSAGES['NEEDS_LOGIN']))


if __name__ == '__main__':
    try:
        main()
    except BlockingIOError:
        pass  # Existing publisher owns status; do not overwrite it.
    except Exception:
        # Configuration/launch failure must not leave an earlier COMPLETE visible.
        import sys
        try:
            store = Path(sys.argv[sys.argv.index('--store') + 1])
            atomic(store/'steam-status.json', dict(status='BLOCKED', message=MESSAGES['BLOCKED']))
        except Exception:
            pass
        raise SystemExit(1)
