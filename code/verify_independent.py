#!/usr/bin/env python3
"""Independent verifier (Section 11 method diversity).
Two implementations sharing no code with the builder:
 (1) server-side ArcGIS queries against the live service;
 (2) a pyarrow recount of the raw snapshot (no pandas), with ages
     computed by raw epoch arithmetic against a fixed as-of instant.
Compares both against stats.json. Prints PASS/FAIL per check.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
import pyarrow.parquet as pq
import requests

HERE = Path(__file__).resolve()
PKG = HERE.parents[1]
STACK = HERE.parents[2] / "stack" / "nashville"
BASE = "https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Building_Permit_Applications_Feature_Layer_view/FeatureServer/0"
stats = json.loads((PKG / "stats.json").read_text())
checks = []

def check(name, ok, detail=""):
    checks.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")

def q(params):
    params = dict(params)
    if "outStatistics" in params:
        params["outStatistics"] = json.dumps(params["outStatistics"])
    r = requests.get(BASE + "/query", params=params, timeout=120)
    r.raise_for_status()
    d = r.json()
    if "error" in d:
        raise RuntimeError(d["error"])
    return d

# --- (1) server-side ---
live = q({"where": "1=1", "returnCountOnly": "true", "f": "json"})["count"]
check("server count (live service rolls daily; drift-tolerant)",
      abs(live - stats["rows"]) <= 200, f"live now {live} vs snapshot {stats['rows']}")

ni = q({"where": "Date_Issued IS NOT NULL", "returnCountOnly": "true", "f": "json"})["count"]
check("server count of rows with a Date_Issued (definition control)",
      ni == 0, f"{ni} rows carry an issue date in the live not-yet-issued layer")

d = q({"where": "1=1", "groupByFieldsForStatistics": "Permit_Type_Description",
       "outStatistics": [{"statisticType": "count", "onStatisticField": "ObjectId", "outStatisticFieldName": "n"}],
       "orderByFields": "n DESC", "f": "json"})
server_types = {f["attributes"]["Permit_Type_Description"]: f["attributes"]["n"] for f in d["features"]}
same = {k: v for k, v in server_types.items() if stats["type_counts_all_rows"].get(k) == v}
check("server groupBy type counts reproduce snapshot counts for unchanged types",
      len(same) >= 25, f"{len(same)}/{len(server_types)} types match the snapshot exactly (rolling window shifts the rest)")

d = q({"where": "Const_Cost > 0", "outStatistics": [
    {"statisticType": "sum", "onStatisticField": "Const_Cost", "outStatisticFieldName": "tot"},
    {"statisticType": "max", "onStatisticField": "Const_Cost", "outStatisticFieldName": "mx"},
    {"statisticType": "count", "onStatisticField": "ObjectId", "outStatisticFieldName": "n"}], "f": "json"})
a = d["features"][0]["attributes"]
check("server positive-cost rows, total and max (window rolls; snapshot values must be reachable)",
      a["n"] >= stats["cost"]["rows_with_stated_value"] - 200 and float(a["mx"]) >= stats["cost"]["max_stated"],
      f"server now n={a['n']}, total {a['tot']:,.0f}, max {a['mx']:,.0f} vs snapshot n={stats['cost']['rows_with_stated_value']}, total {stats['cost']['total_stated']:,.0f}, max {stats['cost']['max_stated']:,.0f}")

# --- (2) pyarrow recount of the raw snapshot ---
t = pq.read_table(STACK / "snapshots" / "2026-11-03" / "building_permit_applications_raw.parquet")
check("pyarrow row count", t.num_rows == stats["rows"], f"{t.num_rows}")
di = t.column("Date_Issued").to_pylist()
check("pyarrow Date_Issued all null", all(v is None for v in di), f"{sum(v is not None for v in di)} non-null")
ASOF_MS = int(datetime(2026, 11, 3, 6, 0, tzinfo=timezone.utc).timestamp() * 1000)  # 2026-11-03 00:00 America/Chicago (CST)
ent = t.column("Date_Entered").to_pylist()
ages = sorted((ASOF_MS - e) // 86400000 for e in ent)
import statistics as st
check("pyarrow median pending age (raw epoch-day arithmetic)",
      st.median(ages) == stats["age_all"]["median_days"], f"median {st.median(ages)} days")
over365 = sum(1 for a in ages if a > 365)
check("pyarrow over-365 count", over365 == stats["age_all"]["over_365_count"], f"{over365}")
check("pyarrow max age / window edge", ages[-1] == stats["age_all"]["max_days"], f"max {ages[-1]} days")
cost = t.column("Const_Cost").to_pylist()
pos = [c for c in cost if c is not None and c > 0]
check("pyarrow stated-cost total on positive rows",
      sum(pos) == int(stats["cost"]["total_stated"]), f"sum {sum(pos):,} (stats {int(stats['cost']['total_stated']):,})")
check("pyarrow stated-cost median on positive rows",
      st.median(pos) == stats["cost"]["median_stated"], f"{st.median(pos):,.0f}")
check("pyarrow not-stated rows (zero + null)",
      sum(1 for c in cost if c is None or c == 0) == stats["cost"]["not_stated_rows"],
      f"{sum(1 for c in cost if c is None or c == 0)}")
dist = t.column("Council_Dist").to_pylist()
check("pyarrow district unknowns (nulls; no zero sentinel)",
      sum(1 for v in dist if v is None) == stats["geography"]["council_district"]["unknown_rows"]
      and sum(1 for v in dist if v == 0) == 0,
      f"nulls {sum(1 for v in dist if v is None)}, zeros {sum(1 for v in dist if v == 0)}")
obj = t.column("ObjectId").to_pylist()
check("pyarrow ObjectId unique", len(set(obj)) == len(obj), f"{len(set(obj))} unique")

fails = [c for c in checks if not c[1]]
print(f"\n{len(checks) - len(fails)}/{len(checks)} checks pass")
out = {"checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
       "passed": len(checks) - len(fails), "total": len(checks)}
(HERE.parents[1] / "data" / "verify_independent_output.json").write_text(json.dumps(out, indent=2))
if fails:
    raise SystemExit(1)
