"""用独立 x87 指令验证整数数值层，另行区分原版游戏函数对照。"""
import sys
sys.dont_write_bytecode = True
import json
import random
import struct
import subprocess
from pathlib import Path
from native_reference import Native, ARG, STOP, bits

def main():
    native = Native()
    uc = native.uc
    rows = []
    rng = random.Random(1006)
    # 显式指令夹具不冒充原版游戏函数；控制字取原版转换函数使用的 0xe7f。
    for operation in ('+', '-', '*', '/', 's'):
        for index in range(600):
            a = ((rng.randrange(1007, 1039) << 52) | rng.getrandbits(52))
            b = ((rng.randrange(1007, 1039) << 52) | rng.getrandbits(52))
            if operation != 's':
                a |= rng.getrandbits(1) << 63
                b |= rng.getrandbits(1) << 63
            uc.mem_write(ARG, struct.pack('<QQ', a, b))
            opcode = {'+': b'\xdc\x05', '-': b'\xdc\x25', '*': b'\xdc\x0d', '/': b'\xdc\x35'}
            code = b'\xdd\x05' + struct.pack('<I', ARG)
            code += b'\xd9\xfa' if operation == 's' else opcode[operation] + struct.pack('<I', ARG + 8)
            code += b'\xdd\x1d' + struct.pack('<I', ARG + 16) + b'\xc3'
            uc.mem_write(STOP + 0x1000, code)
            # 代码位置固定时须清除译码缓存，避免重复执行上一次运算。
            uc.ctl_remove_cache(STOP + 0x1000, STOP + 0x1100)
            native.run(STOP + 0x1000)
            rows.append((operation, a, b, native.raw(ARG + 16)))
    for index in range(600):
        n, d = rng.randrange(1, 0xffffffff), rng.randrange(1, 0xffffffff)
        rows.append(('r', n, d, bits(n / d)))
    source = ''.join(f'{op} {a:016x} {b:016x}\n' for op, a, b, result in rows)
    actual = subprocess.check_output([sys.argv[1], '--numbers'], input=source, encoding='ascii').splitlines()
    assert len(actual) == len(rows)
    failures = []
    for index, (value, row) in enumerate(zip(actual, rows)):
        if int(value, 16) != row[3]: failures.append({'index': index, 'operation': row[0], 'a': f'{row[1]:016x}', 'b': f'{row[2]:016x}', 'native': f'{row[3]:016x}', 'actual': value})
    report = {'passed': not failures, 'scope': '独立 x87 算术与最近偶数规则编码；不是完整原版移动验收', 'checks': len(rows), 'failures': failures}
    with Path(sys.argv[2]).open('w', encoding='utf-8', newline='\n') as output: json.dump(report, output, ensure_ascii=False, indent=2)
    print(json.dumps({'passed': report['passed'], 'checks': len(rows), 'failure_count': len(failures)}))
    return bool(failures)
if __name__ == '__main__': sys.exit(main())
