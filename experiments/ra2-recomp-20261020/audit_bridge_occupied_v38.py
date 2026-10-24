"""Require real crossing queries, an occupied exit wait, and ordinary release motion."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=lambda t,m:[json.loads(l) for l in (S/'runs'/t/m/'state.jsonl').open(encoding='utf-8')]
ordered=lambda rs:[r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');observer=sha(S/'connection-fixture-probe.exe');scenes={}
for item in read(S/'bridge-occupied-fixtures.json')['fixtures']:
    pt='op-'+item['name'];ot='oh-'+item['name']
    for tag,digest in [(pt,production),(ot,observer)]:
        v=read(S/'runs'/tag/'comparison.json');c=v['comparison'];assert v['passed'] and v['exe_sha256']==digest and v['scenario_sha256']==sha(R/item['path'])
        assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901 and c['rng_equal_all_frames']
        assert c['first_difference'] is None and c['command_difference'] is None and c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        assert all(x['passed'] and x['exit_code']==0 and x['save_is_private_copy'] and x['save_before_sha256']==x['save_after_sha256'] for x in v['runs'])
    native=rows(ot,'original');lifted=rows(ot,'generated-c');assert ordered(native)==ordered(lifted);modes={}
    for mode,obs in [('original',native),('generated-c',lifted)]:
        plain=rows(pt,mode);states=[r for r in obs if r['kind']=='state'];assert states==[r for r in plain if r['kind']=='state']
        assert [r for r in ordered(obs) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(plain)
        h={r['frame']:{o['id']:o for o in r['objects']} for r in states};car,foot=item['actor_ids'];block=item['blocker_id'];release=item['release_frame']
        assert h[0][car]['class']==8052216 and h[0][foot]['class']==8009024
        assert all(h[0][u]['owner']==0 and h[0][u]['position'][2]==416 for u in [car,foot]+item['blocker_ids']),(item['name'],'initial layer')
        queries=[];block_queries=[]
        for r in plain:
            if r['kind']!='movement-audit' or r['id']!=car:continue
            f=r['frame']
            if r['stage']==24 and r['value'] in item['blocker_ids'] and 50<f<release:block_queries.append(f)
            if r['stage'] not in [25,26] or r['value']!=foot or f<=5:continue
            a,b,pa,pb=[h[q][u]['position'] for q,u in [(f,car),(f,foot),(f-1,car),(f-1,foot)]]
            direction=1 if item['name']=='north' else -1
            if a[2]==b[2]==416 and direction*(a[1]-pa[1])>0 and direction*(b[1]-pb[1])<0 and abs(a[1]-b[1])<=1024:queries.append(dict(frame=f,stage=r['stage'],vehicle=a,infantry=b,vehicle_previous=pa,infantry_previous=pb))
        longest=[];current=[]
        for f in range(150,release):
            a,pa,b=h[f][car]['position'],h[f-1][car]['position'],h[f][block]['position']
            stopped=all(h[f][u]['position']==h[f-1][u]['position'] and h[f][u]['position'][2]==416 for u in item['blocker_ids'])
            if a==pa and stopped and a[2]==b[2]==416 and [v//256 for v in a[:2]]!=item['goals'][str(car)] and max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=768:current.append(f)
            else:
                if len(current)>len(longest):longest=current
                current=[]
        if len(current)>len(longest):longest=current
        resumed_before_release=next((f for f in range(longest[-1]+1,release) if h[f][car]['position']!=h[longest[-1]][car]['position']),None) if longest else None
        motion={str(u):dict(final_position=h[900][u]['position'],health=h[900][u]['health'],reached_goal_cell=[v//256 for v in h[900][u]['position'][:2]]==item['goals'][str(u)]) for u in [car,foot]}
        relation=sum(q['stage']==25 for q in queries);geometry=sum(q['stage']==26 for q in queries)
        moved_after_release=any(h[f][car]['position']!=h[release-1][car]['position'] for f in range(release+1,901))
        value=dict(relationship_queries=relation,geometry_queries=geometry,query_samples=queries[:8],blocker_queries=len(block_queries),blocker_query_frames=block_queries[:12],longest_near_exit_wait_frames=len(longest),wait_range=[longest[0],longest[-1]] if longest else None,blocker_departed=all(any(h[f][u]['position']!=h[release-1][u]['position'] for f in range(release+1,901)) for u in item['blocker_ids']),vehicle_moved_after_release=moved_after_release,normal_move_reissued_frame=item['reissue_frame'],motion=motion)
        value['first_motion_after_wait_before_release']=resumed_before_release
        print(item['name'],mode,value,flush=True)
        assert relation and geometry and block_queries and len(longest)>=6 and value['blocker_departed'] and moved_after_release,(item['name'],value)
        modes[mode]=value
    assert modes['original']==modes['generated-c'];scenes[item['name']]=dict(passed=True,frames=901,release_frame=release,modes=modes)
v=dict(passed=True,production_scenes=2,production_frames=1802,independent_frames=1802,production_executable_sha256=production,observer_executable_sha256=observer,scenes=scenes,ordinary_map_and_orders=True,raw_state_writes=False,scope='Opposing E2/vehicle queries while both move on deck416. Two ordinary vehicles move to occupy the exit, are queried after initial scans, and stand still during a near-exit wait before arrival. Ordinary frame300 departure and a frame320 repeated player move precede subsequent vehicle motion. This is not an automatic-resumption claim. Arrival is reported separately.',inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),R/'make_bridge_occupied_v38.py',R/'run_bridge_occupied_v38.py',S/'bridge-occupied-fixtures.json']])
out=S/'bridge-occupied-real-scenes.json';assert not out.exists();out.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
