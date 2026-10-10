"""Device login output is shown only to the authenticated phone user, never logs/chat."""
from pathlib import Path
import subprocess
import os

target=Path('/var/lib/fh6/login/device.txt')
try:
    with target.open('w') as output:
        os.chmod(target,0o640)
        subprocess.run(['/usr/local/bin/codex','login','--device-auth'],stdout=output,stderr=output,timeout=900)
finally:
    target.unlink(missing_ok=True)  # Expiring code must not remain as durable evidence.
