"""Install the owner Steam desktop; never enable the publication timer."""
import base64
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pwd
import shutil
import socket
import subprocess
import tempfile
import time

PAYLOAD = {'steam_desktop.py': {'data': 'IiIiRGVkaWNhdGVkIG93bmVyLWNvbnRyb2xsZWQgU3RlYW0gZGVza3RvcC4gTm8gY3JlZGVudGlhbCBsb2dnaW5nLiIiIgppbXBvcnQgb3MKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCmltcG9ydCBzZWNyZXRzCmltcG9ydCBzaWduYWwKaW1wb3J0IHNvY2tldAppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgdGltZQoKUE9SVFMgPSAoOTIyMiwgNTkwMSwgNjA4MSkKUFJPRklMRSA9IFBhdGgoJy92YXIvbGliL2ZoNi9zdGVhbS1icm93c2VyLXByb2ZpbGUnKQpSVU5USU1FID0gUGF0aCgnL3J1bi9maDYtc3RlYW0tZGVza3RvcCcpCgoKZGVmIGJyb3dzZXJfZW52aXJvbm1lbnQocHJvZmlsZSwgcnVudGltZSwgYXV0aCwgc291cmNlPU5vbmUpOgogICAgZW52aXJvbm1lbnQgPSBkaWN0KG9zLmVudmlyb24gaWYgc291cmNlIGlzIE5vbmUgZWxzZSBzb3VyY2UpCiAgICBmb3Iga2V5IGluICgnREJVU19TRVNTSU9OX0JVU19BRERSRVNTJywgJ0RCVVNfU1lTVEVNX0JVU19BRERSRVNTJyk6CiAgICAgICAgZW52aXJvbm1lbnQucG9wKGtleSwgTm9uZSkKICAgIGVudmlyb25tZW50LnVwZGF0ZShIT01FPXN0cihwcm9maWxlKSwgWERHX0NPTkZJR19IT01FPXN0cihwcm9maWxlLydjb25maWcnKSwKICAgICAgICAgICAgICAgICAgICAgICBYREdfQ0FDSEVfSE9NRT1zdHIocHJvZmlsZS8nY2FjaGUnKSwgWERHX1JVTlRJTUVfRElSPXN0cihydW50aW1lKSwKICAgICAgICAgICAgICAgICAgICAgICBESVNQTEFZPSc6OTEnLCBYQVVUSE9SSVRZPXN0cihhdXRoKSkKICAgIHJldHVybiBlbnZpcm9ubWVudAoKCmRlZiB3YWl0X3BvcnQocG9ydCwgcHJvY2Vzc2VzKToKICAgIGRlYWRsaW5lID0gdGltZS5tb25vdG9uaWMoKSArIDM1CiAgICB3aGlsZSB0aW1lLm1vbm90b25pYygpIDwgZGVhZGxpbmU6CiAgICAgICAgaWYgYW55KHAucG9sbCgpIGlzIG5vdCBOb25lIGZvciBwIGluIHByb2Nlc3Nlcyk6CiAgICAgICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcignQSBkZXNrdG9wIGNvbXBvbmVudCBleGl0ZWQgYmVmb3JlIHJlYWRpbmVzcycpCiAgICAgICAgdHJ5OgogICAgICAgICAgICB3aXRoIHNvY2tldC5jcmVhdGVfY29ubmVjdGlvbigoJzEyNy4wLjAuMScsIHBvcnQpLCB0aW1lb3V0PTAuMyk6CiAgICAgICAgICAgICAgICByZXR1cm4KICAgICAgICBleGNlcHQgT1NFcnJvcjoKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjIpCiAgICByYWlzZSBSdW50aW1lRXJyb3IoJ0Rlc2t0b3AgcmVhZGluZXNzIHRpbWVvdXQnKQoKCmRlZiBtYWluKCk6CiAgICBvcy51bWFzaygwbzA3NykKICAgIFBST0ZJTEUubWtkaXIobW9kZT0wbzcwMCwgcGFyZW50cz1UcnVlLCBleGlzdF9vaz1UcnVlKQogICAgaWYgUFJPRklMRS5pc19zeW1saW5rKCkgb3IgUFJPRklMRS5zdGF0KCkuc3RfdWlkICE9IG9zLmdldHVpZCgpOgogICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcignVW5leHBlY3RlZCBTdGVhbSBwcm9maWxlIG93bmVyc2hpcCcpCiAgICBQUk9GSUxFLmNobW9kKDBvNzAwKQogICAgZm9yIGZvbGRlciBpbiAoUFJPRklMRS8nY29uZmlnJywgUFJPRklMRS8nY2FjaGUnKToKICAgICAgICBpZiBmb2xkZXIuaXNfc3ltbGluaygpOgogICAgICAgICAgICByYWlzZSBSdW50aW1lRXJyb3IoJ1VuZXhwZWN0ZWQgYnJvd3NlciBkaXJlY3Rvcnkgc3ltbGluaycpCiAgICAgICAgZm9sZGVyLm1rZGlyKG1vZGU9MG83MDAsIGV4aXN0X29rPVRydWUpCiAgICAgICAgZm9sZGVyLmNobW9kKDBvNzAwKQogICAgYXV0aCA9IFJVTlRJTUUvJ1hhdXRob3JpdHknCiAgICBhdXRoLnRvdWNoKG1vZGU9MG82MDAsIGV4aXN0X29rPVRydWUpCiAgICBhdXRoLmNobW9kKDBvNjAwKQogICAgc3VicHJvY2Vzcy5ydW4oWycvdXNyL2Jpbi94YXV0aCcsICctZicsIHN0cihhdXRoKSwgJ3NvdXJjZScsICctJ10sCiAgICAgICAgICAgICAgICAgICBpbnB1dD1mJ2FkZCA6OTEgLiB7c2VjcmV0cy50b2tlbl9oZXgoMTYpfVxuJywgdGV4dD1UcnVlLAogICAgICAgICAgICAgICAgICAgc3Rkb3V0PXN1YnByb2Nlc3MuREVWTlVMTCwgc3RkZXJyPXN1YnByb2Nlc3MuREVWTlVMTCwgY2hlY2s9VHJ1ZSkKICAgIGNoaWxkcmVuID0gW10KCiAgICBkZWYgc3RhcnQoYXJncywgZW52PU5vbmUpOgogICAgICAgIGNoaWxkID0gc3VicHJvY2Vzcy5Qb3BlbihhcmdzLCBlbnY9ZW52LCBzdGRvdXQ9c3VicHJvY2Vzcy5ERVZOVUxMLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBzdGRlcnI9c3VicHJvY2Vzcy5ERVZOVUxMKQogICAgICAgIGNoaWxkcmVuLmFwcGVuZChjaGlsZCkKICAgICAgICByZXR1cm4gY2hpbGQKCiAgICBkZWYgc3RvcCgqXyk6CiAgICAgICAgcmFpc2UgS2V5Ym9hcmRJbnRlcnJ1cHQKCiAgICBzaWduYWwuc2lnbmFsKHNpZ25hbC5TSUdURVJNLCBzdG9wKQogICAgc2lnbmFsLnNpZ25hbChzaWduYWwuU0lHSU5ULCBzdG9wKQogICAgdHJ5OgogICAgICAgIHN0YXJ0KFsnL3Vzci9iaW4vWHZmYicsICc6OTEnLCAnLXNjcmVlbicsICcwJywgJzEyODB4OTAweDI0JywKICAgICAgICAgICAgICAgJy1ub2xpc3RlbicsICd0Y3AnLCAnLWF1dGgnLCBzdHIoYXV0aCksICctbm9yZXNldCddKQogICAgICAgIGVudmlyb25tZW50ID0gYnJvd3Nlcl9lbnZpcm9ubWVudChQUk9GSUxFLCBSVU5USU1FLCBhdXRoKQogICAgICAgIGRlYWRsaW5lID0gdGltZS5tb25vdG9uaWMoKSArIDE1CiAgICAgICAgd2hpbGUgbm90IFBhdGgoJy90bXAvLlgxMS11bml4L1g5MScpLmV4aXN0cygpOgogICAgICAgICAgICBpZiBjaGlsZHJlblswXS5wb2xsKCkgaXMgbm90IE5vbmUgb3IgdGltZS5tb25vdG9uaWMoKSA+IGRlYWRsaW5lOgogICAgICAgICAgICAgICAgcmFpc2UgUnVudGltZUVycm9yKCdEaXNwbGF5IHVuYXZhaWxhYmxlJykKICAgICAgICAgICAgdGltZS5zbGVlcCgwLjIpCiAgICAgICAgc3RhcnQoWycvdXNyL2Jpbi9jaHJvbWl1bScsICctLXVzZXItZGF0YS1kaXI9JytzdHIoUFJPRklMRSksCiAgICAgICAgICAgICAgICctLXJlbW90ZS1kZWJ1Z2dpbmctYWRkcmVzcz0xMjcuMC4wLjEnLCAnLS1yZW1vdGUtZGVidWdnaW5nLXBvcnQ9OTIyMicsCiAgICAgICAgICAgICAgICctLWRpc2FibGUtZGV2LXNobS11c2FnZScsICctLW5vLWZpcnN0LXJ1bicsICctLW5vLWRlZmF1bHQtYnJvd3Nlci1jaGVjaycsCiAgICAgICAgICAgICAgICctLXBhc3N3b3JkLXN0b3JlPWJhc2ljJywgJy0tZGlzYWJsZS1zYXZlLXBhc3N3b3JkLWJ1YmJsZScsCiAgICAgICAgICAgICAgICctLXdpbmRvdy1zaXplPTEyODAsOTAwJywKICAgICAgICAgICAgICAgJ2h0dHBzOi8vc3RlYW1jb21tdW5pdHkuY29tL3NoYXJlZGZpbGVzL2ZpbGVkZXRhaWxzLz9pZD0zNzg3NzM5NzMwJ10sIGVudmlyb25tZW50KQogICAgICAgIHdhaXRfcG9ydCg5MjIyLCBjaGlsZHJlbikKICAgICAgICBzdGFydChbJy91c3IvYmluL3gxMXZuYycsICctZGlzcGxheScsICc6OTEnLCAnLWF1dGgnLCBzdHIoYXV0aCksCiAgICAgICAgICAgICAgICctbG9jYWxob3N0JywgJy1yZmJwb3J0JywgJzU5MDEnLCAnLWZvcmV2ZXInLCAnLXNoYXJlZCcsICctbm9wdycsCiAgICAgICAgICAgICAgICctbm94ZGFtYWdlJywgJy1xdWlldCddLCBlbnZpcm9ubWVudCkKICAgICAgICB3YWl0X3BvcnQoNTkwMSwgY2hpbGRyZW4pCiAgICAgICAgc3RhcnQoWycvdXNyL2Jpbi93ZWJzb2NraWZ5JywgJy0td2ViJywgJy91c3Ivc2hhcmUvbm92bmMnLAogICAgICAgICAgICAgICAnMTI3LjAuMC4xOjYwODEnLCAnMTI3LjAuMC4xOjU5MDEnXSwgZW52aXJvbm1lbnQpCiAgICAgICAgd2FpdF9wb3J0KDYwODEsIGNoaWxkcmVuKQogICAgICAgIHByaW50KCdTVEVBTV9ERVNLVE9QX1JFQURZJywgZmx1c2g9VHJ1ZSkKICAgICAgICB3aGlsZSBhbGwocC5wb2xsKCkgaXMgTm9uZSBmb3IgcCBpbiBjaGlsZHJlbik6CiAgICAgICAgICAgIHRpbWUuc2xlZXAoMSkKICAgICAgICByYWlzZSBSdW50aW1lRXJyb3IoJ0Rlc2t0b3AgY29tcG9uZW50IHN0b3BwZWQnKQogICAgZXhjZXB0IEtleWJvYXJkSW50ZXJydXB0OgogICAgICAgIHBhc3MKICAgIGZpbmFsbHk6CiAgICAgICAgZm9yIGNoaWxkIGluIHJldmVyc2VkKGNoaWxkcmVuKToKICAgICAgICAgICAgaWYgY2hpbGQucG9sbCgpIGlzIE5vbmU6CiAgICAgICAgICAgICAgICBjaGlsZC50ZXJtaW5hdGUoKQogICAgICAgIGZvciBjaGlsZCBpbiBjaGlsZHJlbjoKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgY2hpbGQud2FpdCh0aW1lb3V0PTUpCiAgICAgICAgICAgIGV4Y2VwdCBzdWJwcm9jZXNzLlRpbWVvdXRFeHBpcmVkOgogICAgICAgICAgICAgICAgY2hpbGQua2lsbCgpCgoKaWYgX19uYW1lX18gPT0gJ19fbWFpbl9fJzoKICAgIG1haW4oKQo=', 'sha256': '7e203212d5b4fa9dc7c67322d678d7600156e38972b8a4a63a8b1dd5c3b12fee'}, 'steam_desktop_guard.py': {'data': 'IiIiSXNvbGF0ZSBkZWRpY2F0ZWQgYnJvd3NlciBwb3J0cyB3aXRob3V0IGNoYW5naW5nIG90aGVyIGZpcmV3YWxsIHRhYmxlcy4iIiIKaW1wb3J0IHB3ZAppbXBvcnQgc3VicHJvY2VzcwoKCmRlZiBydWxlcyhwdWJsaXNoZXIsIG5naW54LCBleGlzdHM9RmFsc2UpOgogICAgcHJlZml4ID0gJ2RlbGV0ZSB0YWJsZSBpbmV0IGZoNl9zdGVhbV9kZXNrdG9wXG4nIGlmIGV4aXN0cyBlbHNlICcnCiAgICByZXR1cm4gcHJlZml4ICsgZicnJ3RhYmxlIGluZXQgZmg2X3N0ZWFtX2Rlc2t0b3Age3sKIGNoYWluIGlucHV0IHt7CiAgdHlwZSBmaWx0ZXIgaG9vayBpbnB1dCBwcmlvcml0eSAtMTA7IHBvbGljeSBhY2NlcHQ7CiAgaWlmbmFtZSAhPSAibG8iIHRjcCBkcG9ydCB7eyA5MjIyLCA1OTAxLCA2MDgxIH19IGRyb3AKIH19CiBjaGFpbiBvdXRwdXQge3sKICB0eXBlIGZpbHRlciBob29rIG91dHB1dCBwcmlvcml0eSAtMTA7IHBvbGljeSBhY2NlcHQ7CiAgb2lmbmFtZSAibG8iIHRjcCBkcG9ydCB7eyA5MjIyLCA1OTAxIH19IG1ldGEgc2t1aWQgIT0ge3sgMCwge3B1Ymxpc2hlcn0gfX0gcmVqZWN0CiAgb2lmbmFtZSAibG8iIHRjcCBkcG9ydCA2MDgxIG1ldGEgc2t1aWQgIT0ge3sgMCwge3B1Ymxpc2hlcn0sIHtuZ2lueH0gfX0gcmVqZWN0CiB9fQp9fQonJycKCgpkZWYgbWFpbigpOgogICAgZXhpc3RzID0gc3VicHJvY2Vzcy5ydW4oWycvdXNyL3NiaW4vbmZ0JywgJ2xpc3QnLCAndGFibGUnLCAnaW5ldCcsICdmaDZfc3RlYW1fZGVza3RvcCddLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgc3Rkb3V0PXN1YnByb2Nlc3MuREVWTlVMTCwgc3RkZXJyPXN1YnByb2Nlc3MuREVWTlVMTCkucmV0dXJuY29kZSA9PSAwCiAgICBjb250ZW50ID0gcnVsZXMocHdkLmdldHB3bmFtKCdmaDYnKS5wd191aWQsIHB3ZC5nZXRwd25hbSgnd3d3LWRhdGEnKS5wd191aWQsIGV4aXN0cykKICAgIHN1YnByb2Nlc3MucnVuKFsnL3Vzci9zYmluL25mdCcsICctYycsICctZicsICctJ10sIGlucHV0PWNvbnRlbnQsIHRleHQ9VHJ1ZSwgY2hlY2s9VHJ1ZSkKICAgIHN1YnByb2Nlc3MucnVuKFsnL3Vzci9zYmluL25mdCcsICctZicsICctJ10sIGlucHV0PWNvbnRlbnQsIHRleHQ9VHJ1ZSwgY2hlY2s9VHJ1ZSkKICAgIHByaW50KCdTVEVBTV9ERVNLVE9QX1BPUlRfR1VBUkRfUkVBRFknKQoKCmlmIF9fbmFtZV9fID09ICdfX21haW5fXyc6CiAgICBtYWluKCkK', 'sha256': '2131b8ee4bc4744d2759e75e69070666c06e80acf6fcc399d462dd90b9de1d10'}, 'fh6-steam-desktop.service': {'data': 'W1VuaXRdCkRlc2NyaXB0aW9uPUZINiBvd25lci1jb250cm9sbGVkIFN0ZWFtIGJyb3dzZXIKUmVxdWlyZXM9Zmg2LXN0ZWFtLWRlc2t0b3AtZ3VhcmQuc2VydmljZQpBZnRlcj1uZXR3b3JrLW9ubGluZS50YXJnZXQgZmg2LXN0ZWFtLWRlc2t0b3AtZ3VhcmQuc2VydmljZQpCaW5kc1RvPWZoNi1zdGVhbS1kZXNrdG9wLWd1YXJkLnNlcnZpY2UKW1NlcnZpY2VdClR5cGU9c2ltcGxlClVzZXI9Zmg2Ckdyb3VwPWZoNgpSdW50aW1lRGlyZWN0b3J5PWZoNi1zdGVhbS1kZXNrdG9wClJ1bnRpbWVEaXJlY3RvcnlNb2RlPTA3MDAKVU1hc2s9MDA3NwpFeGVjU3RhcnQ9L3Vzci9iaW4vcHl0aG9uMyAvdXNyL2xvY2FsL2xpYi9maDYtYnJvd3Nlci9zdGVhbV9kZXNrdG9wLnB5ClJlc3RhcnQ9b24tZmFpbHVyZQpSZXN0YXJ0U2VjPTEwClRpbWVvdXRTdG9wU2VjPTIwCktpbGxNb2RlPWNvbnRyb2wtZ3JvdXAKTm9OZXdQcml2aWxlZ2VzPXRydWUKUHJvdGVjdFN5c3RlbT1mdWxsClByb3RlY3RIb21lPXRydWUKW0luc3RhbGxdCldhbnRlZEJ5PW11bHRpLXVzZXIudGFyZ2V0Cg==', 'sha256': '0e3ec458f6f159c22713c6dde89aceec942d5d51f8e2de986586de0bd16fe3de'}, 'fh6-steam-desktop-guard.service': {'data': 'W1VuaXRdCkRlc2NyaXB0aW9uPVByb3RlY3QgZGVkaWNhdGVkIEZINiBTdGVhbSBicm93c2VyIHBvcnRzCkJlZm9yZT1maDYtc3RlYW0tZGVza3RvcC5zZXJ2aWNlCltTZXJ2aWNlXQpUeXBlPW9uZXNob3QKRXhlY1N0YXJ0PS91c3IvYmluL3B5dGhvbjMgL3Vzci9sb2NhbC9saWIvZmg2LWJyb3dzZXIvc3RlYW1fZGVza3RvcF9ndWFyZC5weQpSZW1haW5BZnRlckV4aXQ9eWVzCltJbnN0YWxsXQpXYW50ZWRCeT1tdWx0aS11c2VyLnRhcmdldAo=', 'sha256': '906870a77e0b7ee5aa6e870d3b533e7abff4027302f81b0a20d4e30cf891ef03'}}
NGINX_EXPECTED = 'server {\n    listen 8443 ssl;\n    server_name _;\n    ssl_certificate /etc/fh6/phone.crt;\n    ssl_certificate_key /etc/fh6/phone.key;\n    ssl_protocols TLSv1.2 TLSv1.3;\n    auth_basic "FH6 private";\n    auth_basic_user_file /etc/fh6/phone.htpasswd;\n    access_log off;\n    client_max_body_size 20m;\n    location = /setup {\n        auth_basic off;\n        access_log off;\n        error_log /dev/null;\n        client_max_body_size 4k;\n        proxy_pass http://127.0.0.1:8765;\n        proxy_set_header Host $http_host;\n        proxy_set_header X-Forwarded-Proto https;\n    }\n    location / {\n        proxy_pass http://127.0.0.1:8765;\n        proxy_set_header Host $http_host;\n        proxy_set_header X-Forwarded-Proto https;\n    }\n}\n'
NGINX_BLOCK = '''    location ^~ /steam-browser/ {
        proxy_pass http://127.0.0.1:6081/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $http_host;
        proxy_read_timeout 3600s;
        proxy_buffering off;
    }
'''
UNITS = ['fh6-steam-desktop-guard.service', 'fh6-steam-desktop.service']


def run(args, **kwargs):
    return subprocess.run(args, check=True, timeout=45, **kwargs)


def replace(path, raw, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.fh6-browser-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchmod(stream.fileno(), mode)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def nginx_file():
    config = subprocess.check_output(['/usr/sbin/nginx', '-T'], stderr=subprocess.DEVNULL, text=True)
    paths = []
    for line in config.splitlines():
        if line.startswith('# configuration file /etc/nginx/') and line.endswith(':'):
            path = Path(line[len('# configuration file '):-1]).resolve()
            if path not in paths and 'listen 8443 ssl;' in path.read_text():
                paths.append(path)
    if len(paths) != 1:
        raise RuntimeError('Expected exactly one panel configuration; nothing changed')
    path = paths[0]
    old = path.read_text()
    if old.strip() != NGINX_EXPECTED.strip():
        raise RuntimeError('Unknown panel configuration; nothing changed')
    return path, old.encode()


def check_port(port, user, allowed):
    code = ('import socket,sys;\ntry:\n'
            f' s=socket.create_connection(("127.0.0.1",{port}),timeout=2);s.close()\n'
            'except OSError:sys.exit(1)\n')
    result = subprocess.run(['/usr/sbin/runuser', '-u', user, '--', '/usr/bin/python3', '-c', code], timeout=5)
    if (result.returncode == 0) != allowed:
        raise RuntimeError(f'Port isolation check failed: {user}, {port}')


def main():
    if os.geteuid() != 0 or socket.gethostname() != 'fh6-collector':
        raise RuntimeError('Run only inside CT109')
    if len(PAYLOAD) != 4 or not NGINX_EXPECTED:
        raise RuntimeError('Installer payload is incomplete; nothing changed')
    for command in ['Xvfb', 'xauth', 'x11vnc', 'websockify', 'chromium', 'nft', 'nginx']:
        if shutil.which(command) is None:
            raise RuntimeError('Missing dependency: '+command)
    if not Path('/usr/share/novnc/vnc.html').is_file():
        raise RuntimeError('Missing noVNC application')
    owner = pwd.getpwnam('fh6'); nginx = pwd.getpwnam('www-data'); pwd.getpwnam('fh6-editor')
    store = Path('/var/lib/fh6')
    with (store/'runner.lock').open('a+b') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX|fcntl.LOCK_NB)
        for unit in UNITS + ['fh6-steam.service', 'fh6-steam.timer']:
            if subprocess.run(['systemctl', 'is-active', '--quiet', unit]).returncode == 0:
                raise RuntimeError('Browser or publication already active; nothing changed')
        for port in (9222, 5901, 6081):
            try:
                with socket.create_connection(('127.0.0.1', port), timeout=0.3):
                    raise RuntimeError('Reserved browser port already occupied; nothing changed')
            except OSError:
                pass
        path, old = nginx_file()
        if subprocess.run(['/usr/sbin/nft', 'list', 'table', 'inet', 'fh6_steam_desktop'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            raise RuntimeError('Existing browser firewall table; nothing changed')
        plans = []
        for name, item in PAYLOAD.items():
            raw = base64.b64decode(item['data'], validate=True)
            if hashlib.sha256(raw).hexdigest() != item['sha256']:
                raise RuntimeError('Payload mismatch; nothing changed')
            if name.endswith('.py'):
                compile(raw, name, 'exec')
            target = (Path('/etc/systemd/system')/name if name.endswith('.service')
                      else Path('/usr/local/lib/fh6-browser')/name)
            if target.exists() or target.is_symlink():
                raise RuntimeError('Existing browser file; nothing changed: '+str(target))
            plans.append((target, raw))
        guard = next(raw for target, raw in plans if target.name == 'steam_desktop_guard.py')
        scope = {'__name__': 'checked_rules'};exec(compile(guard,'guard','exec'),scope)
        run(['/usr/sbin/nft', '-c', '-f', '-'], input=scope['rules'](owner.pw_uid, nginx.pw_uid), text=True)
        profile = store/'steam-browser-profile'
        if profile.exists() or profile.is_symlink():
            raise RuntimeError('Existing browser profile; nothing changed')
        backup = store/'repairs'/('steam-desktop-'+str(time.time_ns()))
        backup.mkdir(parents=True, mode=0o700)
        (backup/'nginx.conf').write_bytes(old)
        (backup/'metadata.json').write_text(json.dumps({'nginxPath':str(path),'newFiles':[str(p) for p,_ in plans]}))
        applied=[]
        try:
            profile.mkdir(mode=0o700);os.chown(profile, owner.pw_uid, owner.pw_gid)
            for target,raw in plans:
                replace(target,raw);applied.append(target)
            for parent in [Path('/usr/local/lib/fh6-browser')]:
                if parent.stat().st_uid != 0 or parent.stat().st_mode & 0o022:
                    raise RuntimeError('Browser code directory is writable by other users')
            run(['systemd-analyze','verify',*[str(Path('/etc/systemd/system')/u) for u in UNITS]])
            run(['systemctl','daemon-reload'])
            run(['systemctl','start',UNITS[0]])
            run(['systemctl','start',UNITS[1]])
            deadline=time.monotonic()+60
            while time.monotonic()<deadline:
                try:
                    with socket.create_connection(('127.0.0.1',6081),timeout=0.5):break
                except OSError:time.sleep(0.5)
            else:raise RuntimeError('Browser did not become ready; inspect desktop service')
            for port in (9222,5901):
                check_port(port,'fh6',True);check_port(port,'fh6-editor',False);check_port(port,'www-data',False)
            check_port(6081,'www-data',True);check_port(6081,'fh6-editor',False)
            if subprocess.run(['/usr/sbin/runuser','-u','fh6-editor','--','test','-r',str(profile)],timeout=5).returncode==0:
                raise RuntimeError('Editor can read Steam profile')
            updated=old.decode().replace('    location / {',NGINX_BLOCK+'    location / {',1)
            if updated==old.decode():raise RuntimeError('Panel insertion point not found')
            replace(path,updated.encode())
            run(['/usr/sbin/nginx','-t']);run(['systemctl','reload','nginx'])
            run(['systemctl','enable',*UNITS])
        except BaseException:
            subprocess.run(['systemctl','stop',*reversed(UNITS)],timeout=30)
            subprocess.run(['systemctl','disable',*UNITS],timeout=30)
            replace(path,old)
            subprocess.run(['/usr/sbin/nginx','-t'],timeout=15)
            subprocess.run(['systemctl','reload','nginx'],timeout=15)
            for target in applied:target.unlink(missing_ok=True)
            subprocess.run(['systemctl','daemon-reload'],timeout=30)
            # The reserved-port rules deliberately stay in place after a failure.
            # No owner has been asked to authenticate; preserve any profile for inspection.
            raise
    print('FH6_STEAM_DESKTOP_READY publication=disabled; editor access denied; browser sandbox retained')
    print('OPEN=https://fh6.knsk45.crazedns.ru/steam-browser/vnc.html?autoconnect=1&resize=scale&path=steam-browser/websockify')
    print('BACKUP='+str(backup))


if __name__ == '__main__':
    main()
