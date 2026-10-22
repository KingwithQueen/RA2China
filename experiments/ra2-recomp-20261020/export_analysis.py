"""导出带原始字节的汇编清单，同时为 C 转换生成轻量函数目录。"""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'ra2/work/game'
SOURCE = ROOT / 'ra2/game/game.exe'


def main():
    raw = SOURCE.read_bytes()
    catalog = json.loads((WORK / 'functions-full.json').read_text(encoding='utf-8'))
    nt = struct.unpack_from('<I', raw, 0x3c)[0]
    section_count = struct.unpack_from('<H', raw, nt + 6)[0]
    optional_size = struct.unpack_from('<H', raw, nt + 20)[0]
    base = struct.unpack_from('<I', raw, nt + 24 + 28)[0]
    sections = []
    for i in range(section_count):
        at = nt + 24 + optional_size + i * 40
        size, rva, raw_size, offset = struct.unpack_from('<IIII', raw, at + 8)
        sections.append((base + rva, raw_size, offset))
    covered = bytearray(catalog['code_end'] - catalog['code_start'])
    instructions = 0
    with (WORK / 'disassembly.asm').open('w', encoding='utf-8', newline='\n') as out:
        out.write('; 原版 1.006 的递归反汇编清单，保留地址与指令字节；不是恢复的原始汇编源码。\n')
        out.write('; 函数共享尾部可能重复列出，未识别区间单独记入报告，不将数据强行认作指令。\n')
        out.write('; 输入 SHA-256: ' + hashlib.sha256(raw).hexdigest() + '\n')
        for function in catalog['functions']:
            out.write('\n; 函数 0x%08X，目录名称 %s\n' % (function['address'], function['name']))
            for block in function.pop('blocks', []):
                out.write('; 基本块 0x%08X\n' % block['start'])
                for ins in block['instructions']:
                    address = ins['address']
                    code = bytes.fromhex(ins['bytes'])
                    section = next((s for s in sections if s[0] <= address < s[0] + s[1]), None)
                    if not section:
                        raise ValueError('指令超出原始节: 0x%08X' % address)
                    start = section[2] + address - section[0]
                    if raw[start:start + len(code)] != code:
                        raise ValueError('指令字节与输入不符: 0x%08X' % address)
                    index = address - catalog['code_start']
                    if 0 <= index and index + len(code) <= len(covered):
                        covered[index:index + len(code)] = b'\x01' * len(code)
                    instructions += 1
                    out.write('%08X  %-44s  %-10s %s\n' % (address, code.hex(' '), ins['mnemonic'], ins['op_str']))
    (WORK / 'functions.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=1), encoding='utf-8')
    gaps = []
    begin = None
    for i, value in enumerate(covered + b'\x01'):
        if not value and begin is None:
            begin = i
        elif value and begin is not None:
            gaps.append({'address': '0x%08X' % (catalog['code_start'] + begin), 'bytes': i - begin})
            begin = None
    result = {'input_sha256': hashlib.sha256(raw).hexdigest(), 'functions': len(catalog['functions']), 'listed_instructions_with_duplicates': instructions,
              'verified_instruction_bytes': sum(covered), 'code_range_bytes': len(covered), 'unclassified_ranges': gaps,
              'catalog_interval_coverage': catalog['stats'], 'all_listed_bytes_match_input': True,
              'complete_semantic_recovery': False, 'note': '目录区间覆盖率可能包含内嵌数据，不能等同于实际指令覆盖率或游戏还原率。'}
    (ROOT / 'evidence/assembly-export.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'unclassified_ranges'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
