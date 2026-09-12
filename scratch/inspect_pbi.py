import json
import os

with open('powerbi/NovaMart.Dataset/model.bim', 'r', encoding='utf-8') as f:
    bim = json.load(f)

with open('powerbi/NovaMart.Report/report.json', 'r', encoding='utf-8') as f:
    rep = json.load(f)

print("=== MODEL.BIM TOP LEVEL ===")
for k, v in bim.items():
    if k != 'model':
        print(f"{k}: {v}")

model = bim.get('model', {})
print("\n=== MODEL PROPERTIES ===")
for k, v in model.items():
    if k not in ['tables', 'relationships', 'dataSources', 'roles', 'cultures']:
        print(f"{k}: {v}")

print("\n=== DATASOURCES ===")
print(json.dumps(model.get('dataSources', []), indent=2))

tables = {t['name']: t for t in model.get('tables', [])}

print("\n=== TABLES & PARTITIONS ===")
for tname, t in tables.items():
    print(f"\nTable: {tname}")
    print("  Columns:")
    for c in t.get('columns', []):
        print(f"    - {c.get('name')} | dataType: {c.get('dataType')} | sourceColumn: {c.get('sourceColumn')} | formatString: {c.get('formatString')} | sortByColumn: {c.get('sortByColumn')}")
    print("  Partitions:")
    for p in t.get('partitions', []):
        print(f"    - {p.get('name')} | mode: {p.get('mode')} | source type: {p.get('source', {}).get('type')}")
        expr = p.get('source', {}).get('expression')
        if expr:
            print("      Expression:")
            for line in str(expr).split('\n'):
                print(f"        {line}")

print("\n=== RELATIONSHIPS ===")
for r in model.get('relationships', []):
    print(json.dumps(r, indent=2))

print("\n=== MEASURES ===")
m_table = tables.get('_Measures', {})
measures = m_table.get('measures', [])
print(f"Total measures: {len(measures)}")
for m in measures:
    print(f"  - {m.get('name')}: {m.get('expression')}")

print("\n=== REPORT SECTIONS ===")
for sec in rep.get('sections', []):
    print(f"\nSection: {sec.get('name')} | DisplayName: {sec.get('displayName')}")
    for vc in sec.get('visualContainers', []):
        print(f"  VisualContainer: {vc.get('name')} | config: {vc.get('config')}")
