# Data Contract — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 3 — Data Contract & Fact Table Grain Specification  
**Status:** Approved & Formally Specified  

---

## 1. Purpose

This Data Contract establishes explicit, binding specifications between the raw source data landed in `data/raw/` and all downstream data pipelines, ETL staging transformations, PostgreSQL warehouse schema definitions, SQL analytical views, and Power BI semantic models.

The contract formally governs:
- Accepted raw source dataset definitions and schemas
- Field-level data types, nullability, validation constraints, and allowed values
- Mathematical formulas for financial metrics (Sales, Discounts, COGS, Gross Profit, Margins)
- Accounting treatment for return/refund transactions
- Identifier conventions and business key uniqueness rules
- Handling of anonymous customer purchases and derived store/location attributes
- Specifications for physical and virtual fact-table grains

---

## 2. Source Files

| Filename | Purpose | Expected Format | Expected Grain | Date Coverage | Immutability | Source / Attribution |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `square_item_sales_detail_24mo.csv` | POS Sales & Refund Line-Item Transactions | CSV (UTF-8) | One line per item per transaction event | `2024-01-01` to `2025-12-31` | Immutable Raw | Square POS Sales Detail Export (24-Month Synthetic Retail Benchmark) |
| `02_ground_truth_event_calendar.csv` | Promotional, Seasonality & Calendar Reference | CSV (UTF-8) | One record per calendar date | `2024-01-01` to `2025-12-31` | Immutable Raw | NovaMart Ground Truth Retail Event Calendar |

---

## 3. Source Field Contract

Below is the field contract for all 22 columns in `square_item_sales_detail_24mo.csv`:

| Source Field | Business Meaning | Expected Data Type | Nullable? | Allowed / Expected Values | Validation Rule | Downstream Usage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Date` | Transaction calendar date | `DATE` (YYYY-MM-DD) | No | `2024-01-01` to `2025-12-31` | Valid ISO date within 2024–2025 range | `dim_date` join key; daily/monthly time series |
| `Time` | Transaction timestamp (time of day) | `TIME` (HH:MM) | No | `09:00` to `20:59` | Valid HH:MM time string | Hourly intraday sales distribution |
| `Time Zone` | Location time zone | `VARCHAR(10)` | No | `'CST'` | Non-null static string | Location timezone metadata |
| `Category` | High-level product category | `VARCHAR(50)` | No | `Home Goods`, `Apparel`, `Electronics`, `Footwear`, `Accessories`, `Beauty` | Member of 6 predefined categories | Category dimension (`dim_product`) |
| `Item` | Product item description / name | `VARCHAR(100)` | No | 32 unique product names | Non-empty text string | Product dimension (`dim_product`) |
| `Qty` | Number of units purchased or returned | `INTEGER` | No | `1`, `2`, `3` for Payment; `-1` for Refund | Non-zero integer | Sales volume & units metric (`fact_sales`) |
| `Price Point Name` | SKU variant or price tier | `VARCHAR(50)` | No | `Regular`, `S`, `M`, `L`, `Black`, `White`, etc. (25 unique) | Non-empty text string | Product variant attribute |
| `SKU` | Stock Keeping Unit identifier | `VARCHAR(50)` | No | `SQ-1001` to `SQ-1067` (67 unique SKUs) | Matches regex `^SQ-\d{4}$` | Product primary key (`dim_product`) |
| `Unit Price` | Selling price per single unit | `NUMERIC(10,2)` | No | `>= 0.00` (`9.50` to `129.00`) | Non-negative numeric | Pricing analytics & revenue verification |
| `Gross Sales` | Total gross sale before discount | `NUMERIC(10,2)` | No | `= Qty * Unit Price` (positive for Payment, negative for Refund) | `Gross Sales == Qty * Unit Price` | Financial metric (`Gross Sales`) |
| `Discounts` | Line item discount amount | `NUMERIC(10,2)` | No | `<= 0.00` (`0.00` to `-154.80`) | Non-positive numeric (0 or negative) | Financial metric (`Discounts`) |
| `Net Sales` | Net revenue collected for line item | `NUMERIC(10,2)` | No | `= Gross Sales + Discounts` | `Net Sales == Gross Sales + Discounts` | Core revenue metric (`Net Sales`) |
| `Tax` | Sales tax collected | `NUMERIC(10,2)` | No | Numeric (positive for Payment, negative for Refund) | Non-null numeric | Financial tax reporting |
| `Total Collected` | Total monetary collection | `NUMERIC(10,2)` | No | `= Net Sales + Tax` | `Total Collected == Net Sales + Tax` | Cashflow & tender reconciliation |
| `Transaction ID` | POS transaction header identifier | `VARCHAR(50)` | No | `TXN1000001` to `TXN1585691` (585,691 unique) | Non-null transaction ID | Header grouping & business key |
| `Payment Method` | Tender type used | `VARCHAR(30)` | No | `Card`, `Cash`, `Other` | Member of approved payment methods | Payment method analytics |
| `Device Name` | POS terminal device | `VARCHAR(50)` | No | `Register 1`, `Register 2`, `iPad POS` | Non-null device name | Channel / terminal analytics |
| `Location` | Store location descriptor | `VARCHAR(100)` | No | `"Store XX - CityName"` (30 unique locations) | Matches pattern `"Store \d{2} - .+"` | Derived `store_id` & `city` (`dim_store`) |
| `Customer ID` | Customer identifier | `VARCHAR(50)` | Yes | `CUST00001` to `CUST20000`, or `NULL` | Valid customer ID or NULL | Customer dimension (`dim_customer`) |
| `Event Type` | POS event classification | `VARCHAR(20)` | No | `'Payment'` or `'Refund'` | Must be `'Payment'` or `'Refund'` | Event filtering & return accounting |
| `Unit Cost` | Cost of goods per unit | `NUMERIC(10,2)` | No | `>= 0.00` (`2.66` to `67.08`) | Non-negative numeric | Cost & profitability calculations |
| `Gross Profit` | Line item gross profit | `NUMERIC(10,2)` | No | `= Net Sales - (Qty * Unit Cost)` | `Gross Profit == Net Sales - COGS` | Core profitability metric (`Gross Profit`) |

---

## 4. Event Type Rule

The source dataset contains exactly two distinct values in the `Event Type` column:

1. **`Payment`**: Represents a completed retail sale.
   - `Qty > 0` (1, 2, or 3 units)
   - `Gross Sales > 0`, `Net Sales > 0`, `Gross Profit > 0`
   - Represents positive revenue generation.

2. **`Refund`**: Represents a customer return/refund event.
   - `Qty = -1` (negative quantity)
   - `Gross Sales < 0`, `Net Sales < 0`, `Gross Profit < 0`
   - Represents negative revenue (revenue reduction).

**Rule:** No other event types exist in the source data. The ETL pipeline must reject or log an alert for any incoming record with an `Event Type` other than `'Payment'` or `'Refund'`.

---

## 5. Financial Rules & Formulations

The financial accounting rules for NovaMart are defined as follows:

### A. Gross Sales
$$\text{Gross Sales} = \text{Qty} \times \text{Unit Price}$$

### B. Discount Amount & Net Sales
In the raw source, discounts are recorded as non-positive numbers (`Discounts <= 0.00`).
- **Accounting Representation (Signed):**
  $$\text{Net Sales} = \text{Gross Sales} + \text{Discounts}$$
- **Positive Metric Representation (for Reporting):**
  $$\text{Discount Amount} = |\text{Discounts}|$$
  $$\text{Net Sales} = \text{Gross Sales} - \text{Discount Amount}$$

### C. Cost of Goods Sold (COGS)
$$\text{COGS} = \text{Qty} \times \text{Unit Cost}$$
*For Refund rows (`Qty = -1`), COGS is negative, correctly reducing total inventory cost.*

### D. Gross Profit
$$\text{Gross Profit} = \text{Net Sales} - \text{COGS}$$
*For Refund rows, Gross Profit is negative, correctly reducing total gross margin.*

### E. Gross Margin %
$$\text{Gross Margin \%} = \begin{cases} \frac{\text{Gross Profit}}{\text{Net Sales}} & \text{if } \text{Net Sales} \neq 0 \\ 0.00 & \text{if } \text{Net Sales} = 0 \end{cases}$$

### F. Discount Rate %
$$\text{Discount Rate \%} = \begin{cases} \frac{|\text{Discounts}|}{\text{Gross Sales}} & \text{if } \text{Gross Sales} \neq 0 \\ 0.00 & \text{if } \text{Gross Sales} = 0 \end{cases}$$

---

## 6. Net Revenue Definition

**NovaMart Definition:**  
$$\text{Net Revenue} = \sum \text{Net Sales}$$

Because refund rows in `square_item_sales_detail_24mo.csv` already carry negative `Net Sales` values (`Event Type = 'Refund'`), summing `Net Sales` directly across any date range or dimension produces the true **Net Revenue** (Gross Revenue minus Discounts minus Refunds) without double-counting.

---

## 7. Refund / Return Contract

- **Identification:** `Event Type = 'Refund'`.
- **Quantity:** `Qty = -1`.
- **Financial Values:** Negative `Gross Sales`, `Net Sales`, `Tax`, and `Total Collected`.
- **COGS & Profit Treatment:** COGS is negative (`-1 * Unit Cost`), and Gross Profit is negative (`Net Sales - COGS`), ensuring profitability metrics remain perfectly balanced when aggregated.
- **Linkage to Original Sale:** Refunds in Square POS exports are recorded as independent refund receipts with unique `Transaction ID` strings. They are not joined to original payment transaction IDs in the raw source.
- **Fact Table Treatment:** Refund lines remain inside `fact_sales` as signed transaction records. Filtered analysis of returns will be supported via a database view (`vw_returns_detail`).

---

## 8. Customer Contract

- **Null Handling:** `Customer ID` is `NULL` for 634,393 rows (65.34%).
- **Business Meaning:** `NULL` represents anonymous walk-in / guest purchases.
- **Downstream Treatment:**
  - In `dim_customer`, create a default surrogate key `cust_0` with `customer_id = 'CUST_ANONYMOUS'` and `customer_name = 'Guest / Anonymous'`.
  - Replace `NULL` values in staging with `'CUST_ANONYMOUS'` so that 100% of transactions join cleanly to `dim_customer` and revenue metrics are never dropped.
- **Customer Segmentation:** Customer-level metrics (RFM, LTV, Retention) must filter for `customer_id != 'CUST_ANONYMOUS'`.

---

## 9. Product Contract

- **Product Primary Key:** `SKU` (67 unique values, e.g., `SQ-1001`).
- **Product Attributes:**
  - `Item` (Product Name, 32 unique values)
  - `Category` (6 categories)
  - `Price Point Name` (Variant / Size / Color, 25 unique values)
  - `Unit Price` & `Unit Cost`
- **Subcategory Availability:** **NOT AVAILABLE** in raw data. Subcategory will not be invented or added to `dim_product`.

---

## 10. Store / Location Contract

- **Raw Source Format:** `"Store XX - CityName"` (e.g., `Store 01 - Austin`, `Store 02 - Dallas`).
- **ETL Staging Parsing:**
  - `store_id` = Extracted store code (`STORE_01`, `STORE_02`, ..., `STORE_30`).
  - `store_name` = Full location string (`Store 01 - Austin`).
  - `city` = Extracted city name (`Austin`, `Dallas`, `Houston`, etc.).
- **State & Region:** **NOT AVAILABLE** in raw source. State and Region columns will only be populated downstream using a documented, external US state/region reference lookup table during staging.

---

## 11. Date Contract

- **Canonical Date:** `Date` column (`YYYY-MM-DD`).
- **Timestamp:** `Time` column (`HH:MM`).
- **Time Zone:** Fixed `CST` time zone.
- **Date Range:** `2024-01-01` through `2025-12-31` (24 full months).
- **Date Dimension Join:** `Date` maps directly to `dim_date.date_key` (format `YYYYMMDD` or `DATE`).
- **Monthly Aggregation:** Truncating `Date` to `YYYY-MM-01` supports monthly financial reporting and revenue forecasting.

---

## 12. Currency Contract

- **Currency:** Implicit United States Dollars (USD, `$`).
- **Storage:** No currency column exists in raw CSV. All monetary fields are numeric USD values.
- **Downstream Representation:** Documented as USD across all database schemas, documentation, and Power BI report headers. No multi-currency conversions are required.

---

## 13. Fact Table Grain Definitions

### A. `fact_sales`
- **Grain Statement:** *"One record per individual POS transaction line-item event."*
- **Candidate Business Key:** `Transaction ID` + `SKU` + `Event Type`
- **Empirical Uniqueness Verification:**
  - Total Raw Rows: **970,838**
  - Unique `(Transaction ID, SKU, Event Type)` Combinations: **970,838**
  - Duplicate Count: **0 (100% Unique)**
- **Conclusion:** `(Transaction ID, SKU, Event Type)` is confirmed as the exact, unique business key for `fact_sales`.

### B. `fact_returns`
- **Decision:** **Do NOT create a separate physical `fact_returns` table.**
- **Reasoning:** Returns in the raw source are already fully structured line-item events inside `square_item_sales_detail_24mo.csv` with negative quantities and signed financial amounts. Keeping them inside `fact_sales` preserves double-entry accounting integrity and prevents split-table join complexity.
- **Reporting View:** A database view `vw_returns_detail` (`SELECT * FROM fact_sales WHERE event_type = 'Refund'`) will be created for dedicated return analysis.

### C. `fact_expenses`
- **Grain Statement:** *"One expense line item record."*
- **Status:** **SIMULATED / DERIVED DATA** (Source dataset does not contain operating expenses).
- **Planned Fields:** `expense_id`, `date_key`, `department_id`, `expense_category`, `amount`, `description`.

### D. `fact_budget`
- **Grain Statement:** *"One department × business-calendar month budget record."*
- **Status:** **SIMULATED / DERIVED DATA** (Source dataset does not contain budget targets).
- **Planned Fields:** `budget_id`, `year_month`, `department_id`, `budgeted_revenue`, `budgeted_cogs`, `budgeted_opex`, `budgeted_gross_profit`.

### E. `fact_forecast`
- **Grain Statement:** *"One forecast date × model output record."*
- **Status:** **DERIVED DATA** (Generated by forecasting Python models).
- **Planned Fields:** `forecast_id`, `forecast_date`, `predicted_net_revenue`, `lower_bound_95`, `upper_bound_95`, `model_name`, `training_cutoff_date`, `created_at`.

---

## 14. Data Quality Validation Rules

The ETL pipeline must enforce the following validation assertions:

1. **Identifier Integrity:**
   - `Transaction ID` != NULL
   - `SKU` != NULL
   - `Event Type` IN (`'Payment'`, `'Refund'`)
   - Composite Key `(Transaction ID, SKU, Event Type)` MUST BE UNIQUE.

2. **Numeric Constraints:**
   - `Qty` != 0
   - `Unit Price` >= 0.00
   - `Unit Cost` >= 0.00

3. **Financial Reconciliation Assertions (Tolerance: $0.01):**
   - `ABS(Gross Sales - (Qty * Unit Price)) <= 0.01`
   - `ABS(Net Sales - (Gross Sales + Discounts)) <= 0.01`
   - `ABS(COGS - (Qty * Unit Cost)) <= 0.01`
   - `ABS(Gross Profit - (Net Sales - COGS)) <= 0.01`

4. **Date Integrity:**
   - `Date` IS VALID DATE AND `Date >= '2024-01-01'` AND `Date <= '2025-12-31'`

5. **Customer Integrity:**
   - `Customer ID` IS NULL OR `Customer ID LIKE 'CUST%'`

---

## 15. Data Contract Status Summary

| Rule / Requirement | Status | Reason |
| :--- | :--- | :--- |
| POS Sales Transactions | **APPROVED** | Verified against 970,838 raw records |
| POS Refund Transactions | **APPROVED** | Verified 9,449 refund rows with signed financial fields |
| `fact_sales` Business Key Uniqueness | **APPROVED** | Tested `(Transaction ID, SKU, Event Type)`: 0 duplicates |
| Customer Purchase History | **APPROVED** | Supported for identified customer IDs |
| Anonymous Customer Treatment | **APPROVED WITH ASSUMPTION** | Map NULL `Customer ID` to `'CUST_ANONYMOUS'` |
| Store & City Parsing | **APPROVED WITH ASSUMPTION** | Derived via string extraction from `Location` |
| Product SKU & Category | **APPROVED** | 67 SKUs across 6 categories |
| Product Subcategories | **NOT AVAILABLE** | Not present in raw source |
| Customer Demographics | **NOT AVAILABLE** | Not present in raw source |
| State & Region Geography | **REQUIRES FUTURE MAPPING** | External state/region lookup table required in staging |
| Operating Expenses (OPEX) | **SIMULATED LATER** | Not present in raw source |
| Department Budgets | **SIMULATED LATER** | Not present in raw source |
| Revenue Forecasting Models | **DERIVABLE LATER** | Generated during forecasting phase |

---
