-- 1. Create Dimension: Sectors
CREATE TABLE dim_sectors (
    sector_id INT PRIMARY KEY,
    naics_sector_code VARCHAR(10) NOT NULL UNIQUE,
    sector_description VARCHAR(255) NOT NULL
);

-- 2. Create Dimension: Banks
CREATE TABLE dim_banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL,
    bank_state VARCHAR(10),
    CONSTRAINT unique_bank UNIQUE (bank_name, bank_state)
);

-- 3. Create Central Fact Table: Credit Portfolio
CREATE TABLE fact_credit_portfolio (
    loan_id SERIAL PRIMARY KEY,
    loan_nr_chk VARCHAR(50) UNIQUE NOT NULL,
    borrower_name VARCHAR(255),
    borrower_city VARCHAR(100),
    borrower_state VARCHAR(10),
    borrower_zip VARCHAR(20),
    bank_id INT,
    sector_id INT,
    approval_date DATE,
    approval_fy INT,
    term_months INT,
    no_emp INT,
    new_exist INT,
    create_job INT,
    retained_job INT,
    franchise_code VARCHAR(50),
    urban_rural_code INT,
    rev_line_cr_flag CHAR(1), 
    low_doc_flag CHAR(1),
    disbursement_date DATE,
    disbursement_gross NUMERIC(15, 2),
    balance_gross NUMERIC(15, 2),
    sba_appv_amount NUMERIC(15, 2),
    loan_status VARCHAR(20), 
    chg_off_amount NUMERIC(15, 2),
    
    CONSTRAINT fk_bank FOREIGN KEY (bank_id) REFERENCES dim_banks(bank_id),
    CONSTRAINT fk_sector FOREIGN KEY (sector_id) REFERENCES dim_sectors(sector_id)
);

-- 4. Create Governance Table: Quarantined Records
CREATE TABLE quarantined_credit_records (
    quarantine_id SERIAL PRIMARY KEY,
    raw_loan_nr_chk VARCHAR(50),
    raw_borrower_name VARCHAR(255),
    raw_bank_name VARCHAR(255),
    raw_bank_state VARCHAR(10),
    raw_naics_code VARCHAR(20),
    raw_rev_line_cr VARCHAR(20),
    disbursement_gross_raw NUMERIC(15, 2),
    sba_appv_raw NUMERIC(15, 2),
    quarantine_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_reason_code VARCHAR(50),
    error_description TEXT
);