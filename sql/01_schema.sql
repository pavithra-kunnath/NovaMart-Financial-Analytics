-- =====================================================================
-- NovaMart Retail Financial Analytics & Revenue Forecasting
-- PostgreSQL DWH Schema Definition (01_schema.sql)
-- Schema: novamart
-- =====================================================================

CREATE SCHEMA IF NOT EXISTS novamart;

-- Set search path
SET search_path TO novamart, public;

-- ---------------------------------------------------------------------
-- 1. DIM_DATE
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS novamart.dim_date (
    date_key        INTEGER NOT NULL PRIMARY KEY, -- Format YYYYMMDD
    date            DATE NOT NULL UNIQUE,
    year            INTEGER NOT NULL,
    month_number    INTEGER NOT NULL CHECK (month_number BETWEEN 1 AND 12),
    month_name      VARCHAR(15) NOT NULL,
    quarter         INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    year_month      VARCHAR(7) NOT NULL, -- Format YYYY-MM
    day_of_week     VARCHAR(15) NOT NULL,
    is_weekend      BOOLEAN NOT NULL,
    financial_year  INTEGER NOT NULL
);

COMMENT ON TABLE novamart.dim_date IS 'Calendar dimension covering 2024-2025 fiscal and daily attributes.';

-- ---------------------------------------------------------------------
-- 2. DIM_CUSTOMER
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS novamart.dim_customer (
    customer_key    SERIAL PRIMARY KEY,
    customer_id     VARCHAR(50) NOT NULL UNIQUE,
    customer_type   VARCHAR(20) NOT NULL CHECK (customer_type IN ('Identified', 'Anonymous')),
    created_at      TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE novamart.dim_customer IS 'Customer dimension storing identified customer IDs and default CUST_ANONYMOUS record.';

-- ---------------------------------------------------------------------
-- 3. DIM_PRODUCT
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS novamart.dim_product (
    product_key      SERIAL PRIMARY KEY,
    sku              VARCHAR(50) NOT NULL UNIQUE,
    item             VARCHAR(100) NOT NULL,
    category         VARCHAR(50) NOT NULL,
    price_point_name VARCHAR(50) NOT NULL,
    unit_cost        NUMERIC(10,2) NOT NULL CHECK (unit_cost >= 0),
    unit_price       NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    created_at       TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE novamart.dim_product IS 'Product dimension storing 67 SKUs across 6 categories.';

-- ---------------------------------------------------------------------
-- 4. DIM_STORE
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS novamart.dim_store (
    store_key   SERIAL PRIMARY KEY,
    store_id    VARCHAR(20) NOT NULL UNIQUE,
    store_name  VARCHAR(100) NOT NULL,
    city        VARCHAR(50) NOT NULL,
    created_at  TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE novamart.dim_store IS 'Store dimension storing 30 retail store locations.';

-- ---------------------------------------------------------------------
-- 5. FACT_SALES
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS novamart.fact_sales (
    sales_key            BIGSERIAL PRIMARY KEY,
    transaction_id       VARCHAR(50) NOT NULL,
    sku                  VARCHAR(50) NOT NULL,
    event_type           VARCHAR(20) NOT NULL CHECK (event_type IN ('Payment', 'Refund')),
    date_key             INTEGER NOT NULL REFERENCES novamart.dim_date(date_key),
    customer_key         INTEGER NOT NULL REFERENCES novamart.dim_customer(customer_key),
    product_key          INTEGER NOT NULL REFERENCES novamart.dim_product(product_key),
    store_key            INTEGER NOT NULL REFERENCES novamart.dim_store(store_key),
    transaction_datetime VARCHAR(30) NOT NULL,
    transaction_date     DATE NOT NULL,
    qty                  INTEGER NOT NULL,
    unit_price           NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    gross_sales          NUMERIC(10,2) NOT NULL,
    discounts            NUMERIC(10,2) NOT NULL CHECK (discounts <= 0),
    discount_amount      NUMERIC(10,2) NOT NULL CHECK (discount_amount >= 0),
    net_sales            NUMERIC(10,2) NOT NULL,
    unit_cost            NUMERIC(10,2) NOT NULL CHECK (unit_cost >= 0),
    cogs                 NUMERIC(10,2) NOT NULL,
    gross_profit         NUMERIC(10,2) NOT NULL,
    gross_margin_pct     NUMERIC(6,4) NOT NULL,
    discount_rate_pct    NUMERIC(6,4) NOT NULL,
    tax                  NUMERIC(10,2) NOT NULL,
    total_collected      NUMERIC(10,2) NOT NULL,
    is_refund            BOOLEAN NOT NULL,
    
    -- Composite Business Key Uniqueness Assertion
    CONSTRAINT uq_fact_sales_bk UNIQUE (transaction_id, sku, event_type)
);

COMMENT ON TABLE novamart.fact_sales IS 'POS sales line-item fact table at transaction_id + sku + event_type grain.';

-- ---------------------------------------------------------------------
-- INDEXES FOR ANALYTICAL WORKLOAD PERFORMANCE
-- ---------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_fact_sales_date ON novamart.fact_sales(transaction_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_date_key ON novamart.fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer ON novamart.fact_sales(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON novamart.fact_sales(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_store ON novamart.fact_sales(store_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_event_type ON novamart.fact_sales(event_type);
CREATE INDEX IF NOT EXISTS idx_fact_sales_txn_id ON novamart.fact_sales(transaction_id);
