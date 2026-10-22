"""Promote generation 16 only after round 17 strict gates, then archive exact bytes."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v17'
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
assert receipt['source_count']==132 and len(receipt['inputs'])==206 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-completion-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
assert all(r['passed'] and r['save_before']==r['save_after'] for r in default['runs'])
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-completion-default'))==select(rows('c-completion-default','generated-c'))
for mode in ['original','generated-c']:
 f28=next(r for r in rows('c-completion-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['turn-verified','segment-verified','completion-verified']}
assert all(x['passed'] for x in parts.values()) and parts['completion-verified']['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
probes={n:read(S/(n+'-verified-01.json')) for n in ['path-anchor-probe','path-turn-rewrite-probe','path-segment-rewrite-probe','path-completion-probe']}
assert all(p['passed'] for p in probes.values())
assert [p['cases'] for p in probes.values()]==[8192,12288,12288,8192]
assert all(p['original_stack_cleanup_verified'] for p in probes.values())
assert probes['path-segment-rewrite-probe']['successes'] and probes['path-segment-rewrite-probe']['failures_or_zero_prefix']
assert probes['path-completion-probe']['successes'] and probes['path-completion-probe']['failures_or_zero_prefix']
new_cases=sum(p['cases'] for p in probes.values())
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,17)]
archives+=[('v17-baseline',S/'baseline','source-manifest.json','')]
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
repair=read(S/'completion-label-repair.json')
assert repair['passed'] and repair['failed_candidate_never_promoted'] and repair['internal_tail_labels_preserved']
assert sha(S/'investigations/completion-label-before-fix/recomp_0003.c')==repair['failed_source_sha256']
assert sha(S/'investigations/completion-label-before-fix/build.log')==repair['failed_build_log_sha256']
assert sha(R/'ra2/src/recomp/gen_game/recomp_0003.c')==repair['repaired_source_sha256']
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards,completion_repair_archive_verified=True)
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
 'Advance interpolation, shared Prepare entries and low-level passage/threat services remain to be organized. Full-game equivalence is unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
effect['budget'].update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,
 default_rules_full_exhaustion_verified=True,natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'))
effect.update(local_path_rewrites=dict(readable=True,anchor_probe=probes['path-anchor-probe'],
 turn_probe=probes['path-turn-rewrite-probe'],segment_probe=probes['path-segment-rewrite-probe'],
 point_lookup_owner_passage_and_threat_services_retained=True),
 search_completion=dict(readable=True,native_probe=probes['path-completion-probe'],
 integration=read(S/'completion-integration.json'),counter_limit_is_equality=True,cleanup_uses_shared_flag_after_callbacks=True))
write(S/'effects.json',effect)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='c-completion-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,
 path_postprocess_orchestration_readable=True,local_turn_rewrite_readable=True,path_anchor_readable=True,
 collision_segment_rewrite_readable=True,search_completion_readable=True,whole_search_readable=False,full_original_equivalence_verified=False)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第十六批-局部碰撞与搜索退出-20261022.txt'
handoff=P/'交接文档-单位移动第十六批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text((R/'movement_report_v17.txt').read_text(encoding='utf-8').format(exe=exe,digest=digest,stage=S,
 part_identities=part_identities,fixture_digest=budget['fixture_executable_sha256']),encoding='utf-8')
handoff.write_text(f'''单位移动第十六批正式验收交接（2026-10-22）

正式代次16 / 验证轮次17：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
两段局部转弯改写428CF0、反向锚点429570、碰撞段改写4296F0及搜索完成/失败外壳已整理为命名C17。
28场景15798帧，另默认规则预算901帧严格一致；56组片段/数值检查通过，新增40960例。
三个部分各自通过默认901帧、三格包围101帧、默认预算901帧后保存回退点。
入口：gameplay/ground_path_local.h/.c、ground_path_completion.h/.c；旧布局：runtime/ground_path_local_bridge.h/.c。
转弯保留遇阻/段尾后额外查格、起点威胁采样和桥面高度；锚点保留-2跳过和首次折返后重新增长即停。
段改写保留两次顺序尝试、每次重置威胁累计、段尾最多3个高威胁格，失败不改方向，成功剩余槽-2。
搜索退出统一接管16处展开尾部；保留无效/已到达免恢复、空根清理、两项计数相等限制、重建→平滑→后处理→恢复顺序。
地图格查询、对象通行和威胁值服务仍由原实现提供。完整寻路、移动和全游戏等价尚未完成。
预算27..37帧10..0，第38帧清空目标，保持停止至240；默认规则下通过正常服务显式构造真实AI车辆圈。
精确4C3895未单独挂钩，未测未干预随机对局频率。
报告：{report}
旧基线：{S/'baseline'}；回退：parts/turn-verified、segment-verified、completion-verified。
完整源码与程序：final-source；清单source-manifest.json、末检final-check.json。
下一步：Advance插值、Prepare共享入口及底层通行/威胁服务，继续默认遭遇战与预算耗尽逐帧验证。
本轮按授权验收后本地提交，不推送；父提交d032599。旧基线、回退及原始输入保留。
''',encoding='utf-8')

guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
guide.write_text(f'''第十六批当前状态（2026-10-22，优先于下文历史描述）

两段转弯、反向锚点、碰撞段改写与搜索完成/失败外壳已整理；28场景15798帧，另默认预算901帧严格一致，56组检查通过。
业务入口ground_path_local.h/.c、ground_path_completion.h/.c；旧地址/对象布局集中于runtime/ground_path_local_bridge.h/.c。
可修改转弯候选、段尝试顺序、威胁阈值与预算、锚点选择和完成条件。改变策略应另建候选并重新逐帧验证。
保留转弯遇阻也查下一格、段尾威胁预算与普通段不同、计数上限只比较相等、恢复标记在回调后读取的原行为。
原地图查询、对象通行/威胁服务仍在旧实现；下一步Advance插值和Prepare共享入口。完整寻路及全游戏等价未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'),encoding='utf-8')
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
main.write_text(main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十六批正式接续：{handoff}\n局部转弯、反向锚点、碰撞段改写和搜索完成/失败外壳已整理；28场景15798帧+默认预算901帧、56组检查通过。\n下一步Advance插值、Prepare共享入口及底层通行/威胁服务；完整游戏等价未完成。本地提交，不推送。\n',encoding='utf-8')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86重编译与可读单位移动完成第十六批正式验收。局部转弯、锚点定位、碰撞段改写及搜索完成/失败处理已整理；28场景15798帧，另默认规则预算901帧严格一致。入口为[第十六批交接](交接文档-单位移动第十六批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续Advance插值、Prepare共享入口及底层服务；完整游戏等价尚未完成，旧基线和手写C引擎保留。\n'
readme.write_text(''.join(lines),encoding='utf-8')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v17*') if p.is_file())
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
validation=dict(passed=True,formal_baseline_generation=16,verification_round=17,exe_sha256=digest,state_schema=12,
 paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 probes=56,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
 frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
 source_files=len(manifest),production_c_sources=132,content_inputs=206,preservation=preservation,unsupported_guards=37,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,
 path_postprocess_orchestration_readable=True,local_turn_rewrite_readable=True,path_anchor_readable=True,collision_segment_rewrite_readable=True,
 search_completion_readable=True,collision_local_rewrite_services_retained=[],
 whole_path_search_readable=False,whole_ground_movement_readable=False,full_original_equivalence_verified=False,report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=16,verification_round=17,
 region_graph_search_readable=True,same_region_shortcut_readable=True,path_smoothing_orchestration_readable=True,path_postprocess_orchestration_readable=True,
 local_turn_rewrite_readable=True,path_anchor_readable=True,collision_segment_rewrite_readable=True,search_completion_readable=True,
 whole_path_search_readable=False,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
 next_readable_region='Advance interpolation, shared Prepare entries, low-level cell passage and threat services; continue strict runtime and default-budget comparison',
 previous_recovery_validation=str(R/'evidence/movement-state-v16/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
 independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
 normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=16,verification_round=17,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
 main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=16,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
