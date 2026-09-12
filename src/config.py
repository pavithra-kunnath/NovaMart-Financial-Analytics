"""Configuration module for NovaMart Financial Analytics project.

Uses project-relative paths for cross-platform portability.
"""

from pathlib import Path
from dotenv import load_dotenv

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Project Root .env Path & Load Environment Variables
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Data Directories
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
STAGING_DIR = DATA_DIR / "staging"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

# Log & Report Directories
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"

# Raw Data File Paths
RAW_SALES_PATH = RAW_DIR / "square_item_sales_detail_24mo.csv"
RAW_CALENDAR_PATH = RAW_DIR / "02_ground_truth_event_calendar.csv"

# Output Staging & Processed File Paths
STAGING_SALES_CSV = STAGING_DIR / "square_sales_staging.csv"
STAGING_SALES_PARQUET = STAGING_DIR / "square_sales_staging.parquet"
STAGING_CALENDAR_CSV = STAGING_DIR / "event_calendar_staging.csv"

PROCESSED_SALES_CSV = PROCESSED_DIR / "fact_sales_processed.csv"
PROCESSED_SALES_PARQUET = PROCESSED_DIR / "fact_sales_processed.parquet"
PROCESSED_REJECTS_CSV = PROCESSED_DIR / "sales_rejected_records.csv"

# Log File Path
PIPELINE_LOG_PATH = LOGS_DIR / "etl_pipeline.log"

# Column Schema Mapping (Raw Source Name -> Standardized Name)
COLUMN_MAPPING = {
    "Date": "date_raw",
    "Time": "time_raw",
    "Time Zone": "time_zone",
    "Category": "category",
    "Item": "item",
    "Qty": "qty",
    "Price Point Name": "price_point_name",
    "SKU": "sku",
    "Unit Price": "unit_price",
    "Gross Sales": "gross_sales",
    "Discounts": "discounts",
    "Net Sales": "net_sales",
    "Tax": "tax",
    "Total Collected": "total_collected",
    "Transaction ID": "transaction_id",
    "Payment Method": "payment_method",
    "Device Name": "device_name",
    "Location": "location_raw",
    "Customer ID": "customer_id_raw",
    "Event Type": "event_type",
    "Unit Cost": "unit_cost",
    "Gross Profit": "gross_profit"
}

# Ensure Output Directories Exist
STAGING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
