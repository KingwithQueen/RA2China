"""Use the unchanged strict fixture runner/comparator with only its host path replaced."""
from pathlib import Path
R=Path(__file__).resolve().parent
source=(R/'run_fixture_comparison.py').read_text(encoding='utf-8')
old="exe = ROOT / 'ra2/build-original-c/ra2.exe'"
assert source.count(old)==1
source=source.replace(old,"exe = ROOT / 'evidence/movement-state-v23/connection-fixture-probe.exe'")
exec(compile(source,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))
