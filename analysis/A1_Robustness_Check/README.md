# A1 Robustness Check: Hyperparameter Sensitivity

> [!TIP]
> **Quick start:** run `./run_all.sh` from the repo root to reproduce paper figures (default), or `./run_all.sh --all` for the full pipeline.

## Overview

This folder is **fully self-contained** and tests the sensitivity of TLRF performance to key hyperparameters (number of trees, minimum node size, telescoping window length bounds). It corresponds to Appendix A1 of the paper.

## Paper Outputs

| Output | Produced by |
|---|---|
| Table: `R2C1_daily_mean_mae_rmse` | `STEP3_R2C1_Analyse_Results.py` |
| Table: `R2C1_parameter` | `STEP3_R2C1_Analyse_Results.py` |

## Files

| File | Description |
|---|---|
| `STEP1_R2C1_DGP.py` | Generates the synthetic DGP for the robustness check; writes `data/TLGRF_R2C1_data_fd_even.parquet` and `data/TLGRF_R2C1_data_fd_odd.parquet` |
| `STEP2_R2C1_Train_GRF.py` | Trains TLRF with varied hyperparameter settings on the DGP data; writes `R2C1_predictions.parquet` |
| `STEP3_R2C1_Analyse_Results.py` | Loads `R2C1_predictions.parquet` and produces the paper tables and figures |
| `R2C1_predictions.parquet` | **Pre-computed** — TLRF predictions across all hyperparameter configurations |
| `data/` | DGP data (`TLGRF_R2C1_data_fd_even.parquet`, `TLGRF_R2C1_data_fd_odd.parquet`) — included |

## Running

`R2C1_predictions.parquet` is pre-computed, so the paper tables can be reproduced by running only STEP3:

```bash
# Easiest — from repo root:
./run_all.sh

# Or manually:
cd analysis/A1_Robustness_Check
python STEP3_R2C1_Analyse_Results.py
```

To regenerate from scratch (`./run_all.sh --all` runs STEP1 and STEP2 automatically; note STEP2 requires R + `grf`):

```bash
python STEP1_R2C1_DGP.py          # generates DGP data into data/
python STEP2_R2C1_Train_GRF.py    # trains GRF variants; requires R + grf
python STEP3_R2C1_Analyse_Results.py
```
