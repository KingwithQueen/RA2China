"""Check useful effects and bounded natural-source evidence, without expanding the matrix."""
from run_batch_v39 import R,S,read,write,sha
from collections import Counter
import re
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
def observer_matches(tag,plain):
 x=read(S/'runs'/tag/'comparison.json');b=read(S/'runs'/plain/'comparison.json')
 assert x['passed'] and b['passed'] and x['seed']==b['seed']==12345 and x['scenario_sha256']==b['scenario_sha256']
 assert x['exe_sha256']==sha(S/'connection-fixture-probe.exe')
 for mode in ['original','generated-c']:
  a=rows(tag,mode);c=rows(plain,mode);assert states(a)==states(c) and events(a)==events(c),(tag,mode)
 return x
matrix=read(S/'final-scene-matrix.json');assert matrix['passed'] and len(matrix['results'])==17
production=sha(R/'ra2/build-original-c/ra2.exe')
for value in matrix['results']:
 tag=value['tag'];x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
 assert x['passed'] and x['seed']==12345 and c['frames_compared']==c['equal_frames']==value['frames']
 assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
 assert all(r['passed'] and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
 assert x['exe_sha256']==(sha(S/'connection-fixture-probe.exe') if tag.startswith(('observed-','alias-')) else production)
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='cross-'+name;observer_matches('observed-'+tag,tag)
 rs=rows(tag,'original');h=history(rs);car,foot=item['actor_ids'];main=item['blocker_id'];early=next(u for u in item['blocker_ids'] if u!=main);direction=1 if name=='north' else -1
 assert h[0][car]['class']==8052216 and h[0][foot]['class']==8009024
 queries=[];block_queries=[]
 for r in events(rs):
  if r['kind']!='movement-audit' or r['id']!=car:continue
  f=r['frame']
  if r['stage']==24 and r['value'] in item['blocker_ids']:block_queries.append(f)
  if r['stage'] not in [25,26] or r['value']!=foot or f<=5:continue
  a,b,pa,pb=[h[q][u]['position'] for q,u in [(f,car),(f,foot),(f-1,car),(f-1,foot)]]
  if a[2]==b[2]==416 and direction*(a[1]-pa[1])>0 and direction*(b[1]-pb[1])<0 and abs(a[1]-b[1])<=1024:queries.append(dict(frame=f,stage=r['stage']))
 waits=[];current=[]
 for f in range(150,min(item['release_frames'].values())):
  a=h[f][car]['position'];b=h[f][main]['position']
  if a==h[f-1][car]['position'] and a[2]==416 and max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=768 and all(h[f][u]['position']==h[f-1][u]['position'] for u in item['blocker_ids']):current.append(f)
  else:
   if len(current)>len(waits):waits=current
   current=[]
 if len(current)>len(waits):waits=current
 detour=[f for f in range(150,501) if h[f][car]['position'][2]==416 and h[f][car]['position'][0]//256 not in [60,61] and h[f][car]['position']!=h[f-1][car]['position']]
 cross=next(f for f in range(150,501) if direction*(h[f][car]['position'][1]-(item['blocker_cell'][1]*256+128))>256)
 arrival=next(f for f in range(150,501) if [v//256 for v in h[f][car]['position'][:2]]==item['goals'][str(car)])
 motion=[]
 for u in sorted(item['blocker_ids'],key=lambda u:item['release_frames'][str(u)]):
  order=item['release_frames'][str(u)];actual=next(f for f in range(order,501) if h[f][u]['position']!=h[f-1][u]['position'])
  motion.append(dict(id=u,order_frame=order,first_actual_motion_frame=actual,delay=actual-order))
 simultaneous=[f for f in range(motion[0]['first_actual_motion_frame'],motion[1]['first_actual_motion_frame']) if h[f][car]['position']!=h[f-1][car]['position'] and h[f][early]['position']!=h[f-1][early]['position'] and h[f][car]['position'][2]==h[f][early]['position'][2]==416 and abs(h[f][car]['position'][1]-h[f][early]['position'][1])<=1024 and h[f][car]['position'][0]//256 not in [60,61]]
 goals={str(u):dict(reached=[v//256 for v in h[500][u]['position'][:2]]==item['goals'][str(u)],final_position=h[500][u]['position'],health=h[500][u]['health']) for u in [car,foot]}
 assert queries and {q['stage'] for q in queries}=={25,26} and block_queries and len(waits)>=6 and detour and simultaneous
 assert motion[0]['first_actual_motion_frame']<cross<item['release_frame']<arrival and all(g['reached'] for g in goals.values())
 assert len([r for r in events(rs) if r['kind']=='submit' and r['id']==car and r['mission']==2])==1
 bridges[name]=dict(passed=True,query_samples=queries,blocker_queries=len(block_queries),wait_range=[waits[0],waits[-1]],wait_frames=len(waits),detour_frames=len(detour),near_exit_simultaneous_frames=simultaneous,cross_frame=cross,arrival_frame=arrival,blocker_motion=motion,main_move_submissions=1,goals=goals)
write(S/'bridge-cross-release-effects.json',dict(passed=True,scenes=bridges,ordinary_orders=True,path_chain_or_motion_injection=False,observer_does_not_change_state=True))
seen=set();candidates=[];alias_records=[]
for group in range(6):
 tag='alias-'+str(group);plain='cross-'+('north' if group%2==0 else 'south');observer_matches(tag,plain)
 cmd=read(S/'runs'/tag/'generated-c/command.json');configured={f'{int(cmd[i+1],0):08X}' for i,x in enumerate(cmd) if x=='--probe'}
 counts=Counter(re.findall(r'^\[probe\] sub_([0-9A-F]{8}) from ',(S/'runs'/tag/'generated-c/run.log').read_text(encoding='utf-8',errors='replace'),re.M))
 primary={'004A1000','004A2670','00703040'};assert all(counts[p] for p in primary)
 aliases=configured-primary;seen.update(aliases)
 candidates += [dict(tag=tag,entry=p,records=counts[p]) for p in sorted(aliases) if counts[p]]
 alias_records.append(dict(tag=tag,configured_aliases=sorted(aliases),first_call_counts={p:counts[p] for p in sorted(configured)}))
assert seen=={e['entry'] for e in read(S/'internal-alias-sources.json')['entries'] if e['entry_kind']=='alias'} and len(seen)==29
prior={e['entry'] for e in read(S/'baseline/parent/internal-alias-sources.json')['entries'] if e['entry_kind']=='alias'}
assert prior==seen
write(S/'alias-inventory-context.json',dict(passed=True,parent_aliases=29,current_aliases=29,new_aliases_this_round=[],legacy_new_aliases_field='The source-audit field new_aliases means expansion from the original nine-entry subset, not newly discovered in this batch. All29 were already catalogued in the accepted parent.'))
write(S/'alias-natural-scenes.json',dict(passed=True,aliases=29,scenes=6,frames=3006,records=alias_records,natural_entry_candidates=candidates,nonprimary_natural_entry_proved=bool(candidates),limits='Each candidate was observed in one of six bounded ordinary bridge scenes; three primary positive controls were hit. No forced C-alias calls. Native intra-function edges are not separate C dispatch. Unseen computed targets and unrun scenarios remain open.'))
anomalies=[]
for tag,z in [('curve-up',436),('curve-tall-down',-193)]:
 h=history(rows(tag,'original'));o=h[600][1022581];assert o['position'][2]==z
 anomalies.append(dict(tag=tag,original_final_position=o['position'],candidate_currently_matches=True,must_replicate_bug=False,scope='Retained original anomaly. Future deliberate correction may be accepted against functionality/rules/effects with an explained comparison.'))
rs=rows('repeat-failure','original');fail=[r['frame'] for r in events(rs) if r['kind']=='movement-audit' and r['stage']==6 and not r['value']]
assert fail==list(range(451,1112,60)),fail
for name in ['meeting-north','meeting-south','enemy-traffic-north']:
 h=history(rows(name,'original'));assert len({tuple(x[1023362]['position']) for x in h.values()})>20
write(S/'effects.json',dict(passed=True,bridge_cross_release=True,ordinary_bridge_meeting=True,hostile_traffic=True,controlled_obstructions=['blocked-tube: diagnostic unit ring at170','repeat-failure: diagnostic unit ring at398'],repeated_failure_frames=fail,original_anomalies=anomalies,whole_game_equivalence_verified=False,rule_and_art_files_changed=False))
print(dict(passed=True,bridges=bridges,aliases=29,natural_alias_candidates=candidates,original_anomalies=anomalies),flush=True)
