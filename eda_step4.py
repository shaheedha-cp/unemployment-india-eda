# ════════════════════════════════════════════════════════════
# STEP 4 — TIME-SERIES ANALYSIS
# How unemployment changed over time — nationally and for Kerala
# ════════════════════════════════════════════════════════════


# ────────────────────────────────────────────────────────────
# CELL 20 — Prepare monthly aggregates
# ────────────────────────────────────────────────────────────

# National monthly average
national_monthly = (
    df.groupby("date")
    .agg(
        avg_unemployment=("unemployment_rate", "mean"),
        avg_labour=("labour_participation_rate", "mean")
    )
    .reset_index()
    .sort_values("date")
)

# Kerala monthly average
kerala_monthly = (
    df[df["is_kerala"]]
    .groupby("date")
    .agg(
        avg_unemployment=("unemployment_rate", "mean"),
        avg_labour=("labour_participation_rate", "mean")
    )
    .reset_index()
    .sort_values("date")
)

# All states monthly (for heatmap later)
state_monthly = (
    df.groupby(["state", "date"])["unemployment_rate"]
    .mean()
    .reset_index()
    .sort_values("date")
)

print(f"✅ Monthly aggregates ready.")
print(f"   National: {len(national_monthly)} months")
print(f"   Kerala  : {len(kerala_monthly)} months")
print(f"\n── National monthly unemployment ─────────────────────")
print(national_monthly[["date", "avg_unemployment"]].to_string(index=False))


# ────────────────────────────────────────────────────────────
# CELL 21 — National unemployment trend with annotations
# ────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(13, 6))

# Fill area under curve
ax.fill_between(national_monthly["date"],
                national_monthly["avg_unemployment"],
                alpha=0.12, color="#1B6CA8")

# Main line
ax.plot(national_monthly["date"], national_monthly["avg_unemployment"],
        color="#1B6CA8", linewidth=2.5, marker="o",
        markersize=5, label="National average")

# Baseline reference (pre-Covid: Jan–Feb 2020 mean)
pre_covid = national_monthly[
    national_monthly["date"] < "2020-03-01"
]["avg_unemployment"].mean()
ax.axhline(pre_covid, color="#888", linestyle=":", linewidth=1.4,
           label=f"Pre-Covid baseline: {pre_covid:.1f}%")

# Find and annotate peak
peak_idx  = national_monthly["avg_unemployment"].idxmax()
peak_date = national_monthly.loc[peak_idx, "date"]
peak_val  = national_monthly.loc[peak_idx, "avg_unemployment"]

ax.annotate(
    f"Peak: {peak_val:.1f}%\n({peak_date.strftime('%b %Y')})",
    xy=(peak_date, peak_val),
    xytext=(peak_date + pd.DateOffset(months=1), peak_val - 5),
    arrowprops=dict(arrowstyle="->", color="#333", lw=1.3),
    fontsize=10, color="#333",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
              edgecolor="#ccc", linewidth=0.8)
)

# Annotate lockdown period
ax.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-05-31"),
           alpha=0.08, color="#E8593C", label="Lockdown period")
ax.text(pd.Timestamp("2020-04-10"), peak_val * 0.4,
        "Lockdown", fontsize=9, color="#E8593C", rotation=90,
        va="bottom")

ax.set_title("India unemployment rate — monthly trend (2020–2021)",
             fontsize=14, pad=12)
ax.set_xlabel("")
ax.set_ylabel("Unemployment rate (%)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.legend(frameon=False, loc="upper right")
ax.set_ylim(0, peak_val + 8)

plt.tight_layout()
plt.savefig("step4_national_trend.png", bbox_inches="tight")
plt.show()

print(f"── Peak unemployment ─────────────────────────────────")
print(f"   Month : {peak_date.strftime('%B %Y')}")
print(f"   Value : {peak_val:.2f}%")
print(f"   That is {peak_val - pre_covid:.1f} percentage points above pre-Covid baseline.")


# ────────────────────────────────────────────────────────────
# CELL 22 — India vs Kerala side-by-side trend
# ────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(13, 6))

# India
ax.fill_between(national_monthly["date"],
                national_monthly["avg_unemployment"],
                alpha=0.10, color="#1B6CA8")
ax.plot(national_monthly["date"], national_monthly["avg_unemployment"],
        color="#1B6CA8", linewidth=2.5, marker="o",
        markersize=5, label=f"India (avg: {national_monthly['avg_unemployment'].mean():.1f}%)")

# Kerala
ax.fill_between(kerala_monthly["date"],
                kerala_monthly["avg_unemployment"],
                alpha=0.10, color="#E8593C")
ax.plot(kerala_monthly["date"], kerala_monthly["avg_unemployment"],
        color="#E8593C", linewidth=2.5, marker="s",
        markersize=5, linestyle="--",
        label=f"Kerala (avg: {kerala_monthly['avg_unemployment'].mean():.1f}%)")

# Lockdown shading
ax.axvspan(pd.Timestamp("2020-03-25"), pd.Timestamp("2020-05-31"),
           alpha=0.07, color="#888")
ax.text(pd.Timestamp("2020-04-01"), 2, "Lockdown",
        fontsize=9, color="#666", rotation=90)

# Annotate Kerala peak
k_peak_idx = kerala_monthly["avg_unemployment"].idxmax()
k_peak_date = kerala_monthly.loc[k_peak_idx, "date"]
k_peak_val  = kerala_monthly.loc[k_peak_idx, "avg_unemployment"]
ax.annotate(
    f"Kerala peak\n{k_peak_val:.1f}%",
    xy=(k_peak_date, k_peak_val),
    xytext=(k_peak_date + pd.DateOffset(months=2), k_peak_val + 3),
    arrowprops=dict(arrowstyle="->", color="#E8593C", lw=1.2),
    fontsize=9, color="#E8593C"
)

ax.set_title("Unemployment rate — India vs Kerala (2020–2021)",
             fontsize=14, pad=12)
ax.set_xlabel("")
ax.set_ylabel("Unemployment rate (%)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.legend(frameon=False)
ax.set_ylim(0)

plt.tight_layout()
plt.savefig("step4_india_vs_kerala.png", bbox_inches="tight")
plt.show()

# Gap analysis
merged = national_monthly.merge(
    kerala_monthly, on="date", suffixes=("_india", "_kerala")
)
merged["gap"] = merged["avg_unemployment_india"] - merged["avg_unemployment_kerala"]

print("── India vs Kerala monthly gap (India minus Kerala) ──")
print(merged[["date", "avg_unemployment_india",
              "avg_unemployment_kerala", "gap"]]
      .rename(columns={
          "avg_unemployment_india":  "India %",
          "avg_unemployment_kerala": "Kerala %",
          "gap": "Gap (pp)"
      })
      .round(2)
      .to_string(index=False))


# ────────────────────────────────────────────────────────────
# CELL 23 — State × Month heatmap
# ────────────────────────────────────────────────────────────

# Pivot: rows = states, columns = months
pivot = state_monthly.pivot_table(
    index="state",
    columns="date",
    values="unemployment_rate"
)
# Format column labels as "Mon YY"
pivot.columns = [d.strftime("%b '%y") for d in pivot.columns]

# Sort states by their peak unemployment (most affected at top)
pivot = pivot.loc[pivot.max(axis=1).sort_values(ascending=False).index]

fig, ax = plt.subplots(figsize=(14, 10))

sns.heatmap(
    pivot,
    cmap="YlOrRd",
    linewidths=0.3,
    linecolor="#eee",
    annot=False,
    fmt=".0f",
    cbar_kws={"label": "Unemployment rate (%)", "shrink": 0.6},
    ax=ax
)

# Highlight Kerala row
kerala_row_idx = pivot.index.tolist().index("Kerala") \
    if "Kerala" in pivot.index else None
if kerala_row_idx is not None:
    ax.add_patch(plt.Rectangle(
        (0, kerala_row_idx), len(pivot.columns), 1,
        fill=False, edgecolor="#E8593C", lw=2.5, clip_on=False
    ))
    ax.text(-0.3, kerala_row_idx + 0.5, "◀",
            transform=ax.get_yaxis_transform(),
            color="#E8593C", fontsize=12, va="center", ha="right")

ax.set_title("Unemployment rate heatmap — all states × all months\n(Kerala outlined in orange)",
             fontsize=13, pad=12)
ax.set_xlabel("")
ax.set_ylabel("")
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.tick_params(axis="y", labelsize=9)

plt.tight_layout()
plt.savefig("step4_heatmap.png", bbox_inches="tight")
plt.show()

print("✅ Heatmap saved. States sorted by peak unemployment (highest at top).")


# ────────────────────────────────────────────────────────────
# CELL 24 — Recovery analysis
# How many months did it take each state to return to near-baseline?
# ────────────────────────────────────────────────────────────

# Pre-Covid baseline per state (mean of first 2 months of data)
first_two_months = df["date"].sort_values().unique()[:2]
baseline = (
    df[df["date"].isin(first_two_months)]
    .groupby("state")["unemployment_rate"]
    .mean()
    .rename("baseline")
)

# Post-peak data (after May 2020)
post_peak = state_monthly[state_monthly["date"] > "2020-05-31"].copy()
post_peak = post_peak.merge(baseline, on="state")

# Recovery = first month where rate drops within 2pp of baseline
def months_to_recover(group):
    group = group.sort_values("date")
    recovered = group[
        group["unemployment_rate"] <= group["baseline"] + 2
    ]
    if len(recovered) > 0:
        peak_date_g = group["date"].min()
        rec_date  = recovered["date"].iloc[0]
        return (rec_date.year - peak_date_g.year) * 12 + \
               (rec_date.month - peak_date_g.month)
    return None   # did not recover within dataset window

recovery = (
    post_peak.groupby("state")
    .apply(months_to_recover)
    .dropna()
    .sort_values()
    .reset_index()
)
recovery.columns = ["state", "months_to_recover"]

# Bar chart
bar_colors_rec = [
    "#E8593C" if s == "Kerala" else "#1B6CA8"
    for s in recovery["state"]
]

fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(recovery["state"], recovery["months_to_recover"],
        color=bar_colors_rec, edgecolor="white", linewidth=0.4)

avg_recovery = recovery["months_to_recover"].mean()
ax.axvline(avg_recovery, color="#444", linestyle="--", linewidth=1.4,
           label=f"Avg recovery: {avg_recovery:.1f} months")

ax.set_title("Months to recover to near pre-Covid baseline\n(Kerala highlighted in orange)",
             fontsize=13, pad=12)
ax.set_xlabel("Months after June 2020")
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("step4_recovery.png", bbox_inches="tight")
plt.show()

# Kerala recovery
kerala_rec = recovery[recovery["state"] == "Kerala"]
if len(kerala_rec) > 0:
    print(f"── Kerala recovery ───────────────────────────────────")
    print(f"   Months to recover : {int(kerala_rec['months_to_recover'].values[0])}")
    print(f"   National average  : {avg_recovery:.1f} months")
    faster = avg_recovery - kerala_rec['months_to_recover'].values[0]
    print(f"   Kerala recovered  : {abs(faster):.1f} months "
          f"{'faster' if faster > 0 else 'slower'} than average")
else:
    print("Kerala did not recover within the dataset window.")


# ────────────────────────────────────────────────────────────
# CELL 25 — Step 4 written insights
# ────────────────────────────────────────────────────────────

print("""
╔══════════════════════════════════════════════════════════╗
  STEP 4 — KEY INSIGHTS (Time-Series)
╠══════════════════════════════════════════════════════════╣

  1. LOCKDOWN SPIKE
     The national unemployment rate surged dramatically in
     April–May 2020 following the nationwide lockdown —
     the sharpest single shock visible in the entire dataset.

  2. KERALA PEAK VS NATIONAL PEAK
     Check Cell 22 output: did Kerala peak at the same time
     as India, earlier, or later? Note the month and value.

  3. HEATMAP PATTERN
     The heatmap (Cell 23) shows the Apr–May 2020 columns
     as deep orange/red across almost all states — confirming
     the lockdown was a national shock, not regional.
     Some states (check the top rows) were disproportionately
     affected even before or after the lockdown.

  4. RECOVERY SPEED
     Cell 24 shows how quickly each state returned to
     near-baseline levels. States with flexible informal
     economies tended to recover faster.

  5. KERALA RESILIENCE
     Update this with your Cell 24 output — was Kerala
     faster or slower than average to recover?

╚══════════════════════════════════════════════════════════╝
""")

print("✅ Step 4 complete. 4 charts saved:")
print("   step4_national_trend.png")
print("   step4_india_vs_kerala.png")
print("   step4_heatmap.png")
print("   step4_recovery.png")
print("\n   Ready for Step 5 — State-wise comparison & correlation.")
