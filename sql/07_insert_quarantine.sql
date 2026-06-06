INSERT INTO quarantined_credit_records (
    raw_loan_nr_chk, raw_borrower_name, raw_bank_name, raw_bank_state, 
    raw_naics_code, raw_rev_line_cr, disbursement_gross_raw, 
    sba_appv_raw, error_reason_code
)
SELECT 
    LoanNr_ChkDgt, Name, Bank, BankState, 
    NAICS, RevLineCr, DisbursementGross, 
    SBA_Appv, error_reason_code
FROM staging_quarantine;