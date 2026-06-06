import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
import plotly.express as px

# --- Configuration & Security ---
st.set_page_config(page_title="Credit Risk Engine", layout="wide")
load_dotenv(dotenv_path='.env')

@st.cache_data
def load_data(query):
    """Securely fetches data from PostgreSQL and caches it to prevent reloading."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""), 
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- UI Header ---
st.title("🏦 Enterprise Credit Portfolio Governance & Risk")
st.markdown("---")

# --- Sidebar Navigation ---
view = st.sidebar.radio("Executive Views", ["1. Data Quality Scorecard", "2. Portfolio Risk Analytics"])

# ==========================================
# VIEW 1: DATA QUALITY SCORECARD
# ==========================================
if view == "1. Data Quality Scorecard":
    st.header("Pipeline Health & Governance")
    
    # Fetch live counts directly from your two tables
    clean_count = load_data("SELECT COUNT(*) as count FROM fact_credit_portfolio").iloc[0]['count']
    quarantine_count = load_data("SELECT COUNT(*) as count FROM quarantined_credit_records").iloc[0]['count']
    total_raw = clean_count + quarantine_count
    yield_rate = (clean_count / total_raw) * 100

    # KPI Layout
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Raw Rows Ingested", f"{total_raw:,}")
    col2.metric("Pristine Records Cleared", f"{clean_count:,}", "Clean Layer")
    col3.metric("Corrupted Records Quarantined", f"{quarantine_count:,}", "-Failed Checks")
    col4.metric("Pipeline Yield Rate", f"{yield_rate:.2f}%")

    st.markdown("### Quarantined Data by Error Code")
    # Fetch error distributions
    error_query = """
        SELECT error_reason_code, COUNT(*) as count 
        FROM quarantined_credit_records 
        GROUP BY error_reason_code 
        ORDER BY count DESC;
    """
    error_df = load_data(error_query)
    
    # Plotly Chart
    fig = px.bar(error_df, x='error_reason_code', y='count', 
                 title="Automated Gatekeeper Defect Routing",
                 color='error_reason_code', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# VIEW 2: RISK ANALYTICS
# ==========================================
elif view == "2. Portfolio Risk Analytics":
    st.header("Macro-Sector Default Exposure")
    
    risk_query = """
        WITH SectorRisk AS (
            SELECT 
                ds.sector_description,
                COUNT(f.loan_id) AS total_loans,
                SUM(CASE WHEN f.loan_status = 'CHGOFF' THEN 1 ELSE 0 END) AS default_count,
                SUM(f.disbursement_gross) AS total_capital_deployed
            FROM fact_credit_portfolio f
            JOIN dim_sectors ds ON f.sector_id = ds.sector_id
            GROUP BY ds.sector_description
        )
        SELECT 
            sector_description as "Industry", 
            total_loans, 
            default_count,
            ROUND((default_count::numeric / total_loans) * 100, 2) AS default_rate,
            total_capital_deployed
        FROM SectorRisk
        WHERE total_loans > 1000
        ORDER BY default_rate DESC;
    """
    risk_df = load_data(risk_query)
    
    # Highlight highest risk
    highest_risk_sector = risk_df.iloc[0]['Industry']
    highest_risk_rate = risk_df.iloc[0]['default_rate']
    
    st.error(f"⚠️ **Urgent Risk Alert:** The **{highest_risk_sector}** sector is currently exhibiting a critical default rate of **{highest_risk_rate}%**.")
    
    # Plotly Chart
    fig2 = px.bar(risk_df, x='Industry', y='default_rate', 
                  title="Historical Charge-Off Rates by Macro-Sector",
                  color='default_rate', color_continuous_scale='Reds')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("### Granular Risk Data")
    st.dataframe(risk_df.style.format({"default_rate": "{:.2f}%", "total_capital_deployed": "${:,.2f}"}))
