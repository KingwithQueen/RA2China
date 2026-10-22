from pathlib import Path
ROOT = Path(__file__).resolve().parent
folder = ROOT / 'evidence/movement-state-v4/fixtures'
target = folder / 'dynamic-trucka.MAP'
assert not target.exists()
source = (folder / 'empty.MAP').read_text(encoding='ascii')
assert 'Player House,HTNK,' in source
target.write_text(source.replace('Player House,HTNK,', 'Player House,TRUCKA,'), encoding='ascii', newline='\n')
