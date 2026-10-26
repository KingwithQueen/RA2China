"""Add optional private ART.INI replacement to the unchanged fixture runner."""
from pathlib import Path
R=Path(__file__).resolve().parent
def fixture_source():
    source=(R/'run_fixture_comparison.py').read_text(encoding='utf-8')
    marker="    ap.add_argument('--scenario-rules', type=Path)";assert source.count(marker)==1
    source=source.replace(marker,marker+"\n    ap.add_argument('--scenario-art', type=Path)")
    marker="        save = game / 'SAVE0029.SAV'";assert source.count(marker)==1
    code="""        if args.scenario_art:
            assert game.resolve().is_relative_to(out.resolve())
            temporary = game / 'art-fixture-new.tmp'
            with temporary.open('xb') as stream:stream.write(args.scenario_art.read_bytes())
            temporary.replace(game / 'ART.INI')
"""
    source=source.replace(marker,code+marker)
    marker="    if all(r['passed'] for r in runs):";assert source.count(marker)==1
    source=source.replace(marker,"    if args.scenario_art:\n        report['scenario_art']=str(args.scenario_art)\n        report['scenario_art_sha256']=sha(args.scenario_art)\n"+marker)
    return source
