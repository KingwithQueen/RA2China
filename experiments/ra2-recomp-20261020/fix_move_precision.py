"""针对已取得真实参数与 CPU 差异证据的原版移动三指令序列应用 C 实现。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0010.c'
before = path.read_text(encoding='utf-8')
needle = '{ float _v = (float)fp_pop(); *(float*)ADDR(esp) = _v; } /* 0x004A241F: fstp dword ptr [esp] */'
replacement = ('{ (void)fp_pop(); MEM32(esp) = ra2_x87_imul_store_f32((int32_t)MEM32(ebp + 0x4C), '
               'MEM64(0x7A05C0), _fpu_cw); } /* 0x004A241F: fstp dword ptr [esp] - PC/RC verified */')
if before.count(needle) != 12 or 'x87_precision.h' in before:
    raise RuntimeError('移动序列数量或应用状态不符，拒绝修改')
backup = ROOT / 'evidence/state-step-v1/baseline/ra2/src/recomp/gen_game/recomp_0010.c'
if hashlib.sha256(backup.read_bytes()).hexdigest() != hashlib.sha256(path.read_bytes()).hexdigest():
    raise RuntimeError('现有分片与已保全基线不符')
after = '#include "x87_precision.h"\n' + before.replace(needle, replacement)
path.write_text(after, encoding='utf-8', newline='\n')
receipt = {'address': '0x004A241F', 'sequence': ['0x004A23F0', '0x004A2404', '0x004A241F'],
           'copies_in_shared_tail_lifts': 12, 'before_sha256': hashlib.sha256(backup.read_bytes()).hexdigest(),
           'after_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
           'scope': 'only this fild int32 / fmul float64 / fstp float32 sequence; not all x87 arithmetic'}
(ROOT / 'evidence/state-step-v1/movement-precision-fix.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
