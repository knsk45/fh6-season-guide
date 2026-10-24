"""Manual request correlation, durable state and safe rendering."""
import unittest,tempfile,json,time
from pathlib import Path
from unittest.mock import patch
import refresh_receipts as rr
import phone_view as view
class Tests(unittest.TestCase):
    def test_bind_is_explicit_and_unrelated_active_cannot_complete_request(self):
        with tempfile.TemporaryDirectory() as d,patch('os.geteuid',return_value=1000):
            root=Path(d);store=root/'store';store.mkdir()
            row=rr.accept(store)
            self.assertEqual(rr.snapshot(root,store)[0]['status'],'ACCEPTED')
            with self.assertRaises(ValueError):rr.accept(store)
            rr.bind(store,'fh6-20261014-180000-123456')
            base=root/'automation/runs/refresh/fh6-20261014-180000-123456';base.mkdir(parents=True)
            (base/'run.json').write_text(json.dumps({'runId':'fh6-20261014-180000-123456','status':'RUNNING','steps':{'publish':{'status':'running','command':'SECRET'},'unknown':{'status':'failed','command':'SECRET'}}}))
            state=rr.snapshot(root,store)[0]
            self.assertEqual(state['status'],'RUNNING');self.assertNotIn('SECRET',json.dumps(state));self.assertNotIn('unknown',state['steps'])
            (base/'run.json').write_text(json.dumps({'runId':'fh6-20261014-180000-123456','status':'COMPLETED','finishedAt':'2026-10-14T18:15:00+07:00','haReceipt':'CONFIRMED','steps':{'publish':{'status':'passed'}}}))
            state=rr.snapshot(root,store)[0]
            self.assertEqual(state['status'],'COMPLETED');self.assertTrue(state['siteVerified']);self.assertTrue(state['notificationReceived'])
            self.assertIn('Проверка завершена',view.refresh_history([state],{}))
            nextrow=rr.accept(store);self.assertNotEqual(row['id'],nextrow['id'])
            state=rr.snapshot(root,store)
            self.assertEqual(state[0]['status'],'ACCEPTED');self.assertEqual(state[1]['status'],'COMPLETED')
    def test_delay_and_failure_are_not_reported_as_completion(self):
        with tempfile.TemporaryDirectory() as d,patch('os.geteuid',return_value=1000):
            root=Path(d);row=rr.accept(root)
            with patch('time.time',return_value=row['acceptedAt']+121):state=rr.snapshot(root,root)[0]
            self.assertEqual(state['status'],'WAITING_FOR_WORKER')
            self.assertIn('Запуск пока не подтверждён',view.refresh_history([state],{}))
            rr.failed(root,row);self.assertEqual(rr.snapshot(root,root)[0]['status'],'FAILED_TO_QUEUE')
    def test_malicious_identity_and_symlink_are_ignored(self):
        with tempfile.TemporaryDirectory() as d,patch('os.geteuid',return_value=1000):
            root=Path(d);row=rr.accept(root);row['runId']='../../private';rr.phone_tasks.save(root/'refresh-history'/(row['id']+'.json'),row)
            self.assertEqual(rr.snapshot(root,root)[0]['status'],'ACCEPTED')
            with self.assertRaises(ValueError):rr.bind(root,'../../private')
