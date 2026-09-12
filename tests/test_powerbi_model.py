"""
Unit and Integration Tests for Power BI Data Model Foundation & DAX Logic (Task 12).

Validates star schema Integrity, dimension uniqueness, referential integrity (zero orphan keys),
extended calendar coverage (2024-01-01 to 2026-06-30), baseline KPI reconciliations against PostgreSQL,
and fact_forecast table structure and bounds.
"""

import pytest
import pandas as pd
import numpy as np
from src.load_postgres import get_db_connection


def test_fact_sales_row_count_and_business_key():
    """Verify fact_sales row count is exactly 970,838 and composite business keys are unique."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM novamart.fact_sales;")
    fact_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(DISTINCT (transaction_id, sku, event_type)) FROM novamart.fact_sales;")
    unique_bk_count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    assert fact_count == 970838, f"Expected 970,838 fact sales rows, got {fact_count}"
    assert unique_bk_count == 970838, f"Expected 970,838 unique business keys, got {unique_bk_count}"


def test_dimension_table_uniqueness():
    """Verify primary key uniqueness across all dimension tables."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT customer_key) FROM novamart.dim_customer;")
    c_tot, c_uniq = cur.fetchone()
    assert c_tot == c_uniq, "dim_customer customer_key contains duplicates!"
    
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT product_key) FROM novamart.dim_product;")
    p_tot, p_uniq = cur.fetchone()
    assert p_tot == p_uniq, "dim_product product_key contains duplicates!"
    
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT store_key) FROM novamart.dim_store;")
    s_tot, s_uniq = cur.fetchone()
    assert s_tot == s_uniq, "dim_store store_key contains duplicates!"
    
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT date_key) FROM novamart.dim_date;")
    d_tot, d_uniq = cur.fetchone()
    assert d_tot == d_uniq, "dim_date date_key contains duplicates!"
    
    cur.close()
    conn.close()


def test_extended_calendar_coverage():
    """Verify dim_date extends from 2024-01-01 through 2026-06-30 (912 days)."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT MIN(date), MAX(date), COUNT(*) FROM novamart.dim_date;")
    min_d, max_d, total_d = cur.fetchone()
    
    cur.close()
    conn.close()
    
    assert str(min_d) == "2024-01-01", f"Expected min date 2024-01-01, got {min_d}"
    assert str(max_d) == "2026-06-30", f"Expected max date 2026-06-30, got {max_d}"
    assert total_d == 912, f"Expected 912 calendar days, got {total_d}"


def test_referential_integrity_zero_orphan_keys():
    """Verify zero orphan foreign keys exist in fact_sales."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Date key orphan check
    cur.execute("""
        SELECT COUNT(*) FROM novamart.fact_sales f 
        LEFT JOIN novamart.dim_date d ON f.date_key = d.date_key 
        WHERE d.date_key IS NULL;
    """)
    assert cur.fetchone()[0] == 0, "Orphan date_key detected in fact_sales!"
    
    # Customer key orphan check
    cur.execute("""
        SELECT COUNT(*) FROM novamart.fact_sales f 
        LEFT JOIN novamart.dim_customer c ON f.customer_key = c.customer_key 
        WHERE c.customer_key IS NULL;
    """)
    assert cur.fetchone()[0] == 0, "Orphan customer_key detected in fact_sales!"
    
    # Product key orphan check
    cur.execute("""
        SELECT COUNT(*) FROM novamart.fact_sales f 
        LEFT JOIN novamart.dim_product p ON f.product_key = p.product_key 
        WHERE p.product_key IS NULL;
    """)
    assert cur.fetchone()[0] == 0, "Orphan product_key detected in fact_sales!"
    
    # Store key orphan check
    cur.execute("""
        SELECT COUNT(*) FROM novamart.fact_sales f 
        LEFT JOIN novamart.dim_store s ON f.store_key = s.store_key 
        WHERE s.store_key IS NULL;
    """)
    assert cur.fetchone()[0] == 0, "Orphan store_key detected in fact_sales!"
    
    cur.close()
    conn.close()


def test_baseline_kpi_reconciliation():
    """Verify financial DAX / SQL measures match authoritative project baseline targets."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            ROUND(SUM(gross_sales), 2) AS gross_sales,
            ROUND(SUM(discounts), 2) AS discounts_signed,
            ROUND(SUM(discount_amount), 2) AS discount_amount,
            ROUND(SUM(net_sales), 2) AS net_revenue,
            ROUND(SUM(cogs), 2) AS cogs,
            ROUND(SUM(gross_profit), 2) AS gross_profit,
            ROUND(SUM(gross_profit) / SUM(net_sales) * 100, 4) AS gross_margin_pct,
            ROUND(SUM(discount_amount) / SUM(gross_sales) * 100, 4) AS discount_rate_pct,
            SUM(qty) AS total_units,
            COUNT(DISTINCT transaction_id) AS distinct_transactions,
            ROUND(SUM(net_sales) / COUNT(DISTINCT transaction_id), 2) AS aov
        FROM novamart.fact_sales;
    """)
    r = cur.fetchone()
    cur.close()
    conn.close()
    
    gross_sales, disc_signed, disc_amt, net_rev, cogs, profit, gm_pct, dr_pct, units, txns, aov = r
    
    assert float(gross_sales) == 49269500.50
    assert float(disc_signed) == -2674327.23
    assert float(disc_amt) == 2674327.23
    assert float(net_rev) == 46595173.27
    assert float(cogs) == 20811116.93
    assert float(profit) == 25784056.34
    assert abs(float(gm_pct) - 55.3363) < 0.001
    assert abs(float(dr_pct) - 5.4280) < 0.001
    assert int(units) == 1173116
    assert int(txns) == 585691
    assert float(aov) == 79.56


def test_fact_forecast_integrity_and_bounds():
    """Verify fact_forecast table structure, 6-month period (Jan-Jun 2026), and bounds validity."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT forecast_month, forecast_net_revenue, lower_bound_95, upper_bound_95, model_name 
        FROM novamart.fact_forecast 
        ORDER BY forecast_month;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # 1. Exactly 6 rows
    assert len(rows) == 6
    
    expected_months = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
    actual_months = [r[0] for r in rows]
    assert actual_months == expected_months
    
    # 2. Check bounds validity: lower_bound <= forecast <= upper_bound
    for r in rows:
        f_month, fc, lower, upper, model = r
        fc, lower, upper = float(fc), float(lower), float(upper)
        assert fc > 0, f"Forecast for {f_month} must be positive!"
        assert lower <= fc <= upper, f"Bound constraint violated for {f_month}: lower={lower}, fc={fc}, upper={upper}"
        assert model == "Seasonal Naive (Lag 12)"


def test_no_actual_2026_data():
    """Confirm zero actual 2026 transaction data exists in fact_sales."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM novamart.fact_sales WHERE transaction_date >= '2026-01-01';")
    count_2026 = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    assert count_2026 == 0, "Fabricated 2026 actual sales data detected in fact_sales!"
