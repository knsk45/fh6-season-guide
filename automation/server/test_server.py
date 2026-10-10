import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
import tempfile

def module(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

ui=module('phone_ui')

class Tests(unittest.TestCase):
    def test_only_image_upload_types(self):
        self.assertEqual(ui.mime(b'\x89PNG\r\n\x1a\nfixture'),'.png')
        self.assertEqual(ui.mime(b'\xff\xd8\xfffixture'),'.jpg')
        with self.assertRaises(ValueError):ui.mime(b'<script>evil</script>')
    def test_approval_binds_both_locales(self):
        self.assertNotEqual(ui.fingerprint('ru\nen'),ui.fingerprint('ru\nchanged'))

if __name__=='__main__':unittest.main()
