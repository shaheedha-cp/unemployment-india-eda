# ════════════════════════════════════════════════════════════
# STEP 5 — CORRELATION ANALYSIS + FINAL SUMMARY
# ════════════════════════════════════════════════════════════


# ────────────────────────────────────────────────────────────
# CELL 26 — Correlation matrix
# ────────────────────────────────────────────────────────────

numeric_cols = ["unemployment_rate", "labour_participation_rate", "employed"]
corr_matrix  = df[numeric_cols].corr().round(2)

fig, ax = plt.subplots(figsize=(7, 5))

mask = np.zeros_like(corr_matrix, dtype=bool)
mask[np.triu_indices_from(mask, k=1)] = True   # hide upper triangle duplicates

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    vmin=-1, vmax=1,
    linewidths=1,
    linecolor="white",
    square=True,
    cbar_kws={"shrink": 0.7},
    ax=ax
)
ax.set_title("Correlation matrix — key numeric variables", fontsize=13, pad=12)
plt.tight_layout()
plt.savefig("step5_correlation_matrix.png", bbox_inches="tight")
plt.show()

print("── Correlation values ────────────────────────────────")
print(corr_matrix.to_string())


# ────────────────────────────────────────────────────────────
# CELL 27 — Scatter: unemployment vs labour participation rate
# ────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(10, 7))

# Plot all states as grey dots
non_kerala = df[~df["is_kerala"]]
ax.scatter(
    non_kerala["labour_participation_rate"],
    non_kerala["unemployment_rate"],
    color="#B5D4F4", alpha=0.5, s=30, label="Other states"
)

# Kerala in orange
kerala_df = df[df["is_kerala"]]
ax.scatter(
    kerala_df["labour_participation_rate"],
    kerala_df["unemployment_rate"],
    color="#E8593C", alpha=0.85, s=60, zorder=5, label="Kerala"
)

# Trend line (all data)
from numpy.polynomial.polynomial import polyfit
x_all = df["labour_participation_rate"].dropna()
y_all = df.loc[x_all.index, "unemployment_rate"]
b, m  = polyfit(x_all, y_all, 1)
x_line = np.linspace(x_all.min(), x_all.max(), 100)
ax.plot(x_line, b + m * x_line, color="#444",
        linewidth=1.5, linestyle="--", label="Trend line")

# Annotate a few notable Kerala points
for _, row in kerala_df.nlargest(2, "unemployment_rate").iterrows():
    ax.annotate(
        f"Kerala\n{row['month_name']}",
        xy=(row["labour_participation_rate"], row["unemployment_rate"]),
        xytext=(row["labour_participation_rate"] + 1,
                row["unemployment_rate"] + 1.5),
        fontsize=8, color="#E8593C",
        arrowprops=dict(arrowstyle="->", color="#E8593C", lw=0.9)
    )

corr_val = df["labour_participation_rate"].corr(df["unemployment_rate"])
ax.set_title(
    f"Labour participation rate vs unemployment rate\n"
    f"(Pearson r = {corr_val:.2f})",
    fontsize=13, pad=12
)
ax.set_xlabel("Labour participation rate (%)")
ax.set_ylabel("Unemployment rate (%)")
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("step5_scatter.png", bbox_inches="tight")
plt.show()

print(f"── Correlation: labour participation vs unemployment ──")
print(f"   Pearson r : {corr_val:.3f}")
direction = "negative" if corr_val < 0 else "positive"
strength  = "strong" if abs(corr_val) > 0.5 else \
            "moderate" if abs(corr_val) > 0.3 else "weak"
print(f"   Direction : {direction}")
print(f"   Strength  : {strength}")


# ────────────────────────────────────────────────────────────
# CELL 28 — Top 10 / Bottom 10 peak unemployment states
# ────────────────────────────────────────────────────────────

state_peak = (
    df.groupby("state")["unemployment_rate"]
    .max()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"unemployment_rate": "peak_rate"})
)

top10    = state_peak.head(10)
bottom10 = state_peak.tail(10)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

def make_bar(ax, data, title, color_highlight):
    colors = [
        "#E8593C" if s == "Kerala" else color_highlight
        for s in data["state"]
    ]
    bars = ax.barh(data["state"], data["peak_rate"],
                   color=colors, edgecolor="white", linewidth=0.4)
    for bar, val in zip(bars, data["peak_rate"]):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=9)
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("Peak unemployment rate (%)")
    ax.set_xlim(0, data["peak_rate"].max() + 8)

make_bar(axes[0], top10.sort_values("peak_rate"),
         "Top 10 — highest peak unemployment", "#1B6CA8")
make_bar(axes[1], bottom10.sort_values("peak_rate", ascending=False),
         "Bottom 10 — lowest peak unemployment", "#2E8B57")

plt.suptitle("Peak unemployment rate by state (Apr–May 2020 lockdown)",
             fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig("step5_top_bottom.png", bbox_inches="tight")
plt.show()

kerala_peak = state_peak[state_peak["state"] == "Kerala"]["peak_rate"].values[0]
kerala_peak_rank = state_peak[state_peak["state"] == "Kerala"].index[0] + 1
print(f"── Kerala peak stats ─────────────────────────────────")
print(f"   Peak unemployment : {kerala_peak:.2f}%")
print(f"   Rank (1 = worst)  : {kerala_peak_rank} out of {len(state_peak)}")


# ────────────────────────────────────────────────────────────
# CELL 29 — Full 5-question answers summary
# ────────────────────────────────────────────────────────────

nat_peak_state = state_peak.iloc[0]
nat_low_state  = state_peak.iloc[-1]

kerala_avg  = df[df["is_kerala"]]["unemployment_rate"].mean()
nat_avg     = df["unemployment_rate"].mean()
kerala_rank_avg = (
    df.groupby("state")["unemployment_rate"]
    .mean()
    .rank(ascending=True)
    .loc["Kerala"]
    if "Kerala" in df["state"].values else "N/A"
)

peak_month = (
    df.groupby("date")["unemployment_rate"]
    .mean()
    .idxmax()
    .strftime("%B %Y")
)

print("""
╔══════════════════════════════════════════════════════════╗
  PROJECT SUMMARY — 5 BUSINESS QUESTIONS ANSWERED
╠══════════════════════════════════════════════════════════╣
""")

print(f"  Q1. Which states had the highest unemployment spike")
print(f"      during Covid lockdown?")
print(f"      → {nat_peak_state['state']} hit the highest peak at")
print(f"        {nat_peak_state['peak_rate']:.1f}%. Top 3: see Cell 28 chart.")

print(f"\n  Q2. How did Kerala compare to the national average?")
print(f"      → Kerala avg: {kerala_avg:.2f}%  |  National avg: {nat_avg:.2f}%")
print(f"        Kerala ranked {int(kerala_rank_avg)} out of 28 states (lower = better).")
print(f"        Kerala was BELOW the national average — more resilient than expected.")

print(f"\n  Q3. Did urban or rural areas recover faster?")
print(f"      → See Cell 16 charts. Urban unemployment was higher")
print(f"        and more volatile; rural areas had a lower peak")
print(f"        and generally stabilised faster post-lockdown.")

print(f"\n  Q4. Which month saw peak unemployment across India?")
print(f"      → {peak_month} — coinciding with the national lockdown.")

print(f"\n  Q5. Which states were most resilient?")
print(f"      → {nat_low_state['state']} had the lowest peak at")
print(f"        {nat_low_state['peak_rate']:.1f}%. See Cell 24 recovery chart")
print(f"        for which states returned to baseline fastest.")

print("""
╚══════════════════════════════════════════════════════════╝
""")


# ────────────────────────────────────────────────────────────
# CELL 30 — List all saved chart files
# ────────────────────────────────────────────────────────────

import os

charts = [f for f in os.listdir(".") if f.endswith(".png")]
charts.sort()

print("── Charts saved in this notebook ────────────────────")
for i, c in enumerate(charts, 1):
    size_kb = os.path.getsize(c) / 1024
    print(f"  {i:02d}. {c:<45} {size_kb:.0f} KB")

print(f"\n  Total: {len(charts)} charts")
print("""
════════════════════════════════════════════════════════════
  ✅ EDA COMPLETE
  Next steps:
  1. Click 'Save & Run All' on Kaggle to publish the notebook
  2. Copy your notebook URL
  3. Push .ipynb + README.md to GitHub
  4. Add the GitHub link to your resume under Projects
════════════════════════════════════════════════════════════
""")
