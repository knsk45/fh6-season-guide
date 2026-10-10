"""Local PC commands are delegated to the single server publisher."""
from pathlib import Path
import subprocess
import base64
import sys

root=Path('/opt/fh6/repo')
result=subprocess.run(['python3',root/'automation/refresh_guard.py',*sys.argv[1:]],cwd=root)
checkpoint=root/'automation/runs/refresh/active.json'
if checkpoint.exists():print('FH6_REMOTE_CHECKPOINT='+base64.b64encode(checkpoint.read_bytes()).decode())
raise SystemExit(result.returncode)
