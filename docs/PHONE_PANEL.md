# Private panel: readable statuses and standing Steam consent

The panel renders separate overview, Codex tasks, Steam text, screenshot and
login cards. It does not display the internal guard JSON. Task history and each
full Steam locale are collapsed by default. Copy controls copy the complete
Steam section, not individual tuning codes. Actions show pending, accepted and
error feedback in place; the same authenticated same-origin endpoints remain.
Without JavaScript, native forms remain available.

The Steam switch explicitly authorizes the current and future checked RU/EN
pairs while enabled. `/var/lib/fh6/steam-consent.json` records `enabled`,
`updatedAt` and scope. Toggle changes invalidate pending automatic approvals.
Manually granted per-pair approvals retain their separate authorization.

The existing task timer synchronizes approvals under the publisher runner
lock. Only saved terminal audited results can receive an automatic SHA-bound
approval; running/blocked results and empty/oversized text are rejected. There
is no publication in this synchronization function. Auto approvals carry
`automatic=true` and the consent version in `standingConsentAt`.

A future Steam publisher MUST recheck the switch is enabled and
`standingConsentAt` equals the current consent version immediately before
each browser write, as well as the pair SHA, existing section identity and
audit validity. A revoked/pending approval is not proof of publication.
Public verification and per-locale publication marking are still mandatory.
Turning the switch off cannot undo a Steam write already completed.

Install the pinned `automation/server/install_phone_panel.py` inside CT109.
It checks the installed panel/task-worker hashes, refuses an active task or
pipeline, backs up files and runs isolated panel/consent/server tests before
restarting the panel. It does not change the daily runner or publish Steam.

Validation here: 10 queue/HTTP tests, 5 panel/action tests, 4 standing-consent
tests and 21 existing non-root tests; inline JavaScript syntax checked with
Node. Root storage tests also run during the server installation. Headless
visual browser validation was unavailable in the development environment.
