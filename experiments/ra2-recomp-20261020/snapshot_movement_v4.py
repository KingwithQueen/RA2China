"""第四批可回退节点；在已有聚焦快照规则上增加显式试验入口源码。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
(ROOT / 'evidence/movement-state-v4/parts').mkdir(exist_ok=True)
source = (ROOT / 'preserve_movement_part.py').read_text(encoding='utf-8')
assert source.count("'evidence/movement-state-v2'") == 1
source = source.replace("'evidence/movement-state-v2'", "'evidence/movement-state-v4'")
source = source.replace("paths.update(['ra2/build-original-c/ra2.exe'", "paths.update(['ra2/src/runtime/movement_fixture.c', 'ra2/src/runtime/movement_fixture.h', 'ra2/build-original-c/ra2.exe'")
exec(compile(source, str(ROOT / 'preserve_movement_part.py'), 'exec'), {'__file__': str(ROOT / 'preserve_movement_part.py'), '__name__': '__main__'})
