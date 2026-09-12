"""Automated Data Quality & Data Contract Test Suite for NovaMart Retail.

Framework: pytest
Scope: Source/Raw Data Validation (`data/raw/`)
"""

import os
import re
import pytest
import pandas as pd
import numpy as np

RAW_DIR = r"c:\Users\pavit\OneDrive\Documents\All Files\projects\NovaMart Retail\data\raw"
SALES_PATH = os.path.join(RAW_DIR, "square_item_sales_detail_24mo.csv")
CALENDAR_PATH = os.path.join(RAW_DIR, "02_ground_truth_event_calendar.csv")

# Expected Schemas
EXPECTED_SALES_COLUMNS = [
    "Date", "Time", "Time Zone", "Category", "Item", "Qty",
    "Price Point Name", "SKU", "Unit Price", "Gross Sales",
    "Discounts", "Net Sales", "Tax", "Total Collected",
    "Transaction ID", "Payment Method", "Device Name", "Location",
    "Customer ID", "Event Type", "Unit Cost", "Gross Profit"
]

EXPECTED_CALENDAR_COLUMNS = [
    "Date", "Weekday", "Event", "Season x Month x Event Mult",
    "DOW Mult", "Month Mult", "Event Mult", "Discount Line Prob",
    "Refund Txn Prob", "Store Closed"
]

EXPECTED_CATEGORIES = [
    "Home Goods", "Apparel", "Electronics", "Footwear", "Accessories", "Beauty"
]


@pytest.fixture(scope="session")
def sales_df():
    """Load and yield the raw sales dataset once per test session."""
    assert os.path.exists(SALES_PATH), f"Sales file not found at {SALES_PATH}"
    df = pd.read_csv(SALES_PATH, low_memory=False)
    return df


@pytest.fixture(scope="session")
def calendar_df():
    """Load and yield the raw event calendar dataset once per test session."""
    assert os.path.exists(CALENDAR_PATH), f"Calendar file not found at {CALENDAR_PATH}"
    df = pd.read_csv(CALENDAR_PATH, low_memory=False)
    return df


# =====================================================================
# PART 2: FILE / DATASET TESTS
# =====================================================================

def test_source_files_exist():
    """Verify that both raw CSV source files exist in data/raw/."""
    assert os.path.exists(SALES_PATH), "Raw sales CSV file is missing."
    assert os.path.exists(CALENDAR_PATH), "Raw calendar CSV file is missing."


def test_datasets_not_empty(sales_df, calendar_df):
    """Verify that both raw datasets are not empty."""
    assert len(sales_df) == 970838, f"Expected 970,838 rows, got {len(sales_df):,}"
    assert len(calendar_df) == 731, f"Expected 731 rows, got {len(calendar_df):,}"


def test_expected_columns_exist(sales_df, calendar_df):
    """Verify that raw files contain all expected contract columns."""
    assert list(sales_df.columns) == EXPECTED_SALES_COLUMNS, "Sales columns do not match contract."
    assert list(calendar_df.columns) == EXPECTED_CALENDAR_COLUMNS, "Calendar columns do not match contract."


# =====================================================================
# PART 3: SCHEMA / NULL TESTS
# =====================================================================

def test_required_fields_not_null(sales_df):
    """Verify all required sales fields have 0 missing values."""
    required_cols = [c for c in EXPECTED_SALES_COLUMNS if c != "Customer ID"]
    for col in required_cols:
        null_cnt = sales_df[col].isnull().sum()
        assert null_cnt == 0, f"Column '{col}' contains {null_cnt:,} unexpected NULL values."


def test_customer_id_allows_nulls(sales_df):
    """Verify Customer ID explicitly permits NULL values (anonymous guest transactions)."""
    null_cnt = sales_df["Customer ID"].isnull().sum()
    assert null_cnt == 634393, f"Expected exactly 634,393 NULL Customer IDs, found {null_cnt:,}"


# =====================================================================
# PART 4: BUSINESS KEY TEST
# =====================================================================

def test_business_key_uniqueness(sales_df):
    """Verify candidate business key (Transaction ID + SKU + Event Type) is 100% unique."""
    bk_cols = ["Transaction ID", "SKU", "Event Type"]
    duplicate_count = sales_df.duplicated(subset=bk_cols).sum()
    assert duplicate_count == 0, f"Found {duplicate_count:,} duplicate business key combinations."


# =====================================================================
# PART 5: EVENT TYPE TESTS
# =====================================================================

def test_event_type_values(sales_df):
    """Verify Event Type contains ONLY 'Payment' and 'Refund'."""
    unique_events = set(sales_df["Event Type"].unique())
    expected_events = {"Payment", "Refund"}
    assert unique_events == expected_events, f"Unexpected Event Types found: {unique_events - expected_events}"


# =====================================================================
# PART 6: DATE TESTS
# =====================================================================

def test_date_validity_and_bounds(sales_df):
    """Verify all sales transaction dates are parseable and fall within 2024-01-01 to 2025-12-31."""
    parsed_dates = pd.to_datetime(sales_df["Date"], errors="coerce")
    assert parsed_dates.isnull().sum() == 0, "Found unparseable dates in sales dataset."
    min_date = parsed_dates.min().strftime("%Y-%m-%d")
    max_date = parsed_dates.max().strftime("%Y-%m-%d")
    assert min_date == "2024-01-01", f"Expected min date 2024-01-01, got {min_date}"
    assert max_date == "2025-12-31", f"Expected max date 2025-12-31, got {max_date}"


# =====================================================================
# PART 7: QUANTITY TESTS
# =====================================================================

def test_quantity_conventions(sales_df):
    """Verify Payment quantities are positive (> 0) and Refund quantities are negative (< 0)."""
    payment_qtys = sales_df[sales_df["Event Type"] == "Payment"]["Qty"]
    refund_qtys = sales_df[sales_df["Event Type"] == "Refund"]["Qty"]

    assert (payment_qtys > 0).all(), "Found non-positive quantities in Payment records."
    assert (refund_qtys < 0).all(), "Found non-negative quantities in Refund records."
    assert (refund_qtys == -1).all(), "Found refund quantities different from -1."


# =====================================================================
# PART 8: PRICE / COST TESTS
# =====================================================================

def test_price_and_cost_numeric_bounds(sales_df):
    """Verify Unit Price and Unit Cost are numeric, non-null, and non-negative."""
    assert (sales_df["Unit Price"] >= 0.0).all(), "Found negative Unit Price."
    assert (sales_df["Unit Cost"] >= 0.0).all(), "Found negative Unit Cost."


# =====================================================================
# PART 9: FINANCIAL RECONCILIATION TESTS
# =====================================================================

def test_financial_reconciliation_formulas(sales_df):
    """Test all four contract financial equations against raw data with $0.01 tolerance."""
    tol = 0.01

    # 1. Gross Sales == Qty * Unit Price
    calc_gross = sales_df["Qty"] * sales_df["Unit Price"]
    diff_gross = (sales_df["Gross Sales"] - calc_gross).abs()
    assert (diff_gross <= tol).all(), f"Gross Sales reconciliation failed on { (diff_gross > tol).sum() } rows."

    # 2. Net Sales == Gross Sales + Discounts
    calc_net = sales_df["Gross Sales"] + sales_df["Discounts"]
    diff_net = (sales_df["Net Sales"] - calc_net).abs()
    assert (diff_net <= tol).all(), f"Net Sales reconciliation failed on { (diff_net > tol).sum() } rows."

    # 3. Gross Profit == Net Sales - (Qty * Unit Cost)
    calc_cogs = sales_df["Qty"] * sales_df["Unit Cost"]
    calc_gp = sales_df["Net Sales"] - calc_cogs
    diff_gp = (sales_df["Gross Profit"] - calc_gp).abs()
    assert (diff_gp <= tol).all(), f"Gross Profit reconciliation failed on { (diff_gp > tol).sum() } rows."


# =====================================================================
# PART 10: DISCOUNT TESTS
# =====================================================================

def test_discount_sign_and_bounds(sales_df):
    """Verify raw Discounts are non-positive (<= 0.00)."""
    assert (sales_df["Discounts"] <= 0.0).all(), "Found positive discount values in raw data."


# =====================================================================
# PART 11: REFUND TESTS
# =====================================================================

def test_refund_negative_conventions(sales_df):
    """Verify Refund records carry negative financial values across all monetary fields."""
    refunds = sales_df[sales_df["Event Type"] == "Refund"]

    assert (refunds["Gross Sales"] < 0).all(), "Found non-negative Gross Sales in Refund records."
    assert (refunds["Net Sales"] < 0).all(), "Found non-negative Net Sales in Refund records."
    assert (refunds["Gross Profit"] < 0).all(), "Found non-negative Gross Profit in Refund records."
    assert (refunds["Tax"] < 0).all(), "Found non-negative Tax in Refund records."


# =====================================================================
# PART 14: LOCATION TESTS
# =====================================================================

def test_location_format_and_parsing(sales_df):
    """Verify Location format matches 'Store XX - CityName'."""
    pattern = re.compile(r"^Store \d{2} - .+$")
    locations = sales_df["Location"].unique()
    for loc in locations:
        assert pattern.match(loc), f"Location '{loc}' does not match expected format 'Store XX - CityName'"


# =====================================================================
# PART 15: CATEGORY / PRODUCT TESTS
# =====================================================================

def test_category_and_product_validity(sales_df):
    """Verify Category values match approved 6 categories, and SKU / Item are non-null."""
    categories = set(sales_df["Category"].unique())
    assert categories == set(EXPECTED_CATEGORIES), f"Unexpected categories found: {categories}"
    assert sales_df["SKU"].nunique() == 67, f"Expected 67 unique SKUs, found {sales_df['SKU'].nunique()}"
    assert sales_df["Item"].nunique() == 32, f"Expected 32 unique Items, found {sales_df['Item'].nunique()}"
