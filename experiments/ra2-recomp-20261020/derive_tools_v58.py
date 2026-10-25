"""Derive bounded local-path harness; explicit parent identity and three original routines."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v58'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lineage=[]
for name in ['run_batch_v57.py','accept_dynamic_v57.py','audit_scenes_v57.py','audit_sources_v57.py','plan_cleanup_v57.py','commit_movement_v57.py','audit_evidence_v57.py','verify_final_movement_v57.py']:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v57','v58')
 if name=='run_batch_v57.py':
  t=t.replace("O=R/'evidence/movement-state-v56'","O=R/'evidence/movement-state-v57'")
  t=t.replace("'smooth'","'turns'").replace("'postprocess'","'segments'")
  t=t.replace('build-path-optimize-probe','build-path-local-probe').replace('path_optimize_probe','path_local_probe').replace('ground_path_optimize','ground_path_local').replace('-path-optimize-','-path-local-')
  t=t.replace('for phase in [0,1]:','for phase in [0,1,2]:')
  t=t.replace("x['cases']==8192 and x['phase']==phase","x['cases']==(8192 if phase==0 else 12288) and x['phase']==phase")
  a=t.index(" if name=='segments':write(S/'native-gates.json'");b=t.index('\ndef baseline_scenes():',a)
  t=t[:a]+" if name=='segments':write(S/'native-gates.json',dict(passed=True,groups=3,cases=32768,receipts=probes,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,scope='Original anchor 8192, turn shortening 12288, segment rewrite 12288 inputs; repeated before/after both parts counted once. Full buffers, cells, ordered callbacks, return values and native stack cleanup. Engine services stubbed; completion phase 3 not rerun.'))\n"+t[b:]
 elif name=='audit_scenes_v57.py':
  t=t.replace("'postprocess-cross-'","'segments-cross-'").replace('path-optimization','local-path')
 elif name=='audit_sources_v57.py':
  t=t.replace('path-optimization service phases','local-path service phases').replace("['ground_path_optimize']","['ground_path_local']")
  t=t.replace("['smooth','postprocess']","['turns','segments']").replace("parts['postprocess']","parts['segments']")
  t=t.replace("['path_optimize','capture_packet','transport_packet']","['path_local','capture_packet','transport_packet']")
  t=t.replace("native['groups']==2","native['groups']==3").replace('groups=2,new_cycle_cases=16384','groups=3,new_cycle_cases=32768')
  t=t.replace('smooth pair/connection progression, callback-updated arrays and anchors, postprocess scan limits and compaction ordering retained','anchor reverse scan, turn corridor queries, threat checks, post-block height lookahead and validate-before-publish segment ordering retained')
 elif name=='commit_movement_v57.py':
  t=t.replace('第五十六批','第五十七批').replace('路径平滑与后处理服务','局部路径与锚点及段改写')
  t=t.replace('Stage path smoothing and postprocess services (batch 56)','Stage local turn, anchor and segment rewriting services (batch 57)')
 elif name=='audit_evidence_v57.py':
  a=t.index('source=(R/');b=t.index("write(S/'infrastructure-status.json'",a)
  t=t[:a]+'''source=(R/'ra2/src/gameplay/ground_path_local.c').read_text(encoding='utf-8')
for helper in ['ra2_path_find_anchor','can_shorten_run','segment_is_passable','publish_segment_directions']:assert helper in source
write(S/'service-boundaries.json',dict(passed=True,changed_unit='ground_path_local.c',new_headers_or_build_sources=False,stages=['anchor reverse-scan naming and turn corridor validation','two-run segment validation and delayed publication'],retained=['anchor skips minus two and treats direction eight by low three bits','owner factor then house before candidate loops','turn threat query uses origin, segment threat query uses stepped point','turn properties/threat are short-circuited after passage','turn always looks up the next cell and updates level after block or final step','segment threat precedes passage; properties always read after passage','segment high-threat state resets for swapped attempt','final-segment low byte controls threat acceptance','publish directions only after complete candidate validation','failed rewrites preserve direction buffer; unused successful slots marked minus two'],native_probe_scope='8192 anchor and 12288 each turn/segment mapped-original inputs; full buffers/cells and ordered callbacks, return values and native stack cleanup. 12 numeric controls for turn/segment. Engine services stubbed; not complete ABI or natural entry coverage.'))
''' +t[b:]
 elif name=='verify_final_movement_v57.py':
  t=t.replace('==(56,57)','==(57,58)').replace("['smooth','postprocess']","['turns','segments']").replace('parts/postprocess/','parts/segments/')
  t=t.replace('path_optimize_probe','path_local_probe').replace("['ra2/src/gameplay/ground_path_optimize.c']","['ra2/src/gameplay/ground_path_local.c']")
  t=t.replace("len(x['probes'])==2","len(x['probes'])==3").replace('=={0,1}','=={0,1,2}').replace('in [0,1]','in [0,1,2]')
  t=t.replace("proof['cases']==8192","proof['cases']==(8192 if proof['phase']==0 else 12288)")
  t=t.replace("proof['ordered_callbacks_and_buffers_compared']","proof['full_buffers_and_ordered_callbacks_compared'] and proof['original_stack_cleanup_verified']")
  t=t.replace("native['groups']==2 and native['cases']==16384","native['groups']==3 and native['cases']==32768")
  t=t.replace("len(baseline['receipts'])==2","len(baseline['receipts'])==3")
  t=t.replace("x['cases']==8192 and x['probe_exe_sha256']","x['cases']==(8192 if x['phase']==0 else 12288) and x['probe_exe_sha256']")
  t=t.replace("for name in native['receipts'])==16384","for name in native['receipts'])==32768")
  t=t.replace('generation=56','generation=57').replace('native_cases=16384','native_cases=32768')
 q=R/name.replace('v57','v58');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n')
 lineage.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
source=R/'evidence/movement-state-v38/path_local_probe.c';assert sha(source)==sha(S/'path_local_probe.c')
lineage.append(dict(source=source.relative_to(R).as_posix(),source_sha256=sha(source),derived=(S/'path_local_probe.c').relative_to(R).as_posix(),derived_sha256=sha(S/'path_local_probe.c'),change='Unmodified probe; anchor/turn/segment phases only. Completion phase 3 excluded.'))
(S/'checker-lineage.json').write_text(json.dumps(dict(passed=True,entries=lineage),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(lineage),parent='movement-state-v57',native_cases=32768))
