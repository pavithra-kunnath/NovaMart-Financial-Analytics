import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.load_postgres import get_db_connection

def run_deep_diagnosis():
    # 1. Load model.bim
    bim_path = Path("powerbi/NovaMart.Dataset/model.bim")
    with open(bim_path, "r", encoding="utf-8") as f:
        bim = json.load(f)
        
    model = bim.get("model", {})
    tables = model.get("tables", [])
    relationships = model.get("relationships", [])
    data_sources = model.get("dataSources", [])
    
    print("==================================================")
    print("1. MODEL.BIM INSPECTION")
    print("==================================================")
    print(f"Name: {bim.get('name')}")
    print(f"CompatibilityLevel: {bim.get('compatibilityLevel')}")
    print(f"Culture: {model.get('culture')}")
    print(f"defaultPowerBIDataSourceVersion: {model.get('defaultPowerBIDataSourceVersion')}")
    print("Annotations:")
    for a in model.get("annotations", []):
        print(f"  {a.get('name')}: {a.get('value')}")
        
    # Table & column registry
    table_cols = {}
    table_measures = {}
    for t in tables:
        t_name = t.get("name")
        cols = [c.get("name") for c in t.get("columns", [])]
        table_cols[t_name] = cols
        measures = [m.get("name") for m in t.get("measures", [])]
        table_measures[t_name] = measures
        print(f"\nTable: {t_name}")
        print(f"  Columns ({len(cols)}): {cols}")
        if measures:
            print(f"  Measures ({len(measures)}): {measures}")
        # Partitions
        for p in t.get("partitions", []):
            p_name = p.get("name")
            p_mode = p.get("mode")
            p_source = p.get("source", {})
            print(f"  Partition: {p_name}, mode: {p_mode}, type: {p_source.get('type')}")
            expr = p_source.get("expression", "")
            print(f"    Expression snippet: {expr.replace(chr(10), ' ')[:100]}...")

    # 2. Check Relationships
    print("\n==================================================")
    print("2. RELATIONSHIPS INSPECTION")
    print("==================================================")
    for r in relationships:
        r_name = r.get("name")
        f_tab = r.get("fromTable")
        f_col = r.get("fromColumn")
        t_tab = r.get("toTable")
        t_col = r.get("toColumn")
        f_card = r.get("fromCardinality")
        t_card = r.get("toCardinality")
        cross = r.get("crossFilteringBehavior")
        
        f_valid = f_tab in table_cols and f_col in table_cols[f_tab]
        t_valid = t_tab in table_cols and t_col in table_cols[t_tab]
        print(f"Rel: {r_name}")
        print(f"  {f_tab}[{f_col}] ({f_card}) -> {t_tab}[{t_col}] ({t_card}), cross: {cross}")
        print(f"  From valid: {f_valid}, To valid: {t_valid}")

    # 3. Check All 29 DAX Measures
    print("\n==================================================")
    print("3. DAX MEASURES VALIDATION")
    print("==================================================")
    measures_list = []
    for t in tables:
        for m in t.get("measures", []):
            measures_list.append((m.get("name"), m.get("expression"), m.get("formatString")))
            
    print(f"Total measures defined: {len(measures_list)}")
    all_measure_names = set(m[0] for m in measures_list)
    
    # Check measure expressions for references
    # Pattern for table[col] or [measure]
    for name, expr, fmt in measures_list:
        # Check [Measure] references
        bracket_refs = re.findall(r'(?<!\w)\[([^\]]+)\]', expr)
        # Check Table[Column] references
        table_col_refs = re.findall(r'(\w+)\[([^\]]+)\]', expr)
        
        issues = []
        for t_ref, c_ref in table_col_refs:
            if t_ref not in table_cols:
                issues.append(f"Unknown table '{t_ref}' in reference '{t_ref}[{c_ref}]'")
            elif c_ref not in table_cols[t_ref]:
                issues.append(f"Unknown column '{c_ref}' in table '{t_ref}'")
                
        for b_ref in bracket_refs:
            # If not part of a table_col_ref
            is_col = False
            for t_ref, c_ref in table_col_refs:
                if c_ref == b_ref:
                    is_col = True
                    break
            if not is_col:
                if b_ref not in all_measure_names:
                    issues.append(f"Unknown measure reference '[{b_ref}]'")
                    
        status = "OK" if not issues else f"FAIL: {issues}"
        print(f"  - {name}: {status}")

    # 4. Check report.json
    print("\n==================================================")
    print("4. REPORT.JSON VALIDATION")
    print("==================================================")
    report_path = Path("powerbi/NovaMart.Report/report.json")
    with open(report_path, "r", encoding="utf-8") as f:
        rep = json.load(f)
        
    print(f"Report top-level keys: {list(rep.keys())}")
    sections = rep.get("sections", [])
    print(f"Sections count: {len(sections)}")
    for s in sections:
        s_name = s.get("name")
        s_disp = s.get("displayName")
        containers = s.get("visualContainers", [])
        print(f"\nSection: '{s_disp}' ({s_name}), ordinal: {s.get('ordinal')}, containers: {len(containers)}")
        for c in containers:
            c_name = c.get("name")
            c_config_str = c.get("config", "")
            try:
                c_conf = json.loads(c_config_str)
                # Check properties inside config
                v_type = c_conf.get("type")
                v_title = c_conf.get("title")
                # Does it have 'singleVisual'?
                has_singleVisual = "singleVisual" in c_conf
                print(f"    Container: {c_name} | Type: {v_type} | Title: {v_title} | has_singleVisual: {has_singleVisual}")
            except Exception as ex:
                print(f"    Container: {c_name} | INVALID JSON: {ex}")

if __name__ == '__main__':
    run_deep_diagnosis()
