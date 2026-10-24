# Collector audit — 2026-10-24

Baseline: `61566962a3d82970cfc9eba9e2cf8e83df421d5c` (`daily-season`).
The sole publisher remains CT109 `/opt/fh6/repo`.

The daily run `fh6-20261024-060007-948343` passed audit, build, portable
package verification, structure validation, browser QA, GitHub publication,
metrics and HA delivery. No failed systemd units were found. The current
season has 13 cards and 11 unresolved weekly visuals. These are evidence gaps,
not compilation errors. The monthly original/crop remain preserved.

The run's historical `PENDING_CONFIRMATION` is valid for its finish time.
Subsequent Steam publication completed; a fresh bilingual checker returned
`STEAM_GUIDES_STATUS=UP_TO_DATE`. Do not rewrite historical run receipts to
make them describe later events.

This branch preserves previously uncommitted server implementation: phone
session authentication, phone tasks, bounded recovery, diagnostic summaries,
refresh request receipts and owner-approved bilingual Steam publishing.
Credentials, browser profiles, approvals, task logs, audit inputs, ignored runs
and live metrics are excluded. This is a source snapshot, not an instruction
to activate services or replace production settings.

Two stale regression assumptions were repaired:

- The portable icon test assumed the photo card always had a confirmed tile
  icon. It now mutates every card, checking both wrong and unexpected icons.
- The panel browser test expected an obsolete response and intercepted a URL
  without the AJAX query parameter. It now checks the current acceptance
  response and intercepts the actual request URL.

Validation on CT109:

- 132 server unittest cases passed with `/opt/fh6/venv/bin/python`.
- 30 refresh guard tests passed.
- 21 portable report tests passed after the repair.
- 8 rollover validation tests passed.
- Notification text tests passed.
- Phone panel browser QA passed at 390 and 1440 pixels; incident clipboard QA
  passed as the unprivileged `fh6` user with Chromium sandbox enabled.
- `PORTABLE_RECEIPT_VERIFIED=OK`; `STRUCTURE_OK cards=13 open_items=11`.
- Both Steam locale checks returned UP_TO_DATE.

Only the two test files were changed on production; originals are retained at
`/var/lib/fh6/maintenance/collector-audit-20261024/` under their relative paths.
No service, timer, publisher, season facts or authentication settings changed.
Use the venv for Playwright tests; browser fixtures requiring sandbox must run
as `fh6`, not root. Test fixture error messages do not indicate production sends.

A local development mirror on the temporary computer delegates guard commands
to CT109 using ignored `automation/runs/server-owner.json`. Its SSH executable
must be available on PATH; the machine-local PowerShell wrapper supplies it.
The mirror is shallow and sparse; fetch additional history/assets when needed.