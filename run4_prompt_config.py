from pathlib import Path
from datetime import datetime

# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
MODEL_ID    = 'anthropic.claude-3-5-sonnet-20241022-v2:0'
MAX_TOKENS  = 500
NER_TOKENS  = 50       # Step 6a NER call - intentionally small
TEMPERATURE = 0.0
BUDGET_USD  = 15.00

# -----------------------------------------------------------------------------
# Merchant lookup config
# -----------------------------------------------------------------------------
RUN_NER_ALWAYS = True  # True = run 6a+6b even if Step 1.5 hit (comparison mode)
                       # False = skip 6a+6b if Step 1.5 hit (production mode)

# -----------------------------------------------------------------------------
# Sample
# -----------------------------------------------------------------------------
TARGET_ROWS      = 1000
BASE_LAYER_ROWS  = 600
TOP_UP_ROWS      = 400
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
]

# -----------------------------------------------------------------------------
# DT settings
# -----------------------------------------------------------------------------
AGGREGATOR_DT_VALUE = '7'
MCC_SKIP            = {'6010', '6011', '6012', '0', '0000', '00000000', 'nan', 'None', ''}
MCC_NON_SPEND       = {'6010', '6011'}
BILLER_CODE_ZEROS   = {'0', '0000', '00000000', 'nan', 'None', ''}

PROVIDER_ANZ        = 'ANZ'
PROVIDER_ING        = 'ING'
PROVIDER_BANKWEST   = 'BANKWEST'
PROVIDER_UP         = 'UP'
PROVIDER_MACQUARIE  = 'MACQUARIE'

# -----------------------------------------------------------------------------
# Invalid key blocklist
# -----------------------------------------------------------------------------
INVALID_KEY_BLOCKLIST = [
    'SAVINGS', 'CHEQUES', 'OTHER_LOANS', 'CASH', 'SPEND', 'NON_SPEND',
    'TRANSPORT', 'ENTERTAINMENT', 'HARDWARE_HOME_IMPROVEMENT', 'PARKING',
    'UTILITIES', 'FINANCIAL_SERVICES', 'BANKING', 'TRANSFER', 'FEES', 'INSURANCE',
]

# -----------------------------------------------------------------------------
# Rules file
# -----------------------------------------------------------------------------
RULES_FILE          = 'assets/rules_sonnet-3.5_20260121.md'
RULES_STRIP_PATTERN = r'^#+\s*3[\.\s]'

# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------
OUTPUT_DIR  = Path('outputs')
OUTPUT_FILE = OUTPUT_DIR / f'run4_results_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
OUTPUT_DIR.mkdir(exist_ok=True)