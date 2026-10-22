"""Promote generation 22 only after round 23's strict real-scene and native gates."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v23'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write_existing(p,value):
 old=p.read_bytes();nl='\r\n' if b'\r\n' in old else '\n';p.write_bytes(value.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
def rows(tag,mode='original'):
 return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json');connections=read(S/'connection-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified'] and connections['passed']
assert connections['production_scenes']==3 and connections['production_frames']==1503
assert connections['normal_exit_runtime_verified'] and connections['occupied_exit_runtime_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']==connections['production_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==156 and len(receipt['inputs'])==255 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/d-final-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for mode in ['original','generated-c']:
 f28=next(r for r in rows('d-final-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['tube-verified','handoff-verified','surface-verified']}
assert all(x['passed'] for x in parts.values())
# The faithful content rebuild changes PE identity; verified source bytes must remain exact.
part_manifest={e['path']:e['sha256'] for e in read(S/'parts/surface-verified/manifest.json')}
part_receipt=read(S/'parts/surface-verified/ra2/build-original-c/source-content-receipt.json');supplement=[]
for name,value in receipt['inputs'].items():
 rel=Path(name).relative_to(R).as_posix()
 if rel in part_manifest:assert part_manifest[rel]==value,rel
 else:
  assert part_receipt['inputs'][name]==value,rel
  supplement.append(dict(path=rel,sha256=value))
assert read(S/'refactor-structure.json')['passed']
native=read(S/'native-internal-identity.json');numeric=read(S/'native-connection-numeric-identity.json');tube=read(S/'native-tube-state-identity.json')
assert native['passed'] and native['total_cases']==131072 and numeric['passed'] and numeric['total_cases']==1601904
assert tube['passed'] and tube['total_cases']==131072
for identity in [native,numeric,tube]:
 for e in identity['inputs']+[identity['probe_executable']]:assert sha(R/e['path'])==e['sha256'],e['path']
new_cases=131072
paired_scenes=28+connections['production_scenes'];paired_frames=15798+connections['production_frames']
observer_scenes=connections['independent_observer_scenes'];observer_frames=connections['independent_observer_frames']
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,23)]
archives+=[('v23-baseline',S/'baseline','source-manifest.json','')]
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
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards,existing_connected_tail_targets_preserved=True)
write(S/'preservation.json',preservation)
write(S/'checkpoint-runtime-supplement.json',dict(passed=True,scope='Unchanged runtime inputs omitted by prior snapshot path selection; hashes match the pre-existing surface checkpoint content receipt. Old archives are not modified; all inputs are included in this final archive.',inputs=supplement))

conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_budget_scope=budget['scope'],
 natural_budget_entries=budget['scenes']['v-default-budget-final']['modes']['original']['budget_events'],new_real_scene_evidence=str(S/'budget-real-scenes.json'),
 new_static_followup=budget['callback_scope'],necessary_conditions=budget['necessary_conditions'])
conditions['unresolved']=['4C3895 callback site remains static inference, not independently hooked.','Untouched random-match frequency is not measured.',
 'Remaining Advance/Prepare internal fragments and terrain/object classifiers retain generated C. Full-game equivalence remains unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');effect.update(shared_sampling=dict(entries=[3,11],native=native['results']['advance-shared-sampling-probe']),
 prepare_internal=dict(entries=[4,5,1],native=native['results']['prepare-internal-probe']),connection_runtime=connections['scenes'],
 connection_coordinate_rounding=dict(native=numeric['results'],fixed_first_frame=42))
effect['budget'].update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_scope=budget['scope'])
effect['tube_exit_waypoints']=tube['results']
write(S/'effects.json',effect)
flags={k:v for k,v in read(R/'evidence/movement-state-v22/validation.json').items() if k.endswith('_readable')}
flags.update(tube_exit_state_readable=True,tube_waypoint_switches_readable=True,advance_internal_handoffs_readable=True,prepare_upper_layer_handoff_readable=True,terrain_tube_tile_classifiers_readable=True,surface_object_support_height_readable=True,whole_tube_movement_readable=False,advance_shared_sampling_entries_readable=True,prepare_internal_rebuild_fragments_readable=True,
 connection_axis_numeric_fragments_readable=True,connection_angle_table_fragments_readable=True,whole_prepare_function_readable=False,whole_advance_function_readable=False,
 whole_prepare_shared_exits_readable=False,whole_object_passage_classifier_readable=False,whole_path_search_readable=False,
 whole_ground_movement_readable=False,full_original_equivalence_verified=False)
accept.update(paired_scenes=paired_scenes,paired_frames=paired_frames,production_default_skirmish='d-final-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
 independent_connection_observer_frames=observer_frames,independent_connection_observer_scenes=observer_scenes,**flags)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第二十二批-隧道状态与内部接续及通行分类-20261022.txt'
handoff=P/'交接文档-单位移动第二十二批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text(f'''单位移动第二十二批正式验收（2026-10-22）
正式代次22 / 验证轮次23
程序：{exe}
SHA-256：{digest}
证据：{S}

一、可读业务C
1. ground_tube_state.h/.c：6FAA45结束判定、6FAB6A剩余距离/速度分支及整个6FAE76出口收尾。出口有人先复制对象快照，随后按原顺序查询类别与行进状态，对静止的指定类别发出让路请求；暂停本单位速度并销毁快照。出口为空时落位、入格、按目标格指针相等判断自身让路请求，再恢复任务、速度与下一连接朝向。让路请求不是停止命令。保留类别1/15的短路查询、可变快照计数及回调后状态重读。路点对齐后重读结束标志，不在回调前缓存结果。
2. ground_handoff.h/.c及ground_tube_state_bridge：Prepare 4A3257桥面/高度层选择1处，保留原低字节与高24位、坐标及完整返回值；Advance 4A2311已选模板接续11处、4A1F90游标推进8处，复用既有纯业务采样服务，不重复查询表或对象。独立重叠入口补回4A237D插值标签，既有生成标签和后续分支保留。
3. ground_surface_class.h/.c：479CC0隧道入口有效索引及地类10判断，47A270连续14项地块族判断，47A290支撑高度：先算坡面高度，再读取开关和对象链；首个类别6支撑对象高度或既有回退服务的85增量。保留有符号比较、32位回绕及回调顺序。
旧地址、布局、虚调用、快照分配与ABI恢复集中在runtime/ground_tube_state_bridge.h/.c；三个业务模块不读取固定游戏地址。业务代码增加中文注释与可读控制流。

二、逐部分验收与回退
三部分均通过默认遭遇战901帧、三格包围101帧、默认规则预算901帧、东西双向隧道各501帧，单部分2905帧。每部分保存源码、程序、清单和验证记录。
{part_identities}
随后按内容执行正式构建和空操作构建；{receipt['source_count']}个C源、{len(receipt['inputs'])}项输入，空操作刷新0，完整内容凭证匹配。正式重新链接前后的业务源字节与surface回退点逐项相同，最终程序另通过完整矩阵。
核对发现历史回退清单漏收7项未改动的共用运行时输入；其哈希与surface回退中既有构建凭证一致。本批最终归档补齐全部255项编译输入，保留旧档原样，详情见checkpoint-runtime-supplement.json。

三、最终严格验收
{paired_scenes}个生产场景{paired_frames}帧逐帧一致：既有27场景14897帧、最终默认901帧、隧道生产{connections['production_frames']}帧。另默认规则构造AI预算901帧、独立隧道观察{observer_frames}帧。命令、随机数、有序内部查询全部相同，缺帧与坐标负控通过；生产记录器/schema12/两个公共比较器不变。
76组原版片段、数值和ABI检查通过；本批新增131072例，出口完整收尾、内部接续、地形分类、路点状态各32768例。检验原机器码执行与C回调值及顺序、非易失寄存器、栈平衡；片段覆盖与实景命中分别记账。旧72组全部重跑，原第42/59帧隧道数值反例及旧失败轨迹保留。
独立隧道观察程序仅替换3个测试对象。原版在4A1470/4A1564/6FAFE1/6FAEB4挂只读记录，C在对应服务点记录；保存寄存器、标志和x87/SSE状态。正式与观察程序的全部状态及原有事件一致，仅排除新增观察记录。直接命中范围见connection-real-scenes.json，不据最终位置推断内部命中。
东西正常出口均在211帧直接命中。新增出口占用场景在170帧用正常服务放置16辆真实车辆，两格边界覆盖78,114出口且不显式调用重寻路；211..255帧连续45次命中占用分支，单位暂停在出口，256帧进入正常出口收尾，257帧采样速度恢复1.0，最终到达80,114并清空目标。两个引擎的分支记录、全部状态及有序事件一致。此为明确构造实景，不称为未经干预的随机遭遇战。
默认步兵第28帧X=17343、三格第52帧、转弯第197帧、二次补建失败399帧、持续失败451..1111帧门槛继续通过。预算场景规则不改，正常对象服务构造AI TRUCKA及16辆敌车，第27..37帧10..0，第38帧清空停止至240；未直接写预算、路径、目标，未测未经构造的随机对局频率，4C3895尚未单独挂钩。

四、边界与接续
旧v9..v22正式归档、本批baseline及三个parts回退点、H盘20项原始输入、游戏/SAV和旧手写C引擎逐项核验。最终精确来源在final-source、source-manifest.json和final-check.json。
本批完成隧道路点切换与整个出口分支；6FABAA后接近点构造、6FAD45/6FAE46高度推进仍保留生成C。完整6FAA30、Advance、Prepare、通行分类、寻路、地面移动和全游戏等价均未完成，37个未实现保护保留。不同保存路段指针等少见分支未新增实景，不扩大为全分支覆盖。
类别6对象支撑高度、上界回绕等边界主要由原版片段探针覆盖，未各自增加独立实景挂点；本批独立分支实景证据限于明确记录的隧道连接、占用及正常出口。
下一步优先整理接近点构造、高度推进及剩余Advance/Prepare片段，再推进更广泛对象通行分类；继续默认遭遇战、预算自然耗尽、双向与出口占用隧道的逐帧门禁。
本地提交，不推送。父提交1a8ed787ef9af63065ebebbf8c38ea19e04e7719。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第二十二批正式验收交接（2026-10-22）
正式代次22 / 验证轮次23：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
已整理：隧道结束/路点切换及完整出口；Advance已选模板接续和游标推进；Prepare桥面高度层选择；隧道入口/地块族分类及对象支撑高度。业务在ground_tube_state、ground_handoff、ground_surface_class，地址/布局/ABI在runtime/ground_tube_state_bridge。
三部分各完成2905帧对照并保存回退；最终{paired_scenes}生产场景{paired_frames}帧，另预算901帧及独立观察{observer_frames}帧。76组检查，本批新增131072例原机器码对照。直接隧道命中与正式程序身份见connection-real-scenes.json。
报告：{report}
旧基线baseline，回退parts/tube-verified、handoff-verified、surface-verified；最终final-source、source-manifest.json、final-check.json。正式内容构建后源字节与surface回退点一致，最终矩阵绑定正式EXE。
默认预算构造真实AI与敌车，27..37帧10..0，第38帧清空停止；未测随机对局频率及独立4C3895挂钩。
下一步6FABAA接近点构造、6FAD45/6FAE46高度推进、其余Advance/Prepare，再推进对象通行分类。完整模块/全游戏等价尚未完成，37个保护保留。
保留旧正式归档、本批回退、原始资源和旧引擎。本地提交，不推送。父提交1a8ed787。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
write_existing(guide,f'''第二十二批当前状态（2026-10-22，优先于下文历史描述）

ground_tube_state：出口对象快照与让路请求、暂停/恢复、入格收尾、路点切换。目标判断是目标格与出口格指针相等。回调后重读状态，保留查询次数与顺序。
ground_handoff：Prepare桥面高度层判断；Advance模板接续与游标推进复用ground_sampling_shared，地址布局由ground_tube_state_bridge适配。
ground_surface_class：隧道入口/连续14项地块族，以及先坡面后对象/回退的支撑高度。修改规则应在业务函数另建候选，逐帧验证后再升级。
最终{paired_scenes}场景{paired_frames}帧，另预算901帧、独立隧道观察{observer_frames}帧；76组检查。本批业务源无固定游戏地址。完整隧道6FAA30、Advance、Prepare、广泛对象通行及全游戏等价尚未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
write_existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第二十二批正式接续：{handoff}\n隧道路点/出口状态、Advance/Prepare内部接续及三项地形对象服务完成；{paired_scenes}场景{paired_frames}帧+预算901帧+独立观察{observer_frames}帧、76组检查通过。\n下一步接近点与高度推进、剩余内部片段和对象通行。全游戏等价未完成。本地提交，不推送。\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]=f'> 当前研究路线（2026-10-22）：原版1.006 C17/x86可读单位移动完成第二十二批正式验收。隧道状态、Advance/Prepare内部接续、地形与对象支撑高度通过；{paired_scenes}场景{paired_frames}帧，另预算901帧和观察{observer_frames}帧、76组检查。入口为[第二十二批交接](交接文档-单位移动第二十二批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续接近点、高度推进及对象通行；全游戏等价尚未完成，旧基线与回退保留。\n'
write_existing(readme,''.join(lines))
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(name).relative_to(R).as_posix() for name in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v23*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c','.h','.asm') or p.name in ['truck-actor-fixture-build-arguments.json','truck-actor-fixture-probe.exe','truck-actor-fixture-receipt.json','connection-fixture-build-arguments.json','connection-fixture-probe.exe']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
 src=R/rel;data=src.read_bytes();dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);manifest.append(dict(path=rel,sha256=sha(src)));prior=S/'baseline'/rel
 if prior.exists() and prior.read_bytes()==data:continue
 if src.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or src.name=='CMakeLists.txt':
  try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],data.decode('utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
  except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest);(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=22,verification_round=23,exe_sha256=digest,state_schema=12,
 part_checkpoints={name:dict(validation=str(S/'parts'/name/'validation.json'),exe_sha256=value['exe_sha256'],scenes=len(value['scenes']),frames=sum(x['frames'] for x in value['scenes'])) for name,value in parts.items()},
 final_build_inputs_match_surface_checkpoint=True,
 unchanged_runtime_checkpoint_inputs_verified_by_receipt=supplement,
 paired_scenes=paired_scenes,paired_frames=paired_frames,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 independent_connection_observer_scenes=observer_scenes,independent_connection_observer_frames=observer_frames,probes=76,new_fragment_cases=new_cases,
 source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,frame_comparison_passed=True,
 default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],source_files=len(manifest),production_c_sources=156,
 content_inputs=255,preservation=preservation,unsupported_guards=37,new_rare_branch_runtime_hits_independently_recorded=True,
 rare_branch_evidence_scope=connections['scope'],all_rare_branches_verified=False,alternate_saved_segment_pointer_real_scene_verified=False,
 connection_runtime_evidence=str(S/'connection-real-scenes.json'),report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=22,verification_round=23,
 paired_scenes=paired_scenes,paired_frames=paired_frames,probes=76,new_fragment_cases=131072,production_c_sources=156,content_inputs=255,
 report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),**flags)
recovery.update(next_readable_region='Tube approach-point construction and height progression, remaining Advance/Prepare fragments, then broader object passage services; preserve default, natural budget, bidirectional and occupied-exit frame gates',
 previous_recovery_validation=str(R/'evidence/movement-state-v22/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),new_rare_branch_runtime_hits_independently_recorded=True,
 rare_branch_evidence_scope=connections['scope'],connection_runtime_evidence=str(S/'connection-real-scenes.json'),all_rare_branches_verified=False)
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=paired_scenes,paired_frames=paired_frames,
 independent_default_budget_frames=901,independent_connection_observer_frames=observer_frames,passed=True,strict_ordered_audit_passed=True,
 first_difference=None,full_original_equivalence_verified=False,normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=22,verification_round=23,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True,formal_baseline=22,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
