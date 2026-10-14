# Owner-controlled Steam desktop on CT109

Install `automation/server/install_steam_desktop.py` as root inside the
`fh6-collector` container after installing Debian's Chromium, Xvfb, xauth,
x11vnc, noVNC, and websockify packages. The installer requires the exact existing
panel nginx configuration, vacant reserved ports, no previous browser files or
profile, and inactive Steam publication units. It refuses unknown configurations.

The desktop runs as the publisher `fh6` with a dedicated mode-0700 profile and
mode-0600 Xauthority file. Chromium's sandbox remains enabled. X11 has no TCP
listener. Only loopback browser control port 9222, VNC 5901, and noVNC proxy 6081
are used. A separate nftables table denies non-loopback traffic to these ports
and denies other local users access: root and fh6 may access 9222/5901; nginx's
www-data may additionally access 6081. Existing firewall tables are untouched.
The desktop requires the guard service. The installer checks allowed connections
and fh6-editor/www-data denials before adding the owner-facing route.

`/steam-browser/` inherits the panel's existing HTTPS and Basic authentication.
The nginx proxy supports WebSocket upgrade. It does not proxy browser-control
port 9222. The setup exception for `/setup` does not apply to the browser route.

After `FH6_STEAM_DESKTOP_READY`, the owner can open:

https://fh6.knsk45.crazedns.ru/steam-browser/vnc.html?autoconnect=1&resize=scale&path=steam-browser/websockify

Enter Steam credentials and approve Steam Guard only in this dedicated browser.
Do not send credentials, QR codes, session cookies, or guard codes to chat.
Desktop child output is suppressed to avoid recording browser URLs or owner
input in service logs. Do not save the account password in Chromium.

This setup starts only the browser. It does not enable the publication timer,
change selector-verification flags, create publication approvals, submit Steam
forms, or mark either locale as published. Authenticated editor selectors still
need inspection and validation. A fresh accepted source/visual audit, current
owner consent, and verification of both public sections remain mandatory.

The installer backs up nginx configuration under `/var/lib/fh6/repairs` and
restores it if a readiness, isolation, or syntax check fails. Failed installation
stops the desktop and removes newly installed runtime files. Reserved-port guard
rules and the private profile remain for inspection; a subsequent attempt
requires reviewing these leftovers. Never flush the full firewall or disable
Chromium's sandbox to force installation.

Local checks validate embedded source hashes, firewall scope, authentication
inheritance, failed isolation handling, and sandbox-preserving launch arguments.
Actual X11/Chromium startup, kernel firewall rules, and protected mobile access
can only be confirmed on CT109. The installer performs the first two; the owner
must confirm the mobile screen before login. A successful package installation
alone is not evidence of working Steam authentication or publication.

After login, run `automation/server/configure_steam_browser.py` as root from a
root-owned file readable by `fh6`. It verifies both configured existing editors
as `fh6`, including the observed `ValidateEditSubSectionForm` JavaScript Save
link, and checks both public bodies in an anonymous context. No form is filled
or submitted. The original configuration is backed up privately before saving
verified selectors with `publishEnabled=false`; the publication timer remains
disabled. Its compact result also reports standing-consent and accepted-audit
booleans. Generic password/one-time-code fields classify challenges; any missing
editor control or changed URL still stops setup. Configuration alone does not
prove a publication, approval, fresh audit, or a permanently valid Steam login.
