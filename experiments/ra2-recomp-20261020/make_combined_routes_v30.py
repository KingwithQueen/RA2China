"""Additional curvature uses only the map's ordinary Tubes section."""
from pathlib import Path
import hashlib, json, re
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v30'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
recipes = []
for direction, source in [('east','tube-curved-tall-east.MAP'), ('west','tube-curved-elevated-west.MAP')]:
    p = S / 'fixtures' / source
    text = p.read_text(encoding='ascii')
    section = re.search(r'(?ms)^\[Tubes\]\n.*\Z', text)
    assert section
    lines = section[0].splitlines()
    output = [lines[0]]
    for line in lines[1:]:
        if not line.strip():
            output.append(line)
            continue
        key, values = line.split('=')
        values = list(map(int, values.split(',')))
        # Header fields are entranceX,Y,heading,exitX,Y; mirror only route headings.
        assert values[-1] == -1 and len(values) >= 16, values
        route = values[5:-1]
        assert len(route) == 10
        values[5:-1] = [(4-d)%8 for d in route]
        output.append(key+'='+','.join(map(str,values)))
    dest = S / 'fixtures' / ('tube-mirror-'+direction+'.MAP')
    assert not dest.exists()
    dest.write_text(text[:section.start()]+'\n'.join(output)+'\n', encoding='ascii', newline='\n')
    recipes.append(dict(path=dest.relative_to(R).as_posix(),sha256=sha(dest),source=p.relative_to(R).as_posix(),source_sha256=sha(p),
                        unchanged_outside_tubes=True,entrances_and_exits_unchanged=True))
out = S / 'combined-route-fixtures.json'
assert not out.exists()
out.write_text(json.dumps(dict(passed=True,recipes=recipes,raw_runtime_writes=False),indent=2)+'\n',encoding='utf-8')
print('Prepared mirrored successful-height route candidates; runtime gates pending')
