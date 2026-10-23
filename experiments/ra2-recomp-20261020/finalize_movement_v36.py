"""Promote generation35 after part checkpoints, native gates and mixed-bridge acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v36';O=R/'evidence/movement-state-v35';T=R/'evidence/movement-state-v34'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,t):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n';p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
vcs=read(S/'vcs-context.json')
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()==vcs['parent_commit']=='dfe36a1d1d816e7cd57b8908646ad0f771b1f694'
assert sha(P/'.git/config')==vcs['config_sha256']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
accept=read(S/'strict-acceptance.json');native=read(S/'native-gates.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==120
assert read(S/'native-round36-identity.json')['passed']
assert native['passed'] and native['groups']==120 and native['new_cases']==196608
evidence={n:read(S/n) for n in ['budget-real-scenes.json','connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','legal-overlap-sources.json','alias-route-inventory.json','overlap-caller-identity.json','recipe-byte-audit.json','bridge-hostile-real-scenes.json','bridge-infantry-real-scenes.json','progress-estimate.json','inherited-fixtures.json','new-fragment-contract.json','north-query-real-scenes.json']}
evidence.update({n:read(S/n) for n in ['internal-alias-sources.json','alias-natural-scenes.json','bridge-occupied-real-scenes.json','alias-occupied-natural-scenes.json','bridge-detour-real-scenes.json']})
evidence['bridge-staggered-real-scenes.json']=read(S/'bridge-staggered-real-scenes.json')
assert evidence['bridge-staggered-real-scenes.json']['passed'] and evidence['bridge-staggered-real-scenes.json']['production_executable_sha256']==digest
evidence['production-scene-totals.json']=read(S/'production-scene-totals.json')
assert evidence['production-scene-totals.json']['production_scenes']==67 and evidence['production-scene-totals.json']['production_frames']==45637
assert evidence['production-scene-totals.json']['production_executable_sha256']==digest
delegated=read(S/'delegated-combined-scenes.json');assignment=read(S/'observer-lane-assignment.json')
assert delegated['passed'] and delegated['job']=='combined-scenes' and delegated['completed_on_freed_core_lane'] and delegated['max_scene_lanes']==2 and delegated['max_game_processes']==4
assert sha(R/delegated['runner'])==delegated['runner_sha256'] and assignment['delegated_jobs']==['combined-scenes']
structure=read(S/'refactor-structure.json');assert structure['passed'] and structure['compile_inputs']==292
assert structure['sample_anchor_internal_entries']==12 and structure['moving_tail_internal_entries']==3
assert structure['advance_service_exit_entries']==2 and structure['advance_service_exit_copies']==14
assert structure['remaining_destination_copies_connected']==4 and structure['enemy_contact_internal_copies']==3 and structure['following_service_copies']==20
assert structure['destination_internal_copies']==24 and structure['allied_relation_internal_copies']==3 and structure['prepare_stop_service_copies']==2
assert structure['register_sample_internal_copies']==8 and structure['enemy_weapon_internal_copies']==3 and structure['owner_stop_service_copies']==7
assert structure['register_destination_internal_copies']==12 and structure['confirmed_building_internal_copies']==3 and structure['placement_restore_service_copies']==13
assert structure['loaded_sample_internal_copies']==8 and structure['terrain_weapon_internal_copies']==3 and structure['invalidate_service_copies']==11
assert evidence['bridge-detour-real-scenes.json']['production_executable_sha256']==digest
assert evidence['bridge-occupied-real-scenes.json']['production_executable_sha256']==digest
for name,v in evidence.items():
    assert v['passed'],name
    for item in v.get('inputs',[]):assert sha(R/item['path'])==item['sha256'],(name,item['path'])
for name in ['connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','bridge-hostile-real-scenes.json','bridge-infantry-real-scenes.json','north-query-real-scenes.json']:
    assert evidence[name]['production_executable_sha256']==digest,name
assert evidence['budget-real-scenes.json']['formal_executable_sha256']==digest
assert evidence['connection-real-scenes.json']['original_equivalent_stall_scenes']==2
assert not evidence['connection-real-scenes.json']['all_curved_height_routes_complete']
assert evidence['bridge-real-scenes.json']['actual_ordered_three_object_traversal_verified']
mixed=evidence['bridge-mixed-real-scenes.json'];assert mixed['mixed_runtime_classes_verified'] and mixed['opposing_bridge_traffic_verified']
assert not mixed['nonprimary_natural_entry_proved']
assert not evidence['internal-real-scenes.json']['nonprimary_overlapping_adapter_naturally_observed']
assert not evidence['overlap-caller-identity.json']['nonprimary_overlapping_adapter_naturally_observed']
alias_runtime=evidence['alias-natural-scenes.json'];assert alias_runtime['passed'] and alias_runtime['static_aliases']==29
assert alias_runtime['additional_observer_frames']==3604 and not alias_runtime['nonprimary_natural_entry_proved']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==171 and len(receipt['inputs'])==292 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,h in receipt['inputs'].items():assert sha(Path(name))==h,name
for rel in ['run_fixture_comparison.py','run_state_comparison.py','ra2/src/runtime/state_trace.c']:
    assert (R/rel).read_bytes()==(S/'baseline'/rel).read_bytes(),rel
for filename,nl in [('recomp_0010.c','LF'),('recomp_0046.c','CRLF')]:
    p=R/'ra2/src/recomp/gen_game'/filename;raw=p.read_bytes();assert (b'\r\n' not in raw) if nl=='LF' else raw.count(b'\n')==raw.count(b'\r\n')
    before=(S/'baseline/ra2/src/recomp/gen_game'/filename).read_text(encoding='utf-8');after=p.read_text(encoding='utf-8')
    for pattern in [r'^L_[0-9A-F]+:',r'case (0x[0-9A-Fa-f]+u): goto',r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)']:
        assert re.findall(pattern,before,re.M)==re.findall(pattern,after,re.M),(filename,pattern)
guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (R/'ra2/src/recomp/gen_game').glob('*.c'));assert guards==37
parts={n:read(S/'parts'/n/'validation.json') for n in ['template-verified','passage-verified','returns-verified']}
for n,v in parts.items():assert v['passed'] and len(v['scenes'])==6 and sum(x['frames'] for x in v['scenes'])==3406,n
assert parts['returns-verified']['exe_sha256']==digest
archived={e['path']:e['sha256'] for e in read(S/'parts/returns-verified/manifest.json')}
for path,h in receipt['inputs'].items():assert archived[Path(path).relative_to(R).as_posix()]==h,path
for identity in S.glob('native-*-identity.json'):
    v=read(identity);assert v['passed']
    for item in v['inputs']+v.get('probe_executables',[])+([v['probe_executable']] if 'probe_executable' in v else []):assert sha(R/item['path'])==item['sha256'],(identity,item['path'])
assert read(S/'native-round31-identity.json')['total_cases']==196608 and read(S/'native-round32-identity.json')['total_cases']==196608
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,36)]
archives += [('v36-baseline',S/'baseline','source-manifest.json','')]
archives += [(name,S/'parts'/name,'manifest.json','') for name in parts]
for label,base,manifest_name,sub in archives:
    entries=read(base/manifest_name)
    for item in entries:assert sha(base/sub/item['path'])==item['sha256'],(label,item['path'])
    counts[label]=len(entries)
for item in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/item['name'])==item['sha256'],item['name']
counts['H_originals']=20
for p,h in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),(R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),(P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==h,str(p)
extra=read(S/'baseline/extra/receipt.json');assert sha(R/extra['path'])==sha(S/'baseline/extra/internal-alias-sources.json')==extra['sha256']
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:assert (P/'reports'/name).read_bytes()==(S/'baseline/project/reports'/name).read_bytes()
preservation=dict(passed=True,counts=counts,unsupported_guards=37,original_inputs_save_old_engine_preserved=True);write(S/'preservation.json',preservation)
startup=read(S/'startup-failures.json');assert startup['passed']
for attempt in startup['attempts']:
    assert attempt['simulation_frames']==0
    for item in attempt['preserved_files']:assert sha(Path(attempt['preserved_path'])/item['path'])==item['sha256']
    assert read(S/'runs'/attempt['tag']/'comparison.json')['passed']
prelaunch=read(S/'prelaunch-failures.json');assert prelaunch['passed']
for attempt in prelaunch['attempts']:
    assert not attempt['game_launched'] and attempt['simulation_frames']==0 and sha(R/attempt['log'])==attempt['sha256']
    assert read(S/'runs'/attempt['tag']/'comparison.json')['passed']
preservation['prelaunch_path_refusals_preserved']=len(prelaunch['attempts'])
trial_receipts=['occupied-open-lane/receipt.json','south-initial-scan/receipt.json','south-subcells/range-rejection/receipt.json','south-subcells/range-rejection-02/receipt.json']
for rel in trial_receipts:
    receipt_path=T/'investigations'/rel;trial=read(receipt_path);assert trial['passed']
    for item in trial['files']:assert sha(receipt_path.parent/item['path'])==item['sha256'],(rel,item['path'])
producer=read(T/'investigations/south-initial-scan/producer-recovery.json');assert producer['passed'] and sha(T/'investigations/south-initial-scan'/producer['path'])==producer['producer_sha256']
old_south=next(v for v in read(T/'investigations/south-initial-scan/bridge-occupied-fixtures.json')['fixtures'] if v['name']=='south')
assert sha(T/'investigations/south-initial-scan/fixtures/bridge-occupied-south.MAP')==old_south['sha256']
preservation['nonqualifying_trial_receipts_preserved']=len(trial_receipts)
cleanup=read(O/'cleanup.json');assert cleanup['passed'] and cleanup['deleted_files']==2428 and cleanup['deleted_bytes']==29649646
cleanup_plan=read(O/'cleanup-plan.json');assert all(not (R/e['path']).exists() for e in cleanup_plan['files'])
preservation['previous_cleanup_verified']=True;preservation['cleanup_performed_this_round']=False
for trial in [S/'investigations/template-build-01/receipt.json']:
    v=read(trial);assert v['passed']
    for e in v['files']:assert sha(trial.parent/e['path'])==e['sha256']
preservation['original_preframe_startup_failures_preserved']=len(startup['attempts']);write(S/'preservation.json',preservation)
run_dirs=[p for p in (S/'runs').iterdir() if p.is_dir()]
assert all((p/'comparison.json').exists() for p in run_dirs)
assert {p.name for p in run_dirs if not read(p/'comparison.json')['passed']}==set()
report=P/'docs/单位移动第三十五批-寄存器目标与建筑门槛及桥上错峰交通组合-20261023.txt'
handoff=P/'交接文档-单位移动第三十五批正式验收-20261023.txt';assert not report.exists() and not handoff.exists()
hostile=evidence['bridge-hostile-real-scenes.json'];assert hostile['hostile_classifier_observed'] and hostile['hostile_bridge_traffic_observed']
body=f'''单位移动第三十五批正式验收（2026-10-23）
正式代次35 / 验证轮次36
父提交：{vcs['parent_commit']}
程序：{exe}
SHA-256：{digest}
证据：{S}

第三十四批dfe36a1及程序1ad182016315f10abe0446f84ce2e1792a3e1474f0dc97e3762780d82d9e2ef1、5317项源封存和干净工作区先核对通过。完整baseline、旧程序与三份回退均保留。

内部模板：4A24F4十二处地图查询接续使用传入ECX/EDX/EBX坐标，保留既有局部接续标签，服务后重读owner；65536例覆盖符号边界、不同栈内缓存和回调写回。
具体对象：703A7F三处共用已确认建筑的1350标志门槛，不重复查询kind；65536例覆盖非布尔标志和INT32两端的通行分类。
服务出口：4A2607十三处共用定位服务及对象74字节恢复。65536例让回调改owner、局部坐标与保存槽，恢复目标可别名到已弹出的EDI/ESI/EBP及尚未弹出的EBX槽，按原顺序恢复。
六项生产源改动；七项相关源、三项探针（其中两项扩展）与观察器从baseline独立重放。未增加原生分派入口，旧标签、指令注解、尾部和37处保护均保留。
每部分六场3406帧，默认901、短包围101、独立AI预算901、双向隧道各501及出口占用501；状态、RNG和有序事件相同。回退身份：
'''+''.join(n+' : '+v['exe_sha256']+'\n' for n,v in parts.items())+f'''

最终120组原版片段门禁通过，含既有117组重跑及本轮196608例。67场生产45637帧，旧65场43835帧和新两场1802帧分组求和；探针、独立观察、短检查与探索不重复算生产。
独立默认预算901、内部观察4054、连接及高差占用9116、桥观察23场20723帧。原入口观察3604与新错峰交通入口观察5406帧单列。
组合验证复用已结束的主队列，且等待入口观察完成后才启动；总并发最多两路、四个游戏进程。分配和完成记录见observer-lane-assignment.json及delegated-combined-scenes.json。
171个C源、292项内容输入；最终构建刷新0，与returns回退相同。公共比较器、schema12、CPU/FPU保存方式、0010 LF和0046 CRLF保持。67份旧地图/规则逐字节继承，新两份地图为旧占用地图的普通副本，只改变正常命令时序。

桥上错峰交通：主车和E2仅第5帧一次对向移动；两辆出口占位车先按正常指令到达，随后第一辆北向210/南向226帧离开，第二辆北向240/南向256帧离开。核对移动交会中的实际关系与几何查询、占位车查询、出口附近等待、两占用车道外绕行，以及主车和第一占位车同时移动而第二辆仍在占位的过程。没有写路径、链指针、运动或桥层；到达结果独立记录。
新场景结果：{ {n:v['modes']['original'] for n,v in evidence['bridge-staggered-real-scenes.json']['scenes'].items()} }
旧持占用到600帧绕行、300/320清空及重发指令、友敌交通、混类对象链、高差占用和异常组合均重跑。旧占用组主车在清空前即绕行，不能称等待清空后自动恢复。

原28个非主别名继续核查，并因4A2607的第十三份父副本新增4A24F0候选，共29个非主别名和三个主入口。{evidence["internal-alias-sources.json"]["unique_native_edges"]}条原生入边逐字节核对。新增六场错峰交通观察分组覆盖全部29候选，新4A24F0同时配置南北两个场景，三个主入口均有正控，未观察到非主C副本合法自然首次调用；并非每候选每方向穷尽。内部边界命中不等于独立C入口。任意计算目标、运行时指针与未覆盖场景仍未排除。
原版4→6上行停滞、7→4下行至-193异常保持，只算异常一致性；既有成功高差占用另行保留。
本轮模板首次编译因四个副本的旧局部标签未连接而被拒绝，模拟0帧；修正配方和源码后通过。原片段探针首次在沙箱启动前因WinError623被拒绝，模拟0帧，环境外按同一程序重试通过。原失败源码、日志与记录保留在investigations/template-build-01。游戏首帧前失败{len(startup['attempts'])}，公共路径检查拒绝{len(prelaunch['attempts'])}。v34旧试验及v35失败记录原地保留。

基线与范围：v9..v35旧封存、本批5317项baseline及三份parts逐项核对。H盘原版允许列表20项、D盘原游戏、SAV与旧手写引擎哈希保持；没有扩大为整个H盘核对。本轮没有删除数据，上一批批准删除的2428个可再生obj继续不存在，旧清理记录保留。

进度估算：{read(S/'progress-estimate.json')['summary_zh']}
剩余工作：{read(S/'progress-estimate.json')['remaining_zh']}
估算权重、证据、区间和限制见progress-estimate.json。通过组数、生成C行数和批次数不是完成率；完整移动、对象分类和全游戏等价均未完成。
完成后只本地提交、不推送。下批先只读运行verify_final_movement_v36.py，再保存新回退；不要原地重跑本轮封存写入脚本。
'''
report.write_text(body,encoding='utf-8',newline='\n');handoff.write_text(body+'\n接手先运行verify_final_movement_v36.py，再保存下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';existing(guide,f'第三十五批当前状态（2026-10-23）\n寄存器目标、建筑门槛、定位回写出口；各部分六场3406帧。67场45637帧、120组门禁，敌我桥交通通过。完整移动和非主自然入口仍未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动第三十五批：寄存器目标、建筑门槛与定位回写出口；67场景45637帧、120组片段门禁，桥上移动步兵/车辆交会与敌我交通通过。入口为[第三十五批交接](交接文档-单位移动第三十五批正式验收-20261023.txt)和 `reports/latest-recovery.json`。基线、回退与原版异常保留；非主入口及全游戏等价未完成。\n';existing(p,''.join(lines))
p=P/'交接文档-新对话继续推进-20261022.txt';existing(p,f'最新接续：第三十五批已验收，正式35 / 验证36。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R/"verify_final_movement_v36.py"}\n以下历史保留。\n\n'+p.read_text(encoding='utf-8'))
p=P/'交接文档-原版逆向与C重编译-20261020.txt';existing(p,p.read_text(encoding='utf-8')+f'\n2026-10-23 第三十五批接续：{handoff}\n67场景45637帧，120组片段门禁；敌我桥交通实景通过，非主自然入口仍未证明。\n')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v36*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ['.c','.h','.asm'] or p.name in ['truck-actor-fixture-probe.exe','connection-fixture-probe.exe','connection-fixture.map','truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[]
for rel in sorted(paths):
    dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(R/rel)))
write(S/'source-manifest.json',manifest)
for document in [report,handoff]:
    with document.open('a',encoding='utf-8') as stream:stream.write(f'\n最终源封存：{len(manifest)}项。当前身份以validation.json/source-manifest.json为准。下一轮必须保留内容构建、独立观察器重建、结构/配方、原版片段和生产逐帧门禁，不能仅替换脚本后缀。\n')
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')};flags.update(four_destination_copies_shared_readable=True,enemy_contact_internal_shared_readable=True,following_service_exits_shared_readable=True,template_destination_internal_readable=True,allied_relation_internal_shared_readable=True,prepare_stop_service_exits_shared_readable=True,template_remainder_index_shared_readable=True,concrete_enemy_kind_shared_readable=True,service_bearing_prepare_exits_shared_readable=True,sample_anchor_internal_readable=True,moving_object_tail_shared_readable=True,advance_service_exits_shared_readable=True)
flags.update(register_destination_internal_shared_readable=True,confirmed_building_internal_shared_readable=True,placement_restore_service_shared_readable=True,register_sample_internal_shared_readable=True,enemy_weapon_internal_shared_readable=True,owner_stop_service_shared_readable=True,loaded_sample_internal_shared_readable=True,terrain_weapon_internal_shared_readable=True,invalidate_service_exits_shared_readable=True)
validation=dict(passed=True,formal_baseline_generation=35,verification_round=36,exe_sha256=digest,state_schema=12,paired_scenes=67,paired_frames=45637,probes=120,new_fragment_cases=196608,
    scene_queue_limit=2,game_process_limit=4,delegated_combined_evidence=str(S/"delegated-combined-scenes.json"),production_c_sources=171,content_inputs=292,source_files=len(manifest),unsupported_guards=37,cleanup_performed_this_round=False,previous_cleanup_receipt=str(O/'cleanup.json'),final_build_inputs_match_returns_checkpoint=True,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    independent_default_budget_frames=901,independent_internal_observer_frames=4054,independent_connection_observer_frames=9116,independent_bridge_observer_frames=20723,
    independent_alias_observer_frames=9010,independent_prior_alias_observer_frames=3604,independent_staggered_alias_observer_frames=5406,legal_alias_sources_examined=29,new_alias_runtime_probe_targets=19,legacy_alias_sources=28,new_alias_sources_this_round=["004A24F0"],current_natural_scene_probe_targets=29,
    north_meeting_dynamic_relation_query_verified=True,north_query_runtime_evidence=str(S/'north-query-real-scenes.json'),progress_estimate=str(S/'progress-estimate.json'),bridge_moving_infantry_vehicle_query_verified=True,bridge_infantry_runtime_evidence=str(S/'bridge-infantry-real-scenes.json'),bridge_upper_and_lower_three_object_traversal_verified=True,bridge_mixed_object_chain_verified=True,bridge_opposing_dynamic_traffic_verified=True,bridge_hostile_dynamic_traffic_verified=True,
    bridge_staggered_exit_verified=True,bridge_staggered_exit_runtime_evidence=str(S/'bridge-staggered-real-scenes.json'),bridge_multiobject_scenes=23,bridge_multiobject_frames=20723,bridge_held_exit_detour_scenes=2,bridge_held_exit_detour_frames=1802,bridge_held_exit_detour_verified=True,bridge_held_exit_detour_runtime_evidence=str(S/'bridge-detour-real-scenes.json'),bridge_meeting_occupied_scenes=2,bridge_meeting_occupied_frames=1802,bridge_meeting_occupied_verified=True,bridge_meeting_occupied_runtime_evidence=str(S/'bridge-occupied-real-scenes.json'),
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    bridge_runtime_evidence=str(S/'bridge-real-scenes.json'),bridge_hostile_runtime_evidence=str(S/'bridge-hostile-real-scenes.json'),bridge_mixed_runtime_evidence=str(S/'bridge-mixed-real-scenes.json'),legal_overlap_sources=str(S/'internal-alias-sources.json'),
    alias_runtime_evidence=str(S/'alias-natural-scenes.json'),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),original_preframe_startup_failures_preserved=len(startup['attempts']),
    rare_branch_evidence_scope=evidence['connection-real-scenes.json']['scope']+' '+hostile['scope']+' '+mixed['scope']+' '+alias_runtime['limits'],
    combined_curved_height_occupied_runtime_verified=True,combined_curved_height_occupied_scenes=4,original_equivalent_stall_scenes=2,all_curved_height_routes_complete=False,
    nonprimary_overlapping_adapter_naturally_observed=False,full_original_equivalence_verified=False,strict_ordered_audit_passed=True,frame_comparison_passed=True,
    default_rules_full_budget_exhaustion_verified=True,budget_scope=evidence['budget-real-scenes.json']['scope'],preservation=preservation,report=str(report),handoff=str(handoff),**flags)
write(S/'continuation.json',dict(status='validation_complete_commit_separately_audited',validation=str(S/'validation.json'),verify=str(R/'verify_final_movement_v36.py'),exe_sha256=digest,commit_policy='local commit only; never push'))
write(S/'validation.json',validation);accept.update(paired_scenes=67,paired_frames=45637,**flags);write(S/'strict-acceptance.json',accept)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update({k:v for k,v in validation.items() if k not in ['exe_sha256','source_files','part_checkpoints','preservation']})
for k in ['system_interruption_recovered','interrupted_pairs_preserved','resumption_evidence','serial_startup_retries_passed']:recovery.pop(k,None)
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),next_readable_region='Remaining loaded-table and register-sourced template continuations and other internal copies; concrete object/locomotor and service side effects; broader bridge traffic and service side effects and legal computed alias sources')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(passed=True,validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=67,paired_frames=45637,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=35,verification_round=36,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(exe),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff)))
print(json.dumps(dict(passed=True,formal_baseline=35,exe_sha256=digest,source_files=len(manifest))))
