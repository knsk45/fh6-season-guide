import copy
import importlib.util
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from datetime import datetime, timedelta

spec = importlib.util.spec_from_file_location('guard', Path(__file__).with_name('refresh_guard.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.guard = g.Guard(self.root)
        self.end = (datetime.now(g.ZONE) + timedelta(days=1)).isoformat()
        g.atomic(self.root/'data/current-season.json', {'season': {'endAt': self.end, 'assetsDirectory': 'reports/assets'},
            'lastContentUpdate': g.now(), 'activities': [{'id':'daily','visual':{'image':'daily.jpg'}}], 'openItems':[]})
        g.atomic(self.root/'data/project.json', {'requiredSources':[{'id':'official'},{'id':'community'}]})
        (self.root/'reports/assets').mkdir(parents=True)
        (self.root/'reports/assets/daily.jpg').write_bytes(b'test fixture')
        (self.root/'reports/SOURCE_NOTES.md').write_text('dated test evidence')
        self.run = self.guard.start()
        self.audit = {'checkedAt':g.now(), 'seasonConfirmed':True, 'seasonEndAt':self.end,
            'sources':[{'id':s,'status':'checked','checkedAt':g.now(),'url':'https://example.com/'+s,'note':'fixture'} for s in ['official','community']],
            'visuals':[{'id':'daily','sha256':g.digest(self.root/'reports/assets/daily.jpg'),'note':'fixture'}],
            'sourceNotesSha256':g.digest(self.root/'reports/SOURCE_NOTES.md')}
        self.audit_path=self.root/'audit.json'

    def tearDown(self): self.temp.cleanup()
    def accept(self):
        g.atomic(self.audit_path, self.audit)
        self.guard.audit(self.run,self.audit_path)

    def test_resume_same_run_after_context_loss(self):
        self.accept()
        fresh=g.Guard(self.root).start()
        self.assertEqual(self.run['runId'],fresh['runId'])
        self.assertEqual(fresh['steps']['audit']['status'],'passed')

    def test_new_run_only_after_terminal(self):
        self.run['status']='BLOCKED';self.guard.save(self.run)
        self.assertNotEqual(self.run['runId'],self.guard.start()['runId'])

    def test_missing_source_rejected(self):
        self.audit['sources'].pop()
        with self.assertRaises(RuntimeError):self.accept()

    def test_duplicate_source_rejected(self):
        self.audit['sources'][1]=copy.deepcopy(self.audit['sources'][0])
        with self.assertRaises(RuntimeError):self.accept()

    def test_stale_audit_rejected(self):
        self.audit['checkedAt']=(datetime.now(g.ZONE)-timedelta(hours=5)).isoformat()
        with self.assertRaises(RuntimeError):self.accept()

    def test_unknown_season_rejected(self):
        self.audit['seasonConfirmed']=False
        with self.assertRaises(RuntimeError):self.accept()

    def test_changed_visual_rejected(self):
        self.audit['visuals'][0]['sha256']='wrong'
        with self.assertRaises(RuntimeError):self.accept()

    def test_changed_state_invalidates_audit(self):
        self.accept()
        state=g.read(self.guard.state_path);state['openItems']=['new']
        g.atomic(self.guard.state_path,state)
        self.assertFalse(self.guard.audit_valid(self.run))

    def test_timestamp_only_preserves_audit(self):
        self.accept()
        state=g.read(self.guard.state_path);state['lastContentUpdate']='different'
        g.atomic(self.guard.state_path,state)
        self.assertTrue(self.guard.audit_valid(self.run))

    def test_visual_changed_after_audit_invalidates_it(self):
        self.accept()
        (self.root/'reports/assets/daily.jpg').write_bytes(b'changed')
        self.assertFalse(self.guard.audit_valid(self.run))

    def test_deleted_audit_is_blocked_not_crash(self):
        self.accept()
        Path(self.run['steps']['audit']['path']).unlink()
        self.assertFalse(self.guard.audit_valid(self.run))

    def complete_fixture(self):
        self.accept()
        for name in ['preflight','timestamp','markdown','artifact','portable','html','structure','publish','steam_render','steam_check','metrics']:
            self.run['steps'][name]={'status':'passed'}
        self.run['steamStatus']='UP_TO_DATE'
        self.run['builtFiles']={str(self.guard.state_path):g.digest(self.guard.state_path)}
        self.run['portableReceipt']='isolated-test-receipt'
        # Real receipt/package rejection cases run in test_portable_report.py.
        mock=patch.object(g.portable,'verify_receipt',return_value={'validation':'passed','package':'passed'})
        self.addCleanup(mock.stop);mock.start()

    def test_receipt_verification_failure_blocks(self):
        self.complete_fixture()
        with patch.object(g.portable,'verify_receipt',side_effect=ValueError('tampered package')):
            self.assertEqual(self.guard.outcome(self.run)[0],'BLOCKED')

    def test_all_gates_can_complete(self):
        self.complete_fixture()
        self.assertEqual(self.guard.outcome(self.run),('COMPLETED',[]))

    def test_steam_change_is_pending_not_completed(self):
        self.complete_fixture()
        self.run['steamStatus']='PENDING_CONFIRMATION'
        self.assertEqual(self.guard.outcome(self.run),('PENDING_CONFIRMATION',[]))

    def test_missing_build_fingerprint_blocks(self):
        self.complete_fixture()
        self.run.pop('builtFiles')
        self.assertEqual(self.guard.outcome(self.run)[0],'BLOCKED')

    def test_incomplete_run_cannot_succeed(self):
        self.accept()
        status,reasons=self.guard.outcome(self.run)
        self.assertEqual(status,'BLOCKED');self.assertIn('portable',reasons)

    def test_command_failure_not_marked_success(self):
        ok,_=self.guard.command(self.run,'test',[g.sys.executable,'-c','raise SystemExit(3)'])
        self.assertFalse(ok);self.assertEqual(self.run['steps']['test']['exitCode'],3)

    def test_missing_marker_blocks_even_exit_zero(self):
        ok,_=self.guard.command(self.run,'test',[g.sys.executable,'-c','print("hello")'],['STRUCTURE_OK'])
        self.assertFalse(ok)

    def test_tampered_evidence_is_rejected(self):
        self.accept()
        self.guard.command(self.run,'test',[g.sys.executable,'-c','print("fixture")'])
        Path(self.run['steps']['test']['log']).write_text('changed')
        self.assertIn('test: changed evidence',self.guard.outcome(self.run)[1])

    def delivery_fixture(self):
        path=self.guard.base/self.run['runId']/'result.json'
        g.atomic(path,{'status':'BLOCKED','notificationType':'CheckBlocked','message':'test result'})
        self.run.update(status='AWAITING_DELIVERY',resultPath=str(path),resultSha256=g.digest(path))
        self.guard.save(self.run)

    def test_notification_failure_does_not_complete(self):
        self.delivery_fixture()
        with patch.object(self.guard,'command',return_value=(False,'HA_NOTIFICATION_STATUS=BLOCKED')):
            self.guard.deliver(self.run)
        self.assertEqual(self.run['status'],'AWAITING_DELIVERY')
        self.assertIsNone(self.run['notification'])

    def test_receipt_failure_retries_without_duplicate_notification(self):
        self.delivery_fixture()
        with patch.object(self.guard,'command',side_effect=[(True,'HA_NOTIFICATION_STATUS=SENT'),(False,'receipt failed')]):
            self.guard.deliver(self.run)
        self.assertEqual(self.run['status'],'AWAITING_DELIVERY')
        with patch.object(self.guard,'command',return_value=(True,'HA_RECEIPT_STATUS=CONFIRMED')) as cmd:
            self.guard.deliver(self.run)
            self.assertEqual(cmd.call_count,1)
            self.assertEqual(cmd.call_args.args[1],'ha_receipt')
        self.assertEqual(self.run['status'],'BLOCKED')
        self.assertEqual(self.run['haReceipt'],'CONFIRMED')

    def test_changed_result_cannot_be_sent(self):
        self.delivery_fixture()
        Path(self.run['resultPath']).write_text('{}')
        with self.assertRaises(RuntimeError):self.guard.deliver(self.run)

    def test_transient_windows_rename_lock_is_retried(self):
        path=self.root/'retry.json'
        original=g.os.replace
        calls=[]
        def locked_once(src,dest):
            calls.append(1)
            if len(calls)==1:raise PermissionError('temporary Windows sharing lock')
            return original(src,dest)
        with patch.object(g.os,'replace',side_effect=locked_once),patch.object(g.time,'sleep'):
            g.atomic(path,{'saved':True})
        self.assertEqual(g.read(path),{'saved':True})
        self.assertEqual(len(calls),2)

    def test_permanent_rename_failure_preserves_previous_checkpoint(self):
        path=self.root/'retry.json';g.atomic(path,{'previous':True})
        with patch.object(g.os,'replace',side_effect=PermissionError('permanent lock')),patch.object(g.time,'sleep'):
            with self.assertRaises(PermissionError):g.atomic(path,{'new':True})
        self.assertEqual(g.read(path),{'previous':True})

    def test_status_is_readable_while_executor_holds_lock(self):
        with g.exclusive(self.guard.base/'process.lock'):
            p=g.subprocess.run([g.sys.executable,str(Path(g.__file__)),'status','--root',str(self.root)],capture_output=True)
        self.assertEqual(p.returncode,0,p.stderr)

if __name__=='__main__':unittest.main()
