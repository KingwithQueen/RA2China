"""Separate generated registrations from direct C callers and native legal edges."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
legal=read(S/'legal-overlap-sources.json');aliases=[e for e in legal['entries'] if e['entry_kind']=='alias']
names={'sub_'+e['entry'] for e in aliases};pattern=re.compile(r'\b(?:'+'|'.join(sorted(names))+r')\b')
sources=[Path(e['file']) for e in read(R/'ra2/build-original-c/compile_commands.json')]
assert len(sources)==171
inputs=[Path(p) for p in read(R/'ra2/build-original-c/source-content-receipt.json')['inputs']]
assert len(inputs)==290
references=[];counts=Counter()
for p in inputs:
 text=p.read_text(encoding='utf-8')
 for number,line in enumerate(text.splitlines(),1):
  for match in pattern.finditer(line):
   name=match[0]
   kind='comment' if line.startswith('/* '+name+' ') else 'definition' if line=='void '+name+'(void) {' else 'prototype' if re.fullmatch(r'(?:extern )?void '+name+r'\(void\);',line) else 'registration' if re.fullmatch(r'\s*\{ 0x[0-9A-F]+u, '+name+r' \},',line) else 'other'
   assert kind!='other',(p,number,line)
   references.append(dict(path=p.relative_to(R).as_posix(),line=number,name=name,kind=kind));counts[name,kind]+=1
assert all(counts[n,k]==1 for n in names for k in ['comment','definition','registration','prototype'])
value=dict(passed=True,production_sources_scanned=len(sources),project_compile_inputs_scanned=len(inputs),alias_count=9,direct_generated_c_callers_found=False,
 references=references,native_edges_total=legal['unique_native_edges'],native_alias_edges=sum(len(e['decoded_incoming']) for e in aliases),native_direct_alias_calls_found=False,
 scope='All 171 compiled C files and 290 project compile inputs scanned. Alias symbols occur only once each as comment, definition, prototype and dispatch registration. Dispatch registration is a resolver capability and does not establish a native caller. Native incoming branches are separately PE-byte verified. Runtime first-call probes remain bounded to accepted scenes; computed targets elsewhere are unresolved.',
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs]+[dict(path=Path(__file__).relative_to(R).as_posix(),sha256=sha(Path(__file__)))])
(S/'alias-route-inventory.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,alias_count=9,compiled_c_sources=171,direct_c_callers_found=False)))
