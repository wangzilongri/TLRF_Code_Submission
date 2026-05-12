# TLGRF Feature Importance

## Overview

This folder aggregates GRF variable importance scores across the full TLRF backtest period and county set, producing the ranked feature importance figures and the TOPV20 itemized table reported in the paper.

## Paper Outputs

| Output | Produced by |
|---|---|
| Feature importance figures | `STEP2_Examine_TLGRF_Feature_Importance.ipynb` |
| Table: `TOPV20_Itemized` | `STEP2_Examine_TLGRF_Feature_Importance.ipynb` |
| Tree depth figures | `STEP3_Examine_TLGRF_Depths.ipynb` |
| Leaf size figures | `STEP4_Examine_TLGRF_Leaf_Sizes.ipynb` |

## Files

| File | Description |
|---|---|
| `STEP1_Extract_TLGRF_Feature_Importance.r` | R script (HPC) that extracts per-feature GRF importance scores from trained forests and writes `feature_importance.csv`, `TLGRF_depth_by_date.csv`, `TLGRF_leaf_and_tree_size_by_date.csv` |
| `STEP2_Examine_TLGRF_Feature_Importance.ipynb` | Loads `feature_importance.csv` and `Sorted_Feature_Importance.csv`; produces ranked importance plots and TOPV20 table |
| `STEP3_Examine_TLGRF_Depths.ipynb` | Loads `TLGRF_depth_by_date.csv`; produces tree depth diagnostic plots |
| `STEP4_Examine_TLGRF_Leaf_Sizes.ipynb` | Loads `TLGRF_leaf_and_tree_size_by_date.csv`; produces leaf and tree size diagnostic plots |
| `feature_importance.csv` | Pre-computed raw GRF importance scores |
| `Sorted_Feature_Importance.csv` | Pre-computed sorted importance scores |
| `TLGRF_depth_by_date.csv` | Pre-computed per-date tree depth statistics |
| `TLGRF_leaf_and_tree_size_by_date.csv` | Pre-computed per-date leaf and tree size statistics |

## Running

All pre-computed CSVs are included. Run STEP2–STEP4 directly:

```bash
cd analysis/TLGRF_Feature_Importance
jupyter notebook
# Open and run STEP2, STEP3, STEP4 in order
```

STEP1 requires the trained GRF forest objects on HPC and is not needed for local replication.
