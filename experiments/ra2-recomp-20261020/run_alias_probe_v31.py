"""Use the unchanged comparator and ordinary scenes with thirteen additional resolver probes."""
from pathlib import Path
R=Path(__file__).resolve().parent
source=(R/'run_fixture_comparison.py').read_text(encoding='utf-8')
needle="exe = ROOT / 'ra2/build-original-c/ra2.exe'";assert source.count(needle)==1
source=source.replace(needle,"exe = ROOT / 'evidence/movement-state-v31/connection-fixture-probe.exe'")
needle='for order in args.order:';assert source.count(needle)==1
source=source.replace(needle,"""groups={'a':['4A199D','4A1ACD','4A1F8D','4A1FA1','4A3C92'],'b':['4A3C9B','4A3DBA','4A3E35','4A3FE3','4A4174'],'c':['4A458C','4A45B7','4A45D0','4A230E','4A2311'],'d':['4A1FDC','4A2112']}
        for address in ['4A1000','4A2670','703040']+groups[args.tag[-1]]:
            cmd += ['--probe','0x'+address]
        for order in args.order:""")
exec(compile(source,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))
