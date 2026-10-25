"""Separate command admission, occupied-target normalization, completion and active waiting."""
from run_batch_v68 import *
from collections import defaultdict
def records(tag,mode='original'):
    with (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8') as f:
        for line in f:yield json.loads(line)
def facts(tag,ids):
    last={};first={};arrival={};motion=defaultdict(int);previous={};area=None;transitions=defaultdict(list);old_goal={};events=[];states={};observations={}
    for j in records(tag):
        if j['kind']=='fixture-map-area':area=j
        elif j['kind']=='fixture-move-boundary' and j['id'] in ids:
            i=j['id'];key=tuple(j['destination'])
            if old_goal.get(i)!=key:transitions[i].append(j);old_goal[i]=key
            if j['frame'] in [6,999,1001,1199,1201]:observations[(j['frame'],i)]=j
        elif j['kind']=='movement-audit' and j.get('id') in ids and j['stage']==6:events.append(j)
        elif j['kind']=='state':
            if j['frame'] in [6,999,1001,1199,1201,2400]:states[j['frame']]=j
            for a in j['objects']:
                i=a['id']
                if i not in ids:continue
                first.setdefault(i,a);last[i]=a
                if previous.get(i)!=a['position'] and i in previous:motion[i]+=1
                previous[i]=a['position']
    return dict(last=last,first=first,motion=motion,area=area,transitions=transitions,events=events,states=states,observations=observations)
def map_inside(a,p,level,slope):
    w=a['width'];x,y,lw,lh=a['local'];cx,cy=p;total=cx+cy
    if slope and total<w+2*y+4+level:level+=1
    return total>w+2*y+level and total<=w+2*(y+lh)+2+level and cx-cy<2*(x+lw)-w and cy-cx<w-2*x
recipes={x['tag']:x for x in read(S/'scene-recipes.json')['fixtures']}
contract=read(S/'baseline-contract.json');parity=[]
for x in contract['contracts']:
    for mode,row in x['rows'].items():
        p=S/'runs'/('f-'+x['tag'])/mode/'state.jsonl';assert sha(p)==row['sha256'],(x['tag'],mode)
        parity.append(dict(tag=x['tag'],mode=mode,baseline=row['sha256'],final=sha(p)))
# The independent recorder must not change any production record.
for label in ['b','f']:
    for mode in ['original','generated-c']:
        source=S/'runs'/(label+'-rq-prod')/mode/'state.jsonl'
        extra_kinds={'fixture-bridge-state','fixture-object-flags','fixture-map-area','fixture-move-boundary'}
        h=hashlib.sha256()
        for l in (S/'runs'/(label+'-rq-valid')/mode/'state.jsonl').open('rb'):
            if json.loads(l)['kind'] not in extra_kinds:h.update(l)
        assert h.hexdigest()==sha(source),(label,mode)
        parity.append(dict(production_parity=label,mode=mode,production_sha256=sha(source)))
write(S/'record-parity.json',dict(passed=True,checks=parity,whole_per_mode_baseline_unchanged=True,production_record_comparator_unchanged=True))
rejected=[];original_boundary=facts('f-rq-boundary',recipes['rq-boundary']['actor_ids'])
valid=recipes['rq-valid'];valid_facts=facts('f-rq-valid',valid['actor_ids']);area=valid_facts['area']
for i,goal in read(S/'scene-recipes-pending.json')['corrections'].items():
    i=int(i);old=recipes['rq-boundary']['goals'][str(i)];f=original_boundary['last'][i]
    assert old[1]-old[0]>=area['width']-2*area['local'][0]
    assert original_boundary['motion'][i]==0 and f['ground_drive']['destination']==[0,0,0]
    new=valid_facts['last'][i];assert [v//256 for v in new['position'][:2]]==goal and valid_facts['motion'][i]>0
    rejected.append(dict(id=i,rejected_goal=old,left_diagonal=old[1]-old[0],strict_left_limit=area['width']-2*area['local'][0],corrected_goal=goal,new_final=new['position'],original_stationary_frames=5401,explanation='Outside usable local map area; no admitted path waiting to be scheduled.'))
arrivals={};request_frames={int(i):f for i,f in valid['request_frames'].items()};goals={int(i):g for i,g in valid['goals'].items()}
for j in records('f-rq-valid'):
    if j['kind']!='state':continue
    for a in j['objects']:
        i=a['id']
        if i in request_frames and j['frame']>=request_frames[i] and [v//256 for v in a['position'][:2]]==goals[i]:arrivals.setdefault(i,j['frame'])
assert set(arrivals)==set(request_frames)
for i in request_frames:
    a=valid_facts['last'][i];assert a['health']==200 and a['mission']==[5,-1,-1]
    assert [v//256 for v in a['position'][:2]]==goals[i] and a['ground_drive']['destination']==[0,0,0]
queue=[dict(id=i,request=request_frames[i],arrival=arrivals[i],wait=arrivals[i]-request_frames[i]) for i in sorted(request_frames)]
write(S/'reachability-fairness.json',dict(passed=True,rejected_out_of_area=rejected,valid_requests=12,exact_arrivals=12,healthy=12,per_request=queue,last_request=max(request_frames.values()),last_arrival=max(arrivals.values()),maximum_request_to_arrival=max(v['wait'] for v in queue),fifo_required=False,unbounded_starvation_freedom_proved=False,scope='Finite admitted queue, unchanged release/request times, all twelve requests finish. Invalid goals are admission failures; normalized or completed missions are not active starvation. No policy or scheduling algorithm was invented without evidence of failure.'))
ids=[1023319,1023320,1023321];mixed=facts('f-bm-stop',ids);zero=facts('f-bm-zero',ids);stops=[]
for i in ids:
    rows=mixed['transitions'][i];normalized=[x for x in rows if x['destination']!=[0,0,0] and x['navigation'][0] and x['navigation'][1:]!=x['requested']]
    assert normalized and normalized[0]['goal_cell'][2]&0x20
    assert mixed['last'][i]['position']==zero['last'][i]['position']
    assert mixed['last'][i]['health']==200
    failures=[e for e in mixed['events'] if not e['value'] and not e.get('caller_goal_valid',True)]
    failures=[e for e in failures if e['id']==i]
    stops.append(dict(id=i,normalization=normalized[0],destination_changes=rows,final=mixed['last'][i]['position'],zero_close_final=zero['last'][i]['position'],failed_search_cleared_goal=failures,interpretation='Occupied requested cell was changed to a nearby destination; later navigation cleared on failed rebuild.' if i==1023321 else 'Occupied requested cell was changed to a nearby destination and that destination was reached.'))
assert stops[2]['failed_search_cleared_goal']
assert mixed['area']['close_enough']==576 and zero['area']['close_enough']==0
controls=[]
for tag in ['stop-free','stop-occupied']:
    x=recipes[tag];i=x['actor_ids'][0];d=facts('f-'+tag,[i]);assert [v//256 for v in d['last'][i]['position'][:2]]==[57,76]
    row=dict(tag=tag,id=i,final=d['last'][i]['position'],goal_changes=d['transitions'][i])
    if tag=='stop-occupied':
        before=next(a for a in d['states'][999]['objects'] if a['id']==i);after=next(a for a in d['states'][1199]['objects'] if a['id']==i)
        assert before['position']==after['position'] and before['ground_drive']['destination']==[0,0,0]
        assert d['observations'][6,i]['goal_cell'][2]&0x20
        assert d['observations'][1201,i]['destination']!=[0,0,0]
        row.update(completed_before_release=True,reissue_frame=1200,release_frame=1000,automatic_resurrection_of_completed_order_required=False)
    controls.append(row)
write(S/'occupation-stop-rules.json',dict(passed=True,mixed_requests=stops,controls=controls,close_enough_counterfactual_did_not_change_these_three_outcomes=True,no_claim_all_near_stops_are_close_enough=True,strict_distance_and_height_native_probes='final-native.json',scope='Read-only occupancy/navigation evidence, normal empty/occupied/released target controls, explicit zero-rule counterfactual and original native stop probes. Preserve stop/normalization semantics; no automatic rescheduling of already completed orders.'))
print(dict(passed=True,raw_parity_checks=len(parity),outside_goals_explained=4,valid_queue_exact=12,near_stops_explained=3,controls=2))
