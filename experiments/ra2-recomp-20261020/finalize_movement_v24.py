"""Promote generation 23 only after round 24's strict real-scene and native gates."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v24'
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
assert connections['production_scenes']==5 and connections['production_frames']==2505
assert connections['normal_exit_runtime_verified'] and connections['occupied_exit_runtime_verified'] and connections['nonzero_height_bidirectional_runtime_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']==connections['production_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==160 and len(receipt['inputs'])==263 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-passage-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for mode in ['original','generated-c']:
 f28=next(r for r in rows('c-passage-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['travel-verified','internal-verified','passage-verified']}
assert all(x['passed'] for x in parts.values())
# Final no-op build preserves the accepted PE; every compiled input must match the last checkpoint.
part_manifest={e['path']:e['sha256'] for e in read(S/'parts/passage-verified/manifest.json')}
for name,value in receipt['inputs'].items():assert part_manifest[Path(name).relative_to(R).as_posix()]==value
assert parts['passage-verified']['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
native=read(S/'native-internal-identity.json');numeric=read(S/'native-connection-numeric-identity.json');tube=read(S/'native-tube-state-identity.json');progress=read(S/'native-progress-identity.json')
assert native['passed'] and native['total_cases']==131072 and numeric['passed'] and numeric['total_cases']==1601904
assert tube['passed'] and tube['total_cases']==131072
assert progress['passed'] and progress['total_cases']==491520
for identity in [native,numeric,tube,progress]:
 for e in identity['inputs']+[identity['probe_executable']]:assert sha(R/e['path'])==e['sha256'],e['path']
new_cases=491520
paired_scenes=28+connections['production_scenes'];paired_frames=15798+connections['production_frames']
observer_scenes=connections['independent_observer_scenes'];observer_frames=connections['independent_observer_frames']
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,24)]
archives+=[('v24-baseline',S/'baseline','source-manifest.json','')]
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
effect['tube_exit_waypoints']=tube['results']
effect['tube_progress_and_classification']=progress['results']
write(S/'effects.json',effect)
flags={k:v for k,v in read(R/'evidence/movement-state-v23/validation.json').items() if k.endswith('_readable')}
flags.update(tube_approach_state_readable=True,tube_height_progress_readable=True,advance_full_sample_header_readable=True,prepare_next_cell_approach_readable=True,object_passage_finish_readable=True,tube_exit_state_readable=True,tube_waypoint_switches_readable=True,advance_internal_handoffs_readable=True,prepare_upper_layer_handoff_readable=True,terrain_tube_tile_classifiers_readable=True,surface_object_support_height_readable=True,whole_tube_movement_readable=False,advance_shared_sampling_entries_readable=True,prepare_internal_rebuild_fragments_readable=True,
 connection_axis_numeric_fragments_readable=True,connection_angle_table_fragments_readable=True,whole_prepare_function_readable=False,whole_advance_function_readable=False,
 whole_prepare_shared_exits_readable=False,whole_object_passage_classifier_readable=False,whole_path_search_readable=False,
 whole_ground_movement_readable=False,full_original_equivalence_verified=False)
accept.update(paired_scenes=paired_scenes,paired_frames=paired_frames,production_default_skirmish='c-passage-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
 independent_connection_observer_frames=observer_frames,independent_connection_observer_scenes=observer_scenes,**flags)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第二十三批-隧道接近点与高度推进及通行收尾-20261022.txt'
handoff=P/'交接文档-单位移动第二十三批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text(f'''单位移动第二十三批正式验收（2026-10-22）
正式代次23 / 验证轮次24
程序：{exe}
SHA-256：{digest}
证据：{S}

一、可读C整理
1. ground_tube_progress.h/.c：6FABAA接近点构造、6FAD1C跨路点剩余高度推进和6FAE1D普通高度推进及完整收尾。先构造偏移探测点，按原顺序查询当前/目标格中心，两次查询后才读取返回数据，再读取当前接近点、平移并增加高度，最后重新请求位置与朝向。保留构造函数返回指针、中心数据别名及回调后的重读。
高度按distance/step_length、乘rise、加base的顺序逐次舍入，直行步长256，斜行步长362.03867196751236。新增整数长除法保留余数，精确模拟24/53/64位精度和四种舍入模式，不依赖宿主double的默认舍入。最后使用原独立转换控制字，原版默认向零转换。两条高度入口分别保留预先装入的坐标寄存器、原基准高度字段、输出位置及栈恢复。
2. ground_internal_next.h/.c：Advance 4A166A五处完整样本入口，剩余推进量减7采用32位回绕，保留零坐标与首样本哨兵规则；其余重叠入口仍通过既有尾调用到同一入口。Prepare 4A32B4两处重置预算、方向8连接分支、相邻格构造与桥层过渡。构造/查询后重新读取单位、坐标、偏移表和原始桥层字节，不合并两次构造与格查询。
3. ground_passage_finish.h/.c：703AA9对象扫描后的七处最终通行收尾，覆盖既有结果、敌方可碾压、占用位、盟友、碾压能力、列车与武器清障结果0/2/5/7。车辆和武器服务各保留原两次查询，第二次的返回值重新读取。完整非易失寄存器和栈收尾与原版一致。
runtime/ground_progress_bridge.h/.c集中保存旧布局和调用约定；三个业务模块没有固定游戏地址。正式记录器、schema12和两个公共比较器保持原字节。

二、逐部分验收及回退
三部分各通过默认遭遇战901帧、三格包围101帧、默认规则预算901帧、双向隧道各501帧及出口占用501帧，共6场景3406帧。
{part_identities}
每个回退点均含全部263项编译输入、源码清单、程序及场景验收。最终程序与passage回退点身份完全相同，空操作构建刷新0；160个C源、263项内容输入逐项一致。最终默认、预算及生产隧道场景使用最后部分的同一程序和原始验收轨迹，不复用旧候选的结果。

三、严格验收
最终33个生产场景18303帧严格一致；另默认规则构造AI预算901帧、独立隧道观察2505帧。命令、随机数、有序内部查询、缺帧与坐标负控均通过；辅助菜单/非法命令等门禁通过。
80组原版片段、数值及ABI检查通过；本批491520例：接近点32768、高度推进393216、内部接续32768、最终对象通行32768。高度覆盖12种运算控制字与4种转换舍入组合、两种步长及两个入口；其余探针包含中心别名、单位替换、偏移表修改、构造返回别名与重复查询副作用。初期适配探针的预载寄存器和转换控制字差异已在接入生产前修正，原始失败记录保存在investigations及native-progress-development.json；不是最终实景遗留差异。
独立观察程序仅替换4个测试对象，原版在4A1470/4A1564/6FAFE1/6FAEB4以及本批6FABAA/6FAD1C/6FAE1D挂只读记录，C在对应服务点记录。保全寄存器、标志和x87/SSE状态。五个隧道场景均直接命中新接近点、跨路点高度及普通高度推进；正式与观察程序的全部状态及原有事件一致，仅排除新增观察记录。具体次数、帧和坐标见connection-real-scenes.json。
原有等高双向隧道正常出口仍在211帧命中；占用场景170帧用正常服务构造16辆真实车，不显式重寻路，211..255帧45次进入占用分支，256帧完成出口，257帧采样速度恢复1.0，最终到达80,114并清空目标。
新增两张地图只修改74..83、108..120区域的合法高度记录：东侧高度层6、西侧4。上坡首次落位高度436、下坡604，最终分别到达高度624/416；上坡211帧出口，下坡220帧出口，原版与C一致。独立观察点的高度范围上行416..611、下行411..624，最终落在目标地面624/416；保持原版下行短暂低于目标地面的行为。没有运行时直接改坐标、高度、路径或预算。
默认步兵第28帧X=17343、三格第52帧、转弯197帧、二次补建失败399帧、持续失败451..1111帧门槛保持通过。默认预算场景规则未改，真实AI TRUCKA与16辆敌车通过正常服务构造，27..37帧10..0，第38帧清空停止；未直接写预算、路径、目标，不称为未经干预的随机对局，4C3895尚未独立挂钩。

四、保存与边界
旧v9..v23正式归档、本批baseline及三个回退点逐项哈希核验；H盘20项原始输入、原游戏/SAV和旧手写C引擎保留。最终精确清单以source-manifest.json为准，全部263项编译输入在final-source归档，final-check.json绑定报告与程序。
完整6FAA30隧道函数、Advance、Prepare、整体对象通行和全游戏等价仍未完成，37个未实现保护保留。新对象分类收尾的人工边界以原版片段检查为主，没有宣称其全部分支都在本批实景独立命中。新增高差实景采用直线路径，斜行高度主要由原版片段探针覆盖。不同保存路段指针等罕见分支仍需另补实景。
下一步优先隧道入口距离/朝向准备与横向推进接续，再整理其余Advance/Prepare模板和对象通行入口，继续六组逐部分门禁及独立双向/出口占用观察。
完成后本地提交，不推送；父提交bd57d68a0f68b5a5a3e894ff43ca8f00d0e87ded。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第二十三批正式验收交接（2026-10-22）
正式代次23 / 验证轮次24：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
本批：隧道6FABAA接近点、6FAD1C/6FAE1D高度及收尾；Advance 4A166A五处样本入口；Prepare 4A32B4两处相邻格/桥层准备；703AA9七处对象通行最终分类。业务位于ground_tube_progress、ground_internal_next、ground_passage_finish，适配在ground_progress_bridge。
三部分各6场景3406帧、各有完整263项编译输入及程序回退。最终33场景18303帧，另预算901帧、独立观察2505帧；80组检查，本批491520例原版片段对照。新接近点及两种高度分支在五个隧道实景中直接命中（含双向非零高差），正式与观察程序状态及既有事件一致。
报告：{report}
旧基线baseline；回退parts/travel-verified、internal-verified、passage-verified；最终final-source、source-manifest.json和final-check.json。最终程序与passage回退一致，160个C源、263项输入，空操作刷新0。
默认规则预算为正常服务构造的真实AI/敌车，27..37帧10..0，第38帧清空停止；未测随机对局频率及4C3895独立挂钩。出口占用211..255帧等待、256帧出口、257帧恢复，最后到达80,114。
下一步隧道入口距离/朝向、横向推进接续、余下Advance/Prepare模板与对象通行入口。完整模块和全游戏等价尚未完成，37个保护保留。
保留旧归档与全部回退；本地提交，不推送。父提交bd57d68。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
write_existing(guide,f'''第二十三批当前状态（2026-10-22，优先于历史描述）

ground_tube_progress：按原查询顺序构造接近点，并使用整数长除法及原精度/舍入控制完成两条高度推进。原转换控制字独立于运算控制字；默认向零，不能直接改用宿主double表达式。
ground_internal_next：Advance完整样本入口与Prepare相邻格/桥层准备。回调后重读单位、坐标和偏移数据，保留首样本哨兵及推进量的32位回绕。
ground_passage_finish：对象扫描后按占用、盟友、碾压、列车及武器结果收尾；重复服务查询不能合并。地址和布局集中在ground_progress_bridge。
三部分各6场景3406帧；最终33场景18303帧，另预算901帧与独立隧道观察2505帧。80组检查、本批491520例原版片段对照。完整隧道函数、Advance/Prepare、对象通行及全游戏等价仍未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
write_existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第二十三批正式接续：{handoff}\n接近点、高度推进、内部样本/桥层接续及对象通行收尾已整理。33场景18303帧+预算901帧+独立观察2505帧、80组检查通过；三部分各6场景3406帧并保存完整回退。\n下一步隧道入口距离/朝向、横向推进及其余内部模板和对象通行入口。全游戏等价尚未完成。本地提交，不推送。\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86可读单位移动完成第二十三批正式验收。隧道接近点/高度、Advance/Prepare内部接续及对象通行收尾通过；33场景18303帧，另预算901帧、独立观察2505帧及80组检查。入口为[第二十三批交接](交接文档-单位移动第二十三批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续隧道入口、横向接续及其余内部模板；全游戏等价未完成，基线和回退保留。\n'
write_existing(readme,''.join(lines))
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(name).relative_to(R).as_posix() for name in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v24*') if p.is_file())
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
validation=dict(passed=True,formal_baseline_generation=23,verification_round=24,exe_sha256=digest,state_schema=12,
 part_checkpoints={name:dict(validation=str(S/'parts'/name/'validation.json'),exe_sha256=value['exe_sha256'],scenes=len(value['scenes']),frames=sum(x['frames'] for x in value['scenes'])) for name,value in parts.items()},
 final_build_inputs_match_passage_checkpoint=True,
 paired_scenes=paired_scenes,paired_frames=paired_frames,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 independent_connection_observer_scenes=observer_scenes,independent_connection_observer_frames=observer_frames,probes=80,new_fragment_cases=new_cases,
 source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,frame_comparison_passed=True,
 default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],source_files=len(manifest),production_c_sources=160,
 content_inputs=263,preservation=preservation,unsupported_guards=37,tube_approach_runtime_verified=True,tube_height_runtime_verified=True,new_rare_branch_runtime_hits_independently_recorded=True,
 rare_branch_evidence_scope=connections['scope'],all_rare_branches_verified=False,alternate_saved_segment_pointer_real_scene_verified=False,
 connection_runtime_evidence=str(S/'connection-real-scenes.json'),report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=23,verification_round=24,
 paired_scenes=paired_scenes,paired_frames=paired_frames,probes=80,new_fragment_cases=491520,production_c_sources=160,content_inputs=263,
 report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),**flags)
recovery.update(next_readable_region='Tube entry distance/heading and horizontal progression handoffs, remaining Advance/Prepare templates and object passage entry services; preserve six per-part real gates and independent tube branch observations',
 previous_recovery_validation=str(R/'evidence/movement-state-v23/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),tube_approach_runtime_verified=True,tube_height_runtime_verified=True,new_rare_branch_runtime_hits_independently_recorded=True,
 rare_branch_evidence_scope=connections['scope'],connection_runtime_evidence=str(S/'connection-real-scenes.json'),all_rare_branches_verified=False)
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=paired_scenes,paired_frames=paired_frames,
 independent_default_budget_frames=901,independent_connection_observer_frames=observer_frames,passed=True,strict_ordered_audit_passed=True,
 first_difference=None,full_original_equivalence_verified=False,normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=23,verification_round=24,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True,formal_baseline=23,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
