"""Cookie authentication gateway. Loopback only; existing htpasswd stays private."""
from collections import defaultdict, deque
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import hashlib
import hmac
import html
import os
import re
import secrets
import subprocess
import threading
import time

SESSION = '__Host-fh6_session'
PREAUTH = '__Host-fh6_signin'
ID = re.compile(r'[A-Za-z0-9_-]{43}')
STYLE = '''*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:#111827;color:#e5e7eb;font:16px/1.5 system-ui,sans-serif;padding:24px}main{width:100%;max-width:420px;padding:30px;border:1px solid #374151;border-radius:20px;background:#182131;box-shadow:0 20px 70px #0004}.brand{color:#7dd3fc;font-size:13px;font-weight:700;letter-spacing:.12em}h1{font-size:28px;line-height:1.2;margin:16px 0}p{color:#b8c4d5}label{display:block;margin-top:18px;font-weight:600}input,button{width:100%;min-height:48px;font:inherit;border-radius:10px;padding:12px}input{margin-top:6px;background:#101827;border:1px solid #64748b;color:#fff}input:focus-visible,button:focus-visible,a:focus-visible{outline:3px solid #7dd3fc;outline-offset:3px}button{margin-top:24px;border:0;background:#7dd3fc;color:#102139;font-weight:750;cursor:pointer}.error{padding:12px;border:1px solid #fda4af;border-radius:10px;color:#fecdd3}a{color:#7dd3fc}.hint{font-size:13px;margin-top:22px}'''


class State:
    def __init__(self, password_file, hosts, clock=time.time):
        self.password_file = Path(password_file)
        self.hosts = frozenset(hosts)
        self.clock = clock
        self.lock = threading.RLock()
        self.sessions = {}
        self.nonces = {}
        self.failures = defaultdict(deque)

    def credentials(self):
        # Read on each check: password replacement also revokes existing sessions.
        lines = self.password_file.read_text().splitlines()
        if len(lines) != 1:
            raise ValueError('Invalid credential file')
        username, hashed = lines[0].split(':', 1)
        if not re.fullmatch(r'\$6\$(?:rounds=\d+\$)?[./A-Za-z0-9]{1,16}\$[./A-Za-z0-9]{86}', hashed):
            raise ValueError('Unsupported password hash')
        return username, hashed, hashlib.sha256(lines[0].encode()).hexdigest()

    def cleanup(self):
        now = self.clock()
        self.nonces = {k: expiry for k, expiry in self.nonces.items() if expiry > now}
        self.sessions = {k: row for k, row in self.sessions.items()
                         if row['expires'] > now and now-row['seen'] < 3600}
        for key in list(self.failures):
            queue = self.failures[key]
            while queue and queue[0] <= now-900:
                queue.popleft()
            if not queue:
                del self.failures[key]

    def nonce(self):
        with self.lock:
            self.cleanup()
            if len(self.nonces) >= 1024:
                return None
            token = secrets.token_urlsafe(32)
            self.nonces[token] = self.clock()+600
            return token

    def consume_nonce(self, cookie, field):
        if not cookie or not field or not hmac.compare_digest(cookie, field):
            return False
        with self.lock:
            self.cleanup()
            return self.nonces.pop(cookie, 0) > self.clock()

    def limited(self, address):
        with self.lock:
            self.cleanup()
            # Also bound distinct sources and total failed work.
            return (len(self.failures.get(address, ())) >= 5
                    or sum(map(len, self.failures.values())) >= 100
                    or len(self.failures) >= 1024)

    def verify(self, username, password):
        stored_user, stored_hash, revision = self.credentials()
        pieces = stored_hash.split('$')
        salt = ('$'.join(pieces[2:-1]))
        result = subprocess.run(['openssl', 'passwd', '-6', '-salt', salt, '-stdin'],
                                input=(password+'\n').encode(), capture_output=True,
                                timeout=5, check=True)
        valid_hash = hmac.compare_digest(result.stdout.decode().strip(), stored_hash)
        return hmac.compare_digest(username.encode(), stored_user.encode()) and valid_hash, revision

    def create_session(self, revision):
        with self.lock:
            self.cleanup()
            if len(self.sessions) >= 256:
                return None
            token = secrets.token_urlsafe(32)
            now = self.clock()
            self.sessions[token] = dict(expires=now+28800, seen=now,
                                        revision=revision, csrf=secrets.token_urlsafe(32))
            return token

    def session(self, token):
        if not token:
            return None
        with self.lock:
            self.cleanup()
            row = self.sessions.get(token)
            if not row:
                return None
            if not hmac.compare_digest(row['revision'], self.credentials()[2]):
                self.sessions.pop(token, None)
                return None
            row['seen'] = self.clock()
            return dict(row)


class Server(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address, state):
        self.auth = state
        self.workers = threading.BoundedSemaphore(8)
        super().__init__(address, Handler)

    def process_request(self, request, address):
        if not self.workers.acquire(blocking=False):
            request.close()
            return
        try:
            super().process_request(request, address)
        except BaseException:
            self.workers.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.workers.release()


class Handler(BaseHTTPRequestHandler):
    server_version = 'FH6'
    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def log_message(self, *args):
        pass  # No credentials, form bodies, cookies, or URL query logs.

    def cookie(self, key):
        jar = cookies.SimpleCookie()
        try:
            jar.load(self.headers.get('Cookie', ''))
            value = jar[key].value if key in jar else ''
            return value if ID.fullmatch(value) else ''
        except cookies.CookieError:
            return ''

    def send(self, status, body='', location=None, cookie_headers=()):
        data = body.encode()
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        for name, value in [('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff'),
                            ('Referrer-Policy', 'same-origin'), ('X-Frame-Options', 'DENY'),
                            ('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")]:
            self.send_header(name, value)
        if location:
            self.send_header('Location', location)
        for value in cookie_headers:
            self.send_header('Set-Cookie', value)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def page(self, title, content):
        return ('<!doctype html><html lang="ru"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>FH6 — '+title+'</title><style>'+STYLE+'</style><main>'
                '<div class="brand">FH6 · ЛИЧНАЯ ПАНЕЛЬ</div><h1>'+title+'</h1>'+content+'</main></html>')

    def sign_in(self, status=200, message=''):
        nonce = self.server.auth.nonce()
        if not nonce:
            return self.send(503, 'Вход временно недоступен. Попробуйте позже.')
        body = '<p>Войдите, чтобы открыть сводку, задачи и управление проектом.</p>'
        if message:
            body += '<p class="error" role="alert">'+html.escape(message)+'</p>'
        body += ('<form action="/signin" method="post"><input type="hidden" name="csrf" value="'+nonce+'">'
                 '<label for="username">Логин</label><input id="username" name="username" value="knsk45" autocomplete="username" required maxlength="128">'
                 '<label for="password">Пароль</label><input id="password" name="password" type="password" autocomplete="current-password" required>'
                 '<button type="submit">Войти в панель</button></form>'
                 '<p class="hint">Используйте ваш текущий пароль панели FH6. Это отдельный вход, не пароль Steam или ChatGPT.</p>')
        return self.send(status, self.page('Вход в панель', body), cookie_headers=[
            f'{PREAUTH}={nonce}; Path=/; Max-Age=600; Secure; HttpOnly; SameSite=Lax'])

    def valid_host(self):
        return self.headers.get('Host', '') in self.server.auth.hosts

    def do_GET(self):
        if not self.valid_host():
            return self.send(400, 'Недопустимый адрес панели.')
        try:
            path = urlsplit(self.path).path
            token = self.cookie(SESSION)
            row = self.server.auth.session(token)
            if path == '/_auth':
                return self.send(204 if row else 401)
            if path == '/signin':
                if row:
                    return self.send(303, location='/')
                return self.sign_in()
            if path == '/signout':
                if not row:
                    return self.send(303, location='/signin')
                body = ('<p>Завершить сеанс на этом устройстве?</p>'
                        '<form method="post" action="/signout"><input type="hidden" name="csrf" value="'+row['csrf']+'">'
                        '<button>Выйти</button></form><p><a href="/">Остаться в панели</a></p>')
                return self.send(200, self.page('Выход', body))
            return self.send(404, 'Страница не найдена.')
        except (OSError, ValueError, subprocess.SubprocessError):
            return self.send(503, 'Сервис входа временно недоступен.')

    def do_POST(self):
        if not self.valid_host():
            return self.send(400, 'Недопустимый адрес панели.')
        # HTTPS is terminated by the loopback nginx proxy; Host is allowlisted.
        if self.headers.get('Origin') not in {'https://'+host for host in self.server.auth.hosts}:
            return self.send(403, 'Запрос отклонён. Откройте страницу входа заново.')
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 4096:
                return self.send(413, 'Форма слишком велика или пуста.')
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/x-www-form-urlencoded':
                return self.send(415, 'Неподдерживаемый формат формы.')
            fields = parse_qs(self.rfile.read(size).decode('utf-8'), keep_blank_values=True, max_num_fields=8)
            path = urlsplit(self.path).path
            if path == '/signin':
                if any(len(fields.get(key, [])) != 1 for key in ('username', 'password', 'csrf')):
                    return self.send(400, 'Заполните логин и пароль.')
                if not self.server.auth.consume_nonce(self.cookie(PREAUTH), fields['csrf'][0]):
                    return self.sign_in(403, 'Форма устарела. Повторите вход.')
                address = self.headers.get('X-Real-IP', self.client_address[0])
                if self.server.auth.limited(address):
                    return self.sign_in(429, 'Слишком много попыток. Повторите вход через 15 минут.')
                username, password = fields['username'][0], fields['password'][0]
                if len(username) > 128 or not password or any(c in password for c in '\r\n\0'):
                    return self.sign_in(400, 'Проверьте логин и пароль.')
                valid, revision = self.server.auth.verify(username, password)
                if not valid:
                    with self.server.auth.lock:
                        self.server.auth.failures[address].append(self.server.auth.clock())
                    return self.sign_in(401, 'Неверный логин или пароль.')
                token = self.server.auth.create_session(revision)
                if not token:
                    return self.sign_in(503, 'Слишком много открытых сеансов. Попробуйте позже.')
                return self.send(303, location='/', cookie_headers=[
                    f'{SESSION}={token}; Path=/; Max-Age=28800; Secure; HttpOnly; SameSite=Lax',
                    f'{PREAUTH}=; Path=/; Max-Age=0; Secure; HttpOnly; SameSite=Lax'])
            if path == '/signout':
                token = self.cookie(SESSION)
                row = self.server.auth.session(token)
                csrf = fields.get('csrf', [])
                if not row or len(csrf) != 1 or not hmac.compare_digest(csrf[0], row['csrf']):
                    return self.send(403, 'Запрос выхода отклонён.')
                with self.server.auth.lock:
                    self.server.auth.sessions.pop(token, None)
                return self.send(303, location='/signin', cookie_headers=[
                    f'{SESSION}=; Path=/; Max-Age=0; Secure; HttpOnly; SameSite=Lax'])
            return self.send(404, 'Страница не найдена.')
        except (OSError, ValueError, UnicodeError, subprocess.SubprocessError):
            return self.send(503, 'Сервис входа временно недоступен.')


if __name__ == '__main__':
    state = State(os.environ.get('FH6_PASSWORD_FILE', '/etc/fh6/phone.htpasswd'),
                  os.environ.get('FH6_AUTH_HOSTS', '192.168.1.55:8443,fh6.knsk45.crazedns.ru').split(','))
    state.credentials()  # Fail closed on missing/unreadable/unsupported credentials.
    Server(('127.0.0.1', 8766), state).serve_forever()
