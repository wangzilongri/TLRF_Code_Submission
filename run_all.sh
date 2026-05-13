#!/usr/bin/env bash
#
# run_all.sh — reproduce paper figures and tables from pre-computed inputs.
#
# Usage:
#   ./run_all.sh            # default: figure-generating steps only (~15–30 min)
#   ./run_all.sh --all      # full pipeline, including upstream preprocessing
#
# Default mode runs only the final analysis/visualisation notebook or script
# in each benchmark — the step that reads pre-computed Parquet/CSV inputs and
# writes the paper figures and metric tables.  All required intermediate data
# is already included in the repository.
#
# --all additionally runs earlier pipeline steps (data preparation, model
# fitting) that were originally executed on an HPC cluster.  Some of those
# steps require R + the grf package or large intermediate datasets not
# included in the repo; they may fail in a plain local environment.
#
# Requirements: Python 3.9+ on PATH. Everything else is installed into .venv/.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$REPO/.venv"
LOG_DIR="$REPO/.run_logs"
mkdir -p "$LOG_DIR"

# ── parse flags ───────────────────────────────────────────────────────────────
FULL_PIPELINE=false
for arg in "$@"; do
  case $arg in
    --all) FULL_PIPELINE=true ;;
    *) echo "Unknown flag: $arg  (valid: --all)"; exit 1 ;;
  esac
done

# ── colours (disabled when stdout is not a terminal) ─────────────────────────
if [[ -t 1 ]]; then
    GRN='\033[0;32m' RED='\033[0;31m' DIM='\033[2m' BLD='\033[1m' RST='\033[0m'
else
    GRN='' RED='' DIM='' BLD='' RST=''
fi
hdr()  { echo -e "\n${BLD}── $* ──${RST}"; }
skip() { echo -e "  ${DIM}skip  $*${RST}"; }

# ── 1. virtual environment ────────────────────────────────────────────────────
hdr "Environment"
if [[ ! -f "$VENV/bin/python" ]]; then
    echo "  Creating .venv ..."
    python3 -m venv "$VENV"
fi
echo "  Installing / verifying packages ..."
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$REPO/requirements.txt"
echo -e "  ${GRN}Environment ready${RST}"

PYTHON="$VENV/bin/python"
JUPYTER="$VENV/bin/jupyter"
export MPLBACKEND=Agg          # headless matplotlib; no display needed

# ── 2. helpers ────────────────────────────────────────────────────────────────
PASS=0; FAIL=0; FAILS=()

run_nb() {                     # run_nb "label" "rel/dir" "notebook.ipynb"
    local label="$1" dir="$2" nb="$3"
    local log="$LOG_DIR/${label// /_}.log"
    printf "  %-54s" "$label"
    if ( cd "$REPO/$dir" && \
         "$JUPYTER" nbconvert --to notebook --execute --inplace \
             --ExecutePreprocessor.kernel_name=python3 \
             --ExecutePreprocessor.timeout=1800 "$nb" \
       ) > "$log" 2>&1; then
        echo -e "${GRN}✓${RST}"; PASS=$((PASS + 1))
    else
        echo -e "${RED}✗${RST}  (log: $log)"; FAILS+=("$label"); FAIL=$((FAIL + 1))
    fi
}

run_py() {                     # run_py "label" "rel/dir" "script.py"
    local label="$1" dir="$2" script="$3"
    local log="$LOG_DIR/${label// /_}.log"
    printf "  %-54s" "$label"
    if ( cd "$REPO/$dir" && "$PYTHON" "$script" ) > "$log" 2>&1; then
        echo -e "${GRN}✓${RST}"; PASS=$((PASS + 1))
    else
        echo -e "${RED}✗${RST}  (log: $log)"; FAILS+=("$label"); FAIL=$((FAIL + 1))
    fi
}

# ── 3. case study ─────────────────────────────────────────────────────────────
hdr "Case study"
if [[ $FULL_PIPELINE == true ]]; then
    run_nb "STEP1 investigation overlap"   case_study/src  STEP1_check_investigation_overlap.ipynb
fi
run_nb "STEP2 outbreak matrix (Figure 3)" case_study/src  STEP2_Generate_Outbreak_Matrix_and_DPs.ipynb
run_nb "STEP3 CDPHE vs TLGRF"             case_study/src  STEP3_CDPHE_vs_TLGRF.ipynb
run_nb "STEP4 threshold policy"           case_study/src  STEP4_try_threshold_policy.ipynb

# ── 4. benchmarks ─────────────────────────────────────────────────────────────
hdr "Benchmarks"
run_nb "GRF variants"                  analysis/benchmark_GRF              Benchmark_TLGRF_vs_Classical_GRF.ipynb
run_nb "Local Linear Forest"           analysis/benchmark_LLF              Benchmark_LLF_TLGRF_Results.ipynb
run_nb "Fixed-window baselines"        analysis/benchmark_fixed_window     STEP2_Analyse_TLGRF_vs_Fixed_Windows.ipynb
run_nb "Delta weighting"               analysis/benchmark_delta            Benchmark_Delta_TLGRF.ipynb
run_nb "k-means TCV"                   analysis/benchmark_tcv_kmeans_code  STEP4_generate_validation_diff.ipynb
run_py "LASSO-TL benchmark (STEP 6)"   analysis/benchmark_transfer_learning STEP6_Evaluate_Stage2_Predictions.py

# ── 5. SEIR (Appendix G) ──────────────────────────────────────────────────────
hdr "SEIR (Appendix G)"
run_nb "SEIR analysis"                 analysis/coronaSEIR  Analyse_SEIR_Results_w_Colorado_Case_Study.ipynb

# ── 6. feature importance ─────────────────────────────────────────────────────
hdr "Feature importance"
run_nb "Feature importance (STEP 2)"   analysis/TLGRF_Feature_Importance  STEP2_Examine_TLGRF_Feature_Importance.ipynb
run_nb "Tree depths (STEP 3)"          analysis/TLGRF_Feature_Importance  STEP3_Examine_TLGRF_Depths.ipynb
run_nb "Leaf sizes (STEP 4)"           analysis/TLGRF_Feature_Importance  STEP4_Examine_TLGRF_Leaf_Sizes.ipynb

# ── 7. OLS telescopic form ────────────────────────────────────────────────────
hdr "OLS telescopic form"
run_nb "OLS weighted telescopic form"  analysis/OLS_Weighted_Telescopic_Form  OLS_Weighted_Telescopic_Form.ipynb

# ── 8. robustness check (Appendix A1) ────────────────────────────────────────
hdr "Appendix A1 robustness check"
run_py "A1 STEP 3 analyse results"     analysis/A1_Robustness_Check  STEP3_R2C1_Analyse_Results.py

# ── 9. upstream pipeline steps (--all only) ───────────────────────────────────
if [[ $FULL_PIPELINE == true ]]; then
    echo ""
    hdr "Upstream pipeline steps (--all)"
    echo -e "  ${DIM}Note: some steps below require HPC intermediate data or R + grf;${RST}"
    echo -e "  ${DIM}they may fail in a plain local environment.${RST}"

    # k-means TCV: data preparation
    run_nb "TCV STEP1 prepare data"        analysis/benchmark_tcv_kmeans_code  STEP1_prepare_data_for_kmeans.ipynb
    run_py "TCV STEP2 k-means script"      analysis/benchmark_tcv_kmeans_code  STEP2_kmeans_hhs_script.py
    run_nb "TCV STEP3 merge clusters"      analysis/benchmark_tcv_kmeans_code  STEP3_Merge_Clusters_w_Panel_Data.ipynb

    # LASSO-TL: intermediate stages
    run_nb "LASSO-TL STEP1 stitch blocks"  analysis/benchmark_transfer_learning  STEP1_Stitch_Blocks.ipynb
    run_py "LASSO-TL STEP2 gram matrices"  analysis/benchmark_transfer_learning  STEP2_Generate_Gram_Matrices.py
    run_py "LASSO-TL STEP2 stage1 betas"   analysis/benchmark_transfer_learning  STEP2_Generate_Stage1_Beta.py
    run_py "LASSO-TL STEP3 stage1 betas"   analysis/benchmark_transfer_learning  STEP3_Generate_Stage1_Beta.py
    run_nb "LASSO-TL STEP4 LOO betas"      analysis/benchmark_transfer_learning  STEP4_Generate_Leave_one_Out_beta.ipynb
    run_py "LASSO-TL STEP5 stage2"         analysis/benchmark_transfer_learning  STEP5_Stage2_Estimator.py

    # A1: DGP and GRF training (STEP2 requires R + grf)
    run_py "A1 STEP1 DGP"                  analysis/A1_Robustness_Check  STEP1_R2C1_DGP.py
    run_py "A1 STEP2 train GRF (needs R)"  analysis/A1_Robustness_Check  STEP2_R2C1_Train_GRF.py
fi

# ── 10. summary ───────────────────────────────────────────────────────────────
echo ""
hdr "Summary"
if [[ $FULL_PIPELINE == true ]]; then
    echo -e "  Mode   : ${BLD}--all${RST} (full pipeline)"
else
    echo -e "  Mode   : ${BLD}default${RST} (figure-generating steps only)"
fi
echo -e "  Passed : ${GRN}${PASS}${RST}"
echo -e "  Failed : ${RED}${FAIL}${RST}"
if [[ $FAIL -gt 0 ]]; then
    echo -e "\n  ${RED}Failed steps:${RST}"
    for f in "${FAILS[@]}"; do echo "    • $f"; done
    echo ""
    echo "  Logs are in $LOG_DIR/"
    exit 1
fi
echo -e "  ${GRN}All steps passed.${RST}"
echo "  Logs are in $LOG_DIR/"
