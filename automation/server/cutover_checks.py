"""Nonmutating checks; no password or device-code output."""
import urllib.request
import urllib.error
import json
from pathlib import Path
import ssl
import subprocess

root=Path('/opt/fh6/repo')
info=json.loads(Path('/etc/fh6/deployment.json').read_text())
context=ssl.create_default_context(cafile='/etc/fh6/phone.crt')
try:urllib.request.urlopen(info['phoneUrl'],context=context,timeout=10)
except urllib.error.HTTPError as error:
    if error.code!=401:raise
else:raise RuntimeError('Private UI is not authentication protected')
print('PHONE_UNAUTHENTICATED=401')
with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=10) as response:
    if response.status!=200:raise RuntimeError('Phone backend unavailable')
print('PHONE_BACKEND=OK')
for file in [root/'automation/runs/steam-publication-state.json',root/'automation/runs/steam-publication-state-en.json',root/'automation/runs/publication-metrics-state.json']:
    json.loads(file.read_text(encoding='utf-8-sig'))
print('MIGRATED_BASELINES=READABLE')
status=subprocess.run(['runuser','-u','fh6-editor','--','/usr/local/bin/codex','login','status'],capture_output=True)
print('EDITOR_AUTH='+('READY' if status.returncode==0 else 'OWNER_LOGIN_REQUIRED'))
print('CUTOVER_CHECKS=PASSED')
