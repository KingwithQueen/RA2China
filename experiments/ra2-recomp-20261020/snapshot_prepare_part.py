"""复用聚焦快照规则，第三批证据独立保存。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
(ROOT / 'evidence/movement-prepare-v3/parts').mkdir(exist_ok=True)
source = (ROOT / 'preserve_movement_part.py').read_text(encoding='utf-8')
assert source.count("'evidence/movement-state-v2'") == 1
source = source.replace("'evidence/movement-state-v2'", "'evidence/movement-prepare-v3'")
exec(compile(source, str(ROOT / 'preserve_movement_part.py'), 'exec'), {'__file__': str(ROOT / 'preserve_movement_part.py'), '__name__': '__main__'})
