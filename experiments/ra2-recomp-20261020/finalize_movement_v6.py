"""核验当前程序、逐帧实景、片段对照和回退后，保存第六批正式节点。"""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT/'evidence/movement-state-v6'
OLD = ROOT/'evidence/movement-state-v5'
EXPECTED = '2e19f68cf45123d97c94460478e81edd00bfbd1ba81dc11bd2ee16548602a638'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def verify_comparison(tag, count, fingerprint):
    r = read(STAGE/'runs'/tag/'comparison.json')
    c = r['comparison']
    assert r['passed'] and r['exe_sha256']==fingerprint, tag
    assert c['equal_frames']==c['frames_compared']==c['consecutive_equal_frames']==count, tag
    assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames'], tag
    assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected'], tag
    assert all(run['passed'] and run['exit_code']==0 and run['save_is_private_copy']
               and run['save_before_sha256']==run['save_after_sha256'] for run in r['runs']), tag
    for mode in ('original','generated-c'):
        with (STAGE/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8') as stream:
            assert json.loads(next(stream))['schema']==8, tag
    return dict(passed=True, paired_frames=count, comparison=str(STAGE/'runs'/tag/'comparison.json'))


def main():
    assert not (STAGE/'validation.json').exists()
    fingerprint = sha(ROOT/'ra2/build-original-c/ra2.exe')
    assert fingerprint==EXPECTED
    matrix = read(STAGE/'schema8-matrix.json')
    assert matrix['passed'] and matrix['exe_sha256']==fingerprint
    tags = {r['tag']:r['frames'] for r in matrix['results']}
    assert len(tags)==10 and sum(tags.values())==5230
    tags['final-zero-delay'] = 601
    results = {tag:verify_comparison(tag,count,fingerprint) for tag,count in tags.items()}
    # 两次地图加载/触发器调查没有产生援军；单列记录，不冒充预算或援军覆盖。
    investigation = {tag:dict(**verify_comparison(tag,601,fingerprint),
        reinforcement_spawn_verified=False) for tag in ('final-chrono-team-02','final-chrono-team-03')}
    probes = {p.name:read(p) for p in STAGE.glob('*-verified-02.json')}
    assert len(probes)==26 and all(p['passed'] for p in probes.values())
    new_probes = {name:value for name,value in probes.items() if name.startswith(('special_probe-','template_probe-'))}
    new_cases = sum(p.get('special_cases',0)+p.get('template_cases',0) for p in new_probes.values())
    assert len(new_probes)==6 and new_cases==393216
    assert all(p['state_calls_abi_cw_verified'] and p['live_stack_locals_verified'] for p in new_probes.values())
    effects = read(STAGE/'effects.json')
    assert effects['passed'] and effects['temporary_obstacle']['primary_special_branch_really_entered']
    assert effects['cloaked_obstacle']['real_world_cloak_and_reveal_verified']
    assert effects['zero_delay']['zero_duration_really_observed']
    assert read(STAGE/'budget-conditions.json')['natural_exhaustion_verified'] is False
    auxiliary = read(STAGE/'auxiliary-final/validation.json')
    assert auxiliary['passed'] and auxiliary['exe_sha256']==fingerprint

    old_manifest = read(OLD/'source-manifest.json')
    assert len(old_manifest)==217
    for e in old_manifest:
        assert sha(OLD/'final-source'/e['path'])==e['sha256'], e['path']
        assert sha(STAGE/'baseline'/e['path'])==e['sha256'], e['path']
    snapshots = {}
    for name in ('special-template-verified','special-template-schema8-verified'):
        directory = STAGE/'parts'/name
        manifest = read(directory/'manifest.json')
        assert all(sha(directory/e['path'])==e['sha256'] for e in manifest)
        snapshots[name] = dict(path=str(directory), files=len(manifest),
            exe_sha256=sha(directory/'ra2/build-original-c/ra2.exe'))
    inputs = []
    for e in read(ROOT/'evidence/original-inputs-before.json'):
        verified = sha(Path(r'H:\开发\运行版本\原版1.006')/e['name'])
        assert verified==e['sha256'], e['name']
        inputs.append(dict(**e, verified_sha256=verified))
    assert len(inputs)==20
    assert sha(PROJECT/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    assert sha(ROOT/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
    assert sha(ROOT/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
    guards = sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8')))
        for p in (ROOT/'ra2/src/recomp/gen_game').glob('*.c'))
    assert guards==37
    write(STAGE/'preservation.json',dict(passed=True, inputs=inputs, all_20_original_inputs_unchanged=True,
        previous_217_source_files_and_v5_executable_preserved=True, old_handwritten_engine_unchanged=True,
        input_game_exe_and_save_unchanged=True, unsupported_guards=guards, component_snapshots=snapshots))

    guide = ROOT/'ra2/src/gameplay/阅读说明-单位移动.txt'
    body = guide.read_text(encoding='utf-8')
    assert '十四、第六批' not in body
    body = body.replace('单位移动的可读 C：第五批，阻挡等待与预算条件',
        '单位移动的可读 C：第六批，临时/隐形障碍与路径模板状态')
    body = body.replace('尚未整理：4A36ED..4A39C8', '第五批结束时尚未整理：4A36ED..4A39C8')
    body += '''
十四、第六批：临时/隐形障碍与路径模板状态

ground_special.h/.c / ra2_ground_handle_special_obstacle：4A36ED..4A39C8。
通行结果 TemporaryObstacle=6：火车转共享清理；允许递归时重置短计时器并再准备一次；禁止递归时按距离、高度和 Tunnel 地形决定停止或通知单元格。
通行结果 CloakedObstacle=1：先揭露格内隐形对象；递归重试不重置短计时器。停止前按目标类型决定取消目标及 StopTarget/StopEmpty。
停止服务可能改变路段，因此保留共享清理的第二次检查。原版已无效路段不会无条件清 driving。
修改这两种障碍策略从此文件开始；数值近似、世界通知和调用参数由 runtime/ground_prepare_bridge.c 保持。
special_distance 使用原版近似开方表与浮点控制字；必须保持本分支 z²+y²+x² 的求和顺序。

ground_template.h/.c / ra2_ground_choose_template：4A3F8B..4A4015，包含 4A3F9F 和 4A3FA1 共享入口。
先处理相邻方向、屏蔽转弯和可碾压覆盖物，再算 selector=下一方向+当前方向*8。
表项首字节为 0 时回退到 当前方向*9；表的 flags & 8 继续进入尚未整理的转弯部分。
共享入口的方向已经部分归一化，不能再次执行主入口的全部规则。路径表原始数据仍由只读服务提供。

ra2_ground_commit_segment：4A45B7..4A4725，包含不重复移队列的 4A45D0 入口。
更新 24 项方向队列、单位目标格、路段索引和提示标志，再发布候选路段并询问原版格服务。
成功后启动路段；拒绝后按存活标志清理，并将选择器/队列头恢复终止值、速度置零。
共享入口必须保留传入终止值；只有常规入口固定使用 -1。服务前后同步状态，以保留回调对单位/Drive 的修改。

十五、第六批验证、预算调查与下一步

正式证据 evidence/movement-state-v6/validation.json：11 组有效场景，5,831 对帧，完整 RNG、对象状态及有序分支记录一致。
原版临时障碍入口实景命中 1 次；隐形走廊在第 197 帧揭露。后者使用原版 INI 的 Cloakable 能力试验，不能宣称默认卡车自带隐形。
新增 6 个片段入口共 393,216 组输入对照，检查对象/Drive、世界调用顺序、AL、栈局部、调用约定和浮点控制字；26 项新旧探针全过。
state schema 8 新增单位当前 locomotor vtable 和 cloak_state；stage 6 同时记录 active_is_caller/caller_goal_valid，stage 15 只在调用者 Drive 并非当前移动器时记录。
固定存档矿车真实切换 Teleport/Drive；已测包装期没有旧 Drive Prepare 命中。不能仅凭存在包装，就推导预算可以自然耗尽。
四个自然失败场景均在重建返回 false 后清空调用者目标、预算仍为 10。显式恢复入口的 10→0 与零预算停止仍仅是受控验收。
超时空援军地图第一次因键名大小写丢失 TaskForce 而在两种模式同时失败；修正后两次各 601 帧相等，但未产生援军，单列调查记录，不计入上述覆盖。
预算自然耗尽的合法触发条件仍待追踪；不能通过改预算、绕过停止、伪造失败来宣称自然触发。

下一步：4A3C9B..4A3F8B 的速度与第二次路径准备；4A4015..4A45B7 的转弯模板和后续碰撞，再继续 AdvanceSegment/CanEnterCell 剩余分支。
这些剩余部分继续使用生成 C，整个 PrepareSegment/AdvanceSegment/CanEnterCell 和全游戏等价尚未完成。
第五批 217 项正式源及程序、两份第六批已验证节点、所有失败试验均保留；没有提交或推送。
'''
    guide.write_text(body, encoding='utf-8', newline='\n')
    report = PROJECT/'docs/单位移动第六批-临时隐形障碍与路径模板-20261021.txt'
    handoff = PROJECT/'交接文档-单位移动第六批-20261021.txt'
    paired_frames = sum(tags.values())
    text = f'''原版 1.006 单位移动第六批：临时/隐形障碍和路径模板状态（2026-10-21）

本批完成
增加 ground_special.c/.h 与 ground_template.c/.h 两组可读纯 C17 核心，原版内存布局、寄存器和世界调用仍在 runtime 适配层。
最终程序：{ROOT/'ra2/build-original-c/ra2.exe'}
SHA-256：{fingerprint}
11 组正式实景共 {paired_frames:,} 对帧全部一致，完整 RNG 与有序命令/分支记录一致。新增 6 个入口共 393,216 组原版机器码片段对照，26 项新旧探针全部通过。
范围限于本批列出的代码、状态字段和场景。整个移动模块可读化与全游戏等价均尚未完成。

可读代码与 MOD 阅读入口
ground_special：临时障碍的火车例外、计时器重置/递归、距离/高度/Tunnel 分流、单元格通知；隐形障碍的揭露、保留计时器重试、停止。
ground_template：方向归一化、碾压强制直行、模板首字节回退、标志分流；路段候选发布、24 项方向队列推进、启动与失败清理。
覆盖 4A36ED..4A39C8、4A3F8B..4A4015、4A45B7..4A4725，并接入 3F9F/3FA1/45D0 共享入口。
模板数据和未知标志保留原版含义；没有以推测名称替换尚未查明的字段。修改障碍策略先读 ground_special，修改方向/路段提交先读 ground_template。
阅读说明：{guide}

验证与实际命中
固定存档移动/转向/停止 811 帧，四车拥堵 811 帧；实际临时障碍分支 1 次、等待 7 次。
Clear/Rock 两个限制地形场景各 301 帧；墙体 1001 帧，实际攻击墙并到达；闸门 701 帧，实际开闸、通过、关闭。
卡车运行中建墙 301 帧，第 27 帧速度位仍为原版 47e17a14ae47d13f。
自然失败压力 301 帧；受控预算恢复入口 101 帧，10→9→…→0，另一次零预算停止。两者分开记录。
隐形走廊 601 帧：敌方 TRUCKA 通过原版地图 INI 获得 Cloakable，第 197 帧触发揭露，隐形状态 2→3→0 和全部移动状态一致。此为 MOD 能力实景，不是默认卡车能力。
完整独立 RULES.INI 的零等待场景 601 帧，真实等待时长为 0；原始规则文件未改。
模板实景：标准场景选择/提交各 13 次，拥堵选择 24/提交 23 次，隐形场景各 3 次。每个候选发布都有对应分支记录参与比较。
探针验证状态、世界调用及顺序、返回 AL、ABI、活跃栈局部和浮点控制字；新模块均以 /W4 /WX /std:c17 编译。
诊断关闭时原版/C 菜单退出正常；错误单位编号按预期退出 7。比较器的坐标 +1 和缺帧反例均检测成功。

预算自然触发条件的推进
新增精确身份记录，比较当前 locomotor 是否就是正在执行的 Drive，而不只是比较 vtable 类型。
四个真实失败场景均显示 active_is_caller=true、caller_goal_valid=false，失败后目标已清空，预算 10 不变；没有自然扣预算入口。
原版路径失败经 Unit StopMoving 清当前移动器目标的调用链仍成立。包装是需要进一步调查的例外方向，但必须先证明包装期间旧 Drive 仍执行 Prepare。
本机原版 RTTI/GUID 确认 Teleport 接口 7AD1A8、IPiggyback 7AD184、Begin 6E1960、End 6E19B0、包装指针 base+48；未套用尤复地址。
固定存档矿车 1032341 实际进入 Teleport：标准场景 388 帧、拥堵场景 387 帧；均多次恢复 Drive。两个场景均没有当前移动器不同却执行旧 Drive Prepare 的记录。
Teleport Process 主体静态未见直接调用 Drive Process/Prepare，也未见读取包装指针；这不是对所有辅助函数和回调的不可达证明。
援军触发器首个地图因小写 TaskForce 键导致原版/C 同时在 6C01A6 失败，保留失败记录。修正大小写后的两次 601 帧对照均通过，但没有产生援军，不计为援军覆盖；后续仍需核对触发器激活/动作参数。
自然预算耗尽仍未验证，不能写成已经找到合法触发条件或已证整个分支不可达。
详细条件与逐次失败证据：{STAGE/'budget-conditions.json'}

保留和回退
{STAGE/'baseline'}：第五批 217 项正式源及程序、旧报告入口，已重新核对 SHA-256。
{STAGE/'parts/special-template-verified'}：共享入口补全后的 schema 7 节点。
{STAGE/'parts/special-template-schema8-verified'}：包含精确身份/隐形观测的当前节点。
{STAGE/'final-source'}：本批源、程序、工具、探针和试验地图；source-manifest.json 给出指纹，source-changes.patch 以第五批为基准。
20 项 H: 原始输入、原版 EXE/存档、旧手写引擎及 37 处未实现保护均核对保持。所有中间失败记录均保留。无提交、无推送。
汇总：{STAGE/'validation.json'}
效果断言：{STAGE/'effects.json'}
回退核验：{STAGE/'preservation.json'}

待续
优先 4A3C9B..4A3F8B 速度与第二路径准备、4A4015..4A45B7 转弯模板与后续碰撞，再继续路径推进和 CanEnterCell 对象扫描。
继续调查包装/替换瞬间、间接服务及区划变化是否能合法保留目标而返回失败。显式预算入口只用于回归，不作为自然触发证据。
暂时不要提交或推送。不要覆盖基线、旧报告或 H: 原始资源。
'''
    assert not report.exists() and not handoff.exists()
    for target in (report,handoff):
        target.write_text(text, encoding='utf-8', newline='\n')

    paths = {e['path'] for e in old_manifest}
    for folder in ('ra2/src/gameplay','ra2/src/runtime'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).glob('ground_*'))
    for pattern in ('*v6*.py','*v6*.ps1'):
        paths.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern))
    for pattern in ('*.c','*.h','*.asm'):
        paths.update(p.relative_to(ROOT).as_posix() for p in STAGE.glob(pattern))
    for pattern in ('*.MAP','*.ini'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (STAGE/'fixtures').glob(pattern))
    for name in ('locomotor-layout.json','budget-conditions.json','effects.json'):
        paths.add((STAGE/name).relative_to(ROOT).as_posix())
    manifest,patch = [],[]
    for relative in sorted(paths):
        source = ROOT/relative
        assert source.resolve().is_relative_to(ROOT.resolve())
        target = STAGE/'final-source'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
        manifest.append(dict(path=relative,bytes=source.stat().st_size,sha256=sha(source)))
        if source.suffix.lower() in ('.c','.h','.py','.ps1','.txt','.ini','.map') or source.name=='CMakeLists.txt':
            previous = STAGE/'baseline'/relative
            before = previous.read_text(encoding='utf-8',errors='replace').splitlines(True) if previous.exists() else []
            after = source.read_text(encoding='utf-8',errors='replace').splitlines(True)
            patch.extend(difflib.unified_diff(before,after,fromfile='v5/'+relative,tofile='v6/'+relative))
    write(STAGE/'source-manifest.json',manifest)
    (STAGE/'source-changes.patch').write_text(''.join(patch),encoding='utf-8',newline='\n')
    # 项目报告额外保存一份；不让实验目录之外的路径进入可执行源清单。
    for source in (report,handoff):
        target = STAGE/'final-source/project'/source.relative_to(PROJECT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
    validation = dict(passed=True,exe=str(ROOT/'ra2/build-original-c/ra2.exe'),exe_sha256=fingerprint,
        state_schema=8,paired_scenes=len(tags),paired_frames=paired_frames,scenarios=results,
        additional_investigation_scenes=investigation,additional_investigation_frames=1202,
        probes=probes,new_native_fragment_cases=new_cases,effects_passed=True,preservation_passed=True,
        auxiliary_passed=True,source_files=len(manifest),full_original_equivalence_verified=False,
        whole_prepare_function_readable=False,whole_ground_movement_readable=False,
        normal_budget_exhaustion_verified=False,controlled_real_world_budget_entry_verified=True,
        committed=False,pushed=False,report=str(report),handoff=str(handoff))
    write(STAGE/'validation.json',validation)
    pointer = read(PROJECT/'reports/latest-recovery.json')
    assert pointer['sha256']=='21bf588194a220e34a8793f3cfe2335e851656c089c34a05da2caf8dcfbf0964'
    pointer.update(validation=str(STAGE/'validation.json'),sha256=fingerprint,report=str(report),state_schema=8,
        temporary_obstacle_scene_verified=True,cloaked_obstacle_scene_verified=True,
        next_readable_region='0x4A3C9B..0x4A3F8B and 0x4A4015..0x4A45B7',
        previous_recovery_validation=str(OLD/'validation.json'),
        previous_recovery_executable=str(STAGE/'baseline/ra2/build-original-c/ra2.exe'),
        previous_recovery_sha256='21bf588194a220e34a8793f3cfe2335e851656c089c34a05da2caf8dcfbf0964')
    write(PROJECT/'reports/latest-recovery.json',pointer)
    write(PROJECT/'reports/latest-state-comparison.json',dict(validation=str(STAGE/'validation.json'),
        exe_sha256=fingerprint,state_schema=8,paired_frames=paired_frames,paired_scenes=len(tags),
        passed=True,first_difference=None,full_original_equivalence_verified=False,
        normal_budget_exhaustion_verified=False,report=str(report)))
    assert all(sha(ROOT/e['path'])==sha(STAGE/'final-source'/e['path'])==e['sha256'] for e in manifest)
    assert sha(ROOT/'ra2/build-original-c/ra2.exe')==fingerprint
    print('Saved verified v6:',len(manifest),'files,',paired_frames,'paired frames,',fingerprint)


if __name__=='__main__':
    main()
