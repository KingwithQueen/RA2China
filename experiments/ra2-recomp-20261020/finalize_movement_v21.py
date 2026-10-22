"""Promote generation 20 only after round 21 strict gates, then archive exact bytes."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v21'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write_existing(path,value,**options):
 old=path.read_bytes();nl='\r\n' if b'\r\n' in old else '\n'
 path.write_bytes(value.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
def rows(tag,mode='original'):
 return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==147 and len(receipt['inputs'])==236 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-slope-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
assert all(r['passed'] and r['save_before']==r['save_after'] for r in default['runs'])
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-slope-default'))==select(rows('c-slope-default','generated-c'))
for mode in ['original','generated-c']:
 f28=next(r for r in rows('c-slope-default',mode) if r['kind']=='state' and r['frame']==28)
 assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
 assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
parts={name:read(S/'parts'/name/'validation.json') for name in ['landing-verified','failure-verified','slope-verified']}
assert all(x['passed'] for x in parts.values()) and parts['slope-verified']['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
probes={n:read(S/(n+'-verified-01.json')) for n in ['advance-landing-probe','prepare-failure-tails-probe','slope-height-probe']}
assert all(p['passed'] and p['original_stack_cleanup_verified'] for p in probes.values())
assert [p['cases'] for p in probes.values()]==[32768,32768,131072]
native_identity=read(S/'native-remainder-identity.json')
assert native_identity['passed'] and native_identity['total_cases']==196608
for entry in native_identity['inputs']+[native_identity['probe_executable']]:assert sha(R/entry['path'])==entry['sha256'],entry['path']
new_cases=sum(p['cases'] for p in probes.values())
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in range(9,21)]
archives+=[('v21-baseline',S/'baseline','source-manifest.json','')]
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
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards,existing_labels_preserved=True)
write(S/'preservation.json',preservation)

conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_budget_scope=budget['scope'],
 new_real_scene_evidence=str(S/'budget-real-scenes.json'),natural_budget_entries=budget['scenes']['h-default-budget']['modes']['original']['budget_events'],
 new_static_followup=budget['callback_scope'],necessary_conditions=budget['necessary_conditions'])
conditions['ordinary_drive_failure_analysis'].update(main_search_failure='AI callbacks can restore a goal after Stop before failed Prepare returns.',
 conclusion='Default-rule constructed AI TRUCKA scene naturally exhausts its normal budget with a restored destination in the same Drive.')
conditions['unresolved']=['Exact 4C3895 callback site is not separately hooked.','Untouched random-match frequency is not measured.',
 'Remaining Advance sampling aliases, Prepare internal fragments and terrain/object classifiers retain generated C. Full-game equivalence is unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
eb.update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,
 natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'))
effect.update(connection_landing=dict(readable=True,entries=[3,4,13],native_probe=probes['advance-landing-probe']),
 remaining_failure_tails=dict(readable=True,entries=[2,7,2,8,3,2,8],native_probe=probes['prepare-failure-tails-probe']),
 slope_height=dict(readable=True,shapes=20,initialization_flags=3,native_probe=probes['slope-height-probe']))
write(S/'effects.json',effect)
flags={k:v for k,v in read(R/'evidence/movement-state-v20/validation.json').items() if k.endswith('_readable')}
flags.update(advance_connection_landing_readable=True,advance_collision_exits_readable=True,prepare_failure_tails_readable=True,
 slope_height_core_readable=True,whole_prepare_function_readable=False,whole_advance_function_readable=False,
 whole_prepare_shared_exits_readable=False,whole_object_passage_classifier_readable=False,
 whole_path_search_readable=False,whole_ground_movement_readable=False,full_original_equivalence_verified=False)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='c-slope-default',production_default_skirmish_frames=901,
 natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,**flags)
write(S/'strict-acceptance.json',accept)
report=P/'docs/单位移动第二十批-特殊连接落位与失败收尾及坡面高度-20261022.txt'
handoff=P/'交接文档-单位移动第二十批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_identities='\n'.join(name+' : '+x['exe_sha256'] for name,x in parts.items())
report.write_text(f'''单位移动第二十批正式验收（2026-10-22）
正式代次20 / 验证轮次21
程序：{exe}
SHA-256：{digest}
证据：{S}

一、本批整理
Advance：方向8的特殊连接落位4A1388共3个展开入口；拒绝方向4A22F9共4处；通用false出口4A263A共13处。
ground_landing.h/.c把离格、清路段、连接索引检查、连接格中心、移除已用路径方向、前方落点、两次地面高度和连接时长插值分开命名。
已有模板时继续原采样分支，不额外查询；无连接时保留原条件下的driving值。落位及高度回调后重读单位，第二次高度查询前重新读取连接终点和时长。
连接高度保持32位差值回绕、有符号除法和加法回绕；合法连接时长必须满足原x86除法约束。拒绝方向写入原寄存器给出的值，false返回只清AL。
Prepare：ground_failure.h/.c整理已揭露障碍重试、失败分类7、直接/已保存指针的路段清理、直接停止，以及必须写入的清理尾部。
7种入口共32处接入：395A=2、3BFD=7、3985=2、3C34=8、3A38=3、39AF=2、3C5D=8。保留失败7的立即重试、其他分类的待播标志清理和selector=-1；已有目标时先取消，再读取当前单位调用目标停止。
已保存路段指针可以与drive.segment_end不同，不能一律改用当前路段。无效坐标已存在时保留driving；直接尾部则仍须清零。递归仍传原aborted指针和两个0，普通停止只清AL，递归/目标停止保留完整返回值。
坡面：ground_slope.h/.c完整整理4706C0的三个初始化缓存位、20种坡面表、基础层高、局部坐标和坡面高度。
850C40是启动流程写入的坡高，不能把原始PE中的0当正常运行值。三个缓存位分别管理高度double、每世界单位比例和坡面表；已有缓存必须保留。第一种坡面的方向/偏移来自静态表，初始化只改上限及额外高度。
基础高度先做32位乘法回绕、加0.5，再按原转换截断并切换控制字。随后按y项、x项、偏移、额外高度的顺序计算，在扩展精度内先限制下限再限制坡顶，最后加基础高度并截断；不能先转double比较或合并表达式。
业务C没有固定游戏地址。旧布局和调用适配集中在runtime/ground_remainder_bridge.h/.c。原生成文件保留其余入口和尾部目标，未宣称完整Advance/Prepare/通行分类已整理。

二、验收
三部分各自通过默认遭遇战901帧、三格包围101帧和默认规则预算901帧，保留独立完整回退点。
最终28个生产场景15798模拟帧严格一致；另默认规则构造AI预算耗尽901帧严格一致。命令、随机数、完整有序内部事件均相同；schema12、记录器和比较器保持原样，缺帧负控通过。
69组片段/数值/ABI回归通过。本批新增196608例机器码对照：落位32768、失败收尾32768、坡面131072；坡面覆盖20种坡型、8种部分缓存状态、12种浮点模式、负层高/边界坐标/回绕和预置坡面参数。探针与实景证据分开记录。特殊连接的有效落位及不同保存指针等少见分支有机器码/ABI覆盖；本批未增加其独立实景命中探针，不把普通场景通过视为这些分支已自然触发。
生产C源147个、内容输入236项，空操作构建刷新0，程序身份稳定。默认步兵1032262第28帧X=17343，保留三格第52帧、转弯第197帧、二次补建失败第399帧及持续失败451..1111帧门槛。
默认预算采用正常对象服务构造真实AI TRUCKA及16辆敌车；规则未改，未直接写预算/路径/目标内部状态。27..37帧预算10..0，第38帧清空目标并停止至240。未测随机对局频率，4C3895回调位置未单独挂钩。

三、回退和下一步
旧正式基线：{S/'baseline'}
{part_identities}
最终归档final-source、source-manifest.json、final-check.json。历代基线和本批三个回退点、原始游戏/SAV、H盘20项输入及旧手写C引擎哈希均保持一致。37个未实现保护保留。
下一步优先核对Advance的15F0、230E等独立采样共享入口和Prepare仍有生成C的内部片段/清理尾部，再推进其余地形及对象通行服务。完整移动、寻路和全游戏等价仍未完成。
完成后仅本地提交，不推送；父提交f0112de。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''单位移动第二十批正式验收交接（2026-10-22）
正式代次20 / 验证轮次21：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
Advance特殊连接落位4A1388的3个入口、拒绝方向4A22F9的4个入口、false出口4A263A的13个入口已整理。
Prepare其余失败收尾7种入口共32处接入，保留已保存路段指针、条件清理/强制清理、立即递归及完整返回值。
4706C0坡面初始化与高度计算完整主入口已整理：三个缓存位、20种坡面及原x87精度/舍入/截断顺序。
28场景15798帧，另默认规则预算901帧严格一致；69组回归通过，本批新增196608例机器码对照。
三部分分别完成默认901帧、三格101帧、预算901帧验收，保留完整源码/程序回退点。
修改入口：gameplay/ground_landing.h/.c、ground_failure.h/.c、ground_slope.h/.c；布局适配runtime/ground_remainder_bridge.h/.c。
默认预算仍在27..37帧10..0，第38帧清空并停止至240；这是正常服务构造的真实AI对象场景，未测随机频率，4C3895未单独挂钩。
报告：{report}
旧基线：{S/'baseline'}；回退parts/landing-verified、failure-verified、slope-verified；最终final-source、清单及final-check.json。
少见有效连接落位及不同保存指针分支有片段/ABI覆盖，本批未新增独立实景命中记录。
下一步Advance的15F0/230E等共享入口和Prepare其余内部片段/清理尾部，补少见连接合法地图场景，再推进其余地形/对象通行服务。完整游戏等价未完成，37个保护仍在。
本地提交，不推送；父提交f0112de。既有基线、回退、H盘输入和旧C引擎保留。
''',encoding='utf-8',newline='\n')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
write_existing(guide,f'''第二十批当前状态（2026-10-22，优先于下文历史描述）

特殊连接落位：ground_landing.h/.c。方向8且无模板时，离格→清路段→找连接→更新路段/路径→前方落点→两次高度查询→按连接时长插值。回调后重读单位，连接终点/时长在第二次高度查询前读取。
失败收尾：ground_failure.h/.c。揭露障碍与失败7有不同的递归前处理；其他分类清待播标志。直接/已保存路段指针必须区分；无效路段的条件清理与强制尾部也不同。
坡面高度：ground_slope.h/.c。缓存初始化分三位，20种坡面命名梯度/偏移/上限/额外高度。保留静态表的首坡面参数、32位乘法回绕、加0.5后截断和控制字切换。坡顶比较在扩展精度内完成。
旧布局及ABI集中在ground_remainder_bridge.c。修改参数另建候选，并重新逐帧比较。
28场景15798帧+默认预算901帧、69组检查，本批新增196608例。Advance/Prepare的其余生成入口和对象/地形服务尚未全部整理，完整游戏等价未完成。
报告：{report}

'''+guide.read_text(encoding='utf-8'))
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
write_existing(main,main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第二十批正式接续：{handoff}\n特殊连接落位、失败收尾和坡面初始化/高度主入口已整理；28场景15798帧+默认预算901帧、69组检查通过。\n下一步其余采样共享入口、Prepare内部片段及地形/对象服务。完整游戏等价未完成。本地提交，不推送。\n')
readme=P/'README.md';lines=readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0]='> 当前研究路线（2026-10-22）：原版1.006 C17/x86重编译与可读单位移动完成第二十批正式验收。特殊连接落位、失败收尾及坡面初始化/高度主入口已整理；28场景15798帧，另默认预算901帧一致。入口为[第二十批交接](交接文档-单位移动第二十批正式验收-20261022.txt)及 `reports/latest-recovery.json`。继续其余采样共享入口、Prepare内部片段和地形/对象服务；完整游戏等价尚未完成，旧基线和手写C引擎保留。\n'
write_existing(readme,''.join(lines))


paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v21*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c','.h','.asm') or p.name in ['truck-actor-fixture-build-arguments.json','truck-actor-fixture-probe.exe','truck-actor-fixture-receipt.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
 src=R/rel;data=src.read_bytes();dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 manifest.append(dict(path=rel,sha256=sha(src)));prior=S/'baseline'/rel
 if prior.exists() and prior.read_bytes()==data:continue
 if src.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or src.name=='CMakeLists.txt':
  try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],data.decode('utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
  except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest);(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=20,verification_round=21,exe_sha256=digest,state_schema=12,
 paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
 probes=69,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
 frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
 source_files=len(manifest),production_c_sources=147,content_inputs=236,preservation=preservation,unsupported_guards=37,
 retained_passage_services=['remaining terrain/object services','remaining Advance/Prepare internal fragment entries'],report=str(report),handoff=str(handoff),**flags)
validation.update(new_rare_branch_runtime_hits_independently_recorded=False,rare_branch_evidence_scope='Valid special connection landing and alternate saved segment pointer: native original fragments and ABI probes; production scenes are regression gates, with no new independent hit recorder.',slope_regression_scenes=['f-slope-healthy','f-slope-damaged'])
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=20,verification_round=21,
 report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),**flags)
recovery.update(next_readable_region='Advance 4A15F0/4A230E shared sampling entries and remaining Prepare internal/cleanup fragments; add legal-map valid-connection runtime coverage, then remaining terrain/object classifiers; continue strict runtime and default-budget comparison',
 previous_recovery_validation=str(R/'evidence/movement-state-v20/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
 previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
recovery.update(new_rare_branch_runtime_hits_independently_recorded=False,rare_branch_evidence_scope=validation['rare_branch_evidence_scope'])
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
 independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
 normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=20,verification_round=21,
 executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
 exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
 main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=20,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
