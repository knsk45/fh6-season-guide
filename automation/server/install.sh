#!/bin/bash
# Run only inside the dedicated Debian FH6 container, never on the PVE host.
set -euo pipefail
test "$(hostname)" = fh6-collector
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl wget gnupg python3 python3-venv python3-pil nodejs npm git gh chromium fonts-dejavu fonts-noto-color-emoji openssl rsync sudo acl
curl --fail --silent --show-error https://packages.microsoft.com/config/debian/13/packages-microsoft-prod.deb -o /tmp/fh6-microsoft.deb
dpkg -i /tmp/fh6-microsoft.deb
apt-get update
apt-get install -y powershell
npm install -g @openai/codex
id fh6 >/dev/null 2>&1 || useradd --create-home --shell /bin/bash fh6
id fh6-editor >/dev/null 2>&1 || useradd --create-home --shell /bin/bash fh6-editor
install -d -m 0750 -o fh6 -g fh6 /opt/fh6/repo /var/lib/fh6 /var/lib/fh6/inbox /etc/fh6
install -d -m 0700 -o fh6-editor -g fh6-editor /var/lib/fh6/editor
timedatectl set-timezone Asia/Krasnoyarsk
python3 -m venv /opt/fh6/venv
/opt/fh6/venv/bin/pip install 'playwright>=1.55,<2'
echo FH6_RUNTIME_INSTALLED
