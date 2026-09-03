---
name: fh6-season-maintainer
description: Maintain, roll over, validate, build, and publish the Russian Forza Horizon 6 Festival Playlist guide. Use for daily gap-filling, Thursday season changes, current-season research, card or image repairs, portable report rebuilding, and the fh6 scheduled task in this repository.
---

# FH6 season maintainer

Keep the public guide complete without inventing missing facts or breaking its card structure.

## Start every run

Before the list below, read [run recovery](../../../docs/RUN_RECOVERY.md) via the repository root `docs/RUN_RECOVERY.md` and run `python automation/refresh_guard.py start`. After context compaction run `status` before acting: the recorded unfinished update remains the task; older conversation messages must not replace it. Follow genuine new user instructions. Record audit evidence with guard `audit`; execute build/publication/finalization through guard `execute`. Its independent RunId supersedes the older lastContentUpdate-as-RunId convention. Return the saved result in chat, never an unrelated historical answer. The guard validates evidence and delivery; it does not replace live research.

1. Read `AGENTS.md`, `data/current-season.json`, `data/project.json`, `docs/WORKFLOW.md`, `docs/SOURCES.md`, and `reports/SOURCE_NOTES.md`.
2. Read [references/season-state.md](references/season-state.md) before changing the state schema, performing a rollover, or adding an unresolved item.
3. Check the current time in `Asia/Krasnoyarsk` and verify the active season from live official Forza sources before trusting local dates.
4. Check every source in `data/project.json.requiredSources` and add a dated audit to `reports/SOURCE_NOTES.md`. A source without a fresh current-week publication is recorded as checked/no-current-item; it does not justify old evidence.
5. Inspect Git status. Preserve unrelated user changes.

## Choose the run mode

- If the live season still matches `data/current-season.json`, perform a daily gap-fill run.
- If the live season has changed, perform a rollover. Do not infer a rollover only because the stored deadline passed; confirm the new Playlist first.
- If official sources are unavailable, keep the current state, record the access problem in `openItems`, and do not fabricate a new season.

## Daily gap-fill

1. Search `openItems`, every activity's `missingFields`, empty content fields, `TODO`, and conflicting evidence.
2. Independently audit the `visual` of every activity on every run, including visuals not listed in `openItems`. Check the current Season page, official Playlist/News, fresh current-week Reddit guides, and current-week guide sites for a more exact image.
3. Prefer an exact current-week game tile. If it is unavailable, use a distinct activity-specific current-week screenshot or a clearly labelled derivative from the current season overview. Never reuse a prior-week image. Do not accept one shared fallback as completed while distinct current-week visuals are available; keep any temporary fallback `preliminary` and open for replacement.
4. Research the remaining gaps plus fresh corrections for the active week.
5. Update `data/current-season.json`. Keep unknown values empty and update both `missingFields` and `openItems` together. Record the visual audit summary and counts by completeness status in `reports/SOURCE_NOTES.md`.
6. After the complete required-source audit has succeeded and live evidence confirms the stored active season, run `automation/refresh_last_content_update.ps1`. `lastContentUpdate` is the time of the latest successful full audit, so refresh it even when facts, evidence, visuals, and recommendations did not change. If live confirmation or the required-source audit is incomplete, do not refresh it.
7. Run the full build, validation, and publication sequence below on every successful daily audit. A no-card-change run still publishes the refreshed verification time; it is not an empty commit.

## Thursday rollover

1. Confirm Series, season, start/end timestamps, rewards, and exact card order from live sources.
2. Create `automation/new-season-input.json` from `data/season-state.schema.json`. Include every confirmed card; use empty fields plus missing-state entries for unknown details.
3. Download compact current-season visuals into a new directory under `reports/assets/`. Try to give every card a distinct current-week visual immediately. Use a season-specific fallback rather than a broken image only when no activity-specific current-week visual exists; keep that visual `preliminary` and in `openItems` until replaced.
4. Run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File automation/start_new_season.ps1 -InputPath automation/new-season-input.json`.
5. Confirm that the old state was copied into `data/history/`, a new archive file was created, and no older season was deleted.
6. Remove the local input after success; it is ignored by Git.
7. Do not modify `data/project.json` during rollover. Preserve its branding icons and enabled visit analytics in the public HTML. Keep the visit counter inside the enabled support block after all activities in both `README.md` and the public report; the support block is not a Playlist card.

## Build and validate

Run in this order:

1. `automation/render_season_markdown.ps1`
2. `reports/build_artifact.ps1`
3. `python automation/build_portable_report.py build` — repository-owned compatible provider `fh6-portable/1.0.0`, authorized 2026-09-03 in place of the unavailable legacy plugin file. Require validation/package passed and a verified SHA-bound receipt/ZIP; never call this the original plugin validator. See `docs/RUN_RECOVERY.md` for the contract. Guard supplies a per-run receipt; publisher verifies the current receipt again.
4. `reports/enhance_portable_html.mjs`
5. `automation/validate_season.ps1`
6. `automation/render_steam_guide.ps1` when `data/project.json.steamGuide.enabled=true`
7. `automation/check_steam_guide.ps1` when Steam mirroring is enabled
8. `automation/collect_publication_metrics.ps1 -RunId <lastContentUpdate>` after public GitHub Pages and Steam verification

The validator, not a remembered number, decides the required card count. Treat any structural error as blocking. Treat unresolved evidence as a warning that remains in `openItems`. Every specifically recommended vehicle must have its four-digit model year. Publish tune share codes without tuner names. Put every hyperlink in `sourceHtml`, never in condition, solution, or tune fields, and give every card link `target="_blank" rel="noopener noreferrer"`. Keep PI restrictions as plain text in season state; the builder must decorate every D/C/B/A/S1/S2/R/X plus three-digit PI token and the validator must compare badge count with state. Validation must confirm the configured favicon assets in the public HTML. When project support is enabled, it must also confirm exactly one final support block, its local QR asset, and its configured link in README and the public report. When project analytics is enabled, validation must confirm exactly one counter inside that final support block, the configured hits.sh image/dashboard URLs, and the restricted CSP allowance.

## Publish

Publish only after the portable validation/package and `STRUCTURE_OK` succeed:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File automation/publish_to_github.ps1 -CommitMessage "Update FH6 current season YYYY-MM-DD"`

Require `PUBLISHED_SHA` and `PAGES_URL`, then verify the public HTML and referenced image URLs. Never force-push and never delete season archives.

When Steam mirroring is enabled, render `reports/steam-guide-current.txt` after the GitHub Pages version is verified and run the Steam checker. It compares substantive Steam text with the last browser-verified publication fingerprint stored under ignored `automation/runs/`; the daily `lastContentUpdate` by itself is not a Steam change. Keep exact daily freshness in the linked HTML report rather than forcing a Steam edit every morning.

Keep the generated current-week Steam subsection at or below the project safe ceiling of 4,800 characters. This guard exists because Steam returned error 8 (`Description is too long`) for a 5,611-character subsection, while the compact 4,066-character replacement was accepted. `automation/render_steam_guide.ps1` must print `STEAM_GUIDE_CHARACTERS` and fail before browser editing when the ceiling is exceeded. Compact repeated labels, generic no-tune advice, and repeated caveats first; never remove activities, change their game order, omit a specific recommended car/share code, or remove the prominent report links at the beginning and end merely to meet the limit.

On an unattended daily run, do not edit Steam. If the checker reports `UPDATE_REQUIRED`, send a Home Assistant `UpdateRequired` push and finish as `PENDING_CONFIRMATION`; if it reports `UP_TO_DATE`, send `UpToDate`; if the audit/publication/check is incomplete, send `CheckBlocked`. Use `automation/send_home_assistant_notification.ps1` with the successful audit timestamp as `RunId` so retries are deduplicated. After the user confirms the Steam replacement, update only the single existing current-week section, verify the public page, run `automation/mark_steam_guide_published.ps1`, and require a final `UP_TO_DATE`. Never create a duplicate section or mark an unverified edit as published.

After both publication targets are checked, collect public metrics with the same `RunId`. The ignored local snapshot is the baseline for deltas on the next successful run. Always include Steam unique visitors added, Steam current favorites added, and GitHub guide views added in the final chat summary and in the single Home Assistant notification, together with their current totals. A first-run baseline has zero deltas and must be labelled as a baseline. If the current metrics cannot be collected, report `PUBLIC_METRICS_STATUS=BLOCKED`; do not reuse stale deltas as current results.
