# Case Study: Colorado CDPHE Outbreak-Alert Comparison

> [!TIP]
> **Run everything at once** from the repo root:
> ```bash
> ./run_all.sh
> ```
> All four case-study notebooks are included. No cluster access or additional data required.

## Overview

This folder contains the code and data for the case study reported in the paper. The goal is to compare TLGRF-derived outbreak alerts against Colorado Department of Public Health and Environment (CDPHE) county-level outbreak investigations, asking whether a simple TLGRF threshold rule can identify counties that later required formal capacity investigations by public health officials.

---

## Directory Layout

```
case_study/
├── README.md          # This file
├── data/              # Input Parquet files (see below)
└── src/               # Analysis notebooks (STEP1–STEP4)
```

---

## Data Files (`data/`)

The `data/` folder contains pre-computed Parquet files from the TLGRF backtest.

**Top-level files:**

| File | Contents |
|---|---|
| `cdphe_tlgrf_historical_filtered.parquet` | TLGRF predictions joined with CDPHE investigation records (filtered to counties with complete data) |
| `cdphe_tlgrf_historical_unfiltered.parquet` | Same join, unfiltered — includes all counties regardless of data completeness |
| `changepoint_matrix.parquet` | County x time matrix of TLGRF-detected changepoints / growth-rate inflection dates |
| `colorado_outbreak_matrix.parquet` | County x time binary outbreak indicator matrix (used in Figure 3) |
| `colorado_outbreaks_2023-04-26.parquet` | Snapshot of CDPHE outbreak investigation records as of 2023-04-26 |

**`data/Colorado_Data/`:**

| File | Contents |
|---|---|
| `Colorado_Outbreak_Data_2023-04-26.parquet` | Full CDPHE outbreak investigation dataset (Colorado counties) |
| `county_fips_master.parquet` | County FIPS code reference table with population and region fields |

**`data/matching/`:**

| File | Contents |
|---|---|
| `ReplicationData_CrossSection.parquet` | Cross-sectional replication dataset for alert-investigation matching |
| `ReplicationData_TimeSeries_CO.parquet` | Time-series replication dataset for Colorado counties |
| `facilities.parquet` | Facility-level metadata used in outbreak investigation matching |

> All notebooks run from the pre-computed Parquet files in this folder. No additional raw data is required.

---

## Notebooks (`src/`)

All notebooks run from the pre-computed Parquet files in `data/`. Run them in order:

### STEP1 — Investigation overlap analysis
**Notebook:** `STEP1_check_investigation_overlap.ipynb`
**Produces:** Exploratory summary of CDPHE investigation timing and county overlap.

Loads CDPHE investigation records and computes active-investigation counts over time, duration distributions, and county-level overlap statistics.

### STEP2 — Generate outbreak matrix and detection points
**Notebook:** `STEP2_Generate_Outbreak_Matrix_and_DPs.ipynb`
**Produces:** Paper **Figure 3** (Outbreak Matrix) and detection-point summary statistics.

Constructs the county × time outbreak indicator matrix from CDPHE investigation records and computes alert lead times.

### STEP3 — CDPHE capacity vs. TLGRF comparison
**Notebook:** `STEP3_CDPHE_vs_TLGRF.ipynb`
**Produces:** CDPHE capacity vs. TLGRF figures; tables `combined_confusion`, `populous_binary`, and `rankings`.

Joins TLGRF alert signals with CDPHE investigation records, computes confusion matrices, and generates the main case study figures and tables.

### STEP4 — Threshold sensitivity and policy analysis
**Notebook:** `STEP4_try_threshold_policy.ipynb`
**Produces:** Threshold sensitivity figures and policy comparison plots.

Sweeps the alert threshold parameter and evaluates precision/recall tradeoffs.

---

## Running the Self-Contained Steps

```bash
# Easiest — from repo root (runs STEP2, STEP3, STEP4 by default):
./run_all.sh

# Include STEP1 (exploratory overlap analysis):
./run_all.sh --all

# Or manually:
cd case_study/src
jupyter notebook   # open and run STEP1–STEP4
```

---

