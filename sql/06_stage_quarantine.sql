DROP TABLE IF EXISTS staging_quarantine;

CREATE TABLE staging_quarantine (
    LoanNr_ChkDgt VARCHAR(50), Name VARCHAR(255), City VARCHAR(100), 
    State VARCHAR(10), Zip VARCHAR(20), Bank VARCHAR(255), 
    BankState VARCHAR(10), NAICS VARCHAR(50), ApprovalDate VARCHAR(50), 
    ApprovalFY VARCHAR(50), Term VARCHAR(50), NoEmp VARCHAR(50), 
    NewExist VARCHAR(50), CreateJob VARCHAR(50), RetainedJob VARCHAR(50), 
    FranchiseCode VARCHAR(50), UrbanRural VARCHAR(50), RevLineCr VARCHAR(50), 
    LowDoc VARCHAR(50), ChgOffDate VARCHAR(50), DisbursementDate VARCHAR(50), 
    DisbursementGross NUMERIC(15, 2), BalanceGross NUMERIC(15, 2), 
    MIS_Status VARCHAR(50), ChgOffPrinGr NUMERIC(15, 2), 
    GrAppv NUMERIC(15, 2), SBA_Appv NUMERIC(15, 2), 
    macro_sector_code VARCHAR(50), error_reason_code VARCHAR(50)
);