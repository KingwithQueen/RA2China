"""Derive bounded inherited checkers; preserve their original hashes and scope."""
from run_batch_v55 import *
lineage=[]
for name in ['accept_dynamic_v54.py','audit_scenes_v54.py','audit_sources_v54.py','plan_cleanup_v54.py','commit_movement_v54.py']:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v54','v55')
 if name=='accept_dynamic_v54.py':
  t=t.replace("['mi','sc']","['mi','sc','fm']")
  t=t.replace("assert [u for _,u in drops]==[foot,car]","assert [u for _,u in drops]==recipe.get('drop_order',[foot,car])")
  t=t.replace("if kind=='sc':assert traffic_at_unload", "if kind in ['sc','fm']:assert traffic_at_unload")
 elif name=='audit_scenes_v54.py':
  t=t.replace("'exclusions-cross-'","'frontier-cross-'")
  t=t.replace("['mi','sc','aw3']","['mi','sc','aw3','fm']")
  t=t.replace("path-preparation","path-search")
  t=t.replace("excluded=read(S/'excluded-explorations.json')","excluded=dict(parent=str(O/'effects.json'),sha256=sha(O/'effects.json'),rerun=False)")
 elif name=='audit_sources_v54.py':
  t=t.replace("['ground_path_prepare']","['ground_path_search']")
  t=t.replace("['levels','exclusions']","['neighbors','frontier']").replace("parts['exclusions']","parts['frontier']")
  t=t.replace("['path_lifecycle','capture_packet','transport_packet']","['path_search','capture_packet','transport_packet']")
  t=t.replace('live bridge levels, region snapshot/root creation and ninth-facing query ordering retained','nine-neighbor lookup, repeated region cell reads, live numeric controls and cache publication ordering retained')
 elif name=='plan_cleanup_v54.py':
  t=t.replace('assert candidates','assert candidates is not None')
 elif name=='commit_movement_v54.py':
  t=t.replace('第五十三批','第五十四批').replace('路径准备与混合载员及南侧岸段','路径搜索与步兵先登载')
  t=t.replace('Stage path preparation services; validate mixed passengers and southern shore (batch 53)','Stage path search services; validate infantry-first transport and traffic (batch 54)')
 q=R/name.replace('v54','v55');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n')
 lineage.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
write(S/'checker-lineage.json',dict(passed=True,entries=lineage,scope='Only current harness/checkers derived. Prior source archives and accepted traces remain in place.'))
print(dict(passed=True,derived=len(lineage)))
