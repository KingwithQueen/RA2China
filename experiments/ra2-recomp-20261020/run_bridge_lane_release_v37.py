"""Bounded production or independent observation of the held-exit detours."""
from pathlib import Path
R=Path(__file__).resolve().parent
t=(R/'run_bridge_mixed_v37.py').read_text(encoding='utf-8').replace('bridge-mixed-fixtures.json','bridge-lane-release-fixtures.json').replace("'mh-'","'lh-'").replace("'mp-'","'lp-'")
exec(compile(t,str(Path(__file__)),'exec'),dict(__file__=str(Path(__file__)),__name__='__main__'))
