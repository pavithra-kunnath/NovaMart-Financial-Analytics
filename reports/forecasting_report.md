# Production Revenue Forecasting & Backtesting Report — NovaMart Retail

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 10 — Python Revenue Forecasting & Backtesting Pipeline  
**Target Variable:** Monthly Net Revenue (`net_revenue`)  
**Pipeline Script:** `python -m src.forecast`  
**Execution Timestamp:** 2026-09-09T11:14:40+05:30  
**Status:** Approved & Validated against Test Suite  

---

## 1. Objective

The objective of Task 10 is to construct a production-quality, reproducible time-series revenue forecasting pipeline for NovaMart Retail. The pipeline evaluates baseline and statistical models using chronological rolling-origin backtesting, selects a champion model based on empirical accuracy, and generates a 6-month forward Net Revenue forecast for H1 2026 (January 2026 through June 2026).

---

## 2. Forecast Target

The authoritative forecast target is **Monthly Net Revenue** at the overall company portfolio level.

- **Formula:** $\text{Net Revenue} = \text{Gross Sales} + \text{Discounts (signed)}$
- **Refund Accounting:** Refund records (`event_type = 'Refund'`, `qty = -1`) remain included as signed negative sales transactions per Data Contract specifications.

---

## 3. Historical Period

The historical dataset spans **24 calendar months**:
- **Start Month:** `2024-01` (January 2024)
- **End Month:** `2025-12` (December 2025)
- **Observations:** Exactly 24 monthly records.

---

## 4. Monthly Aggregation & Reconciliation

The processed transaction dataset (`data/processed/fact_sales_processed.csv`, 970,838 line items) was aggregated by calendar month (`transaction_date[:7]`).

- **Total Aggregated Revenue:** **$46,595,173.27**
- **Reconciliation Verdict:** **100.000% MATCH** with PostgreSQL DWH `novamart.fact_sales`.
- **Continuity Check:** 24 continuous months, 0 missing months, 0 duplicate months.

---

## 5. Backtesting Methodology (Rolling-Origin Evaluation)

To avoid data leakage and simulate real-world production forecasting, a **chronological 1-step-ahead rolling-origin backtesting** strategy was implemented across 12 historical origins:

- **Initial Training Window:** 12 months (`2024-01` through `2024-12`).
- **Evaluation Origins:** Origins $t = 12, 13, \dots, 23$.
- **Evaluation Period:** January 2025 through December 2025 (12 one-step forecasts).
- **No Data Leakage:** Models at origin $t$ are trained exclusively on observations available up to month $t$.

---

## 6. Naive Baseline Model

- **Definition:** Next month's forecast equals the most recent observed month's actual revenue:
  $$F_{t+1} = Y_t$$
- **Backtest Performance:** MAE = $\$390,025.42$, WAPE = **$19.57\%$**.
- **Assessment:** Fails to handle monthly retail seasonality.

---

## 7. Seasonal Naive Baseline Model

- **Definition:** Next month's forecast equals actual revenue from the same calendar month in the previous year (lag 12):
  $$F_{t+1} = Y_{t+1-12}$$
- **Backtest Performance:** MAE = **$103,709.95**, WAPE = **$5.20\%$**.
- **Assessment:** Outstanding performance. Captures recurring annual retail seasonality with high precision.

---

## 8. Statistical Candidate Models (ARIMA & SARIMAX)

Four statistical candidate models were evaluated on the 24-month history:
1. `ARIMA(1,1,0)`: First-differenced autoregressive candidate. (WAPE: $18.65\%$)
2. `ARIMA(0,1,1)`: First-differenced moving-average candidate. (WAPE: $18.26\%$)
3. `ARIMA(1,1,1)`: Combined non-seasonal candidate. (WAPE: $20.07\%$)
4. `SARIMAX(0,1,0)(1,0,0,12)`: Seasonal AR model. (WAPE: $39.95\%$; logged matrix decomposition warning at origin 19).

---

## 9. Accuracy Metrics Definitions

For every model, accuracy was computed over all 12 rolling evaluation points:
- **MAE (Mean Absolute Error):** $\frac{1}{N} \sum |y_i - \hat{y}_i|$
- **RMSE (Root Mean Squared Error):** $\sqrt{\frac{1}{N} \sum (y_i - \hat{y}_i)^2}$
- **MAPE (Mean Absolute Percentage Error):** $\frac{100}{N} \sum \left| \frac{y_i - \hat{y}_i}{y_i} \right|$
- **sMAPE (Symmetric MAPE):** $\frac{200}{N} \sum \frac{|y_i - \hat{y}_i|}{|y_i| + |\hat{y}_i|}$
- **WAPE (Weighted Absolute Percentage Error):** $\frac{\sum |y_i - \hat{y}_i|}{\sum y_i} \times 100$

Zero denominators are safely handled in `src/accuracy_monitor.py`.

---

## 10. Model Comparison Table

| Rank | Model Name | Forecasts | MAE ($) | RMSE ($) | MAPE (%) | sMAPE (%) | WAPE (%) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Seasonal Naive (Lag 12)** | **12** | **$103,709.95** | **$113,212.87** | **5.20%** | **5.37%** | **5.20%** | **CHAMPION** |
| **2** | `ARIMA(0,1,1)` | 12 | $\$363,926.10$ | $\$511,313.57$ | $19.01\%$ | $17.27\%$ | $18.26\%$ | Candidate |
| **3** | `ARIMA(1,1,0)` | 12 | $\$371,836.87$ | $\$521,200.20$ | $19.46\%$ | $17.63\%$ | $18.65\%$ | Candidate |
| **4** | `Naive` ($F_{t+1} = Y_t$) | 12 | $\$390,025.42$ | $\$494,313.53$ | $20.49\%$ | $18.95\%$ | $19.57\%$ | Baseline |
| **5** | `ARIMA(1,1,1)` | 12 | $\$400,069.49$ | $\$537,088.54$ | $21.00\%$ | $19.36\%$ | $20.07\%$ | Candidate |
| **6** | `SARIMAX(0,1,0)(1,0,0,12)`| 12 | $\$796,242.82$ | $\$986,037.61$ | $41.40\%$ | $57.42\%$ | $39.95\%$ | Unstable |

---

## 11. Champion Model Selection

**Seasonal Naive (Lag 12)** is selected as the Champion Model because it achieves the lowest WAPE (**5.20%**) and lowest MAE (**$103,709.95**), outperforming non-seasonal ARIMA candidates by over 13 percentage points.

---

## 12. Six-Month Forward Forecast (H1 2026)

Retraining **Seasonal Naive** on full 24-month historical observations (through December 2025) yields the H1 2026 forecast:

| Month | Predicted Net Revenue ($) | Lower Bound 95% ($) | Upper Bound 95% ($) |
| :--- | :--- | :--- | :--- |
| **2026-01** | $\$1,521,877.18$ | $\$1,432,888.01$ | $\$1,610,866.35$ |
| **2026-02** | $\$1,738,075.29$ | $\$1,649,086.12$ | $\$1,827,064.46$ |
| **2026-03** | $\$2,077,924.19$ | $\$1,988,935.02$ | $\$2,166,913.36$ |
| **2026-04** | $\$1,907,958.09$ | $\$1,818,968.92$ | $\$1,996,947.26$ |
| **2026-05** | $\$2,252,591.87$ | $\$2,163,602.70$ | $\$2,341,581.04$ |
| **2026-06** | $\$1,989,500.38$ | $\$1,900,511.21$ | $\$2,078,489.55$ |
| **TOTAL** | **$11,487,927.00** | **$10,953,992.00** | **$12,021,861.00** |

### 95% Prediction Interval Methodology QA
- **Calculation Formula**: $\text{Interval}_{95\%} = \hat{Y}_{t+h} \pm 1.96 \times S_e$
- **Historical Error Distribution**: Residual standard error $S_e = \$45,402.64$, computed from the 12 out-of-sample rolling-origin backtest errors across 2025 ($e_i = Y_{\text{actual, 2025}} - \hat{Y}_{\text{Seasonal Naive, 2025}}$), assuming a zero-mean normal error distribution $e_t \sim \mathcal{N}(0, S_e^2)$.
- **Statistical Appropriateness**: For Seasonal Naive (a heuristic lag model without parametric likelihood equations), constructing residual-based prediction bounds from out-of-sample backtest errors is the standard, statistically sound approach.
- **Data Boundary Verification**: Bounds are calculated strictly using 2024–2025 historical data. No 2026 data was used or referenced.
- **Point Forecast Integrity**: Point forecasts remain completely unchanged.

---

## 13. Important Limitations

> [!WARNING]
> - **Small Sample Size ($N=24$)**: Having only 24 monthly observations provides only 2 full annual cycles. This limits statistical power and seasonal parameter estimation for complex SARIMAX models.
> - **Confidence Bounds**: Prediction intervals reflect historical residual variance ($S_e = \$45,402.64$) and assume constant macroeconomic environment.

---

## 14. Reproducibility

The forecasting pipeline is 100% deterministic and reproducible by running:
```bash
python -m src.forecast
```

---

## 15. Validation Results

All figures are generated in `reports/figures/forecast/`:
1. `historical_and_6month_forecast.png`
2. `actual_vs_backtest_predictions.png`
3. `model_accuracy_comparison.png`
4. `forecast_with_prediction_intervals.png`

Automated test suite (`tests/test_forecasting.py`) passed 100%.
