"""
Unit and Integration Tests for Forecast Accuracy Monitoring System (Task 11).

Validates metrics calculations, zero-handling, input contracts, validation checks,
historical baseline reconciliation, performance degradation, and prediction interval coverage.
"""

import math
import pandas as pd
import pytest
from src.accuracy_monitor import (
    calc_mae,
    calc_rmse,
    calc_mape,
    calc_smape,
    calc_wape,
    calc_bias,
    calculate_mae,
    calculate_rmse,
    calculate_mape,
    calculate_smape,
    calculate_wape,
    calculate_bias,
    calculate_error_metrics,
    validate_monitoring_inputs,
    generate_backtest_monitoring_data,
    check_performance_degradation,
    check_interval_coverage,
    DEFAULT_THRESHOLDS
)


def test_mae_calculation():
    """Test Mean Absolute Error calculation."""
    actuals = pd.Series([100.0, 200.0, 300.0])
    forecasts = pd.Series([110.0, 190.0, 330.0])
    # Errors: |-10| + |10| + |-30| = 50 / 3 = 16.6666...
    mae = calculate_mae(actuals, forecasts)
    assert abs(mae - (50.0 / 3.0)) < 1e-5


def test_rmse_calculation():
    """Test Root Mean Squared Error calculation."""
    actuals = pd.Series([100.0, 200.0, 300.0])
    forecasts = pd.Series([110.0, 190.0, 330.0])
    # Squared errors: 100 + 100 + 900 = 1100 / 3 = 366.666... -> sqrt = 19.14854
    rmse = calculate_rmse(actuals, forecasts)
    expected = math.sqrt(1100.0 / 3.0)
    assert abs(rmse - expected) < 1e-5


def test_mape_zero_handling():
    """Test MAPE calculation with non-zero and zero actuals."""
    # Normal case
    actuals = pd.Series([100.0, 200.0])
    forecasts = pd.Series([110.0, 190.0])
    # |10/100| = 0.10, |-10/200| = 0.05 -> mean = 0.075 -> 7.5%
    mape = calculate_mape(actuals, forecasts)
    assert abs(mape - 7.5) < 1e-5

    # Zero actual handling
    actuals_zero = pd.Series([0.0, 200.0])
    mape_zero = calculate_mape(actuals_zero, forecasts)
    assert not math.isnan(mape_zero)  # Non-zero mask excludes 0.0, returning 5.0%


def test_smape_zero_handling():
    """Test sMAPE calculation when actual and forecast are zero or positive."""
    actuals = pd.Series([0.0, 200.0])
    forecasts = pd.Series([0.0, 190.0])
    smape = calculate_smape(actuals, forecasts)
    assert not math.isnan(smape)
    assert smape >= 0.0


def test_wape_zero_handling():
    """Test WAPE calculation with normal and zero totals."""
    actuals = pd.Series([100.0, 200.0])
    forecasts = pd.Series([110.0, 190.0])
    wape = calculate_wape(actuals, forecasts)
    assert abs(wape - (20.0 / 300.0 * 100.0)) < 1e-5

    # All zeros
    wape_zero = calculate_wape(pd.Series([0.0, 0.0]), pd.Series([0.0, 0.0]))
    assert wape_zero == 0.0


def test_error_calculation():
    """Test directional error calculation (Actual - Forecast)."""
    df = pd.DataFrame({
        "forecast_month": ["2025-01", "2025-02"],
        "actual_net_revenue": [1000.0, 2000.0],
        "forecast_net_revenue": [900.0, 2200.0]
    })
    res = calculate_error_metrics(df)
    assert list(res["error"]) == [100.0, -200.0]


def test_absolute_error():
    """Test absolute error calculation."""
    df = pd.DataFrame({
        "forecast_month": ["2025-01", "2025-02"],
        "actual_net_revenue": [1000.0, 2000.0],
        "forecast_net_revenue": [900.0, 2200.0]
    })
    res = calculate_error_metrics(df)
    assert list(res["absolute_error"]) == [100.0, 200.0]


def test_squared_error():
    """Test squared error calculation."""
    df = pd.DataFrame({
        "forecast_month": ["2025-01", "2025-02"],
        "actual_net_revenue": [1000.0, 2000.0],
        "forecast_net_revenue": [900.0, 2200.0]
    })
    res = calculate_error_metrics(df)
    assert list(res["squared_error"]) == [10000.0, 40000.0]


def test_bias_calculation():
    """Test mean forecast bias calculation (Actual - Forecast)."""
    actuals = pd.Series([1000.0, 2000.0, 3000.0])
    forecasts = pd.Series([900.0, 1800.0, 2700.0])
    bias = calculate_bias(actuals, forecasts)
    assert abs(bias - 200.0) < 1e-5


def test_monitoring_input_validation():
    """Test valid input contract passes validation."""
    df = pd.DataFrame({
        "forecast_month": ["2025-01", "2025-02"],
        "actual_net_revenue": [1000.0, 2000.0],
        "forecast_net_revenue": [900.0, 2200.0]
    })
    res = validate_monitoring_inputs(df)
    assert len(res) == 2


def test_duplicate_month_detection():
    """Test that duplicate forecast months fail validation loudly."""
    df = pd.DataFrame({
        "forecast_month": ["2025-01", "2025-01"],
        "actual_net_revenue": [1000.0, 2000.0],
        "forecast_net_revenue": [900.0, 2200.0]
    })
    with pytest.raises(ValueError, match="Duplicate forecast months"):
        validate_monitoring_inputs(df)


def test_chronological_ordering():
    """Test that non-chronological forecast months fail validation loudly."""
    df = pd.DataFrame({
        "forecast_month": ["2025-02", "2025-01"],
        "actual_net_revenue": [1000.0, 2000.0],
        "forecast_net_revenue": [900.0, 2200.0]
    })
    with pytest.raises(ValueError, match="not chronologically sorted"):
        validate_monitoring_inputs(df)


def test_negative_forecast_validation():
    """Test that negative forecasts fail validation loudly."""
    df = pd.DataFrame({
        "forecast_month": ["2025-01", "2025-02"],
        "actual_net_revenue": [1000.0, 2000.0],
        "forecast_net_revenue": [-900.0, 2200.0]
    })
    with pytest.raises(ValueError, match="Negative forecast values"):
        validate_monitoring_inputs(df)


def test_prediction_interval_validation():
    """Test lower_bound <= forecast <= upper_bound validation."""
    df_invalid = pd.DataFrame({
        "forecast_month": ["2025-01"],
        "actual_net_revenue": [1000.0],
        "forecast_net_revenue": [900.0],
        "lower_bound": [950.0],
        "upper_bound": [1200.0]
    })
    with pytest.raises(ValueError, match="exceeds"):
        validate_monitoring_inputs(df_invalid)


def test_historical_baseline_reconciliation():
    """Reconcile backtest monitoring dataset metrics against Task 10 champion benchmarks."""
    df_mon = generate_backtest_monitoring_data()
    
    # 1. Exactly 12 observations
    assert len(df_mon) == 12

    # 2. Check months 2025-01 to 2025-12
    expected_months = [f"2025-{m:02d}" for m in range(1, 13)]
    actual_months = list(df_mon["forecast_month"])
    assert actual_months == expected_months

    # 3. Check baseline metrics within numerical tolerance
    mae = calculate_mae(df_mon["actual_net_revenue"], df_mon["forecast_net_revenue"])
    rmse = calculate_rmse(df_mon["actual_net_revenue"], df_mon["forecast_net_revenue"])
    mape = calculate_mape(df_mon["actual_net_revenue"], df_mon["forecast_net_revenue"])
    smape = calculate_smape(df_mon["actual_net_revenue"], df_mon["forecast_net_revenue"])
    wape = calculate_wape(df_mon["actual_net_revenue"], df_mon["forecast_net_revenue"])

    assert abs(mae - 103709.95) < 1.0
    assert abs(rmse - 113212.87) < 1.0
    assert abs(mape - 5.20) < 0.1
    assert abs(smape - 5.37) < 0.1
    assert abs(wape - 5.20) < 0.1


def test_degradation_calculation():
    """Test performance degradation detection logic."""
    df_baseline = generate_backtest_monitoring_data()
    
    # Simulate a degraded current period
    df_degraded = df_baseline.copy()
    df_degraded["forecast_net_revenue"] = df_degraded["forecast_net_revenue"] * 0.70  # Larger errors

    deg_res = check_performance_degradation(df_baseline, df_degraded)
    assert "baseline_wape" in deg_res
    assert "current_wape" in deg_res
    assert deg_res["wape_change"] > 0
    assert deg_res["is_degraded"] is True


def test_interval_coverage_calculation():
    """Test prediction interval coverage calculation when bounds are available."""
    df = pd.DataFrame({
        "forecast_month": ["2025-01", "2025-02", "2025-03"],
        "actual_net_revenue": [1000.0, 2000.0, 3000.0],
        "forecast_net_revenue": [950.0, 1950.0, 2500.0],
        "lower_bound": [900.0, 1800.0, 2600.0],  # Month 3 actual (3000) exceeds upper bound (2900)
        "upper_bound": [1100.0, 2100.0, 2900.0]
    })
    cov_res = check_interval_coverage(df)
    assert cov_res["total_observations"] == 3
    assert cov_res["covered_observations"] == 2
    assert abs(cov_res["coverage_rate"] - (2.0 / 3.0)) < 1e-5
    assert cov_res["upper_bound_breaches"] == 1
    assert cov_res["lower_bound_breaches"] == 0
