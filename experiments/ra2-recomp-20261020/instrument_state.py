"""只为两个已核实函数加入按帧状态探针，保留完整分片备份且拒绝重复修改。"""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
backup = ROOT / 'evidence/state-step-v1/baseline'
specs = [('recomp_0021.c', 'sub_0053D890', 'ra2_state_tick();'),
         ('recomp_0011.c', 'sub_004B65C0', 'ra2_state_event(g_ecx);'),
         ('recomp_0048.c', 'sub_007220C0', 'ra2_state_math(g_esp, g_ebp, g_ecx, g_edx);')]
receipt = []
for filename, function, call in specs:
    path = ROOT / 'ra2/src/recomp/gen_game' / filename
    before = path.read_text(encoding='utf-8')
    if '#include "state_trace.h"' in before:
        raise RuntimeError('探针已存在，拒绝重复修改: ' + filename)
    target = 'void %s(void) {' % function
    if before.count(target) != 1:
        raise RuntimeError('函数入口不唯一: ' + function)
    dest = backup / path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise RuntimeError('备份已存在，拒绝覆盖: ' + str(dest))
    shutil.copy2(path, dest)
    after = '#include "state_trace.h"\n' + before.replace(target, target + '\n    ' + call, 1)
    path.write_text(after, encoding='utf-8', newline='\n')
    receipt.append({'file': str(path.relative_to(ROOT)), 'function': function, 'call': call,
                    'before_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
                    'after_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
(ROOT / 'evidence/state-step-v1/instrumentation.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
