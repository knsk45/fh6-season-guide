"""Private inbox/status UI, behind nginx TLS + Basic auth. No shell endpoints."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib
import html
import json
import os
import time
import uuid
from urllib.parse import parse_qs, urlsplit

ROOT=Path(os.environ.get('FH6_ROOT','/opt/fh6/repo'))
STORE=Path(os.environ.get('FH6_STORE','/var/lib/fh6'))
MAX_UPLOAD=20*1024*1024

def load(file):
    try: return json.loads(file.read_text(encoding='utf-8-sig'))
    except (OSError,ValueError): return {}

def fingerprint(text): return hashlib.sha256(text.encode()).hexdigest()

def mime(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'): return '.png'
    if data.startswith(b'\xff\xd8\xff'): return '.jpg'
    if data[:4]==b'RIFF' and data[8:12]==b'WEBP': return '.webp'
    raise ValueError('Only original PNG, JPEG or WebP is accepted')

class UI(BaseHTTPRequestHandler):
    def log_message(self,*args): pass  # Do not log credentials/query contents.
    def respond(self,code,body,kind='text/html; charset=utf-8'):
        data=body.encode()
        self.send_response(code);self.send_header('Content-Type',kind)
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if urlsplit(self.path).path!='/': return self.respond(404,'Not found')
        active=load(ROOT/'automation/runs/refresh/active.json')
        state=load(ROOT/'data/current-season.json')
        editor=load(STORE/'editor-status.json')
        safe_status=dict(runId=active.get('runId'),status=active.get('status'),nextAction=active.get('nextAction'),
                         notification=active.get('notification'),haReceipt=active.get('haReceipt'),editor=editor,
                         updated=state.get('lastContentUpdate'),season=state.get('season',{}).get('reportTitle'))
        steam=[]
        for language,name in [('ru','steam-guide-current.txt'),('en','steam-guide-current-en.txt')]:
            text=(ROOT/'reports'/name).read_text(encoding='utf-8-sig')
            steam.append(f'<h2>Steam {language}</h2><pre>{html.escape(text)}</pre>')
        combined='\n'.join((ROOT/'reports'/name).read_text(encoding='utf-8-sig') for name in ['steam-guide-current.txt','steam-guide-current-en.txt'])
        sha=fingerprint(combined)
        body='''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FH6 — сервер</title>
        <style>body{font:16px system-ui;max-width:950px;margin:auto;padding:20px;background:#151825;color:#eee}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#232940;padding:16px}button,input{font:inherit;padding:12px}a{color:#8ce6ff}</style>
        <h1>FH6 — серверный сборщик</h1><p>Доступ только через домашнюю сеть/VPN. Пароль не вводите в чате.</p>'''
        body+=f'<pre>{html.escape(json.dumps(safe_status,ensure_ascii=False,indent=2))}</pre>'
        body+='<h2>Облачный редактор</h2><form method="post" action="/login"><button>Войти в Codex на сервере</button></form><p>После нажатия обновите страницу через 5 секунд. Код вводит только владелец; не отправляйте его в чат.</p>'
        login=STORE/'login/device.txt'
        if login.is_file():
            body+='<pre>'+html.escape(login.read_text(encoding='utf-8',errors='replace'))+'</pre>'
        body+='''<h2>Оригинальные скриншоты</h2><input id="screens" type="file" accept="image/png,image/jpeg,image/webp" multiple><button onclick="upload()">Передать оригиналы</button><p id="message"></p>
        <script>async function upload(){for(const f of document.querySelector('#screens').files){const r=await fetch('/upload',{method:'POST',headers:{'Content-Type':'application/octet-stream','X-FH6-Request':'upload'},body:f});document.querySelector('#message').textContent=await r.text();if(!r.ok)break;}}</script>'''
        body+=''.join(steam)
        body+=f'''<p>Подтверждение сохраняется для редактора. Оно не означает, что Steam уже опубликован.</p><form method="post" action="/approve"><input type="hidden" name="sha" value="{sha}"><button>Разрешаю заменить эти два текста Steam</button></form>
        <p>Steam редактируется после входа владельца через браузер. Публичная проверка обязательна.</p></html>'''
        self.respond(200,body)
    def do_POST(self):
        # Same-origin only; Basic auth is checked by nginx before forwarding.
        origin=self.headers.get('Origin')
        if origin != 'https://'+self.headers.get('Host',''):
            return self.respond(403,'Same-origin request required')
        size=int(self.headers.get('Content-Length','0'))
        if not 0<size<=MAX_UPLOAD:return self.respond(413,'Upload must be at most 20 MiB')
        path=urlsplit(self.path).path
        data=self.rfile.read(size)
        try:
            if path=='/upload':
                if self.headers.get('X-FH6-Request')!='upload':return self.respond(403,'Invalid upload request')
                extension=mime(data)
                name=str(uuid.uuid4())+extension
                dest=STORE/'inbox'/name
                with dest.open('xb') as stream:stream.write(data)
                os.chmod(dest,0o640)
                receipt=dict(file=name,sha256=hashlib.sha256(data).hexdigest(),receivedAt=time.time(),bytes=len(data))
                (STORE/'inbox'/(name+'.json')).write_text(json.dumps(receipt),encoding='utf-8')
                return self.respond(200,'Оригинал сохранён без изменений; ожидает редакторской проверки.','text/plain; charset=utf-8')
            if path=='/approve':
                fields=parse_qs(data.decode())
                text='\n'.join((ROOT/'reports'/n).read_text(encoding='utf-8-sig') for n in ['steam-guide-current.txt','steam-guide-current-en.txt'])
                sha=fingerprint(text)
                if fields.get('sha')!=[sha]:return self.respond(409,'Тексты изменились; перечитайте их и подтвердите заново.')
                dest=STORE/('steam-approval-'+str(uuid.uuid4())+'.json')
                dest.write_text(json.dumps(dict(sha256=sha,approvedAt=time.time(),action='replace-current-ru-en',status='AWAITING_BROWSER_PUBLICATION')),encoding='utf-8')
                return self.respond(200,'Подтверждение записано. Steam ещё не опубликован. <a href="/">Вернуться</a>')
            if path=='/login':
                request=STORE/'login-request'
                if request.exists() and time.time()-request.stat().st_mtime<920:
                    return self.respond(409,'Вход уже запущен; обновите страницу.')
                request.write_text(str(time.time()),encoding='ascii')
                return self.respond(200,'Запрос входа передан. <a href="/">Обновить страницу через 5 секунд</a>')
            self.respond(404,'Not found')
        except ValueError as exc:self.respond(400,html.escape(str(exc)))

if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',8765),UI).serve_forever()
