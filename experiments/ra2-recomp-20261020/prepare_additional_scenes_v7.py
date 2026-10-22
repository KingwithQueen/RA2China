"""复用原版真实坡地及地图对象解析；不改原始地形/规则。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
folder = ROOT/'evidence/movement-state-v7/fixtures'
base = (ROOT/'evidence/movement-state-v4/fixtures/empty.MAP').read_text(encoding='ascii')
for name,health in [('slope-healthy',256),('slope-damaged',64)]:
    target = folder/(name+'.MAP')
    data = base.replace('HTNK,256,67,114','HTNK,'+str(health)+',94,120')
    if target.exists():
        assert target.read_text(encoding='ascii')==data
    else:
        target.write_text(data,encoding='ascii',newline='\n')
base = (ROOT/'evidence/movement-state-v6/fixtures/chrono-team-03.MAP').read_text(encoding='ascii')
base = base.replace('06F00004=1,13,0,3','06F00004=1,13,0,0')
for name, data in [('chrono-immediate',base),('chrono-team-reference',
    base.replace('1,107,0,06F00001','1,107,1,06F00001'))]:
    target = folder/(name+'.MAP')
    if target.exists():
        assert target.read_text(encoding='ascii')==data
    else:
        target.write_text(data,encoding='ascii',newline='\n')
