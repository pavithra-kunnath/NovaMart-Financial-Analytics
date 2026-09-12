"""Cleaning, Standardization, & Financial Transformation Module for NovaMart Retail.

Transforms raw ingested POS data into standardized staging and processed layers.
"""

import os
import re
from datetime import datetime
import pandas as pd
import numpy as np
from src.config import (
    COLUMN_MAPPING, STAGING_SALES_CSV, STAGING_SALES_PARQUET,
    PROCESSED_SALES_CSV, PROCESSED_SALES_PARQUET, PROCESSED_REJECTS_CSV
)
from src.logging_config import setup_logger
from src.ingest import ingest_raw_data

logger = setup_logger("clean")


def parse_location(loc_str: str):
    """Parse 'Store XX - CityName' into (store_id, city)."""
    if pd.isnull(loc_str):
        return ("STORE_UNKNOWN", "Unknown")
    match = re.match(r"^Store\s+(\d{2})\s*-\s*(.+)$", str(loc_str).strip())
    if match:
        store_num = match.group(1)
        city_name = match.group(2).strip()
        return (f"STORE_{store_num}", city_name)
    return ("STORE_UNKNOWN", str(loc_str).strip())


def process_etl_pipeline(sales_df: pd.DataFrame = None, cal_df: pd.DataFrame = None):
    """Executes full ETL transformation from raw to staging and processed data layers.

    Returns:
        tuple: (processed_df, staging_df, validation_summary)
    """
    start_time = datetime.now()
    logger.info("=== STARTING ETL PIPELINE (RAW -> STAGING -> PROCESSED) ===")

    if sales_df is None or cal_df is None:
        sales_df, cal_df, _ = ingest_raw_data()

    raw_input_rows = len(sales_df)
    rejected_records = []

    # -------------------------------------------------------------
    # STEP 1: COLUMN STANDARDIZATION & STAGING LAYER
    # -------------------------------------------------------------
    logger.info("Step 1: Standardizing column names...")
    staging_df = sales_df.copy()
    staging_df = staging_df.rename(columns=COLUMN_MAPPING)

    # Add ingestion audit metadata to staging
    staging_df["source_file"] = "square_item_sales_detail_24mo.csv"
    staging_df["ingestion_timestamp"] = start_time.isoformat()

    logger.info(f"Saving staging dataset to {STAGING_SALES_CSV.name}...")
    staging_df.to_csv(STAGING_SALES_CSV, index=False)
    try:
        staging_df.to_parquet(STAGING_SALES_PARQUET, index=False)
    except Exception as e:
        logger.warning(f"Could not save staging parquet file (pyarrow/fastparquet required): {e}")

    # -------------------------------------------------------------
    # STEP 2: PROCESSED LAYER TRANSFORMATIONS
    # -------------------------------------------------------------
    logger.info("Step 2: Performing data cleaning and feature engineering...")
    df = staging_df.copy()

    # A. Date Parsing & Validation
    df["transaction_date"] = pd.to_datetime(df["date_raw"], errors="coerce")
    invalid_dates_mask = df["transaction_date"].isnull()
    if invalid_dates_mask.sum() > 0:
        logger.warning(f"Found {invalid_dates_mask.sum():,} invalid transaction dates. Rejecting records...")
        rejected_records.append(df[invalid_dates_mask])
        df = df[~invalid_dates_mask]

    # Format transaction_date as string YYYY-MM-DD
    df["transaction_date_str"] = df["transaction_date"].dt.strftime("%Y-%m-%d")
    df["transaction_datetime"] = df["transaction_date_str"] + " " + df["time_raw"].astype(str)

    # Date range validation (2024-01-01 to 2025-12-31)
    out_of_bounds_mask = (df["transaction_date"] < "2024-01-01") | (df["transaction_date"] > "2025-12-31")
    if out_of_bounds_mask.sum() > 0:
        logger.warning(f"Found {out_of_bounds_mask.sum():,} out-of-bounds dates. Rejecting records...")
        rejected_records.append(df[out_of_bounds_mask])
        df = df[~out_of_bounds_mask]

    # B. Store & Location Parsing
    logger.info("Parsing store locations into store_id and city...")
    loc_parsed = df["location_raw"].apply(parse_location)
    df["store_id"] = [p[0] for p in loc_parsed]
    df["city"] = [p[1] for p in loc_parsed]

    # C. Customer Standardization
    logger.info("Standardizing Customer ID and Customer Type...")
    df["customer_type"] = np.where(df["customer_id_raw"].isnull(), "Anonymous", "Identified")
    df["customer_id"] = df["customer_id_raw"].fillna("CUST_ANONYMOUS")

    # D. Event Type & Refund Flag
    logger.info("Standardizing Event Type and Refund Flag...")
    df["is_refund"] = (df["event_type"] == "Refund")

    # E. Financial Transformations
    logger.info("Calculating derived financial fields...")
    df["gross_sales_calculated"] = df["qty"] * df["unit_price"]
    df["discount_amount"] = df["discounts"].abs()
    df["net_sales_calculated"] = df["gross_sales"] + df["discounts"]
    df["cogs"] = df["qty"] * df["unit_cost"]
    df["gross_profit_calculated"] = df["net_sales"] - df["cogs"]

    df["gross_margin_pct"] = np.where(
        df["net_sales"] != 0,
        (df["gross_profit"] / df["net_sales"]),
        0.0
    )

    df["discount_rate_pct"] = np.where(
        df["gross_sales"] != 0,
        (df["discount_amount"] / df["gross_sales"].abs()),
        0.0
    )

    # -------------------------------------------------------------
    # STEP 3: PROCESSED SCHEMA SELECTION & ORDERING
    # -------------------------------------------------------------
    processed_cols = [
        "transaction_id",
        "sku",
        "item",
        "category",
        "price_point_name",
        "location_raw",
        "store_id",
        "city",
        "customer_id",
        "customer_type",
        "event_type",
        "is_refund",
        "transaction_datetime",
        "transaction_date_str",
        "qty",
        "unit_price",
        "gross_sales",
        "discounts",
        "discount_amount",
        "net_sales",
        "unit_cost",
        "cogs",
        "gross_profit",
        "gross_margin_pct",
        "discount_rate_pct",
        "tax",
        "total_collected",
        "payment_method",
        "device_name",
        "time_zone"
    ]

    processed_df = df[processed_cols].rename(columns={"transaction_date_str": "transaction_date"})

    # Save rejected records if any
    rejected_count = 0
    if rejected_records:
        df_rejects = pd.concat(rejected_records, ignore_index=True)
        rejected_count = len(df_rejects)
        df_rejects.to_csv(PROCESSED_REJECTS_CSV, index=False)
        logger.warning(f"Saved {rejected_count:,} rejected records to {PROCESSED_REJECTS_CSV.name}")

    # -------------------------------------------------------------
    # STEP 4: DATA QUALITY VALIDATION ASSERTIONS
    # -------------------------------------------------------------
    logger.info("Step 4: Running post-ETL data quality validation assertions...")

    # Assertion 1: Row Count Preservation
    processed_rows = len(processed_df)
    logger.info(f"Processed row count: {processed_rows:,} (Raw input: {raw_input_rows:,})")

    # Assertion 2: Business Key Uniqueness
    bk_cols = ["transaction_id", "sku", "event_type"]
    bk_dups = processed_df.duplicated(subset=bk_cols).sum()
    logger.info(f"Business Key ({bk_cols}) duplicates: {bk_dups}")
    assert bk_dups == 0, f"ETL failed: Found {bk_dups} duplicate business keys in processed dataset!"

    # Assertion 3: Financial Reconciliations ($0.01 tolerance)
    tol = 0.01
    re1_diff = (processed_df["gross_sales"] - (processed_df["qty"] * processed_df["unit_price"])).abs()
    assert (re1_diff <= tol).all(), "Gross sales reconciliation assertion failed."

    re2_diff = (processed_df["net_sales"] - (processed_df["gross_sales"] + processed_df["discounts"])).abs()
    assert (re2_diff <= tol).all(), "Net sales reconciliation assertion failed."

    re3_diff = (processed_df["gross_profit"] - (processed_df["net_sales"] - processed_df["cogs"])).abs()
    assert (re3_diff <= tol).all(), "Gross profit reconciliation assertion failed."

    logger.info("All post-ETL validation assertions PASSED successfully!")

    # -------------------------------------------------------------
    # STEP 5: SAVE PROCESSED DATASET
    # -------------------------------------------------------------
    logger.info(f"Saving production-ready processed dataset to {PROCESSED_SALES_CSV.name}...")
    processed_df.to_csv(PROCESSED_SALES_CSV, index=False)
    try:
        processed_df.to_parquet(PROCESSED_SALES_PARQUET, index=False)
    except Exception as e:
        logger.warning(f"Could not save processed parquet file: {e}")

    end_time = datetime.now()
    duration_sec = (end_time - start_time).total_seconds()

    validation_summary = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": round(duration_sec, 2),
        "raw_input_rows": raw_input_rows,
        "staging_rows": len(staging_df),
        "processed_rows": processed_rows,
        "rejected_rows": rejected_count,
        "business_key_duplicates": bk_dups,
        "refund_line_count": (processed_df["event_type"] == "Refund").sum(),
        "anonymous_customer_count": (processed_df["customer_id"] == "CUST_ANONYMOUS").sum(),
        "store_count": processed_df["store_id"].nunique(),
        "min_date": processed_df["transaction_date"].min(),
        "max_date": processed_df["transaction_date"].max()
    }

    logger.info(f"=== ETL PIPELINE COMPLETED SUCCESSFULLY IN {duration_sec:.2f}s ===")
    return processed_df, staging_df, validation_summary


if __name__ == "__main__":
    p_df, s_df, summary = process_etl_pipeline()
    print("ETL Run Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
