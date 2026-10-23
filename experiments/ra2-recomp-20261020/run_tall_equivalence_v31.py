"""Reuse the accepted tall scene definitions while preserving the native stall."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
source=(R/'run_tall_curves_v31.py').read_text(encoding='utf-8')
old="dict(passed=all(r['paired'] and r['completed'] for r in results), results=results)"
assert source.count(old)==1
source=source.replace(old,"dict(passed=all(r['paired'] for r in results), all_routes_complete=all(r['completed'] for r in results), results=results)")
old="assert all(r['paired'] and r['completed'] for r in results), results"
assert source.count(old)==1
source=source.replace(old,"assert all(r['paired'] for r in results) and sum(r['completed'] for r in results)==2, results")
exec(compile(source,str(R/'run_tall_curves_v31.py'),'exec'),dict(__file__=str(R/'run_tall_curves_v31.py'),__name__='__main__'))
