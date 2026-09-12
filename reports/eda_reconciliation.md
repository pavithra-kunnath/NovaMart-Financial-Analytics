# Python EDA Reconciliation Report — NovaMart Retail

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 9 — Python Exploratory Data Analysis & Financial Analysis  
**Data Source:** `data/processed/fact_sales_processed.csv`  
**Execution Timestamp:** 2026-09-09T11:03:00+05:30  
**Status:** **100.000% RECONCILED & VALIDATED**  

---

## 1. Executive Summary & Purpose

This document provides formal technical reconciliation between the Python Exploratory Data Analysis (EDA) environment (`notebooks/02_eda.ipynb`, `data/processed/fact_sales_processed.csv`) and the authoritative PostgreSQL Data Warehouse baseline (`novamart_db`).

All Python EDA calculations match the database baseline down to the exact penny with **zero variance**.

---

## 2. Authoritative Reconciliation Matrix

| Financial / Operational Metric | Authoritative DWH Baseline | Python Processed EDA Result | Absolute Variance | Reconciliation Status |
| :--- | :--- | :--- | :--- | :--- |
| **`fact_sales` Total Row Count** | `970,838` rows | `970,838` rows | `0` rows | **100.000% MATCH** |
| **Unique Business Key Count** | `970,838` keys | `970,838` keys | `0` duplicates | **100.000% MATCH** |
| **Total Gross Sales** | $\$49,269,500.50$ | $\$49,269,500.50$ | $\$0.00$ | **100.000% MATCH** |
| **Total Discounts (Signed)** | $-\$2,674,327.23$ | $-\$2,674,327.23$ | $\$0.00$ | **100.000% MATCH** |
| **Total Discount Amount** | $\$2,674,327.23$ | $\$2,674,327.23$ | $\$0.00$ | **100.000% MATCH** |
| **Total Net Revenue** | $\$46,595,173.27$ | $\$46,595,173.27$ | $\$0.00$ | **100.000% MATCH** |
| **Total COGS** | $\$20,811,116.93$ | $\$20,811,116.93$ | $\$0.00$ | **100.000% MATCH** |
| **Total Gross Profit** | $\$25,784,056.34$ | $\$25,784,056.34$ | $\$0.00$ | **100.000% MATCH** |
| **Overall Gross Margin %** | $55.3363\%$ | $55.3363\%$ | $0.0000\%$ | **100.000% MATCH** |
| **Discount Rate %** | $5.4280\%$ | $5.4280\%$ | $0.0000\%$ | **100.000% MATCH** |
| **Refund Line Items Count** | $9,449$ rows | $9,449$ rows | `0` rows | **100.000% MATCH** |
| **Refund Revenue Impact** | $\$396,495.00$ | $\$396,495.00$ | $\$0.00$ | **100.000% MATCH** |
| **Total Units Moved** | $1,173,116$ units | $1,173,116$ units | `0` units | **100.000% MATCH** |
| **Distinct Header Transactions** | $585,691$ receipts | $585,691$ receipts | `0` receipts | **100.000% MATCH** |
| **Average Order Value (AOV)** | $\$79.56$ | $\$79.56$ | $\$0.00$ | **100.000% MATCH** |

---

## 3. Python Verification Assertion Log

The following automated assertion block was executed in Python against `fact_sales_processed.csv`:

```python
assert len(df) == 970838
assert df.duplicated(subset=['transaction_id', 'sku', 'event_type']).sum() == 0
assert round(df['net_sales'].sum(), 2) == 46595173.27
assert round(df['cogs'].sum(), 2) == 20811116.93
assert round(df['gross_profit'].sum(), 2) == 25784056.34
assert round((df['gross_profit'].sum() / df['net_sales'].sum()) * 100, 4) == 55.3363
assert (df['event_type'] == 'Refund').sum() == 9449
assert round(df[df['event_type'] == 'Refund']['net_sales'].abs().sum(), 2) == 396495.00
```

All 8 assertions passed with 0 exceptions.

---

## 4. Conclusion

The Python EDA environment is 100% reconciled to the PostgreSQL database baseline. All findings, figures, and charts are derived directly from the reconciled dataset with zero manual typing or fabrication.
