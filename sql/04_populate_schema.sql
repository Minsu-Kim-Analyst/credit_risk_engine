-- 1. Extract and load unique banks into the Bank Dimension
INSERT INTO dim_banks (bank_name, bank_state)
SELECT DISTINCT Bank, BankState
FROM staging_credit_data
WHERE Bank IS NOT NULL
ON CONFLICT (bank_name, bank_state) DO NOTHING;

-- 2. Load the core analytical columns into the Fact Table
INSERT INTO fact_credit_portfolio (
    loan_nr_chk, borrower_name, borrower_state, bank_id, sector_id, 
    term_months, rev_line_cr_flag, disbursement_gross, sba_appv_amount, loan_status
)
SELECT 
    s.LoanNr_ChkDgt,
    s.Name,
    s.State,
    b.bank_id,
    ds.sector_id,
    s.Term,
    s.RevLineCr,
    s.DisbursementGross,
    s.SBA_Appv,
    s.MIS_Status
FROM staging_credit_data s
-- Map the foreign keys
LEFT JOIN dim_banks b 
    ON s.Bank = b.bank_name AND s.BankState = b.bank_state
LEFT JOIN dim_sectors ds 
    ON s.macro_sector_code = ds.naics_sector_code
WHERE s.MIS_Status IN ('P I F', 'CHGOFF') -- Only keep rows with known final outcomes
ON CONFLICT (loan_nr_chk) DO NOTHING;