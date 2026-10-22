"""第三批的诊断关闭菜单、错误对象失败保护，保留旧证据。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'run_state_auxiliary.py').read_text(encoding='utf-8')
old = "OUT = ROOT / 'evidence/state-step-v1/auxiliary-final'"
assert source.count(old) == 1
source = source.replace(old, "OUT = ROOT / 'evidence/movement-state-v4/auxiliary-final'")
exec(compile(source, str(ROOT / 'run_state_auxiliary.py'), 'exec'), {'__file__': str(ROOT / 'run_state_auxiliary.py'), '__name__': '__main__'})
