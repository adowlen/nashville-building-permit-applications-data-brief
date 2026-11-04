# Verification - Nashville Building Permit Applications brief (2026-11-04)

## Source verification

- Dataset: Building_Permit_Applications_Feature_Layer_view (layer 0), hosted feature service on services2.arcgis.com/HdTo6HJqh92wn4D8 (NashvilleOpenData). Service metadata read 2026-11-03: layer name "Building_Permit_Applications_Feature_Layer_view", 21 fields. ArcGIS item 4c38be57f3fd47d6844ba820d1ea677c.
- **Definitional source read BEFORE analysis (standards 7.3):** "Building Permit Applications Metadata" v2.0, last updated 2023-06-05 (ArcGIS item db06911b1e814e07b1c58fe5037da1a9), archived at data/source-metadata.pdf. What it establishes:
  - The dataset details "building permit applications that have not yet been approved and issued over a rolling three-year period"; a record is "an application for a building permit that has not been issued."
  - The dataset does NOT contain issued building permits, trade applications, or trade permits (those live in separate datasets).
  - Time period of content: "three years prior to current date through present" (rolling), updated daily.
  - Source: Cityworks/ePermits; provided by Codes Administration, Zoning Review Division.
  - Construction Cost = stated value of construction; Date Entered = date applied for; Date Issued = date approved and issued.
  - Consequence verified in the data: Date_Issued is null on all 6,036 pulled rows, exactly as the definition requires.
- Fresh ArcGIS pull 2026-11-03 (America/Chicago dates; pull executed the evening of 2026-11-03 Denver time, which is the same calendar day in Nashville): 6,036 rows from 7 pages of 1,000 (maxRecordCount 2000 not binding; pulled in ObjectId order with returnIdsOnly count check: live count = pulled count = 6,036). Raw snapshot: stack/nashville/snapshots/2026-11-03/building_permit_applications_raw.parquet, sha256 f573ac6874a29974cff919352b6be7555cd82f9df4461f99c56f1e20bc872ff3. Pull script: code/pull_data.py; pull record: data/pull_log.json.
- Unit: one record = one permit application filing (rows). 6,036 rows carry 6,026 unique permit numbers (10 rows share a number, the multi-parcel pattern also present in the issued layer) across 4,620 unique parcels. Row-level unit stated in the brief.
- Provenance grade: A (direct agency ArcGIS service plus the agency's own definitional metadata document).
- Scope limits printed in the brief: the layer records only "not issued" (no status field); ages are right-truncated at 1,100 days by the rolling entry window; 35.2 percent of records state no construction value; the layer carries no Census tract field.

## Headline figures (all from stats.json, computed by code/build_stats.py)

- Pending applications on 2026-11-03: 6,036 (unit: applications/records).
- Age of the pending stock: median 330 days, mean 417.0, p90 951, max 1,100. Over 365 days: 2,865 (47.47 percent). Over 730 days: 1,474 (24.42 percent). Within 30 days: 580 (9.61 percent).
- Mature-cohort residue (entries 2024-2025, observable in either same-day layer): 2,928 of 22,654 still unissued (12.92 percent). By year: 2024 1,405/10,965 (12.81 percent); 2025 1,523/11,689 (13.03 percent). Full quarters 2024Q1-2025Q4 range 9.36 to 15.67 percent.
- Class residue, entries 2024-2025: Commercial New 37.13 percent (336/905); Use & Occupancy 30.48 percent (114/374); Sign Permit 3.86 percent (60/1,554); Residential New 12.54 percent (1,052/8,390).
- Stock median ages by class (>= 80 pending): Sign Permit 518 days (n 82); Residential Rehab 498 (396); Use & Occupancy 460.5 (188; printed as 460); Residential Addition 453 (567); Residential New 443 (1,945); Demolition 391 (441); Commercial New 335 (650); Commercial Tenant Finish Out 201 (468); Commercial Rehab 173 (822).
- Mix: Commercial New 10.77 percent of pending vs 2.91 percent of issued; Sign Permit 1.36 percent vs 6.71 percent; Residential New 32.22 percent vs 36.94 percent.
- Stated value: 3,910 records with a positive stated value totaling $1,896,350,756 (median $150,393.50); 2,126 records (35.22 percent) with zero (2,125) or null (1) value, excluded from all cost figures.
- Geography: District 2 most pending (480, median age 715 days); District 19 largest stated pending value ($384,826,611 = 20.29 percent of all stated pending value, on 178 of its 424 records); ZIP 37207 most pending (718). District known on 6,033 records; 3 nulls; no zero-district sentinel exists in this layer.
- Cross-layer control: 0 permit numbers appear in both layers (6,026 pending numbers vs 29,600 issued numbers).

## Methods checklist (standards section 3)

- [x] Source is a primary dataset (the agency's own ArcGIS service, definition confirmed against the agency's metadata document archived with the package).
- [x] Time window stated (entries 2023-10-30 to 2026-11-02; ages as of the 2026-11-03 pull date; the layer updates daily and later pulls will differ).
- [x] Unit stated on every published count (applications/records; rows vs permit numbers vs parcels distinguished in the brief's composition note).
- [x] At least two independent variables joined or explicitly ruled out (this brief joins the applications layer to the same-day issued layer by entry cohort and permit number for the residue and partition claims; council district and ZIP provide the geographic breakdowns).
- [x] No tract-level claims: the layer has no Census tract field, and the brief says so rather than substituting a coarser unit silently. District and ZIP figures are printed as what they are, with district unknown counts named.
- [x] Layering admission test (standards 9.1): the issued-layer join is admitted because the brief's central claims (the mature-cohort residue, the mix comparison, the zero-overlap partition) cannot be made from the applications layer alone, and each carries its definition in the brief.
- [x] Denominator check passed (Section 10 audit below: age-bucket counts sum to 6,036; every cohort row's issued + pending = observed total; stated + not-stated = 6,036; district known + unknown = 6,036).
- [x] "Who can act" section included, each item naming the lever owner, a concrete action, a cost class, and an outcome measure.
- [x] Strongest alternative explanation included in "What this might mean" for both readings (live long-cycle projects vs dead filings for the residue; pure stock selection for the ages).

## Pre-flight audit (Section 10, run 2026-11-03; code/audit_section10.py, output at data/audit_output.txt)

```
rows in cleaned layer: 6036
[definition] Date_Issued null on all 6036 rows (layer = not-yet-issued applications per metadata v2.0) PASS
[10.1.1] Const_Cost zero rows: 2125 and null rows: 1 mapped not-stated (2126 total, excluded from all cost figures); Council_Dist 0-sentinel rows: 0 (none exist in this layer); district unknown total 3 (all null); coords complete, no 0,0 PASS
[10.1.2] age polarity: 0 rows with negative age (entry after pull date); youngest matched sample: [['Building Residential - New', 1], ['Building Commercial - Rehab', 1], ['Building Commercial - Rehab', 1]]; oldest matched sample: [['Building Residential - Rehab', 1100], ['Building Demolition Permit', 1100], ['Building Demolition Permit', 1100]] PASS
[10.1.3] over-365 share recomputed 0.4747 on denominator 6036 applications; mature-cohort residual 2928/22654 applications over applications PASS
[10.1.4] Permit_Type_Description Counter: 29 values, counts sum to 6036, matches stats.json exactly PASS
[10.1.5] district known 6033 + unknown 3 = 6036; age buckets sum to 6036; stated 3910 + not-stated 2126 = 6036; every cohort row's issued + pending = observed total PASS
[10.2] controls: (a) Date_Entered carries only UTC hours 5/6 = America/Chicago midnights, so local-date reads and ages are correct; (b) cross-layer partition control: 0 of 6026 pending permit numbers appear in the issued layer's 29600 numbers, matching the metadata's partition of the two layers; (c) window-edge control: 16 rows entered exactly on 2023-10-30, the rolling window's first observable date, shared with the issued layer's window start PASS
[12.3] effective window: entered 2023-10-30 to 2026-11-02; ages as of 2026-11-03 are right-truncated at 1,100 days by the rolling entry window, and the pending stock is selected for slowness (fast applications leave the stock); recent entry cohorts' pending shares are mechanically high PASS
ALL SECTION 10 GATES PASS
```

Trap dispositions:
- 10.1.1 sentinels: Const_Cost zero (2,125 rows) and null (1 row) are "value not yet recorded" states in an applications layer (a recorded $0 construction does not occur in the companion issued layer either; the stated-value population is the 3,910 positive rows). Council_Dist has no 0 code in this layer (values 1-35 plus 3 nulls) - the issued layer's 0-sentinel trap does not carry over, verified rather than assumed.
- 10.1.2 polarity: the age filter (age >= 0) matched set sampled at both ends (youngest 1 day, oldest 1,100 days, both plausible filings); the excluded set is empty by construction and asserted.
- 10.1.4 categorical exhaustiveness: the Counter printed in the audit covers all 29 type values and matches stats.json key for key. Classes present only in pending: Building Blasting Permit (1), Building Residential - Tenant Finish Out (34). Classes present only in issued: the two storm-damage classes. Small niches: Blasting Permit (1, median age 1,100), HPR (1, 51 days), Residential - Other (22, 276.5 days).
- 10.1.5 nullable denominators: district split 6,033 + 3 = 6,036; the 3 null-district rows carry addresses/ZIPs but no district code (composition in stats.json).
- 10.2 controls: (a) timestamp control - entry epochs fall only at UTC hours 5/6 (Chicago midnights under CDT/CST), so local-date conversion and age arithmetic are safe; (b) partition control - zero permit-number overlap with the issued layer matches the metadata's definition of the two layers as disjoint populations; (c) window-edge control - 16 rows sit exactly on the shared window start date, the expected fingerprint of a rolling window boundary rather than a data spike.

## Internal consistency controls (from exploration, all reproduced by the build)

- Sum of pending entry-cohort counts by year (200 + 1,405 + 1,523 + 2,908) = 6,036 = layer rows.
- The fusion's pending side by entry year equals the applications layer's own entered-by-year counts exactly (2024: 1,405; 2025: 1,523; 2026: 2,908), and its issued side reconciles to the issued layer's entry-date distribution for window cohorts.
- 2023 entry-year cohort share (6.53 percent) is NOT used in the brief: entries before 2023-10-30 are unobservable on the pending side, so that denominator mixes observable issued rows with an unobservable pending population. The brief's cohort claims start at 2024 (years) and the chart marks 2023 Q4 within the window (the pending side of 2023 Q4 begins October 30; the chart's stated range for full quarters uses 2024 Q1 to 2025 Q4 only).
- Purpose is null on 18 records; no brief figure uses Purpose. Subdivision_Lot and Contact are unused. City/State/ZIP: ZIP present broadly (top-10 panel in data/); no ZIP figure relies on geocoding.

## Independent verification (Section 11, code/verify_independent.py; full output at data/verify_independent_output.txt and .json)

Method diversity per 11.1: (1) server-side ArcGIS queries (live service aggregates, no local computation); (2) a pyarrow recount of the raw snapshot (no pandas, no builder code) with ages computed by raw epoch arithmetic against a fixed as-of instant (2026-11-03 00:00 America/Chicago = 06:00 UTC, CST), a different computation path from the builder's local-date arithmetic. Result: **14/14 checks pass, with exact equality on every snapshot-side figure** (the live service still held the identical 6,036-row state at verification time; zero drift on counts, type distribution, cost total and max, and the Date_Issued-null definition check returns 0 server-side).

## QA cross-checks (brief text vs stats.json)

- Every number in brief-draft.md was checked against stats.json fields and the data/ panels after the final build: pending count, age median/mean/p90/max, all six age buckets with counts and shares, over-365 and over-730 counts and shares, cohort years and quarters, mature residue, all ten class-residue lines, all nine stock-age-by-class lines, all five mix lines, cost totals/median/max and the not-stated count, district lines (2, 5, 19, 17, 20, 6, 21, 13), ZIP lines (37207, 37209, 37203, 37211, 37206), composition (6,026 numbers, 10 shared-number rows, 4,620 parcels, 0 overlap), and the issued comparison (29,651; 29 days; 119 days).
- Use & Occupancy stock median age is 460.5 days in stats.json and is printed as 460 in the brief and charts (whole-day rounding, disclosed here).
- Derived shares in prose were recomputed from the underlying counts (47.5, 24.4, 12.9, 12.8, 13.0, 29.7, 69.3, 20.3 percent) and match the stored shares at the printed precision.
- Charts (all viewed after rendering, re-rendered after title-length fixes): chart_age_distribution.png, chart_age_by_type.png, chart_cohort_pending_share.png, chart_district_pending.png. Every chart prints its population, measure, and framing on the graphic.
- Hero (hero.png): generated illustration (hero_source/hero-art.webp) with the headline figure and framing composited from stats.json by code/hero_composite.py; VIEWED after compositing - headline "330 days", the sub-line, and the source line are fully legible, and the text sits on the illustration's clean dark field. hero-headline.txt records the same text.

## Adversarial notes (framing standard: what could make the headline wrong)

- **The 330-day median is a stock age, not a wait.** If any downstream use quotes it as "applicants wait 330 days," it becomes false: the median completed wait is 29 days. The brief states the distinction in its definitions, in Finding 1, on the hero, and on every chart. This is the single most likely misuse of the package.
- **The residue could be records, not projects.** If Codes purges or never purges closed-without-issuance filings in a way the metadata does not describe, the 12.9 percent mature residue mixes live and dead filings in unknown proportions. The brief never calls the residue a backlog of live projects; both readings are printed with the alternative.
- **Window truncation cuts both ways.** Ages above 1,100 days cannot appear, so the stock's true tail (applications pending since before October 2023) is invisible and the stock is, if anything, older than it looks. Printed in the brief.
- **Removals caveat for cohorts.** If applications closed without issuance are removed from the pending extract at some point, they vanish from both layers and the residue understates non-conversion. The metadata does not describe removals, and the presence of 1,474 records older than two years shows records are not aggressively purged; the caveat is printed in the brief's definitions.
- District medians are composition-sensitive (permit mix differs by district); printed unadjusted with the caveat, as in the issued brief.

## Sync gate (standards 10.3)

- README dependency list matches the imports across code/ (stdlib; matplotlib; numpy (transitively via pandas/matplotlib; imported directly by charts stack); pandas; Pillow; pyarrow; requests). No figure is hardcoded in charts.py or hero_composite.py: both read stats.json at run time.
- social-drafts.md leads with the verified headline pair (330-day stock median age against the 29-day completed-wait median) and the 12.9 percent mature residue, both traced in sources.md.

## Section 11.3 exception flags

- **First publication use of this dataset (11.3d):** the Building Permit Applications layer has not been used in a prior Machine Readable brief (its companion issued layer was, on 2026-11-03). The definitional traps found are recorded above and in the stack manifest: pending-stock selection, no status field, window truncation at 1,100 days, 35.2 percent of records with no stated value, no Census tract field, and a district field with nulls but no zero sentinel.
- **Codes Administration (11.3a/c):** named only as the layer's listed provider and as the lever owner in "Who can act" (a public agency acting in its public capacity). No individual is named anywhere in the package.
- **Timely hook, not a claim:** the Metro Council Planning and Zoning Committee meets November 4, 2026, and a special Council meeting is scheduled November 5, 2026 (Nashville.gov news release, October 2, 2026). No permit item appears on either agenda; the hook is timing for the "Who can act" ask, not evidence in any finding.

## Stack deposit

- Layer: building_permit_applications_clean at stack/nashville/layers/building_permit_applications_clean.parquet (6,036 rows), snapshot and manifest entry added 2026-11-03; see stack/nashville/manifest.json and stack/nashville/verification.md.

## Outcome

Package complete; Section 10 audit passes; independent verifier 14/14 with exact equality. Ready for the 2026-11-04 6:30 AM QA run (cron daily-civic-data-leads), which handles publication.
