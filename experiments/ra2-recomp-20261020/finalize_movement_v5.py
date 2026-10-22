"""第五批正式节点：同一程序上的逐帧、分支效果、探针和回退均核对后再更新入口。"""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT/'evidence/movement-state-v5'
OLD = ROOT/'evidence/movement-state-v4'

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
    assert fingerprint == '21bf588194a220e34a8793f3cfe2335e851656c089c34a05da2caf8dcfbf0964'
    tags = {'final-standard-01':811,'final-congestion-01':811,'final-restricted-rock':301,
        'final-restricted-clear':301,'final-wall':1001,'final-gate':701,'final-truck':301,
        'final-budget-natural':301,'final-budget-entry':101,'final-rapid-traffic':601,
        'final-rapid-obstructed':601,'final-zero-delay':601}
    results = {}
    for tag,count in tags.items():
        r = read(STAGE/'runs'/tag/'comparison.json')
        c = r['comparison']
        assert r['passed'] and r['exe_sha256']==fingerprint and c['first_difference'] is None,tag
        assert c['equal_frames']==c['frames_compared']==count and c['rng_equal_all_frames'],tag
        results[tag] = dict(passed=True,paired_frames=count,comparison=str(STAGE/'runs'/tag/'comparison.json'))
    assert read(STAGE/'final-matrix.json')['passed']
    probes = {p.name:read(p) for p in STAGE.glob('*-verified.json')}
    assert len(probes)==20 and all(p['passed'] for p in probes.values())
    effects = read(STAGE/'effects.json')
    assert effects['passed'] and effects['traffic_wait']['native_entries']>0
    assert effects['final-zero-delay']['comparison_passed'] and effects['final-zero-delay']['zero_wait_duration_observed']
    assert read(STAGE/'budget-conditions.json')['natural_exhaustion_verified'] is False
    auxiliary = read(STAGE/'auxiliary-final/validation.json')
    assert auxiliary['passed'] and auxiliary['exe_sha256']==fingerprint
    old_manifest = read(OLD/'source-manifest.json')
    for e in old_manifest:
        assert sha(OLD/'final-source'/e['path'])==e['sha256']
        assert sha(STAGE/'baseline'/e['path'])==e['sha256']
    snapshots = {}
    for name in ('wait-terrain-verified','reaction-verified'):
        directory = STAGE/'parts'/name
        m = read(directory/'manifest.json')
        assert all(sha(directory/e['path'])==e['sha256'] for e in m)
        snapshots[name] = dict(path=str(directory),files=len(m),exe_sha256=sha(directory/'ra2/build-original-c/ra2.exe'))
    inputs = []
    for e in read(ROOT/'evidence/original-inputs-before.json'):
        verified = sha(Path(r'H:\开发\运行版本\原版1.006')/e['name'])
        assert verified==e['sha256'],e['name']
        inputs.append(dict(**e,verified_sha256=verified))
    assert len(inputs)==20
    assert sha(PROJECT/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    guards = sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8')))
        for p in (ROOT/'ra2/src/recomp/gen_game').glob('*.c'))
    assert guards==37
    write(STAGE/'preservation.json',dict(passed=True,inputs=inputs,all_20_original_inputs_unchanged=True,
        previous_164_source_files_and_v4_executable_preserved=True,old_handwritten_engine_unchanged=True,
        unsupported_guards=guards,component_snapshots=snapshots))

    report_path = PROJECT/'docs/单位移动第五批-阻挡等待与预算条件-20261021.txt'
    guide = ROOT/'ra2/src/gameplay/阅读说明-单位移动.txt'
    body = guide.read_text(encoding='utf-8')
    assert '十二、第五批' not in body
    body = body.replace('第四批，障碍观察与路段准备','第五批，阻挡等待与预算条件')
    body = body.replace('接续位置：PrepareSegment 的 0x4A3550..0x4A4725','第四批留下的接续位置：PrepareSegment 的 0x4A3550..0x4A4725')
    body += '''
十二、第五批：净空、车辆等待和阻挡响应

ground_wait.h/.c：下一格覆盖物净空和高度/地形分流（4A3550..4A364F），以及车辆阻挡的双计时器（4A364F..4A36ED、4A39C8..4A3A8E）。
Ra2TrafficWaitState.retry 来自 PathDelay：原版以分钟值乘 900，再按 x87 转整数；obstruction 来自 BlockagePathDelay：直接以帧计数。
短计时器到期才重寻路，长等待到期把搜索模式 1 提升为 2。start==-1、负值及帧回绕沿用原版规则。
净空检查区分通行、可碾压覆盖物、高度差、闸门、车辆等待和其他阻挡。相同世界查询重复出现时保持原版顺序。

ground_reaction.h/.c：阻挡提示、友/敌方对象和墙体攻击、递归重试、最终停止（4A3A8E..4A3C92）。
先按通行结果分流；允许递归时清队列并重置短计时器，再以原版参数调用准备函数；禁止递归时保持原版攻击/停止行为。
查询对象会执行多次，攻击前重新读取。不要把同盟查询前后返回的对象随意缓存成一个指针。
ra2_ground_reaction_bridge 还接入 REPORT/ATTACK/FINISH 共享标签，覆盖正常函数流及这些恢复入口。

ground_terrain.h/.c：MovementRestrictedTo、斜坡子格与桥覆盖物限制（7030B6..703182）。
已从原版 70AD4E 确认 UnitType+B94 对应 MovementRestrictedTo；-1 表示没有该限制。
tile_property_2b4/2b8 的正式名称仍未确认，保留偏移名；地形 10 在原版枚举中为 Tunnel，不能只凭其外观猜测。
INI 地形枚举：Clear=0、Road=1、Water=2、Rock=3、Wall=4、Tiberium=5、Beach=6、Rough=7、Ice=8、Railroad=9、Tunnel=10、Weeds=11。

十三、第五批验证与 MOD 入口

详细报告：docs/单位移动第五批-阻挡等待与预算条件-20261021.txt。
证据目录：experiments/ra2-recomp-20261020/evidence/movement-state-v5。
修改等待策略从 ground_wait.c 阅读；修改障碍攻击和递归/停止策略从 ground_reaction.c 阅读；修改限制地形从 ground_terrain.c 阅读。
新增规则实景通过完整、独立的 RULES.INI 副本加载 PathDelay=0 和 BlockagePathDelay=0；仅把它们写进战役地图并不能保证生效，必须检查实际计时器。
规则试验由原版解析、原版对象和真实路径服务执行，两种运行模式使用相同规则；默认游戏规则没有改动。
run_fixture_comparison.py --scenario-rules 使用先写新文件再替换私有目录项，避免覆写可能存在的硬链接源文件。

预算的必要条件和带前提控制流分析见 evidence/movement-state-v5/budget-conditions.json。
标准 Drive 的普通搜索失败经 4C371A→4C4B60→49FEF0 清目标；2AC 提前拒绝目标时又会在复核处返回，所以已测场景没有扣预算。
不能把“搜索返回 false”直接等同于“必定减预算”；必须同时保留有效目标、复核通过且走到 4A2DFD。
预算耗尽的自然合法场景仍未得到；显式恢复入口覆盖 10→0 和零预算收尾只算受控实景。不能宣称全游戏分支不可达。

尚未整理：4A36ED..4A39C8 的临时/隐形障碍特殊处理，4A3C9B..4A4725 的速度、转弯和路径模板选择，路径推进和 CanEnterCell 对象扫描的剩余分支。
完整顶层 Process 已恢复，不代表整个 PrepareSegment/AdvanceSegment/CanEnterCell 都已可读化。旧生成代码继续提供尚未整理的行为。
第五批保留第四批全部正式源、程序、报告，另有 parts/wait-terrain-verified 与 parts/reaction-verified。无提交、无推送。
'''
    guide.write_text(body,encoding='utf-8',newline='\n')
    paired_frames = sum(tags.values())
    text = f'''原版 1.006 单位移动第五批：阻挡等待、碰撞地形与预算条件（2026-10-21）

本批结果
整理 ground_wait.c/.h、ground_reaction.c/.h、ground_terrain.c/.h 三组可读纯 C17 核心，原版布局和调用约定继续放在 runtime 适配层。
最终程序：{ROOT / 'ra2/build-original-c/ra2.exe'}
SHA-256：{fingerprint}
最终 12 组双路场景共 {paired_frames:,} 对帧状态一致，RNG 一致；新增原版机器码片段输入对照 983,040 组，20 项新旧探针报告全部通过。
这些结果限于列明字段、片段和场景；没有宣称整个移动模块和全游戏均已可读化或等价。

代码覆盖
ground_wait：覆盖物净空、地面高度与地形分流，车辆阻挡短重试/长等待及原版模式 1/2 的选择。
ground_reaction：阻挡提示、重新查询敌我对象、墙体攻击、一次递归准备、阻塞停止和共享入口。
ground_terrain：MovementRestrictedTo、斜坡子格、地形 Tunnel 及桥覆盖物 237/238 的原版特例。
内核没有原版地址和寄存器；未知字段保留偏移名，未猜测新的玩法含义。

逐帧与实景
固定存档移动/转向/停止 811 帧，四车拥堵 811 帧；拥堵实际进入等待分支 7 次。
指定地形 Clear、Rock 两图各 301 帧，每图真实命中对应地形碰撞 33 次。
墙体 1001 帧，坦克攻击阻挡墙后到达；闸门 701 帧，实际开闸、通行、再关闭。
卡车建墙 301 帧，第 27 帧速度位保持原版 47e17a14ae47d13f。
受控恢复入口 101 帧，10→9→…→0，再一次 0→0 停止与清理；普通失败压力图 301 帧，预算始终 10。
四车聚拢 601 帧没有触发等待，保留为未命中记录；四车加原版 CAWASH07 建筑 601 帧实际触发等待 7 次。
另以完整独立 RULES.INI 的 PathDelay/BlockagePathDelay=0 实景 601 帧验证实际零等待计时器，两种模式逐帧一致。
诊断关闭时原版/C 菜单退出正常；错误单位编号按预期失败退出 7。

自然预算的结论与未完成项
已查明必要条件：短计时器允许重建，重建失败，所有者存在，二次可达性通过，目标仍有效，未被近距离停止提前返回，随后进入失败障碍观察和 4A2DFD。
正预算每次减一；减到零与真正执行零预算停止是两次不同的失败入口。
已测三个自然失败场景均显示：当前确为 Ground Drive，重建返回 false 后目标已无效，预算 10 不变，无自然 4A2DFD 命中。
原版普通搜索失败调用 48C→4C4B60→当前 locomotor StopMoving→49FF97..49FFB0 清目标。
提前拒绝路径并不清目标，但对同一非负格和稳定区划，随后相同 2AC 仍拒绝，不能到扣预算处。
在“目标格非负、Unit/区划稳定、当前 locomotor 就是本 Drive”的前提内可解释为什么普通失败绕开预算；尚未证明所有游戏状态都不可达。
尚未找到合法玩法中满足反常组合的自然耗尽场景；locomotor 包装/替换、服务期间目标或区划变化只列为待调查方向，不能写成已证实触发条件。

保留与复现
{STAGE / 'baseline'}：第四批 164 项源和正式程序、报告入口。
{STAGE / 'parts'}：净空/等待/地形、阻挡响应两个验证节点。
{STAGE / 'final-source'}：本批正式源、工具、探针、试验地图/规则；source-manifest.json 对应指纹，source-changes.patch 对应差异。
20 项 H: 原始输入、旧手写引擎、第四批已发布源和 37 处失败保护均核验保留。没有提交或推送。
汇总：{STAGE / 'validation.json'}
效果断言：{STAGE / 'effects.json'}
预算条件：{STAGE / 'budget-conditions.json'}

接续位置
优先整理 4A36ED..4A39C8 的临时/隐形阻挡；再整理 4A3C9B..4A4725 速度与模板选择。
随后继续 AdvanceSegment 其余状态，以及 CanEnterCell 的方向/特殊建筑/对象链表碰撞。
自然预算耗尽继续保持未验证；不要改写预算、禁用停止或伪造搜索结果来制造自然验收。
'''
    report_path.write_text(text,encoding='utf-8',newline='\n')
    handoff_path = PROJECT/'交接文档-单位移动第五批-20261021.txt'
    handoff_path.write_text(text,encoding='utf-8',newline='\n')

    paths = {e['path'] for e in old_manifest}
    for folder in ('ra2/src/gameplay','ra2/src/runtime'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).glob('ground_*'))
    for pattern in ('*v5*.py','*v5*.ps1'):
        paths.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern))
    paths.update(p.relative_to(ROOT).as_posix() for p in STAGE.glob('*.c'))
    paths.update(p.relative_to(ROOT).as_posix() for p in STAGE.glob('*.h'))
    paths.update(p.relative_to(ROOT).as_posix() for p in (STAGE/'fixtures').glob('*.MAP'))
    paths.update(p.relative_to(ROOT).as_posix() for p in (STAGE/'fixtures').glob('*.ini'))
    manifest = []
    patch = []
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
            patch.extend(difflib.unified_diff(before,after,fromfile='v4/'+relative,tofile='v5/'+relative))
    write(STAGE/'source-manifest.json',manifest)
    (STAGE/'source-changes.patch').write_text(''.join(patch),encoding='utf-8',newline='\n')
    validation = dict(passed=True,exe=str(ROOT/'ra2/build-original-c/ra2.exe'),exe_sha256=fingerprint,
        state_schema=7,paired_scenes=len(tags),paired_frames=paired_frames,scenarios=results,
        probes=probes,new_native_fragment_cases=983040,effects_passed=True,preservation_passed=True,
        auxiliary_passed=True,source_files=len(manifest),full_original_equivalence_verified=False,
        whole_prepare_function_readable=False,whole_ground_movement_readable=False,
        normal_budget_exhaustion_verified=False,controlled_real_world_budget_entry_verified=True,
        committed=False,pushed=False,report=str(report_path))
    write(STAGE/'validation.json',validation)
    pointer = read(PROJECT/'reports/latest-recovery.json')
    pointer.update(validation=str(STAGE/'validation.json'),sha256=fingerprint,report=str(report_path),
        next_readable_region='0x4A36ED..0x4A39C8 and 0x4A3C9B..0x4A4725',
        previous_recovery_validation=str(OLD/'validation.json'),
        previous_recovery_executable=str(STAGE/'baseline/ra2/build-original-c/ra2.exe'),
        previous_recovery_sha256='a91b434a273fe2e621b6fdfa500e6eecd0f4c33f1c7cc41e2f48e7e3a1f7ce0d')
    write(PROJECT/'reports/latest-recovery.json',pointer)
    write(PROJECT/'reports/latest-state-comparison.json',dict(validation=str(STAGE/'validation.json'),
        exe_sha256=fingerprint,state_schema=7,paired_frames=paired_frames,paired_scenes=len(tags),
        passed=True,first_difference=None,full_original_equivalence_verified=False,
        normal_budget_exhaustion_verified=False,report=str(report_path)))
    assert all(sha(ROOT/e['path'])==sha(STAGE/'final-source'/e['path'])==e['sha256'] for e in manifest)
    print('Published verified v5:',len(manifest),'files,',paired_frames,'paired frames,',fingerprint)

if __name__=='__main__':
    main()
