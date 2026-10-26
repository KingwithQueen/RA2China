"""Content-bound source scope, original statements, fixed assets and actual native gate."""
from combat_batch_v70 import *
import re
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==186 and len(receipt['inputs'])==321
assert receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')['inputs'];changed=[];added=[]
for p,d in receipt['inputs'].items():
    assert sha(Path(p))==d,p
    rel=Path(p).relative_to(R).as_posix()
    if p not in old:added.append(rel)
    elif old[p]!=d:changed.append(rel)
assert changed==['ra2/src/recomp/gen_game/recomp_0007.c'],changed
assert set(added)=={'ra2/src/'+x for x in ['gameplay/combat_damage.c','gameplay/combat_damage.h','runtime/combat_damage_bridge.c','runtime/combat_damage_bridge.h']},added
rel='ra2/src/recomp/gen_game/recomp_0007.c';before=(S/'baseline'/rel).read_bytes();after=(R/rel).read_bytes();eol=b'\r\n' if b'\r\n' in before else b'\n'
block='''    {
        RECOMP_REGS_OUT(); RECOMP_FLAGS_OUT();
        ra2_combat_damage_bridge();
        RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
        return;
    }
'''.encode().replace(b'\n',eol)
assert after==b'#include "combat_damage_bridge.h"'+eol+before.replace(b'L_0047E1C0:'+eol,b'L_0047E1C0:'+eol+block)
rel='ra2/CMakeLists.txt';assert (R/rel).read_bytes()==(S/'baseline'/rel).read_bytes()+b'\ntarget_sources(ra2 PRIVATE src/gameplay/combat_damage.c src/runtime/combat_damage_bridge.c)\nset_source_files_properties(src/gameplay/combat_damage.c src/runtime/combat_damage_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
functions=read(R/'ra2/work/game/functions.json')['functions'];assert not [x for x in functions if 0x47E1C0<x['address']<0x47E2AD]
guards=definitions=0
for p,d in receipt['inputs'].items():
    p=Path(p)
    if p.parent!=R/'ra2/src/recomp/gen_game' or not re.fullmatch(r'recomp_[0-9]+\.c',p.name):continue
    text=p.read_text(encoding='utf-8');guards+=len(re.findall(r'ra2_recovery_unimplemented\(0x[0-9A-Fa-f]+',text));definitions+=len(re.findall(r'(?m)^void [A-Za-z_0-9]+\(void\)\s*\{',text))
assert (guards,definitions)==(37,23117)
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256']
for label,source in [('baseline',before),('final',after)]:
    p=S/('baseline-observer/damage_generated.c' if label=='baseline' else 'observer-build/damage_generated.c')
    assert p.read_bytes()==source.replace(b'void sub_0047E1C0(void) {',b'void observed_damage_original(void) {')
probe=read(S/'damage-probe-final.log');assert probe['passed'] and probe['damage_cases']==262146 and probe['neighbor_results']==[179,180]
write(S/'native-validation.json',dict(passed=True,result=probe,exe_sha256=sha(S/'damage_probe.exe'),original_sha256=sha(R/'ra2/game/game.exe'),inputs=[dict(path=str(p),sha256=sha(p)) for p in [S/'damage_probe.c',S/'native_probe_host.h',R/'ra2/src/gameplay/combat_damage.c',R/'ra2/src/gameplay/combat_damage.h',R/'ra2/src/runtime/combat_damage_bridge.c',R/'ra2/src/runtime/combat_damage_bridge.h',R/'ra2/src/compat/x87_arithmetic.c',R/'ra2/src/compat/x87_arithmetic.h']],finite_bounded_numeric_contract=True,actual_original_damage_and_integer_conversion=True,dead_x87_register_contents_required=False))
write(S/'source-preservation.json',dict(passed=True,changed_compile_inputs=changed,added_compile_inputs=added,c_sources=186,headers=135,compile_inputs=321,guard_sites=guards,generated_definitions=definitions,original_statements_and_labels_retained=True,entry='0047E1C0',original_size=237,original_instructions=75,internal_entries_removed=False,health_death_shared_numeric_and_movement_files_unchanged=True,protected_files=len(read(S/'protected-inputs.json')['files']),parent_archive_files=len(read(O/'source-manifest.json')),recorder_comparator_and_original_rules_preserved=True))
write(S/'observer-scope.json',dict(passed=True,generated_source_path=str(S/'observer-build/damage_generated.c'),generated_source_sha256=sha(S/'observer-build/damage_generated.c'),only_one_definition_renamed=True,production_dispatch_unchanged=True,native_entry_and_positive_exit_sites=['0047E1C0','0047E299','0047E2A5'],scope='Entry/result observer used only for the three new nonnegative rifle/splash scenes. Existing healing/immunity/combat regressions use the command-only host and production records; actual negative branches are separately covered by the native probe.',inherited_command_source_sha256=sha(S/'combat_command.c'),initial_observer_generated_source_relocated_to_ignored_build_folder=True))
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:shutil.copy2(O/n,S/n)
print(dict(passed=True,changed=changed,added=added,guards=guards,functions=definitions))
