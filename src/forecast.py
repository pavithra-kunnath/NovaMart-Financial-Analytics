"""Production Monthly Revenue Forecasting & Backtesting Pipeline for NovaMart Retail.

Pipeline Entry Point: python -m src.forecast
Generates 6-month forward Net Revenue forecasts, rolling-origin backtest metrics,
and forecast visualization figures under reports/figures/forecast/.
"""

import sys
import os
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

from src.config import PROCESSED_SALES_CSV, BASE_DIR, REPORTS_DIR
from src.logging_config import setup_logger
from src.accuracy_monitor import evaluate_predictions

warnings.filterwarnings('ignore')
logger = setup_logger("forecast")

FORECAST_FIG_DIR = REPORTS_DIR / "figures" / "forecast"
FORECAST_FIG_DIR.mkdir(parents=True, exist_ok=True)


def build_monthly_dataset() -> pd.DataFrame:
    """Load processed dataset and build 24-month monthly Net Revenue time series."""
    logger.info(f"Loading processed dataset from {PROCESSED_SALES_CSV.name}...")
    df = pd.read_csv(PROCESSED_SALES_CSV, low_memory=False)
    
    df['month'] = df['transaction_date'].str.slice(0, 7)
    m_df = df.groupby('month').agg(net_revenue=('net_sales', 'sum')).reset_index().sort_values('month')
    
    # Validation assertions
    assert len(m_df) == 24, f"Expected exactly 24 monthly observations, got {len(m_df)}"
    assert m_df['month'].iloc[0] == '2024-01', f"Expected start month 2024-01, got {m_df['month'].iloc[0]}"
    assert m_df['month'].iloc[-1] == '2025-12', f"Expected end month 2025-12, got {m_df['month'].iloc[-1]}"
    
    total_rev = round(m_df['net_revenue'].sum(), 2)
    assert total_rev == 46595173.27, f"Net revenue reconciliation mismatch: expected 46595173.27, got {total_rev}"
    
    logger.info("Monthly dataset successfully built and reconciled ($46,595,173.27 across 24 months).")
    return m_df


def run_rolling_origin_backtest(m_df: pd.DataFrame) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """Execute rolling-origin 1-step-ahead backtesting across origins 12 through 23."""
    actuals = m_df['net_revenue'].values
    months = m_df['month'].values
    
    models = {
        'Naive': [],
        'Seasonal Naive': [],
        'ARIMA(1,1,0)': [],
        'ARIMA(0,1,1)': [],
        'ARIMA(1,1,1)': [],
        'SARIMAX(0,1,0)(1,0,0,12)': []
    }
    
    eval_actuals = actuals[12:] # 12 actuals for 2025 (Jan 2025 - Dec 2025)
    eval_months = months[12:]
    
    logger.info("Executing 1-step-ahead rolling-origin backtest across 12 origins (Jan 2025 to Dec 2025)...")
    
    for origin in range(12, 24):
        train = actuals[:origin]
        
        # 1. Naive
        models['Naive'].append(train[-1])
        
        # 2. Seasonal Naive (lag 12)
        models['Seasonal Naive'].append(actuals[origin - 12])
        
        # 3. ARIMA(1,1,0)
        try:
            res = ARIMA(train, order=(1, 1, 0)).fit()
            models['ARIMA(1,1,0)'].append(float(res.forecast(steps=1)[0]))
        except Exception as e:
            logger.warning(f"ARIMA(1,1,0) failed at origin {origin}: {e}")
            models['ARIMA(1,1,0)'].append(train[-1])
            
        # 4. ARIMA(0,1,1)
        try:
            res = ARIMA(train, order=(0, 1, 1)).fit()
            models['ARIMA(0,1,1)'].append(float(res.forecast(steps=1)[0]))
        except Exception as e:
            logger.warning(f"ARIMA(0,1,1) failed at origin {origin}: {e}")
            models['ARIMA(0,1,1)'].append(train[-1])
            
        # 5. ARIMA(1,1,1)
        try:
            res = ARIMA(train, order=(1, 1, 1)).fit()
            models['ARIMA(1,1,1)'].append(float(res.forecast(steps=1)[0]))
        except Exception as e:
            logger.warning(f"ARIMA(1,1,1) failed at origin {origin}: {e}")
            models['ARIMA(1,1,1)'].append(train[-1])
            
        # 6. SARIMAX(0,1,0)(1,0,0,12)
        try:
            res = SARIMAX(train, order=(0, 1, 0), seasonal_order=(1, 0, 0, 12)).fit(disp=False)
            models['SARIMAX(0,1,0)(1,0,0,12)'].append(float(res.forecast(steps=1)[0]))
        except Exception as e:
            logger.warning(f"SARIMAX failed at origin {origin}: {e}")
            models['SARIMAX(0,1,0)(1,0,0,12)'].append(train[-1])

    # Evaluate accuracy metrics
    metrics_list = []
    for name, preds in models.items():
        metrics = evaluate_predictions(eval_actuals, np.array(preds), model_name=name)
        metrics_list.append(metrics)
        
    metrics_df = pd.DataFrame(metrics_list).sort_values(by=['WAPE (%)', 'MAE'])
    
    # Build backtest predictions dataframe
    backtest_preds_df = pd.DataFrame({'month': eval_months, 'actual': eval_actuals})
    for name, preds in models.items():
        backtest_preds_df[name] = preds
        
    return metrics_df, models, backtest_preds_df


def generate_forward_forecast(m_df: pd.DataFrame, champion_name: str, models_dict: dict, eval_actuals: np.array) -> pd.DataFrame:
    """Generate 6-month forward forecast (Jan 2026 to Jun 2026) using full 24-month history."""
    actuals = m_df['net_revenue'].values
    future_months = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06']
    
    logger.info(f"Retraining selected champion model '{champion_name}' on all 24 historical observations...")
    
    if champion_name == 'Seasonal Naive':
        fc = actuals[12:18] # 2025-01 to 2025-06 actuals
        res_std = np.std(eval_actuals - np.array(models_dict['Seasonal Naive']))
        lower = fc - 1.96 * res_std
        upper = fc + 1.96 * res_std
    elif champion_name == 'Naive':
        fc = np.full(6, actuals[-1])
        res_std = np.std(eval_actuals - np.array(models_dict['Naive']))
        lower = fc - 1.96 * res_std
        upper = fc + 1.96 * res_std
    else:
        # ARIMA / SARIMAX
        if champion_name.startswith('ARIMA'):
            p, d, q = eval(champion_name.replace('ARIMA', ''))
            fit = ARIMA(actuals, order=(p, d, q)).fit()
        else:
            fit = SARIMAX(actuals, order=(0, 1, 0), seasonal_order=(1, 0, 0, 12)).fit(disp=False)
            
        pred_res = fit.get_forecast(steps=6)
        fc = pred_res.predicted_mean
        conf = pred_res.conf_int(alpha=0.05)
        lower = conf[:, 0]
        upper = conf[:, 1]
        
    fc_df = pd.DataFrame({
        'forecast_month': future_months,
        'predicted_net_revenue': fc,
        'lower_bound_95': lower,
        'upper_bound_95': upper
    })
    
    return fc_df


def save_forecast_visualizations(m_df: pd.DataFrame, backtest_preds_df: pd.DataFrame, metrics_df: pd.DataFrame, fc_df: pd.DataFrame, champion_name: str):
    """Generate and save the 4 required forecast visualization charts."""
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # 1. Historical monthly revenue + 6-month forecast
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(m_df['month'], m_df['net_revenue'] / 1e6, marker='o', label='Historical Actuals (2024-2025)', color='#1f77b4', linewidth=2)
    ax.plot(fc_df['forecast_month'], fc_df['predicted_net_revenue'] / 1e6, marker='s', label=f'6-Month Forecast ({champion_name})', color='#ff7f0e', linewidth=2, linestyle='--')
    ax.fill_between(fc_df['forecast_month'], fc_df['lower_bound_95'] / 1e6, fc_df['upper_bound_95'] / 1e6, color='#ff7f0e', alpha=0.2, label='95% Prediction Interval')
    
    all_months = list(m_df['month']) + list(fc_df['forecast_month'])
    ax.set_title('NovaMart Monthly Net Revenue: Historical Actuals & 6-Month Forward Forecast', fontsize=13, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Net Revenue ($ Millions)')
    plt.xticks(ticks=range(len(all_months)), labels=all_months, rotation=45, ha='right')
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(FORECAST_FIG_DIR / 'historical_and_6month_forecast.png', dpi=300)
    plt.close()
    
    # 2. Actual vs Backtest Predictions
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(backtest_preds_df['month'], backtest_preds_df['actual'] / 1e6, marker='o', label='Actual 2025 Revenue', color='black', linewidth=2.5)
    for col in ['Seasonal Naive', 'ARIMA(0,1,1)', 'Naive']:
        if col in backtest_preds_df.columns:
            ax.plot(backtest_preds_df['month'], backtest_preds_df[col] / 1e6, marker='x', label=f'Backtest: {col}', linestyle='--')
            
    ax.set_title('2025 Rolling-Origin Backtest Predictions vs Actuals', fontsize=13, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Net Revenue ($ Millions)')
    plt.xticks(rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.savefig(FORECAST_FIG_DIR / 'actual_vs_backtest_predictions.png', dpi=300)
    plt.close()
    
    # 3. Model Accuracy Comparison (WAPE %)
    fig, ax = plt.subplots(figsize=(10, 5))
    metrics_sorted = metrics_df.sort_values(by='WAPE (%)', ascending=True)
    bars = ax.barh(metrics_sorted['Model'], metrics_sorted['WAPE (%)'], color='#2ca02c', alpha=0.85)
    ax.set_title('Model Accuracy Comparison: WAPE (%) across 12 Backtest Origins', fontsize=13, fontweight='bold')
    ax.set_xlabel('WAPE (%) — Lower is Better')
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.5, bar.get_y() + bar.get_height()/2, f'{w:.2f}%', va='center')
    plt.tight_layout()
    plt.savefig(FORECAST_FIG_DIR / 'model_accuracy_comparison.png', dpi=300)
    plt.close()
    
    # 4. Forecast with Prediction Intervals
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(fc_df['forecast_month'], fc_df['predicted_net_revenue'] / 1e6, marker='s', color='#d62728', linewidth=2.5, label='Predicted Revenue')
    ax.fill_between(fc_df['forecast_month'], fc_df['lower_bound_95'] / 1e6, fc_df['upper_bound_95'] / 1e6, color='#d62728', alpha=0.25, label='95% Confidence Interval')
    ax.set_title(f'H1 2026 Net Revenue Forecast ({champion_name}) with 95% Confidence Bounds', fontsize=13, fontweight='bold')
    ax.set_xlabel('Forecast Month')
    ax.set_ylabel('Net Revenue ($ Millions)')
    for idx, row in fc_df.iterrows():
        val = row['predicted_net_revenue'] / 1e6
        ax.text(idx, val + 0.05, f'${val:.2f}M', ha='center', fontweight='bold')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(FORECAST_FIG_DIR / 'forecast_with_prediction_intervals.png', dpi=300)
    plt.close()
    
    logger.info(f"Forecast figures successfully saved in {FORECAST_FIG_DIR}.")


def main():
    """Execute complete production forecasting workflow."""
    logger.info("=== STARTING NOVAMART MONTHLY REVENUE FORECASTING PIPELINE ===")
    
    # 1. Build Dataset
    m_df = build_monthly_dataset()
    
    # 2. Backtest
    metrics_df, models_dict, backtest_preds_df = run_rolling_origin_backtest(m_df)
    
    # Print accuracy table
    print("\n" + "="*80)
    print("MODEL BACKTEST ACCURACY COMPARISON TABLE (12 ROLLING ORIGINS)")
    print("="*80)
    print(metrics_df.to_string(index=False))
    print("="*80 + "\n")
    
    # 3. Select Champion
    champion_name = metrics_df.iloc[0]['Model']
    logger.info(f"Champion Model Selected: '{champion_name}' (Lowest WAPE: {metrics_df.iloc[0]['WAPE (%)']:.2f}%).")
    
    # 4. Generate Forward Forecast
    eval_actuals = m_df['net_revenue'].values[12:]
    fc_df = generate_forward_forecast(m_df, champion_name, models_dict, eval_actuals)
    
    print("="*80)
    print(f"FORWARD 6-MONTH REVENUE FORECAST (H1 2026) — CHAMPION: {champion_name}")
    print("="*80)
    for _, r in fc_df.iterrows():
        print(f"  {r['forecast_month']} | Forecast: ${r['predicted_net_revenue']:11,.2f} | 95% CI: [${r['lower_bound_95']:11,.2f} .. ${r['upper_bound_95']:11,.2f}]")
    print(f"  TOTAL H1 2026 FORECAST: ${fc_df['predicted_net_revenue'].sum():,.2f}")
    print("="*80 + "\n")
    
    # 5. Visualizations
    save_forecast_visualizations(m_df, backtest_preds_df, metrics_df, fc_df, champion_name)
    
    logger.info("=== REVENUE FORECASTING PIPELINE COMPLETED SUCCESSFULLY ===")
    return {
        "champion": champion_name,
        "metrics": metrics_df.to_dict(orient="records"),
        "forecast": fc_df.to_dict(orient="records")
    }


if __name__ == "__main__":
    main()
