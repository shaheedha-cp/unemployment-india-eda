# ============================================================
# UNEMPLOYMENT IN INDIA — EDA PROJECT
# Kaggle Dataset: https://www.kaggle.com/datasets/gokulrajkmv/unemployment-in-india
# Author: Shaheedha
# ============================================================


# ────────────────────────────────────────────────────────────
# CELL 1 — Import libraries
# ────────────────────────────────────────────────────────────

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Plot style — clean, professional
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams.update({
    "figure.dpi":        120,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "font.family":       "sans-serif",
})

print("✅ Libraries imported successfully.")
print(f"   pandas  : {pd.__version__}")
print(f"   numpy   : {np.__version__}")
print(f"   seaborn : {sns.__version__}")


# ────────────────────────────────────────────────────────────
# CELL 2 — Load the dataset
# ────────────────────────────────────────────────────────────

# On Kaggle the file is at: /kaggle/input/unemployment-in-india/Unemployment in India.csv
# If running locally, adjust the path below.

FILE_PATH = "/kaggle/input/unemployment-in-india/Unemployment in India.csv"

df_raw = pd.read_csv(FILE_PATH)

print(f"✅ Dataset loaded.")
print(f"   Shape  : {df_raw.shape[0]} rows × {df_raw.shape[1]} columns\n")
print("── First 5 rows ──────────────────────────────────────")
df_raw.head()


# ────────────────────────────────────────────────────────────
# CELL 3 — Inspect column names and types
# ────────────────────────────────────────────────────────────

print("── Column info ───────────────────────────────────────")
df_raw.info()

print("\n── Raw column names ──────────────────────────────────")
for i, col in enumerate(df_raw.columns):
    print(f"  [{i}] '{col}'")


# ────────────────────────────────────────────────────────────
# CELL 4 — Basic statistics
# ────────────────────────────────────────────────────────────

print("── Descriptive statistics ────────────────────────────")
df_raw.describe(include="all").round(2)


# ────────────────────────────────────────────────────────────
# CELL 5 — Check for missing values
# ────────────────────────────────────────────────────────────

print("── Missing value counts ──────────────────────────────")
missing = df_raw.isnull().sum()
missing_pct = (missing / len(df_raw) * 100).round(2)

missing_report = pd.DataFrame({
    "Missing count": missing,
    "Missing %":     missing_pct
})
print(missing_report[missing_report["Missing count"] > 0]
      if missing.sum() > 0
      else "  ✅ No missing values found.")


# ════════════════════════════════════════════════════════════
# STEP 2 — DATA CLEANING
# ════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────
# CELL 6 — Rename columns to clean, consistent names
# ────────────────────────────────────────────────────────────

# The raw dataset has leading/trailing spaces in column names — strip them first
df_raw.columns = df_raw.columns.str.strip()

print("── Stripped column names ─────────────────────────────")
print(df_raw.columns.tolist())

# Rename to clean, readable names
RENAME_MAP = {
    "Region":                         "state",
    "Date":                           "date",
    "Frequency":                      "frequency",
    "Estimated Unemployment Rate (%)": "unemployment_rate",
    "Estimated Employed":             "employed",
    "Estimated Labour Participation Rate (%)": "labour_participation_rate",
    "Area":                           "area",
}

df = df_raw.rename(columns=RENAME_MAP)

# Keep only the columns we renamed (drop any extra unnamed columns)
df = df[[col for col in RENAME_MAP.values() if col in df.columns]]

print("\n── Cleaned column names ──────────────────────────────")
print(df.columns.tolist())
print(f"\n   Shape: {df.shape}")


# ────────────────────────────────────────────────────────────
# CELL 7 — Parse date column
# ────────────────────────────────────────────────────────────

# The date column looks like "31-01-2020" — parse it
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

# Check for any dates that failed to parse
bad_dates = df["date"].isnull().sum()
print(f"Dates parsed successfully. Unparseable dates: {bad_dates}")

# Extract useful time columns
df["year"]       = df["date"].dt.year
df["month"]      = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%b %Y")   # e.g. "Apr 2020"
df["month_num"]  = df["date"].dt.to_period("M")       # for sorting

print("\n── Date range ────────────────────────────────────────")
print(f"   From : {df['date'].min().strftime('%d %b %Y')}")
print(f"   To   : {df['date'].max().strftime('%d %b %Y')}")
print(f"   Unique months : {df['date'].dt.to_period('M').nunique()}")


# ────────────────────────────────────────────────────────────
# CELL 8 — Clean numeric columns
# ────────────────────────────────────────────────────────────

NUMERIC_COLS = ["unemployment_rate", "employed", "labour_participation_rate"]

for col in NUMERIC_COLS:
    if df[col].dtype == object:
        df[col] = pd.to_numeric(df[col].str.replace(",", "").str.strip(), errors="coerce")

print("── Numeric column dtypes after cleaning ──────────────")
print(df[NUMERIC_COLS].dtypes)
print("\n── Numeric summary ───────────────────────────────────")
print(df[NUMERIC_COLS].describe().round(2))


# ────────────────────────────────────────────────────────────
# CELL 9 — Standardise categorical columns
# ────────────────────────────────────────────────────────────

# Standardise state names (strip whitespace, title case)
df["state"] = df["state"].str.strip().str.title()

# Standardise area column
df["area"] = df["area"].str.strip().str.title()

print("── Unique states ─────────────────────────────────────")
print(sorted(df["state"].unique()))

print(f"\n── Area categories ───────────────────────────────────")
print(df["area"].value_counts())


# ────────────────────────────────────────────────────────────
# CELL 10 — Handle missing values
# ────────────────────────────────────────────────────────────

print("── Missing values after cleaning ─────────────────────")
missing_after = df.isnull().sum()
print(missing_after[missing_after > 0] if missing_after.sum() > 0
      else "  ✅ No missing values.")

# If any numeric NaNs exist, fill with state-level median
for col in NUMERIC_COLS:
    if df[col].isnull().sum() > 0:
        df[col] = df.groupby("state")[col].transform(
            lambda x: x.fillna(x.median())
        )
        print(f"  Filled {col} NaNs with state-level median.")


# ────────────────────────────────────────────────────────────
# CELL 11 — Add Kerala flag column (useful for highlighting later)
# ────────────────────────────────────────────────────────────

df["is_kerala"] = df["state"].str.contains("Kerala", case=False)

kerala_rows = df["is_kerala"].sum()
print(f"✅ Kerala rows identified: {kerala_rows}")


# ────────────────────────────────────────────────────────────
# CELL 12 — Final cleaned dataset overview
# ────────────────────────────────────────────────────────────

print("════════════════════════════════════════════════════")
print("  CLEANED DATASET SUMMARY")
print("════════════════════════════════════════════════════")
print(f"  Rows            : {df.shape[0]}")
print(f"  Columns         : {df.shape[1]}")
print(f"  States          : {df['state'].nunique()}")
print(f"  Date range      : {df['date'].min().strftime('%b %Y')} → {df['date'].max().strftime('%b %Y')}")
print(f"  Area types      : {df['area'].unique().tolist()}")
print(f"  Avg unemp. rate : {df['unemployment_rate'].mean():.2f}%")
print(f"  Max unemp. rate : {df['unemployment_rate'].max():.2f}%  "
      f"({df.loc[df['unemployment_rate'].idxmax(), 'state']}, "
      f"{df.loc[df['unemployment_rate'].idxmax(), 'month_name']})")
print(f"  Kerala rows     : {kerala_rows}")
print("════════════════════════════════════════════════════")

print("\n── Final column dtypes ───────────────────────────────")
print(df.dtypes)

print("\n── First 5 rows of cleaned data ──────────────────────")
df.head()


# ────────────────────────────────────────────────────────────
# CELL 13 — Quick sanity-check plot (unemployment over time)
# ────────────────────────────────────────────────────────────

# National average per month
national_avg = (
    df.groupby("date")["unemployment_rate"]
    .mean()
    .reset_index()
    .sort_values("date")
)

# Kerala average per month
kerala_avg = (
    df[df["is_kerala"]]
    .groupby("date")["unemployment_rate"]
    .mean()
    .reset_index()
    .sort_values("date")
)

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(national_avg["date"], national_avg["unemployment_rate"],
        color="#1B6CA8", linewidth=2.2, label="India (national avg)")
ax.plot(kerala_avg["date"], kerala_avg["unemployment_rate"],
        color="#E8593C", linewidth=2.2, linestyle="--", label="Kerala")

# Annotate Covid lockdown peak
peak_idx = national_avg["unemployment_rate"].idxmax()
peak_date = national_avg.loc[peak_idx, "date"]
peak_val  = national_avg.loc[peak_idx, "unemployment_rate"]
ax.annotate(
    f"Lockdown peak\n{peak_val:.1f}%",
    xy=(peak_date, peak_val),
    xytext=(pd.Timestamp("2020-06-15"), peak_val - 8),
    arrowprops=dict(arrowstyle="->", color="#444", lw=1.2),
    fontsize=10, color="#444"
)

ax.set_title("Unemployment rate over time — India vs Kerala", fontsize=14, pad=12)
ax.set_xlabel("")
ax.set_ylabel("Unemployment rate (%)")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("sanity_check_plot.png", bbox_inches="tight")
plt.show()

print("\n✅ Step 1 & 2 complete. Data is clean and ready for EDA.")
print("   'df' is your working dataframe for all subsequent steps.")
