"""Proxy CSRF receipts use disposable state; no real account or publication."""
import sys,threading,tempfile,urllib.request,urllib.error,urllib.parse
from pathlib import Path
from unittest.mock import patch
import unittest
sys.path.insert(0,str(Path(__file__).parent))
import test_phone_view
import phone_ui as ui
class Tests(unittest.TestCase):
    def test_proxy_csrf_gate(self):
        with tempfile.TemporaryDirectory() as d,patch.object(ui,'STORE',Path(d)),patch.object(ui,'panel_data',test_phone_view.fixture),patch('os.geteuid',return_value=1000),patch.object(ui,'CSRF_TOKEN',ui.CSRF_TOKEN):
            server=ui.ThreadingHTTPServer(('127.0.0.1',0),ui.UI);threading.Thread(target=server.serve_forever,daemon=True).start()
            base='http://127.0.0.1:'+str(server.server_port)
            body=urllib.request.urlopen(base).read().decode()
            assert body.count('name="_csrf"')==body.count('<form ')
            assert "fetch('/upload?_csrf="+ui.CSRF_TOKEN in body
            def post(fields,origin=None):
                headers={'X-FH6-UI':'1','Host':'192.168.1.55'}
                if origin is not None:headers['Origin']=origin
                try:return urllib.request.urlopen(urllib.request.Request(base+'/consent',data=urllib.parse.urlencode(fields,doseq=True).encode(),headers=headers)).status
                except urllib.error.HTTPError as e:return e.code
            assert post({'enabled':'true'})==403
            assert not (Path(d)/'steam-consent.json').exists()
            assert post({'enabled':'true','_csrf':'bad'})==403
            assert post({'enabled':'true','_csrf':'☃'})==403
            assert post({'enabled':'true','_csrf':ui.CSRF_TOKEN},'https://evil.example')==403
            assert post({'enabled':'true','_csrf':[ui.CSRF_TOKEN,ui.CSRF_TOKEN]})==403
            assert post({'enabled':'true','_csrf':ui.CSRF_TOKEN})==200
            assert ui.steam_consent.state(Path(d))['enabled']
            assert post({'_csrf':ui.CSRF_TOKEN},ui.PUBLIC_ORIGIN)==200
            assert not ui.steam_consent.state(Path(d))['enabled']
            assert post({'enabled':'true','_csrf':ui.CSRF_TOKEN},'null')==200
            old=ui.CSRF_TOKEN;ui.CSRF_TOKEN='a'*43
            assert post({'_csrf':old})==403
            server.shutdown();server.server_close()
