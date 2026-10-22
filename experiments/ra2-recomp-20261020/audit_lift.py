"""建立函数索引，列出转换残留项；不把成功生成代码当成完整还原。"""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = ROOT / 'ra2/src/recomp/gen_game'


def main():
    dispatch = (GEN / 'recomp_dispatch.c').read_text(encoding='utf-8')
    names = {name: int(address, 16) for address, name in re.findall(r'\{ 0x([0-9A-F]+)u, (\w+) \}', dispatch)}
    index = []
    residuals = []
    manifest = []
    for path in sorted(GEN.glob('*.c')):
        data = path.read_bytes()
        manifest.append({'file': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
        for line_number, line in enumerate(data.decode('utf-8').splitlines(), 1):
            match = re.match(r'void (\w+)\(void\)\s*\{', line)
            if match and match[1] in names:
                index.append({'address': '0x%08X' % names[match[1]], 'name': match[1], 'file': path.name, 'line': line_number})
            if any(marker in line for marker in ('/* UNIMPLEMENTED:', '/* ERROR ', 'RECOMP_NOT_LIFTED(0x')):
                residuals.append({'file': path.name, 'line': line_number, 'text': line.strip()})
    with (ROOT / 'evidence/function-index.tsv').open('w', encoding='utf-8-sig', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=['address', 'name', 'file', 'line'], delimiter='\t')
        writer.writeheader()
        writer.writerows(sorted(index, key=lambda item: item['address']))
    stats = json.loads((ROOT / 'ra2/work/game/lift_stats.json').read_text())
    result = {'stats': stats, 'dispatch_entries': len(names), 'indexed_bodies': len(index), 'all_dispatch_bodies_indexed': len(index) == len(names),
              'unimplemented_or_error_markers': residuals, 'generated_files': manifest,
              'machine_code_bridge_required': True, 'original_source_structure_recovered': False,
              'note': '当前是保留寄存器和地址语义的 C 转换；原始变量名、原始源文件和高级结构不能由编译结果自动恢复。'}
    (ROOT / 'evidence/lift-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'dispatch_entries': len(names), 'indexed_bodies': len(index), 'residual_markers': len(residuals)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
