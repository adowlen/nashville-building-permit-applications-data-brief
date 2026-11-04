# Independent verification ledger - Nashville Building Permit Applications brief (2026-11-04)

Verifier: code/verify_independent.py (Section 11 method diversity: two implementations sharing no code with code/build_stats.py). Full output: data/verify_independent_output.txt and data/verify_independent_output.json. Result: **14/14 checks pass, exact equality on every snapshot-side figure.**

## Method 1 - live server-side ArcGIS aggregates (no local computation)

- Live row count: 6,036 vs snapshot 6,036 (drift-tolerant gate; observed drift zero).
- Definition control: server-side count of rows where Date_Issued IS NOT NULL = 0, confirming the layer contains only not-yet-issued applications, per metadata v2.0.
- groupBy Permit_Type_Description: 29 of 29 type counts match the snapshot exactly.
- Positive-cost population: server n = 3,910, total $1,896,350,756, max $150,000,000 - all identical to stats.json.

## Method 2 - pyarrow recount of the raw snapshot (no pandas, no builder code)

- Row count 6,036; ObjectId unique on all 6,036 rows.
- Date_Issued null on all rows (0 non-null).
- Median pending age recomputed by raw epoch arithmetic (as-of instant fixed at 2026-11-03 06:00 UTC = Chicago midnight CST; age = whole days between epoch timestamps): 330 days, matching the builder's local-date computation exactly.
- Over-365 count 2,865; max age 1,100 days (the rolling-window ceiling).
- Stated-cost total on positive rows $1,896,350,756; median $150,394 (stats.json stores $150,393.50); not-stated rows (zero + null) 2,126.
- District unknowns: 3 nulls, 0 zero codes.

## Discrepancies

None. Every independently recomputed figure equals the builder's figure.
