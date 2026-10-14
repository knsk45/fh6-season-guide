# Steam worker staging and activation

The reviewed proposal now supports versioned standing consent, refreshed
24-hour hash-bound approvals, the shared runner lock, fresh accepted guard
audits, durable pre-Save state and partial RU/EN recovery. Both public sections
must match before publication baselines are updated. A lost Save response is
UNCERTAIN and never triggers a blind repeat. The private panel displays these
states in its existing Steam card; the proposal's old phone_ui is not installed.

Public page observation on 2026-10-14 confirmed guide 3787739730 and existing
sections 9235220 (Актуальная неделя · Русский) and 9330926 (Current Week · English).
Their public bodies are `[id="9235220"] > .subSectionDesc` and
`[id="9330926"] > .subSectionDesc`. No authenticated edit fields were inspected.

`stage_steam_publish.py` installs reviewed code and units but leaves the Steam
timer disabled. It writes a nonsecret `/etc/fh6/steam-browser.json` with
`publishEnabled=false`, `selectorsVerified=false` and placeholders for the
unobserved edit/login controls. Existing configuration is preserved. No real
browser connection, Steam write, credentials or login are performed by staging.
Known panel/module hashes, backups and isolated tests protect the existing UI.

Before activation the owner must sign into a dedicated server Chromium session
and complete Steam Guard themselves. This ChatGPT browser is a different session
and cannot provide the server's login. Credentials/cookies/profile files are
never uploaded into the panel or this chat. The proposed loopback CDP transport
must also be restricted to the publisher, including preventing the isolated
fh6-editor account from reaching it; loopback alone does not isolate local users.
Do not expose CDP on the router, VPN or LAN.

After sign-in, inspect both existing edit pages without saving, verify title,
textarea and Save selectors and their unique visible/enabled identity. A server
browser fixture test and one controlled real write must precede unattended use.
Set selector verification and publication enabled only after these steps. Do not
guess selectors or create new sections. Require a fresh complete refresh if the
accepted audit is older than four hours. Toggle consent can then authorize the
current/future pair; each Save rechecks it immediately beforehand.

The installed worker still uses the reviewed proposal's CDP adapter. Server
browser provisioning, isolated owner sign-in and authenticated selector mapping
are outstanding work; staging is not a claim of end-to-end Steam automation.

Statuses: NEEDS_SETUP, NEEDS_LOGIN, STEAM_GUARD, NEEDS_APPROVAL,
STALE_APPROVAL, AUDIT_REQUIRED, PUBLISHING, VERIFYING, UNCERTAIN,
BLOCKED and COMPLETE. COMPLETE for an older SHA is never shown as success for
the current panel texts. A re-enabled switch has a new version; old automatic
approvals cannot be reused. Manually granted per-pair approvals remain separate.
