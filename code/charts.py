"""Data-drawn charts for the Nashville building permit applications
brief (2026-11-04). Brand palette: dark charcoal, amber, teal. Every
chart prints its population, measure, and scope labels on the graphic
itself (framing standard): all ages are the ages of applications still
recorded as not issued on the pull date (a stock, not completed
waits); all cost figures are applicant-stated value where recorded.

Layout: titles and footnotes are figure-level text with fixed axes
margins (no tight_layout), so no footnote can clip or overlap an axis.
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
stats = json.loads((ROOT / "stats.json").read_text())
CH = ROOT / "charts"
CH.mkdir(exist_ok=True)
CHARCOAL = "#23272b"; AMBER = "#f5a800"; TEAL = "#2a9d8f"; GREY = "#8a8f98"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": CHARCOAL,
                     "axes.edgecolor": CHARCOAL, "axes.labelcolor": CHARCOAL,
                     "xtick.color": CHARCOAL, "ytick.color": CHARCOAL})
SNAP = stats["snapshot_date"]
ROWS = stats["rows"]
FOOT = (f"Source: Nashville Building Permit Applications layer (Building_Permit_Applications_Feature_Layer_view), pulled {SNAP}; {ROWS:,} applications recorded as not issued.\n"
        "Ages are days from application entry to the pull date, for the pending stock only; applications already issued are in the companion issued layer, not here.")


def frame(fig, title, foot, top=0.80, bottom=0.17, left=0.09, right=0.985):
    fig.text(0.012, 0.975, title, fontsize=10.5, va="top", ha="left")
    fig.text(0.012, 0.012, foot, fontsize=7.5, color=GREY, va="bottom", ha="left")
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right)


def save(fig, name):
    fig.savefig(CH / name, dpi=200, facecolor="white")
    plt.close(fig)
    print(name)


def short(name):
    return name.replace("Building ", "")


# (a) Age distribution of the pending stock
ad = stats["age_distribution"]
fig, ax = plt.subplots(figsize=(9.5, 5.2))
vals = [b["share_of_pending"] * 100 for b in ad]
ax.bar([b["bucket"] for b in ad], vals,
       color=[TEAL, TEAL, TEAL, CHARCOAL, CHARCOAL, AMBER])
for b_, r in zip(ax.patches, ad):
    ax.text(b_.get_x() + b_.get_width() / 2, b_.get_height() + 0.8,
            f"{r['share_of_pending']*100:.1f}%\n{r['permits']:,} applications",
            ha="center", fontsize=8.5)
ax.set_ylim(0, max(vals) * 1.35)
ax.set_ylabel("Share of pending applications (%)")
ax.spines[["top", "right"]].set_visible(False)
frame(fig,
      "Age distribution of Nashville's pending building permit applications\n"
      f"Population: {ROWS:,} applications recorded as not issued on {SNAP}; median age {stats['age_all']['median_days']:.0f} days, mean {stats['age_all']['mean_days']:.0f} days\n"
      "Ages are truncated at 1,100 days by the layer's rolling three-year entry window; nothing entered before 2023-10-30 is observable",
      FOOT, top=0.80, bottom=0.15, left=0.065, right=0.99)
save(fig, "chart_age_distribution.png")

# (b) Median pending age by permit type (types with at least 80 pending)
by_type = stats["age_by_type"]
rows_b = [(k, v) for k, v in by_type.items() if v["n_permits"] >= 80]
rows_b.sort(key=lambda kv: kv[1]["median_days"])
fig, ax = plt.subplots(figsize=(9.5, 5.8))
ax.barh([short(k) for k, _ in rows_b], [v["median_days"] for _, v in rows_b],
        color=[AMBER if k == "Building Residential - Rehab" else TEAL for k, _ in rows_b])
for i, (k, v) in enumerate(rows_b):
    ax.text(v["median_days"] + 12, i, f"{v['median_days']:.0f} days (n = {v['n_permits']:,})",
            va="center", fontsize=8.5)
ax.set_xlim(0, max(v["median_days"] for _, v in rows_b) * 1.45)
ax.set_xlabel("Median age in days (entry to pull date), pending applications only")
ax.spines[["top", "right"]].set_visible(False)
frame(fig,
      "Median age of pending applications by permit type\n"
      f"Population: pending applications on {SNAP} in types with 80 or more pending; overall median age {stats['age_all']['median_days']:.0f} days\n"
      "Stock ages, not completed waits: a class's pending-stock age and its completed wait rank differently",
      FOOT, top=0.80, bottom=0.14, left=0.30, right=0.99)
save(fig, "chart_age_by_type.png")

# (c) Pending share of observed applications by entry quarter (fusion)
cq = [r for r in stats["cohort_resolution"]["by_entry_quarter"] if r["period"] >= "2023Q4"]
fig, ax = plt.subplots(figsize=(9.5, 5.2))
shares = [r["pending_share"] * 100 for r in cq]
colors = [TEAL if r["period"] < "2026Q1" else AMBER for r in cq]
ax.bar([r["period"].replace("Q", " Q") for r in cq], shares, color=colors)
for b_, r in zip(ax.patches, cq):
    ax.text(b_.get_x() + b_.get_width() / 2, b_.get_height() + 1.6,
            f"{r['pending_share']*100:.1f}%\n({r['observed_total']:,})",
            ha="center", fontsize=7.8)
ax.set_ylim(0, max(shares) * 1.30)
ax.set_ylabel("Still unissued on 2026-11-03 (% of observed applications)")
ax.spines[["top", "right"]].set_visible(False)
frame(fig,
      "Share of each entry quarter's applications still unissued on November 3, 2026\n"
      "Population: applications observable in either layer on the pull date (same-day pulls of both layers)\n"
      "Recent quarters (amber) are mechanically high: their applications have had months, not years, to issue\n"
      "Labels give the share and the observed count; the eight full quarters of 2024 Q1 to 2025 Q4 range from 9.4% to 15.7%",
      FOOT, top=0.76, bottom=0.15, left=0.065, right=0.99)
save(fig, "chart_cohort_pending_share.png")

# (d) Pending applications by council district, top 10 by count
dist = stats["geography"]["council_district"]["by_district_sorted_by_pending_count"][:10]
dist = list(reversed(dist))
fig, ax = plt.subplots(figsize=(9.5, 5.4))
ax.barh([f"District {r['district']}" for r in dist], [r["permits"] for r in dist],
        color=[AMBER if r["district"] == 2 else TEAL for r in dist])
for i, r in enumerate(dist):
    ax.text(r["permits"] + 10, i,
            f"{r['permits']:,} pending - median age {r['median_age_days']:.0f} days",
            va="center", fontsize=8.5)
ax.set_xlim(0, max(r["permits"] for r in dist) * 1.55)
ax.set_xlabel("Pending applications on the pull date")
ax.spines[["top", "right"]].set_visible(False)
frame(fig,
      "Pending applications by council district: top 10 by count, with median age\n"
      f"Population: pending applications on {SNAP} with a known council district ({stats['geography']['council_district']['known_rows']:,} of {ROWS:,})\n"
      "District medians are unadjusted: districts differ in permit mix, and class ages differ (chart b)",
      FOOT, top=0.80, bottom=0.15, left=0.105, right=0.99)
save(fig, "chart_district_pending.png")
print("charts done")
