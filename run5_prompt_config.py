# =============================================================================
# run5_prompt_config.py
# All tunable parameters for Run 5 (9. llm_enrichment_run5.ipynb).
# Basis: run4_prompt_config.py
#
# Changes from Run 4:
#   - RUN_NER_ALWAYS: False (production mode - NER only on P1 miss rows)
#   - P1_SHORTCIRCUIT: False (new flag - skip main LLM call on P1 hits)
#   - OUTPUT_FILE: updated to run5_results
#   - NER_TOKENS: increased slightly to accommodate extended schema
# =============================================================================

from pathlib import Path
from datetime import datetime

# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
MODEL_ID    = 'anthropic.claude-3-5-sonnet-20241022-v2:0'
MAX_TOKENS  = 300    # main classification call
NER_TOKENS  = 100    # NER call - extended schema (merchant + category), still compact
TEMPERATURE = 0.0

# -----------------------------------------------------------------------------
# Budget
# -----------------------------------------------------------------------------
BUDGET_USD  = 20.0   # hard stop

# -----------------------------------------------------------------------------
# Run 5 flags (new / changed vs Run 4)
# -----------------------------------------------------------------------------
# Production NER mode - only run NER on P1-miss rows.
# Run 4 used True (comparison mode - NER on every row).
RUN_NER_ALWAYS   = False

# P1 short-circuit - if True, skip main LLM call on P1 hits and use
# p1_bank_db_key directly as llm_final_pred_key. Saves ~124 Bedrock calls
# at negligible accuracy cost (+0.8pp in Run 4). Set False to keep full
# pipeline active and measure the delta properly in Notebook 10 analysis.
P1_SHORTCIRCUIT  = False

# -----------------------------------------------------------------------------
# Sample parameters (same as Run 4 for comparability)
# -----------------------------------------------------------------------------
TARGET_ROWS      = 990
BASE_LAYER_ROWS  = 600
TOP_UP_ROWS      = 390
TOP_UP_PER_CAT   = 50
FOCUS_CATEGORIES = [
    'HEALTHCARE_MEDICAL',
    'BAR',
    'CAFE',
    'REWARDS',
    'HOME_RENOVATION___MAINTENANCE',
    'INSURANCE_GENERAL',
    'INTERNAL_TRANSFER',
    'EXTERNAL_TRANSFER_IN',
    'EXTERNAL_TRANSFER_OUT',
]

# -----------------------------------------------------------------------------
# Decision tree parameters (unchanged)
# -----------------------------------------------------------------------------
AGGREGATOR_DT_VALUE = 7
MCC_SKIP            = {'6012', '0', ''}   # ambiguous / non-definitive codes
MCC_NON_SPEND       = {'6010', '6011'}
BILLER_CODE_ZEROS   = {'0', '00', '000', '0000', '00000', '000000', '0000000'}

PROVIDER_ANZ        = 'ANZ'
PROVIDER_ING        = 'ING'
PROVIDER_BANKWEST   = 'BANKWEST'
PROVIDER_UP         = 'UP'
PROVIDER_MACQUARIE  = 'MACQUARIE'

# -----------------------------------------------------------------------------
# Valid key gate
# -----------------------------------------------------------------------------
INVALID_KEY_BLOCKLIST = {
    'SAVINGS',          # post-process only - not a valid LLM output
    'CASH',             # invalid taxonomy key
    'TRANSFER',         # truncated - use INTERNAL_TRANSFER / EXTERNAL_TRANSFER_IN/OUT
    'FEES',             # truncated - use specific fee key
    'INSURANCE',        # truncated - use INSURANCE_GENERAL / INSURANCE_OTHER
    'RESTAURANTS__CAFES',  # removed from taxonomy
    'PARKING',          # removed from taxonomy
}

# -----------------------------------------------------------------------------
# Rules file
# -----------------------------------------------------------------------------
RULES_FILE         = 'assets/rules_sonnet-3.5_20260121.md'
RULES_STRIP_PATTERN = r'^#{1,3}\s*(section\s*3|issues|analysis|known issues)'

# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------
OUTPUT_DIR  = Path('outputs')
TIMESTAMP   = datetime.now().strftime('%Y%m%d_%H%M')
OUTPUT_FILE = OUTPUT_DIR / f'run5_results_{TIMESTAMP}.csv'