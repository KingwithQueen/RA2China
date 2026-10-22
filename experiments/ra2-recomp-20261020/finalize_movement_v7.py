"""第七批：所有正式场景、探针和回退核验后才更新项目入口。"""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT/'evidence/movement-state-v7'
OLD = ROOT/'evidence/movement-state-v6'
EXPECTED = '8d84594096407e3442a6e66c0d1baa64c34996256b1a9fef97cb0d24f98f6b0f'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    assert not (STAGE/'validation.json').exists()
    fingerprint = sha(ROOT/'ra2/build-original-c/ra2.exe')
    assert fingerprint==EXPECTED
    matrix = read(STAGE/'c-matrix.json')
    assert matrix['passed'] and matrix['exe_sha256']==fingerprint and len(matrix['results'])==15
    results = {}
    for row in matrix['results']:
        tag,count = row['tag'],row['frames']
        report = read(STAGE/'runs'/tag/'comparison.json')
        comparison = report['comparison']
        assert report['passed'] and report['exe_sha256']==fingerprint,tag
        assert comparison['equal_frames']==comparison['frames_compared']==comparison['consecutive_equal_frames']==count,tag
        assert comparison['first_difference'] is None and comparison['command_difference'] is None,tag
        assert comparison['rng_equal_all_frames'] and comparison['negative_control']['passed'],tag
        assert comparison['negative_control']['missing_frame_rejected'],tag
        for mode in ('original','generated-c'):
            with (STAGE/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8') as stream:
                assert json.loads(next(stream))['schema']==9
        assert all(r['exit_code']==0 and r['passed'] and r['save_is_private_copy']
            and r['save_before_sha256']==r['save_after_sha256'] for r in report['runs'])
        results[tag] = dict(passed=True,paired_frames=count,comparison=str(STAGE/'runs'/tag/'comparison.json'))
    paired_frames = sum(r['paired_frames'] for r in results.values())
    assert paired_frames==8235
    probes = {p.name:read(p) for p in STAGE.glob('*-verified-01.json')
        if not p.name.startswith(('followup_probe-','turn_probe-'))}
    for name in ('followup_probe-0-verified-02.json','followup_probe-1-verified-02.json','turn_probe-0-verified-03.json'):
        probes[name] = read(STAGE/name)
    assert len(probes)==29 and all(p['passed'] for p in probes.values())
    assert probes['turn_probe-0-verified-03.json']['owner_removed_cases']==3537
    assert all(probes['turn_probe-0-verified-03.json']['classified_counts'])
    new_cases = sum(p.get('followup_cases',0)+p.get('turn_cases',0) for p in probes.values())
    assert new_cases==196608
    effects,budget = read(STAGE/'effects.json'),read(STAGE/'budget-conditions.json')
    assert effects['passed'] and not budget['natural_exhaustion_verified']
    assert effects['chrono']['c-chrono-seam-budget']['real_walls_created']==8
    auxiliary = read(STAGE/'auxiliary-final-02/validation.json')
    assert auxiliary['passed'] and auxiliary['exe_sha256']==fingerprint
    old_manifest = read(OLD/'source-manifest.json')
    assert len(old_manifest)==286
    for e in old_manifest:
        assert sha(OLD/'final-source'/e['path'])==e['sha256'],e['path']
        assert sha(STAGE/'baseline'/e['path'])==e['sha256'],e['path']
    snapshots = {}
    for name in ('speed-followup-verified-02','turn-collision-verified','final-owner-guard-verified'):
        folder = STAGE/'parts'/name
        manifest = read(folder/'manifest.json')
        assert all(sha(folder/e['path'])==e['sha256'] for e in manifest)
        snapshots[name] = dict(path=str(folder),files=len(manifest),exe_sha256=sha(folder/'ra2/build-original-c/ra2.exe'))
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
    write(STAGE/'preservation.json',dict(passed=True,inputs=inputs,all_20_original_inputs_unchanged=True,
        previous_286_source_files_and_v6_executable_preserved=True,old_handwritten_engine_unchanged=True,
        original_game_exe_and_save_unchanged=True,unsupported_guards=guards,component_snapshots=snapshots,
        incomplete_early_snapshot_not_used_for_rollback='parts/speed-followup-verified: missing new runtime bridge; complete copy is -02'))

    guide = ROOT/'ra2/src/gameplay/阅读说明-单位移动.txt'
    body = guide.read_text(encoding='utf-8')
    assert '十六、第七批' not in body
    body = body.replace('单位移动的可读 C：第六批，临时/隐形障碍与路径模板状态',
        '单位移动的可读 C：第七批，速度准备与转弯碰撞')
    body = body.replace('表的 flags & 8 继续进入尚未整理的转弯部分。',
        '表的 flags & 8 进入转弯部分；该部分已在第七批 ground_turn.c 整理。')
    body = body.replace('下一步：4A3C9B..4A3F8B','第六批结束时的下一步：4A3C9B..4A3F8B')
    body += '''
十六、第七批：速度和第二次路径准备

ground_followup.h/.c / ra2_ground_prepare_speed：4A3C9B..4A3E35。
地形系数先把大于 1 的值限制为 1，再按目标/当前地表高度选上下坡系数；系数为 0 时沿用原版 0.5 回退。
Unit 种类在本机原版 v2C 返回 1；其 SpeedClass=1 和其它类使用两组坡度参数，未确认的参数名保留保守命名。
生命比例不大于 ConditionYellow 时再乘 0.75。比较使用原版精度，不能把它改成统一的 double 中间值。
地形上限只在坡度修正之前应用，所以真实下坡系数可以达到 1.2000000476837158。
模板选择器小于 64 时写 Drive 的速度系数；其它情况与单位当前速度比较，不同才调用速度设置服务。
MOD 修改限速/坡度/受损速度从该函数阅读；精确数值与规则布局在 runtime/ground_followup_bridge.c。

ra2_ground_prepare_followup：4A3E35..4A3F8B，并接回原版 4A3F9F 的强制直行入口。
先让原版单位准备候选格，然后读取第二方向；已有第二方向直接选择模板。
没有第二方向时，距目标不大于 512 则直行；更远才按火车模式补建路径。
补建失败后检查所有者、写中止标记或复核目的地并停止，最后重新读第二方向。这一段没有直接扣失败预算。
同样的距离数值服务在此按 z²+y²+x² 求和，转弯特殊阻挡分支按 x²+y²+z² 求和，不能随意共用轴顺序。

十七、第七批：转弯模板及后续碰撞

ground_turn.h/.c / ra2_ground_prepare_turn：4A4015..4A45B7。
先检查当前候选格是否接纳单位，再把下一方向的偏移加到候选点并检查第二格的完整通行码。
火车和可碾压覆盖物有单独特例；成功时一次消耗两个方向，并设置桥切换标志，再接入已有路段提交。
开闸、移动车辆、临时障碍、隐形障碍、硬阻挡分别决定通知、重试、揭露、停止或丢弃候选。
移动障碍重试不清队列；临时/硬阻挡的允许递归重试清头并重置计时器；隐形重试清头但不重置计时器。
递归后所有者可以消失，适配层不再访问其队列。原版片段已覆盖 3,537 组该边界输入。
本批实景命中转弯通行 0/2；另外六类已在片段对照覆盖，但不能声称都自然触发过。

十八、第七批验证及待续

正式 15 组实景共 8,235 对帧，schema 9，完整 RNG、对象和有序分支记录一致；29 项新旧探针通过，新增 196,608 组片段输入。
满血/受损坦克都真实经过 416→520→416 坡地；速度分别为 1/1.2000000476837158 与 0.75/0.9000000357627869。
援军动作需要 TeamType 引用选择器 1：107,1,TeamID。已通过原版地图创建新单位并观察到 Teleport→Drive。
另在包装时发令、落地后重新发令并放置真实墙体，预算仍为 10，未见包装期旧 Drive Prepare。
比较器现按实际出生/存在帧比较受控单位；保留了旧比较器遇到中途出生单位时的失败记录。
中间节点封墙后带 Stop 的调查有 601 对帧相等，但末任务仍为 [13,2,-1]，不计为停止完成；正式预算场景单独验证移动和封墙。
长试验目录中 C 模式出现过 ra2.csf 初始化失败；短目录完成正式对照。根因尚未定位，不能宣称已修复启动路径兼容。
自然失败预算耗尽仍未验证；普通失败仍清目标。入格/世界服务在旧调用栈中替换移动器只是一条待验证方向。
第二次路径补建失败若没有 stage 18 实景命中，也只算原版片段验证。
接着整理 AdvanceSegment、CanEnterCell 剩余分支，并审计 PrepareSegment 的共享/恢复入口；全游戏等价尚未完成。
报告和接续文档：docs/单位移动第七批-速度准备与转弯碰撞-20261021.txt、交接文档-单位移动第七批-20261021.txt。
第六批 286 项基线和本批各验证节点、所有失败试验均保留。没有提交或推送。
'''
    guide.write_text(body,encoding='utf-8',newline='\n')
    report = PROJECT/'docs/单位移动第七批-速度准备与转弯碰撞-20261021.txt'
    handoff = PROJECT/'交接文档-单位移动第七批-20261021.txt'
    assert not report.exists() and not handoff.exists()
    text = f'''原版 1.006 单位移动第七批：速度准备、第二路径与转弯碰撞（2026-10-21）

本批完成
ground_followup.c/.h、ground_turn.c/.h 两组可读纯 C17 核心，以及独立 runtime/ground_followup_bridge.c/.h 适配层。
覆盖 4A3C9B..4A3F8B、4A4015..4A45B7，接回第六批模板选择和路段提交；通过常规入口可读地执行 PrepareSegment 后半段。
整个 PrepareSegment、AdvanceSegment、CanEnterCell 和全游戏等价仍未全部完成，未知字段和其它共享/恢复入口继续审计。
最终程序：{ROOT/'ra2/build-original-c/ra2.exe'}
SHA-256：{fingerprint}
15 组正式场景 {paired_frames:,} 对帧全部一致，完整 RNG、对象状态及有序命令/分支一致。29 项新旧探针通过，新增 196,608 组原版片段输入。

可读行为与 MOD 入口
ground_followup.c：地形基础上限、上下坡、零系数回退、ConditionYellow 以下 0.75 减速、按模板状态写 Drive 或单位速度。
保留存回 double 与寄存器中未再次舍入值的差异，使用已有整数表示的数值兼容层；全部新文件以 /W4 /WX /std:c17 编译。
同文件第二函数：候选格准备、第二方向检查、512 距离回退、火车模式补建、所有者消失及复核停止。
ground_turn.c：第二候选格、8 类通行码、火车/碾压特例、开闸、重试、隐形揭露、停止、丢弃候选和一次消耗两个方向。
世界服务前后同步候选点、队列及 Drive；递归返回后不再访问已消失所有者。3,537 组原版片段输入覆盖该边界。
阅读说明：{guide}

真实验证
固定存档移动/转向/停止 811 帧，四车拥堵 811 帧；Clear/Rock 限制地形各 301 帧。
墙体 1001 帧、闸门 701 帧、卡车动态建墙 301 帧，旧第 27 帧速度位保持 47e17a14ae47d13f。
自然失败压力 301 帧、受控预算入口 101 帧；隐形走廊 601 帧、第 197 帧揭露；完整规则零等待 601 帧。
新增满血/受损坦克坡地各 601 帧，实际高度 416→520→416，回到起点并完成停止。
满血系数出现 1.0 和 1.2000000476837158；受损系数为 0.75 和 0.9000000357627869，生命 400/100。
新增超时空援军 601 帧，动作参数引用选择器改为 1 后原版真正创建单位 1022584，观察 Teleport/Drive 切换。
新增包装期间发令、落地后再发令并封墙的预算场景 601 帧，真实创建 8 段墙、实际移动，两路逐帧相等。
转弯实景命中通行 0 和 2；八类通行码均在原版片段输入中覆盖，不能把其它六类写成已自然命中。
state schema 9：stage 16 速度入口，17 第二方向准备，18 二次补建失败，19 转弯分类；保留原有所有者身份记录。
比较器检查实际出生帧和存在区间；坐标 +1 与缺帧反例检测通过。关闭诊断正常退出；错误编号保护退出 7。

预算自然耗尽调查
四个自然失败场景仍显示 active_is_caller=true，失败后调用者目标无效、预算保持 10。
已补齐真实援军包装生命周期及其后移动/墙体阻挡，仍未见旧 Drive 在别的当前移动器期间执行 Prepare，没有自然扣预算入口。
2AC 可达性复核读取目标 x/y 格、桥标志和区划，不读取目标 z；单独目标高度差不能解释两次复核不一致。
本机静态候选：Prepare 的 8 处直接 CALL 都位于 Drive 函数族；Process 只有 Drive 表槽 7A050C 的静态指针候选。未证明全部间接流。
后续可追踪入格触发器/世界服务在同一旧 Drive 调用栈中替换移动器，再返回旧 Prepare 的瞬间。这是待验证假设，尚不是已查明的触发条件。
第二补建失败的 stage 18 真实命中情况以 effects.json/budget-conditions.json 为准，零命中只算片段验证。
受控入口 10→0 及额外零预算停止仍单列，不冒充自然耗尽。

保留的未通过记录与限制
旧援军动作选择器 0 没有创建单位；修正为 1 才真实出现，历史地图和记录均保留。
中间节点带 Stop 的封墙调查 601 对帧一致，但末任务仍是 [13,2,-1]，严格停止门槛未满足；不计正式停止通过。
原比较器假定单位第 0 帧存在，已修正后处理并保留异常日志。该调查从原始完整轨迹补做比较，没有伪造游戏结果。
较长目录下 C 路出现 ra2.csf 初始化失败，原版正常；正式 c- 短目录完成对照。观察到路径相关性，根因未定位，也没有宣称启动兼容已修复。
验证限于列出的输入、字段和场景，没有宣称全游戏等价或全部移动状态可读。

基线、回退和复现
{STAGE/'baseline'}：第六批 286 项正式源及程序、旧报告入口，全部指纹核对。
{STAGE/'parts/speed-followup-verified-02'}：第一部分 811 帧通过后的配套源码/程序；早期无 -02 的不完整快照另存，不作为回退节点。
{STAGE/'parts/turn-collision-verified'}：转弯碰撞首轮通过节点。
{STAGE/'parts/final-owner-guard-verified'}：最终所有者边界保护节点。
{STAGE/'final-source'}：正式源、程序、工具和探针；source-manifest.json、source-changes.patch 给出指纹与差异。
20 项 H: 原始输入、原版 EXE/存档、旧手写引擎和 37 处失败保护均核对保留。没有提交、推送或修改原始资源。
汇总：{STAGE/'validation.json'}
效果：{STAGE/'effects.json'}
预算：{STAGE/'budget-conditions.json'}

下一步
继续 AdvanceSegment 和 CanEnterCell 剩余状态/对象扫描，审计 PrepareSegment 的共享/恢复入口。
追踪入格/世界服务期间的移动器替换，并寻找真正失败后仍保留有效目标的合法场景；不得写预算或伪造寻路失败来制造自然覆盖。
启动长目录问题保持单列；未定位之前继续使用保留证据的短目录进行对照。保留既有基线和回退，不提交或推送。
'''
    for path in (report,handoff):
        path.write_text(text,encoding='utf-8',newline='\n')
    paths = {e['path'] for e in old_manifest}
    for folder in ('ra2/src/gameplay','ra2/src/runtime'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).glob('ground_*'))
    for pattern in ('*v7*.py','*v7*.ps1'):
        paths.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern))
    for pattern in ('*.c','*.h','*.asm','*.txt'):
        paths.update(p.relative_to(ROOT).as_posix() for p in STAGE.glob(pattern))
    for pattern in ('*.MAP','*.ini'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (STAGE/'fixtures').glob(pattern))
    for name in ('effects.json','budget-conditions.json','drive-entry-references.json','trigger-layout.json'):
        paths.add((STAGE/name).relative_to(ROOT).as_posix())
    manifest,patch = [],[]
    for relative in sorted(paths):
        source = ROOT/relative
        target = STAGE/'final-source'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
        manifest.append(dict(path=relative,bytes=source.stat().st_size,sha256=sha(source)))
        if source.suffix.lower() in ('.c','.h','.py','.ps1','.txt','.ini','.map') or source.name=='CMakeLists.txt':
            before = STAGE/'baseline'/relative
            previous = before.read_text(encoding='utf-8',errors='replace').splitlines(True) if before.exists() else []
            current = source.read_text(encoding='utf-8',errors='replace').splitlines(True)
            patch.extend(difflib.unified_diff(previous,current,fromfile='v6/'+relative,tofile='v7/'+relative))
    write(STAGE/'source-manifest.json',manifest)
    (STAGE/'source-changes.patch').write_text(''.join(patch),encoding='utf-8',newline='\n')
    for path in (report,handoff):
        target = STAGE/'final-source/project'/path.relative_to(PROJECT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,target)
    validation = dict(passed=True,exe=str(ROOT/'ra2/build-original-c/ra2.exe'),exe_sha256=fingerprint,
        state_schema=9,paired_scenes=15,paired_frames=paired_frames,scenarios=results,probes=probes,
        new_native_fragment_cases=new_cases,owner_removed_native_cases=3537,source_files=len(manifest),
        effects_passed=True,preservation_passed=True,auxiliary_passed=True,
        investigation_equal_frames_with_unmet_stop_requirement=601,
        investigation_exe_sha256=read(STAGE/'runs/verified-chrono-seam-02/comparison.json')['exe_sha256'],
        investigation_comparison=str(STAGE/'runs/verified-chrono-seam-02/comparison.json'),
        full_original_equivalence_verified=False,whole_prepare_function_readable=False,
        whole_ground_movement_readable=False,normal_budget_exhaustion_verified=False,
        all_turn_results_naturally_observed=False,controlled_real_world_budget_entry_verified=True,
        long_directory_startup_compatibility_fixed=False,committed=False,pushed=False,
        report=str(report),handoff=str(handoff))
    write(STAGE/'validation.json',validation)
    pointer = read(PROJECT/'reports/latest-recovery.json')
    assert pointer['sha256']=='2e19f68cf45123d97c94460478e81edd00bfbd1ba81dc11bd2ee16548602a638'
    pointer.update(validation=str(STAGE/'validation.json'),sha256=fingerprint,report=str(report),state_schema=9,
        next_readable_region='AdvanceSegment/CanEnterCell remaining branches and PrepareSegment shared/recovery entry audit',
        previous_recovery_validation=str(OLD/'validation.json'),
        previous_recovery_executable=str(STAGE/'baseline/ra2/build-original-c/ra2.exe'),
        previous_recovery_sha256='2e19f68cf45123d97c94460478e81edd00bfbd1ba81dc11bd2ee16548602a638')
    write(PROJECT/'reports/latest-recovery.json',pointer)
    write(PROJECT/'reports/latest-state-comparison.json',dict(validation=str(STAGE/'validation.json'),
        exe_sha256=fingerprint,state_schema=9,paired_frames=paired_frames,paired_scenes=15,passed=True,
        first_difference=None,full_original_equivalence_verified=False,normal_budget_exhaustion_verified=False,report=str(report)))
    assert all(sha(ROOT/e['path'])==sha(STAGE/'final-source'/e['path'])==e['sha256'] for e in manifest)
    print('Saved verified v7:',len(manifest),'files,',paired_frames,'paired frames,',fingerprint)


if __name__=='__main__':
    main()
