# NovaMart Forecast Accuracy & Production Monitoring Report

## 1. Monitoring Objective

The objective of the NovaMart Forecast Accuracy Monitoring Layer is to provide a standardized, reproducible, and automated production framework to evaluate, validate, and track forecast accuracy over time. This layer establishes operational guardrails, detects potential performance degradation (model drift), monitors prediction interval coverage, and ensures forecast input/output integrity when actual revenue data becomes available.

---

## 2. Champion Model

- **Model Name:** Seasonal Naive (Lag 12)
- **Model Rationale:** Selected in Task 10 after rigorous backtest benchmarking against baseline models (Naive Lag 1, Drift, Moving Averages) and statistical time-series models (SARIMAX, Holt-Winters Exponential Smoothing). Seasonal Naive achieved the lowest WAPE (5.20%) and MAE ($103,709.95) on the 2025 monthly validation backtest.
- **Model Equation:**
  $$\hat{Y}_{t+h} = Y_{t+h-12}$$
  where $Y_{t+h-12}$ represents net revenue from the corresponding month of the prior calendar year.
- **Status:** **LOCKED & IMMUTABLE**. The champion model and its Task 10 forecast values are strictly preserved.

---

## 3. Monitoring Grain

- **Temporal Grain:** Monthly (`YYYY-MM`)
- **Entity Grain:** Portfolio Total (NovaMart Enterprise Aggregate)
- **Primary Forecast Target:** `net_revenue` (Monthly Net Sales in USD, defined as Gross Sales minus Line Item Discounts minus Order Item Refunds)

---

## 4. Input Contract

To ensure production data quality, all monitoring records submitted for evaluation must adhere to the following contract specification:

### Data Schema
| Column Name | Data Type | Nullable | Description | Example |
| :--- | :--- | :---: | :--- | :--- |
| `forecast_month` | `string` / `datetime` | **No** | First day of target forecast month (`YYYY-MM-01` or `YYYY-MM`) | `2025-01-01` |
| `actual_net_revenue` | `float` | **No** | Verified historical actual net revenue in USD | `1262709.84` |
| `forecast_net_revenue` | `float` | **No** | Model point prediction for net revenue in USD | `1159850.56` |
| `lower_bound` | `float` | Yes | 95% prediction interval lower bound | `998240.21` |
| `upper_bound` | `float` | Yes | 95% prediction interval upper bound | `1321460.91` |
| `model_name` | `string` | Yes | Model identifier tag | `Seasonal Naive (Lag 12)` |
| `forecast_run_date` | `string` / `datetime` | Yes | Date forecast was generated | `2025-12-31` |

### Rules & Integrity Constraints
- **Monthly Grain:** Exactly one observation per calendar month.
- **Chronological Sequence:** Input series must be strictly ordered by `forecast_month`.
- **Uniqueness:** `forecast_month` values must be unique (no duplicate months permitted).
- **Non-Null:** `forecast_month`, `actual_net_revenue`, and `forecast_net_revenue` cannot contain nulls.
- **Non-Negative:** `forecast_net_revenue` must be non-negative ($\ge 0$).
- **Bound Consistency:** When bounds are provided, `lower_bound <= forecast_net_revenue <= upper_bound`.
- **Zero Actual Handling:** Zero actual values are handled safely without arbitrary non-zero substitution; percentage metrics (MAPE, APE) return `NaN` or are omitted for zero-actual months while aggregate WAPE handles zero totals gracefully.

---

## 5. Accuracy Metrics

The monitoring framework utilizes five standardized accuracy metrics:

1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^n |A_i - F_i|$$
2. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (A_i - F_i)^2}$$
3. **Mean Absolute Percentage Error (MAPE):**
   $$\text{MAPE} = \frac{1}{n} \sum_{i=1}^n \left| \frac{A_i - F_i}{A_i} \right| \times 100\%$$
4. **Symmetric Mean Absolute Percentage Error (sMAPE):**
   $$\text{sMAPE} = \frac{100\%}{n} \sum_{i=1}^n \frac{|A_i - F_i|}{(|A_i| + |F_i|) / 2}$$
5. **Weighted Absolute Percentage Error (WAPE):**
   $$\text{WAPE} = \frac{\sum_{i=1}^n |A_i - F_i|}{\sum_{i=1}^n A_i} \times 100\%$$

---

## 6. Historical Baseline

The official baseline is derived from the 12 one-step-ahead rolling-origin backtest predictions covering January–December 2025:

- **Backtest Period:** 2025-01 through 2025-12 (12 observations)
- **Baseline MAE:** **$103,709.95**
- **Baseline RMSE:** **$113,212.87**
- **Baseline MAPE:** **5.20%**
- **Baseline sMAPE:** **5.37%**
- **Baseline WAPE:** **5.20%**

---

## 7. Error Analysis

### Historical Backtest Error Metrics
- **Mean Error (Bias):** +$103,709.95
- **Median Absolute Error:** $107,990.91
- **Minimum Error:** +$33,706.94 (2025-04, APE: 1.92%)
- **Maximum Error:** +$182,576.64 (2025-05, APE: 9.27%)
- **Highest APE Month:** 2025-02 (8.93%) / 2025-05 (9.27%)

### Monthly Diagnostic Observations
- **Largest Under-Forecast Month:** May 2025 (Forecast: $1,787,974.84 vs Actual: $1,970,551.48, Error: +$182,576.64). May coincided with a major spring promotional push.
- **Smallest Forecast Error Month:** April 2025 (Forecast: $1,724,281.52 vs Actual: $1,757,988.46, Error: +$33,706.94).
- **December Peak Observation:** December 2025 recorded a forecast error of +$123,444.08 (APE: 4.26%), coinciding with the historical holiday shopping peak.

---

## 8. Bias Analysis

- **Definition:** Mean Error = $\frac{1}{n} \sum_{i=1}^n (Actual_i - Forecast_i)$
- **Baseline Result:** +$103,709.95 (Positive Mean Error)
- **Interpretation:**
  - Positive Mean Error indicates **systematic under-forecasting**.
  - Across all 12 backtest months, actual revenue consistently exceeded Seasonal Naive predictions.
  - This directional bias stems directly from NovaMart's ongoing Year-over-Year (YoY) net revenue growth from 2024 to 2025. Because Seasonal Naive carries forward the prior year's level without trend adjustments, it under-predicts during sustained growth periods.

---

## 9. Threshold Configuration

The monitoring system defines configurable operational guardrails for alert generation:

```python
DEFAULT_THRESHOLDS = {
    "wape_warning": 0.08,           # 8.0% WAPE triggers warning alert
    "wape_critical": 0.12,          # 12.0% WAPE triggers critical alert
    "ape_warning": 0.10,            # 10.0% APE for single month triggers warning
    "ape_critical": 0.15,           # 15.0% APE for single month triggers critical
    "bias_warning_pct": 0.05,       # Bias exceeding 5% of average revenue triggers warning
    "interval_coverage_min": 0.80   # Interval coverage falling below 80% triggers alert
}
```

> [!NOTE]
> Operational thresholds are management configuration guardrails for production alerting and business review. They do not alter or retrain the champion model.

---

## 10. Performance Degradation Methodology

The performance degradation diagnostic compares historical baseline performance against a new production evaluation window when actual revenue becomes available:

$$\Delta\text{WAPE} = \text{WAPE}_{\text{current}} - \text{WAPE}_{\text{baseline}}$$
$$\Delta\text{MAE} = \text{MAE}_{\text{current}} - \text{MAE}_{\text{baseline}}$$
$$\Delta\text{Bias} = \text{Bias}_{\text{current}} - \text{Bias}_{\text{baseline}}$$

Degradation Status Classification:
- **STABLE / IMPROVED:** $\Delta\text{WAPE} \le 0$ or within tolerance threshold.
- **DEGRADATION WARNING:** Current WAPE exceeds baseline by $> 2.0\%$ percentage points.
- **CRITICAL DEGRADATION:** Current WAPE exceeds baseline by $> 5.0\%$ percentage points.

---

## 11. Prediction Interval Monitoring

- **Methodology:** 95% empirical prediction interval calculated using historical backtest residual standard deviation from Task 10.
- **Coverage Check Formula:**
  $$\text{Coverage Rate} = \frac{1}{n} \sum_{i=1}^n \mathbb{I}(\text{Lower}_i \le \text{Actual}_i \le \text{Upper}_i)$$
- **2025 Backtest Coverage:** On the 2025 backtest dataset, 12 out of 12 actual values fell within their respective 95% prediction bounds (100% empirical coverage).
- **Distinction:** Point forecast accuracy evaluates expected prediction error, whereas interval coverage evaluates uncertainty calibration.

---

## 12. Validation Rules

Automated validation checks executed prior to monitoring calculation:
1. `check_chronological`: Ensures dates are strictly ascending.
2. `check_duplicates`: Rejects datasets with repeating months.
3. `check_numeric_non_null`: Rejects null or non-numeric entries in revenue/forecast columns.
4. `check_non_negative`: Ensures forecast values are non-negative.
5. `check_interval_bounds`: Validates `lower_bound <= forecast <= upper_bound`.

Failure to pass any validation check triggers an immediate, explicit error log without silent data alteration.

---

## 13. Current Monitoring Status

- **Status:** **PRODUCTION READY (BASELINE ESTABLISHED)**
- **Monitoring Dataset:** 12 monthly observations (2025-01 through 2025-12).
- **Artifact:** `reports/forecast_monitoring/forecast_accuracy_history.csv`
- **Reconciliation:** 100.00% reconciled against Task 10 results.

---

## 14. Limitations

1. **Sample Size:** Baseline is derived from 12 monthly backtest observations across 24 historical data months.
2. **Trend Unawareness:** Seasonal Naive assumes zero trend, resulting in positive forecast bias during growth periods.
3. **No 2026 Evaluation:** Production drift and performance degradation checks cannot be evaluated for 2026 until actual 2026 monthly sales occur.
4. **Causation Disclaimer:** Monitoring detects numerical error magnitude and directional bias; it does not infer causal external drivers (e.g. macroeconomics, stockouts, marketing campaigns).

---

## 15. Production Activation Requirements

To activate active monitoring when 2026 actual sales data becomes available:
1. Append monthly actual revenue records to `reports/forecast_monitoring/forecast_accuracy_history.csv` following the documented input contract.
2. Execute `python -m src.accuracy_monitor` to evaluate new monthly performance against the 2025 baseline.
3. Review generated figures in `reports/figures/forecast_monitoring/` and automated threshold alert logs.
