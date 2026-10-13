"""Regression for publisher denied access to a successful editorial handoff."""
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name+'.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

repair = module('repair_editor_access')
with patch.dict(os.environ, {'FH6_ROOT': str(Path(__file__).resolve().parents[2])}):
    runner = module('runner')

class RepairTests(unittest.TestCase):
    def test_exact_deployed_version_and_idempotent_repair(self):
        current = Path(__file__).with_name('runner.py').read_bytes()
        original = current.decode().replace(repair.HELPER, '', 1).replace(
            '                grant_candidate_read_access(work)\n', '', 1).encode()
        self.assertEqual(hashlib.sha256(original).hexdigest(), repair.ORIGINAL)
        self.assertEqual(repair.patched(original), current)
        self.assertEqual(repair.patched(current), current)

    def test_unknown_version_fails_without_replacement(self):
        for raw in [b'', b'unknown deployment', Path(__file__).with_name('runner.py').read_bytes()+b'\n']:
            with self.assertRaises(RuntimeError):
                repair.patched(raw)

    def test_workspace_symlink_rejected_before_any_acl(self):
        with tempfile.TemporaryDirectory() as folder:
            editor = Path(folder)/'editor'
            editor.mkdir()
            elsewhere = Path(folder)/'private'
            elsewhere.mkdir()
            (editor/'work').symlink_to(elsewhere, target_is_directory=True)
            with patch.object(runner, 'EDITOR', editor), patch.object(runner.subprocess, 'run') as run:
                with self.assertRaises(RuntimeError):
                    runner.grant_candidate_read_access(editor/'work')
                run.assert_not_called()

    def test_real_acl_handoff_is_read_only_and_does_not_follow_symlinks(self):
        if os.name != 'posix' or os.geteuid() != 0 or not shutil.which('setfacl'):
            self.skipTest('Requires Linux root, acl package and server users')
        import pwd
        try:
            publisher = pwd.getpwnam('fh6')
            editor_user = pwd.getpwnam('fh6-editor')
        except KeyError:
            self.skipTest('Requires dedicated server users')
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            editor = root/'editor'
            work = editor/'work'
            work.mkdir(parents=True)
            state = work/'state.json'
            state.write_text('public synthetic fixture')
            private = root/'private.json'
            private.write_text('private synthetic fixture')
            private.chmod(0o600)
            (work/'outside').symlink_to(private)
            for path in [editor, work, state]:
                os.chown(path, editor_user.pw_uid, editor_user.pw_gid)
                path.chmod(0o700 if path.is_dir() else 0o600)
            subprocess.run(['setfacl','-m','u:fh6:--x',str(root)], check=True)
            def access(flag, path):
                return subprocess.run(['runuser','-u',publisher.pw_name,'--','test',flag,str(path)]).returncode == 0
            self.assertFalse(access('-r', state))
            with patch.object(runner, 'EDITOR', editor):
                runner.grant_candidate_read_access(work)
            self.assertTrue(access('-r', state))
            self.assertFalse(access('-w', state))
            self.assertFalse(access('-w', work))
            self.assertFalse(access('-r', editor))
            self.assertFalse(access('-r', private))
            self.assertFalse(access('-r', work/'outside'))
            # A subsequent editor rewrite with restrictive permissions must work too.
            state.unlink()
            state.write_text('new synthetic fixture')
            os.chown(state, editor_user.pw_uid, editor_user.pw_gid)
            state.chmod(0o600)
            with patch.object(runner, 'EDITOR', editor):
                runner.grant_candidate_read_access(work)
            self.assertTrue(access('-r', state))
            self.assertFalse(access('-w', state))

if __name__ == '__main__':
    unittest.main()
