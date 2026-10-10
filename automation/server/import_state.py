"""One-time migration, verify bytes first and retain original path-bearing journals."""
import json
from pathlib import Path
import hashlib
import shutil
import os
import sys

source=Path(sys.argv[1]).resolve()
root=Path('/opt/fh6/repo')
target=root/'automation/runs'
manifest=json.loads((source/'manifest.json').read_text(encoding='utf-8-sig'))
for relative,wanted in manifest['files'].items():
    file=(source/relative).resolve()
    if not file.is_relative_to(source) or hashlib.sha256(file.read_bytes()).hexdigest()!=wanted:
        raise RuntimeError('Migration SHA mismatch: '+relative)
if (target/'refresh/active.json').exists():raise RuntimeError('Server already has a run; do not overwrite it')
for name in ['steam-publication-state.json','steam-publication-state-en.json','publication-metrics-state.json','home-assistant-notification-state.json']:
    if (source/name).exists():
        target.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/name,target/name)
shutil.copytree(source/'refresh',target/'refresh')
old=manifest['sourceRoot']
def relocate(value):
    if isinstance(value,dict):return {relocate(k):relocate(v) for k,v in value.items()}
    if isinstance(value,list):return [relocate(v) for v in value]
    if isinstance(value,str) and value.startswith(old+'\\'):
        return str(root/Path(value[len(old)+1:].replace('\\','/')))
    return value
active=target/'refresh/active.json'
shutil.copyfile(active,active.with_name('migration-original-active.json'))
run=relocate(json.loads(active.read_text(encoding='utf-8-sig')))
run['migration']={'sourceRoot':old,'targetRoot':str(root),'evidenceBytesPreserved':True}
for file in [active,target/'refresh'/run['runId']/'run.json']:
    file.write_text(json.dumps(run,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(source/'home-assistant.json','/etc/fh6/home-assistant.json')
os.chmod('/etc/fh6/home-assistant.json',0o600);shutil.chown('/etc/fh6/home-assistant.json','fh6','fh6')
(target/'home-assistant-notification.local.json').write_text(json.dumps({'schemaVersion':1,'homeAssistantSecretPath':'/etc/fh6/home-assistant.json','notifyService':'notify.mobile_app_kns_iphone_15_pro_max'}),encoding='utf-8')
shutil.chown(target,'fh6','fh6')
for file in target.rglob('*'):
    shutil.chown(file,'fh6','fh6')
    os.chmod(file,0o700 if file.is_dir() else 0o600)
print('MIGRATION_SHA_VERIFICATION=PASSED')
print('MIGRATION_RUN_ID='+run['runId'])
