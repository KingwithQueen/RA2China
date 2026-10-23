"""Promote generation31 after part checkpoints, native gates and mixed-bridge acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v32';O=R/'evidence/movement-state-v31'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,t):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n';p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
vcs=read(S/'vcs-context.json')
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()==vcs['parent_commit']=='4d4fcb2e4fc7f58ef3006cd7e214ec2867dd1c1a'
assert sha(P/'.git/config')==vcs['config_sha256']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
accept=read(S/'strict-acceptance.json');native=read(S/'native-gates.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==108
assert native['passed'] and native['groups']==108 and native['new_cases']==196608
evidence={n:read(S/n) for n in ['budget-real-scenes.json','connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','legal-overlap-sources.json','alias-route-inventory.json','overlap-caller-identity.json','recipe-byte-audit.json','bridge-hostile-real-scenes.json','bridge-infantry-real-scenes.json','progress-estimate.json','inherited-fixtures.json']}
evidence.update({n:read(S/n) for n in ['internal-alias-sources.json','alias-natural-scenes.json']})
structure=read(S/'refactor-structure.json');assert structure['passed'] and structure['compile_inputs']==291
assert structure['sample_anchor_internal_entries']==12 and structure['moving_tail_internal_entries']==3
assert structure['advance_service_exit_entries']==2 and structure['advance_service_exit_copies']==14
assert structure['destination_internal_copies']==16 and structure['allied_relation_internal_copies']==3 and structure['prepare_stop_service_copies']==2
for name,v in evidence.items():
    assert v['passed'],name
    for item in v.get('inputs',[]):assert sha(R/item['path'])==item['sha256'],(name,item['path'])
for name in ['connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','bridge-hostile-real-scenes.json','bridge-infantry-real-scenes.json']:
    assert evidence[name]['production_executable_sha256']==digest,name
assert evidence['budget-real-scenes.json']['formal_executable_sha256']==digest
assert evidence['connection-real-scenes.json']['original_equivalent_stall_scenes']==2
assert not evidence['connection-real-scenes.json']['all_curved_height_routes_complete']
assert evidence['bridge-real-scenes.json']['actual_ordered_three_object_traversal_verified']
mixed=evidence['bridge-mixed-real-scenes.json'];assert mixed['mixed_runtime_classes_verified'] and mixed['opposing_bridge_traffic_verified']
assert not mixed['nonprimary_natural_entry_proved']
assert not evidence['internal-real-scenes.json']['nonprimary_overlapping_adapter_naturally_observed']
assert not evidence['overlap-caller-identity.json']['nonprimary_overlapping_adapter_naturally_observed']
alias_runtime=evidence['alias-natural-scenes.json'];assert alias_runtime['passed'] and alias_runtime['static_aliases']==26
assert alias_runtime['additional_observer_frames']==3604 and not alias_runtime['nonprimary_natural_entry_proved']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==171 and len(receipt['inputs'])==291 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
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
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,32)]
archives += [('v32-baseline',S/'baseline','source-manifest.json','')]
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
report=P/'docs/单位移动第三十一批-移动步兵车辆交会与模板目标及停驶服务出口-20261023.txt'
handoff=P/'交接文档-单位移动第三十一批正式验收-20261023.txt';assert not report.exists() and not handoff.exists()
hostile=evidence['bridge-hostile-real-scenes.json'];assert hostile['hostile_classifier_observed'] and hostile['hostile_bridge_traffic_observed']
body=f'''单位移动第三十一批正式验收（2026-10-23）
正式代次31 / 验证轮次32
父提交：4d4fcb2e4fc7f58ef3006cd7e214ec2867dd1c1a
程序：{exe}
SHA-256：{digest}
证据：{S}

第三十批基线4d4fcb2、程序524115b6683fbf3050d10280fb38e881e36ecf19baea33a2b4771e3c298f3bd4及4108项归档已逐项核对，开始工作区干净；先保存完整baseline、项目文档和指针。

1. 本批整理、分段对照和回退
模板目标：4A24C6/4A24DC的两种目标坐标接续，复用有序坐标保存及548000地图服务。服务完成后重读owner，保留服务对坐标和局部槽的修改。各12个原始副本中，8个具有完整2528接续边界并接入，共16处；另4个缺少该标签的父副本保持原代码，列于progress-estimate.json，不删代码、不补造自然入口。
对象分类：allied_relation将敌我关系、运动状态、朝向、相对方向与距离服务共用，70372C三处内部接续与完整入口共享。即使方向不同也仍执行原相对方向服务，使用原数学服务和控制字。新增header不改变旧公共头文件。
服务出口：4A26EC/4A2916在414/410服务前设置原owner对象，服务后分别进入写回出口或清低字节返回。回调可改变输出指针及保存寄存器，保留输出与保存槽重叠时原先后顺序。两类两处，未宣称全部共享出口完成。
每部分六场3406帧：默认901、包围101、真实AI默认预算901、双向隧道各501、出口占用501。完整状态、命令、RNG及有序事件与原版逐帧一致；三份parts包含全部源、编译输入和EXE。
'''+''.join(n+' : '+v['exe_sha256']+'\n' for n,v in parts.items())+f'''
最终171个C源、291项编译输入，内容构建最终刷新0；返回阶段回退与当前编译输入/程序逐字节一致。0010的LF、0046的CRLF、所有旧标签、静态尾目标、37处保护、schema12、记录器及公共比较器保持。

2. 原版片段和完整实景
108组原版片段门禁全部重跑通过。新增三组各65536例，共196608例，覆盖目标服务改owner/坐标、关系分流及停驶回调改保存槽/输出别名；对象关系结果[清除,阻挡,敌方,静止,继续]为[0,48,32756,16400,16332]。片段验证不等同自然入口覆盖。
最终60个生产场景39330帧：既有56场35726帧，加步兵/车辆四场3604帧。独立默认预算901、内部观察4054、连接及高差占用9116、桥观察16场14416、别名四场3604帧分别统计。所有比较含坐标扰动和缺帧负控、私有存档及种子身份检查。
原版399帧失败、重复失败、52帧包围、197帧转弯、27..37帧预算10..0与38帧停止继续通过。未经干预的预算随机出现频率及4C3895独立回调仍未覆盖。

3. 桥上移动步兵与车辆
普通地图放置本方E2与TRUCKA，使用正常本方移动命令，双向迎面交会及同向跟行各两场；桥面与桥下静态混类链保留，阻挡车辆通过普通命令让行。没有写运动状态、链指针、桥层或路径。
四场生产与原版、独立观察与原版、生产与观察的完整状态、命令、RNG、有序事件逐帧相等。步兵和车辆各自确实改变位置；同时在416高度桥面上的实际跨类通行查询与最终到达分开记录。其中南向迎面交会和跟行观察到双方在查询同一帧均改变位置，北向交会仅在移动前第6帧初始扫描查询到对方，后续两者移动并到达，但北向移动过程查询仍未观察到，不能把156次桥面查询全部当成双方正移动。实际查询与到达计数：{evidence['bridge-infantry-real-scenes.json']['totals']}。具体帧、查询ID、最终坐标/任务/生命值见bridge-infantry-real-scenes.json；未以发出命令替代实际移动，未以查询替代穿越成功。
独立观察沿用上一批全部原始字节检查及CPU/FPU保存，仅扩大明确演员ID白名单，仍为十二项测试对象替换，正式记录器未改。既有上下层三对象链、友方混类、敌方原生小队交通全部重跑；敌车仍由原生CreateTeam/Tags/Script动作3控制，没有向敌车发送玩家命令。

4. 合法入口和原版异常
针对本批两种目标、两种停驶出口及关系分流的所有父副本，重新核对累计26个非主别名、三主入口和83条原生入边；扫描171源/291输入。未发现直接C调用、原生CALL、函数外跳入或非代码地址常量来源；已知入边为原函数内部跳转。
四场合法敌我桥场景按每组最多八个探针重跑十七个扩展候选；原九个由友方桥实景回归。主703040首次调用正控存在，26个非主C副本自然入口仍未证明；任意计算目标、运行时构造指针和未跑场景未排除。原生内部边界命中不能当成非主C入口命中。
4→6弯曲上行停滞与7→4下行高度下漂仍与原版一致，计异常一致性、不计成功穿越；四组弯曲高差加出口占用成功路线继续验证等待和最终退出。上一批敌方玩家命令被拒及缺Tags的小队试验原始记录继续保留在movement-state-v31，本批没有重写历史失败结论。
本批首次步兵地图将桥端高地的桥层高度叠加成832，原版/C一致但步兵未移动；地图、初始位置和原始记录保留于investigations/infantry-placement-height-trial，改用既有低地桥跨区间后重新验证，前次不计移动验收。
本批初次模板构建因部分副本缺少接续标签未通过；原始构建日志和中止试验留investigations/incomplete-label-build-trial，未纳入验收。随后只接入边界完整副本并重跑全部分段。原版首帧前启动失败{len(startup['attempts'])}次，若有则按startup-failures.json保留零帧现场和重试结果，不隐藏模拟差异。

5. 剩余内容与估算口径
地面移动与寻路可读整理及受控验收，工程估算约70%，区间60%–75%；整个可读、可维护且独立的C17新引擎约20%，区间15%–25%。这是明确权重的里程碑估算，不能当行为覆盖率或剩余工时预测；权重、进度信用、依据及不确定性记录于progress-estimate.json。生成C行数、91.63%反汇编区间覆盖、批数和通过测试数均不作为全游戏完成率。
当前移动子项目还剩：Advance/Prepare内部模板和副本统一；建筑/地形、碾压、毁桥及更多具体移动器/敌我对象组合；含服务/递归/写回副作用出口；非主C副本合法自然来源；替代保存路段指针、复杂交通和更多高差占用组合的实景。完整Advance/Prepare/Tube/对象分类/寻路状态仍为未完成。
全引擎还需广泛恢复战斗、经济建造生产、AI任务、渲染/UI/音频、存档/网络等可读模块，分类37处指令保护并复核终止/尾目标，完成整场状态、完整战役、网络同步、性能和独立ABI/布局验收。已有静态C程序可运行与整个新引擎完成是不同验收口径。

v9..v31旧归档、本轮4108项baseline及三份parts逐项复核；H盘原始20项允许列表、原游戏、SAV和旧手写引擎哈希保持。六项生产源、两项探针、一项观察器和四份新地图通过隔离配方逐字节重放。只核对允许列表，不扩大成整个H盘未变化的结论。
完成后本地提交，不推送，不改远端配置。下一批先运行verify_final_movement_v32.py，再保留完整新回退；不要原地重跑本轮封存写入脚本。
'''
report.write_text(body,encoding='utf-8',newline='\n');handoff.write_text(body+'\n接手先运行verify_final_movement_v32.py，再保存下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';existing(guide,f'第三十一批当前状态（2026-10-23）\n目标坐标、对象关系、停驶服务出口；各部分六场3406帧。60场39330帧、108组门禁，敌我桥交通通过。完整移动和非主自然入口仍未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动第三十一批：目标坐标、对象关系与停驶服务出口；60场景39330帧、108组片段门禁，桥上移动步兵/车辆交会与敌我交通通过。入口为[第三十一批交接](交接文档-单位移动第三十一批正式验收-20261023.txt)和 `reports/latest-recovery.json`。基线、回退与原版异常保留；非主入口及全游戏等价未完成。\n';existing(p,''.join(lines))
p=P/'交接文档-新对话继续推进-20261022.txt';existing(p,f'最新接续：第三十一批已验收，正式31 / 验证32。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R/"verify_final_movement_v32.py"}\n以下历史保留。\n\n'+p.read_text(encoding='utf-8'))
p=P/'交接文档-原版逆向与C重编译-20261020.txt';existing(p,p.read_text(encoding='utf-8')+f'\n2026-10-23 第三十一批接续：{handoff}\n60场景39330帧，108组片段门禁；敌我桥交通实景通过，非主自然入口仍未证明。\n')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v32*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ['.c','.h','.asm'] or p.name in ['truck-actor-fixture-probe.exe','connection-fixture-probe.exe','connection-fixture.map','truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[]
for rel in sorted(paths):
    dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(R/rel)))
write(S/'source-manifest.json',manifest)
for document in [report,handoff]:
    with document.open('a',encoding='utf-8') as stream:stream.write(f'\n最终源封存：{len(manifest)}项。当前身份以validation.json/source-manifest.json为准。下一轮必须保留内容构建、独立观察器重建、结构/配方、原版片段和生产逐帧门禁，不能仅替换脚本后缀。\n')
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')};flags.update(template_destination_internal_readable=True,allied_relation_internal_shared_readable=True,prepare_stop_service_exits_shared_readable=True,template_remainder_index_shared_readable=True,concrete_enemy_kind_shared_readable=True,service_bearing_prepare_exits_shared_readable=True,sample_anchor_internal_readable=True,moving_object_tail_shared_readable=True,advance_service_exits_shared_readable=True)
validation=dict(passed=True,formal_baseline_generation=31,verification_round=32,exe_sha256=digest,state_schema=12,paired_scenes=60,paired_frames=39330,probes=108,new_fragment_cases=196608,
    production_c_sources=171,content_inputs=291,source_files=len(manifest),unsupported_guards=37,final_build_inputs_match_returns_checkpoint=True,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    independent_default_budget_frames=901,independent_internal_observer_frames=4054,independent_connection_observer_frames=9116,independent_bridge_observer_frames=14416,
    independent_alias_observer_frames=3604,legal_alias_sources_examined=26,new_alias_runtime_probe_targets=17,
    progress_estimate=str(S/'progress-estimate.json'),bridge_moving_infantry_vehicle_query_verified=True,bridge_infantry_runtime_evidence=str(S/'bridge-infantry-real-scenes.json'),bridge_upper_and_lower_three_object_traversal_verified=True,bridge_mixed_object_chain_verified=True,bridge_opposing_dynamic_traffic_verified=True,bridge_hostile_dynamic_traffic_verified=True,
    bridge_multiobject_scenes=16,bridge_multiobject_frames=14416,
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    bridge_runtime_evidence=str(S/'bridge-real-scenes.json'),bridge_hostile_runtime_evidence=str(S/'bridge-hostile-real-scenes.json'),bridge_mixed_runtime_evidence=str(S/'bridge-mixed-real-scenes.json'),legal_overlap_sources=str(S/'internal-alias-sources.json'),
    alias_runtime_evidence=str(S/'alias-natural-scenes.json'),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),original_preframe_startup_failures_preserved=len(startup['attempts']),
    rare_branch_evidence_scope=evidence['connection-real-scenes.json']['scope']+' '+hostile['scope']+' '+mixed['scope']+' '+alias_runtime['limits'],
    combined_curved_height_occupied_runtime_verified=True,combined_curved_height_occupied_scenes=4,original_equivalent_stall_scenes=2,all_curved_height_routes_complete=False,
    nonprimary_overlapping_adapter_naturally_observed=False,full_original_equivalence_verified=False,strict_ordered_audit_passed=True,frame_comparison_passed=True,
    default_rules_full_budget_exhaustion_verified=True,budget_scope=evidence['budget-real-scenes.json']['scope'],preservation=preservation,report=str(report),handoff=str(handoff),**flags)
write(S/'continuation.json',dict(status='validation_complete_commit_separately_audited',validation=str(S/'validation.json'),verify=str(R/'verify_final_movement_v32.py'),exe_sha256=digest,commit_policy='local commit only; never push'))
write(S/'validation.json',validation);accept.update(paired_scenes=60,paired_frames=39330,**flags);write(S/'strict-acceptance.json',accept)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update({k:v for k,v in validation.items() if k not in ['exe_sha256','source_files','part_checkpoints','preservation']})
for k in ['system_interruption_recovered','interrupted_pairs_preserved','resumption_evidence','serial_startup_retries_passed']:recovery.pop(k,None)
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),next_readable_region='Remaining register-sourced template continuations and four raw destination copies; concrete object/locomotor and service side effects; broader infantry/hostile bridge traffic and legal computed alias sources')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(passed=True,validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=60,paired_frames=39330,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=31,verification_round=32,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(exe),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff)))
print(json.dumps(dict(passed=True,formal_baseline=31,exe_sha256=digest,source_files=len(manifest))))
