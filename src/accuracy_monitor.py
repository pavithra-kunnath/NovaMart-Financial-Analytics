"""Production Forecast Accuracy Monitoring Layer for NovaMart Retail.

Pipeline Entry Point: python -m src.accuracy_monitor
Provides data validation, error calculation, bias diagnostics, operational threshold checks,
degradation monitoring, prediction interval coverage analysis, and chart generation.
"""

import sys
import os
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.config import PROCESSED_SALES_CSV, BASE_DIR, REPORTS_DIR
from src.logging_config import setup_logger

warnings.filterwarnings('ignore')
logger = setup_logger("accuracy_monitor")

MONITORING_DIR = REPORTS_DIR / "forecast_monitoring"
MONITORING_DIR.mkdir(parents=True, exist_ok=True)

MONITORING_FIG_DIR = REPORTS_DIR / "figures" / "forecast_monitoring"
MONITORING_FIG_DIR.mkdir(parents=True, exist_ok=True)

# Configurable Operational Monitoring Thresholds (Default Example Thresholds requiring Business Calibration)
DEFAULT_THRESHOLDS = {
    "wape_warning_pct": 10.0,
    "wape_critical_pct": 15.0,
    "ape_warning_pct": 10.0,
    "ape_critical_pct": 20.0,
    "bias_warning_abs": 50000.0
}


def calc_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Mean Absolute Error (MAE)."""
    return float(np.mean(np.abs(y_true - y_pred)))


def calc_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Root Mean Squared Error (RMSE)."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def calc_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Mean Absolute Percentage Error (MAPE) with zero-denominator safety."""
    y_true, y_pred = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    nonzero_mask = y_true != 0
    if not np.any(nonzero_mask):
        return 0.0
    return float(np.mean(np.abs((y_true[nonzero_mask] - y_pred[nonzero_mask]) / y_true[nonzero_mask])) * 100.0)


def calc_smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Symmetric Mean Absolute Percentage Error (sMAPE) with zero-denominator safety."""
    y_true, y_pred = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    denom = np.abs(y_true) + np.abs(y_pred)
    nonzero_mask = denom != 0
    if not np.any(nonzero_mask):
        return 0.0
    return float(np.mean(200.0 * np.abs(y_true[nonzero_mask] - y_pred[nonzero_mask]) / denom[nonzero_mask]))


def calc_wape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Weighted Absolute Percentage Error (WAPE)."""
    y_true, y_pred = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    sum_true = np.sum(np.abs(y_true))
    if sum_true == 0:
        return 0.0
    return float((np.sum(np.abs(y_true - y_pred)) / sum_true) * 100.0)


def calc_bias(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Mean Forecast Bias = Mean(Actual - Forecast).
    Positive = systematic under-forecasting; Negative = systematic over-forecasting.
    """
    return float(np.mean(np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float)))


# Function Aliases for external compatibility and unit test compliance
calculate_mae = calc_mae
calculate_rmse = calc_rmse
calculate_mape = calc_mape
calculate_smape = calc_smape
calculate_wape = calc_wape
calculate_bias = calc_bias


def calculate_error_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate error, absolute error, squared error, and APE columns on a DataFrame."""
    res_df = df.copy()
    res_df['error'] = res_df['actual_net_revenue'] - res_df['forecast_net_revenue']
    res_df['absolute_error'] = np.abs(res_df['error'])
    res_df['squared_error'] = res_df['error'] ** 2
    res_df['ape'] = (res_df['absolute_error'] / res_df['actual_net_revenue']) * 100.0
    return res_df


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, model_name: str = "Model") -> dict:
    """Calculate comprehensive accuracy & bias metrics for a set of predictions."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    
    return {
        "Model": model_name,
        "Forecasts": len(y_true),
        "MAE": calc_mae(y_true, y_pred),
        "RMSE": calc_rmse(y_true, y_pred),
        "MAPE (%)": calc_mape(y_true, y_pred),
        "sMAPE (%)": calc_smape(y_true, y_pred),
        "WAPE (%)": calc_wape(y_true, y_pred),
        "Bias": calc_bias(y_true, y_pred)
    }


def validate_monitoring_inputs(df: pd.DataFrame, require_actuals: bool = True) -> pd.DataFrame:
    """Rigorous input contract validation for forecast monitoring dataframes.
    Fails loudly with descriptive error messages if contracts are violated.
    """
    required_cols = ['forecast_month', 'forecast_net_revenue']
    if require_actuals:
        required_cols.append('actual_net_revenue')
        
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Input Validation Error: Missing required column '{col}'.")
            
    if df.empty:
        raise ValueError("Input Validation Error: Provided dataframe is empty.")
        
    # Check month format (YYYY-MM or YYYY-MM-DD)
    if not df['forecast_month'].str.match(r'^\d{4}-\d{2}(-\d{2})?$').all():
        raise ValueError("Input Validation Error: 'forecast_month' must be in 'YYYY-MM' or 'YYYY-MM-DD' format.")
        
    # Check duplicate months
    if df['forecast_month'].duplicated().any():
        dupes = list(df[df['forecast_month'].duplicated()]['forecast_month'])
        raise ValueError(f"Input Validation Error: Duplicate forecast months detected: {dupes}.")
        
    # Check chronological ordering
    if not df['forecast_month'].is_monotonic_increasing:
        raise ValueError("Input Validation Error: 'forecast_month' sequence is not chronologically sorted.")
        
    # Check non-null and numeric for numeric columns
    numeric_cols = [c for c in required_cols if c != 'forecast_month']
    for col in numeric_cols:
        if df[col].isnull().any():
            raise ValueError(f"Input Validation Error: Column '{col}' contains NULL values.")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Input Validation Error: Column '{col}' must be numeric.")
            
    # Check non-negative forecasts
    if (df['forecast_net_revenue'] < 0).any():
        raise ValueError("Input Validation Error: Negative forecast values detected in 'forecast_net_revenue'.")
        
    # Check bounds if present
    if 'lower_bound' in df.columns and 'upper_bound' in df.columns:
        if (df['lower_bound'] > df['forecast_net_revenue']).any():
            raise ValueError("Input Validation Error: 'lower_bound' exceeds 'forecast_net_revenue'.")
        if (df['forecast_net_revenue'] > df['upper_bound']).any():
            raise ValueError("Input Validation Error: 'forecast_net_revenue' exceeds 'upper_bound'.")
            
    logger.info(f"Input contract validation passed successfully for {len(df)} records.")
    return df


def generate_historical_backtest_monitoring_dataset() -> pd.DataFrame:
    """Build the 12-month Seasonal Naive 2025 backtest monitoring dataset."""
    from src.forecast import build_monthly_dataset, run_rolling_origin_backtest
    
    m_df = build_monthly_dataset()
    metrics_df, models_dict, backtest_preds_df = run_rolling_origin_backtest(m_df)
    
    snaive_preds = models_dict['Seasonal Naive']
    eval_actuals = m_df['net_revenue'].values[12:]
    eval_months = m_df['month'].values[12:]
    
    mon_df = pd.DataFrame({
        'forecast_month': eval_months,
        'actual_net_revenue': eval_actuals,
        'forecast_net_revenue': snaive_preds
    })
    
    # Calculate detailed error columns
    mon_df['error'] = mon_df['actual_net_revenue'] - mon_df['forecast_net_revenue']
    mon_df['abs_error'] = np.abs(mon_df['error'])
    mon_df['squared_error'] = mon_df['error'] ** 2
    mon_df['ape'] = (mon_df['abs_error'] / mon_df['actual_net_revenue']) * 100
    
    # Save CSV artifact
    csv_path = MONITORING_DIR / "forecast_accuracy_history.csv"
    mon_df.to_csv(csv_path, index=False)
    logger.info(f"Saved historical monitoring artifact to {csv_path.name}.")
    
    return mon_df


generate_backtest_monitoring_data = generate_historical_backtest_monitoring_dataset


def check_performance_degradation(baseline_input, current_input) -> dict:
    """Compare baseline accuracy metrics against a current monitoring period to detect drift.
    Accepts either DataFrames (containing actual_net_revenue and forecast_net_revenue) or metric dicts.
    """
    if isinstance(baseline_input, pd.DataFrame):
        baseline_metrics = evaluate_predictions(baseline_input['actual_net_revenue'].values, baseline_input['forecast_net_revenue'].values)
    else:
        baseline_metrics = baseline_input

    if isinstance(current_input, pd.DataFrame):
        current_metrics = evaluate_predictions(current_input['actual_net_revenue'].values, current_input['forecast_net_revenue'].values)
    else:
        current_metrics = current_input

    wape_diff = current_metrics.get("WAPE (%)", 0) - baseline_metrics.get("WAPE (%)", 0)
    mae_diff = current_metrics.get("MAE", 0) - baseline_metrics.get("MAE", 0)
    bias_diff = current_metrics.get("Bias", 0) - baseline_metrics.get("Bias", 0)
    
    degradation_flag = wape_diff > 3.0  # Alert if WAPE deteriorates by > 3 percentage points
    
    return {
        "baseline_wape": baseline_metrics.get("WAPE (%)", 0),
        "current_wape": current_metrics.get("WAPE (%)", 0),
        "wape_change": wape_diff,
        "baseline_mae": baseline_metrics.get("MAE", 0),
        "current_mae": current_metrics.get("MAE", 0),
        "mae_change": mae_diff,
        "bias_change": bias_diff,
        "degradation_flag": degradation_flag,
        "is_degraded": degradation_flag,
        "status": "ALERT: Performance Degradation Detected" if degradation_flag else "STABLE: Performance Within Normal Drift Parameters"
    }


def check_interval_coverage(df: pd.DataFrame) -> dict:
    """Calculate prediction interval coverage rate and bound breach counts when bounds exist."""
    if 'lower_bound' not in df.columns or 'upper_bound' not in df.columns or 'actual_net_revenue' not in df.columns:
        return {"status": "SKIPPED: Bounds or actuals not present in input dataset."}
        
    inside = (df['actual_net_revenue'] >= df['lower_bound']) & (df['actual_net_revenue'] <= df['upper_bound'])
    coverage_rate = float(inside.mean() * 100.0)
    lower_breaches = int((df['actual_net_revenue'] < df['lower_bound']).sum())
    upper_breaches = int((df['actual_net_revenue'] > df['upper_bound']).sum())
    
    return {
        "evaluated_records": len(df),
        "total_observations": len(df),
        "records_inside_interval": int(inside.sum()),
        "covered_observations": int(inside.sum()),
        "coverage_rate_pct": coverage_rate,
        "coverage_rate": float(inside.mean()),
        "lower_bound_breaches": lower_breaches,
        "upper_bound_breaches": upper_breaches
    }


def save_monitoring_visualizations(mon_df: pd.DataFrame):
    """Generate and save the 5 required monitoring figures under reports/figures/forecast_monitoring/."""
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # 1. Actual vs Forecast by Month
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(mon_df['forecast_month'], mon_df['actual_net_revenue'] / 1e6, marker='o', label='Actual 2025 Revenue', color='black', linewidth=2)
    ax.plot(mon_df['forecast_month'], mon_df['forecast_net_revenue'] / 1e6, marker='s', label='Seasonal Naive Backtest', color='#ff7f0e', linestyle='--', linewidth=2)
    ax.set_title('2025 Actual vs Seasonal Naive Forecast Net Revenue ($ Millions)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Net Revenue ($ Millions)')
    plt.xticks(rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.savefig(MONITORING_FIG_DIR / 'actual_vs_forecast_monthly.png', dpi=300)
    plt.close()
    
    # 2. Forecast Error by Month (Actual - Forecast)
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#2ca02c' if err >= 0 else '#d62728' for err in mon_df['error']]
    ax.bar(mon_df['forecast_month'], mon_df['error'] / 1e3, color=colors, alpha=0.85)
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_title('Forecast Error by Month (Actual - Forecast, $ Thousands)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Error ($ Thousands)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(MONITORING_FIG_DIR / 'forecast_error_monthly.png', dpi=300)
    plt.close()
    
    # 3. Absolute Percentage Error (APE) by Month
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(mon_df['forecast_month'], mon_df['ape'], marker='d', color='#9467bd', linewidth=2)
    ax.axhline(10.0, color='#d62728', linestyle='--', label='10% APE Warning Threshold')
    ax.set_title('Absolute Percentage Error (APE %) by Month', fontsize=12, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('APE (%)')
    ax.set_ylim(0, 15)
    plt.xticks(rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.savefig(MONITORING_FIG_DIR / 'absolute_percentage_error_monthly.png', dpi=300)
    plt.close()
    
    # 4. Error Distribution Histogram & KDE
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(mon_df['error'] / 1e3, bins=6, color='#1f77b4', edgecolor='black', alpha=0.7)
    ax.axvline(mon_df['error'].mean() / 1e3, color='#d62728', linestyle='--', linewidth=2, label=f"Mean Bias: +${mon_df['error'].mean()/1e3:.1f}k")
    ax.set_title('Forecast Error Distribution ($ Thousands)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Error ($ Thousands)')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.tight_layout()
    plt.savefig(MONITORING_FIG_DIR / 'error_distribution.png', dpi=300)
    plt.close()
    
    # 5. Actual vs Forecast Scatter Plot
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(mon_df['forecast_net_revenue'] / 1e6, mon_df['actual_net_revenue'] / 1e6, color='#1f77b4', s=60, alpha=0.9, label='2025 Monthly Points')
    
    # 45-degree reference line
    min_val = min(mon_df['forecast_net_revenue'].min(), mon_df['actual_net_revenue'].min()) / 1e6
    max_val = max(mon_df['forecast_net_revenue'].max(), mon_df['actual_net_revenue'].max()) / 1e6
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect 1:1 Accuracy')
    
    ax.set_title('Actual vs Forecast Net Revenue Scatter Plot', fontsize=12, fontweight='bold')
    ax.set_xlabel('Forecast Net Revenue ($ Millions)')
    ax.set_ylabel('Actual Net Revenue ($ Millions)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(MONITORING_FIG_DIR / 'actual_vs_forecast_scatter.png', dpi=300)
    plt.close()
    
    logger.info(f"Saved 5 monitoring visualization figures to {MONITORING_FIG_DIR}.")


def main():
    """Execute complete forecast accuracy monitoring workflow."""
    logger.info("=== STARTING FORECAST ACCURACY MONITORING WORKFLOW ===")
    
    # 1. Generate & Validate Dataset
    mon_df = generate_historical_backtest_monitoring_dataset()
    validate_monitoring_inputs(mon_df, require_actuals=True)
    
    # 2. Compute Summary Metrics & Error Analysis
    eval_metrics = evaluate_predictions(mon_df['actual_net_revenue'].values, mon_df['forecast_net_revenue'].values, model_name="Seasonal Naive (2025 Backtest)")
    
    print("\n" + "="*80)
    print("HISTORICAL CHAMPION FORECAST ACCURACY BASELINE (12 MONTHS 2025)")
    print("="*80)
    for k, v in eval_metrics.items():
        if isinstance(v, float):
            print(f"  {k:12s}: {v:12,.2f}")
        else:
            print(f"  {k:12s}: {v}")
            
    min_err = mon_df['error'].min()
    max_err = mon_df['error'].max()
    med_abs_err = mon_df['abs_error'].median()
    print(f"  Min Error   : ${min_err:12,.2f}")
    print(f"  Max Error   : ${max_err:12,.2f}")
    print(f"  Median Abs E: ${med_abs_err:12,.2f}")
    print("="*80 + "\n")
    
    # 3. Save Visualizations
    save_monitoring_visualizations(mon_df)
    
    logger.info("=== FORECAST ACCURACY MONITORING WORKFLOW COMPLETED SUCCESSFULLY ===")
    return eval_metrics


if __name__ == "__main__":
    main()
