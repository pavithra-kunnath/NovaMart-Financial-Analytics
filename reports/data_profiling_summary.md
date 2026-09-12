# Data Profiling & Exploratory Quality Analysis Summary

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 4 — Data Profiling & Exploratory Quality Analysis  
**Target Dataset:** `data/raw/square_item_sales_detail_24mo.csv`  

---

## 1. Executive Summary

This report presents a thorough, non-destructive exploratory data analysis and quality profile of NovaMart's 24-month Point-of-Sale (POS) dataset (970,838 transaction line records). 

Key findings include:
- **Zero Structural Anomalies**: 100% pass rate on composite business key uniqueness (`Transaction ID + SKU + Event Type`) across all 970,838 rows.
- **100% Financial Reconciliation**: 0 arithmetic discrepancies found across all 970,838 rows for Gross Sales, Net Sales, COGS, and Gross Profit equations.
- **Continuous 24-Month Time Series**: Unbroken daily transaction coverage from `2024-01-01` through `2025-12-31`.
- **Customer Anonymous Segment**: 65.34% of transaction lines are guest/walk-in purchases with `Customer ID = NULL`.

---

## 2. Dataset Size & Basic Profile

- **Total Rows:** 970,838
- **Total Columns:** 23
- **In-Memory Size:** 857.55 MB

### Field Summary Table

| Column | Data Type | Non-Null Count | Null Count | Null % | Unique Count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Date` | `object` | 970,838 | 0 | 0.00% | 729 |
| `Time` | `object` | 970,838 | 0 | 0.00% | 720 |
| `Time Zone` | `object` | 970,838 | 0 | 0.00% | 1 |
| `Category` | `object` | 970,838 | 0 | 0.00% | 6 |
| `Item` | `object` | 970,838 | 0 | 0.00% | 32 |
| `Qty` | `int64` | 970,838 | 0 | 0.00% | 4 |
| `Price Point Name` | `object` | 970,838 | 0 | 0.00% | 25 |
| `SKU` | `object` | 970,838 | 0 | 0.00% | 67 |
| `Unit Price` | `float64` | 970,838 | 0 | 0.00% | 31 |
| `Gross Sales` | `float64` | 970,838 | 0 | 0.00% | 107 |
| `Discounts` | `float64` | 970,838 | 0 | 0.00% | 242 |
| `Net Sales` | `float64` | 970,838 | 0 | 0.00% | 394 |
| `Tax` | `float64` | 970,838 | 0 | 0.00% | 378 |
| `Total Collected` | `float64` | 970,838 | 0 | 0.00% | 394 |
| `Transaction ID` | `object` | 970,838 | 0 | 0.00% | 585,691 |
| `Payment Method` | `object` | 970,838 | 0 | 0.00% | 3 |
| `Device Name` | `object` | 970,838 | 0 | 0.00% | 3 |
| `Location` | `object` | 970,838 | 0 | 0.00% | 30 |
| `Customer ID` | `object` | 336,445 | 634,393 | 65.34% | 20,000 |
| `Event Type` | `object` | 970,838 | 0 | 0.00% | 2 |
| `Unit Cost` | `float64` | 970,838 | 0 | 0.00% | 36 |
| `Gross Profit` | `float64` | 970,838 | 0 | 0.00% | 559 |

---

## 3. Data Completeness

- **High Missingness Column:** `Customer ID` has **634,393 missing values (65.34%)**. This represents anonymous guest/walk-in POS transactions.
- **100% Complete Columns:** All remaining 21 columns (`Date`, `Time`, `Category`, `Item`, `Qty`, `SKU`, `Unit Price`, `Gross Sales`, `Discounts`, `Net Sales`, `Tax`, `Total Collected`, `Transaction ID`, `Payment Method`, `Device Name`, `Location`, `Event Type`, `Unit Cost`, `Gross Profit`) have **0 nulls (0.00% missing)**.
- **Empty Columns:** None.

---

## 4. Identifier Profile & Business Key Verification

| Identifier Field | Unique Values | Null Count | String Length Range | Suspicious Patterns Found |
| :--- | :--- | :--- | :--- | :--- |
| `Transaction ID` | 585,691 | 0 | 10 chars (`TXN...`) | None |
| `SKU` | 67 | 0 | 7 chars (`SQ-10..`) | None |
| `Customer ID` | 19,999 | 634,393 | 9 chars (`CUST..`) | None |
| `Event Type` | 2 | 0 | 7–7 chars | None (`Payment`, `Refund` only) |
| `Location` | 30 | 0 | 17–25 chars | Combined Store + City string |

### Business Key Uniqueness Verification
- **Candidate Key:** `Transaction ID` + `SKU` + `Event Type`
- **Total Tested Rows:** 970,838
- **Unique Combinations:** 970,838
- **Duplicates Found:** **0**

---

## 5. Transaction Line-Item Analysis

- **Unique Transactions:** 585,691
- **Total Line Items:** 970,838
- **Average Lines per Transaction:** 1.66
- **Min Lines per Transaction:** 1
- **Max Lines per Transaction:** 4

---

## 6. Date & Time Profile

- **Minimum Date:** `2024-01-01`
- **Maximum Date:** `2025-12-31`
- **Unique Dates:** 729 (729 active sales days; 2 store-closed days in calendar)
- **Invalid / Unparseable Dates:** 0
- **Calendar Months Covered:** 24 full months (`2024-01` through `2025-12`)
- **Peak Volume Date:** `2025-12-20` (2,748 transaction lines)

---

## 7. Financial Metric Profile

### Percentile Distribution ($ USD)

| Metric | Min | 1st % | 25th % | Median | Mean | 75th % | 99th % | Max | Std |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Unit Price` | 9.50 | 9.50 | 21.00 | 35.00 | 42.00 | 59.00 | 129.00 | 129.00 | 26.42 |
| `Gross Sales` | -129.00 | 9.50 | 22.00 | 40.00 | 50.75 | 68.00 | 178.00 | 387.00 | 41.41 |
| `Discounts` | -154.80 | -26.70 | -3.50 | 0.00 | -2.75 | 0.00 | 0.00 | 0.00 | 5.96 |
| `Net Sales` | -129.00 | 6.65 | 21.00 | 39.00 | 47.99 | 60.00 | 178.00 | 387.00 | 39.64 |
| `Tax` | -10.64 | 0.55 | 1.73 | 3.22 | 3.96 | 4.95 | 14.68 | 31.93 | 3.27 |
| `Total Collected` | -139.64 | 7.20 | 22.73 | 42.22 | 51.95 | 64.95 | 192.68 | 418.93 | 42.91 |
| `Unit Cost` | 2.66 | 2.66 | 7.04 | 12.60 | 17.74 | 28.32 | 67.08 | 67.08 | 14.47 |
| `Gross Profit` | -61.92 | 3.60 | 13.65 | 22.40 | 26.56 | 31.60 | 93.60 | 185.76 | 19.47 |

---

## 8. Financial Reconciliation Results

| Reconciliation Equation | Total Tested | Passing | Failing | Pass % | Max Abs Diff | Typical Diff | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Gross Sales == Qty * Unit Price` | 970,838 | 970,838 | 0 | 100.00% | $0.00 | $0.00 | **PASS** |
| `Net Sales == Gross Sales + Discounts` | 970,838 | 970,838 | 0 | 100.00% | $0.00 | $0.00 | **PASS** |
| `Gross Profit == Net Sales - COGS` | 970,838 | 970,838 | 0 | 100.00% | $0.00 | $0.00 | **PASS** |

---

## 9. Discount Analysis

- **Discounted Line Items:** 312,053 (32.14% of all lines)
- **Total Discount Value:** $2,674,327.23
- **Average Discount Amount:** $8.57
- **Median Discount Amount:** $6.30
- **Maximum Line Discount:** $154.80

---

## 10. Refund / Return Profiling

- **Payment Lines:** 961,389 (99.03%)
- **Refund Lines:** 9,449 (0.97%)
- **Total Refunded Quantity:** 9,449 units
- **Total Refunded Net Sales:** $396,495.00
- **Total Refunded Gross Profit:** $228,862.70

---

## 11. Customer Profiling

- **Identified Customer Transactions:** 336,445 lines (34.66%) across 19,999 unique customers.
- **Anonymous / Guest Transactions:** 634,393 lines (65.34%).
- **Identified Customer AOV:** $81.62
- **Average Purchase Frequency:** 10.08 transactions per customer.

---

## 12. Monthly Financial Summary Table

| Month | Line Items | Unique Txns | Quantity | Gross Sales | Discounts | Net Sales | COGS | Gross Profit | Gross Margin % | Refund Net | Refund Rate % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2024-01 | 28,659 | 17,299 | 34,606 | $1,452,966.00 | $-67,054.41 | $1,385,911.59 | $613,464.60 | $772,446.99 | 55.74% | $-11,817.00 | 1.04% |
| 2024-02 | 34,932 | 20,992 | 42,273 | $1,759,743.50 | $-79,326.51 | $1,680,416.99 | $741,588.20 | $938,828.79 | 55.87% | $-11,619.50 | 0.78% |
| 2024-03 | 39,469 | 23,758 | 47,823 | $2,011,709.00 | $-90,645.94 | $1,921,063.06 | $850,222.19 | $1,070,840.87 | 55.74% | $-13,535.00 | 0.81% |
| 2024-04 | 38,650 | 23,315 | 46,799 | $1,962,715.00 | $-88,463.85 | $1,874,251.15 | $829,547.72 | $1,044,703.43 | 55.74% | $-14,772.50 | 0.90% |
| 2024-05 | 43,007 | 26,065 | 52,045 | $2,171,563.00 | $-101,547.77 | $2,070,015.23 | $915,212.82 | $1,154,802.41 | 55.79% | $-14,804.50 | 0.88% |
| 2024-06 | 39,752 | 23,967 | 48,036 | $1,995,274.50 | $-90,722.25 | $1,904,552.25 | $839,681.14 | $1,064,871.11 | 55.91% | $-15,251.50 | 0.95% |
| 2024-07 | 36,191 | 21,883 | 43,797 | $1,825,081.00 | $-86,125.86 | $1,738,955.14 | $769,144.00 | $969,811.14 | 55.77% | $-12,372.00 | 0.82% |
| 2024-08 | 40,820 | 24,516 | 49,582 | $2,154,512.50 | $-99,348.39 | $2,055,164.11 | $915,915.46 | $1,139,248.65 | 55.43% | $-15,708.00 | 0.90% |
| 2024-09 | 33,334 | 20,045 | 40,330 | $1,704,072.00 | $-77,431.69 | $1,626,640.31 | $720,989.87 | $905,650.44 | 55.68% | $-13,861.50 | 0.90% |
| 2024-10 | 35,265 | 21,199 | 42,706 | $1,798,829.50 | $-82,879.00 | $1,715,950.50 | $760,271.43 | $955,679.07 | 55.69% | $-12,233.50 | 0.86% |
| 2024-11 | 41,234 | 24,936 | 49,718 | $2,092,643.00 | $-138,979.96 | $1,953,663.04 | $885,849.46 | $1,067,813.58 | 54.66% | $-14,656.50 | 0.89% |
| 2024-12 | 60,567 | 36,816 | 72,752 | $3,050,661.00 | $-301,917.45 | $2,748,743.55 | $1,288,481.60 | $1,460,261.95 | 53.12% | $-38,021.00 | 1.48% |
| 2025-01 | 31,330 | 18,900 | 37,901 | $1,594,161.50 | $-72,284.32 | $1,521,877.18 | $674,372.63 | $847,504.55 | 55.69% | $-14,047.00 | 1.09% |
| 2025-02 | 36,163 | 21,815 | 43,642 | $1,818,146.00 | $-80,070.71 | $1,738,075.29 | $765,331.03 | $972,744.26 | 55.97% | $-15,244.00 | 0.95% |
| 2025-03 | 42,769 | 25,773 | 51,762 | $2,176,516.50 | $-98,592.31 | $2,077,924.19 | $919,694.72 | $1,158,229.47 | 55.74% | $-17,677.50 | 0.95% |
| 2025-04 | 39,449 | 23,826 | 47,818 | $1,997,989.50 | $-90,031.41 | $1,907,958.09 | $842,931.92 | $1,065,026.17 | 55.82% | $-12,604.50 | 0.82% |
| 2025-05 | 46,850 | 28,159 | 56,601 | $2,361,003.00 | $-108,411.13 | $2,252,591.87 | $995,009.25 | $1,257,582.62 | 55.83% | $-18,395.50 | 0.93% |
| 2025-06 | 41,213 | 24,816 | 49,952 | $2,081,866.50 | $-92,366.12 | $1,989,500.38 | $877,428.13 | $1,112,072.25 | 55.90% | $-14,565.50 | 0.86% |
| 2025-07 | 38,826 | 23,452 | 46,952 | $1,956,701.50 | $-92,900.33 | $1,863,801.17 | $824,365.83 | $1,039,435.34 | 55.77% | $-12,918.00 | 0.81% |
| 2025-08 | 43,197 | 26,010 | 52,137 | $2,260,978.50 | $-101,647.49 | $2,159,331.01 | $961,439.45 | $1,197,891.56 | 55.48% | $-18,034.50 | 0.95% |
| 2025-09 | 34,432 | 20,761 | 41,624 | $1,741,790.50 | $-81,081.39 | $1,660,709.11 | $735,086.67 | $925,622.44 | 55.74% | $-13,702.00 | 0.93% |
| 2025-10 | 37,248 | 22,360 | 45,024 | $1,880,125.00 | $-85,722.95 | $1,794,402.05 | $792,871.13 | $1,001,530.92 | 55.81% | $-13,771.00 | 0.89% |
| 2025-11 | 44,355 | 26,788 | 53,829 | $2,245,703.00 | $-152,585.47 | $2,093,117.53 | $949,758.84 | $1,143,358.69 | 54.62% | $-16,232.50 | 0.87% |
| 2025-12 | 63,126 | 38,240 | 75,407 | $3,174,749.00 | $-314,190.52 | $2,860,558.48 | $1,342,458.84 | $1,518,099.64 | 53.07% | $-40,650.50 | 1.52% |

---

## 13. Data Quality Findings Table

| Issue Description | Severity | Affected Rows | Evidence | Recommended Treatment |
| :--- | :--- | :--- | :--- | :--- |
| Missing `Customer ID` | **INFORMATIONAL** | 634,393 (65.34%) | `Customer ID` is NULL | Map `NULL` -> `'CUST_ANONYMOUS'` in staging |
| Combined `Location` format | **LOW** | 970,838 (100.0%) | `"Store XX - City"` | Parse into `store_id` & `city` in staging |
| Negative Refund Signage | **INFORMATIONAL** | 9,449 (0.97%) | `Qty = -1`, `Net Sales < 0` | Retain signed accounting in `fact_sales` |
| Negative Discount Representation | **INFORMATIONAL** | 312,053 (32.14%) | `Discounts <= 0` | Derive positive `discount_amount` metric |
| Implicit USD Currency | **INFORMATIONAL** | 970,838 (100.0%) | No currency column | Document USD standard across reporting |

---

## 14. Recommended Cleaning & Transformation Actions for Task 5 (ETL)

1. **Staging Table Creation**:
   - Parse `Location` into `store_id` (`STORE_01` .. `STORE_30`) and `city` (`Austin`, `Dallas`, etc.).
   - Replace NULL `Customer ID` with `'CUST_ANONYMOUS'`.
2. **Dimension Tables Population**:
   - `dim_date`: Build full 731-day date dimension (2024–2025).
   - `dim_product`: Populate from 67 SKUs, 32 Items, 6 Categories, and Price Point Names.
   - `dim_store`: Populate 30 stores with parsed City and State/Region lookup mapping.
   - `dim_customer`: Populate 19,999 identified customers plus `'CUST_ANONYMOUS'`.
3. **Fact Table Loading**:
   - Load `fact_sales` with composite primary key `(transaction_id, sku, event_type)`.

---
