# Nashville building permits, the pending side: 6,036 applications were still unissued on November 3, 2026, their median age was 330 days, and about 1 in 8 applications entered in 2024-2025 remains unissued

**One-line finding:** Nashville's open permit queue held 6,036 unissued building permit applications on November 3, 2026; half were more than 330 days old and 47.5 percent were more than a year old, while the median completed wait among permits that did issue in the last three years was 29 days (companion brief, November 3, 2026).

## Source and definitions

The dataset is the Building Permit Applications layer published by NashvilleOpenData (ArcGIS item 4c38be57f3fd47d6844ba820d1ea677c), pulled November 3, 2026: 6,036 records. Per the layer's own metadata (v2.0, archived with this package), each record is an application for a building permit that has not been issued, over a rolling three-year period; the layer does not contain issued building permits, trade applications, or trade permits. The source system is Cityworks/ePermits, provided by Codes Administration, Zoning Review Division, updated daily.

Fields used: permit type (Permit_Type_Description), date entered, construction cost as stated by the applicant, council district, ZIP code, parcel, and coordinates.

Definitions used in this brief:

- **Pending application / the pending stock:** a record in this layer on the pull date. The layer records only that an application has not been issued. It carries no status field, so a long-pending record may be in active review, awaiting action by the applicant, denied or withdrawn without being removed, or superseded by a newer filing. The data cannot distinguish those states, and this brief does not claim to.
- **Age:** days from the application's entry date to the pull date, November 3, 2026, in America/Chicago local dates. Ages describe the pending stock only. They are not waits: an application that issues quickly leaves the stock, so the stock is selected for slowness by construction. The comparison figure for completed waits is the companion issued layer, pulled the same day: among 29,651 permits issued in the last three years, the median entry-to-issuance wait was 29 days.
- **Observed application (cohort figures only):** an application entered in a stated period that appears in either layer on the pull date, issued or still pending. Applications closed without issuance and removed from the pending extract would appear in neither layer; the metadata does not describe such removals, and the layer's old stock (Finding 1) shows records persisting for years.
- **Construction cost:** the applicant-stated value of construction, counted only where a positive value is recorded. 2,126 of the 6,036 records (35.2 percent) carry a zero or blank value, read here as not yet stated; they are excluded from every cost figure, with the count printed beside it.
- **Window:** entries run from October 30, 2023 to November 2, 2026. The rolling three-year entry window truncates every age at 1,100 days: no application entered before October 30, 2023 is observable in this layer, however long it has been pending.

## Finding 1: The pending stock is old. Half of it has been waiting more than 330 days, and nearly half more than a year

Of the 6,036 applications recorded as not issued on November 3, 2026, the median age was 330 days and the mean was 417 days. The oldest observable age was 1,100 days, the window's ceiling; 16 records were entered on October 30, 2023, the first observable date.

The age distribution of the stock:

- 0 to 30 days: 580 applications (9.6 percent)
- 31 to 90 days: 816 (13.5 percent)
- 91 to 180 days: 693 (11.5 percent)
- 181 to 365 days: 1,082 (17.9 percent)
- 366 to 730 days: 1,391 (23.1 percent)
- Over 730 days: 1,474 (24.4 percent)

In total, 2,865 applications (47.5 percent) had been pending more than a year and 1,474 (24.4 percent) more than two years. Only 580 (9.6 percent) were a month old or less. Read against the companion issued layer's median completed wait of 29 days, the stock's shape is the point: applications that resolve leave, so what accumulates is exactly the residue that does not resolve quickly. The 330-day figure is the median age of that residue, not the wait a typical applicant experiences.

## Finding 2: Mature cohorts leave a stable residue of about 1 in 8. Of applications entered in 2024 and 2025, 12.9 percent are still unissued

Joining the two same-day layers by entry period shows how much of each entry cohort remains unissued. Applications entered in 2024: 1,405 of 10,965 observed applications (12.8 percent) were still pending on November 3, 2026. Applications entered in 2025: 1,523 of 11,689 (13.0 percent). Combined, 2,928 of 22,654 applications entered in 2024-2025 (12.9 percent) remain unissued, with exposure running from ten months (end of 2025 entries) to just under three years (start of 2024 entries). The eight full entry quarters of 2024 and 2025 each sit in a narrow band, from 9.4 percent (2024 Q4) to 15.7 percent (2024 Q1).

Recent cohorts read higher for a mechanical reason and are not evidence of a slowdown: applications entered in 2026 show 29.7 percent still pending (2,908 of 9,788) because most have had months, not years, to issue, and the partial 2026 Q4 (entries from October 1 to November 2) shows 69.3 percent (649 of 937). The mature-cohort figures are the informative ones: after two to three years, about one application in eight has still not converted to an issued permit in either layer's record.

## Finding 3: The residue is concentrated by class. 37.1 percent of commercial new-construction applications entered in 2024-2025 are still unissued, against 3.9 percent of sign permits

Among applications entered in 2024-2025, by permit class (classes with at least 100 observed applications):

- Building Commercial - New: 37.1 percent still unissued (336 of 905)
- Building Use & Occupancy: 30.5 percent (114 of 374)
- Building Commercial - Addition: 20.6 percent (41 of 199)
- Building Commercial - Shell: 19.3 percent (21 of 109)
- Building Demolition Permit: 14.1 percent (235 of 1,671)
- Building Residential - New: 12.5 percent (1,052 of 8,390)
- Building Commercial - Tenant Finish Out: 11.4 percent (133 of 1,169)
- Building Commercial - Rehab: 9.3 percent (255 of 2,748)
- Building Tree Removal Permit: 4.8 percent (11 of 229)
- Building Sign Permit: 3.9 percent (60 of 1,554)

The stock's age profile tells the same story from the other side. Median ages within the pending stock, for classes with at least 80 pending: sign permits 518 days (82 pending), residential rehab 498 days (396), use and occupancy 460 days (188), residential addition 453 days (567), residential new 443 days (1,945), demolition 391 days (441), commercial new 335 days (650), commercial tenant finish out 201 days (468), and commercial rehab 173 days (822).

The two views can rank a class oppositely, and sign permits show why. Only 3.9 percent of mature sign applications remain unissued, the lowest residue of any large class, yet the 82 that remain have the oldest median age in the stock. A class can clear almost everything it receives and still accumulate a small, very old residue. Commercial tenant finish out inverts the issued brief's headline the same way: it carried the slowest median completed wait among issued permits (119 days) but its pending stock is comparatively young (median 201 days), because most of its applications do eventually issue.

## Finding 4: The pending mix is not the issued mix. Commercial new construction is 10.8 percent of the pending stock but 2.9 percent of issued permits

Comparing each class's share of the 6,036 pending applications with its share of the 29,651 permits issued in the last three years:

- Building Commercial - New: 10.8 percent of pending (650 applications) vs 2.9 percent of issued
- Building Use & Occupancy: 3.1 percent (188) vs 1.3 percent
- Building Commercial - Tenant Finish Out: 7.8 percent (468) vs 5.3 percent
- Building Sign Permit: 1.4 percent (82) vs 6.7 percent
- Building Residential - New: 32.2 percent (1,945) vs 36.9 percent, the largest class in both populations

Classes whose share of the stock runs well above their share of completed permits are the classes where applications accumulate; classes underrepresented in the stock, like sign permits, are classes where almost everything filed eventually issues.

## Finding 5: District 2 holds the most pending applications and the oldest large-district stock; District 19 holds a fifth of the stated pending value

Pending applications by council district (6,033 of 6,036 records carry a district; 3 are blank, and this layer uses no zero district code):

- District 2: 480 pending, the most of any district, with a median age of 715 days, the oldest median among the ten highest-count districts
- District 5: 464 pending, median age 272 days
- District 19: 424 pending, median age 330 days
- District 17: 379 pending, median age 257 days
- District 20: 330 pending, median age 139 days
- District 6: 313 pending, median age 515 days
- District 21: 299 pending, median age 621 days

By ZIP code, 37207 holds the most pending applications (718, median age 322 days), followed by 37209 (541, median age 411 days), 37203 (497, median age 126 days), 37211 (406, median age 315 days), and 37206 (385, median age 515 days).

Stated construction value in the pending stock totals $1,896,350,756 across the 3,910 records with a recorded value (median $150,394; largest single stated value $150,000,000), with 2,126 records (35.2 percent) stating no value. District 19 alone accounts for $384,826,611 of the stated total, 20.3 percent, recorded on 178 of its 424 applications. District 13 shows the opposite shape: only 129 pending applications but $184,484,262 of stated value on 77 of them. District medians are unadjusted; districts differ in permit mix, and class ages differ (Finding 3).

Composition note: the 6,036 records carry 6,026 distinct permit numbers (10 records share a number with another record, the multi-parcel filing pattern also seen in the issued layer) across 4,620 distinct parcels. No permit number appears in both this layer and the issued layer: the two layers partition the permit system exactly as their metadata describe.

## What this might mean

This section is interpretation. The findings above are measurements; the readings below are contestable, and each is paired with the strongest alternative explanation the data cannot rule out.

**Reading 1: roughly one application in eight never converts, and the queue Nashville sees is partly a records artifact.** A stable 12.9 percent residue across two full entry years, and a stock whose median age (330 days) is eleven times the median completed wait (29 days), are what a permit system produces when a fixed share of filings is never resolved in either direction: not issued, and not closed. If a large part of that residue is dead filings (projects abandoned, applications superseded, denials never recorded as closures), then the published pending count overstates the live workload by an unknown amount, and any staffing or backlog decision made from the raw count inherits that error. The strongest alternative explanation is that the residue is mostly live: large commercial projects can legitimately spend years in pre-issuance review, financing, and revision cycles, and the residue's concentration in commercial new construction (37.1 percent) fits that reading too. The layer cannot adjudicate between the two, because it records no status. That gap, not any single number, is the finding with a lever attached (see Who can act).

**Reading 2: the queue's problem is a tail, not the typical case.** The typical completed wait is 29 days at the median. What accumulates is a tail of filings that stall early and then sit. Interventions aimed at the median applicant would miss the measured problem; interventions aimed at identifying and closing or escalating aged filings address the stock that actually exists. The alternative explanation is selection alone: any queue with varied processing times produces an old stock, even a healthy one, and the stock's age by itself proves nothing about dysfunction. That alternative is correct as far as it goes, and it is why this brief's cohort figures matter more than its stock ages: the 12.9 percent mature-cohort residue is the measurement a healthy-queue explanation has to account for, and the published data offers no field that would let anyone check whether it does.

## Who can act

- **Metro Codes Administration (publishes this layer; Zoning Review Division is the listed provider):** add an application status field to the public layer (in review, awaiting applicant, denied, withdrawn, superseded), or publish a periodic purge of records closed without issuance, so the pending stock separates live work from dead filings. Cost class: staff time and a minor change to an existing daily extract. Outcome measure: the share of the pending stock carrying a live status, published with the layer; the 12.9 percent mature residue becomes decomposable into live and closed.
- **Metro Council, Planning and Zoning Committee (meets November 4, 2026):** request a briefing from Codes Administration on the pending stock's age profile and status composition, and ask for the stock to be reported quarterly with ages and statuses. Cost class: none beyond existing oversight time. Outcome measure: a recurring published report in which the pending count, the over-one-year count, and the status split can be tracked quarter to quarter against this brief's baseline (6,036 pending; 2,865 over one year).
- **Applicants and their expediters with aged filings:** verify the status of any application older than a year in ePermits, the source system named in the layer's metadata, and withdraw filings for projects that will not proceed. Cost class: minutes per filing. Outcome measure: withdrawals shrink the residue directly; if aged filings are mostly live, the verification itself produces the status information the public layer lacks.

## Data notes

- Ages are computed to the pull date, November 3, 2026, and the layer updates daily; a later pull will show different counts. The figures here are reproducible from the archived snapshot in this package.
- The layer carries no Census tract field (the issued layer does), so no tract-level figures are published in this brief.
- Entry timestamps are recorded at America/Chicago midnights; ages were computed on local dates and verified against raw epoch arithmetic by an independent check (verification.md).
- District is blank on 3 records. Coordinates are present and inside the Nashville area on all 6,036 records.
- The issued-layer comparison figures are from the November 3, 2026 brief's same-day pull of Building_Permits_Issued_Feature_Layer_view (29,651 permits issued from October 30, 2023 to November 2, 2026).

## Files in this package

See README.md for the full manifest, the pull script, the cleaned Nashville stack layer, and verification.md for the methods checklist and pre-flight audit record.
