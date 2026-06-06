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
    sector_description AS "Macro Industry",
    total_loans AS "Total Loans Issued",
    default_count AS "Total Defaults",
    ROUND((default_count::numeric / total_loans) * 100, 2) AS "Default Rate (%)",
    CAST(total_capital_deployed::numeric::money AS VARCHAR) AS "Total Capital Disbursed"
FROM SectorRisk
WHERE total_loans > 1000 -- Filter out sample-size anomalies
ORDER BY "Default Rate (%)" DESC;