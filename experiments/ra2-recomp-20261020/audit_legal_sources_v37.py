"""Native byte-checked incoming edges, separate from generated alias registrations."""
from pathlib import Path
import hashlib, json, re, struct
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v37'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
targets = {0x4A1000, 0x4A12F1, 0x4A134F, 0x4A161D, 0x4A166A, 0x4A17A2,
           0x4A2670, 0x4A32B4, 0x703040, 0x70346B, 0x70372C, 0x7038EF}
functions = json.loads((R / 'ra2/work/game/functions.json').read_text(encoding='utf-8'))['functions']
image = (R / 'ra2/game/game.exe').read_bytes()
assert sha(R / 'ra2/game/game.exe') == 'fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
pe = struct.unpack_from('<I', image, 0x3C)[0]
base = struct.unpack_from('<I', image, pe + 24 + 28)[0]
headers = pe + 24 + struct.unpack_from('<H', image, pe + 20)[0]
sections = []
for i in range(struct.unpack_from('<H', image, pe + 6)[0]):
    h = headers + 40 * i
    vs, va, size, raw = struct.unpack_from('<IIII', image, h + 8)
    sections.append(dict(name=image[h:h+8].rstrip(b'\0').decode(), va=va+base,
                         size=size, raw=raw, executable=bool(struct.unpack_from('<I', image, h+36)[0] & 0x20000000)))

def native(address, count):
    s = next(s for s in sections if s['va'] <= address and address + count <= s['va'] + s['size'])
    start = s['raw'] + address - s['va']
    return image[start:start+count]

edges = {}
line_pattern = re.compile(r'^([0-9A-F]{8})\s+((?:[0-9a-f]{2} )+)\s+(call|j\w+|loop\w*)\s+0x([0-9a-f]+)\s*$')
with (R / 'ra2/work/game/disassembly.asm').open(encoding='utf-8') as stream:
    for line in stream:
        match = line_pattern.match(line)
        if not match or int(match[4], 16) not in targets:
            continue
        address, target = int(match[1], 16), int(match[4], 16)
        code = bytes.fromhex(match[2])
        assert native(address, len(code)) == code, hex(address)
        if code[0] in (0xE8, 0xE9):
            displacement = int.from_bytes(code[1:5], 'little', signed=True)
        elif code[0] == 0x0F:
            assert 0x80 <= code[1] <= 0x8F
            displacement = int.from_bytes(code[2:6], 'little', signed=True)
        else:
            assert code[0] == 0xEB or 0x70 <= code[0] <= 0x7F or 0xE0 <= code[0] <= 0xE3, code.hex()
            displacement = int.from_bytes(code[1:2], 'little', signed=True)
        assert (address + len(code) + displacement) & 0xFFFFFFFF == target
        edges[address] = dict(address=f'{address:08X}', target=f'{target:08X}', instruction=match[3], bytes=code.hex())

entries = []
for target in sorted(targets):
    fn = next(f for f in functions if f['address'] == target)
    incoming = sorted((e for e in edges.values() if int(e['target'], 16) == target), key=lambda e:e['address'])
    references = []
    needle = struct.pack('<I', target)
    for s in sections:
        start = s['raw']
        data = image[start:start+s['size']]
        pos = data.find(needle)
        while pos >= 0:
            references.append(dict(address=f"{s['va']+pos:08X}", section=s['name'], executable=s['executable'], aligned=(s['va']+pos)%4 == 0))
            pos = data.find(needle, pos+1)
    entries.append(dict(entry=f'{target:08X}', entry_kind=fn['entry_kind'], decoded_incoming=incoming,
                        image_address_literals=references,
                        direct_native_call_found=any(e['instruction']=='call' for e in incoming),
                        noncode_address_literal_found=any(not ref['executable'] for ref in references)))
aliases = [e for e in entries if e['entry_kind']=='alias']
assert len(aliases) == 9
assert all(not e['direct_native_call_found'] and not e['noncode_address_literal_found'] for e in aliases)
assert all(e['decoded_incoming'] for e in aliases)
value = dict(passed=True, entries=entries, unique_native_edges=len(edges),
             alias_count=len(aliases), nonprimary_natural_entry_proved=False,
             conclusion='All nine examined nonprimary entries are recursive-disassembler aliases. Their legal native sources are intra-function branches. No direct CALL or non-code image address literal points to these aliases in the scanned evidence. An alias lookup registration is not a native call source.',
             limits=['Decoded disassembly coverage is bounded; arbitrary computed targets and runtime-built pointers are not excluded.',
                     'Internal native-boundary hits do not prove entry through the separately generated C alias function.'],
             inputs=[dict(path=p.relative_to(R).as_posix(), sha256=sha(p)) for p in
                     [R/'ra2/game/game.exe', R/'ra2/work/game/functions.json', R/'ra2/work/game/disassembly.asm', Path(__file__)]])
out = S / 'legal-overlap-sources.json'
assert not out.exists()
out.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(passed=True, aliases=len(aliases), byte_checked_native_edges=len(edges))))
