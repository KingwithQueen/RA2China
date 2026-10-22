"""Promote generation 21 only after round 22's strict real-scene and native gates."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v22'
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
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']==connections['production_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==152 and len(receipt['inputs'])==247 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/d-connection-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for mode in ['original','generated-c']:
 f28=next(r for r in rows('d-connection-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['sampling-verified','prepare-verified','numeric-verified','connection-verified']}
assert all(x['passed'] for x in parts.values()) and parts['connection-verified']['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
native=read(S/'native-internal-identity.json');numeric=read(S/'native-connection-numeric-identity.json')
assert native['passed'] and native['total_cases']==131072 and numeric['passed'] and numeric['total_cases']==1601904
for identity in [native,numeric]:
 for e in identity['inputs']+[identity['probe_executable']]:assert sha(R/e['path'])==e['sha256'],e['path']
new_cases=1732976
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,22)]
archives+=[('v22-baseline',S/'baseline','source-manifest.json','')]
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
 natural_budget_entries=budget['scenes']['v-default-budget']['modes']['original']['budget_events'],new_real_scene_evidence=str(S/'budget-real-scenes.json'),
 new_static_followup=budget['callback_scope'],necessary_conditions=budget['necessary_conditions'])
conditions['unresolved']=['4C3895 callback site remains static inference, not independently hooked.','Untouched random-match frequency is not measured.',
 'Remaining Advance/Prepare internal fragments and terrain/object classifiers retain generated C. Full-game equivalence remains unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');effect.update(shared_sampling=dict(entries=[3,11],native=native['results']['advance-shared-sampling-probe']),
 prepare_internal=dict(entries=[4,5,1],native=native['results']['prepare-internal-probe']),connection_runtime=connections['scenes'],
 connection_coordinate_rounding=dict(native=numeric['results'],fixed_first_frame=42))
effect['budget'].update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_scope=budget['scope'])
write(S/'effects.json',effect)
flags={k:v for k,v in read(R/'evidence/movement-state-v21/validation.json').items() if k.endswith('_readable')}
flags.update(advance_shared_sampling_entries_readable=True,prepare_internal_rebuild_fragments_readable=True,
 connection_axis_numeric_fragments_readable=True,connection_angle_table_fragments_readable=True,whole_prepare_function_readable=False,whole_advance_function_readable=False,
 whole_prepare_shared_exits_readable=False,whole_object_passage_classifier_readable=False,whole_path_search_readable=False,
 whole_ground_movement_readable=False,full_original_equivalence_verified=False)
accept.update(paired_scenes=30,paired_frames=16800,production_default_skirmish='d-connection-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
 independent_connection_observer_frames=1002,independent_connection_observer_scenes=2,**flags)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第二十一批-共享采样与内部重建及隧道实景-20261022.txt'
handoff=P/'交接文档-单位移动第二十一批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text(f'''单位移动第二十一批正式验收（2026-10-22）
正式代次21 / 验证轮次22
程序：{exe}
SHA-256：{digest}
证据：{S}

一、可读 C 整理
ground_sampling_shared.h/.c：Advance 4A15F0的3处展开、4A230E的11处展开。保留调用方方向哨兵、先选表后校验方向、普通/转弯模板、已选模板的采样以及表尾哨兵。已选入口不重复查询路径；插值输入及局部变量写入时点与原版相同。
ground_prepare_internal.h/.c：4A39C8的4处普通重建、4A39CA的5处带标记重建，以及4A3216的1处清理。目标坐标按有符号除法向零截断，再截为两个int16打包；尝试次数分别1/2。保留原ECX调用对象和完整返回值，重建后重新读取当前单位进入既有共享出口。清理入口首坐标沿用原EAX，其余两坐标读取原无效坐标常量。
runtime/ground_internal_bridge.h/.c集中保存旧布局和调用约定；业务函数没有固定游戏地址。未修改正式状态记录器、schema12及两个公共比较器；旧生成标签和尾部目标保留。

二、新实景发现并修复的差异
合法地图[Tubes]通过原引擎解析，正常移动命令自然产生方向8，未直接写连接/路径/目标/预算内部状态。东西两个方向分别使用连接索引0/1，入口68,114与78,114，时长10。
独立观察程序仅替换movement_fixture和ground_remainder_bridge两个对象：原版在4A1470、4A1564挂只读记录，C在相同服务时点记录。两个方向均在第40帧命中连接开始和落位完成。保全通用寄存器、标志和x87/SSE状态；记录入口/出口/时长/路段/坐标/高度/driving/selector/标志。
反向实景最初在第42帧出现Y=29311/29312差异，保留j/k前缀失败轨迹及prepare-verified回退程序。根因为6FADD5与6FADF1两个隧道行进片段采用宿主默认double舍入，丢失极小正分量在原x87向零舍入下造成的1单位变化。
第59帧还涉及跨路点的余量数值链，两条链均已接入。ground_connection_numeric.h/.c及runtime同名桥接逐次执行乘法、加/减和向零截断，服从原控制字，修复两个坐标轴；角度换算与4BA480/4BA4D0的查表逻辑在隧道局部用可读C保留舍入，其他调用者保持原服务。X分支先调整栈16字节，因此输入原坐标必须读取调整前frame+84。整理角度换算、正余弦表索引和两段坐标数值片段，未宣称完整隧道状态机已可读。

三、严格验收
四个部分分别完成默认遭遇战901帧、三格包围101帧和默认规则预算901帧，保存独立源码/程序回退点。
最终30个生产场景16800模拟帧严格一致：既有27场景14897帧、最终默认901帧、双向隧道1002帧。另默认规则构造AI预算901帧，以及独立连接观察程序1002帧。正式程序与观察程序的全部状态和原有有序事件逐项一致，只排除新增观察记录。
72组片段/数值/ABI检查通过。本批1732976例：共享采样65536、Prepare内部65536、隧道数值1601904；新数值覆盖两个轴、12种精度/舍入模式、全部65536种16位朝向和第42帧反例。新共享片段以接续拦截验证栈平衡、局部状态和插值输入，完整既有出口/收尾仍由原有独立ABI探针覆盖。
默认步兵1032262第28帧X=17343；三格第52帧、转弯第197帧、二次补建失败第399帧、持续失败451..1111帧门槛保留。命令、随机数、有序内部事件全部相同，缺帧和坐标负控通过，辅助菜单/非法命令门禁通过。
默认预算场景使用正常对象服务构造AI TRUCKA及16辆敌车，规则未改，未直接写预算/路径/目标；第27..37帧10..0，第38帧清空并停止至240。未测随机对局频率，4C3895回调位置尚未单独挂钩。
生产152个C源、247项内容输入；空操作构建刷新0，程序身份稳定。原始游戏/SAV、H盘20项输入、旧C引擎、历代正式基线及本批回退清单逐项核对。

四、回退和下一步
旧正式基线：{S/'baseline'}
{part_identities}
最终final-source、source-manifest.json、final-check.json记录精确身份。
已补齐合法双向连接的独立实景；其他少见分支（例如与当前路段不同的保存指针）仍只有片段/ABI覆盖，不宣称所有少见分支均已实景命中。
下一步优先整理隧道行进6FAA30的其余状态机、Advance剩余内部接续及Prepare尚未接入的片段，再推进地形/对象通行分类；继续逐部分固定输入对照和预算实景。完整Advance/Prepare、完整寻路、完整地面移动和全游戏等价仍未完成，37个未实现保护保留。
完成后本地提交，不推送；父提交d3207de。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第二十一批正式验收交接（2026-10-22）
正式代次21 / 验证轮次22：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
Advance共享采样15F0/230E共3/11处，Prepare内部重建39C8/39CA共4/5处和3216清理1处已整理成业务C，布局集中在ground_internal_bridge。
合法双向隧道已独立实景命中：第40帧连接开始及落位完成。反向第42/59帧Y差异已按原x87舍入及角度量化修复；新增ground_connection_numeric及其桥接，保留最初失败轨迹。
最终30场景16800帧，另默认预算901帧、独立连接观察1002帧；72组检查，本批1732976例机器码对照。四部分各有默认/三格/预算逐帧门禁及完整回退点。
报告：{report}
旧基线baseline；回退parts/sampling-verified、prepare-verified、numeric-verified、connection-verified；最终final-source、清单及final-check.json。
默认预算27..37帧10..0，第38帧清空停止；正常服务构造真实对象，未测随机对局频率，4C3895未单独挂钩。
独立观察与正式程序的状态及既有事件一致。不同保存指针等其他少见分支未补实景；不能扩大为全分支覆盖。
下一步隧道6FAA30其余状态机、Advance/Prepare剩余内部接续，然后其余地形/对象服务；完整游戏等价未完成，37个保护保留。
本地提交，不推送；父提交d3207de。既有基线、回退、H盘输入和旧C引擎保留。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
write_existing(guide,f'''第二十一批当前状态（2026-10-22，优先于下文历史描述）

共享采样：ground_sampling_shared.h/.c，区分初次入口和保留方向哨兵/已选模板的共享入口。先选表后校验，不增加引擎查询。表尾的两个坐标与游标要共同判断。
内部重建：ground_prepare_internal.h/.c，坐标向零截断后按int16打包，普通重建一次、带标记重建两次；原调用对象及返回值保持一致。
隧道数值：ground_connection_numeric.h/.c，两个坐标轴分别按原x87控制字执行乘法及加减后截断。极小分量也能产生1单位变化，不能改成普通double表达式。旧布局在对应runtime桥接中。
本批30场景16800帧、默认预算901帧、独立双向连接观察1002帧、72组检查通过。合法连接第40帧直接命中，反向第42帧差异已修复；其他少见分支仍须另补实景。
修改上述业务函数或参数后须另建候选，保留基线并逐帧比较。完整隧道状态机、Advance、Prepare和全游戏等价尚未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
write_existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第二十一批正式接续：{handoff}\n共享采样、Prepare内部重建及双向隧道实景已完成；反向第42/59帧差异修复。30场景16800帧+默认预算901帧+独立连接观察1002帧、72组检查通过。\n下一步隧道与Advance/Prepare剩余状态机及地形/对象服务；完整游戏等价未完成。本地提交，不推送。\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86重编译与可读单位移动完成第二十一批正式验收。共享采样、Prepare内部重建、双向隧道独立实景及反向第42帧数值修复通过；30场景16800帧，另预算901帧、连接观察1002帧。入口为[第二十一批交接](交接文档-单位移动第二十一批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续剩余状态机及地形/对象服务；完整游戏等价尚未完成，旧基线和手写C引擎保留。\n'
write_existing(readme,''.join(lines))
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v22*') if p.is_file())
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
validation=dict(passed=True,formal_baseline_generation=21,verification_round=22,exe_sha256=digest,state_schema=12,
 paired_scenes=30,paired_frames=16800,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 independent_connection_observer_scenes=2,independent_connection_observer_frames=1002,probes=72,new_fragment_cases=new_cases,
 source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,frame_comparison_passed=True,
 default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],source_files=len(manifest),production_c_sources=152,
 content_inputs=247,preservation=preservation,unsupported_guards=37,new_rare_branch_runtime_hits_independently_recorded=True,
 rare_branch_evidence_scope=connections['scope'],all_rare_branches_verified=False,alternate_saved_segment_pointer_real_scene_verified=False,
 connection_runtime_evidence=str(S/'connection-real-scenes.json'),report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=21,verification_round=22,
 report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),**flags)
recovery.update(next_readable_region='Remaining Tube movement 6FAA30 state machine, Advance/Prepare internal fragments, then terrain/object passage classifiers; continue strict frame and natural default-budget gates',
 previous_recovery_validation=str(R/'evidence/movement-state-v21/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),new_rare_branch_runtime_hits_independently_recorded=True,
 rare_branch_evidence_scope=connections['scope'],connection_runtime_evidence=str(S/'connection-real-scenes.json'),all_rare_branches_verified=False)
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=30,paired_frames=16800,
 independent_default_budget_frames=901,independent_connection_observer_frames=1002,passed=True,strict_ordered_audit_passed=True,
 first_difference=None,full_original_equivalence_verified=False,normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=21,verification_round=22,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True,formal_baseline=21,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
