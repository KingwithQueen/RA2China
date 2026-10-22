"""第十批候选通过原定严格范围后升级；扩展实景及全游戏边界单列。"""
from pathlib import Path
import difflib,hashlib,json,re,shutil
from budget_conditions_v11 import reconcile
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v11'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def records(tag,mode='original'):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json');preservation=read(S/'preservation-before-promotion.json')
assert accept['passed'] and accept['strict_ordered_audit_passed'] and preservation['passed']
assert budget['natural_exhaustion_verified'] and not budget['default_rules_full_exhaustion_verified']
skirmish=read(S/'skirmish-investigation.json');assert skirmish['preexisting_infantry_difference_confirmed']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe);assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['executable_sha256']==digest and receipt['refreshed_count']==0
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
    assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (R/'ra2/src/recomp/gen_game').glob('*.c'))
assert guards==37
old_manifest=read(S/'baseline/source-manifest.json')
for e in old_manifest:assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
for e in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256']
assert sha(R/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
assert sha(R/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
assert sha(P/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
reconcile(S)

# 精确记录查询差异被移除，而非放宽命令比较器。
query=lambda seq:[r for r in seq if r['kind']=='movement-audit' and r['stage']==27 and r['frame']==52 and r['cell']==[69,113]]
before=[len(query(records('a-ur3',m))) for m in ['original','generated-c']]
after=[len(query(records('e-ur3',m))) for m in ['original','generated-c']]
assert before==[20,22] and after==[20,20]
write(S/'path-cost-investigation.json',dict(passed=True,original_cached_cost=2.010999917984009,old_c_cached_cost=2.011000156402588,
    query_causing_divergence='float accumulation store at 427E10',original_control='E7F (53-bit precision, toward zero)',
    old_queries=before,new_queries=after,frame=52,cell=[69,113],new_ordered_commands=1064,
    implementation='gameplay/ground_path_cost.c: ra2_ground_accumulate_path_cost',
    diagnostics=['a-ur3','b-path','c-gstore'],final_scene='e-ur3',comparator_unchanged=True,
    old_v10_build_identity_warning='Restoring old source timestamps could reuse diagnostic objects; this round rebuilt all 110 previous C sources and tracked content. Old v10 binary/source claims are historical, not reused as proof.'))

report=P/'docs/单位移动第十批-正式验收与预算回调-20261021.txt'
handoff=P/'交接文档-单位移动第十批正式验收-20261021.txt'
report_text=f'''第十批正式验收与失败预算回调调查（2026-10-21）

正式结果

第 52 帧两次额外查询已解决。第十批候选修正版已通过原定严格验收范围，可升级为正式基线。
默认程序：{exe}
SHA-256：{digest}
严格汇总：{S/'strict-acceptance.json'}
正式验收：{S/'validation.json'}
原有 27 场景、14897 帧的对象状态、RNG、外部命令及内部有序观测全部一致。
40 组映射原版片段/数值检查通过；累计代价新增 786432 组输入，覆盖三种精度和四种舍入方式。
固定 SAVE0029.SAV、seed 12345、2190..3000 窗口继续通过，包含此前第 2247 帧。
三格包围 e-ur3 的 351 帧严格通过；第 52 帧 69,113 格查询原为 20/22，现为 20/20；命令与有序观测总数同为 1064。
墙、门、转弯、二次补建失败、临时及隐形障碍、拥堵、零速度地形等原有实景门槛均重新检查。
新增友方入口 2290 次，移动友方几何 88 次，零速度地面尾部 9 次；入口次数不等于所有子分支自然命中。

可读 C 与差异根因

可读入口：{R/'ra2/src/gameplay/ground_path_cost.c'}
接口：ra2_ground_accumulate_path_cost(previous_cost, step_cost, control)。
原版 427E09..427E10 先按当前 x87 精度相加，再按当前舍入方式存 float。
旧生成代码默认就近舍入，把缓存代价从 2.010999917984009 抬至 2.011000156402588，改变缓存剪枝。
本轮先用只读寻路候选/评分记录找到分歧，再修正累计保存；不按特定帧、对象或格子打补丁。
正式函数以已有纯 C 数值层执行相加与保存，生成外壳只适配旧字段，FPU 栈净变化仍为零。
当前仅覆盖有限、非负路径代价；不是通用 IEEE 非有限数模拟器。
ground_allied.c 与 ground_terrain.c 的第十批可读整理一并通过本轮完整新编译的实景验收。
完整寻路评分、堆及缓存算法尚未整体改成命名 C；其余评分保存仍属于后续可读化范围。

构建一致性修正

上轮恢复源码保留旧时间戳，Ninja 可能复用诊断目标文件；旧候选 EXE 与归档源的一致性不能靠该日志证明。
本轮重新编译全部原有 110 个 C 源，先用该新程序重现 101 帧旧差异；正式可读修正后共 111 个 C 源。
build-faithful.ps1 按编译输入内容哈希刷新源文件，并记录产物哈希；已存在头文件变化和单独 EXE 回退也会触发必要构建。
正式只读诊断已撤出。恢复源码后的内容变化确实触发重编译；最终无变化构建刷新 0 源、程序哈希不变。
构建证据：build-fresh-01.log、build-readable-01.log、build-content-noop-01.log 及相应内容清单。
原有严格比较器未改，位移 +1 和缺帧反例继续被拒绝。

失败预算：已补齐合法规则实景的自然扣减及耗尽

新的线索是停止之后的回调，而非必须替换移动器。
4C371A 调用 Stop 后，4C3895 可以进入 Unit.SetDestination 7053F0，经 Foot.SetDestination 4C8030 在 4C8165 调用当前移动器 MoveTo。
实景中同一 Drive 的 Prepare 返回 false 时目标仍有效，并在随后帧改变为 AI 回退目标；这支持停止后重新赋予目标的控制流。
具体 4C3895 回调点本轮未单独挂钩记录，精确回调链由本机原版反汇编与上述状态共同支持。

独立实景工具：{S/'ai-fixture-probe.exe'}
此工具只将测试摆放器的阻挡阵营选择推广到 AI；游戏对象、移动算法和原版服务沿用已验收对象文件。
正式程序、其源码和对象文件没有因该工具而变化；编译路径及链接参数保存在 ai-fixture-build-arguments.json。
此前编译路径未替换的试验 k 失败记录保留；build-ai-fixture-02.log 确认实际编译 ai_movement_fixture.c。

m-sk-ai-ring：原版遭遇战菜单、seed 12345、AI 车辆 1032258 自动移动，第 27 帧用原版服务创建 16 辆真实阻挡车辆，半径 2。
不主动调用寻路；explicit_rebuild_result=FFFFFFFF；未写预算、路径队列或 Drive 目标。
使用合法独立 RULES：E1/E2.Speed=0，MTNK/HTNK.Primary=none，以隔离尚未整理的步兵运动和攻击。
CloseEnough 保持原版 2.25。第 58..60 帧自然进入预算入口，值为 10、9、8，扣后到 7；之后近距离分支停止。
901 帧的状态、RNG、命令及全部有序观测严格一致。

n-sk-zero-close：仅在上述规则副本中再将 CloseEnough 改为 0，隔离近距离提前停止。
第 58..67 帧从 10 连续扣到 0，第 68 帧以零预算进入停止；第 69 帧目标为空、预算 0，此状态保持到 200 帧。
201 帧严格一致；11 个预算入口按 10..0 完整有序出现。这里没有主动寻路，也没有预算、队列或目标注入。
因此合法规则实景的自然耗尽已经验证；原版默认规则下完整耗尽尚未验证，不能混为同一结论。
l-sk-ai-ring 的 651 帧也严格一致，但一格摆放器主动调用了重寻路，单独归类，不能当自然入口证明。
完整证据：{S/'budget-real-scenes.json'}。

尚未通过的扩展范围

默认遭遇战 f-skirmish 在第 28 帧的步兵 1032262 位置 x 原版为 17343、C 为 17344，之后 RNG 也出现分歧。
class/vtable=7A3540，即步兵；本轮未整理该移动器。该 901 帧扩展场景未通过，不能列入正式 27 场景验收。
本轮全新编译的修正前程序 g-sk-control 在同一帧同一字段重现；修正前后 C 的前 121 帧状态逐项相同。
该边界记录在 skirmish-investigation.json；它不是本次累计代价修正造成的回归，也不是全游戏等价证明。
整个游戏等价、全部移动代码可读化及所有 MOD 参数兼容仍未完成。

保全与回退

第九批 536 项、第十批 637 项归档、两个 540 项部分回退均逐项通过哈希检查，旧失败记录不改写。
本轮基线：{S/'baseline'}；其中 formal-v9.exe 是此前正式程序，ra2/build-original-c/ra2.exe 是原第十批候选。
新正式源与程序：{S/'final-source'}；source-manifest.json、source-changes.patch 与 final-check.json 给出身份和差异。
新可回退节点：{S/'parts/path-cost-strict-verified'}。
20 项 H: 原始输入、game.exe、SAVE0029.SAV、旧手写引擎及 37 处未支持保护保持原指纹。
没有提交、推送、重置、清理或删除旧基线。

下一步

1. 从本轮正式源和哈希继续，保留旧候选作为历史证据，不再把旧时间戳构建视为源/程序一致性证明。
2. 继续命名整理路径评分/缓存与尚余 Advance、Prepare 外壳；每部分仍做原版片段和逐帧严格验证。
3. 把新的 AI 预算回退条件加入长期实景回归，进一步缩小规则隔离项，验证默认 CloseEnough 下完整自然耗尽。
4. 步兵第 28 帧差异是扩展范围的明确后续入口；不要宣称全游戏等价。
'''
assert not report.exists() and not handoff.exists()
report.write_text(report_text,encoding='utf-8')
handoff.write_text(report_text,encoding='utf-8')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';t=guide.read_text(encoding='utf-8')
a=t.index('二十八、第十批验证边界：候选与正式基线分开');b=t.index('二十九、第十批预算调查',a)
t=t[:a]+f'''二十八、第十批正式验收（本轮修正，2026-10-21）

第 52 帧额外两次查询已由 ground_path_cost.c 的累计代价相加/保存修正。
原有 27 场景 14897 帧的状态、RNG、命令和内部有序观测全部一致；40 组原版片段回归通过。
默认程序与工作源码现为已升级正式基线，程序 SHA-256：{digest}。
第十批旧候选与未通过记录仍保留，不能把它们的旧二进制与源码一致性当成新验收证据。
全游戏等价尚未完成；默认遭遇战第 28 帧的步兵移动差异已用修正前程序重现，单独待办。
详细证据与回退：{handoff}。

'''+t[b:]
t=t.replace('二十九、第十批预算调查','二十九、第十批早期预算调查（由第三十节补充）',1)
t+='''
三十、累计路径代价与预算回调的新边界

ground_path_cost.h/.c：ra2_ground_accumulate_path_cost(previous_cost, step_cost, control)。
保存累计 float 代价时必须保留原版 x87 舍入；一位变化会影响缓存剪枝和查询次数。
生成外壳只读取父节点与边代价，FPU 栈净变化为 0。该函数适用于有限非负路径代价。
合法规则 AI 包围实景现已观测到同一 Drive 重建失败后目标仍有效、预算自然扣减。
CloseEnough=0 的独立规则实景中，第 58..68 帧预算入口按 10..0 出现，第 69 帧目标清空。
原版默认 CloseEnough=2.25 的对应实景只扣到 7 后近距离停止；默认规则完整耗尽仍未验证。
一格摆放主动重寻路与两格纯摆放必须分开记账；完整过程见本轮交接和 budget-real-scenes.json。
'''
guide.write_text(t,encoding='utf-8')

main=P/'交接文档-原版逆向与C重编译-20261020.txt';target=S/'baseline/project'/main.name;shutil.copy2(main,target)
main.write_text(main.read_text(encoding='utf-8')+f'\n\n2026-10-21 第十批正式验收接续入口：{handoff}\n第 52 帧两次查询已解决，27 场景严格通过；合法规则实景自然预算耗尽已验证，默认遭遇战步兵第 28 帧差异单列待办。\n',encoding='utf-8')

paths={e['path'] for e in old_manifest}
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v11*') if p.is_file())
paths.update(['ra2/src/gameplay/ground_path_cost.c','ra2/src/gameplay/ground_path_cost.h','ra2/build-original-c/source-content-receipt.json'])
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.name.endswith('_probe.c') or p.name in ['native_probe_host.h','audit_noop.c','ai_movement_fixture.c','ai-fixture-build-arguments.json','ai-fixture-probe.exe']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
    source=R/rel;data=source.read_bytes();dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    manifest.append(dict(path=rel,sha256=sha(source)))
    prior=S/'baseline'/rel
    if prior.exists() and prior.read_bytes()==data:continue
    if source.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or source.name=='CMakeLists.txt':
        try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],data.decode('utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
        except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest);(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
part=S/'parts/path-cost-strict-verified';part.mkdir(parents=True)
part_paths=['ra2/CMakeLists.txt','build-faithful.ps1','ra2/src/recomp/gen_game/recomp_0003.c','ra2/src/gameplay/ground_path_cost.c','ra2/src/gameplay/ground_path_cost.h','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json']
for rel in part_paths:
    dest=part/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest)
write(part/'manifest.json',[e for e in manifest if e['path'] in part_paths]);write(part/'validation-source.json',dict(validation=str(S/'strict-acceptance.json'),exe_sha256=digest))
validation=dict(passed=True,formal_baseline_generation=10,verification_round=11,exe_sha256=digest,state_schema=12,
    frame_comparison_passed=True,strict_ordered_audit_passed=True,refactor_checks_passed=True,
    paired_scenes=27,paired_frames=14897,probes=40,source_content_verified=True,diagnostics_removed=True,
    preservation=preservation,unsupported_guards=guards,source_files=len(manifest),
    legal_rules_natural_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=False,
    independent_budget_probe_scenes=3,independent_budget_probe_frames=1753,
    full_original_equivalence_verified=False,whole_ground_movement_readable=False,
    additional_unaccepted_investigations=[skirmish],report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),executable=str(exe),sha256=digest,state_schema=12,
    bounded_state_comparison_passed=True,strict_ordered_audit_passed=True,formal_baseline_generation=10,
    moving_allied_geometry_readable=True,terrain_tail_readable=True,cumulative_path_cost_readable=True,
    legal_rules_natural_budget_exhaustion_verified=True,normal_budget_exhaustion_verified=False,
    budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),report=str(report),handoff=str(handoff),
    previous_recovery_validation=str(P/'reports/latest-recovery.json'),previous_recovery_executable=str(S/'baseline/formal-v9.exe'),
    previous_recovery_sha256=sha(S/'baseline/formal-v9.exe'),
    next_difference=dict(scene='default skirmish, outside the 27 accepted scenes',**skirmish['same_first_difference']),
    next_readable_region='Path score/cache algorithm; Advance front/interpolation and Prepare shared entries; separate Infantry frame-28 difference')
recovery['previous_recovery_validation']=read(S/'baseline/project/reports/latest-recovery.json')['validation']
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=27,paired_frames=14897,
    passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
    normal_budget_exhaustion_verified=False,legal_rules_natural_budget_exhaustion_verified=True,
    additional_known_difference=skirmish['same_first_difference'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=10,verification_round=11,
    executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),historical_candidate=str(R/'evidence/movement-state-v10/candidate/ra2.exe'),
    full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,
    exe_sha256=digest,old_baselines_preserved=True,report_sha256=sha(report),handoff_sha256=sha(handoff),main_previous_sha256=sha(target),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=10,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
