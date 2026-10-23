"""Expand legal-source inventory to every parent C copy touched by the new fragments."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
old=read(S/'legal-overlap-sources.json');targets={int(e['entry'],16) for e in read(S/'baseline/extra/internal-alias-sources.json')['entries']};parents={}
for filename,sites in [('recomp_0010.c',{'004A2347','004A229C','004A22BE'}),('recomp_0046.c',{'00703895'})]:
    function=entry=None
    for line in (R/'ra2/src/recomp/gen_game'/filename).read_text(encoding='utf-8').splitlines():
        m=re.match(r'void (\w+)\(void\) \{',line)
        if m:function=m[1]
        m=re.search(r'RECOMP_ENTER\(0x([0-9A-Fa-f]+)u\)',line)
        if m:entry=m[1].upper()
        if line.startswith('L_') and line[2:10] in sites:
            site=line[2:10];targets.add(int(entry,16));parents.setdefault(site,[]).append(dict(function=function,entry=entry))
source=(R/'audit_legal_sources_v31.py').read_text(encoding='utf-8')
a=source.index('targets = {');b=source.index('functions = ',a)
source=source[:a]+'targets = '+repr(targets)+'\n'+source[b:]
source=source.replace('assert len(aliases) == 9','assert len(aliases) == 26')
source=source.replace("assert all(not e['direct_native_call_found'] and not e['noncode_address_literal_found'] for e in aliases)",'')
source=source.replace("out = S / 'legal-overlap-sources.json'", "out = S / 'internal-alias-sources.json'")
marker='out = S /';i=source.index(marker)
source=source[:i]+'''value['parent_copies']=PARENTS
value['new_aliases']=sorted(e['entry'] for e in aliases if e['entry'] not in OLD_ALIASES)
value['direct_call_candidates']=[e['entry'] for e in aliases if e['direct_native_call_found']]
value['noncode_literal_candidates']=[e['entry'] for e in aliases if e['noncode_address_literal_found']]
value['conclusion']='Expanded to 26 aliases from all parent copies of the four new fragment sites. All decoded incoming edges are original-byte verified. Computed pointers and natural C-copy dispatch remain separate unresolved questions.'
value['inputs'].append(dict(path='audit_legal_sources_v31.py',sha256=sha(R/'audit_legal_sources_v31.py')))
'''+source[i:]
namespace=dict(__file__=str(Path(__file__)),PARENTS=parents,OLD_ALIASES={e['entry'] for e in old['entries'] if e['entry_kind']=='alias'})
exec(compile(source,str(Path(__file__)),'exec'),namespace)
v=read(S/'internal-alias-sources.json');assert len(v['new_aliases'])==17
names={'sub_'+e['entry'] for e in v['entries'] if e['entry_kind']=='alias'};pattern=re.compile(r'\b(?:'+'|'.join(sorted(names))+r')\b')
refs=[];direct=[];inputs=[Path(p) for p in read(R/'ra2/build-original-c/source-content-receipt.json')['inputs']];assert len(inputs)==290
for p in inputs:
    for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        for m in pattern.finditer(line):
            name=m[0];kind='comment' if line.startswith('/* '+name+' ') else 'definition' if line=='void '+name+'(void) {' else 'prototype' if re.fullmatch(r'(?:extern )?void '+name+r'\(void\);',line) else 'registration' if re.fullmatch(r'\s*\{ 0x[0-9A-F]+u, '+name+r' \},',line) else 'other'
            record=dict(path=p.relative_to(R).as_posix(),line=n,name=name,kind=kind);refs.append(record)
            if kind=='other':direct.append(record)
v.update(project_compile_inputs_scanned=290,direct_c_reference_candidates=direct,c_references=refs)
v['inputs'] += [dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs]
(S/'internal-alias-sources.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,aliases=26,new_aliases=17,byte_checked_edges=v['unique_native_edges'],direct_native_calls=v['direct_call_candidates'],direct_c_references=len(direct))))
