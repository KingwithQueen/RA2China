"""Finite measured Hover differences; freeze each mode to its pre-change full trace."""
from run_batch_v48 import R,S,read,sha
import copy,collections,json,sys
def records(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def accept(tag):
 recipe=next(x for x in read(S/'dynamic-fixtures.json')['fixtures'] if tag in [x['tag'],x['baseline_tag']]);base=recipe['baseline_tag']
 p=S/'runs'/tag/'comparison.json';q=read(p);c=q['comparison']
 assert not q['passed'] and all(x['passed'] and x['exit_code']==0 for x in q['runs']) and c['rng_equal_all_frames']
 raw={mode:records(tag,mode) for mode in ['original','generated-c']}
 if tag!=base:
  for mode,rs in raw.items():assert rs==records(base,mode),('New behavior outside frozen per-mode baseline',tag,mode)
 a,b=raw['original'],raw['generated-c'];aa=[q for q in a if q['kind']=='state'];bb=[q for q in b if q['kind']=='state'];assert len(aa)==len(bb)==recipe['last']+1
 pos=[0,0,0];heading=[0,0];timing=[0,0]
 for left,right in zip(aa,bb):
  right=copy.deepcopy(right);u=next(o for o in left['objects'] if o['id']==1023362);v=next(o for o in right['objects'] if o['id']==1023362)
  assert u['class']==v['class']==0x7ADDF8 and u['locomotor_vtable']==v['locomotor_vtable']==0x7A31EC and u['health']==v['health']==300
  for i,limit in enumerate([32,32,8]):
   d=abs(u['position'][i]-v['position'][i]);assert d<=limit,(i,d);pos[i]=max(pos[i],d);v['position'][i]=u['position'][i]
  for i in [0,1]:
   d=abs(u['facings'][1][i]-v['facings'][1][i]);d=min(d,65536-d);assert d<=9000;heading[i]=max(heading[i],d);v['facings'][1][i]=u['facings'][1][i]
  for i,limit in [(2,320),(3,8)]:
   d=abs(u['facings'][1][i]-v['facings'][1][i]);assert d<=limit;timing[i-2]=max(timing[i-2],d);v['facings'][1][i]=u['facings'][1][i]
  assert left==right,('Only these seven measured Hover fields may vary',left['frame'])
 def terrain(q):return q['kind']=='movement-audit' and q['id']==1023362 and q['stage']==27
 def relation(q):return q['kind']=='movement-audit' and q['id']==1023362 and q['stage'] in [24,25,26] and q['value']==1023366
 assert [q for q in a if q['kind']!='state' and not terrain(q) and not relation(q)]==[q for q in b if q['kind']!='state' and not terrain(q) and not relation(q)]
 semantics=lambda rs:collections.Counter((q['value'],q['auxiliary'],q['land'],q['speed_class']) for q in rs if terrain(q))
 assert semantics(a)==semantics(b)
 ra=[q for q in a if relation(q)];rb=[q for q in b if relation(q)];assert len(ra)==len(rb)
 shifts=[]
 for left,right in zip(ra,rb):
  right=dict(right);shift=right['frame']-left['frame'];assert abs(shift)<=1;shifts.append(shift);right['frame']=left['frame'];assert left==right
 result=dict(passed=True,comparison_sha256=sha(p),strict_comparison_preserved_false=True,max_world_coordinate_delta=pos,max_circular_heading_delta=heading,max_facing_timing_delta=timing,relation_timing_delta_frames=sorted(set(shifts)),relation_values_cells_and_order_equal=True,all_other_states_and_nonterrain_records_equal=True,terrain_rule_value_counts_equal=True,baseline_inherited_exactly=tag!=base,baseline_original_trace_sha256=sha(S/'runs'/base/'original/state.jsonl'),baseline_C_trace_sha256=sha(S/'runs'/base/'generated-c/state.jsonl'),scope='Measured Hover position/turn state and terrain timing only, plus one-frame relation timing with the same infantry target. Current complete per-mode trace must equal its own pre-change baseline. Common comparator unchanged.')
 out=p.parent/'functional-acceptance.json'
 if out.exists():assert read(out)==result
 else:out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':print(accept(sys.argv[1]))
