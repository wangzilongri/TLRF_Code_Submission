# Benchmark: LASSO Transfer Learner (LASSOTL)

> [!TIP]
> **Quick start:** run `./run_all.sh` from the repo root to reproduce paper figures (default), or `./run_all.sh --all` for the full pipeline.

## Overview

This folder implements the LASSO Transfer Learner (LASSOTL) benchmark described in Appendix E of the paper. LASSOTL is a two-stage estimator: Stage 1 fits a LASSO regression per county using leave-one-out cross-validation; Stage 2 applies a transfer-learning correction to adapt Stage 1 predictions across counties. Results are compared against TLRF on the Colorado backtest.

## Paper Outputs

| Output | Produced by |
|---|---|
| LASSOTL benchmark plots (MAE, RMSE) | `STEP6_Evaluate_Stage2_Predictions.py` |
| Pre-computed figures (λ = 10⁻⁵) | `Benchmark_Stage2_lambda_exp=-5_mae.png`, `Benchmark_Stage2_lambda_exp=-5_rmse.png` |

Pre-computed `stage2_benchmark_results/` is included so STEP6 can be run without earlier steps.

## Pipeline

| Step | File | Description |
|---|---|---|
| 1 | `STEP1_Stitch_Blocks.ipynb` | Reads imputed block CSV files from `../data/imputed_block_windowsize=2/`; stitches even/odd time blocks into `imputed_even_blocks.parquet` and `imputed_odd_blocks.parquet` |
| 2a | `STEP2_Generate_Gram_Matrices.py` | Computes per-cutoff gram matrices X′X and writes them to `./gram_matrices/` |
| 2b | `STEP2_Generate_Stage1_Beta.py` | Fits LASSO Stage 1 betas and writes them to `./betas/` |
| 3 | `STEP3_Generate_Stage1_Beta.py` | Refines Stage 1 beta estimates |
| 4 | `STEP4_Generate_Leave_one_Out_beta.ipynb` | Applies leave-one-out Woodbury updates to compute LOO betas; reads from `./betas/` and `./gram_matrices/` |
| 5 | `STEP5_Stage2_Estimator.py` | Runs the Stage 2 transfer-learning estimator; writes per-county NPY prediction files to `./stage2_betas_organized/` |
| 6 | `STEP6_Evaluate_Stage2_Predictions.py` | Aggregates Stage 2 NPY files into `./stage2_benchmark_results/*.parquet`; computes MAE/RMSE vs. TLRF and saves figures |

## Pre-computed Outputs (included)

| Folder/File | Contents |
|---|---|
| `stage2_benchmark_results/` | Stage 2 prediction Parquets and benchmark metric CSVs/figures for λ ∈ {10⁻⁵, 10⁻⁴} |
| `stage1_lasso/` | Stage 1 LASSO model objects (`.pkl`) and coefficient CSVs per cutoff |
| `approximate_stage1_results/` | Intermediate Stage 1 result CSVs |

## Running

To reproduce the paper figures from pre-computed outputs:

```bash
# Easiest — from repo root:
./run_all.sh

# Or manually (default step only):
cd analysis/benchmark_transfer_learning
python STEP6_Evaluate_Stage2_Predictions.py
```

To run the full pipeline from scratch (requires intermediate data from HPC), use `./run_all.sh --all`, which runs STEP1–STEP6 in order.
