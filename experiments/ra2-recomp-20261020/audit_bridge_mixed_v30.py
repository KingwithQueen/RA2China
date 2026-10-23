"""Require actual mixed-class visits, bridge traffic interaction and exact observer parity."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
production=sha(R/'ra2/build-original-c/ra2.exe');observer=sha(S/'connection-fixture-probe.exe')
scenes={};aliases=set();totals=Counter()
for item in read(S/'bridge-mixed-fixtures.json')['fixtures']:
    plain_tag='mp-'+item['name'];observed_tag='mh-'+item['name']
    for tag,digest in [(plain_tag,production),(observed_tag,observer)]:
        report=read(S/'runs'/tag/'comparison.json');c=report['comparison']
        assert report['passed'] and report['exe_sha256']==digest and report['scenario_sha256']==sha(R/item['path'])
        assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
        assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        assert all(r['passed'] and r['exit_code']==0 and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256'] for r in report['runs'])
    originals=rows(observed_tag,'original');generated=rows(observed_tag,'generated-c');assert ordered(originals)==ordered(generated)
    modes={}
    for mode,observed in [('original',originals),('generated-c',generated)]:
        plain=rows(plain_tag,mode);states=[r for r in observed if r['kind']=='state']
        assert states==[r for r in plain if r['kind']=='state']
        assert [r for r in ordered(observed) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(plain)
        first=states[0]['objects'];classes={o['id']:o['class'] for o in first}
        cooccupied=[o for o in first if o['position'][0]//256==60 and o['position'][1]//256==66]
        for z in [0,416]:
            layer=[o for o in cooccupied if o['position'][2]==z]
            assert len(layer)==3 and len({o['class'] for o in layer})==2,(item['name'],z,layer)
        motion={}
        for uid in item['actor_ids']:
            actor=[next(o for o in r['objects'] if o['id']==uid) for r in states]
            assert len({tuple(o['position']) for o in actor})>1,(item['name'],uid)
            motion[str(uid)]=dict(distinct_positions=len({tuple(o['position']) for o in actor}),upper_frames=sum(bool(o['ground_drive']['owner_flags_74_79'][1]) for o in actor),
                final_position=actor[-1]['position'],final_destination=actor[-1]['ground_drive']['destination'])
        full=[];mixed_visits=[]
        for uid in item['actor_ids']:
            hits=[r for r in observed if r['kind']=='fixture-internal-hit' and r['id']==uid]
            groups=[];current=None
            for hit in hits:
                if hit['stage']==18:
                    if current:groups.append(current)
                    current=dict(frame=hit['frame'],upper=bool(hit['value'][0]),head=hit['value'][1],visits=[])
                elif current and hit['stage']==23:current['lengths']=hit['value']
                elif current and hit['stage']==22:current['visits'].append(hit['value'])
            if current:groups.append(current)
            for g in groups:
                visits=g['visits'];ids=[v[0] for v in visits]
                if not g['upper'] or len({classes.get(i) for i in ids})<2:continue
                assert all(i in classes for i in ids)
                mixed_visits.append(g)
                if ids and ids[0]==g['head'] and len(ids)==g['lengths'][1] and [v[1] for v in visits]==ids[1:]+[0]:full.append(g)
        assert mixed_visits,item['name']
        if not item['dynamic']:assert full,item['name']
        interactions=[r for r in plain if r['kind']=='movement-audit' and r['stage'] in [24,25,26]
            and r['id'] in item['actor_ids'] and r['value'] in item['actor_ids'] and r['id']!=r['value']]
        moving=[r for r in interactions if r['stage']==25];geometry=[r for r in interactions if r['stage']==26]
        if item['dynamic']:
            assert moving and geometry,(item['name'],'No actual opposing moving traffic classification')
            samples={r['frame']:r for r in states}
            assert any(next(o for o in samples[r['frame']]['objects'] if o['id']==r['id'])['position'][2]==416 for r in moving)
        modes[mode]=dict(full_upper_mixed_chains=len(full),mixed_upper_queries=len(mixed_visits),sample_full_chains=full[:3],
            motion=motion,moving_interactions=len(moving),geometry_interactions=len(geometry),sample_interactions=interactions[:6],
            reached_primary_goal=motion[str(item['actor_ids'][0])]['final_position']==[item['goal'][0]*256+128,item['goal'][1]*256+128,416]
                and motion[str(item['actor_ids'][0])]['final_destination']==[0,0,0])
        if mode=='original':totals.update(full_mixed_chains=len(full),mixed_queries=len(mixed_visits),moving_interactions=len(moving),geometry_interactions=len(geometry))
    command=read(S/'runs'/observed_tag/'generated-c/command.json')
    configured={f'{int(command[i+1],0):08X}' for i,x in enumerate(command) if x=='--probe'}
    text=(S/'runs'/observed_tag/'generated-c/run.log').read_text(encoding='utf-8',errors='replace')
    hits=Counter(re.findall(r'^\[probe\] sub_([0-9A-F]{8}) from ',text,re.M));assert hits['00703040']>0
    examined=configured-{'004A1000','004A2670','00703040'};aliases.update(examined)
    assert all(hits[a]==0 for a in examined)
    scenes[item['name']]=dict(passed=True,dynamic=item['dynamic'],frames=901,modes=modes,configured_aliases=sorted(examined))
assert len(aliases)==9
value=dict(passed=True,production_scenes=4,production_frames=3604,independent_frames=3604,production_executable_sha256=production,
    observer_executable_sha256=observer,scenes=scenes,totals=dict(totals),mixed_runtime_classes_verified=True,opposing_bridge_traffic_verified=True,
    nonprimary_natural_entry_proved=False,scope='Normal map loading places infantry and vehicles on both real bridge layers. Three ordinary move orders create opposing traffic. No raw motion, chain, bridge-layer, path or budget writes. Complete states and ordered events match native/C and uninstrumented production. Alias absence is limited to these configured first-call probes.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),R/'make_bridge_mixed_v30.py',R/'run_bridge_mixed_v30.py',R/'extend_observer_v30.py',R/'run_connection_v30.py',S/'connection_observer.c']])
out=S/'bridge-mixed-real-scenes.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,frames=3604,totals=dict(totals))))
