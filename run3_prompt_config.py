# =============================================================================
# run3_prompt_config.py
# Prompt configuration for Notebook 5 - Run 3 LLM Enrichment
# Edit this file to tune prompt behaviour without touching notebook code.
# =============================================================================

from pathlib import Path
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. MODEL AND SAMPLING
# -----------------------------------------------------------------------------
MODEL_ID        = 'anthropic.claude-3-5-sonnet-20241022-v2:0'
MAX_TOKENS      = 500                        # Max output tokens per transaction
TEMPERATURE     = 0.0                        # Deterministic
BUDGET_USD      = 15.00                      # Hard stop - ~$12 expected at $0.058/row
TARGET_ROWS     = 1000

# -----------------------------------------------------------------------------
# 2. SAMPLE STRATIFICATION
# -----------------------------------------------------------------------------
BASE_LAYER_ROWS  = 600                       # Rows distributed across providers
TOP_UP_ROWS      = 400                       # Rows from focus categories
TOP_UP_PER_CAT   = 50                        # Rows per focus category

FOCUS_CATEGORIES = [
    'HEALTHCARE_MEDICAL',
    'BAR',
    'CAFE',
    'REWARDS',
    'HOME_RENOVATION___MAINTENANCE',
    'INSURANCE_GENERAL',
    'INTERNAL_TRANSFER',
    'EXTERNAL_TRANSFER_IN',
]

# -----------------------------------------------------------------------------
# 3. PRE-FILTER SETTINGS
# -----------------------------------------------------------------------------
AGGREGATOR_DT_VALUE = '7'                    # DT only applies to this aggregator

# MCC codes excluded from definitive spend classification
MCC_SKIP = {'6010', '6011', '6012', '0', '0000', '00000000', 'nan', 'None', ''}

# MCC codes that signal non-spend (Rule 4)
MCC_NON_SPEND = {'6010', '6011'}

# Biller code values treated as not populated
BILLER_CODE_ZEROS = {'0', '0000', '00000000', 'nan', 'None', ''}

# Provider name fragments (case-insensitive match)
PROVIDER_ANZ       = 'ANZ'
PROVIDER_ING       = 'ING'
PROVIDER_BANKWEST  = 'BANKWEST'
PROVIDER_UP        = 'UP'
PROVIDER_MACQUARIE = 'MACQUARIE'

# -----------------------------------------------------------------------------
# 4. INVALID KEY BLOCKLIST
# LLM must never return these keys
# -----------------------------------------------------------------------------
INVALID_KEY_BLOCKLIST = [
    # Confirmed invalid taxonomy keys
    'SAVINGS',
    'CHEQUES',
    'OTHER_LOANS',
    'CASH',
    # Truncated / deprecated forms returned by LLM in Run 1
    'SPEND',
    'NON_SPEND',
    'TRANSPORT',
    'ENTERTAINMENT',
    'HARDWARE_HOME_IMPROVEMENT',
    'PARKING',
    'UTILITIES',
    'FINANCIAL_SERVICES',
    'BANKING',
    'TRANSFER',
    'FEES',
    'INSURANCE',
]

# -----------------------------------------------------------------------------
# 5. RULES FILE CONFIG
# -----------------------------------------------------------------------------
RULES_FILE          = 'assets/rules_sonnet-3.5_20260121.md'
RULES_STRIP_PATTERN = r'^#{1,3}\s*section\s*3'   # Strip Section 3 onwards

# -----------------------------------------------------------------------------
# 6. OUTPUT PATHS
# -----------------------------------------------------------------------------
OUTPUT_DIR  = Path('outputs')
OUTPUT_FILE = OUTPUT_DIR / f'run3_results_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'