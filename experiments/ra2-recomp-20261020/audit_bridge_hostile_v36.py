"""Validate hostile classification, mixed-class traversal and actual final outcomes."""
from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');observer=sha(S/'connection-fixture-probe.exe')
scenes={};totals=Counter()
recipes=read(S/'bridge-hostile-fixtures.json');assert recipes['enemy_native_team_script'] and not recipes['enemy_player_orders']
for item in recipes['fixtures']:
    if item['dynamic']:assert not any(':1023363:' in o for o in item['orders'])
    plain_tag='ep-'+item['name'];observed_tag='eh-'+item['name']
    for tag,digest in [(plain_tag,production),(observed_tag,observer)]:
        x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
        assert x['passed'] and x['exe_sha256']==digest and x['scenario_sha256']==sha(R/item['path'])
        assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
        assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        assert all(r['passed'] and r['exit_code']==0 and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256'] for r in x['runs'])
    native=rows(observed_tag,'original');lifted=rows(observed_tag,'generated-c');assert ordered(native)==ordered(lifted)
    modes={}
    for mode,observed in [('original',native),('generated-c',lifted)]:
        plain=rows(plain_tag,mode);states=[r for r in observed if r['kind']=='state']
        assert states==[r for r in plain if r['kind']=='state']
        assert [r for r in ordered(observed) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(plain)
        first={o['id']:o for o in states[0]['objects']};assert first[1023362]['owner']==0 and first[item['enemy_id']]['owner']==1
        for z in [0,416]:
            layer=[o for o in first.values() if o['position'][0]//256==60 and o['position'][1]//256==66 and o['position'][2]==z]
            assert len(layer)==3 and len({o['class'] for o in layer})==2
        hits=[r for r in observed if r['kind']=='fixture-internal-hit' and r['id'] in item['actor_ids']]
        enemy=[r for r in hits if r['stage']==27 and r['id']==1023362 and r['value'][0]==item['enemy_id']]
        assert enemy,(item['name'],'No actual enemy classifier entry')
        assert all(r['value'][1]==first[item['enemy_id']]['class'] for r in enemy)
        assert any(r['position'][2]==416 for r in enemy)
        mixed=[];group=[];upper=False
        for r in hits:
            if r['id']!=1023362:continue
            if r['stage']==18:
                if upper and group and len({first[v]['class'] for v in group})>1:mixed.append(group)
                group=[];upper=bool(r['value'][0])
            elif r['stage']==22 and r['value'][0] in first:group.append(r['value'][0])
        if upper and group and len({first[v]['class'] for v in group})>1:mixed.append(group)
        assert mixed,item['name']
        motion={}
        for uid in sorted(set(item['actor_ids']+[item['enemy_id']])):
            history=[(s['frame'],next((o for o in s['objects'] if o['id']==uid),None)) for s in states]
            present=[(f,o) for f,o in history if o is not None];assert present
            positions={tuple(o['position']) for _,o in present}
            if uid in item['actor_ids']:assert len(positions)>1,(item['name'],uid)
            final=history[-1][1]
            motion[str(uid)]=dict(distinct_positions=len(positions),last_present_frame=present[-1][0],
                final_position=final['position'] if final else None,final_destination=final['ground_drive']['destination'] if final else None,
                final_health=final['health'] if final else None,absent_at_end=final is None)
        if item['dynamic']:
            pair_hits=[r for r in plain if r['kind']=='movement-audit' and r['stage']==25 and r['id']==1023362 and r['value']==item['enemy_id']]
            assert pair_hits,(item['name'],'No ordinary traffic relationship query')
            positions={s['frame']:{o['id']:o['position'] for o in s['objects']} for s in states}
            assert any(positions[r['frame']].get(1023362,[0,0,0])[2]==416 and positions[r['frame']].get(item['enemy_id'],[0,0,0])[2]==416 for r in pair_hits)
        else:pair_hits=[]
        primary=motion['1023362'];reached=primary['final_position']==[60*256+128,item['goal'][1]*256+128,416] and primary['final_destination']==[0,0,0]
        modes[mode]=dict(enemy_classifier_entries=len(enemy),enemy_samples=enemy[:4],mixed_queries=len(mixed),sample_mixed_visits=mixed[:4],
            hostile_traffic_queries=len(pair_hits),motion=motion,reached_primary_goal=reached)
        if mode=='original':totals.update(enemy_classifier_entries=len(enemy),mixed_queries=len(mixed),hostile_traffic_queries=len(pair_hits),goals_reached=int(reached))
    scenes[item['name']]=dict(passed=True,dynamic=item['dynamic'],frames=901,modes=modes)
value=dict(passed=True,production_scenes=4,production_frames=3604,independent_frames=3604,
    production_executable_sha256=production,observer_executable_sha256=observer,scenes=scenes,totals=dict(totals),
    hostile_classifier_observed=True,hostile_bridge_traffic_observed=True,all_routes_required_to_complete=False,
    scope='Original bridge overlays, accepted lower terrain, ordinary map units and unchanged native house alliances. Normal move orders only. The byte-checked observer relocates one original CALL and preserves CPU/FPU state. Full states, RNG, commands and ordered events match native/C and production. Enemy classifier entries and bridge traffic queries are observed separately from final arrival; original stalls, destruction and diversions are retained.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),S/'bridge-hostile-fixtures.json',R/'make_bridge_hostile_v36.py',R/'extend_bridge_hostile_ai_v36.py',R/'run_bridge_hostile_v36.py',R/'extend_observer_v36.py',R/'make_connection_fixture_v36.py',S/'connection_observer.c']])
out=S/'bridge-hostile-real-scenes.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,frames=3604,totals=dict(totals))))
