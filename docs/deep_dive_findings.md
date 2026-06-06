# 📊 Deep Dive: Macroeconomic Risk & Model Evaluation

This document serves as the extended technical appendix to the Enterprise Credit Portfolio Governance engine. It details the specific data governance yields, SQL-derived macroeconomic insights, and the mathematical rationale behind the machine learning classifier.

---

## 1. Data Governance & Pipeline Yield 

Commercial ledger data frequently contains critical entry errors, such as null disbursement dates or mathematically impossible loan guarantees. The `gatekeeper.py` pipeline acts as a strict automated firewall.

### Pipeline Yield Metrics
* **Total Raw Ingestion:** 890,453 records
* **Passed Validation (Clean):** 447,987 records
* **Quarantined (Malformed):** 442,466 records
* **Pipeline Yield Rate:** **50.3%**

*Business Impact:* By intercepting over 442,000 malformed rows *before* they enter the PostgreSQL warehouse, we prevent downstream executive dashboards from displaying artificially inflated or corrupted portfolio balances.

---

## 2. Macroeconomic Sector Analysis (SQL Aggregations)

Using advanced Common Table Expressions (CTEs) within PostgreSQL, the pristine data was joined with NAICS (North American Industry Classification System) dimensional tables to identify systemic risk across business sectors.

### Highest Risk Exposure Sectors
The analysis revealed that certain industries are fundamentally over-leveraged, leading to disproportionate default rates. The baseline default rate for the entire portfolio was **21.8%**, but the top three sectors far exceeded this average:

| NAICS Code | Industry Sector | Total Loans | Charge-Off Rate (Default) |
| :--- | :--- | :--- | :--- |
| **52** | Finance and Insurance | 9,451 | **33.69%** |
| **53** | Real Estate, Rental and Leasing | 13,248 | **32.86%** |
| **48-49** | Transportation and Warehousing | 22,810 | **29.56%** |

*Strategic Recommendation:* The portfolio is heavily exposed to the Finance and Real Estate sectors. Tightening credit policies, reducing exposure limits, or requiring higher collateral for NAICS codes starting with 52 and 53 will organically lower the aggregate portfolio risk.

---

## 3. Predictive Modeling Evaluation (Logistic Regression)

The ultimate goal of the machine learning pipeline is to predict the `ChargeOff` probability of a loan *prior* to disbursement. 

### The Imbalance Reality & The Recall Strategy
The baseline dataset exhibited a significant class imbalance (78.1% Paid vs. 21.8% Default). In commercial lending, classification models must weigh the asymmetric cost of errors:
* **False Positive:** Predicting a default when the client would have paid. (Cost: Lost interest margin).
* **False Negative:** Predicting a successful payoff when the client actually defaults. (Cost: **Catastrophic loss of principal capital**).

Because capital preservation is paramount, the Logistic Regression model was optimized using `class_weight='balanced'` to prioritize **Recall** (catching defaults) over pure Accuracy.

### Model Performance (Test Set)
* **Final ROC-AUC Score:** **0.8193**
* **Default Identification (Recall):** **79.0%** ### The Confusion Matrix
Out of 91,138 test cases, the model achieved the following distribution:
* **True Negatives (Correctly predicted Paid):** 50,501
* **True Positives (Correctly predicted Default):** 15,717
* **False Positives (Predicted Default, actually Paid):** 20,740
* **False Negatives (Predicted Paid, actually Default):** 4,180

*Insight:* The model successfully intercepted 15,717 defaults that would have otherwise resulted in severe capital destruction. While the False Positive count increased, sacrificing potential interest margin is mathematically preferable to losing the core principal.

---

## 4. Feature Importance (Top Drivers of Default)

By extracting the coefficients from the Logistic Regression model, we identified the three variables that most heavily influence the probability of a commercial loan default:

1. **`term_months` (Coefficient: -1.93):** The duration of the loan was the single most powerful predictor. 
2. **`is_revolving_line` (Coefficient: -0.44):** The structure of the credit facility (revolving vs. fixed term) significantly altered repayment behaviors.
3. **`sba_guarantee_ratio` (Coefficient: -0.35):** Loans with a higher federal backstop displayed different risk profiles, likely due to altered bank underwriting standards when principal is federally insured.

---
*Note: This architecture is a continuous deployment. Future iterations will explore integrating XGBoost for non-linear feature relationships to further reduce the False Positive rate without sacrificing principal protection.*