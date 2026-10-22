"""保存第十批候选与严格验收缺口，保留第九批正式入口和可执行基线。"""
from pathlib import Path
import difflib
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parent; PROJECT=ROOT.parent.parent
S=ROOT/'evidence/movement-state-v10'; OLD=ROOT/'evidence/movement-state-v9'
FORMAL='734138bb0a3b1638745a3e61adb9f59953e3e48ddca2129d1a4ef585407b0bfa'
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
    boundary=read(S/'acceptance-boundary.json')
    assert not boundary['passed'] and boundary['frame_comparison_passed'] and boundary['refactor_checks_passed']
    effects,budget=read(S/'effects.json'),read(S/'budget-conditions.json')
    assert effects['passed'] and not budget['natural_exhaustion_verified']
    exe=ROOT/'ra2/build-original-c/ra2.exe'; fingerprint=sha(exe)
    matrices=[read(S/'m-matrix.json'),read(S/'m-additional-matrix.json')]
    assert all(m['exe_sha256']==fingerprint for m in matrices)
    cases=[r for m in matrices for r in m['results']]
    assert len(cases)==27 and sum(r['frames'] for r in cases)==14897
    for row in cases:
        p=S/'runs'/row['tag']; report=read(p/'comparison.json'); c=report['comparison']
        assert report['exe_sha256']==fingerprint and report['seed']==12345
        assert c['equal_frames']==c['consecutive_equal_frames']==c['frames_compared']==row['frames']
        assert c['rng_equal_all_frames'] and c['first_difference'] is None
        assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
        for run in report['runs']:
            assert run['passed'] and run['exit_code']==0 and run['save_is_private_copy']
            assert run['save_before_sha256']==run['save_after_sha256']
        for mode in ('original','generated-c'):
            with (p/mode/'state.jsonl').open(encoding='utf-8') as f: assert json.loads(next(f))['schema']==12
    probes={p.name:read(p) for p in S.glob('*-verified-02.json')}
    assert len(probes)==39 and all(p['passed'] for p in probes.values())
    assert probes['allied_probe-verified-02.json']['allied_cases']==65536
    assert probes['tail_probe-verified-02.json']['terrain_tail_cases']==65536
    assert probes['round_probe-verified-02.json']['round_cases']==131072
    aux=read(S/'auxiliary-final-03/validation.json')
    assert aux['passed'] and aux['exe_sha256']==fingerprint
    previous=read(OLD/'source-manifest.json'); assert len(previous)==536
    for e in previous:
        assert sha(OLD/'final-source'/e['path'])==e['sha256'],e['path']
        assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
    assert sha(S/'baseline/ra2/build-original-c/ra2.exe')==FORMAL
    for rel in ('reports/latest-recovery.json','reports/latest-state-comparison.json'):
        assert (PROJECT/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes()
    assert read(PROJECT/'reports/latest-recovery.json')['sha256']==FORMAL
    snapshots={}
    for name in ('allied-collision-verified','terrain-tail-verified'):
        p=S/'parts'/name; m=read(p/'manifest.json'); assert len(m)==540
        assert all(sha(p/e['path'])==e['sha256'] for e in m)
        snapshots[name]=dict(path=str(p),files=len(m),validation=read(p/'validation-source.json'))
    inputs=[]
    for e in read(ROOT/'evidence/original-inputs-before.json'):
        actual=sha(Path(r'H:\开发\运行版本\原版1.006')/e['name']); assert actual==e['sha256']
        inputs.append(dict(**e,verified_sha256=actual))
    assert len(inputs)==20
    assert sha(ROOT/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
    assert sha(ROOT/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
    assert sha(PROJECT/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8')))
        for p in (ROOT/'ra2/src/recomp/gen_game').glob('*.c'))
    assert guards==37
    report=PROJECT/'docs/单位移动第十批-友方碰撞与地形尾部-候选-20261021.txt'
    handoff=PROJECT/'交接文档-单位移动第十批-20261021.txt'
    assert not report.exists() and not handoff.exists()
    candidate=S/'candidate/ra2.exe'; candidate.parent.mkdir(exist_ok=True); shutil.copy2(exe,candidate)
    assert sha(candidate)==fingerprint
    guide=ROOT/'ra2/src/gameplay/阅读说明-单位移动.txt'
    t=guide.read_text(encoding='utf-8'); assert '二十六、第十批' not in t
    t=t.replace('单位移动的可读 C：第九批，转弯接续与对象碰撞',
        '单位移动的可读 C：第十批候选，移动友方碰撞与地形尾部',1)
    t+='''
二十六、第十批：移动友方对象怎样决定是否让路

ground_allied.h/.c / ra2_ground_classify_allied_motion：703693..70394F。
先保留两次任务查询与目的对象/目标对象特例，再判断对象是否具有移动状态。
目的地存在、正在转向、移动器 IsMoving 任一成立时，按移动对象处理；敌方及静止友方交回第九批的独立分类。
移动友方先量化双方朝向，算出物体相反方向及相对位置方向；方向不同也照原版计算相对方向。
只有双方迎向、原版距离结果不大于 511、相对方向也符合时才硬阻挡；其余再查询 5A0 标志和移动器通行请求，必要时提升为分类 2。
未知 5A0 标志保留偏移名，不能直接称为某个 INI 配置；15 号对象仍须重新查询移动器。
原版地图 y 轴与角度函数 y 轴相反。距离沿用原版近似数学服务，不直接换成宿主 sqrt/atan2。
适配层 ground_allied_bridge.c 负责旧字段/服务及数值表示，玩法核心只表达命名状态和判断顺序。
方向整数转换前不提前落成 double；compat/x87_arithmetic.c 的 ra2_real_round_i32 按原版 RC 取整数低 32 位。
该函数用于有限、范围受约束的坐标/方向值，不是所有 IEEE 非有限数与 64 位溢出的通用转换器。

二十七、第十批：对象扫描之后的地形尾部

ground_terrain.c / ra2_ground_terrain_speed_is_blocked：703905..70394F。
上层占用跳过地面速度表限制；地面层按实际地形及速度类别读取速度系数。
正负零导致硬阻挡，其它有限非零系数交回既有 ground_collision.c 的占格收尾。
原版 fcomp 的无序标志也会走零值分支；NaN 只在片段边界测试中使用，合法实景使用有限非负规则。
rules-zero-road.ini 对原图实际使用的 Road/Rough 的 Wheel 系数设零，原版和候选读取同一独立规则文件。
早期只改 Clear 的试验没有覆盖地图实际地形，保留为调查记录，不当作零速度分支命中证明。

二十八、第十批验证边界：候选与正式基线分开

候选已记录状态、RNG、外部命令在 27 场景共 14897 帧相等；39 组片段/数值回归通过，新增 262144 组输入。
两个部分有独立回退：友方碰撞通过固定存档 811 帧和拥堵 601 帧；地形尾部通过真实零速度规则 301 帧。
三格包围第 52 帧，候选多出两条地形观测（同一 69,113 格）；原版和候选 351 帧状态/RNG 一致，但严格有序观测比较失败。
同时切回第九批的两段原流程、只保留只读观测后，101 帧控制仍重现完全相同的两条差异。
差异来自路径搜索评分调用；单改评分舍入未解决，试验已撤出工作源。路径评分生成文件 recomp_0003.c 已恢复为本批试验前保存的原内容。
严格比较器未放宽，m-ur3/comparison.json 仍为 false。整批 validation.json 的 passed 也为 false。
第九批正式入口及默认程序已保留；第十批编译候选单独存于 evidence/movement-state-v10/candidate/ra2.exe。
当前工作源是第十批候选，重新构建会生成候选程序；继续前先读第十批交接，不能把第九批正式程序的指纹当成候选指纹。

二十九、第十批预算调查

长路线二次补建失败第 399 帧之后，在 450..1110 每隔 60 帧发一次合法移动命令，共 12 次。
12 次主重建分别在 451..1111 失败，同一 Drive 的目标每次都清空，预算全程为 10，没有进入预算扣减入口。
原版与候选在该实景 1251 帧的状态、命令、有序观测一致；这仍不等同预算自然耗尽。
继续寻找目标保留且可达性复核通过的合法回调/移动器替换场景；不要主动改预算或保留目标制造命中。
不同类虚表的同一偏移不能不加核实地都叫 Stop；Infantry 的已核实停止函数仍调用 Foot.Stop。
全部未通过调查、基线、两个回退和接续位置见第十批交接文档。
'''
    guide.write_text(t,encoding='utf-8',newline='\n')
    e=effects['allied_motion']; terrain=effects['terrain_tail']
    text=f'''原版 1.006 单位移动第十批：移动友方碰撞与地形尾部（候选，2026-10-21）

当前结论

已整理两部分纯 C17，并完成片段和实景对照。27 场景、14897 帧的已记录对象状态、RNG、外部命令相等。
三格包围仍有一项已确认在整理前存在的内部查询次数差异；严格门槛未通过，因此没有升级第九批正式入口。
整批 passed=false；refactor_checks_passed=true；frame_comparison_passed=true；strict_ordered_audit_passed=false。
预算自然耗尽仍未验证。没有提交、推送、重置或清理旧证据。

程序与代码

候选程序：{candidate}
候选 SHA-256：{fingerprint}
正式默认程序：{exe}，已回退至第九批 SHA-256 {FORMAL}。
工作源仍是第十批候选；构建它会覆盖默认程序为候选。需要恢复正式源时使用本批 baseline 或第九批 final-source。
阅读入口：{guide}
ground_allied.h/.c：703693..70394F，任务特例、移动状态、敌我分流、迎面方向/距离及移动通行请求。
ground_allied_bridge.c：旧布局和虚调用；原版 y 轴符号、x*x+z*z+y*y 次序、原版近似角度/距离服务与整数转换。
ground_terrain.c 新函数：703905..70394F，上层占用跳过速度表，地面零速度阻挡，随后复用已有占格收尾。
compat/x87_arithmetic.c 新增受限有限值 RC 整数转换，避免扩展精度方向值提前存 double 的边界变化。
新增核心和适配层按 /W4 /WX /std:c17 /utf-8 编译；未确认标志保守命名。

对照证据

最终候选 schema 12、seed 12345。固定 SAVE0029.SAV 2190..3000 窗口含第 2247 帧，继续逐帧相等。
原 25 场景 13345 帧全部重跑，增加重复失败命令 1251 帧与实际零速度地形 301 帧，共 27 场景 14897 帧。
26 场景严格比较 passed=true；m-ur3 的 351 帧状态/RNG 仍相等，但多两条内部地形查询观测，严格 passed=false。
外部发令、执行、实景对象创建记录逐条相等；原比较器的位移差异/缺帧反例仍拒绝，未修改比较器。
39 组最终片段/数值回归通过。新增友方碰撞 65536、地形尾部 65536、原版 __ftol 多控制字 131072，共 262144 组输入。
友方片段使用映射原版实际数学服务验证调用者，不以宿主 sqrt/atan2 代替原版近似表。
实景友方分流入口 {e['total_entries']} 次，移动友方几何入口 {e['total_geometry_entries']} 次；入口次数不代表所有分支均自然命中。
地形尾部入口 {terrain['total_entries']} 次，原版地面零速度命中 {terrain['zero_speed_entries']} 次。NaN 测试仅为片段边界，不作合法实景证明。
附加启动/保护检查：{S/'auxiliary-final-03/validation.json'}。

既有差异及未接受的试验

m-ur3 第 52 帧，C 比原版多两次 69,113 格地形入口；系数同为 1，最后路径及全部已记录状态仍相等。
n-control 在同时绕过新友方/地形模块后重现相同两条差异；两路各自的观测流与候选首轮逐项一致（除后来增加的地形元数据）。
查询来源：原版评分调用返回 427837；C 的评分调用父函数为 427370。此格区划查询次数两路均 18，评分查询为 2/4。
单改评分乘加、或 16 处单精度保存均未解决严格差异，已撤出工作源；recomp_0003.c 已恢复为本批评分试验前保存的原内容。
该评分文件不在第九批 536 项已修改文件清单内；额外原件和指纹单列 extended-baseline.json，不虚构旧清单覆盖。
未证明数值舍入就是根因，不能把调查方向当成已解决。Native 查询期间实测 CW 为 E7F；帧边界 CW 不能代替查询现场证据。
早期友方片段发现 double 提前舍入和 y 轴符号错误，修正后通过；失败日志 allied-probe-01/02.json 保留。
Clear-only、Track-only 规则试验没有覆盖图中实际地形/速度组合，不列零速度覆盖；最终针对实际 Road/Rough、Wheel 类规则命中。
诊断构建、源码、失败轨迹和未接受的评分试验保留在本批 evidence 下，不能当作发布程序。

失败预算合法条件

m-repeat-failure 在第 398 帧围入 16 辆真实卡车，第 399 帧正常二次补建失败。
随后 450..1110 每隔 60 帧合法发 Move，共 12 次；主重建在 451..1111 每次失败，均为同一 Drive、目标已清空。
实景 1251 帧的状态、命令、有序观测全部一致；预算值只有 10，没有 stage 3 扣减或耗尽。
不写目标/队列/预算、不额外主动寻路；普通重复命令不能作为自然耗尽证明。
Infantry 虚表 7A3540 的停止槽 504AE0 两条尾路仍调用 Foot.Stop 4C4B60；不同地址不等于绕过目标清理。
非 Foot 对象同偏移不能当成同一虚函数；aircraft-stop.asm 是早期错误命名的类槽调查，不是已确认的飞机停止证据。
继续寻找合法回调/移动器替换时保留旧 Drive 目标且通过可达性复核的情形；没有证明全游戏预算分支不可达。

保全与回退

第九批 536 项正式文件与 {OLD/'final-source'}、{S/'baseline'} 逐项核对。
友方碰撞验证回退（固定存档 811 帧及拥堵 601 帧）：{S/'parts/allied-collision-verified'}。
地形尾部验证回退（实际零速度 301 帧）：{S/'parts/terrain-tail-verified'}。
最终候选源、工具、程序：{S/'final-source'}；清单 source-manifest.json，差异 source-changes.patch。
20 项 H: 原始输入、game.exe、SAVE0029.SAV、旧手写引擎、37 处未支持保护均保持原指纹。
正式 reports/latest-recovery.json 和 latest-state-comparison.json 保持第九批，不改写其通过结论。
候选入口单独为 reports/latest-movement-candidate.json，passed=false。
汇总：{S/'validation.json'}；边界：{S/'acceptance-boundary.json'}；效果：{S/'effects.json'}；预算：{S/'budget-conditions.json'}。

接续工作（先读这里，避免误用第九批正式指针重做）

1. 当前可读源是本批候选，默认 EXE 是第九批正式程序；从 candidate/ra2.exe 或 final-source 继续试验，构建前记录候选身份。
2. 优先解决路径评分在三格包围第 52 帧的两次额外空格查询；先以 n-control 对照确认新改动不造成回归，不能放宽有序比较器。
3. 评分单点舍入试验未解决；继续比较评分输入、局部缓存/优先队列和实际查询返回，不先假定根因。
4. 严格问题解决后重跑本批 27 场景、39 组片段及保护检查，再考虑升级正式指针。
5. 继续原版合法预算目标保留条件调查；已完成的二次失败及 12 次重复失败不必重新探索，不得注入预算作自然证明。
6. Advance 前部/接续后插值、Prepare 共享入口及对象扫描少量外壳仍需后续整理；全游戏等价尚未完成。
7. 保留全部基线、两个回退、失败及控制证据，继续不提交或推送。
'''
    for p in (report,handoff): p.write_text(text,encoding='utf-8',newline='\n')
    write(S/'preservation.json',dict(passed=True,inputs=inputs,all_20_original_inputs_unchanged=True,
        previous_536_files_preserved=True,component_snapshots=snapshots,unsupported_guards=guards,
        original_game_and_save_unchanged=True,old_handwritten_engine_unchanged=True,formal_pointers_unchanged=True))
    paths={e['path'] for e in previous}
    paths.add('ra2/src/recomp/gen_game/recomp_0003.c')
    for folder in ('gameplay','runtime'):
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'ra2/src'/folder).glob('ground_*'))
    for pattern in ('*v10*.py','*v10*.ps1'):
        paths.update(p.relative_to(ROOT).as_posix() for p in ROOT.glob(pattern))
    for pattern in ('*.c','*.h','*.asm','*.txt'):
        paths.update(p.relative_to(ROOT).as_posix() for p in S.glob(pattern))
    paths.update(p.relative_to(ROOT).as_posix() for p in (S/'fixtures').glob('*') if p.is_file())
    for name in ('effects.json','budget-conditions.json','acceptance-boundary.json','action-bounds.json','pathfinder-investigation.json','extended-baseline.json'):
        paths.add((S/name).relative_to(ROOT).as_posix())
    manifest=[]; patch=[]
    for relative in sorted(paths):
        p=ROOT/relative; target=S/'final-source'/relative; target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,target)
        manifest.append(dict(path=relative,bytes=p.stat().st_size,sha256=sha(p)))
        if p.suffix.lower() in ('.c','.h','.py','.ps1','.txt','.ini','.map') or p.name=='CMakeLists.txt':
            b=S/'baseline'/relative
            before=b.read_text(encoding='utf-8',errors='replace').splitlines(True) if b.exists() else []
            patch.extend(difflib.unified_diff(before,p.read_text(encoding='utf-8',errors='replace').splitlines(True),fromfile='v9/'+relative,tofile='v10-candidate/'+relative))
    write(S/'source-manifest.json',manifest)
    (S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
    assert all(sha(ROOT/e['path'])==e['sha256']==sha(S/'final-source'/e['path']) for e in manifest)
    # 不把带严格缺口的候选置换成正式程序。copy2 保留旧时间戳，下一次构建会正常重新链接。
    shutil.copy2(S/'baseline/ra2/build-original-c/ra2.exe',exe); assert sha(exe)==FORMAL
    pointer=dict(validation=str(S/'validation.json'),candidate_executable=str(candidate),exe_sha256=fingerprint,
        state_schema=12,passed=False,frame_comparison_passed=True,strict_ordered_audit_passed=False,
        paired_scenes=27,paired_frames=14897,formal_executable=str(exe),formal_sha256=FORMAL,
        formal_baseline_unchanged=True,report=str(report),handoff=str(handoff))
    write(PROJECT/'reports/latest-movement-candidate.json',pointer)
    validation=dict(**pointer,refactor_checks_passed=True,new_native_fragment_cases=262144,probes=probes,
        source_files=len(manifest),scenarios=cases,preservation_passed=True,auxiliary_passed=True,
        full_original_equivalence_verified=False,normal_budget_exhaustion_verified=False,
        second_search_failure_naturally_observed=True,repeated_legal_failure_orders=12,
        working_source_is_candidate=True,default_executable_restored_to_v9=True,committed=False,pushed=False)
    write(S/'validation.json',validation)
    for p in (report,handoff,PROJECT/'reports/latest-movement-candidate.json'):
        target=S/'final-source/project'/p.relative_to(PROJECT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    for rel in ('reports/latest-recovery.json','reports/latest-state-comparison.json'):
        assert (PROJECT/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes()
    assert all(sha(ROOT/e['path'])==e['sha256'] for e in manifest if e['path']!='ra2/build-original-c/ra2.exe')
    print(json.dumps(dict(candidate_saved=True,strict_acceptance=False,scenes=27,frames=14897,
        source_files=len(manifest),candidate_sha256=fingerprint,formal_sha256=FORMAL),indent=2))

if __name__=='__main__': main()
