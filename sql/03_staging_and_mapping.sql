-- 1. Create the Staging Table to perfectly match the CSV output
DROP TABLE IF EXISTS staging_credit_data;

CREATE TABLE staging_credit_data (
    LoanNr_ChkDgt VARCHAR(50),
    Name VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(10),
    Zip VARCHAR(20),
    Bank VARCHAR(255),
    BankState VARCHAR(10),
    NAICS VARCHAR(20),
    ApprovalDate VARCHAR(50),
    ApprovalFY VARCHAR(50),
    Term INT,
    NoEmp INT,
    NewExist VARCHAR(10),
    CreateJob INT,
    RetainedJob INT,
    FranchiseCode VARCHAR(50),
    UrbanRural INT,
    RevLineCr VARCHAR(10),
    LowDoc VARCHAR(10),
    ChgOffDate VARCHAR(50),
    DisbursementDate VARCHAR(50),
    DisbursementGross NUMERIC(15, 2),
    BalanceGross NUMERIC(15, 2),
    MIS_Status VARCHAR(50),
    ChgOffPrinGr NUMERIC(15, 2),
    GrAppv NUMERIC(15, 2),
    SBA_Appv NUMERIC(15, 2),
    macro_sector_code VARCHAR(10)
);