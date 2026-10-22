"""原版墙体/闸门建图测试，地图修改明确局限于试验副本。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
FOLDER = ROOT / 'evidence/movement-state-v4/fixtures'
base = (FOLDER / 'empty.MAP').read_text(encoding='ascii')

def write(name, walls, gates=()):
    entries = []
    for x, y in sorted(set(walls)):
        entries.append(f'Player House,NAWALL,256,{x},{y},0,None,1,0,1,0,0,None,None,None,0,0')
    for x, y in gates:
        entries.append(f'Player House,GAGATE_A,256,{x},{y},0,None,1,0,1,0,0,None,None,None,0,0')
    target = FOLDER / (name + '.MAP')
    assert not target.exists()
    target.write_text(base + ''.join(f'{i+1}={entry}\n' for i, entry in enumerate(entries)), encoding='ascii', newline='\n')

write('wall-line', [(x, 111) for x in range(60, 77)])
write('budget-ring', [(67 + x, 114 + y) for x in range(-1, 2) for y in range(-1, 2) if x or y])
walls = [(x, 111) for x in range(60, 77) if x not in (66, 67, 68)]
walls += [(x, y) for x in (64, 70) for y in range(107, 117) if y != 111]
walls += [(x, y) for x in range(64, 71) for y in (107, 116)]
write('allied-gate', walls, [(66, 111)])
print('Created 3 barrier maps')
