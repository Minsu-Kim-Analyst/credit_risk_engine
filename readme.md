# 🏦 Enterprise Credit Portfolio Governance & Risk Engine

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.0+-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)

An end-to-end data architecture and predictive analytics engine built to assess commercial credit risk, enforce data governance, and predict commercial loan defaults. 

## 📌 Executive Summary
Commercial lending data is notoriously prone to human error, missing fields, and logical impossibilities. This project bridges the gap between Data Engineering and Data Science by constructing a robust ETL governance pipeline that quarantines corrupted ledger entries *before* they enter the data warehouse. 

Using the pristine data, a machine learning classification model is deployed to predict default probabilities, all surfaced via an interactive executive web dashboard.

### 📊 Key Business Outcomes:
* **Risk Mitigation:** Successfully identified **79%** of historical loan defaults by tuning a Logistic Regression model to prioritize recall (ROC-AUC: 0.82), protecting against catastrophic principal loss.
* **Data Governance:** Intercepted and quarantined **442,000+** logically invalid financial records (50.3% yield rate) to prevent downstream reporting corruption.
* **Strategic Insight:** Engineered SQL Common Table Expressions (CTEs) to map macroeconomic exposure, revealing a severe **33.69% charge-off rate** within the highly leveraged Finance & Insurance sector.

---

## 🏗 System Architecture & Directory

```text
credit_risk_project/
├── .env                       # Local database credentials (Ignored by Git)
├── .gitignore                 # Enterprise security and system file exclusions
├── README.md                  # Project documentation and setup guide
├── requirements.txt           # Strict version-pinned Python dependencies
├── assets/                    # Rendered UI components for repository documentation
│   ├── risk_map.png           # Portfolio risk geolocation chart
│   └── scorecard.png          # Data governance pipeline yield visualization
├── dashboards/                # Front-End Executive Analytics
│   └── portfolio_risk.py      # Streamlit production dashboard application
├── data/                      # Local data storage (Ignored by Git for security)
│   ├── clean/                 # Validated rows processed by Python pipeline
│   ├── quarantine/            # Corrupted rows isolated with exact error codes
│   └── raw/                   # Raw federal ledger records expecting CSV injection
├── docs/                      # Technical Appendices & Reporting
│   └── deep_dive_findings.md  # Comprehensive model evaluation & SQL audit findings
├── models/
│   └── notebooks/             # Model Development Environment
│       └── credit_scoring_train.ipynb # Feature engineering & model training pipeline
├── scripts/                   # Automated Environment Utilities
│   └── generate_requirements.py # Custom Python script for strict dependency tracking
├── sql/                       # Relational Database Architecture & ELT Scripts
│   ├── 01_ddl_schema.sql      # Star Schema production table definitions
│   ├── naics_mapping.sql      # Dimensional mapping for macro-sectors
│   ├── staging_and_mapping.sql # Raw data transformation and alignment
│   ├── populate_schema.sql    # Production data loading execution
│   ├── risk_analysis.sql      # Advanced analytical CTE portfolio queries
│   ├── stage_quarantine.sql   # Data isolation layer infrastructure
│   └── insert_quarantine.sql  # Automated routing for corrupted records
└── src/                       # Core Python ETL & Governance Engine
    ├── gatekeeper.py          # Data validation firewall pipeline
    └── sba_profiler.py        # Automated schema and missing-value profiler
```

---

## 🛠 Core Features & Tech Stack

### 1. Automated Data Governance Pipeline (`gatekeeper.py`)
* **Tech:** Python, Pandas, Numpy
* **Function:** Ingests raw CSV ledgers, standardizes financial string objects to numeric floats, and enforces strict business logic (e.g., *Guarantee Amount cannot exceed Total Disbursement*). Routes clean data to the warehouse and pushes failed rows to a quarantine layer with attached `error_reason_codes`.

### 2. Relational Data Warehouse (`PostgreSQL`)
* **Tech:** PostgreSQL, SQL (DDL, DML, CTEs)
* **Function:** A normalized Star Schema architecture built via command-line ELT. Foreign keys map dimensional macro-sectors (NAICS codes) and banking entities to the central loan fact table.

### 3. Predictive Risk Modeling (`Scikit-Learn`)
* **Tech:** Python, Scikit-Learn, Jupyter
* **Function:** Engineered financial exposure features (e.g., `sba_guarantee_ratio`) and trained a class-weight-balanced Logistic Regression model to forecast charge-offs before capital is deployed.

### 4. Executive BI Dashboard (`Streamlit`)
* **Tech:** Streamlit, Plotly, Psycopg2, Python-dotenv
* **Function:** A full-stack web application securely querying the local PostgreSQL database to render real-time pipeline yield metrics, quarantine distribution charts, and geographic/sector risk alerts.

---

## 📸 Dashboard Previews

> **Data Quality Scorecard:** Visualizing pipeline yield rates and quarantine error distributions.
> <br>![Data Quality Scorecard](assets/scorecard.png) 

> **Portfolio Risk Analytics:** Highlighting macro-sector default exposure.
> <br>![Portfolio Risk Analytics](assets/risk_map.png)

---

## 🚀 Local Deployment & Setup

> **⚠️ Data Privacy & Compliance Notice**
> The raw 890,000-row commercial loan dataset and the local `.env` database credentials have been strictly excluded from this repository via `.gitignore` to comply with financial data privacy standards and GitHub storage limits. The source code is provided for architectural demonstration. To run the pipeline locally, place a compatible CSV into the `data/raw/` directory matching the schema defined in `sql/01_ddl_schema.sql`.

**1. Clone the repository**
```bash
git clone [https://github.com/Minsu-Kim-Analyst/credit_risk_engine.git](https://github.com/Minsu-Kim-Analyst/credit_risk_engine.git)
cd credit_risk_engine
```

**2. Establish the isolated virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Freeze and audit dependencies automatically**
```bash
python scripts/generate_requirements.py
pip install -r requirements.txt
```

**4. Configure secure environment variables**
Create a `.env` file in the root directory to map your local PostgreSQL instance:
```text
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=credit_risk_db
```

**5. Deploy the full-stack dashboard**
```bash
streamlit run dashboards/portfolio_risk.py
```

---
*Developed as a comprehensive Business Analytics and Data Engineering portfolio initiative.*