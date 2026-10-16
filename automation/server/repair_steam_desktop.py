"""Resume interrupted desktop installation with private writable Chrome paths."""
import base64
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pwd
import socket
import subprocess
import time
import types
import urllib.request

BASE_URL = ('https://raw.githubusercontent.com/knsk45/fh6-season-guide/'
            '38ae9bc076a7eb5e773fcd23ac80770c8dfa6aee/'
            'automation/server/install_steam_desktop.py')
BASE_SHA = 'f0025e7425859dacb7735383a58f18e9c2ed1f6b13834c8012dcd5f86eb39a78'
UPDATED = {'data': 'IiIiRGVkaWNhdGVkIG93bmVyLWNvbnRyb2xsZWQgU3RlYW0gZGVza3RvcC4gTm8gY3JlZGVudGlhbCBsb2dnaW5nLiIiIgppbXBvcnQgb3MKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCmltcG9ydCBzZWNyZXRzCmltcG9ydCBzaWduYWwKaW1wb3J0IHNvY2tldAppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgdGltZQoKUE9SVFMgPSAoOTIyMiwgNTkwMSwgNjA4MSkKUFJPRklMRSA9IFBhdGgoJy92YXIvbGliL2ZoNi9zdGVhbS1icm93c2VyLXByb2ZpbGUnKQpSVU5USU1FID0gUGF0aCgnL3J1bi9maDYtc3RlYW0tZGVza3RvcCcpCgoKZGVmIGJyb3dzZXJfZW52aXJvbm1lbnQocHJvZmlsZSwgcnVudGltZSwgYXV0aCwgc291cmNlPU5vbmUpOgogICAgZW52aXJvbm1lbnQgPSBkaWN0KG9zLmVudmlyb24gaWYgc291cmNlIGlzIE5vbmUgZWxzZSBzb3VyY2UpCiAgICBmb3Iga2V5IGluICgnREJVU19TRVNTSU9OX0JVU19BRERSRVNTJywgJ0RCVVNfU1lTVEVNX0JVU19BRERSRVNTJyk6CiAgICAgICAgZW52aXJvbm1lbnQucG9wKGtleSwgTm9uZSkKICAgIGVudmlyb25tZW50LnVwZGF0ZShIT01FPXN0cihwcm9maWxlKSwgWERHX0NPTkZJR19IT01FPXN0cihwcm9maWxlLydjb25maWcnKSwKICAgICAgICAgICAgICAgICAgICAgICBYREdfQ0FDSEVfSE9NRT1zdHIocHJvZmlsZS8nY2FjaGUnKSwgWERHX1JVTlRJTUVfRElSPXN0cihydW50aW1lKSwKICAgICAgICAgICAgICAgICAgICAgICBESVNQTEFZPSc6OTEnLCBYQVVUSE9SSVRZPXN0cihhdXRoKSkKICAgIHJldHVybiBlbnZpcm9ubWVudAoKCmRlZiB3YWl0X3BvcnQocG9ydCwgcHJvY2Vzc2VzKToKICAgIGRlYWRsaW5lID0gdGltZS5tb25vdG9uaWMoKSArIDM1CiAgICB3aGlsZSB0aW1lLm1vbm90b25pYygpIDwgZGVhZGxpbmU6CiAgICAgICAgaWYgYW55KHAucG9sbCgpIGlzIG5vdCBOb25lIGZvciBwIGluIHByb2Nlc3Nlcyk6CiAgICAgICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcignQSBkZXNrdG9wIGNvbXBvbmVudCBleGl0ZWQgYmVmb3JlIHJlYWRpbmVzcycpCiAgICAgICAgdHJ5OgogICAgICAgICAgICB3aXRoIHNvY2tldC5jcmVhdGVfY29ubmVjdGlvbigoJzEyNy4wLjAuMScsIHBvcnQpLCB0aW1lb3V0PTAuMyk6CiAgICAgICAgICAgICAgICByZXR1cm4KICAgICAgICBleGNlcHQgT1NFcnJvcjoKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjIpCiAgICByYWlzZSBSdW50aW1lRXJyb3IoJ0Rlc2t0b3AgcmVhZGluZXNzIHRpbWVvdXQnKQoKCmRlZiBtYWluKCk6CiAgICBvcy51bWFzaygwbzA3NykKICAgIFBST0ZJTEUubWtkaXIobW9kZT0wbzcwMCwgcGFyZW50cz1UcnVlLCBleGlzdF9vaz1UcnVlKQogICAgaWYgUFJPRklMRS5pc19zeW1saW5rKCkgb3IgUFJPRklMRS5zdGF0KCkuc3RfdWlkICE9IG9zLmdldHVpZCgpOgogICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcignVW5leHBlY3RlZCBTdGVhbSBwcm9maWxlIG93bmVyc2hpcCcpCiAgICBQUk9GSUxFLmNobW9kKDBvNzAwKQogICAgZm9yIGZvbGRlciBpbiAoUFJPRklMRS8nY29uZmlnJywgUFJPRklMRS8nY2FjaGUnKToKICAgICAgICBpZiBmb2xkZXIuaXNfc3ltbGluaygpOgogICAgICAgICAgICByYWlzZSBSdW50aW1lRXJyb3IoJ1VuZXhwZWN0ZWQgYnJvd3NlciBkaXJlY3Rvcnkgc3ltbGluaycpCiAgICAgICAgZm9sZGVyLm1rZGlyKG1vZGU9MG83MDAsIGV4aXN0X29rPVRydWUpCiAgICAgICAgZm9sZGVyLmNobW9kKDBvNzAwKQogICAgYXV0aCA9IFJVTlRJTUUvJ1hhdXRob3JpdHknCiAgICBhdXRoLnRvdWNoKG1vZGU9MG82MDAsIGV4aXN0X29rPVRydWUpCiAgICBhdXRoLmNobW9kKDBvNjAwKQogICAgc3VicHJvY2Vzcy5ydW4oWycvdXNyL2Jpbi94YXV0aCcsICctZicsIHN0cihhdXRoKSwgJ3NvdXJjZScsICctJ10sCiAgICAgICAgICAgICAgICAgICBpbnB1dD1mJ2FkZCA6OTEgLiB7c2VjcmV0cy50b2tlbl9oZXgoMTYpfVxuJywgdGV4dD1UcnVlLAogICAgICAgICAgICAgICAgICAgc3Rkb3V0PXN1YnByb2Nlc3MuREVWTlVMTCwgc3RkZXJyPXN1YnByb2Nlc3MuREVWTlVMTCwgY2hlY2s9VHJ1ZSkKICAgIGNoaWxkcmVuID0gW10KCiAgICBkZWYgc3RhcnQoYXJncywgZW52PU5vbmUpOgogICAgICAgIGNoaWxkID0gc3VicHJvY2Vzcy5Qb3BlbihhcmdzLCBlbnY9ZW52LCBzdGRvdXQ9c3VicHJvY2Vzcy5ERVZOVUxMLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzdGRlcnI9c3VicHJvY2Vzcy5ERVZOVUxMKQogICAgICAgIGNoaWxkcmVuLmFwcGVuZChjaGlsZCkKICAgICAgICByZXR1cm4gY2hpbGQKCiAgICBkZWYgc3RvcCgqXyk6CiAgICAgICAgcmFpc2UgS2V5Ym9hcmRJbnRlcnJ1cHQKCiAgICBzaWduYWwuc2lnbmFsKHNpZ25hbC5TSUdURVJNLCBzdG9wKQogICAgc2lnbmFsLnNpZ25hbChzaWduYWwuU0lHSU5ULCBzdG9wKQogICAgdHJ5OgogICAgICAgIHN0YXJ0KFsnL3Vzci9iaW4vWHZmYicsICc6OTEnLCAnLXNjcmVlbicsICcwJywgJzEyODB4OTAweDI0JywKICAgICAgICAgICAgICAgJy1ub2xpc3RlbicsICd0Y3AnLCAnLWF1dGgnLCBzdHIoYXV0aCksICctbm9yZXNldCddKQogICAgICAgIGVudmlyb25tZW50ID0gYnJvd3Nlcl9lbnZpcm9ubWVudChQUk9GSUxFLCBSVU5USU1FLCBhdXRoKQogICAgICAgIGRlYWRsaW5lID0gdGltZS5tb25vdG9uaWMoKSArIDE1CiAgICAgICAgd2hpbGUgbm90IFBhdGgoJy90bXAvLlgxMS11bml4L1g5MScpLmV4aXN0cygpOgogICAgICAgICAgICBpZiBjaGlsZHJlblswXS5wb2xsKCkgaXMgbm90IE5vbmUgb3IgdGltZS5tb25vdG9uaWMoKSA+IGRlYWRsaW5lOgogICAgICAgICAgICAgICAgcmFpc2UgUnVudGltZUVycm9yKCdEaXNwbGF5IHVuYXZhaWxhYmxlJykKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjIpCiAgICAgICAgc3RhcnQoWycvdXNyL2Jpbi9jaHJvbWl1bScsICctLXVzZXItZGF0YS1kaXI9JytzdHIoUFJPRklMRSksCiAgICAgICAgICAgICAgICctLXJlbW90ZS1kZWJ1Z2dpbmctYWRkcmVzcz0xMjcuMC4wLjEnLCAnLS1yZW1vdGUtZGVidWdnaW5nLXBvcnQ9OTIyMicsCiAgICAgICAgICAgICAgICctLWRpc2FibGUtZGV2LXNobS11c2FnZScsICctLW5vLWZpcnN0LXJ1bicsICctLW5vLWRlZmF1bHQtYnJvd3Nlci1jaGVjaycsCiAgICAgICAgICAgICAgICctLXBhc3N3b3JkLXN0b3JlPWJhc2ljJywgJy0tZGlzYWJsZS1zYXZlLXBhc3N3b3JkLWJ1YmJsZScsCiAgICAgICAgICAgICAgICctLXdpbmRvdy1zaXplPTEyODAsOTAwJywKICAgICAgICAgICAgICAgJ2h0dHBzOi8vc3RlYW1jb21tdW5pdHkuY29tL3NoYXJlZGZpbGVzL2ZpbGVkZXRhaWxzLz9pZD0zNzg3NzM5NzMwJ10sIGVudmlyb25tZW50KQogICAgICAgIHdhaXRfcG9ydCg5MjIyLCBjaGlsZHJlbikKICAgICAgICBzdGFydChbJy91c3IvYmluL3gxMXZuYycsICctZGlzcGxheScsICc6OTEnLCAnLWF1dGgnLCBzdHIoYXV0aCksCiAgICAgICAgICAgICAgICctbG9jYWxob3N0JywgJy1yZmJwb3J0JywgJzU5MDEnLCAnLWZvcmV2ZXInLCAnLXNoYXJlZCcsICctbm9wdycsCiAgICAgICAgICAgICAgICctbm94ZGFtYWdlJywgJy1xdWlldCddLCBlbnZpcm9ubWVudCkKICAgICAgICB3YWl0X3BvcnQoNTkwMSwgY2hpbGRyZW4pCiAgICAgICAgc3RhcnQoWycvdXNyL2Jpbi93ZWJzb2NraWZ5JywgJy0td2ViJywgJy91c3Ivc2hhcmUvbm92bmMnLAogICAgICAgICAgICAgICAnMTI3LjAuMC4xOjYwODEnLCAnMTI3LjAuMC4xOjU5MDEnXSwgZW52aXJvbm1lbnQpCiAgICAgICAgd2FpdF9wb3J0KDYwODEsIGNoaWxkcmVuKQogICAgICAgIHByaW50KCdTVEVBTV9ERVNLVE9QX1JFQURZJywgZmx1c2g9VHJ1ZSkKICAgICAgICB3aGlsZSBhbGwocC5wb2xsKCkgaXMgTm9uZSBmb3IgcCBpbiBjaGlsZHJlbik6CiAgICAgICAgICAgIHRpbWUuc2xlZXAoMSkKICAgICAgICByYWlzZSBSdW50aW1lRXJyb3IoJ0Rlc2t0b3AgY29tcG9uZW50IHN0b3BwZWQnKQogICAgZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgogICAgICAgIHBhc3MKICAgIGZpbmFsbHk6CiAgICAgICAgZm9yIGNoaWxkIGluIHJldmVyc2VkKGNoaWxkcmVuKToKICAgICAgICAgICAgaWYgY2hpbGQucG9sbCgpIGlzIE5vbmU6CiAgICAgICAgICAgICAgICBjaGlsZC50ZXJtaW5hdGUoKQogICAgICAgIGZvciBjaGlsZCBpbiBjaGlsZHJlbjoKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgY2hpbGQud2FpdCh0aW1lb3V0PTUpCiAgICAgICAgICAgIGV4Y2VwdCBzdWJwcm9jZXNzLlRpbWVvdXRFeHBpcmVkOgogICAgICAgICAgICAgICAgY2hpbGQua2lsbCgpCgoKaWYgX19uYW1lX18gPT0gJ19fbWFpbl9fJzoKICAgIG1haW4oKQo=', 'sha256': '7e203212d5b4fa9dc7c67322d678d7600156e38972b8a4a63a8b1dd5c3b12fee'}


def main():
    if os.geteuid()!=0 or socket.gethostname()!='fh6-collector':
        raise RuntimeError('Run only inside CT109')
    with urllib.request.urlopen(BASE_URL,timeout=30) as response:raw=response.read(100000)
    if hashlib.sha256(raw).hexdigest()!=BASE_SHA:raise RuntimeError('Pinned installer mismatch')
    base=types.ModuleType('reviewed_desktop');exec(compile(raw,BASE_URL,'exec'),base.__dict__)
    content=base64.b64decode(UPDATED['data'],validate=True)
    if hashlib.sha256(content).hexdigest()!=UPDATED['sha256']:raise RuntimeError('Repair payload mismatch')
    compile(content,'steam_desktop.py','exec')
    store=Path('/var/lib/fh6');runtime=Path('/usr/local/lib/fh6-browser/steam_desktop.py')
    with (store/'runner.lock').open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        for unit in ('fh6-steam.service','fh6-steam.timer'):
            if subprocess.run(['systemctl','is-active','--quiet',unit]).returncode==0:
                raise RuntimeError('Publication active; nothing changed')
        if json.loads(Path('/etc/fh6/steam-browser.json').read_text()).get('publishEnabled') is True:
            raise RuntimeError('Publication enabled; nothing changed')
        for name,item in base.PAYLOAD.items():
            target=Path('/etc/systemd/system')/name if name.endswith('.service') else runtime.parent/name
            accepted={item['sha256']}
            if name=='steam_desktop.py':accepted.add(UPDATED['sha256'])
            if (target.is_symlink() or not target.is_file() or target.stat().st_uid!=0
                    or target.stat().st_mode&0o022 or hashlib.sha256(target.read_bytes()).hexdigest() not in accepted):
                raise RuntimeError('Unknown interrupted installation file: '+name)
        if runtime.parent.stat().st_uid!=0 or runtime.parent.stat().st_mode&0o022:
            raise RuntimeError('Unexpected browser code directory permissions')
        owner=pwd.getpwnam('fh6');profile=store/'steam-browser-profile'
        if profile.is_symlink() or not profile.is_dir() or profile.stat().st_uid!=owner.pw_uid or profile.stat().st_mode&0o077:
            raise RuntimeError('Unexpected private profile permissions')
        original=base.NGINX_EXPECTED
        updated=original.replace('    location / {',base.NGINX_BLOCK+'    location / {',1)
        try:path,nginx_before=base.nginx_file()
        except RuntimeError:
            base.NGINX_EXPECTED=updated;path,nginx_before=base.nginx_file()
        backup=store/'repairs'/('steam-desktop-environment-'+str(time.time_ns()))
        backup.mkdir(parents=True,mode=0o700)
        (backup/'steam_desktop.py').write_bytes(runtime.read_bytes())
        (backup/'nginx.conf').write_bytes(nginx_before)
        base.run(['systemctl','stop','fh6-steam-desktop.service'])
        base.replace(runtime,content)
        try:
            base.run(['systemctl','restart','fh6-steam-desktop-guard.service'])
            base.run(['systemctl','start','fh6-steam-desktop.service'])
            deadline=time.monotonic()+60
            while time.monotonic()<deadline:
                try:
                    with socket.create_connection(('127.0.0.1',6081),timeout=0.5):break
                except OSError:time.sleep(0.5)
            else:raise RuntimeError('Desktop not ready; no owner route enabled')
            for port in (9222,5901):
                base.check_port(port,'fh6',True);base.check_port(port,'fh6-editor',False);base.check_port(port,'www-data',False)
            base.check_port(6081,'www-data',True);base.check_port(6081,'fh6-editor',False)
            if subprocess.run(['/usr/sbin/runuser','-u','fh6-editor','--','test','-r',str(profile)],timeout=5).returncode==0:
                raise RuntimeError('Editor can read Steam profile')
            base.replace(path,updated.encode())
            base.run(['/usr/sbin/nginx','-t']);base.run(['systemctl','reload','nginx'])
            base.run(['systemctl','enable',*base.UNITS])
        except BaseException:
            subprocess.run(['systemctl','stop','fh6-steam-desktop.service'],timeout=30)
            base.replace(path,nginx_before)
            subprocess.run(['/usr/sbin/nginx','-t'],timeout=15)
            subprocess.run(['systemctl','reload','nginx'],timeout=15)
            raise
    print('FH6_STEAM_DESKTOP_READY publication=disabled; editor access denied; private Chrome environment verified')
    print('BACKUP='+str(backup))


if __name__=='__main__':main()
