"""Promote generation 28 only after all round-29 production and native gates pass."""
from pathlib import Path
import difflib, hashlib, json, re, shutil, subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v29';O=R/'evidence/movement-state-v28'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def existing(p,text):
    nl='\r\n' if b'\r\n' in p.read_bytes() else '\n'
    p.write_bytes(text.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
tubes=read(S/'connection-real-scenes.json');internal=read(S/'internal-real-scenes.json');combined=read(S/'combined-real-scenes.json')
for item in [accept,budget,tubes,internal,combined,read(S/'native-gates.json'),read(S/'refactor-structure.json'),read(S/'legal-overlap-sources.json')]:
    assert item['passed']
assert accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==99
assert tubes['production_scenes']==12 and tubes['production_frames']==6712
assert tubes['completed_scenes']==10 and tubes['original_equivalent_stall_scenes']==2 and not tubes['all_curved_height_routes_complete']
assert combined['production_scenes']==4 and combined['production_frames']==2404
assert internal['independent_frames']==4054 and all(internal['stages'][str(i)]>0 for i in range(10,22))
assert not internal['nonprimary_overlapping_adapter_naturally_observed']
assert budget['default_rules_full_exhaustion_verified']
for report_name in ['legal-overlap-sources.json','overlap-caller-identity.json','recipe-byte-audit.json','alias-route-inventory.json']:
    identity=read(S/report_name)
    assert identity['passed']
    for item in identity['inputs']:assert sha(R/item['path'])==item['sha256'],item['path']
for entry in read(S/'legal-overlap-sources.json')['entries']:
    if entry['entry_kind']!='alias':continue
    address=int(entry['entry'],16)
    lo,hi=(0x4A1000,0x4A2670) if address<0x4A2670 else (0x4A2670,0x4A4740) if address<0x700000 else (0x703040,0x703BD0)
    assert all(lo<=int(edge['address'],16)<hi and edge['instruction']!='call' for edge in entry['decoded_incoming'])
bridge=read(S/'bridge-real-scenes.json');assert bridge['passed'] and bridge['actual_ordered_three_object_traversal_verified']
assert bridge['full_chains']['upper']>0 and bridge['full_chains']['lower']>0
startup=read(S/'startup-failures.json');assert startup['passed']
resumption=read(S/'resumption-validation.json');assert resumption['passed']
assert resumption['incomplete_pairs_preserved']==2 and resumption['replacements_strictly_passed']
assert resumption['production_exe_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
for item in resumption['inputs']:assert sha(R/item['path'])==item['sha256'],item['path']
for entry in startup['attempts']:
    assert entry['simulation_frames']==0
    base=Path(entry['preserved_path']);assert base.resolve().is_relative_to(S.resolve())
    for item in entry['preserved_files']:assert sha(base/item['path'])==item['sha256']
    assert read(S/'runs'/entry['tag']/'comparison.json')['passed']
assert read(S/'bridge-goal-controls.json')['passed']

exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']==tubes['production_executable_sha256']==internal['production_executable_sha256']==combined['production_executable_sha256']==bridge['production_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==171 and len(receipt['inputs'])==288 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
parts={name:read(S/'parts'/name/'validation.json') for name in ['template-verified','passage-verified','returns-verified']}
for name,value in parts.items():
    assert value['passed'] and len(value['scenes'])==6 and sum(x['frames'] for x in value['scenes'])==3406
    archived={e['path']:e['sha256'] for e in read(S/'parts'/name/'manifest.json')}
    inputs=read(S/'parts'/name/'ra2/build-original-c/source-content-receipt.json')['inputs']
    assert all(archived[Path(p).relative_to(R).as_posix()]==h for p,h in inputs.items())
assert parts['returns-verified']['exe_sha256']==digest
final_inputs={e['path']:e['sha256'] for e in read(S/'parts/returns-verified/manifest.json')}
assert all(final_inputs[Path(p).relative_to(R).as_posix()]==h for p,h in receipt['inputs'].items())
default=read(S/'runs/c-final-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for mode in ['original','generated-c']:
    for line in (S/'runs/c-final-default'/mode/'state.jsonl').open(encoding='utf-8'):
        row=json.loads(line)
        if row['kind']=='state' and row['frame']==28:
            assert next(o for o in row['objects'] if o['id']==1032262)['position'][0]==17343
            break
    else:raise AssertionError('missing frame28')
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
    assert (P/'reports'/name).read_bytes()==(S/'baseline/project/reports'/name).read_bytes(),name
identities={}
for name,cases in [('internal',131072),('connection-numeric',1601904),('tube-state',131072),('progress',491520),('travel',360448),('joint',262144),('overlap',262144),('round28',196608),('round29',196608)]:
    identity=read(S/('native-'+name+'-identity.json'))
    assert identity['passed'] and identity['total_cases']==cases,name
    for item in identity['inputs']+identity.get('probe_executables',[])+([identity['probe_executable']] if 'probe_executable' in identity else []):
        assert sha(R/item['path'])==item['sha256'],item['path']
    identities[name]=identity
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,29)]
archives += [('v29-baseline',S/'baseline','source-manifest.json','')]
archives += [(name,S/'parts'/name,'manifest.json','') for name in parts]
for label,base,manifest_name,sub in archives:
    entries=read(base/manifest_name)
    for item in entries:assert sha(base/sub/item['path'])==item['sha256'],(label,item['path'])
    counts[label]=len(entries)
for item in read(R/'evidence/original-inputs-before.json'):
    assert sha(Path('H:/开发/运行版本/原版1.006')/item['name'])==item['sha256'],item['name']
counts['H_originals']=20
for p,h in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),
            (R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),
            (P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==h,str(p)
guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (R/'ra2/src/recomp/gen_game').glob('*.c'))
assert guards==37
preservation=dict(passed=True,counts=counts,unsupported_guards=guards,game_save_old_engine_preserved=True)
preservation['original_preframe_startup_failures_preserved']=len(startup['attempts'])
write(S/'preservation.json',preservation)
exits=read(S/'pending/shared-exit-integration.json')
assert exits['unique_entries']==4 and exits['overlapping_copies']==11
for source,dest in [('template-integration.json','template-integration.json'),('object-kind-integration.json','passage-integration.json'),('shared-exit-integration.json','returns-integration.json')]:
    write(S/dest,read(S/'pending'/source))
report=P/'docs/单位移动第二十八批-桥层多对象链与内部接续及写回出口-20261023.txt'
handoff=P/'交接文档-单位移动第二十八批正式验收-20261023.txt'
assert not report.exists() and not handoff.exists()
parent=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
part_text='\n'.join(name+' : '+value['exe_sha256'] for name,value in parts.items())
body=f'''单位移动第二十八批正式验收（2026-10-23）
正式代次28 / 验证轮次29
父提交：{parent}
程序：{exe}
SHA-256：{digest}
证据：{S}

1. 当前基线与逐部分回退
接手先只读核对第二十七批3cbe4f4、EXE 597bfc9d99c93154564687292098ed199b8a98ea5848d587459317aa0859e5e8及3340项源封存，工作区干净。
本批先保存全部3340项基线及项目指针。三部分各6场景3406帧：默认遭遇战901、三格包围101、默认规则真实AI预算901、双向隧道各501、出口占用501。
{part_text}
每部分保留EXE、全部编译输入、源清单和验收身份；最终288项输入及EXE与returns回退一致。

2. 可读C17/x86整理
模板表选择与直行回退抽成ground_template_table；主模板选择和4A3FE3的7处内部副本复用，布局及活跃寄存器/标志恢复留在runtime。
建筑筛选拆出ground_building_flags，完整建筑筛选与7035DF的2处内部接续共享，保留建筑任务、阵营、邻格查询及其顺序。
4A26FE、4A28F6、4A2F3B、4A3F55共4类11处带写内存出口共享实现。保留写调用者结果、清模板状态、AL及高位、指针返回高位和出栈顺序。专门覆盖输出地址与已保存EDI/ESI/EBP/EBX重叠，以及模板写入覆盖保存区的先后顺序。
正式仍171个C源，增加两个业务头，共288项编译输入，空操作构建刷新0。0010保留LF、0046保留CRLF；旧标签、尾部目标、37个未实现保护保留。schema12和两份公共比较器未改。

3. 原版片段与逐帧验证
99组原版片段检查通过，既有96组重新运行；本批模板表、建筑标志内部入口、4类写回出口各65536例，共196608例。
最终48个生产场景28518帧，状态、命令、随机数及有序记录完全一致；另默认预算901帧、内部观察4054帧、连接观察9116帧、桥链独立观察3604帧。
连续帧、坐标差异/缺帧负控、辅助菜单及非法命令门禁通过。既有步兵第28帧、包围第52帧、转弯第197帧、失败第399帧与451..1111每60帧、默认预算27..37帧10..0及第38帧停止持续保持。
默认预算仍是正常服务构造AI TRUCKA和敌车的受控场景；没有把未经干预随机频率或4C3895独立回调写成已测。

4. 优先完成的桥上多对象链实景
保留原SOV01T桥覆盖物，用合法IsoMapPack5在桥上基图配置24格桥下地面、在桥下横穿图配置60格通行走廊；普通地图对象装载在同一60,66格的上下层各放三名E2，使用2/3/4正常步兵子位置。原版初态桥下Z=0、桥上Z=416。
TRUCKA分别从桥北、桥南及桥下东西两侧桥外接受普通移动命令，4个生产/4个独立观察场景各901帧。未写桥层标记、对象链、路径或预算内存。
独立记录每次请求层、两层真实链长度及实际非自身对象访问。原版与C有序记录一致，三对象完整链上层{bridge['full_chains']['upper']}次、下层{bridge['full_chains']['lower']}次；计数仅纳入两层均有3对象的共同占格查询；链头、逐项访问、下一对象和零链尾相符，另一层对象没有混入。下层步兵会按原版正常让路而离开共格，之后的额外三对象链另记，不混入本门槛。生产/观察状态及命令逐帧一致。
703473已被正式记录器占用，独立观察器串接经字节核对的原钩子，保留原日志和顺序。观察程序仍仅替换12个诊断对象，不进入正式程序。
桥多对象链覆盖的是同类友方步兵与普通车辆查询；不同类对象混链、桥上拥堵/攻击/毁桥/所有桥结构组合未穷尽。通行判断命中不等于全部路线成功通过，本批成功到达并清空目的地{bridge['completed_crossings']} / 4，最终位置/目的地逐场记录在bridge-real-scenes.json。

5. 非主C副本合法来源继续核查
对三个主入口和九个别名共38条原生入边（其中别名27条）与PE字节再次核对，已知来源仍为原函数内部跳转。未发现直接CALL或非代码区地址常量指向别名；生成C注册不是原生来源。扫描全部171个正式C源及288项项目编译输入，九个符号仅出现为注释、声明、定义和注册，没有直接C调用。
在四个桥实景中分两组启用既有间接入口首次调用日志，覆盖全部九个别名，并以703040主入口实际命中作正控。九个别名均无首次调用记录。固定帧完成使用ExitProcess，未输出全程计数；既有日志会打印每个目标前五次调用。结合真实返回地址、链接MAP及调用字节，当前自然对象链适配仍从703040主入口进入。
因此非主C副本合法自然入口仍未证明。任意计算目标、运行中构造指针及未跑场景没有被排除，不人为跳入别名冒充自然覆盖。

6. 高差组合、原版异常与保存
原有12个连接场景6712帧及4个弯曲高差/出口占用组合2404帧继续回归。4→7上行、6→4下行和镜像组合完成；4→6弯曲上行与7→4弯曲下行仍忠实复现原版停滞/漂移，仅算一致性，不算成功穿越。没有兼容性修补。另有{len(startup['attempts'])}次原版在首帧前Prep direct draw阶段访问冲突，完整目录/日志/哈希收据封存于startup-failures.json所列路径；相同程序和场景串行重跑通过。未产生模拟状态的启动失败不计入模拟差异，启动根因仍未确定。
v9..v28旧正式档、本轮3340项baseline及三份parts重新核对；H盘20项原始输入、原game.exe、SAV及旧手写引擎保持。桥下最初两场目标仍在桥格，原版拒绝移动/无链查询；保留h3-lower-north/south及b-lower-north/south，仅算一致性，不算链覆盖。开发阶段脚本/构建错误、观察参数超限及钩子冲突均保留日志和旧观察程序，不覆盖旧正式证据。
用户报告系统蓝屏后恢复：先核对第二十七批3340项基线和当前288项编译输入，z-tu/z-td两场未完成记录及日志按哈希封存于interruption-recovery.json所列目录，未计入验收；相同程序重新生成私有测试目录并完成逐帧对照。另一次受限进程在建立资源硬链接时被拒绝，发生于游戏启动前，现场和日志保留；随后使用获准执行环境完成补测。恢复期间正式程序未改。resumption-validation.json绑定封存与替代记录，不对系统蓝屏根因作判断。
集成脚本从受保护基线隔离重放9项生产源，2项探针、观察器及4份桥地图逐字节复现。最终源码和验收来源封存。
完整Advance、Prepare、对象分类、连接及全游戏等价仍未完成。下一批继续内部模板/具体对象分支与含服务调用的共享出口，扩展桥上混类/动态交通组合，并只按合法自然来源增加非主副本覆盖声明。
本地提交，不推送，不修改远端。
'''
report.write_text(body,encoding='utf-8',newline='\n')
handoff.write_text(body+'\n接手先运行verify_final_movement_v29.py，再建立下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt'
shutil.copy2(guide,S/'reading-guide-before.txt')
existing(guide,f'第二十八批当前状态（2026-10-23，优先于历史）\n内部模板表/建筑标志接续/4类11处写回出口；各部分6场景3406帧。最终48场景28518帧、99组片段门禁，本批196608例。桥上下层三对象实际链遍历通过，四个高差占用组合回归，两例原版异常保留；非主C自然入口及全游戏等价未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt'
existing(main,main.read_text(encoding='utf-8')+f'\n2026-10-23 第二十八批正式接续：{handoff}\n48场景28518帧，99组片段门禁；桥上下层三对象链实景通过，非主C入口仍未证明。\n')
continuation=P/'交接文档-新对话继续推进-20261022.txt'
existing(continuation,f'最新接续：第二十八批已验收，正式代次28 / 验证轮次29。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R / "verify_final_movement_v29.py"}\n以下旧批次说明作为历史保留。\n\n'+continuation.read_text(encoding='utf-8'))
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动第二十八批：内部模板表、建筑标志接续与写回出口；48场景28518帧、99组片段门禁，桥上下层三对象链实景通过。入口为[第二十八批交接](交接文档-单位移动第二十八批正式验收-20261023.txt)及 `reports/latest-recovery.json`。原版异常、基线与回退保留，非主入口及全游戏等价未完成。\n'
existing(readme,''.join(lines))
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')}
flags.update(template_table_internal_shared_readable=True,building_flags_internal_shared_readable=True,prepare_written_epilogues_shared_readable=True,full_original_equivalence_verified=False)
accept.update(paired_scenes=48,paired_frames=28518,independent_default_budget_frames=901,independent_internal_observer_frames=4054,
              independent_connection_observer_frames=9116,combined_curved_height_occupied_scenes=4,**flags)
write(S/'strict-acceptance.json',accept)
conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(default_rules_full_exhaustion_verified=True,natural_exhaustion_verified=True,natural_budget_scope=budget['scope'],new_real_scene_evidence=str(S/'budget-real-scenes.json'),
                  natural_budget_entries=budget['scenes']['v-default-budget']['modes']['original']['budget_events'],
                  unresolved=['Exact 4C3895 callback is not independently hooked.','Untouched random-match frequency is unmeasured.','Nonprimary generated aliases are not naturally observed.'])
write(S/'budget-conditions.json',conditions)
paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(Path(p).relative_to(R).as_posix() for p in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ['.c','.h','.txt'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v29*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ['.c','.h','.asm'] or p.name in ['truck-actor-fixture-probe.exe','connection-fixture-probe.exe','connection-fixture.map','truck-actor-fixture-build-arguments.json','connection-fixture-build-arguments.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
    source=R/rel;dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    manifest.append(dict(path=rel,sha256=sha(source)))
    prior=S/'baseline'/rel
    if prior.exists() and prior.read_bytes()==source.read_bytes():continue
    if source.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or source.name=='CMakeLists.txt':
        try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],source.read_text(encoding='utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
        except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest)
for document in [report,handoff]:
    with document.open('a',encoding='utf-8') as stream:stream.write(f'\n最终源封存：{len(manifest)}项。当前身份以validation.json/source-manifest.json为准。\n本批production控制脚本只跑矩阵/辅助，observer控制脚本只跑场景；空操作构建、结构预检及观察器配方/构建已分别先行完成。下一轮须明确保留这些门禁，勿只改脚本后缀。\n')
(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=28,verification_round=29,exe_sha256=digest,state_schema=12,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    final_build_inputs_match_returns_checkpoint=True,paired_scenes=48,paired_frames=28518,probes=99,new_fragment_cases=196608,
    independent_default_budget_scenes=1,independent_default_budget_frames=901,independent_internal_observer_scenes=4,independent_internal_observer_frames=4054,
    independent_connection_observer_scenes=16,independent_connection_observer_frames=9116,source_files=len(manifest),production_c_sources=171,content_inputs=288,
    source_content_verified=True,strict_ordered_audit_passed=True,frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
    preservation=preservation,unsupported_guards=37,combined_curved_height_occupied_scenes=4,combined_curved_height_occupied_runtime_verified=True,
    original_equivalent_stall_scenes=2,completed_connection_scenes=14,all_curved_height_routes_complete=False,
    all_rare_branches_verified=False,nonprimary_overlapping_adapter_naturally_observed=False,alternate_saved_segment_pointer_real_scene_verified=False,
    rare_branch_evidence_scope=tubes['scope']+' '+internal['scope']+' '+combined['scope'],
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    legal_overlap_sources=str(S/'legal-overlap-sources.json'),report=str(report),handoff=str(handoff),**flags)
validation.update(original_preframe_startup_failures_preserved=len(startup['attempts']),serial_startup_retries_passed=True,bridge_multiobject_scenes=4,bridge_multiobject_frames=3604,independent_bridge_observer_frames=3604,bridge_upper_and_lower_three_object_traversal_verified=True,bridge_runtime_evidence=str(S/'bridge-real-scenes.json'))
validation.update(system_interruption_recovered=True,interrupted_pairs_preserved=2,resumption_evidence=str(S/'resumption-validation.json'))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update({k:v for k,v in validation.items() if k not in ['preservation','part_checkpoints','source_files','exe_sha256']})
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
    previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
    previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),
    next_readable_region='Remaining template/object branches and service-bearing exits; bridge traffic, mixed object types and runtime computed alias sources remain bounded')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=48,paired_frames=28518,
    independent_default_budget_frames=901,independent_connection_observer_frames=9116,independent_internal_observer_frames=4054,passed=True,strict_ordered_audit_passed=True,first_difference=None,
    full_original_equivalence_verified=False,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=28,verification_round=29,executable=str(exe),exe_sha256=digest,
    validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256'],item['path']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
    exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True,formal_baseline=28,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
