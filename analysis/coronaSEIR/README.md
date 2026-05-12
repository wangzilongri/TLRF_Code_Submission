# coronaSEIR: TLRF Growth Rate Integration into SEIR Models

## Overview

This folder contains the code and pre-computed results for Appendix G §"Using TLRF to Improve SEIR Estimates of Colorado Counties" in the paper. It demonstrates that TLRF growth rate estimates can be plugged into a standard SEIR compartmental model to improve county-level case forecasts in Colorado.

## Paper Outputs

| Output | File |
|---|---|
| Table: SEIR-TLRF vs. SEIR-tcv MAE/RMSE | `combined_metrics.csv` (pre-computed) |
| Figure: SEIR MAE benchmark | `SEIR_Benchmarks_MAE.png` (pre-computed) |
| Figure: SEIR RMSE benchmark | `SEIR_Benchmarks_RMSE.png` (pre-computed) |

The pre-computed outputs above are included in this folder. The main analysis notebook `Analyse_SEIR_Results_w_Colorado_Case_Study.ipynb` regenerates these from `combined_metrics.csv` and produces the paper figures.

## Running the Analysis

The analysis notebook requires `combined_metrics.csv` (included) and the CDPHE case study data from `../../../case_study/data/`.

The heavy SEIR simulation step (spawn scripts) that originally generated `combined_metrics.csv` requires HPC resources and the per-county simulation outputs in `./sim_results/`. These are not included in the submission due to size (7,000+ files). The pre-computed `combined_metrics.csv` is provided so the table and figures in the paper can be reproduced without re-running the simulation.

## Key Files

| File | Description |
|---|---|
| `Analyse_SEIR_Results_w_Colorado_Case_Study.ipynb` | Main analysis notebook — produces paper table and figures |
| `SEIR_Changepoints_TLGRF.py` | SEIR simulation script using TLRF growth rates (HPC) |
| `SEIR_Changepoints_tcv.py` | SEIR simulation script using tcv growth rates (HPC) |
| `spawn_TLGRF.sh` / `spawn_tcv.sh` | HPC job submission scripts for SEIR simulations |
| `combined_metrics.csv` | Pre-computed daily MAE/RMSE metrics (SEIR-TLRF vs. SEIR-tcv) |
| `filtered_colorado_df.csv` | Colorado county FIPS list used in the analysis |
| `simulated_colorado_SEIR.csv` | Example SEIR trajectory for a Colorado county |
| `corona_model/` | Third-party SEIR model package (see LICENSE) |

## Third-Party License

The `corona_model/` package is a third-party SEIR implementation. See `LICENSE` for its terms.
