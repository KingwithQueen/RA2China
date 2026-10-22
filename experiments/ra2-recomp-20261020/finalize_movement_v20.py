"""Promote generation 19 only after round 20 strict gates, then archive exact bytes."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v20'
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
assert receipt['source_count']==143 and len(receipt['inputs'])==228 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-passage-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
assert all(r['passed'] and r['save_before']==r['save_after'] for r in default['runs'])
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-passage-default'))==select(rows('c-passage-default','generated-c'))
for mode in ['original','generated-c']:
 f28=next(r for r in rows('c-passage-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['arrival-verified','cleanup-verified','passage-verified']}
assert all(x['passed'] for x in parts.values()) and parts['passage-verified']['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
probes={n:read(S/(n+'-verified-01.json')) for n in ['advance-arrival-completion-probe','prepare-target-cleanup-probe','base-passage-probe','ground-height-entry-probe']}
assert all(p['passed'] and p['original_stack_cleanup_verified'] for p in probes.values())
assert [p['cases'] for p in probes.values()]==[65536,32768,32768,32768]
native_identity=read(S/'native-completion-identity.json')
assert native_identity['passed'] and native_identity['total_cases']==163840
for entry in native_identity['inputs']+native_identity['probe_executables']:assert sha(R/entry['path'])==entry['sha256'],entry['path']
new_cases=sum(p['cases'] for p in probes.values())
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,20)]
archives+=[('v20-baseline',S/'baseline','source-manifest.json','')]
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
conditions['unresolved']=['Exact 4C3895 callback site is not separately hooked.','Untouched random-match frequency is not measured.',
 'Slope plane core 4706C0 and remaining Advance/Prepare internal fragments are retained. Full-game equivalence is unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
eb.update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,
 natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'))
effect.update(arrival_completion=dict(readable=True,expanded_entries=6,native_probe=probes['advance-arrival-completion-probe']),
 target_cleanup=dict(readable=True,expanded_entries=59,native_probe=probes['prepare-target-cleanup-probe']),
 base_passage=dict(readable=True,primary_functions=2,native_probe=probes['base-passage-probe']),
 ground_height_entry=dict(readable=True,native_probe=probes['ground-height-entry-probe'],slope_core_readable=False))
write(S/'effects.json',effect)
flags=dict(advance_arrival_completion_readable=True,prepare_target_cleanup_readable=True,prepare_recursive_tails_readable=True,
 base_locomotor_passage_readable=True,bridge_ramp_transition_readable=True,ground_height_entry_readable=True,
 whole_prepare_function_readable=False,whole_advance_function_readable=False,whole_prepare_shared_exits_readable=False,
 whole_object_passage_classifier_readable=False,slope_height_core_readable=False,whole_path_search_readable=False,
 whole_ground_movement_readable=False,full_original_equivalence_verified=False)
flags={**{k:v for k,v in read(R/'evidence/movement-state-v19/validation.json').items() if k.endswith('_readable')},**flags}
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='c-passage-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,**flags)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第十九批-到达收尾与目标清理及基础通行高度服务-20261022.txt'
handoff=P/'交接文档-单位移动第十九批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text(f'''单位移动第十九批正式验收（2026-10-22）
正式代次19 / 验证轮次20
程序：{exe}
SHA-256：{digest}
证据：{S}

本批修改
1. Advance到达收尾统一接入4A1FDC，共6个展开入口。ground_completion.c以32位回绕求曼哈顿距离，再沿原x87精度与舍入顺序计算余量；转换后保持原控制字切换。
既有ground_arrival.c继续处理跨格落位、占格恢复、目标格和高度容差、任务停止与下一采样；ABI桥在回调后重读drive.owner，不缓存旧单位。
新增65536例通过生产桥对照原机器码，覆盖12种浮点模式、负坐标/溢出边界和回调更换单位。旧65536例到达回归也重新运行。
2. Prepare目标清理与递归共享出口：8种命名入口，59处展开接入。322E停止空目标、44B3取消目标、4450/4522清理路段、4502计时尾部、4429清路径后递归、44D1失败分类与立即重试、322A清驱动标志。
保留无效路段重复清理时driving不变；普通停止仅清AL，目标停止和递归返回完整EAX；已保存单位与回调后新单位分开读取。递归沿用aborted指针，另外两个参数保持0。
3. 基础通行：4C86E0的移动器委派和4C8730的桥层/坡道/高度差分类。保留先读取移动器再看开关、低字节布尔、未给起点时先查相邻格、-1方向特殊处理，以及高度差0/1/4的不同分支和输出写入时机。
4. 地形高度：55A280整理为完整32位世界坐标选格、越界后备格和4706C0坡面高度服务调用。核心坡面初始化及其浮点计算仍使用原生成C，尚未整理，不能据此宣称完整地形高度模块可读。
业务修改入口：gameplay/ground_completion.h/.c、ground_passage.h/.c；落位语义见ground_arrival.h/.c。旧布局集中在runtime/ground_completion_bridge.h/.c及ground_arrival_bridge.c。

验收
三部分各自通过默认遭遇战901帧、三格包围101帧、默认预算901帧，并保留完整源码/程序回退点。
最终28个生产场景15798模拟帧严格一致；另默认规则构造AI预算耗尽901帧严格一致。状态schema12、命令、随机数、完整有序movement-audit/fixture事件一致，缺帧负控通过；未修改轨迹器和比较器。
66组原版片段/数值/ABI回归全部通过；本批新增163840例，验证栈清理与回调输入/状态。生产C源143个、内容输入228项，空操作重编译刷新0，EXE身份稳定。
默认遭遇战步兵1032262第28帧X=17343；保留三格包围第52帧、转弯第197帧、二次补建失败第399帧及持续失败451..1111帧门槛。
默认预算实景用正常对象服务构造AI TRUCKA及16辆敌方车，规则未改、未写预算/路径/目标内部状态；27..37帧预算10..0，38帧清空并停止至240。此为构造真实对象场景；随机对局频率未测，4C3895回调位置未单独挂钩。

回退与边界
本批前正式基线：{S/'baseline'}
{part_identities}
最终源归档：final-source；清单source-manifest.json；核验final-check.json。历代基线、原始游戏/SAV、H盘20项原始输入及旧手写C引擎哈希均保持一致。37个未实现保护仍在。
完整Advance、Prepare、寻路、对象通行分类和全游戏等价尚未完成。下一步整理Advance剩余碰撞/落位分支与Prepare其余失败收尾，再推进4706C0坡面初始化和高度计算；继续固定存档、seed12345与真实模拟帧对照。
完成后仅本地提交，不推送；父提交2289382。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第十九批正式验收交接（2026-10-22）
正式代次19 / 验证轮次20：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
Advance到达收尾4A1FDC的6个入口已统一；回调后重读单位，保留32位回绕和原x87计算顺序。
Prepare目标清理/递归共享出口8种入口、59处接入；保留路段清理条件、完整返回值和递归参数。
基础通行4C86E0/4C8730与地形高度入口55A280已整理；4706C0坡面核心仍保留生成C。
28场景15798帧，另默认规则预算901帧严格一致；66组检查通过，新增163840例机器码对照。
三部分各自保留默认901帧、三格101帧、预算901帧验收后的完整回退点。
修改入口：gameplay/ground_completion.h/.c、ground_passage.h/.c，runtime/ground_completion_bridge.h/.c、ground_arrival_bridge.c。
默认预算：正常对象服务构造真实AI车及包围，27..37帧10..0，38帧清空并停止至240；未测随机频率，4C3895未单独挂钩。
报告：{report}
旧基线：{S/'baseline'}；回退：parts/arrival-verified、cleanup-verified、passage-verified；最终final-source与清单、final-check.json。
完整Advance/Prepare/对象通行/寻路及全游戏等价仍未完成，37个保护仍在。
下一步Advance剩余碰撞/落位分支、Prepare其余失败收尾与4706C0坡面初始化/高度计算。继续逐部分逐帧验收。
本地提交，不推送；父提交2289382。既有基线、回退、H盘输入和旧C引擎保留。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
write_existing(guide,f'''第十九批当前状态（2026-10-22，优先于下文历史描述）

到达收尾：ground_completion.c的ra2_ground_arrival_adjustment处理回绕距离/x87余量；ground_arrival.c处理落位、目标判定与任务停止。回调后必须重读drive.owner。
目标清理与递归：ground_completion.h/.c的Ra2PrepareFinishEntry命名8种出口；分别清路段/驱动/路径、取消目标、停止或重启计时后递归。旧布局和调用顺序在ground_completion_bridge.c。
基础通行：ground_passage.h/.c。ra2_ground_base_can_enter负责移动器委派；ra2_ground_classify_transition判断坡道、桥层及高度差，按需更新level/changing_layer。
地形高度入口ra2_ground_height_at按完整世界坐标选格并调用坡面服务；4706C0坡面初始化/浮点核心仍待整理。
28场景15798帧+默认预算901帧、66组回归，本批新增163840例。修改规则另建候选并重新逐帧比较。
下一步Advance剩余碰撞/落位、Prepare其余失败收尾及坡面高度核心；完整游戏等价尚未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
write_existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十九批正式接续：{handoff}\n到达收尾、目标清理/递归出口、基础通行与地形高度入口已整理；28场景15798帧+默认预算901帧、66组检查通过。\n下一步剩余碰撞/落位、其余失败收尾与4706C0坡面高度核心。完整游戏等价未完成。本地提交，不推送。\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86重编译与可读单位移动完成第十九批正式验收。到达收尾、目标清理/递归出口及基础通行/地形高度入口已整理；28场景15798帧，另默认预算901帧一致。入口为[第十九批交接](交接文档-单位移动第十九批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续剩余碰撞/落位、其余失败收尾和坡面高度核心；完整游戏等价尚未完成，旧基线和手写C引擎保留。\n'
write_existing(readme,''.join(lines))
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v20*') if p.is_file())
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
validation=dict(passed=True,formal_baseline_generation=19,verification_round=20,exe_sha256=digest,state_schema=12,
 paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 probes=66,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
 frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
 source_files=len(manifest),production_c_sources=143,content_inputs=228,preservation=preservation,unsupported_guards=37,
 retained_passage_services=['4706C0 slope plane initialization and arithmetic','remaining terrain/object services'],report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=19,verification_round=20,
 report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),**flags)
recovery.update(next_readable_region='Advance remaining collision/placement branches, remaining Prepare failure tails, then 4706C0 slope plane initialization and height arithmetic; continue strict runtime and default-budget comparison',
 previous_recovery_validation=str(R/'evidence/movement-state-v19/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
 independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
 normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=19,verification_round=20,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
 main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=19,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
