import contextlib
from datetime import datetime,timedelta
import importlib.util
import json
import os
from pathlib import Path
import signal
import select
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch,Mock

sys.path.insert(0,str(Path(__file__).parent))
with patch.dict(os.environ,{'FH6_ROOT':str(Path(__file__).resolve().parents[2])}):
    import recovery
runner=recovery.runner
AT=datetime.fromisoformat('2026-10-14T06:10:00+07:00')

def failed_run(**kwargs):
    return dict(runId='fixture-run',runDate=AT.date().isoformat(),status='BLOCKED',steps={},**kwargs)

class PolicyTests(unittest.TestCase):
    def test_editor_handoff_error_uses_bounded_image_recovery(self):
        state,queue=recovery.decision(failed_run(),{}, {'error':'HandoffError'},'',AT)
        self.assertEqual(state['reason'],'IMAGE_HANDOFF_FAILED')
        self.assertEqual(state['status'],'WAITING');self.assertFalse(queue)
        state,queue=recovery.decision(failed_run(),state,{'error':'HandoffError'},'',AT+timedelta(minutes=5))
        self.assertTrue(queue);self.assertEqual(state['retryCount'],1)
    def test_backoff_three_attempts_then_stop_and_reset_next_day(self):
        run=failed_run();state={};at=AT
        for count,seconds in enumerate(recovery.DELAYS):
            state,queue=recovery.decision(run,state,{},'HTTP 503 service unavailable',at)
            self.assertFalse(queue)
            due=at+timedelta(seconds=seconds)
            self.assertEqual(datetime.fromisoformat(state['nextAttemptAt']),due)
            early,queue=recovery.decision(run,state,{},'HTTP 503',due-timedelta(seconds=1))
            self.assertFalse(queue)
            state,queue=recovery.decision(run,early,{},'HTTP 503',due)
            self.assertTrue(queue)
            self.assertEqual(state['retryCount'],count+1)
            # A subsequent failed guard run retains the day's shared budget.
            run=dict(run,runId='retry-'+str(count));at=due
        state,queue=recovery.decision(run,state,{},'HTTP 503',at)
        self.assertEqual(state['status'],'LIMIT_REACHED');self.assertFalse(queue)
        tomorrow=AT+timedelta(days=1)
        run=dict(run,runDate=tomorrow.date().isoformat())
        state,queue=recovery.decision(run,state,{},'HTTP 503',tomorrow)
        self.assertEqual(state['retryCount'],0);self.assertEqual(state['status'],'WAITING')

    def test_success_confirmation_and_delivery_never_restart(self):
        for status in ['COMPLETED','PENDING_CONFIRMATION','AWAITING_DELIVERY']:
            state,queue=recovery.decision(dict(failed_run(),status=status),{}, {},'HTTP 503',AT)
            self.assertFalse(queue);self.assertEqual(state['status'],'IDLE')

    def test_permanent_structure_failure_does_not_retry_even_with_network_text(self):
        run=failed_run();run['steps']={'structure':{'status':'failed'}}
        state,queue=recovery.decision(run,{}, {},'STRUCTURE_FAILED; link contained 503',AT)
        self.assertEqual(state['status'],'NEEDS_REVIEW');self.assertFalse(queue)

    def test_auth_waits_without_inference_then_resumes_on_verified_login(self):
        run=failed_run();editor={'status':'AUTH_REQUIRED'}
        state,queue=recovery.decision(run,{},editor,'',AT)
        self.assertEqual(state['status'],'NEEDS_LOGIN');self.assertFalse(queue)
        state,queue=recovery.decision(run,state,editor,'',AT,True)
        self.assertEqual(state['status'],'WAITING');self.assertFalse(queue)
        state,queue=recovery.decision(run,state,editor,'',AT+timedelta(minutes=5),True)
        self.assertTrue(queue)

    def test_interrupted_run_and_editor_timeout_get_delayed_retries(self):
        for run,editor,reason in [(dict(failed_run(),status='RUNNING'),{},'INTERRUPTED'),
                                  (failed_run(),{'error':'TimeoutExpired'},'TIMEOUT')]:
            state,queue=recovery.decision(run,{},editor,'',AT)
            self.assertFalse(queue);self.assertEqual(state['status'],'WAITING')
            self.assertEqual(state['reason'],reason)

    def test_unknown_errors_and_private_log_text_not_exported(self):
        private='SYNTHETIC_PRIVATE_VALUE'
        state,queue=recovery.decision(failed_run(),{}, {},private,AT)
        self.assertEqual(state['status'],'NEEDS_REVIEW');self.assertFalse(queue)
        self.assertNotIn(private,json.dumps(state))

    def test_activating_service_counts_as_busy(self):
        with patch.object(recovery.subprocess,'run',return_value=Mock(returncode=0,stdout='activating\n')):
            self.assertTrue(recovery.running())

    def test_stored_credentials_alone_or_old_login_do_not_resume_auth_failure(self):
        run=failed_run();run['finishedAt']=AT.isoformat()
        for login in [{},{'status':'CONNECTED','updatedAt':AT.timestamp()-1},
                      {'status':'WAITING_FOR_OWNER','updatedAt':AT.timestamp()+1}]:
            self.assertFalse(recovery.login_restored(run,login))
        self.assertTrue(recovery.login_restored(run,{'status':'CONNECTED','updatedAt':AT.timestamp()+1}))

class ExecutionTests(unittest.TestCase):
    def test_old_audit_is_not_copied_and_previous_logs_survive(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'repo';store=Path(folder)/'store'
            (root/'automation/server').mkdir(parents=True)
            (root/'automation/server/editor-prompt.md').write_text('synthetic prompt')
            (root/'automation/editor-audit.json').write_text('old synthetic audit')
            (store/'inbox').mkdir(parents=True)
            (store/'source-snapshots.json').write_text('{}')
            (store/'editor.log').write_text('old synthetic log')
            (store/'candidate-validation.log').write_text('old synthetic validation')
            process=Mock(returncode=0)
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),\
                 patch.object(runner,'EDITOR',store/'editor'),\
                 patch.object(runner.subprocess,'run',return_value=Mock(returncode=0)),\
                 patch.object(runner.subprocess,'Popen',return_value=process):
                self.assertIsNone(runner.editor())
            self.assertFalse((store/'editor/work/automation/editor-audit.json').exists())
            self.assertEqual(json.loads((store/'editor-status.json').read_text())['status'],'NO_AUDIT')
            self.assertEqual({p.read_text() for p in (store/'editor-logs').iterdir()},
                             {'old synthetic log','old synthetic validation'})

    def test_recent_accepted_audit_reused_without_model_and_changed_run_skipped(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);checkpoint=root/'automation/runs/refresh/active.json'
            checkpoint.parent.mkdir(parents=True)
            run=failed_run();run['steps']={'audit':{'status':'passed','path':'synthetic-audit.json'}}
            checkpoint.write_text(json.dumps(run))
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',root/'store'),\
                 patch.object(runner,'guard') as guard,patch.object(runner,'Guard') as gate,\
                 patch.object(runner,'editor') as editor,patch.object(runner,'collect') as collect:
                gate.return_value.audit_valid.return_value=True
                runner.run(recovery_run_id=run['runId'])
                self.assertEqual([call.args[0] for call in guard.call_args_list],['start','audit','execute'])
                self.assertEqual(guard.call_args_list[1].args[2],'synthetic-audit.json')
                editor.assert_not_called();collect.assert_not_called()
                guard.reset_mock()
                runner.run(recovery_run_id='outdated-request')
                guard.assert_not_called()
                checkpoint.write_text(json.dumps(dict(run,status='PENDING_CONFIRMATION')))
                runner.run(recovery_run_id=run['runId'])
                guard.assert_not_called()

    def test_active_service_tick_does_not_read_or_queue_work(self):
        with patch.object(recovery,'running',return_value=True),patch.object(recovery,'load') as load,\
             patch.object(recovery.subprocess,'run') as run:
            recovery.tick();load.assert_not_called();run.assert_not_called()

    def test_source_503_retries_but_404_does_not(self):
        import urllib.error
        row={'id':'fixture','url':'https://fixture.invalid'}
        for status,count in [(503,3),(404,1)]:
            error=urllib.error.HTTPError(row['url'],status,'fixture',None,None)
            with patch.object(runner.urllib.request,'urlopen',side_effect=error) as open_url,\
                 patch.object(runner.time,'sleep'):
                result=runner.fetch(row)
            self.assertEqual(open_url.call_count,count)
            self.assertEqual(result['httpStatus'],status)
            self.assertEqual(result['editorialStatus'],'NOT_REVIEWED')

    @unittest.skipUnless(os.name=='posix','Linux process groups')
    def test_timeout_stops_codex_invocation_descendants(self):
        with tempfile.TemporaryDirectory() as folder:
            pidfile=Path(folder)/'child.pid'
            child="import signal,time,os,pathlib;signal.signal(signal.SIGTERM,signal.SIG_IGN);pathlib.Path("+repr(str(pidfile))+").write_text(str(os.getpid()));time.sleep(60)"
            parent="import subprocess,sys,signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);subprocess.Popen([sys.executable,'-c',"+repr(child)+"]);time.sleep(60)"
            process=subprocess.Popen([sys.executable,'-c',parent],start_new_session=True,stdout=subprocess.PIPE)
            try:
                deadline=time.monotonic()+3
                while not pidfile.exists() and time.monotonic()<deadline:time.sleep(.01)
                self.assertTrue(pidfile.exists())
                with self.assertRaises(subprocess.TimeoutExpired):runner.wait_editor(process,timeout=.03,grace=.03)
                self.assertIsNotNone(process.returncode)
                # The TERM-resistant child inherits this pipe. EOF proves that
                # stopping runuser alone did not leave a descendant holding it.
                ready,_,_=select.select([process.stdout],[],[],2)
                self.assertTrue(ready,'Descendant still holds the invocation output pipe')
                self.assertEqual(os.read(process.stdout.fileno(),1),b'')
            finally:
                try:os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                process.wait()
                process.stdout.close()

if __name__=='__main__':unittest.main()
