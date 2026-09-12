# Power BI DAX Measure Dictionary — NovaMart Financial Analytics

## 1. Document Overview

This dictionary documents all **29 standardized DAX measures** implemented in the NovaMart Power BI Data Model. Every measure complies strictly with the authoritative business definitions specified in `docs/kpi_dictionary.md` and `docs/data_contract.md`.

---

## 2. Complete DAX Measure Catalog

| Measure Name | Display Folder / Group | DAX Expression | Formatting String | Business Rationale & Description |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Sales** | `01 Financial Core` | `SUM(vw_pbi_fact_sales[gross_sales])` | `$#,##0.00` | Total gross sales value prior to discounts or returns. |
| **Discounts Signed** | `01 Financial Core` | `SUM(vw_pbi_fact_sales[discounts])` | `$#,##0.00` | Total signed discount value (negative). |
| **Discount Amount** | `01 Financial Core` | `SUM(vw_pbi_fact_sales[discount_amount])` | `$#,##0.00` | Absolute positive discount value for reporting. |
| **Net Revenue** | `01 Financial Core` | `SUM(vw_pbi_fact_sales[net_sales])` | `$#,##0.00` | Primary financial target ($Gross Sales + Signed Discounts$). |
| **COGS** | `01 Financial Core` | `SUM(vw_pbi_fact_sales[cogs])` | `$#,##0.00` | Direct Cost of Goods Sold. |
| **Gross Profit** | `01 Financial Core` | `SUM(vw_pbi_fact_sales[gross_profit])` | `$#,##0.00` | Net margin ($Net Revenue - COGS$). |
| **Gross Margin %** | `01 Financial Core` | `DIVIDE([Gross Profit], [Net Revenue], 0)` | `0.00%` | Profitability efficiency percentage (Baseline: 55.34%). |
| **Discount Rate %** | `01 Financial Core` | `DIVIDE([Discount Amount], [Gross Sales], 0)` | `0.00%` | Discount rate relative to gross sales (Baseline: 5.43%). |
| **Total Units** | `02 Operational` | `SUM(vw_pbi_fact_sales[qty])` | `#,##0` | Total physical units moved (Baseline: 1,173,116). |
| **Transaction Lines** | `02 Operational` | `COUNTROWS(vw_pbi_fact_sales)` | `#,##0` | POS line-item record count (Baseline: 970,838). |
| **Distinct Transactions** | `02 Operational` | `DISTINCTCOUNT(vw_pbi_fact_sales[transaction_id])` | `#,##0` | Header receipt transaction count (Baseline: 585,691). |
| **Average Order Value** | `02 Operational` | `DIVIDE([Net Revenue], [Distinct Transactions], 0)` | `$#,##0.00` | Net revenue per header transaction (Baseline: $79.56). |
| **Refund Line Items** | `02 Operational` | `CALCULATE(COUNTROWS(vw_pbi_fact_sales), vw_pbi_fact_sales[event_type] = "Refund")` | `#,##0` | Count of return line items (Baseline: 9,449). |
| **Refund Revenue Impact** | `02 Operational` | `CALCULATE(SUM(vw_pbi_fact_sales[discount_amount]) + SUM(vw_pbi_fact_sales[gross_sales]), vw_pbi_fact_sales[event_type] = "Refund")` | `$#,##0.00` | Absolute gross revenue reduction from returns ($396,495.00). |
| **Refund Rate %** | `02 Operational` | `DIVIDE([Refund Line Items], [Transaction Lines], 0)` | `0.00%` | Percentage of transaction line items refunded (0.97%). |
| **Identified Customer Revenue** | `03 Customer Segments` | `CALCULATE([Net Revenue], dim_customer[customer_type] = "Identified")` | `$#,##0.00` | Net revenue contributed by registered customers. |
| **Anonymous Guest Revenue** | `03 Customer Segments` | `CALCULATE([Net Revenue], dim_customer[customer_type] = "Anonymous")` | `$#,##0.00` | Net revenue contributed by anonymous guest checkout. |
| **Identified Customer AOV** | `03 Customer Segments` | `CALCULATE([Average Order Value], dim_customer[customer_type] = "Identified")` | `$#,##0.00` | Average order value for registered customers. |
| **Anonymous Guest AOV** | `03 Customer Segments` | `CALCULATE([Average Order Value], dim_customer[customer_type] = "Anonymous")` | `$#,##0.00` | Average order value for anonymous guests. |
| **Net Revenue PM** | `04 Time Intelligence` | `CALCULATE([Net Revenue], DATEADD(dim_date[date], -1, MONTH))` | `$#,##0.00` | Net revenue for the prior calendar month. |
| **Revenue MoM %** | `04 Time Intelligence` | `DIVIDE([Net Revenue] - [Net Revenue PM], [Net Revenue PM], 0)` | `0.00%` | Month-over-month net revenue growth percentage. |
| **Net Revenue PY** | `04 Time Intelligence` | `CALCULATE([Net Revenue], SAMEPERIODLASTYEAR(dim_date[date]))` | `$#,##0.00` | Net revenue for the same period last year. |
| **Revenue YoY %** | `04 Time Intelligence` | `DIVIDE([Net Revenue] - [Net Revenue PY], [Net Revenue PY], 0)` | `0.00%` | Year-over-year net revenue growth percentage. |
| **Gross Profit PY** | `04 Time Intelligence` | `CALCULATE([Gross Profit], SAMEPERIODLASTYEAR(dim_date[date]))` | `$#,##0.00` | Gross profit for the same period last year. |
| **Gross Profit YoY %** | `04 Time Intelligence` | `DIVIDE([Gross Profit] - [Gross Profit PY], [Gross Profit PY], 0)` | `0.00%` | Year-over-year gross profit growth percentage. |
| **Forecast Net Revenue** | `05 Forecasting` | `SUM(vw_pbi_fact_forecast[forecast_net_revenue])` | `$#,##0.00` | Model point prediction for future net revenue. |
| **Forecast Lower Bound** | `05 Forecasting` | `SUM(vw_pbi_fact_forecast[lower_bound_95])` | `$#,##0.00` | 95% empirical prediction interval lower bound. |
| **Forecast Upper Bound** | `05 Forecasting` | `SUM(vw_pbi_fact_forecast[upper_bound_95])` | `$#,##0.00` | 95% empirical prediction interval upper bound. |
| **Combined Revenue** | `05 Forecasting` | `IF(ISBLANK([Net Revenue]), [Forecast Net Revenue], [Net Revenue])` | `$#,##0.00` | Combined actual net revenue (2024-2025) & forecast (2026). |
