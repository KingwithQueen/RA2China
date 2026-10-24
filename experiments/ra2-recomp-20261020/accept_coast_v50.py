"""Finite functional gates; keep strict failures and freeze each mode to its full baseline."""
from run_batch_v50 import R,S,read,sha
import json,hashlib
from map_codec_v50 import unpack
def records(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def analyze(tag):
 recipe=next(x for x in read(S/'coast-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag']]);air=recipe['tag']=='a2';end=recipe['last'];base=recipe['baseline_tag']
 p=S/'runs'/tag/'comparison.json';q=read(p);assert all(x['passed'] and x['exit_code']==0 for x in q['runs'])
 assert hashlib.sha256(unpack((R/recipe['path']).read_text(encoding='ascii'))[1]).hexdigest()==recipe['natural_terrain_pack_sha256']
 output={};raw={}
 for mode in ['original','generated-c']:
  rs=records(tag,mode);raw[mode]=rs
  if tag!=base:assert rs==records(base,mode),('Full pre-change mode trace changed',tag,mode)
  h={r['frame']:{o['id']:o for o in r['objects']} for r in rs if r['kind']=='state'};assert len(h)==end+1
  carrier=1023362;cargo=1023365 if air else 1023363;ship=1023363 if air else 1023364;tele=1023366 if air else 1023368;foot=1023367
  expected={carrier:175 if air else 300,cargo:125 if air else 200,ship:600,tele:125,foot:125}
  if not air:expected[1023366]=200
  assert all(all(u in r and r[u]['health']==hp for u,hp in expected.items()) for r in h.values())
  assert h[0][carrier]['locomotor_vtable']==(0x7A52A4 if air else 0x7A31EC) and h[0][ship]['locomotor_vtable']==0x7AB13C
  flags={r['frame']:r['bytes_74_75_76_79_7a_7d'] for r in rs if r['kind']=='fixture-object-flags' and r['id']==cargo}
  board=next(f for f,v in flags.items() if not v[0] and v[2]);drop=next(f for f,v in flags.items() if f>board and v[0] and not v[2])
  assert board==(77 if air else 120) and drop==(2004 if air else 1904)
  assert all(not flags[f][0] and flags[f][2] for f in range(board,drop))
  cells={tuple(c['cell']):c for c in read(S/'runs'/tag/mode/'cells.json')['cells']}
  cell=lambda o:tuple(v//256 for v in o['position'][:2])
  terrain=lambda o:cells[cell(o)]['land']
  water=[f for f in range(board,drop) if terrain(h[f][carrier])==2];beach=[f for f in range(board,drop) if terrain(h[f][carrier])==6]
  assert len(water)>500 and beach and terrain(h[0][cargo])==0 and terrain(h[drop][cargo])==0
  assert cell(h[1100][carrier])==(129,103) and cell(h[end][carrier])==((139,102) if air else (138,102))
  assert cell(h[end][cargo])==((140,104) if air else (139,104)) and h[end][cargo]['mission'][0]==5
  if air:
   assert all(480<=h[f][carrier]['position'][2]<=520 for f in water) and h[drop][carrier]['position'][2]==0
  else:assert all(0<h[f][carrier]['position'][2]<120 for f in water)
  ship_water=[f for f in h if terrain(h[f][ship])==2 and h[f][ship]['position'][2]==0]
  assert len(ship_water)==end+1 and cell(h[1000][ship])==(130,106) and cell(h[end][ship])==((130,96) if air else (130,94))
  assert cells[(139,96)]['land']==6 and cell(h[1200][tele])==cell(h[0][tele]) and cell(h[end][tele])==(138,105) and h[end][tele]['mission'][0]==5
  assert cell(h[end][foot])==(140,100)
  if not air:assert cell(h[end][1023366])==(138,104)
  ship_motion=[f for f in range(1,end+1) if h[f][ship]['position']!=h[f-1][ship]['position']]
  teleports=[dict(frame=f,before=h[f-1][tele]['position'],after=h[f][tele]['position']) for f in range(1,end+1) if cell(h[f][tele])!=cell(h[f-1][tele])]
  assert ship_motion and len(teleports)==1
  output[mode]=dict(board_frame=board,drop_frame=drop,water_frames=len(water),water_range=[water[0],water[-1]],beach_frames=len(beach),landing_cell=list(cell(h[drop][cargo])),landing_land=terrain(h[drop][cargo]),carrier_final_cell=list(cell(h[end][carrier])),cargo_final_cell=list(cell(h[end][cargo])),ship_final_cell=list(cell(h[end][ship])),teleport_final_cell=list(cell(h[end][tele])),teleports=teleports,beach_target_rejected=True,actor_health=expected,ship_motion_frames=len(ship_motion),water_height_range=[min(h[f][carrier]['position'][2] for f in water),max(h[f][carrier]['position'][2] for f in water)])
 # Compare the effects, allowing recorded intermediate time/subcell differences.
 keys=['board_frame','drop_frame','landing_cell','landing_land','carrier_final_cell','cargo_final_cell','ship_final_cell','teleport_final_cell','actor_health']
 assert all(output['original'][k]==output['generated-c'][k] for k in keys)
 rng={m:{r['frame']:r['rng'] for r in rs if r['kind']=='state'} for m,rs in raw.items()}
 differences=[f for f in rng['original'] if rng['original'][f]!=rng['generated-c'][f]]
 result=dict(passed=True,comparison_sha256=sha(p),strict_trace_passed=q['passed'],strict_failure_preserved=not q['passed'],baseline_inherited_exactly=tag!=base,baseline_traces={m:sha(S/'runs'/base/m/'state.jsonl') for m in raw},effect_modes=output,core_functional_goals_equal=True,health_and_transport_state_preserved=True,rng_first_different_frame=differences[0] if differences else None,rng_different_frames=len(differences),scope='Finite natural coast transport, ship travel and a rejected beach target plus one valid land teleport only. Recorded arrival/subcell/scheduling differences accepted for these effects; no RNG reset or comparator change. Current full per-mode trace must equal its pre-change baseline; not full-game equivalence.')
 # JSON object keys are strings; compare the persisted representation on repeated audits.
 result=json.loads(json.dumps(result))
 out=p.parent/'functional-acceptance.json'
 if out.exists():assert read(out)==result
 else:out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys
 x=analyze(sys.argv[1]);print(dict(passed=x['passed'],tag=sys.argv[1],modes=x['effect_modes'],rng_first=x['rng_first_different_frame']))
