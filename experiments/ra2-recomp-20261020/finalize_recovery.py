"""汇总真实生成、编译和运行证据，明确区分已通过项目与尚未证明的等价性。"""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
EVIDENCE = ROOT / 'evidence'
ORIGINAL = Path(r'H:\开发\运行版本\原版1.006')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def main():
    preservation = []
    for item in read(EVIDENCE / 'original-inputs-before.json'):
        path = ORIGINAL / item['name']
        actual = digest(path)
        preservation.append({'name': item['name'], 'sha256': actual, 'unchanged': actual == item['sha256'] and path.stat().st_size == item['bytes']})
    before = read(EVIDENCE / 'existing-product-before.json')
    current_product = digest(Path(before['Path']))
    preserved = all(item['unchanged'] for item in preservation) and current_product == before['Hash'].lower()
    (EVIDENCE / 'preservation.json').write_text(json.dumps({'passed': preserved, 'original_inputs': preservation,
        'existing_product_sha256': current_product, 'existing_product_unchanged': current_product == before['Hash'].lower(),
        'writes_to_old_project_or_original_inputs': False}, ensure_ascii=False, indent=2), encoding='utf-8')
    if not preserved:
        raise ValueError('原始输入或既有产品指纹发生变化，停止发布通过结论。')
    baseline = read(EVIDENCE / 'baseline-runtime/runtime-comparison.json')
    current = read(EVIDENCE / 'runtime-comparison.json')
    default = read(EVIDENCE / 'runtime-final-default.json')
    executable = ROOT / 'ra2/build-original-c/ra2.exe'
    executable_hash = digest(executable)
    if executable_hash != current['exe_sha256'] or executable_hash != default['exe_sha256']:
        raise ValueError('最终运行报告与当前 EXE 指纹不一致。')
    target_test = (EVIDENCE / 'instruction-differential-target.log').read_text(encoding='utf-8', errors='replace')
    if '372/372 match hardware, 0 known divergences, 0 failures' not in target_test:
        raise ValueError('与目标编译器匹配的指令差异测试尚未通过。')
    pixels = {}
    for name in ('menu-idle', 'skirmish-start', 'save-load-isolated-paused', 'save-load-frozen-world', 'save-load-fixed-seed-world'):
        path = EVIDENCE / 'pixels' / name / 'comparison.json'
        if path.exists():
            pixels[name] = read(path)
    if 'save-load-fixed-seed-world' not in pixels:
        raise ValueError('最终固定输入画面报告尚未完成。')
    stats = read(ROOT / 'ra2/work/game/lift_stats.json')
    generated = ROOT / 'ra2/src/recomp/gen_game'
    dispatch = set(re.findall(r'\{ 0x([0-9A-F]{8})u,', (generated / 'recomp_dispatch.c').read_text()))
    unresolved = []
    for path in generated.glob('recomp_0*.c'):
        for address in re.findall(r'L_([0-9A-F]{8}): RECOMP_ITAIL', path.read_text(encoding='utf-8')):
            if address not in dispatch:
                unresolved.append({'file': path.name, 'address': '0x' + address})
    seeds = {}
    for mode, suffix in (('original', '.original'), ('generated-c', '')):
        log = (ROOT / 'ra2/work/tests-game' / ('skirmish-build' + suffix) / 'run.log').read_text(encoding='utf-8', errors='replace')
        seeds[mode] = re.findall(r'Seed is ([0-9a-fA-F]+)', log)
    guard_hits = []
    for path in (ROOT / 'ra2/work/tests-game').glob('*/run.log'):
        text = path.read_text(encoding='utf-8', errors='replace')
        if '[recovery-unimplemented]' in text or '\nICALL:' in text or '\nITAIL' in text or '\n=== fault' in text:
            guard_hits.append(str(path.relative_to(ROOT)))
    summary = {'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'pipeline_compiled_and_exercised': True,
        'full_original_equivalence_verified': False, 'original_source_structure_fully_recovered': False,
        'experiment_directory': str(ROOT), 'executable': str(executable), 'exe_sha256': executable_hash,
        'source_provenance': read(EVIDENCE / 'provenance.json'), 'conversion': stats,
        'assembly': read(EVIDENCE / 'assembly-export.json'), 'instruction_differential': {'passed': 372, 'failed': 0,
            'reference': 'Unicorn 2.1.4', 'compiler': 'MSVC 19.51 x86 /O2 /d2SSAOptimizer- /std:c17'},
        'baseline_runtime': baseline, 'final_runtime': current, 'final_default_runtime': default, 'pixel_comparisons': pixels,
        'pending_unresolved_tail_targets': unresolved, 'unimplemented_guard_count': read(EVIDENCE / 'unsupported-guards.json')['count'],
        'runtime_guard_or_unresolved_hits': guard_hits, 'uncontrolled_skirmish_seeds': seeds,
        'preservation_passed': preserved, 'initial_save_test_superseded': '硬链接复用了以 0x12 独占打开的存档；改为真实副本后读档通过。最初暂停场景要求五个不同画面也已修正。',
        'runtime_dependencies': '原版 EXE 的静态数据、原版资源副本、BINKW32.DLL、Blowfish.dll 和 Windows x86 调用桥；不是脱离旧数据布局的独立 C 引擎。',
        'multicore_optimization_completed': False}
    (EVIDENCE / 'validation.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    pointer = {'experiment': str(ROOT), 'validation': str(EVIDENCE / 'validation.json'), 'executable': str(executable), 'sha256': executable_hash,
               'full_original_equivalence_verified': False, 'preservation_passed': preserved}
    (PROJECT / 'reports/latest-recovery.json').write_text(json.dumps(pointer, ensure_ascii=False, indent=2), encoding='utf-8')
    joint = pixels['save-load-fixed-seed-world']
    document = f'''原版 1.006 汇编恢复与 C 静态重编译实验（2026-10-20）

已经完成实际生成与编译，能够运行菜单、遭遇战和盟苏首关，并能读取现有原版存档。
这是一份用于后续还原与差异定位的 C 参考版本，尚未完成所有战役、逻辑和画面的等价验收。

工作目录：{ROOT}
当前 EXE：{executable}
SHA-256：{executable_hash}
正常启动参数：
--run --exe "{ROOT / 'ra2/game/game.exe'}" --game "{ROOT / 'ra2/game'}" --scale nearest
以上执行生成的 C。添加 --original 可在同一宿主下执行原始机器码作对照。
复现受控画面时额外使用 --seed 12345 --freeze-game-frame 2250，停帧选项仅用于诊断。

汇编清单：ra2/work/game/disassembly.asm
完整函数与指令目录：ra2/work/game/functions-full.json
生成 C：ra2/src/recomp/gen_game/
函数地址、名称与源码行号索引：evidence/function-index.tsv
重点入口：evidence/core-entrypoints.json
正式证据：evidence/validation.json
上游提交和工具版本：evidence/provenance.json
本地适配：evidence/upstream-adaptation.patch、evidence/tools-adaptation.patch；新增 C 辅助实现在 ra2/src/runtime/recovery_checks.c。

恢复与验证情况：
1. 恢复 944 个 RTTI 类，识别 23,111 个目录入口；最终生成 {stats['lifted']} 个 C 函数入口，58 个代码分片，约 578 万行转换代码及头文件。
2. 零转换错误、零未转换函数占位。仍有 {stats['no_terminator']} 个终止边界不明确的函数、37 处未实现指令保护和 {len(unresolved)} 个未解析尾跳转目标，不能据此声称完整恢复。
3. 递归汇编清单保留地址与字节，所有列出的指令字节均与输入 EXE 对应。目录覆盖约 91.63%，不等同于游戏还原率；原始变量名和源文件结构尚未全部恢复。
4. 使用目标 MSVC 19.51 x86 和优化设置，与 Unicorn 的 372 组指令差异测试全部通过。
5. 基线验证覆盖菜单停留、正常退出、遭遇战启动、盟苏首关持续运行、读档与暂停。建造测试两边均完成生产和放置，但未固定种子的两局生存结果不同，仍保留为待核对项。
6. 最初并行读档使用硬链接，引发原版复合存档的独占访问冲突；独立 C 探针复现 0x80030020，真实副本均能打开。修正后，两条执行路径都成功读档。
7. 菜单取得 899 个精确匹配 RGB 采样帧、419 种不同画面；同存档暂停选项界面取得 907 个匹配帧，但该界面覆盖战场，不能用来验收模型。
8. 同存档、种子 12345、第 2250 模拟帧的真实战场：精确匹配采样帧 {joint['exact_matching_c_frames_after_first_90']} 个，共同 RGB 哈希 {joint['unique_common_rgb_hashes']} 种。该结果只对应明确的受控场景，不能替代整场游戏的状态校验。

保护与边界：
H 盘原始目录的 20 个输入逐个 SHA-256 保持不变。既有 build/ra2battle.exe 保持不变，没有写入旧项目。
新增代码、构建与测试数据位于 D 盘独立实验目录；说明与入口位于本项目 docs/reports。既有手写 C 引擎未被覆盖。
游戏逻辑转换为 C17，Windows ABI 桥仍包含必要的 x86 内联汇编，并继续使用原版静态数据与外部 DLL。
默认关闭重制功能的代码补丁。自动生成部分保留生成器原貌，新增辅助代码使用中文注释。
当前没有进行多核优化，没有把编译成功或少量运行场景当成完整玩法一致性证明。
工程根目录没有 Git 仓库；两个第三方仓库固定在 provenance.json 所列提交，本轮无提交或推送。

后续优先顺序：
先固定随机种子、存档初态和原版模拟帧命令，建立状态与渲染参数的差异定位；再处理未支持指令、尾跳转和边界疑点。
以真实原版渲染结果为基准研究调色板、光照、模型和动画，恢复可读的 C 数据结构与模块接口。
最后在等价验收的基础上拆分资源、渲染和模拟任务，实测多核收益；中国阵营仍只预留扩展接口。
'''
    (PROJECT / 'docs/逆向恢复与C重编译.txt').write_text(document, encoding='utf-8')
    print(json.dumps({'exe_sha256': executable_hash, 'preservation_passed': preserved, 'fixed_world_matching_frames': joint['exact_matching_c_frames_after_first_90'],
                      'full_original_equivalence_verified': False, 'runtime_guard_hits': guard_hits}, ensure_ascii=False))


if __name__ == '__main__':
    main()
