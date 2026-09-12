# Data Dictionary — NovaMart Financial Analytics

This document provides the complete data dictionary for the NovaMart Financial Analytics project, explicitly classifying **SOURCE FIELDS**, **DERIVED FIELDS**, and **SIMULATED FIELDS**.

---

## 1. Processed Fact Table Schema: `fact_sales_processed.csv`

**File Location:** `data/processed/fact_sales_processed.csv` (and `.parquet`)  
**Description:** Production-ready point-of-sale transaction line-item dataset covering 24 months (2024–2025).  
**Total Rows:** 970,838 | **Total Columns:** 30 | **Primary Business Key:** `(transaction_id, sku, event_type)`  

| Column Name | Classification | Data Type | Nullable | Description |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | **SOURCE FIELD** | `VARCHAR(50)` | No | Unique POS transaction header identifier (585,691 unique). Composite PK 1/3. |
| `sku` | **SOURCE FIELD** | `VARCHAR(50)` | No | Stock Keeping Unit identifier (67 unique SKUs). Composite PK 2/3. |
| `item` | **SOURCE FIELD** | `VARCHAR(100)` | No | Product item name / description (32 unique items). |
| `category` | **SOURCE FIELD** | `VARCHAR(50)` | No | High-level product category (*Home Goods, Apparel, Electronics, Footwear, Accessories, Beauty*). |
| `price_point_name` | **SOURCE FIELD** | `VARCHAR(50)` | No | Product variant / size / color tier (25 unique). |
| `location_raw` | **SOURCE FIELD** | `VARCHAR(100)` | No | Original raw store location string (`"Store XX - CityName"`). |
| `store_id` | **DERIVED FIELD** | `VARCHAR(20)` | No | Standardized store code parsed from `location_raw` (`STORE_01` .. `STORE_30`). |
| `city` | **DERIVED FIELD** | `VARCHAR(50)` | No | Extracted store city name (`Austin`, `Dallas`, `Houston`, etc.). |
| `customer_id` | **DERIVED FIELD** | `VARCHAR(50)` | No | Standardized customer ID (`CUST_ANONYMOUS` for guest purchases; 634,393 rows). |
| `customer_type` | **DERIVED FIELD** | `VARCHAR(20)` | No | Customer classification (`"Identified"` vs `"Anonymous"`). |
| `event_type` | **SOURCE FIELD** | `VARCHAR(20)` | No | POS transaction event classification (`"Payment"` or `"Refund"`). Composite PK 3/3. |
| `is_refund` | **DERIVED FIELD** | `BOOLEAN` | No | Logical indicator flag (`True` if `event_type == 'Refund'`, `False` otherwise). |
| `transaction_datetime` | **DERIVED FIELD** | `VARCHAR(30)` | No | Combined transaction ISO timestamp string (`YYYY-MM-DD HH:MM`). |
| `transaction_date` | **DERIVED FIELD** | `DATE` | No | Canonical transaction calendar date (`YYYY-MM-DD`). |
| `qty` | **SOURCE FIELD** | `INTEGER` | No | Units sold (`1`, `2`, `3`) or returned (`-1`). |
| `unit_price` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Selling price per single unit. |
| `gross_sales` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Raw line gross sales (`qty * unit_price`). Negative for refunds. |
| `discounts` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Raw line discount amount (recorded as negative float, e.g. `-13.50`). |
| `discount_amount` | **DERIVED FIELD** | `NUMERIC(10,2)`| No | Positive representation of discount amount for reporting (`ABS(discounts)`). |
| `net_sales` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Raw line net sales (`gross_sales + discounts`). |
| `unit_cost` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Cost of goods per unit. |
| `cogs` | **DERIVED FIELD** | `NUMERIC(10,2)`| No | Cost of Goods Sold (`qty * unit_cost`). Negative for refunds. |
| `gross_profit` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Raw line gross profit (`net_sales - cogs`). Negative for refunds. |
| `gross_margin_pct` | **DERIVED FIELD** | `NUMERIC(6,4)` | No | Line gross profit margin ratio (`gross_profit / net_sales`). 0.00 if `net_sales == 0`. |
| `discount_rate_pct` | **DERIVED FIELD** | `NUMERIC(6,4)` | No | Line discount percentage (`discount_amount / ABS(gross_sales)`). 0.00 if `gross_sales == 0`. |
| `tax` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Sales tax collected. Negative for refunds. |
| `total_collected` | **SOURCE FIELD** | `NUMERIC(10,2)`| No | Total tender collected (`net_sales + tax`). |
| `payment_method` | **SOURCE FIELD** | `VARCHAR(30)` | No | Payment method tender (`Card`, `Cash`, `Other`). |
| `device_name` | **SOURCE FIELD** | `VARCHAR(50)` | No | POS device terminal (`Register 1`, `Register 2`, `iPad POS`). |
| `time_zone` | **SOURCE FIELD** | `VARCHAR(10)` | No | Location timezone (`CST`). |

---

## 2. Source Calendar Reference Schema: `02_ground_truth_event_calendar.csv`

**File Location:** `data/raw/02_ground_truth_event_calendar.csv`  
**Total Rows:** 731 | **Total Columns:** 10 | **Primary Key:** `Date`  

| Column Name | Classification | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Date` | **SOURCE FIELD** | `DATE` | Calendar date (`YYYY-MM-DD`). |
| `Weekday` | **SOURCE FIELD** | `VARCHAR(15)` | Day of week (*Monday* .. *Sunday*). |
| `Event` | **SOURCE FIELD** | `VARCHAR(100)` | Event name (e.g., `New Year's Day`, `Black Friday`). Null on non-event days. |
| `Season x Month x Event Mult` | **SOURCE FIELD** | `NUMERIC(6,4)` | Demand multiplier combining season, month, and event factors. |
| `DOW Mult` | **SOURCE FIELD** | `NUMERIC(4,2)` | Day of week multiplier. |
| `Month Mult` | **SOURCE FIELD** | `NUMERIC(4,2)` | Monthly seasonality factor. |
| `Event Mult` | **SOURCE FIELD** | `NUMERIC(4,2)` | Specific event factor. |
| `Discount Line Prob` | **SOURCE FIELD** | `NUMERIC(4,2)` | Probability of line discount application on date. |
| `Refund Txn Prob` | **SOURCE FIELD** | `NUMERIC(6,4)` | Probability of return transaction on date. |
| `Store Closed` | **SOURCE FIELD** | `INTEGER` | Binary flag (`1` if store closed, `0` otherwise). |

---

## 3. Simulated Tables (To Be Ingested/Created in Future Tasks)

| Table Name | Classification | Planned Grain | Description |
| :--- | :--- | :--- | :--- |
| `fact_expenses` | **SIMULATED FIELD** | One expense line item record | Operating expenses (OPEX), payroll, and marketing spend for EBITDA analytics. |
| `fact_budget` | **SIMULATED FIELD** | One department × month record | Target budget tracking and Budget vs. Actual variance analysis. |
| `fact_forecast` | **DERIVED FIELD** | One forecast date × model record | Output table for revenue forecasting models and accuracy benchmarks. |

---
