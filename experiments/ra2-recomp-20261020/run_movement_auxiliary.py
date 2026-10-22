"""复用既有诊断关闭/失败保护场景，但输出到本轮独立证据目录。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'run_state_auxiliary.py').read_text(encoding='utf-8')
old = "OUT = ROOT / 'evidence/state-step-v1/auxiliary-final'"
assert source.count(old) == 1
source = source.replace(old, "OUT = ROOT / 'evidence/movement-readable-v1/auxiliary-final'")
exec(compile(source, str(ROOT / 'run_state_auxiliary.py'), 'exec'), {'__file__': str(ROOT / 'run_state_auxiliary.py'), '__name__': '__main__'})
