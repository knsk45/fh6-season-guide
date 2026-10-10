"""Retry only saved final delivery; never start a new audit or fake receipt."""
from pathlib import Path
import sys

root=Path('/opt/fh6/repo')
sys.path.insert(0,str(root/'automation'))
from refresh_guard import Guard,read,now,exclusive
guard=Guard(root)
if guard.active.exists():
    with exclusive(guard.base/'process.lock'):
        active=guard.load()
        if active['status']=='AWAITING_DELIVERY' and active.get('resultPath'):
            if read(active['resultPath'])['runDate']<now()[:10] and not active.get('notification'):
                guard.close_expired(active)
            guard.execute(active)
            if active['status']=='AWAITING_DELIVERY':raise SystemExit(2)
