"""Run the selected legal scene through production and an independent observer."""
from pathlib import Path
R=Path(__file__).resolve().parent
t=(R/'run_bridge_mixed_v37.py').read_text(encoding='utf-8').replace('bridge-mixed-fixtures.json','north-query-fixtures.json').replace("'mh-'","'nh-'").replace("'mp-'","'np-'")
exec(compile(t,str(Path(__file__)),'exec'),dict(__file__=str(Path(__file__)),__name__='__main__'))
