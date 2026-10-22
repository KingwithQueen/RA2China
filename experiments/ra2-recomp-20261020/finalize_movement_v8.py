"""所有配对实景、分支效果、片段回归和保全核对通过后，才更新正式入口。"""
from pathlib import Path
import hashlib,json,re,shutil,difflib
ROOT=Path(__file__).resolve().parent; PROJECT=ROOT.parent.parent
S=ROOT/'evidence/movement-state-v8'; OLD=ROOT/'evidence/movement-state-v7'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    assert not (S/'validation.json').exists()
    exe=ROOT/'ra2/build-original-c/ra2.exe'; fingerprint=sha(exe)
    matrices=[read(S/'g-matrix.json'),read(S/'g-additional-matrix.json')]
    assert all(m['passed'] and m['exe_sha256']==fingerprint for m in matrices)
    cases=[r for m in matrices for r in m['results']]; assert len(cases)==23
    for row in cases:
        p=S/'runs'/row['tag']; report=read(p/'comparison.json'); c=report['comparison']
        assert report['passed'] and report['exe_sha256']==fingerprint,row['tag']
        assert c['equal_frames']==c['consecutive_equal_frames']==c['frames_compared']==row['frames']
        assert c['rng_equal_all_frames'] and c['first_difference'] is None and c['command_difference'] is None
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        for run in report['runs']:
            assert run['passed'] and run['exit_code']==0 and run['save_is_private_copy']
            assert run['save_before_sha256']==run['save_after_sha256']
        for mode in ('original','generated-c'):
            with (p/mode/'state.jsonl').open(encoding='utf-8') as f: assert json.loads(next(f))['schema']==10
    frames=sum(r['frames'] for r in cases); assert frames==11193
    probes={p.name:read(p) for p in S.glob('*-verified-01.json')}
    probes['advance-probe-final-02.json']=read(S/'advance-probe-final-02.json')
    probes['entry-probe-final.json']=read(S/'entry-probe-final.json')
    assert len(probes)==31 and all(r['passed'] for r in probes.values())
    assert probes['advance-probe-final-02.json']['advance_cases']==65536
    assert probes['entry-probe-final.json']['entry_cases']==65536
    effects,budget=read(S/'effects.json'),read(S/'budget-conditions.json')
    assert effects['passed'] and not budget['natural_exhaustion_verified']
    assert effects['turn_cloaked_obstacle']['passage']==1 and effects['path_advance']['total_entries']>0
    aux=read(S/'auxiliary-final-03/validation.json'); assert aux['passed'] and aux['exe_sha256']==fingerprint
    previous=read(OLD/'source-manifest.json'); assert len(previous)==361
    for e in previous:
        assert sha(OLD/'final-source'/e['path'])==e['sha256'],e['path']
        assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
    snapshots={}
    for name in ('path-advance-verified','entry-collision-verified','final-world-only-verified'):
        p=S/'parts'/name; manifest=read(p/'manifest.json')
        assert all(sha(p/e['path'])==e['sha256'] for e in manifest)
        snapshots[name]=dict(path=str(p),files=len(manifest),exe_sha256=sha(p/'ra2/build-original-c/ra2.exe'))
    inputs=[]
    for e in read(ROOT/'evidence/original-inputs-before.json'):
        actual=sha(Path(r'H:\开发\运行版本\原版1.006')/e['name']); assert actual==e['sha256']
        inputs.append(dict(**e,verified_sha256=actual))
    assert len(inputs)==20
    assert sha(ROOT/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
    assert sha(ROOT/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
    assert sha(PROJECT/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (ROOT/'ra2/src/recomp/gen_game').glob('*.c'))
    assert guards==37
    preservation=dict(passed=True,inputs=inputs,all_20_original_inputs_unchanged=True,
        previous_361_source_files_and_v7_executable_preserved=True,component_snapshots=snapshots,
        original_game_exe_and_save_unchanged=True,old_handwritten_engine_unchanged=True,unsupported_guards=guards)
    write(S/'preservation.json',preservation)
    guide=ROOT/'ra2/src/gameplay/阅读说明-单位移动.txt'
    text=guide.read_text(encoding='utf-8'); assert '十九、第八批' not in text
    text=text.replace('单位移动的可读 C：第七批，速度准备与转弯碰撞','单位移动的可读 C：第八批，路径跨格推进与碰撞前置')
    text+='''
十九、第八批：路径采样后的跨格推进

ground_advance.h/.c / ra2_ground_advance_sample：4A16A6..4A1B60。
从上一采样/当前位置确定前一格，对当前采样调用已有坐标变换，然后放置单位。
负坐标先向零取整再保留 16 位格坐标；当前采样 x/y 必须使用先前缓存值，只重新读取方向。
跨格：解除占用→放置→核对前后格层级→桥面层切换→列车碰撞→存活检查→恢复占用→覆盖物碾压。
同格：暂时清除占用更新标记后放置，再恢复标记。最后刷新放置、设置方向，在模板过渡采样重新标记位置。
列车按实际高度选格子对象链；伤害前先保存下一对象，因为伤害会移除当前链项。
对不可碾压对象沿用原版两次伤害：对象 10000、列车 20；不把看起来反直觉的原版分支擅自修正。
桥面/碾压的规则、世界服务和旧对象布局位于 runtime/ground_advance_bridge.c，玩法流程在 gameplay。
flag_5B8 等尚未确认含义的字段保留保守命名；不要据此套用其他版本的规则名称。
后续 Advance 的转弯接续碰撞 4A1B60..4A1F8D 仍待整理，并非整个 Advance 已完成。

二十、第八批：碰撞前置阶段

ground_entry.h/.c / ra2_ground_check_entry：703182..703331。
方向 8 用连接对象的端点判断；其他方向先检查本格和来路连接的方向差。
随后调用原版放置约束服务，保留其修改的参考层级和占用层标志。
桥面高四级时选择上层占用/步兵归属，再检查可见性限制，最后保留基础通行码，交给既有墙体和对象扫描。
连接对象名称尚未完全核实，使用 link/endpoint 而不假定是某一 MOD 设施。
真实桥面层与方向 8 的本批覆盖仍以原版片段为主，不能把片段输入写成全部实景命中。
CanEnterCell 的对象扫描、建筑特例及其它剩余分支仍待整理。

二十一、第八批验证和下一步

23 个最终配对实景共 11193 帧，schema 10；完整对象、RNG、命令及有序分支一致。
31 组片段/回归通过，新增 131072 组原版片段输入。第 2247 帧既有修正仍通过固定存档回归。
新增窄弯在第 197 帧自然命中转弯第二格隐形障碍并实际揭露；三格单位包围在第 52 帧命中转弯硬阻挡，转弯实景目前覆盖 0/1/2/7。
隐形窄弯使用独立地图的 Cloakable=yes / CloakingSpeed=1 合法规则覆盖；它不是原版卡车默认自带技能。
两/三格动态单位包围分别实际创建 16/24 辆障碍；不额外调用寻路，不写路径队列、预算或假碰撞码。
旧一格压力试验仍保留其显式重建步骤，不把它当作完全由普通逐帧更新自然耗尽预算的证明。
二次补建失败及预算自然耗尽的最终命中情况见本批 effects.json 与 budget-conditions.json；未命中继续列为待验。
本机原版动作分发先减 1 再与 0x74 作无符号比较，动作 128 超出范围，不能使用其它版本的 TeleportAll 作合法证明。
保留了早期新增观测字段读未初始化临时值的失败记录，改为读取有效队列字段后重新运行；游戏状态本身没有对应差异。
三格包围与旧发电厂占地冲突的试验、两格墙体被原版拒绝放置的试验均保留，不列入正式通过场景。
完整预算条件、分支次数、程序指纹、基线和回退清单见第八批报告/交接文档。
'''
    guide.write_text(text,encoding='utf-8',newline='\n')
    report=PROJECT/'docs/单位移动第八批-路径推进与碰撞前置-20261021.txt'
    handoff=PROJECT/'交接文档-单位移动第八批-20261021.txt'
    assert not report.exists() and not handoff.exists()
    second=len(budget['second_search_failure_events']); natural=len(budget['natural_budget_entries'])
    turn=effects['late_preparation']['turn_passage_counts']
    text=f'''原版 1.006 单位移动第八批：路径跨格推进与碰撞前置（2026-10-21）

本批成果
可读纯 C17：ground_advance.h/.c（4A16A6..4A1B60）和 ground_entry.h/.c（703182..703331），各有独立 runtime 适配层。
路径核心展开跨格放置、桥面层切换、列车对象链伤害、覆盖物碾压、存活检查与朝向更新。
碰撞前置展开连接方向、放置约束、桥面占用选择、可见性限制及基础通行结果；未知字段保守命名。
所有新增核心/适配文件以 /W4 /WX /std:c17 /utf-8 编译。没有更改玩法参数、原版规则或资源。
程序：{exe}
SHA-256：{fingerprint}
最终 23 个配对实景共 {frames:,} 帧，完整对象状态、RNG、命令及有序观测全部一致；31 组片段/回归通过，新增 131072 组输入。
这仍是有边界的等价验证；整个 Advance、CanEnterCell、全部移动状态和全游戏等价尚未完成。

实景及自然条件
保留并重跑原有 15 场景 8235 帧；覆盖固定存档移动/转向/停止、拥堵、地形、墙、闸门、坡地、隐形单位和真实超时空包装。
新增 8 场景 2958 帧：两/三格静态墙圈、大建筑目标、三组窄弯隐形障碍、两/三格动态单位包围。
窄弯第 197 帧转弯第二格通行码 1，真实隐形单位随后被揭露；转弯实景累计分类计数：{json.dumps(turn,ensure_ascii=False)}。
隐形窄弯地图给 TRUCKA 设置 Cloakable=yes / CloakingSpeed=1，原版和 C 读取相同独立地图规则；不是声称原版卡车默认能隐形。
路径推进 stage 20 真实记录 {effects['path_advance']['total_entries']} 次采样入口；schema 10 对转弯记录候选格、候选坐标及有效的第二方向队列值。
新增动态包围 16/24 个真实单位，由原版构造/放置服务创建；之后只让正常模拟帧处理，不主动重建路径、不写预算、不伪造返回值。
旧一格预算压力场景放置单位后会显式调用原版重建路径，仍保留，但与新增无额外寻路调用的场景区分。
最终自然二次补建失败 stage 18 记录 {second} 次；自然预算入口 stage 3 记录 {natural} 次。预算自然耗尽验证仍为 false。
普通失败清空当前 Drive 目标的带前提分析继续有效；没有扩大成全游戏不可达证明。
本机动作分发表 6ADB04..6ADB11 对 (action-1) 作上限 0x74 检查，128 号超出本机范围；这只排除该动作号，不排除其他合法超时空途径。
依据：{S/'action-bounds.json'}。

保留的失败/调查记录
d-standard/congestion/wall/slope 首轮游戏状态一致，但新增 next_direction 读到未初始化临时值，观测记录不一致；修正来源后 e-/g- 完整重跑通过。
e-ur3 与旧发电厂占地冲突；f-ur3 移远发电厂后成立，但仍沿用旧显式重建步骤，仅列调查。
e-wr2 的 65,116 格墙体被原版放置服务拒绝，两路都保护退出 7；未修改格子强行通过，未列正式验证。
长目录 ra2.csf 初始化兼容问题沿用第七批未解状态；本批使用短标签完成比较，不宣称已修复。

基线、回退与证据
第七批正式 361 项代码/工具/程序分别与 {OLD/'final-source'}、{S/'baseline'} 核对。
路径推进独立验证节点：{S/'parts/path-advance-verified'}。
碰撞前置及观测节点：{S/'parts/entry-collision-verified'}。
最终无额外寻路调用节点：{S/'parts/final-world-only-verified'}。
最终配套源、工具、程序：{S/'final-source'}；指纹 source-manifest.json，差异 source-changes.patch。
20 项 H: 原始输入、game.exe、SAVE0029.SAV、旧手写引擎和 37 处未支持保护均保持原指纹。没有提交、推送或清理旧证据。
汇总：{S/'validation.json'}
效果：{S/'effects.json'}
预算：{S/'budget-conditions.json'}
阅读入口：{guide}

接续工作
1. 优先整理 Advance 的 4A1B60..4A1F8D 转弯接续和后续碰撞，保持样本进度及共享尾部行为。
2. 整理 CanEnterCell 的 703439..703A95 对象链/建筑特例，审计 Prepare 的共享/恢复入口。
3. 根据两/三格无额外重建包围的实际队列演变继续定位 stage 18，不能用主动清队列制造自然覆盖。
4. 检查本机支持的超时空/入格世界回调在旧 Drive 调用栈中的移动器替换；自然预算耗尽仍须真实命中才验收。
5. 每个可读部分继续片段和实景逐帧对照；保留所有基线、完整回退、失败证据，继续不提交或推送。
'''
    for p in (report,handoff): p.write_text(text,encoding='utf-8',newline='\n')
    paths={e['path'] for e in previous}
    for folder in ('gameplay','runtime'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'ra2/src'/folder).glob('ground_*'))
    for pattern in ('*v8*.py','*v8*.ps1'):
        paths.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern))
    for pattern in ('*.c','*.h','*.asm','*.txt'):
        paths.update(p.relative_to(ROOT).as_posix() for p in S.glob(pattern))
    for p in (S/'fixtures').glob('*'):
        if p.is_file(): paths.add(p.relative_to(ROOT).as_posix())
    for name in ('effects.json','budget-conditions.json','action-bounds.json'):
        paths.add((S/name).relative_to(ROOT).as_posix())
    manifest=[]; patch=[]
    for relative in sorted(paths):
        p=ROOT/relative; target=S/'final-source'/relative; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,target)
        manifest.append(dict(path=relative,bytes=p.stat().st_size,sha256=sha(p)))
        if p.suffix.lower() in ('.c','.h','.py','.ps1','.txt','.ini','.map') or p.name=='CMakeLists.txt':
            b=S/'baseline'/relative
            before=b.read_text(encoding='utf-8',errors='replace').splitlines(True) if b.exists() else []
            patch.extend(difflib.unified_diff(before,p.read_text(encoding='utf-8',errors='replace').splitlines(True),fromfile='v7/'+relative,tofile='v8/'+relative))
    write(S/'source-manifest.json',manifest); (S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8',newline='\n')
    for p in (report,handoff):
        target=S/'final-source/project'/p.relative_to(PROJECT); target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,target)
    validation=dict(passed=True,exe=str(exe),exe_sha256=fingerprint,state_schema=10,paired_scenes=23,paired_frames=frames,
        scenarios=cases,probes=probes,new_native_fragment_cases=131072,source_files=len(manifest),
        preservation_passed=True,effects_passed=True,auxiliary_passed=True,full_original_equivalence_verified=False,
        whole_prepare_function_readable=False,whole_ground_movement_readable=False,normal_budget_exhaustion_verified=False,
        second_search_failure_naturally_observed=budget['second_search_failure_naturally_observed'],
        turn_cloaked_obstacle_scene_verified=True,all_turn_results_naturally_observed=False,
        controlled_real_world_budget_entry_verified=True,long_directory_startup_compatibility_fixed=False,
        committed=False,pushed=False,report=str(report),handoff=str(handoff))
    write(S/'validation.json',validation)
    pointer=read(PROJECT/'reports/latest-recovery.json'); assert pointer['sha256']=='8d84594096407e3442a6e66c0d1baa64c34996256b1a9fef97cb0d24f98f6b0f'
    pointer.update(validation=str(S/'validation.json'),executable=str(exe),sha256=fingerprint,state_schema=10,report=str(report),
        preservation_passed=True,previous_recovery_validation=str(OLD/'validation.json'),
        previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
        previous_recovery_sha256='8d84594096407e3442a6e66c0d1baa64c34996256b1a9fef97cb0d24f98f6b0f',
        next_readable_region='Advance 4A1B60..4A1F8D; CanEnterCell object scan 703439..703A95; Prepare shared/recovery entries',
        turn_cloaked_obstacle_scene_verified=True,second_search_failure_naturally_observed=budget['second_search_failure_naturally_observed'])
    write(PROJECT/'reports/latest-recovery.json',pointer)
    write(PROJECT/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=fingerprint,
        state_schema=10,paired_frames=frames,paired_scenes=23,passed=True,first_difference=None,full_original_equivalence_verified=False,
        normal_budget_exhaustion_verified=False,second_search_failure_naturally_observed=budget['second_search_failure_naturally_observed'],report=str(report)))
    for relative in ('reports/latest-recovery.json','reports/latest-state-comparison.json'):
        target=S/'final-source/project'/relative; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(PROJECT/relative,target)
    assert all(sha(ROOT/e['path'])==e['sha256'] and sha(S/'final-source'/e['path'])==e['sha256'] for e in manifest)
    print(json.dumps(dict(passed=True,exe_sha256=fingerprint,paired_scenes=23,paired_frames=frames,source_files=len(manifest)),indent=2))
if __name__=='__main__': main()
