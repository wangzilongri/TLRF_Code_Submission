# Benchmark: Local Linear Forest (LLF)

## Overview

Compares TLRF against Local Linear Forest (LLF) and a two-stage GRF + OLS pipeline. Assesses whether forest-based nonparametric weighting is necessary relative to local linear approximations.

## Paper Outputs

| Output | Produced by |
|---|---|
| LLF / Stage-2 benchmark plots | `Benchmark_LLF_TLGRF_Results.ipynb` |

## Files

| File | Description |
|---|---|
| `Benchmark_LLF_TLGRF_Results.ipynb` | Main analysis notebook — loads pre-computed benchmark Parquets from `../data/` and produces comparison plots |

## Input Data

Reads the following pre-computed Parquet files from `../data/`:

- `benchmark_llf_classical.parquet` — classical LLF predictions
- `benchmark_llf_tlgrf.parquet` — LLF variant using TLRF covariate set
- `benchmark_llrf_blocked.parquet` — blocked LLF predictions
- `benchmark_llrf_blocked_top10.parquet` — blocked LLF, top-10 features
- `benchmark_regression_forest_blocked.parquet` — blocked Regression Forest
- `benchmark_tlgrf.parquet` — TLRF predictions (baseline)

## Running

```bash
cd analysis/benchmark_LLF
jupyter notebook Benchmark_LLF_TLGRF_Results.ipynb
```
