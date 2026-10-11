"""One-use owner password setup. Never print tokens, passwords or hashes."""
import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import socket
import stat
import struct
import tempfile
import time
import urllib.request

ETC = Path('/etc/fh6')
SOCKET = Path('/run/fh6-phone/password.sock')
USERNAME = 'knsk45'
HASH = re.compile(r'\$6\$[./A-Za-z0-9]{1,16}\$[./A-Za-z0-9]{86}')


def read_state():
    try:
        return json.loads((ETC / 'phone-first-login.json').read_text())
    except (OSError, ValueError):
        return {}


def valid_invitation(state, token, now=None):
    if not isinstance(token, str) or not re.fullmatch(r'[A-Za-z0-9_-]{43}', token):
        return False
    return (state.get('status') == 'pending'
            and state.get('expiresAt', 0) > (time.time() if now is None else now)
            and hmac.compare_digest(state.get('tokenSha256', ''),
                                    hashlib.sha256(token.encode()).hexdigest()))


def atomic(file, content, group, mode):
    import grp
    descriptor, name = tempfile.mkstemp(dir=file.parent, prefix='.phone-')
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chown(name, 0, grp.getgrnam(group).gr_gid)
        os.chmod(name, mode)
        os.replace(name, file)
        directory = os.open(file.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def apply(request):
    state = read_state()
    token, hashed = request.get('token'), request.get('hash')
    if not valid_invitation(state, token):
        return dict(ok=False, reason='expired_or_used')
    if not isinstance(hashed, str) or not HASH.fullmatch(hashed):
        return dict(ok=False, reason='invalid_hash')
    # Retire the invitation first: interruption must fail closed, never allow replay.
    state = dict(status='applying', username=USERNAME, updatedAt=time.time())
    atomic(ETC / 'phone-first-login.json', json.dumps(state), 'fh6', 0o640)
    atomic(ETC / 'phone.htpasswd', USERNAME + ':' + hashed + '\n', 'www-data', 0o640)
    state['status'] = 'complete'
    atomic(ETC / 'phone-first-login.json', json.dumps(state), 'fh6', 0o640)
    return dict(ok=True, username=USERNAME)


def serve():
    import grp
    import pwd
    allowed = pwd.getpwnam('fh6').pw_uid
    if SOCKET.exists():
        if not stat.S_ISSOCK(SOCKET.lstat().st_mode):
            raise RuntimeError('Unexpected object at credential socket')
        SOCKET.unlink()
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listener.bind(str(SOCKET))
    os.chown(SOCKET, 0, grp.getgrnam('fh6').gr_gid)
    os.chmod(SOCKET, 0o660)
    listener.listen(4)
    while True:
        connection, _ = listener.accept()
        with connection:
            try:
                connection.settimeout(3)
                _, uid, _ = struct.unpack('3i', connection.getsockopt(
                    socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
                if uid != allowed:
                    continue
                chunks = b''
                while len(chunks) <= 4096:
                    part = connection.recv(4097 - len(chunks))
                    if not part:
                        break
                    chunks += part
                if len(chunks) > 4096:
                    result = dict(ok=False, reason='too_large')
                else:
                    request = json.loads(chunks)
                    result = apply(request) if isinstance(request, dict) else dict(ok=False)
                connection.sendall(json.dumps(result).encode())
            except Exception:
                # Do not put request material in journald or an HTTP error.
                try:
                    connection.sendall(b'{"ok":false,"reason":"setup_failed"}')
                except OSError:
                    pass


def prepare():
    if read_state().get('status') in ('pending', 'applying', 'complete'):
        raise RuntimeError('Setup already prepared; no automatic password reset')
    token = secrets.token_urlsafe(32)
    state = dict(status='pending', username=USERNAME, createdAt=time.time(),
                 expiresAt=time.time() + 86400,
                 tokenSha256=hashlib.sha256(token.encode()).hexdigest())
    # Preserve the old hash only in a root-private recovery file, never reveal it.
    previous = ETC / 'phone.htpasswd'
    backup = ETC / 'phone.htpasswd.before-first-login'
    if previous.exists() and not backup.exists():
        atomic(backup, previous.read_text(), 'root', 0o600)
    atomic(ETC / 'phone-first-login.json', json.dumps(state), 'fh6', 0o640)
    atomic(previous, USERNAME + ':!\n', 'www-data', 0o640)
    info = json.loads((ETC / 'deployment.json').read_text())
    secret = json.loads((ETC / 'home-assistant.json').read_text())['home_assistant']
    url = info['phoneUrl'].rstrip('/') + '/setup?key=' + token
    body = dict(title='FH6 — установите свой пароль',
                message='Логин: knsk45. Откройте одноразовую ссылку и задайте пароль сами. '
                        'Ссылка действует 24 часа. Пароль и ссылку не присылайте в чат.\n' + url,
                data=dict(tag='fh6-first-password', url=url))
    request = urllib.request.Request(
        secret['api_base_url'].rstrip('/') + '/services/notify/mobile_app_kns_iphone_15_pro_max',
        data=json.dumps(body, ensure_ascii=False).encode(), method='POST',
        headers={'Content-Type': 'application/json',
                 'Authorization': 'Bearer ' + secret['long_lived_access_tokens']['health_auto_export']['raw_token']})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError('Setup invitation was not accepted')
    print('FIRST_LOGIN_INVITATION=ACCEPTED USERNAME=knsk45')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'serve'])
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit('Root required')
    if args.action == 'prepare':
        prepare()
    else:
        serve()
