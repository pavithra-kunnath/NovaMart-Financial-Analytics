# Model Comparison & Champion Selection Report — NovaMart Retail

**Project:** NovaMart Financial Analytics & Revenue Forecasting  
**Phase:** Task 10 — Python Revenue Forecasting & Backtesting Pipeline  
**Target Variable:** Monthly Net Revenue (`net_revenue`)  
**Evaluation Strategy:** 1-Step-Ahead Rolling-Origin Backtest across 12 Origins (Jan 2025 – Dec 2025)  
**Execution Timestamp:** 2026-09-09T11:14:40+05:30  
**Status:** Approved & Formally Evaluated  

---

## 1. Executive Summary & Champion Model Selection

To forecast NovaMart's monthly Net Revenue, six candidate time-series models were evaluated using a strict **1-step-ahead rolling-origin backtest** across 12 historical origins (evaluating predictions for every month of 2025).

### Selected Champion Model: **Seasonal Naive (Lag 12)**

- **WAPE Error:** **5.20%**
- **MAE Error:** **$103,709.95**
- **sMAPE Error:** **5.37%**
- **RMSE Error:** **$113,212.87**
- **Justification:** Seasonal Naive significantly outperformed all benchmark and statistical ARIMA models. NovaMart's retail revenue exhibits strong annual seasonality (e.g. December holiday peak, May/August secondary surges). Non-seasonal ARIMA models fail to capture annual seasonal shifts ($18.26\% - 20.07\%$ WAPE), while complex SARIMAX models suffer from instability and matrix decomposition errors on small sample sizes ($N=24$).

---

## 2. Model Accuracy Comparison Table

Models are ranked primarily by **WAPE (%)** and **MAE ($)** across all 12 rolling-origin evaluation forecasts:

| Rank | Model Name | Forecasts Evaluated | MAE ($) | RMSE ($) | MAPE (%) | sMAPE (%) | WAPE (%) | Selection Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Seasonal Naive (Lag 12)** | **12** | **$103,709.95** | **$113,212.87** | **5.20%** | **5.37%** | **5.20%** | **CHAMPION** |
| **2** | `ARIMA(0,1,1)` | 12 | $\$363,926.10$ | $\$511,313.57$ | $19.01\%$ | $17.27\%$ | $18.26\%$ | Candidate |
| **3** | `ARIMA(1,1,0)` | 12 | $\$371,836.87$ | $\$521,200.20$ | $19.46\%$ | $17.63\%$ | $18.65\%$ | Candidate |
| **4** | `Naive` ($F_{t+1} = Y_t$) | 12 | $\$390,025.42$ | $\$494,313.53$ | $20.49\%$ | $18.95\%$ | $19.57\%$ | Mandatory Baseline |
| **5** | `ARIMA(1,1,1)` | 12 | $\$400,069.49$ | $\$537,088.54$ | $21.00\%$ | $19.36\%$ | $20.07\%$ | Candidate |
| **6** | `SARIMAX(0,1,0)(1,0,0,12)`| 12 | $\$796,242.82$ | $\$986,037.61$ | $41.40\%$ | $57.42\%$ | $39.95\%$ | Unstable / Failed |

---

## 3. Model Performance & Evaluation Insights

### 1. Seasonal Naive ($F_{t+1} = Y_{t+1-12}$)
- **Why it Won:** Retail revenue in 2025 matched 2024 seasonal patterns remarkably well. The December 2025 revenue ($2.86M) matched December 2024 ($2.75M) with a small steady YoY growth multiplier. Seasonal Naive captured the annual shape with minimal lag error.
- **Accuracy:** WAPE of 5.20% represents high predictive reliability for financial budgeting.

### 2. Simple Naive ($F_{t+1} = Y_t$)
- **Why it Failed:** Simple Naive assumes next month equals current month. In retail with strong month-to-month volatility (e.g. Dec $2.75M to Jan $1.52M = -44.63% drop), Simple Naive produces huge errors ($19.57\%$ WAPE).

### 3. Non-Seasonal ARIMA Candidates (1,1,0), (0,1,1), (1,1,1)
- **Why They Failed:** Non-seasonal ARIMA models differenced the series once ($d=1$) and fitted local autoregressive/moving-average components. Without a seasonal component, they predicted near-flat continuation of recent trend, missing annual peaks entirely ($18.26\% - 20.07\%$ WAPE).

### 4. SARIMAX(0,1,0)(1,0,0,12)
- **Why it Failed:** Fitting a seasonal autoregressive component on only 24 monthly observations provides only 1 complete seasonal cycle for parameter estimation. At origin 19, statsmodels produced a linear algebra matrix decomposition error (`LU decomposition error`). Across origins, parameter estimates overfitted noise, yielding a high WAPE of 39.95%.

---

## 4. Forward 6-Month Revenue Forecast (Jan 2026 – Jun 2026)

Using the Champion **Seasonal Naive** model retrained on full 24-month historical observations (through December 2025):

| Forecast Month | Predicted Net Revenue ($) | Lower Bound 95% ($) | Upper Bound 95% ($) |
| :--- | :--- | :--- | :--- |
| **2026-01** | $\$1,521,877.18$ | $\$1,432,888.18$ | $\$1,610,866.18$ |
| **2026-02** | $\$1,738,075.29$ | $\$1,649,086.29$ | $\$1,827,064.29$ |
| **2026-03** | $\$2,077,924.19$ | $\$1,988,935.19$ | $\$2,166,913.19$ |
| **2026-04** | $\$1,907,958.09$ | $\$1,818,969.09$ | $\$1,996,947.09$ |
| **2026-05** | $\$2,252,591.87$ | $\$2,163,602.87$ | $\$2,341,580.87$ |
| **2026-06** | $\$1,989,500.38$ | $\$1,900,511.38$ | $\$2,078,489.38$ |
| **TOTAL H1 2026** | **$11,487,926.99** | **$10,953,992.99** | **$12,021,860.99** |

---

## 5. Conclusion & Recommendation

**Seasonal Naive** is formally designated as the Champion Forecasting Model for NovaMart monthly Net Revenue. Its 5.20% WAPE provides a robust, transparent, and accurate baseline for corporate financial planning.
