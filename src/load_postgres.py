"""PostgreSQL Loading & Database Warehouse Ingestion Module for NovaMart Retail.

Loads processed data layer (data/processed/fact_sales_processed.csv) into PostgreSQL.
Reads database credentials from environment variables (.env).
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from src.config import PROCESSED_SALES_CSV, BASE_DIR, ENV_PATH
from src.logging_config import setup_logger

load_dotenv(dotenv_path=ENV_PATH)
logger = setup_logger("load_postgres")

# Read Database Credentials from Environment (prioritizing PG* then DB_*)
DB_HOST = os.getenv("PGHOST") or os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("PGPORT") or os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("PGDATABASE") or os.getenv("DB_NAME", "novamart_db")
DB_USER = os.getenv("PGUSER") or os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("PGPASSWORD") or os.getenv("DB_PASSWORD", "")


def get_db_connection():
    """Establish and return connection to PostgreSQL instance."""
    import psycopg2
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=5
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL at {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}: {e}")
        raise


def build_date_dimension(start_date="2024-01-01", end_date="2026-06-30"):
    """Generate calendar DataFrame for dim_date covering 2024-2026-06."""
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    date_rows = []
    for dt in dates:
        date_key = int(dt.strftime("%Y%m%d"))
        date_str = dt.strftime("%Y-%m-%d")
        year = dt.year
        month_num = dt.month
        month_name = dt.strftime("%B")
        quarter = dt.quarter
        year_month = dt.strftime("%Y-%m")
        day_name = dt.strftime("%A")
        is_weekend = dt.dayofweek >= 5
        fin_year = year # Fiscal year aligns with calendar year

        date_rows.append({
            "date_key": date_key,
            "date": date_str,
            "year": year,
            "month_number": month_num,
            "month_name": month_name,
            "quarter": quarter,
            "year_month": year_month,
            "day_of_week": day_name,
            "is_weekend": is_weekend,
            "financial_year": fin_year
        })
    return pd.DataFrame(date_rows)


def load_dwh_pipeline():
    """Executes schema DDL setup and loads processed datasets into PostgreSQL DWH."""
    logger.info("=== STARTING POSTGRESQL DWH INGESTION PIPELINE ===")
    
    # 1. Connect to PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor()
    logger.info("Connected to PostgreSQL successfully.")

    # 2. Execute DDL Schema Creation
    schema_sql_path = BASE_DIR / "sql" / "01_schema.sql"
    if schema_sql_path.exists():
        logger.info("Applying DDL schema (sql/01_schema.sql)...")
        with open(schema_sql_path, "r", encoding="utf-8") as f:
            ddl_sql = f.read()
        cursor.execute(ddl_sql)
        conn.commit()

    # 3. Read Processed Dataset
    logger.info(f"Reading processed dataset from {PROCESSED_SALES_CSV.name}...")
    df = pd.read_csv(PROCESSED_SALES_CSV, low_memory=False)
    logger.info(f"Loaded {len(df):,} processed transaction records.")

    # 4. Truncate Tables for Idempotent Reload
    logger.info("Truncating PostgreSQL tables for idempotent reload...")
    cursor.execute("""
        TRUNCATE TABLE novamart.fact_sales, 
                       novamart.dim_customer, 
                       novamart.dim_product, 
                       novamart.dim_store, 
                       novamart.dim_date CASCADE;
    """)
    conn.commit()

    # 5. Populate DIM_DATE
    logger.info("Populating novamart.dim_date (731 days)...")
    dim_date_df = build_date_dimension()
    for _, r in dim_date_df.iterrows():
        cursor.execute("""
            INSERT INTO novamart.dim_date (date_key, date, year, month_number, month_name, quarter, year_month, day_of_week, is_weekend, financial_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (r['date_key'], r['date'], r['year'], r['month_number'], r['month_name'], r['quarter'], r['year_month'], r['day_of_week'], r['is_weekend'], r['financial_year']))
    conn.commit()

    # 6. Populate DIM_CUSTOMER
    logger.info("Populating novamart.dim_customer...")
    cust_df = df[['customer_id', 'customer_type']].drop_duplicates()
    for _, r in cust_df.iterrows():
        cursor.execute("""
            INSERT INTO novamart.dim_customer (customer_id, customer_type)
            VALUES (%s, %s);
        """, (r['customer_id'], r['customer_type']))
    conn.commit()

    # Fetch customer key map
    cursor.execute("SELECT customer_id, customer_key FROM novamart.dim_customer;")
    cust_key_map = dict(cursor.fetchall())

    # 7. Populate DIM_PRODUCT
    logger.info("Populating novamart.dim_product...")
    prod_df = df[['sku', 'item', 'category', 'price_point_name', 'unit_cost', 'unit_price']].drop_duplicates(subset=['sku'])
    for _, r in prod_df.iterrows():
        cursor.execute("""
            INSERT INTO novamart.dim_product (sku, item, category, price_point_name, unit_cost, unit_price)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (r['sku'], r['item'], r['category'], r['price_point_name'], r['unit_cost'], r['unit_price']))
    conn.commit()

    # Fetch product key map
    cursor.execute("SELECT sku, product_key FROM novamart.dim_product;")
    prod_key_map = dict(cursor.fetchall())

    # 8. Populate DIM_STORE
    logger.info("Populating novamart.dim_store...")
    store_df = df[['store_id', 'location_raw', 'city']].drop_duplicates(subset=['store_id'])
    for _, r in store_df.iterrows():
        cursor.execute("""
            INSERT INTO novamart.dim_store (store_id, store_name, city)
            VALUES (%s, %s, %s);
        """, (r['store_id'], r['location_raw'], r['city']))
    conn.commit()

    # Fetch store key map
    cursor.execute("SELECT store_id, store_key FROM novamart.dim_store;")
    store_key_map = dict(cursor.fetchall())

    # 9. Populate FACT_SALES
    logger.info("Mapping foreign keys and preparing fact_sales batch load...")
    df['date_key'] = df['transaction_date'].str.replace('-', '').astype(int)
    df['customer_key'] = df['customer_id'].map(cust_key_map)
    df['product_key'] = df['sku'].map(prod_key_map)
    df['store_key'] = df['store_id'].map(store_key_map)

    logger.info("Inserting records into novamart.fact_sales...")
    # Use executemany or string formatting batch load
    insert_sql = """
        INSERT INTO novamart.fact_sales (
            transaction_id, sku, event_type, date_key, customer_key, product_key, store_key,
            transaction_datetime, transaction_date, qty, unit_price, gross_sales, discounts,
            discount_amount, net_sales, unit_cost, cogs, gross_profit, gross_margin_pct,
            discount_rate_pct, tax, total_collected, is_refund
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    fact_tuples = [
        (
            row.transaction_id, row.sku, row.event_type, int(row.date_key), int(row.customer_key),
            int(row.product_key), int(row.store_key), row.transaction_datetime, row.transaction_date,
            int(row.qty), float(row.unit_price), float(row.gross_sales), float(row.discounts),
            float(row.discount_amount), float(row.net_sales), float(row.unit_cost), float(row.cogs),
            float(row.gross_profit), float(row.gross_margin_pct), float(row.discount_rate_pct),
            float(row.tax), float(row.total_collected), bool(row.is_refund)
        )
        for row in df.itertuples(index=False)
    ]

    import psycopg2.extras
    psycopg2.extras.execute_batch(cursor, insert_sql, fact_tuples, page_size=5000)
    conn.commit()

    # 10. Execute Views & Power BI DDL Creation
    views_sql_path = BASE_DIR / "sql" / "02_views.sql"
    if views_sql_path.exists():
        logger.info("Creating reporting views (sql/02_views.sql)...")
        with open(views_sql_path, "r", encoding="utf-8") as f:
            views_sql = f.read()
        cursor.execute(views_sql)
        conn.commit()

    pbi_sql_path = BASE_DIR / "sql" / "04_powerbi_views.sql"
    if pbi_sql_path.exists():
        logger.info("Creating Power BI views & fact_forecast table (sql/04_powerbi_views.sql)...")
        with open(pbi_sql_path, "r", encoding="utf-8") as f:
            pbi_sql = f.read()
        cursor.execute(pbi_sql)
        conn.commit()

    # 10b. Populate fact_forecast with Task 10 Seasonal Naive 6-Month Forecast
    logger.info("Populating novamart.fact_forecast table with Task 10 Seasonal Naive predictions...")
    from src.forecast import build_monthly_dataset, run_rolling_origin_backtest, generate_forward_forecast
    m_df = build_monthly_dataset()
    metrics_df, models_dict, backtest_preds_df = run_rolling_origin_backtest(m_df)
    eval_actuals = m_df['net_revenue'].values[12:]
    fc_df = generate_forward_forecast(m_df, "Seasonal Naive", models_dict, eval_actuals)

    cursor.execute("TRUNCATE TABLE novamart.fact_forecast CASCADE;")
    
    forecast_tuples = []
    for row in fc_df.itertuples(index=False):
        f_month = row.forecast_month
        f_date = f"{f_month}-01"
        date_key = int(f_month.replace("-", "") + "01")
        forecast_tuples.append((
            date_key, f_month, f_date, round(float(row.predicted_net_revenue), 2),
            round(float(row.lower_bound_95), 2), round(float(row.upper_bound_95), 2),
            "Seasonal Naive (Lag 12)", "2025-12-31"
        ))

    insert_fc_sql = """
        INSERT INTO novamart.fact_forecast (
            date_key, forecast_month, forecast_date, forecast_net_revenue,
            lower_bound_95, upper_bound_95, model_name, forecast_run_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    psycopg2.extras.execute_batch(cursor, insert_fc_sql, forecast_tuples)
    conn.commit()

    # 11. Run DWH Reconciliations
    logger.info("Running DWH database validation assertions...")
    cursor.execute("SELECT COUNT(*) FROM novamart.fact_sales;")
    loaded_fact_rows = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT (transaction_id, sku, event_type)) FROM novamart.fact_sales;")
    unique_bk_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM novamart.fact_sales WHERE event_type = 'Refund';")
    refund_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM novamart.fact_sales f 
        JOIN novamart.dim_customer c ON f.customer_key = c.customer_key 
        WHERE c.customer_id = 'CUST_ANONYMOUS';
    """)
    anon_count = cursor.fetchone()[0]

    logger.info(f"Loaded fact rows: {loaded_fact_rows:,}")
    logger.info(f"Unique business keys: {unique_bk_count:,}")
    logger.info(f"Refund rows: {refund_count:,}")
    logger.info(f"Anonymous customer rows: {anon_count:,}")

    assert loaded_fact_rows == len(df), f"Fact row mismatch: expected {len(df)}, got {loaded_fact_rows}"
    assert unique_bk_count == len(df), "Business key uniqueness constraint violated!"
    assert refund_count == 9449, f"Refund count mismatch: expected 9449, got {refund_count}"
    assert anon_count == 634393, f"Anonymous count mismatch: expected 634393, got {anon_count}"

    cursor.close()
    conn.close()

    logger.info("=== POSTGRESQL DWH INGESTION COMPLETED SUCCESSFULLY ===")
    return {
        "fact_rows": loaded_fact_rows,
        "unique_bk_count": unique_bk_count,
        "refund_count": refund_count,
        "anon_count": anon_count
    }


if __name__ == "__main__":
    try:
        summary = load_dwh_pipeline()
        print("PostgreSQL Load Summary:", summary)
    except Exception as e:
        print(f"PostgreSQL Load Error: {e}")
