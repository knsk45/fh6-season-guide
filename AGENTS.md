# FH6 project instructions

- For every Festival Playlist refresh, season rollover, report repair, or scheduled run, use the repo skill `$fh6-season-maintainer` from `.agents/skills/fh6-season-maintainer/`.
- Treat `data/current-season.json` as the only editable source of current-season card content, ordering, deadline, visuals, completeness, and missing fields.
- Treat `data/project.json` as the persistent source for project-wide content. The enabled support block must remain at the end of `README.md` and `reports/current-week.html`, and must never be counted as a Festival Playlist card.
- Treat the current file in `seasons/`, `CURRENT_WEEK.md`, `reports/artifact.json`, and `reports/current-week.html` as generated outputs. Regenerate them; do not hand-edit their duplicated content.
- Never hardcode a universal card count. Read `season.expectedCardCount` and `season.expectedDailyItems` from the current state.
- On season rollover, preserve all files in `seasons/` and `data/history/`. Never reuse a prior-week tune code or solution without fresh current-week evidence.
- Unknown facts stay empty in the activity field and are listed in both `missingFields` and top-level `openItems`. Missing evidence is allowed; structural drift is not.
- Before publication run `automation/validate_season.ps1`. Publish only when it prints `STRUCTURE_OK` and the portable build has passed validation/package.
- Publish through `automation/publish_to_github.ps1` on branch `daily-season`; never force-push.
