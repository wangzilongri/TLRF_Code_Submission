# Benchmark: k-means Time-Series Cross-Validation (TCV)

> [!TIP]
> **Quick start:** run `./run_all.sh` from the repo root to reproduce all paper outputs at once.

## Overview

This folder implements and evaluates a k-means time-series cross-validation benchmark that compares TLRF's county grouping approach against k-means-based temporal stratification.

## Paper Outputs

| Output | Produced by |
|---|---|
| k-means TCV benchmark figures | `STEP4_generate_validation_diff.ipynb` |
| Table: `Best_Kmeans_Table` | `STEP4_generate_validation_diff.ipynb` |

## Pipeline

| Step | File | Description |
|---|---|---|
| 1 | `STEP1_prepare_data_for_kmeans.ipynb` | Loads county-level panel data from `../data/augmented_us_counties.parquet` and reference tables (`ZipHsaHrr15.csv`, `ZIP_to_FIPS.csv`, `hhs_regions.csv`); produces `hhs_kmeans_data.csv` |
| 2 | `STEP2_kmeans_hhs_script.py` | Runs k-means clustering over a range of cluster counts (100–3200) using Dask-ML; writes cluster assignment CSVs |
| 3 | `STEP3_Merge_Clusters_w_Panel_Data.ipynb` | Merges cluster assignments back onto the panel data for validation |
| 4 | `STEP4_generate_validation_diff.ipynb` | Loads merged data from `../data/augmented_us_counties.parquet`; computes validation differences and produces the Best_Kmeans_Table and figures |

## Reference Data (in `../data/`)

| File | Description |
|---|---|
| `ZipHsaHrr15.csv` | ZIP-to-HSA/HRR crosswalk (Dartmouth Atlas, 2015) |
| `ZIP_to_FIPS.csv` | ZIP-to-county FIPS crosswalk |
| `hhs_regions.csv` | HHS region assignments for all US states and territories |

## Running

STEP1, STEP3, and STEP4 can be run interactively. STEP2 (k-means over thousands of clusters) is a standalone script:

```bash
cd analysis/benchmark_tcv_kmeans_code
jupyter notebook              # open and run STEP1, STEP3, STEP4
python STEP2_kmeans_hhs_script.py  # run STEP2 separately
```
