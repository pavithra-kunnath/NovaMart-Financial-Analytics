import psycopg2, os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(
    host=os.getenv('PGHOST', 'localhost'),
    port=os.getenv('PGPORT', 5432),
    dbname=os.getenv('PGDATABASE', 'novamart_db'),
    user=os.getenv('PGUSER', 'postgres'),
    password=os.getenv('PGPASSWORD')
)
cur = conn.cursor()

tables = ['dim_date', 'dim_customer', 'dim_product', 'dim_store', 'vw_pbi_fact_sales', 'vw_pbi_fact_forecast']

for t in tables:
    print(f"=== POSTGRESQL TABLE/VIEW: novamart.{t} ===")
    cur.execute(f"""
        SELECT column_name, data_type, udt_name, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'novamart' AND table_name = '{t}'
        ORDER BY ordinal_position;
    """)
    cols = cur.fetchall()
    for c in cols:
        print(f"  {c[0]} | {c[1]} ({c[2]}) | nullable: {c[3]}")
    print()

cur.close()
conn.close()
