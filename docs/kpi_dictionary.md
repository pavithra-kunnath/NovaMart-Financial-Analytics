# KPI Dictionary — NovaMart Financial Analytics

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 8 — SQL Financial Analysis & KPI Validation  
**Status:** Approved & Formally Specified  

---

## 1. Executive Summary & Purpose

This KPI Dictionary establishes formal, binding business definitions, mathematical formulations, database column mappings, and SQL logic snippets for all financial and operational key performance indicators (KPIs) used across the NovaMart Retail data warehouse, analytical views, Python models, and Power BI dashboards.

All metrics comply strictly with the rules established in `docs/data_contract.md`.

---

## 2. Core Financial & Operational KPI Catalog

### 1. Gross Sales
- **Business Description:** Total gross monetary value of merchandise sold prior to applying any promotional discounts or returns.
- **Mathematical Formula:**  
  $$\text{Gross Sales} = \sum (\text{qty} \times \text{unit\_price})$$
- **Source Table & Columns:** `novamart.fact_sales.gross_sales` (or derived from `qty * unit_price`).
- **SQL Implementation:**
  ```sql
  SUM(gross_sales) AS total_gross_sales
  ```
- **Allowed Range:** Real number ($> 0.00$ for Payment, $< 0.00$ for Refund). Overall portfolio sum $> \$0.00$.
- **Accounting Note:** Positive for sales, negative for returns.

---

### 2. Discounts (Signed)
- **Business Description:** Total monetary value of line-item promotional discounts applied at checkout.
- **Mathematical Formula:**  
  $$\text{Discounts} = \sum \text{discounts}$$
- **Source Table & Columns:** `novamart.fact_sales.discounts`.
- **SQL Implementation:**
  ```sql
  SUM(discounts) AS total_discounts_signed
  ```
- **Allowed Range:** Non-positive numeric ($\le 0.00$).

---

### 3. Discount Amount (Absolute Metric for Reporting)
- **Business Description:** Absolute positive monetary representation of discounts, used for reporting and discount rate analysis.
- **Mathematical Formula:**  
  $$\text{Discount Amount} = \sum |\text{discounts}|$$
- **Source Table & Columns:** `novamart.fact_sales.discount_amount`.
- **SQL Implementation:**
  ```sql
  SUM(discount_amount) AS total_discounts
  ```
- **Allowed Range:** Non-negative numeric ($\ge 0.00$).

---

### 4. Net Revenue / Net Sales
- **Business Description:** Net monetary revenue realized by NovaMart after subtractive discounts and refund adjustments.
- **Mathematical Formula:**  
  $$\text{Net Revenue} = \sum \text{net\_sales} = \sum (\text{gross\_sales} + \text{discounts})$$
- **Source Table & Columns:** `novamart.fact_sales.net_sales`.
- **SQL Implementation:**
  ```sql
  SUM(net_sales) AS total_net_revenue
  ```
- **Allowed Range:** Real numeric value.
- **Accounting Note:** Because return records (`event_type = 'Refund'`) carry negative `net_sales` values in `fact_sales`, direct aggregation yields true Net Revenue without double-counting.

---

### 5. Cost of Goods Sold (COGS)
- **Business Description:** Total direct product acquisition cost associated with items sold or returned.
- **Mathematical Formula:**  
  $$\text{COGS} = \sum (\text{qty} \times \text{unit\_cost})$$
- **Source Table & Columns:** `novamart.fact_sales.cogs`.
- **SQL Implementation:**
  ```sql
  SUM(cogs) AS total_cogs
  ```
- **Allowed Range:** Real numeric value (positive for sales, negative for refunds).

---

### 6. Gross Profit
- **Business Description:** Net financial margin remaining after deducting Cost of Goods Sold from Net Revenue.
- **Mathematical Formula:**  
  $$\text{Gross Profit} = \text{Net Revenue} - \text{COGS} = \sum \text{gross\_profit}$$
- **Source Table & Columns:** `novamart.fact_sales.gross_profit`.
- **SQL Implementation:**
  ```sql
  SUM(gross_profit) AS total_gross_profit
  ```
- **Allowed Range:** Real numeric value.

---

### 7. Gross Margin %
- **Business Description:** Profitability efficiency ratio indicating the percentage of Net Revenue retained as Gross Profit.
- **Mathematical Formula:**  
  $$\text{Gross Margin \%} = \begin{cases} \frac{\sum \text{gross\_profit}}{\sum \text{net\_sales}} \times 100 & \text{if } \sum \text{net\_sales} \neq 0 \\ 0.00 & \text{if } \sum \text{net\_sales} = 0 \end{cases}$$
- **Source Table & Columns:** Derived from `novamart.fact_sales`.
- **SQL Implementation:**
  ```sql
  ROUND((SUM(gross_profit) / NULLIF(SUM(net_sales), 0)) * 100, 2) AS gross_margin_pct
  ```
- **Allowed Range:** Percentage between $-100.00\%$ and $+100.00\%$ (NovaMart portfolio benchmark: $\approx 55.34\%$).

---

### 8. Discount Rate %
- **Business Description:** Percentage of Gross Sales given away as promotional discounts.
- **Mathematical Formula:**  
  $$\text{Discount Rate \%} = \begin{cases} \frac{\sum \text{discount\_amount}}{\sum \text{gross\_sales}} \times 100 & \text{if } \sum \text{gross\_sales} \neq 0 \\ 0.00 & \text{if } \sum \text{gross\_sales} = 0 \end{cases}$$
- **Source Table & Columns:** Derived from `novamart.fact_sales`.
- **SQL Implementation:**
  ```sql
  ROUND((SUM(discount_amount) / NULLIF(SUM(gross_sales), 0)) * 100, 2) AS discount_rate_pct
  ```
- **Allowed Range:** Percentage between $0.00\%$ and $100.00\%$ (NovaMart portfolio benchmark: $\approx 5.43\%$).

---

### 9. Refund Count
- **Business Description:** Total number of line-item return transactions processed.
- **Mathematical Formula:**  
  $$\text{Refund Count} = \sum \mathbb{I}(\text{event\_type} = \text{'Refund'})$$
- **Source Table & Columns:** `novamart.fact_sales.event_type`.
- **SQL Implementation:**
  ```sql
  SUM(CASE WHEN event_type = 'Refund' THEN 1 ELSE 0 END) AS refund_lines_count
  ```
- **Allowed Range:** Integer $\ge 0$ (NovaMart benchmark: 9,449 rows).

---

### 10. Refund Revenue Impact
- **Business Description:** Absolute monetary reduction in gross/net revenue caused by customer returns.
- **Mathematical Formula:**  
  $$\text{Refund Amount} = \sum_{\text{Refund}} |\text{net\_sales}|$$
- **Source Table & Columns:** `novamart.fact_sales.net_sales` filtered by `event_type = 'Refund'`.
- **SQL Implementation:**
  ```sql
  SUM(CASE WHEN event_type = 'Refund' THEN ABS(net_sales) ELSE 0 END) AS total_refund_amount
  ```
- **Allowed Range:** Non-negative numeric ($\ge 0.00$, NovaMart benchmark: $\$396,495.00$).

---

### 11. Refund Rate %
- **Business Description:** Percentage of total transaction line items that resulted in customer returns.
- **Mathematical Formula:**  
  $$\text{Refund Rate \%} = \frac{\text{Refund Count}}{\text{Total Line Items}} \times 100$$
- **Source Table & Columns:** Derived from `novamart.fact_sales`.
- **SQL Implementation:**
  ```sql
  ROUND((SUM(CASE WHEN event_type = 'Refund' THEN 1 ELSE 0 END)::NUMERIC / COUNT(sales_key)::NUMERIC) * 100, 2) AS refund_rate_pct
  ```
- **Allowed Range:** $0.00\%$ to $100.00\%$ (NovaMart benchmark: $0.97\%$).

---

### 12. Units Sold / Moved
- **Business Description:** Net physical unit volume moved across all POS sales and return events.
- **Mathematical Formula:**  
  $$\text{Units Moved} = \sum \text{qty}$$
- **Source Table & Columns:** `novamart.fact_sales.qty`.
- **SQL Implementation:**
  ```sql
  SUM(qty) AS total_units_moved
  ```
- **Allowed Range:** Integer value (NovaMart benchmark: 1,173,116 units).

---

### 13. Transaction / Line Item Count
- **Business Description:** Operational count of distinct header transaction receipts and detail line-item records.
- **Mathematical Formula:**  
  $$\text{Line Items} = \text{COUNT}(\text{sales\_key}), \quad \text{Transactions} = \text{COUNT(DISTINCT } \text{transaction\_id})$$
- **Source Table & Columns:** `novamart.fact_sales`.
- **SQL Implementation:**
  ```sql
  COUNT(sales_key) AS total_line_items,
  COUNT(DISTINCT transaction_id) AS total_transactions
  ```
- **Allowed Range:** Positive integers (NovaMart benchmark: 970,838 line items across 585,691 header transactions).

---

### 14. Average Order Value (AOV)
- **Business Description:** Average net monetary revenue generated per distinct POS transaction receipt.
- **Mathematical Formula:**  
  $$\text{AOV} = \frac{\text{Net Revenue}}{\text{Total Transactions}} = \frac{\sum \text{net\_sales}}{\text{COUNT(DISTINCT } \text{transaction\_id})}$$
- **Source Table & Columns:** Derived from `novamart.fact_sales`.
- **SQL Implementation:**
  ```sql
  ROUND(SUM(net_sales) / NULLIF(COUNT(DISTINCT transaction_id), 0), 2) AS average_order_value_aov
  ```
- **Allowed Range:** Positive currency value (NovaMart benchmark: $\$79.56$).

---

## 3. Summary KPI Matrix

| Metric Name | Canonical Formula | SQL Aggregation | Expected Value | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Sales** | $\sum (\text{qty} \times \text{unit\_price})$ | `SUM(gross_sales)` | $\$49,269,500.50$ | **VERIFIED** |
| **Discounts (Signed)** | $\sum \text{discounts}$ | `SUM(discounts)` | $-\$2,674,327.23$ | **VERIFIED** |
| **Discount Amount** | $\sum |\text{discounts}|$ | `SUM(discount_amount)` | $\$2,674,327.23$ | **VERIFIED** |
| **Net Revenue** | $\sum \text{net\_sales}$ | `SUM(net_sales)` | $\$46,595,173.27$ | **VERIFIED** |
| **COGS** | $\sum (\text{qty} \times \text{unit\_cost})$ | `SUM(cogs)` | $\$20,811,116.93$ | **VERIFIED** |
| **Gross Profit** | $\text{Net Revenue} - \text{COGS}$ | `SUM(gross_profit)` | $\$25,784,056.34$ | **VERIFIED** |
| **Gross Margin %** | $\frac{\text{Gross Profit}}{\text{Net Revenue}} \times 100$ | `ROUND((SUM(gross_profit)/SUM(net_sales))*100, 2)` | $55.34\%$ | **VERIFIED** |
| **Discount Rate %** | $\frac{\text{Discount Amount}}{\text{Gross Sales}} \times 100$ | `ROUND((SUM(discount_amount)/SUM(gross_sales))*100, 2)` | $5.43\%$ | **VERIFIED** |
| **Refund Count** | $\sum \mathbb{I}(\text{Refund})$ | `SUM(CASE WHEN event_type='Refund' THEN 1 ELSE 0 END)` | $9,449$ rows | **VERIFIED** |
| **Refund Amount** | $\sum_{\text{Refund}} |\text{net\_sales}|$ | `SUM(CASE WHEN event_type='Refund' THEN ABS(net_sales) ELSE 0 END)` | $\$396,495.00$ | **VERIFIED** |
| **Refund Rate %** | $\frac{\text{Refund Count}}{\text{Line Items}} \times 100$ | `ROUND((Refund Lines / Line Items)*100, 2)` | $0.97\%$ | **VERIFIED** |
| **Units Moved** | $\sum \text{qty}$ | `SUM(qty)` | $1,173,116$ | **VERIFIED** |
| **Line Items** | $\text{COUNT(sales\_key)}$ | `COUNT(sales_key)` | $970,838$ | **VERIFIED** |
| **AOV** | $\frac{\text{Net Revenue}}{\text{Transactions}}$ | `ROUND(SUM(net_sales)/COUNT(DISTINCT txn_id), 2)` | $\$79.56$ | **VERIFIED** |
