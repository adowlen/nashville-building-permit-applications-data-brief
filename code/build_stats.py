#!/usr/bin/env python3
"""Builder: Nashville Building Permit Applications cleaned layer + stats.json.

Reads the 2026-11-03 raw snapshot of the applications layer (the pending
side of Nashville's permit queue) and, for the fusion comparison, the
same-day 2026-11-03 raw snapshot of the issued layer plus the published
2026-11-03 brief's stats.json (hidden_files/nashville-building-permits-
brief-2026-11-03/stats.json) for the issued population's headline figures.
Writes:
  stack/nashville/layers/building_permit_applications_clean.parquet
  <package>/stats.json and the package data panels (CSV) into data/.
Definitions (metadata v2.0, 2023-06-05): one row = an application for a
building permit that has NOT been issued; the dataset does not contain
issued building permits or trade applications; coverage is a rolling
three years, updated daily, extracted from ePermits/CityWorks.
Age = pull date (2026-11-03, America/Chicago) minus Date_Entered local
date. Cleaning never deletes rows: sentinel/invalid values are mapped to
unknown and flagged. Section 10.1 assertions run inline before stats are
written; a failed assertion aborts the build.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
PKG = HERE.parents[1]
STACK = HERE.parents[2] / "stack" / "nashville"
RAW = STACK / "snapshots" / "2026-11-03" / "building_permit_applications_raw.parquet"
RAW_ISSUED = STACK / "snapshots" / "2026-11-03" / "building_permits_issued_raw.parquet"
ISSUED_STATS = HERE.parents[2] / "nashville-building-permits-brief-2026-11-03" / "stats.json"
CLEAN = STACK / "layers" / "building_permit_applications_clean.parquet"
AS_OF = pd.Timestamp("2026-11-03")  # pull date, America/Chicago

df = pd.read_parquet(RAW)
N = len(df)
assert N > 5000, N

# --- Definition control: the metadata says this layer holds applications
# that have not been issued. Date_Issued must be null on every row; any
# non-null value would contradict the layer's own definition and is a
# hard stop, not a cleaning step.
n_issued_nonnull = int(df["Date_Issued"].notna().sum())
assert n_issued_nonnull == 0, f"Date_Issued non-null on {n_issued_nonnull} rows"

# --- dates: served epochs are local (America/Chicago) midnights.
# Control: UTC hour is only 5 (CDT) or 6 (CST) across Date_Entered.
hrs = pd.to_datetime(df["Date_Entered"], unit="ms", utc=True).dt.hour.unique()
assert set(hrs) <= {5, 6}, hrs
entered = pd.to_datetime(df["Date_Entered"], unit="ms", utc=True).dt.tz_convert("America/Chicago").dt.date
entered = pd.to_datetime(entered)
assert entered.notna().all()

out = df.copy()
out["date_entered_local"] = entered
out["age_days"] = (AS_OF - entered).dt.days
# 10.1.2 polarity: ages are >= 0 by construction; a negative age would
# mean an entry dated after the pull date. None may exist silently.
n_neg_age = int((out["age_days"] < 0).sum())
assert n_neg_age == 0, n_neg_age
out["pending_flag"] = True  # every row: Date_Issued is null (asserted above)

# 10.1.1 sentinel traps: Council_Dist has NO 0 sentinel in this layer
# (verified: values run 1-35; only nulls are unknown). Assert the claim
# rather than assuming the issued layer's pattern carries over.
n_dist_zero = int((df["Council_Dist"] == 0).sum())
assert n_dist_zero == 0, n_dist_zero
out["council_dist_known"] = out["Council_Dist"].where(out["Council_Dist"].between(1, 35))
out["council_dist_unknown_flag"] = out["council_dist_known"].isna()
n_dist_null = int(df["Council_Dist"].isna().sum())
assert int(out["council_dist_unknown_flag"].sum()) == n_dist_null

# Cost: stated value. In this layer 0 (and the single null) mean no
# stated value has been recorded - the issued layer carries a positive
# stated value on every row by issuance. 10.1.1: map 0/null to
# "not stated" and exclude them from every cost figure, with counts.
out["cost_stated_flag"] = df["Const_Cost"].notna() & (df["Const_Cost"] > 0)
n_cost_zero = int((df["Const_Cost"] == 0).sum())
n_cost_null = int(df["Const_Cost"].isna().sum())
n_cost_negative = int((df["Const_Cost"] < 0).sum())
assert n_cost_negative == 0
out["const_cost"] = df["Const_Cost"].astype(float)

# Coordinates: check completeness, 0,0 sentinel, Nashville bbox.
n_coord_bad = int(df["Lat"].isna().sum() + ((df["Lat"] == 0) & (df["Lon"] == 0)).sum())
assert n_coord_bad == 0
assert df["Lat"].between(35.9, 36.5).all() and df["Lon"].between(-87.1, -86.4).all()
out["coords_unknown_flag"] = False

# Census tract: this layer serves NO census tract field (unlike the
# issued layer). Recorded as a layer difference, not repaired.
assert "Census_Tract" not in df.columns

out.to_parquet(CLEAN, index=False)

ages = out["age_days"]
def age_stats(frame):
    a = frame["age_days"]
    return {
        "n_permits": int(len(frame)),
        "median_days": float(a.median()),
        "mean_days": round(float(a.mean()), 1),
        "p90_days": float(a.quantile(0.9)),
        "max_days": int(a.max()),
        "over_365_share": round(float((a > 365).mean()), 4),
        "over_730_share": round(float((a > 730).mean()), 4),
    }

age_all = age_stats(out)
age_all["over_365_count"] = int((ages > 365).sum())
age_all["over_730_count"] = int((ages > 730).sum())
age_all["over_180_count"] = int((ages > 180).sum())
age_all["over_90_count"] = int((ages > 90).sum())
age_all["within_30_count"] = int((ages <= 30).sum())

_bucket_defs = [("0-30 days", (ages >= 0) & (ages <= 30)),
                ("31-90 days", (ages >= 31) & (ages <= 90)),
                ("91-180 days", (ages >= 91) & (ages <= 180)),
                ("181-365 days", (ages >= 181) & (ages <= 365)),
                ("366-730 days", (ages >= 366) & (ages <= 730)),
                ("over 730 days", ages > 730)]
age_distribution = [{"bucket": name, "permits": int(mask.sum()),
                     "share_of_pending": round(float(mask.mean()), 4)} for name, mask in _bucket_defs]
assert sum(b["permits"] for b in age_distribution) == N

# 10.1.4 categorical exhaustiveness: full Counter of the type field.
type_counts_all = df["Permit_Type_Description"].value_counts(dropna=False)
assert int(type_counts_all.sum()) == N
type_counts = {str(k): int(v) for k, v in type_counts_all.items()}

by_type = {}
for name, g in out.groupby("Permit_Type_Description"):
    by_type[name] = age_stats(g)
by_type = dict(sorted(by_type.items(), key=lambda kv: -kv[1]["n_permits"]))

# Cost figures on stated rows only (10.1.1 / 10.1.5: denominator printed).
stated = out[out["cost_stated_flag"]]
cost = {
    "definition": "stated value of construction (applicant-stated, per metadata), computed only on rows with a recorded positive value",
    "rows_with_stated_value": int(len(stated)),
    "rows_zero_value": n_cost_zero,
    "rows_null_value": n_cost_null,
    "not_stated_rows": int(N - len(stated)),
    "not_stated_share": round(float((N - len(stated)) / N), 4),
    "total_stated": float(stated["Const_Cost"].sum()),
    "median_stated": float(stated["Const_Cost"].median()),
    "mean_stated": round(float(stated["Const_Cost"].mean()), 0),
    "max_stated": float(stated["Const_Cost"].max()),
    "min_positive": float(stated["Const_Cost"].min()),
}

# Geography: district table over known-district rows (10.1.5).
known = out[~out["council_dist_unknown_flag"]]
assert len(known) + int(out["council_dist_unknown_flag"].sum()) == N
dist = known.groupby("council_dist_known").agg(
    permits=("Permit__", "size"),
    median_age=("age_days", "median"),
    stated_total=("Const_Cost", lambda s: float(s[s > 0].sum())),
    stated_rows=("cost_stated_flag", "sum"))
dist_rows = [{"district": int(i), "permits": int(r.permits), "median_age_days": float(r.median_age),
              "stated_total": float(r.stated_total), "stated_rows": int(r.stated_rows)}
             for i, r in dist.sort_values("permits", ascending=False).iterrows()]
top_district_by_stated = max(dist_rows, key=lambda r: r["stated_total"])
zipg = out.groupby("ZIP").agg(permits=("Permit__", "size"), median_age=("age_days", "median"))
zip_rows = [{"zip": str(i), "permits": int(r.permits), "median_age_days": float(r.median_age)}
            for i, r in zipg.sort_values("permits", ascending=False).head(10).iterrows()]

# --- Fusion with the issued layer (same-day pull): cohort resolution.
iss = pd.read_parquet(RAW_ISSUED)
iss_entered = pd.to_datetime(pd.to_datetime(iss["Date_Entered"], unit="ms", utc=True)
                             .dt.tz_convert("America/Chicago").dt.date)
issued_stats = json.loads(ISSUED_STATS.read_text())
assert len(iss) == issued_stats["rows"], (len(iss), issued_stats["rows"])

# Cross-layer permit-number partition control (10.2): the two layers
# must share no permit number - a number in both would contradict the
# metadata's partition (issued permits are not in the applications layer).
overlap = set(df["Permit__"].astype(str)) & set(iss["Permit__"].astype(str))
n_overlap = len(overlap)
assert n_overlap == 0, n_overlap

def cohort_table(idx_pending, idx_issued):
    p = idx_pending.value_counts().sort_index()
    i = idx_issued.value_counts().sort_index()
    keys = sorted(set(p.index) | set(i.index))
    rows = []
    for k in keys:
        pn, isn = int(p.get(k, 0)), int(i.get(k, 0))
        rows.append({"period": str(k), "issued": isn, "pending": pn,
                     "observed_total": isn + pn,
                     "pending_share": round(pn / (isn + pn), 4) if (isn + pn) else None})
    return rows

cohort_years = cohort_table(entered.dt.year, iss_entered.dt.year)
cohort_quarters = cohort_table(entered.dt.to_period("Q"), iss_entered.dt.to_period("Q"))

# Mature-cohort residual (entries in calendar 2024-2025, the two full
# years whose cohorts have had at least 10 months to resolve).
m_pen = out[(entered >= "2024-01-01") & (entered < "2026-01-01")]
m_iss = iss[(iss_entered >= "2024-01-01") & (iss_entered < "2026-01-01")]
mature = {"entry_years": "2024-2025", "pending": int(len(m_pen)), "issued": int(len(m_iss)),
          "observed_total": int(len(m_pen) + len(m_iss)),
          "pending_share": round(len(m_pen) / (len(m_pen) + len(m_iss)), 4)}

# Per-class mature-cohort residual (classes with >= 100 observed).
pc = m_pen["Permit_Type_Description"].value_counts()
ic = m_iss["Permit_Type_Description"].value_counts()
class_residual = []
for name in sorted(set(pc.index) | set(ic.index)):
    pn, isn = int(pc.get(name, 0)), int(ic.get(name, 0))
    if pn + isn >= 100:
        class_residual.append({"permit_type": name, "pending": pn, "issued": isn,
                               "observed_total": pn + isn,
                               "pending_share": round(pn / (pn + isn), 4)})
class_residual.sort(key=lambda r: -r["pending_share"])

# Mix comparison: each class's share of the pending stock vs its share
# of the issued population (shares on each population's own total).
iss_type_counts = iss["Permit_Type_Description"].value_counts()
mix_rows = []
for name in sorted(set(type_counts) | set(iss_type_counts.index)):
    pn, isn = type_counts.get(name, 0), int(iss_type_counts.get(name, 0))
    mix_rows.append({"permit_type": name, "pending_n": pn, "issued_n": isn,
                     "pending_share": round(pn / N, 4),
                     "issued_share": round(isn / len(iss), 4)})
mix_rows.sort(key=lambda r: -r["pending_n"])

entered_year_counts = entered.dt.year.value_counts().sort_index()
entered_month_counts = entered.dt.to_period("M").astype(str).value_counts().sort_index()

stats = {
  "dataset": "Nashville Building Permit Applications (Building_Permit_Applications_Feature_Layer_view layer 0)",
  "snapshot_date": "2026-11-03",
  "as_of_date": "2026-11-03",
  "rows": N,
  "unit": "one row = one building permit application that has NOT been issued (metadata v2.0, 2023-06-05); issued building permits and trade applications are NOT in this dataset; the layer carries no status field, so it does not record whether an application is in review, awaiting the applicant, or no longer being pursued",
  "coverage": {
    "date_entered_min": str(entered.min().date()), "date_entered_max": str(entered.max().date()),
    "window_rule": "rolling three years per source metadata; observed entries run 2023-10-30 to 2026-11-02, so no application entered before 2023-10-30 is observable and no pending age above 1,100 days can appear",
    "rows_at_window_edge_2023_10_30": int((entered == "2023-10-30").sum()),
    "rows_entered_before_2023_11_03": int((entered < "2023-11-03").sum())
  },
  "age_all": age_all,
  "age_distribution": age_distribution,
  "age_by_type": by_type,
  "type_counts_all_rows": type_counts,
  "types_only_in_pending": sorted(set(type_counts) - set(iss_type_counts.index)),
  "types_only_in_issued": sorted(set(iss_type_counts.index) - set(type_counts)),
  "cost": cost,
  "geography": {
    "council_district": {
      "known_rows": int(len(known)), "unknown_rows": int(out["council_dist_unknown_flag"].sum()),
      "unknown_composition": f"{n_dist_null} rows null; no district-0 sentinel rows exist in this layer (asserted)",
      "top_district_by_stated": {"district": int(top_district_by_stated["district"]),
                                 "stated_total": top_district_by_stated["stated_total"],
                                 "share_of_all_stated": round(top_district_by_stated["stated_total"] / cost["total_stated"], 4)},
      "by_district_sorted_by_pending_count": dist_rows
    },
    "zip_top10_by_pending": zip_rows,
    "coords": "Lat/Lon present on 100% of rows, no 0,0 sentinel, all inside Nashville-Davidson bbox",
    "census_tract": "this layer serves no census tract field (the issued layer does); no tract figure is computed"
  },
  "cohort_resolution": {
    "basis": "applications entered in a period and observable in either layer on 2026-11-03: issued (companion issued layer, same-day pull) or still pending (this layer). Applications closed without issuance and removed from the pending extract would appear in neither layer; the metadata does not describe such removals",
    "by_entry_year": cohort_years,
    "by_entry_quarter": cohort_quarters,
    "mature_cohorts_2024_2025": mature,
    "class_residual_2024_2025_min100": class_residual
  },
  "mix_comparison": mix_rows,
  "cross_layer_controls": {
    "date_issued_null_rows": int(df["Date_Issued"].isna().sum()),
    "permit_numbers_in_both_layers": n_overlap,
    "issued_rows_same_day_pull": int(len(iss))
  },
  "duplicates": {"permit_number_duplicate_rows": int(df["Permit__"].duplicated().sum()),
                 "unique_permit_numbers": int(df["Permit__"].nunique()),
                 "unique_parcels": int(df["Parcel"].nunique()),
                 "note": "rows sharing a permit number are multi-parcel or multi-unit filings under one number (the same pattern as the issued layer); rows are the unit throughout"},
  "entered_by_year": {str(k): int(v) for k, v in entered_year_counts.items()},
  "entered_by_month": {str(k): int(v) for k, v in entered_month_counts.items()},
  "purpose_null_rows": int(df["Purpose"].isna().sum()),
  "issued_comparison": {
    "source": "2026-11-03 brief stats.json (same-day pull of the companion issued layer)",
    "issued_rows": issued_stats["rows"],
    "issued_median_wait_days": issued_stats["timing_all_valid"]["median_days"],
    "issued_mean_wait_days": issued_stats["timing_all_valid"]["mean_days"],
    "issued_window": f"{issued_stats['coverage']['date_issued_min']} to {issued_stats['coverage']['date_issued_max']}",
    "tenant_finish_out_median_wait_days": issued_stats["timing_by_type"]["Building Commercial - Tenant Finish Out"]["median_days"]
  },
  "censoring_note": "Pending ages are ages of a stock observed on one date (2026-11-03), not completed waits: applications that resolve quickly leave the stock, so the stock is selected for slowness and its median age is not comparable to a completed-wait median. Ages are also right-truncated by the layer's rolling three-year entry window (nothing entered before 2023-10-30 is observable). Recent entry cohorts' pending shares are mechanically high because little time has passed; the mature 2024-2025 cohorts are the like-for-like basis."
}

# Data panels (CSV) for the package
DATA = PKG / "data"; DATA.mkdir(parents=True, exist_ok=True)
pd.DataFrame([{"permit_type": k, **v} for k, v in by_type.items()]).to_csv(DATA / "age_by_type_panel.csv", index=False)
pd.DataFrame(dist_rows).to_csv(DATA / "district_pending_panel.csv", index=False)
pd.DataFrame(cohort_years).to_csv(DATA / "cohort_by_year_panel.csv", index=False)
pd.DataFrame(cohort_quarters).to_csv(DATA / "cohort_by_quarter_panel.csv", index=False)
pd.DataFrame(class_residual).to_csv(DATA / "class_residual_panel.csv", index=False)
pd.DataFrame(mix_rows).to_csv(DATA / "mix_comparison_panel.csv", index=False)
pd.DataFrame(age_distribution).to_csv(DATA / "age_distribution_panel.csv", index=False)
pd.DataFrame(zip_rows).to_csv(DATA / "zip_top10_panel.csv", index=False)

(PKG / "stats.json").write_text(json.dumps(stats, indent=2))
print(f"clean layer: {CLEAN} rows={len(out)}")
print(f"pending median age {age_all['median_days']}d, mean {age_all['mean_days']}d, over-365 {age_all['over_365_count']} ({age_all['over_365_share']}), over-730 {age_all['over_730_count']} ({age_all['over_730_share']})")
print(f"stated: {cost['rows_with_stated_value']} rows, total ${cost['total_stated']:,.0f}, median ${cost['median_stated']:,.0f}; not stated {cost['not_stated_rows']} ({cost['not_stated_share']})")
print(f"mature cohort residual: {mature['pending']}/{mature['observed_total']} = {mature['pending_share']}")
print(f"cross-layer permit overlap: {n_overlap}")
print("BUILD OK")
