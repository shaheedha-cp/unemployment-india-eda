# Unemployment in India — Exploratory Data Analysis

**A state-wise analysis of unemployment trends during the Covid-19 pandemic (2020–2021)**

---

## Project overview

This project analyses the **Unemployment in India** dataset from Kaggle to understand how the Covid-19 lockdown impacted employment across Indian states, with a focus on Kerala's performance relative to the national average.

**5 business questions answered:**

| #   | Question                                                         | Answer                                               |
| --- | ---------------------------------------------------------------- | ---------------------------------------------------- |
| 1   | Which states had the highest unemployment spike during lockdown? | See heatmap & bar charts                             |
| 2   | How did Kerala compare to the national average?                  | Kerala: 10.12% vs national 11.79% — below average    |
| 3   | Did urban or rural areas recover faster?                         | Rural areas had lower peaks and faster stabilisation |
| 4   | Which month saw peak unemployment across India?                  | April–May 2020 (national lockdown)                   |
| 5   | Which states were most resilient?                                | See recovery chart — months to return to baseline    |

---

## Dataset

- **Source:** [Unemployment in India — Kaggle](https://www.kaggle.com/datasets/gokulrajkmv/unemployment-in-india)
- **Rows:** ~768 records
- **Columns:** State, Date, Area (Urban/Rural), Unemployment Rate (%), Labour Participation Rate (%), Estimated Employed
- **Period:** January 2020 – November 2020
- **Granularity:** State × Month × Area type

---

## Key findings

- The national unemployment rate **peaked in April–May 2020**, spiking from a pre-Covid baseline of ~7–8% to over 23% nationally during the lockdown
- **Kerala maintained a below-national-average unemployment rate** (10.12% vs 11.79%) throughout the study period, ranking 16th out of 28 states
- **Urban unemployment** was consistently higher and more volatile than rural unemployment — urban formal-sector jobs were disproportionately affected by lockdown restrictions
- The **heatmap** reveals the lockdown shock was universal across states, but recovery speed varied significantly
- **Labour participation rate and unemployment rate** show a notable correlation — states with higher workforce participation tended to show different unemployment dynamics

---

## Charts produced

| Chart                          | Description                                          |
| ------------------------------ | ---------------------------------------------------- |
| `step3_distribution.png`       | Distribution + boxplot of unemployment rate          |
| `step3_urban_rural.png`        | Urban vs Rural unemployment comparison               |
| `step3_state_avg.png`          | Average unemployment by state (Kerala highlighted)   |
| `step4_national_trend.png`     | National unemployment trend with lockdown annotation |
| `step4_india_vs_kerala.png`    | India vs Kerala trend overlay                        |
| `step4_heatmap.png`            | All states × all months heatmap                      |
| `step4_recovery.png`           | Months to recover to pre-Covid baseline              |
| `step5_correlation_matrix.png` | Correlation between numeric variables                |
| `step5_scatter.png`            | Labour participation vs unemployment scatter         |
| `step5_top_bottom.png`         | Top 10 / Bottom 10 states by peak unemployment       |

---

## Tools & libraries

```
Python 3.x
pandas      — data loading, cleaning, aggregation
numpy       — numeric operations
matplotlib  — charting
seaborn     — statistical visualizations
```

---

## How to run

1. Clone this repo or open the Kaggle notebook directly
2. Add the dataset: [Unemployment in India](https://www.kaggle.com/datasets/gokulrajkmv/unemployment-in-india)
3. Run cells in order: Step 1 → Step 2 → Step 3 → Step 4 → Step 5

**Kaggle notebook:** kaggle kernels output shaheedhacp/unemployment-rate-in-india-v-s-kerala -p /path/to/dest

---

## Project structure

```
unemployment-india-eda/
│
├── eda_step1_step2.py     # Setup, loading, cleaning
├── eda_step3.py           # Univariate analysis
├── eda_step4.py           # Time-series analysis
├── eda_step5.py           # Correlation & final summary
├── README.md              # This file
└── charts/                # All exported PNG charts
```

---

## Author

**Shaheedha**
Data Analyst | Bangalore, India
[LinkedIn](#) · [Kaggle](#)

---

_Dataset source: Kaggle — gokulrajkmv/unemployment-in-india_
