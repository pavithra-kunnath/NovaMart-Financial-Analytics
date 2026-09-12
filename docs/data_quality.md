# Data Quality Testing Documentation — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 5 — Automated Data-Quality Tests  
**Test Suite File:** `tests/test_quality.py`  
**Scope:** Source / Raw Layer Data Validation (`data/raw/`)  

---

## 1. Purpose of Automated Data-Quality Testing

The automated data-quality test suite enforces contract-level assertion testing against landed datasets before any ETL transformations or warehouse ingestion occur. The goal is to detect upstream schema drifts, missing fields, arithmetic calculation discrepancies, invalid date values, or broken key uniqueness rules before bad data can corrupt downstream database tables, analytics views, or revenue forecasting models.

---

## 2. Test Framework & Architecture

- **Test Runner:** `pytest`
- **Data Engine:** `pandas`, `numpy`
- **Design Pattern:** Session-scoped fixtures (`sales_df`, `calendar_df`) load raw datasets into memory once per test execution run, maximizing performance over large datasets (~970k rows).
- **Rule Enforcement:** Tests raise explicit `AssertionError` failures upon contract violations. No automatic data cleaning or silent repairs occur inside the test suite.

---

## 3. Validation Layers

| Layer | Target Location | Purpose & Validation Scope | Status |
| :--- | :--- | :--- | :--- |
| **RAW Validation** | `data/raw/` | Validates file existence, schema completeness, non-null required fields, event types, business key uniqueness, and formula reconciliation on raw POS CSV exports. | **ACTIVE (Task 5)** |
| **STAGING Validation** | `data/staging/` | Validates parsed store IDs, city fields, customer ID default mappings (`CUST_ANONYMOUS`), and data type casting. | *Future Phase (Task 6)* |
| **PROCESSED / DWH Validation**| PostgreSQL DWH | Validates foreign key referential integrity, surrogate key uniqueness, and aggregated fact vs dimension grain matching. | *Future Phase (Task 7)* |

---

## 4. Summary of Data Contract Rules Tested

### A. Dataset & Schema Verification
- `test_source_files_exist`: Confirms `square_item_sales_detail_24mo.csv` and `02_ground_truth_event_calendar.csv` exist.
- `test_datasets_not_empty`: Asserts exactly 970,838 sales rows and 731 calendar rows.
- `test_expected_columns_exist`: Asserts exact 22 sales columns and 10 calendar columns.

### B. Nullability & Customer ID Handling
- `test_required_fields_not_null`: Asserts 0 nulls across 21 required columns (`Transaction ID`, `SKU`, `Item`, `Category`, `Location`, `Event Type`, `Qty`, `Unit Price`, `Gross Sales`, `Discounts`, `Net Sales`, `Tax`, `Total Collected`, `Unit Cost`, `Gross Profit`, etc.).
- `test_customer_id_allows_nulls`: Confirms `Customer ID` permits `NULL` values and asserts exactly 634,393 null rows (65.34%) for guest/anonymous transactions.

### C. Business Key Uniqueness
- `test_business_key_uniqueness`: Asserts zero duplicate combinations for `Transaction ID` + `SKU` + `Event Type` across all 970,838 rows.

### D. Event Type & Dates
- `test_event_type_values`: Confirms `Event Type` contains ONLY `'Payment'` and `'Refund'`.
- `test_date_validity_and_bounds`: Confirms all dates parse correctly and span `2024-01-01` to `2025-12-31`.

### E. Financial Reconciliation & Sign Conventions
- `test_financial_reconciliation_formulas`: Asserts $0.01 tolerance for:
  - $\text{Gross Sales} == \text{Qty} \times \text{Unit Price}$
  - $\text{Net Sales} == \text{Gross Sales} + \text{Discounts}$
  - $\text{Gross Profit} == \text{Net Sales} - (\text{Qty} \times \text{Unit Cost})$
- `test_discount_sign_and_bounds`: Confirms raw `Discounts <= 0.00`.
- `test_refund_negative_conventions`: Confirms `Event Type = 'Refund'` rows carry `Qty = -1` and negative values for `Gross Sales`, `Net Sales`, `Tax`, and `Gross Profit`.

### F. Location & Product Validation
- `test_location_format_and_parsing`: Confirms `Location` strings follow `"Store XX - CityName"`.
- `test_category_and_product_validity`: Confirms 6 valid categories, 67 SKUs, and 32 Item descriptions.

---

## 5. How to Run the Test Suite

Execute `pytest` from the project root directory:

```bash
pytest tests/test_quality.py -v
```

To run with short summary output:
```bash
pytest tests/test_quality.py -q
```

---

## 6. Failure Triage Procedure

If a test fails during execution:

1. **Do NOT modify raw data** in `data/raw/` to force a test to pass.
2. Inspect the `AssertionError` log output to identify the exact failing row(s) and column(s).
3. Determine whether the failure represents:
   - **Upstream Data Corruption** (e.g. invalid date format, missing required column): Report issue to data engineering source team.
   - **Flawed Test Assumption**: If the test logic contradicts the approved Data Contract (`docs/data_contract.md`), update the test file to align with the contract.

---
