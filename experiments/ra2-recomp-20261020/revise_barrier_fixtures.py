"""为原版墙体试验启用所属国家的 WallOwner，防止墙体被建为无主敌对障碍。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
folder = ROOT / 'evidence/movement-state-v4/fixtures'
for name in ['wall-line', 'budget-ring', 'allied-gate']:
    source = (folder / (name + '.MAP')).read_text(encoding='ascii')
    start = source.index('[Player]\n')
    end = source.index('\n[', start + 1)
    old = source[start:end]
    assert 'WallOwner=no' in old
    source = source[:start] + old.replace('WallOwner=no', 'WallOwner=yes') + source[end:]
    target = folder / (name + '-owned.MAP')
    assert not target.exists()
    target.write_text(source, encoding='ascii', newline='\n')
