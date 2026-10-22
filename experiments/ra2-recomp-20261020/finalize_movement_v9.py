"""验收本批全部证据、保全回退，再写入第九批正式入口。"""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
S = ROOT/'evidence/movement-state-v9'
OLD = ROOT/'evidence/movement-state-v8'
EXPECTED = '734138bb0a3b1638745a3e61adb9f59953e3e48ddca2129d1a4ef585407b0bfa'
PREVIOUS = 'e16033580b82aed1fea031052703407d5b39dfe305b271c36cf6501ce0056ae9'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def write(p, value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    assert not (S/'validation.json').exists()
    exe = ROOT/'ra2/build-original-c/ra2.exe'
    assert sha(exe)==EXPECTED
    pointer = read(PROJECT/'reports/latest-recovery.json')
    assert pointer['sha256']==PREVIOUS
    matrices = [read(S/'i-matrix.json'),read(S/'i-additional-matrix.json')]
    assert all(m['passed'] and m['exe_sha256']==EXPECTED for m in matrices)
    cases = [r for m in matrices for r in m['results']]
    frames = sum(r['frames'] for r in cases)
    assert len(cases)==25 and frames==13345
    for row in cases:
        p = S/'runs'/row['tag']
        report = read(p/'comparison.json')
        c = report['comparison']
        assert report['passed'] and report['exe_sha256']==EXPECTED and report['seed']==12345,row['tag']
        assert c['equal_frames']==c['consecutive_equal_frames']==c['frames_compared']==row['frames']
        assert c['rng_equal_all_frames'] and c['first_difference'] is None and c['command_difference'] is None
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        for run in report['runs']:
            assert run['passed'] and run['exit_code']==0 and run['save_is_private_copy']
            assert run['save_before_sha256']==run['save_after_sha256']
        for mode in ('original','generated-c'):
            with (p/mode/'state.jsonl').open(encoding='utf-8') as f:
                assert json.loads(next(f))['schema']==11
    probes = {p.name:read(p) for p in S.glob('*-verified-01.json')}
    assert len(probes)==36 and all(p['passed'] for p in probes.values())
    assert probes['continuation_probe-verified-01.json']['continuation_cases']==65536
    assert probes['continuation_probe-verified-01.json']['all_eight_passages']
    assert all(probes[f'objects_probe-{i}-verified-01.json']['object_cases']==65536 for i in range(4))
    effects, budget = read(S/'effects.json'),read(S/'budget-conditions.json')
    assert effects['passed'] and budget['second_search_failure_naturally_observed']
    assert not budget['natural_exhaustion_verified'] and not budget['natural_budget_entries']
    assert effects['natural_secondary_failure']['failure_frame']==399
    assert effects['turn_continuation']['passage_counts']=={'0':4,'1':1}
    assert effects['object_collision']['total_entries']==903
    aux = read(S/'auxiliary-final-02/validation.json')
    assert aux['passed'] and aux['exe_sha256']==EXPECTED

    previous = read(OLD/'source-manifest.json')
    assert len(previous)==449
    for e in previous:
        assert sha(OLD/'final-source'/e['path'])==e['sha256'],e['path']
        assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
    assert sha(S/'baseline/ra2/build-original-c/ra2.exe')==PREVIOUS
    snapshots = {}
    for name, expected_count in [('turn-continuation-verified',453),('object-collision-verified',457)]:
        p = S/'parts'/name
        manifest = read(p/'manifest.json')
        assert len(manifest)==expected_count
        assert all(sha(p/e['path'])==e['sha256'] for e in manifest)
        snapshots[name] = dict(path=str(p),files=len(manifest),
            exe_sha256=sha(p/'ra2/build-original-c/ra2.exe'),validation=read(p/'validation-source.json'))
    inputs = []
    for e in read(ROOT/'evidence/original-inputs-before.json'):
        actual = sha(Path(r'H:\开发\运行版本\原版1.006')/e['name'])
        assert actual==e['sha256'],e['name']
        inputs.append(dict(**e,verified_sha256=actual))
    assert len(inputs)==20
    assert sha(ROOT/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
    assert sha(ROOT/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
    assert sha(PROJECT/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    guards = sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8')))
        for p in (ROOT/'ra2/src/recomp/gen_game').glob('*.c'))
    assert guards==37
    report = PROJECT/'docs/单位移动第九批-转弯接续与对象碰撞-20261021.txt'
    handoff = PROJECT/'交接文档-单位移动第九批-20261021.txt'
    assert not report.exists() and not handoff.exists()
    guide = ROOT/'ra2/src/gameplay/阅读说明-单位移动.txt'
    guide_text = guide.read_text(encoding='utf-8')
    assert '二十二、第九批' not in guide_text
    assert '单位移动的可读 C：第八批，路径跨格推进与碰撞前置' in guide_text

    preservation = dict(passed=True,all_20_original_inputs_unchanged=True,inputs=inputs,
        previous_449_source_files_and_v8_executable_preserved=True,component_snapshots=snapshots,
        original_game_exe_and_save_unchanged=True,old_handwritten_engine_unchanged=True,
        unsupported_guards=guards,committed=False,pushed=False)
    write(S/'preservation.json',preservation)
    guide_text = guide_text.replace('单位移动的可读 C：第八批，路径跨格推进与碰撞前置',
        '单位移动的可读 C：第九批，转弯接续与对象碰撞',1)
    guide_text += '''
二十二、第九批：怎样接上下一段转弯

ground_continuation.h/.c / ra2_ground_continue_turn：4A1B60..4A1F8D。
在模板过渡采样检查下一方向和朝向差，选择后继模板；无有效模板时沿用现有收尾。
候选格由当前路段终点加方向偏移得到，先保存单位速度位，再调用真实通行查询。
通行码 0/2：更新模板与采样索引→刷新单位→检查存活及停止标志→设置下一终点。
候选格接受单位后开始新路段，恢复先前速度，并左移方向队列 23 项、以 -1 结束。
通行码 1 揭露隐形对象，3 请求闸门，6 根据桥面层通知临时障碍；其余分类保留原版收尾。
这里移动障碍 2 可以接续，不能直接套用 Prepare 的让路重试处理。
返回 0 只表示中止本次 Advance；普通受阻也可能返回 1 继续原有采样收尾。
gameplay 展示规则顺序；runtime/ground_continuation_bridge.c 负责旧模板表、对象布局和服务调用。
Type+BA4、owner flag 76/7A 等未确定名称的字段继续保守命名，避免给 MOD 作者虚构规则键。

二十三、第九批：格子中的对象怎样影响通行

ground_objects.h/.c 提供四个短流程，适配层是 runtime/ground_objects_bridge.c。
ra2_ground_filter_object（70346B..703536）：自身/关联对象过滤、建筑占地及配对类型判断，再交给闸门或一般碰撞。
ra2_ground_filter_building（7035AC..703693）：方向与占地、任务阶段、所属方标志、相邻格锚点等建筑例外。
ra2_ground_classify_enemy（70397C..703A95）：隐形→可碾压→武器/列车条件→特殊建筑/地形武器→可破坏障碍。
ra2_ground_classify_stationary_ally（70394F..70397C）：静止友方建筑硬阻挡，其他对象至少为临时障碍。
碾压分支按原版重新查询阵营关系；扫描结果用取最大值的方式提升通行分类，不能覆盖已有更强阻挡。
现有 ground_barrier.c 继续处理闸门；新代码复用它，没有把门与普通建筑揉成一个判断。
Type+BB0、建筑字节标志等含义未完全确认；修改前先核对调用点及实景，不能仅凭偏移套用其它版本的规则名称。
移动友方对象的朝向/距离几何 703693..70394F、地形/层级尾部及 Advance 前后剩余部分尚未整理。

二十四、第九批：二次补建失败已经自然出现

参照 i-long：第 5 帧命令卡车驶向 100,114，正常沿长路线行驶；第 399 帧第二方向缺失、剩余距离 2560，正常请求二次补建并成功。
对照 i-second-failure：同样路线，第 398 帧由原版世界服务合法放置半径两格的 16 辆敌方卡车；不额外调用重建，不写队列和预算。
第 398 帧队列自然仅剩 [2]；第 399 帧补建失败（stage 18），同一 Drive 的目标被清空，下一帧队列为空。
两路 651 帧的已记录对象状态、RNG、命令、有序分支全部相等。失败预算全程为 10，没有 stage 3。
这补齐二次补建失败的实景，但预算自然耗尽仍未验收；继续调查目标保留和移动器替换/回调条件。
旧一格预算压力场景含显式重建步骤，仍单独标注，不能当作普通更新自然耗尽的证明。

二十五、第九批验证范围及修改方法

最终程序 schema 11，25 个配对实景共 13345 帧；36 组原版片段/回归通过，新增 327680 组片段输入。
接续分类在墙体、坡地、窄弯中实际出现 5 次：通行码 0 四次、1 一次；其它通行码以原版片段覆盖为准。
对象过滤入口实际记录 903 次；这不表示对象扫描的所有分支都已在实景自然命中。
stage 22 记录候选服务返回后的有效第二方向，stage 23 记录缺方向且距离大于 512 的正常补建请求。
stage 24 只记录本扫描检查的对象 flags14 位 0/2；h-fail 曾因未使用高位不同而严格对照失败，失败证据保留。
未证明高位差异来源；修正观测范围后，以同一最终程序重跑全部 25 场景通过，游戏状态比较未放宽。
修改 MOD 流程应先修改命名 gameplay 判断，再对照原版片段确认未改动路径的行为，最后运行相关实景及固定存档回归。
新增玩法若有意改变结果，必须单独记录预期差异；不能悄悄改验证阈值来宣称和原版相等。
全部基线、两部分回退、程序指纹及剩余工作见第九批交接文档；全游戏等价仍未完成。
'''
    guide.write_text(guide_text,encoding='utf-8',newline='\n')
    text = f'''原版 1.006 单位移动第九批：转弯接续与对象碰撞（2026-10-21）

一、本批结果

已整理并接入纯 C17 的 ground_continuation.h/.c、ground_objects.h/.c；各有独立 runtime 适配层。
接续部分对应 4A1B60..4A1F8D；对象部分对应 70346B..703536、7035AC..703693、70394F..703A95。
可读流程包括后继模板选择、候选通行、速度保存恢复、接续后队列左移，以及对象过滤、建筑例外、敌方碾压/武器条件和静止友方处理。
新核心/适配文件按 /W4 /WX /std:c17 /utf-8 编译；玩法核心不直接访问旧对象地址，未知字段保守命名。
未修改原版资源或正式规则，没有提交、推送、重置或清理旧证据。
程序：{exe}
SHA-256：{EXPECTED}
阅读入口：{guide}

二、逐帧和片段验收

最终 25 场景共 {frames:,} 个连续模拟帧：已记录的对象状态、RNG、命令、有序分支全部一致，schema 11，seed 12345。
保留原 15 场景 8235 帧及第八批 8 场景 2958 帧，新增长路线 1501 帧与二次失败 651 帧。
固定 SAVE0029.SAV 的 2190..3000 窗口继续通过，包含第 2247 帧；移动/转弯/停止、拥堵、墙体、闸门、坡地、隐形和超时空场景均重跑。
每场原版与 C 使用独立存档副本，并检查存档前后指纹；比较器的位移差异和缺帧反例均能被拒绝。
36 组原版片段/回归通过；新增接续 65536 组、对象四阶段各 65536 组，共 327680 组输入。
片段对照包括服务调用顺序、活跃状态/临时量及相关浮点环境；接续片段覆盖八种通行分类。
实景 stage 21 仅命中 5 次，通行码 0 四次、1 一次；不是八种接续碰撞都已自然覆盖。
命中：i-wall 第 677 帧、i-slope-healthy 第 33 帧、i-slope-damaged 第 40 帧、i-tc0/i-tc2 第 223 帧。
对象 stage 24 共 903 次入口；不能把入口次数当成所有内部例外均已自然命中。
诊断关闭启动、保护退出等附加检查通过：{S/'auxiliary-final-02/validation.json'}。

三、二次补建失败：本批新增实景证据

i-long 和 i-second-failure 使用相同独立地图与第 5 帧卡车移动命令：从 67,114 向 100,114 行驶。
短路线的队列过去往往在接近目标、距离不大于 512 时耗尽，因此不会进入正常二次补建请求。
长路线在第 398 帧自然只剩方向 [2]；第 399 帧第二方向为 -1，剩余距离 2560，大于 512，stage 23 正常请求二次补建。
i-long 无新障碍，补建成功，继续走完；i-second-failure 在第 398 帧围入半径两格的 16 辆真实敌方卡车。
障碍由原版构造/放置服务创建；当前目的地可达性前后均为 1；没有额外调用寻路、注入路径队列、改预算或伪造碰撞返回值。
第 399 帧自然命中 stage 18：二次补建失败，同一活动 Drive，调用者/活动 Drive 目标都已无效；第 400 帧可见目标清零和空队列。
失败实景两路完整 651 帧一致。参照长路线两路 1501 帧一致。
失败预算始终为 10，stage 3 为 0；二次补建失败验收为 true，预算自然耗尽仍为 false。
旧一格压力试验包含显式重建，不算自然耗尽证明；本批两/三格包围及上述新失败试验不额外调用重建。
预算分支需要失败后仍保留目标并通过后续可达性复核，当前真实失败清空目标；继续关注旧 Drive 栈中的移动器替换/世界回调。
这是待验证条件，不是整个游戏预算分支不可达的证明。本机动作范围 1..117，动作 128 不能用来证明合法 TeleportAll 触发。
候选服务 705160 的静态片段未见直接写方向队列；不能把它命名成“截断队列”，其世界服务回调仍须按实际状态重新查询。

四、保留的调查与比较边界

h-fail 的游戏状态和 RNG 651 帧相等，但新增 stage 24 原始 flags14 高位不同（31/7），严格有序观测比较失败。
只记录此扫描实际检查的 mask 0x05 后，用最终程序重新运行全部 25 场景通过；没有放宽对象状态、命令顺序或 RNG 的比较。
未证明未使用高位不同的具体原因；h-fail 的失败轨迹和首轮程序保留，不把它列为正式通过。
schema 11 新增 stage 21 接续分类、22 候选返回后第二方向、23 正常二次请求、24 对象过滤；均保留原版与 C 的观测。
隐形窄弯使用相同地图规则给卡车启用合法隐形属性，不是声称原版卡车默认隐形。
长目录 ra2.csf 初始化兼容问题仍未修复，沿用短标签完成验证。既有失败试验继续保留。
全 Advance、CanEnterCell、完整移动和全游戏等价仍为 false；已通过的是上述范围与固定输入窗口。

五、基线、回退、验收文件

第八批 449 项正式代码/工具/程序与 {OLD/'final-source'}、{S/'baseline'} 逐项哈希核对。
转弯接续独立节点（453 项，固定存档 811 帧通过）：{S/'parts/turn-continuation-verified'}。
对象碰撞最终节点（457 项，二次失败实景通过）：{S/'parts/object-collision-verified'}。
最终配套源、工具与程序：{S/'final-source'}；清单 source-manifest.json，差异 source-changes.patch。
H: 原始 20 项输入、game.exe、SAVE0029.SAV、旧手写引擎及 37 处未支持保护保持原指纹。
第八批正式 EXE SHA-256：{PREVIOUS}；本批 baseline 内保留完整可回退程序。
正式汇总：{S/'validation.json'}
效果统计：{S/'effects.json'}
预算条件：{S/'budget-conditions.json'}
保全核对：{S/'preservation.json'}
正式入口：{PROJECT/'reports/latest-recovery.json'}、{PROJECT/'reports/latest-state-comparison.json'}。

六、下一批从这里继续

1. 优先整理移动友方对象的朝向/距离几何 703693..70394F 和后续地形/层级碰撞尾部，注意原版浮点舍入与再次读取状态。
2. 完善 Advance 前部 4A1000..4A16A6 及接续后的 4A1F8D 以后插值/放置尾部；保留既有跨格和接续模块。
3. 审计 Prepare 共享/恢复入口，继续核实未命名建筑标志，不套用其它游戏版本的 INI 键。
4. 二次失败已完成实景覆盖；以该合法场景为新参照，继续调查目标保留、可达性复核与旧 Drive 回调中的移动器替换，直到实际观察到预算自然扣减/耗尽。
5. 每部分继续原版片段与实景逐帧对照，保留当前全部基线、失败证据和完整回退；暂时不提交或推送。
'''
    for p in (report,handoff):
        p.write_text(text,encoding='utf-8',newline='\n')

    paths = {e['path'] for e in previous}
    for folder in ('gameplay','runtime'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'ra2/src'/folder).glob('ground_*'))
    for pattern in ('*v9*.py','*v9*.ps1'):
        paths.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern))
    for pattern in ('*.c','*.h','*.asm','*.txt'):
        paths.update(p.relative_to(ROOT).as_posix() for p in S.glob(pattern))
    paths.update(p.relative_to(ROOT).as_posix() for p in (S/'fixtures').glob('*') if p.is_file())
    for name in ('effects.json','budget-conditions.json','action-bounds.json'):
        paths.add((S/name).relative_to(ROOT).as_posix())
    manifest, patch = [], []
    for relative in sorted(paths):
        p = ROOT/relative
        target = S/'final-source'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,target)
        manifest.append(dict(path=relative,bytes=p.stat().st_size,sha256=sha(p)))
        if p.suffix.lower() in ('.c','.h','.py','.ps1','.txt','.ini','.map') or p.name=='CMakeLists.txt':
            b = S/'baseline'/relative
            before = b.read_text(encoding='utf-8',errors='replace').splitlines(True) if b.exists() else []
            patch.extend(difflib.unified_diff(before,p.read_text(encoding='utf-8',errors='replace').splitlines(True),
                fromfile='v8/'+relative,tofile='v9/'+relative))
    write(S/'source-manifest.json',manifest)
    (S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8',newline='\n')
    for p in (report,handoff):
        target = S/'final-source/project'/p.relative_to(PROJECT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,target)
    validation = dict(passed=True,exe=str(exe),exe_sha256=EXPECTED,state_schema=11,
        paired_scenes=25,paired_frames=frames,scenarios=cases,probes=probes,
        new_native_fragment_cases=327680,source_files=len(manifest),
        preservation_passed=True,effects_passed=True,auxiliary_passed=True,
        full_original_equivalence_verified=False,whole_prepare_function_readable=False,
        whole_ground_movement_readable=False,normal_budget_exhaustion_verified=False,
        second_search_failure_naturally_observed=True,natural_secondary_failure_frame=399,
        turn_continuation_naturally_observed=True,all_continuation_results_naturally_observed=False,
        turn_cloaked_obstacle_scene_verified=True,all_turn_results_naturally_observed=False,
        controlled_real_world_budget_entry_verified=True,long_directory_startup_compatibility_fixed=False,
        committed=False,pushed=False,report=str(report),handoff=str(handoff))
    assert all(sha(ROOT/e['path'])==e['sha256'] and sha(S/'final-source'/e['path'])==e['sha256'] for e in manifest)
    write(S/'validation.json',validation)
    pointer.update(validation=str(S/'validation.json'),executable=str(exe),sha256=EXPECTED,state_schema=11,
        report=str(report),preservation_passed=True,previous_recovery_validation=str(OLD/'validation.json'),
        previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=PREVIOUS,
        next_readable_region='CanEnterCell moving-allied geometry 703693..70394F and terrain/layer tail; Advance front and interpolation tail; Prepare shared/recovery entries',
        turn_continuation_naturally_observed=True,second_search_failure_naturally_observed=True)
    write(PROJECT/'reports/latest-recovery.json',pointer)
    write(PROJECT/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=EXPECTED,
        state_schema=11,paired_frames=frames,paired_scenes=25,passed=True,first_difference=None,
        full_original_equivalence_verified=False,normal_budget_exhaustion_verified=False,
        second_search_failure_naturally_observed=True,report=str(report)))
    for relative in ('reports/latest-recovery.json','reports/latest-state-comparison.json'):
        target = S/'final-source/project'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(PROJECT/relative,target)
    print(json.dumps(dict(passed=True,exe_sha256=EXPECTED,paired_scenes=25,paired_frames=frames,
        source_files=len(manifest),secondary_failure_verified=True,natural_budget_exhaustion=False),indent=2))

if __name__=='__main__':
    main()
