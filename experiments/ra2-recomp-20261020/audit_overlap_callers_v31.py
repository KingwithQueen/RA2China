"""Bind real host return addresses to generated functions and verified CALL bytes."""
from pathlib import Path
from bisect import bisect_right
import hashlib, json, re, struct

R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v31'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
map_path = S / 'connection-fixture.map'
symbols = {}
for line in map_path.read_text(encoding='utf-8', errors='replace').splitlines():
    match = re.match(r'^\s+[0-9A-Fa-f]{4}:[0-9A-Fa-f]{8}\s+(\S+)\s+([0-9A-Fa-f]{8})\s+f\s+(\S+)', line)
    if match:
        symbols.setdefault(int(match[2], 16), []).append(dict(name=match[1], object=match[3]))
addresses = sorted(symbols)
targets = {item['name']: address for address, items in symbols.items() for item in items}
image_path = S / 'connection-fixture-probe.exe'
image = image_path.read_bytes()
pe = struct.unpack_from('<I', image, 0x3C)[0]
base = struct.unpack_from('<I', image, pe + 24 + 28)[0]
assert base == 0x60000000
section_count = struct.unpack_from('<H', image, pe + 6)[0]
headers = pe + 24 + struct.unpack_from('<H', image, pe + 20)[0]

def code_at(address, count):
    rva = address - base
    for index in range(section_count):
        virtual_size, virtual_rva, raw_size, raw = struct.unpack_from('<IIII', image, headers + index * 40 + 8)
        if virtual_rva <= rva and rva + count <= virtual_rva + raw_size:
            offset = raw + rva - virtual_rva
            return image[offset:offset + count]
    raise AssertionError(hex(address))

parents = {}
for filename, sites in [('recomp_0010.c', {16: '004A17FE', 17: '004A3502'}), ('recomp_0046.c', {18: '00703439', 19: '007038EF'})]:
    current, origin = None, None
    for line in (R / 'ra2/src/recomp/gen_game' / filename).read_text(encoding='utf-8').splitlines():
        match = re.match(r'void (\w+)\(void\) \{', line)
        if match:
            current = match[1]
        match = re.search(r'RECOMP_ENTER\(0x([0-9A-Fa-f]+)u\)', line)
        if match:
            origin = match[1].upper()
        for stage, site in sites.items():
            if line == 'L_' + site + ':':
                parents.setdefault(stage, []).append(dict(function=current, original_entry=origin))

routes = []
for scene in ['j-default', 'j-long', 'j-tc1', 'j-fail']:
    report = json.loads((S / 'runs' / scene / 'comparison.json').read_text(encoding='utf-8'))
    assert report['passed'] and report['exe_sha256'] == sha(image_path)
    log = (S / 'runs' / scene / 'generated-c/run.log').read_text(encoding='utf-8', errors='replace')
    for match in re.finditer(r'\[overlap-route\] site=(\d+) return=([0-9A-F]{8}) frame=(\d+)', log):
        stage, return_address = int(match[1]), int(match[2], 16)
        start = addresses[bisect_right(addresses, return_address - 1) - 1]
        candidates = symbols[start]
        generated = [parent for parent in parents[stage] if any(item['name'] == '_' + parent['function'] for item in candidates)]
        assert len(generated) == 1, (stage, candidates)
        call = code_at(return_address - 5, 5)
        assert call[0] == 0xE8
        call_target = (return_address + struct.unpack_from('<i', call, 1)[0]) & 0xFFFFFFFF
        expected = '_ra2_ground_template_transition_bridge' if stage < 18 else '_ra2_ground_object_chain_bridge'
        assert call_target == targets[expected], (stage, hex(call_target), expected)
        routes.append(dict(scene=scene, stage=stage, generated_entry=generated[0]['original_entry'], generated_function=generated[0]['function'], first_frame=int(match[3]),
                           host_return=f'{return_address:08X}', host_function_start=f'{start:08X}',
                           host_call_bytes=call.hex(), host_call_target=f'{call_target:08X}', call_target_symbol=expected))
assert {18, 19}.issubset({r['stage'] for r in routes})
value = dict(passed=True, routes=routes, static_parent_entries=parents, method='Real _ReturnAddress in the adapter; link-map enclosing generated function; five-byte E8 CALL verified against observer PE bytes. Mutable g_cur_func marker is not used.',
             nonprimary_overlapping_adapter_naturally_observed=any(r['generated_function'] != 'UnitClass__virtual_101' for r in routes),
             inputs=[dict(path=p.relative_to(R).as_posix(), sha256=sha(p)) for p in [image_path, map_path, R / 'audit_overlap_callers_v31.py', S / 'connection_overlap_bridge.c']])
(S / 'overlap-caller-identity.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(passed=True, routes=len(routes), actual_generated_entries=sorted({r['generated_entry'] for r in routes}))))
