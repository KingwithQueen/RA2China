"""Observe bounded resolver first-call records during ordinary occupied bridge traffic."""
from pathlib import Path
R=Path(__file__).resolve().parent
t=(R/'run_fixture_comparison.py').read_text(encoding='utf-8')
t=t.replace("exe = ROOT / 'ra2/build-original-c/ra2.exe'","exe = ROOT / 'evidence/movement-state-v36/connection-fixture-probe.exe'")
marker='for order in args.order:';assert t.count(marker)==1
t=t.replace(marker,"""aliases=sorted(e['entry'] for e in json.loads((ROOT/'evidence/movement-state-v36/internal-alias-sources.json').read_text(encoding='utf-8'))['entries'] if e['entry_kind']=='alias')
        group=int(args.tag.rsplit('-',1)[1]);selected=aliases[group*5:(group+1)*5];assert selected and len(selected)<=5
        if group==5 and '004A24F0' not in selected:selected.append('004A24F0')
        assert len(selected)<=5
        for address in ['004A1000','004A2670','00703040']+selected:cmd+=['--probe','0x'+address]
        for order in args.order:""")
exec(compile(t,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))
