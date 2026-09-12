import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.load_postgres import get_db_connection

def verify_all_details():
    with open("powerbi/NovaMart.Dataset/model.bim", "r", encoding="utf-8") as f:
        bim = json.load(f)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    model = bim["model"]
    tables = model["tables"]
    
    print("=== CHECKING COLUMNS DATA TYPES MATCH ===")
    for t in tables:
        t_name = t["name"]
        if t_name == "_Measures":
            continue
        print(f"\nChecking table/view: {t_name}")
        cur.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'novamart' AND table_name = '{t_name}';
        """)
        pg_cols = dict(cur.fetchall())
        bim_cols = {c["name"]: c.get("dataType") for c in t.get("columns", [])}
        
        # Compare
        for c_name, b_type in bim_cols.items():
            pg_type = pg_cols.get(c_name)
            if not pg_type:
                print(f"  [ERROR] Column {c_name} in model.bim does not exist in PostgreSQL {t_name}!")
            else:
                print(f"  [OK] {c_name}: bim={b_type}, pg={pg_type}")
                
        for pg_c in pg_cols:
            if pg_c not in bim_cols:
                print(f"  [WARNING] PostgreSQL column {pg_c} not included in model.bim {t_name}")

    print("\n=== CHECKING RELATIONSHIPS KEYS DATA TYPES ===")
    for r in model.get("relationships", []):
        f_tab, f_col = r["fromTable"], r["fromColumn"]
        t_tab, t_col = r["toTable"], r["toColumn"]
        
        # Get bim data types
        f_t_obj = next(t for t in tables if t["name"] == f_tab)
        t_t_obj = next(t for t in tables if t["name"] == t_tab)
        f_col_type = next(c["dataType"] for c in f_t_obj["columns"] if c["name"] == f_col)
        t_col_type = next(c["dataType"] for c in t_t_obj["columns"] if c["name"] == t_col)
        
        # Check pg types
        cur.execute(f"SELECT data_type FROM information_schema.columns WHERE table_schema='novamart' AND table_name='{f_tab}' AND column_name='{f_col}';")
        pg_f_type = cur.fetchone()[0]
        cur.execute(f"SELECT data_type FROM information_schema.columns WHERE table_schema='novamart' AND table_name='{t_tab}' AND column_name='{t_col}';")
        pg_t_type = cur.fetchone()[0]
        
        print(f"Rel {r['name']}:")
        print(f"  {f_tab}.{f_col} ({f_col_type}, pg:{pg_f_type}) -> {t_tab}.{t_col} ({t_col_type}, pg:{pg_t_type})")
        assert f_col_type == t_col_type, f"Type mismatch in BIM: {f_col_type} vs {t_col_type}"
        print(f"  -> MATCH OK")

    cur.close()
    conn.close()

if __name__ == "__main__":
    verify_all_details()
