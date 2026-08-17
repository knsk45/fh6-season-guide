# FH6 project instructions

- For every Festival Playlist refresh, season rollover, report repair, or scheduled run, use the repo skill `$fh6-season-maintainer` from `.agents/skills/fh6-season-maintainer/`.
- Treat `data/current-season.json` as the only editable source of current-season card content, ordering, deadline, visuals, completeness, and missing fields.
- Treat `data/project.json` as the persistent source for project-wide content. Its branding assets and enabled visit analytics must remain linked from the public HTML. The visit counter stays inside the final support block. The enabled support block must remain at the end of `README.md` and `reports/current-week.html`, and must never be counted as a Festival Playlist card.
- Check every entry in `data/project.json.requiredSources` on every refresh. Record the result in `reports/SOURCE_NOTES.md`; a source with no current-week publication is a checked absence, not permission to reuse old data.
- Treat the current file in `seasons/`, `CURRENT_WEEK.md`, `reports/artifact.json`, and `reports/current-week.html` as generated outputs. Regenerate them; do not hand-edit their duplicated content.
- Never hardcode a universal card count. Read `season.expectedCardCount` and `season.expectedDailyItems` from the current state.
- Keep performance class and PI restrictions as plain text in season state. The report builder decorates D/C/B/A/S1/S2/R/X plus three digits as game-style badges; validation must reject missing badge conversions.
- Every specifically recommended vehicle must include its four-digit model year. Show tune share codes without tuner names. Keep all hyperlinks in `sourceHtml`, never inside `conditionHtml`, `howHtml`, or `tuneHtml`; every card link must use `target="_blank"` and `rel="noopener noreferrer"`.
- On season rollover, preserve all files in `seasons/` and `data/history/`. Never reuse a prior-week tune code or solution without fresh current-week evidence.
- Unknown facts stay empty in the activity field and are listed in both `missingFields` and top-level `openItems`. Missing evidence is allowed; structural drift is not.
- Before publication run `automation/validate_season.ps1`. Publish only when it prints `STRUCTURE_OK` and the portable build has passed validation/package.
- Publish through `automation/publish_to_github.ps1` on branch `daily-season`; never force-push.
