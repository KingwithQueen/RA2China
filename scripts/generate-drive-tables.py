"""只读原版 1.006 数值轨迹，生成纯 C 的坐标表；不复制或执行游戏机器码。"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from native_reference import Native
import struct

n = Native()
points, records = [], [(0, 0, -1, 0, -1)]
for index in range(1, 7):
    pointer, jump, entry, middle = struct.unpack('<Iiii', n.uc.mem_read(0x7a00a0+index*16, 16))
    start = len(points)
    while True:
        point = struct.unpack('<iiI', n.uc.mem_read(pointer+12*(len(points)-start), 12))
        points.append(point)
        if point[0] == point[1] == 0: break
        assert len(points)-start < 100
    records.append((start, len(points)-start, jump, entry, middle))
controls=[]
for index in range(64):
    raw, turn, direction, flags = struct.unpack('<BB2xII', n.uc.mem_read(0x7a0180+index*12, 12))
    assert raw <= 6
    controls.append((raw, direction, flags))
text = ['/* 原版 1.006 的普通履带数值轨迹；由 scripts/generate-drive-tables.py 只读生成。 */',
        'static const battle_track_point track_points[] = {']
for x,y,d in points: text.append(f'    {{{x}, {y}, {d}}},')
text += ['};', 'static const battle_track tracks[7] = {']
for row in records: text.append('    {'+', '.join(map(str,row))+'},')
text += ['};', 'static const battle_track_control track_controls[64] = {']
for row in controls: text.append('    {'+', '.join(map(str,row))+'},')
text += ['};', '']
Path('src/battle_tracks.inc').write_text('\n'.join(text), encoding='utf-8', newline='\n')
print('generated points', len(points), 'controls', len(controls))
