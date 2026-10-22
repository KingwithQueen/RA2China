"""Promote generation 14 only after all round 15 strict gates pass."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v15'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rows(tag,mode='original'):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==126 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-rebuild-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
assert all(r['passed'] and r['save_before']==r['save_after'] for r in default['runs'])
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-rebuild-default'))==select(rows('c-rebuild-default','generated-c'))
for mode in ['original','generated-c']:
    f28=next(r for r in rows('c-rebuild-default',mode) if r['kind']=='state' and r['frame']==28)
    assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
    assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
assert read(S/'parts/rebuild-verified/validation.json')['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
prepare=read(S/'path-prepare-probe-verified-01.json');route=read(S/'region-route-probe-verified-01.json');rebuild=read(S/'path-rebuild-probe-verified-01.json')
assert all(p['passed'] for p in [prepare,route,rebuild])
assert prepare['cases']==8192 and all(prepare['stop_cases']) and route['cases']==4096 and rebuild['cases']==16384
new_cases=sum(p['cases'] for p in [prepare,route,rebuild]);assert new_cases==28672
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in [9,10,11,12,13,14]]
archives+=[('v15-baseline',S/'baseline','source-manifest.json','')]
archives+=[(name,S/'parts'/name,'manifest.json','') for name in ['entry-verified','route-verified','rebuild-verified']]
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
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards)
write(S/'preservation.json',preservation)

conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_budget_scope=budget['scope'],
    new_real_scene_evidence=str(S/'budget-real-scenes.json'),natural_budget_entries=budget['scenes']['h-default-budget']['modes']['original']['budget_events'],
    new_static_followup=budget['callback_scope'],necessary_conditions=budget['necessary_conditions'])
ordinary=conditions['ordinary_drive_failure_analysis']
ordinary.update(main_search_failure='Stop clears the destination; later AI failure callbacks can restore it before failed Prepare returns.',
    conclusion='The default-rule AI TRUCKA fixture exhausts its normal budget naturally with a restored goal in the same Drive.')
ordinary['assumptions'].append('No-consumption inference additionally requires that callbacks do not restore a destination; the default AI scene violates this premise.')
conditions['unresolved']=['Exact 4C3895 callback site is not separately hooked.','Untouched random-match frequency is not measured.',
    'Region graph search, same-region shortcut, path smoothing/postprocessing, completion shell and full-game equivalence remain unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
eb.update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,
    natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'),natural_budget_events=conditions['natural_budget_entries'],natural_stop_frame=38)
effect['search_preparation']=dict(readable=True,native_probe=prepare,integration=read(S/'entry-integration.json'),
    facing_queries=9,root_created_before_same_cell_check=True,entry_cache_layer_rule_distinct=True)
effect['region_route_publication']=dict(readable=True,native_probe=route,integration=read(S/'route-integration.json'),
    root_in_route_not_remarked=True,region_graph_search_still_generated=True)
effect['path_rebuild']=dict(readable=True,native_probe=rebuild,integration=read(S/'rebuild-integration.json'),
    smoothing_and_postprocessing_still_generated=True)
write(S/'effects.json',effect)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='c-rebuild-default',production_default_skirmish_frames=901,
    natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
    search_preparation_readable=True,region_route_publication_readable=True,path_rebuild_readable=True,whole_search_readable=False,full_original_equivalence_verified=False)
write(S/'strict-acceptance.json',accept)

report=P/'docs/单位移动第十四批-搜索准备与路线重建-20261022.txt'
handoff=P/'交接文档-单位移动第十四批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
parts={name:read(S/'parts'/name/'validation.json') for name in ['entry-verified','route-verified','rebuild-verified']}
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text((R/'movement_report_v15.txt').read_text(encoding='utf-8').format(exe=exe,digest=digest,stage=S,
    prepare_stops=prepare['stop_cases'],part_identities=part_identities,fixture_digest=budget['fixture_executable_sha256']),encoding='utf-8')
handoff.write_text(f'''单位移动第十四批正式验收交接（2026-10-22）

搜索入口准备、区域父链路线发布和节点父链到行走方向/高度的重建已整理为命名C。
正式代次14 / 验证轮次15：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
28场景/15798帧，另默认规则预算耗尽901帧严格一致；49组片段/数值检查通过，本轮新增28672例。
三个部分各自完成默认遭遇战901帧、三格包围101帧、默认预算901帧验证，再保存回退点。
入口保持九次朝向查询、根节点先创建、独立的缓存层阈值；区域根包含在路线里但不重新标记；行走路径末槽-1、零评分改1。
第2247帧、默认步兵第28帧、三格包围第52帧修正继续通过。
预算第27..37帧自然消耗10..0，第38帧清空目标。实景是默认规则下通过原服务构造的AI车辆圈，没有直接写预算/路径/目标。
业务入口：{R/'ra2/src/gameplay/ground_path_prepare.h'}；ground_region_route.h/.c；ground_path_rebuild.h/.c。
旧布局适配：runtime/ground_path_lifecycle_bridge.h/.c。
详细说明：{report}
完整源和程序：{S/'final-source'}；清单source-manifest.json，差异source-changes.patch，末检final-check.json。
前正式基线：{S/'baseline/ra2/build-original-c/ra2.exe'}，SHA-256 fb33d2fb448b87116d20f0cf5efe1da73c590de33688912bc198b29f147c76da。
回退点：parts/entry-verified、parts/route-verified、parts/rebuild-verified；编译标签修复前源码/日志亦保留。
下一步：区域图搜索/同区域快捷分支、路径平滑/后处理和完成外壳，然后Advance插值、Prepare共享入口。
完整寻路、完整单位移动和全游戏等价尚未完成。原始输入与全部旧基线保持；未提交或推送。
''',encoding='utf-8')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
guide.write_text(f'''第十四批当前状态（2026-10-22，优先于下文历史阶段描述）

搜索入口准备、区域父链路线发布和行走路径重建已整理。28场景/15798帧，另默认预算901帧严格一致，49组检查通过。
入口ground_path_prepare.h/.c、ground_region_route.h/.c、ground_path_rebuild.h/.c。区域图搜索、同区域快捷分支、路径平滑/后处理及完成外壳仍在旧实现。
本轮说明：{report}

'''+guide.read_text(encoding='utf-8')+'''
三十四、搜索准备与路线重建的修改入口

ground_path_prepare.h/.c：Ra2PathPreparation与服务接口，管理表面高度、根节点、区域游标及入口缓存排除。
保留类型和类别查询次序；九次朝向查询不可合并，第九次只查询；入口缓存阈值与邻格循环的高度差规则不同。
根节点先于同点/同高度检查创建；负上限用0xFFF7。类型标记的原偏移仅在runtime中解释。
ground_region_route.h/.c：Ra2RegionRouteNode、ra2_region_route_publish。连接标记排除根，输出路线包含根，保留区域号低16位。
ground_path_rebuild.h/.c：Ra2RebuiltPath、ra2_path_rebuild。长度包含根，高度来自父链；相邻格查原方向表，长连接为8，末槽为-1。
评分向零截断，0改1；保留未用缓冲槽。合法容量、父链和有限分数由调用者保证。
runtime/ground_path_lifecycle_bridge.h/.c负责旧布局、服务分派和输出地址，业务C不访问原版绝对地址。
区域图搜索、同区域快捷分支、平滑/后处理和完成外壳未全部整理。新MOD策略须另建候选，继续默认遭遇战、预算圈和原版片段验证。
''',encoding='utf-8')
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
main.write_text(main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十四批正式验收接续入口：{handoff}\n搜索入口准备、区域父链路线发布及行走路径重建已整理；28场景15798帧，另默认预算901帧严格通过，49组检查通过。\n下一步区域图搜索、路径平滑/后处理及完成外壳。完整寻路和全游戏等价未完成；不提交、不推送。\n',encoding='utf-8')

paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v15*') if p.is_file())
paths.add('ra2/tools/playtest.py')
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c','.h','.asm') or p.name in ['truck-actor-fixture-build-arguments.json','truck-actor-fixture-probe.exe','truck-actor-fixture-receipt.json','playtest-before-link-pool.py']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in (S/'pending').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
    src=R/rel;data=src.read_bytes();dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);manifest.append(dict(path=rel,sha256=sha(src)))
    prior=S/'baseline'/rel
    if prior.exists() and prior.read_bytes()==data:continue
    if src.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or src.name=='CMakeLists.txt':
        try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],data.decode('utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
        except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest);(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=14,verification_round=15,exe_sha256=digest,state_schema=12,
    paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
    probes=49,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
    frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
    source_files=len(manifest),production_c_sources=126,content_inputs=len(receipt['inputs']),preservation=preservation,unsupported_guards=37,
    search_preparation_readable=True,region_route_publication_readable=True,path_rebuild_readable=True,
    original_approximate_distance_service_retained=True,whole_path_search_readable=False,whole_ground_movement_readable=False,
    full_original_equivalence_verified=False,report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=14,verification_round=15,
    search_preparation_readable=True,region_route_publication_readable=True,path_rebuild_readable=True,
    whole_path_search_readable=False,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
    next_readable_region='Region graph search and same-region shortcut, path smoothing/postprocessing and completion shell; Advance and Prepare shared entries',
    previous_recovery_validation=str(R/'evidence/movement-state-v14/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
    previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
    independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
    normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=14,verification_round=15,
    executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
    exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
    main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=14,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
