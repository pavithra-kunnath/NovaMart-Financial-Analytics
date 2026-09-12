# SQL Financial Analysis & Executive Report — NovaMart Retail

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 8 — SQL Financial Analysis & KPI Validation  
**Database:** `novamart_db` (PostgreSQL DWH)  
**Schema:** `novamart`  
**Data Coverage:** `2024-01-01` to `2025-12-31` (24 Calendar Months)  
**Status:** Approved & Validated against Database Engine  

---

## 1. Executive Summary

This report delivers a comprehensive financial performance analysis for NovaMart Retail, derived directly from the production PostgreSQL Data Warehouse (`novamart_db`).

Over the 24-month period spanning 2024–2025, NovaMart achieved:
- **Total Net Revenue:** **$46,595,173.27**
- **Total Gross Profit:** **$25,784,056.34**
- **Overall Gross Margin:** **55.34%**
- **Total Units Moved:** **1,173,116 units** across **970,838 line items** and **585,691 distinct transactions**
- **Average Order Value (AOV):** **$79.56**
- **Total Promotional Discounts:** **$2,674,327.23** (Effective Discount Rate of **5.43%**)
- **Customer Refund Impact:** **$396,495.00** across **9,449 refund transactions** (Refund Rate of **0.97%**)

---

## 2. Portfolio Financial Overview

| Financial Metric | Portfolio Total | Percentage / Rate |
| :--- | :--- | :--- |
| **Gross Sales** | $\$49,269,500.50$ | $105.74\%$ of Net Revenue |
| **Discounts (Promotional)** | $\$2,674,327.23$ | $5.43\%$ Discount Rate |
| **Net Revenue** | $\$46,595,173.27$ | $100.00\%$ |
| **Cost of Goods Sold (COGS)** | $\$20,811,116.93$ | $44.66\%$ of Net Revenue |
| **Gross Profit** | $\$25,784,056.34$ | **55.34% Gross Margin** |
| **Refund Amount Impact** | $\$396,495.00$ | $0.85\%$ of Net Revenue |
| **Refund Line Items** | $9,449$ rows | **0.97% Refund Rate** |
| **Line Items Sold** | $970,838$ rows | — |
| **Transactions Count** | $585,691$ receipts | — |
| **Average Order Value (AOV)** | $\$79.56$ | — |

---

## 3. Monthly Financial Trend & Growth Analysis (2024 vs 2025)

NovaMart demonstrated strong revenue growth in 2025 across identical calendar months, driven by holiday promotions and seasonal peaks.

### 24-Month Detailed P&L Trend

| Year-Month | Gross Sales ($) | Discounts ($) | Net Revenue ($) | COGS ($) | Gross Profit ($) | Gross Margin (%) | Refund Count | Refund Amount ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2024-01** | $1,452,966.00$ | $67,054.41$ | $1,385,911.59$ | $613,464.60$ | $772,446.99$ | $55.74\%$ | $299$ | $11,817.00$ |
| **2024-02** | $1,759,743.50$ | $79,326.51$ | $1,680,416.99$ | $741,588.20$ | $938,828.79$ | $55.87\%$ | $271$ | $11,619.50$ |
| **2024-03** | $2,011,709.00$ | $90,645.94$ | $1,921,063.06$ | $850,222.19$ | $1,070,840.87$ | $55.74\%$ | $321$ | $13,535.00$ |
| **2024-04** | $1,962,715.00$ | $88,463.85$ | $1,874,251.15$ | $829,547.72$ | $1,044,703.43$ | $55.74\%$ | $349$ | $14,772.50$ |
| **2024-05** | $2,171,563.00$ | $101,547.77$ | $2,070,015.23$ | $915,212.82$ | $1,154,802.41$ | $55.79\%$ | $378$ | $14,804.50$ |
| **2024-06** | $1,995,274.50$ | $90,722.25$ | $1,904,552.25$ | $839,681.14$ | $1,064,871.11$ | $55.91\%$ | $376$ | $15,251.50$ |
| **2024-07** | $1,825,081.00$ | $86,125.86$ | $1,738,955.14$ | $769,144.00$ | $969,811.14$ | $55.77\%$ | $296$ | $12,372.00$ |
| **2024-08** | $2,154,512.50$ | $99,348.39$ | $2,055,164.11$ | $915,915.46$ | $1,139,248.65$ | $55.43\%$ | $366$ | $15,708.00$ |
| **2024-09** | $1,704,072.00$ | $77,431.69$ | $1,626,640.31$ | $720,989.87$ | $905,650.44$ | $55.68\%$ | $301$ | $13,861.50$ |
| **2024-10** | $1,798,829.50$ | $82,879.00$ | $1,715,950.50$ | $760,271.43$ | $955,679.07$ | $55.69\%$ | $303$ | $12,233.50$ |
| **2024-11** | $2,092,643.00$ | $138,979.96$ | $1,953,663.04$ | $885,849.46$ | $1,067,813.58$ | $54.66\%$ | $365$ | $14,656.50$ |
| **2024-12** | $3,050,661.00$ | $301,917.45$ | $2,748,743.55$ | $1,288,481.60$ | $1,460,261.95$ | $53.12\%$ | $896$ | $38,021.00$ |
| **2025-01** | $1,594,161.50$ | $72,284.32$ | $1,521,877.18$ | $674,372.63$ | $847,504.55$ | $55.69\%$ | $342$ | $14,047.00$ |
| **2025-02** | $1,818,146.00$ | $80,070.71$ | $1,738,075.29$ | $765,331.03$ | $972,744.26$ | $55.97\%$ | $345$ | $15,244.00$ |
| **2025-03** | $2,176,516.50$ | $98,592.31$ | $2,077,924.19$ | $919,694.72$ | $1,158,229.47$ | $55.74\%$ | $408$ | $17,677.50$ |
| **2025-04** | $1,997,989.50$ | $90,031.41$ | $1,907,958.09$ | $842,931.92$ | $1,065,026.17$ | $55.82\%$ | $322$ | $12,604.50$ |
| **2025-05** | $2,361,003.00$ | $108,411.13$ | $2,252,591.87$ | $995,009.25$ | $1,257,582.62$ | $55.83\%$ | $436$ | $18,395.50$ |
| **2025-06** | $2,081,866.50$ | $92,366.12$ | $1,989,500.38$ | $877,428.13$ | $1,112,072.25$ | $55.90\%$ | $355$ | $14,565.50$ |
| **2025-07** | $1,956,701.50$ | $92,900.33$ | $1,863,801.17$ | $824,365.83$ | $1,039,435.34$ | $55.77\%$ | $313$ | $12,918.00$ |
| **2025-08** | $2,260,978.50$ | $101,647.49$ | $2,159,331.01$ | $961,439.45$ | $1,197,891.56$ | $55.48\%$ | $412$ | $18,034.50$ |
| **2025-09** | $1,741,790.50$ | $81,081.39$ | $1,660,709.11$ | $735,086.67$ | $925,622.44$ | $55.74\%$ | $319$ | $13,702.00$ |
| **2025-10** | $1,880,125.00$ | $85,722.95$ | $1,794,402.05$ | $792,871.13$ | $1,001,530.92$ | $55.81\%$ | $331$ | $13,771.00$ |
| **2025-11** | $2,245,703.00$ | $152,585.47$ | $2,093,117.53$ | $949,758.84$ | $1,143,358.69$ | $54.62\%$ | $385$ | $16,232.50$ |
| **2025-12** | $3,174,749.00$ | $314,190.52$ | $2,860,558.48$ | $1,342,458.84$ | $1,518,099.64$ | $53.07\%$ | $960$ | $40,650.50$ |

### YoY Growth Observations
- **December Peak**: December is the highest revenue month in both years ($2.75M in Dec 2024 and $2.86M in Dec 2025), experiencing $+4.07\%$ YoY sales growth.
- **Consistent Profitability**: Gross Margin % remained extremely stable across all 24 months, hovering between $53.07\%$ (December holiday discount surge) and $55.97\%$ (February regular pricing).

---

## 4. Category Profitability Breakdown

NovaMart operates across 6 distinct merchandise categories. Apparel and Footwear generate over $69\%$ of total net revenue.

| Category | Line Items | Units Sold | Gross Sales ($) | Discounts ($) | Net Revenue ($) | Gross Profit ($) | Gross Margin (%) | Refund Lines | Refund Amount ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Apparel** | $362,144$ | $437,413$ | $\$18,923,601.00$ | $\$1,018,301.99$ | $\$17,905,299.01$ | $\$10,260,660.81$ | **57.31%** | $3,454$ | $\$148,396.00$ |
| **Footwear** | $181,903$ | $219,996$ | $\$15,139,159.00$ | $\$820,681.55$ | $\$14,318,477.45$ | $\$6,970,083.63$ | **48.68%** | $1,812$ | $\$124,108.00$ |
| **Electronics** | $117,737$ | $142,468$ | $\$5,442,443.00$ | $\$305,069.80$ | $\$5,137,373.20$ | $\$2,530,736.75$ | **49.26%** | $1,142$ | $\$44,454.00$ |
| **Accessories**| $106,102$ | $128,195$ | $\$4,497,959.00$ | $\$244,621.50$ | $\$4,253,337.50$ | $\$2,750,078.58$ | **64.66%** | $1,024$ | $\$35,944.00$ |
| **Home Goods** | $114,804$ | $138,471$ | $\$3,539,192.00$ | $\$192,504.50$ | $\$3,346,687.50$ | $\$2,157,744.86$ | **64.47%** | $1,146$ | $\$29,440.00$ |
| **Beauty** | $88,148$ | $106,573$ | $\$1,727,146.50$ | $\$93,147.89$ | $\$1,633,998.61$ | $\$1,114,751.71$ | **68.22%** | $871$ | $\$14,153.00$ |

### Strategic Category Insights
1. **Highest Revenue Producer**: **Apparel** ($\$17.91\text{M}$ Net Revenue, $57.31\%$ Gross Margin).
2. **Highest Margin Efficiency**: **Beauty** ($68.22\%$ Gross Margin) followed by **Accessories** ($64.66\%$) and **Home Goods** ($64.47\%$).
3. **Lowest Margin Efficiency**: **Footwear** ($48.68\%$ Gross Margin) due to higher unit acquisition costs.

---

## 5. Product-Level Performance Analysis

### Top 5 Revenue-Generating SKUs

| SKU | Item Name | Category | Units Sold | Net Revenue ($) | Gross Profit ($) | Gross Margin (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SQ-1049` | Wireless Earbuds | Electronics | $17,167$ | $\$1,279,302.30$ | $\$533,396.15$ | $41.69\%$ |
| `SQ-1048` | Wireless Earbuds | Electronics | $16,987$ | $\$1,266,512.20$ | $\$528,427.05$ | $41.72\%$ |
| `SQ-1035` | Running Shoes | Footwear | $14,602$ | $\$1,228,965.40$ | $\$579,176.40$ | $47.13\%$ |
| `SQ-1033` | Running Shoes | Footwear | $14,575$ | $\$1,227,492.45$ | $\$578,904.95$ | $47.16\%$ |
| `SQ-1034` | Running Shoes | Footwear | $14,429$ | $\$1,214,672.00$ | $\$572,581.50$ | $47.14\%$ |

---

## 6. Store Location Financial Performance

NovaMart operates 30 retail store locations.
- **Top Performing Location**: `STORE_09` (Store 09 - Chicago) with **$2,873,583.44** Net Revenue.
- **Lowest Performing Location**: `STORE_24` (Store 24 - Las Vegas) with **$853,737.80** Net Revenue.
- **Average Store Revenue**: **$1,553,172.44** per store over 24 months.

### Top 5 Store Locations

| Store ID | Location Name | City | Transactions | Net Revenue ($) | Gross Profit ($) | Gross Margin (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STORE_09` | Store 09 - Chicago | Chicago | $36,018$ | $\$2,873,583.44$ | $\$1,590,432.69$ | $55.35\%$ |
| `STORE_18` | Store 18 - Memphis | Memphis | $36,024$ | $\$2,873,208.39$ | $\$1,586,552.39$ | $55.22\%$ |
| `STORE_28` | Store 28 - Sacramento | Sacramento | $35,861$ | $\$2,868,244.32$ | $\$1,587,352.60$ | $55.34\%$ |
| `STORE_29` | Store 29 - Minneapolis | Minneapolis | $36,060$ | $\$2,863,350.63$ | $\$1,583,733.53$ | $55.31\%$ |
| `STORE_26` | Store 26 - Los Angeles | Los Angeles | $35,874$ | $\$2,852,094.23$ | $\$1,578,984.16$ | $55.36\%$ |

---

## 7. Customer Segment Performance

Source data differentiates between registered **Identified Customers** ($19,999$ unique accounts) and walk-in **Anonymous Guests** (`CUST_ANONYMOUS`).

| Customer Type | Distinct Accounts | Total Orders | Line Items | Net Revenue ($) | Gross Profit ($) | Gross Margin (%) | AOV ($) | Refund Lines |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Anonymous** | $1$ | $384,024$ | $634,393$ | $\$30,134,645.45$ | $\$16,672,704.75$ | $55.33\%$ | $\$78.47$ | $9,449$ |
| **Identified** | $19,999$ | $201,667$ | $336,445$ | $\$16,460,527.82$ | $\$9,111,351.59$ | $55.35\%$ | $\$81.62$ | $0$ |

### Customer Insights
1. Identified customers generate an Average Order Value of **$81.62**, which is **$3.15 higher** (+4.01%) than walk-in anonymous guests ($78.47).
2. Walk-in guest purchases represent **64.67% of total revenue**, highlighting an opportunity to convert guests into registered loyalty members.

---

## 8. Refund & Return Impact Analysis

| Event Type | Total Records | Total Qty | Gross Sales ($) | Signed Discounts ($) | Net Revenue ($) | COGS ($) | Gross Profit ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Payment** | $961,389$ | $1,182,565$ | $\$49,665,995.50$ | $-\$2,674,327.23$ | $\$46,991,668.27$ | $\$20,976,575.43$ | $\$26,015,092.84$ |
| **Refund** | $9,449$ | $-9,449$ | $-\$396,495.00$ | $\$0.00$ | $-\$396,495.00$ | $-\$165,458.50$ | $-\$231,036.50$ |
| **TOTAL** | **970,838** | **1,173,116** | **$49,269,500.50** | **-$2,674,327.23** | **$46,595,173.27** | **$20,811,116.93** | **$25,784,056.34** |

### Accounting Verification
- Refunds directly reduce Gross Sales by **-$396,495.00**, COGS by **-$165,458.50**, and Gross Profit by **-$231,036.50**.
- Summing `net_sales` directly across all rows properly accounts for refunds without double-counting.
