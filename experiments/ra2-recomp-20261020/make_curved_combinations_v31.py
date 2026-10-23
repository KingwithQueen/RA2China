"""Compose already accepted legal terrain heights and non-straight TubeClass routes."""
from pathlib import Path
import hashlib, json, re
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v31'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
recipes = []
for direction in ['east', 'west']:
    elevated = S / f'fixtures/tube-elevated-{direction}.MAP'
    curved = S / f'fixtures/tube-curved-{direction}.MAP'
    height_text = elevated.read_text(encoding='ascii')
    curved_text = curved.read_text(encoding='ascii')
    height_tubes = re.search(r'(?ms)^\[Tubes\]\n.*\Z', height_text)
    curved_tubes = re.search(r'(?ms)^\[Tubes\]\n.*\Z', curved_text)
    assert height_tubes and curved_tubes
    output = height_text[:height_tubes.start()] + curved_tubes.group()
    dest = S / f'fixtures/tube-curved-elevated-{direction}.MAP'
    assert not dest.exists()
    dest.write_text(output, encoding='ascii', newline='\n')
    assert dest.read_text(encoding='ascii')[:height_tubes.start()] == height_text[:height_tubes.start()]
    recipes.append(dict(path=dest.relative_to(R).as_posix(), sha256=sha(dest),
                        height_source_sha256=sha(elevated), route_source_sha256=sha(curved),
                        entrance_exit_levels=[4, 6], unchanged_outside_tube_section=True))
value = dict(passed=True, recipes=recipes, raw_runtime_writes=False,
             scope='Legal IsoMapPack5 heights 4/6 combined with the accepted six-diagonal TubeClass route. Exit blockers use normal engine constructors/placement at frame217 on the curved east fixture, radius2; acceptance requires actual occupied-exit observations, not configuration alone.')
(S / 'curved-combination-fixtures.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print('Prepared curved uphill/downhill maps; runtime validation pending')
