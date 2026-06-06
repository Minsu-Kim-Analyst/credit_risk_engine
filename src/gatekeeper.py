import pandas as pd
import numpy as np
import warnings

# Suppress pandas chained assignment warnings for clean terminal output
warnings.filterwarnings('ignore')

# --- Enterprise Path Configuration ---
RAW_DATA_PATH = '../data/raw/SBAnational.csv'
CLEAN_DATA_PATH = '../data/clean_credit_portfolio.csv'
QUARANTINE_PATH = '../data/quarantine/quarantined_records.csv'

def clean_currency(x):
    """Converts messy currency strings (e.g., '$1,000.00') into clean floats."""
    if pd.isna(x):
        return np.nan
    if isinstance(x, str):
        x = x.replace('$', '').replace(',', '').strip()
        try:
            return float(x)
        except ValueError:
            return np.nan
    return float(x)

def run_gatekeeper():
    print("Initializing Enterprise Data Governance Pipeline...\n")

    # 1. Ingestion
    print(f"[1/5] Ingesting raw ledger from {RAW_DATA_PATH}...")
    df = pd.read_csv(RAW_DATA_PATH, low_memory=False)
    initial_count = len(df)
    
    quarantined_dfs = [] # A bin to catch all failing records

    # 2. Financial Type Standardization
    print("[2/5] Standardizing financial strings into numeric formats...")
    currency_cols = ['DisbursementGross', 'BalanceGross', 'SBA_Appv', 'GrAppv', 'ChgOffPrinGr']
    for col in currency_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_currency)

    # 3. Structural Mapping (NAICS)
    print("[3/5] Extracting 2-digit macro-sector codes from NAICS...")
    # Fill NA and convert to string, then slice the first 2 characters
    df['NAICS'] = df['NAICS'].fillna(0).astype(int).astype(str)
    df['macro_sector_code'] = df['NAICS'].str[:2]

    # 4. Enforcing Business Rules & Quarantining
    print("[4/5] Enforcing integrity rules and quarantining corrupted data...")
    
    # Rule A: Missing Critical Markers
    missing_mask = df['BankState'].isna() | (df['NAICS'] == '0')
    q_missing = df[missing_mask].copy()
    q_missing['error_reason_code'] = 'ERR_MISSING_CRITICAL_MARKERS'
    quarantined_dfs.append(q_missing)
    df_clean = df[~missing_mask].copy()

    # Rule B: Revolving Line of Credit Standardization ('Y' or 'N')
    invalid_rev_mask = ~df_clean['RevLineCr'].isin(['Y', 'N'])
    q_rev = df_clean[invalid_rev_mask].copy()
    q_rev['error_reason_code'] = 'ERR_CORRUPT_REVFLAG'
    quarantined_dfs.append(q_rev)
    df_clean = df_clean[~invalid_rev_mask].copy()

    # Rule C: Logical Financial Impossibility
    logical_error_mask = df_clean['SBA_Appv'] > df_clean['DisbursementGross']
    q_logic = df_clean[logical_error_mask].copy()
    q_logic['error_reason_code'] = 'ERR_APPV_EXCEEDS_GROSS'
    quarantined_dfs.append(q_logic)
    df_clean = df_clean[~logical_error_mask].copy()

    # 5. Routing & Export
    print("[5/5] Routing records to respective storage layers...")
    if quarantined_dfs:
        final_quarantine_df = pd.concat(quarantined_dfs, ignore_index=True)
        final_quarantine_df.to_csv(QUARANTINE_PATH, index=False)
        print(f" -> Pushed {len(final_quarantine_df):,} corrupted records to Quarantine Layer.")

    df_clean.to_csv(CLEAN_DATA_PATH, index=False)
    print(f" -> Pushed {len(df_clean):,} validated records to Clean Layer.")

    # --- Executive Summary ---
    print("\n===========================================")
    print("      PIPELINE EXECUTION SUMMARY")
    print("===========================================")
    print(f"Total Raw Records Ingested  : {initial_count:,}")
    print(f"Records Quarantined         : {initial_count - len(df_clean):,}")
    print(f"Records Cleared for DB Load : {len(df_clean):,}")
    print(f"Data Yield Rate             : {(len(df_clean)/initial_count)*100:.2f}%")
    print("===========================================")

if __name__ == "__main__":
    run_gatekeeper()
