# NovaMart Retail Financial Analytics & Revenue Forecasting

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop_PBIP-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Test Suite](https://img.shields.io/badge/Tests-56_Passed-success?logo=pytest&logoColor=white)](https://docs.pytest.org/)

An end-to-end, portfolio-grade analytics engineering and time-series forecasting platform built for **NovaMart**, a multi-location retail chain with 30 store locations and 67 SKUs across 6 merchandise categories. The project transforms 24 months of raw Point-of-Sale (POS) transaction records into an audited, contract-governed PostgreSQL star schema data warehouse, executes in-depth SQL financial analysis, performs 12-month rolling-origin forecast backtesting to select an optimal champion revenue forecasting model with empirical 95% prediction intervals, establishes an automated forecast accuracy monitoring framework, and delivers a 5-page Power BI Desktop analytical dashboard.

---

## 1. Business Objectives

- **Financial Performance Visibility**: Establish single-source-of-truth financial baselines for executive leadership across 24 continuous historical months ($46.6M Net Revenue, $25.8M Gross Profit, 55.34% Gross Margin).
- **Unit Economics & Margin Diagnostics**: Quantify category margin contributions, price points, and promotional discount erosion across merchandise hierarchies.
- **Customer Segmentation Insights**: Compare spending behavior between Identified Loyalty Members and Anonymous Walk-in Guests to measure loyalty basket uplift.
- **Store Network Benchmarking**: Evaluate sales volume and margin efficiency across 30 nationwide retail store locations.
- **Time-Series Revenue Forecasting**: Implement a rigorous, chronological rolling-origin backtest across candidate statistical models to generate an authoritative 6-month forward revenue forecast (H1 2026) with calibrated 95% prediction intervals.
- **Continuous Monitoring & Drift Detection**: Build an operational monitoring baseline to track actual-vs-forecast accuracy, detect systematic directional bias, and alert on performance degradation.

---

## 2. Key Results & Portfolio KPI Snapshot

Across the audited 24-month historical period (January 1, 2024 – December 31, 2025), the platform reconciled the following financial and operational totals from PostgreSQL:

| Metric | Portfolio Total | Business Context |
| :--- | :---: | :--- |
| **Total Line Items** | **970,838** | Reconciled POS sales and refund line items |
| **Distinct Transactions** | **585,691** | Unique customer checkout baskets |
| **Total Units Moved** | **1,173,116** | Net physical items sold across 30 stores |
| **Gross Sales** | **$49,269,500.50** | Baseline sales before promotional price reductions |
| **Discounts** | **$2,674,327.23** | 5.43% average promotional discount rate |
| **Net Revenue** | **$46,595,173.27** | Net realized revenue after discounts and refunds |
| **Cost of Goods Sold (COGS)** | **$20,811,116.93** | Inventory acquisition cost of goods sold |
| **Gross Profit** | **$25,784,056.34** | Gross profit realized ($Net\ Sales - COGS$) |
| **Gross Margin %** | **55.34%** | Portfolio-wide gross margin percentage |
| **Average Order Value (AOV)** | **$79.56** | Average net revenue collected per transaction |
| **Refund Line Items** | **9,449** | Reconciled return events totaling $396,495.00 refunded sales (0.97% line rate) |

---

## 3. Technology Stack

- **Data Engineering & Analytics**: Python 3.11, `pandas`, `NumPy`, `psycopg2-binary`, `SQLAlchemy`, `python-dotenv`
- **Statistical Modeling & Forecasting**: `statsmodels` (ARIMA, SARIMAX), `scikit-learn`, `matplotlib`, `seaborn`
- **Data Warehousing & Database**: PostgreSQL 13+, pgAdmin 4, SQL (DDL, DML, Window Functions, Aggregate Views)
- **Business Intelligence & Reporting**: Microsoft Power BI Desktop (PBIP developer format, Tabular Object Model / TMSL, 29 custom DAX measures)
- **Automated Testing & QA**: `pytest` (56 automated unit, schema, and regression test assertions)
- **Environment & Version Control**: Git, GitHub, Antigravity

---

## 4. End-to-End System Architecture

```
+---------------------------------------------------------------------------------------+
| 1. RAW DATA SOURCE LAYER                                                              |
|    - square_item_sales_detail_24mo.csv (970,838 transaction rows, 22 columns)          |
|    - 02_ground_truth_event_calendar.csv (731 daily event & multiplier records)         |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 2. AUDIT, DATA CONTRACT & QUALITY GATES                                               |
|    - docs/dataset_audit.md (Source inventory, grain identification, missingness profile)  |
|    - docs/data_contract.md (Formal schema types, business key rules, mathematical bounds) |
|    - tests/test_quality.py (Automated pytest suite validating raw data contracts)       |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 3. PYTHON INGESTION & ETL PIPELINE                                                    |
|    - src/ingest.py (Audit tagging, source checksums, metadata logging)                |
|    - src/clean.py (Location parsing, customer null handling, derived financial metrics) |
|    - data/staging/ & data/processed/ (Parquet / CSV production datasets)               |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 4. POSTGRESQL DATA WAREHOUSE (STAR SCHEMA)                                            |
|    - sql/01_schema.sql (DDL for dim_date, dim_customer, dim_product, dim_store, fact) |
|    - src/load_postgres.py (Idempotent batch loader, surrogate key mapping, TRUNCATE)  |
|    - sql/02_views.sql & sql/04_powerbi_views.sql (Production analytical views)        |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 5. ADVANCED SQL ANALYTICS & RECONCILIATION                                            |
|    - sql/03_financial_kpis.sql (MoM growth, category mix, store rankings, refunds)    |
|    - tests/test_sql_kpis.py (Automated database assertion tests against DWH views)    |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 6. TIME-SERIES REVENUE FORECASTING & ACCURACY MONITORING                              |
|    - src/forecast.py (12-origin rolling backtest, candidate benchmarking, H1 2026 fc) |
|    - Champion Selection: Seasonal Naive (Lag 12) with WAPE = 5.20%                    |
|    - Forward H1 2026 Projection: $11,487,927.00 with 95% Prediction Intervals         |
|    - src/accuracy_monitor.py (Baseline drift monitoring, bias tracking, alert gates) |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 7. POWER BI DESKTOP ANALYTICAL REPORTING (PBIP)                                       |
|    - Native PostgreSQL connector import mode                                          |
|    - Star schema relationships (5 1-to-many single-direction relationships)           |
|    - 29 production DAX measures in dedicated _Measures table                          |
|    - 5 analytical pages: Exec Overview, Revenue & Profit, Product, Store, Forecast     |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| 8. VERSION CONTROL & GITHUB REPOSITORY                                                |
|    - Git version control tracking all code, SQL, documentation, reports, and PBIP     |
+---------------------------------------------------------------------------------------+
```

---

## 5. Data Source & Dataset Characteristics

> [!NOTE]
> **Synthetic Retail Benchmark Notice**: The dataset analyzed in this project is a synthetic retail Point-of-Sale transaction dataset modeled after Square POS export schemas. It was generated to provide a realistic multi-unit retail point-of-sale benchmark without containing real proprietary customer or commercial data.
>
> The benchmark dataset structure and methodology are based on the published synthetic retail transaction dataset on the **[Mendeley Data Repository](https://data.mendeley.com/)**, audited and profiled in [`docs/dataset_audit.md`](docs/dataset_audit.md).

### Dataset Specifications
- **Temporal Horizon**: 24 continuous calendar months from **January 1, 2024 through December 31, 2025** (729 active trading days; 2 store-closed days).
- **Transaction Volume**: **970,838 line-item records** across **585,691 distinct transactions** (average 1.66 line items per basket; maximum 4 items).
- **Retail Footprint**: **30 brick-and-mortar retail store locations** across major US metropolitan areas.
- **Product Assortment**: **67 distinct SKUs** across 32 unique commercial items.
- **Merchandise Categories (6)**: Apparel, Footwear, Electronics, Accessories, Home Goods, and Beauty.
- **Customer Representation**: 336,445 records associated with **19,999 identified loyalty member IDs**; 634,393 records represent walk-in anonymous guest transactions (`Customer ID = NULL`).
- **Event Types**: Two distinct POS event classifications: `Payment` (961,389 lines) and `Refund` (9,449 lines).

---

## 6. Data Engineering Pipeline

### A. Source Audit & Data Contract
Before writing pipeline code, a complete file inventory and grain audit was conducted ([`docs/dataset_audit.md`](docs/dataset_audit.md)), followed by a formally binding Data Contract ([`docs/data_contract.md`](docs/data_contract.md)):
- **Grain Definition**: Exactly one record per line item per transaction event.
- **Composite Business Key**: `(Transaction ID, SKU, Event Type)`.
- **Mathematical Consistency Rules**: Strict numerical assertions enforced for gross sales, discounts, net sales, taxes, total collected, cost of goods, and gross profit.

### B. Automated Data Quality Gates
Prior to ingestion, `tests/test_quality.py` executes 20+ automated `pytest` quality gates on raw CSV files:
- Validation of expected column headers and allowed data types.
- Zero duplicate records across all 22 raw columns.
- Composite business key uniqueness across all 970,838 rows.
- Non-negativity constraints on unit price and unit cost.
- Mathematical equality: `Gross Sales == Qty * Unit Price` and `Net Sales == Gross Sales + Discounts`.
- Sign convention verification: refund lines must have `Qty = -1` and negative dollar amounts; payment discounts must be non-positive floats ($\le 0$).

### C. Python ETL (`src/ingest.py` & `src/clean.py`)
- **Location Normalization**: Parses embedded location strings (e.g. `"Store 01 - Austin"`) into structured attributes: `store_id` (`STORE_01`), `store_name` (`Store 01 - Austin`), and `city` (`Austin`).
- **Customer Null Standardization**: Imputes missing customer identifiers with `'CUST_ANONYMOUS'` and creates a categorical feature `customer_type` (`Identified` vs `Anonymous`).
- **Derived Financial Metrics**: Derives positive `discount_amount` ($|Discounts|$), calculated `cogs` ($Qty \times Unit\ Cost$), `gross_margin_pct`, and `discount_rate_pct`.
- **Pipeline Output**: Generates clean staging and production datasets saved to `data/staging/` and `data/processed/`.

### D. PostgreSQL Data Warehouse Loading (`src/load_postgres.py`)
- **Star Schema Architecture**: Implements 4 dimension tables and 1 central fact table:
  - `novamart.dim_date` (912 calendar days generated covering 2024-01-01 through 2026-06-30 to span historical sales and the H1 2026 forecast window).
  - `novamart.dim_customer` (19,999 identified members + 1 default `CUST_ANONYMOUS` record).
  - `novamart.dim_product` (67 SKUs with item names, categories, and unit price/cost).
  - `novamart.dim_store` (30 retail locations with city mappings).
  - `novamart.fact_sales` (970,838 transaction line items with integer surrogate foreign keys).
  - `novamart.fact_forecast` (6 forward forecast records for H1 2026).
- **Idempotency**: Implements a `TRUNCATE ... CASCADE` batch loading pattern ensuring 100% idempotent reruns without duplicate dimension or fact keys.
- **Financial Reconciliation Assertions**: Automatic post-load assertions verify that database sums for gross sales, discounts, net revenue, COGS, and profit match the source data down to $0.00.

---

## 7. SQL Financial Analytics

Authoritative financial views and analytical queries are implemented in `sql/02_views.sql`, `sql/03_financial_kpis.sql`, and `sql/04_powerbi_views.sql`:

### Merchandise Category Performance
Financial breakdown by product category sorted by net revenue contribution:

| Category | Net Revenue | Gross Profit | Gross Margin % | Revenue Share |
| :--- | :---: | :---: | :---: | :---: |
| **Apparel** | $17,905,299.01 | $10,260,660.81 | 57.31% | 38.4% |
| **Footwear** | $14,318,477.45 | $6,970,083.63 | 48.68% | 30.7% |
| **Electronics** | $5,137,373.20 | $2,530,736.75 | 49.26% | 11.0% |
| **Accessories** | $4,253,337.50 | $2,750,078.58 | 64.66% | 9.1% |
| **Home Goods** | $3,346,687.50 | $2,157,744.86 | 64.47% | 7.2% |
| **Beauty** | $1,633,998.61 | $1,114,751.71 | 68.22% | 3.5% |

### Customer Segmentation Mix
Breakdown between identified loyalty members and anonymous guest checkout:

| Customer Segment | Net Revenue | Order Count | AOV | Revenue Share |
| :--- | :---: | :---: | :---: | :---: |
| **Anonymous Guests** | $30,134,645.45 | 384,024 | $78.47 | 64.7% |
| **Identified Members** | $16,460,527.82 | 201,667 | $81.62 | 35.3% |

*Identified loyalty customers averaged **$81.62 AOV** compared to **$78.47 AOV** for anonymous guests (+$3.15 per order).*

### Top 5 Retail Store Locations

| Store Location | City | Net Revenue | Gross Margin % |
| :--- | :--- | :---: | :---: |
| **Store 09 - Chicago** | Chicago, IL | $2,873,583.44 | 55.35% |
| **Store 18 - Memphis** | Memphis, TN | $2,873,208.39 | 55.22% |
| **Store 28 - Sacramento** | Sacramento, CA | $2,868,244.32 | 55.34% |
| **Store 29 - Minneapolis** | Minneapolis, MN | $2,863,350.63 | 55.31% |
| **Store 26 - Los Angeles** | Los Angeles, CA | $2,852,094.23 | 55.36% |

### Returns & Refund Accounting
- **Refund Volume**: 9,449 line items (0.97% line-item frequency).
- **Refund Total**: Reconciled total of $396,495.00 in returned merchandise value deducted from gross sales to yield net revenue.

---

## 8. Time-Series Revenue Forecasting

The forecasting engine (`src/forecast.py`) models monthly portfolio Net Revenue over the 24-month historical series (`2024-01` to `2025-12`).

### A. Chronological Rolling-Origin Backtesting
To ensure realistic evaluation without data leakage, candidate models were evaluated using **1-step-ahead rolling-origin backtesting across 12 origins** spanning January 2025 through December 2025:

| Candidate Model | MAE ($) | RMSE ($) | MAPE (%) | WAPE (%) | Mean Bias ($) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Seasonal Naive (Lag 12)** | **$103,709.95** | **$113,212.87** | **5.20%** | **5.20%** | **+$103,709.95** | 🏆 **Champion** |
| **ARIMA(0,1,1)** | $363,926.10 | $511,313.57 | 19.01% | 18.26% | -$8,564.26 | Challenger |
| **ARIMA(1,1,0)** | $371,836.87 | $521,200.20 | 19.46% | 18.65% | -$12,236.69 | Challenger |
| **Naive (Lag 1)** | $390,025.42 | $494,313.53 | 20.49% | 19.57% | +$9,317.91 | Baseline |
| **ARIMA(1,1,1)** | $400,069.49 | $537,088.54 | 21.00% | 20.07% | +$18,326.56 | Challenger |
| **SARIMAX(0,1,0)(1,0,0,12)** | $796,242.82 | $986,037.61 | 41.40% | 39.95% | +$377,509.35 | Disqualified |

### B. Champion Selection
**Seasonal Naive (Lag 12)** was selected as the champion model based strictly on empirical backtest metrics, achieving the lowest **WAPE (5.20%)**, **MAE ($103,709.95)**, and **RMSE ($113,212.87)** across the 12 evaluation origins.

### C. Forward 6-Month Revenue Projection (H1 2026)

> [!IMPORTANT]
> **Forecast Disclaimer**: The figures below represent statistical model projections for the first half of 2026. They are **NOT** actual financial results. Zero actual 2026 transaction data exists in the database.

Using all 24 months of training data, the champion model projected the following forward trajectory for H1 2026 with 95% empirical prediction intervals:

| Forecast Month | Predicted Net Revenue | 95% Lower Prediction Bound | 95% Upper Prediction Bound |
| :---: | :---: | :---: | :---: |
| **2026-01** | $1,521,877.18 | $1,432,888.01 | $1,610,866.35 |
| **2026-02** | $1,738,075.29 | $1,649,086.12 | $1,827,064.46 |
| **2026-03** | $2,077,924.19 | $1,988,935.02 | $2,166,913.36 |
| **2026-04** | $1,907,958.09 | $1,818,968.92 | $1,996,947.26 |
| **2026-05** | $2,252,591.87 | $2,163,602.70 | $2,341,581.04 |
| **2026-06** | $1,989,500.38 | $1,900,511.21 | $2,078,489.55 |
| **H1 2026 Total** | **$11,487,927.00** | **$10,953,991.98** | **$12,021,862.02** |

- **Prediction Interval Coverage**: During the 12-month 2025 backtest, **100% of actual monthly revenue observations fell inside the 95% prediction intervals**, validating interval calibration.

---

## 9. Forecast Accuracy Monitoring Framework

The monitoring pipeline (`src/accuracy_monitor.py`) operationalizes continuous model governance:
- **Baseline Accuracy Targets**: Established at MAE $103,709.95, RMSE $113,212.87, and WAPE 5.20%.
- **Directional Bias Tracking**: Tracks positive error patterns ($Actual > Forecast$) observed during backtesting when 2025 monthly net revenues exceeded 2024 baseline values.
- **Degradation Alert Thresholds**:
  - **WAPE > 10.0%**: Triggers a model review flag.
  - **3 Consecutive Months of Directional Bias**: Triggers retraining and candidate model re-evaluation.
- **Monitoring Artifacts**: Records performance tracking to `reports/forecast_monitoring/forecast_accuracy_history.csv` and outputs diagnostic visualization plots.

---

## 10. Power BI Analytical Dashboard

The Power BI solution is maintained in Microsoft's developer-friendly **Power BI Project (`.pbip`)** format under `powerbi/`:

```
powerbi/
├── NovaMart.pbip                 # Main PBIP project entrypoint
├── NovaMart.Dataset/
│   ├── definition.pbism          # Semantic model dataset definition
│   └── model.bim                 # Tabular Object Model (TMSL) schema & 29 DAX measures
└── NovaMart.Report/
    ├── definition.pbir           # Report binding definition
    └── report.json               # Visual layouts, containers, coordinates, and bindings
```

### Semantic Data Model
- **Import Storage Mode**: VertiPaq in-memory engine providing sub-second analytical query response times across all filter contexts.
- **Star Schema Relationships**: 5 active, single-direction 1-to-many relationships connecting dimension tables (`dim_date`, `dim_customer`, `dim_product`, `dim_store`) to fact views (`vw_pbi_fact_sales` and `vw_pbi_fact_forecast`).
- **DAX Measure Catalog**: 29 business measures cataloged in a dedicated `_Measures` table covering financial core metrics, operational KPIs, time intelligence (YoY, MoM), customer segmentation, and forecast bands.

### Implemented Analytical Pages (5)

1. **`01 Executive Overview`**: C-suite executive dashboard displaying high-level KPI cards (Net Revenue, Gross Profit, Gross Margin %, Units, Transactions, AOV), 24-month revenue and gross profit trend lines, revenue YoY clustered column comparison, category contribution donut chart, and store performance rankings.
2. **`02 Revenue & Profitability`**: Financial P&L analysis breaking down Gross Sales, Discount Amounts, COGS, Net Revenue, and Gross Margin expansion trends over time.
3. **`03 Product & Category`**: SKU-level matrix, product profitability rankings, category gross margin comparisons, and unit sales volume.
4. **`04 Store & Customer`**: Geographic analysis of 30 store locations, customer segmentation mix (Identified Members vs. Anonymous Walk-in Guests), order frequency, and loyalty basket uplift.
5. **`05 Forecast & Outlook`**: Time-series visualization connecting historical actuals (2024–2025) to forward 6-month Seasonal Naive predictions (H1 2026) with a shaded 95% confidence ribbon, monthly projection table, and mandatory forecast disclaimer.

---

## 11. Automated Testing & Verification

The project includes an automated test suite executed via `pytest`:

```bash
python -m pytest -v
```

### Latest Test Results:
```text
56 passed, 68 warnings
```

- **56 Passed**: 100% pass rate across all unit and integration tests:
  - `tests/test_quality.py`: Raw CSV schemas, nullability, composite business keys, price bounds, and financial reconciliation formulas (15 tests).
  - `tests/test_sql_kpis.py`: PostgreSQL fact table row counts, view integrity, and financial KPI reconciliation against database baselines (5 tests).
  - `tests/test_forecasting.py`: Time series aggregation, zero-denominator safety, rolling-origin backtest execution, and forward forecast bounds (5 tests).
  - `tests/test_accuracy_monitor.py`: MAE, RMSE, MAPE, sMAPE, WAPE calculations, zero-handling, negative forecast validation, and prediction interval coverage (17 tests).
  - `tests/test_powerbi_model.py`: Star schema referential integrity, zero orphan keys, extended calendar coverage (912 days), and baseline reconciliation (7 tests).
  - `tests/test_powerbi_report.py`: PBIP artifact structure, model.bim TMSL semantic model, 5 report pages, and visual KPI reconciliation (7 tests).
- **68 Warnings**: These are `statsmodels` statistical estimation and convergence warnings (`ConvergenceWarning`, `EstimationWarning` on non-stationary or non-invertible starting parameters) emitted during rolling-origin backtests of SARIMAX models on short 12-to-23-month time series. They are **statistical model notifications, not software defects or test failures**.

---

## 12. Repository Structure

```
NovaMart Retail/
├── data/
│   ├── external/                 # External references and lookups
│   ├── processed/                # Production processed fact and dimension CSVs
│   ├── raw/                      # Immutable raw source CSV files
│   └── staging/                  # Staging transformed datasets
├── docs/                         # Formal engineering and data governance specifications
│   ├── data_contract.md          # Formal data contract & schema specification
│   ├── data_dictionary.md        # Column definitions and data dictionary
│   ├── data_lineage.md           # End-to-end data pipeline lineage
│   ├── data_quality.md           # Data quality rules and validation bounds
│   ├── dataset_audit.md          # Comprehensive raw dataset audit report
│   ├── deployment.md             # PostgreSQL DWH deployment guide
│   ├── kpi_dictionary.md         # Financial metric calculation formulas
│   ├── powerbi_data_model.md     # Star schema model specification
│   ├── powerbi_dax_measure_dictionary.md  # 29 DAX measure definitions
│   └── powerbi_report_dictionary.md       # Visual containers and page layouts
├── notebooks/                    # Exploratory analysis and profiling notebooks
├── powerbi/                      # Power BI Desktop PBIP solution
│   ├── NovaMart.pbip             # PBIP project file
│   ├── NovaMart.Dataset/         # Tabular semantic model definition (model.bim)
│   ├── NovaMart.Report/          # Report definition and visual layout (report.json)
│   └── README.md                 # Power BI data model and DAX documentation
├── reports/                      # Formal analytical and reconciliation reports
│   └── figures/                  # High-resolution generated charts and plots
│       ├── forecast/             # Forecast trajectory and backtest accuracy plots
│       └── forecast_monitoring/  # Error distribution and actual-vs-forecast charts
├── scratch/                      # Diagnostic and verification utility scripts
│   └── run_demo.py               # End-to-end executive demo script
├── sql/                          # Production PostgreSQL DDL and analytical queries
│   ├── 01_schema.sql             # Star schema DDL (dimensions & fact tables)
│   ├── 02_views.sql              # Analytical reporting views
│   ├── 03_financial_kpis.sql     # Executive financial KPI queries
│   └── 04_powerbi_views.sql      # Views optimized for Power BI Import mode
├── src/                          # Modular Python application code
│   ├── accuracy_monitor.py       # Forecast accuracy monitoring engine
│   ├── clean.py                  # Cleaning, standardization, and derivation module
│   ├── config.py                 # Central project paths and database configuration
│   ├── forecast.py               # Time-series forecasting and backtesting engine
│   ├── ingest.py                 # Raw data ingestion and verification
│   ├── load_postgres.py          # PostgreSQL automated DWH loader
│   └── logging_config.py         # Standardized logging setup
├── tests/                        # Automated pytest test suites
│   ├── test_accuracy_monitor.py
│   ├── test_forecasting.py
│   ├── test_powerbi_model.py
│   ├── test_powerbi_report.py
│   ├── test_quality.py
│   └── test_sql_kpis.py
├── .env.example                  # Template for database environment variables
├── .gitignore                    # Git ignore file (excludes .env and raw data)
├── README.md                     # Project overview and documentation
└── requirements.txt              # Production Python package dependencies
```

---

## 13. Reproducibility & Setup Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/pavithra-kunnath/NovaMart-Financial-Analytics.git
cd NovaMart-Financial-Analytics
```

### Step 2: Set Up Python Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Configure Database Credentials
Create a `.env` file in the root directory from the provided `.env.example`:
```bash
cp .env.example .env
```
Edit `.env` with your PostgreSQL instance credentials:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=novamart_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
LOG_LEVEL=INFO
```

### Step 4: Run ETL Pipeline (Clean & Transform)
Process the raw transaction data into standardized staging and production datasets:
```bash
python -m src.clean
```

### Step 5: Run the Automated PostgreSQL DWH Loader
Ensure PostgreSQL is running and the database `novamart_db` exists, then execute the loader:
```bash
python -m src.load_postgres
```
*This applies DDL schemas, populates dimensions (including the 912-day calendar), maps surrogate keys, loads 970,838 fact rows, creates reporting views, and executes database assertions.*

### Step 6: Run Time-Series Forecasting & Monitoring Pipelines
```bash
# Execute 12-origin backtesting, champion selection, and H1 2026 forecast
python -m src.forecast

# Execute production accuracy monitoring baseline and plot generation
python -m src.accuracy_monitor
```

### Step 7: Run the Full End-to-End Terminal Demo
To print the complete portfolio financial summary, category breakdowns, customer segmentation mix, top stores, model comparisons, and forward forecasts in a single command:
```bash
python scratch/run_demo.py
```

### Step 8: Run Automated Test Suite
```bash
python -m pytest -v
```

### Step 9: Open Power BI Report
Open `powerbi/NovaMart.pbip` in **Power BI Desktop** to explore the interactive 5-page dashboard.

---

## 14. Power BI Deployment Status & Environment Notes

- **Development Environment**: The Power BI solution was developed, modeled, and validated entirely within **Microsoft Power BI Desktop** using the Git-integrated **Power BI Project (`.pbip`)** format.
- **Power BI Service Deployment Status**: Cloud deployment to Power BI Service (`app.powerbi.com`) and automated scheduled cloud refresh via the On-Premises Data Gateway were **NOT configured**. This was because the available development account and operating environment did not support the organizational / corporate Microsoft 365 tenant account required for Power BI Service cloud publishing.
- **Local Fidelity**: All visual coordinate layouts, filter interactions, DAX measures, and numerical outputs have been validated against the local PostgreSQL data warehouse to ensure full local operational fidelity.

---

## 15. Limitations & Future Roadmap

1. **Power BI Service Deployment**: Migrate `.pbip` artifacts to a Power BI Service cloud workspace with scheduled gateway refresh once an organizational Microsoft 365 tenant is available.
2. **Actuals vs. Forecast Tracking**: Ingest and reconcile actual monthly sales data as 2026 progresses to evaluate real-world forecast drift against the 5.20% WAPE baseline.
3. **Advanced Machine Learning Models**: Explore hierarchical reconciliation (e.g. `scikit-hts`), Prophet, or gradient-boosted trees (`LightGBM`) as historical depth expands beyond 24 months.
4. **Customer Loyalty Expansion**: Enrich the 34.66% identified customer base with demographic, RFM (Recency, Frequency, Monetary), and churn risk models.

---

## 16. License & Source Notes

- **Dataset Attribution**: Synthetic retail benchmark based on Square POS transaction schemas and the Mendeley Data retail repository.
- **Project Type**: Educational and portfolio demonstration analytics engineering project.

---

## 17. Author

**Pavithra Kunnath**  
GitHub: [@pavithra-kunnath](https://github.com/pavithra-kunnath)  
Repository: [NovaMart-Financial-Analytics](https://github.com/pavithra-kunnath/NovaMart-Financial-Analytics)
