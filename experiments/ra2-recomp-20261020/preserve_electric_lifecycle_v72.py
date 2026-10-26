from combat_batch_v72 import *
from lifecycle_scenes_v72 import execute
x=next(x for x in read(S/'qualified-scene-recipes.json')['fixtures'] if x['tag']=='electric');value=execute('f-electric-diagnostic',x,1200)
proofs=[]
for mode in ['original','generated-c']:
    a=S/'runs/b-electric'/mode/'state.jsonl';b=S/'runs/f-electric-diagnostic'/mode/'state.jsonl';assert sha(a)==sha(b),mode;proofs.append(dict(mode=mode,baseline_sha256=sha(a),final_sha256=sha(b)))
write(S/'electric-exception-preservation.json',dict(passed=True,accepted_natural_equivalence=False,result=value,complete_per_mode_before_after=proofs,parent_rng_and_timing_gap_preserved=True,raw_comparator_relaxed=False))
