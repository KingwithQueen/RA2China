"""Promote generation32 after part checkpoints, native gates and mixed-bridge acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v33';O=R/'evidence/movement-state-v32'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,t):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n';p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
vcs=read(S/'vcs-context.json')
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()==vcs['parent_commit']=='ccc6e7204cd9deac4e32deadcc263d1f8a2ce4b5'
assert sha(P/'.git/config')==vcs['config_sha256']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
accept=read(S/'strict-acceptance.json');native=read(S/'native-gates.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==111
assert native['passed'] and native['groups']==111 and native['new_cases']==196608
evidence={n:read(S/n) for n in ['budget-real-scenes.json','connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','legal-overlap-sources.json','alias-route-inventory.json','overlap-caller-identity.json','recipe-byte-audit.json','bridge-hostile-real-scenes.json','bridge-infantry-real-scenes.json','progress-estimate.json','inherited-fixtures.json','destination-copy-contract.json','north-query-real-scenes.json']}
evidence.update({n:read(S/n) for n in ['internal-alias-sources.json','alias-natural-scenes.json']})
evidence['production-scene-totals.json']=read(S/'production-scene-totals.json')
assert evidence['production-scene-totals.json']['production_scenes']==61 and evidence['production-scene-totals.json']['production_frames']==40231
assert evidence['production-scene-totals.json']['production_executable_sha256']==digest
structure=read(S/'refactor-structure.json');assert structure['passed'] and structure['compile_inputs']==292
assert structure['sample_anchor_internal_entries']==12 and structure['moving_tail_internal_entries']==3
assert structure['advance_service_exit_entries']==2 and structure['advance_service_exit_copies']==14
assert structure['remaining_destination_copies_connected']==4 and structure['enemy_contact_internal_copies']==3 and structure['following_service_copies']==20
assert structure['destination_internal_copies']==24 and structure['allied_relation_internal_copies']==3 and structure['prepare_stop_service_copies']==2
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
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,33)]
archives += [('v33-baseline',S/'baseline','source-manifest.json','')]
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
preservation['original_preframe_startup_failures_preserved']=len(startup['attempts']);write(S/'preservation.json',preservation)
run_dirs=[p for p in (S/'runs').iterdir() if p.is_dir()]
assert all((p/'comparison.json').exists() for p in run_dirs)
assert {p.name for p in run_dirs if not read(p/'comparison.json')['passed']}==set()
report=P/'docs/单位移动第三十二批-四副本接续与北向移动交会及对象服务出口-20261023.txt'
handoff=P/'交接文档-单位移动第三十二批正式验收-20261023.txt';assert not report.exists() and not handoff.exists()
hostile=evidence['bridge-hostile-real-scenes.json'];assert hostile['hostile_classifier_observed'] and hostile['hostile_bridge_traffic_observed']
body=f'''单位移动第三十二批正式验收（2026-10-23）
正式代次32 / 验证轮次33
父提交：ccc6e7204cd9deac4e32deadcc263d1f8a2ce4b5
程序：{exe}
SHA-256：{digest}
证据：{S}

第三十一批ccc6e72、程序d03ef60ce68c447108299d173677ded81af794a8aa5b25b8d184a6efe6c0e45f与4390项封存先行只读核对，工作区干净；完整baseline、项目文档及指针已保存。

1. 三部分整理和回退
四个内部副本4A1F8D、4A1FA1、4A230E、4A2311中，原生2528指令本来存在，只缺少同名C标签。本批在原有指令前放置函数内局部C接续标签，将24C6/24DC两入口接回已验证的目标坐标服务。四父副本共八处完成，累计目标入口24处；保留全部原生指令注解、旧标签、尾目标、保护分支及分派入口，没有新增原生入口。每副本22条原始指令逐项核对，destination-copy-contract.json记录结构与来源。接续整理不等于非主C入口自然执行证明。
具体对象：70399A三处敌方接触接续与完整分类共用碾压标志/能力、可碾压属性、阵营重查、武器/列车门槛，再接既有建筑/地形/其他类别尾部。保留查询短路和顺序，能力回调改变阵营查询结果的65536例通过。
含服务出口：4A456E九处先执行原收尾服务，再重读owner并调用414；4A46BD十一处执行原采样服务后清低字节返回。两类二十处共用原Prepare返回帧；回调可改owner、采样内容与保存寄存器，EAX高位和出栈顺序保持。65536例记录425984项有序回调值通过。
每部分仍为六场3406帧：默认901、包围101、真实AI默认预算901、双向隧道各501、出口占用501。状态、命令、RNG及有序事件逐帧一致。完整回退：
'''+''.join(n+' : '+v['exe_sha256']+'\n' for n,v in parts.items())+f'''
171个C源、292项编译输入；新增ground_enemy_contact.h，旧公共头未改。最终内容构建刷新0，当前EXE/编译输入与returns回退一致。0010的LF、0046的CRLF、schema12、正式记录器和公共比较器未变；37处保护保留。

2. 原版检查和实景
111组原版片段门禁通过，原108组完整重跑；本轮三组新增或扩展绑定各65536例，共196608例，其中四副本复用原目标服务契约并单独核对接续形状，不把重复契约试验说成四个自然函数入口已经执行。
production-scene-totals.json从实际完成的最终EXE场景逐项求和，短包围检查和探索试验单列，不重复计数。最终61个生产场景40231帧：既有60场39330帧全部回归，加一场北向对向交会901帧。独立默认预算901、内部观察4054、连接与组合9116、桥观察17场15317、别名四场3604帧另列，未混算成生产覆盖。负控包括坐标扰动和缺帧拒绝；存档为私有副本，完整状态、RNG、命令和有序事件相等。
原399帧失败及重复失败、52帧包围、197帧转弯、27..37帧预算10..0和38帧停止继续通过。未经干预的预算随机频率及4C3895独立回调仍未测。

3. 北向桥上移动步兵与车辆交会过程查询
沿用已验证的普通地图和桥跨，TRUCKA与E2均属本方，仅以普通地图字段设置初始位置、朝向和子格，发出正常对向移动及让行命令。没有写运动状态、路径、链指针或桥层。先后三组反向时机、车辆改派、相邻车道试验各903帧，原版/C均一致但未命中目标查询，全部计入正式验收0帧；地图、配方与记录分别保留在investigations/north-first-turnback-trials、north-retarget-trials、north-lane-trials。再按普通地图朝向与南向演员镜像构造三组301帧候选，north-query-trials.json仍单列试验0验收帧，选中者重跑完整901帧生产与观察。
只统计初始命令之后、车辆Y增加且步兵Y减小的同一帧、双方均在416高度桥面且相距四格内的实际关系查询25与几何查询26；初始扫描不计。north-query-real-scenes.json逐项记录前后帧坐标、查询及到达：{ {n:dict(relationship_queries=v['modes']['original']['relationship_queries'],geometry_queries=v['modes']['original']['geometry_queries'],query_after_frame=v['query_after_frame'],motion=v['modes']['original']['motion']) for n,v in evidence['north-query-real-scenes.json']['scenes'].items()} }。
生产/原版、独立观察/原版及生产/观察完整记录相等；查询、移动和到达分开验收，不将查询次数当成穿越成功。原北向直行场景仍仅有第6帧初始查询，其结果原样保留；本批通过合法的动态对向场景补齐了移动交会查询，未改写旧结论。
独立观察器所有原始字节检查、CPU/FPU保存、演员白名单均与上一批逐字节一致，仍替换十二项测试对象。上下层三对象链、友方混类/对向交通、敌方原生CreateTeam/Tags/Script驱动交通及既有步兵交会全部重跑。

4. 合法来源与原版异常
本批服务出口父副本加入4A44D1、4A4522，累计28个非主别名、三主入口，85条原生入边逐字节核对；扫描171源/292输入。未发现直接C调用、直接原生CALL、函数外跳入或非代码地址常量来源；已知入边为原函数内部跳转。
合法桥交通场景按每组最多八个参数覆盖十九个扩展候选，既有九个由友方桥实景覆盖。主703040有首次调用正控，28个非主C副本自然首次调用仍未观察到。任意计算目标、运行时构造指针及未跑场景仍未排除；内部原生边界命中与独立C副本入口不是同一结论。
4→6弯曲上行停滞和7→4下行高度下漂继续一致，计异常一致性，不计成功穿越。四组成功高差加出口占用保留原等待和退出；原版跟行停在目标前格、以前错误桥端放置及缺Tags/敌方命令拒绝试验均保留旧记录，未修原版异常。
本轮有一次较长私有目录标签下的两路CSF首帧前初始化失败，模拟帧为0；原目录、命令、地图与控制哈希完整保留，仅缩短诊断标签后重试。startup-failures.json记录{len(startup['attempts'])}次；如有重试则startup-failures.json保留零帧现场与哈希，任何模拟差异均不按启动失败移走。

5. 保留与剩余
v9..v32旧档、4390项baseline和三份parts逐项复核；H盘允许列表20项、原游戏、SAV和旧手写引擎哈希保持。六项生产源、两项探针、一项观察器和三份候选地图通过隔离配方逐字节重放；60份旧场景文件逐字节复用。只声称允许列表已核对，不扩大成整个H盘未变化。
本批四个指定副本与北向动态关系查询已完成对应范围。剩余为其他Advance/Prepare模板和副本、更多具体对象/移动器/建筑/地形/碾压/毁桥与交通组合、服务/递归/写回副作用出口、28个非主C自然来源、替代保存路段指针及更广高差占用场景；完整移动、寻路、Tube、对象分类和全游戏等价仍未完成。全引擎其他模块、指令保护分类、完整战役、网络同步和性能验收仍需推进。
上一批百分比仅留作历史工程估算，本轮没有重新测算完成率，详见progress-estimate.json的historical_only/reestimated_this_round。
完成后本地提交，不推送，不改远端配置。下一批先运行verify_final_movement_v33.py，再保存完整回退；不要原地重跑本轮封存写入脚本。
'''
report.write_text(body,encoding='utf-8',newline='\n');handoff.write_text(body+'\n接手先运行verify_final_movement_v33.py，再保存下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';existing(guide,f'第三十二批当前状态（2026-10-23）\n四副本接续、敌方接触、后续服务出口；各部分六场3406帧。61场40231帧、111组门禁，敌我桥交通通过。完整移动和非主自然入口仍未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动第三十二批：四副本接续、敌方接触与后续服务出口；61场景40231帧、111组片段门禁，桥上移动步兵/车辆交会与敌我交通通过。入口为[第三十二批交接](交接文档-单位移动第三十二批正式验收-20261023.txt)和 `reports/latest-recovery.json`。基线、回退与原版异常保留；非主入口及全游戏等价未完成。\n';existing(p,''.join(lines))
p=P/'交接文档-新对话继续推进-20261022.txt';existing(p,f'最新接续：第三十二批已验收，正式32 / 验证33。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R/"verify_final_movement_v33.py"}\n以下历史保留。\n\n'+p.read_text(encoding='utf-8'))
p=P/'交接文档-原版逆向与C重编译-20261020.txt';existing(p,p.read_text(encoding='utf-8')+f'\n2026-10-23 第三十二批接续：{handoff}\n61场景40231帧，111组片段门禁；敌我桥交通实景通过，非主自然入口仍未证明。\n')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v33*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ['.c','.h','.asm'] or p.name in ['truck-actor-fixture-probe.exe','connection-fixture-probe.exe','connection-fixture.map','truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[]
for rel in sorted(paths):
    dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(R/rel)))
write(S/'source-manifest.json',manifest)
for document in [report,handoff]:
    with document.open('a',encoding='utf-8') as stream:stream.write(f'\n最终源封存：{len(manifest)}项。当前身份以validation.json/source-manifest.json为准。下一轮必须保留内容构建、独立观察器重建、结构/配方、原版片段和生产逐帧门禁，不能仅替换脚本后缀。\n')
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')};flags.update(four_destination_copies_shared_readable=True,enemy_contact_internal_shared_readable=True,following_service_exits_shared_readable=True,template_destination_internal_readable=True,allied_relation_internal_shared_readable=True,prepare_stop_service_exits_shared_readable=True,template_remainder_index_shared_readable=True,concrete_enemy_kind_shared_readable=True,service_bearing_prepare_exits_shared_readable=True,sample_anchor_internal_readable=True,moving_object_tail_shared_readable=True,advance_service_exits_shared_readable=True)
validation=dict(passed=True,formal_baseline_generation=32,verification_round=33,exe_sha256=digest,state_schema=12,paired_scenes=61,paired_frames=40231,probes=111,new_fragment_cases=196608,
    production_c_sources=171,content_inputs=292,source_files=len(manifest),unsupported_guards=37,final_build_inputs_match_returns_checkpoint=True,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    independent_default_budget_frames=901,independent_internal_observer_frames=4054,independent_connection_observer_frames=9116,independent_bridge_observer_frames=15317,
    independent_alias_observer_frames=3604,legal_alias_sources_examined=28,new_alias_runtime_probe_targets=19,
    north_meeting_dynamic_relation_query_verified=True,north_query_runtime_evidence=str(S/'north-query-real-scenes.json'),progress_estimate=str(S/'progress-estimate.json'),bridge_moving_infantry_vehicle_query_verified=True,bridge_infantry_runtime_evidence=str(S/'bridge-infantry-real-scenes.json'),bridge_upper_and_lower_three_object_traversal_verified=True,bridge_mixed_object_chain_verified=True,bridge_opposing_dynamic_traffic_verified=True,bridge_hostile_dynamic_traffic_verified=True,
    bridge_multiobject_scenes=17,bridge_multiobject_frames=15317,
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    bridge_runtime_evidence=str(S/'bridge-real-scenes.json'),bridge_hostile_runtime_evidence=str(S/'bridge-hostile-real-scenes.json'),bridge_mixed_runtime_evidence=str(S/'bridge-mixed-real-scenes.json'),legal_overlap_sources=str(S/'internal-alias-sources.json'),
    alias_runtime_evidence=str(S/'alias-natural-scenes.json'),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),original_preframe_startup_failures_preserved=len(startup['attempts']),
    rare_branch_evidence_scope=evidence['connection-real-scenes.json']['scope']+' '+hostile['scope']+' '+mixed['scope']+' '+alias_runtime['limits'],
    combined_curved_height_occupied_runtime_verified=True,combined_curved_height_occupied_scenes=4,original_equivalent_stall_scenes=2,all_curved_height_routes_complete=False,
    nonprimary_overlapping_adapter_naturally_observed=False,full_original_equivalence_verified=False,strict_ordered_audit_passed=True,frame_comparison_passed=True,
    default_rules_full_budget_exhaustion_verified=True,budget_scope=evidence['budget-real-scenes.json']['scope'],preservation=preservation,report=str(report),handoff=str(handoff),**flags)
write(S/'continuation.json',dict(status='validation_complete_commit_separately_audited',validation=str(S/'validation.json'),verify=str(R/'verify_final_movement_v33.py'),exe_sha256=digest,commit_policy='local commit only; never push'))
write(S/'validation.json',validation);accept.update(paired_scenes=61,paired_frames=40231,**flags);write(S/'strict-acceptance.json',accept)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update({k:v for k,v in validation.items() if k not in ['exe_sha256','source_files','part_checkpoints','preservation']})
for k in ['system_interruption_recovered','interrupted_pairs_preserved','resumption_evidence','serial_startup_retries_passed']:recovery.pop(k,None)
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),next_readable_region='Remaining register-sourced template continuations and other internal copies; concrete object/locomotor and service side effects; broader bridge traffic and service side effects and legal computed alias sources')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(passed=True,validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=61,paired_frames=40231,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=32,verification_round=33,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(exe),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff)))
print(json.dumps(dict(passed=True,formal_baseline=32,exe_sha256=digest,source_files=len(manifest))))
