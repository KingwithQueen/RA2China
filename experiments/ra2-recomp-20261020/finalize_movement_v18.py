"""Promote generation 17 only after round 18 strict gates, then archive exact bytes."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v18'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rows(tag,mode='original'):
 return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==136 and len(receipt['inputs'])==214 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-services-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
assert all(r['passed'] and r['save_before']==r['save_after'] for r in default['runs'])
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-services-default'))==select(rows('c-services-default','generated-c'))
for mode in ['original','generated-c']:
 f28=next(r for r in rows('c-services-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['interpolation-verified','prepare-verified','services-verified']}
assert all(x['passed'] for x in parts.values()) and parts['services-verified']['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
probes={n:read(S/(n+'-verified-01.json')) for n in ['advance-interpolation-probe','prepare-shared-probe','cell-services-probe']}
assert all(p['passed'] and p['original_stack_cleanup_verified'] for p in probes.values())
assert [p['cases'] for p in probes.values()]==[12288,8192,32768]
native_identity=read(S/'native-services-identity.json')
assert native_identity['passed'] and native_identity['total_cases']==53248
assert sha(S/'ground_services_probe.exe')==native_identity['probe_sha256']
for entry in native_identity['inputs']:assert sha(R/entry['path'])==entry['sha256'],entry['path']
newline_identity=read(S/'newline-object-equivalence.json')
assert newline_identity['passed'] and newline_identity['production_executable_unchanged'] and newline_identity['production_objects_unchanged']
assert newline_identity['exe_sha256']==digest
for entry in newline_identity['results']:
 assert sha(Path(entry['source']))==entry['after_sha256']
 assert entry['object_bytes_equal_except_coff_creation_timestamp']
new_cases=sum(p['cases'] for p in probes.values())
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,18)]
archives+=[('v18-baseline',S/'baseline','source-manifest.json','')]
archives+=[(name,S/'parts'/name,'manifest.json','') for name in parts]
for label,base,name,subdir in archives:
 entries=read(base/name)
 for e in entries:assert sha(base/subdir/e['path'])==e['sha256'],(label,e['path'])
 counts[label]=len(entries)
for e in read(R/'evidence/original-inputs-before.json'):
 assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256'],e['name']
counts['H_originals']=20
assert sha(R/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
assert sha(R/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
assert sha(P/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (R/'ra2/src/recomp/gen_game').glob('*.c'))
assert guards==37
repair=read(S/'prepare-label-repair.json')
assert repair['passed'] and repair['failed_candidate_never_promoted'] and repair['undefined_goto_labels']==0
assert sha(S/'investigations/prepare-label-before-fix/recomp_0010.c')==repair['failed_source_sha256']
assert sha(S/'investigations/prepare-label-before-fix/build.log')==repair['failed_build_log_sha256']
assert sha(R/'ra2/src/recomp/gen_game/recomp_0010.c')==repair['repaired_source_sha256']
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards,prepare_repair_archive_verified=True)
write(S/'preservation.json',preservation)
conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_budget_scope=budget['scope'],
 new_real_scene_evidence=str(S/'budget-real-scenes.json'),natural_budget_entries=budget['scenes']['h-default-budget']['modes']['original']['budget_events'],
 new_static_followup=budget['callback_scope'],necessary_conditions=budget['necessary_conditions'])
conditions['ordinary_drive_failure_analysis'].update(main_search_failure='AI callbacks can restore a goal after Stop before failed Prepare returns.',
 conclusion='Default-rule constructed AI TRUCKA scene naturally exhausts its normal budget with a restored destination in the same Drive.')
conditions['ordinary_drive_failure_analysis']['assumptions'].append('The no-consumption inference requires callbacks not to restore a goal; the default AI fixture violates that premise.')
conditions['unresolved']=['Exact 4C3895 callback site is not separately hooked.','Untouched random-match frequency is not measured.',
 'Full Advance/Prepare state machines and owner CanEnterCell classification remain to be organized. Full-game equivalence is unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
effect['budget'].update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,
 default_rules_full_exhaustion_verified=True,natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'))
effect.update(advance_interpolation=dict(readable=True,native_probe=probes['advance-interpolation-probe'],entries=8),
 prepare_shared_entry=dict(readable=True,native_probe=probes['prepare-shared-probe'],success_entries=2,cached_entries=2),
 cell_and_threat_services=dict(readable=True,native_probe=probes['cell-services-probe'],world_lookup=True,point_lookup=True,slot_presence=True,threat_lookup=True,
 whole_owner_passage_classifier_readable=False))
write(S/'effects.json',effect)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='c-services-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,
 path_postprocess_orchestration_readable=True,local_turn_rewrite_readable=True,path_anchor_readable=True,
 collision_segment_rewrite_readable=True,search_completion_readable=True,advance_interpolation_readable=True,prepare_shared_success_readable=True,cell_lookup_readable=True,threat_read_service_readable=True,whole_search_readable=False,full_original_equivalence_verified=False)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第十七批-插值与共享入口及格子威胁服务-20261022.txt'
handoff=P/'交接文档-单位移动第十七批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text((R/'movement_report_v18.txt').read_text(encoding='utf-8').format(exe=exe,digest=digest,stage=S,
 part_identities=part_identities,fixture_digest=budget['fixture_executable_sha256']),encoding='utf-8')
handoff.write_text(f'''单位移动第十七批正式验收交接（2026-10-22）
正式代次17 / 验证轮次18：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
Advance插值尾部4A237D..4A2633的8处展开副本、Prepare重建成功4A32B4的2处共享入口，及548000/548070/5480B0/54E3A0格子和威胁服务已接入可读C17。
28场景15798帧，另默认规则预算901帧严格一致；59组检查通过，新增53248例机器码对照。
三部分各自完成默认901帧、三格包围101帧、预算901帧验收并保存回退点。
阅读与修改：gameplay/ground_interpolation.h/.c、ground_prepare_shared.h/.c、ground_cell_services.h/.c。
旧布局与调用适配：runtime/ground_services_bridge.h/.c。插值保留四次格子查询、向零取格、原浮点舍入和桥面/占格更新顺序。
Prepare共享成功入口先恢复10次预算，再读取当前队首；已有队列入口沿用缓存值。
格子查询保留备用格坐标副作用；世界坐标入口使用地图容量，格坐标入口固定262144；内部存在性入口不增加原版没有的范围检查。
威胁用实际格坐标而非请求坐标，4x4块、每行130项，负值除法向零。
完整Prepare/Advance内部状态机和对象CanEnterCell分类仍未全部整理；完整移动、寻路及全游戏等价尚未完成。
预算27..37帧10..0，第38帧目标清空并停止至240；默认规则正常对象服务构造真实AI车辆圈。精确4C3895未单独挂钩，未测随机对局发生频率。
报告：{report}
旧基线：{S/'baseline'}；回退：parts/interpolation-verified、prepare-verified、services-verified。
完整源码与程序：final-source；source-manifest.json和final-check.json。Prepare未通过编译的标签候选和日志归档于investigations/prepare-label-before-fix。
下一步：Advance余量/采样选择与Prepare剩余共享出口，继续对象通行分类和地形/区域服务；保持逐帧和预算验收。
本轮按授权完成后本地提交，不推送；父提交4b68703。旧基线、回退及原始输入保留。
''',encoding='utf-8')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
guide.write_text(f'''第十七批当前状态（2026-10-22，优先于下文历史描述）

Advance不足一采样步的插值/放置、Prepare重建成功共享入口和格子/威胁读取已整理。
业务入口ground_interpolation.h/.c、ground_prepare_shared.h/.c、ground_cell_services.h/.c；原版布局集中在runtime/ground_services_bridge.h/.c。
插值先变换，构造终点，再插值、查起点和中间格，按格子身份选择位置；跨格按离开→放置→桥层→进入顺序，同格临时清placement_flag。
四次格子查询、变换前快照与变换后重读、progress>3边界、原x87精度/转换控制字均须保留。
Prepare重建成功恢复10次预算并重读队首；已有队列共享入口不重置预算。
世界坐标查询使用地图count，格坐标查询固定262144，空槽/越界都更新同一备用格坐标。存在性入口要求调用方保证有效索引。
威胁索引使用实际返回格坐标：(x/4)+(y/4)*130；负数向零，不能改成位移或向下取整。
28场景15798帧+独立默认预算901帧，59组检查通过。改变MOD策略后另建候选重新对照。
完整Prepare/Advance、对象CanEnterCell分类与全游戏等价仍未完成。下一步整理余量/采样入口和剩余共享出口，再继续对象/地形底层服务。
报告：{report}

'''+guide.read_text(encoding='utf-8'),encoding='utf-8')
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
main.write_text(main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十七批正式接续：{handoff}\nAdvance插值、Prepare共享成功入口及格子/威胁服务已整理；28场景15798帧+默认预算901帧、59组检查通过。\n下一步余量/采样和剩余共享出口、对象通行与地形/区域服务；完整游戏等价未完成。本地提交，不推送。\n',encoding='utf-8')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86重编译与可读单位移动完成第十七批正式验收。Advance插值、Prepare共享成功入口和格子/威胁服务已整理；28场景15798帧，另默认规则预算901帧严格一致。入口为[第十七批交接](交接文档-单位移动第十七批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续余量/采样、共享出口和对象通行服务；完整游戏等价尚未完成，旧基线和手写C引擎保留。\n'
readme.write_text(''.join(lines),encoding='utf-8')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v18*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c','.h','.asm') or p.name in ['truck-actor-fixture-build-arguments.json','truck-actor-fixture-probe.exe','truck-actor-fixture-receipt.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
 src=R/rel;data=src.read_bytes();dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 manifest.append(dict(path=rel,sha256=sha(src)));prior=S/'baseline'/rel
 if prior.exists() and prior.read_bytes()==data:continue
 if src.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or src.name=='CMakeLists.txt':
  try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],data.decode('utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
  except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest);(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=17,verification_round=18,exe_sha256=digest,state_schema=12,
 paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 probes=59,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
 frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
 source_files=len(manifest),production_c_sources=136,content_inputs=214,preservation=preservation,unsupported_guards=37,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,
 path_postprocess_orchestration_readable=True,local_turn_rewrite_readable=True,path_anchor_readable=True,collision_segment_rewrite_readable=True,
 search_completion_readable=True,advance_interpolation_readable=True,prepare_shared_success_readable=True,cell_lookup_readable=True,threat_read_service_readable=True,whole_prepare_function_readable=False,whole_advance_function_readable=False,retained_passage_services=['owner CanEnterCell classification','terrain and object services'],
 whole_path_search_readable=False,whole_ground_movement_readable=False,full_original_equivalence_verified=False,report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=17,verification_round=18,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,path_postprocess_orchestration_readable=True,
 local_turn_rewrite_readable=True,path_anchor_readable=True,collision_segment_rewrite_readable=True,search_completion_readable=True,
 whole_path_search_readable=False,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
 advance_interpolation_readable=True,prepare_shared_success_readable=True,cell_lookup_readable=True,threat_read_service_readable=True,whole_advance_function_readable=False,
 next_readable_region='Advance progress/sample selection, remaining Prepare shared exits, owner passage classification and terrain/region services; continue strict runtime and default-budget comparison',
 previous_recovery_validation=str(R/'evidence/movement-state-v17/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
 independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
 normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=17,verification_round=18,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
 main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=17,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
