# NovaMart Forecast Accuracy Baseline (2025 Champion Model)

## 1. Executive Summary & Baseline Context

This document establishes the official production forecast accuracy baseline for NovaMart Retail's monthly Net Revenue forecasting engine. The baseline is built on **12 one-step-ahead rolling-origin backtest predictions** covering **January 2025 through December 2025** using the champion **Seasonal Naive (Lag 12)** model trained on 2024–2025 historical monthly transaction data.

### Champion Model Specification
- **Model Type:** Seasonal Naive (Lag 12)
- **Target Variable:** Monthly Net Revenue (`net_revenue`), aggregated portfolio-level.
- **Historical Fitting Window:** January 2024 – December 2025 (24 monthly observations).
- **Backtest Strategy:** 12 one-step-ahead rolling-origin evaluations (expanding window training).

---

## 2. Benchmark Metric Baseline Summary

The table below presents the verified baseline accuracy metrics established from the 2025 historical backtest. These metrics represent the target performance benchmark against which all future production forecast runs will be monitored.

| Metric | Baseline Value | Interpretation & Formula |
| :--- | :---: | :--- |
| **MAE** | **$103,709.95** | Mean Absolute Error. Average magnitude of forecast errors in currency units. |
| **RMSE** | **$113,212.87** | Root Mean Squared Error. Penalizes larger forecast deviations more heavily. |
| **MAPE** | **5.20%** | Mean Absolute Percentage Error. Average relative error percentage. |
| **sMAPE** | **5.37%** | Symmetric Mean Absolute Percentage Error. Bound between 0% and 200%. |
| **WAPE** | **5.20%** | Weighted Absolute Percentage Error. Total Absolute Error divided by Total Actuals. |
| **Mean Forecast Bias** | **+$103,709.95** | Mean Error ($Actual - Forecast$). Indicates systematic under-forecasting. |

---

## 3. Detailed Monthly Backtest Records

| Forecast Month | Actual Net Revenue ($) | Seasonal Naive Forecast ($) | Forecast Error ($) | Absolute Error ($) | Squared Error ($²) | Absolute Percentage Error (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2025-01** | $1,262,709.84 | $1,159,850.56 | +$102,859.28 | $102,859.28 | 10,580,031,482 | 8.15% |
| **2025-02** | $1,192,203.22 | $1,085,770.82 | +$106,432.40 | $106,432.40 | 11,327,855,793 | 8.93% |
| **2025-03** | $1,732,877.21 | $1,597,975.38 | +$134,901.83 | $134,901.83 | 18,198,503,733 | 7.78% |
| **2025-04** | $1,757,988.46 | $1,724,281.52 | +$33,706.94 | $33,706.94 | 1,136,157,808 | 1.92% |
| **2025-05** | $1,970,551.48 | $1,787,974.84 | +$182,576.64 | $182,576.64 | 33,334,229,487 | 9.27% |
| **2025-06** | $2,008,612.30 | $1,885,070.76 | +$123,541.54 | $123,541.54 | 15,262,512,118 | 6.15% |
| **2025-07** | $2,082,126.96 | $1,972,577.00 | +$109,549.96 | $109,549.96 | 12,001,193,738 | 5.26% |
| **2025-08** | $2,125,528.27 | $2,019,096.38 | +$106,431.89 | $106,431.89 | 11,327,747,218 | 5.01% |
| **2025-09** | $2,254,435.32 | $2,141,894.20 | +$112,541.12 | $112,541.12 | 12,665,503,696 | 4.99% |
| **2025-10** | $2,301,844.75 | $2,192,207.24 | +$109,637.51 | $109,637.51 | 12,020,383,109 | 4.76% |
| **2025-11** | $2,333,745.82 | $2,234,449.60 | +$99,296.22 | $99,296.22 | 9,859,739,314 | 4.25% |
| **2025-12** | $2,897,298.81 | $2,773,854.73 | +$123,444.08 | $123,444.08 | 15,238,440,892 | 4.26% |

---

## 4. Error Distribution & Directional Bias Analysis

### Directional Bias Profile
- **Mean Error (Bias):** +$103,709.95
- **Bias Direction:** **Systematic Under-Forecasting** (Positive Mean Error).
- **Positive Error Frequency:** **12 out of 12 months** (100% of backtest predictions understated actual revenue).
- **Analytical Context:** Because Seasonal Naive projects the prior year's same-month actual revenue without trend adjustment, and NovaMart experienced consistent month-over-month YoY revenue expansion throughout 2025, every monthly forecast fell below the realized actual revenue.

### Summary Statistics of Errors
- **Minimum Error (Smallest under-forecast):** +$33,706.94 (April 2025, APE: 1.92%)
- **Maximum Error (Largest under-forecast):** +$182,576.64 (May 2025, APE: 9.27%)
- **Median Absolute Error:** $107,990.91
- **Minimum APE:** 1.92% (2025-04)
- **Maximum APE:** 9.27% (2025-05)

---

## 5. Performance Limits & Monitoring Guidance

1. **Baseline Validity:** The baseline WAPE of **5.20%** and MAE of **$103,709.95** establish the acceptable noise threshold for Seasonal Naive. Performance degradation triggers will compare future production outcomes against these baseline figures.
2. **Evaluation Scope:** The baseline reflects 12 one-step-ahead monthly predictions. When 2026 actual revenue data becomes available, new actual-vs-forecast observations must be compared against this baseline using `check_performance_degradation`.
3. **No 2026 Data Usage:** The baseline strictly excludes 2026 data.
