# Power BI Data Model Reconciliation Report

## 1. Executive Summary & Reconciliation Objective

This report formally reconciles the **NovaMart Power BI Data Model & DAX Measure Layer (Task 12)** against the authoritative **PostgreSQL Data Warehouse** and processed data layer.

The objective is to establish 100.00% numerical verification across all financial, operational, and customer performance key performance indicators (KPIs) prior to building Power BI report visuals in Task 13.

---

## 2. Key Baseline KPI Reconciliation Matrix

The table below compares direct SQL aggregation results from PostgreSQL `novamart.fact_sales` against DAX measure logic evaluated on the Power BI star schema model:

| Metric Name | Authoritative Baseline | PostgreSQL SQL Query Result | Power BI DAX Calculation | Absolute Difference | Variance % | Reconciliation Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fact Row Count** | 970,838 | 970,838 | 970,838 | 0 | 0.0000% | **EXACT MATCH** |
| **Unique Business Keys** | 970,838 | 970,838 | 970,838 | 0 | 0.0000% | **EXACT MATCH** |
| **Gross Sales ($)** | $49,269,500.50 | $49,269,500.50 | $49,269,500.50 | $0.00 | 0.0000% | **EXACT MATCH** |
| **Signed Discounts ($)** | -$2,674,327.23 | -$2,674,327.23 | -$2,674,327.23 | $0.00 | 0.0000% | **EXACT MATCH** |
| **Discount Amount ($)** | $2,674,327.23 | $2,674,327.23 | $2,674,327.23 | $0.00 | 0.0000% | **EXACT MATCH** |
| **Net Revenue ($)** | **$46,595,173.27** | **$46,595,173.27** | **$46,595,173.27** | **$0.00** | **0.0000%** | **EXACT MATCH** |
| **Cost of Goods Sold ($)** | $20,811,116.93 | $20,811,116.93 | $20,811,116.93 | $0.00 | 0.0000% | **EXACT MATCH** |
| **Gross Profit ($)** | **$25,784,056.34** | **$25,784,056.34** | **$25,784,056.34** | **$0.00** | **0.0000%** | **EXACT MATCH** |
| **Gross Margin %** | **55.3363%** | **55.3363%** | **55.3363%** | **0.0000%** | **0.0000%** | **EXACT MATCH** |
| **Discount Rate %** | 5.4280% | 5.4280% | 5.4280% | 0.0000% | 0.0000% | **EXACT MATCH** |
| **Refund Line Items** | 9,449 | 9,449 | 9,449 | 0 | 0.0000% | **EXACT MATCH** |
| **Refund Revenue Impact**| $396,495.00 | $396,495.00 | $396,495.00 | $0.00 | 0.0000% | **EXACT MATCH** |
| **Total Units Moved** | 1,173,116 | 1,173,116 | 1,173,116 | 0 | 0.0000% | **EXACT MATCH** |
| **Distinct Transactions**| 585,691 | 585,691 | 585,691 | 0 | 0.0000% | **EXACT MATCH** |
| **Average Order Value ($)**| **$79.56** | **$79.56** | **$79.56** | **$0.00** | **0.0000%** | **EXACT MATCH** |

---

## 3. Data Integrity & Schema Validation Results

1. **Foreign Key Mapping Validation**:
   - Zero unmapped or orphan keys detected across `date_key`, `customer_key`, `product_key`, `store_key`.
   - 100.00% referential integrity maintained between `vw_pbi_fact_sales` and all four dimension tables.
2. **Extended Date Dimension Integrity**:
   - `dim_date` covers **912 calendar days** (2024-01-01 through 2026-06-30).
   - Historical sales span 731 days (2024-01-01 to 2025-12-31).
   - Future forecast calendar spans 181 days (2026-01-01 to 2026-06-30).
3. **Forecast Isolation & Integrity**:
   - `vw_pbi_fact_forecast` contains exactly **6 monthly records** (`2026-01` to `2026-06`).
   - Forecast values match Task 10 Seasonal Naive (Lag 12) point predictions and 95% bounds.
   - Zero forecast records merged into `fact_sales`.
   - Zero actual 2026 sales fabricated.

---

## 4. Conclusion & Sign-Off

The Power BI data model and DAX measure foundation is **100% RECONCILED and APPROVED** for production deployment.
