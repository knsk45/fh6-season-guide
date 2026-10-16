"""Safe diagnostics and bounded model delegation; no live model or publication."""
import hashlib,json,tempfile,unittest,time,threading,urllib.request,urllib.error,urllib.parse
from pathlib import Path
from unittest.mock import patch,Mock
import incident_reports as incidents
import phone_tasks
import phone_view
import refresh_receipts
import phone_ui

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'repo';self.root.mkdir()
        self.store=Path(self.temp.name)/'store';self.store.mkdir()
        self.run_id='fh6-20261016-162200-123456'
        self.base=self.root/'automation/runs/refresh'/self.run_id;self.base.mkdir(parents=True)
        self.run={'runId':self.run_id,'status':'BLOCKED','startedAt':'2026-10-16T16:22:00+07:00',
                  'finishedAt':'2026-10-16T16:23:00+07:00','steps':{'publish':{'status':'failed','exitCode':1}}}

    def log(self,text):
        data=text.encode();(self.base/'publish.log').write_bytes(data)
        self.run['steps']['publish']['sha256']=hashlib.sha256(data).hexdigest()

    def test_classifies_without_exporting_raw_log_or_credentials(self):
        secret='SYNTHETIC_PRIVATE_SECRET'
        self.log('fatal: Authentication failed for https://user:'+secret+'@example.test\nCookie: '+secret+'\nHOME='+secret)
        self.run['blockers']=[secret];self.run['steps']['publish']['command']=secret
        result=incidents.report(self.root,self.store,self.run)
        self.assertIn('GIT_AUTH',result['text']);self.assertNotIn(secret,json.dumps(result))
        self.assertNotIn('https://user',result['text'])

    def test_git_divergence_and_pages_timeout_are_distinct(self):
        self.log('Local branch does not contain origin/daily-season. Resolve the divergence before publishing.')
        self.assertIn('BRANCH_DIVERGED',incidents.report(self.root,self.store,self.run)['text'])
        self.log('GitHub Pages did not confirm deployment of commit abc within three minutes.')
        self.assertIn('PAGES_PENDING',incidents.report(self.root,self.store,self.run)['text'])

    def test_unknown_log_is_not_copied(self):
        self.log('Private arbitrary diagnostic payload')
        result=incidents.report(self.root,self.store,self.run)['text']
        self.assertIn('UNCLASSIFIED',result);self.assertNotIn('Private arbitrary',result)

    def test_log_identity_hash_and_symlink_checks(self):
        self.log('Permission denied')
        (self.base/'publish.log').write_text('Authentication failed SECRET')
        result=incidents.report(self.root,self.store,self.run)['text']
        self.assertIn('LOG_CHANGED',result);self.assertNotIn('GIT_AUTH',result)
        (self.base/'publish.log').unlink();(self.store/'private').write_text('Permission denied SECRET')
        (self.base/'publish.log').symlink_to(self.store/'private')
        self.assertNotIn('FILE_PERMISSIONS',incidents.report(self.root,self.store,self.run)['text'])
        with self.assertRaises(ValueError):incidents.load_run(self.root,'../../private')

    def test_correlated_review_only(self):
        path=self.store/'review-required.json'
        path.write_text(json.dumps({'at':'2026-10-15T01:00:00+07:00','reason':'references missing asset SECRET'}))
        self.assertNotIn('ASSET_MISSING',incidents.report(self.root,self.store,self.run)['text'])
        path.write_text(json.dumps({'at':'2026-10-16T16:22:30+07:00','reason':'references missing asset SECRET'}))
        text=incidents.report(self.root,self.store,self.run)['text']
        self.assertIn('ASSET_MISSING',text);self.assertNotIn('SECRET',text)

    def test_automatic_queue_is_deduplicated_and_bounded(self):
        self.log('Permission denied')
        with patch('os.geteuid',return_value=1000),patch.object(phone_tasks,'STORE',self.store):
            self.assertEqual(incidents.queue_analysis(self.root,self.store,self.run,automatic=True),'QUEUED')
            self.assertEqual(incidents.queue_analysis(self.root,self.store,self.run,automatic=True),'QUEUED')
            row=phone_tasks.latest()[0]
            self.assertIn('FH6_DIAGNOSTICS_V1',row['diagnostic'])
            self.assertIn('Изменения не устанавливаются автоматически',row['task'])
            self.assertEqual(len(phone_tasks.latest()),1)
            phone_tasks.save(self.store/'tasks'/(row['id']+'.json'),dict(row,status='FINISHED'))
            second=dict(self.run,runId='fh6-20261016-162400-123456')
            self.assertEqual(incidents.queue_analysis(self.root,self.store,second,automatic=True),'QUEUED')
            third=dict(self.run,runId='fh6-20261016-162500-123456')
            self.assertEqual(incidents.queue_analysis(self.root,self.store,third,automatic=True),'DAILY_LIMIT')

    def test_busy_task_is_not_overwritten(self):
        with patch('os.geteuid',return_value=1000),patch.object(phone_tasks,'STORE',self.store):
            row=phone_tasks.enqueue('Owner task')
            self.assertEqual(incidents.queue_analysis(self.root,self.store,self.run,automatic=True),'BUSY')
            self.assertEqual(phone_tasks.latest()[0]['id'],row['id'])
            with self.assertRaises(ValueError):incidents.queue_analysis(self.root,self.store,dict(self.run,status='COMPLETED'))

    def test_history_copy_is_escaped_and_run_bound(self):
        self.log('Permission denied')
        (self.base/'run.json').write_text(json.dumps(self.run))
        with patch('os.geteuid',return_value=1000):
            row=refresh_receipts.accept(self.store);refresh_receipts.bind(self.store,self.run_id)
            rows=refresh_receipts.snapshot(self.root,self.store)
        self.assertIn(self.run_id,rows[0]['diagnostic'])
        rows[0]['diagnostic']+='<script>bad()</script>'
        markup=phone_view.refresh_history(rows,{})
        self.assertIn('Скопировать диагностику',markup)
        self.assertIn('/diagnose',markup);self.assertIn('&lt;script&gt;',markup)
        self.assertNotIn('<script>bad()',markup)

    def test_invalid_diagnostic_cannot_be_enqueued(self):
        with patch('os.geteuid',return_value=1000),patch.object(phone_tasks,'STORE',self.store):
            with self.assertRaises(ValueError):phone_tasks.enqueue('Analyze',diagnostic='raw log')

    def test_bound_finished_request_is_not_still_displayed_as_queued(self):
        self.run['startedAt']=__import__('datetime').datetime.now().astimezone().isoformat(timespec='seconds')
        (self.base/'run.json').write_text(json.dumps(self.run))
        (self.base.parent/'active.json').write_text(json.dumps(self.run))
        (self.store/'refresh-request').touch()
        with patch('os.geteuid',return_value=1000),patch.object(phone_ui,'ROOT',self.root),patch.object(phone_ui,'STORE',self.store),patch.object(phone_tasks,'STORE',self.store):
            refresh_receipts.accept(self.store);refresh_receipts.bind(self.store,self.run_id)
            self.assertFalse(phone_ui.panel_data()['queued'])

    def test_diagnose_endpoint_rejects_hostile_origin_and_traversal(self):
        (self.base/'run.json').write_text(json.dumps(self.run))
        with patch('os.geteuid',return_value=1000),patch.object(phone_ui,'ROOT',self.root),patch.object(phone_ui,'STORE',self.store),patch.object(phone_tasks,'STORE',self.store):
            server=phone_ui.ThreadingHTTPServer(('127.0.0.1',0),phone_ui.UI)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            host='127.0.0.1:'+str(server.server_port)
            def post(run_id,origin):
                return urllib.request.urlopen(urllib.request.Request('http://'+host+'/diagnose?_ui=1',
                    data=urllib.parse.urlencode({'runId':run_id,'_csrf':phone_ui.CSRF_TOKEN}).encode(),
                    headers={'Origin':origin,'X-FH6-UI':'1'}))
            try:
                with self.assertRaises(urllib.error.HTTPError) as err:post(self.run_id,'https://evil.example')
                self.assertEqual(err.exception.code,403);self.assertEqual(phone_tasks.latest(),[])
                with self.assertRaises(urllib.error.HTTPError) as err:post('../../private','https://'+host)
                self.assertEqual(err.exception.code,400)
                self.assertEqual(json.load(post(self.run_id,'https://'+host))['anchor'],'tasks')
                self.assertEqual(len(phone_tasks.latest()),1)
            finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
