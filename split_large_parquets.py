"""
split_large_parquets.py
-----------------------
Splits large parquet files (>50 MB) in analysis/data/ into part directories
so every part file is under 50 MB for GitHub compatibility.

Each original X.parquet becomes a directory X/ containing part_000.parquet,
part_001.parquet, etc.  pandas.read_parquet("path/to/X/") reads the directory
natively via pyarrow and returns the full DataFrame.

Run from the repo root:
    python split_large_parquets.py
"""

import math
import os
import pathlib
import shutil

import pandas as pd

TARGET_MB = 40          # target part size in MB (keep well under 50 MB limit)
DATA_DIR = pathlib.Path("analysis/data")

LARGE_FILES = [
    "benchmark_fixed_window.parquet",
    "benchmark_llf_tlgrf.parquet",
    "benchmark_tlgrf_top10.parquet",
    "benchmark_tlgrf_imputed.parquet",
    "benchmark_tlgrf.parquet",
    "benchmark_regression_forest_blocked.parquet",
    "benchmark_llf_classical.parquet",
    "benchmark_llrf_blocked.parquet",
    "benchmark_llrf_blocked_top10.parquet",
    "benchmark_grf_shifted_W_time_variant.parquet",
    "benchmark_grf_time_variant.parquet",
    "benchmark_grf_shifted_W_time_invariant.parquet",
    "benchmark_grf_time_invariant.parquet",
]


def split_parquet(src: pathlib.Path, target_mb: int = TARGET_MB) -> None:
    size_mb = src.stat().st_size / (1024 ** 2)
    if size_mb <= target_mb:
        print(f"  SKIP  {src.name} ({size_mb:.0f} MB — already under {target_mb} MB)")
        return

    print(f"  SPLIT {src.name} ({size_mb:.0f} MB) ...", flush=True)
    df = pd.read_parquet(src)
    n_rows = len(df)
    n_parts = math.ceil(size_mb / target_mb)
    rows_per_part = math.ceil(n_rows / n_parts)

    out_dir = src.parent / src.stem          # e.g. analysis/data/benchmark_tlgrf/
    out_dir.mkdir(exist_ok=True)

    for i in range(n_parts):
        chunk = df.iloc[i * rows_per_part : (i + 1) * rows_per_part]
        part_path = out_dir / f"part_{i:03d}.parquet"
        chunk.to_parquet(part_path, index=False)
        part_mb = part_path.stat().st_size / (1024 ** 2)
        print(f"    wrote {part_path.name}  ({len(chunk):,} rows, {part_mb:.1f} MB)")

    src.unlink()
    print(f"  -> deleted {src.name}, directory {out_dir.name}/ has {n_parts} parts")


if __name__ == "__main__":
    for fname in LARGE_FILES:
        src = DATA_DIR / fname
        if src.exists():
            split_parquet(src)
        else:
            print(f"  MISSING {fname} — skipping")
