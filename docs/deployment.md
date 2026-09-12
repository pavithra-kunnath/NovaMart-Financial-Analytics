# Deployment & PostgreSQL Setup Guide — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 7 — PostgreSQL Data Warehouse Deployment  

---

## 1. Prerequisites

- **PostgreSQL Database Server** (v13+ recommended) running on `localhost:5432` or remote host.
- **Python 3.11+** environment with packages declared in `requirements.txt` (`psycopg2-binary`, `pandas`, `python-dotenv`).

---

## 2. Environment Configuration

1. Copy `.env.example` to `.env` in the repository root directory:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` to configure your PostgreSQL credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=novamart_db
   DB_USER=postgres
   DB_PASSWORD=your_actual_password_here
   LOG_LEVEL=INFO
   ```
   *> Note: `.env` is listed in `.gitignore` and must never be committed to source control.*

---

## 3. Database & Schema Creation

1. Ensure the PostgreSQL database `novamart_db` exists:
   ```sql
   CREATE DATABASE novamart_db;
   ```

2. Apply DDL schema manually or allow the automated loader to execute `sql/01_schema.sql`:
   ```bash
   psql -h localhost -U postgres -d novamart_db -f sql/01_schema.sql
   ```

---

## 4. Pipeline Execution & Data Loading

Run the automated PostgreSQL loader module:

```bash
python -m src.load_postgres
```

The loader automatically:
1. Verifies database connectivity.
2. Applies DDL schemas (`sql/01_schema.sql`).
3. Truncates target tables for clean, idempotent execution.
4. Generates and loads `dim_date` (731 days spanning 2024-01-01 to 2025-12-31).
5. Populates `dim_customer` (19,999 identified + 1 `CUST_ANONYMOUS`).
6. Populates `dim_product` (67 SKUs across 6 categories).
7. Populates `dim_store` (30 retail locations).
8. Maps surrogate keys and loads `fact_sales` (970,838 transaction line records).
9. Creates reporting views (`sql/02_views.sql`).
10. Executes database-level reconciliation assertions.

---

## 5. Rerun Procedure & Idempotency

The PostgreSQL load pipeline uses a `TRUNCATE CASCADE` and batch reload pattern. Executing `python -m src.load_postgres` multiple times is **100% idempotent**:
- No duplicate dimension records are created.
- No duplicate fact records are created.
- Business key uniqueness `(transaction_id, sku, event_type)` is strictly enforced.
- Financial totals reconcile perfectly on every run.

---

## 6. Verification Queries

Run validation queries in `psql` or your SQL editor:

```sql
SET search_path TO novamart, public;

-- Verify fact row count
SELECT COUNT(*) FROM fact_sales; -- Expected: 970,838

-- Verify refund count
SELECT COUNT(*) FROM fact_sales WHERE event_type = 'Refund'; -- Expected: 9,449

-- Verify anonymous customer transactions
SELECT COUNT(*) FROM fact_sales f 
JOIN dim_customer c ON f.customer_key = c.customer_key 
WHERE c.customer_id = 'CUST_ANONYMOUS'; -- Expected: 634,393

-- Verify business key uniqueness
SELECT COUNT(DISTINCT (transaction_id, sku, event_type)) FROM fact_sales; -- Expected: 970,838
```

---
