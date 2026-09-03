"""Compatibility and negative tests in an isolated copy; no network or publication."""
import copy
import contextlib
import io
import json
import re
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import build_portable_report as b

class PortableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='fh6-portable-tests-')
        cls.root = Path(cls.temp.name)
        source = Path(__file__).resolve().parents[1]
        for directory in ['data', 'reports/assets']:
            shutil.copytree(source/directory, cls.root/directory)
        for name in b.CHAIN + ['reports/artifact.json','reports/current-week.html',
            'automation/send_home_assistant_notification.ps1','automation/collect_publication_metrics.ps1',
            'automation/mark_steam_guide_published.ps1','automation/check_steam_guide.ps1']:
            target=cls.root/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source/name,target)
        cls.state=b.read(cls.root/'data/current-season.json')
        cls.artifact=b.read(cls.root/'reports/artifact.json')
        cls.project=b.read(cls.root/'data/project.json')
        # Validator checks existence only. Never copy credentials or invoke HA in tests.
        b.atomic_json(cls.root/cls.project['notifications']['localConfigPath'], {'testFixture':True})
        cls.html=(cls.root/'reports/current-week.html').read_text(encoding='utf-8')
        cls.receipt=cls.root/'automation/runs/test/receipt.json'
        b.build(cls.root,cls.receipt)

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_real_build_preserves_exact_existing_html(self):
        self.assertEqual((self.root/'reports/current-week.html').read_text(encoding='utf-8'),self.html)
        self.assertEqual(b.verify_receipt(self.root,self.receipt)['cards'],len(self.state['activities']))

    def test_real_zip_contains_html_and_all_local_assets(self):
        r=b.read(self.receipt)
        with zipfile.ZipFile(self.root/r['zipPath']) as z:
            self.assertIn('current-week.html',z.namelist())
            self.assertIn(self.project['branding']['faviconPng'].removeprefix('reports/'),z.namelist())
            self.assertEqual(set(z.namelist()),set(r['files']))

    def bad_artifact(self,modify):
        artifact=copy.deepcopy(self.artifact);modify(artifact)
        with self.assertRaises(ValueError):b.validate_artifact(self.root,self.state,artifact)

    def test_missing_card_rejected(self):self.bad_artifact(lambda a:a['manifest']['blocks'].pop())
    def test_reordered_cards_rejected(self):self.bad_artifact(lambda a:a['manifest']['blocks'].reverse())
    def test_stale_timestamp_rejected(self):self.bad_artifact(lambda a:a['snapshot'].update(generatedAt='2020-01-01T00:00:00+00:00'))
    def test_lost_open_items_rejected(self):self.bad_artifact(lambda a:a['snapshot'].update(accessIssues=['incorrect evidence list']))
    def test_unknown_block_rejected(self):self.bad_artifact(lambda a:a['manifest']['blocks'][0].update(type='chart'))
    def test_forged_card_text_rejected(self):
        self.bad_artifact(lambda a:a['manifest']['blocks'][0].update(body=a['manifest']['blocks'][0]['body'].replace('<h2>','<h2>FORGED ')))
    def test_embedded_image_different_from_disk_rejected(self):
        def corrupt_image(artifact):
            block = artifact['manifest']['blocks'][0]
            body, changed = re.subn(r'(data:image/(?:jpeg|png|webp);base64,)', r'\1AAAA', block['body'], count=1)
            self.assertEqual(changed, 1, 'The negative test must actually corrupt an image, regardless of season format')
            block['body'] = body
        self.bad_artifact(corrupt_image)
    def test_javascript_link_rejected(self):
        self.bad_artifact(lambda a:a['manifest']['blocks'][0].update(body=a['manifest']['blocks'][0]['body'].replace('https://forza.net/fh6playlists','javascript:alert(1)')))
    def test_script_injection_rejected(self):
        self.bad_artifact(lambda a:a['manifest']['blocks'][0].update(body=a['manifest']['blocks'][0]['body']+'<script>alert(1)</script>'))
    def test_event_handler_rejected(self):
        self.bad_artifact(lambda a:a['manifest']['blocks'][0].update(body=a['manifest']['blocks'][0]['body'].replace('<img ','<img onerror="alert(1)" ',1)))
    def test_traversal_rejected(self):
        with self.assertRaises(ValueError):b.safe_path(self.root,'../outside.txt')
    def test_missing_favicon_rejected(self):
        bad=self.html.replace('rel="icon"','rel="unused"')
        with self.assertRaises(ValueError):b.validate_html(self.root,bad,self.state,self.artifact,self.project)
    def test_public_content_change_rejected(self):
        bad=self.html.replace('<h2>','<h2>FORGED ')
        with self.assertRaises(ValueError):b.validate_html(self.root,bad,self.state,self.artifact,self.project)
    def test_receipt_missing_validation_rejected(self):
        r=b.read(self.receipt);r['validation']='skipped'
        target=self.receipt.with_name('bad.json');b.atomic_json(target,r)
        with self.assertRaises(ValueError):b.verify_receipt(self.root,target)
    def test_changed_package_rejected(self):
        r=b.read(self.receipt);original=self.root/r['zipPath']
        bad=original.with_name('changed.zip');shutil.copyfile(original,bad)
        with zipfile.ZipFile(bad,'a') as z:z.writestr('unexpected.txt','bad')
        r.update(zipPath=bad.relative_to(self.root).as_posix(),zipSha256=b.sha(bad))
        target=self.receipt.with_name('bad-package.json');b.atomic_json(target,r)
        with self.assertRaises(ValueError):b.verify_receipt(self.root,target)
    def test_failure_does_not_overwrite_public_html(self):
        before=b.sha(self.root/'reports/current-week.html')
        with patch.object(b,'validate_artifact',side_effect=ValueError('bad input')):
            with self.assertRaises(ValueError):b.build(self.root,self.receipt)
        self.assertEqual(before,b.sha(self.root/'reports/current-week.html'))

if __name__=='__main__':unittest.main()
