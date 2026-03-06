# =============================================================================
# run2_prompt_config.py
# Prompt configuration for Notebook 4 — Run 2 LLM Enrichment
# Edit this file to tune prompt behaviour without touching notebook code.
# Source of truth for valid keys: cat_keys.txt (110 keys, loaded from DB)
# =============================================================================

# -----------------------------------------------------------------------------
# 1. MODEL & SAMPLING
# -----------------------------------------------------------------------------
MODEL_ID        = "anthropic.claude-3-5-sonnet-20241022-v2:0"       # Bedrock model string
MAX_TOKENS      = 400                        # Max output tokens per transaction
TEMPERATURE     = 0.0                        # Deterministic
BUDGET_USD      = 3.00                       # Hard stop for batch run
TARGET_ROWS     = 500                        # Run 2a target sample size

# -----------------------------------------------------------------------------
# 2. SAMPLE STRATIFICATION
# -----------------------------------------------------------------------------
BASE_LAYER_ROWS   = 300                      # Rows distributed across providers
TOP_UP_ROWS       = 200                      # Rows from focus categories
TOP_UP_PER_CAT    = 25                       # Rows per focus category

FOCUS_CATEGORIES = [
    "HEALTHCARE_MEDICAL",
    "BAR",
    "CAFE",
    "REWARDS",
    "HOME_RENOVATION___MAINTENANCE",
    "INSURANCE_GENERAL",
    "INTERNAL_TRANSFER",
    # SAVINGS removed — post-process only, not a valid LLM prediction target
]

# -----------------------------------------------------------------------------
# 3. PRE-FILTER SETTINGS
# -----------------------------------------------------------------------------
AGGREGATOR_DT_VALUE = "7"                    # DT only applies to this aggregator

# MCC codes excluded from Rule 6 (not treated as definitive spend)
MCC_SKIP = {"6010", "6011", "6012", "0", "0000", "00000000", ""}

# MCC codes that signal non-spend (Rule 4)
MCC_NON_SPEND = {"6010", "6011"}

# Biller code values treated as "not populated"
BILLER_CODE_ZEROS = {"0", "0000", "00000000", "nan", "None", ""}

# Provider name substrings used in DT rules (case-insensitive match)
PROVIDER_ANZ       = "ANZ"
PROVIDER_ING       = "ING"
PROVIDER_BANKWEST  = "BANKWEST"
PROVIDER_UP        = "UP"
PROVIDER_MACQUARIE = "MACQUARIE"

# -----------------------------------------------------------------------------
# 4. INVALID KEY BLOCKLIST
# Keys the LLM must never return.
# Source: Run 1 invalid key analysis + taxonomy cross-check against cat_keys.txt
# NOTE: UTILITIES is a valid key (id 58) — removed from blocklist vs earlier draft
# NOTE: PARKING is not in cat_keys — correctly blocked
# NOTE: HARDWARE_HOME_IMPROVEMENT is not in cat_keys — use HOME_RENOVATION___MAINTENANCE
# NOTE: FAST_FOOD is not in cat_keys — use TAKEAWAY___SNACKS
# NOTE: FUEL is not in cat_keys — use GASOLINE_FUEL
# NOTE: SAVINGS is valid in DB but post-process only — LLM must not predict it
# -----------------------------------------------------------------------------
INVALID_KEY_BLOCKLIST = [
    "SPEND",
    "NON_SPEND",
    "TRANSPORT",                        # truncated — use PUBLIC_TRANSPORT, TAXI___RIDESHARE, etc.
    "ENTERTAINMENT",                    # not in cat_keys — use RECREATION, GAMBLING_LOTTERIES, etc.
    "HARDWARE_HOME_IMPROVEMENT",        # not in cat_keys — use HOME_RENOVATION___MAINTENANCE
    "PARKING",                          # not in cat_keys — use AUTOMOTIVE or TRANSPORT sub-keys
    "FINANCIAL_SERVICES",               # not in cat_keys
    "BANKING",                          # not in cat_keys
    "FAST_FOOD",                        # not in cat_keys — use TAKEAWAY___SNACKS
    "FUEL",                             # not in cat_keys — use GASOLINE_FUEL
    "SAVINGS",                          # valid in DB but assigned by post-process only
    "TRANSFER",                         # truncated — use INTERNAL_TRANSFER, EXTERNAL_TRANSFER_IN/OUT
    "FEES",                             # truncated — use specific fee keys
    "INSURANCE",                        # truncated — use INSURANCE_GENERAL / INSURANCE_MEDICAL / INSURANCE_OTHER
]

# -----------------------------------------------------------------------------
# 5. MERCHANT → CATEGORY OVERRIDES
# Known failure cases from Run 1 — injected into system prompt as guardrails.
# -----------------------------------------------------------------------------
MERCHANT_OVERRIDES = {
    "Bunnings":          "HOME_RENOVATION___MAINTENANCE",   # never HARDWARE_HOME_IMPROVEMENT
    "Chemist Warehouse": "HEALTHCARE_MEDICAL",
    "Priceline":         "HEALTHCARE_MEDICAL",
    "Terry White":       "HEALTHCARE_MEDICAL",
    "Amcal":             "HEALTHCARE_MEDICAL",
    "Woolworths":        "GROCERIES",
    "Coles":             "GROCERIES",
    "Aldi":              "GROCERIES",
    "IGA":               "GROCERIES",
    "McDonald's":        "TAKEAWAY___SNACKS",               # corrected: was FAST_FOOD
    "KFC":               "TAKEAWAY___SNACKS",
    "Subway":            "TAKEAWAY___SNACKS",
    "Hungry Jack's":     "TAKEAWAY___SNACKS",
}

# -----------------------------------------------------------------------------
# 6. KEYWORD → CATEGORY OVERRIDES
# Applied to original_description before LLM reasoning.
# -----------------------------------------------------------------------------
KEYWORD_OVERRIDES = {
    "CASHBACK":      "REWARDS",
    "FLYBUYS":       "REWARDS",
    "QANTAS POINTS": "REWARDS",
}

# -----------------------------------------------------------------------------
# 7. DISAMBIGUATION RULES
# Injected into system prompt to resolve known boundary ambiguities.
# -----------------------------------------------------------------------------
DISAMBIGUATION_RULES = {
    "BAR vs RESTAURANT":    "If venue name contains Bar, Hotel, Pub, Tavern → BAR",
    "CAFE vs RESTAURANT":   "If coffee chain or café name → CAFE",
    "INSURANCE":            "Use INSURANCE_GENERAL unless clearly life/income protection → INSURANCE_OTHER",
    "CABLE vs UTILITIES":   "Foxtel, NBN, internet → CABLE_SATELLITE_TELECOM, not UTILITIES. Gas/electricity/water → UTILITIES",
    "REFUNDS":              "Refund WITH merchant present → REFUNDS_ADJUSTMENTS (spend). Refund with NO merchant → REFUNDS_ADJUSTMENTS (non-spend)",
    "SAVINGS vs TRANSFER":  "Internal transfers to/from savings accounts → INTERNAL_TRANSFER, never SAVINGS",
    "BNPL":                 "Afterpay, Zip, Klarna, Humm, Laybuy → BNPL",
    "PAY_ON_DEMAND":        "Earnd, Beforepay, WagePay → PAY_ON_DEMAND",
    "REDRAW":               (
        "REDRAW PROCEEDS / LOAN REDRAW → "
        "MORTGAGE if account_type in {17,18,19,20,21,24}; "
        "LOAN if account_type in {22,23,25,26,42,45}"
    ),
    "UNCATEGORISED":        "Use UNCATEGORISED only as a genuine last resort when no other key fits. Attempt categorisation first.",
}

# -----------------------------------------------------------------------------
# 8. PROVIDER DATA QUALITY NOTES
# Injected into system prompt to help LLM navigate provider-specific quirks.
# -----------------------------------------------------------------------------
PROVIDER_NOTES = {
    "MACQUARIE":   "transaction_type is unreliable (90% in type 3/4). Reason from description. 'To linked account' → INTERNAL_TRANSFER. 'From [payer] - Funds Transfer' → EXTERNAL_TRANSFER_IN.",
    "UP":          "transaction_types 3+4 are internal transfers; type 5 = EXTERNAL_TRANSFER_IN/OUT by amount sign.",
    "ANZ":         "ANZ Plus has merchant enrichment — trust merchant_name.",
    "CBA":         "'Transfer from CBA Netbank' is usually salary → EXTERNAL_TRANSFER_IN.",
    "P&N":         "transaction_type=3 can contain spend transactions — rely on description.",
    "ST GEORGE":   "All spend transactions appear in transaction_type=7 — rely on description/merchant.",
    "AMP":         "transaction_type unreliable — use description.",
    "BANKWEST":    "transaction_type=6 includes mixed spend/non-spend — use description.",
}

# -----------------------------------------------------------------------------
# 9. CONFIDENCE LEVEL DEFINITIONS
# -----------------------------------------------------------------------------
CONFIDENCE_DEFINITIONS = {
    "high":   "At least one strong signal: biller_category, mcc_category, known merchant name, or unambiguous keyword match.",
    "medium": "Signals present but partial, conflicting, or indirect. Reasonable inference but some uncertainty.",
    "low":    "Minimal or no signals. Best guess from limited context.",
}

# -----------------------------------------------------------------------------
# 10. FLAG TYPES
# -----------------------------------------------------------------------------
FLAG_TYPES = [
    "taxonomy_gap",             # LLM wants a key that doesn't exist in cat_keys
    "rule_conflict",            # Pre-filter hint contradicts LLM's own assessment
    "ambiguous_boundary",       # Genuine ambiguity between two valid keys
    "ground_truth_suspicion",   # LLM suspects the ground truth label may be wrong
]

# -----------------------------------------------------------------------------
# 11. FEW-SHOT EXAMPLE TRANSACTION IDS
# Excluded from stratified sample to prevent leakage.
# Populate after selecting examples from enrichment_results.csv.
# -----------------------------------------------------------------------------
FEW_SHOT_TRANSACTION_IDS: set[str] = set()  # e.g. {"txn_001", "txn_042", ...}

# -----------------------------------------------------------------------------
# 12. RULES FILE LOADING
# Section 3 (issues analysis) stripped at load time — not suitable for injection.
# -----------------------------------------------------------------------------
RULES_FILE       = "rules_sonnet-3.5_20260121.md"
RULES_STRIP_FROM = "# 3. Analysis"          # Everything from here onwards excluded

# -----------------------------------------------------------------------------
# 13. ASSET & OUTPUT PATHS
# -----------------------------------------------------------------------------
from pathlib import Path

ASSET_DIR  = Path("assets")
OUTPUT_DIR = Path("outputs")
DATA_DIR   = Path("data")