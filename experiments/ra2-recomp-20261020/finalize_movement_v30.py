"""Promote generation29 after part checkpoints, native gates and mixed-bridge acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v30';O=R/'evidence/movement-state-v29'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,t):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n';p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
vcs=read(S/'vcs-context.json')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()==vcs['parent_commit']=='018c1bb719d0f51508111400b040583ecb0414dd'
assert sha(P/'.git/config')==vcs['config_sha256']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
accept=read(S/'strict-acceptance.json');native=read(S/'native-gates.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==102
assert native['passed'] and native['groups']==102 and native['new_cases']==196608
evidence={n:read(S/n) for n in ['budget-real-scenes.json','connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','legal-overlap-sources.json','alias-route-inventory.json','overlap-caller-identity.json','recipe-byte-audit.json']}
evidence.update({n:read(S/n) for n in ['internal-alias-sources.json','alias-natural-scenes.json']})
structure=read(S/'refactor-structure.json');assert structure['passed'] and structure['compile_inputs']==289
assert structure['template_index_internal_entries']==10 and structure['enemy_kind_internal_entries']==3
assert structure['service_exit_entries']==3 and structure['service_exit_copies']==26
for name,v in evidence.items():
    assert v['passed'],name
    for item in v.get('inputs',[]):assert sha(R/item['path'])==item['sha256'],(name,item['path'])
for name in ['connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json']:
    assert evidence[name]['production_executable_sha256']==digest,name
assert evidence['budget-real-scenes.json']['formal_executable_sha256']==digest
assert evidence['connection-real-scenes.json']['original_equivalent_stall_scenes']==2
assert not evidence['connection-real-scenes.json']['all_curved_height_routes_complete']
assert evidence['bridge-real-scenes.json']['actual_ordered_three_object_traversal_verified']
mixed=evidence['bridge-mixed-real-scenes.json'];assert mixed['mixed_runtime_classes_verified'] and mixed['opposing_bridge_traffic_verified']
assert not mixed['nonprimary_natural_entry_proved']
assert not evidence['internal-real-scenes.json']['nonprimary_overlapping_adapter_naturally_observed']
assert not evidence['overlap-caller-identity.json']['nonprimary_overlapping_adapter_naturally_observed']
alias_runtime=evidence['alias-natural-scenes.json'];assert alias_runtime['passed'] and alias_runtime['static_aliases']==22
assert alias_runtime['additional_observer_frames']==2703 and not alias_runtime['nonprimary_natural_entry_proved']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==171 and len(receipt['inputs'])==289 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
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
assert read(S/'native-round30-identity.json')['total_cases']==196608
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,30)]
archives += [('v30-baseline',S/'baseline','source-manifest.json','')]
archives += [(name,S/'parts'/name,'manifest.json','') for name in parts]
for label,base,manifest_name,sub in archives:
    entries=read(base/manifest_name)
    for item in entries:assert sha(base/sub/item['path'])==item['sha256'],(label,item['path'])
    counts[label]=len(entries)
for item in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/item['name'])==item['sha256'],item['name']
counts['H_originals']=20
for p,h in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),(R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),(P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==h,str(p)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:assert (P/'reports'/name).read_bytes()==(S/'baseline/project/reports'/name).read_bytes()
preservation=dict(passed=True,counts=counts,unsupported_guards=37,original_inputs_save_old_engine_preserved=True);write(S/'preservation.json',preservation)
startup=read(S/'startup-failures.json');assert startup['passed']
for attempt in startup['attempts']:
    assert attempt['simulation_frames']==0
    for item in attempt['preserved_files']:assert sha(Path(attempt['preserved_path'])/item['path'])==item['sha256']
    assert read(S/'runs'/attempt['tag']/'comparison.json')['passed']
preservation['original_preframe_startup_failures_preserved']=len(startup['attempts']);write(S/'preservation.json',preservation)
report=P/'docs/单位移动第二十九批-桥上混类链与动态交通及服务出口-20261023.txt'
handoff=P/'交接文档-单位移动第二十九批正式验收-20261023.txt';assert not report.exists() and not handoff.exists()
template=read(S/'pending/template-remainder-integration.json');objects=read(S/'pending/enemy-kind-integration.json');exits=read(S/'pending/service-exit-integration.json')
assert template['copies']==10 and objects['copies']==3 and exits['unique_entries']==3
body=f'''单位移动第二十九批正式验收（2026-10-23）
正式代次29 / 验证轮次30
父提交：018c1bb719d0f51508111400b040583ecb0414dd
程序：{exe}
SHA-256：{digest}
证据：{S}

第二十八批018c1bb、6853d622795908f7f15aa15421cfbf59b5682ada6339382e40a2e3bbad6a13bb及3584项源封存先行只读核对，工作区干净；本批先保存完整基线与项目指针。

1. 分段整理及回退
模板普通/备用索引抽成ra2_ground_template_index，主完整步进与4A1FBE的10处内部接续共用，保留带符号表字节、AL宽度测试和活跃寄存器。
敌方具体类别尾部抽成ra2_ground_classify_enemy_kind，完整敌方分类与703A12三处内部接续共用。保留建筑1350标志、地形选武器/取武器/取弹头/146标志的短路顺序和通行等级提升；没有将这些未确认字段强行命名为INI选项。
4A46FE清模板及路径后调用4C8归零服务、4A41AE/4A41CC递归Prepare并返回，三类共{exits['copies']}处共享出口。保持写入、重读owner、服务参数、回调修改保存区、返回EAX高位及出栈顺序。
每部分6场景3406帧（默认901、三格包围101、默认规则真实AI预算901、双向隧道各501、出口占用501），全部与原版逐帧一致；每份保留全部编译输入、EXE与源码清单：
'''+''.join(n+' : '+v['exe_sha256']+'\n' for n,v in parts.items())+f'''
最终仍171个C源，新增ground_enemy_kind.h，共289项编译输入。最终内容构建强制刷新0，最终输入和EXE与returns回退一致。生成0010保留LF、0046保留CRLF；旧标签、尾部目标、37个未实现保护、schema12与两份公共比较器保持。

2. 原版对照
102组片段门禁通过，既有99组重跑；新增模板索引、具体对象类别及含服务调用出口各65536例，共196608例。片段检查与自然运行证据分别保留。
最终52个生产场景32122帧（原移动矩阵27场14897帧、默认901帧、连接12场6712帧、四个高差占用组合2404帧、原桥链四场3604帧、新混类/交通四场3604帧）完整状态、随机数、命令和有序查询一致。另预算901帧、内部观察4054帧、连接观察9116帧、两套桥观察7208帧、新别名探测三场2703帧；后三场重用已验收合法地图/命令及观察程序，只增加首次解析探测参数，原版/C与正式状态均一致。
原有第28帧步兵坐标、包围第52帧、转弯第197帧、失败第399帧及持续失败、27..37帧预算10..0和第38帧停止继续保持。默认预算仍是正常构造和初次下令的受控场景；未经干预随机发生频率及4C3895独立回调未测。

3. 桥上混类链与动态交通
保留原版真实桥覆盖物和已验收桥下地形，普通地图对象格式使同一60,66格上下层各有两名E2及一辆TRUCKA，初态Z分别0/416。新四场各901帧；双向混类场景和双向对向交通场景，交通通过普通移动命令让原地车辆离开并使两辆车相向行驶。没有原始运动、链指针、桥层、路径或预算写入。
独立观察沿用12个测试对象替换和已核对串接钩子，增加第二交通对象过滤。原版/C以及正式/观察记录完全一致；实际完整上层混类链{mixed['totals']['full_mixed_chains']}次，混类上层查询{mixed['totals']['mixed_queries']}次，对向移动分类{mixed['totals']['moving_interactions']}次、几何判断{mixed['totals']['geometry_interactions']}次。计数依据访问的实际对象ID和运行时对象类，链头、各项next及零链尾按实测核对。
逐场最终位置、目标是否清空及原版行为写入bridge-mixed-real-scenes.json；查询或交通命中不自动等于成功穿越。对象范围为友方步兵与普通车辆，建筑/地形/敌方混链、毁桥及所有桥结构组合未穷尽。

4. 合法自然来源及原版异常
保留三主入口/原九别名的38条入边核对，并按本批五处新片段的所有父C副本扩大到22个别名（新增13个）、三主入口，共{evidence['internal-alias-sources.json']['unique_native_edges']}条原生入边逐条核对PE字节，扫描全部171源和289输入。已知别名来源仍为原函数内部跳转；没有直接C调用、直接原生CALL、函数外跳入或非代码区地址常量来源。新三场合法桥移动在八项参数限制内分组覆盖13个新增候选，原九个由混类四场覆盖；首次间接解析日志以主703040为正控，22个非主C副本均无首次调用记录。没有排除任意计算目标、运行中产生的指针和未运行场景；非主副本合法自然入口仍未证明。
既有4→6弯曲上行停滞、7→4弯曲下行高度下漂继续与原版一致，只算一致性、不计成功穿越。四个成功高差/出口占用组合回归，真实占用、连续等待及最终退出均验证，未改原版异常。
v9..v29旧档、本轮3584项baseline及三份parts逐项复核，H盘20项输入、原游戏、SAV和旧手写引擎保持。开发阶段预检失败保留于investigations，未作为验收。本轮原版首帧前图形启动失败共{len(startup['attempts'])}次，现场、哈希及替代结果另载startup-failures.json；若有此类失败，不计为模拟差异，也不对启动根因作结论。
新九项生产源、两项探针、一项观察器及四份混类桥地图通过隔离配方重放。所有通过记录绑定本批实际程序和来源。
完整Advance、Prepare、对象分类、连接及全游戏等价仍未完成。下一批继续其余内部模板、具体类别/动态关系接续和含服务调用出口，扩大异类/敌方桥交通；非主副本只按合法自然来源增加覆盖声明。
本地提交，不推送，不修改远端配置。
'''
report.write_text(body,encoding='utf-8',newline='\n');handoff.write_text(body+'\n接手先运行verify_final_movement_v30.py，再保存下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';existing(guide,f'第二十九批当前状态（2026-10-23）\n模板索引/具体敌方对象类别/三类服务出口；各部分6场景3406帧。52场景32122帧、102组门禁，桥上混类链与对向交通实景通过。完整移动和非主C自然入口仍未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动第二十九批：内部模板索引、具体对象分类与服务出口；52场景32122帧、102组片段门禁，桥上混类链与动态交通实景通过。入口为[第二十九批交接](交接文档-单位移动第二十九批正式验收-20261023.txt)和 `reports/latest-recovery.json`。基线、回退与原版异常保留；非主入口及全游戏等价未完成。\n';existing(p,''.join(lines))
p=P/'交接文档-新对话继续推进-20261022.txt';existing(p,f'最新接续：第二十九批已验收，正式29 / 验证30。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R/"verify_final_movement_v30.py"}\n以下历史保留。\n\n'+p.read_text(encoding='utf-8'))
p=P/'交接文档-原版逆向与C重编译-20261020.txt';existing(p,p.read_text(encoding='utf-8')+f'\n2026-10-23 第二十九批接续：{handoff}\n52场景32122帧，102组片段门禁；桥上混类/动态交通实景通过，非主入口仍未证明。\n')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v30*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ['.c','.h','.asm'] or p.name in ['truck-actor-fixture-probe.exe','connection-fixture-probe.exe','connection-fixture.map','truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[]
for rel in sorted(paths):
    dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(R/rel)))
write(S/'source-manifest.json',manifest)
for document in [report,handoff]:
    with document.open('a',encoding='utf-8') as stream:stream.write(f'\n最终源封存：{len(manifest)}项。当前身份以validation.json/source-manifest.json为准。下一轮必须保留内容构建、独立观察器重建、结构/配方、原版片段和生产逐帧门禁，不能仅替换脚本后缀。\n')
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')};flags.update(template_remainder_index_shared_readable=True,concrete_enemy_kind_shared_readable=True,service_bearing_prepare_exits_shared_readable=True)
validation=dict(passed=True,formal_baseline_generation=29,verification_round=30,exe_sha256=digest,state_schema=12,paired_scenes=52,paired_frames=32122,probes=102,new_fragment_cases=196608,
    production_c_sources=171,content_inputs=289,source_files=len(manifest),unsupported_guards=37,final_build_inputs_match_returns_checkpoint=True,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    independent_default_budget_frames=901,independent_internal_observer_frames=4054,independent_connection_observer_frames=9116,independent_bridge_observer_frames=7208,
    independent_alias_observer_frames=2703,legal_alias_sources_examined=22,new_alias_runtime_probe_targets=13,
    bridge_upper_and_lower_three_object_traversal_verified=True,bridge_mixed_object_chain_verified=True,bridge_opposing_dynamic_traffic_verified=True,
    bridge_multiobject_scenes=8,bridge_multiobject_frames=7208,
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    bridge_runtime_evidence=str(S/'bridge-real-scenes.json'),bridge_mixed_runtime_evidence=str(S/'bridge-mixed-real-scenes.json'),legal_overlap_sources=str(S/'internal-alias-sources.json'),
    alias_runtime_evidence=str(S/'alias-natural-scenes.json'),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),original_preframe_startup_failures_preserved=len(startup['attempts']),
    rare_branch_evidence_scope=evidence['connection-real-scenes.json']['scope']+' '+mixed['scope']+' '+alias_runtime['limits'],
    combined_curved_height_occupied_runtime_verified=True,combined_curved_height_occupied_scenes=4,original_equivalent_stall_scenes=2,all_curved_height_routes_complete=False,
    nonprimary_overlapping_adapter_naturally_observed=False,full_original_equivalence_verified=False,strict_ordered_audit_passed=True,frame_comparison_passed=True,
    default_rules_full_budget_exhaustion_verified=True,budget_scope=evidence['budget-real-scenes.json']['scope'],preservation=preservation,report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation);accept.update(paired_scenes=52,paired_frames=32122,**flags);write(S/'strict-acceptance.json',accept)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update({k:v for k,v in validation.items() if k not in ['exe_sha256','source_files','part_checkpoints','preservation']})
for k in ['system_interruption_recovered','interrupted_pairs_preserved','resumption_evidence','serial_startup_retries_passed']:recovery.pop(k,None)
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),next_readable_region='Remaining template and concrete object continuations, service exits, hostile bridge traffic and legal computed alias sources')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(passed=True,validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=52,paired_frames=32122,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=29,verification_round=30,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(exe),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff)))
print(json.dumps(dict(passed=True,formal_baseline=29,exe_sha256=digest,source_files=len(manifest))))
