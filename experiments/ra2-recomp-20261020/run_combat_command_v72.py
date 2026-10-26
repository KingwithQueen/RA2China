from pathlib import Path
R=Path(__file__).resolve().parent
from lifecycle_fixture_v72 import fixture_source
source=fixture_source()
old="exe = ROOT / 'ra2/build-original-c/ra2.exe'"
assert source.count(old)==1
source=source.replace(old,"exe = ROOT / 'evidence/combat-state-v4/combat-command.exe'")
exec(compile(source,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))
