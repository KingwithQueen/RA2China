"""Production and independent observation of the occupied meeting exits."""
from pathlib import Path
R=Path(__file__).resolve().parent
t=(R/'run_bridge_mixed_v34.py').read_text(encoding='utf-8').replace('bridge-mixed-fixtures.json','bridge-occupied-fixtures.json').replace("'mh-'","'oh-'").replace("'mp-'","'op-'")
exec(compile(t,str(Path(__file__)),'exec'),dict(__file__=str(Path(__file__)),__name__='__main__'))
