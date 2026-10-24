"""Use the bounded production/observer pair runner for ordinary moving infantry."""
from pathlib import Path
R=Path(__file__).resolve().parent
import json,os
S=R/'evidence/movement-state-v38'
if json.loads((S/'observer-lane-assignment.json').read_text(encoding='utf-8')).get('bridge_infantry_on_core_lane') and os.environ.get('RA2_V38_CORE_INFANTRY')!='1':
    print('Infantry scenes assigned to the end of the owned core lane',flush=True);raise SystemExit(0)
t=(R/'run_bridge_mixed_v38.py').read_text(encoding='utf-8').replace('bridge-mixed-fixtures.json','bridge-infantry-fixtures.json').replace("'mh-'","'ih-'").replace("'mp-'","'ip-'")
exec(compile(t,str(Path(__file__)),'exec'),dict(__file__=str(Path(__file__)),__name__='__main__'))
