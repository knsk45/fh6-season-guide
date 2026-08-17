---
name: fh6-season-maintainer
description: Maintain, roll over, validate, build, and publish the Russian Forza Horizon 6 Festival Playlist guide. Use for daily gap-filling, Thursday season changes, current-season research, card or image repairs, portable report rebuilding, and the fh6 scheduled task in this repository.
---

# FH6 season maintainer

Keep the public guide complete without inventing missing facts or breaking its card structure.

## Start every run

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
2. Research only those gaps plus fresh corrections for the active week.
3. Update `data/current-season.json`. Keep unknown values empty and update both `missingFields` and `openItems` together.
4. Set `lastContentUpdate` only when facts, evidence, visuals, or recommendations materially changed.
5. Run the build sequence below. On a true no-op, skip regeneration and commits, but still verify the existing public URL.

## Thursday rollover

1. Confirm Series, season, start/end timestamps, rewards, and exact card order from live sources.
2. Create `automation/new-season-input.json` from `data/season-state.schema.json`. Include every confirmed card; use empty fields plus missing-state entries for unknown details.
3. Download compact current-season visuals into a new directory under `reports/assets/`. Use a season-specific fallback visual rather than a broken image; keep the exact tile in `openItems` if still missing.
4. Run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File automation/start_new_season.ps1 -InputPath automation/new-season-input.json`.
5. Confirm that the old state was copied into `data/history/`, a new archive file was created, and no older season was deleted.
6. Remove the local input after success; it is ignored by Git.
7. Do not modify `data/project.json` during rollover. Preserve its branding icons and enabled visit analytics in the public HTML. Keep the visit counter inside the enabled support block after all activities in both `README.md` and the public report; the support block is not a Playlist card.

## Build and validate

Run in this order:

1. `automation/render_season_markdown.ps1`
2. `reports/build_artifact.ps1`
3. the build-report `deliver_portable_artifact.mjs`
4. `reports/enhance_portable_html.mjs`
5. `automation/validate_season.ps1`

The validator, not a remembered number, decides the required card count. Treat any structural error as blocking. Treat unresolved evidence as a warning that remains in `openItems`. Every specifically recommended vehicle must have its four-digit model year. Publish tune share codes without tuner names. Put every hyperlink in `sourceHtml`, never in condition, solution, or tune fields, and give every card link `target="_blank" rel="noopener noreferrer"`. Keep PI restrictions as plain text in season state; the builder must decorate every D/C/B/A/S1/S2/R/X plus three-digit PI token and the validator must compare badge count with state. Validation must confirm the configured favicon assets in the public HTML. When project support is enabled, it must also confirm exactly one final support block, its local QR asset, and its configured link in README and the public report. When project analytics is enabled, validation must confirm exactly one counter inside that final support block, the configured hits.sh image/dashboard URLs, and the restricted CSP allowance.

## Publish

Publish only after the portable validation/package and `STRUCTURE_OK` succeed:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File automation/publish_to_github.ps1 -CommitMessage "Update FH6 current season YYYY-MM-DD"`

Require `PUBLISHED_SHA` and `PAGES_URL`, then verify the public HTML and referenced image URLs. Never force-push and never delete season archives.
