"""Focused retries, safe rollover and canonical rollback; no real model calls."""
import contextlib,json,tempfile,unittest,os,pwd,shutil,subprocess
from pathlib import Path
from unittest.mock import Mock,patch
import test_recovery
runner=test_recovery.runner
recovery=test_recovery.recovery

class Tests(unittest.TestCase):
    def editor_fixture(self,folder,produce_at=None,invalid_first=False):
        root=Path(folder)/'repo';store=Path(folder)/'store'
        (root/'automation/server').mkdir(parents=True)
        (root/'automation/server/editor-prompt.md').write_text('Audit live evidence')
        (store/'inbox').mkdir(parents=True);(store/'source-snapshots.json').write_text('{}')
        calls=[]
        def process(*args,**kwargs):
            calls.append((args,kwargs))
            if produce_at and len(calls)>=produce_at:
                (kwargs['cwd']/'automation/editor-audit.json').write_text('{}')
            return Mock(returncode=0)
        return root,store,calls,process

    def test_missing_handoff_is_repaired_in_same_workspace(self):
        with tempfile.TemporaryDirectory() as d:
            root,store,calls,process=self.editor_fixture(d,2)
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner,'EDITOR',store/'editor'),patch.object(runner.subprocess,'run',return_value=Mock(returncode=0)),patch.object(runner.subprocess,'Popen',side_effect=process),patch.object(runner,'wait_editor') as wait,patch.object(runner,'validate_editor_handoff'):
                self.assertEqual(runner.editor(),store/'editor/work')
            self.assertEqual(len(calls),2);self.assertEqual(calls[0][1]['cwd'],calls[1][1]['cwd'])
            self.assertIn('SUPERVISOR:',calls[1][0][0][-1])
            self.assertEqual([c.kwargs['timeout'] for c in wait.call_args_list],[900,150])

    def test_invalid_audit_receives_concrete_feedback_then_revalidates(self):
        with tempfile.TemporaryDirectory() as d:
            root,store,calls,process=self.editor_fixture(d,1)
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner,'EDITOR',store/'editor'),patch.object(runner.subprocess,'run',return_value=Mock(returncode=0)),patch.object(runner.subprocess,'Popen',side_effect=process),patch.object(runner,'wait_editor'),patch.object(runner,'validate_editor_handoff',side_effect=[ValueError('Missing required source fixture'),None]):
                self.assertIsNotNone(runner.editor())
            self.assertEqual(len(calls),2)
            self.assertIn('Missing required source fixture',(store/'editor/work/supervisor-feedback.txt').read_text())

    def test_three_empty_results_never_fabricate_an_audit(self):
        with tempfile.TemporaryDirectory() as d:
            root,store,calls,process=self.editor_fixture(d)
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner,'EDITOR',store/'editor'),patch.object(runner.subprocess,'run',return_value=Mock(returncode=0)),patch.object(runner.subprocess,'Popen',side_effect=process),patch.object(runner,'wait_editor'):
                self.assertIsNone(runner.editor())
            self.assertEqual(len(calls),3)
            self.assertEqual(json.loads((store/'editor-status.json').read_text())['reasonCode'],'EDITOR_HANDOFF_INCOMPLETE')
            self.assertFalse((store/'editor/work/automation/editor-audit.json').exists())
            self.assertEqual(recovery.failure({'status':'BLOCKED'},{'status':'NO_AUDIT'},'old HTTP 503 timeout'),'AUDIT_INCOMPLETE')

    def rollover_fixture(self,d):
        root=Path(d)/'repo';work=Path(d)/'work'
        before={'season':{'archiveFile':'seasons/summer.md','assetsDirectory':'reports/assets/summer'},'activities':[]}
        after={'season':{'archiveFile':'seasons/autumn.md','assetsDirectory':'reports/assets/autumn'},'activities':[]}
        for path,value in [(root/'data/current-season.json',before),(work/'data/current-season.json',after),(work/'data/history/summer.json',before)]:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
        (root/'seasons').mkdir();(work/'seasons').mkdir()
        (root/'seasons/summer.md').write_text('old');(work/'seasons/summer.md').write_text('old');(work/'seasons/autumn.md').write_text('new')
        return root,work

    def test_rollover_adds_only_exact_old_state_and_new_archive(self):
        with tempfile.TemporaryDirectory() as d:
            root,work=self.rollover_fixture(d)
            with patch.object(runner,'ROOT',root):
                files=runner.safe_candidate(work)
                self.assertIn(work/'data/history/summer.json',files);self.assertIn(work/'seasons/autumn.md',files)
                (work/'seasons/summer.md').write_text('changed')
                with self.assertRaisesRegex(RuntimeError,'existing history'):runner.safe_candidate(work)

    def test_registration_failure_restores_state_and_retains_rejected_new_file(self):
        with tempfile.TemporaryDirectory() as d:
            root,work=self.rollover_fixture(d);store=Path(d)/'store';store.mkdir()
            before=(root/'data/current-season.json').read_bytes()
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner.shutil,'chown'),patch.object(runner,'guard',side_effect=RuntimeError('audit rejected')):
                with self.assertRaises(RuntimeError):runner.promote_candidate(work,[work/'data/current-season.json',work/'seasons/autumn.md'])
            self.assertEqual((root/'data/current-season.json').read_bytes(),before)
            self.assertFalse((root/'seasons/autumn.md').exists())
            self.assertEqual(len(list(store.glob('before-editor-*/rejected/seasons/autumn.md'))),1)

    def test_monthly_visual_cannot_be_dropped(self):
        with tempfile.TemporaryDirectory() as d:
            root,work=self.rollover_fixture(d)
            before=json.loads((root/'data/current-season.json').read_text())
            after=json.loads((work/'data/current-season.json').read_text())
            activity={'id':'monthly','kind':'monthly_rivals','title':'same event','visual':{'sourceImage':'reports/assets/raw.png','image':'reports/assets/tile.png'}}
            before['activities']=[activity];after['activities']=[dict(activity,visual=None)]
            before['season'].update(seriesNumber=6,startAt='2026-10-08')
            after['season'].update(seriesNumber=6,startAt='2026-10-15')
            (root/'data/current-season.json').write_text(json.dumps(before));(work/'data/current-season.json').write_text(json.dumps(after));(work/'data/history/summer.json').write_text(json.dumps(before))
            with patch.object(runner,'ROOT',root):
                with self.assertRaisesRegex(RuntimeError,'Monthly visual'):runner.safe_candidate(work)

    def test_state_symlink_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as d:
            root,work=self.rollover_fixture(d)
            (work/'data/current-season.json').unlink()
            (work/'data/current-season.json').symlink_to(root/'data/current-season.json')
            with patch.object(runner,'ROOT',root):
                with self.assertRaisesRegex(RuntimeError,'escapes workspace'):runner.safe_candidate(work)

    def monthly_fixture(self, d):
        root, work = self.rollover_fixture(d)
        before = json.loads((root/'data/current-season.json').read_text())
        after = json.loads((work/'data/current-season.json').read_text())
        activity = {'id':'monthly', 'kind':'monthly_rivals', 'title':'same event',
                    'visual':{'sourceImage':'original.png', 'image':'tile.png'}}
        before['activities'] = [activity]; after['activities'] = [activity]
        before['season'].update(seriesNumber=6, startAt='2026-10-08')
        after['season'].update(seriesNumber=6, startAt='2026-10-15')
        (root/'data/current-season.json').write_text(json.dumps(before))
        (work/'data/current-season.json').write_text(json.dumps(after))
        (work/'data/history/summer.json').write_text(json.dumps(before))
        for base, state in ((root,before),(work,after)):
            folder = base/state['season']['assetsDirectory']; folder.mkdir(parents=True)
            (folder/'original.png').write_bytes(b'original screenshot fixture')
            (folder/'tile.png').write_bytes(b'prepared crop fixture')
        return root, work

    def test_identical_monthly_images_resolve_relative_to_each_season_assets(self):
        with tempfile.TemporaryDirectory() as d:
            root, work = self.monthly_fixture(d)
            with patch.object(runner,'ROOT',root):
                self.assertIn(work/'seasons/autumn.md',runner.safe_candidate(work))

    def test_changed_monthly_original_or_crop_is_rejected(self):
        for name in ('original.png','tile.png'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
                root, work = self.monthly_fixture(d)
                (work/'reports/assets/autumn'/name).write_bytes(b'changed')
                with patch.object(runner,'ROOT',root):
                    with self.assertRaisesRegex(RuntimeError,'bytes changed'):runner.safe_candidate(work)

    def test_monthly_image_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root, work = self.monthly_fixture(d)
            target = work/'reports/assets/autumn/tile.png'
            target.unlink(); target.symlink_to(root/'reports/assets/summer/tile.png')
            with patch.object(runner,'ROOT',root):
                with self.assertRaises(RuntimeError):runner.safe_candidate(work)

    def test_candidate_validation_reads_candidate_assets_using_trusted_script(self):
        with tempfile.TemporaryDirectory() as d:
            root,work=self.rollover_fixture(d);store=Path(d)/'store';store.mkdir()
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner.subprocess,'run',return_value=Mock(returncode=0,stdout='{}')) as process:
                runner.validate_candidate_state(work)
            args=process.call_args.args[0]
            self.assertEqual(args[args.index('-File')+1],str(root/'automation/validate_season.ps1'))
            self.assertEqual(args[args.index('-SeasonAssetsBasePath')+1],str(work))
            self.assertNotIn('-ContentOnly',args)
            self.assertIn('-AsJson',args)

    def test_candidate_validation_retains_concrete_errors(self):
        with tempfile.TemporaryDirectory() as d:
            store=Path(d)
            output=json.dumps({'errors':['missing original fixture']})
            with patch.object(runner,'STORE',store),patch.object(runner.subprocess,'run',return_value=Mock(returncode=1,stdout=output)):
                with self.assertRaisesRegex(RuntimeError,'missing original fixture'):runner.validate_candidate_state(store)

    def reusable_fixture(self,d):
        root,store,calls,process=self.editor_fixture(d)
        (root/'data').mkdir();(root/'data/current-season.json').write_text('{}')
        work=store/'editor/work';work.mkdir(parents=True)
        (work/'retained-evidence.txt').write_text('keep')
        (store/'editor-status.json').write_text(json.dumps({'status':'FINISHED','at':'2026-10-16T12:00:00+07:00'}))
        (store/'review-required.json').write_text(json.dumps({'stateSha256':runner.digest(root/'data/current-season.json'),'at':'2026-10-16T12:00:01+07:00'}))
        return root,store,work

    def test_fresh_finished_candidate_resumes_without_model_or_workspace_rebuild(self):
        with tempfile.TemporaryDirectory() as d:
            root,store,work=self.reusable_fixture(d)
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner,'EDITOR',store/'editor'),patch.object(runner,'validate_editor_handoff') as validate,patch.object(runner.subprocess,'Popen') as model:
                self.assertEqual(runner.editor(),work)
                model.assert_not_called();validate.assert_called_once_with(work)
            self.assertTrue((work/'retained-evidence.txt').is_file())

    def test_changed_base_or_expired_audit_prevents_candidate_reuse(self):
        with tempfile.TemporaryDirectory() as d:
            root,store,work=self.reusable_fixture(d)
            status={'status':'FINISHED','at':'2026-10-16T12:00:00+07:00'}
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner,'validate_editor_handoff',side_effect=RuntimeError('expired audit')):
                self.assertFalse(runner.reusable_editor_candidate(work,status))
            (root/'data/current-season.json').write_text('{"newer":true}')
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner,'validate_editor_handoff') as validate:
                self.assertFalse(runner.reusable_editor_candidate(work,status));validate.assert_not_called()

    @unittest.skipUnless(os.geteuid()==0 and shutil.which('runuser'),'Requires root for real unprivileged access test')
    def test_published_monthly_images_are_readable_by_unprivileged_publisher(self):
        user=pwd.getpwnam('daemon')
        mapping=Path('/proc/self/uid_map')
        if mapping.exists() and not any(int(row.split()[0])<=user.pw_uid<int(row.split()[0])+int(row.split()[2]) for row in mapping.read_text().splitlines()):
            self.skipTest('Unprivileged UID is not mapped in this test environment')
        for stale in (False,True):
            with self.subTest(stale=stale),tempfile.TemporaryDirectory() as d:
                Path(d).chmod(0o755)
                root,work=self.monthly_fixture(d);store=Path(d)/'store';store.mkdir()
                destination=root/'reports/assets/autumn'
                if stale:destination.mkdir(mode=0o750)
                files=[work/'data/current-season.json',work/'reports/assets/autumn/original.png',work/'reports/assets/autumn/tile.png']
                def ownership(path,user=None,group=None):
                    os.chown(path,pwd.getpwnam('daemon').pw_uid,pwd.getpwnam('daemon').pw_gid)
                def register(*args):
                    result=subprocess.run(['runuser','-u','daemon','--','python3','-c',
                        'from pathlib import Path;import sys;assert Path(sys.argv[1]).read_bytes()==b"prepared crop fixture"',
                        str(destination/'tile.png')],capture_output=True,text=True)
                    self.assertEqual(result.returncode,0,result.stderr)
                with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner.shutil,'chown',side_effect=ownership),patch.object(runner,'guard',side_effect=register):
                    runner.promote_candidate(work,files)
                self.assertEqual(destination.stat().st_uid,user.pw_uid)

    def test_rollover_parent_ownership_is_prepared_before_audit_registration(self):
        with tempfile.TemporaryDirectory() as d:
            root,work=self.monthly_fixture(d);store=Path(d)/'store';store.mkdir()
            destination=root/'reports/assets/autumn'
            destination.mkdir(mode=0o750)
            files=[work/'data/current-season.json',work/'reports/assets/autumn/tile.png']
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner.shutil,'chown') as chown,patch.object(runner,'guard'):
                runner.promote_candidate(work,files)
            self.assertTrue(any(call.args==(destination,) and call.kwargs=={'user':'fh6','group':'fh6'} for call in chown.call_args_list))
            self.assertFalse(any(call.args==(root/'automation',) for call in chown.call_args_list))

if __name__=='__main__':unittest.main()
