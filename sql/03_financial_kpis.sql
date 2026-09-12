-- =====================================================================
-- NovaMart Retail Financial Analytics & Revenue Forecasting
-- Task 8: SQL Financial KPI Reference Queries (sql/03_financial_kpis.sql)
-- Schema: novamart
-- Database: novamart_db
-- =====================================================================

SET search_path TO novamart, public;

-- ---------------------------------------------------------------------
-- 1. OVERALL PORTFOLIO FINANCIAL SUMMARY (KPI DASHBOARD REFERENCE)
-- Computes core portfolio KPIs: Gross Sales, Discounts, Net Revenue, COGS,
-- Gross Profit, Margins %, Discount Rate %, Refund Impact, and AOV.
-- ---------------------------------------------------------------------
SELECT 
    COUNT(sales_key) AS total_line_items,
    COUNT(DISTINCT transaction_id) AS total_transactions,
    SUM(qty) AS total_units_moved,
    SUM(gross_sales) AS total_gross_sales,
    SUM(discount_amount) AS total_discounts,
    SUM(net_sales) AS total_net_revenue,
    SUM(cogs) AS total_cogs,
    SUM(gross_profit) AS total_gross_profit,
    ROUND((SUM(gross_profit) / SUM(net_sales)) * 100, 2) AS gross_margin_pct,
    ROUND((SUM(discount_amount) / SUM(gross_sales)) * 100, 2) AS overall_discount_rate_pct,
    SUM(CASE WHEN event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_lines_count,
    SUM(CASE WHEN event_type = 'Refund' THEN ABS(net_sales) ELSE 0 END) AS total_refund_amount,
    ROUND((SUM(CASE WHEN event_type = 'Refund' THEN 1 ELSE 0 END)::NUMERIC / COUNT(sales_key)::NUMERIC) * 100, 2) AS overall_refund_rate_pct,
    ROUND(SUM(net_sales) / NULLIF(COUNT(DISTINCT transaction_id), 0), 2) AS average_order_value_aov
FROM novamart.fact_sales;


-- ---------------------------------------------------------------------
-- 2. MONTH-OVER-MONTH (MoM) REVENUE & PROFIT GROWTH RATES
-- Calculates month-over-month growth percentage for Net Revenue and Gross Profit.
-- ---------------------------------------------------------------------
WITH monthly AS (
    SELECT 
        d.year_month,
        SUM(f.net_sales) AS net_sales,
        SUM(f.gross_profit) AS gross_profit
    FROM novamart.fact_sales f
    JOIN novamart.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year_month
)
SELECT 
    year_month,
    net_sales,
    LAG(net_sales) OVER (ORDER BY year_month) AS prev_month_net_sales,
    ROUND(
        ((net_sales - LAG(net_sales) OVER (ORDER BY year_month)) / NULLIF(LAG(net_sales) OVER (ORDER BY year_month), 0)) * 100, 
        2
    ) AS mom_net_sales_growth_pct,
    gross_profit,
    ROUND(
        ((gross_profit - LAG(gross_profit) OVER (ORDER BY year_month)) / NULLIF(LAG(gross_profit) OVER (ORDER BY year_month), 0)) * 100, 
        2
    ) AS mom_gross_profit_growth_pct
FROM monthly
ORDER BY year_month;


-- ---------------------------------------------------------------------
-- 3. YEAR-OVER-YEAR (YoY) MONTHLY COMPARISON (2024 vs 2025)
-- Compares identical calendar months across fiscal years 2024 and 2025.
-- ---------------------------------------------------------------------
WITH monthly AS (
    SELECT 
        d.year,
        d.month_number,
        d.month_name,
        SUM(f.net_sales) AS net_sales,
        SUM(f.gross_profit) AS gross_profit
    FROM novamart.fact_sales f
    JOIN novamart.dim_date d ON f.date_key = d.date_key
    GROUP BY d.year, d.month_number, d.month_name
)
SELECT 
    m2024.month_number,
    m2024.month_name,
    m2024.net_sales AS sales_2024,
    m2025.net_sales AS sales_2025,
    ROUND(((m2025.net_sales - m2024.net_sales) / m2024.net_sales) * 100, 2) AS yoy_sales_growth_pct,
    m2024.gross_profit AS gp_2024,
    m2025.gross_profit AS gp_2025,
    ROUND(((m2025.gross_profit - m2024.gross_profit) / m2024.gross_profit) * 100, 2) AS yoy_gp_growth_pct
FROM monthly m2024
JOIN monthly m2025 ON m2024.month_number = m2025.month_number AND m2024.year = 2024 AND m2025.year = 2025
ORDER BY m2024.month_number;


-- ---------------------------------------------------------------------
-- 4. 24-MONTH DETAILED FINANCIAL TREND
-- Comprehensive monthly P&L view covering all 24 months in the dataset.
-- ---------------------------------------------------------------------
SELECT 
    d.year,
    d.month_number,
    d.year_month,
    SUM(f.gross_sales) AS gross_sales,
    SUM(f.discount_amount) AS discounts,
    SUM(f.net_sales) AS net_revenue,
    SUM(f.cogs) AS cogs,
    SUM(f.gross_profit) AS gross_profit,
    ROUND((SUM(f.gross_profit) / SUM(f.net_sales)) * 100, 2) AS gross_margin_pct,
    SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_count,
    SUM(CASE WHEN f.event_type = 'Refund' THEN ABS(f.net_sales) ELSE 0 END) AS refund_amount
FROM novamart.fact_sales f
JOIN novamart.dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month_number, d.year_month
ORDER BY d.year_month;


-- ---------------------------------------------------------------------
-- 5. CATEGORY PROFITABILITY ANALYSIS
-- Evaluates financial contribution and margins across 6 product categories.
-- ---------------------------------------------------------------------
SELECT 
    p.category,
    COUNT(f.sales_key) AS line_items,
    SUM(f.qty) AS units_sold,
    SUM(f.gross_sales) AS gross_sales,
    SUM(f.discount_amount) AS discounts,
    SUM(f.net_sales) AS net_revenue,
    SUM(f.cogs) AS cogs,
    SUM(f.gross_profit) AS gross_profit,
    ROUND((SUM(f.gross_profit) / SUM(f.net_sales)) * 100, 2) AS gross_margin_pct,
    ROUND((SUM(f.discount_amount) / SUM(f.gross_sales)) * 100, 2) AS discount_rate_pct,
    SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_lines,
    SUM(CASE WHEN f.event_type = 'Refund' THEN ABS(f.net_sales) ELSE 0 END) AS refund_amount
FROM novamart.fact_sales f
JOIN novamart.dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY net_revenue DESC;


-- ---------------------------------------------------------------------
-- 6A. PRODUCT PERFORMANCE: TOP 10 REVENUE LEADERS
-- ---------------------------------------------------------------------
SELECT 
    p.sku,
    p.item,
    p.category,
    SUM(f.qty) AS units_sold,
    SUM(f.net_sales) AS net_revenue,
    SUM(f.cogs) AS cogs,
    SUM(f.gross_profit) AS gross_profit,
    ROUND((SUM(f.gross_profit) / SUM(f.net_sales)) * 100, 2) AS gross_margin_pct,
    SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_lines
FROM novamart.fact_sales f
JOIN novamart.dim_product p ON f.product_key = p.product_key
GROUP BY p.sku, p.item, p.category
ORDER BY net_revenue DESC
LIMIT 10;


-- ---------------------------------------------------------------------
-- 6B. PRODUCT PERFORMANCE: TOP 10 HIGHEST RETURNED SKUS BY COUNT
-- ---------------------------------------------------------------------
SELECT 
    p.sku,
    p.item,
    p.category,
    SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_lines,
    SUM(CASE WHEN f.event_type = 'Refund' THEN ABS(f.net_sales) ELSE 0 END) AS refund_amount,
    COUNT(f.sales_key) AS total_line_items,
    ROUND((SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END)::NUMERIC / COUNT(f.sales_key)::NUMERIC) * 100, 2) AS refund_rate_pct
FROM novamart.fact_sales f
JOIN novamart.dim_product p ON f.product_key = p.product_key
GROUP BY p.sku, p.item, p.category
ORDER BY refund_lines DESC
LIMIT 10;


-- ---------------------------------------------------------------------
-- 7. STORE LOCATION FINANCIAL PERFORMANCE
-- Evaluates revenue, profit, margin %, and transaction volume across all 30 stores.
-- ---------------------------------------------------------------------
SELECT 
    s.store_id,
    s.store_name,
    s.city,
    COUNT(DISTINCT f.transaction_id) AS total_transactions,
    COUNT(f.sales_key) AS line_items,
    SUM(f.gross_sales) AS gross_sales,
    SUM(f.discount_amount) AS total_discounts,
    SUM(f.net_sales) AS net_revenue,
    SUM(f.cogs) AS cogs,
    SUM(f.gross_profit) AS gross_profit,
    ROUND((SUM(f.gross_profit) / SUM(f.net_sales)) * 100, 2) AS gross_margin_pct,
    ROUND(SUM(f.net_sales) / NULLIF(COUNT(DISTINCT f.transaction_id), 0), 2) AS average_order_value_aov,
    ROUND((SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END)::NUMERIC / COUNT(f.sales_key)::NUMERIC) * 100, 2) AS refund_rate_pct
FROM novamart.fact_sales f
JOIN novamart.dim_store s ON f.store_key = s.store_key
GROUP BY s.store_id, s.store_name, s.city
ORDER BY net_revenue DESC;


-- ---------------------------------------------------------------------
-- 8. CUSTOMER SEGMENT PERFORMANCE (IDENTIFIED VS ANONYMOUS GUESTS)
-- Compares identified registered customers against anonymous walk-in purchases.
-- ---------------------------------------------------------------------
SELECT 
    c.customer_type,
    COUNT(DISTINCT c.customer_id) AS distinct_customers,
    COUNT(DISTINCT f.transaction_id) AS total_orders,
    COUNT(f.sales_key) AS line_items,
    SUM(f.qty) AS units_sold,
    SUM(f.gross_sales) AS gross_sales,
    SUM(f.discount_amount) AS total_discounts,
    SUM(f.net_sales) AS net_revenue,
    SUM(f.cogs) AS cogs,
    SUM(f.gross_profit) AS gross_profit,
    ROUND((SUM(f.gross_profit) / SUM(f.net_sales)) * 100, 2) AS gross_margin_pct,
    ROUND(SUM(f.net_sales) / NULLIF(COUNT(DISTINCT f.transaction_id), 0), 2) AS average_order_value_aov,
    SUM(CASE WHEN f.event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_count
FROM novamart.fact_sales f
JOIN novamart.dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_type;


-- ---------------------------------------------------------------------
-- 9. REFUND & RETURN FINANCIAL IMPACT ANALYSIS
-- Isolated analysis of return transactions by event_type.
-- ---------------------------------------------------------------------
SELECT 
    event_type,
    COUNT(sales_key) AS total_records,
    SUM(qty) AS total_qty,
    SUM(gross_sales) AS gross_sales,
    SUM(discounts) AS signed_discounts,
    SUM(net_sales) AS net_revenue,
    SUM(cogs) AS cogs,
    SUM(gross_profit) AS gross_profit
FROM novamart.fact_sales
GROUP BY event_type;


-- ---------------------------------------------------------------------
-- 10. RECONCILIATION & AGGREGATION INTEGRITY CHECK
-- Asserts row counts, total net sales, and duplicate key safety.
-- ---------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_fact_rows,
    COUNT(DISTINCT (transaction_id, sku, event_type)) AS unique_business_keys,
    SUM(net_sales) AS total_net_revenue,
    SUM(gross_profit) AS total_gross_profit
FROM novamart.fact_sales;
