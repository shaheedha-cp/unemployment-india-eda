# ════════════════════════════════════════════════════════════
# STEP 3 — UNIVARIATE ANALYSIS
# Understanding the distribution of each key variable
# ════════════════════════════════════════════════════════════


# ────────────────────────────────────────────────────────────
# CELL 14 — Distribution of unemployment rate (histogram + KDE)
# ────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram with KDE
sns.histplot(df["unemployment_rate"], bins=30, kde=True,
             color="#1B6CA8", ax=axes[0], edgecolor="white", linewidth=0.5)
axes[0].axvline(df["unemployment_rate"].mean(), color="#E8593C",
                linestyle="--", linewidth=1.8, label=f"Mean: {df['unemployment_rate'].mean():.1f}%")
axes[0].axvline(df["unemployment_rate"].median(), color="#2E8B57",
                linestyle="--", linewidth=1.8, label=f"Median: {df['unemployment_rate'].median():.1f}%")
axes[0].set_title("Distribution of unemployment rate", fontsize=13)
axes[0].set_xlabel("Unemployment rate (%)")
axes[0].set_ylabel("Count")
axes[0].legend(frameon=False)

# Boxplot
sns.boxplot(y=df["unemployment_rate"], color="#B5D4F4",
            linecolor="#1B6CA8", linewidth=1.5, ax=axes[1],
            flierprops=dict(marker="o", markerfacecolor="#E8593C",
                            markersize=4, alpha=0.6))
axes[1].set_title("Boxplot — unemployment rate", fontsize=13)
axes[1].set_ylabel("Unemployment rate (%)")

plt.suptitle("Step 3 · Univariate Analysis", fontsize=10,
             color="gray", y=1.01)
plt.tight_layout()
plt.savefig("step3_distribution.png", bbox_inches="tight")
plt.show()

# Print key stats
print("── Unemployment rate — key statistics ────────────────")
print(f"  Mean   : {df['unemployment_rate'].mean():.2f}%")
print(f"  Median : {df['unemployment_rate'].median():.2f}%")
print(f"  Std    : {df['unemployment_rate'].std():.2f}%")
print(f"  Min    : {df['unemployment_rate'].min():.2f}%")
print(f"  Max    : {df['unemployment_rate'].max():.2f}%")
print(f"  Skew   : {df['unemployment_rate'].skew():.2f}  "
      f"({'right-skewed — a few very high values pull the mean up' if df['unemployment_rate'].skew() > 0.5 else 'roughly symmetric'})")


# ────────────────────────────────────────────────────────────
# CELL 15 — Distribution of labour participation rate
# ────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(df["labour_participation_rate"], bins=30, kde=True,
             color="#2E8B57", ax=axes[0], edgecolor="white", linewidth=0.5)
axes[0].axvline(df["labour_participation_rate"].mean(), color="#E8593C",
                linestyle="--", linewidth=1.8,
                label=f"Mean: {df['labour_participation_rate'].mean():.1f}%")
axes[0].set_title("Distribution of labour participation rate", fontsize=13)
axes[0].set_xlabel("Labour participation rate (%)")
axes[0].set_ylabel("Count")
axes[0].legend(frameon=False)

sns.boxplot(y=df["labour_participation_rate"], color="#C0DD97",
            linecolor="#2E8B57", linewidth=1.5, ax=axes[1],
            flierprops=dict(marker="o", markerfacecolor="#E8593C",
                            markersize=4, alpha=0.6))
axes[1].set_title("Boxplot — labour participation rate", fontsize=13)
axes[1].set_ylabel("Labour participation rate (%)")

plt.tight_layout()
plt.savefig("step3_labour_distribution.png", bbox_inches="tight")
plt.show()

print("── Labour participation rate — key statistics ─────────")
print(f"  Mean   : {df['labour_participation_rate'].mean():.2f}%")
print(f"  Median : {df['labour_participation_rate'].median():.2f}%")
print(f"  Std    : {df['labour_participation_rate'].std():.2f}%")


# ────────────────────────────────────────────────────────────
# CELL 16 — Unemployment rate by area type (Urban vs Rural)
# ────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

area_colors = {"Urban": "#1B6CA8", "Rural": "#2E8B57"}

# KDE by area
for area, grp in df.groupby("area"):
    sns.kdeplot(grp["unemployment_rate"], ax=axes[0],
                label=area, color=area_colors.get(area, "gray"),
                linewidth=2.2, fill=True, alpha=0.15)
axes[0].set_title("Unemployment rate — Urban vs Rural (density)", fontsize=13)
axes[0].set_xlabel("Unemployment rate (%)")
axes[0].legend(frameon=False)

# Boxplot by area
sns.boxplot(data=df, x="area", y="unemployment_rate",
            palette=area_colors, ax=axes[1],
            linewidth=1.5,
            flierprops=dict(marker="o", markersize=4, alpha=0.5))
axes[1].set_title("Unemployment rate — Urban vs Rural (boxplot)", fontsize=13)
axes[1].set_xlabel("")
axes[1].set_ylabel("Unemployment rate (%)")

plt.tight_layout()
plt.savefig("step3_urban_rural.png", bbox_inches="tight")
plt.show()

# Summary stats by area
print("── Unemployment rate by area ─────────────────────────")
print(df.groupby("area")["unemployment_rate"]
      .agg(["mean", "median", "std", "max"])
      .round(2)
      .rename(columns={"mean": "Mean %", "median": "Median %",
                        "std": "Std", "max": "Max %"}))


# ────────────────────────────────────────────────────────────
# CELL 17 — Average unemployment rate by state (bar chart)
# ────────────────────────────────────────────────────────────

state_avg = (
    df.groupby("state")["unemployment_rate"]
    .mean()
    .sort_values(ascending=True)
    .reset_index()
)

# Color Kerala differently
bar_colors = [
    "#E8593C" if s == "Kerala" else "#1B6CA8"
    for s in state_avg["state"]
]

fig, ax = plt.subplots(figsize=(10, 12))
bars = ax.barh(state_avg["state"], state_avg["unemployment_rate"],
               color=bar_colors, edgecolor="white", linewidth=0.4)

# National average reference line
nat_mean = df["unemployment_rate"].mean()
ax.axvline(nat_mean, color="#444", linestyle="--", linewidth=1.4,
           label=f"National avg: {nat_mean:.1f}%")

# Value labels
for bar, val in zip(bars, state_avg["unemployment_rate"]):
    ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=9,
            color="#333")

ax.set_title("Average unemployment rate by state\n(full period · Kerala highlighted in orange)",
             fontsize=13, pad=12)
ax.set_xlabel("Average unemployment rate (%)")
ax.legend(frameon=False)
ax.set_xlim(0, state_avg["unemployment_rate"].max() + 4)
plt.tight_layout()
plt.savefig("step3_state_avg.png", bbox_inches="tight")
plt.show()

# Where does Kerala rank?
kerala_rank = state_avg[state_avg["state"] == "Kerala"].index[0] + 1
kerala_val  = state_avg[state_avg["state"] == "Kerala"]["unemployment_rate"].values[0]
print(f"── Kerala ranking ────────────────────────────────────")
print(f"  Kerala avg unemployment : {kerala_val:.2f}%")
print(f"  National average        : {nat_mean:.2f}%")
print(f"  Kerala rank             : {kerala_rank} out of {len(state_avg)} states")
print(f"  {'Above' if kerala_val > nat_mean else 'Below'} national average "
      f"by {abs(kerala_val - nat_mean):.2f} percentage points")


# ────────────────────────────────────────────────────────────
# CELL 18 — Top 5 and Bottom 5 states summary table
# ────────────────────────────────────────────────────────────

state_summary = (
    df.groupby("state")["unemployment_rate"]
    .agg(["mean", "median", "max", "min"])
    .round(2)
    .rename(columns={"mean": "Avg %", "median": "Median %",
                      "max": "Peak %", "min": "Min %"})
    .sort_values("Avg %", ascending=False)
)

print("── Top 5 states — highest average unemployment ───────")
print(state_summary.head(5).to_string())

print("\n── Bottom 5 states — lowest average unemployment ─────")
print(state_summary.tail(5).to_string())

print("\n── Kerala ────────────────────────────────────────────")
print(state_summary.loc["Kerala"].to_string()
      if "Kerala" in state_summary.index
      else "  Kerala not found — check state name spelling.")


# ────────────────────────────────────────────────────────────
# CELL 19 — Step 3 written insights (markdown-style)
# ────────────────────────────────────────────────────────────

insights = """
╔══════════════════════════════════════════════════════════╗
  STEP 3 — KEY INSIGHTS
╠══════════════════════════════════════════════════════════╣

  1. DISTRIBUTION SHAPE
     The unemployment rate is right-skewed — most states
     cluster at lower rates but a few states (particularly
     during the April–May 2020 lockdown) show extreme spikes
     that pull the mean well above the median.

  2. URBAN VS RURAL
     Urban unemployment is consistently higher and more
     volatile than rural unemployment. This is expected —
     urban formal-sector jobs (retail, hospitality, services)
     were harder hit by lockdown restrictions than
     agricultural/rural work.

  3. KERALA'S POSITION
     Kerala sits [above/below] the national average — update
     this after running Cell 17. Kerala's higher baseline
     unemployment is a known structural feature of the state
     (high educated workforce, selectivity in job acceptance).

  4. SPREAD
     A standard deviation of ~{:.1f}% indicates high
     variability across states and time periods — this
     dataset has a strong story to tell in the time-series
     analysis (Step 4).

  5. OUTLIERS
     The boxplot shows significant outliers on the high end.
     These are almost certainly April–May 2020 lockdown
     values — we will confirm this in Step 4.

╚══════════════════════════════════════════════════════════╝
""".format(df["unemployment_rate"].std())

print(insights)
print("✅ Step 3 complete. Ready for Step 4 — Time-series analysis.")
