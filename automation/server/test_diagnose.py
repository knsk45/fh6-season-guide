import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('diagnose', Path(__file__).with_name('diagnose.py'))
diagnose = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnose)


class SnapshotTests(unittest.TestCase):
    def test_sensitive_and_unexpected_fields_are_not_exported(self):
        secret = 'SYNTHETIC_PRIVATE_VALUE'
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            def write(name, data):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(data))
            write('data/current-season.json', {'season': {'season': secret, 'endAt': secret},
                                             'lastContentUpdate': secret, 'activities': [], 'token': secret})
            write('automation/runs/refresh/active.json', {'status': secret, 'nextAction': secret,
                  'blockers': [secret], 'steps': {'audit': {'status': secret, 'log': secret}, secret: {'status': secret}},
                  'notification': {'token': secret}})
            write('editor-status.json', {'status': secret, 'error': secret})
            with patch.object(diagnose, 'probe', return_value=(1, secret)):
                report = diagnose.snapshot(root, root)
            self.assertNotIn(secret, json.dumps(report))
            self.assertEqual(report['guardStatus'], 'UNKNOWN')
            self.assertEqual(report['steps'], {'audit': 'UNKNOWN'})
            self.assertIsNone(report['lastContentUpdate'])

    def test_snapshot_does_not_write_or_invoke_pipeline(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / 'data/current-season.json'
            path.parent.mkdir()
            path.write_text(json.dumps({'season': {'season': 'summer', 'endAt': '2026-10-15T21:30:00+07:00'},
                                        'lastContentUpdate': '2026-10-10T06:00:53+07:00', 'activities': [{}]}))
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with patch.object(diagnose, 'probe', return_value=(0, 'active')) as probe:
                report = diagnose.snapshot(root, root)
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before, after)
            self.assertEqual(report['activityCount'], 1)
            for call in probe.call_args_list:
                argv = call.args[0]
                self.assertTrue(argv[0] in {'git', 'systemctl', 'runuser'})
                self.assertNotIn('exec', argv)
                self.assertNotIn('start', argv)
                self.assertNotIn('refresh_guard.py', ' '.join(argv))


if __name__ == '__main__':
    unittest.main()
