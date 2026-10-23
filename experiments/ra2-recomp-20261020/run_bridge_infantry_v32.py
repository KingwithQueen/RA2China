"""Use the bounded production/observer pair runner for ordinary moving infantry."""
from pathlib import Path
R=Path(__file__).resolve().parent
t=(R/'run_bridge_mixed_v32.py').read_text(encoding='utf-8').replace('bridge-mixed-fixtures.json','bridge-infantry-fixtures.json').replace("'mh-'","'ih-'").replace("'mp-'","'ip-'")
exec(compile(t,str(Path(__file__)),'exec'),dict(__file__=str(Path(__file__)),__name__='__main__'))
