import copy
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

import configure_steam_browser as setup
from stage_steam_publish import CONFIG


class Tests(unittest.TestCase):
    def setUp(self):
        self.config = copy.deepcopy(CONFIG)
        self.project = {'steamGuide': {'url': CONFIG['publicUrl'], 'sections': {
            lang: {'title': CONFIG['sections'][lang]['titleText']} for lang in setup.SECTION_IDS}}}
        self.result = dict(sections={lang: dict(editorVerified=True, saveVerified=True,
            publicMatchesCurrent=False, generatedCharacters=100) for lang in setup.SECTION_IDS},
            consentEnabled=False, freshAuditAccepted=False)

    def test_disabled_candidate_preserves_existing_guide_and_public_mapping(self):
        value = setup.candidate(self.config, self.project)
        self.assertIs(value['publishEnabled'], False)
        self.assertIs(value['selectorsVerified'], False)
        self.assertEqual(value['sections']['en']['publicText'], CONFIG['sections']['en']['publicText'])
        self.assertEqual(value['sections']['ru']['save'], setup.SAVE)
        self.assertEqual(self.config['sections']['ru']['save'], 'UNVERIFIED_SAVE_SELECTOR')

    def test_enabled_or_different_section_is_rejected(self):
        self.config['publishEnabled'] = True
        with self.assertRaises(ValueError): setup.candidate(self.config, self.project)
        self.config['publishEnabled'] = False
        self.config['sections']['en']['editUrl'] = self.config['sections']['ru']['editUrl']
        with self.assertRaises(ValueError): setup.candidate(self.config, self.project)

    def test_missing_editor_or_unknown_public_check_is_rejected(self):
        for key in ('editorVerified', 'saveVerified', 'publicMatchesCurrent'):
            value = copy.deepcopy(self.result)
            value['sections']['en'][key] = None
            with self.subTest(key=key), self.assertRaises(ValueError): setup.verified(value)

    def test_empty_oversized_or_boolean_length_is_rejected(self):
        for count in (0, 4801, True):
            self.result['sections']['ru']['generatedCharacters'] = count
            with self.subTest(count=count), self.assertRaises(ValueError): setup.verified(self.result)

    def test_diagnostics_exclude_exception_text_and_unknown_fields(self):
        with patch.multiple(setup, PHASE='RU_EDITOR', DETAILS={'saveCount': 0}):
            value = setup.diagnostic(RuntimeError('PRIVATE_COOKIE_OR_URL'))
        value['private'] = 'PRIVATE_COOKIE_OR_URL'
        value['details'].update(cookie='PRIVATE_COOKIE', title='PRIVATE_ACCOUNT')
        safe = setup.safe_diagnostic(value)
        self.assertEqual(safe['details'], {'saveCount': 0})
        self.assertNotIn('PRIVATE', json.dumps(safe))
        self.assertIsNone(setup.safe_diagnostic(dict(phase='PRIVATE_URL', errorType='Error', status='BLOCKED')))

    def run_setup(self, child_success):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); root = base/'repo'; store = base/'store'
            (root/'data').mkdir(parents=True); store.mkdir(); (store/'runner.lock').touch()
            (root/'data/project.json').write_text(json.dumps(self.project))
            config = base/'config.json'; original = json.dumps(self.config).encode(); config.write_bytes(original)
            source = base/'setup.py'; source.write_text('# protected fixture')
            def run(args, **kwargs):
                if args[0] == 'systemctl': return SimpleNamespace(returncode=1)
                self.assertEqual(args[:4], ['runuser', '-u', 'fh6', '--'])
                proposed = json.loads(kwargs['input'])
                self.assertIs(proposed['publishEnabled'], False)
                return SimpleNamespace(returncode=0 if child_success else 1,
                                       stdout=json.dumps(self.result), stderr='PRIVATE_BROWSER_DETAIL')
            with patch.multiple(setup, ROOT=root, STORE=store, CONFIG=config, __file__=str(source)), \
                 patch.object(setup.sys, 'argv', [str(source)]), \
                 patch.object(setup.pwd, 'getpwnam', return_value=SimpleNamespace(pw_gid=0)), \
                 patch.object(setup.subprocess, 'run', side_effect=run):
                if child_success:
                    setup.main()
                    value = json.loads(config.read_bytes())
                    self.assertIs(value['selectorsVerified'], True)
                    self.assertIs(value['publishEnabled'], False)
                    self.assertEqual(config.stat().st_mode & 0o777, 0o640)
                    backups = list((store/'repairs').glob('*/steam-browser.json'))
                    self.assertEqual(len(backups), 1)
                    self.assertEqual(backups[0].read_bytes(), original)
                else:
                    with self.assertRaises(RuntimeError): setup.main()
                    self.assertEqual(config.read_bytes(), original)
                    self.assertFalse((store/'repairs').exists())

    def test_browser_failure_preserves_configuration_without_backup_or_write(self):
        self.run_setup(False)

    def test_success_backs_up_and_saves_disabled_configuration(self):
        self.run_setup(True)


if __name__ == '__main__': unittest.main()
