"""Mixed vehicle/infantry passengers at two natural shores and inherited full-occupancy retry."""
from run_batch_v55 import R,S,read,sha
import json
def records_from(root,tag,mode):return [json.loads(l) for l in (root/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def records(tag,mode):return records_from(S,tag,mode)
def analyze(tag):
 recipe=next(x for x in read(S/'dynamic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag']]);kind=recipe['tag'];base=recipe['baseline_tag'];end=recipe['last'];base_root=R/'evidence'/recipe.get('baseline_stage',S.name)
 p=S/'runs'/tag/'comparison.json';q=read(p);assert all(x['passed'] and x['exit_code']==0 for x in q['runs']);effects={};rng={}
 for mode in ['original','generated-c']:
  rs=records(tag,mode)
  current_baseline=(base_root==S and tag==base)
  if not current_baseline:assert rs==records_from(base_root,base,mode),('Full pre-change trace changed',tag,mode)
  h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'};assert len(h)==end+1
  rng[mode]={r['frame']:r['rng'] for r in rs if r['kind']=='state'};cells={tuple(c['cell']):c for c in read(S/'runs'/tag/mode/'cells.json')['cells']}
  cell=lambda o:tuple(v//256 for v in o['position'][:2]);land=lambda o:cells[cell(o)]['land']
  carrier,ship,other=[recipe[k] for k in ['carrier_id','ship_id','other_id']]
  cargo_ids=recipe.get('cargo_ids',[recipe.get('cargo_id')]);expected={carrier:300,ship:600,other:125}
  for u in cargo_ids:expected[u]=125 if kind in ['mi','sc','fm'] and u==1023368 else 200
  for u in recipe.get('traffic_ids',[]):expected[u]=200
  for b in recipe.get('blockers',[]):expected[b['id']]=200
  if recipe.get('foot_id'):expected[recipe['foot_id']]=125
  assert all(all(u in v and v[u]['health']==hp for u,hp in expected.items()) for v in h.values())
  assert h[0][carrier]['locomotor_vtable']==0x7A31EC and h[0][ship]['locomotor_vtable']==0x7AB13C
  assert all(land(v[ship])==2 and v[ship]['position'][2]==0 for v in h.values())
  assert cell(h[end][carrier])==tuple(recipe.get('shore',[138,102]))
  assert cell(h[end][ship])==(130,106)
  flags={u:{r['frame']:r['bytes_74_75_76_79_7a_7d'] for r in rs if r['kind']=='fixture-object-flags' and r['id']==u} for u in cargo_ids}
  changes={}
  for u,values in flags.items():
   previous=False;changes[u]=[];assert len(values)==end+1
   for f,v in values.items():
    loaded=not v[0] and bool(v[2])
    if loaded!=previous:changes[u].append((f,loaded));previous=loaded
  loaded_ids=recipe.get('expected_loaded_ids',cargo_ids)
  cycles={}
  for u in loaded_ids:
   ch=changes[u];assert [v for _,v in ch]==[True,False],(kind,mode,u,ch)
   cycles[u]=[]
   for (board,_),(drop,_) in zip(ch[::2],ch[1::2]):
    assert all(not flags[u][f][0] and flags[u][f][2] for f in range(board,drop))
    water=[f for f in range(board,drop) if land(h[f][carrier])==2];beach=[f for f in range(board,drop) if land(h[f][carrier])==6]
    assert water and beach and land(h[drop][u]) in [0,7]
    cycles[u].append(dict(board_frame=board,drop_frame=drop,water_frames=len(water),landing_cell=list(cell(h[drop][u])),landing_land=land(h[drop][u])))
  special={}
  if kind=='aw3':
   u=cargo_ids[0];drop=cycles[u][0]['drop_frame'];neighbours={(x,y) for x in range(137,140) for y in range(101,104) if (x,y)!=(138,102)}
   assert len(neighbours)==8 and all(cells[c]['land'] in [0,7] and not cells[c]['bridge'] for c in neighbours)
   assert all(cell(h[0][b['id']]) not in neighbours and h[0][b['id']]['locomotor_vtable']==0x7A04CC for b in recipe['blockers'])
   assert all(h[f][b['id']]['position'][2]==0 for f in range(recipe['unload_order'],recipe['release_order']) for b in recipe['blockers'])
   full=[f for f in range(recipe['unload_order'],recipe['release_order']) if neighbours.issubset({cell(h[f][b['id']]) for b in recipe['blockers']})]
   assert len(full)>=100 and full==list(range(recipe['unload_order'],recipe['release_order'])),('Not fully occupied',mode,len(full))
   assert all(not flags[u][f][0] and flags[u][f][2] for f in full) and drop>=recipe['release_order']
   release=recipe['release_id'];first=next(f for f in range(recipe['release_order'],end+1) if h[f][release]['position']!=h[f-1][release]['position'])
   vacancy=next(f for f in range(first,end+1) if not neighbours.issubset({cell(h[f][b['id']]) for b in recipe['blockers']}))
   assert first<=vacancy<drop and cell(h[end][u])==tuple(recipe['cargo_goal'])
   assert cell(h[end][release])==tuple(recipe['release_goal']) and cell(h[end][recipe['foot_id']])==(141,100) and cell(h[end][other])==(140,100)
   special=dict(full_occupied_range=[full[0],full[-1]],full_occupied_frames=len(full),legal_adjacent_cells=[list(v) for v in sorted(neighbours)],release_order=recipe['release_order'],first_actual_release_motion=first,first_vacant_cell_frame=vacancy,unload_retry_order=recipe['unload_retry_order'],first_actual_unload=drop,automatic_unload_before_retry=drop<recipe['unload_retry_order'],cargo_final_cell=recipe['cargo_goal'],release_final_cell=recipe['release_goal'])
  elif kind in ['mi','sc','fm']:
   car,foot=cargo_ids;assert h[0][car]['class']==0x7ADDF8 and h[0][foot]['class']==0x7A3540
   assert h[0][car]['locomotor_vtable']==0x7A04CC
   simultaneous=[f for f in range(end+1) if all(not flags[u][f][0] and flags[u][f][2] for u in cargo_ids)]
   water=[f for f in simultaneous if land(h[f][carrier])==2];beach=[f for f in simultaneous if land(h[f][carrier])==6]
   assert len(water)>100 and beach
   drops=sorted((cycles[u][0]['drop_frame'],u) for u in cargo_ids);assert [u for _,u in drops]==recipe.get('drop_order',[foot,car])
   for u,goal in recipe['goals'].items():
    assert cell(h[end][int(u)])==tuple(goal),(kind,mode,u,cell(h[end][int(u)]),goal)
    assert h[end][int(u)]['mission'][0]==5
   sx,sy=recipe['shore'];offsets=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
   neighbours=[cells[(sx+dx,sy+dy)]['land'] for dx,dy in offsets]
   assert neighbours==([7,0,0,0,0,0,0,0] if kind=='mi' else [0,0,0,7,7,6,6,6])
   traffic_at_unload={u:list(cell(h[recipe['unload_order']][u])) for u in recipe['traffic_ids']}
   if kind in ['sc','fm']:assert traffic_at_unload=={1023366:[139,106],1023367:[137,106]}
   special=dict(simultaneous_loaded_range=[simultaneous[0],simultaneous[-1]],mixed_passengers=[dict(id=car,type='TRUCKA',size=6),dict(id=foot,type='E2',size=1)],payload_size=7,capacity=12,size_limit=6,water_with_both_frames=len(water),beach_with_both_frames=len(beach),drop_order=[u for _,u in drops],drop_frames=[f for f,_ in drops],shore=recipe['shore'],shore_land=cells[(sx,sy)]['land'],neighbour_land_vector=neighbours,traffic_at_unload=traffic_at_unload,all_normal_goals_guard=True)
  else:raise ValueError(kind)
  effects[mode]=dict(cycles=cycles,actor_health=expected,carrier_final_cell=list(cell(h[end][carrier])),ship_final_cell=list(cell(h[end][ship])),cargo_final_cells={u:list(cell(h[end][u])) for u in cargo_ids},special=special)
 keys=['actor_health','carrier_final_cell','ship_final_cell','cargo_final_cells']
 assert all(effects['original'][k]==effects['generated-c'][k] for k in keys)
 for u in loaded_ids:assert [(c['landing_cell'],c['landing_land']) for c in effects['original']['cycles'][u]]==[(c['landing_cell'],c['landing_land']) for c in effects['generated-c']['cycles'][u]]
 different=[f for f in rng['original'] if rng['original'][f]!=rng['generated-c'][f]]
 result=dict(passed=True,kind=kind,comparison_sha256=sha(p),strict_trace_passed=q['passed'],strict_failure_preserved=not q['passed'],baseline_inherited_exactly=not(base_root==S and tag==base),baseline_traces={m:sha(base_root/'runs'/base/m/'state.jsonl') for m in effects},effect_modes=effects,core_functional_goals_equal=True,rng_first_different_frame=different[0] if different else None,rng_different_frames=len(different),scope='Only observed capacity, full adjacent occupancy/wait/release, unload order and natural traffic effects. Current complete per-mode traces equal pre-change baselines; raw strict failures preserved, no RNG reset/comparator relaxation or whole-game equivalence claim.')
 result=json.loads(json.dumps(result));out=p.parent/'functional-acceptance.json'
 if out.exists():assert read(out)==result
 else:out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys
 x=analyze(sys.argv[1]);print(dict(passed=True,kind=x['kind'],effects=x['effect_modes'],rng_first=x['rng_first_different_frame']))
