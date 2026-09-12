# Formal EDA Findings Layer — NovaMart Retail

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 9 — Python Exploratory Data Analysis & Financial Analysis  
**Data Source:** `data/processed/fact_sales_processed.csv`  
**Status:** Approved & Formally Documented  

---

## 1. Finding Record #1: Strong Q4 Holiday Seasonality (December Peak)

- **Finding:** NovaMart experiences massive revenue surges every December, generating over $2.74M in Dec 2024 and $2.86M in Dec 2025.
- **Evidence / Metric:** December Net Revenue increases by +40.70% MoM in 2024 (from $1.95M in Nov to $2.75M in Dec) and by +36.66% MoM in 2025 (from $2.09M in Nov to $2.86M in Dec).
- **Business Impact:** Q4 holiday sales contribute over 18.5% of total annual revenue and generate peak annual cash flows.
- **Possible Interpretation:** High consumer holiday shopping demand combined with promotional discount campaigns drives massive retail foot traffic.
- **Recommended Action:** Optimize inventory forecasting for Q4 starting in August to prevent stockouts of high-demand categories (Apparel & Footwear).

---

## 2. Finding Record #2: Revenue Concentration in Apparel & Footwear

- **Finding:** Apparel and Footwear categories drive 69.16% of total Net Revenue ($32.22M of $46.60M).
- **Evidence / Metric:** Apparel generates $17.91M (38.43% share) and Footwear generates $14.32M (30.73% share). Combined Gross Profit contribution is $17.23M (66.82% of portfolio total).
- **Business Impact:** Corporate performance is heavily dependent on fashion apparel and footwear demand.
- **Possible Interpretation:** Core brand positioning and merchandise assortment favor softlines over electronics or home goods.
- **Recommended Action:** Preserve prime floor space and marketing budget for Apparel while expanding cross-selling opportunities into high-margin Accessories.

---

## 3. Finding Record #3: High Margin Efficiency in Beauty & Accessories

- **Finding:** Beauty and Accessories deliver the highest Gross Margins in the portfolio (68.22% and 64.66%, respectively).
- **Evidence / Metric:** Beauty achieves a 68.22% Gross Margin ($1.11M profit on $1.63M net sales) despite representing only 3.51% of revenue. Accessories achieves 64.66% ($2.75M profit on $4.25M net sales).
- **Business Impact:** High-margin niche categories provide disproportionate profitability relative to inventory investment.
- **Possible Interpretation:** Lower cost-of-goods acquisition combined with premium retail markup on impulse beauty/accessory items.
- **Recommended Action:** Expand SKU assortment in Beauty and place impulse accessory displays near checkout registers across all 30 store locations.

---

## 4. Finding Record #4: Customer Loyalty AOV Premium vs Walk-In Revenue Share

- **Finding:** Registered Identified Customers generate a higher Average Order Value ($81.62 vs $78.47), but Anonymous Walk-In Guests generate 64.67% of total revenue.
- **Evidence / Metric:** Identified Customers spend +$3.15 (+4.01%) more per transaction receipt. However, 634,393 of 970,838 transaction lines ($30.13M of $46.60M) belong to guest purchases.
- **Business Impact:** NovaMart is missing customer retention, re-engagement, and lifetime value optimization on nearly 2/3 of its customer transactions.
- **Possible Interpretation:** POS checkout frictionless guest processing without incentive to register for a loyalty program.
- **Recommended Action:** Launch a POS digital loyalty enrollment initiative (e.g. 5% instant discount on first registered purchase) to convert anonymous walk-ins into identified repeat shoppers.

---

## 5. Finding Record #5: Geographic Store Performance Disparity

- **Finding:** Top store location Store 09 - Chicago generates 3.37x the revenue of lowest store Location Store 24 - Las Vegas.
- **Evidence / Metric:** Store 09 Chicago generates $2,873,583.44 Net Revenue (36,018 transactions), while Store 24 Las Vegas generates $853,737.80 (10,839 transactions).
- **Business Impact:** Significant operational resource imbalance across retail locations.
- **Possible Interpretation:** High urban population density and foot traffic in metropolitan Chicago vs lower store footprint / location traffic in Las Vegas.
- **Recommended Action:** Perform location-specific marketing audits and evaluate inventory allocation models tailored to local store volume capacity.

---

## 6. Finding Record #6: Low Overall Return Rate & Signed Refund Accounting Integrity

- **Finding:** Customer refund rate is exceptionally low at 0.97% of total line items ($396.495.00 total refund impact).
- **Evidence / Metric:** Exactly 9,449 of 970,838 lines are refunds (`event_type = 'Refund'`, `qty = -1`). Total refund impact is $396,495.00 (0.85% of Gross Sales).
- **Business Impact:** Minimal revenue erosion from customer returns; strong product satisfaction.
- **Possible Interpretation:** Accurate product sizing, quality control, and effective final sale policies.
- **Recommended Action:** Maintain current return handling procedures and continue monitoring refund spikes during January post-holiday return cycles ($14.0k in Jan 2025).

---

## 7. Finding Record #7: Revenue Leadership of Consumer Electronics & Footwear SKUs

- **Finding:** Individual SKUs in Electronics (`Wireless Earbuds` SQ-1049 & SQ-1048) and Footwear (`Running Shoes` SQ-1035 & SQ-1033) drive top individual product revenues exceeding $1.2M each.
- **Evidence / Metric:** Wireless Earbuds SQ-1049 generated $1,279,302.30 Net Revenue across 17,167 units sold. Running Shoes SQ-1035 generated $1,228,965.40 across 14,602 units sold.
- **Business Impact:** High unit velocity on key anchor SKUs anchors top-line growth.
- **Possible Interpretation:** Strong consumer tech and athletic footwear market demand for everyday lifestyle items.
- **Recommended Action:** Maintain high safety stock buffers for top 5 SKUs to prevent revenue loss from out-of-stock events.

---

## 8. Finding Record #8: Gross Margin Stability Across Time

- **Finding:** Portfolio Gross Margin % remains remarkably consistent throughout the 24 months, averaging 55.34%.
- **Evidence / Metric:** Monthly Gross Margin ranges from a tight low of 53.07% (December 2025 heavy holiday promotions) to a high of 55.97% (February 2025).
- **Business Impact:** Predictable unit economics and cost control across seasons.
- **Possible Interpretation:** Stable supplier wholesale pricing and disciplined promotional discount caps (max 5.43% average discount rate).
- **Recommended Action:** Maintain disciplined discount governance during promotional sales events to preserve 55%+ gross margin targets.
