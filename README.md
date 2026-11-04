# Nashville Building Permit Applications - a Machine Readable data brief

On November 3, 2026, Nashville's open building permit queue held 6,036 applications recorded as not issued; their median age was 330 days, 47.5 percent were over a year old, and about 1 in 8 applications entered in 2024-2025 (2,928 of 22,654 observable in either of Metro's two permit layers) remains unissued. All ages describe the pending stock only: applications that resolve leave the stock, and the median completed wait among permits issued in the last three years was 29 days (companion brief, 2026-11-03). All cost figures are applicant-stated construction value, counted only on the 3,910 records that state one (2,126 records, 35.2 percent, state no value).

Part of Machine Readable: https://adowlen.github.io/machine-readable/

Proposed repository (created by the publication run, not by this package): https://github.com/adowlen/nashville-building-permit-applications-data-brief

## Contents

- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief, produced by code/build_stats.py from the 2026-11-03 snapshot and the companion issued layer's same-day snapshot
- verification.md - source verification (including the agency metadata document read before analysis), methods checklist, Section 10 pre-flight audit record (ALL SECTION 10 GATES PASS), internal controls, independent verifier record (14 of 14 checks passed), and Section 11.3 flags
- verification-ledger-independent.md - the independent verifier's recomputation ledger (summary of data/verify_independent_output.txt)
- reviewer-notes.md - claims most likely challenged, checks not completed, surprises, flags
- sources.md - dataset citations and the per-figure source audit
- social-drafts.md - LinkedIn draft (held for a future Friday synthesis under the Friday-only rule; Machine Readable never posts to X)
- hero-headline.txt - the headline figure and story description for the hero illustration
- hero.png - hero graphic (generated illustration in hero_source/hero-art.webp, headline figure composited by code/hero_composite.py over a top gradient scrim, with all text generated from stats.json). Viewed during the build: a permits counter stacked with application folders, the tallest stack topped by one curled, aged folder, a torn-page wall calendar, dark storefronts and houses waiting outside the window; headline, sub-line, and source line fully legible on the scrimmed dark field
- charts/ - chart_age_distribution.png, chart_age_by_type.png, chart_cohort_pending_share.png, chart_district_pending.png (each prints its population and framing on the graphic; all viewed after rendering)
- data/ - pull_log.json, audit_output.txt, verify_independent_output.txt, verify_independent_output.json, source-metadata.pdf (Building Permit Applications Metadata v2.0), age_distribution_panel.csv, age_by_type_panel.csv, cohort_by_year_panel.csv, cohort_by_quarter_panel.csv, class_residual_panel.csv, mix_comparison_panel.csv, district_pending_panel.csv, zip_top10_panel.csv. The raw snapshot itself is the warehouse file stack/nashville/snapshots/2026-11-03/building_permit_applications_raw.parquet in the project stack (immutable; sha256 in data/pull_log.json), and code/build_stats.py also writes the cleaned layer to stack/nashville/layers/building_permit_applications_clean.parquet
- code/ - pull_data.py, build_stats.py, audit_section10.py, verify_independent.py, charts.py, hero_composite.py

## Dependencies (match code imports)

Python standard library (datetime, hashlib, json, pathlib, statistics, sys, time); matplotlib; numpy; pandas; Pillow; pyarrow; requests.

## Reuse and citation

Licensed CC-BY-4.0 (see LICENSE). Cite as: Machine Readable, "Nashville building permits, the pending side: 6,036 applications were still unissued on November 3, 2026, their median age was 330 days, and about 1 in 8 applications entered in 2024-2025 remains unissued" (2026), https://github.com/adowlen/nashville-building-permit-applications-data-brief
