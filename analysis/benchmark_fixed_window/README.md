# Benchmark: Fixed-Window Baselines

> [!TIP]
> **Quick start:** run `./run_all.sh` from the repo root to reproduce all paper outputs at once.

## Overview

Compares TLRF mean absolute error against a suite of fixed-window exponential growth rate estimators (7-, 14-, 21-, and 28-day windows). Demonstrates that the adaptive telescoping window outperforms any single fixed choice across the county population distribution.

## Paper Outputs

| Output | Produced by |
|---|---|
| Figure 2 (MAE vs. Fixed Windows) | `STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb` |
| Table: `fixed_windows` | `STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb` |

## Files

| File | Description |
|---|---|
| `STEP1_Generate_TLGRF_vs_Fixed_Windows_script.py` | Generates fixed-window predictions from raw backtest data; writes `../data/benchmark_fixed_window.parquet` |
| `STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb` | Loads `../data/benchmark_fixed_window.parquet` and `../data/benchmark_tlgrf.parquet`; produces Figure 2 and the fixed windows table |

## Running

`../data/benchmark_fixed_window.parquet` is pre-computed. Run only STEP2 for local replication:

```bash
cd analysis/benchmark_fixed_window
jupyter notebook STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb
```
