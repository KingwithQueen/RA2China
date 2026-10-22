"""为原版触发器补上独立 Tag，保留前两次地图及运行记录。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
folder = ROOT / 'evidence/movement-state-v6/fixtures'
source = (folder / 'chrono-team-02.MAP').read_text(encoding='ascii')
source += '\n[Tags]\n06F00005=0,Chrono trial,06F00004\n'
target = folder / 'chrono-team-03.MAP'
assert not target.exists()
target.write_text(source, encoding='ascii', newline='\n')
