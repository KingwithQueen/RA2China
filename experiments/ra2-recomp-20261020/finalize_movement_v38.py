"""Promote generation37 after part checkpoints, native gates and mixed-bridge acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v38';O=R/'evidence/movement-state-v37';T=R/'evidence/movement-state-v34'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,t):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n';p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
vcs=read(S/'vcs-context.json')
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()==vcs['parent_commit']=='6a948c6763d1ec5ce5e9e0911b1620bcf6f53950'
assert sha(P/'.git/config')==vcs['config_sha256']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
accept=read(S/'strict-acceptance.json');native=read(S/'native-gates.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==126
assert read(S/'native-round38-identity.json')['passed']
assert native['passed'] and native['groups']==126 and native['new_cases']==196608
evidence={n:read(S/n) for n in ['budget-real-scenes.json','connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','legal-overlap-sources.json','alias-route-inventory.json','overlap-caller-identity.json','recipe-byte-audit.json','bridge-hostile-real-scenes.json','bridge-infantry-real-scenes.json','progress-estimate.json','inherited-fixtures.json','new-fragment-contract.json','north-query-real-scenes.json']}
evidence.update({n:read(S/n) for n in ['internal-alias-sources.json','alias-natural-scenes.json','bridge-occupied-real-scenes.json','alias-occupied-natural-scenes.json','bridge-detour-real-scenes.json']})
evidence.update({n:read(S/n) for n in ['bridge-neighbor-release-real-scenes.json','bridge-neighbor-release-motion.json']})
assert evidence['bridge-neighbor-release-real-scenes.json']['production_executable_sha256']==digest
evidence['bridge-lane-release-motion.json']=read(S/'bridge-lane-release-motion.json')
evidence['bridge-lane-release-real-scenes.json']=read(S/'bridge-lane-release-real-scenes.json')
assert evidence['bridge-lane-release-real-scenes.json']['passed'] and evidence['bridge-lane-release-real-scenes.json']['production_executable_sha256']==digest
evidence['bridge-staggered-real-scenes.json']=read(S/'bridge-staggered-real-scenes.json')
assert evidence['bridge-staggered-real-scenes.json']['passed'] and evidence['bridge-staggered-real-scenes.json']['production_executable_sha256']==digest
evidence['production-scene-totals.json']=read(S/'production-scene-totals.json')
assert evidence['production-scene-totals.json']['production_scenes']==71 and evidence['production-scene-totals.json']['production_frames']==49241
assert evidence['production-scene-totals.json']['production_executable_sha256']==digest
delegated=read(S/'delegated-combined-scenes.json');assignment=read(S/'observer-lane-assignment.json')
assert delegated['passed'] and delegated['job']=='combined-scenes' and delegated['completed_on_freed_core_lane'] and delegated['max_scene_lanes']==2 and delegated['max_game_processes']==4
assert sha(R/delegated['runner'])==delegated['runner_sha256'] and assignment['delegated_jobs']==['combined-scenes']
infantry_lane=read(S/'delegated-bridge-infantry-scenes.json');assert infantry_lane['passed'] and infantry_lane['completed_on_owned_core_lane'] and infantry_lane['max_scene_lanes']==2 and infantry_lane['max_game_processes']==4
for e in infantry_lane['inputs']:assert sha(R/e['path'])==e['sha256']
structure=read(S/'refactor-structure.json');assert structure['passed'] and structure['compile_inputs']==292
assert structure['late_layer_internal_copies']==13 and structure['loaded_weapon_internal_copies']==3 and structure['leave_place_mark_service_copies']==13
assert evidence['recipe-byte-audit.json']['production_sources_changed']==4
assert evidence['inherited-fixtures.json']['reused_fixture_files']==71
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
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,38)]
archives += [('v38-baseline',S/'baseline','source-manifest.json','')]
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
cleanup=read(R/'evidence/movement-state-v35/cleanup.json');assert cleanup['passed'] and cleanup['deleted_files']==2428 and cleanup['deleted_bytes']==29649646
cleanup_plan=read(R/'evidence/movement-state-v35/cleanup-plan.json');assert all(not (R/e['path']).exists() for e in cleanup_plan['files'])
current_cleanup=read(S/'cleanup.json');plan=read(S/'cleanup-plan.json')
assert current_cleanup['passed'] and current_cleanup['protected_files_unchanged'] and current_cleanup['plan_sha256']==sha(S/'cleanup-plan.json')
assert current_cleanup['deleted_files']==len(plan['files']) and current_cleanup['deleted_bytes']==sum(e['bytes'] for e in plan['files'])
for e in plan['files']:assert not (R/e['path']).exists(),e['path']
for e in plan['protected_files']:assert sha(R/e['path'])==e['sha256'],e['path']
preservation['previous_cleanup_verified']=True;preservation['cleanup_performed_this_round']=True;preservation['current_cleanup']=current_cleanup
for trial in [R/'evidence/movement-state-v36/investigations/template-build-01/receipt.json']:
    v=read(trial);assert v['passed']
    for e in v['files']:assert sha(trial.parent/e['path'])==e['sha256']
recovery=read(S/'native-recovery.json');assert recovery['passed'] and recovery['groups']==126 and recovery['production_executable_unchanged']
for e in recovery['inputs']:assert sha(R/e['path'])==e['sha256']
trial=S/'investigations/neighbor-audit-01/receipt.json';v=read(trial);assert v['passed'] and v['simulation_failures']==0
for e in v['files']:assert sha(trial.parent/e['path'])==e['sha256']
preservation['neighbor_audit_measurement_correction_preserved']=str(trial)
trial=S/'investigations/audit-seed-01/receipt.json';v=read(trial);assert v['passed'] and v['simulation_failures']==0 and v['original_run_seed']==12345
for e in v['files']:assert sha(trial.parent/e['path'])==e['sha256']
preservation['audit_seed_correction_preserved']=str(trial)
trial=S/'investigations/native-build-01/receipt.json';v=read(trial);assert v['passed'] and v['simulation_frames']==0 and not v['game_launched']
for e in v['files']:assert sha(trial.parent/e['path'])==e['sha256']
preservation['probe_link_failure_preserved']=str(trial)
preservation['original_preframe_startup_failures_preserved']=len(startup['attempts']);write(S/'preservation.json',preservation)
run_dirs=[p for p in (S/'runs').iterdir() if p.is_dir()]
assert all((p/'comparison.json').exists() for p in run_dirs)
assert {p.name for p in run_dirs if not read(p/'comparison.json')['passed']}==set()
report=P/'docs/单位移动第三十七批-桥层写回与武器分类及桥上相邻车道放行组合-20261024.txt'
handoff=P/'交接文档-单位移动第三十七批正式验收-20261024.txt';assert not report.exists() and not handoff.exists()
hostile=evidence['bridge-hostile-real-scenes.json'];assert hostile['hostile_classifier_observed'] and hostile['hostile_bridge_traffic_observed']
body=f'''单位移动第三十七批正式验收（2026-10-24）
正式代次37 / 验证轮次38
父提交：{vcs['parent_commit']}
程序：{exe}
SHA-256：{digest}
证据：{S}

本轮先只读核对第三十六批6a948c6、程序4db5d31b232480adb2f7aa7142e71add8d3721bf4b75c9b21bdf17c882487c73、5980项封存和干净工作区；完整baseline、旧程序和三部分回退保留。
内部模板：4A25A0桥层写回共十三段（八处原生标签、五处嵌入段），复用纯C桥层判断，保持已取格子指针、符号高度与重复读取标志顺序。65536例覆盖全部有符号高度字节组合和写回与标志/保存指针重叠；不新增原生入口。
具体对象：703A45三处从已载入武器检查可空弹头及146字节，复用已验纯C分类，不重选武器或查询kind。65536例包含空弹头、256种字节值和有符号通行边界，零服务调用。
共享出口：4A2586十三处离格11C(0)→定位19C→桥层写回→进入11C(1)→Advance出栈。首次使用入口ECX，后续在回调后重读owner和两个格子；65536例检查回调改换owner、坐标、格子、保存槽及返回EAX。
四项生产C源改动；七项相关源、三项探针、观察器和两份新地图由基线独立重放，逐字节相同。旧标签、指令注解、尾部、37处保护保留。
每部分六场3406帧：默认901、短包围101、独立预算901、双向隧道各501及出口占用501。状态、RNG和有序事件逐帧一致。三部分封存回退：
'''+''.join(n+' : '+v['exe_sha256']+chr(10) for n,v in parts.items())+f'''
最终126组原版片段门禁通过，旧123组重跑，本轮新增196608例。生产共71场49241帧（原69场47439帧及新两场1802帧）。独立默认预算901、内部4054、连接及高差占用9116、桥观察27场24327帧；入口观察3604+5406帧单列，不重复计入生产。
最多两路、四个游戏进程；步兵桥八组接到核心观察路末尾，核心完成标记在这些配对之后才发出；桥路跳过该组后继续入口观察。编译/探针构建串行。171个C源、292项内容输入，最终刷新0且与returns回退一致。公共比较器、schema12、CPU/FPU方式和0010 LF、0046 CRLF保持。71份既有地图/规则逐字节继承，新两份地图为普通地图副本，只改变正常命令时序。

新增桥组合：主车与E2在第5帧各一次对向移动；两普通占位车先到桥出口。北210/南226帧放行61列相邻车道，60列主车道占位车到北420/南436帧才收到离开命令。必须从实际逐帧位置确认相邻车先运动、主车绕行跨出口时主车道仍占用，并同时存在主车与早放行占位车的动态交通。放行命令、实际开始运动、跨出口和到达分别记录；没有写入路径、链、运动或桥层。
新增结果：{ {n:v['modes']['original'] for n,v in evidence['bridge-neighbor-release-real-scenes.json']['scenes'].items()} }
实际放行运动：{evidence['bridge-neighbor-release-motion.json']['scenes']}
旧主车道先放行、错峰放行、持续占用到600帧、300/320清空与重发、友敌混类、移动步兵和弯曲高差出口占用全部重跑。旧主车道先放行的命令到实际运动延迟仍按原版保留，不将命令发出当作车道清空。

29个非主C副本及三个主入口继续核查；{evidence['internal-alias-sources.json']['unique_native_edges']}条原生入边逐字节核对。新组合六场观察覆盖29候选，4A24F0配置南北向，主入口正控均须出现。未观察到非主C副本合法自然首次调用；不是每个候选在每个方向穷尽，计算目标、运行时指针和未跑场景仍待核。原生内部跳转不等于独立C首次调用。
原版4→6上行停滞和7→4下行到-193异常保留，4→7和6→4完成组单列；曲线长组每场实际601帧。完整移动与全游戏等价未完成。
本轮首帧前失败{len(startup['attempts'])}，公共路径拒绝{len(prelaunch['attempts'])}；旧v34不达标试验、v35拒绝和v36首次模板编译失败原地核对保留。本轮独立探针首次漏链桥层模块的LNK2019原始配方、日志和对象存于investigations/native-build-01；只修复探针链接配方，无生产源变更，完整片段门禁随后重跑通过。新桥审计首次错误地用晚放行前的位置衡量早放行车辆，已改为分别按各自命令前的位置核验，原审计与日志保留于investigations/neighbor-audit-01；实景对照没有失败或改写。最终审计还保留audit-seed-01：更新门禁数量的前缀替换误将审计种子改为12645，实际所有运行种子仍为12345；恢复审计常量后完整重跑剩余验收，不改变程序或重做有效游戏配对。
v9..v37旧封存、5980项本轮baseline和三部分回退逐项核对；H盘允许列表20项、D盘原游戏、SAV和旧引擎指纹保持。清理仅删v36/v37根目录{current_cleanup['deleted_files']}个可再生探针obj（{current_cleanup['deleted_bytes']}字节），其余{current_cleanup['protected_files']}个文件逐项未变；不含fixture链接对象、程序、日志、轨迹和封存。v35已批准清理记录及旧2428项缺失状态保持。

剩余：{read(S/'progress-estimate.json')['remaining_zh']}
本轮没有重新估算百分比；旧工程估算明确标作历史，不能由批次/行数推算完成率。
完成后只本地提交，不推送。下批先只读运行verify_final_movement_v38.py，再保存新回退；不要原地重跑封存写入脚本。
'''
report.write_text(body,encoding='utf-8',newline=chr(10));handoff.write_text(body,encoding='utf-8',newline=chr(10))
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';existing(guide,f'''第三十七批当前状态（2026-10-24）
4A25A0桥层写回、703A45武器分类、4A2586离格定位出口；每部分六场3406帧，71场49241帧、126组门禁。非主自然入口与完整移动仍未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='''> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第三十七批：桥层写回、武器分类与离格定位出口；71场49241帧、126组片段门禁，桥上相邻车道先放行且主车道持续占用组合通过。入口为[第三十七批交接](交接文档-单位移动第三十七批正式验收-20261024.txt)和 `reports/latest-recovery.json`。基线、回退与原版异常保留；非主入口及全游戏等价未完成。
''';existing(p,''.join(lines))
p=P/'交接文档-新对话继续推进-20261022.txt';existing(p,f'''最新接续：第三十七批已验收，正式37 / 验证38。
先读：{handoff}
程序SHA-256：{digest}
只读核对：{R/"verify_final_movement_v38.py"}
以下历史保留。

'''+p.read_text(encoding='utf-8'))
p=P/'交接文档-原版逆向与C重编译-20261020.txt';existing(p,p.read_text(encoding='utf-8')+f'''
2026-10-24 第三十七批：{handoff}
71场49241帧，126组片段门禁；非主C自然入口仍未证明。
''')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v38*') if p.is_file())
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
flags.update(late_layer_internal_shared_readable=True,loaded_weapon_internal_shared_readable=True,leave_place_mark_service_shared_readable=True)
flags.update(loaded_destination_internal_shared_readable=True,loaded_warhead_internal_shared_readable=True,mark_enter_service_shared_readable=True)
validation=dict(passed=True,formal_baseline_generation=37,verification_round=38,exe_sha256=digest,state_schema=12,paired_scenes=71,paired_frames=49241,probes=126,new_fragment_cases=196608,
    scene_queue_limit=2,game_process_limit=4,delegated_combined_evidence=str(S/"delegated-combined-scenes.json"),production_c_sources=171,content_inputs=292,source_files=len(manifest),unsupported_guards=37,cleanup_performed_this_round=True,previous_cleanup_receipt=str(R/'evidence/movement-state-v35/cleanup.json'),final_build_inputs_match_returns_checkpoint=True,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    independent_default_budget_frames=901,independent_internal_observer_frames=4054,independent_connection_observer_frames=9116,independent_bridge_observer_frames=24327,
    independent_alias_observer_frames=9010,independent_prior_alias_observer_frames=3604,independent_staggered_alias_observer_frames=5406,legal_alias_sources_examined=29,new_alias_runtime_probe_targets=0,prior_expanded_alias_runtime_probe_targets=19,legacy_runtime_aliases=28,aliases_in_previous_baseline=29,legacy_alias_sources=29,new_alias_sources_this_round=[],current_natural_scene_probe_targets=29,
    north_meeting_dynamic_relation_query_verified=True,north_query_runtime_evidence=str(S/'north-query-real-scenes.json'),progress_estimate=str(S/'progress-estimate.json'),bridge_moving_infantry_vehicle_query_verified=True,bridge_infantry_runtime_evidence=str(S/'bridge-infantry-real-scenes.json'),bridge_upper_and_lower_three_object_traversal_verified=True,bridge_mixed_object_chain_verified=True,bridge_opposing_dynamic_traffic_verified=True,bridge_hostile_dynamic_traffic_verified=True,
    bridge_neighbor_lane_release_verified=True,bridge_neighbor_lane_release_runtime_evidence=str(S/"bridge-neighbor-release-real-scenes.json"),bridge_main_lane_release_verified=True,bridge_main_lane_release_runtime_evidence=str(S/"bridge-lane-release-real-scenes.json"),bridge_staggered_exit_verified=True,bridge_staggered_exit_runtime_evidence=str(S/'bridge-staggered-real-scenes.json'),bridge_multiobject_scenes=27,bridge_multiobject_frames=24327,bridge_held_exit_detour_scenes=2,bridge_held_exit_detour_frames=1802,bridge_held_exit_detour_verified=True,bridge_held_exit_detour_runtime_evidence=str(S/'bridge-detour-real-scenes.json'),bridge_meeting_occupied_scenes=2,bridge_meeting_occupied_frames=1802,bridge_meeting_occupied_verified=True,bridge_meeting_occupied_runtime_evidence=str(S/'bridge-occupied-real-scenes.json'),
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    bridge_runtime_evidence=str(S/'bridge-real-scenes.json'),bridge_hostile_runtime_evidence=str(S/'bridge-hostile-real-scenes.json'),bridge_mixed_runtime_evidence=str(S/'bridge-mixed-real-scenes.json'),legal_overlap_sources=str(S/'internal-alias-sources.json'),
    alias_runtime_evidence=str(S/'alias-natural-scenes.json'),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),original_preframe_startup_failures_preserved=len(startup['attempts']),
    rare_branch_evidence_scope=evidence['connection-real-scenes.json']['scope']+' '+hostile['scope']+' '+mixed['scope']+' '+alias_runtime['limits'],
    combined_curved_height_occupied_runtime_verified=True,combined_curved_height_occupied_scenes=4,original_equivalent_stall_scenes=2,all_curved_height_routes_complete=False,
    nonprimary_overlapping_adapter_naturally_observed=False,full_original_equivalence_verified=False,strict_ordered_audit_passed=True,frame_comparison_passed=True,
    default_rules_full_budget_exhaustion_verified=True,budget_scope=evidence['budget-real-scenes.json']['scope'],preservation=preservation,report=str(report),handoff=str(handoff),**flags)
write(S/'continuation.json',dict(status='validation_complete_commit_separately_audited',validation=str(S/'validation.json'),verify=str(R/'verify_final_movement_v38.py'),exe_sha256=digest,commit_policy='local commit only; never push'))
write(S/'validation.json',validation);accept.update(paired_scenes=71,paired_frames=49241,**flags);write(S/'strict-acceptance.json',accept)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update({k:v for k,v in validation.items() if k not in ['exe_sha256','source_files','part_checkpoints','preservation']})
for k in ['system_interruption_recovered','interrupted_pairs_preserved','resumption_evidence','serial_startup_retries_passed']:recovery.pop(k,None)
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),next_readable_region='Other loaded-table, coordinate-selection and template continuations and other internal copies; concrete object/locomotor and service side effects; broader bridge traffic and service side effects and legal computed alias sources')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(passed=True,validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=71,paired_frames=49241,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=37,verification_round=38,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(exe),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff)))
print(json.dumps(dict(passed=True,formal_baseline=37,exe_sha256=digest,source_files=len(manifest))))
