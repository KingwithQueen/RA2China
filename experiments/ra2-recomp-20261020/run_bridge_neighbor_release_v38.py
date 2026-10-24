"""Bounded production or independent observation of the held-exit detours."""
from pathlib import Path
R=Path(__file__).resolve().parent
t=(R/'run_bridge_mixed_v38.py').read_text(encoding='utf-8').replace('bridge-mixed-fixtures.json','bridge-neighbor-release-fixtures.json').replace("'mh-'","'nh-'").replace("'mp-'","'nr-'")
exec(compile(t,str(Path(__file__)),'exec'),dict(__file__=str(Path(__file__)),__name__='__main__'))
