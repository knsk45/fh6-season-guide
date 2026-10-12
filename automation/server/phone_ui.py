"""Private inbox/status UI, behind nginx TLS + Basic auth. No shell endpoints."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import hashlib
import html
import json
import os
import hmac
import re
import socket
import subprocess
import time
import uuid
from urllib.parse import parse_qs, urlsplit

ROOT=Path(os.environ.get('FH6_ROOT','/opt/fh6/repo'))
STORE=Path(os.environ.get('FH6_STORE','/var/lib/fh6'))
MAX_UPLOAD=20*1024*1024
FIRST_LOGIN=Path('/etc/fh6/phone-first-login.json')
PASSWORD_SOCKET='/run/fh6-phone/password.sock'

def invitation_valid(token):
    state=load(FIRST_LOGIN)
    return (isinstance(token,str) and re.fullmatch(r'[A-Za-z0-9_-]{43}',token)
            and state.get('status')=='pending' and state.get('expiresAt',0)>time.time()
            and hmac.compare_digest(state.get('tokenSha256',''),fingerprint(token)))

def password_hash(password,confirmation):
    if password!=confirmation:raise ValueError('Пароли не совпадают.')
    if not password:raise ValueError('Введите пароль.')
    if any(c in password for c in '\r\n\0'):
        raise ValueError('Пароль не может содержать перевод строки или нулевой символ.')
    result=subprocess.run(['openssl','passwd','-6','-stdin'],input=password+'\n',
                          text=True,capture_output=True,check=True,timeout=5)
    hashed=result.stdout.strip()
    if not re.fullmatch(r'\$6\$[./A-Za-z0-9]{1,16}\$[./A-Za-z0-9]{86}',hashed):
        raise ValueError('Не удалось подготовить пароль.')
    return hashed

def set_password(token,hashed):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as connection:
        connection.settimeout(5);connection.connect(PASSWORD_SOCKET)
        connection.sendall(json.dumps(dict(token=token,hash=hashed)).encode())
        connection.shutdown(socket.SHUT_WR)
        return json.loads(connection.recv(1024))

def load(file):
    try: return json.loads(file.read_text(encoding='utf-8-sig'))
    except (OSError,ValueError): return {}

def fingerprint(text): return hashlib.sha256(text.encode()).hexdigest()

def login_status():
    saved=load(STORE/'login/status.json')
    state=saved.get('status','IDLE')
    started=saved.get('startedAt',0)
    if state not in {'IDLE','STARTING','WAITING_FOR_OWNER','CONNECTED','FAILED','EXPIRED'}:
        state='FAILED'
    if state in {'STARTING','WAITING_FOR_OWNER'} and time.time()-started>920:
        state='EXPIRED'
    request=STORE/'login-request'
    if request.exists() and request.stat().st_mtime>saved.get('updatedAt',0) and time.time()-request.stat().st_mtime<15:
        state='QUEUED'
    code=STORE/'login/device.txt'
    ready=state=='WAITING_FOR_OWNER' and code.is_file() and code.stat().st_size>0
    return dict(status=state,codeReady=ready)

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
        # no-referrer makes browsers send Origin:null on native form POSTs.
        # strict-origin preserves Origin and never sends the invitation URL path/query.
        self.send_header('Referrer-Policy','strict-origin')
        self.send_header('X-Frame-Options','DENY')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if urlsplit(self.path).path=='/login':return self.redirect_login()
        if urlsplit(self.path).path=='/login-status':
            return self.respond(200,json.dumps(login_status()),'application/json; charset=utf-8')
        if urlsplit(self.path).path=='/setup':
            token=parse_qs(urlsplit(self.path).query).get('key',[''])[0]
            if not invitation_valid(token):return self.respond(404,'Ссылка недействительна, истекла или уже использована.')
            return self.respond(200,'''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FH6 — свой пароль</title>
            <style>body{font:17px system-ui;max-width:440px;margin:32px auto;padding:20px;background:#151825;color:#eee}label,input,button{display:block;box-sizing:border-box;width:100%;font:inherit}input,button{padding:12px;margin:8px 0 20px}button{background:#8ce6ff;border:0;border-radius:8px}</style>
            <h1>Установите свой пароль</h1><p>Логин: <strong>knsk45</strong>. Пароль только для панели FH6, не для ChatGPT.</p>
            <form method="post" action="/setup"><input type="hidden" name="key" value="'''+html.escape(token)+'''">
            <label>Новый пароль<input type="password" name="password" autocomplete="new-password" required></label>
            <label>Повторите пароль<input type="password" name="confirmation" autocomplete="new-password" required></label>
            <button>Установить пароль и перейти к входу</button></form><p>Одноразовая ссылка перестанет работать после сохранения.</p></html>''')
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
        body+='<form method="post" action="/refresh"><button>Запустить внеплановую проверку на сервере</button></form>'
        auth=login_status()
        labels={'IDLE':'Codex ещё не подключён. Нажмите кнопку входа.',
                'QUEUED':'Запрос принят — запускаем вход…','STARTING':'Запускаем вход…',
                'WAITING_FOR_OWNER':'Ожидаем подтверждения владельца на странице OpenAI.',
                'CONNECTED':'Codex подключён. Авторизация на сервере подтверждена.',
                'FAILED':'Вход завершился с ошибкой. Нажмите кнопку, чтобы повторить.',
                'EXPIRED':'Время входа истекло. Нажмите кнопку для нового кода.'}
        body+='<h2 id="codex">Codex на сервере</h2><p id="codex-status">'+labels[auth['status']]+'</p>'
        if auth['status']!='CONNECTED':
            body+='<form method="post" action="/login"><button>Войти в Codex на сервере</button></form>'
        body+='<p>Откройте <a href="https://auth.openai.com/codex/device" target="_blank" rel="noopener noreferrer">официальную страницу входа OpenAI</a> и введите код ниже. Код и пароль вводит только владелец; не отправляйте их в чат.</p>'
        login=STORE/'login/device.txt'
        if auth['codeReady']:
            try:body+='<pre id="codex-code">'+html.escape(login.read_text(encoding='utf-8',errors='replace'))+'</pre>'
            except OSError:pass
        if auth['status'] in {'QUEUED','STARTING','WAITING_FOR_OWNER'}:
            body+='<p>Статус обновляется автоматически. Если код ещё не появился, подождите.</p>'
            body+='<script>const initialLogin='+json.dumps(auth)+''';setInterval(async()=>{try{const r=await fetch('/login-status',{cache:'no-store'});if(!r.ok)return;const s=await r.json();if(s.status!==initialLogin.status||s.codeReady!==initialLogin.codeReady)location.reload();}catch{}},3000);</script>'''
        body+='''<h2>Оригинальные скриншоты</h2><input id="screens" type="file" accept="image/png,image/jpeg,image/webp" multiple><button onclick="upload()">Передать оригиналы</button><p id="message"></p>
        <script>async function upload(){for(const f of document.querySelector('#screens').files){const r=await fetch('/upload',{method:'POST',headers:{'Content-Type':'application/octet-stream','X-FH6-Request':'upload'},body:f});document.querySelector('#message').textContent=await r.text();if(!r.ok)break;}}</script>'''
        body+=''.join(steam)
        body+=f'''<p>Подтверждение сохраняется для редактора. Оно не означает, что Steam уже опубликован.</p><form method="post" action="/approve"><input type="hidden" name="sha" value="{sha}"><button>Разрешаю заменить эти два текста Steam</button></form>
        <p>Steam редактируется после входа владельца через браузер. Публичная проверка обязательна.</p></html>'''
        self.respond(200,body)
    def redirect_login(self):
        self.send_response(303)
        self.send_header('Location','/#codex')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length','0')
        self.end_headers()
    def do_POST(self):
        # Same-origin only; Basic auth is checked by nginx before forwarding.
        origin=self.headers.get('Origin')
        if origin != 'https://'+self.headers.get('Host',''):
            return self.respond(403,'Same-origin request required')
        try:size=int(self.headers.get('Content-Length','0'))
        except ValueError:return self.respond(400,'Invalid content length')
        path=urlsplit(self.path).path
        if path not in {'/setup','/upload','/approve','/login','/refresh'}:
            return self.respond(404,'Not found')
        if size<0:return self.respond(400,'Invalid content length')
        if path=='/setup' and not 0<size<=4096:
            return self.respond(413,'Форма слишком велика.')
        if path=='/upload' and not 0<size<=MAX_UPLOAD:
            return self.respond(413,'Upload must be at most 20 MiB')
        # Native button-only forms (/login and /refresh) have a zero-byte body.
        # Keep upload validation separate from small control requests.
        if path!='/upload' and size>4096:
            return self.respond(413,'Форма слишком велика.')
        data=self.rfile.read(size)
        try:
            if path=='/setup':
                fields=parse_qs(data.decode('utf-8'),keep_blank_values=True)
                if any(len(fields.get(key,[]))!=1 for key in ['key','password','confirmation']):
                    return self.respond(400,'Заполните пароль и подтверждение.')
                token=fields['key'][0]
                if not invitation_valid(token):return self.respond(404,'Ссылка недействительна, истекла или уже использована.')
                hashed=password_hash(fields['password'][0],fields['confirmation'][0])
                result=set_password(token,hashed)
                if not result.get('ok'):return self.respond(409,'Не удалось сохранить пароль; ссылка могла истечь или уже использована.')
                return self.respond(200,'Пароль установлен. <a href="/">Открыть панель</a> и войти с логином <strong>knsk45</strong> и вашим паролем.')
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
                auth=login_status()
                if auth['status'] in {'QUEUED','STARTING','WAITING_FOR_OWNER','CONNECTED'}:
                    return self.redirect_login()
                request.write_text(str(time.time()),encoding='ascii')
                return self.redirect_login()
            if path=='/refresh':
                request=STORE/'refresh-request'
                if request.exists() and time.time()-request.stat().st_mtime<60:
                    return self.respond(409,'Запрос уже отправлен; дождитесь результата.')
                request.write_text(str(time.time()),encoding='ascii')
                return self.respond(200,'Внеплановая проверка поставлена в очередь. <a href="/">Посмотреть статус</a>')
            self.respond(404,'Not found')
        except ValueError as exc:
            if path=='/setup' and not str(exc).startswith(('Пароли','Пароль не может','Введите пароль.','Не удалось подготовить')):
                return self.respond(400,'Некорректная форма.')
            self.respond(400,html.escape(str(exc)))
        except (OSError,subprocess.SubprocessError):self.respond(503,'Сервис временно недоступен. Попробуйте снова.')

if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',8765),UI).serve_forever()
