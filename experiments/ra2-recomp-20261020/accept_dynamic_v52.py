"""Finite coast effects with unchanged pre-change per-mode traces and raw differences."""
from run_batch_v52 import R,S,read,sha
import json
def records(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def analyze(tag):
 recipe=next(x for x in read(S/'dynamic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag']]);kind=recipe['tag'];base=recipe['baseline_tag'];end=recipe['last'];assert kind in ['ww','js']
 p=S/'runs'/tag/'comparison.json';q=read(p);assert all(x['passed'] and x['exit_code']==0 for x in q['runs'])
 effects={};rng={}
 for mode in ['original','generated-c']:
  rs=records(tag,mode)
  if tag!=base:assert rs==records(base,mode),('Full pre-change trace changed',tag,mode)
  h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'};assert len(h)==end+1
  rng[mode]={r['frame']:r['rng'] for r in rs if r['kind']=='state'};cells={tuple(c['cell']):c for c in read(S/'runs'/tag/mode/'cells.json')['cells']}
  cell=lambda o:tuple(v//256 for v in o['position'][:2]);land=lambda o:cells[cell(o)]['land']
  air=kind=='js';carrier,cargo,ship,foot,other=[recipe[k] for k in ['carrier_id','cargo_id','ship_id','foot_id','other_id']]
  expected={carrier:175 if air else 300,cargo:125 if air else 200,ship:600,foot:125,other:125}
  if not air:expected[recipe['blocker_id']]=200
  assert all(all(u in v and v[u]['health']==hp for u,hp in expected.items()) for v in h.values())
  assert h[0][carrier]['locomotor_vtable']==(0x7A52A4 if air else 0x7A31EC) and h[0][ship]['locomotor_vtable']==0x7AB13C
  assert h[0][other]['class']==h[0][foot]['class']==0x7A3540
  flags={r['frame']:r['bytes_74_75_76_79_7a_7d'] for r in rs if r['kind']=='fixture-object-flags' and r['id']==cargo};changes=[];previous=False
  for f,v in flags.items():
   loaded=not v[0] and bool(v[2])
   if loaded!=previous:changes.append((f,loaded));previous=loaded
  assert [v for f,v in changes]==[True,False,True,False]
  cycles=[]
  for (board,_),(drop,_) in zip(changes[::2],changes[1::2]):
   assert all(not flags[f][0] and flags[f][2] for f in range(board,drop))
   water=[f for f in range(board,drop) if land(h[f][carrier])==2];beach=[f for f in range(board,drop) if land(h[f][carrier])==6]
   assert len(water)>100 and beach and land(h[drop][cargo]) in [0,7]
   heights=[h[f][carrier]['position'][2] for f in water]
   assert all(450<=z<=550 for z in heights) if air else all(0<z<160 for z in heights)
   cycles.append(dict(board_frame=board,drop_frame=drop,landing_cell=list(cell(h[drop][cargo])),landing_land=land(h[drop][cargo]),water_frames=len(water),water_range=[water[0],water[-1]],water_height_range=[min(heights),max(heights)]))
  assert cell(h[end][cargo])==((140,104) if air else (139,104)) and h[end][cargo]['mission'][0]==5
  assert cell(h[end][carrier])==((139,102) if air else (138,102))
  assert cell(h[end][ship])==((130,96) if air else (130,106)) and cell(h[end][foot])==(140,100) and cell(h[end][other])==(138,105)
  assert all(land(v[ship])==2 and v[ship]['position'][2]==0 for v in h.values())
  assert all(v[foot]['position'][2]==0 for v in h.values())
  water_request=None;jumpjet=None;occupied=None
  if air:
   flight=[f for f,v in h.items() if v[other]['position'][2]>=450]
   moving=[f for f in flight if f and h[f][other]['position']!=h[f-1][other]['position']]
   peak=max(v[other]['position'][2] for v in h.values())
   assert len(flight)>500 and moving and 500<=peak<=650
   assert h[end][other]['position'][2]==500
   jumpjet=dict(airborne_frames=len(flight),moving_airborne_frames=len(moving),peak_height=peak,final_height=500,final_mission=h[end][other]['mission'][0],normal_ground_foot_height=0,infantry_locomotor_guid_from_rules=True,infantry_locomotor_pointer_not_recorded=True,submarine_depth_not_claimed=True,final_move_mission_not_claimed_guard=True)
  else:
   submitted=[r for r in rs if r['kind'] in ['submit','execute'] and r['frame']==700 and r['id']==carrier and r['mission']==16]
   assert {r['kind'] for r in submitted}=={'submit','execute'} and land(h[700][carrier])==2
   assert all(not flags[f][0] and flags[f][2] for f in range(700,900)) and cycles[0]['drop_frame']>900
   water_request=dict(submit_frame=700,execute_frame=700,carrier_cell=list(cell(h[700][carrier])),terrain=2,loaded_through_frame=899,first_actual_drop_frame=cycles[0]['drop_frame'],direct_unload_service_outcome_not_claimed=True)
   blocker=recipe['blocker_id'];drop=cycles[0]['drop_frame']
   assert cell(h[drop][blocker])==(138,101) and cycles[0]['landing_cell']!=[138,101] and drop<1500
   assert cell(h[end][blocker])==(138,104)
   first=next(f for f in range(1500,end+1) if h[f][blocker]['position']!=h[f-1][blocker]['position'])
   occupied=dict(occupied_cell=[138,101],initial_move_order=1500,followup_move_order=2250,first_actual_motion=first,alternate_landing=cycles[0]['landing_cell'])
  effects[mode]=dict(cycles=cycles,cycle_count=2,carrier_final_cell=list(cell(h[end][carrier])),cargo_final_cell=list(cell(h[end][cargo])),ship_final_cell=list(cell(h[end][ship])),other_final_cell=list(cell(h[end][other])),foot_final_cell=list(cell(h[end][foot])),actor_health=expected,water_unload_request=water_request,jumpjet_infantry=jumpjet,occupied_shore=occupied)
 keys=['cycle_count','carrier_final_cell','cargo_final_cell','ship_final_cell','other_final_cell','foot_final_cell','actor_health','water_unload_request']
 assert all(effects['original'][k]==effects['generated-c'][k] for k in keys)
 assert [(x['landing_cell'],x['landing_land']) for x in effects['original']['cycles']]==[(x['landing_cell'],x['landing_land']) for x in effects['generated-c']['cycles']]
 different=[f for f in rng['original'] if rng['original'][f]!=rng['generated-c'][f]]
 result=dict(passed=True,kind=kind,comparison_sha256=sha(p),strict_trace_passed=q['passed'],strict_failure_preserved=not q['passed'],baseline_inherited_exactly=tag!=base,baseline_traces={m:sha(S/'runs'/base/m/'state.jsonl') for m in effects},effect_modes=effects,core_functional_goals_equal=True,rng_first_different_frame=different[0] if different else None,rng_different_frames=len(different),scope='Only these repeated coast cycles, water unload request, landing occupancy and mixed infantry/vehicle/ship effects. Preserve timing/height/subcell differences; no RNG synchronization or comparator relaxation. Full current traces must equal their pre-change mode baselines; not whole-game equivalence.')
 result=json.loads(json.dumps(result));out=p.parent/'functional-acceptance.json'
 if out.exists():assert read(out)==result
 else:out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys
 x=analyze(sys.argv[1]);print(dict(passed=True,kind=x['kind'],effects=x['effect_modes'],rng_first=x['rng_first_different_frame']))
