"""Distinguish legal command execution, motion, actual queries and final arrival."""
from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=lambda tag,mode:[json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
ordered=lambda rs:[r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');observer=sha(S/'connection-fixture-probe.exe');totals=Counter();scenes={}
for item in read(S/'bridge-infantry-fixtures.json')['fixtures']:
    a='ip-'+item['name'];b='ih-'+item['name']
    for tag,digest in [(a,production),(b,observer)]:
        v=read(S/'runs'/tag/'comparison.json');c=v['comparison'];assert v['passed'] and v['exe_sha256']==digest and v['scenario_sha256']==sha(R/item['path'])
        assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901 and c['rng_equal_all_frames']
        assert c['first_difference'] is None and c['command_difference'] is None
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        assert all(x['passed'] and x['exit_code']==0 and x['save_is_private_copy'] and x['save_before_sha256']==x['save_after_sha256'] for x in v['runs'])
    native=rows(b,'original');lifted=rows(b,'generated-c');assert ordered(native)==ordered(lifted)
    modes={}
    for mode,observed in [('original',native),('generated-c',lifted)]:
        plain=rows(a,mode);states=[r for r in observed if r['kind']=='state'];assert states==[r for r in plain if r['kind']=='state']
        assert [r for r in ordered(observed) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(plain)
        first={o['id']:o for o in states[0]['objects']};vehicle=item['vehicle_id'];foot=item['infantry_id']
        assert first[vehicle]['class']==8052216 and first[foot]['class']==8009024
        assert all(first[u]['owner']==0 and first[u]['position'][2]==416 for u in [vehicle,foot])
        history={s['frame']:{o['id']:o for o in s['objects']} for s in states};motion={}
        for u in item['actor_ids']:
            present=[(s['frame'],history[s['frame']][u]) for s in states if u in history[s['frame']]];positions={tuple(o['position']) for _,o in present};assert len(positions)>1,(item['name'],u)
            final=history[states[-1]['frame']].get(u);goal=item['goals'][str(u)]
            reached=bool(final and [x//256 for x in final['position'][:2]]==goal and final['position'][2]==416)
            motion[str(u)]=dict(distinct_positions=len(positions),final_position=final['position'] if final else None,final_mission=final['mission'] if final else None,final_health=final['health'] if final else None,reached_goal_cell=reached,absent_at_end=final is None)
        pair=[r for r in plain if r['kind']=='movement-audit' and r['stage'] in [24,25] and ((r['id']==vehicle and r['value']==foot) or (r['id']==foot and r['value']==vehicle))]
        upper=[r for r in pair if all(history[r['frame']].get(u,{}).get('position',[0,0,0])[2]==416 for u in [vehicle,foot])]
        moving_queries=[]
        for r in upper:
            f=r['frame']
            if f and all(u in history.get(f-1,{}) and history[f][u]['position']!=history[f-1][u]['position'] for u in [vehicle,foot]):moving_queries.append(r)
        modes[mode]=dict(same_frame_both_moving_queries=len(moving_queries),sample_both_moving_queries=moving_queries[:6],motion=motion,cross_class_queries=len(pair),simultaneous_upper_queries=len(upper),sample_queries=upper[:6])
        if mode=='original':totals.update(same_frame_both_moving_queries=len(moving_queries),cross_class_queries=len(pair),simultaneous_upper_queries=len(upper),vehicle_goals=int(motion[str(vehicle)]['reached_goal_cell']),infantry_goals=int(motion[str(foot)]['reached_goal_cell']))
    scenes[item['name']]=dict(passed=True,meeting=item['meeting'],frames=901,modes=modes)
assert totals['simultaneous_upper_queries']>0,'No actual upper-bridge moving infantry/vehicle query'
assert all(scenes[n]['modes']['original']['simultaneous_upper_queries']>0 for n in ['meeting-north','meeting-south'])
assert totals['same_frame_both_moving_queries']>0
assert scenes['meeting-south']['modes']['original']['same_frame_both_moving_queries']>0
value=dict(north_meeting_dynamic_query_observed=bool(scenes['meeting-north']['modes']['original']['same_frame_both_moving_queries']),passed=True,production_scenes=4,production_frames=3604,independent_frames=3604,production_executable_sha256=production,observer_executable_sha256=observer,scenes=scenes,totals=dict(totals),
    ordinary_legal_player_orders=True,raw_movement_state_writes=False,bridge_moving_infantry_vehicle_query_verified=True,
    scope='Ordinary map objects and normal player-owned moves on the original bridge overlay. Motion, queries with both actors on deck, queries where both positions change that frame, and final goal cells are separately reported. North meeting only queries the pair in its initial frame6 scan before motion; south meeting and following supply actual simultaneous motion queries. No assumption that a query guarantees arrival or that all routes complete.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),R/'make_bridge_infantry_v33.py',R/'run_bridge_infantry_v33.py',R/'extend_observer_v33.py',S/'bridge-infantry-fixtures.json',S/'connection_observer.c']])
out=S/'bridge-infantry-real-scenes.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(dict(passed=True,frames=3604,totals=dict(totals)))
