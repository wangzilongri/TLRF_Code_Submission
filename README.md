# TLRF: Transfer Learning Random Forest

> [!TIP]
> **Reproduce all paper figures and tables in one command:**
> ```bash
> # Option A — clone the full repo (includes all pre-computed data, ~1.5 GB):
> git clone https://github.com/wangzilongri/TLRF_Code_Submission && cd TLRF_Code_Submission
> ./run_all.sh          # figure-generating steps only  (~15–30 min)
> ./run_all.sh --all    # full pipeline including upstream preprocessing
>
> # Option B — download the source-only archive from the GitHub release (~30 MB),
> #             then let run_all.sh fetch the data automatically (~1.5 GB):
> tar -xzf TLRF_Code_Submission_source.tar.gz && cd TLRF_Code_Submission
> ./run_all.sh          # detects missing data and downloads it before running
> ```
> `run_all.sh` creates a Python virtual environment, installs every dependency, and runs all notebooks and scripts that produce paper outputs. When Parquet data files are absent it fetches them from GitHub automatically. Requires **Python 3.9+** and **git 2.25+**.

Code repository for the paper:

> **Small Area Estimation of Case Growths for Timely COVID-19 Outbreak Detection**
> She, Wang, Ayer, Chhatwal. *Operations Research* (submitted 2025)

---

## Overview

This repository contains the code and pre-computed model outputs needed to replicate the figures, tables, and benchmarks in the paper. The TLRF model estimates time-varying, county-level COVID-19 exponential growth rates by combining a telescoping window design with the Random Forest framework. The repository is organized into two top-level components: a **case study** comparing TLRF outbreak alerts to Colorado CDPHE investigations, and an **analysis** folder containing all benchmark comparisons (fixed-window baselines, GRF variants, Local Linear Forest, delta-weighting, and k-means TCV). TLRF model outputs are provided as pre-computed Parquet files so that all notebooks can be run locally without re-running GRF training.

---

## Repository Structure

```
TLRF_Code_Submission/
├── README.md                        # This file
├── LICENSE                          # MIT License
├── AUTHORS                          # Author list
├── requirements.txt                 # Python package requirements
├── r_packages.R                     # R package installation script
├── run_all.sh                       # One-command replication script
│
├── case_study/                      # Colorado CDPHE outbreak-alert comparison
│   ├── README.md                    # Case study overview and step-by-step guide
│   ├── data/                        # Pre-computed Parquet inputs for case study
│   └── src/                         # Jupyter notebooks (STEP1–STEP4)
│
└── analysis/                        # Benchmark comparisons and robustness checks
    ├── README.md                    # Analysis overview and figure/table map
    ├── data/                        # Pre-computed benchmark Parquet files
    │   ├── augmented_us_counties.parquet
    │   ├── imputed_augmented_us_counties.parquet
    │   ├── benchmark_tlgrf/         # TLRF backtest predictions (chunked)
    │   ├── benchmark_grf_*/         # GRF variant predictions (chunked)
    │   ├── benchmark_llf_*/         # LLF predictions (chunked)
    │   ├── benchmark_fixed_window/  # Fixed-window predictions (chunked)
    │   └── ...                      # Other benchmark Parquets
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

### Quick start (recommended)

Two equivalent starting points:

**Option A — clone the full repo** (includes all pre-computed Parquet data, ~1.5 GB download):
```bash
git clone https://github.com/wangzilongri/TLRF_Code_Submission
cd TLRF_Code_Submission
./run_all.sh
```

**Option B — source-only archive** (download `TLRF_Code_Submission_source.tar.gz` from the [GitHub release](https://github.com/wangzilongri/TLRF_Code_Submission/releases), ~30 MB). The archive contains all code and notebooks but not the large Parquet data files. `run_all.sh` detects the missing data and downloads it automatically (~1.5 GB) before running:
```bash
tar -xzf TLRF_Code_Submission_source.tar.gz
cd TLRF_Code_Submission
./run_all.sh           # auto-fetches data on first run, then proceeds normally
```

`run_all.sh` creates `.venv/`, installs all Python dependencies, sets `MPLBACKEND=Agg` for headless rendering, and runs each notebook in its correct working directory. Per-step logs are written to `.run_logs/`. Requires **Python 3.9+** and **git 2.25+** on `PATH`.

**Default mode** runs only the final analysis/visualisation step for each benchmark — the step that reads pre-computed Parquet/CSV inputs and writes paper figures and metric tables.

**`--all` mode** additionally runs upstream preprocessing and model-fitting steps that were originally executed on an HPC cluster. Some of those steps require R + the `grf` package or large intermediate datasets not included in the repo; they may fail in a plain local environment.

### Manual setup

```bash
# Create and activate a virtual environment
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
TLRF model outputs — county-level estimated growth rates, prediction intervals, and backtest metrics — are provided as Parquet files inside `case_study/data/` and `analysis/data/`. The full repository (git clone or full tar) includes these files. The source-only archive omits them; `run_all.sh` fetches them automatically on first run.

### What `run_all.sh` downloads (when data is absent)
Three directories are fetched via `git sparse-checkout` from the public GitHub repository (~1.5 GB total):
- `analysis/data/` — all benchmark Parquet files (~1.4 GB)
- `case_study/data/` — case study Parquet files (~16 MB)
- `analysis/benchmark_transfer_learning/stage2_benchmark_results/` — LASSO-TL pre-computed results (~78 MB)

### Case study (`case_study/`)
The case study is **fully self-contained** — all four notebooks run from the pre-computed Parquet files in `case_study/data/`.

### Analysis benchmarks (`analysis/`)
The benchmark notebooks in `analysis/` require the pre-computed benchmark Parquet files in `analysis/data/`.

---

## Replication

The fastest path is `./run_all.sh` from the repo root. To run a single sub-folder manually, `cd` into it and open the notebook(s) in Jupyter, or run the `.py` script directly with `python`.

### Case study (Colorado CDPHE comparison)

All notebooks read from pre-computed Parquet files in `case_study/data/` — no additional data required.

| Notebook | Produces | run_all.sh mode |
|---|---|---|
| `STEP1_check_investigation_overlap.ipynb` | Exploratory overlap summary | `--all` only |
| `STEP2_Generate_Outbreak_Matrix_and_DPs.ipynb` | Paper **Figure 3** | default |
| `STEP3_CDPHE_vs_TLGRF.ipynb` | Main case study figures and tables | default |
| `STEP4_try_threshold_policy.ipynb` | Threshold policy figures | default |

### Analysis benchmarks

Each sub-folder is independent. All figure-generating steps read from pre-computed Parquets in `analysis/data/`.

| Sub-folder | Produces | Default step |
|---|---|---|
| `benchmark_fixed_window/` | Figure 2, fixed-windows table | `STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb` |
| `benchmark_GRF/` | GRF benchmark plots, `updated_flexible_table` | `Benchmark_TLGRF_vs_Classical_GRF.ipynb` |
| `benchmark_LLF/` | LLF / Stage-2 benchmark plots | `Benchmark_LLF_TLGRF_Results.ipynb` |
| `benchmark_delta/` | Delta weighting benchmark | `Benchmark_Delta_TLGRF.ipynb` |
| `TLGRF_Feature_Importance/` | Feature importance plots, `TOPV20_Itemized` | STEP2, STEP3, STEP4 |
| `coronaSEIR/` | SEIR-TLRF vs. SEIR-tcv figures, `SEIR_metrics` | `Analyse_SEIR_Results_w_Colorado_Case_Study.ipynb` |
| `benchmark_tcv_kmeans_code/` | k-means TCV benchmark, `Best_Kmeans_Table` | `STEP4_generate_validation_diff.ipynb` |
| `benchmark_transfer_learning/` | LASSO-TL benchmark (Appendix E) | `STEP6_Evaluate_Stage2_Predictions.py` |
| `OLS_Weighted_Telescopic_Form/` | `Inclusion_Exclusion_Table_OLS` | `OLS_Weighted_Telescopic_Form.ipynb` |

### Robustness check (Appendix A1)

`analysis/A1_Robustness_Check/` is self-contained — pre-computed predictions included. The default step is `STEP3_R2C1_Analyse_Results.py`; `--all` additionally runs STEP1 (DGP) and STEP2 (GRF training, requires R).

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

---

## Hardware Requirements

### For running the analysis notebooks (local replication)
Most notebooks read from pre-computed Parquet files and can be run on a standard laptop or workstation:
- **CPU:** Any modern multi-core processor
- **Memory:** 16 GB RAM recommended (largest Parquet files are ~330 MB; peak in-memory usage is under 8 GB)
- **Storage:** ~2 GB for the full repository including all Parquet files (or ~30 MB for the source archive + ~1.5 GB downloaded on first run)

### For TLRF model training (outputs pre-computed)
Re-running the GRF training is **not required** to replicate the paper's figures and tables — all outputs are provided as Parquet files.

---

## Paper Reference

She, Z., Wang, Z., Chhatwal, J., Ayer, T. (2025). Small Area Estimation of Case Growths for Timely COVID-19 Outbreak Detection. *Operations Research* (submitted).

**Preprint:** <https://arxiv.org/abs/2312.04110>

**Code:** <https://github.com/wangzilongri/TLRF_Code_Submission>

### BibTeX

```bibtex
@misc{she2023small,
  title         = {Small Area Estimation of Case Growths for Timely {COVID}-19 Outbreak Detection},
  author        = {She, Zhaowei and Wang, Zilong and Chhatwal, Jagpreet and Ayer, Turgay},
  year          = {2023},
  eprint        = {2312.04110},
  archivePrefix = {arXiv},
  primaryClass  = {stat.ML},
  doi           = {10.48550/arXiv.2312.04110},
  url           = {https://arxiv.org/abs/2312.04110}
}
```

---

## License

MIT License. See `LICENSE` for details.
