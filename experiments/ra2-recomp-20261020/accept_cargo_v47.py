"""Local functional exception, frozen to the exact pre-change Hover traces of this recipe."""
from pathlib import Path
import copy,hashlib,json,collections
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v47'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def records(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').read_text(encoding='utf-8').splitlines()]
def accept(tag):
 baseline={'vc':'b-vc','cc':'b-cc','b-vc':'b-vc','b-cc':'b-cc'}[tag]
 root=S/'runs'/tag;p=root/'comparison.json';x=json.loads(p.read_text());c=x['comparison'];assert not x['passed'] and all(q['passed'] and q['exit_code']==0 for q in x['runs'])
 assert c['rng_equal_all_frames'] and c['first_difference']['path'].startswith('state.objects[id=1023362]')
 raw={mode:records(tag,mode) for mode in ['original','generated-c']}
 if tag!=baseline:
  for mode,rs in raw.items():assert rs==records(baseline,mode),('Must exactly preserve pre-change behavior for each mode',tag,mode)
 a=raw['original'];b=raw['generated-c'];aa=[q for q in a if q['kind']=='state'];bb=[q for q in b if q['kind']=='state'];assert len(aa)==len(bb)==1901
 position=[0,0];facing=[0,0];timing=[0,0]
 for left,right in zip(aa,bb):
  right=copy.deepcopy(right);u=next(o for o in left['objects'] if o['id']==1023362);v=next(o for o in right['objects'] if o['id']==1023362)
  assert u['class']==v['class']==0x7ADDF8 and u['locomotor_vtable']==v['locomotor_vtable']==0x7A31EC and u['health']==v['health']==300
  for i in [0,1]:
   delta=abs(u['position'][i]-v['position'][i]);assert delta<=32;position[i]=max(position[i],delta);v['position'][i]=u['position'][i]
   delta=(u['facings'][1][i]-v['facings'][1][i])%65536;delta=min(delta,65536-delta);assert delta<=8192;facing[i]=max(facing[i],delta);v['facings'][1][i]=u['facings'][1][i]
  for i,limit in [(2,320),(3,4)]:
   delta=abs(u['facings'][1][i]-v['facings'][1][i]);assert delta<=limit;timing[i-2]=max(timing[i-2],delta);v['facings'][1][i]=u['facings'][1][i]
  assert left==right,('Every field outside these six existing Hover fields must match',left['frame'])
 def terrain(q):return q['kind']=='movement-audit' and q['id']==1023362 and q['stage']==27
 assert [q for q in a if q['kind']!='state' and not terrain(q)]==[q for q in b if q['kind']!='state' and not terrain(q)]
 semantics=lambda data:collections.Counter((q['value'],q['auxiliary'],q['land'],q['speed_class']) for q in data if terrain(q))
 assert semantics(a)==semantics(b) and sum(semantics(a).values())>0
 for states in [aa,bb]:
  u=next(o for o in states[-1]['objects'] if o['id']==1023362);assert [v//256 for v in u['position'][:2]]==[63,59]
  assert max(o['position'][1] for q in states for o in q['objects'] if o['id']==1023362)-min(o['position'][1] for q in states for o in q['objects'] if o['id']==1023362)>4000
 result=dict(passed=True,comparison_sha256=sha(p),strict_comparison_preserved_false=True,max_world_coordinate_delta=position,max_circular_heading_delta=facing,max_facing_timing_delta=timing,all_other_state_fields_and_ordinary_commands_equal=True,all_ground_and_nonterrain_audit_records_equal=True,hover_terrain_rule_value_counts_equal=True,baseline_inherited_exactly=tag!=baseline,baseline_original_trace_sha256=sha(S/'runs'/baseline/'original/state.jsonl'),baseline_C_trace_sha256=sha(S/'runs'/baseline/'generated-c/state.jsonl'),scope='Only existing Hover horizontal position/turn state and its terrain-query timing vary. Ground vehicles, infantry, bridge effects, health, missions, RNG and ordinary commands match. Current traces must match each baseline mode exactly; no global comparator relaxation.')
 q=root/'functional-acceptance.json'
 if q.exists():assert json.loads(q.read_text())==result
 else:q.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 import sys;print(accept(sys.argv[1]))
