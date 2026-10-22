"""Integrate independently validated entries, retaining all original tail labels."""
from pathlib import Path
import argparse, json
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v27'
parser = argparse.ArgumentParser()
parser.add_argument('part', choices=['template', 'passage', 'returns'])
part = parser.parse_args().part
counts = {}

def load(path):
    raw = path.read_bytes()
    return raw.decode('utf-8').replace('\r\n', '\n'), '\r\n' if b'\r\n' in raw else '\n'

def insert(text, address, body):
    marker = 'L_' + address + ':\n'
    count = text.count(marker)
    assert count, address
    counts[address] = count
    return text.replace(marker, marker + body)

if part == 'template':
    path = R / 'ra2/src/recomp/gen_game/recomp_0010.c'
    text, newline = load(path)
    text = '#include "ground_overlap_bridge.h"\n' + text
    text = insert(text, '004A17FE',
        '    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t cells_resume=ra2_ground_template_transition_bridge(0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); if(cells_resume==0x4A1AB0) goto L_004A1AB0; goto L_004A186C;\n')
    text = insert(text, '004A3502',
        '    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_template_transition_bridge(1); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); goto L_004A3550;\n')
    path.write_text(text, encoding='utf-8', newline=newline)
    path = R / 'ra2/CMakeLists.txt'
    text, newline = load(path)
    files = 'src/gameplay/ground_template_transition.c src/gameplay/ground_object_chain.c src/runtime/ground_overlap_bridge.c'
    text += f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
    path.write_text(text, encoding='utf-8', newline=newline)
else:
    prior = 'template' if part == 'passage' else 'passage'
    assert json.loads((S / f'parts/{prior}-verified/validation.json').read_text(encoding='utf-8'))['passed']
    path = R / 'ra2/src/recomp/gen_game/recomp_0046.c'
    text, newline = load(path)
    if part == 'passage':
        text = '#include "ground_overlap_bridge.h"\n' + text
        for address, entry in [('00703439', 0), ('007038EF', 1)]:
            text = insert(text, address,
                f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t chain_resume_{entry}=ra2_ground_object_chain_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); if(chain_resume_{entry}==0x70346B) goto L_0070346B; goto L_00703905;\n')
    else:
        for entry, address in enumerate(['007031B1', '00703B5A', '00703B69', '00703BA8', '00703BBC']):
            text = insert(text, address,
                f'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_passage_return_bridge({entry}); RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;\n')
    path.write_text(text, encoding='utf-8', newline=newline)

(S / (part + '-integration.json')).write_text(json.dumps(dict(
    passed=True, entries=counts, existing_tail_targets_preserved=True), indent=2) + '\n', encoding='utf-8')
print(part, counts)
