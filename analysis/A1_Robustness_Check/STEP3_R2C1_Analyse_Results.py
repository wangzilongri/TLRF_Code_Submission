"""
STEP3_R2C1_Analyse_Results.py
------------------------------
Analyses predictions from the TLGRF robustness check (Reviewer 2, Comment 1)
and reproduces the paper's tables and figures.

Inputs
------
  ./R2C1_predictions.parquet    -- pre-computed model predictions (or STEP2 output)

Outputs (printed / displayed)
------------------------------
  - Per-county plot of predicted vs actual growth rates
  - Daily mean RMSE / MAE plot for growth rate estimation
  - R2C1_daily_mean_mae_rmse           (DataFrame — paper table)
  - R2C1_parameter_daily_mean_mae_rmse (DataFrame — paper table)
  - 7-day-ahead case prediction RMSE / MAE plots
  - Summary table: median log-RMSE and log-MAE by model

Run: python STEP3_R2C1_Analyse_Results.py
"""

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ---

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
RESULTS_PATH = os.path.join(SCRIPT_DIR, "R2C1_predictions.parquet")

# ---
# Load predictions

results_df = pd.read_parquet(RESULTS_PATH).sort_values(["t", "c"]).reset_index(drop=True)

print("Predictions shape:", results_df.shape)
print(results_df.head())

# ---
# Plot: Predicted growth rate vs actual growth rate per county

df_plot = results_df[["c", "t", "r_tc", "pred_d_log_I", "pred_d_I"]].copy()

counties = sorted(df_plot["c"].unique())
n    = len(counties)
cols = 3
rows = math.ceil(n / cols)

fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4), sharex=True, sharey=True)
axes = axes.flatten()

for idx, c_id in enumerate(counties):
    ax     = axes[idx]
    sub_df = df_plot[df_plot["c"] == c_id].sort_values("t")

    ax.plot(sub_df["t"], sub_df["r_tc"],          label=r"$r_{tc}$",
            color="black", linewidth=1.8)
    ax.plot(sub_df["t"], sub_df["pred_d_log_I"],  label=r"$\widehat{d_{\log I}}$",
            linestyle="--", color="C1")
    ax.plot(sub_df["t"], sub_df["pred_d_I"],      label=r"$\widehat{d_I}$",
            linestyle=":",  color="C2")

    ax.set_title(f"County {c_id}")
    ax.set_xlabel("t")
    ax.set_ylabel("Growth / Diff")
    ax.grid(True)

for j in range(n, len(axes)):
    fig.delaxes(axes[j])

custom_legend = [
    Line2D([0], [0], color="black", lw=1.8,           label=r"$r_{tc}$"),
    Line2D([0], [0], color="C1",    linestyle="--",   label=r"$\widehat{d_{\log I}}$"),
    Line2D([0], [0], color="C2",    linestyle=":",    label=r"$\widehat{d_I}$"),
]
fig.legend(handles=custom_legend, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.02))
fig.tight_layout()
plt.show()

# ---
# Compute growth-rate error metrics (squared / absolute errors per row)

df_metrics = results_df.copy()
df_metrics["se_log"]     = (df_metrics["pred_d_log_I"] - df_metrics["r_tc"]) ** 2
df_metrics["se_lin"]     = (df_metrics["pred_d_I"]     - df_metrics["r_tc"]) ** 2
df_metrics["ae_log"]     = (df_metrics["pred_d_log_I"] - df_metrics["r_tc"]).abs()
df_metrics["ae_lin"]     = (df_metrics["pred_d_I"]     - df_metrics["r_tc"]).abs()
df_metrics["se_exp_log"] = (np.exp(df_metrics["pred_d_log_I"]) - df_metrics["r_tc"]) ** 2
df_metrics["ae_exp_log"] = (np.exp(df_metrics["pred_d_log_I"]) - df_metrics["r_tc"]).abs()

# Daily mean RMSE and MAE  (R2C1_daily_mean_mae_rmse)
daily_metrics = (
    df_metrics.groupby("t")
    .agg(
        mean_rmse_log    =("se_log",     lambda x: np.sqrt(x.mean())),
        mean_rmse_lin    =("se_lin",     lambda x: np.sqrt(x.mean())),
        mean_rmse_exp_log=("se_exp_log", lambda x: np.sqrt(x.mean())),
        mean_mae_log     =("ae_log",     "mean"),
        mean_mae_lin     =("ae_lin",     "mean"),
        mean_mae_exp_log =("ae_exp_log", "mean"),
    )
    .reset_index()
    .sort_values("t")
)

R2C1_daily_mean_mae_rmse = daily_metrics
print("\nR2C1_daily_mean_mae_rmse:")
print(R2C1_daily_mean_mae_rmse)

# ---
# RMSE plot

y_max_rmse = max(daily_metrics["mean_rmse_log"].max(), daily_metrics["mean_rmse_lin"].max())
y_max_mae  = max(daily_metrics["mean_mae_log"].max(),  daily_metrics["mean_mae_lin"].max())
y_max_rmse = np.ceil(y_max_rmse * 4) / 4
y_max_mae  = np.ceil(y_max_mae  * 4) / 4
y_max      = max(y_max_rmse, y_max_mae) + 0.5

plt.figure(figsize=(10, 4))
plt.plot(daily_metrics["t"], daily_metrics["mean_rmse_log"], label="Mis-specified Exponential Growth Rate Model")
plt.plot(daily_metrics["t"], daily_metrics["mean_rmse_lin"], label="Linear Growth Rate Model")
plt.xlabel("Day (t)")
plt.ylabel("Mean RMSE across counties")
plt.title("Daily Mean RMSE of growth rate parameter estimate by Model")
plt.ylim(0, y_max)
plt.legend()
plt.tight_layout()
plt.show()

# MAE plot
plt.figure(figsize=(10, 4))
plt.plot(daily_metrics["t"], daily_metrics["mean_mae_log"], label="Mis-specified Exponential Growth Rate Model")
plt.plot(daily_metrics["t"], daily_metrics["mean_mae_lin"], label="Linear Growth Rate Model")
plt.xlabel("Day (t)")
plt.ylabel("Mean MAE across counties")
plt.title("Daily Mean MAE of growth rate parameter estimate by Model")
plt.ylim(0, y_max)
plt.legend()
plt.tight_layout()
plt.show()

# ---
# Overall growth-rate summary  (R2C1_parameter_daily_mean_mae_rmse)

overall_summary = {
    "avg_daily_mean_rmse_log": daily_metrics["mean_rmse_log"].mean(),
    "avg_daily_mean_rmse_lin": daily_metrics["mean_rmse_lin"].mean(),
    "avg_daily_mean_mae_log":  daily_metrics["mean_mae_log"].mean(),
    "avg_daily_mean_mae_lin":  daily_metrics["mean_mae_lin"].mean(),
}
R2C1_parameter_daily_mean_mae_rmse = pd.DataFrame([overall_summary])
print("\nR2C1_parameter_daily_mean_mae_rmse:")
print(R2C1_parameter_daily_mean_mae_rmse)

# ---
# 7-day-ahead prediction error

df_7 = results_df.copy()
df_7["pred_I_7ahead_lin"] = df_7["I_tc"] + 7 * df_7["pred_d_I"]
df_7["pred_I_7ahead_log"] = df_7["I_tc"] * np.exp(7 * df_7["pred_d_log_I"])

# Build ground-truth I_{t+7, c} by joining df to a copy shifted by 7
df_future = df_7[["c", "t", "I_tc"]].copy()
df_future = df_future.rename(columns={"t": "t_future", "I_tc": "I_tc_7days_later"})
df_future["t_join"] = df_future["t_future"] - 7   # join key = original t

df_joined = df_7.merge(
    df_future[["c", "t_join", "I_tc_7days_later"]],
    left_on=["c", "t"],
    right_on=["c", "t_join"],
    how="inner",
).drop(columns=["t_join"])

# Filter to positive values before log-transform
mask = (
    (df_joined["I_tc_7days_later"]  > 0) &
    (df_joined["pred_I_7ahead_lin"] > 0) &
    (df_joined["pred_I_7ahead_log"] > 0)
)
df_joined_log = df_joined[mask].copy()

df_joined_log["log_true"]      = np.log(df_joined_log["I_tc_7days_later"])
df_joined_log["log_pred_lin"]  = np.log(df_joined_log["pred_I_7ahead_lin"])
df_joined_log["log_pred_log"]  = np.log(df_joined_log["pred_I_7ahead_log"])

df_joined_log["log_sq_err_lin"]  = (df_joined_log["log_pred_lin"] - df_joined_log["log_true"]) ** 2
df_joined_log["log_sq_err_log"]  = (df_joined_log["log_pred_log"] - df_joined_log["log_true"]) ** 2
df_joined_log["log_abs_err_lin"] = (df_joined_log["log_pred_lin"] - df_joined_log["log_true"]).abs()
df_joined_log["log_abs_err_log"] = (df_joined_log["log_pred_log"] - df_joined_log["log_true"]).abs()

daily_log_metrics = (
    df_joined_log.groupby("t")
    .agg(
        log_rmse_lin=("log_sq_err_lin",  lambda x: np.sqrt(x.mean())),
        log_rmse_log=("log_sq_err_log",  lambda x: np.sqrt(x.mean())),
        log_mae_lin =("log_abs_err_lin", "mean"),
        log_mae_log =("log_abs_err_log", "mean"),
    )
    .reset_index()
    .sort_values("t")
)

# ---
# 7-day-ahead RMSE plot

plt.figure(figsize=(10, 5))
plt.plot(daily_log_metrics["t"], daily_log_metrics["log_rmse_lin"], label="Linear Growth Rate Model")
plt.plot(daily_log_metrics["t"], daily_log_metrics["log_rmse_log"], label="Mis-specified Exponential Growth Rate Model")
plt.ylabel("Log RMSE")
plt.xlabel("t")
plt.title("Root Mean Squared Error (RMSE) in One-Week Ahead Case Predictions")
plt.legend()
plt.grid(True)
plt.show()

# 7-day-ahead MAE plot
plt.figure(figsize=(10, 5))
plt.plot(daily_log_metrics["t"], daily_log_metrics["log_mae_lin"], label="Linear Growth Rate Model")
plt.plot(daily_log_metrics["t"], daily_log_metrics["log_mae_log"], label="Mis-specified Exponential Growth Rate Model")
plt.ylabel("Log MAE")
plt.xlabel("t")
plt.title("Mean Absolute Error (MAE) in One-Week Ahead Case Prediction")
plt.legend()
plt.grid(True)
plt.show()

# ---
# Summary table (paper table)

avg_log_rmse_lin = daily_log_metrics["log_rmse_lin"].median()
avg_log_rmse_log = daily_log_metrics["log_rmse_log"].median()
avg_log_mae_lin  = daily_log_metrics["log_mae_lin"].median()
avg_log_mae_log  = daily_log_metrics["log_mae_log"].median()

summary_table = pd.DataFrame({
    "Method": ["Linear Model", "Exponential Model"],
    "MAE":    [avg_log_mae_lin,  avg_log_mae_log],
    "RMSE":   [avg_log_rmse_lin, avg_log_rmse_log],
}).round(3)

print("\nSummary table (median log-MAE / log-RMSE):")
print(summary_table)
print("\nLaTeX rows:")
print("\\\\\n".join([
    f"{row['Method']} & {row['MAE']:.3f} & {row['RMSE']:.3f}"
    for _, row in summary_table.iterrows()
]))

# ---
# Per-county 7-day-ahead log-prediction plot

df_plot_7 = df_joined_log[["c", "t", "log_pred_lin", "log_pred_log", "log_true"]].copy()

counties = sorted(df_plot_7["c"].unique())
n    = len(counties)
cols = 3
rows = math.ceil(n / cols)

fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4), sharex=True, sharey=True)
axes = axes.flatten()

for idx, c_id in enumerate(counties):
    ax  = axes[idx]
    sub = df_plot_7[df_plot_7["c"] == c_id].sort_values("t")

    ax.plot(sub["t"], sub["log_true"],     label="Log True",              color="black", linewidth=2)
    ax.plot(sub["t"], sub["log_pred_lin"], label="Log Pred — Linear",     ls="--", color="C1")
    ax.plot(sub["t"], sub["log_pred_log"], label="Log Pred — Exponential", ls=":",  color="C2")
    ax.set_title(f"County {c_id}")
    ax.set_xlabel("t")
    ax.set_ylabel("log(cases)")
    ax.grid(True)

for j in range(n, len(axes)):
    fig.delaxes(axes[j])

custom_lines = [
    Line2D([0], [0], color="black", lw=2,          label="Log True"),
    Line2D([0], [0], color="C1",    linestyle="--", label="Linear Model"),
    Line2D([0], [0], color="C2",    linestyle=":",  label="Exponential Model"),
]
fig.legend(handles=custom_lines, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.02))
fig.tight_layout()
plt.show()
