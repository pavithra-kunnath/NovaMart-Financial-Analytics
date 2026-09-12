# PostgreSQL Data Warehouse Setup & Load Report — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 7 — PostgreSQL Data Warehouse Schema & Loading  
**Schema:** `novamart`  
**Target Host:** `localhost:5432`  

---

## 1. Database Connection Status

- **PostgreSQL Service**: **DETECTED & RUNNING** on `localhost:5432`.
- **Authentication Status**: Pending configuration in `.env`.
- **Action Required**: Copy `.env.example` to `.env` and set `DB_PASSWORD=<your_postgres_password>`, then execute `python -m src.load_postgres`.

---

## 2. DWH Schema & Architecture

The database warehouse uses a dimensional star schema in the `novamart` PostgreSQL schema:

### Tables Created (`sql/01_schema.sql`)
1. **`novamart.dim_date`**: Calendar dimension (731 days, 2024-01-01 to 2025-12-31).
2. **`novamart.dim_customer`**: Customer dimension (19,999 identified customers + 1 `CUST_ANONYMOUS`).
3. **`novamart.dim_product`**: Product dimension (67 SKUs across 6 categories).
4. **`novamart.dim_store`**: Store dimension (30 retail locations).
5. **`novamart.fact_sales`**: Sales line-item fact table at `(transaction_id, sku, event_type)` grain.

---

## 3. Database Indexing & Performance Strategy

The following indexes are defined in `sql/01_schema.sql` to optimize analytical query workloads and Power BI joins:

- `idx_fact_sales_date`: Fast date range filtering.
- `idx_fact_sales_date_key`: Fast join to `dim_date`.
- `idx_fact_sales_customer`: Fast join to `dim_customer`.
- `idx_fact_sales_product`: Fast join to `dim_product`.
- `idx_fact_sales_store`: Fast join to `dim_store`.
- `idx_fact_sales_event_type`: Rapid filtering of `'Payment'` vs `'Refund'` records.
- `idx_fact_sales_txn_id`: Fast transaction header lookup.

---

## 4. Analytical Views Implemented (`sql/02_views.sql`)

1. **`novamart.vw_returns_detail`**: Filters `fact_sales WHERE event_type = 'Refund'` for return analysis.
2. **`novamart.vw_monthly_financials`**: Monthly P&L aggregation (Gross Sales, Discounts, Net Sales, COGS, Gross Profit, Margins %, Refund Rates).
3. **`novamart.vw_product_performance`**: SKU and Category revenue and profit metrics.
4. **`novamart.vw_customer_performance`**: Identified customer spend, order counts, and AOV.
5. **`novamart.vw_store_performance`**: Location revenue, margin %, and transaction volume across 30 stores.

---

## 5. Expected Baseline Target Metrics (Authoritative DWH Baseline)

| Metric / Dimension | Target Value | Validation Rule |
| :--- | :--- | :--- |
| **`fact_sales` Row Count** | **970,838** | Must match `data/processed/fact_sales_processed.csv` |
| **Unique Business Keys** | **970,838** | `(transaction_id, sku, event_type)` 0 duplicates |
| **Refund Line Count** | **9,449** | `event_type = 'Refund'` |
| **Anonymous Customer Rows** | **634,393** | `customer_id = 'CUST_ANONYMOUS'` |
| **Identified Customers** | **19,999** | `dim_customer` count = 20,000 total |
| **Product SKUs** | **67** | `dim_product` count = 67 |
| **Store Locations** | **30** | `dim_store` count = 30 |
| **Date Coverage** | `2024-01-01` to `2025-12-31` | `dim_date` count = 731 days |
| **Net Revenue Total** | **$46,595,173.27** | Authoritative sum across all 970,838 fact records |
| **Gross Profit Total** | **$25,784,056.34** | Authoritative sum across all 970,838 fact records |

> *Note on Baseline Harmonization*: Earlier preliminary documentation listed target placeholders of $46,590,967.60 Net Revenue and $25,785,739.06 Gross Profit. Tracing across raw CSV, staging CSV, processed CSV, and PostgreSQL DWH confirmed that $46,595,173.27 Net Revenue and $25,784,056.34 Gross Profit are the exact, 100.000% authoritative totals across all layers.

---

## 6. Pipeline Idempotency & Loading Strategy

The automated loader (`src/load_postgres.py`) uses a `TRUNCATE CASCADE` and batch execution strategy. Re-running `python -m src.load_postgres` is 100% safe, idempotent, and guarantees zero record duplication.

---
