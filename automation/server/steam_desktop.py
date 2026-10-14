"""Dedicated owner-controlled Steam desktop. No credential logging."""
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import time

PORTS = (9222, 5901, 6081)
PROFILE = Path('/var/lib/fh6/steam-browser-profile')
RUNTIME = Path('/run/fh6-steam-desktop')


def wait_port(port, processes):
    deadline = time.monotonic() + 35
    while time.monotonic() < deadline:
        if any(p.poll() is not None for p in processes):
            raise RuntimeError('A desktop component exited before readiness')
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.3):
                return
        except OSError:
            time.sleep(0.2)
    raise RuntimeError('Desktop readiness timeout')


def main():
    os.umask(0o077)
    PROFILE.mkdir(mode=0o700, parents=True, exist_ok=True)
    if PROFILE.is_symlink() or PROFILE.stat().st_uid != os.getuid():
        raise RuntimeError('Unexpected Steam profile ownership')
    PROFILE.chmod(0o700)
    auth = RUNTIME/'Xauthority'
    auth.touch(mode=0o600, exist_ok=True)
    auth.chmod(0o600)
    subprocess.run(['/usr/bin/xauth', '-f', str(auth), 'source', '-'],
                   input=f'add :91 . {secrets.token_hex(16)}\n', text=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    children = []

    def start(args, env=None):
        child = subprocess.Popen(args, env=env, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        children.append(child)
        return child

    def stop(*_):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        start(['/usr/bin/Xvfb', ':91', '-screen', '0', '1280x900x24',
               '-nolisten', 'tcp', '-auth', str(auth), '-noreset'])
        environment = dict(os.environ, DISPLAY=':91', XAUTHORITY=str(auth))
        deadline = time.monotonic() + 15
        while not Path('/tmp/.X11-unix/X91').exists():
            if children[0].poll() is not None or time.monotonic() > deadline:
                raise RuntimeError('Display unavailable')
            time.sleep(0.2)
        start(['/usr/bin/chromium', '--user-data-dir='+str(PROFILE),
               '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=9222',
               '--disable-dev-shm-usage', '--no-first-run', '--no-default-browser-check',
               '--password-store=basic', '--disable-save-password-bubble',
               '--window-size=1280,900',
               'https://steamcommunity.com/sharedfiles/filedetails/?id=3787739730'], environment)
        wait_port(9222, children)
        start(['/usr/bin/x11vnc', '-display', ':91', '-auth', str(auth),
               '-localhost', '-rfbport', '5901', '-forever', '-shared', '-nopw',
               '-noxdamage', '-quiet'], environment)
        wait_port(5901, children)
        start(['/usr/bin/websockify', '--web', '/usr/share/novnc',
               '127.0.0.1:6081', '127.0.0.1:5901'], environment)
        wait_port(6081, children)
        print('STEAM_DESKTOP_READY', flush=True)
        while all(p.poll() is None for p in children):
            time.sleep(1)
        raise RuntimeError('Desktop component stopped')
    except KeyboardInterrupt:
        pass
    finally:
        for child in reversed(children):
            if child.poll() is None:
                child.terminate()
        for child in children:
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()


if __name__ == '__main__':
    main()
