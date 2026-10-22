"""Promote generation 27 only after all round-28 production and native gates pass."""
from pathlib import Path
import difflib, hashlib, json, re, shutil, subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v28';O=R/'evidence/movement-state-v27'
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
assert accept['paired_scenes']==27 and accept['paired_frames']==14897 and len(accept['probes'])==96
assert tubes['production_scenes']==12 and tubes['production_frames']==6712
assert tubes['completed_scenes']==10 and tubes['original_equivalent_stall_scenes']==2 and not tubes['all_curved_height_routes_complete']
assert combined['production_scenes']==4 and combined['production_frames']==2404
assert internal['independent_frames']==4054 and all(internal['stages'][str(i)]>0 for i in range(10,22))
assert not internal['nonprimary_overlapping_adapter_naturally_observed']
assert budget['default_rules_full_exhaustion_verified']
for report_name in ['legal-overlap-sources.json','overlap-caller-identity.json','recipe-byte-audit.json']:
    identity=read(S/report_name)
    assert identity['passed']
    for item in identity['inputs']:assert sha(R/item['path'])==item['sha256'],item['path']
for entry in read(S/'legal-overlap-sources.json')['entries']:
    if entry['entry_kind']!='alias':continue
    address=int(entry['entry'],16)
    lo,hi=(0x4A1000,0x4A2670) if address<0x4A2670 else (0x4A2670,0x4A4740) if address<0x700000 else (0x703040,0x703BD0)
    assert all(lo<=int(edge['address'],16)<hi and edge['instruction']!='call' for edge in entry['decoded_incoming'])
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']==tubes['production_executable_sha256']==internal['production_executable_sha256']==combined['production_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==171 and len(receipt['inputs'])==286 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
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
for name,cases in [('internal',131072),('connection-numeric',1601904),('tube-state',131072),('progress',491520),('travel',360448),('joint',262144),('overlap',262144),('round28',196608)]:
    identity=read(S/('native-'+name+'-identity.json'))
    assert identity['passed'] and identity['total_cases']==cases,name
    for item in identity['inputs']+identity.get('probe_executables',[])+([identity['probe_executable']] if 'probe_executable' in identity else []):
        assert sha(R/item['path'])==item['sha256'],item['path']
    identities[name]=identity
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,28)]
archives += [('v28-baseline',S/'baseline','source-manifest.json','')]
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
write(S/'preservation.json',preservation)
exits=read(S/'pending/shared-exit-integration.json')
assert exits['unique_entries']==27 and exits['overlapping_copies']==140
for source,dest in [('template-integration.json','template-integration.json'),('object-kind-integration.json','passage-integration.json'),('shared-exit-integration.json','returns-integration.json')]:
    write(S/dest,read(S/'pending'/source))
report=P/'docs/单位移动第二十七批-桥层模板与类别过滤及共享出口-20261023.txt'
handoff=P/'交接文档-单位移动第二十七批正式验收-20261023.txt'
assert not report.exists() and not handoff.exists()
part_text='\n'.join(name+' : '+value['exe_sha256'] for name,value in parts.items())
wait_text='\n'.join(name+' : 等待'+str(len(v['modes']['original']['wait_frames']))+'帧，出口帧'+str(v['modes']['original']['exit_frame']) for name,v in combined['scenes'].items())
parent=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
body=f'''单位移动第二十七批正式验收（2026-10-23）
正式代次27 / 验证轮次28
程序：{exe}
SHA-256：{digest}
证据：{S}

1. 可读 C17/x86 整理
ground_template_transition 增加跨格桥层切换；Advance 主业务与4A18AB六处重叠片段复用同一助手。保持层高、重复标志查询和桥层写入顺序，固定布局及寄存器恢复留在ground_overlap_bridge。
ground_object_kind 将类别过滤从完整对象前置中分出，主分类器与7034BF两处内部接续复用。保留重复类别回调、建筑占格、配对标记及下一对象接续。
Prepare 26个纯返回入口及703940通行硬阻挡出口，共27类、140个生成副本复用ground_return_frame。保留旧标签/尾部目标、EAX高位、AL置0/1/不变、栈清理、非易失寄存器和相关标志位。生成0010保留LF、0046保留CRLF。
正式程序仍171个C源；新增一个业务头文件，共286项编译输入。最终空操作构建刷新0。正式schema12记录器和两份公共比较器未改。

2. 分段验收和回退
每部分6场景3406帧：默认遭遇战901、三格包围101、默认规则真实AI预算901、双向隧道各501、出口占用501。
{part_text}
每份保存当时全部编译输入、EXE和来源清单。最终286项输入及EXE与returns回退一致。

3. 最终逐帧验收
44个生产场景24914模拟帧，完整状态、命令、随机数及有序查询一致；另默认预算901帧、内部独立观察4054帧、连接独立观察9116帧。连续帧、坐标差异/缺帧负控、辅助菜单和非法命令门禁通过。
96组原版片段检查通过；本批新增196608例，桥层模板、带可变回调的类别过滤和27类出口各65536例。既有93组重新运行。
默认步兵第28帧X=17343、包围第52帧、转弯第197帧、失败第399帧及451..1111每60帧持续失败保持。默认预算仍是正常服务构造AI TRUCKA与16辆敌车，27..37帧10..0，第38帧停止；未经干预随机频率和4C3895独立回调仍未测。

4. 合法重叠来源与独立观察
legal-overlap-sources.json 对原版反汇编目录、38条入边及PE原始指令字节逐项核对。九个非主入口均为递归反汇编别名，已知合法来源是函数内部跳转；扫描未发现指向别名的直接CALL或非代码区地址常量。未排除任意计算目标或运行中生成的指针，生成别名注册不能当作原生调用来源。
真实返回地址、链接MAP和E8调用字节继续核对，对象链适配自然从00703040主入口执行。非主生成入口自然执行仍未证明，不注入运动状态或人为跳转冒充实景。
独立观察由10处增加至12处，新增4A18AB桥层模板与7034BF类别过滤，原版分别自然命中{internal['stages']['20']}次、{internal['stages']['21']}次；原版/C完整有序记录及正式/观察状态一致。观察程序替换12个测试对象，不进入正式程序。桥层链头请求另记录层标记与对象ID；当前四场景上层请求{internal['bridge_layer_chain_entries']}次、非空上层链头{internal['bridge_layer_nonempty_chain_entries']}次，此统计不替代专门桥上多对象场景。

5. 弯曲高差与占用组合
新增4→7上行、6→4下行及各自镜像曲率四个组合，每场景601帧。合法Tubes/地图层高，通过正常构造、放置服务在第217帧放16辆敌车；出口格实际被占用。要求弯曲轨迹、多个路点、非零高差、连续等待、随后退出并到达目标清空目的地；没有显式重建路径或原始运动/预算/路径写入。
{wait_text}
四个生产场景2404帧及四个独立观察2404帧均通过。原有12个连接场景6712帧持续回归；4→6上行和7→4下行两例仍忠实复现原版异常，只算一致性、不算成功穿越。高差取整根因及全部安全范围没有新增穷尽结论。

6. 保存、限制与接续
v9..v27旧正式档、本轮3116项baseline和三份parts逐项复核；H盘20项原始输入、原游戏/SAV和旧手写引擎保持。失败编译/集成预检日志保留在investigations，没有覆盖旧正式证据。
本批仍未完成完整Advance、Prepare、对象分类、隧道或全游戏等价；37个未实现保护保留。继续其余内部模板/具体对象分支及带副作用出口，扩展专门桥上多对象场景；非主入口只有找到合法运行来源才增加覆盖声明。
父提交：{parent}。本地提交，不推送，不改远端配置。
'''
report.write_text(body,encoding='utf-8',newline='\n')
handoff.write_text(body+'\n接手时先运行 verify_final_movement_v28.py，再创建下一轮完整回退；不要重跑本轮封存写入脚本。\n',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt'
shutil.copy2(guide,S/'reading-guide-before.txt')
existing(guide,f'第二十七批当前状态（2026-10-23，优先于历史段落）\n桥层模板/对象类别内部接续/27类140个共享出口；每部分6场景3406帧。最终44场景24914帧，另预算901、内部观察4054、连接观察9116帧；96组片段检查，本批196608例。四个弯曲高差+出口占用组合通过；两例原版高差异常保留。非主生成入口和全游戏等价未完成。\n报告：{report}\n\n'+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt'
existing(main,main.read_text(encoding='utf-8')+f'\n2026-10-23 第二十七批正式接续：{handoff}\n44场景24914帧，96组片段检查；四个弯曲高差/占用组合通过，非主入口与全游戏等价未完成。基线/回退保留，本地提交不推送。\n')
continuation=P/'交接文档-新对话继续推进-20261022.txt'
existing(continuation,f'最新接续：第二十七批已验收，正式代次27 / 验证轮次28。\n先读：{handoff}\n程序SHA-256：{digest}\n只读核对：{R / "verify_final_movement_v28.py"}\n以下第二十六批说明作为历史基线保留；当前身份以最新指针和第二十七批交接为准。\n\n'+continuation.read_text(encoding='utf-8'))
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-23）：原版1.006 C17/x86单位移动完成第二十七批正式验收：桥层模板、类别接续及共享出口；44场景24914帧，96组片段检查，四个弯曲高差与出口占用组合通过。入口为[第二十七批交接](交接文档-单位移动第二十七批正式验收-20261023.txt)及 `reports/latest-recovery.json`。原版异常、基线与回退保留，非主入口及全游戏等价未完成。\n'
existing(readme,''.join(lines))
flags={k:v for k,v in read(O/'validation.json').items() if k.endswith('_readable')}
flags.update(template_bridge_layer_shared_readable=True,object_kind_continuation_shared_readable=True,prepare_pure_epilogues_shared_readable=True,full_original_equivalence_verified=False)
accept.update(paired_scenes=44,paired_frames=24914,independent_default_budget_frames=901,independent_internal_observer_frames=4054,
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
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v28*') if p.is_file())
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
(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=27,verification_round=28,exe_sha256=digest,state_schema=12,
    part_checkpoints={n:dict(validation=str(S/'parts'/n/'validation.json'),exe_sha256=v['exe_sha256'],scenes=6,frames=3406) for n,v in parts.items()},
    final_build_inputs_match_returns_checkpoint=True,paired_scenes=44,paired_frames=24914,probes=96,new_fragment_cases=196608,
    independent_default_budget_scenes=1,independent_default_budget_frames=901,independent_internal_observer_scenes=4,independent_internal_observer_frames=4054,
    independent_connection_observer_scenes=16,independent_connection_observer_frames=9116,source_files=len(manifest),production_c_sources=171,content_inputs=286,
    source_content_verified=True,strict_ordered_audit_passed=True,frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
    preservation=preservation,unsupported_guards=37,combined_curved_height_occupied_scenes=4,combined_curved_height_occupied_runtime_verified=True,
    original_equivalent_stall_scenes=2,completed_connection_scenes=14,all_curved_height_routes_complete=False,
    all_rare_branches_verified=False,nonprimary_overlapping_adapter_naturally_observed=False,alternate_saved_segment_pointer_real_scene_verified=False,
    rare_branch_evidence_scope=tubes['scope']+' '+internal['scope']+' '+combined['scope'],
    internal_runtime_evidence=str(S/'internal-real-scenes.json'),connection_runtime_evidence=str(S/'connection-real-scenes.json'),combined_runtime_evidence=str(S/'combined-real-scenes.json'),
    legal_overlap_sources=str(S/'legal-overlap-sources.json'),report=str(report),handoff=str(handoff),**flags)
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update({k:v for k,v in validation.items() if k not in ['preservation','part_checkpoints','source_files','exe_sha256']})
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
    previous_recovery_validation=str(O/'validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
    previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),
    next_readable_region='Remaining side-effecting template/object branches and exits; dedicated bridge-layer object chains; computed legal alias sources remain unproved')
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=44,paired_frames=24914,
    independent_default_budget_frames=901,independent_connection_observer_frames=9116,independent_internal_observer_frames=4054,passed=True,strict_ordered_audit_passed=True,first_difference=None,
    full_original_equivalence_verified=False,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=27,verification_round=28,executable=str(exe),exe_sha256=digest,
    validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for item in manifest:assert sha(R/item['path'])==sha(S/'final-source'/item['path'])==item['sha256'],item['path']
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
    exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True,formal_baseline=27,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
