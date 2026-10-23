"""Run one bounded bridge lane; never overlap more than the two allowed scene lanes."""
from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
jobs=[['run_north_query_v33.py','production'],['run_north_query_v33.py','observer'],
      ['audit_north_query_v33.py'],['record_remaining_v33.py']]
for script in ['run_bridge_mixed_v33.py','run_bridge_hostile_v33.py','run_bridge_infantry_v33.py']:
    jobs += [[script,'production'],[script,'observer']]
jobs += [['run_alias_scenes_v33.py'],
         ['run_acceptance_v33.py','observer','--only','tall-scenes','combined-scenes','bridge-observer']]
for args in jobs:
    print('Starting '+' '.join(args),flush=True)
    subprocess.run([sys.executable,'-X','utf8','-B',str(R/args[0]),*args[1:]],cwd=R,check=True)
print('Bridge and remaining observer lane complete',flush=True)
