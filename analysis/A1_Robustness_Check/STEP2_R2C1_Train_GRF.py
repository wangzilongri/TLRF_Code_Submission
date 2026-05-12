"""
STEP2_R2C1_Train_GRF.py
------------------------
Trains the Two-Lag Growth Rate Forest (TLGRF) model on the synthetic DGP data
produced by STEP1.

NOTE: Pre-computed results are provided in R2C1_predictions.parquet (same directory).
Running STEP2 from scratch requires ~1-2 hours on a modern laptop.
Skip to STEP3 to reproduce the paper's tables and figures using the pre-computed file.

What this script does
---------------------
1. Reads the even/odd first-difference parquet files from ./data/.
2. For each time step t in [21, t_max], trains two RegressionForest models
   (one log-differenced, one linear-differenced) on data up to t using the
   matching parity (even t -> even training set, odd t -> odd training set).
3. Predicts d_log_I and d_I at t for all counties.
4. Writes predictions to ./R2C1_predictions.parquet.

Run: python STEP2_R2C1_Train_GRF.py
"""

import os
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.model_selection import GridSearchCV
from econml.grf import RegressionForest

# ---

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(SCRIPT_DIR, "data")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "R2C1_predictions.parquet")

# ---
# Load data produced by STEP1

even_path = os.path.join(DATA_DIR, "TLGRF_R2C1_data_fd_even.parquet")
odd_path  = os.path.join(DATA_DIR, "TLGRF_R2C1_data_fd_odd.parquet")

df_fd_even = pd.read_parquet(even_path)
df_fd_odd  = pd.read_parquet(odd_path)

print("Even data shape:", df_fd_even.shape)
print(df_fd_even.head())

print("\nOdd data shape:", df_fd_odd.shape)
print(df_fd_odd.head())

# ---

t_max_odd  = df_fd_odd["t"].max()
t_max_even = df_fd_even["t"].max()
t_max      = max(t_max_odd, t_max_even)
print(f"\nt_max = {t_max}")

# ---

param_grid = {
    "n_estimators":     [100, 200],
    "max_depth":        [5, 10, None],
    "min_samples_leaf": [2, 5, 10],
    "max_features":     ["auto", "sqrt", 0.5],
}

FEATURE_COLS = [f"X_{i}" for i in range(1, 7)]

# ---
# Pre-materialise all data slices (avoids re-reading inside worker)

def collect_pd(t):
    df_source = df_fd_even if t % 2 == 0 else df_fd_odd
    return (t, df_source[df_source["t"] <= t].copy())

t_index_range     = list(range(21, t_max + 1))
materialized_data = [collect_pd(t) for t in t_index_range]

# ---
# Per-timestep training function

def process_t_index(t_and_df):
    t_index, df_pd = t_and_df

    X      = df_pd[FEATURE_COLS].values
    y_log  = df_pd["d_log_I"].values   # mis-specified log-linear target
    y_lin  = df_pd["d_I"].values       # correctly specified linear target

    # Fit mis-specified (log-differenced) model
    grid_log = GridSearchCV(
        estimator=RegressionForest(),
        param_grid=param_grid,
        cv=3,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
    )
    grid_log.fit(X, y_log)
    best_forest_log = grid_log.best_estimator_

    # Fit correctly specified (linear-differenced) model
    grid_lin = GridSearchCV(
        estimator=RegressionForest(),
        param_grid=param_grid,
        cv=3,
        scoring="neg_mean_squared_error",
        n_jobs=-1,
    )
    grid_lin.fit(X, y_lin)
    best_forest_lin = grid_lin.best_estimator_

    # Predict for t == t_index only
    df_pred  = df_pd[df_pd["t"] == t_index]
    X_pred   = df_pred[FEATURE_COLS].values

    y_pred_log = best_forest_log.predict(X_pred)
    y_pred_lin = best_forest_lin.predict(X_pred)

    I_tc = df_pred["I_tc"].values

    lengths = {
        "c":           len(df_pred["c"]),
        "t":           len(df_pred),
        "I_tc":        len(I_tc),
        "pred_d_log_I": len(y_pred_log),
        "pred_d_I":    len(y_pred_lin),
        "r_tc":        len(df_pred["r_tc"]),
    }
    print(f"Lengths at t={t_index}: {lengths}")

    pred_df = pd.DataFrame({
        "c":           df_pred["c"].values.ravel(),
        "t":           [t_index] * len(df_pred),
        "I_tc":        I_tc.ravel(),
        "pred_d_log_I": y_pred_log.ravel(),
        "pred_d_I":    y_pred_lin.ravel(),
        "r_tc":        df_pred["r_tc"].values.ravel(),
    })

    return pred_df, best_forest_log, best_forest_lin

# ---
# Parallel execution across time steps

results_list = Parallel(n_jobs=-1, verbose=10)(
    delayed(process_t_index)(item) for item in materialized_data
)

# ---
# Unpack results

all_preds           = [res[0] for res in results_list]
best_estimators_log = {t: res[1] for (t, _), res in zip(materialized_data, results_list)}
best_estimators_lin = {t: res[2] for (t, _), res in zip(materialized_data, results_list)}

results_df = pd.concat(all_preds, ignore_index=True).sort_values(["t", "c"])
print("\nResults shape:", results_df.shape)
print(results_df.head())

# ---
# Save predictions

results_df.to_parquet(OUTPUT_PATH, index=False, compression="snappy")
print(f"\nPredictions written to: {OUTPUT_PATH}")

# Optional: persist best models with joblib
# import joblib
# for t in best_estimators_log:
#     joblib.dump(best_estimators_log[t], os.path.join(SCRIPT_DIR, f"best_forest_log_t{t}.pkl"))
#     joblib.dump(best_estimators_lin[t], os.path.join(SCRIPT_DIR, f"best_forest_lin_t{t}.pkl"))
