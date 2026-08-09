# Season state contract

`data/current-season.json` is the single editable source for the active guide. Generated Markdown, artifact JSON, and HTML must not become competing sources.

## Required season metadata

- `seriesNumber`, `seriesSlug`, `seriesName`, `season`, `seasonDisplay`
- ISO 8601 `startAt`, `endAt`, and top-level `lastContentUpdate`
- `reportTitle`, `archiveFile`, `assetsDirectory`
- `fandomUrl`, `officialPlaylistUrl`
- `expectedCardCount`, `expectedDailyItems`, `maxPublicHtmlBytes`

`archiveFile` must stay under `seasons/`. `assetsDirectory` must stay under `reports/assets/`. Counts describe the live Playlist and may change between seasons.

## Activity contract

Keep activities in game order. Every activity has:

- stable sequential `id` and two-digit `number`;
- `kind`, `title`, `points`;
- `conditionHtml`, `howHtml`, `tuneHtml`, `sourceHtml`;
- `visual.image`, `visual.icon`, `visual.position`, source URL and label;
- `completeness` states for `condition`, `solution`, `vehicleTune`, and `visual`;
- `missingFields` containing every intentionally empty or provisional field.

Allowed completeness values: `confirmed`, `community`, `preliminary`, `missing`, `not_applicable`.

## Open items

Each unresolved item must exist in top-level `openItems` with:

- `activityId` matching an activity;
- `field` matching its `missingFields` entry;
- short `reason`;
- `nextCheck` describing which live source to revisit;
- `status`: `missing`, `preliminary`, or `conflict`.

An unknown value stays empty. Never insert a prior-week solution, guessed share code, fake image path, or placeholder prose into a factual field.

## Update invariants

- Change `lastContentUpdate` only for a material content, evidence, or visual change.
- Keep one Daily activity card and all daily items inside it.
- Store exact current-week source links, not search URLs.
- Use fresh confirmation before carrying a tune into another season.
- Preserve prior states in `data/history/` and prior Markdown in `seasons/`.

