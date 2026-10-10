#!/bin/bash
set -euo pipefail
test "$(hostname)" = fh6-collector
python3 /opt/fh6/repo/automation/server/cutover_checks.py
install -m 0644 /opt/fh6/repo/automation/server/*.service /opt/fh6/repo/automation/server/*.timer /opt/fh6/repo/automation/server/*.path /etc/systemd/system/
systemd-analyze verify /etc/systemd/system/fh6-refresh.service /etc/systemd/system/fh6-refresh.timer /etc/systemd/system/fh6-preflight.service /etc/systemd/system/fh6-preflight.timer /etc/systemd/system/fh6-phone.service
systemctl daemon-reload
systemctl restart fh6-phone.service
systemctl enable --now fh6-refresh.timer fh6-preflight.timer
systemctl list-timers --all fh6-refresh.timer fh6-preflight.timer --no-pager
echo FH6_CUTOVER_READY
