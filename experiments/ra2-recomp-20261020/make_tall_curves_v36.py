"""Use legal map levels4/7 with the original six-diagonal curved route."""
from pathlib import Path
import base64, hashlib, json, re, struct
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v36'
scope = dict(__file__=str(R / 'make_elevated_tubes_v36.py'))
source = (R / 'make_elevated_tubes_v36.py').read_text(encoding='utf-8')
exec(compile(source[:source.index('recipes=[]')], str(R / 'make_elevated_tubes_v36.py'), 'exec'), scope)
unpack, encode, decode = scope['unpack'], scope['encode'], scope['decode']
recipes = []
for direction in ['east', 'west']:
    original = S / f'fixtures/tube-curved-elevated-{direction}.MAP'
    text = original.read_text(encoding='ascii')
    match, cells = unpack(text)
    size = len(cells) - 4 if len(cells) % 11 == 4 and cells[-4:] == bytes(4) else len(cells)
    changed = []
    for offset in range(0, size, 11):
        x, y = struct.unpack_from('<HH', cells, offset)
        if 74 <= x <= 83 and 108 <= y <= 120:
            assert cells[offset + 9] == 6
            cells[offset + 9] = 7
            changed.append([x, y])
    packed = bytearray()
    for offset in range(0, len(cells), 8192):
        block = bytes(cells[offset:offset + 8192])
        encoded = encode(block)
        assert decode(encoded, len(block)) == block
        packed += struct.pack('<HH', len(encoded), len(block)) + encoded
    value = base64.b64encode(packed).decode('ascii')
    lines = ''.join(f'{i // 70 + 1}={value[i:i+70]}\n' for i in range(0, len(value), 70))
    output = text[:match.start(1)] + lines + '\n' + text[match.end(1):]
    assert unpack(output)[1] == cells
    path = S / f'fixtures/tube-curved-tall-{direction}.MAP'
    assert not path.exists()
    path.write_text(output, encoding='ascii', newline='\n')
    recipes.append(dict(path=path.relative_to(R).as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(), changed_cells=changed))
(S / 'tall-curved-fixtures.json').write_text(json.dumps(dict(passed=True, recipes=recipes, height_levels=[4, 7], route_segments=10, diagonal_segments=6, raw_runtime_writes=False), indent=2) + '\n', encoding='utf-8')
print('Prepared legal map level4/7 curves; runtime completion remains to be checked')
