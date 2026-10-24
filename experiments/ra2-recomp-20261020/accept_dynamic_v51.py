"""Finite transport/aircraft effects, with full per-mode pre-change trace identity."""
from run_batch_v51 import R,S,read,sha
import json
def records(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def analyze(tag):
 recipe=next(x for x in read(S/'dynamic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag']]);kind=recipe['tag'];base=recipe['baseline_tag'];end=recipe['last']
 p=S/'runs'/tag/'comparison.json';q=read(p);assert all(x['passed'] and x['exit_code']==0 for x in q['runs'])
 effects={};rng={}
 for mode in ['original','generated-c']:
  rs=records(tag,mode)
  if tag!=base:assert rs==records(base,mode),('Full pre-change trace changed',tag,mode)
  h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'};assert len(h)==end+1
  rng[mode]={r['frame']:r['rng'] for r in rs if r['kind']=='state'};cells={tuple(c['cell']):c for c in read(S/'runs'/tag/mode/'cells.json')['cells']}
  cell=lambda o:tuple(v//256 for v in o['position'][:2])
  land=lambda o:cells[cell(o)]['land']
  if kind=='of':
   plane,ship,foot=recipe['aircraft_id'],recipe['ship_id'],recipe['foot_id'];field=1023368
   expected={plane:150,ship:600,foot:125,field:600}
   assert all(all(u in v and v[u]['health']==hp for u,hp in expected.items()) for v in h.values())
   assert h[0][plane]['class']==0x79B12C and h[0][field]['class']==0x79CBBC
   assert h[0][plane]['owner']==h[0][field]['owner']
   airborne=[f for f,v in h.items() if v[plane]['position'][2]>50];groups=[]
   for f in airborne:
    if not groups or groups[-1][-1]!=f-1:groups.append([f])
    else:groups[-1].append(f)
   assert len(groups)>=3 and max(v[plane]['position'][2] for v in h.values())>=800
   assert any(v[plane]['mission'][0]==7 for v in h.values())
   assert h[end][plane]['position']==[34944,26240,0] and h[end][plane]['mission'][0]==5
   assert cell(h[end][ship])==(130,94) and cell(h[end][foot])==(140,100)
   assert all(land(v[ship])==2 and v[ship]['position'][2]==0 for v in h.values())
   effects[mode]=dict(airborne_groups=[[g[0],g[-1]] for g in groups],peak_height=max(v[plane]['position'][2] for v in h.values()),aircraft_final=h[end][plane]['position'],aircraft_final_mission=5,airport_health=600,aircraft_health=150,ship_final_cell=list(cell(h[end][ship])),foot_final_cell=list(cell(h[end][foot])),enter_mission_observed=True,requested_water_cells_not_claimed_reached=True)
   continue
  air=kind=='ca';carrier=recipe['carrier_id'];cargo=recipe['cargo_id'];ship=1023363 if air else 1023364;foot=1023367;tele=1023366 if air else 1023368
  expected={carrier:175 if air else 300,cargo:125 if air else 200,ship:600,foot:125,tele:125}
  if not air:expected[1023366]=200
  assert all(all(u in v and v[u]['health']==hp for u,hp in expected.items()) for v in h.values())
  assert h[0][carrier]['locomotor_vtable']==(0x7A52A4 if air else 0x7A31EC) and h[0][ship]['locomotor_vtable']==0x7AB13C
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
  assert cell(h[end][ship])==((130,96) if air else (130,106)) and cell(h[end][foot])==(140,100) and cell(h[end][tele])==(138,105)
  assert all(land(v[ship])==2 and v[ship]['position'][2]==0 for v in h.values())
  blocker=None
  if not air:
   drop=cycles[0]['drop_frame'];assert cell(h[drop][1023366])==(138,101) and cycles[0]['landing_cell']!=[138,101] and drop<1500
   assert cell(h[end][1023366])==(138,104)
   first=next(f for f in range(1500,end+1) if h[f][1023366]['position']!=h[f-1][1023366]['position'])
   blocker=dict(occupied_cell=[138,101],initial_move_order=1500,followup_move_order=2250,first_actual_motion=first,alternate_landing=cycles[0]['landing_cell'])
  effects[mode]=dict(cycles=cycles,cycle_count=2,carrier_final_cell=list(cell(h[end][carrier])),cargo_final_cell=list(cell(h[end][cargo])),ship_final_cell=list(cell(h[end][ship])),teleport_final_cell=list(cell(h[end][tele])),foot_final_cell=list(cell(h[end][foot])),actor_health=expected,occupied_shore=blocker)
 if kind=='of':keys=['aircraft_final','aircraft_final_mission','airport_health','aircraft_health','ship_final_cell','foot_final_cell']
 else:keys=['cycle_count','carrier_final_cell','cargo_final_cell','ship_final_cell','teleport_final_cell','foot_final_cell','actor_health']
 assert all(effects['original'][k]==effects['generated-c'][k] for k in keys)
 if kind!='of':
  assert [(x['landing_cell'],x['landing_land']) for x in effects['original']['cycles']]==[(x['landing_cell'],x['landing_land']) for x in effects['generated-c']['cycles']]
 different=[f for f in rng['original'] if rng['original'][f]!=rng['generated-c'][f]]
 result=dict(passed=True,kind=kind,comparison_sha256=sha(p),strict_trace_passed=q['passed'],strict_failure_preserved=not q['passed'],baseline_inherited_exactly=tag!=base,baseline_traces={m:sha(S/'runs'/base/m/'state.jsonl') for m in effects},effect_modes=effects,core_functional_goals_equal=True,rng_first_different_frame=different[0] if different else None,rng_different_frames=len(different),scope='Only these transport cycles, occupied-shore fallback or normal-airfield flight/return effects. Timing/height/subcell differences recorded, no RNG synchronization or global comparator relaxation. Complete current traces must equal their pre-change mode baselines; not whole-game equivalence.')
 result=json.loads(json.dumps(result));out=p.parent/'functional-acceptance.json'
 if out.exists():assert read(out)==result
 else:out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys
 x=analyze(sys.argv[1]);print(dict(passed=True,kind=x['kind'],effects=x['effect_modes'],rng_first=x['rng_first_different_frame']))
