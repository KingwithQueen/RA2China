"""Bind the death tail, original assets, compressed archives and actual native gate."""
from combat_batch_v71 import *
import re
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==188 and len(receipt['inputs'])==325 and receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')['inputs'];changed=[];added=[]
for p,d in receipt['inputs'].items():
    assert sha(Path(p))==d,p;rel=Path(p).relative_to(R).as_posix()
    if p not in old:added.append(rel)
    elif old[p]!=d:changed.append(rel)
assert changed==['ra2/src/recomp/gen_game/recomp_0029.c']
assert set(added)=={'ra2/src/'+x for x in ['gameplay/combat_death.c','gameplay/combat_death.h','runtime/combat_death_bridge.c','runtime/combat_death_bridge.h']}
rel='ra2/src/recomp/gen_game/recomp_0029.c';before=(S/'baseline'/rel).read_bytes();after=(R/rel).read_bytes();eol=b'\r\n' if b'\r\n' in before else b'\n'
block='''    {
        RECOMP_REGS_OUT(); RECOMP_FLAGS_OUT();
        ra2_combat_death_bridge();
        RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
        return;
    }
'''.encode().replace(b'\n',eol)
assert after==b'#include "combat_death_bridge.h"'+eol+before.replace(b'L_005D3E68:'+eol,b'L_005D3E68:'+eol+block)
rel='ra2/CMakeLists.txt';assert (R/rel).read_bytes()==(S/'baseline'/rel).read_bytes()+b'\ntarget_sources(ra2 PRIVATE src/gameplay/combat_death.c src/runtime/combat_death_bridge.c)\nset_source_files_properties(src/gameplay/combat_death.c src/runtime/combat_death_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
assert not [x for x in read(R/'ra2/work/game/functions.json')['functions'] if 0x5D3E68<x['address']<0x5D4157]
guards=defs=0
for p in receipt['inputs']:
    p=Path(p)
    if p.parent==R/'ra2/src/recomp/gen_game' and re.fullmatch(r'recomp_[0-9]+\.c',p.name):
        t=p.read_text(encoding='utf-8');guards+=len(re.findall(r'ra2_recovery_unimplemented\(0x[0-9A-Fa-f]+',t));defs+=len(re.findall(r'(?m)^void [A-Za-z_0-9]+\(void\)\s*\{',t))
assert (guards,defs)==(37,23117)
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256']
for label,body in [('baseline',before),('final',after)]:
    p=S/('baseline-observer/death_generated.c' if label=='baseline' else 'observer-build/death_generated.c');assert p.read_bytes()==body.replace(b'void WaveClass__virtual_86(void) {',b'void observed_health_original(void) {')
probe=read(S/'death-probe-final.log');assert probe['passed'] and probe['death_cases']==131072
write(S/'native-validation.json',dict(passed=True,result=probe,exe_sha256=sha(S/'death_probe.exe'),original_sha256=sha(R/'ra2/game/game.exe'),inputs=[dict(path=str(p),sha256=sha(p)) for p in [S/'death_probe.c',S/'native_probe_host.h',R/'ra2/src/gameplay/combat_death.c',R/'ra2/src/gameplay/combat_death.h',R/'ra2/src/runtime/combat_death_bridge.c',R/'ra2/src/runtime/combat_death_bridge.h',R/'ra2/src/compat/x87_arithmetic.c',R/'ra2/src/compat/x87_arithmetic.h']],real_tail_and_ftol=True,engine_callbacks_mocked=True,special_fraction=.25,posture_bit_is_not_lifetime_recovery_marker=True))
write(S/'source-preservation.json',dict(passed=True,changed_compile_inputs=changed,added_compile_inputs=added,c_sources=188,headers=137,compile_inputs=325,guard_sites=guards,generated_definitions=defs,entry='005D3E68',end='005D4157',original_size=751,original_statements_and_labels_retained=True,health_damage_movement_and_shared_numeric_sources_unchanged=True,internal_entries_removed=False,protected_files=28,parent_archive_files=len(read(O/'source-manifest.json')),production_recorder_comparator_and_original_rules_preserved=True))
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:shutil.copy2(O/n,S/n)
sd=R/'evidence/storage-review-v1';v=read(sd/'validation.json');assert v['passed'] and read(sd/'postcheck.json')['passed'] and sha(sd/'journal.jsonl')==v['journal_sha256'] and (R/'evidence').stat().st_file_attributes&0x800
write(S/'storage-review.json',dict(passed=True,saved_bytes=v['saved_bytes'],free_before=v['free_before'],free_after_storage=v['free_after'],files=v['files'],all_paths_and_bytes_retained=True,report=str(P/'docs/存储占用核查与无损整理-20261026.txt'),bindings=[dict(path=str(p),sha256=sha(p)) for p in [sd/'plan.json',sd/'validation.json',sd/'postcheck.json',sd/'journal.jsonl',R/'storage_review_v71.py',P/'docs/存储占用核查与无损整理-20261026.txt']]))
print(dict(passed=True,c_sources=188,inputs=325,guards=37,native_cases=131072,storage_saved_GiB=round(v['saved_bytes']/2**30,2)))
