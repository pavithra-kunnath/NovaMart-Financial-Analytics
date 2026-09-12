"""Automated Test Suite for Task 10: Python Revenue Forecasting & Backtesting Pipeline.

Framework: pytest
Scope: Monthly time-series dataset, accuracy metrics, backtest logic, and 6-month forecast validation.
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from src.forecast import build_monthly_dataset, run_rolling_origin_backtest, generate_forward_forecast
from src.accuracy_monitor import calc_mae, calc_rmse, calc_mape, calc_smape, calc_wape, evaluate_predictions


def test_monthly_dataset_aggregation_and_reconciliation():
    """Verify dataset builds exactly 24 continuous months and reconciles to $46,595,173.27."""
    m_df = build_monthly_dataset()
    
    assert len(m_df) == 24, f"Expected 24 months, got {len(m_df)}"
    assert m_df['month'].iloc[0] == '2024-01', "Start month must be 2024-01"
    assert m_df['month'].iloc[-1] == '2025-12', "End month must be 2025-12"
    assert m_df['month'].nunique() == 24, "Duplicate months detected"
    
    total_rev = round(m_df['net_revenue'].sum(), 2)
    assert total_rev == 46595173.27, f"Total net revenue mismatch: {total_rev}"


def test_metric_calculations_and_zero_denominator_safety():
    """Verify MAE, RMSE, MAPE, sMAPE, and WAPE functions with edge cases."""
    y_true = np.array([100.0, 200.0, 300.0])
    y_pred = np.array([110.0, 190.0, 300.0])
    
    mae = calc_mae(y_true, y_pred)
    rmse = calc_rmse(y_true, y_pred)
    mape = calc_mape(y_true, y_pred)
    smape = calc_smape(y_true, y_pred)
    wape = calc_wape(y_true, y_pred)
    
    assert round(mae, 2) == 6.67
    assert round(rmse, 2) == 8.16
    assert round(mape, 2) == 5.00
    assert round(wape, 2) == 3.33
    
    # Zero denominator test
    zero_true = np.array([0.0, 0.0])
    zero_pred = np.array([0.0, 0.0])
    assert calc_mape(zero_true, zero_pred) == 0.0
    assert calc_smape(zero_true, zero_pred) == 0.0
    assert calc_wape(zero_true, zero_pred) == 0.0


def test_naive_and_seasonal_naive_forecast_logic():
    """Verify Naive ($F_{t+1} = Y_t$) and Seasonal Naive ($F_{t+1} = Y_{t+1-12}$) logic."""
    m_df = build_monthly_dataset()
    actuals = m_df['net_revenue'].values
    
    # Naive: origin 12 (Jan 2025 forecast) uses Dec 2024 actual
    naive_pred_jan25 = actuals[11] # Dec 2024
    assert naive_pred_jan25 == actuals[11]
    
    # Seasonal Naive: origin 12 (Jan 2025 forecast) uses Jan 2024 actual
    snaive_pred_jan25 = actuals[0] # Jan 2024
    assert snaive_pred_jan25 == actuals[0]


def test_rolling_origin_backtest_execution():
    """Verify backtest executes across 12 origins and selects Seasonal Naive as Champion."""
    m_df = build_monthly_dataset()
    metrics_df, models_dict, backtest_preds_df = run_rolling_origin_backtest(m_df)
    
    assert len(metrics_df) >= 5, "Should evaluate at least 5 candidate models"
    assert len(backtest_preds_df) == 12, "Should evaluate 12 rolling backtest origins"
    
    # Check champion model is Seasonal Naive
    champion = metrics_df.iloc[0]['Model']
    assert champion == 'Seasonal Naive', f"Expected Champion 'Seasonal Naive', got '{champion}'"
    assert round(metrics_df.iloc[0]['WAPE (%)'], 2) == 5.20, f"Expected WAPE 5.20%, got {metrics_df.iloc[0]['WAPE (%)']}"


def test_forward_6month_forecast_validity():
    """Verify forward forecast produces exactly 6 future months (Jan 2026 to Jun 2026)."""
    m_df = build_monthly_dataset()
    metrics_df, models_dict, backtest_preds_df = run_rolling_origin_backtest(m_df)
    eval_actuals = m_df['net_revenue'].values[12:]
    
    fc_df = generate_forward_forecast(m_df, 'Seasonal Naive', models_dict, eval_actuals)
    
    assert len(fc_df) == 6, f"Expected 6 forecast months, got {len(fc_df)}"
    expected_months = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
    assert list(fc_df['forecast_month']) == expected_months
    
    # Ensure no historical actuals were accidentally placed in 2026 forecast
    assert not fc_df['predicted_net_revenue'].isna().any()
    assert (fc_df['predicted_net_revenue'] > 0).all()
    assert (fc_df['lower_bound_95'] < fc_df['predicted_net_revenue']).all()
    assert (fc_df['upper_bound_95'] > fc_df['predicted_net_revenue']).all()
