"""Promote generation 25 only after all round 26 gates pass; retain every rollback."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v26'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,value):
 old=p.read_bytes();nl='\r\n' if b'\r\n' in old else '\n';p.write_bytes(value.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json');tubes=read(S/'connection-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert len(accept['probes'])==89 and budget['passed'] and budget['default_rules_full_exhaustion_verified']
assert tubes['passed'] and tubes['production_scenes']==7 and tubes['production_frames']==3707
internal=read(S/'internal-real-scenes.json');assert internal['passed'] and internal['independent_frames']==4054
assert tubes['curved_bidirectional_runtime_verified']
assert tubes['tube_entry_runtime_verified'] and tubes['tube_horizontal_runtime_verified'] and tubes['occupied_exit_runtime_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']==tubes['production_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==168 and len(receipt['inputs'])==279 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-final-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901 and c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for mode in ['original','generated-c']:
 rows=[json.loads(l) for l in (S/'runs/c-final-default'/mode/'state.jsonl').open(encoding='utf-8')]
 f=next(r for r in rows if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f['objects'] if o['id']==1032262)['position'][0]==17343
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 assert (P/'reports'/name).read_bytes()==(S/'baseline/project/reports'/name).read_bytes(),name
parts={name:read(S/'parts'/name/'validation.json') for name in ['template-verified','passage-verified','returns-verified']}
for name,x in parts.items():
 assert x['passed'] and len(x['scenes'])==6 and sum(r['frames'] for r in x['scenes'])==3406,name
 m={e['path']:e['sha256'] for e in read(S/'parts'/name/'manifest.json')}
 assert all(Path(p).relative_to(R).as_posix() in m for p in receipt['inputs']),name
assert parts['returns-verified']['exe_sha256']==digest
final_inputs={e['path']:e['sha256'] for e in read(S/'parts/returns-verified/manifest.json')}
assert all(final_inputs[Path(p).relative_to(R).as_posix()]==v for p,v in receipt['inputs'].items())
assert read(S/'refactor-structure.json')['passed']
identities={}
for name,cases in [('internal',131072),('connection-numeric',1601904),('tube-state',131072),('progress',491520),('travel',360448),('joint',262144)]:
 identity=read(S/('native-'+name+'-identity.json'));assert identity['passed'] and identity['total_cases']==cases
 for e in identity['inputs']+[identity['probe_executable']]:assert sha(R/e['path'])==e['sha256'],e['path']
 identities[name]=identity
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,26)]
archives+=[('v26-baseline',S/'baseline','source-manifest.json','')]
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
conditions['independent_internal_evidence']=str(S/'internal-real-scenes.json')
conditions['unresolved']=['4C3895 callback site remains static inference, not independently hooked.','Untouched random-match frequency is not measured.','Remaining internal fragments and classifiers retain generated C; full-game equivalence is unfinished.']
write(S/'budget-conditions.json',conditions)
effects=read(S/'effects.json');effects['internal_templates_passage_shared_returns']=identities['joint']['results'];effects['connection_runtime']=tubes['scenes'];effects['budget'].update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_scope=budget['scope']);write(S/'effects.json',effects)
flags={k:v for k,v in read(R/'evidence/movement-state-v25/validation.json').items() if k.endswith('_readable')}
flags.update(template_entry_fragments_readable=True,passage_entry_services_readable=True,shared_movement_returns_readable=True,tube_entry_preparation_readable=True,tube_horizontal_continuations_readable=True,advance_template_sample_continuation_readable=True,prepare_next_template_gates_readable=True,neighbor_direction_passage_readable=True,whole_tube_movement_readable=False,whole_prepare_function_readable=False,whole_advance_function_readable=False,whole_object_passage_classifier_readable=False,whole_ground_movement_readable=False,full_original_equivalence_verified=False)
accept.update(paired_scenes=35,paired_frames=19505,production_default_skirmish='c-final-default',production_default_skirmish_frames=901,natural_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,independent_connection_observer_scenes=7,independent_connection_observer_frames=3707,independent_internal_observer_scenes=4,independent_internal_observer_frames=4054,**flags);write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第二十五批-内部模板与通行入口及共享返回-20261022.txt'
handoff=P/'交接文档-单位移动第二十五批正式验收-20261022.txt';assert not report.exists() and not handoff.exists()
part_text='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text(f'''单位移动第二十五批正式验收（2026-10-22）
正式代次25 / 验证轮次26
程序：{exe}
SHA-256：{digest}
证据：{S}

一、可读C整理
1. ground_template_entry：Advance 4A17D5六处内部样本坐标准备，保留负坐标修正的32位回绕；世界坐标转格子仍先有符号向零除256，再截低16位。既有完整采样业务和变换服务也使用同一可读格子换算。Prepare 4A3486两处通行准备：构造下一格、离格标记、通行分类、恢复标记；每次服务重读当前单位，保留分类后恢复标记对共享输出的修改。
2. ground_passage_entry：70323E剩余内部对象通行入口，包含委托虚函数及输出、匹配桥层的占用和归属、可见性限制、基础Foot分类及硬阻挡提前返回。基础查询前重新读取调用方向、层高及既有分类，保留最初装入的特殊标记，避免错误合并回调之间的重读。
3. ground_return_plan与ground_joint_bridge：按Advance/Prepare/对象通行三类帧布局统一恢复非易失寄存器、EAX、栈及标志。落位、失败收尾和Prepare完成外壳改用共享返回。目标清理和重寻路行为仍由原业务执行，不混入ABI返回。旧标签和尾调用保持。
主流程ground_entry/ground_segment仍与重叠片段适配并存；本批独立观察同时覆盖既有高层服务边界，不宣称每个新副本均被自然调用。后续修改行为需检查主入口与剩余内部入口，尚未完成全部副本统一。
三个业务模块无旧游戏固定地址；布局与调用约定集中ground_joint_bridge。运行时代码仍为纯C17，正式记录器/schema12及两个公共比较器不变。

二、逐部分验收与回退
模板、对象入口、共享返回三部分各通过默认遭遇战901帧、三格包围101帧、默认规则AI预算901帧、双向隧道各501帧和出口占用501帧，共6场景3406帧。
{part_text}
每个回退保存全部279项编译输入及程序；最终程序与returns回退一致。168个C源、279项输入逐项一致，最终空操作构建刷新0。

三、逐帧与原版片段检查
最终35个生产场景19505帧严格一致；另默认规则真实AI预算901帧、七个隧道独立观察3707帧、四个内部独立观察4054帧。命令、随机数、有序内部查询、连续帧和坐标/缺帧负控通过，辅助菜单/非法命令门禁通过。
89组检查通过；本批262144例：样本入口、Prepare通行准备、对象入口、共享返回各65536例。极值坐标、回调换单位、共享输出、可见性短路和完整栈/寄存器返回均与原版片段一致。开发期发现基础查询方向需从共享参数重新读取，已在生产接入前修正，见native-joint-identity.json及joint-development.json。
默认步兵28帧X=17343、三格52帧、转弯197帧、二次补建失败399帧及451..1111帧持续失败门槛保持。预算场景仍为默认规则下通过正常服务构造的真实AI TRUCKA与16辆敌车，27..37帧10..0，第38帧清空停止，无直接预算/路径/目标写入；未测未经干预随机对局频率，4C3895未独立挂钩。

四、新增独立实景
两张弯曲地图保持原入口68,114、出口78,114及反向端点，仅使用合法Tubes路段：正向2,1,1,2,3,3,2,1,3,2，反向按倒序加4；含六段斜向，完整路径回到原端点。方向偏移来自原初始化4916D0，属于运行期BSS，不能当作PE文件内静态表读取。原基线先试跑、最终生产再复验，均无首差。实际轨迹偏离原直线，经过多个路点并最终到达目标、清空目的地，不把地图构造或普通地面绕行当成隧道验收。
七个隧道场景含原双向、出口占用、双向高差及双向弯曲。原版/C入口与高度/水平推进记录逐项一致；每个观察场景的完整状态和既有有序事件还与不挂观察点的正式程序一致。原等高出口211帧、占用211..255帧等待/256帧出口，高差上/下行211/220帧出口保持。弯曲出口帧、Y范围和直接路点命中见connection-real-scenes.json。
独立内部观察在原版4A17A2当前样本、4A1725非首样本、4A17D5变换结果、4A3486 Prepare通行准备、70323E对象入口和4A263A共享返回六点保存只读记录，并与C相同业务边界对照。既有高层实现会直接处理部分边界，独立观察同时记录这些既有服务与新内部适配；不把新重叠副本均已自然触发作为结论。默认遭遇战、长距离、转弯隐形障碍和持续失败四场景直接命中全部六点，包含sample>0的前一采样接续。保全原版寄存器、标志和x87/SSE状态；新增观察程序仅替换九个测试对象，不进入生产程序。原版/C全部记录、正式/观察完整状态与原有事件均一致。internal-real-scenes.json保存计数、代表记录和完整有序命中哈希，全部原始轨迹保留在runs；没有声称全部重叠入口均已独立覆盖。

五、保存和后续
v9..v25旧正式归档、本批baseline与三个回退逐项哈希核验；H盘20项原始输入、原游戏/SAV和旧手写C引擎保持原样。final-source与source-manifest.json归档最终源码及全部279项编译输入，final-check绑定报告与程序。
完整Advance、Prepare、对象通行、隧道模块和全游戏等价仍未完成，37个未实现保护保留。后续继续其余内部模板、对象链入口/分类和共享出口，补弯曲高差、弯曲出口占用及其余少见重叠入口的合法独立实景；保留默认遭遇战和预算耗尽持续回归。
开发观察程序的初次漏记和两个长标记路径启动失败均完整保留。前者补上既有主入口服务点后重新验收；后者用更短标记复核同一程序和地图，未改游戏逻辑或放宽比较器。见observer-development.json。
本地提交，不推送；父提交21dcfd4177c6bdf7420da75f9381efc2cd3210c5。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第二十五批正式验收交接（2026-10-22）
正式代次25 / 验证轮次26：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
本批：ground_template_entry的Advance样本和Prepare通行准备；ground_passage_entry对象入口；ground_return_plan共享返回，适配ground_joint_bridge。4A17D5六处、4A3486两处、70323E入口；落位/失败和Prepare完成返回复用。
三部分各6场景3406帧，全部279项输入及程序独立回退；最终35场景19505帧，另预算901、七个隧道观察3707、四个内部观察4054帧；89组检查，本批262144例。
新增双向非直线隧道含六段斜向，实际偏离直线并到达原端点。内部观察六点全部直接命中，包含sample>0接续；正式/观察、原版/C完整状态及有序记录一致。
报告：{report}
baseline、parts/template-verified、passage-verified、returns-verified保留；final-source/source-manifest及final-check绑定168个C源、279项输入，空操作刷新0。
默认预算27..37帧10..0、38帧停止，是正常服务构造的真实AI/敌车；未经干预随机频率和4C3895独立挂钩仍未测。完整模块和全游戏等价未完成，37个保护保留。
下一步其余模板/对象链与共享出口，补弯曲高差、弯曲出口占用和未覆盖重叠入口。保留全部旧基线/回退。本地提交，不推送。父提交21dcfd4。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
existing(guide,f'''第二十五批当前状态（2026-10-22，优先于历史描述）
ground_template_entry：样本坐标准备与下一格通行准备；ground_passage_entry：委托/桥层占用/可见性/Foot分类入口；ground_return_plan：共享帧恢复，旧地址在ground_joint_bridge。
主流程ground_entry/ground_segment/ground_advance与重叠入口仍并存；修改行为需检查主入口。完整副本统一尚未完成。
三部分各6场景3406帧。最终35场景19505帧，另预算901、隧道观察3707、内部观察4054帧；89组检查，本批262144例。双向弯曲隧道和六个内部边界已独立实景命中。完整模块和全游戏等价尚未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第二十五批正式接续：{handoff}\n内部模板、对象通行入口与共享返回完成本批验收，新增双向弯曲隧道和六个内部边界独立观察。35场景19505帧+预算901帧+隧道观察3707帧+内部观察4054帧，89组检查；三部分各6场景3406帧保存回退。继续其余内部模板、对象链和共享出口，补弯曲高差及未覆盖入口。全游戏等价未完成。本地提交，不推送。\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86可读单位移动完成第二十五批正式验收。内部模板、通行入口和共享返回通过，双向弯曲隧道及六个内部边界已独立观察；35场景19505帧，另预算901帧、隧道观察3707帧、内部观察4054帧及89组检查。入口为[第二十五批交接](交接文档-单位移动第二十五批正式验收-20261022.txt)及 `reports/latest-recovery.json`。完整模块和全游戏等价仍未完成，旧基线及回退保留。\n';existing(readme,''.join(lines))
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(name).relative_to(R).as_posix() for name in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v26*') if p.is_file())
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
validation=dict(passed=True,formal_baseline_generation=25,verification_round=26,exe_sha256=digest,state_schema=12,
 part_checkpoints={name:dict(validation=str(S/'parts'/name/'validation.json'),exe_sha256=x['exe_sha256'],scenes=len(x['scenes']),frames=sum(r['frames'] for r in x['scenes'])) for name,x in parts.items()},
 final_build_inputs_match_returns_checkpoint=True,paired_scenes=35,paired_frames=19505,independent_default_budget_scenes=1,independent_default_budget_frames=901,independent_internal_observer_scenes=4,independent_internal_observer_frames=4054,independent_connection_observer_scenes=7,independent_connection_observer_frames=3707,
 probes=89,new_fragment_cases=262144,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],source_files=len(manifest),production_c_sources=168,content_inputs=279,
 preservation=preservation,unsupported_guards=37,curved_bidirectional_runtime_verified=True,previous_sample_real_scene_verified=True,internal_runtime_evidence=str(S/'internal-real-scenes.json'),tube_approach_runtime_verified=True,tube_height_runtime_verified=True,tube_entry_runtime_verified=True,tube_horizontal_runtime_verified=True,new_rare_branch_runtime_hits_independently_recorded=True,rare_branch_evidence_scope=tubes['scope']+' '+internal['scope'],all_rare_branches_verified=False,alternate_saved_segment_pointer_real_scene_verified=False,connection_runtime_evidence=str(S/'connection-real-scenes.json'),report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=25,verification_round=26,paired_scenes=35,paired_frames=19505,probes=89,new_fragment_cases=262144,production_c_sources=168,content_inputs=279,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),**flags)
recovery.update(independent_internal_observer_frames=4054,independent_connection_observer_frames=3707,curved_bidirectional_runtime_verified=True,previous_sample_real_scene_verified=True,internal_runtime_evidence=str(S/'internal-real-scenes.json'),next_readable_region='Remaining internal templates, object-chain and shared-exit fragments; add curved elevated/occupied tube scenes and uncovered overlapping entries while retaining default/budget regressions',previous_recovery_validation=str(R/'evidence/movement-state-v25/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),tube_entry_runtime_verified=True,tube_horizontal_runtime_verified=True,new_rare_branch_runtime_hits_independently_recorded=True,rare_branch_evidence_scope=tubes['scope']+' '+internal['scope'],connection_runtime_evidence=str(S/'connection-real-scenes.json'),all_rare_branches_verified=False)
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=35,paired_frames=19505,independent_default_budget_frames=901,independent_connection_observer_frames=3707,independent_internal_observer_frames=4054,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=25,verification_round=26,executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True,formal_baseline=25,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
