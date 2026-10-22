"""预算压力图只将原版 CloseEnough 改为零，防止邻格失败被提前近距离停止吞掉。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
folder = ROOT / 'evidence/movement-state-v4/fixtures'
target = folder / 'budget-stress.MAP'
assert not target.exists()
source = (folder / 'dynamic-trucka.MAP').read_text(encoding='ascii')
assert '[General]' not in source
target.write_text(source + '\n[General]\nCloseEnough=0.0\n', encoding='ascii', newline='\n')
