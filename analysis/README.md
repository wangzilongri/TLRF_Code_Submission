# Analysis: Benchmarks and Robustness Checks

## Overview

This folder contains all benchmark comparisons and the Appendix A1 robustness check for the TLRF paper. Each sub-folder is largely independent and maps to one or more specific figures or tables in the paper. The TLRF model outputs required as inputs to these benchmarks are provided as pre-computed Parquet files in `analysis/data/`.

---

## Directory Layout

```
analysis/
├── README.md                        # This file
├── data/                            # Pre-computed benchmark Parquet files (see below)
├── A1_Robustness_Check/             # Appendix A1 parameter sensitivity — self-contained
├── benchmark_GRF/                   # GRF variant benchmarks
├── benchmark_LLF/                   # Local Linear Forest / Stage-2 benchmarks
├── benchmark_fixed_window/          # Fixed-window baseline benchmarks
├── benchmark_delta/                 # Delta (weighting scheme) benchmarks
├── TLGRF_Feature_Importance/        # Feature importance analysis
├── coronaSEIR/                      # SEIR benchmark (Appendix G; third-party LICENSE)
├── benchmark_tcv_kmeans_code/       # k-means TCV benchmark
├── benchmark_transfer_learning/     # LASSO Transfer Learner benchmark (Appendix E)
└── OLS_Weighted_Telescopic_Form/    # OLS weighted telescopic form derivation
```

---

## Data Files (`data/`)

The `data/` folder contains pre-computed Parquet files used as inputs across multiple benchmark notebooks.

| File pattern | Contents |
|---|---|
| `tlgrf_backtest_*.parquet` | TLGRF county-day predictions from the full backtest |
| `benchmark_grf_*.parquet` | GRF variant predictions (standard GRF, GRF without telescoping) |
| `benchmark_llf_*.parquet` | Local Linear Forest predictions |
| `benchmark_fixed_window_*.parquet` | Fixed-window baseline predictions at various window lengths |
| `benchmark_delta_*.parquet` | Delta (alternative weighting) model predictions |
| `feature_importance_*.parquet` | Per-feature GRF importance scores aggregated over the backtest |

---

## Benchmark Sub-folder Map

### `benchmark_fixed_window/`
**Paper output:** Figure 2 (MAE vs. Fixed Windows), Table `fixed_windows`

Compares TLGRF mean absolute error against a suite of fixed-window exponential growth rate estimators (7-day, 14-day, 21-day, 28-day windows). Demonstrates that the adaptive telescoping window outperforms any single fixed choice across the county population distribution.

### `benchmark_GRF/`
**Paper output:** GRF benchmark plots, Table `updated_flexible_table`

Compares TLGRF against standard GRF (no telescoping) and GRF with alternative covariate sets. Isolates the contribution of the telescoping window design.

### `benchmark_LLF/`
**Paper output:** LLF / Stage-2 benchmark plots

Compares TLGRF against Local Linear Forest (LLF) and a two-stage GRF + OLS pipeline, assessing whether the forest-based nonparametric weighting is necessary relative to local linear approximations.

### `benchmark_delta/`
**Paper output:** Delta weighting benchmark figures

Evaluates alternative weighting schemes for the GRF forest (delta-based weights vs. the telescoping window weights used in TLGRF).

### `TLGRF_Feature_Importance/`
**Paper output:** Feature importance plots, Table `TOPV20_Itemized`

Aggregates GRF variable importance scores across the full backtest period and county set. Produces the ranked feature importance figures and the TOPV20 itemized table reported in the paper.

### `A1_Robustness_Check/`
**Paper output:** Appendix A1 Tables `R2C1_daily_mean_mae_rmse`, `R2C1_parameter`
**Status: Fully self-contained — pre-computed results included.**

Tests sensitivity of TLGRF performance to key hyperparameters (number of trees, minimum node size, telescoping window length bounds). The pre-computed predictions file `R2C1_predictions.parquet` is included; the DGP simulation code is in `STEP1_R2C1_DGP.py`. Additional intermediate data is in `A1_Robustness_Check/data/`. Originally developed on Databricks (PySpark); ported to local Python for this submission.

### `coronaSEIR/`
**Paper output:** Table `SEIR_metrics` (SEIR-TLRF vs. SEIR-tcv MAE/RMSE), Figures `SEIR_MAE` and `SEIR_RMSE` (Appendix G)
**Pre-computed results included:** `combined_metrics.csv`, `SEIR_Benchmarks_MAE.png`, `SEIR_Benchmarks_RMSE.png`

Integrates TLRF growth rate estimates into a SEIR compartmental model and compares forecast accuracy (SEIR-TLRF vs. SEIR-tcv) on Colorado counties. The `Analyse_SEIR_Results_w_Colorado_Case_Study.ipynb` notebook reproduces the paper table and figures from the included `combined_metrics.csv`. The `corona_model/` package is a third-party SEIR implementation — see `coronaSEIR/LICENSE`.

---

## Additional Sub-folders

### `benchmark_tcv_kmeans_code/`
**Paper output:** k-means TCV benchmark figures, Table `Best_Kmeans_Table`

k-means time-series cross-validation benchmark comparing TLGRF's county grouping approach against k-means-based temporal stratification.

### `OLS_Weighted_Telescopic_Form/`
**Paper output:** Table `Inclusion_Exclusion_Table_OLS`

Derivation and numerical validation of the OLS weighted telescopic form used in the theoretical motivation section of the paper.

---

## Running the Benchmarks

```bash
# From the repo root
pip install -r requirements.txt

# Example: reproduce Figure 2 (fixed-window benchmark)
cd analysis/benchmark_fixed_window
jupyter notebook  # open and run the notebook(s) in this folder

# Example: reproduce A1 robustness check (self-contained)
cd analysis/A1_Robustness_Check
jupyter notebook
```

Each sub-folder may contain its own brief README with notebook-specific instructions.
