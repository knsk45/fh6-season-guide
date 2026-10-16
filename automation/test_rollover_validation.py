"""Exercise the real PowerShell validator without HA configuration or network."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

PWSH = shutil.which('pwsh')

@unittest.skipUnless(PWSH, 'PowerShell is required for behavioral validation')
class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fh6-rollover-validation-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = Path(__file__).resolve().parents[1]
        for directory in ('data', 'reports/assets'):
            shutil.copytree(source/directory, self.root/directory)
        (self.root/'automation').mkdir()
        for script in (source/'automation').glob('*.ps1'):
            shutil.copyfile(script, self.root/'automation'/script.name)
        self.state_path = self.root/'data/current-season.json'
        self.original = self.state_path.read_bytes()
        self.state = json.loads(self.original)
        self.project_path = self.root/'data/project.json'
        self.project = json.loads(self.project_path.read_text(encoding='utf-8-sig'))
        self.config = self.root/self.project['notifications']['localConfigPath']
        self.assertFalse(self.config.exists())

    def invoke(self, script, *args):
        return subprocess.run([PWSH, '-NoProfile', '-File',
            str(self.root/'automation'/script), *args], cwd=self.root,
            capture_output=True, text=True, timeout=60)

    def test_full_validation_still_requires_operational_config(self):
        result = self.invoke('validate_season.ps1', '-SkipOutputs', '-AsJson')
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        errors = json.loads(result.stdout)['errors']
        self.assertIn('Home Assistant notification local config is missing', errors)

    def test_editorial_validation_succeeds_without_config(self):
        result = self.invoke('validate_season.ps1', '-SkipOutputs', '-ContentOnly')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('STRUCTURE_OK', result.stdout)
        self.assertFalse(self.config.exists())

    def test_invalid_content_is_still_rejected(self):
        self.state['season']['expectedCardCount'] += 1
        self.state_path.write_text(json.dumps(self.state))
        result = self.invoke('validate_season.ps1', '-SkipOutputs', '-ContentOnly', '-AsJson')
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(any('activities, found' in error for error in json.loads(result.stdout)['errors']))

    def test_editorial_validation_keeps_config_path_constraint(self):
        self.project['notifications']['localConfigPath'] = 'reports/not-a-secret.json'
        self.project_path.write_text(json.dumps(self.project))
        result = self.invoke('validate_season.ps1', '-SkipOutputs', '-ContentOnly', '-AsJson')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('project.notifications.localConfigPath must stay under ignored automation/runs/', json.loads(result.stdout)['errors'])

    def test_rollover_prepares_history_and_archive_without_config(self):
        self.state['season']['archiveFile'] = 'seasons/isolated-rollover-test.md'
        draft = self.root/'automation/new-season-input.json'
        draft.write_text(json.dumps(self.state))
        result = self.invoke('start_new_season.ps1', '-InputPath', str(draft))
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('ROLLOVER_OK', result.stdout)
        old = json.loads(self.original)
        history = self.root/'data/history'/(Path(old['season']['archiveFile']).stem+'.json')
        self.assertEqual(json.loads(history.read_text(encoding='utf-8-sig')), old)
        self.assertTrue((self.root/'seasons/isolated-rollover-test.md').is_file())
        self.assertEqual(json.loads(self.state_path.read_text(encoding='utf-8-sig')), self.state)
        self.assertFalse(self.config.exists())

    def candidate_fixture(self):
        work=self.root/'isolated-candidate'
        source=self.root/self.state['season']['assetsDirectory']
        self.state['season']['assetsDirectory']='reports/assets/candidate-season'
        shutil.copytree(source,work/self.state['season']['assetsDirectory'])
        (work/'data').mkdir(parents=True)
        candidate=work/'data/current-season.json'
        candidate.write_text(json.dumps(self.state))
        self.config.parent.mkdir(parents=True,exist_ok=True)
        self.config.write_text('{"testFixture":true}')
        return work,candidate

    def test_trusted_validator_reads_unpromoted_candidate_assets(self):
        work,candidate=self.candidate_fixture()
        old=self.invoke('validate_season.ps1','-StatePath',str(candidate),'-SkipOutputs','-AsJson')
        self.assertNotEqual(old.returncode,0)
        self.assertTrue(any('references missing asset:' in error for error in json.loads(old.stdout)['errors']))
        result=self.invoke('validate_season.ps1','-StatePath',str(candidate),'-SeasonAssetsBasePath',str(work),'-SkipOutputs','-AsJson')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertTrue(json.loads(result.stdout)['ok'])
        self.assertEqual(self.state_path.read_bytes(),self.original)

    def test_candidate_assets_do_not_disable_operational_config_check(self):
        work,candidate=self.candidate_fixture();self.config.unlink()
        result=self.invoke('validate_season.ps1','-StatePath',str(candidate),'-SeasonAssetsBasePath',str(work),'-SkipOutputs','-AsJson')
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Home Assistant notification local config is missing',json.loads(result.stdout)['errors'])

    def test_candidate_asset_override_requires_input_validation_mode(self):
        work,candidate=self.candidate_fixture()
        result=self.invoke('validate_season.ps1','-StatePath',str(candidate),'-SeasonAssetsBasePath',str(work))
        self.assertNotEqual(result.returncode,0)
        self.assertIn('SeasonAssetsBasePath requires SkipOutputs',result.stdout+result.stderr)

if __name__ == '__main__':
    unittest.main()
