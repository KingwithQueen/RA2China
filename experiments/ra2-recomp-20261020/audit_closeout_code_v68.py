"""Compile-bound movement inventory and bounded treatment of original internal entries."""
from run_batch_v68 import *
import re,bisect,collections
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==182 and len(receipt['inputs'])==313
assert sha(R/'ra2/build-original-c/ra2.exe')==receipt['executable_sha256']
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')['inputs'];changed=[];added=[]
for p,d in receipt['inputs'].items():
    assert sha(Path(p))==d,p
    rel=Path(p).relative_to(R).as_posix()
    if p not in old:added.append(rel)
    elif old[p]!=d:changed.append(rel)
expected={'ra2/src/gameplay/'+n for n in ['ground_cell_services.c','ground_cell_services.h','ground_failure_transition.c','ground_failure_transition.h','ground_prepare.c','ground_obstacle.c','ground_arrival.c','ground_collision.c']}
expected|={'ra2/src/runtime/ground_services_bridge.h','ra2/src/recomp/gen_game/recomp_0023.c'}
assert set(changed)==expected and added==['ra2/src/runtime/ground_map_bounds_bridge.c'],(changed,added)
before=(S/'baseline/ra2/src/recomp/gen_game/recomp_0023.c').read_text(encoding='utf-8');after=(R/'ra2/src/recomp/gen_game/recomp_0023.c').read_text(encoding='utf-8')
pattern=r'void sub_0055A660\(void\) \{.*?\n\}'
a=re.search(pattern,before,re.S);b=re.search(pattern,after,re.S);assert a and b
assert after=='#include "ground_services_bridge.h"\n'+before[:a.start()]+b[0]+before[a.end():]
assert (S/'map-area-generated-before.c').read_text(encoding='utf-8')==a[0]+'\n'
protected=read(S/'protected-inputs.json')['files']
for e in protected:assert sha(Path(e['path']))==e['sha256'],e['path']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256'],e['path']
for folder in ['baseline','parts/closeout']:
    for e in read(S/folder/'manifest.json'):assert sha(S/folder/e['path'])==e['sha256'],(folder,e['path'])
alias=read(O/'alias-evidence-inheritance.json');assert alias['aliases']==29
for key in ['parent_static_inventory','parent_natural_observations']:assert sha(Path(alias[key]))==alias[key+'_sha256']
entries=read(Path(alias['parent_static_inventory']))['entries']
alias_locations={e['entry']:[] for e in entries if e['entry_kind']=='alias'}
units=[];guards=[];definitions=0
for p,d in receipt['inputs'].items():
    p=Path(p)
    if p.suffix!='.c':continue
    text=p.read_text(encoding='utf-8');rel=p.relative_to(R).as_posix()
    if p.parent==R/'ra2/src/gameplay' or (p.parent==R/'ra2/src/runtime' and ('ground_' in p.name or 'movement' in p.name)):
        names=re.findall(r'(?m)^(?!static)(?:[A-Za-z_][A-Za-z_0-9]*[ \t*]+)+(ra2_[A-Za-z_0-9]+)\s*\(',text)
        units.append(dict(path=rel,sha256=d,functions=names,changed_current=rel in changed or rel in added,scope='current implementation and affected checks' if rel in changed or rel in added else 'byte-identical accepted parent; finite evidence inherited'))
    if p.parent==R/'ra2/src/recomp/gen_game':
        for address in alias_locations:
            if 'L_'+address+':' in text:
                assert old[str(p)]==d,('Alias-bearing chunk changed',rel,address)
                alias_locations[address].append(rel)
        defs=list(re.finditer(r'(?m)^void ([A-Za-z_][A-Za-z_0-9]*)\(void\)\s*\{',text));positions=[x.start() for x in defs]
        if re.fullmatch(r'recomp_[0-9]+\.c',p.name):definitions+=len(defs)
        for m in re.finditer(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',text):
            i=bisect.bisect_right(positions,m.start())-1
            guards.append(dict(path=rel,function=defs[i][1],target=m[1]))
assert len(guards)==37 and definitions==23117
prior=read(O/'progress-inventory.json')['guard_inventory']
assert sorted((g['path'],g['function'],g['target']) for g in guards)==sorted((g['path'],g['enclosing_function'],g['target']) for g in prior)
alias_checks=[]
for e in entries:
    if e['entry_kind']!='alias':continue
    address=e['entry'];found=alias_locations[address]
    assert found,address
    alias_checks.append(dict(entry=address,unchanged_chunks=found,direct_original_call=e['direct_native_call_found'],natural_nonprimary_entry_proved=False))
assert len(alias_checks)==29
rtti_path=R/'ra2/work/game/rtti.json';rtti=read(rtti_path);classes=[]
for name,meta in rtti['classes'].items():
    if name.endswith('LocomotionClass'):
        methods=[a for a,c in rtti['methods'].items() if c==name]
        classes.append(dict(class_name=name,primary_vtable=meta['vtable'],mapped_virtual_entries=methods,implementation='Original lifted C retained; ground/common named services and measured natural cases separately enumerated. Not a claim all members were rewritten.'))
assert len(classes)==12
write(S/'movement-code-inventory.json',dict(passed=True,compile_inputs=313,c_sources=182,headers=131,readable_units=units,locomotor_classes=classes,rtti_sha256=sha(rtti_path),generated_definitions=definitions,global_guard_sites=guards,guard_sites=37,guard_targets=36,alias_inventory=alias_checks,aliases=29,unused_interfaces_forced=False,all_locomotors_readably_rewritten=False,scope='Every compiled named movement file and RTTI locomotor family inventoried. Unaffected source and original internal labels retained; neither a guard nor an alias count is a count of missing movement features.'))
write(S/'source-preservation.json',dict(passed=True,changed_compile_inputs=changed,added_compile_inputs=added,compile_inputs=313,c_sources=182,headers=131,only_one_generated_function_replaced=True,generated_aliases_removed=False,guard_sites=37,protected_files=len(protected),parent_archive_files=len(read(O/'source-manifest.json')),baseline_and_valid_checkpoint_verified=True,recorder_comparator_original_assets_policy_preserved=True))
print(dict(passed=True,changed=len(changed),added=len(added),named_movement_units=len(units),locomotor_families=len(classes),guards=37,aliases=29))
