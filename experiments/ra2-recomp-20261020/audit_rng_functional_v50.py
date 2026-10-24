"""Inspect finite functional impact of retained/new RNG variants; no new synchronization."""
from run_batch_v50 import *
T=R/'evidence/movement-state-v48/runs/b3-dc';modes={};rng={};protected=[O/'rng-provenance.json',T/'comparison.json']
for mode in ['original','generated-c']:
 p=T/mode/'state.jsonl';protected.append(p);rs=[json.loads(l) for l in p.open(encoding='utf-8')];h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'}
 rng[mode]={r['frame']:r['rng'] for r in rs if r['kind']=='state'}
 flags={r['frame']:r['bytes_74_75_76_79_7a_7d'] for r in rs if r['kind']=='fixture-object-flags' and r['id']==1023363};board=next(f for f,v in flags.items() if not v[0] and v[2]);drop=next(f for f,v in flags.items() if f>board and v[0] and not v[2]);assert all(not flags[f][0] and flags[f][2] for f in range(board,drop))
 bridge={r['frame']:r['bridge'] for r in rs if r['kind']=='fixture-bridge-state'};collapse=next(f for f,v in bridge.items() if v==[0,0]);trap=next(f for f,q in h.items() if 1023364 not in q)
 cell=lambda o:[v//256 for v in o['position'][:2]]
 expected={1023362:([63,59],300),1023363:([64,62],200),1023365:([64,72],200),1023366:([65,61],125)}
 assert all(cell(h[2200][u])==xy and h[2200][u]['health']==hp and h[2200][u]['mission'][0]==5 for u,(xy,hp) in expected.items())
 modes[mode]=dict(board_frame=board,drop_frame=drop,collapse_frame=collapse,trap_removed_frame=trap,landing_cell=cell(h[drop][1023363]),goal_cells={str(u):cell(h[2200][u]) for u in expected},final_health={str(u):h[2200][u]['health'] for u in expected},final_positions={str(u):h[2200][u]['position'] for u in expected})
keys=['board_frame','drop_frame','collapse_frame','trap_removed_frame','landing_cell','goal_cells','final_health'];assert all(modes['original'][k]==modes['generated-c'][k] for k in keys)
diff=[f for f in rng['original'] if rng['original'][f]!=rng['generated-c'][f]];assert diff[0]==1029
new={}
for tag in ['w2','a2']:
 x=read(S/'runs'/tag/'functional-acceptance.json');assert x['passed'] and x['baseline_inherited_exactly'] and x['core_functional_goals_equal'] and x['strict_failure_preserved']
 recipe=next(q for q in read(S/'dynamic-fixtures.json')['fixtures'] if q['tag']==tag);base=recipe['baseline_tag'];ship=1023364 if tag=='w2' else 1023363;arrival={}
 for mode in ['original','generated-c']:
  rs=[json.loads(l) for l in (S/'runs'/base/mode/'state.jsonl').open(encoding='utf-8')];h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'}
  arrival[mode]=[dict(frame=f,position=h[f][ship]['position'],mission=h[f][ship]['mission']) for f in range(345,351)]
 new[tag]=dict(functional_acceptance_sha256=sha(S/'runs'/tag/'functional-acceptance.json'),first_rng_frame=x['rng_first_different_frame'],rng_different_frames=x['rng_different_frames'],ship_arrival_observations=arrival,exact_rng_call_source_proved_this_round=False,whole_tail_random_assignment_equal=False,finite_transport_health_and_goals_equal=True)
write(S/'rng-functional-impact.json',dict(passed=True,scope='Finite effects analysis; old1029 trace inherited/read only, new natural coast scenes measured this round. No new RNG hook, reset, seed change or global comparator relaxation.',protected_parent_files=[dict(path=str(p),sha256=sha(p)) for p in protected],old_variant=dict(modes=modes,rng_different_frames=len(diff),first_rng_frame=diff[0],functional_effect_keys_equal=keys,exact_subcell_positions_equal=False,inherited_call_provenance_sha256=sha(O/'rng-provenance.json'),not_counted_as_new_scene_pair=True),new_variants=new,conclusion='Observed differences preserve these transport states, target cells, health and bridge effects. Arrival/height/subcell timing and later random assignments remain recorded differences; no full-game equivalence or exact new ship-call attribution claim.'))
print(dict(passed=True,old_rng_frames=len(diff),new={k:v['first_rng_frame'] for k,v in new.items()}))
