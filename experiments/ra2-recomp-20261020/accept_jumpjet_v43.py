"""Bounded functional acceptance of the already-present Jumpjet coordinate/heading variation."""
from pathlib import Path
import copy,json,hashlib
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v43'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def accept(tag):
 root=S/'runs'/tag;p=root/'comparison.json';x=json.loads(p.read_text(encoding='utf-8'));c=x['comparison']
 assert not x['passed'] and all(r['passed'] and r['exit_code']==0 for r in x['runs']) and c['rng_equal_all_frames'] and c['command_difference'] is None
 assert c['first_difference']['frame']==581 and c['first_difference']['path']=='state.objects[id=1023364].position[0]'
 records={mode:[json.loads(l) for l in (root/mode/'state.jsonl').read_text(encoding='utf-8').splitlines()] for mode in ['original','generated-c']}
 if tag!='baseline-jumpjet':
  for mode,rs in records.items():assert rs==[json.loads(l) for l in (S/'runs/baseline-jumpjet'/mode/'state.jsonl').read_text(encoding='utf-8').splitlines()],('Variation must be exactly inherited',tag,mode)
 a=records['original'];b=copy.deepcopy(records['generated-c']);maximum=[0,0];heading=[0,0];air=[]
 for left,right in zip(a,b):
  if left['kind']=='state':
   u=next(o for o in left['objects'] if o['id']==1023364);v=next(o for o in right['objects'] if o['id']==1023364)
   assert u['class']==v['class']==0x7A3540 and u['health']==v['health']==125
   for i,limit in [(0,1),(1,22)]:
    d=abs(u['position'][i]-v['position'][i]);assert d<=limit;maximum[i]=max(maximum[i],d);v['position'][i]=u['position'][i]
   for i in [0,1]:
    d=(u['facings'][1][i]-v['facings'][1][i])%65536;d=min(d,65536-d);assert d<=580;heading[i]=max(heading[i],d);v['facings'][1][i]=u['facings'][1][i]
   if 65<=u['position'][1]//256<=67 and u['position'][2]>800:air.append(left['frame'])
  assert left==right,('Only four already-audited fields may differ',left.get('frame'))
 assert air and len([q for q in a if q['kind']=='state'])==1001 and c['negative_control']['passed']
 for mode,rs in records.items():
  u=next(o for o in [q for q in rs if q['kind']=='state'][-1]['objects'] if o['id']==1023364);assert [z//256 for z in u['position'][:2]]==[60,75]
 result=dict(passed=True,comparison_sha256=sha(p),strict_comparison_preserved_false=True,max_world_coordinate_delta=maximum,max_circular_facing_delta=heading,position_z_health_mission_rng_and_all_other_fields_equal=True,airborne_gap_crossing_frames=air,baseline_inherited_exactly=tag!='baseline-jumpjet',baseline_original_trace_sha256=sha(S/'runs/baseline-jumpjet/original/state.jsonl'),baseline_C_trace_sha256=sha(S/'runs/baseline-jumpjet/generated-c/state.jsonl'),scope='At most22/256 cell and580/65536 turn; same airborne crossing, goal cell, health, mission, RNG and ordinary commands. No new flight implementation or bug-for-bug fix in this batch.')
 q=root/'functional-acceptance.json'
 if q.exists():assert json.loads(q.read_text())==result
 else:q.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys;print(accept(sys.argv[1]))
