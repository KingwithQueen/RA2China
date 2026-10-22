from pathlib import Path
ROOT = Path(__file__).resolve().parent
source = (ROOT/'run_state_auxiliary.py').read_text(encoding='utf-8')
source = source.replace("OUT = ROOT / 'evidence/state-step-v1/auxiliary-final'",
                        "OUT = ROOT / 'evidence/movement-state-v11/auxiliary-final-01'")
exec(compile(source,str(ROOT/'run_state_auxiliary.py'),'exec'),{'__file__':str(ROOT/'run_state_auxiliary.py'),'__name__':'__main__'})
