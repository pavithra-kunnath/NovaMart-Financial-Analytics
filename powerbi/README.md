# NovaMart Retail Power BI Project Foundation & Data Model Specification

## 1. Overview & Project Scope

This document provides the technical specification, database connection parameters, storage mode rationale, relationship map, DAX measure dictionary, and manual setup instructions for building the **NovaMart Retail Power BI Financial Analytics & Revenue Forecasting Model**.

This phase establishes the **Data Model & Measures Layer (Task 12)**. Report visual pages and layout design will be created in Task 13.

---

## 2. PostgreSQL Source Connection Parameters

Connect Power BI Desktop to the authoritative PostgreSQL Data Warehouse instance using the Native PostgreSQL Connector:

- **Server:** `localhost` (or `$PGHOST`)
- **Port:** `5432` (or `$PGPORT`)
- **Database:** `novamart_db` (or `$PGDATABASE`)
- **Schema:** `novamart`
- **Authentication:** Database Username / Password (configured in project `.env` file; do NOT hardcode credentials).
- **Import Views / Tables**:
  1. `novamart.dim_date` (Calendar dimension covering 2024-01-01 to 2026-06-30)
  2. `novamart.dim_customer` (Customer dimension including `CUST_ANONYMOUS`)
  3. `novamart.dim_product` (Product dimension containing 67 SKUs across 6 categories)
  4. `novamart.dim_store` (Store dimension covering 30 retail locations)
  5. `novamart.vw_pbi_fact_sales` (Primary POS line-item transactional fact table, 970,838 rows)
  6. `novamart.vw_pbi_fact_forecast` (Isolated 6-month forward forecast table, 6 monthly records)

---

## 3. Storage Mode Selection & Architectural Rationale

- **Selected Storage Mode:** **Import Mode** (VertiPaq In-Memory Engine)
- **Architectural Rationale:**
  - **Dataset Size:** `fact_sales` contains **970,838 records** (~150 MB raw CSV, ~35 MB compressed in VertiPaq memory), which easily fits into standard Power BI Desktop memory limits.
  - **Analytical Performance:** High-velocity sub-second DAX aggregations across multi-column filter contexts (Category, Store, Customer Type, Time Intelligence).
  - **DAX Capability:** Enables full DAX time-intelligence functions (`SAMEPERIODLASTYEAR`, `DATEADD`) without DirectQuery query translation limitations or SQL server round-trip latency.

---

## 4. Star Schema Relationship Architecture

Configure single-direction 1-to-Many ($1 \rightarrow *$) active relationships between dimensions and fact tables:

```
                  dim_date (1)
                   /       \
              (1->*)      (1->*)
                 /           \
   vw_pbi_fact_sales (N)    vw_pbi_fact_forecast (N)
        /      |       \
    (N<-1)   (N<-1)   (N<-1)
      /        |        \
dim_customer  dim_product  dim_store
    (1)          (1)          (1)
```

### Relationship Specification Table

| Primary Key (Dimension) | Foreign Key (Fact) | Cardinality | Cross-Filter Direction | State | Rationale |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `dim_date[date_key]` | `vw_pbi_fact_sales[date_key]` | $1 \rightarrow *$ | Single | **Active** | Filters sales transactions chronologically |
| `dim_date[date_key]` | `vw_pbi_fact_forecast[date_key]` | $1 \rightarrow *$ | Single | **Active** | Filters forecast records chronologically |
| `dim_customer[customer_key]` | `vw_pbi_fact_sales[customer_key]` | $1 \rightarrow *$ | Single | **Active** | Segment sales by Identified vs Anonymous |
| `dim_product[product_key]` | `vw_pbi_fact_sales[product_key]` | $1 \rightarrow *$ | Single | **Active** | Segment sales by Category and SKU |
| `dim_store[store_key]` | `vw_pbi_fact_sales[store_key]` | $1 \rightarrow *$ | Single | **Active** | Segment sales across 30 store locations |

> [!IMPORTANT]
> `vw_pbi_fact_sales` and `vw_pbi_fact_forecast` co-exist through shared `dim_date` filtering. There is NO direct relationship between `vw_pbi_fact_sales` and `vw_pbi_fact_forecast`.

---

## 5. DAX Measure Layer Catalog

Create a dedicated measure table named `_Measures` in Power BI.

### 5.1 Financial Core Measures

```dax
// 1. Gross Sales ($)
Gross Sales = SUM(vw_pbi_fact_sales[gross_sales])

// 2. Signed Discounts ($)
Discounts Signed = SUM(vw_pbi_fact_sales[discounts])

// 3. Discount Amount ($ Absolute)
Discount Amount = SUM(vw_pbi_fact_sales[discount_amount])

// 4. Net Revenue ($)
Net Revenue = SUM(vw_pbi_fact_sales[net_sales])

// 5. Cost of Goods Sold ($)
COGS = SUM(vw_pbi_fact_sales[cogs])

// 6. Gross Profit ($)
Gross Profit = SUM(vw_pbi_fact_sales[gross_profit])

// 7. Gross Margin %
Gross Margin % = DIVIDE([Gross Profit], [Net Revenue], 0)

// 8. Discount Rate %
Discount Rate % = DIVIDE([Discount Amount], [Gross Sales], 0)
```

### 5.2 Operational & Transactional Measures

```dax
// 9. Total Units Sold
Total Units = SUM(vw_pbi_fact_sales[qty])

// 10. Transaction Line Items Count
Transaction Lines = COUNTROWS(vw_pbi_fact_sales)

// 11. Distinct Header Transactions
Distinct Transactions = DISTINCTCOUNT(vw_pbi_fact_sales[transaction_id])

// 12. Average Order Value ($ AOV)
Average Order Value = DIVIDE([Net Revenue], [Distinct Transactions], 0)

// 13. Refund Line Items
Refund Line Items = CALCULATE(COUNTROWS(vw_pbi_fact_sales), vw_pbi_fact_sales[event_type] = "Refund")

// 14. Refund Revenue Impact ($ Absolute)
Refund Revenue Impact = CALCULATE(SUM(vw_pbi_fact_sales[discount_amount]) + SUM(vw_pbi_fact_sales[gross_sales]), vw_pbi_fact_sales[event_type] = "Refund")

// 15. Refund Rate %
Refund Rate % = DIVIDE([Refund Line Items], [Transaction Lines], 0)
```

### 5.3 Customer Segment Measures

```dax
// 16. Identified Customer Revenue ($)
Identified Customer Revenue = CALCULATE([Net Revenue], dim_customer[customer_type] = "Identified")

// 17. Anonymous Guest Revenue ($)
Anonymous Guest Revenue = CALCULATE([Net Revenue], dim_customer[customer_type] = "Anonymous")

// 18. Identified Customer AOV ($)
Identified Customer AOV = CALCULATE([Average Order Value], dim_customer[customer_type] = "Identified")

// 19. Anonymous Guest AOV ($)
Anonymous Guest AOV = CALCULATE([Average Order Value], dim_customer[customer_type] = "Anonymous")
```

### 5.4 Time Intelligence & Growth Measures

```dax
// 20. Net Revenue Prior Month ($)
Net Revenue PM = CALCULATE([Net Revenue], DATEADD(dim_date[date], -1, MONTH))

// 21. Net Revenue MoM Growth %
Revenue MoM % = DIVIDE([Net Revenue] - [Net Revenue PM], [Net Revenue PM], 0)

// 22. Net Revenue Prior Year ($)
Net Revenue PY = CALCULATE([Net Revenue], SAMEPERIODLASTYEAR(dim_date[date]))

// 23. Net Revenue YoY Growth %
Revenue YoY % = DIVIDE([Net Revenue] - [Net Revenue PY], [Net Revenue PY], 0)

// 24. Gross Profit Prior Year ($)
Gross Profit PY = CALCULATE([Gross Profit], SAMEPERIODLASTYEAR(dim_date[date]))

// 25. Gross Profit YoY Growth %
Gross Profit YoY % = DIVIDE([Gross Profit] - [Gross Profit PY], [Gross Profit PY], 0)
```

### 5.5 Forecast & Prediction Interval Measures

```dax
// 26. Forecasted Net Revenue ($)
Forecast Net Revenue = SUM(vw_pbi_fact_forecast[forecast_net_revenue])

// 27. Forecast 95% Lower Bound ($)
Forecast Lower Bound = SUM(vw_pbi_fact_forecast[lower_bound_95])

// 28. Forecast 95% Upper Bound ($)
Forecast Upper Bound = SUM(vw_pbi_fact_forecast[upper_bound_95])

// 29. Actual or Forecast Net Revenue ($ Combined Visual Measure)
Combined Revenue = IF(ISBLANK([Net Revenue]), [Forecast Net Revenue], [Net Revenue])
```

---

## 6. Power BI Desktop Manual Setup Instructions

1. **Launch Power BI Desktop** and choose **Get Data** $\rightarrow$ **PostgreSQL database**.
2. Enter Server `localhost` and Database `novamart_db`. Select **Data Connectivity mode: Import**.
3. Select schema `novamart` and load tables: `dim_date`, `dim_customer`, `dim_product`, `dim_store`, `vw_pbi_fact_sales`, `vw_pbi_fact_forecast`.
4. Open **Model View** and verify relationships match Section 4:
   - Ensure `dim_date` is marked as Date Table (`dim_date[date]`).
   - Confirm all cross-filter directions are **Single**.
5. Create New Table `_Measures` and paste DAX measures from Section 5.
6. Format measures:
   - Currency ($): `Gross Sales`, `Net Revenue`, `COGS`, `Gross Profit`, `Average Order Value`, `Refund Revenue Impact`, `Forecast Net Revenue` (Format: `$#,##0.00`).
   - Percentages (%): `Gross Margin %`, `Discount Rate %`, `Refund Rate %`, `Revenue MoM %`, `Revenue YoY %`, `Gross Profit YoY %` (Format: `0.00%`).
   - Whole Numbers: `Total Units`, `Transaction Lines`, `Distinct Transactions`, `Refund Line Items` (Format: `#,##0`).
7. Save project file as `powerbi/NovaMart.pbix` or modern project format `powerbi/NovaMart.pbip`.

---

## 7. Model Validation & Quality Checklist

- [x] Fact row count equals exactly **970,838** records.
- [x] Unique composite business key (`transaction_id + sku + event_type`) equals **970,838**.
- [x] Dimension key uniqueness verified for `dim_customer`, `dim_product`, `dim_store`, `dim_date`.
- [x] Zero orphan foreign keys in `fact_sales`.
- [x] Extended `dim_date` covers `2024-01-01` through `2026-06-30` (912 calendar days).
- [x] `fact_forecast` contains exactly 6 monthly records (`2026-01` to `2026-06`) matching Task 10 Seasonal Naive predictions.
- [x] Net Revenue reconciles to **$46,595,173.27**.
- [x] Gross Profit reconciles to **$25,784,056.34**.
- [x] Gross Margin % reconciles to **55.3363%**.
