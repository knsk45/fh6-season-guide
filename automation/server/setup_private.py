"""Create private web credentials and deliver them directly to owner's HA phone.

Never print credentials. Re-running must not rotate a password or send another
setup push. A failure leaves the unsent payload in a private local file for retry.
"""
from pathlib import Path
import json
import secrets
import subprocess
import urllib.request
import os

etc=Path('/etc/fh6')
secret=json.loads((etc/'home-assistant.json').read_text())['home_assistant']
web=etc/'phone.htpasswd'
payload=etc/'setup-notification.json'
sent=etc/'setup-delivered'
if not web.exists():
    password=secrets.token_urlsafe(22)
    hashed=subprocess.run(['openssl','passwd','-6','-stdin'],input=password+'\n',text=True,capture_output=True,check=True).stdout.strip()
    web.write_text('kns:'+hashed+'\n')
    os.chmod(web,0o640)
    subprocess.run(['chown','root:www-data',str(web)],check=True)
    info=json.loads((etc/'deployment.json').read_text())
    certificate=subprocess.run(['openssl','x509','-in',str(etc/'phone.crt'),'-noout','-fingerprint','-sha256'],text=True,capture_output=True,check=True).stdout.strip()
    data={'title':'FH6 — сервер готов к входу','message':f"Закрытая страница: {info['phoneUrl']}\nЛогин: kns\nПароль: {password}\nСамоподписанный сертификат, сверьте SHA256: {certificate}\nДля входа редактора нажмите кнопку Codex. Пароль и код не присылайте в чат.",
          'data':{'tag':'fh6-server-setup','url':info['phoneUrl']}}
    payload.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');os.chmod(payload,0o600)
if not sent.exists():
    api=secret['api_base_url'].rstrip('/')
    request=urllib.request.Request(api+'/services/notify/mobile_app_kns_iphone_15_pro_max',data=payload.read_bytes(),headers={'Authorization':'Bearer '+secret['long_lived_access_tokens']['health_auto_export']['raw_token'],'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(request,timeout=30) as response:
        if response.status!=200:raise RuntimeError('HA setup delivery not accepted')
    sent.touch();payload.unlink()
    print('PHONE_SETUP_NOTIFICATION=ACCEPTED')
else:print('PHONE_SETUP_NOTIFICATION=ALREADY_ACCEPTED')
