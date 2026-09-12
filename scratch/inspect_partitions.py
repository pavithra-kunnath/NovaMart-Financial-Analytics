import json

with open('powerbi/NovaMart.Dataset/model.bim', 'r', encoding='utf-8') as f:
    bim = json.load(f)

model = bim.get('model', {})
tables = model.get('tables', [])

for t in tables:
    print(f"=== TABLE: {t.get('name')} ===")
    print("Columns:")
    for c in t.get('columns', []):
        print(f"  {json.dumps(c)}")
    print("Partitions:")
    for p in t.get('partitions', []):
        print(f"  {json.dumps(p, indent=4)}")
    print()
