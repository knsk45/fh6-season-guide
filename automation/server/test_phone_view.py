"""Panel presentation and action receipts, with disposable state only."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import unittest
import tempfile
import threading
import json
import urllib.request
import urllib.error
import urllib.parse
from unittest.mock import patch
import phone_view as view
import phone_ui as ui

def fixture():
    return dict(active={'status':'PENDING_CONFIRMATION','steps':{'publish':{'status':'passed'}},'haReceipt':'CONFIRMED'},
        state={'lastContentUpdate':'2026-10-14T06:05:42+07:00','season':{'reportTitle':'Лето'}},editor={},recovery={},
        auth={'status':'CONNECTED','codeReady':False},tasks=[],texts={'ru':'Текст <script> & код','en':'English'},sha='a'*64,
        approval=False,queued=False,consent={'enabled':False,'updatedAt':None})

class Tests(unittest.TestCase):
    def test_readable_statuses_and_collapsed_text(self):
        body=view.render(**fixture())
        self.assertIn('Сайт обновлён',body);self.assertIn('Получено',body)
        self.assertNotIn('"status":',body);self.assertNotIn('"runId":',body)
        self.assertIn('data-copy="steam-ru"',body);self.assertIn('data-copy="steam-en"',body)
        self.assertIn('<details><summary>Показать текст',body)
        self.assertNotIn('<details open',body)
        self.assertIn('Текст &lt;script&gt; &amp; код',body)
        self.assertNotIn('Открыть страницу входа OpenAI',body)
    def test_approval_visible_and_no_repeat_button(self):
        data=fixture();data['approval']=True;body=view.render(**data)
        self.assertIn('Разрешение сохранено',body);self.assertNotIn('action="/approve"',body)
        self.assertIn('Ожидается публикация',body)
    def test_running_task_and_old_history(self):
        data=fixture();data['tasks']=[dict(id='a',status='RUNNING',task='<img>'),dict(id='b',status='FAILED',task='Old',result='<script>')]
        body=view.render(**data)
        self.assertIn('Предыдущие задачи (1)',body);self.assertIn('Выполняется',body)
        self.assertIn('&lt;img&gt;',body);self.assertIn('&lt;script&gt;',body)
        self.assertNotIn('action="/task"',body)
    def test_signature_has_no_private_commands(self):
        data=fixture();data['active']['steps']['publish']['command']='secret command'
        self.assertNotIn('secret command',json.dumps(ui.panel_signature(data)))
    def test_steam_complete_bound_to_current_pair(self):
        data=fixture();data['steam_publication']={'status':'COMPLETE','sha256':'old'}
        self.assertNotIn('Оба раздела опубликованы',view.render(**data))
        data['steam_publication']['sha256']=data['sha']
        self.assertIn('Сайт и Steam обновлены',view.render(**data))
    def test_ajax_actions_and_same_origin(self):
        with tempfile.TemporaryDirectory() as d,patch.object(ui,'STORE',Path(d)),patch.object(ui,'ROOT',Path(d)):
            root=Path(d);(root/'reports').mkdir()
            for name,text in [('steam-guide-current.txt','Russian'),('steam-guide-current-en.txt','English')]:
                (root/'reports'/name).write_text(text)
            server=ui.ThreadingHTTPServer(('127.0.0.1',0),ui.UI)
            worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            host='127.0.0.1:'+str(server.server_port);base='http://'+host
            def post(path,fields,origin=None):
                return urllib.request.urlopen(urllib.request.Request(base+path,data=urllib.parse.urlencode(fields).encode(),headers={'Origin':origin or 'https://'+host,'X-FH6-UI':'1'}))
            try:
                with self.assertRaises(urllib.error.HTTPError) as err:urllib.request.urlopen(base+'/steam-review.zip')
                self.assertEqual(err.exception.code,404)
                (root/'steam-review.zip').write_bytes(b'PK disposable archive')
                download=urllib.request.urlopen(base+'/steam-review.zip')
                self.assertEqual(download.read(),b'PK disposable archive')
                self.assertIn('attachment',download.headers['Content-Disposition'])
                (root/'steam-review.zip').unlink()
                (root/'steam-review.zip').symlink_to(root/'reports/steam-guide-current.txt')
                with self.assertRaises(urllib.error.HTTPError) as err:urllib.request.urlopen(base+'/steam-review.zip')
                self.assertEqual(err.exception.code,404)
                response=post('/approve',{'sha':ui.fingerprint('Russian\nEnglish')})
                self.assertIn('application/json',response.headers['Content-Type'])
                self.assertIn('Разрешение сохранено',json.load(response)['message'])
                self.assertTrue(ui.panel_data()['approval'])
                with self.assertRaises(urllib.error.HTTPError) as err:post('/approve',{'sha':'old'})
                self.assertEqual(err.exception.code,409)
                self.assertIn('Тексты изменились',json.load(err.exception)['message'])
                with self.assertRaises(urllib.error.HTTPError) as err:post('/refresh',{},'https://evil.example')
                self.assertEqual(err.exception.code,403)
                self.assertEqual(json.load(post('/refresh',{}))['anchor'],'overview')
            finally:server.shutdown();server.server_close();worker.join()

if __name__=='__main__':unittest.main()
