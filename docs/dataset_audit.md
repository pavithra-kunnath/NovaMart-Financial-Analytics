# Dataset Source Audit Report — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 2B — Dataset Source Audit  
**Audit Scope:** Raw files located in `data/raw/`  

---

## 1. File Inventory

| Filename | File Type | File Size | Compressed | Number of Rows | Number of Columns |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `square_item_sales_detail_24mo.csv` | CSV (Text) | 157,254,068 bytes (149.97 MB) | No | 970,838 | 22 |
| `02_ground_truth_event_calendar.csv` | CSV (Text) | 38,734 bytes (0.04 MB) | No | 731 | 10 |

---

## 2. Schema & Data Types

### A. `square_item_sales_detail_24mo.csv`

| # | Column Name | Inferred Data Type | Classification | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `Date` | `object` (YYYY-MM-DD) | Date/Time | `2024-01-01`, `2024-01-02` |
| 2 | `Time` | `object` (HH:MM) | Date/Time | `14:41`, `15:50` |
| 3 | `Time Zone` | `object` | Categorical | `CST` |
| 4 | `Category` | `object` | Categorical | `Home Goods`, `Apparel`, `Electronics` |
| 5 | `Item` | `object` | Categorical / Text | `Ceramic Coffee Mug`, `Classic Denim Jacket` |
| 6 | `Qty` | `int64` | Numeric (Discrete) | `1`, `2`, `-1` |
| 7 | `Price Point Name` | `object` | Categorical | `Regular`, `S`, `Black` |
| 8 | `SKU` | `object` | Identifier | `SQ-1058`, `SQ-1001` |
| 9 | `Unit Price` | `float64` | Numeric (Continuous) | `16.0`, `79.0`, `45.0` |
| 10 | `Gross Sales` | `float64` | Numeric (Continuous) | `16.0`, `79.0`, `-129.0` |
| 11 | `Discounts` | `float64` | Numeric (Continuous) | `0.0`, `-13.5`, `-11.8` |
| 12 | `Net Sales` | `float64` | Numeric (Continuous) | `16.0`, `79.0`, `-129.0` |
| 13 | `Tax` | `float64` | Numeric (Continuous) | `1.32`, `6.52`, `-10.64` |
| 14 | `Total Collected` | `float64` | Numeric (Continuous) | `17.32`, `85.52`, `-139.64` |
| 15 | `Transaction ID` | `object` | Identifier | `TXN1000001`, `TXN1000002` |
| 16 | `Payment Method` | `object` | Categorical | `Card`, `Cash`, `Other` |
| 17 | `Device Name` | `object` | Categorical | `Register 2`, `Register 1`, `iPad POS` |
| 18 | `Location` | `object` | Categorical / Text | `Store 01 - Austin`, `Store 02 - Dallas` |
| 19 | `Customer ID` | `object` | Identifier | `CUST16654`, `CUST02796`, `NaN` |
| 20 | `Event Type` | `object` | Categorical | `Payment`, `Refund` |
| 21 | `Unit Cost` | `float64` | Numeric (Continuous) | `4.48`, `35.55`, `43.45` |
| 22 | `Gross Profit` | `float64` | Numeric (Continuous) | `11.52`, `43.45`, `-61.92` |

### B. `02_ground_truth_event_calendar.csv`

| # | Column Name | Inferred Data Type | Classification | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `Date` | `object` (YYYY-MM-DD) | Date/Time | `2024-01-01`, `2024-01-02` |
| 2 | `Weekday` | `object` | Categorical | `Monday`, `Tuesday` |
| 3 | `Event` | `object` | Categorical | `New Year's Day`, `Valentine's Eve`, `NaN` |
| 4 | `Season x Month x Event Mult` | `float64` | Numeric | `0.401`, `0.682` |
| 5 | `DOW Mult` | `float64` | Numeric | `0.9`, `0.85` |
| 6 | `Month Mult` | `float64` | Numeric | `0.8`, `0.92` |
| 7 | `Event Mult` | `float64` | Numeric | `0.5`, `0.85` |
| 8 | `Discount Line Prob` | `float64` | Numeric | `0.3`, `0.45` |
| 9 | `Refund Txn Prob` | `float64` | Numeric | `0.015`, `0.0375` |
| 10 | `Store Closed` | `int64` | Categorical / Flag | `0`, `1` |

---

## 3. Data Completeness

### `square_item_sales_detail_24mo.csv`
- **Total Rows:** 970,838
- **Missing Values:**
  - `Customer ID`: 634,393 missing values (**65.34% missing**). This reflects guest / anonymous POS purchases, which is standard in retail POS data.
  - All other 21 columns have **0 missing values (0.00% missing)**.
- **Completely Empty Columns:** None.

### `02_ground_truth_event_calendar.csv`
- **Total Rows:** 731
- **Missing Values:**
  - `Event`: 671 missing values (**91.79% missing**). This is expected because most calendar days do not have a named promotional or holiday event.
  - All other 9 columns have **0 missing values (0.00% missing)**.

---

## 4. Data Uniqueness & Key Identification

### `square_item_sales_detail_24mo.csv`
- **Duplicate Rows:** 0 exact duplicate rows across all 22 columns.
- **Transaction ID Uniqueness:** 585,691 distinct transaction IDs across 970,838 rows (average 1.66 line items per transaction, max 4 lines).
- **Candidate Primary Key (Line Item Grain):** Composite key of `(Transaction ID, SKU, Event Type)` or auto-increment surrogate key (`sales_line_id`).
- **Unique Identifier Counts:**
  - `Transaction ID`: 585,691 unique
  - `Customer ID`: 19,999 unique (among 336,445 non-null records)
  - `SKU`: 67 unique
  - `Location`: 30 unique
  - `Item`: 32 unique

### `02_ground_truth_event_calendar.csv`
- **Duplicate Rows:** 0 exact duplicate rows.
- **Candidate Primary Key:** `Date` (731 unique dates out of 731 rows, 100% unique).

---

## 5. Date Audit

- **Date Range:** `2024-01-01` to `2025-12-31`
- **Distinct Dates:** 729 distinct dates present in sales detail (731 calendar days total; 2 store-closed days in calendar have 0 sales).
- **Unparseable / Invalid Dates:** 0 invalid date records.
- **Time Distribution:** Transactions recorded between `09:00` and `20:59` daily across a fixed `CST` time zone.
- **Monthly Distribution:** 24 continuous calendar months represented with 28,659 to 63,126 transactions per month. Excellent continuity for monthly financial forecasting and seasonal decomposition.

---

## 6. Sales / Financial Field Audit

| Financial Item | Source Field(s) | Status | Logic / Notes |
| :--- | :--- | :--- | :--- |
| Quantity | `Qty` | **DIRECTLY AVAILABLE** | `1`, `2`, `3` for payments; `-1` for refunds. |
| Unit Price | `Unit Price` | **DIRECTLY AVAILABLE** | Item selling price per unit. |
| Gross Sales | `Gross Sales` | **DIRECTLY AVAILABLE** | Exactly equals `Qty * Unit Price`. |
| Discount | `Discounts` | **DIRECTLY AVAILABLE** | Line discount amount (recorded as negative float, e.g. `-13.5`). |
| Discount Rate | N/A | **DERIVABLE** | `ABS(Discounts) / Gross Sales` when `Gross Sales > 0`. |
| Net Sales | `Net Sales` | **DIRECTLY AVAILABLE** | Exactly equals `Gross Sales + Discounts`. |
| Tax | `Tax` | **DIRECTLY AVAILABLE** | Sales tax collected. |
| Refund / Return Amount | `Gross Sales` / `Net Sales` | **DIRECTLY AVAILABLE** | Captured on rows where `Event Type = 'Refund'` (negative dollar amounts). |
| Refund / Return Quantity | `Qty` | **DIRECTLY AVAILABLE** | `-1` on rows where `Event Type = 'Refund'`. |
| Unit Cost | `Unit Cost` | **DIRECTLY AVAILABLE** | Cost of goods per unit. |
| COGS | N/A | **DERIVABLE** | `Qty * Unit Cost` (negative for refunds). |
| Gross Profit | `Gross Profit` | **DIRECTLY AVAILABLE** | Exactly equals `Net Sales - (Qty * Unit Cost)`. |
| Currency | N/A | **NOT AVAILABLE** | Implicitly USD ($). No explicit currency column in raw CSV. |

---

## 7. Customer Audit

- **Customer ID:** **DIRECTLY AVAILABLE** (`Customer ID` column, 19,999 unique IDs).
- **Customer Attributes:** **NOT AVAILABLE** (No customer name, email, address, or demographic columns).
- **Customer Purchase History:** **DERIVABLE** (Aggregating transactions by `Customer ID`).
- **Customer Revenue Contribution:** **DERIVABLE** (`SUM(Net Sales)` grouped by `Customer ID`).
- **Order Frequency:** **DERIVABLE** (`COUNT(DISTINCT Transaction ID)` grouped by `Customer ID`).
- **Average Order Value (AOV):** **DERIVABLE** (`SUM(Net Sales) / COUNT(DISTINCT Transaction ID)` grouped by `Customer ID`).

---

## 8. Product Audit

- **Product ID / SKU:** **DIRECTLY AVAILABLE** (`SKU` column, 67 unique SKUs).
- **Product Name:** **DIRECTLY AVAILABLE** (`Item` column, 32 unique item names).
- **Category:** **DIRECTLY AVAILABLE** (`Category` column, 6 categories: `Home Goods`, `Apparel`, `Electronics`, `Footwear`, `Accessories`, `Beauty`).
- **Subcategory:** **NOT AVAILABLE** (Not present in source data).
- **Unit Cost:** **DIRECTLY AVAILABLE** (`Unit Cost` column).
- **Unit Price:** **DIRECTLY AVAILABLE** (`Unit Price` column).
- **Product-Level Revenue:** **DERIVABLE** (`SUM(Net Sales)` grouped by `SKU` / `Item`).
- **Product-Level Profit:** **DERIVABLE** (`SUM(Gross Profit)` grouped by `SKU` / `Item`).
- **Product-Level Returns:** **DERIVABLE** (`SUM(Qty)` or `SUM(Net Sales)` where `Event Type = 'Refund'` grouped by `SKU`).

---

## 9. Store / Geography Audit

- **Store ID:** **DERIVABLE** (Parsing `Store XX` from `Location` string, e.g. `Store 01`).
- **Store Name / Location:** **DIRECTLY AVAILABLE** (`Location` column, 30 distinct retail locations).
- **City:** **DERIVABLE** (Parsing city name after hyphen in `Location`, e.g. `Austin`, `Dallas`, `Houston`).
- **State / Province:** **NOT AVAILABLE** (Only city names are embedded in location strings; state mapping table can be derived in staging).
- **Region:** **NOT AVAILABLE** (Can be derived from city/state mapping in staging).
- **Geographic Hierarchy:** **DERIVABLE** (Location -> City -> State -> Region via staging mapping).

---

## 10. Returns / Refunds Audit

- **Refund Records:** Exist as distinct rows in `square_item_sales_detail_24mo.csv` where `Event Type = 'Refund'` (9,449 rows, ~0.97% of all transaction lines).
- **Identification:** `Event Type` column explicitly specifies `'Payment'` vs `'Refund'`.
- **Refund Values:**
  - `Qty = -1`
  - `Gross Sales` is negative (e.g. `-129.0`)
  - `Net Sales` is negative
  - `Tax` is negative
  - `Total Collected` is negative
  - `Gross Profit` is negative
- **Linking Refunds to Original Sales:** `Transaction ID` for refund lines is a distinct refund transaction ID (e.g. `TXN...`). Refunds are separate transaction events logged by POS devices.
- **Partial Returns:** Captured as single-item refund line items (`Qty = -1`).

---

## 11. Time-Series Suitability

- **Available Historical Period:** Exactly 24 continuous calendar months (`2024-01-01` to `2025-12-31`).
- **Number of Months:** 24 full months.
- **Monthly Revenue Aggregation:** Highly suitable (over 970k rows evenly distributed across all 24 months).
- **Year-Over-Year (YoY) Analysis:** Fully supported (2024 vs 2025 comparison).
- **Forecasting Models Supported:** Baseline Naive, Seasonal Naive, Holt-Winters Exponential Smoothing, ARIMA/SARIMAX, and regression-based ML models.
- **Chronological Backtesting:** Supported (e.g. Train on 2024–2025 Q3, Test/Backtest on 2025 Q4).

---

## 12. Data Quality Risks & Anomalies

1. **High Missingness in Customer ID (65.34% Null):**
   - *Impact:* Customer cohort and RFM analysis can only be performed on the 34.66% identified customer transactions.
   - *Handling:* Group remaining transactions under `Anonymous / Guest` in staging/analytics.
2. **Embedded Location Structure:**
   - *Impact:* `Location` string contains combined store code and city name (`Store 01 - Austin`).
   - *Handling:* Parse into separate `store_id`, `store_name`, and `city` columns during ETL clean step.
3. **Negative Value Representation for Refunds:**
   - *Impact:* Refunds have negative quantities and negative monetary values.
   - *Handling:* Retain negative signs for simple additive aggregations (`SUM(net_sales)` naturally subtracts returns), while isolating refund metrics using `Event Type = 'Refund'`.
4. **Discounts Recorded as Negative Floats:**
   - *Impact:* `Discounts` are negative (e.g., `-13.50`), so `Net Sales = Gross Sales + Discounts`.
   - *Handling:* Enforce explicit sign conventions in ETL and metric definitions (`discount_amount = ABS(Discounts)`).
5. **No Operating Expenses or Budget Data in Raw Source:**
   - *Impact:* Operating Expenses (OPEX), Net Profit, and Budget Variance cannot be calculated directly from source transaction CSVs.
   - *Handling:* Generate structured simulated budget and expense data in later task phases.

---

## 13. NovaMart Requirement Mapping

| Requirement | Source Field(s) | Status | Notes |
| :--- | :--- | :--- | :--- |
| Sales transactions | `Transaction ID`, `Date`, `Time`, `SKU`, `Qty` | **DIRECTLY AVAILABLE** | 970,838 line items across 585,691 transactions. |
| Customer analysis | `Customer ID` | **DERIVABLE** | Supported for 336,445 identified customer transactions. |
| Product analysis | `SKU`, `Item`, `Category`, `Unit Price`, `Unit Cost` | **DIRECTLY AVAILABLE** | 67 SKUs across 6 product categories. |
| Store/region analysis | `Location` | **DERIVABLE** | 30 store locations with embedded city names. |
| Gross Sales | `Gross Sales` | **DIRECTLY AVAILABLE** | Native POS column equal to `Qty * Unit Price`. |
| Discounts | `Discounts` | **DIRECTLY AVAILABLE** | Recorded as negative monetary amounts. |
| Net Sales | `Net Sales` | **DIRECTLY AVAILABLE** | Native POS column equal to `Gross Sales + Discounts`. |
| Returns/Refunds | `Event Type`, `Qty`, `Gross Sales` | **DIRECTLY AVAILABLE** | Identified by `Event Type = 'Refund'`. |
| Net Revenue | `Net Sales` | **DIRECTLY AVAILABLE** | `SUM(Net Sales)` accounts for revenue net of discounts and refunds. |
| Unit Cost | `Unit Cost` | **DIRECTLY AVAILABLE** | Item cost of goods per unit. |
| COGS | `Qty`, `Unit Cost` | **DERIVABLE** | Calculated as `Qty * Unit Cost`. |
| Gross Profit | `Gross Profit` | **DIRECTLY AVAILABLE** | Native column equal to `Net Sales - COGS`. |
| Gross Margin % | `Gross Profit`, `Net Sales` | **DERIVABLE** | Calculated as `Gross Profit / Net Sales`. |
| Monthly Revenue | `Date`, `Net Sales` | **DERIVABLE** | Monthly aggregation supported across 24 full months. |
| Forecasting | `Date`, `Net Sales`, `02_ground_truth_event_calendar.csv` | **DERIVABLE** | Supported using daily/monthly historical series and calendar multipliers. |
| Forecast Backtesting | `Date`, `Net Sales` | **DERIVABLE** | Supported using chronological split (e.g. 2024-2025Q3 train vs 2025Q4 test). |
| Expenses | N/A | **NOT AVAILABLE** | Must be simulated in later project phase. |
| Budget | N/A | **NOT AVAILABLE** | Must be simulated in later project phase. |
| Business Calendar | `02_ground_truth_event_calendar.csv` | **DIRECTLY AVAILABLE** | Complete 731-day event calendar with event weights and discount/refund probabilities. |

---

## 14. Fact-Table Grain Analysis

**Proposed Grain:**  
The `fact_sales` table will be stored at the **individual POS transaction line-item grain** (one record per line item per transaction event).

**Candidate Business Key:**  
`Transaction ID` + `SKU` + `Event Type`

---

## 15. Recommendation

### A. What the Dataset Supports Very Well
- High-volume transaction detail (970,838 rows) across 24 continuous months (2024–2025).
- Precise unit economics (Unit Price, Unit Cost, Gross Sales, Discounts, Net Sales, Tax, Gross Profit).
- Store-level transaction distribution across 30 retail locations.
- Event and seasonal calendar matching via `02_ground_truth_event_calendar.csv`.

### B. What Can Be Derived Reliably
- COGS, Gross Margin %, Discount Rate %, Average Order Value (AOV).
- City, Store ID, and geographic groupings from `Location`.
- Monthly and daily revenue time series for backtesting and forecasting models.
- Refund rates and return impact on sales volume and net revenue.

### C. What Is Missing
- Operating Expenses (OPEX), Marketing Spend, Payroll, and Corporate Overheads.
- Annual/Monthly Budget Targets.
- Product Subcategories and Customer Profile Attributes (Name, Email, Gender, Segment).
- Explicit Currency Column (implicitly USD).

### D. What Must Be Simulated Later
- Monthly OPEX/Expense records and Department Budget targets to enable Operating Profit (EBITDA) and Budget vs. Actual variance analysis.

### E. Important Limitations for Portfolio Project
- Customer analysis is limited to non-null Customer IDs (34.66% of transactions).
- Store geography requires string parsing to extract store numbers and city names.

### F. Recommendation
**YES — Recommend proceeding.** The dataset is exceptionally clean, realistic, rich in financial fields, perfectly structured for retail analytics, and ideal for time-series forecasting.

---
