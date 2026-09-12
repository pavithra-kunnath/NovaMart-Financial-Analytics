"""Data Ingestion Module for NovaMart Financial Analytics.

Locates, reads, and validates immutable raw source files from data/raw/.
"""

import os
from datetime import datetime
import pandas as pd
from src.config import RAW_SALES_PATH, RAW_CALENDAR_PATH, COLUMN_MAPPING
from src.logging_config import setup_logger

logger = setup_logger("ingest")


def ingest_raw_data():
    """Ingests raw sales and event calendar files from data/raw/.

    Returns:
        tuple: (raw_sales_df, raw_calendar_df, metadata_dict)
    """
    logger.info("=== STARTING RAW DATA INGESTION ===")
    ingestion_time = datetime.now().isoformat()

    # 1. Check raw file existence
    if not RAW_SALES_PATH.exists():
        logger.error(f"Raw sales file missing at: {RAW_SALES_PATH}")
        raise FileNotFoundError(f"Missing raw sales file: {RAW_SALES_PATH}")

    if not RAW_CALENDAR_PATH.exists():
        logger.error(f"Raw calendar file missing at: {RAW_CALENDAR_PATH}")
        raise FileNotFoundError(f"Missing raw calendar file: {RAW_CALENDAR_PATH}")

    # 2. Ingest raw sales dataset
    logger.info(f"Reading raw sales file: {RAW_SALES_PATH.name}...")
    sales_df = pd.read_csv(RAW_SALES_PATH, low_memory=False)
    sales_rows, sales_cols = sales_df.shape
    logger.info(f"Successfully read sales dataset: {sales_rows:,} rows, {sales_cols} columns.")

    # Validate raw sales columns
    expected_sales_cols = list(COLUMN_MAPPING.keys())
    missing_sales_cols = set(expected_sales_cols) - set(sales_df.columns)
    if missing_sales_cols:
        logger.error(f"Sales dataset missing expected columns: {missing_sales_cols}")
        raise ValueError(f"Missing expected columns in raw sales dataset: {missing_sales_cols}")

    # 3. Ingest raw calendar dataset
    logger.info(f"Reading raw calendar file: {RAW_CALENDAR_PATH.name}...")
    calendar_df = pd.read_csv(RAW_CALENDAR_PATH, low_memory=False)
    calendar_rows, calendar_cols = calendar_df.shape
    logger.info(f"Successfully read calendar dataset: {calendar_rows:,} rows, {calendar_cols} columns.")

    # 4. Build ingestion metadata
    metadata = {
        "ingestion_timestamp": ingestion_time,
        "raw_sales_file": str(RAW_SALES_PATH),
        "raw_sales_rows": sales_rows,
        "raw_sales_cols": sales_cols,
        "raw_calendar_file": str(RAW_CALENDAR_PATH),
        "raw_calendar_rows": calendar_rows,
        "raw_calendar_cols": calendar_cols
    }

    logger.info("=== INGESTION COMPLETED SUCCESSFULLY ===")
    return sales_df, calendar_df, metadata


if __name__ == "__main__":
    sales_df, cal_df, meta = ingest_raw_data()
    print(f"Ingested {len(sales_df):,} sales rows and {len(cal_df):,} calendar rows at {meta['ingestion_timestamp']}.")
