import json
import tempfile
import time
import unittest
from unittest.mock import patch
from pathlib import Path
import steam_publish as worker


class Browser:
    def __init__(self):
        self.public = {}
        self.calls = []
        self.fail = None
        self.crash = False

    def matches(self, lang, text):
        return self.public.get(lang) == text

    def ready(self, lang):
        if lang == self.fail:
            raise worker.Stop('STEAM_GUARD')

    def replace(self, lang, text,before_save):
        before_save()
        self.calls.append(lang)
        self.public[lang] = text
        if self.crash:
            raise RuntimeError('private browser detail')


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'repo'
        self.store = Path(self.tmp.name)/'store'
        (self.root/'reports').mkdir(parents=True)
        (self.root/'data').mkdir()
        self.store.mkdir()
        for lang, name in worker.FILES.items():
            (self.root/'reports'/name).write_text('[b]'+lang+'[/b]')
        project = dict(steamGuide=dict(url='https://steamcommunity.com/sharedfiles/filedetails/?id=1', sections={
            lang: dict(title=lang, publicationStatePath=f'automation/runs/{lang}.json') for lang in worker.FILES}))
        (self.root/'data/project.json').write_text(json.dumps(project))
        (self.root/'data/current-season.json').write_text(json.dumps(dict(lastContentUpdate='fixture')))
        self.approval = dict(action='replace-current-ru-en', status='AWAITING_BROWSER_PUBLICATION',
                             sha256=worker.combined(worker.texts(self.root)), approvedAt=time.time())
        self.browser = Browser()
        audit=patch.object(worker,'fresh_audit',return_value=True);audit.start();self.addCleanup(audit.stop)

    def run_worker(self):
        return worker.publish(self.root, self.store, self.approval, self.browser)

    def test_success_and_replay_never_resubmits(self):
        self.assertEqual(self.run_worker()['status'], 'COMPLETE')
        self.assertEqual(self.run_worker()['status'], 'COMPLETE')
        self.assertEqual(self.browser.calls, ['ru', 'en'])
        for lang in worker.FILES:
            self.assertTrue((self.root/f'automation/runs/{lang}.json').exists())

    def test_stale_and_expired_approval(self):
        self.approval['sha256'] = 'bad'
        self.assertEqual(self.run_worker()['status'], 'STALE_APPROVAL')
        self.assertEqual(self.browser.calls, [])
        self.approval['sha256'] = worker.combined(worker.texts(self.root))
        self.approval['approvedAt'] -= 86401
        self.assertEqual(self.run_worker()['status'], 'STALE_APPROVAL')

    def test_partial_guard_and_resume(self):
        self.browser.fail = 'en'
        self.assertEqual(self.run_worker()['status'], 'STEAM_GUARD')
        self.assertFalse((self.root/'automation/runs/ru.json').exists())
        self.browser.fail = None
        self.assertEqual(self.run_worker()['status'], 'COMPLETE')
        self.assertEqual(self.browser.calls, ['ru', 'en'])

    def test_crash_after_remote_save_recovers_without_duplicate(self):
        self.browser.crash = True
        self.assertEqual(self.run_worker()['status'], 'UNCERTAIN')
        self.browser.crash = False
        self.assertEqual(self.run_worker()['status'], 'COMPLETE')
        self.assertEqual(self.browser.calls, ['ru', 'en'])

    def test_unknown_submit_blocks_retry(self):
        def fail(lang, text,before_save):
            before_save()
            self.browser.calls.append(lang)
            raise RuntimeError('private fixture')
        self.browser.replace = fail
        self.run_worker()
        self.assertEqual(self.run_worker()['status'], 'UNCERTAIN')
        self.assertEqual(self.browser.calls, ['ru'])
        self.assertNotIn('private fixture', (self.store/'steam-status.json').read_text())

    def test_changed_between_locales(self):
        original = self.browser.replace
        def replace(lang, text,before_save):
            original(lang, text,before_save)
            (self.root/'reports'/worker.FILES['en']).write_text('changed')
        self.browser.replace = replace
        self.assertEqual(self.run_worker()['status'], 'STALE_APPROVAL')
        self.assertEqual(self.browser.calls, ['ru'])

    def test_login_stops_before_submit(self):
        def login(lang):
            raise worker.Stop('NEEDS_LOGIN')
        self.browser.ready = login
        self.assertEqual(self.run_worker()['status'], 'NEEDS_LOGIN')
        self.assertEqual(self.browser.calls, [])

    def test_oversized_text_is_blocked(self):
        (self.root/'reports'/worker.FILES['en']).write_text('a'*4801)
        self.approval['sha256'] = worker.combined(worker.texts(self.root))
        self.assertEqual(self.run_worker()['status'], 'BLOCKED')
        self.assertEqual(self.browser.calls, [])

    def test_final_public_check_required(self):
        calls = []
        original = self.browser.matches
        def matches(lang, text):
            calls.append(lang)
            return False if len(calls) == 5 else original(lang, text)
        self.browser.matches = matches
        self.assertEqual(self.run_worker()['status'], 'UNCERTAIN')
        self.assertFalse((self.root/'automation/runs/ru.json').exists())

    def standing(self,enabled=True,version=1):
        (self.store/'steam-consent.json').write_text(json.dumps(dict(enabled=enabled,updatedAt=version)))
        self.approval.update(automatic=True,standingConsentAt=1)

    def test_disabled_or_new_consent_version_blocks(self):
        self.standing(False)
        self.assertEqual(self.run_worker()['status'],'STALE_APPROVAL')
        self.standing(True,2)
        self.assertEqual(self.run_worker()['status'],'STALE_APPROVAL')
        self.assertEqual(self.browser.calls,[])

    def test_switch_off_between_locales_blocks_second_write(self):
        self.standing();original=self.browser.replace
        def replace(lang,text,before_save):
            original(lang,text,before_save)
            self.standing(False)
        self.browser.replace=replace
        self.assertEqual(self.run_worker()['status'],'NEEDS_APPROVAL')
        self.assertEqual(self.browser.calls,['ru'])

    def test_switch_off_after_fill_before_save_blocks_write(self):
        self.standing()
        def replace(lang,text,before_save):
            self.standing(False);before_save()
            self.browser.calls.append(lang)
        self.browser.replace=replace
        self.assertEqual(self.run_worker()['status'],'NEEDS_APPROVAL')
        self.assertEqual(self.browser.calls,[])

    def test_fresh_audit_required(self):
        with patch.object(worker,'fresh_audit',return_value=False):
            self.assertEqual(self.run_worker()['status'],'AUDIT_REQUIRED')
        self.assertEqual(self.browser.calls,[])

    def test_audit_expires_during_browser_ready(self):
        with patch.object(worker,'fresh_audit',side_effect=[True,False]):
            self.assertEqual(self.run_worker()['status'],'AUDIT_REQUIRED')
        self.assertEqual(self.browser.calls,[])

    def test_journal_fsynced_before_save(self):
        original=self.browser.replace
        def replace(lang,text,before_save):
            before_save()
            journal=self.store/'steam-publication'/(self.approval['sha256']+'.json')
            self.assertEqual(json.loads(journal.read_text())['sections'][lang],'SUBMITTING')
            original(lang,text,lambda:None)
        self.browser.replace=replace
        self.assertEqual(self.run_worker()['status'],'COMPLETE')

    def test_bad_second_baseline_path_does_not_write_first(self):
        file=self.root/'data/project.json';project=json.loads(file.read_text())
        project['steamGuide']['sections']['en']['publicationStatePath']='outside.json';file.write_text(json.dumps(project))
        self.assertEqual(self.run_worker()['status'],'BLOCKED')
        self.assertFalse((self.root/'automation/runs/ru.json').exists())


if __name__ == '__main__':
    unittest.main()
