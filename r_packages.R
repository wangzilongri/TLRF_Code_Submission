# R package installer for TLGRF code submission
# Run with: Rscript r_packages.R
# Requires R >= 4.0

pkgs <- c(
  # Core GRF / causal forest (TLGRF model and all GRF/LLF benchmarks)
  "grf",          # >= 2.0.0  — main model package (Tibshirani et al.)

  # Data manipulation
  "data.table",   # fast CSV reading (county-level panel data)
  "dplyr",
  "plyr",
  "tidyr",

  # Modelling utilities used in R scripts
  "caret",
  "mltools",
  "rpart",
  "minpack.lm",   # nonlinear LS (used in some benchmark scripts)
  "Rcpp",

  # Parallel execution (model training loops)
  "doParallel",
  "foreach",

  # Time-series utilities
  "zoo",
  "dtw",
  "anytime",

  # Misc
  "rlist",
  "rattle",
  "evaluate",
  "ggplot2"
)

new_pkgs <- pkgs[!(pkgs %in% installed.packages()[, "Package"])]
if (length(new_pkgs) > 0) {
  install.packages(new_pkgs, repos = "https://cloud.r-project.org", dependencies = TRUE)
} else {
  message("All R packages already installed.")
}

lapply(pkgs, library, character.only = TRUE)
message("All packages loaded successfully.")
