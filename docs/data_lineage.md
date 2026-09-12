# Data Lineage Documentation — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 6 — Data Lineage & Pipeline Architecture  

---

## 1. End-to-End Data Pipeline Flow

```
+-------------------------------------------------------------------+
| RAW SOURCE LAYER (data/raw/)                                      |
| - square_item_sales_detail_24mo.csv (970,838 rows)                |
| - 02_ground_truth_event_calendar.csv (731 rows)                   |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| INGESTION MODULE (src/ingest.py)                                  |
| - File existence & schema structure verification                 |
| - Audit metadata tagging (ingestion_timestamp, source_file)       |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| STAGING LAYER (data/staging/)                                     |
| - square_sales_staging.csv / .parquet (970,838 rows)              |
| - Column standardization (snake_case)                             |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| CLEANING & TRANSFORMATION MODULE (src/clean.py)                   |
| - Location string parsing: location_raw -> store_id, city          |
| - Customer null standardization: NULL -> CUST_ANONYMOUS           |
| - Date parsing & bounds validation (2024-01-01 to 2025-12-31)     |
| - Derived financial metrics (cogs, gross_margin_pct, etc.)        |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| VALIDATION MODULE (src/clean.py Assertions)                      |
| - Business Key Uniqueness (transaction_id, sku, event_type)       |
| - Financial Formula Reconciliations (Gross Sales, Net Sales, GP)  |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| PROCESSED LAYER (data/processed/)                                 |
| - fact_sales_processed.csv / .parquet (970,838 rows)              |
| - Production-ready fact table for DWH, PostgreSQL & Power BI      |
+-------------------------------------------------------------------+
```

---

## 2. Detailed Field Lineage & Transformation Mapping

| Target Field Name (Processed) | Source Field Name (Raw) | Transformation Rules & Logic | Target Data Type |
| :--- | :--- | :--- | :--- |
| `transaction_id` | `Transaction ID` | Direct mapping (snake_case standardization). | `VARCHAR(50)` |
| `sku` | `SKU` | Direct mapping. Stock Keeping Unit identifier. | `VARCHAR(50)` |
| `item` | `Item` | Direct mapping. Product description. | `VARCHAR(100)` |
| `category` | `Category` | Direct mapping. Product category. | `VARCHAR(50)` |
| `price_point_name` | `Price Point Name` | Direct mapping. Pricing variant / tier. | `VARCHAR(50)` |
| `location_raw` | `Location` | Preserved original location string (`"Store XX - City"`). | `VARCHAR(100)` |
| `store_id` | `Location` | Extracted regex pattern `Store XX` -> `STORE_XX`. | `VARCHAR(20)` |
| `city` | `Location` | Extracted city name string after hyphen in `Location`. | `VARCHAR(50)` |
| `customer_id_raw` | `Customer ID` | Preserved original raw customer identifier. | `VARCHAR(50)` |
| `customer_id` | `Customer ID` | Replaced `NULL` values with `'CUST_ANONYMOUS'`. | `VARCHAR(50)` |
| `customer_type` | `Customer ID` | Assigned `'Identified'` if non-null, `'Anonymous'` if null. | `VARCHAR(20)` |
| `event_type` | `Event Type` | Direct mapping (`'Payment'` or `'Refund'`). | `VARCHAR(20)` |
| `is_refund` | `Event Type` | Evaluated boolean: `True` if `event_type == 'Refund'`, `False` otherwise. | `BOOLEAN` |
| `transaction_date` | `Date` | Parsed ISO date string (`YYYY-MM-DD`). | `DATE` |
| `transaction_datetime` | `Date` + `Time` | Concatenated date and time into timestamp string (`YYYY-MM-DD HH:MM`). | `VARCHAR(30)` |
| `qty` | `Qty` | Direct mapping. Positive for payments, `-1` for refunds. | `INTEGER` |
| `unit_price` | `Unit Price` | Direct mapping. Unit selling price. | `NUMERIC(10,2)` |
| `gross_sales` | `Gross Sales` | Direct mapping. Raw line gross sales (`qty * unit_price`). | `NUMERIC(10,2)` |
| `discounts` | `Discounts` | Direct mapping. Raw line discount (negative float). | `NUMERIC(10,2)` |
| `discount_amount` | `Discounts` | Calculated positive discount metric: `ABS(discounts)`. | `NUMERIC(10,2)` |
| `net_sales` | `Net Sales` | Direct mapping (`gross_sales + discounts`). | `NUMERIC(10,2)` |
| `unit_cost` | `Unit Cost` | Direct mapping. Cost of goods per unit. | `NUMERIC(10,2)` |
| `cogs` | `Qty` & `Unit Cost` | Derived: `qty * unit_cost` (negative for refunds). | `NUMERIC(10,2)` |
| `gross_profit` | `Gross Profit` | Direct mapping (`net_sales - cogs`). | `NUMERIC(10,2)` |
| `gross_margin_pct` | `Gross Profit` & `Net Sales` | Derived ratio: `gross_profit / net_sales` (0.0 if `net_sales == 0`). | `NUMERIC(6,4)` |
| `discount_rate_pct` | `Discounts` & `Gross Sales` | Derived ratio: `ABS(discounts) / ABS(gross_sales)` (0.0 if `gross_sales == 0`). | `NUMERIC(6,4)` |
| `tax` | `Tax` | Direct mapping. Sales tax collected. | `NUMERIC(10,2)` |
| `total_collected` | `Total Collected` | Direct mapping (`net_sales + tax`). | `NUMERIC(10,2)` |
| `payment_method` | `Payment Method` | Direct mapping (`Card`, `Cash`, `Other`). | `VARCHAR(30)` |
| `device_name` | `Device Name` | Direct mapping (`Register 1`, `Register 2`, `iPad POS`). | `VARCHAR(50)` |

---
