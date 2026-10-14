"""Explicit standing consent creates hash-bound approvals, never publishes."""
from pathlib import Path
import json
import os
import pwd
import time
import uuid
import hashlib
from phone_tasks import lock,save,read

def state(store):
    value=read(Path(store)/'steam-consent.json')
    return dict(enabled=value.get('enabled') is True,updatedAt=value.get('updatedAt'))

def consent_lock(store):
    path=Path(store)/'steam-consent.lock'
    if path.is_symlink():raise ValueError('Unexpected consent lock')
    path.touch(exist_ok=True)
    if os.geteuid()==0:
        owner=pwd.getpwnam('fh6');os.chown(path,owner.pw_uid,owner.pw_gid);path.chmod(0o640)
    return lock(path,blocking=True)

def revoke(store):
    for file in Path(store).glob('steam-approval-*.json'):
        if file.is_symlink():continue
        value=read(file)
        if value.get('automatic') is True and value.get('status')=='AWAITING_BROWSER_PUBLICATION':
            value.update(status='REVOKED',revokedAt=time.time());save(file,value)

def set_enabled(store,enabled):
    with consent_lock(store):
        save(Path(store)/'steam-consent.json',dict(enabled=bool(enabled),updatedAt=time.time(),scope='current-and-future-ru-en'))
        # Every change creates a new consent version. Old automatic approvals
        # cannot silently become valid again when the switch is re-enabled.
        revoke(store)

def sync(root,store):
    """Caller holds runner.lock: the pair cannot change during generation."""
    if not state(store)['enabled']:return
    with consent_lock(store):
        policy=state(store)
        if not policy['enabled']:return
        active=read(Path(root)/'automation/runs/refresh/active.json')
        if active.get('status') not in {'PENDING_CONFIRMATION','COMPLETED','AWAITING_DELIVERY'}:return
        texts=[]
        for name in ['steam-guide-current.txt','steam-guide-current-en.txt']:
            file=Path(root)/'reports'/name
            if file.is_symlink() or not file.is_file():return
            text=file.read_text(encoding='utf-8-sig')
            if not text.strip() or len(text)>4800:return
            texts.append(text)
        sha=hashlib.sha256('\n'.join(texts).encode()).hexdigest()
        for file in Path(store).glob('steam-approval-*.json'):
            if file.is_symlink():continue
            value=read(file)
            if value.get('sha256')==sha and value.get('status')=='AWAITING_BROWSER_PUBLICATION':
                if not value.get('automatic') or value.get('standingConsentAt')==policy['updatedAt']:return
        save(Path(store)/('steam-approval-'+uuid.uuid4().hex+'.json'),
             dict(sha256=sha,approvedAt=time.time(),action='replace-current-ru-en',
                  status='AWAITING_BROWSER_PUBLICATION',automatic=True,standingConsentAt=policy['updatedAt']))
