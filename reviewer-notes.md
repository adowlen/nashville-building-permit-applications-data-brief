# Reviewer notes - Nashville building permit applications brief (2026-11-04)

## Claims most likely to be challenged

1. **"Median age 330 days" read as "applicants wait 330 days."** The most likely challenge and the most likely misuse. The 330 days is the median age of the pending stock, which is selected for slowness (fast applications leave it). The median completed wait among issued permits is 29 days. The brief states the distinction in its definitions, in Finding 1, on the hero, and on every chart; the two figures are always printed as a pair with their populations named. If a critic says the headline misleads, the defense is that the package never prints 330 days without its population attached - but the risk is real and is why the hero sub-line carries the 29-day figure.
2. **The 12.9 percent mature-cohort residue as "never issued."** The residue is "not issued in either layer's record as of November 3, 2026." Applications closed without issuance and removed from the pending extract would be invisible in both layers and would bias the residue down; applications denied or withdrawn but never purged bias its interpretation, not its arithmetic. The metadata does not describe removals. The brief prints the caveat in the definitions and offers both readings (live long-cycle projects vs dead filings) in "What this might mean."
3. **Ages truncated at 1,100 days.** The rolling entry window means nothing pending longer than the window can appear; the stock's true age tail is unobservable. The brief prints this with the count at the edge (16 rows on 2023-10-30). A critic could argue the window start shared by both layers is an artifact of the issued layer's issue-date window; checked: the applications layer's own coverage begins exactly 2023-10-30 and its metadata defines a rolling three-year entry window, so the truncation is the layer's own rule.
4. **District 19's $384.8M stated pending value.** Computed on 178 of the district's 424 records; the other 246 state no value. The brief prints the recorded-on count with the figure. District rankings by stated value are sensitive to which large projects have recorded values; the count-based rankings (District 2 first) do not share that sensitivity.
5. **Class residue for Commercial New (37.1 percent).** Based on 905 observed applications entered 2024-2025. The strongest innocent explanation (multi-year pre-issuance cycles for large projects) is printed. The figure is a share of observed applications, not a failure rate: some of the 336 will still issue.
6. **Whole-day rounding.** Use & Occupancy's stock median age is 460.5 days, printed as 460; the stated-value median is $150,393.50, printed as $150,394. Both roundings are disclosed in verification.md.

## Checks that could not be completed

- **No status split is possible.** The layer has no status or activity field, so the package cannot say how many pending records are in active review, awaiting the applicant, denied, withdrawn, or superseded. This is the dataset's central gap and the brief's main ask; it is a limit, not an oversight.
- **No tract-level analysis is possible.** Unlike the issued layer, this layer carries no Census tract field. District and ZIP are the finest geographies published; no tract claim appears anywhere in the package.
- **No project-level dedupe beyond permit number.** One project can file multiple applications (and one permit number can cover multiple parcels); the package counts applications throughout and says so. Project-level counts would require the Contact/Purpose fields to carry reliable project identity, which they do not (Purpose is null on 18 records and free-text elsewhere).
- **Pre-window pending stock is unobservable.** Applications entered before October 30, 2023 and still pending do not exist in this layer. The brief cannot size that population; the truncation note is the disclosure.
- **The 2023 entry year is excluded from cohort claims** (pending side unobservable for most of it); cohort claims rest on 2024-2025 entries and the eight full quarters of those years.

## Findings that surprised us

- **The residue is flat across two full entry years (12.8 and 13.0 percent).** A queue clearing a backlog would show falling residue in later cohorts; a stable one-in-eight share looks structural rather than episodic.
- **Sign permits invert completely between the two layers' views:** the lowest mature residue of any large class (3.9 percent) and the oldest median age in the pending stock (518 days, on only 82 records). Small, ancient residues in fast classes are exactly what a never-purged records tail looks like - suggestive for Reading 1, not proof.
- **A third of the pending stock states no construction value at all** (35.2 percent), against zero such records among issued permits in the companion layer. The applications layer's zeros are a workflow state (value not yet recorded), which is why every cost figure in the brief is fenced to the 3,910 stated records.
- **District 13's shape:** only 129 pending applications but $184.5M of stated value (median age just 84 days) - a small number of very large, recent filings, the opposite profile from District 2's 480 older filings.

## Flags

- Hero and all four charts were VIEWED after final rendering (charts re-rendered once to fix clipped title lines; hero recomposited once to keep the source line on the dark field). All text legible.
- The live service returned the identical 6,036-row state during independent verification (zero drift); the layer updates daily, so the 6:30 AM run should expect small count drift and should not treat it as an error.
- Publication is NOT done by this package: the 2026-11-04 6:30 AM QA run (cron daily-civic-data-leads) creates the repo and publishes if its gates pass.
