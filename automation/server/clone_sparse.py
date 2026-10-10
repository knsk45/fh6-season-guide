"""Sparse working copy preserves history in Git without downloading old asset blobs."""
from pathlib import Path
import subprocess
import time
import json
import urllib.request

root=Path('/opt/fh6/repo')
# Only the incomplete clone made by this migration may be displaced.
if root.exists() and not (root/'data/current-season.json').exists():
    root.rename(root.with_name('clone-incomplete-'+str(time.time_ns())))
if not root.exists():
    subprocess.run(['git','clone','--depth','1','--filter=blob:none','--no-checkout','--single-branch','--branch','daily-season','https://github.com/knsk45/fh6-season-guide.git',str(root)],check=True)
request=urllib.request.Request('https://raw.githubusercontent.com/knsk45/fh6-season-guide/daily-season/data/current-season.json',headers={'User-Agent':'FH6-setup'})
with urllib.request.urlopen(request,timeout=30) as response:state=json.load(response)
assets=state['season']['assetsDirectory'].strip('/')
if not assets.startswith('reports/assets/') or '..' in Path(assets).parts:raise RuntimeError('Unexpected assets path')
patterns='/*\n!/reports/assets/*\n/reports/assets/project/\n/reports/assets/activity-icons/\n/'+assets+'/\n'
subprocess.run(['git','-C',str(root),'sparse-checkout','set','--no-cone','--stdin'],input=patterns,text=True,check=True)
subprocess.run(['git','-C',str(root),'checkout','daily-season'],check=True)
print('FH6_SPARSE_CLONE_READY')
