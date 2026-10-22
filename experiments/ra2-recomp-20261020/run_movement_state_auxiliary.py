"""复用诊断关闭/失败保护场景，保留第一批可读代码阶段的原始证据。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'run_state_auxiliary.py').read_text(encoding='utf-8')
old = "OUT = ROOT / 'evidence/state-step-v1/auxiliary-final'"
assert source.count(old) == 1
source = source.replace(old, "OUT = ROOT / 'evidence/movement-state-v2/auxiliary-final'")
exec(compile(source, str(ROOT / 'run_state_auxiliary.py'), 'exec'), {'__file__': str(ROOT / 'run_state_auxiliary.py'), '__name__': '__main__'})
