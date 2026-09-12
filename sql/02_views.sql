-- =====================================================================
-- NovaMart Retail Financial Analytics & Revenue Forecasting
-- SQL Analytical Views Definition (02_views.sql)
-- Schema: novamart
-- =====================================================================

SET search_path TO novamart, public;

-- ---------------------------------------------------------------------
-- 1. VW_RETURNS_DETAIL
-- Detailed line-item view for all refund/return transactions
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW novamart.vw_returns_detail AS
SELECT 
    f.sales_key,
    f.transaction_id,
    f.transaction_date,
    f.transaction_datetime,
    p.sku,
    p.item,
    p.category,
    s.store_id,
    s.city,
    c.customer_id,
    c.customer_type,
    f.qty,
    f.unit_price,
    f.gross_sales,
    f.discounts,
    f.net_sales,
    f.unit_cost,
    f.cogs,
    f.gross_profit,
    f.tax,
    f.total_collected
FROM novamart.fact_sales f
JOIN novamart.dim_product p ON f.product_key = p.product_key
JOIN novamart.dim_store s ON f.store_key = s.store_key
JOIN novamart.dim_customer c ON f.customer_key = c.customer_key
WHERE f.event_type = 'Refund';

COMMENT ON VIEW novamart.vw_returns_detail IS 'Exposes all return transactions with full dimensional context.';

-- ---------------------------------------------------------------------
-- 2. VW_MONTHLY_FINANCIALS
-- Monthly aggregate P&L summary and financial metrics
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW novamart.vw_monthly_financials AS
SELECT 
    d.year_month,
    COUNT(f.sales_key) AS line_items,
    COUNT(DISTINCT f.transaction_id) AS unique_transactions,
    SUM(f.qty) AS total_quantity,
    SUM(f.gross_sales) AS gross_sales,
    SUM(f.discount_amount) AS discount_amount,
    SUM(f.net_sales) AS net_sales,
    SUM(f.cogs) AS cogs,
    SUM(f.gross_profit) AS gross_profit,
    CASE 
        WHEN SUM(f.net_sales) <> 0 THEN ROUND(SUM(f.gross_profit) / SUM(f.net_sales), 4)
        ELSE 0.0000 
    END AS gross_margin_pct,
    SUM(CASE WHEN f.event_type = 'Refund' THEN ABS(f.net_sales) ELSE 0 END) AS refund_amount,
    ROUND(
        (SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END)::NUMERIC / COUNT(f.sales_key)::NUMERIC) * 100, 
        2
    ) AS refund_rate_pct
FROM novamart.fact_sales f
JOIN novamart.dim_date d ON f.date_key = d.date_key
GROUP BY d.year_month
ORDER BY d.year_month;

COMMENT ON VIEW novamart.vw_monthly_financials IS 'Monthly financial aggregation for P&L reporting and revenue forecasting.';

-- ---------------------------------------------------------------------
-- 3. VW_PRODUCT_PERFORMANCE
-- Product-level revenue, gross profit, and return performance
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW novamart.vw_product_performance AS
SELECT 
    p.sku,
    p.item,
    p.category,
    p.price_point_name,
    p.unit_price,
    p.unit_cost,
    COUNT(f.sales_key) AS line_items_sold,
    SUM(f.qty) AS total_units_sold,
    SUM(f.gross_sales) AS gross_sales,
    SUM(f.discount_amount) AS discount_amount,
    SUM(f.net_sales) AS net_sales,
    SUM(f.cogs) AS cogs,
    SUM(f.gross_profit) AS gross_profit,
    CASE 
        WHEN SUM(f.net_sales) <> 0 THEN ROUND(SUM(f.gross_profit) / SUM(f.net_sales), 4)
        ELSE 0.0000 
    END AS gross_margin_pct,
    SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_lines,
    ROUND(
        (SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END)::NUMERIC / COUNT(f.sales_key)::NUMERIC) * 100, 
        2
    ) AS refund_rate_pct
FROM novamart.fact_sales f
JOIN novamart.dim_product p ON f.product_key = p.product_key
GROUP BY p.sku, p.item, p.category, p.price_point_name, p.unit_price, p.unit_cost;

COMMENT ON VIEW novamart.vw_product_performance IS 'Product and category level financial performance metrics.';

-- ---------------------------------------------------------------------
-- 4. VW_CUSTOMER_PERFORMANCE
-- Performance analytics for identified customer segments
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW novamart.vw_customer_performance AS
SELECT 
    c.customer_id,
    c.customer_type,
    COUNT(DISTINCT f.transaction_id) AS total_orders,
    COUNT(f.sales_key) AS total_line_items,
    SUM(f.qty) AS total_units_purchased,
    SUM(f.net_sales) AS total_spend_net,
    SUM(f.gross_profit) AS total_profit_contributed,
    ROUND(SUM(f.net_sales) / NULLIF(COUNT(DISTINCT f.transaction_id), 0), 2) AS average_order_value,
    SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END) AS total_refunds
FROM novamart.fact_sales f
JOIN novamart.dim_customer c ON f.customer_key = c.customer_key
WHERE c.customer_type = 'Identified'
GROUP BY c.customer_id, c.customer_type;

COMMENT ON VIEW novamart.vw_customer_performance IS 'Metrics for identified customer segments (AOV, Total Spend, Profit).';

-- ---------------------------------------------------------------------
-- 5. VW_STORE_PERFORMANCE
-- Store location performance analytics
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW novamart.vw_store_performance AS
SELECT 
    s.store_id,
    s.store_name,
    s.city,
    COUNT(DISTINCT f.transaction_id) AS total_transactions,
    COUNT(f.sales_key) AS total_line_items,
    SUM(f.gross_sales) AS gross_sales,
    SUM(f.discount_amount) AS total_discounts,
    SUM(f.net_sales) AS net_sales,
    SUM(f.cogs) AS total_cogs,
    SUM(f.gross_profit) AS gross_profit,
    CASE 
        WHEN SUM(f.net_sales) <> 0 THEN ROUND(SUM(f.gross_profit) / SUM(f.net_sales), 4)
        ELSE 0.0000 
    END AS gross_margin_pct,
    ROUND(
        (SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END)::NUMERIC / COUNT(f.sales_key)::NUMERIC) * 100, 
        2
    ) AS refund_rate_pct
FROM novamart.fact_sales f
JOIN novamart.dim_store s ON f.store_key = s.store_key
GROUP BY s.store_id, s.store_name, s.city;

COMMENT ON VIEW novamart.vw_store_performance IS 'Store-level financial performance metrics across 30 locations.';
