"""
STEP1_R2C1_DGP.py
-----------------
Generates the synthetic Data Generating Process (DGP) for the A1 Robustness Check
(Reviewer 2, Comment 1).

Produces:
  ./data/TLGRF_R2C1_data_fd_even.parquet   -- even time-period rows
  ./data/TLGRF_R2C1_data_fd_odd.parquet    -- odd  time-period rows

Run: python STEP1_R2C1_DGP.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---

np.random.seed(42)

# Parameters
T = 200   # time periods
C = 100   # counties
K = 6     # features

# ---

records = []
C_history = {}   # (c, t) -> cumulative cases C_tc

for c in range(1, C + 1):
    C_tc = 100.0   # initialise cumulative cases
    for t in range(1, T + 1):
        X = np.random.normal(loc=0.05 * t, scale=40.0, size=K)
        intercept   = float(np.sum(X))
        growth_rate = float(np.sum([max(0, x) for x in X[:2]]))

        C_tc += growth_rate   # strictly non-negative accumulation
        C_history[(c, t)] = C_tc

        # I_tc := C_tc - C_{t-22, c}
        if t > 22:
            I_tc = C_tc - C_history[(c, t - 22)]
        else:
            I_tc = C_tc

        log_C_tc = float(np.log(C_tc + 0.001))
        log_I_tc = float(np.log(I_tc + 0.001))

        row_data = {
            "t":        t,
            "c":        c,
            "C_tc":     float(C_tc),
            "log_C_tc": log_C_tc,
            "I_tc":     float(I_tc),
            "log_I_tc": log_I_tc,
            "alpha_tc": intercept,
            "r_tc":     growth_rate,
        }
        for k in range(K):
            row_data[f"X_{k+1}"] = float(X[k])

        records.append(row_data)

df = pd.DataFrame(records)

# ---

print(f"DGP DataFrame shape: {df.shape}")
print(df.head())

# ---

# Plot I_tc over time for first 10 counties
plt.figure(figsize=(12, 6))
for c_id in sorted(df["c"].unique())[:10]:
    county_data = df[df["c"] == c_id]
    plt.plot(county_data["t"], county_data["I_tc"], label=f"County {c_id}")

plt.xlabel("Time (t)")
plt.ylabel(r"$I_{t,c}$ (Observed Outcome)")
plt.title(r"Observed Outcome Incident $I_{t,c}$ Over Time by County")
plt.legend(title="County", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()

# ---
# Build lagged first-difference columns

df_sorted = df.sort_values(["c", "t"]).copy()

df_sorted["I_prev"]      = df_sorted.groupby("c")["I_tc"].shift(1)
df_sorted["log_I_prev"]  = df_sorted.groupby("c")["log_I_tc"].shift(1)

# Drop rows where lag is missing (first row per county)
df_model = df_sorted.dropna(subset=["I_prev"]).copy()

df_model["d_log_I"] = df_model["log_I_tc"] - df_model["log_I_prev"]
df_model["d_I"]     = df_model["I_tc"]     - df_model["I_prev"]

# Select final columns
keep_cols = ["t", "c", "I_tc", "log_I_tc", "r_tc", "d_log_I", "d_I",
             "X_1", "X_2", "X_3", "X_4", "X_5", "X_6"]
df_model = df_model[keep_cols].reset_index(drop=True)

# ---
# Split into even / odd time periods

df_even = df_model[df_model["t"] % 2 == 0].reset_index(drop=True)
df_odd  = df_model[df_model["t"] % 2 == 1].reset_index(drop=True)

print(f"\nEven split shape: {df_even.shape}")
print(df_even.head())

print(f"\nOdd split shape:  {df_odd.shape}")
print(df_odd.head())

# ---

even_path = os.path.join(OUTPUT_DIR, "TLGRF_R2C1_data_fd_even.parquet")
odd_path  = os.path.join(OUTPUT_DIR, "TLGRF_R2C1_data_fd_odd.parquet")

df_even.to_parquet(even_path, index=False)
df_odd.to_parquet(odd_path,  index=False)

print(f"\nWritten: {even_path}")
print(f"Written: {odd_path}")
