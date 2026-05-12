# TLRF: Transfer Learning Random Forest

Code repository for the paper:

> **Small Area Estimation of Case Growths for Timely COVID-19 Outbreak Detection**
> She, Wang, Ayer, Chhatwal. *Operations Research* (submitted 2025)

---

## Overview

This repository contains the code and pre-computed model outputs needed to replicate the figures, tables, and benchmarks in the paper. The TLRF model estimates time-varying, county-level COVID-19 exponential growth rates by combining a telescoping window design with the Random Forest framework. The repository is organized into two top-level components: a **case study** comparing TLRF outbreak alerts to Colorado CDPHE investigations, and an **analysis** folder containing all benchmark comparisons (fixed-window baselines, GRF variants, Local Linear Forest, delta-weighting, and k-means TCV). TLRF model outputs are provided as pre-computed Parquet files so that most notebooks can be run without access to the original HPC cluster.

---

## Repository Structure

```
TLRF_Code_Submission/
├── README.md                        # This file
├── LICENSE                          # MIT License
├── AUTHORS                          # Author list
├── requirements.txt                 # Python package requirements
├── r_packages.R                     # R package installation script
│
├── case_study/                      # Colorado CDPHE outbreak-alert comparison
│   ├── README.md                    # Case study overview and step-by-step guide
│   ├── data/                        # Input parquet files for case study notebooks
│   └── src/                         # Jupyter notebooks (STEP1–STEP4)
│
└── analysis/                        # Benchmark comparisons and robustness checks
    ├── README.md                    # Analysis overview and figure/table map
    ├── data/                        # Pre-computed benchmark parquet files
    ├── A1_Robustness_Check/         # Appendix A1 parameter sensitivity (self-contained)
    ├── benchmark_GRF/               # GRF variant benchmarks
    ├── benchmark_LLF/               # Local Linear Forest / Stage-2 benchmarks
    ├── benchmark_fixed_window/      # Fixed-window baseline benchmarks
    ├── benchmark_delta/             # Delta (weighting scheme) benchmarks
    ├── TLGRF_Feature_Importance/    # Feature importance analysis
    ├── coronaSEIR/                  # SEIR benchmark (Appendix G)
    ├── benchmark_tcv_kmeans_code/   # k-means TCV benchmark
    ├── benchmark_transfer_learning/ # LASSO Transfer Learner benchmark (Appendix E)
    └── OLS_Weighted_Telescopic_Form/# OLS weighted telescopic form derivation
```

---

## Installation

### Python environment

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv tlrf-env
source tlrf-env/bin/activate        # macOS / Linux
# tlrf-env\Scripts\activate         # Windows

# Install all Python dependencies
pip install -r requirements.txt
```

Requires **Python 3.9 or later**. The full list of packages with minimum version constraints is in `requirements.txt`.

### R environment

R is only required to re-run the TLRF model training (GRF fitting step). Pre-computed outputs are provided, so **R is not needed to replicate the paper's figures and tables**.

If you do wish to run the GRF training:

```r
# In R (4.x):
source("r_packages.R")
```

This installs `grf`, `tidyverse`, `data.table`, and `arrow`.

### Launching notebooks

```bash
cd TLRF_Code_Submission
jupyter notebook
# or: jupyter lab
```

Navigate to `case_study/src/` or any `analysis/` sub-folder and open the relevant notebook.

---

## Data

### Pre-computed TLRF outputs (Parquet)
TLRF model outputs — county-level estimated growth rates, prediction intervals, and backtest metrics — are provided as Parquet files inside `case_study/data/` and `analysis/data/`. These files were generated on an HPC cluster and are included so that reviewers and replicators do not need to re-run the GRF training step.

### Case study (`case_study/`)
The case study is **fully self-contained** — all four notebooks run from the pre-computed Parquet files in `case_study/data/`.

### Analysis benchmarks (`analysis/`)
The benchmark notebooks in `analysis/` require the pre-computed benchmark Parquet files in `analysis/data/`. These files are included in the repository. If you need to regenerate them from raw per-county CSVs (e.g., after updating the training window), see the data pipeline notes in `analysis/README.md`.

---

## Replication

### Step 1 — Case study (Colorado CDPHE comparison)
Run notebooks in order inside `case_study/src/`. All run from pre-computed Parquet files — no additional data required.

| Notebook | Description | Produces |
|---|---|---|
| `STEP1_check_investigation_overlap.ipynb` | CDPHE investigation timing and overlap | Exploratory summary |
| `STEP2_Generate_Outbreak_Matrix_and_DPs.ipynb` | County × time outbreak indicator matrix | Paper **Figure 3** |
| `STEP3_CDPHE_vs_TLGRF.ipynb` | CDPHE capacity vs. TLRF comparison | Main case study figures and tables |
| `STEP4_try_threshold_policy.ipynb` | Threshold sensitivity sweep | Policy comparison figures |

### Step 2 — Analysis benchmarks
Each sub-folder inside `analysis/` is independent. Run the notebooks within each folder after ensuring `analysis/data/` is populated:

```
analysis/benchmark_fixed_window/   →  Figure 2, fixed-windows table
analysis/benchmark_GRF/            →  GRF benchmark plots, updated_flexible_table
analysis/benchmark_LLF/            →  LLF / Stage-2 benchmark plots
analysis/benchmark_delta/          →  Delta weighting benchmark
analysis/TLGRF_Feature_Importance/ →  Feature importance plots, TOPV20_Itemized table
analysis/coronaSEIR/               →  SEIR-TLRF vs. SEIR-tcv figures and table (Appendix G)
analysis/benchmark_tcv_kmeans_code/→  k-means TCV benchmark, Best_Kmeans_Table
analysis/benchmark_transfer_learning/ →  LASSO Transfer Learner benchmark (Appendix E)
```

### Step 3 — Robustness check (Appendix A1)
`analysis/A1_Robustness_Check/` is fully self-contained (pre-computed results included). Run the notebook(s) inside to reproduce the `R2C1_daily_mean_mae_rmse` and `R2C1_parameter` tables.

---

## Paper Figure / Table Reference

| Paper item | Generating code location |
|---|---|
| Figure 2 (MAE vs. Fixed Windows) | `analysis/benchmark_fixed_window/` |
| Figure 3 (Outbreak Matrix) | `case_study/src/STEP2_Generate_Outbreak_Matrix_and_DPs.ipynb` |
| CDPHE capacity figures | `case_study/src/STEP3_CDPHE_vs_TLGRF.ipynb` |
| Threshold policy figures | `case_study/src/STEP4_try_threshold_policy.ipynb` |
| GRF benchmark plots | `analysis/benchmark_GRF/` |
| LLF / Stage-2 benchmark plots | `analysis/benchmark_LLF/` |
| Delta weighting benchmark | `analysis/benchmark_delta/` |
| k-means TCV benchmark | `analysis/benchmark_tcv_kmeans_code/` |
| Feature importance plots | `analysis/TLGRF_Feature_Importance/` |
| SEIR-TLRF vs. SEIR-tcv figures | `analysis/coronaSEIR/Analyse_SEIR_Results_w_Colorado_Case_Study.ipynb` |
| LLF / Stage-2 (LASSOTL) benchmark plots | `analysis/benchmark_transfer_learning/` |
| Table: R2C1_daily_mean_mae_rmse | `analysis/A1_Robustness_Check/` |
| Table: R2C1_parameter | `analysis/A1_Robustness_Check/` |
| Table: fixed_windows | `analysis/benchmark_fixed_window/` |
| Table: combined_confusion, populous_binary, rankings | `case_study/src/STEP3_CDPHE_vs_TLGRF.ipynb` |
| Table: Best_Kmeans_Table | `analysis/benchmark_tcv_kmeans_code/` |
| Table: updated_flexible_table | `analysis/benchmark_GRF/` |
| Table: Inclusion_Exclusion_Table_OLS | `analysis/OLS_Weighted_Telescopic_Form/` |
| Table: TOPV20_Itemized | `analysis/TLGRF_Feature_Importance/` |
| Table: SEIR_metrics (SEIR-TLRF vs. SEIR-tcv) | `analysis/coronaSEIR/Analyse_SEIR_Results_w_Colorado_Case_Study.ipynb` |

---

## Software Requirements

### Python
- Python 3.9+
- See `requirements.txt` for the full package list. Key packages:
  - `pandas`, `numpy`, `scipy`
  - `pyarrow` (Parquet I/O)
  - `scikit-learn`
  - `matplotlib`, `seaborn`
  - `jupyter`

### R
- R 4.x
- See `r_packages.R` for the installation script. Key packages:
  - `grf` (the Random Forest engine that powers TLRF)
  - `tidyverse`, `data.table`, `arrow`

### Operating System
- The analysis notebooks are OS-independent and have been tested on macOS and Linux.
- The TLRF model training was run on **Linux** (RHEL 8.6, kernel 4.18.0, x86\_64).

### Notes
- Most analysis notebooks were originally developed on Databricks (PySpark); the versions in this repository have been ported to run on a local Python environment.
- The TLRF model training itself (not included here — outputs provided as Parquet) was run on an HPC cluster using R with the `grf` package.

---

## Hardware Requirements

### For running the analysis notebooks (local replication)
Most notebooks read from pre-computed Parquet files and can be run on a standard laptop or workstation:
- **CPU:** Any modern multi-core processor
- **Memory:** 16 GB RAM recommended (largest Parquet files are ~330 MB; peak in-memory usage is under 8 GB)
- **Storage:** ~2 GB for the full repository including all Parquet files

### For TLRF model training (HPC — outputs pre-computed)
The GRF training and backtest that produced the Parquet files in `analysis/data/` and `case_study/data/` were run on the Georgia Tech ISyE HPC cluster:
- **Node:** `isye-syang605.isye.gatech.edu`
- **CPU:** 127 × AMD EPYC-Rome cores
- **Memory:** 960 GiB RAM
- **OS:** Linux RHEL 8.6 (kernel 4.18.0-372.26.1.el8\_6.x86\_64)

Re-running the GRF training is **not required** to replicate the paper's figures and tables — all outputs are provided as Parquet files.

---

## Paper Reference

```
She, Z., Wang, Z., Ayer, T., Chhatwal, J. (2025). Small Area Estimation of Case
Growths for Timely COVID-19 Outbreak Detection. Operations Research (submitted).
```

---

## License

MIT License. See `LICENSE` for details.
