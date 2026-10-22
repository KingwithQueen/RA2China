"""从本存档真实格数据中选择邻域为水面的远目标，不假设某坐标属于水面。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-prepare-v3'
source = STAGE / 'runs/cell-catalog/original/cells.json'
catalog = json.loads(source.read_text(encoding='utf-8'))
cells = {tuple(item['cell']): item for item in catalog['cells']}
origin = (67, 114)
candidates = []
for point, item in cells.items():
    distance = abs(point[0] - origin[0]) + abs(point[1] - origin[1])
    if item['land'] != 2 or item['bridge'] or not 16 <= distance <= 50:
        continue
    neighborhood = [cells.get((point[0] + dx, point[1] + dy)) for dx in range(-2, 3) for dy in range(-2, 3)]
    if all(cell and cell['land'] == 2 and not cell['bridge'] for cell in neighborhood):
        candidates.append((distance, point))
assert candidates
distance, target = min(candidates)
result = {'catalog': str(source), 'source_frame': catalog['frame'], 'object_id': 1032240, 'origin_cell': origin,
    'target_cell': target, 'manhattan_cell_distance': distance, 'all_25_neighbor_cells_land_2_without_bridge': True,
    'land_2_water_evidence': '原版 Process 水面尾迹使用 Cell+0xEC==2；本轮未改变地形或可通行条件。'}
path = STAGE / 'blocked-route-selection.json'
assert not path.exists()
path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
