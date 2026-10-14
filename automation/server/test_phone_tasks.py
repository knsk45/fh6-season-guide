"""Disposable queue/HTTP tests; no live Codex or publication."""
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.request
import urllib.error
import urllib.parse
import sys
sys.path.insert(0,str(Path(__file__).parent))
import phone_tasks as tasks
import phone_ui as ui

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.patches=[patch.object(tasks,'STORE',self.root),patch.object(tasks.os,'geteuid',return_value=1000),
                      patch.object(tasks,'reserved_for_schedule',return_value=False)]
        for p in self.patches:p.start()
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.tmp.cleanup()
    def test_unicode_and_duplicate(self):
        row=tasks.enqueue('Проверь сборщик')
        self.assertEqual(tasks.latest()[0]['task'],'Проверь сборщик')
        with self.assertRaises(ValueError):tasks.enqueue('Ещё задача')
        self.assertEqual(len(list((self.root/'tasks').glob('*.json'))),1)
    def test_limits(self):
        for text in ['', ' '*10,'x'*2001,'bad\0task']:
            with self.assertRaises(ValueError):tasks.enqueue(text)
    def test_busy_pipeline_keeps_queue(self):
        tasks.enqueue('Проверить')
        with tasks.lock(self.root/'runner.lock'),patch.object(tasks,'execute') as execute:
            tasks.tick();execute.assert_not_called()
        self.assertEqual(tasks.latest()[0]['status'],'QUEUED')
    def test_scheduled_window_keeps_queue(self):
        tasks.enqueue('Проверить')
        with patch.object(tasks,'reserved_for_schedule',return_value=True),patch.object(tasks,'execute') as execute:
            tasks.tick();execute.assert_not_called()
        self.assertEqual(tasks.latest()[0]['status'],'QUEUED')
    def test_result_saved_no_second_execution(self):
        tasks.enqueue('Проверить')
        with patch.object(tasks,'execute',return_value=('FINISHED','Предложение готово')) as execute:
            tasks.tick();tasks.tick();execute.assert_called_once()
        self.assertEqual(tasks.latest()[0]['result'],'Предложение готово')
    def test_interrupted_not_replayed(self):
        row=tasks.enqueue('Проверить');row['status']='RUNNING'
        tasks.save(self.root/'tasks'/(row['id']+'.json'),row)
        with patch.object(tasks,'execute') as execute:
            tasks.tick();execute.assert_not_called()
        self.assertEqual(tasks.latest()[0]['status'],'INTERRUPTED')
    def test_worker_error_has_no_log_secrets(self):
        tasks.enqueue('Проверить')
        with patch.object(tasks,'execute',side_effect=RuntimeError('secret-token')):tasks.tick()
        self.assertEqual(tasks.latest()[0]['status'],'FAILED')
        self.assertNotIn('secret-token',tasks.latest()[0]['result'])
    def test_http_origin_and_submission(self):
        server=ui.ThreadingHTTPServer(('127.0.0.1',0),ui.UI)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        host='127.0.0.1:'+str(server.server_port);base='http://'+host
        data=urllib.parse.urlencode({'task':'Задача <script>'}).encode()
        try:
            bad=urllib.request.Request(base+'/task',data=data,headers={'Origin':'https://evil.example'})
            with self.assertRaises(urllib.error.HTTPError) as caught:urllib.request.urlopen(bad)
            self.assertEqual(caught.exception.code,403);self.assertEqual(tasks.latest(),[])
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self,*args):return None
            good=urllib.request.Request(base+'/task',data=data,headers={'Origin':'https://'+host})
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.build_opener(NoRedirect).open(good)
            self.assertEqual(caught.exception.code,303)
            self.assertEqual(tasks.latest()[0]['task'],'Задача <script>')
            reports=self.root/'reports';reports.mkdir()
            for name in ['steam-guide-current.txt','steam-guide-current-en.txt']:(reports/name).write_text('fixture')
            with patch.object(ui,'ROOT',self.root),patch.object(ui,'STORE',self.root):
                body=urllib.request.urlopen(base).read().decode()
            self.assertIn('Задача &lt;script&gt;',body)
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
