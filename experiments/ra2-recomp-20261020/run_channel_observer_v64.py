"""Unchanged strict comparator, isolated readonly channel observer executable."""
from pathlib import Path
R=Path(__file__).resolve().parent
t=(R/'run_fixture_comparison.py').read_text(encoding='utf-8');old="exe = ROOT / 'ra2/build-original-c/ra2.exe'";assert t.count(old)==1
t=t.replace(old,"exe = ROOT / 'evidence/movement-state-v64/channel-observer.exe'")
exec(compile(t,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))
