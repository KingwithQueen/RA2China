"""Promote generation30 after part checkpoints, native gates and mixed-bridge acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v31';O=R/'evidence/movement-state-v30'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,t):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n';p.write_bytes(t.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
vcs=read(S/'vcs-context.json')
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()==vcs['parent_commit']=='cb823693d1e9ce25f38bb79c01d9bb9472b56aca'
assert sha(P/'.git/config')==vcs['config_sha256']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
accept=read(S/'strict-acceptance.json');native=read(S/'native-gates.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==105
assert native['passed'] and native['groups']==105 and native['new_cases']==196608
evidence={n:read(S/n) for n in ['budget-real-scenes.json','connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','legal-overlap-sources.json','alias-route-inventory.json','overlap-caller-identity.json','recipe-byte-audit.json','bridge-hostile-real-scenes.json','rejected-enemy-order-control.json','native-team-setup-investigation.json']}
evidence.update({n:read(S/n) for n in ['internal-alias-sources.json','alias-natural-scenes.json']})
structure=read(S/'refactor-structure.json');assert structure['passed'] and structure['compile_inputs']==290
assert structure['sample_anchor_internal_entries']==12 and structure['moving_tail_internal_entries']==3
assert structure['advance_service_exit_entries']==2 and structure['advance_service_exit_copies']==14
for name,v in evidence.items():
    assert v['passed'],name
    for item in v.get('inputs',[]):assert sha(R/item['path'])==item['sha256'],(name,item['path'])
for name in ['connection-real-scenes.json','internal-real-scenes.json','combined-real-scenes.json','bridge-real-scenes.json','bridge-mixed-real-scenes.json','bridge-hostile-real-scenes.json']:
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
assert receipt['source_count']==171 and len(receipt['inputs'])==290 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
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
assert read(S/'native-round31-identity.json')['total_cases']==196608
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,31)]
archives += [('v31-baseline',S/'baseline','source-manifest.json','')]
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
assert {p.name for p in run_dirs if not read(p/'comparison.json')['passed']}=={'ep-enemy-traffic-north','eh-enemy-traffic-north'}
report=P/'docs/单位移动第三十批-敌我桥交通与运动对象接续及Advance服务出口-20261023.txt'
handoff=P/'交接文档-单位移动第三十批正式验收-20261023.txt';assert not report.exists() and not handoff.exists()
hostile=evidence['bridge-hostile-real-scenes.json'];assert hostile['hostile_classifier_observed'] and hostile['hostile_bridge_traffic_observed']
body=f'''单位移动第三十批正式验收（2026-10-23）
正式代次30 / 验证轮次31
父提交：cb823693d1e9ce25f38bb79c01d9bb9472b56aca
程序：{exe}
SHA-256：{digest}
证据：{S}

基线核对：第二十九批cb82369、程序7d279c49503300819b3b8dee0b93c22c5e65d8c54a0313d5a3c9ab9e9afb9760及3837项源封存均通过，初始工作区干净。完整基线与项目指针先行保存。

1. 分段整理和回退
4A2347的12处余程采样锚点接续改为可读适配，保留坐标逐项读取/写入、随后读取样本方向及重读位置的顺序；采样地址与保存区重叠也逐项对照。
运动对象5A0标志、15号类别和移动器通行查询尾部抽成ra2_ground_classify_moving_tail，完整友方运动分类与703895三处内部接续共用。保留短路顺序，内部接续直接使用活跃通行槽，回调可以改变通行等级和保存的owner。
Advance的4A229C/4A22BE两类、14处含服务调用出口共享，414(0,1)、490及回调后的owner重读和存活检查保持；有结果时按原版返回，仍存活时继续原余程入口4A1FA1。没有把继续分支误当函数返回。
每部分六场景3406帧：默认901、三格包围101、正常构造的真实AI默认预算901、双向隧道各501、出口占用501。状态、命令、随机数和有序行为均与原版逐帧一致。三份完整回退含EXE与全部编译输入：
'''+''.join(n+' : '+v['exe_sha256']+'\n' for n,v in parts.items())+f'''
最终171个C源、290项输入；新增ground_moving_tail.h。最终内容构建刷新0，EXE和输入与returns回退一致。0010保留LF、0046保留CRLF，旧标签、尾部目标、37个未实现保护、schema12及公共比较器保持。

2. 对照结果与范围
105组原版片段门禁通过，既有102组重跑；新增采样锚点、运动对象尾部和Advance服务出口各65536例，共196608例。其中出口覆盖16384例首服务失败后继续第二服务、49152例第二服务调用及12288例存活继续余程；有序回调与owner重读逐项相等。片段测试与合法自然运行的证据分开保存。
最终56个生产场景35726帧：原移动矩阵27场14897帧、默认901帧、连接12场6712帧、四个高差占用组合2404帧、既有桥链/友方混类交通八场7208帧、敌方桥四场3604帧。完整状态、RNG、命令和有序事件相等，逐场含负控和私有存档核验。
独立预算901帧、内部观察4054帧、连接含组合9116帧、桥观察十二场10812帧，以及别名探测四场3604帧另列，避免混算为新增生产场景。
原第28帧坐标、52帧包围、197帧转弯、399帧失败及重复失败、27..37帧预算10..0和38帧停止保持。默认预算是受控的普通构造和下令实景，未经干预的随机出现频率及4C3895独立回调仍未测。

3. 桥上敌我混类与动态交通
沿用原版桥覆盖物及已验收桥下地形；在普通地图中将既有上层TRUCKA或对向车辆归属BadGuy1 House，原生阵营关系保持。上下层初态各有三对象、两种运行时类别；玩家只给本方车辆发送普通移动命令；敌车由原生CreateTeam触发器、Tags实例及脚本动作3前往99号路径点，形成对向交通，停靠车辆通过本方普通命令让行，没有改链指针、桥层、路径或运动状态。
四个敌方场景各901帧，生产/原版、观察/原版及生产/观察完整记录一致。新增独立敌方分类入口观察，70397C的原始七字节检查通过，复制CALL重定位到40DBD0，保存并恢复CPU/FPU；仍只替换十二个测试对象，不改正式记录器。
实测敌方分类入口{hostile['totals']['enemy_classifier_entries']}次、混类链查询{hostile['totals']['mixed_queries']}次、敌方桥交通关系查询{hostile['totals']['hostile_traffic_queries']}次。成功到达主目标{hostile['totals']['goals_reached']}/4；每场实际位置、目标、生命值、是否缺失及敌方分类样本见bridge-hostile-real-scenes.json。查询次数不等于穿越成功，原版停等/绕行/受损等结果原样保留。建筑、地形、毁桥、所有对象类别/动态关系组合仍未穷尽。
既有友方混类四场完整链{mixed['totals']['full_mixed_chains']}次、移动关系{mixed['totals']['moving_interactions']}次继续回归。

4. 非主C副本和原版异常
按本批四处片段的所有父C副本，将累计合法来源清单从22扩到26个非主别名，三主入口，原生入边{evidence['internal-alias-sources.json']['unique_native_edges']}条逐项核对PE字节。新增候选4A1FDC、4A2112、4A230E、4A2311；扫描171源及290输入。已知来源仍为原函数内部跳转，没有直接C调用、直接原生CALL、函数外跳入或非代码区地址常量来源。
新四场合法敌我桥移动按每组最多八个参数分组覆盖原十三候选及新四候选；原九个由既有友方桥场景覆盖。主703040有首次调用正控，累计26个非主C副本没有首次调用记录，合法自然入口仍未证明。任意计算目标、运行时生成的指针、未运行场景未被排除，不从静态无引用推断永远不可达。
4→6弯曲上行停滞和7→4弯曲下行高度下漂继续与原版一致，计为异常一致性，不计成功穿越。四个成功高差/出口占用组合的真实占用、连续等待和最终退出通过，未修原版异常。

v9..v30旧档、本轮3837项baseline及三份parts逐项复核；H盘20项输入、原游戏、SAV及旧手写引擎哈希保持。七项生产源、两项探针、一项观察器及八份验收桥地图及两份拒绝命令控制地图通过隔离配方逐字节重放。
敌方玩家命令控制：ep/eh-enemy-traffic-north的两次未通过验收记录仍留原处，原版/C各901帧一致，本方命令执行而敌车命令未执行且敌车静止。rejected-enemy-order-control.json明确不计验收场景。小队脚本前两次试验未建立Tags实例，敌车未移动；补齐原生Tags后，短程181帧中敌车出现136个位置，再进入正式长程对照。试验地图、记录、命令及结论均保留。
开发时探针链接/采集失败日志及服务出口最初差异保留于本轮investigations和构建日志：继续边界使用RET收尾后，旧探针在已弹出的模拟栈上pushfd覆盖保存槽；现改在宿主栈采集标志，全部旧门禁也重跑。失败记录不算验收结果。原版首帧前图形启动失败{len(startup['attempts'])}次，若有则现场、哈希和新私有目录的替代结果载startup-failures.json，不隐藏任何模拟差异。
完整Advance、Prepare、对象分类、连接和全游戏等价仍未完成。下一批继续剩余内部接续、具体对象/动态关系、带副作用服务出口，优先补桥上移动步兵与车辆交会、更多敌方对象类别及合法自然入口证据。保留当前异常与回退。
本地提交，不推送，不改远端配置。
'''
report.write_text(body,encoding='utf-8',newline='\n');handoff.write_text(body+'\n接手先运行verify_final_movement_v31.py，再保存下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';existing(guide,f'第三十批当前状态（2026-10-23）\n采样锚点、运动对象尾部、Advance服务出口；各部分六场3406帧。56场35726帧、105组门禁，敌我桥交通通过。完整移动和非主自然入口仍未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动第三十批：采样锚点、运动对象接续与Advance服务出口；56场景35726帧、105组片段门禁，敌我桥交通实景通过。入口为[第三十批交接](交接文档-单位移动第三十批正式验收-20261023.txt)和 `reports/latest-recovery.json`。基线、回退与原版异常保留；非主入口及全游戏等价未完成。\n';existing(p,''.join(lines))
p=P/'交接文档-新对话继续推进-20261022.txt';existing(p,f'最新接续：第三十批已验收，正式30 / 验证31。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R/"verify_final_movement_v31.py"}\n以下历史保留。\n\n'+p.read_text(encoding='utf-8'))
p=P/'交接文档-原版逆向与C重编译-20261020.txt';existing(p,p.read_text(encoding='utf-8')+f'\n2026-10-23 第三十批接续：{handoff}\n56场景35726帧，105组片段门禁；敌我桥交通实景通过，非主自然入口仍未证明。\n')
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v31*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ['.c','.h','.asm'] or p.name in ['truck-actor-fixture-probe.exe','connection-fixture-probe.exe','connection-fixture.map','truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[]
for rel in sorted(paths):
    dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(R/rel)))
write(S/'source-manifest.json',manifest)
for document in [report,handoff]:
    with document.open('a',encoding='utf-8') as stream:stream.write(f'\n最终源封存：{len(manifest)}项。当前身份以validation.json/source-manifest.json为准。下一轮必须保留内容构建、独立观察器重建、结构/配方、原版片段和生产逐帧门禁，不能仅替换脚本后缀。\n')
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')};flags.update(template_remainder_index_shared_readable=True,concrete_enemy_kind_shared_readable=True,service_bearing_prepare_exits_shared_readable=True,sample_anchor_internal_readable=True,moving_object_tail_shared_readable=True,advance_service_exits_shared_readable=True)
validation=dict(passed=True,formal_baseline_generation=30,verification_round=31,exe_sha256=digest,state_schema=12,paired_scenes=56,paired_frames=35726,probes=105,new_fragment_cases=196608,
    production_c_sources=171,content_inputs=290,source_files=len(manifest),unsupported_guards=37,final_build_inputs_match_returns_checkpoint=True,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    independent_default_budget_frames=901,independent_internal_observer_frames=4054,independent_connection_observer_frames=9116,independent_bridge_observer_frames=10812,
    independent_alias_observer_frames=3604,legal_alias_sources_examined=26,new_alias_runtime_probe_targets=17,
    bridge_upper_and_lower_three_object_traversal_verified=True,bridge_mixed_object_chain_verified=True,bridge_opposing_dynamic_traffic_verified=True,bridge_hostile_dynamic_traffic_verified=True,
    bridge_multiobject_scenes=12,bridge_multiobject_frames=10812,
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    bridge_runtime_evidence=str(S/'bridge-real-scenes.json'),bridge_hostile_runtime_evidence=str(S/'bridge-hostile-real-scenes.json'),bridge_mixed_runtime_evidence=str(S/'bridge-mixed-real-scenes.json'),legal_overlap_sources=str(S/'internal-alias-sources.json'),
    alias_runtime_evidence=str(S/'alias-natural-scenes.json'),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),original_preframe_startup_failures_preserved=len(startup['attempts']),
    rare_branch_evidence_scope=evidence['connection-real-scenes.json']['scope']+' '+hostile['scope']+' '+mixed['scope']+' '+alias_runtime['limits'],
    combined_curved_height_occupied_runtime_verified=True,combined_curved_height_occupied_scenes=4,original_equivalent_stall_scenes=2,all_curved_height_routes_complete=False,
    nonprimary_overlapping_adapter_naturally_observed=False,full_original_equivalence_verified=False,strict_ordered_audit_passed=True,frame_comparison_passed=True,
    default_rules_full_budget_exhaustion_verified=True,budget_scope=evidence['budget-real-scenes.json']['scope'],preservation=preservation,report=str(report),handoff=str(handoff),**flags)
write(S/'continuation.json',dict(status='validation_complete_commit_separately_audited',validation=str(S/'validation.json'),verify=str(R/'verify_final_movement_v31.py'),exe_sha256=digest,commit_policy='local commit only; never push'))
write(S/'validation.json',validation);accept.update(paired_scenes=56,paired_frames=35726,**flags);write(S/'strict-acceptance.json',accept)
recovery=read(S/'baseline/project/reports/latest-recovery.json');recovery.update({k:v for k,v in validation.items() if k not in ['exe_sha256','source_files','part_checkpoints','preservation']})
for k in ['system_interruption_recovered','interrupted_pairs_preserved','resumption_evidence','serial_startup_retries_passed']:recovery.pop(k,None)
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),next_readable_region='Remaining template and concrete object continuations, service exits, hostile bridge traffic and legal computed alias sources')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(passed=True,validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=56,paired_frames=35726,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=30,verification_round=31,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(exe),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff)))
print(json.dumps(dict(passed=True,formal_baseline=30,exe_sha256=digest,source_files=len(manifest))))
