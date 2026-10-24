"""Require real crossing queries, an occupied exit wait, and ordinary release motion."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=lambda t,m:[json.loads(l) for l in (S/'runs'/t/m/'state.jsonl').open(encoding='utf-8')]
ordered=lambda rs:[r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');observer=sha(S/'connection-fixture-probe.exe');scenes={}
for item in read(S/'bridge-neighbor-release-fixtures.json')['fixtures']:
    pt='nr-'+item['name'];ot='nh-'+item['name']
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
        value=dict(relationship_queries=relation,geometry_queries=geometry,query_samples=queries[:8],blocker_queries=len(block_queries),blocker_query_frames=block_queries[:12],longest_near_exit_wait_frames=len(longest),wait_range=[longest[0],longest[-1]] if longest else None,blocker_departed=all(any(h[f][u]['position']!=h[item['release_frames'][str(u)]-1][u]['position'] for f in range(item['release_frames'][str(u)]+1,901)) for u in item['blocker_ids']),vehicle_moved_after_release=moved_after_release,normal_move_reissued_frame=item['reissue_frame'],motion=motion)
        first_release=min(item['release_frames'].values());held=bool(longest) and all(h[f][u]['position']==h[longest[0]][u]['position'] for u in item['blocker_ids'] for f in range(longest[0],first_release))
        detour=[f for f in range(150,release) if h[f][car]['position'][2]==416 and h[f][car]['position'][0]//256 not in [60,61] and h[f][car]['position']!=h[f-1][car]['position']]
        direction=1 if item['name']=='north' else -1;exit_y=item['blocker_cell'][1]*256+128
        crossed=next((f for f in range(150,901) if direction*(h[f][car]['position'][1]-exit_y)>256),None)
        arrival=next((f for f in range(150,release) if [v//256 for v in h[f][car]['position'][:2]]==item['goals'][str(car)]),None)
        early,late=sorted(item['blocker_ids'],key=lambda u:item['release_frames'][str(u)]);dynamic=[]
        for f in range(first_release+1,release):
            moving_car=h[f][car]['position']!=h[f-1][car]['position']
            early_moving=h[f][early]['position']!=h[f-1][early]['position']
            late_still=h[f][late]['position']==h[first_release-1][late]['position']
            if moving_car and early_moving and late_still:dynamic.append(f)
        main_orders=[q for q in plain if q['kind']=='submit' and q['id']==car and q['mission']==2]
        assert len(main_orders)==1 and main_orders[0]['frame']==5
        assert all(any(q['kind']=='submit' and q['id']==int(u) and q['frame']==f for q in plain) for u,f in item['release_frames'].items())
        value.update(first_release_frame=first_release,second_release_frame=release,partial_clearance_dynamic_frames=dynamic[:12],partial_clearance_dynamic_frame_count=len(dynamic),main_move_submissions=len(main_orders))
        value.update(blockers_stood_until_first_release=held,detour_frames=detour[:12],detour_frame_count=len(detour),crossed_exit_frame=crossed,crossed_before_full_clear=bool(crossed and crossed<release),arrived_before_release_frame=arrival,main_move_reissued=False)
        value['first_motion_after_wait_before_release']=resumed_before_release
        print(item['name'],mode,value,flush=True)
        assert relation and geometry and block_queries and len(longest)>=6 and held and detour and crossed and resumed_before_release and value['blocker_departed'] and dynamic,(item['name'],value)
        modes[mode]=value
    assert modes['original']==modes['generated-c'];scenes[item['name']]=dict(passed=True,frames=901,release_frame=release,modes=modes)
v=dict(passed=True,production_scenes=2,production_frames=1802,independent_frames=1802,production_executable_sha256=production,observer_executable_sha256=observer,scenes=scenes,ordinary_map_and_orders=True,raw_state_writes=False,scope='Opposing E2/vehicle queries on deck416, near-exit wait, detour, ordinary adjacent-lane departure while the main-lane blocker remains held. Main car and first blocker must both move while the second blocker still holds its position. Only one main move is submitted; no path, chain, motion or bridge state is written. Arrival is reported separately.',inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),R/'make_bridge_neighbor_release_v38.py',R/'run_bridge_neighbor_release_v38.py',S/'bridge-neighbor-release-fixtures.json']])
out=S/'bridge-neighbor-release-real-scenes.json';assert not out.exists();out.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
