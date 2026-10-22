"""把自然预算分支的必要条件与已观察结果分开，不用显式入口证明自然可达。"""
from pathlib import Path
import hashlib
import json
import struct
import sys
ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v5'
sys.path.insert(0,str(ROOT/'python_lib'))
import capstone
import pefile

path = ROOT/'ra2/game/game.exe'
assert hashlib.sha256(path.read_bytes()).hexdigest() == 'fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
image = pefile.PE(str(path)).get_memory_mapped_image()
md = capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
code = list(md.disasm(image[0xC3000:0xC38C6],0x4C3000))
returns = [i.address for i in code if i.mnemonic == 'ret']
assert returns == [0x4C307C,0x4C36E9,0x4C38A6,0x4C38C3]
unit_stop = struct.unpack_from('<I',image,0x7ADDF8-0x400000+0x48C)[0]
unit_accept = struct.unpack_from('<I',image,0x7ADDF8-0x400000+0x2AC)[0]
assert unit_stop == 0x4C4B60 and unit_accept == 0x4C2EF0
assert image[0xC371A:0xC3720].hex() == 'ff928c040000'
evidence = []
for tag in ('final-budget-natural','final-restricted-clear','final-restricted-rock'):
    rows = [json.loads(line) for line in (STAGE/'runs'/tag/'original/state.jsonl').open(encoding='utf-8')]
    failures = [r for r in rows if r['kind']=='movement-audit' and r['stage']==6 and r['value']==0]
    assert failures and all(r['active_ground_drive'] and not r['active_goal_valid'] for r in failures)
    assert not any(r['kind']=='movement-audit' and r['stage']==3 for r in rows)
    values = sorted({o['ground_drive']['path_failure_counter'] for r in rows if r['kind']=='state'
        for o in r['objects'] if o['id']==1022579})
    assert values == [10]
    evidence.append(dict(tag=tag,failed_rebuilds=failures,failure_budget_values=values,natural_budget_entries=0))
result = dict(passed=True, original_returns=[hex(a) for a in returns],
    original_unit_stop_slot=hex(unit_stop), original_unit_accept_slot=hex(unit_accept),
    necessary_conditions=[
        '队列头为 -1；短重试计时器允许重建。',
        '原版 4C3000 返回 false，且所有者仍存在。',
        '随后对 Drive.destination 的 2AC 查询返回 true，目标仍不是无效点。',
        '未被近距离任务停止分支提前返回；进入 4A2A83 的失败障碍观察。',
        '观察未被近距离友方对象停止分支提前返回，最终进入 4A2DFD。',
        '正预算每次只扣 1；从 10 起连续十次到 0，另一次失败才执行零预算停止。'],
    ordinary_drive_failure_analysis={
        'main_search_failure':'4C36EC..4C371A 调用所有者 48C；Unit 的该槽为 4C4B60，调用当前 locomotor 的 StopMoving。当前 locomotor 就是本 Drive 时，49FF97..49FFB0 清空目标。',
        'early_rejection':'4C3069 的提前失败不会清空目标，但失败原因是 2AC 拒绝格中心。对相同非负目标格、稳定区划和相同 Unit 而言，随后 2AC 仍拒绝，先返回而不扣预算。',
        'assumptions':['有效目标格坐标非负','两次可达性查询之间区划和 Unit 身份稳定','所有者当前 locomotor 就是正在准备的 Drive'],
        'conclusion':'在上述范围内，普通路径失败不能自然扣预算；这是带前提的控制流结论，不是整个游戏分支不可达证明。'},
    unresolved=['尚未找到原版合法玩法中同时保留目标、返回重建失败、后续可达性通过的场景。',
        '可继续检查 locomotor 包装/替换或服务期间目标、区划变化；这些只是待调查方向，尚无自然耗尽实景。'],
    natural_exhaustion_verified=False, controlled_entry_is_natural=False, real_scene_evidence=evidence)
(STAGE/'budget-conditions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Budget conditions verified; natural exhaustion remains unverified.')
