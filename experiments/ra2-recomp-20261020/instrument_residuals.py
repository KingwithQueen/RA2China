"""为自动转换中尚未支持的指令加入失败保护，原始 C 另存后再改写。"""
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = ROOT / 'ra2/src/recomp/gen_game'
SAVED = ROOT / 'evidence/uninstrumented-c'


def main():
    SAVED.mkdir(exist_ok=True)
    records = []
    for path in sorted(GEN.glob('recomp_0*.c')):
        text = path.read_text(encoding='utf-8')
        if '/* UNIMPLEMENTED:' not in text:
            continue
        if 'ra2_recovery_unimplemented(' in text:
            raise ValueError('拒绝重复修改: ' + path.name)
        saved = SAVED / path.name
        if saved.exists():
            raise ValueError('原始 C 备份已经存在: ' + path.name)
        shutil.copy2(path, saved)
        lines = []
        for line in text.splitlines(keepends=True):
            if '/* UNIMPLEMENTED:' in line:
                instruction = re.search(r'/\* UNIMPLEMENTED: (.*?) \*/', line)[1]
                address = re.search(r'/\* 0x([0-9A-Fa-f]+):', line)[1]
                encoded = json.dumps(instruction, ensure_ascii=True)
                line = line.replace('; /* UNIMPLEMENTED:', 'ra2_recovery_unimplemented(0x%su, %s); /* UNIMPLEMENTED:' % (address, encoded), 1)
                records.append({'file': path.name, 'address': '0x' + address, 'instruction': instruction})
            lines.append(line)
        text = ''.join(lines).replace('#include "recomp_funcs.h"\n', '#include "recomp_funcs.h"\nextern void ra2_recovery_unimplemented(uint32_t address, const char *instruction);\n', 1)
        path.write_text(text, encoding='utf-8', newline='\n')
    result = {'guarded_instructions': records, 'count': len(records), 'behavior': '执行到未实现指令时输出地址并以代码 5 退出，不能静默跳过。'}
    (ROOT / 'evidence/unsupported-guards.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'guarded_instructions': len(records), 'saved_files': len(list(SAVED.glob('*.c')))}))


if __name__ == '__main__':
    main()
