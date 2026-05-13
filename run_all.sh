#!/usr/bin/env bash
#
# run_all.sh — reproduce every paper figure, table, and benchmark from
#              the pre-computed inputs included in this repository.
#
# Usage:
#   ./run_all.sh
#
# Requirements: Python 3.9+ available as `python3`. Everything else
# (packages, Jupyter) is installed automatically into .venv/.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$REPO/.venv"
LOG_DIR="$REPO/.run_logs"
mkdir -p "$LOG_DIR"

# ── colours (disabled when not writing to a terminal) ────────────────────────
if [[ -t 1 ]]; then
    GRN='\033[0;32m' RED='\033[0;31m' BLD='\033[1m' RST='\033[0m'
else
    GRN='' RED='' BLD='' RST=''
fi
hdr() { echo -e "\n${BLD}── $* ──${RST}"; }
ok()  { echo -e "${GRN}✓${RST}"; }
fail(){ echo -e "${RED}✗${RST}  (log: $1)"; }

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
    printf "  %-52s" "$label"
    if ( cd "$REPO/$dir" && \
         "$JUPYTER" nbconvert --to notebook --execute --inplace \
             --ExecutePreprocessor.kernel_name=python3 \
             --ExecutePreprocessor.timeout=1800 "$nb" \
       ) > "$log" 2>&1; then
        ok; PASS=$((PASS + 1))
    else
        fail "$log"; FAILS+=("$label"); FAIL=$((FAIL + 1))
    fi
}

run_py() {                     # run_py "label" "rel/dir" "script.py"
    local label="$1" dir="$2" script="$3"
    local log="$LOG_DIR/${label// /_}.log"
    printf "  %-52s" "$label"
    if ( cd "$REPO/$dir" && "$PYTHON" "$script" ) > "$log" 2>&1; then
        ok; PASS=$((PASS + 1))
    else
        fail "$log"; FAILS+=("$label"); FAIL=$((FAIL + 1))
    fi
}

# ── 3. case study ─────────────────────────────────────────────────────────────
hdr "Case study"
run_nb "STEP1 investigation overlap"   case_study/src  STEP1_check_investigation_overlap.ipynb
run_nb "STEP2 outbreak matrix"         case_study/src  STEP2_Generate_Outbreak_Matrix_and_DPs.ipynb
run_nb "STEP3 CDPHE vs TLGRF"          case_study/src  STEP3_CDPHE_vs_TLGRF.ipynb
run_nb "STEP4 threshold policy"        case_study/src  STEP4_try_threshold_policy.ipynb

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

# ── 9. summary ────────────────────────────────────────────────────────────────
echo ""
hdr "Summary"
echo -e "  Passed : ${GRN}${PASS}${RST}"
echo -e "  Failed : ${RED}${FAIL}${RST}"
if [[ $FAIL -gt 0 ]]; then
    echo -e "\n  ${RED}Failed steps:${RST}"
    for f in "${FAILS[@]}"; do echo "    • $f"; done
    echo ""
    echo "  Logs are in $LOG_DIR/"
    exit 1
fi
echo -e "  ${GRN}All paper outputs reproduced.${RST}"
echo "  Logs are in $LOG_DIR/"
