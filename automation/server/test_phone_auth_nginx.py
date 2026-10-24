"""Real nginx, isolated loopback ports, fake panel and disposable password only."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import http.client
from pathlib import Path
import re
import socket
import subprocess
import tempfile
import threading
import time
import unittest
from urllib.parse import urlencode
import phone_auth as auth
from test_phone_auth import make_hash


class Panel(BaseHTTPRequestHandler):
    writes = 0
    def log_message(self,*args):pass
    def do_GET(self):
        if self.headers.get('Upgrade','').lower()=='websocket':
            self.send_response(101);self.send_header('Upgrade','websocket');self.send_header('Connection','upgrade');self.end_headers();return
        self.send_response(200);self.send_header('Content-Length','7');self.end_headers();self.wfile.write(b'PRIVATE')
    def do_POST(self):
        self.rfile.read(int(self.headers.get('Content-Length','0')))
        type(self).writes+=1
        self.do_GET()


class Tests(unittest.TestCase):
    def test_nginx_full_boundary(self):
        with tempfile.TemporaryDirectory() as folder:
            folder=Path(folder)
            credential=folder/'passwd';credential.write_text('knsk45:'+make_hash('disposable-nginx-fixture')+'\n')
            state=auth.State(credential,{'192.168.1.55:8443'})
            authentication=auth.Server(('127.0.0.1',0),state)
            panel=ThreadingHTTPServer(('127.0.0.1',0),Panel)
            threads=[]
            for server in (authentication,panel):
                thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();threads.append(thread)
            reservation=socket.socket();reservation.bind(('127.0.0.1',0));port=reservation.getsockname()[1];reservation.close()
            conf=(Path(__file__).parent/'phone-nginx.conf').read_text()
            conf=conf.replace('listen 8443 ssl;',f'listen 127.0.0.1:{port};')
            conf='\n'.join(line for line in conf.splitlines() if not line.strip().startswith(('ssl_certificate','ssl_protocols')))
            conf=conf.replace('127.0.0.1:8766',f'127.0.0.1:{authentication.server_port}')
            conf=conf.replace('127.0.0.1:8765',f'127.0.0.1:{panel.server_port}').replace('127.0.0.1:6081',f'127.0.0.1:{panel.server_port}')
            full=f'pid {folder}/nginx.pid; error_log {folder}/error.log crit; events {{ worker_connections 64; }} http {{ access_log off; '+conf+' }'
            config=folder/'nginx.conf';config.write_text(full)
            process=subprocess.Popen(['nginx','-c',str(config),'-p',str(folder),'-g','daemon off;'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            def request(path,fields=None,cookie='',headers=None):
                connection=http.client.HTTPConnection('127.0.0.1',port,timeout=4)
                options={'Host':'192.168.1.55:8443','Cookie':cookie,'Origin':'https://192.168.1.55:8443'}
                options.update(headers or {})
                body=None if fields is None else urlencode(fields)
                if body is not None:options['Content-Type']='application/x-www-form-urlencoded'
                connection.request('GET' if body is None else 'POST',path,body,options)
                response=connection.getresponse();status=response.status;result_headers=response.getheaders()
                content=response.read().decode();connection.close()
                return status,result_headers,content
            try:
                for _ in range(60):
                    if process.poll() is not None:self.fail('nginx fixture failed to start: '+process.stderr.read().decode())
                    try:request('/signin');break
                    except OSError:time.sleep(.05)
                for endpoint in ('/','/panel-status','/login-status','/task-status','/steam-review.zip','/steam-browser/vnc.html','/steam-browser/websockify'):
                    status,headers,body=request(endpoint)
                    self.assertEqual(status,303,endpoint)
                    normalized={key.lower():value for key,value in headers}
                    self.assertTrue(normalized.get('location','').endswith('/signin'),headers)
                    self.assertNotIn('PRIVATE',body)
                    self.assertFalse(any(k.lower()=='www-authenticate' for k,v in headers))
                self.assertEqual(request('/_fh6_auth')[0],404)
                before=Panel.writes
                for endpoint in ('/refresh','/task','/upload','/approve','/login','/consent','/diagnose'):
                    self.assertEqual(request(endpoint,{'fixture':'blocked'})[0],303)
                self.assertEqual(Panel.writes,before)
                self.assertEqual(request('/setup?key=fixture')[0],200)
                self.assertEqual(request('/',cookie=auth.SESSION+'='+'a'*43)[0],303)
                status,headers,body=request('/signin');self.assertEqual(status,200)
                nonce=re.search(r'name="csrf" value="([^"]+)"',body).group(1)
                preauth=next(v for k,v in headers if k.lower()=='set-cookie').split(';')[0]
                fields={'username':'knsk45','password':'disposable-nginx-fixture','csrf':nonce}
                self.assertEqual(request('/signin',fields,preauth,{'Origin':'https://evil.example'})[0],403)
                status,headers,_=request('/signin',fields,preauth);self.assertEqual(status,303)
                cookie=next(v for k,v in headers if k.lower()=='set-cookie' and v.startswith(auth.SESSION+'=')).split(';')[0]
                self.assertEqual(request('/')[0],303)
                for endpoint in ('/','/panel-status','/steam-review.zip','/steam-browser/vnc.html'):
                    self.assertEqual(request(endpoint,cookie=cookie)[0],200)
                status,_,_=request('/steam-browser/websockify',cookie=cookie,headers={'Upgrade':'websocket','Connection':'upgrade'})
                self.assertEqual(status,101)
                self.assertEqual(request('/task',{'fixture':'allowed'},cookie)[0],200)
                self.assertEqual(Panel.writes,before+1)
                status,_,body=request('/signout',cookie=cookie);self.assertEqual(status,200)
                csrf=re.search(r'name="csrf" value="([^"]+)"',body).group(1)
                self.assertEqual(request('/signout',{'csrf':csrf},cookie)[0],303)
                self.assertEqual(request('/',cookie=cookie)[0],303)
                authentication.shutdown();authentication.server_close();threads[0].join()
                self.assertIn(request('/')[0],(500,502))  # Auth outage never exposes private UI.
            finally:
                process.terminate()
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:process.kill();process.wait()
                process.stderr.close()
                if threads[0].is_alive():authentication.shutdown();authentication.server_close();threads[0].join()
                panel.shutdown();panel.server_close();threads[1].join()


if __name__=='__main__':unittest.main()
