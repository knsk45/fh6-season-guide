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
import secrets
import sys
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0,str(Path(__file__).parent))
import phone_tasks
import phone_view
import steam_consent
import refresh_receipts
import incident_reports
import tile_search

ROOT=Path(os.environ.get('FH6_ROOT','/opt/fh6/repo'))
STORE=Path(os.environ.get('FH6_STORE','/var/lib/fh6'))
CSRF_TOKEN=secrets.token_urlsafe(32)
PUBLIC_ORIGIN='https://fh6.knsk45.crazedns.ru'
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


def panel_data():
    active=load(ROOT/'automation/runs/refresh/active.json')
    state=load(ROOT/'data/current-season.json')
    texts={}
    for language,name in [('ru','steam-guide-current.txt'),('en','steam-guide-current-en.txt')]:
        try:texts[language]=(ROOT/'reports'/name).read_text(encoding='utf-8-sig')
        except OSError:texts[language]=''
    sha=fingerprint(texts['ru']+'\n'+texts['en'])
    approval=any(load(f).get('sha256')==sha and load(f).get('status')=='AWAITING_BROWSER_PUBLICATION'
                 for f in STORE.glob('steam-approval-*.json') if not f.is_symlink())
    request=STORE/'refresh-request';queued=False
    if request.exists():
        try:
            from datetime import datetime
            started=datetime.fromisoformat(active.get('startedAt','')).timestamp()
        except (ValueError,TypeError):started=0
        queued=request.stat().st_mtime>started and time.time()-request.stat().st_mtime<60
    refresh_requests=refresh_receipts.snapshot(ROOT,STORE)
    if refresh_requests and refresh_requests[0].get('runId') and refresh_requests[0]['runId']==active.get('runId'):
        queued=False  # Explicit worker binding beats sub-second request timestamps.
    published=load(STORE/'steam-status.json')
    steam_publication={k:published.get(k) for k in ['status','sha256','updatedAt']}
    return dict(active=active,state=state,editor=load(STORE/'editor-status.json'),
                recovery=load(STORE/'recovery.json'),auth=login_status(),tasks=phone_tasks.latest(),
                texts=texts,sha=sha,approval=approval,queued=queued,refresh_requests=refresh_requests,consent=steam_consent.state(STORE),steam_publication=steam_publication,tile_search_state=tile_search.snapshot(ROOT,STORE))

def panel_signature(data):
    return dict(runId=data['active'].get('runId'),status=data['active'].get('status'),
                steps={k:(v.get('status') if isinstance(v,dict) else v) for k,v in data['active'].get('steps',{}).items()},updated=data['state'].get('lastContentUpdate'),
                notification=data['active'].get('notification'),receipt=data['active'].get('haReceipt'),
                auth=data['auth'],tasks=[[t['id'],t.get('status')] for t in data['tasks']],
                refresh_requests=data.get('refresh_requests',[]),recovery=data['recovery'].get('status'),sha=data['sha'],approval=data['approval'],queued=data['queued'],consent=data['consent'],steam_publication=data.get('steam_publication'),tile_search=data.get('tile_search_state'))

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
        if urlsplit(self.path).path=='/steam-review.zip':
            file=STORE/'steam-review.zip'
            if file.is_symlink() or not file.is_file():return self.respond(404,'Архив для проверки ещё не подготовлен.')
            if file.stat().st_size>2_000_000:return self.respond(413,'Архив слишком велик.')
            data=file.read_bytes()
            self.send_response(200);self.send_header('Content-Type','application/zip')
            self.send_header('Content-Disposition','attachment; filename="fh6-steam-review.zip"')
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
        if urlsplit(self.path).path=='/login':return self.redirect_login()
        if urlsplit(self.path).path=='/login-status':
            return self.respond(200,json.dumps(login_status()),'application/json; charset=utf-8')
        if urlsplit(self.path).path=='/panel-status':
            return self.respond(200,json.dumps(panel_signature(panel_data())),'application/json; charset=utf-8')
        if urlsplit(self.path).path=='/task-status':
            return self.respond(200,json.dumps(phone_tasks.latest(),ensure_ascii=False),'application/json; charset=utf-8')
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
        data=panel_data()
        login_code=''
        if data['auth']['codeReady']:
            try:login_code=(STORE/'login/device.txt').read_text(encoding='utf-8',errors='replace')
            except OSError:pass
        body=phone_view.render(**data,login_code=login_code,signature=panel_signature(data))
        body=re.sub(r'(<form\b[^>]*>)',lambda m:m.group(1)+'<input type="hidden" name="_csrf" value="'+CSRF_TOKEN+'">',body)
        body=body.replace("fetch('/upload',", "fetch('/upload?_csrf="+CSRF_TOKEN+"',")
        self.respond(200,body)
    def is_ajax(self):
        # Query fallback survives proxies that remove custom request headers.
        # This selects response format only; it never authorizes a request.
        return self.headers.get('X-FH6-UI')=='1' or parse_qs(urlsplit(self.path).query).get('_ui')==['1']
    def action_result(self,code,message,anchor):
        if self.is_ajax():
            return self.respond(code,json.dumps(dict(message=message,anchor=anchor),ensure_ascii=False),'application/json; charset=utf-8')
        return self.respond(code,html.escape(message)+' <a href="/#'+anchor+'">Вернуться в панель</a>')
    def redirect_login(self):
        if self.headers.get('X-FH6-UI')=='1':
            return self.action_result(200,'Запрос входа принят. Статус подключения обновится ниже.','codex')
        self.send_response(303)
        self.send_header('Location','/#codex')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length','0')
        self.end_headers()
    def do_POST(self):
        # Same-origin only; Basic auth is checked by nginx before forwarding.
        origin=self.headers.get('Origin')
        same_origin=origin == 'https://'+self.headers.get('Host','')
        try:size=int(self.headers.get('Content-Length','0'))
        except ValueError:return self.respond(400,'Invalid content length')
        path=urlsplit(self.path).path
        if path not in {'/setup','/upload','/approve','/login','/refresh','/task','/consent','/diagnose','/tile-search'}:
            return self.respond(404,'Not found')
        if size<0:return self.respond(400,'Invalid content length')
        if path=='/setup' and not 0<size<=4096:
            return self.respond(413,'Форма слишком велика.')
        if path=='/upload' and not 0<size<=MAX_UPLOAD:
            return self.respond(413,'Upload must be at most 20 MiB')
        # Native button-only forms (/login and /refresh) have a zero-byte body.
        # Keep upload validation separate from small control requests.
        if path!='/upload' and size>(24000 if path=='/task' else 4096):
            return self.respond(413,'Форма слишком велика.')
        data=self.rfile.read(size)
        # KeenDNS may replace Host and omit Origin. Only an unpredictable token
        # from the authenticated, no-store panel may authorize this fallback.
        if not same_origin:
            tokens=parse_qs(urlsplit(self.path).query).get('_csrf',[]) if path=='/upload' else parse_qs(data.decode('utf-8',errors='replace')).get('_csrf',[])
            if path=='/setup' or origin not in (None,'null',PUBLIC_ORIGIN) or len(tokens)!=1 or not re.fullmatch(r'[A-Za-z0-9_-]{43}',tokens[0]) or not hmac.compare_digest(tokens[0],CSRF_TOKEN):
                return self.respond(403,json.dumps(dict(message='HTTP 403: защитный токен отсутствует или устарел. Обновите страницу панели.',anchor='overview'),ensure_ascii=False),'application/json; charset=utf-8')
        try:
            if path=='/tile-search':
                fields=parse_qs(data.decode('utf-8'),keep_blank_values=True)
                if fields.get('enabled') not in (None,['true']):raise ValueError('Некорректное значение настройки.')
                enabled=fields.get('enabled')==['true']
                tile_search.set_enabled(STORE,enabled)
                return self.action_result(200,'Поиск плиток включён. Первая попытка — в течение минуты.' if enabled else 'Поиск плиток выключен. Начатая публикация, если есть, завершится.','screenshots')
            if path=='/consent':
                fields=parse_qs(data.decode('utf-8'),keep_blank_values=True)
                enabled=fields.get('enabled')==['true']
                if fields.get('enabled') not in (None,['true']):raise ValueError('Некорректное значение согласия.')
                steam_consent.set_enabled(STORE,enabled)
                return self.action_result(200,'Постоянное согласие включено для текущих и будущих текстов RU/EN.' if enabled else 'Постоянное согласие выключено. Автоматические разрешения отозваны.','steam')
            if path=='/task':
                fields=parse_qs(data.decode('utf-8'),keep_blank_values=True)
                if len(fields.get('task',[]))!=1:return self.respond(400,'Введите одну задачу.')
                phone_tasks.enqueue(fields['task'][0])
                if self.headers.get('X-FH6-UI')=='1':return self.action_result(200,'Задача принята. Ожидайте ответ в разделе задач.','tasks')
                self.send_response(303);self.send_header('Location','/#tasks')
                self.send_header('Content-Length','0');self.end_headers();return
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
                if fields.get('sha')!=[sha]:return self.action_result(409,'Тексты изменились. Обновите страницу и подтвердите новые тексты.','steam')
                dest=STORE/('steam-approval-'+str(uuid.uuid4())+'.json')
                dest.write_text(json.dumps(dict(sha256=sha,approvedAt=time.time(),action='replace-current-ru-en',status='AWAITING_BROWSER_PUBLICATION')),encoding='utf-8')
                return self.action_result(200,'Разрешение сохранено для двух текущих текстов. Steam ещё не опубликован.','steam')
            if path=='/login':
                request=STORE/'login-request'
                auth=login_status()
                if auth['status'] in {'QUEUED','STARTING','WAITING_FOR_OWNER','CONNECTED'}:
                    return self.redirect_login()
                request.write_text(str(time.time()),encoding='ascii')
                return self.redirect_login()
            if path=='/diagnose':
                fields=parse_qs(data.decode('utf-8'))
                ids=fields.get('runId',[])
                if len(ids)!=1:raise ValueError('Укажите один запуск.')
                run=incident_reports.load_run(ROOT,ids[0])
                state=incident_reports.queue_analysis(ROOT,STORE,run)
                messages={'BUSY':'Codex занят другой задачей. Повторите разбор позже.','NEEDS_LOGIN':'Для разбора требуется вход в Codex.'}
                return self.action_result(409 if state=='BUSY' else 200,messages.get(state,'Разбор сохранён. Ответ появится в разделе «Задачи для Codex».'),'tasks')
            if path=='/refresh':
                request=STORE/'refresh-request'
                if request.exists() and time.time()-request.stat().st_mtime<60:
                    return self.action_result(409,'Запрос уже отправлен. Дождитесь результата.','overview')
                if load(ROOT/'automation/runs/refresh/active.json').get('status') in {'RUNNING','AWAITING_DELIVERY'}:
                    return self.action_result(409,'Проверка уже выполняется. Дождитесь результата в обзоре.','overview')
                receipt=refresh_receipts.accept(STORE)
                try:request.write_text(str(time.time()),encoding='ascii')
                except OSError:
                    refresh_receipts.failed(STORE,receipt)
                    return self.action_result(500,'Не удалось поставить запрос в очередь. Повторите после проверки службы.','overview')
                return self.action_result(200,'Запрос принят. Ход проверки и итог появятся под кнопкой.','overview')
            self.respond(404,'Not found')
        except ValueError as exc:
            if path=='/setup' and not str(exc).startswith(('Пароли','Пароль не может','Введите пароль.','Не удалось подготовить')):
                return self.respond(400,'Некорректная форма.')
            if self.headers.get('X-FH6-UI')=='1':return self.action_result(400,str(exc),'tasks')
            self.respond(400,html.escape(str(exc)))
        except (OSError,subprocess.SubprocessError):
            if self.headers.get('X-FH6-UI')=='1':return self.action_result(503,'Сервис временно недоступен. Проверьте статус перед повтором.','overview')
            self.respond(503,'Сервис временно недоступен. Попробуйте снова.')

if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',8765),UI).serve_forever()
