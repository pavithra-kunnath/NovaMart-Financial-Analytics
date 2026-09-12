# Power BI Data Model Architecture & Schema Specification

## 1. Executive Summary & Architecture Overview

The **NovaMart Retail Power BI Data Model** is structured as an analytical **Star Schema** designed for enterprise performance analytics, financial reporting, and revenue forecasting integration.

The model is sourced directly from the authoritative PostgreSQL Data Warehouse (`novamart_db`, schema `novamart`) and imported into Power BI using VertiPaq Import Mode for high-performance sub-second DAX execution.

---

## 2. Conceptual Star Schema Diagram

```
                              [dim_date] (Calendar)
                               (1)      (1)
                                |        |
                             (1->*)    (1->*)
                                |        |
[dim_customer] (1) ---> (1->*) [fact_sales] (N) <--- (1->*) [dim_product] (1)
                                |
                             (1->*)
                                |
                        [dim_store] (1)

                        [fact_forecast] (N) <--- (1<-1) [dim_date] (1)
```

---

## 3. Fact Tables & Granularity

### 3.1 `vw_pbi_fact_sales` (Sales Fact Table)
- **Source Object:** `novamart.vw_pbi_fact_sales` / `novamart.fact_sales`
- **Granularity:** One record per individual Point-of-Sale (POS) line-item transaction event.
- **Composite Business Key:** `transaction_id + sku + event_type`
- **Row Count:** Exactly **970,838** records (covering 2024-01-01 to 2025-12-31).
- **Primary Metrics:** `qty`, `unit_price`, `gross_sales`, `discounts`, `discount_amount`, `net_sales`, `unit_cost`, `cogs`, `gross_profit`, `tax`, `total_collected`.
- **Event Types:** `'Payment'` (Standard sale) and `'Refund'` (Customer return line item).

### 3.2 `vw_pbi_fact_forecast` (Revenue Forecast Fact Table)
- **Source Object:** `novamart.vw_pbi_fact_forecast` / `novamart.fact_forecast`
- **Granularity:** One record per target forecast month.
- **Primary Key:** `forecast_month` (e.g. `2026-01` to `2026-06`).
- **Row Count:** Exactly **6** records (Jan–Jun 2026).
- **Primary Metrics:** `forecast_net_revenue`, `lower_bound_95`, `upper_bound_95`.
- **Model Tag:** `'Seasonal Naive (Lag 12)'` (Task 10 Approved Champion Model).

---

## 4. Dimension Tables

### 4.1 `dim_date` (Calendar Dimension)
- **Primary Key:** `date_key` (Format: `YYYYMMDD`, e.g. `20240101`).
- **Date Range:** `2024-01-01` through `2026-06-30` (**912 calendar days**).
- **Role:** Central time dimension connecting historical sales (2024–2025) and forward forecasts (2026-01 to 2026-06).
- **Attributes:** `date`, `year`, `month_number`, `month_name`, `quarter`, `year_month`, `day_of_week`, `is_weekend`, `financial_year`.
- **Sorting Configuration:** `month_name` sorted by `month_number`; `year_month` sorted by `date_key`. Marked as Power BI Date Table (`dim_date[date]`).

### 4.2 `dim_customer` (Customer Dimension)
- **Primary Key:** `customer_key`.
- **Natural Key:** `customer_id`.
- **Row Count:** **20,000** unique customer entities + default `CUST_ANONYMOUS`.
- **Classification:** `customer_type` ('Identified' vs 'Anonymous').

### 4.3 `dim_product` (Product Dimension)
- **Primary Key:** `product_key`.
- **Natural Key:** `sku`.
- **Row Count:** **67** unique SKUs across **6** merchandise categories.
- **Attributes:** `item`, `category`, `price_point_name`, `unit_price`, `unit_cost`.

### 4.4 `dim_store` (Retail Store Dimension)
- **Primary Key:** `store_key`.
- **Natural Key:** `store_id`.
- **Row Count:** **30** retail store locations.
- **Attributes:** `store_name`, `city`.

---

## 5. Relationship Map Specification

All relationships are 1-to-Many ($1 \rightarrow *$), single direction, active:

1. `dim_date[date_key]` ($1$) $\rightarrow$ `vw_pbi_fact_sales[date_key]` ($*$) [Active]
2. `dim_date[date_key]` ($1$) $\rightarrow$ `vw_pbi_fact_forecast[date_key]` ($*$) [Active]
3. `dim_customer[customer_key]` ($1$) $\rightarrow$ `vw_pbi_fact_sales[customer_key]` ($*$) [Active]
4. `dim_product[product_key]` ($1$) $\rightarrow$ `vw_pbi_fact_sales[product_key]` ($*$) [Active]
5. `dim_store[store_key]` ($1$) $\rightarrow$ `vw_pbi_fact_sales[store_key]` ($*$) [Active]

---

## 6. Storage Mode & Performance Optimization

- **Storage Mode:** **Import Mode** (VertiPaq In-Memory Engine).
- **Compressibility:** High column cardinality optimization.
- **Query Execution:** Sub-second response time for multi-dimensional time intelligence aggregations.
