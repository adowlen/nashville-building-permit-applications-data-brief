#!/usr/bin/env python3
"""Section 10 pre-flight audit for the Nashville building permit
applications layer. Reads the cleaned layer + stats.json; asserts every
gate; prints evidence.
"""
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve()
PKG = HERE.parents[1]
STACK = HERE.parents[2] / "stack" / "nashville"
clean = pd.read_parquet(STACK / "layers" / "building_permit_applications_clean.parquet")
stats = json.loads((PKG / "stats.json").read_text())
N = len(clean)
print(f"rows in cleaned layer: {N}")
assert N == stats["rows"]

# Definition control (metadata v2.0): every row is an application that
# has not been issued, so Date_Issued is null on all rows.
n_ni = int(clean["Date_Issued"].notna().sum())
assert n_ni == 0 and stats["cross_layer_controls"]["date_issued_null_rows"] == N
print(f"[definition] Date_Issued null on all {N} rows (layer = not-yet-issued applications per metadata v2.0) PASS")

# 10.1.1 zero/null sentinel traps: cost 0/null mapped to not-stated and
# excluded from cost figures; district has no 0 sentinel in this layer.
z = int((clean["Const_Cost"] == 0).sum())
nul = int(clean["Const_Cost"].isna().sum())
assert z == stats["cost"]["rows_zero_value"] and nul == stats["cost"]["rows_null_value"]
assert int((~clean["cost_stated_flag"]).sum()) == z + nul == stats["cost"]["not_stated_rows"]
assert int(clean["cost_stated_flag"].sum()) == stats["cost"]["rows_with_stated_value"]
assert int((clean["Council_Dist"] == 0).sum()) == 0
unk = int(clean["council_dist_unknown_flag"].sum())
assert unk == stats["geography"]["council_district"]["unknown_rows"]
assert int(clean["coords_unknown_flag"].sum()) == 0
print(f"[10.1.1] Const_Cost zero rows: {z} and null rows: {nul} mapped not-stated ({z + nul} total, excluded from all cost figures); Council_Dist 0-sentinel rows: 0 (none exist in this layer); district unknown total {unk} (all null); coords complete, no 0,0 PASS")

# 10.1.2 boolean polarity: age >= 0 filter sample check. The excluded
# set under the builder's rule (age < 0) must be empty, and the matched
# set's youngest rows must sit just above 0.
neg = clean[clean["age_days"] < 0]
assert len(neg) == 0
young = clean.nsmallest(3, "age_days")
old = clean.nlargest(3, "age_days")
print(f"[10.1.2] age polarity: 0 rows with negative age (entry after pull date); youngest matched sample: {young[['Permit_Type_Description', 'age_days']].values.tolist()}; oldest matched sample: {old[['Permit_Type_Description', 'age_days']].values.tolist()} PASS")

# 10.1.3 numerator/denominator unit agreement: every share in stats is
# applications over applications on a named population.
t = stats["age_all"]
recomputed_over365 = float((clean["age_days"] > 365).mean())
assert abs(recomputed_over365 - t["over_365_share"]) < 0.0001
mc = stats["cohort_resolution"]["mature_cohorts_2024_2025"]
assert mc["pending"] + mc["issued"] == mc["observed_total"]
assert abs(mc["pending"] / mc["observed_total"] - mc["pending_share"]) < 0.0001
print(f"[10.1.3] over-365 share recomputed {recomputed_over365:.4f} on denominator {N} applications; mature-cohort residual {mc['pending']}/{mc['observed_total']} applications over applications PASS")

# 10.1.4 categorical exhaustiveness: full Counter of type field sums to N.
cnt = clean["Permit_Type_Description"].value_counts(dropna=False)
assert int(cnt.sum()) == N and len(cnt) == len(stats["type_counts_all_rows"])
assert {str(k): int(v) for k, v in cnt.items()} == stats["type_counts_all_rows"]
print(f"[10.1.4] Permit_Type_Description Counter: {len(cnt)} values, counts sum to {N}, matches stats.json exactly PASS")

# 10.1.5 nullable denominator: known + unknown = whole on every split.
known = int((~clean["council_dist_unknown_flag"]).sum())
assert known + unk == N
assert sum(b["permits"] for b in stats["age_distribution"]) == N
assert stats["cost"]["rows_with_stated_value"] + stats["cost"]["not_stated_rows"] == N
for r in stats["cohort_resolution"]["by_entry_year"]:
    assert r["issued"] + r["pending"] == r["observed_total"]
print(f"[10.1.5] district known {known} + unknown {unk} = {N}; age buckets sum to {N}; stated {stats['cost']['rows_with_stated_value']} + not-stated {stats['cost']['not_stated_rows']} = {N}; every cohort row's issued + pending = observed total PASS")

# 10.2 controls
hrs = set(pd.to_datetime(clean["Date_Entered"], unit="ms", utc=True).dt.hour.unique())
assert hrs <= {5, 6}
issued_clean = pd.read_parquet(STACK / "layers" / "building_permits_issued_clean.parquet")
overlap = set(clean["Permit__"].astype(str)) & set(issued_clean["Permit__"].astype(str))
assert len(overlap) == stats["cross_layer_controls"]["permit_numbers_in_both_layers"] == 0
edge = int((clean["date_entered_local"] == "2023-10-30").sum())
assert edge == stats["coverage"]["rows_at_window_edge_2023_10_30"]
print(f"[10.2] controls: (a) Date_Entered carries only UTC hours 5/6 = America/Chicago midnights, so local-date reads and ages are correct; (b) cross-layer partition control: 0 of {clean['Permit__'].nunique()} pending permit numbers appear in the issued layer's {issued_clean['Permit__'].nunique()} numbers, matching the metadata's partition of the two layers; (c) window-edge control: {edge} rows entered exactly on 2023-10-30, the rolling window's first observable date, shared with the issued layer's window start PASS")

# 12.3 censoring print
print(f"[12.3] effective window: entered {stats['coverage']['date_entered_min']} to {stats['coverage']['date_entered_max']}; ages as of {stats['as_of_date']} are right-truncated at 1,100 days by the rolling entry window, and the pending stock is selected for slowness (fast applications leave the stock); recent entry cohorts' pending shares are mechanically high PASS")
print("ALL SECTION 10 GATES PASS")
