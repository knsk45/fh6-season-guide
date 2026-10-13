import base64
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('installer',Path(__file__).with_name('install_recovery.py'))
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)

class InstallerTests(unittest.TestCase):
    def item(self,raw,previous=(),systemd=False):
        return dict(data=base64.b64encode(raw).decode(),sha256=installer.digest(raw),previous=list(previous),systemd=systemd)
    def test_unknown_version_rejects_whole_plan_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'old.py').write_text('owner modification')
            before=(root/'old.py').read_bytes()
            manifest={'new.py':self.item(b'NEW=1\n'),'old.py':self.item(b'NEW=2\n')}
            with self.assertRaises(RuntimeError):installer.prepare(root,root/'units',manifest)
            self.assertFalse((root/'new.py').exists())
            self.assertEqual((root/'old.py').read_bytes(),before)
    def test_pin_syntax_and_known_version_checks(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'old.py').write_bytes(b'OLD=1\n')
            manifest={'old.py':self.item(b'NEW=2\n',[installer.digest(b'OLD=1\n')])}
            self.assertEqual(installer.prepare(root,root/'units',manifest)[0][2],b'OLD=1\n')
            manifest['old.py']['sha256']='0'*64
            with self.assertRaises(RuntimeError):installer.prepare(root,root/'units',manifest)
            with self.assertRaises(SyntaxError):installer.prepare(root,root/'units',{'bad.py':self.item(b'if\n')})
    def test_all_bundled_payloads_are_pinned_and_compile(self):
        self.assertTrue(installer.MANIFEST)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            plans=installer.prepare(root,root/'units')
            self.assertEqual(len(plans),len(installer.MANIFEST))
            self.assertFalse(any(p.exists() for p,_,_,_ in plans))

if __name__=='__main__':unittest.main()
