# Benchmark: GRF Variants

> [!TIP]
> **Quick start:** run `./run_all.sh` from the repo root to reproduce paper figures (default), or `./run_all.sh --all` for the full pipeline.

## Overview

Compares TLRF against standard GRF (no telescoping window) and GRF with alternative covariate sets. Isolates the contribution of the telescoping window design by holding the Random Forest model class fixed.

## Paper Outputs

| Output | Produced by |
|---|---|
| GRF benchmark plots | `Benchmark_TLGRF_vs_Classical_GRF.ipynb` |
| Table: `updated_flexible_table` | `Benchmark_TLGRF_vs_Classical_GRF.ipynb` |

## Files

| File | Description |
|---|---|
| `Benchmark_TLGRF_vs_Classical_GRF.ipynb` | Main analysis notebook — loads pre-computed benchmark Parquets from `../data/` and produces benchmark plots and the updated flexible table |

## Input Data

Reads the following pre-computed Parquet files from `../data/`:

- `benchmark_grf_shifted_W_time_invariant.parquet` — GRF with time-invariant covariates, shifted window
- `benchmark_grf_shifted_W_time_variant.parquet` — GRF with time-variant covariates, shifted window
- `benchmark_grf_time_invariant.parquet` — standard GRF, time-invariant covariates
- `benchmark_grf_time_variant.parquet` — standard GRF, time-variant covariates
- `benchmark_tlgrf.parquet` — TLRF predictions (baseline)

## Running

```bash
# Easiest — from repo root:
./run_all.sh

# Or manually:
cd analysis/benchmark_GRF
jupyter notebook Benchmark_TLGRF_vs_Classical_GRF.ipynb
```
