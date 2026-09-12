# Power BI Report Design & Visual Layout Specification

## 1. Executive Summary & Design System

This document specifies the complete visual design system, page layouts, visual container configurations, slicer placements, drill-through fields, custom tooltips, and navigation rules for the **NovaMart Retail Power BI Dashboard**.

### Design Philosophy
- **Executive-First Hierarchy:** High-level KPI cards placed at top-left; primary trend charts in center; detailed multi-column matrices at bottom.
- **Color Palette & Contrast:**
  - **Primary Brand / Actuals:** Deep Slate Navy (`#1E293B` / `#0F172A`)
  - **Accent / Highlight:** Cobalt Blue (`#2563EB`)
  - **Forecast Trend:** Amber / Bronze (`#D97706` / `#F59E0B`) with 20% alpha shaded interval ribbon.
  - **Positive Margin / Growth:** Forest Emerald (`#059669`)
  - **Negative Margin / Refund Warning:** Crimson Red (`#DC2626`)
  - **Neutral Grid / Cards:** Off-White Card Background (`#F8FAFC`), Slate Border (`#E2E8F0`).
- **Typography & Formatting:**
  - **Font Family:** Segoe UI (Power BI Native Standard).
  - **KPI Title:** 10pt Semi-Bold Grey (`#64748B`).
  - **KPI Callout Value:** 24pt Bold Dark Slate (`#0F172A`).
  - **Visual Chart Titles:** 12pt Bold Dark Navy (`#1E293B`).

---

## 2. Report Page Architecture Overview

The report consists of **5 main analytical pages** plus **2 dedicated drill-through pages**:

1. `01 Executive Overview` (C-Suite performance dashboard)
2. `02 Revenue & Profitability` (P&L breakdown, discounts, margin analysis)
3. `03 Product & Category` (SKU rankings, margin performance, category mix)
4. `04 Store & Customer` (Store location rankings & Identified vs Anonymous customer mix)
5. `05 Forecast & Outlook` (6-month Seasonal Naive revenue predictions & 95% bounds)
6. `Drillthrough_Product_Detail` (Deep-dive SKU analysis page)
7. `Drillthrough_Store_Detail` (Deep-dive Store location performance page)

---

## 3. Page Specifications & Visual Layouts

### Page 1 — `01 Executive Overview`
- **Page Purpose:** Provide C-suite executives with an immediate, high-impact view of top-line revenue, gross profit, margin efficiency, transaction volume, and key analytical findings.
- **Top Row KPI Cards (X=0 to 1200, Y=40, H=90):**
  - `Net Revenue`: `$46,595,173.27`
  - `Gross Profit`: `$25,784,056.34`
  - `Gross Margin %`: `55.34%`
  - `Total Units`: `1,173,116`
  - `Distinct Transactions`: `585,691`
  - `Average Order Value`: `$79.56`
- **Main Body Visuals:**
  1. *Monthly Net Revenue Trend (2024–2025)* (Line Chart, 24 months, chronological X-axis).
  2. *Monthly Gross Profit Trend* (Area Chart, showing steady profit expansion).
  3. *Revenue YoY Comparison* (Clustered Column Chart, comparing 2024 vs 2025 month-by-month).
  4. *Category Revenue Contribution* (Donut Chart: Apparel 32.0%, Footwear 25.8%, Electronics 15.2%, Home & Kitchen 12.5%, Beauty 8.4%, Food & Bev 6.1%).
  5. *Store Performance Ranking* (Horizontal Bar Chart, top 30 retail store locations).
  6. *Executive Business Insights Box* (Formatted Text Box highlighting December peak, Apparel/Footwear dominance, Electronics margin lead, and Anonymous guest revenue share).
- **Global Page Slicers (Top Banner, Y=0):**
  - `Year` (Multi-select), `Quarter`, `Month`, `Category`, `Store`, `Customer Segment`.

---

### Page 2 — `02 Revenue & Profitability`
- **Page Purpose:** In-depth financial P&L decomposition covering Gross Sales, Promotional Discounts, Net Revenue, COGS, Gross Profit, and Margin percentages.
- **Top Row KPI Cards:**
  - `Gross Sales`: `$49,269,500.50`
  - `Discount Amount`: `$2,674,327.23`
  - `Net Revenue`: `$46,595,173.27`
  - `COGS`: `$20,811,116.93`
  - `Gross Profit`: `$25,784,056.34`
  - `Gross Margin %`: `55.34%`
  - `Discount Rate %`: `5.43%`
- **Main Body Visuals:**
  1. *Gross Sales vs Net Revenue Trend* (Combo Line/Column Chart illustrating discount gap).
  2. *Monthly Gross Margin % Line* (Tracking profitability consistency between 54.8% and 56.1%).
  3. *Revenue MoM % Growth* (Waterfall / Column Chart highlighting monthly velocity).
  4. *Revenue YoY % Growth* (Column Chart tracking 2025 vs 2024 expansion).
  5. *Category Profitability Matrix* (Multi-column Matrix: Category, Gross Sales, Discount Amount, Net Revenue, COGS, Gross Profit, Gross Margin %, Discount Rate %).
  6. *Discount Analysis by Category & Store* (Clustered Bar Chart).
- **Slicers:** `Year`, `Quarter`, `Category`, `Store`.

---

### Page 3 — `03 Product & Category`
- **Page Purpose:** SKU-level merchandise performance analysis, top/bottom product identification, and category margin benchmarking.
- **Main Body Visuals:**
  1. *Top 10 Products by Net Revenue* (Horizontal Bar Chart).
  2. *Top 10 Products by Gross Profit* (Horizontal Bar Chart).
  3. *Bottom 10 Products by Gross Profit* (Horizontal Bar Chart, enabling low-margin SKU detection).
  4. *Category Revenue vs Gross Profit* (Clustered Column Chart).
  5. *Product Gross Margin % Distribution* (Scatter / Column Chart).
  6. *Product Detail Matrix* (Columns: `SKU`, `Product Name`, `Category`, `Total Units`, `Net Revenue`, `Gross Profit`, `Gross Margin %`, `Refund Line Items`).
- **Interactive Drilldown:** Category $\rightarrow$ SKU hierarchy. Top/Bottom 10 filters dynamically update under slicer context.
- **Slicers:** `Year`, `Category`, `Product`, `Store`.

---

### Page 4 — `04 Store & Customer`
- **Page Purpose:** Dual analytical breakdown comparing store location performance and customer segment purchasing behavior.
- **Store Section (Left Half):**
  1. *Store Net Revenue Ranking* (Horizontal Bar Chart across 30 stores).
  2. *Store Gross Profit Ranking* (Horizontal Bar Chart).
  3. *Store Average Order Value ($ AOV)* (Column Chart by City).
  4. *Store Performance Matrix* (`Store`, `City`, `Net Revenue`, `Gross Profit`, `Gross Margin %`, `Units`, `Transactions`, `AOV`, `Refund Lines`).
- **Customer Section (Right Half):**
  5. *Identified vs Anonymous Guest Revenue Contribution* (Donut Chart: 71.9% Anonymous vs 28.1% Identified).
  6. *Identified vs Anonymous Guest AOV Comparison* (Bar Chart: `$98.12` Identified vs `$72.54` Anonymous).
  7. *Customer Segment Performance Table* (`Customer Type`, `Transactions`, `Net Revenue`, `Gross Profit`, `AOV`, `Refund Rate %`).
- **Slicers:** `Year`, `Category`, `Store`, `Customer Segment`.

---

### Page 5 — `05 Forecast & Outlook`
- **Page Purpose:** Present the official Task 10 Seasonal Naive (Lag 12) 6-month forward revenue forecast (Jan–Jun 2026) alongside prediction bounds and model benchmarks.
- **Top Row KPI Cards:**
  - `Historical Net Revenue (2024-2025)`: `$46,595,173.27`
  - `Forecast H1 2026 Revenue`: `$11,487,927.00`
  - `Forecast Avg Monthly Revenue`: `$1,914,654.50`
  - `Champion Model`: `Seasonal Naive (Lag 12)`
  - `Historical Backtest WAPE`: `5.20%`
- **Main Body Visuals:**
  1. *Historical Net Revenue & 2026 Forward Forecast Chart* (Solid Navy line for 2024-2025 actuals; Dashed Amber line for 2026 forecast; 20% alpha shaded Amber ribbon for 95% prediction interval).
  2. *H1 2026 Forecast Monthly Table*:
     - `2026-01`: Forecast `$1,521,877.18` (Lower: `$1,432,888.01`, Upper: `$1,610,866.35`)
     - `2026-02`: Forecast `$1,738,075.29` (Lower: `$1,649,086.12`, Upper: `$1,827,064.46`)
     - `2026-03`: Forecast `$2,077,924.19` (Lower: `$1,988,935.02`, Upper: `$2,166,913.36`)
     - `2026-04`: Forecast `$1,907,958.09` (Lower: `$1,818,968.92`, Upper: `$1,996,947.26`)
     - `2026-05`: Forecast `$2,252,591.87` (Lower: `$2,163,602.70`, Upper: `$2,341,581.04`)
     - `2026-06`: Forecast `$1,989,500.38` (Lower: `$1,900,511.21`, Upper: `$2,078,489.55`)
  3. *Task 10 Model Backtest Benchmarks Table* (Comparing Seasonal Naive WAPE 5.20%, ARIMA(0,1,1) 5.94%, ARIMA(1,1,0) 6.08%, ARIMA(1,1,1) 6.16%, Naive 7.29%).
  4. *Mandatory Forecast Disclaimer Box*:
     > **FORECAST DISCLAIMER:**  
     > Forecast values are analytical estimates generated by the approved Seasonal Naive (Lag 12) champion model based on 2024–2025 historical sales. Actual 2026 revenue data is not yet available.
- **Slicers:** `Category`, `Store`.

---

## 4. Drill-Through Pages Specification

### 1. `Drillthrough_Product_Detail`
- **Target Field:** `dim_product[sku]` or `dim_product[item]`
- **Visuals:** Product Name & Category header card; Monthly Revenue Trend line chart; Net Revenue, Gross Profit, Gross Margin %, Units, and Refund Line Items KPI cards; Store breakdown table for the selected product.

### 2. `Drillthrough_Store_Detail`
- **Target Field:** `dim_store[store_id]` or `dim_store[store_name]`
- **Visuals:** Store Name & City header card; Monthly Revenue & Margin trend; Net Revenue, Gross Profit, AOV, Transactions, and Refund Rate % cards; Product Category breakdown table for the selected store.

---

## 5. Report Interactions, Tooltips, & Formatting Rules

- **Visual Interactions:**
  - Slicers set to filter all relevant page visuals.
  - Slicer selection on `dim_product[category]` dynamically filters Product matrices and rankings.
  - Slicer selection on `dim_store[store_name]` dynamically filters Store and Customer visuals.
- **Custom Tooltips:**
  - *Revenue Tooltip:* Net Revenue, Gross Profit, Gross Margin %, YoY Growth %.
  - *Product Tooltip:* Item Name, Category, Units Sold, Net Revenue, Gross Profit, Refund Lines.
  - *Forecast Tooltip:* Target Month, Forecast Revenue, 95% Lower Bound, 95% Upper Bound, Model Tag.
- **Conditional Formatting Rules:**
  - `Gross Margin %`: Green gradient for $\ge 55.0\%$; Amber gradient for $50.0\% - 54.9\%$; Red tint for $< 50.0\%$.
  - `Refund Rate %`: Highlight red if $> 1.5\%$.
