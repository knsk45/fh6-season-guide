#!/bin/bash
# Invoked inside CT109 after the shallow clone and archives have arrived.
set -euo pipefail
test "$(hostname)" = fh6-collector
test -d /opt/fh6/repo/.git
tar -xf /tmp/fh6-server-patch-ready.tar -C /opt/fh6/repo
install -d -m 0700 /tmp/fh6-import
tar -xf /tmp/fh6-server-state-ready.tar -C /tmp/fh6-import
python3 /opt/fh6/repo/automation/server/import_state.py /tmp/fh6-import
chown -R fh6:fh6 /opt/fh6/repo
chmod 2750 /var/lib/fh6
python3 /opt/fh6/repo/automation/server/setup_git.py
runuser -u fh6 -- git -C /opt/fh6/repo remote set-url origin git@github.com:knsk45/fh6-season-guide.git
runuser -u fh6 -- git -C /opt/fh6/repo config user.name 'FH6 server'
runuser -u fh6 -- git -C /opt/fh6/repo config user.email 'knsk45@users.noreply.github.com'
echo FH6_SERVER_DEPLOYED
