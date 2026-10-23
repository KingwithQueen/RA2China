"""Retain all accepted read-only hooks and include the second ordinary traffic actor."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
t=(R/'evidence/movement-state-v29/connection_observer.c').read_text(encoding='utf-8')
needle='if(id!=1023362&&id!=1022579&&';assert t.count(needle)==1
t=t.replace(needle,'if(id!=1023363&&id!=1023362&&id!=1022579&&')
(S/'connection_observer.c').write_text(t,encoding='utf-8',newline='\n')
print('Observer retains twelve replacements and includes traffic actor1023363')
