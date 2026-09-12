# Monthly Forecasting Data Reconciliation Report — NovaMart Retail

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 10 — Python Revenue Forecasting & Backtesting Pipeline  
**Target Variable:** Monthly Net Revenue (`net_revenue`)  
**Historical Period:** `2024-01-01` through `2025-12-31` (24 Calendar Months)  
**Execution Timestamp:** 2026-09-09T11:14:40+05:30  
**Status:** **100.000% RECONCILED & VALIDATED**  

---

## 1. Executive Summary & Reconciliation Objective

This document proves that the monthly time-series dataset (`m_df`) constructed for forecasting in `src/forecast.py` and `notebooks/03_forecasting.ipynb` reconciles with **100.000% precision** against both the processed data layer (`data/processed/fact_sales_processed.csv`) and the PostgreSQL Data Warehouse (`novamart.fact_sales`).

---

## 2. Multi-Layer Reconciliation Matrix

| Layer / Source | Row Count | Start Month | End Month | Total Net Revenue ($) | Reconciliation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Raw POS Export (`square_item_sales_detail_24mo.csv`)** | $970,838$ lines | `2024-01-01` | `2025-12-31` | $\$46,595,173.27$ | **100.000% MATCH** |
| **Staging CSV (`square_sales_staging.csv`)** | $970,838$ lines | `2024-01-01` | `2025-12-31` | $\$46,595,173.27$ | **100.000% MATCH** |
| **Processed CSV (`fact_sales_processed.csv`)** | $970,838$ lines | `2024-01-01` | `2025-12-31` | $\$46,595,173.27$ | **100.000% MATCH** |
| **PostgreSQL DWH (`novamart.fact_sales`)** | $970,838$ lines | `2024-01-01` | `2025-12-31` | $\$46,595,173.27$ | **100.000% MATCH** |
| **Monthly Forecast Dataset (`m_df`)** | $24$ months | `2024-01` | `2025-12` | $\$46,595,173.27$ | **100.000% MATCH** |

---

## 3. Monthly Net Revenue Reconciliation Table (24 Calendar Months)

| Month | Line Items Count | Unique Txns | Net Revenue ($) | Percentage of Total | Running Cumulative ($) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2024-01** | $28,659$ | $17,299$ | $\$1,385,911.59$ | $2.97\%$ | $\$1,385,911.59$ |
| **2024-02** | $34,932$ | $20,992$ | $\$1,680,416.99$ | $3.61\%$ | $\$3,066,328.58$ |
| **2024-03** | $39,469$ | $23,758$ | $\$1,921,063.06$ | $4.12\%$ | $\$4,987,391.64$ |
| **2024-04** | $38,650$ | $23,315$ | $\$1,874,251.15$ | $4.02\%$ | $\$6,861,642.79$ |
| **2024-05** | $43,007$ | $26,065$ | $\$2,070,015.23$ | $4.44\%$ | $\$8,931,658.02$ |
| **2024-06** | $39,752$ | $23,967$ | $\$1,904,552.25$ | $4.09\%$ | $\$10,836,210.27$ |
| **2024-07** | $36,191$ | $21,883$ | $\$1,738,955.14$ | $3.73\%$ | $\$12,575,165.41$ |
| **2024-08** | $40,820$ | $24,516$ | $\$2,055,164.11$ | $4.41\%$ | $\$14,630,329.52$ |
| **2024-09** | $33,334$ | $20,045$ | $\$1,626,640.31$ | $3.49\%$ | $\$16,256,969.83$ |
| **2024-10** | $35,265$ | $21,199$ | $\$1,715,950.50$ | $3.68\%$ | $\$17,972,920.33$ |
| **2024-11** | $41,234$ | $24,936$ | $\$1,953,663.04$ | $4.19\%$ | $\$19,926,583.37$ |
| **2024-12** | $60,567$ | $36,816$ | $\$2,748,743.55$ | $5.90\%$ | $\$22,675,326.92$ |
| **2025-01** | $31,330$ | $18,900$ | $\$1,521,877.18$ | $3.27\%$ | $\$24,197,204.10$ |
| **2025-02** | $36,163$ | $21,815$ | $\$1,738,075.29$ | $3.73\%$ | $\$25,935,279.39$ |
| **2025-03** | $42,769$ | $25,773$ | $\$2,077,924.19$ | $4.46\%$ | $\$28,013,203.58$ |
| **2025-04** | $39,449$ | $23,826$ | $\$1,907,958.09$ | $4.09\%$ | $\$29,921,161.67$ |
| **2025-05** | $46,850$ | $28,159$ | $\$2,252,591.87$ | $4.83\%$ | $\$32,173,753.54$ |
| **2025-06** | $41,213$ | $24,816$ | $\$1,989,500.38$ | $4.27\%$ | $\$34,163,253.92$ |
| **2025-07** | $38,826$ | $23,452$ | $\$1,863,801.17$ | $4.00\%$ | $\$36,027,055.09$ |
| **2025-08** | $43,197$ | $26,010$ | $\$2,159,331.01$ | $4.63\%$ | $\$38,186,386.10$ |
| **2025-09** | $34,432$ | $20,761$ | $\$1,660,709.11$ | $3.56\%$ | $\$39,847,095.21$ |
| **2025-10** | $37,248$ | $22,360$ | $\$1,794,402.05$ | $3.85\%$ | $\$41,641,497.26$ |
| **2025-11** | $44,355$ | $26,788$ | $\$2,093,117.53$ | $4.49\%$ | $\$43,734,614.79$ |
| **2025-12** | $63,126$ | $38,240$ | $\$2,860,558.48$ | $6.14\%$ | **$46,595,173.27** |

---

## 4. Integrity Assertions & Verification Log

The following validation checks were executed automatically:
1. **Total Revenue Check:** Sum of `net_revenue` = **$46,595,173.27** (0 variance).
2. **Month Continuity Check:** Exactly 24 unique months (`2024-01` through `2025-12`).
3. **No Duplicate Months:** 0 duplicate month strings.
4. **No Missing Months:** 24 continuous calendar months.
5. **Signed Refund Integration:** Sum of `net_sales` includes negative return amounts according to Data Contract specifications.

---

## 5. Conclusion

The monthly forecasting dataset is **100.000% reconciled and approved** for time-series backtesting and model evaluation.
