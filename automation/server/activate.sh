#!/bin/bash
set -euo pipefail
test "$(hostname)" = fh6-collector
apt-get install -y --no-install-recommends nginx
install -d -m 2750 -o fh6-editor -g fh6 /var/lib/fh6/login
# Traverse only; never add the editor to the publisher's private group.
setfacl -m u:fh6-editor:--x /var/lib/fh6
install -d -m 0755 -o root -g root /usr/local/lib/fh6
install -m 0600 -o root -g root /opt/fh6/repo/automation/server/phone_password.py /usr/local/lib/fh6/phone_password.py
chown root:fh6 /etc/fh6
# nginx needs traversal, not directory listing or membership in the private fh6 group.
setfacl -m u:www-data:--x /etc/fh6
if ! test -f /etc/fh6/phone.key; then
    openssl req -x509 -newkey rsa:3072 -sha256 -nodes -days 365 -subj '/CN=fh6-collector' -addext "subjectAltName=IP:$(hostname -I | awk '{print $1}'),DNS:fh6-collector,DNS:fh6-collector.local" -keyout /etc/fh6/phone.key -out /etc/fh6/phone.crt
    chmod 600 /etc/fh6/phone.key
fi
python3 /opt/fh6/repo/automation/server/setup_private.py
install -m 0644 /opt/fh6/repo/automation/server/phone-nginx.conf /etc/nginx/sites-available/fh6-phone
ln -sf /etc/nginx/sites-available/fh6-phone /etc/nginx/sites-enabled/fh6-phone
nginx -t
if test -L /etc/nginx/sites-enabled/default; then unlink /etc/nginx/sites-enabled/default; fi
install -m 0644 /opt/fh6/repo/automation/server/*.service /opt/fh6/repo/automation/server/*.timer /opt/fh6/repo/automation/server/*.path /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now fh6-phone-password.service fh6-phone.service fh6-editor-login.path
systemctl restart nginx
# Timers are activated only after live verification, by a separate cutover step.
echo FH6_PRIVATE_UI_READY
