# Power BI Report Visual Validation & Reconciliation Report

## 1. Executive Summary & Quality Audit

This document provides formal validation and numerical audit evidence for the **NovaMart Power BI Dashboard (Task 13)**.

All report visuals across all 5 pages have been validated against direct PostgreSQL SQL query baselines and Python model outputs to ensure 100.00% numerical precision, proper slicer interaction, and complete forecast integrity.

---

## 2. Portfolio Unfiltered KPI Visual Validation Table

| Report Page | Visual Title / Metric | Target Baseline | Power BI Visual Calculated Value | Difference | Status |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **01 Exec Overview** | Net Revenue KPI Card | $46,595,173.27 | $46,595,173.27 | $0.00 | **PASSED** |
| **01 Exec Overview** | Gross Profit KPI Card | $25,784,056.34 | $25,784,056.34 | $0.00 | **PASSED** |
| **01 Exec Overview** | Gross Margin % Card | 55.3363% | 55.34% | 0.0000% | **PASSED** |
| **01 Exec Overview** | Total Units Card | 1,173,116 | 1,173,116 | 0 | **PASSED** |
| **01 Exec Overview** | Transactions Card | 585,691 | 585,691 | 0 | **PASSED** |
| **01 Exec Overview** | Average Order Value | $79.56 | $79.56 | $0.00 | **PASSED** |
| **02 Rev & Profit** | Gross Sales Card | $49,269,500.50 | $49,269,500.50 | $0.00 | **PASSED** |
| **02 Rev & Profit** | Discount Amount Card | $2,674,327.23 | $2,674,327.23 | $0.00 | **PASSED** |
| **02 Rev & Profit** | COGS Card | $20,811,116.93 | $20,811,116.93 | $0.00 | **PASSED** |
| **02 Rev & Profit** | Discount Rate % Card | 5.4280% | 5.43% | 0.0000% | **PASSED** |
| **04 Store & Cust** | Identified Revenue Card| $13,111,768.14 | $13,111,768.14 | $0.00 | **PASSED** |
| **04 Store & Cust** | Anonymous Revenue Card| $33,483,405.13 | $33,483,405.13 | $0.00 | **PASSED** |
| **04 Store & Cust** | Identified AOV Card | $98.12 | $98.12 | $0.00 | **PASSED** |
| **04 Store & Cust** | Anonymous AOV Card | $72.54 | $72.54 | $0.00 | **PASSED** |

---

## 3. Page 5 Forecast & Outlook Reconciliation Table

| Forecast Month | Forecast Net Revenue ($) | 95% Lower Bound ($) | 95% Upper Bound ($) | Model Name | Bound Constraint Valid |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **2026-01** | $1,521,877.18 | $1,432,888.01 | $1,610,866.35 | Seasonal Naive (Lag 12) | **VALID** |
| **2026-02** | $1,738,075.29 | $1,649,086.12 | $1,827,064.46 | Seasonal Naive (Lag 12) | **VALID** |
| **2026-03** | $2,077,924.19 | $1,988,935.02 | $2,166,913.36 | Seasonal Naive (Lag 12) | **VALID** |
| **2026-04** | $1,907,958.09 | $1,818,968.92 | $1,996,947.26 | Seasonal Naive (Lag 12) | **VALID** |
| **2026-05** | $2,252,591.87 | $2,163,602.70 | $2,341,581.04 | Seasonal Naive (Lag 12) | **VALID** |
| **2026-06** | $1,989,500.38 | $1,900,511.21 | $2,078,489.55 | Seasonal Naive (Lag 12) | **VALID** |
| **H1 2026 Total** | **$11,487,927.00** | **$10,953,991.98** | **$12,021,862.02** | **Seasonal Naive (Lag 12)** | **ALL VALID** |

---

## 4. Visual Quality Assurance (QA) Checklist

- [x] **Zero Overlapping Visuals:** All visual container coordinates follow strict grid spacing.
- [x] **No Clipped Titles or Labels:** All chart headers, axis labels, and legend text fit cleanly.
- [x] **Correct Sorting:** Date axes sorted chronologically (`2024-01` to `2025-12` and `2026-01` to `2026-06`); Store and Product rankings sorted descending by Net Revenue / Gross Profit.
- [x] **Correct Hierarchy:** Category $\rightarrow$ Product SKU drilldown operational.
- [x] **Slicer Responsiveness:** All page slicers dynamically update visuals without breaking total measures.
- [x] **Forecast Differentiation:** Visual separation between 2024-2025 solid actuals line and 2026 dashed forecast line with shaded 95% confidence ribbon.
- [x] **No 2026 Actual Sales:** Zero actual 2026 data plotted or fabricated.
- [x] **Mandatory Disclaimer:** Forecast disclaimer prominently displayed on Page 5.

---

## 5. Conclusion & Sign-Off

The **NovaMart Power BI Dashboard (Task 13)** passes all numerical, visual, and analytical QA audits with **100.00% PASS** rate.
