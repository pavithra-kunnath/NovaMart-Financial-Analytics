# ETL Pipeline Execution Report — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 6 — ETL Pipeline & Staging/Processed Data Layers  
**Execution Timestamp:** 2026-09-08T15:38:49  
**Pipeline Entry Point:** `python -m src.clean`  
**Status:** **SUCCESSFUL & IDEMPOTENT**  

---

## 1. ETL Pipeline Overview

The NovaMart ETL pipeline ingests immutable raw POS transaction data and event reference calendars, standardizes field naming conventions, performs store location and customer transformations, computes derived financial metrics (COGS, Gross Margin %, Discount Rate %), verifies contract validation assertions, and outputs production-ready datasets to `data/staging/` and `data/processed/`.

---

## 2. Input Datasets

| Dataset | File Path | File Format | Raw Input Rows | Raw Columns |
| :--- | :--- | :--- | :--- | :--- |
| Raw Sales Transactions | `data/raw/square_item_sales_detail_24mo.csv` | CSV | **970,838** | 22 |
| Raw Event Calendar | `data/raw/02_ground_truth_event_calendar.csv` | CSV | **731** | 10 |

---

## 3. Pipeline Output Summary

| Data Layer | Target File Path | Format(s) | Output Row Count | Column Count | Rejected Rows |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Staging Layer** | `data/staging/square_sales_staging.csv` | CSV & Parquet | **970,838** | 24 | 0 |
| **Processed Layer** | `data/processed/fact_sales_processed.csv` | CSV & Parquet | **970,838** | 30 | 0 |
| **Rejects Log** | `data/processed/sales_rejected_records.csv` | CSV | **0** | 0 | N/A |

---

## 4. Transformations Performed

1. **Column Standardization**: Transformed 22 PascalCase/Space-separated raw column headers into standardized `snake_case` database field names.
2. **Store & Location Parsing**: Parsed raw `"Store XX - CityName"` values (e.g. `Store 01 - Austin`) into `store_id` (`STORE_01`) and `city` (`Austin`), preserving `location_raw`.
3. **Customer Standardization**: Mapped `NULL` `Customer ID` values to `'CUST_ANONYMOUS'` and created `customer_type` (`"Identified"` for 336,445 lines vs `"Anonymous"` for 634,393 lines).
4. **Event Type & Refund Flagging**: Flagged `is_refund = True` for 9,449 `Refund` event records (`Qty = -1`), maintaining original signed financial conventions.
5. **Date Standardization**: Standardized `transaction_date` (`YYYY-MM-DD`) and `transaction_datetime` (`YYYY-MM-DD HH:MM`). Bounds confirmed within `2024-01-01` to `2025-12-31`.
6. **Financial Transformations**:
   - `cogs` = `qty * unit_cost` (negative for refunds)
   - `discount_amount` = `ABS(discounts)` (positive reporting metric)
   - `gross_margin_pct` = `gross_profit / net_sales` (0.0 if `net_sales == 0`)
   - `discount_rate_pct` = `discount_amount / ABS(gross_sales)` (0.0 if `gross_sales == 0`)

---

## 5. Post-ETL Quality Validation Results

| Assertion Test | Rule Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Row Count Preservation** | Processed rows must equal raw input rows | 970,838 rows | 970,838 rows | **PASSED** |
| **Business Key Uniqueness** | `(transaction_id, sku, event_type)` must be unique | 0 duplicates | 0 duplicates | **PASSED** |
| **Gross Sales Reconciliation** | `gross_sales == qty * unit_price` ($0.01 tol) | 100.00% pass | 100.00% pass | **PASSED** |
| **Net Sales Reconciliation** | `net_sales == gross_sales + discounts` ($0.01 tol) | 100.00% pass | 100.00% pass | **PASSED** |
| **Gross Profit Reconciliation** | `gross_profit == net_sales - cogs` ($0.01 tol) | 100.00% pass | 100.00% pass | **PASSED** |
| **Date Range Validation** | Dates must span 2024-01-01 to 2025-12-31 | 2024-01-01 .. 2025-12-31 | 2024-01-01 .. 2025-12-31 | **PASSED** |
| **Store Parsing Validation** | All stores must yield valid `STORE_XX` codes | 30 unique stores | 30 unique stores | **PASSED** |

---

## 6. Idempotency Test Result

The ETL pipeline was executed twice sequentially:
- **Run 1 Duration**: 29.62 seconds (Produced 970,838 processed rows)
- **Run 2 Duration**: 28.87 seconds (Produced 970,838 processed rows)
- **Idempotency Verification**: Running the pipeline multiple times produced identical row counts, zero duplicate keys, zero file corruption, and zero raw file alterations.

---

## 7. Pytest Validation Suite Result

Executed existing contract validation test suite:
```bash
python -m pytest tests/test_quality.py -v
```
- **Total Tests**: 15
- **Passed**: **15 passed in 5.02 seconds**
- **Failed**: **0**

---

## 8. Summary & Final Status

**FINAL STATUS: SUCCESSFUL & APPROVED FOR TASK 7**  
The staging and processed data layers have been populated at `data/staging/` and `data/processed/` with 100% data integrity, zero lost records, and full alignment with the approved Data Contract.
