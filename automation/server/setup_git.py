"""Repo-only SSH deploy key, GitHub host keys pinned through HTTPS metadata."""
from pathlib import Path
import json
import subprocess
import urllib.request
import os
import shutil

ssh=Path('/home/fh6/.ssh')
ssh.mkdir(mode=0o700,exist_ok=True)
key=ssh/'fh6_deploy'
if not key.exists():subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',str(key),'-C','fh6-ct109'],check=True)
request=urllib.request.Request('https://api.github.com/meta',headers={'User-Agent':'FH6-setup'})
with urllib.request.urlopen(request,timeout=30) as response:metadata=json.load(response)
keys=[k for k in metadata['ssh_keys'] if k.startswith('ssh-ed25519 ')]
if not keys:raise RuntimeError('GitHub did not provide an ed25519 host key')
(ssh/'known_hosts').write_text('\n'.join(host+' '+k for host in ['github.com','[ssh.github.com]:443'] for k in keys)+'\n')
(ssh/'config').write_text('Host github.com\n  HostName ssh.github.com\n  Port 443\n  User git\n  IdentityFile /home/fh6/.ssh/fh6_deploy\n  IdentitiesOnly yes\n  StrictHostKeyChecking yes\n  ConnectTimeout 10\n')
for file in ssh.iterdir():os.chmod(file,0o600);shutil.chown(file,'fh6','fh6')
shutil.chown(ssh,'fh6','fh6')
print('GITHUB_DEPLOY_PUBLIC_KEY='+key.with_suffix('.pub').read_text().strip())
