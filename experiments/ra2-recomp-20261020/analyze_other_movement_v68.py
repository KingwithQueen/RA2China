"""Natural locomotor effects, retained pre-existing ship precision variation, and recorder parity."""
from run_batch_v68 import *
from collections import Counter,defaultdict
from difflib import SequenceMatcher
def data(tag,mode):
    with (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8') as f:
        for line in f:yield json.loads(line)
def states(tag,mode):return (x for x in data(tag,mode) if x['kind']=='state')
x=read(S/'other-movement-ground-recipe.json');actors={c['id']:c for c in x['checks']};cases=[];differences=[];maximum=0;differing_frames=set();path_counts=Counter();observed={};motion=Counter();previous={};last={}
for mode in ['original','generated-c']:
    b=S/'runs/b-gtypes'/mode/'state.jsonl';f=S/'runs/f-gtypes'/mode/'state.jsonl'
    assert sha(b)==sha(f),(mode,'New source changed existing locomotor behavior')
    extra={'fixture-bridge-state','fixture-object-flags','fixture-map-area','fixture-move-boundary','fixture-other-locomotor'};h=hashlib.sha256()
    for l in (S/'runs/f-gtypes-obs'/mode/'state.jsonl').open('rb'):
        j=json.loads(l)
        if j['kind'] not in extra:h.update(l)
        if j['kind']=='fixture-other-locomotor' and j['id'] in actors:
            key=(mode,j['id']);observed.setdefault(key,j)
    assert h.hexdigest()==sha(f),mode
    cases.append(dict(mode=mode,baseline_sha256=sha(b),final_sha256=sha(f),observer_production_records_equal=True))
for left,right in zip(states('f-gtypes','original'),states('f-gtypes','generated-c')):
    assert left.keys()==right.keys();lo={a['id']:a for a in left['objects']};ro={a['id']:a for a in right['objects']};assert lo.keys()==ro.keys()
    for key in left:
        if key!='objects':assert left[key]==right[key],(left['frame'],key)
    for i,a in lo.items():
        b=ro[i]
        if i in actors:
            if i in previous and previous[i]!=a['position']:motion[i]+=1
            previous[i]=a['position'];last[i]=a
        assert a.keys()==b.keys()
        for key in a:
            if a[key]==b[key]:continue
            assert i==next(c['id'] for c in x['checks'] if c['type']=='DEST') and key=='position',(left['frame'],i,key)
            assert a['position'][2]==b['position'][2]
            delta=max(abs(q-w) for q,w in zip(a[key],b[key]));maximum=max(maximum,delta);differing_frames.add(left['frame']);path_counts[key]+=1
            if len(differences)<8:differences.append(dict(frame=left['frame'],id=i,original=a[key],generated_c=b[key]))
assert len(differing_frames)==32
# Bound measured effects, not arbitrary internal values. This inherited C path has no current edit.
assert maximum<=4
outcomes=[]
for i,c in actors.items():
    a=last[i];ob=observed['original',i];cb=observed['generated-c',i]
    assert ob['type']==cb['type']==c['type'],(c,ob,cb)
    assert ob['locomotor']==cb['locomotor'] and ob['locomotor']
    assert a['health']>0 and [p//256 for p in a['position'][:2]]==c['goal'] and motion[i]>0
    outcomes.append(dict(type=c['type'],id=i,locomotor_vtable=ob['locomotor'],goal=c['goal'],final=a['position'],health=a['health'],mission=a['mission'],moving_frames=motion[i],initial=c['start']))
assert len({a['locomotor_vtable'] for a in outcomes})==6
commands={}
for mode in ['original','generated-c']:
    commands[mode]=[r for r in data('f-gtypes',mode) if r['kind'] in ['submit','execute']]
assert commands['original']==commands['generated-c'] and len(commands['original'])==12
audits={m:[json.dumps(r,sort_keys=True) for r in data('f-gtypes',m) if r['kind']=='movement-audit'] for m in ['original','generated-c']};hunks=[]
for op,a,b,c,d in SequenceMatcher(None,audits['original'],audits['generated-c'],autojunk=False).get_opcodes():
    if op!='equal':hunks.append(dict(operation=op,original=[json.loads(z) for z in audits['original'][a:b]],generated_c=[json.loads(z) for z in audits['generated-c'][c:d]]))
ship=next(c['id'] for c in x['checks'] if c['type']=='DEST')
assert all(r['id']==ship and r['stage'] in [24,25,26,27] for h in hunks for r in h['original']+h['generated_c'])
def without_frame(rows):
    return Counter(json.dumps({k:v for k,v in json.loads(t).items() if k!='frame'},sort_keys=True) for t in rows)
oc=without_frame(audits['original']);cc=without_frame(audits['generated-c'])
assert not oc-cc and sum((cc-oc).values())==1
# Every ordered query difference is bound to the frozen pre-edit pair, not a relaxed comparator.
review=read(S/'other-movement-checker-review.json')
assert sha(S/'analyze-other-initial.py')==review['initial_checker_sha256']
assert [dict(operation=h['op'],original=h['original'],generated_c=h['generated_c']) for h in review['actual_hunks']]==hunks
write(S/'other-movement-acceptance.json',dict(passed=True,functional_acceptance=True,strict_original_c_equality=False,types=outcomes,per_mode_before_after_and_observer_parity=cases,rng_equal_all_frames=True,ordinary_commands_equal=True,preexisting_ship_variation=dict(differing_frames=len(differing_frames),maximum_world_unit_delta=maximum,cell_size=256,examples=differences,audit_hunks=hunks,current_generated_ship_source_changed=False),initial_invalid_infantry_layout_excluded=True,other_locomotors_all_readably_rewritten=False,scope='Drive, hover water-to-shore, ship, walk, jumpjet and teleport ordinary missions reach their requested cells alive. Existing 32-frame ship subcell precision/extra terrain query accepted by effects and exact per-mode pre/post parity; no comparator weakening. Jumpjet retains airborne Move state; hover retains vertical motion.'))
print(dict(passed=True,locomotors=6,healthy_arrived=6,ship_difference_frames=32,maximum_world_delta=maximum,all_current_changes_preserve_parent_behavior=True))
