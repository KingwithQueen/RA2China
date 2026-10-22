"""Promote generation 24 only after all round 25 gates pass; retain every rollback."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v25'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,value):
 old=p.read_bytes();nl='\r\n' if b'\r\n' in old else '\n';p.write_bytes(value.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json');tubes=read(S/'connection-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert len(accept['probes'])==85 and budget['passed'] and budget['default_rules_full_exhaustion_verified']
assert tubes['passed'] and tubes['production_scenes']==5 and tubes['production_frames']==2505
assert tubes['tube_entry_runtime_verified'] and tubes['tube_horizontal_runtime_verified'] and tubes['occupied_exit_runtime_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']==tubes['production_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==164 and len(receipt['inputs'])==271 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-passage-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901 and c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for mode in ['original','generated-c']:
 rows=[json.loads(l) for l in (S/'runs/c-passage-default'/mode/'state.jsonl').open(encoding='utf-8')]
 f=next(r for r in rows if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f['objects'] if o['id']==1032262)['position'][0]==17343
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 assert (P/'reports'/name).read_bytes()==(S/'baseline/project/reports'/name).read_bytes(),name
parts={name:read(S/'parts'/name/'validation.json') for name in ['travel-verified','internal-verified','passage-verified']}
for name,x in parts.items():
 assert x['passed'] and len(x['scenes'])==6 and sum(r['frames'] for r in x['scenes'])==3406,name
 m={e['path']:e['sha256'] for e in read(S/'parts'/name/'manifest.json')}
 assert all(Path(p).relative_to(R).as_posix() in m for p in receipt['inputs']),name
assert parts['passage-verified']['exe_sha256']==digest
final_inputs={e['path']:e['sha256'] for e in read(S/'parts/passage-verified/manifest.json')}
assert all(final_inputs[Path(p).relative_to(R).as_posix()]==v for p,v in receipt['inputs'].items())
assert read(S/'refactor-structure.json')['passed']
identities={}
for name,cases in [('internal',131072),('connection-numeric',1601904),('tube-state',131072),('progress',491520),('travel',360448)]:
 identity=read(S/('native-'+name+'-identity.json'));assert identity['passed'] and identity['total_cases']==cases
 for e in identity['inputs']+[identity['probe_executable']]:assert sha(R/e['path'])==e['sha256'],e['path']
 identities[name]=identity
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,25)]
archives+=[('v25-baseline',S/'baseline','source-manifest.json','')]
archives+=[(name,S/'parts'/name,'manifest.json','') for name in parts]
for label,base,name,sub in archives:
 entries=read(base/name)
 for e in entries:assert sha(base/sub/e['path'])==e['sha256'],(label,e['path'])
 counts[label]=len(entries)
for e in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256'],e['name']
counts['H_originals']=20
assert sha(R/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
assert sha(R/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
assert sha(P/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (R/'ra2/src/recomp/gen_game').glob('*.c'));assert guards==37
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards,existing_connected_tail_targets_preserved=True)
write(S/'preservation.json',preservation)
conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(necessary_conditions=budget['necessary_conditions'],new_static_followup=budget['callback_scope'],natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_budget_scope=budget['scope'],natural_budget_entries=budget['scenes']['v-default-budget']['modes']['original']['budget_events'],new_real_scene_evidence=str(S/'budget-real-scenes.json'))
conditions['unresolved']=['4C3895 callback site remains static inference, not independently hooked.','Untouched random-match frequency is not measured.','Remaining internal fragments and classifiers retain generated C; full-game equivalence is unfinished.']
write(S/'budget-conditions.json',conditions)
effects=read(S/'effects.json');effects['tube_entry_horizontal_and_template_neighbor']=identities['travel']['results'];effects['connection_runtime']=tubes['scenes'];effects['budget'].update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_scope=budget['scope']);write(S/'effects.json',effects)
flags={k:v for k,v in read(R/'evidence/movement-state-v24/validation.json').items() if k.endswith('_readable')}
flags.update(tube_entry_preparation_readable=True,tube_horizontal_continuations_readable=True,advance_template_sample_continuation_readable=True,prepare_next_template_gates_readable=True,neighbor_direction_passage_readable=True,whole_tube_movement_readable=False,whole_prepare_function_readable=False,whole_advance_function_readable=False,whole_object_passage_classifier_readable=False,whole_ground_movement_readable=False,full_original_equivalence_verified=False)
accept.update(paired_scenes=33,paired_frames=18303,production_default_skirmish='c-passage-default',production_default_skirmish_frames=901,natural_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,independent_connection_observer_scenes=5,independent_connection_observer_frames=2505,**flags);write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第二十四批-隧道入口与水平接续及内部模板-20261022.txt'
handoff=P/'交接文档-单位移动第二十四批正式验收-20261022.txt';assert not report.exists() and not handoff.exists()
part_text='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text(f'''单位移动第二十四批正式验收（2026-10-22）
正式代次24 / 验证轮次25
程序：{exe}
SHA-256：{digest}
证据：{S}

一、可读C实现
ground_tube_travel：整理6FAA66..6FAB6A入口距离、路段选择、朝向、速度与两端高度准备；先请求位置/距离，再重新选择路段和请求位置/朝向，按原顺序查询入口和出口高度，使用查询前读取的段数计算每段高度差。端点Cell坐标先按有符号16位解释，再换算世界中心，保留32位回绕。
6FAC70..6FAD1C跨路点剩余推进和6FAD75..6FAE1D普通水平推进均整理为同一可读计算流程。先扩展朝向低16位，再减0x3FFF、换弧度、查正弦/余弦，Y减、X加，各次乘加保留原精度。查表和最终整数转换均遵循独立转换控制字，不能直接用宿主sin/cos或普通double表达式。两种分支的距离来源、方向来源、坐标缓冲位置和高度接续入口各自保留。构造返回指针仍按原版处理，后续高度使用实际输出缓冲和预载寄存器。
ground_template_next：Advance 4A17A2六处内部模板样本/朝向变换接续；Prepare 4A33C3两处继续条件、下一格接受检查及完整提前返回。可重入服务之间重读单位和坐标；世界坐标转Cell先向零除256再截16位，保留负值和极值。原采样高层入口仍通过既有业务代码运行，本批没有宣称六个内部入口都已实景独立命中。
ground_passage_neighbor：7031F2相邻对象方向分类。查反向相邻格，再查障碍；仅方向差绝对值3..5且方向有效时硬阻挡，保留无障碍、方向-1及方向回绕。其余对象通行入口和整体分类仍需继续整理。
ground_travel_bridge集中旧对象布局、地址、栈及寄存器接续；三个业务模块没有固定游戏地址。原始标签和现有业务适配均保留，原版记录器、schema12和两个公共比较器字节不变。

二、逐部分验收与回退
隧道、内部模板、相邻对象三部分分别通过6场景3406帧：默认遭遇战901、三格包围101、默认规则真实AI预算901、双向隧道各501、出口占用501。每一部分验收后保存独立程序和全部271项编译输入。
{part_text}
最终程序与passage回退一致。164个C源、271项输入逐项核对，最终空操作构建刷新0。

三、原版逐帧及片段验证
最终33个生产场景18303个模拟帧全部严格一致，另默认规则AI预算901帧、独立隧道观察2505帧。命令、随机数、有序内部查询、连续帧以及坐标/缺帧负控均通过；菜单和非法命令等辅助门禁通过。
85组原版片段/数值/ABI检查通过；本批360448例：入口32768、跨路点水平131072、普通水平131072、内部模板32768、相邻通行32768。涵盖12种运算控制字、4种转换舍入、朝向遍历、构造返回别名、回调修改速度/单位/坐标、负坐标和提前返回。开发期探针发现的转换舍入、共享缓冲、输出地址及测试桩布局问题均在生产接入前修正，过程见native-travel-development.json；最终结果以native-travel-identity.json绑定的源码和程序为准。
本轮独立观察仅替换5个测试对象，在原有七个只读观察点外增加原版6FAA66/6FAC70/6FAD75及对应C服务点。保全寄存器、标志、x87/SSE；五个隧道场景均直接命中入口、跨路点和普通水平分支。正式与观察程序全部状态及既有有序事件逐项一致，原版与C新增观察事件顺序、帧、位置也一致。详细次数见connection-real-scenes.json。
等高双向出口211帧；出口占用通过170帧正常构造16辆真实车产生，211..255帧等待，256帧出口，257帧速度恢复，最终到达80,114。高差地图保留原记录，仅东侧合法高度层6、西侧4；上/下行最终高度624/416，分别211/220帧出口，保持原版下行短暂低于地面的数值行为。
默认步兵第28帧X=17343、三格第52帧、转弯197帧、二次补建失败399帧及持续失败451..1111帧门槛保持通过。
预算耗尽仍为默认规则下通过正常服务构造的真实AI TRUCKA和16辆敌车：27..37帧10..0，第38帧清空停止，未直接写预算、路径或目标。尚未测未经干预随机遭遇战中的发生频率，4C3895仍未独立挂钩。

四、保护与边界
v9..v24旧正式归档、本轮baseline和三个部分回退逐项哈希核验；H盘20项原始输入、原游戏/SAV和旧手写C程序保持原样。source-manifest.json与final-source保存最终源码及全部271项输入，final-check.json绑定报告与程序。
完整6FAA30、Advance、Prepare、对象通行及全游戏等价仍未完成，37个未实现保护保留。本轮高差实景使用直线路径，非直线、不同保存路段指针及内部模板的少见独立触发仍需另补，不将原版片段探针计为实景覆盖。
下一步继续剩余Advance/Prepare内部入口模板、对象通行入口与共享返回，补充非直线隧道和内部片段独立实景观察；继续默认遭遇战、预算耗尽、双向隧道、出口占用逐部分门禁。
完成后本地提交，不推送。父提交42b8053ae7e56bd2ed59c812e6305a124ddde3a8。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第二十四批正式验收交接（2026-10-22）
正式代次24 / 验证轮次25：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
本批：ground_tube_travel入口距离/朝向、两种水平推进；ground_template_next内部模板样本与下一格门禁；ground_passage_neighbor相邻障碍方向分类。适配ground_travel_bridge。入口6FAA66、6FAC70、6FAD75；内部4A17A2六处、4A33C3两处；相邻7031F2。
三部分各6场景3406帧，全部271项输入独立回退；最终33场景18303帧，另预算901、独立观察2505帧；85组检查，本批360448例原版片段。五个隧道实景均直接命中三条新入口，原版/C及正式/观察程序逐项一致。
报告：{report}
旧baseline；回退parts/travel-verified、internal-verified、passage-verified；final-source、source-manifest.json、final-check.json。164个C源、271项输入，空操作刷新0。
默认预算为正常服务构造的真实AI/敌车，27..37帧10..0、第38帧清空；未经干预随机对局频率和4C3895独立挂钩仍未测。出口占用211..255帧等待、256帧出口；上/下行高差出口211/220帧。内部模板和邻格分类没有宣称全部分支实景独立命中。
下一步剩余内部模板/共享返回、对象通行入口，补非直线隧道及罕见内部接续的独立观察。完整模块和全游戏等价尚未完成，37个保护保留。
保留旧归档与全部回退；本地提交，不推送。父提交42b8053。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
existing(guide,f'''第二十四批当前状态（2026-10-22，优先于历史描述）
ground_tube_travel：入口距离/朝向/速度/高度准备及两种水平推进，独立转换控制字、端点有符号坐标和两套输出缓冲均保留。
ground_template_next：内部样本变换和下一格门禁，服务后重读单位及坐标，提前返回完整保留。
ground_passage_neighbor：相邻障碍方向差3..5的硬阻挡，保留无方向和空对象。旧地址集中ground_travel_bridge。
三部分各6场景3406帧；最终33场景18303帧，另预算901与观察2505帧，85组检查、本批360448例。完整模块及全游戏等价尚未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第二十四批正式接续：{handoff}\n入口距离/朝向、水平接续、内部模板及相邻对象方向分类完成本批验收。33场景18303帧+预算901帧+独立观察2505帧，85组检查；三部分各6场景3406帧保存回退。继续剩余内部模板、对象通行入口及非直线隧道。全游戏等价未完成。本地提交，不推送。\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86可读单位移动完成第二十四批正式验收。隧道入口/水平接续、内部模板与相邻对象分类通过；33场景18303帧，另预算901帧、观察2505帧及85组检查。入口为[第二十四批交接](交接文档-单位移动第二十四批正式验收-20261022.txt)及 `reports/latest-recovery.json`。完整模块和全游戏等价仍未完成，旧基线及回退保留。\n';existing(readme,''.join(lines))
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(name).relative_to(R).as_posix() for name in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v25*') if p.is_file())
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
validation=dict(passed=True,formal_baseline_generation=24,verification_round=25,exe_sha256=digest,state_schema=12,
 part_checkpoints={name:dict(validation=str(S/'parts'/name/'validation.json'),exe_sha256=x['exe_sha256'],scenes=len(x['scenes']),frames=sum(r['frames'] for r in x['scenes'])) for name,x in parts.items()},
 final_build_inputs_match_passage_checkpoint=True,paired_scenes=33,paired_frames=18303,independent_default_budget_scenes=1,independent_default_budget_frames=901,independent_connection_observer_scenes=5,independent_connection_observer_frames=2505,
 probes=85,new_fragment_cases=360448,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],source_files=len(manifest),production_c_sources=164,content_inputs=271,
 preservation=preservation,unsupported_guards=37,tube_approach_runtime_verified=True,tube_height_runtime_verified=True,tube_entry_runtime_verified=True,tube_horizontal_runtime_verified=True,new_rare_branch_runtime_hits_independently_recorded=True,rare_branch_evidence_scope=tubes['scope'],all_rare_branches_verified=False,alternate_saved_segment_pointer_real_scene_verified=False,connection_runtime_evidence=str(S/'connection-real-scenes.json'),report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=24,verification_round=25,paired_scenes=33,paired_frames=18303,probes=85,new_fragment_cases=360448,production_c_sources=164,content_inputs=271,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),**flags)
recovery.update(next_readable_region='Remaining internal Advance/Prepare templates and object passage entry/shared return paths; add non-straight tube and rare internal continuation observations while retaining per-part real-scene gates',previous_recovery_validation=str(R/'evidence/movement-state-v24/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),tube_entry_runtime_verified=True,tube_horizontal_runtime_verified=True,new_rare_branch_runtime_hits_independently_recorded=True,rare_branch_evidence_scope=tubes['scope'],connection_runtime_evidence=str(S/'connection-real-scenes.json'),all_rare_branches_verified=False)
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=33,paired_frames=18303,independent_default_budget_frames=901,independent_connection_observer_frames=2505,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=24,verification_round=25,executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True,formal_baseline=24,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
