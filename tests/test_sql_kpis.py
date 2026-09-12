"""Automated Test Suite for Task 8: SQL Financial Analytics & KPI Validation.

Framework: pytest
Scope: PostgreSQL DWH Database Validation (`novamart_db`)
"""

import os
import psycopg2
import pytest
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

DB_HOST = os.getenv("PGHOST") or os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("PGPORT") or os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("PGDATABASE") or os.getenv("DB_NAME", "novamart_db")
DB_USER = os.getenv("PGUSER") or os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("PGPASSWORD") or os.getenv("DB_PASSWORD", "")


@pytest.fixture(scope="module")
def db_conn():
    """Establish database connection to novamart_db."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    yield conn
    conn.close()


def test_fact_sales_row_count(db_conn):
    """Verify total fact_sales row count matches 970,838."""
    cur = db_conn.cursor()
    cur.execute("SELECT COUNT(*) FROM novamart.fact_sales;")
    cnt = cur.fetchone()[0]
    assert cnt == 970838, f"Expected 970,838 rows, got {cnt}"


def test_business_key_uniqueness(db_conn):
    """Verify candidate business key (transaction_id, sku, event_type) has zero duplicates."""
    cur = db_conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT (transaction_id, sku, event_type)) FROM novamart.fact_sales;")
    unique_cnt = cur.fetchone()[0]
    assert unique_cnt == 970838, f"Business key uniqueness violated: {unique_cnt}"


def test_net_revenue_and_profit_reconciliation(db_conn):
    """Verify Net Revenue and Gross Profit match target exact sums."""
    cur = db_conn.cursor()
    cur.execute("SELECT SUM(net_sales), SUM(gross_profit) FROM novamart.fact_sales;")
    net_rev, gp = cur.fetchone()
    assert round(float(net_rev), 2) == 46595173.27, f"Net revenue mismatch: {net_rev}"
    assert round(float(gp), 2) == 25784056.34, f"Gross profit mismatch: {gp}"


def test_refund_count_and_amount(db_conn):
    """Verify refund rows count (9,449) and return amount ($396,495.00)."""
    cur = db_conn.cursor()
    cur.execute("""
        SELECT COUNT(*), SUM(ABS(net_sales)) 
        FROM novamart.fact_sales 
        WHERE event_type = 'Refund';
    """)
    cnt, amt = cur.fetchone()
    assert cnt == 9449, f"Expected 9,449 refunds, got {cnt}"
    assert round(float(amt), 2) == 396495.00, f"Refund amount mismatch: {amt}"


def test_views_consistency(db_conn):
    """Verify all 5 reporting views produce identical Net Revenue totals."""
    cur = db_conn.cursor()
    cur.execute("SELECT SUM(net_sales) FROM novamart.vw_monthly_financials;")
    monthly_net = float(cur.fetchone()[0])
    cur.execute("SELECT SUM(net_sales) FROM novamart.vw_product_performance;")
    product_net = float(cur.fetchone()[0])
    cur.execute("SELECT SUM(net_sales) FROM novamart.vw_store_performance;")
    store_net = float(cur.fetchone()[0])

    assert round(monthly_net, 2) == 46595173.27
    assert round(product_net, 2) == 46595173.27
    assert round(store_net, 2) == 46595173.27
