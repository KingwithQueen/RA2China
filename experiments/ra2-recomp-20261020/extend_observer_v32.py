"""Keep all accepted byte-checked hooks; extend only the observed actor allowlist."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
t=(S/'baseline/evidence/movement-state-v31/connection_observer.c').read_text(encoding='utf-8')
m='if(id!=1023363&&id!=1023362&&';assert t.count(m)==1
t=t.replace(m,'if(id!=1023367&&id!=1023363&&id!=1023362&&')
(S/'connection_observer.c').write_text(t,encoding='utf-8',newline='\n')
print('Kept accepted hooks and added actual moving infantry ID')
