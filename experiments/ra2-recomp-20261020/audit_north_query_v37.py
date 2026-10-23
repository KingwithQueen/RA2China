"""Require relationship queries during real opposite motion, not the initial path scan."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=lambda t,m:[json.loads(l) for l in (S/'runs'/t/m/'state.jsonl').open(encoding='utf-8')]
ordered=lambda rs:[r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');observer=sha(S/'connection-fixture-probe.exe');scenes={}
for item in read(S/'north-query-fixtures.json')['fixtures']:
    pt='np-'+item['name'];ot='nh-'+item['name']
    for tag,digest in [(pt,production),(ot,observer)]:
        v=read(S/'runs'/tag/'comparison.json');c=v['comparison'];assert v['passed'] and v['exe_sha256']==digest and v['scenario_sha256']==sha(R/item['path'])
        assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901 and c['rng_equal_all_frames']
        assert c['first_difference'] is None and c['command_difference'] is None and c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        assert all(x['passed'] and x['exit_code']==0 and x['save_is_private_copy'] and x['save_before_sha256']==x['save_after_sha256'] for x in v['runs'])
    native=rows(ot,'original');lifted=rows(ot,'generated-c');assert ordered(native)==ordered(lifted);modes={}
    for mode,observed in [('original',native),('generated-c',lifted)]:
        plain=rows(pt,mode);states=[r for r in observed if r['kind']=='state'];assert states==[r for r in plain if r['kind']=='state']
        assert [r for r in ordered(observed) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(plain)
        history={r['frame']:{o['id']:o for o in r['objects']} for r in states};first=history[0]
        assert first[1023362]['class']==8052216 and first[1023367]['class']==8009024
        assert all(first[u]['owner']==0 and first[u]['position'][2]==416 for u in item['actor_ids'])
        qualified=[]
        for r in plain:
            if r['kind']!='movement-audit' or r['stage'] not in [25,26] or r['id']!=1023362 or r['value']!=1023367 or r['frame']<=item['query_after_frame']:continue
            f=r['frame']
            if not all(u in history.get(f,{}) and u in history.get(f-1,{}) for u in item['actor_ids']):continue
            a,b=history[f][1023362]['position'],history[f][1023367]['position'];pa,pb=history[f-1][1023362]['position'],history[f-1][1023367]['position']
            if a[2]==b[2]==416 and a[1]>pa[1] and b[1]<pb[1] and abs(a[1]-b[1])<=1024:
                qualified.append(dict(frame=f,stage=r['stage'],vehicle=a,infantry=b,vehicle_previous=pa,infantry_previous=pb))
        relation=[r for r in qualified if r['stage']==25];geometry=[r for r in qualified if r['stage']==26];assert relation and geometry,(item['name'],mode)
        motion={}
        for u in item['actor_ids']:
            present=[h[u] for h in history.values() if u in h];assert len({tuple(o['position']) for o in present})>1
            final=history[900].get(u);goal=item['goals'][str(u)]
            motion[str(u)]=dict(final_position=final['position'] if final else None,final_mission=final['mission'] if final else None,final_health=final['health'] if final else None,reached_goal_cell=bool(final and [x//256 for x in final['position'][:2]]==goal and final['position'][2]==416))
        modes[mode]=dict(relationship_queries=len(relation),geometry_queries=len(geometry),samples=qualified[:8],motion=motion)
    assert modes['original']==modes['generated-c'];scenes[item['name']]=dict(passed=True,frames=901,query_after_frame=item['query_after_frame'],modes=modes)
value=dict(passed=True,production_scenes=len(scenes),production_frames=len(scenes)*901,independent_frames=len(scenes)*901,production_executable_sha256=production,observer_executable_sha256=observer,scenes=scenes,
    north_meeting_dynamic_relation_query_verified=True,opposite_motion_on_same_frame_verified=True,initial_scan_not_counted=True,raw_state_writes=False,
    scope='Player-owned E2 and vehicle receive ordinary opposing moves from ordinary map placement and headings. Count only pair queries after initial orders while vehicle Y increases and infantry Y decreases in the same recorded frame, both at deck416 and within four cells. Full schema12 states, RNG, commands and ordered events match original/C and production/observer. Arrival and query coverage are separate.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),S/'north-query-fixtures.json',R/'make_bridge_north_query_v37.py',R/'trial_north_query_v37.py',R/'run_north_query_v37.py']])
out=S/'north-query-real-scenes.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print({n:v['modes']['original'] for n,v in scenes.items()})
