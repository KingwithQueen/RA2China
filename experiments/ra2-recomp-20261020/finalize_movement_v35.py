"""Promote generation34 after part checkpoints, native gates and mixed-bridge acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v35';O=R/'evidence/movement-state-v34'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,t):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n';p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
vcs=read(S/'vcs-context.json')
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()==vcs['parent_commit']=='5a9d504094af006a82d5245099022f6007b30414'
assert sha(P/'.git/config')==vcs['config_sha256']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
accept=read(S/'strict-acceptance.json');native=read(S/'native-gates.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==117
assert read(S/'native-round35-identity.json')['passed']
assert native['passed'] and native['groups']==117 and native['new_cases']==196608
evidence={n:read(S/n) for n in ['budget-real-scenes.json','connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','legal-overlap-sources.json','alias-route-inventory.json','overlap-caller-identity.json','recipe-byte-audit.json','bridge-hostile-real-scenes.json','bridge-infantry-real-scenes.json','progress-estimate.json','inherited-fixtures.json','new-fragment-contract.json','north-query-real-scenes.json']}
evidence.update({n:read(S/n) for n in ['internal-alias-sources.json','alias-natural-scenes.json','bridge-occupied-real-scenes.json','alias-occupied-natural-scenes.json','bridge-detour-real-scenes.json']})
evidence['production-scene-totals.json']=read(S/'production-scene-totals.json')
assert evidence['production-scene-totals.json']['production_scenes']==65 and evidence['production-scene-totals.json']['production_frames']==43835
assert evidence['production-scene-totals.json']['production_executable_sha256']==digest
structure=read(S/'refactor-structure.json');assert structure['passed'] and structure['compile_inputs']==292
assert structure['sample_anchor_internal_entries']==12 and structure['moving_tail_internal_entries']==3
assert structure['advance_service_exit_entries']==2 and structure['advance_service_exit_copies']==14
assert structure['remaining_destination_copies_connected']==4 and structure['enemy_contact_internal_copies']==3 and structure['following_service_copies']==20
assert structure['destination_internal_copies']==24 and structure['allied_relation_internal_copies']==3 and structure['prepare_stop_service_copies']==2
assert structure['register_sample_internal_copies']==8 and structure['enemy_weapon_internal_copies']==3 and structure['owner_stop_service_copies']==7
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
alias_runtime=evidence['alias-natural-scenes.json'];assert alias_runtime['passed'] and alias_runtime['static_aliases']==28
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
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,35)]
archives += [('v35-baseline',S/'baseline','source-manifest.json','')]
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
    receipt_path=O/'investigations'/rel;trial=read(receipt_path);assert trial['passed']
    for item in trial['files']:assert sha(receipt_path.parent/item['path'])==item['sha256'],(rel,item['path'])
producer=read(O/'investigations/south-initial-scan/producer-recovery.json');assert producer['passed'] and sha(O/'investigations/south-initial-scan'/producer['path'])==producer['producer_sha256']
old_south=next(v for v in read(O/'investigations/south-initial-scan/bridge-occupied-fixtures.json')['fixtures'] if v['name']=='south')
assert sha(O/'investigations/south-initial-scan/fixtures/bridge-occupied-south.MAP')==old_south['sha256']
preservation['nonqualifying_trial_receipts_preserved']=len(trial_receipts)
cleanup=read(S/'cleanup.json');assert cleanup['passed'] and not cleanup['blocked'] and cleanup['deleted_files']==2428 and cleanup['deleted_bytes']==29649646 and cleanup['user_approved_exact_allowlist']
cleanup_plan=read(S/'cleanup-plan.json');assert cleanup_plan['passed'] and len(cleanup_plan['files'])==2428
assert all(not (R/e['path']).exists() for e in cleanup_plan['files'])
preservation['cleanup_policy_blocked']=False;preservation['cleanup_deleted_files']=2428;preservation['cleanup_deleted_bytes']=29649646
preservation['original_preframe_startup_failures_preserved']=len(startup['attempts']);write(S/'preservation.json',preservation)
run_dirs=[p for p in (S/'runs').iterdir() if p.is_dir()]
assert all((p/'comparison.json').exists() for p in run_dirs)
assert {p.name for p in run_dirs if not read(p/'comparison.json')['passed']}==set()
report=P/'docs/单位移动第三十四批-载入表接续与地形武器及桥上占用绕行组合-20261023.txt'
handoff=P/'交接文档-单位移动第三十四批正式验收-20261023.txt';assert not report.exists() and not handoff.exists()
hostile=evidence['bridge-hostile-real-scenes.json'];assert hostile['hostile_classifier_observed'] and hostile['hostile_bridge_traffic_observed']
body=f'''单位移动第三十四批正式验收（2026-10-23）
正式代次34 / 验证轮次35
父提交：5a9d504094af006a82d5245099022f6007b30414
程序：{exe}
SHA-256：{digest}
证据：{S}

第三十三批提交5a9d504、程序7d0e3eb5e601f84218ff5c1a75baadb7c372b4a5224b6c593b9e233a16b1ceca与4997项源封存先只读核对通过，原工作区干净。完整baseline、旧文档、程序及指针均保留。

1. 三部分与原版逐帧对照及回退
内部模板：4A2320八处接续直接使用入口EAX载入的表和ECX缩放偏移，终止判定仍使用传入EDX。65536例使载入表与全局表不同，含非三倍数偏移及终止边界，核对内存、结果、非易失寄存器及栈。
具体对象：703A23三处共用地形武器选择与弹头门槛，已确认对象类型后不重复查询kind。65536例含武器服务写回弹头指针和标志，保留查询顺序与短路。
服务出口：4A46D7十一处共用存活门槛、按序目标清空、owner重读和4C8速度服务。65536例令输出别名到owner指针、保存栈槽及全局无效坐标，保留服务写回、EAX高位和出栈。
旧原生标签、注解、跳转及37处保护均保留，没有增加原生分派入口，不等于非主C副本已有自然入口证明。
每部分六场3406帧：默认901、短包围101、独立真实AI预算901、双向隧道各501及出口占用501；状态、RNG、命令及有序事件一致。三份完整源、程序、探针及场景回退：
'''+''.join(n+' : '+v['exe_sha256']+'\n' for n,v in parts.items())+f'''
171个C源、292项内容输入；最终内容构建刷新0并与returns回退相同。正式记录器、公共比较器、schema12、0010的LF和0046的CRLF保持。七项生产源、三项探针、一项观察器和四份组合地图从本批baseline独立重放逐字节一致。原65份地图/规则逐字节继承。

2. 最终回归
117组原版片段门禁通过，包含既有114组完整重跑及本轮三项各65536例。生产清单实际求和65场43835帧，包含上一批63场42033帧及两场持占用绕行各901帧。短包围检查、探索试验和观察程序不重复计入生产。
独立默认预算901、内部观察4054、连接及高差占用9116、桥观察21场18921、原入口观察3604和新增持占用绕行入口观察5406帧分别统计。坐标扰动与缺帧负控均拒绝差异；存档使用私有副本。

3. 桥上移动步兵与车辆交会加出口占用
沿用原版桥跨及普通地图对象，两辆本方TRUCKA先按第1帧正常指令进入北向70格、南向63格的出口两条车道，E2与主车辆正常对向移动；300帧向两辆占位车下达驶离命令，320帧向主车重发正常移动命令。后续移动属于这些正常指令下的结果，不声称未经重发命令就自动恢复。未写路径、链指针、运动状态或桥层。
生产/原版、独立观察/原版、生产/观察的状态和有序事件全部相等。要求双方在416桥面同帧反向移动时有实际关系与几何查询，主车辆确实在初始扫描之后查询占位车，并在两辆占位车停止、自己尚未到达目标的出口附近等待。随后核对占位车驶离及主车收到320帧重发命令后的移动；到达与查询分别统计，保留原版最终行为。上一批首轮单车占位出现绕行、清空前到达，四次对照3604帧虽原版/C一致但未满足目标过程，地图、配方、完整轨迹及控制哈希保留在上一批movement-state-v34/investigations/occupied-open-lane，正式验收计0帧。
继承占用两场结果：{ {n:v['modes']['original'] for n,v in evidence['bridge-occupied-real-scenes.json']['scenes'].items()} }
北向195..200帧等待6帧，201帧开始绕行；南向205..216帧等待12帧，217帧开始绕行。两者均在300帧占位车驶离之前已重规划移动，不能称为等清空才恢复。两路最终均到达各自目标格。
上一批南向原车道的生产/观察两次1802帧只有初始查询，另有五个子格/车道候选各301帧用于调查，均单列正式验收0帧；上一批原记录分别保留在movement-state-v34/investigations/south-initial-scan、south-subcells和south-lanes。选中的普通车道方案随后独立完成完整901帧生产及观察验收。
上一批北向移动查询108帧、既有交会/跟行、友方和原生AI敌方交通、上下层三对象链均已重跑。观察器原字节检查和CPU/FPU保存与上一批相同，替换十二项测试对象，完整状态身份单独核对。

本批额外两场持占用绕行：占位车完成初始驶入后，从等待窗口起持续静止至600帧，主车仅第5帧接受一次移动命令，不重发320帧命令。要求等待后在两条占用车道以外移动，并在清空前越过被占用出口；到达结果另行记录。
绕行验收：{ {n:v['modes']['original'] for n,v in evidence['bridge-detour-real-scenes.json']['scenes'].items()} }

4. 非主自然入口与原版异常
继续检查28个非主别名、三个主入口和85条原生入边，扫描171源与292输入；全部原生入边逐字节核对。没有新增独立原生入口或强行调用非主C副本。主入口正控有记录，扩展十九个候选加既有九个在合法桥实景中仍未观察到自然首次调用；新持占用绕行组合另加六场5406帧，分组覆盖全部28个候选，三个主入口均有正控。每个候选并非在两个场景均穷尽测试。函数内部边界命中不等于独立C入口命中；任意计算目标、运行时指针和未覆盖场景仍未排除。
4→6上行停滞及7→4下行至-193的异常继续与原版一致，只计异常一致性。四组既有成功高差加占用继续保留原等待和退出；旧错误桥端摆放、缺Tags及敌方命令拒绝、旧逐帧失败和上一批零帧CSF失败记录均保留，未修改原版异常。
本批第一次短包围启动在创建私有目录前被路径检查拒绝，尚未启动游戏或产生模拟帧；prelaunch-failures.json及原日志完整保留，同一路径补跑通过。比较器和路径保护完全未改。当前游戏首帧前失败{len(startup['attempts'])}次。
上一批南向子格短试验有两次指令触及或超出跟踪末帧的配置拒绝，两路均在模拟前返回7，原场景、命令、日志与哈希保留在上一批movement-state-v34/investigations/south-subcells的两份range-rejection中。修正只限制短试验指令早于300帧，完整901帧正式命令不变；不把配置拒绝归作原版运行异常。

5. 清理、保留、范围及继续工作
清理已完成：按用户明确批准的清单和逐文件SHA256，普通删除2428个未跟踪、可重新生成的旧探针obj，共29649646字节（约28.3 MiB），并确认清单内文件全部不存在。未使用强制或递归删除，基线、parts、final-source、runs、investigations、程序、PDB和当前构建缓存保留。此前含强制选项的三次命令被自动审批以blocked by policy拒绝；改为普通文件删除后成功执行，原拒绝次数与用户授权均留在cleanup.json中。
v9..v34旧封存、本批4997项baseline和三份parts均逐项核对；H盘原版允许列表20项、原游戏、SAV及旧手写引擎哈希保持。只声称核对的允许列表，不扩大成整个H盘未变化。
本批对应八处载入表接续、三处地形武器门槛、十一处清空目标服务出口及两场持占用绕行组合完成验收。其他内部模板、更多具体对象/移动器/建筑/地形/碾压/毁桥、其他服务与递归写回出口、28个非主自然入口、更广高差和占用组合仍需继续；完整移动、寻路、对象分类及全游戏等价未完成。没有重新估算百分比，旧估算仅为历史记录。
完成后只本地提交，不推送。下批先运行verify_final_movement_v35.py核对，再建立新回退；不要原地重跑本轮封存写入脚本。
'''
report.write_text(body,encoding='utf-8',newline='\n');handoff.write_text(body+'\n接手先运行verify_final_movement_v35.py，再保存下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';existing(guide,f'第三十四批当前状态（2026-10-23）\n载入表接续、地形武器门槛、清空目标服务出口；各部分六场3406帧。65场43835帧、117组门禁，敌我桥交通通过。完整移动和非主自然入口仍未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动第三十四批：载入表接续、地形武器门槛与清空目标服务出口；65场景43835帧、117组片段门禁，桥上移动步兵/车辆交会与敌我交通通过。入口为[第三十四批交接](交接文档-单位移动第三十四批正式验收-20261023.txt)和 `reports/latest-recovery.json`。基线、回退与原版异常保留；非主入口及全游戏等价未完成。\n';existing(p,''.join(lines))
p=P/'交接文档-新对话继续推进-20261022.txt';existing(p,f'最新接续：第三十四批已验收，正式34 / 验证35。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R/"verify_final_movement_v35.py"}\n以下历史保留。\n\n'+p.read_text(encoding='utf-8'))
p=P/'交接文档-原版逆向与C重编译-20261020.txt';existing(p,p.read_text(encoding='utf-8')+f'\n2026-10-23 第三十四批接续：{handoff}\n65场景43835帧，117组片段门禁；敌我桥交通实景通过，非主自然入口仍未证明。\n')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v35*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ['.c','.h','.asm'] or p.name in ['truck-actor-fixture-probe.exe','connection-fixture-probe.exe','connection-fixture.map','truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[]
for rel in sorted(paths):
    dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(R/rel)))
write(S/'source-manifest.json',manifest)
for document in [report,handoff]:
    with document.open('a',encoding='utf-8') as stream:stream.write(f'\n最终源封存：{len(manifest)}项。当前身份以validation.json/source-manifest.json为准。下一轮必须保留内容构建、独立观察器重建、结构/配方、原版片段和生产逐帧门禁，不能仅替换脚本后缀。\n')
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')};flags.update(four_destination_copies_shared_readable=True,enemy_contact_internal_shared_readable=True,following_service_exits_shared_readable=True,template_destination_internal_readable=True,allied_relation_internal_shared_readable=True,prepare_stop_service_exits_shared_readable=True,template_remainder_index_shared_readable=True,concrete_enemy_kind_shared_readable=True,service_bearing_prepare_exits_shared_readable=True,sample_anchor_internal_readable=True,moving_object_tail_shared_readable=True,advance_service_exits_shared_readable=True)
flags.update(register_sample_internal_shared_readable=True,enemy_weapon_internal_shared_readable=True,owner_stop_service_shared_readable=True,loaded_sample_internal_shared_readable=True,terrain_weapon_internal_shared_readable=True,invalidate_service_exits_shared_readable=True)
validation=dict(passed=True,formal_baseline_generation=34,verification_round=35,exe_sha256=digest,state_schema=12,paired_scenes=65,paired_frames=43835,probes=117,new_fragment_cases=196608,
    production_c_sources=171,content_inputs=292,source_files=len(manifest),unsupported_guards=37,cleanup_completed=True,cleanup_policy_blocked=False,cleanup_receipt=str(S/'cleanup.json'),final_build_inputs_match_returns_checkpoint=True,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    independent_default_budget_frames=901,independent_internal_observer_frames=4054,independent_connection_observer_frames=9116,independent_bridge_observer_frames=18921,
    independent_alias_observer_frames=9010,independent_prior_alias_observer_frames=3604,independent_detour_alias_observer_frames=5406,legal_alias_sources_examined=28,new_alias_runtime_probe_targets=19,
    north_meeting_dynamic_relation_query_verified=True,north_query_runtime_evidence=str(S/'north-query-real-scenes.json'),progress_estimate=str(S/'progress-estimate.json'),bridge_moving_infantry_vehicle_query_verified=True,bridge_infantry_runtime_evidence=str(S/'bridge-infantry-real-scenes.json'),bridge_upper_and_lower_three_object_traversal_verified=True,bridge_mixed_object_chain_verified=True,bridge_opposing_dynamic_traffic_verified=True,bridge_hostile_dynamic_traffic_verified=True,
    bridge_multiobject_scenes=21,bridge_multiobject_frames=18921,bridge_held_exit_detour_scenes=2,bridge_held_exit_detour_frames=1802,bridge_held_exit_detour_verified=True,bridge_held_exit_detour_runtime_evidence=str(S/'bridge-detour-real-scenes.json'),bridge_meeting_occupied_scenes=2,bridge_meeting_occupied_frames=1802,bridge_meeting_occupied_verified=True,bridge_meeting_occupied_runtime_evidence=str(S/'bridge-occupied-real-scenes.json'),
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    bridge_runtime_evidence=str(S/'bridge-real-scenes.json'),bridge_hostile_runtime_evidence=str(S/'bridge-hostile-real-scenes.json'),bridge_mixed_runtime_evidence=str(S/'bridge-mixed-real-scenes.json'),legal_overlap_sources=str(S/'internal-alias-sources.json'),
    alias_runtime_evidence=str(S/'alias-natural-scenes.json'),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),original_preframe_startup_failures_preserved=len(startup['attempts']),
    rare_branch_evidence_scope=evidence['connection-real-scenes.json']['scope']+' '+hostile['scope']+' '+mixed['scope']+' '+alias_runtime['limits'],
    combined_curved_height_occupied_runtime_verified=True,combined_curved_height_occupied_scenes=4,original_equivalent_stall_scenes=2,all_curved_height_routes_complete=False,
    nonprimary_overlapping_adapter_naturally_observed=False,full_original_equivalence_verified=False,strict_ordered_audit_passed=True,frame_comparison_passed=True,
    default_rules_full_budget_exhaustion_verified=True,budget_scope=evidence['budget-real-scenes.json']['scope'],preservation=preservation,report=str(report),handoff=str(handoff),**flags)
write(S/'continuation.json',dict(status='validation_complete_commit_separately_audited',validation=str(S/'validation.json'),verify=str(R/'verify_final_movement_v35.py'),exe_sha256=digest,commit_policy='local commit only; never push'))
write(S/'validation.json',validation);accept.update(paired_scenes=65,paired_frames=43835,**flags);write(S/'strict-acceptance.json',accept)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update({k:v for k,v in validation.items() if k not in ['exe_sha256','source_files','part_checkpoints','preservation']})
for k in ['system_interruption_recovered','interrupted_pairs_preserved','resumption_evidence','serial_startup_retries_passed']:recovery.pop(k,None)
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),next_readable_region='Remaining loaded-table and register-sourced template continuations and other internal copies; concrete object/locomotor and service side effects; broader bridge traffic and service side effects and legal computed alias sources')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(passed=True,validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=65,paired_frames=43835,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=34,verification_round=35,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(exe),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff)))
print(json.dumps(dict(passed=True,formal_baseline=34,exe_sha256=digest,source_files=len(manifest))))
