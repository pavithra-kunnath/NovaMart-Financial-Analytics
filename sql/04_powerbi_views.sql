-- =====================================================================
-- NovaMart Retail Financial Analytics & Revenue Forecasting
-- Power BI Model Views & Forecast Table Definition (04_powerbi_views.sql)
-- Schema: novamart
-- =====================================================================

SET search_path TO novamart, public;

-- ---------------------------------------------------------------------
-- 1. FACT_FORECAST TABLE
-- Isolated table storing 6-month Seasonal Naive revenue predictions (Jan 2026 - Jun 2026)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS novamart.fact_forecast (
    forecast_key            SERIAL PRIMARY KEY,
    date_key                INTEGER NOT NULL REFERENCES novamart.dim_date(date_key),
    forecast_month          VARCHAR(7) NOT NULL, -- Format YYYY-MM
    forecast_date           DATE NOT NULL,
    forecast_net_revenue    NUMERIC(12,2) NOT NULL CHECK (forecast_net_revenue >= 0),
    lower_bound_95          NUMERIC(12,2) NOT NULL,
    upper_bound_95          NUMERIC(12,2) NOT NULL,
    model_name              VARCHAR(50) NOT NULL,
    forecast_run_date       DATE NOT NULL,
    created_at              TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_fact_forecast_month UNIQUE (forecast_month)
);

COMMENT ON TABLE novamart.fact_forecast IS 'Stores official 6-month Seasonal Naive forward forecasts and 95% prediction bounds.';

-- ---------------------------------------------------------------------
-- 2. VW_PBI_FACT_SALES
-- Power BI optimized sales fact view
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW novamart.vw_pbi_fact_sales AS
SELECT 
    sales_key,
    transaction_id,
    sku,
    event_type,
    date_key,
    customer_key,
    product_key,
    store_key,
    transaction_datetime,
    transaction_date,
    qty,
    unit_price,
    gross_sales,
    discounts,
    discount_amount,
    net_sales,
    unit_cost,
    cogs,
    gross_profit,
    gross_margin_pct,
    discount_rate_pct,
    tax,
    total_collected,
    is_refund
FROM novamart.fact_sales;

COMMENT ON VIEW novamart.vw_pbi_fact_sales IS 'Direct Power BI source view for fact_sales.';

-- ---------------------------------------------------------------------
-- 3. VW_PBI_FACT_FORECAST
-- Power BI optimized forecast fact view
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW novamart.vw_pbi_fact_forecast AS
SELECT 
    forecast_key,
    date_key,
    forecast_month,
    forecast_date,
    forecast_net_revenue,
    lower_bound_95,
    upper_bound_95,
    model_name,
    forecast_run_date
FROM novamart.fact_forecast;

COMMENT ON VIEW novamart.vw_pbi_fact_forecast IS 'Direct Power BI source view for fact_forecast.';
