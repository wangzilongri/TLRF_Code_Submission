# Benchmark: Fixed-Window Baselines

> [!TIP]
> **Quick start:** run `./run_all.sh` from the repo root to reproduce paper figures (default), or `./run_all.sh --all` for the full pipeline.

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
| `STEP1_Generate_TLGRF_vs_Fixed_Windows_script.py` | Generates fixed-window predictions from raw backtest data; writes `../data/benchmark_fixed_window/` (chunked Parquet) |
| `STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb` | Loads `../data/benchmark_fixed_window/` and `../data/benchmark_tlgrf/`; produces Figure 2 and the fixed windows table |

## Running

Pre-computed Parquets are included in `../data/benchmark_fixed_window/`. Run only STEP2 to reproduce the paper figures:

```bash
# Easiest — from repo root:
./run_all.sh

# Or manually:
cd analysis/benchmark_fixed_window
jupyter notebook STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb
```

To regenerate predictions from scratch (requires HPC backtest outputs), run `STEP1` first, then `STEP2`.
