"""Promote generation 18 only after round 19 strict gates, then archive exact bytes."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v19'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write_existing(path,value,**options):
 old=path.read_bytes();nl='\r\n' if b'\r\n' in old else '\n'
 path.write_bytes(value.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
def rows(tag,mode='original'):
 return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==140 and len(receipt['inputs'])==222 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-objects-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
assert all(r['passed'] and r['save_before']==r['save_after'] for r in default['runs'])
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-objects-default'))==select(rows('c-objects-default','generated-c'))
for mode in ['original','generated-c']:
 f28=next(r for r in rows('c-objects-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['sampling-verified','exits-verified','objects-verified']}
assert all(x['passed'] for x in parts.values()) and parts['objects-verified']['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
probes={n:read(S/(n+'-verified-01.json')) for n in ['advance-sampling-probe','prepare-exits-probe','object-terrain-services-probe']}
assert all(p['passed'] and p['original_stack_cleanup_verified'] for p in probes.values())
assert [p['cases'] for p in probes.values()]==[32768,12288,32768]
native_identity=read(S/'native-dispatch-identity.json')
assert native_identity['passed'] and native_identity['total_cases']==77824
assert sha(S/'route_control_probe.exe')==native_identity['probe_sha256']
for entry in native_identity['inputs']:assert sha(R/entry['path'])==entry['sha256'],entry['path']
new_cases=sum(p['cases'] for p in probes.values())
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,19)]
archives+=[('v19-baseline',S/'baseline','source-manifest.json','')]
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
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards,existing_labels_preserved=True)
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
 'Advance arrival, remaining Prepare target/retry shared tails and base CanEnterCell/ground-height services remain. Full-game equivalence is unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
effect['budget'].update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,
 default_rules_full_exhaustion_verified=True,natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'))
effect.update(advance_sampling=dict(readable=True,native_probe=probes['advance-sampling-probe'],entries=[3,9,10],interpolation_entries=10),
 prepare_exit=dict(readable=True,native_probe=probes['prepare-exits-probe'],entries=[10,6,8,4]),
 object_and_terrain_services=dict(readable=True,native_probe=probes['object-terrain-services-probe'],primary_functions=6,whole_owner_passage_classifier_readable=False))
write(S/'effects.json',effect)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='c-objects-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,
 path_postprocess_orchestration_readable=True,local_turn_rewrite_readable=True,path_anchor_readable=True,
 collision_segment_rewrite_readable=True,search_completion_readable=True,advance_interpolation_readable=True,prepare_shared_success_readable=True,cell_lookup_readable=True,threat_read_service_readable=True,advance_sampling_readable=True,prepare_retry_exits_readable=True,object_scan_services_readable=True,surface_height_services_readable=True,whole_search_readable=False,full_original_equivalence_verified=False)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第十八批-采样推进与共享退出及对象地形服务-20261022.txt'
handoff=P/'交接文档-单位移动第十八批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text((R/'movement_report_v19.txt').read_text(encoding='utf-8').format(exe=exe,digest=digest,stage=S,
 part_identities=part_identities,fixture_digest=budget['fixture_executable_sha256']),encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第十八批正式验收交接（2026-10-22）
正式代次18 / 验证轮次19：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
Advance余量/采样选择：4A15ED初次选表3处、4A1F8D游标推进9处、4A1FA1余量选择10处；另补齐两处独立入口的插值转接，插值共10处。
Prepare重建返回复核、重试计时、清理与返回共享出口共28处展开接入；其余目标清理/递归尾部仍须继续。
对象/地形服务：4717B0建筑筛选、4717E0地形对象筛选、471830步兵优先的障碍对象筛选、47A130连接读取、5D47D0桥层高度、5D4810离地高度。
28场景15798帧，另默认规则预算901帧严格一致；62组检查通过，新增77824例机器码对照。
三部分分别完成默认901帧、三格包围101帧、默认预算901帧验收，保留三个完整回退点。
修改入口：gameplay/ground_sampling.h/.c、ground_prepare_exit.h/.c、ground_object_services.h/.c。旧布局和调用适配：runtime/ground_dispatch_bridge.h/.c。
保留余量>7、0号零坐标采样有效、先选表再验证方向、-1和8方向例外；共享出口保留目标复核→停止，读帧→延迟换算→重读单位并写计时器。
对象类别回调后才读next；障碍筛选保留步兵→原服务→再次读开关并查地形对象；高度保留回调后桥层/位置重读。
默认预算27..37帧10..0，第38帧清空目标并停止至240。正常对象服务构造真实AI TRUCKA和16辆敌方车，规则保持默认；未测随机对局频率，4C3895未单独挂钩。
完整Advance/Prepare、对象CanEnterCell基础分类与地表高度插值仍未全部整理；完整移动、寻路及全游戏等价尚未完成。
报告：{report}
旧基线：{S/'baseline'}；回退：parts/sampling-verified、exits-verified、objects-verified。
完整归档：final-source；source-manifest.json及final-check.json。生成文件保留原LF，不需要上批换行等价重编译流程。
下一步：Advance到达收尾4A1FDC..4A22F9、Prepare目标清理/递归共享尾部，再推进基础CanEnterCell与地表高度插值服务。
完成后本地提交，不推送；父提交fc6cfcc。既有基线、回退、H盘原始输入和旧手写C引擎保留。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
write_existing(guide,f'''第十八批当前状态（2026-10-22，优先于下文历史描述）

余量与选表：ground_sampling.h/.c。余量>7继续整步，等于7走尾部；0号的(0,0)不是结束。
初次选表在方向检查前执行，-1和8不比较朝向；游标按32位回绕增加。两处独立余量入口也接入已有可读插值。
共享退出：ground_prepare_exit.h/.c。重建返回先判单位，失败再复核目标，拒绝则停止并false；否则读当前帧→算延迟→重读单位写计时器并true。
清理出口清待播声音并令selector=-1。其余目标清理/递归共享尾部尚未全部整理。
对象/地形：ground_object_services.h/.c。建筑6、步兵2、地形对象36沿原链顺序查找；类别回调后读取next。障碍对象优先步兵，然后原服务，最后重读开关并扫描地形对象。
桥层高度在当前格回调后读取桥层标记；离地高度先查地面，再重读单位Z和桥层，最后扣桥高，保持32位回绕。
旧布局集中在runtime/ground_dispatch_bridge.h/.c，业务C不含游戏固定地址。
28场景15798帧+默认预算901帧，62组检查通过。策略修改另建候选并逐帧复核。
下一步Advance到达收尾、Prepare目标清理/递归尾部、基础CanEnterCell及地表高度插值。完整游戏等价尚未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
write_existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十八批正式接续：{handoff}\nAdvance余量/采样、Prepare共享退出、对象筛选与桥层高度服务已整理；28场景15798帧+默认预算901帧、62组检查通过。\n下一步到达收尾、目标清理/递归尾部、基础CanEnterCell和地表高度插值；完整游戏等价未完成。本地提交，不推送。\n',encoding='utf-8',newline='\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86重编译与可读单位移动完成第十八批正式验收。Advance余量/采样、Prepare共享退出及对象/桥层高度服务已整理；28场景15798帧，另默认规则预算901帧严格一致。入口为[第十八批交接](交接文档-单位移动第十八批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续到达收尾、目标清理/递归尾部及基础通行/地表高度服务；完整游戏等价尚未完成，旧基线和手写C引擎保留。\n'
write_existing(readme,''.join(lines),encoding='utf-8',newline='\n')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v19*') if p.is_file())
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
validation=dict(passed=True,formal_baseline_generation=18,verification_round=19,exe_sha256=digest,state_schema=12,
 paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 probes=62,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
 frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
 source_files=len(manifest),production_c_sources=140,content_inputs=222,preservation=preservation,unsupported_guards=37,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,
 path_postprocess_orchestration_readable=True,local_turn_rewrite_readable=True,path_anchor_readable=True,collision_segment_rewrite_readable=True,
 search_completion_readable=True,advance_interpolation_readable=True,prepare_shared_success_readable=True,cell_lookup_readable=True,threat_read_service_readable=True,advance_sampling_readable=True,prepare_retry_exits_readable=True,object_scan_services_readable=True,surface_height_services_readable=True,whole_prepare_function_readable=False,whole_advance_function_readable=False,whole_prepare_shared_exits_readable=False,whole_object_passage_classifier_readable=False,retained_passage_services=['base CanEnterCell 4C86E0','ground-height interpolation 55A280','remaining terrain/object services'],
 whole_path_search_readable=False,whole_ground_movement_readable=False,full_original_equivalence_verified=False,report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=18,verification_round=19,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,path_postprocess_orchestration_readable=True,
 local_turn_rewrite_readable=True,path_anchor_readable=True,collision_segment_rewrite_readable=True,search_completion_readable=True,
 whole_path_search_readable=False,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
 advance_interpolation_readable=True,prepare_shared_success_readable=True,cell_lookup_readable=True,threat_read_service_readable=True,advance_sampling_readable=True,prepare_retry_exits_readable=True,object_scan_services_readable=True,surface_height_services_readable=True,whole_advance_function_readable=False,whole_prepare_shared_exits_readable=False,whole_object_passage_classifier_readable=False,
 next_readable_region='Advance arrival handling 4A1FDC..4A22F9, Prepare target clearing/recursive shared tails, base CanEnterCell and ground-height interpolation; continue strict runtime and default-budget comparison',
 previous_recovery_validation=str(R/'evidence/movement-state-v18/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
 independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
 normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=18,verification_round=19,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
 main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=18,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
