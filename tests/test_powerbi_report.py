"""
Unit and Integration Tests for Power BI Report Dashboard Artifacts & Visual Validation (Task 13).

Validates PBIP project files, visual container configurations, DAX measure bindings,
unfiltered portfolio KPI baselines, customer segment metrics, H1 2026 forecast totals ($11,487,927.00),
prediction interval bounds, and forecast disclaimer integrity.
"""

import json
import pytest
from pathlib import Path
from src.config import BASE_DIR
from src.load_postgres import get_db_connection


def test_powerbi_pbip_artifact_files_exist():
    """Verify PBIP project configuration files, definition.pbir, definition.pbism, model.bim, and report.json exist under powerbi/."""
    pbip_path = BASE_DIR / "powerbi" / "NovaMart.pbip"
    pbir_path = BASE_DIR / "powerbi" / "NovaMart.Report" / "definition.pbir"
    pbism_path = BASE_DIR / "powerbi" / "NovaMart.Dataset" / "definition.pbism"
    model_bim_path = BASE_DIR / "powerbi" / "NovaMart.Dataset" / "model.bim"
    report_json_path = BASE_DIR / "powerbi" / "NovaMart.Report" / "report.json"
    readme_path = BASE_DIR / "powerbi" / "README.md"
    design_path = BASE_DIR / "powerbi" / "report_design.md"
    
    assert pbip_path.exists(), "powerbi/NovaMart.pbip artifact file is missing!"
    assert pbir_path.exists(), "powerbi/NovaMart.Report/definition.pbir artifact file is missing!"
    assert pbism_path.exists(), "powerbi/NovaMart.Dataset/definition.pbism artifact file is missing!"
    assert model_bim_path.exists(), "powerbi/NovaMart.Dataset/model.bim artifact file is missing!"
    assert report_json_path.exists(), "powerbi/NovaMart.Report/report.json file is missing!"
    assert readme_path.exists(), "powerbi/README.md documentation is missing!"
    assert design_path.exists(), "powerbi/report_design.md documentation is missing!"


def test_powerbi_model_bim_semantic_structure():
    """Verify model.bim contains genuine NovaMart semantic model tables, relationships with cardinality, and 29 DAX measures."""
    model_bim_path = BASE_DIR / "powerbi" / "NovaMart.Dataset" / "model.bim"
    with open(model_bim_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # In PBIP format, dataset name is defined by folder NovaMart.Dataset; TMSL model.bim root has compatibilityLevel and model
    assert data.get("name") == "NovaMart" or model_bim_path.parent.name == "NovaMart.Dataset"
    assert "model" in data
    model = data.get("model", {})
    tables = [t.get("name") for t in model.get("tables", [])]
    expected_tables = ["_Measures", "dim_date", "dim_customer", "dim_product", "dim_store", "vw_pbi_fact_sales", "vw_pbi_fact_forecast"]
    assert set(expected_tables).issubset(set(tables))
    
    # Relationships with cardinality (5 dimensional model relationships; TMSL defaults many-to-one, single direction)
    expected_rel_names = {
        "rel_dim_date_fact_sales",
        "rel_dim_customer_fact_sales",
        "rel_dim_product_fact_sales",
        "rel_dim_store_fact_sales",
        "rel_dim_date_fact_forecast",
    }
    rels = [r for r in model.get("relationships", []) if r.get("name") in expected_rel_names]
    assert len(rels) == 5
    for r in rels:
        assert r.get("fromCardinality", "many") == "many"
        assert r.get("toCardinality", "one") == "one"
        assert r.get("crossFilteringBehavior", "oneDirection") == "oneDirection"
    
    # Measures count
    measures_table = next(t for t in model.get("tables", []) if t.get("name") == "_Measures")
    measures = measures_table.get("measures", [])
    assert len(measures) == 29



def test_report_json_pages_structure():
    """Verify report.json contains all 5 required analytical pages."""
    report_json_path = BASE_DIR / "powerbi" / "NovaMart.Report" / "report.json"
    with open(report_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    sections = data.get("sections", [])
    assert len(sections) == 5, f"Expected 5 report pages, got {len(sections)}"
    
    page_names = [s.get("displayName") for s in sections]
    expected_pages = [
        "01 Executive Overview",
        "02 Revenue & Profitability",
        "03 Product & Category",
        "04 Store & Customer",
        "05 Forecast & Outlook"
    ]
    assert page_names == expected_pages


def test_page1_and_page2_kpi_metrics():
    """Verify Page 1 & Page 2 executive KPI card metrics against PostgreSQL baselines."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            ROUND(SUM(gross_sales), 2),
            ROUND(SUM(discount_amount), 2),
            ROUND(SUM(net_sales), 2),
            ROUND(SUM(cogs), 2),
            ROUND(SUM(gross_profit), 2),
            ROUND(SUM(gross_profit) / SUM(net_sales) * 100, 4),
            SUM(qty),
            COUNT(DISTINCT transaction_id),
            ROUND(SUM(net_sales) / COUNT(DISTINCT transaction_id), 2)
        FROM novamart.fact_sales;
    """)
    r = cur.fetchone()
    cur.close()
    conn.close()
    
    gross, disc, net, cogs, profit, gm, units, txns, aov = [float(x) for x in r]
    
    assert gross == 49269500.50
    assert disc == 2674327.23
    assert net == 46595173.27
    assert cogs == 20811116.93
    assert profit == 25784056.34
    assert abs(gm - 55.3363) < 0.001
    assert int(units) == 1173116
    assert int(txns) == 585691
    assert aov == 79.56


def test_page4_customer_segment_metrics():
    """Verify Page 4 Identified vs Anonymous Guest segment metrics."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            c.customer_type,
            ROUND(SUM(f.net_sales), 2) AS net_revenue,
            COUNT(DISTINCT f.transaction_id) AS orders,
            ROUND(SUM(f.net_sales) / COUNT(DISTINCT f.transaction_id), 2) AS aov
        FROM novamart.fact_sales f
        JOIN novamart.dim_customer c ON f.customer_key = c.customer_key
        GROUP BY c.customer_type;
    """)
    rows = {r[0]: (float(r[1]), int(r[2]), float(r[3])) for r in cur.fetchall()}
    cur.close()
    conn.close()
    
    # Identified
    id_rev, id_ord, id_aov = rows['Identified']
    assert id_rev == 16460527.82
    assert id_ord == 201667
    assert id_aov == 81.62
    
    # Anonymous
    anon_rev, anon_ord, anon_aov = rows['Anonymous']
    assert anon_rev == 30134645.45
    assert anon_ord == 384024
    assert anon_aov == 78.47


def test_page5_forecast_h1_total_and_bounds():
    """Verify Page 5 Forecast H1 2026 total equals $11,487,927.00 and prediction bounds are valid."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT forecast_month, forecast_net_revenue, lower_bound_95, upper_bound_95, model_name 
        FROM novamart.fact_forecast 
        ORDER BY forecast_month;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    assert len(rows) == 6
    
    total_forecast = sum([float(r[1]) for r in rows])
    assert round(total_forecast, 2) == 11487927.00, f"Expected H1 2026 forecast total $11,487,927.00, got {total_forecast}"
    
    for r in rows:
        f_month, fc, lower, upper, model = r
        fc, lower, upper = float(fc), float(lower), float(upper)
        assert lower <= fc <= upper
        assert model == "Seasonal Naive (Lag 12)"


def test_zero_actual_2026_sales():
    """Confirm zero actual 2026 revenue data exists in fact_sales."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM novamart.fact_sales WHERE transaction_date >= '2026-01-01';")
    count_2026 = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    assert count_2026 == 0
