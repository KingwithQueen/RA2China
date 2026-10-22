"""Alternative legal non-straight route; retain the original diagonal uphill stall."""
from pathlib import Path
import hashlib, json, re
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v28'
route = [2, 2, 0, 2, 2, 4, 2, 2, 2, 2, 2, 2]
reverse = [(d + 4) % 8 for d in reversed(route)]
offsets = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
assert sum(offsets[d][0] for d in route) == 10 and sum(offsets[d][1] for d in route) == 0
recipes = []
for direction in ['east', 'west']:
    source = S / f'fixtures/tube-elevated-{direction}.MAP'
    text = source.read_text(encoding='ascii')
    match = re.search(r'(?ms)^\[Tubes\]\n.*\Z', text)
    assert match
    rows = '[Tubes]\n0=68,114,2,78,114,' + ','.join(map(str, route)) + ',-1\n1=78,114,6,68,114,' + ','.join(map(str, reverse)) + ',-1\n'
    path = S / f'fixtures/tube-cardinal-elevated-{direction}.MAP'
    assert not path.exists()
    path.write_text(text[:match.start()] + rows, encoding='ascii', newline='\n')
    recipes.append(dict(path=path.relative_to(R).as_posix(), sha256=hashlib.sha256(path.read_bytes()).hexdigest(), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
(S / 'cardinal-curved-fixtures.json').write_text(json.dumps(dict(passed=True, forward=route, reverse=reverse, height_levels=[4, 6], duration=12, fixtures=recipes, raw_runtime_writes=False), indent=2) + '\n', encoding='utf-8')
print('Prepared twelve-segment cardinal curves; runtime completion is not assumed')
