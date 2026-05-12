# Benchmark: Delta Weighting

## Overview

Evaluates alternative weighting schemes for the GRF forest — delta-based weights versus the telescoping window weights used in TLRF. Tests whether the specific weight construction in TLRF is necessary for performance.

## Paper Outputs

| Output | Produced by |
|---|---|
| Delta weighting benchmark figures | `Benchmark_Delta_TLGRF.ipynb` |

## Files

| File | Description |
|---|---|
| `Benchmark_Delta_TLGRF.ipynb` | Main analysis notebook — loads pre-computed benchmark Parquets from `../data/` and produces delta vs. TLRF comparison plots |

## Input Data

Reads the following pre-computed Parquet files from `../data/`:

- `benchmark_delta_*.parquet` — delta-weighted model predictions
- `benchmark_tlgrf.parquet` — TLRF predictions (baseline)

## Running

```bash
cd analysis/benchmark_delta
jupyter notebook Benchmark_Delta_TLGRF.ipynb
```
