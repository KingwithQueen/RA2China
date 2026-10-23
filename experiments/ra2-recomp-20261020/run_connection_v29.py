"""Use the unchanged strict fixture runner/comparator with only its host path replaced."""
from pathlib import Path
R=Path(__file__).resolve().parent
source=(R/'run_fixture_comparison.py').read_text(encoding='utf-8')
old="exe = ROOT / 'ra2/build-original-c/ra2.exe'"
assert source.count(old)==1
source=source.replace(old,"exe = ROOT / 'evidence/movement-state-v29/connection-fixture-probe.exe'")
source=source.replace("for order in args.order:", "probe_groups=[['4A1000','4A2670','703040','4A12F1','4A134F','4A161D','4A166A','4A17A2'],['4A1000','4A2670','703040','4A32B4','70346B','70372C','7038EF']]\n        probe_group=0 if any(order.endswith((':72',':68')) for order in args.order) else 1\n        for address in probe_groups[probe_group]:\n            cmd += ['--probe', '0x'+address]\n        for order in args.order:")
exec(compile(source,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))
