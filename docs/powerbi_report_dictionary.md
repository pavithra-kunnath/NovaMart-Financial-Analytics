# Power BI Report Visual Dictionary & Layout Catalog

## 1. Document Purpose

This document provides a comprehensive catalog of all **35 visual containers** implemented across the 5 report pages of the NovaMart Power BI Dashboard. Every visual is mapped to its underlying DAX measures, column fields, visual type, and filter context.

---

## 2. Visual Catalog by Page

### 2.1 Page 1: `01 Executive Overview`

| Visual ID | Visual Type | Title | Data Fields & DAX Measures Bound | Filter & Interaction Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `P1_CARD_01` | Card | Net Revenue | `[Net Revenue]` ($46,595,173.27) | Responds to all slicers. |
| `P1_CARD_02` | Card | Gross Profit | `[Gross Profit]` ($25,784,056.34) | Responds to all slicers. |
| `P1_CARD_03` | Card | Gross Margin % | `[Gross Margin %]` (55.34%) | Responds to all slicers. |
| `P1_CARD_04` | Card | Total Units | `[Total Units]` (1,173,116) | Responds to all slicers. |
| `P1_CARD_05` | Card | Transactions | `[Distinct Transactions]` (585,691) | Responds to all slicers. |
| `P1_CARD_06` | Card | Average Order Value | `[Average Order Value]` ($79.56) | Responds to all slicers. |
| `P1_CHART_01`| Line Chart | Monthly Net Revenue Trend | X: `dim_date[year_month]`, Y: `[Net Revenue]` | Chronological sequence 2024-01 to 2025-12. |
| `P1_CHART_02`| Area Chart | Monthly Gross Profit Trend | X: `dim_date[year_month]`, Y: `[Gross Profit]` | Chronological sequence 2024-01 to 2025-12. |
| `P1_CHART_03`| Column Chart| Revenue YoY Comparison | X: `dim_date[month_name]`, Legend: `dim_date[year]`, Y: `[Net Revenue]` | Compares monthly performance across years. |
| `P1_CHART_04`| Donut Chart | Category Revenue Contribution | Legend: `dim_product[category]`, Values: `[Net Revenue]` | Highlights Apparel & Footwear dominance. |
| `P1_CHART_05`| Bar Chart | Store Performance Ranking | Y: `dim_store[store_name]`, X: `[Net Revenue]` | Top 30 retail store locations. |
| `P1_TEXT_01` | Text Box | Key Executive Insights | Formatted text box summarizing validated EDA & SQL findings | Static commentary. |

---

### 2.2 Page 2: `02 Revenue & Profitability`

| Visual ID | Visual Type | Title | Data Fields & DAX Measures Bound | Filter & Interaction Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `P2_CARD_01` | Card | Gross Sales | `[Gross Sales]` ($49,269,500.50) | Responds to all slicers. |
| `P2_CARD_02` | Card | Discount Amount | `[Discount Amount]` ($2,674,327.23) | Responds to all slicers. |
| `P2_CARD_03` | Card | Net Revenue | `[Net Revenue]` ($46,595,173.27) | Responds to all slicers. |
| `P2_CARD_04` | Card | COGS | `[COGS]` ($20,811,116.93) | Responds to all slicers. |
| `P2_CARD_05` | Card | Gross Profit | `[Gross Profit]` ($25,784,056.34) | Responds to all slicers. |
| `P2_CARD_06` | Card | Gross Margin % | `[Gross Margin %]` (55.34%) | Responds to all slicers. |
| `P2_CARD_07` | Card | Discount Rate % | `[Discount Rate %]` (5.43%) | Responds to all slicers. |
| `P2_CHART_01`| Combo Chart | Gross Sales vs Net Revenue | X: `dim_date[year_month]`, Series: `[Gross Sales]`, `[Net Revenue]` | Displays discount gap month-by-month. |
| `P2_CHART_02`| Line Chart | Monthly Gross Margin % | X: `dim_date[year_month]`, Y: `[Gross Margin %]` | Evaluates margin stability (54.8% - 56.1%). |
| `P2_CHART_03`| Column Chart| Revenue MoM % Growth | X: `dim_date[year_month]`, Y: `[Revenue MoM %]` | Monthly revenue growth rate. |
| `P2_CHART_04`| Column Chart| Revenue YoY % Growth | X: `dim_date[year_month]`, Y: `[Revenue YoY %]` | Year-over-year expansion rate. |
| `P2_MAT_01`  | Matrix | Category Profitability Matrix | Rows: `dim_product[category]`, Cols: `[Gross Sales]`, `[Discount Amount]`, `[Net Revenue]`, `[COGS]`, `[Gross Profit]`, `[Gross Margin %]`, `[Discount Rate %]` | Comprehensive P&L breakdown by category. |

---

### 2.3 Page 3: `03 Product & Category`

| Visual ID | Visual Type | Title | Data Fields & DAX Measures Bound | Filter & Interaction Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `P3_CHART_01`| Bar Chart | Top 10 Products by Net Revenue | Y: `dim_product[item]`, X: `[Net Revenue]`, TopN: 10 | Responds to Category/Store filters. |
| `P3_CHART_02`| Bar Chart | Top 10 Products by Gross Profit | Y: `dim_product[item]`, X: `[Gross Profit]`, TopN: 10 | Responds to Category/Store filters. |
| `P3_CHART_03`| Bar Chart | Bottom 10 Products by Gross Profit| Y: `dim_product[item]`, X: `[Gross Profit]`, BottomN: 10 | Responds to Category/Store filters. |
| `P3_CHART_04`| Column Chart| Category Net Revenue vs Profit | X: `dim_product[category]`, Series: `[Net Revenue]`, `[Gross Profit]` | Category side-by-side comparison. |
| `P3_MAT_01`  | Matrix | Product Detail Matrix | Rows: `dim_product[sku]`, `dim_product[item]`, `dim_product[category]`, Cols: `[Total Units]`, `[Net Revenue]`, `[Gross Profit]`, `[Gross Margin %]`, `[Refund Line Items]` | Drill-through target for SKU deep-dive. |

---

### 2.4 Page 4: `04 Store & Customer`

| Visual ID | Visual Type | Title | Data Fields & DAX Measures Bound | Filter & Interaction Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `P4_CHART_01`| Bar Chart | Store Net Revenue Ranking | Y: `dim_store[store_name]`, X: `[Net Revenue]` | Ranks all 30 store locations. |
| `P4_CHART_02`| Bar Chart | Store Gross Profit Ranking | Y: `dim_store[store_name]`, X: `[Gross Profit]` | Ranks profit contribution by store. |
| `P4_CHART_03`| Column Chart| Store Average Order Value ($ AOV)| X: `dim_store[city]`, Y: `[Average Order Value]` | AOV variation across cities. |
| `P4_MAT_01`  | Matrix | Store Location Performance Matrix| Rows: `dim_store[store_name]`, `dim_store[city]`, Cols: `[Net Revenue]`, `[Gross Profit]`, `[Gross Margin %]`, `[Total Units]`, `[Distinct Transactions]`, `[Average Order Value]`, `[Refund Line Items]` | Full store performance drilldown. |
| `P4_CHART_04`| Pie Chart | Customer Segment Revenue Split | Legend: `dim_customer[customer_type]`, Values: `[Net Revenue]` | Identified ($13.11M) vs Anonymous ($33.48M). |
| `P4_CHART_05`| Column Chart| Customer Segment AOV Comparison | X: `dim_customer[customer_type]`, Y: `[Average Order Value]` | Identified ($98.12) vs Anonymous ($72.54). |

---

### 2.5 Page 5: `05 Forecast & Outlook`

| Visual ID | Visual Type | Title | Data Fields & DAX Measures Bound | Filter & Interaction Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `P5_CARD_01` | Card | Historical Net Revenue | `[Net Revenue]` ($46,595,173.27) | Covers 2024-01 to 2025-12. |
| `P5_CARD_02` | Card | Forecast H1 2026 Revenue | `[Forecast Net Revenue]` ($11,487,927.00) | Sum of Jan-Jun 2026 predictions. |
| `P5_CARD_03` | Card | Forecast Avg Monthly Revenue | `[Forecast Avg Monthly Revenue]` ($1,914,654.50) | Average monthly prediction. |
| `P5_CARD_04` | Card | Champion Model | Text: `Seasonal Naive (Lag 12)` | Task 10 Approved Champion. |
| `P5_CARD_05` | Card | Historical Backtest WAPE | Text: `5.20%` | Verified 2025 Backtest WAPE. |
| `P5_CHART_01`| Line & Ribbon| 2024-2025 Actuals & 2026 Forecast | X: `dim_date[year_month]`, Lines: `[Net Revenue]`, `[Forecast Net Revenue]`, Ribbon: `[Forecast Lower Bound]`, `[Forecast Upper Bound]` | Visual separation of actuals vs forecast. |
| `P5_TABLE_01`| Table | H1 2026 Forecast Monthly Table | Cols: `vw_pbi_fact_forecast[forecast_month]`, `[forecast_net_revenue]`, `[lower_bound_95]`, `[upper_bound_95]`, `[model_name]` | 6 monthly forecast records. |
| `P5_TABLE_02`| Table | Task 10 Model Comparison Table | Cols: `Model Name`, `MAE`, `RMSE`, `MAPE (%)`, `sMAPE (%)`, `WAPE (%)` | Benchmarks all 6 evaluated models. |
| `P5_TEXT_01` | Text Box | Forecast Disclaimer Box | Text: Mandatory analytical forecast disclaimer | Static disclaimer. |
