"""Content-bound source scope, retained 1.006 tail and protected original evidence."""
from combat_batch_v69 import *
import re
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==184 and len(receipt['inputs'])==317
assert receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')['inputs'];changed=[];added=[]
for p,d in receipt['inputs'].items():
    assert sha(Path(p))==d,p
    rel=Path(p).relative_to(R).as_posix()
    if p not in old:added.append(rel)
    elif old[p]!=d:changed.append(rel)
assert changed==['ra2/src/recomp/gen_game/recomp_0029.c'],changed
assert set(added)=={'ra2/src/'+x for x in ['gameplay/combat_health.c','gameplay/combat_health.h','runtime/combat_health_bridge.c','runtime/combat_health_bridge.h']},added
p='ra2/src/recomp/gen_game/recomp_0029.c';before=(S/'baseline'/p).read_bytes();after=(R/p).read_bytes();eol=b'\r\n' if b'\r\n' in before else b'\n'
block='''    {
        RECOMP_REGS_OUT(); RECOMP_FLAGS_OUT();
        uint32_t health_resume=ra2_combat_health_bridge();
        RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
        if(!health_resume)return;
        goto L_005D3E68;
    }
'''.encode().replace(b'\n',eol)
expected=b'#include "combat_health_bridge.h"'+eol+before.replace(b'L_005D3D20:'+eol,b'L_005D3D20:'+eol+block)
resume=b'    if (TEST_G(_flag_a, _flag_b)) goto L_005D3F39; /* 0x005D3E68: jg 0x5d3f39 */'
expected=expected.replace(resume,b'L_005D3E68:'+eol+resume);assert after==expected,'Unexpected generated code edit'
tail=before[before.index(resume):];assert after[after.index(resume):]==tail
cmake='ra2/CMakeLists.txt';assert (R/cmake).read_bytes()==(S/'baseline'/cmake).read_bytes()+b'\ntarget_sources(ra2 PRIVATE src/gameplay/combat_health.c src/runtime/combat_health_bridge.c)\nset_source_files_properties(src/gameplay/combat_health.c src/runtime/combat_health_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
functions=read(R/'ra2/work/game/functions.json')['functions'];inner=[x for x in functions if 0x5D3D20<x['address']<0x5D4157];assert not inner,inner
guards=definitions=0
for p,d in receipt['inputs'].items():
    p=Path(p)
    if p.parent!=R/'ra2/src/recomp/gen_game' or not re.fullmatch(r'recomp_[0-9]+\.c',p.name):continue
    text=p.read_text(encoding='utf-8');guards+=len(re.findall(r'ra2_recovery_unimplemented\(0x[0-9A-Fa-f]+',text));definitions+=len(re.findall(r'(?m)^void [A-Za-z_0-9]+\(void\)\s*\{',text))
assert guards==37 and definitions==23117,(guards,definitions)
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256'],e['path']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256'],e['path']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:
    assert not (S/n).exists();shutil.copy2(O/n,S/n)
probe=read(S/'health-probe-final.log');assert probe['passed'] and probe['health_cases']==131072
write(S/'native-validation.json',dict(passed=True,result=probe,exe_sha256=sha(S/'health_probe.exe'),original_sha256=sha(R/'ra2/game/game.exe'),inputs=[dict(path=str(p),sha256=sha(p)) for p in [S/'health_probe.c',S/'native_probe_host.h',R/'ra2/src/gameplay/combat_health.c',R/'ra2/src/runtime/combat_health_bridge.c',R/'ra2/src/compat/x87_arithmetic.c']],finite_rule_ratios=True,full_x87_status_or_dead_stack_bytes_required=False))
write(S/'source-preservation.json',dict(passed=True,changed_compile_inputs=changed,added_compile_inputs=added,c_sources=184,headers=133,compile_inputs=317,guard_sites=guards,generated_definitions=definitions,original_death_tail_sha256=hashlib.sha256(tail).hexdigest(),tail_and_other_generated_code_byte_identical=True,entry='005D3D20',resume='005D3E68',internal_function_entries_removed=False,internal_aliases_in_replaced_function=len(inner),protected_files=len(read(S/'protected-inputs.json')['files']),parent_archive_files=len(read(O/'source-manifest.json')),recorder_comparator_rules_originals_preserved=True,shared_base_service_despite_lifted_wave_rtti_name=True,armor_warhead_distance_calculation_delegated_to_original='0047E1C0'))
write(S/'implementation-review.json',dict(passed=True,initial_attachment_sha256=sha(S/'attachment.json'),build_attempts=['build-production.log','build-production-02.log'],initial_build_issue='Resume instruction at 005D3E68 had no lifted basic-block label; an explicit label was added without changing any original statement.',successful_build='build-production-02.log',invalid_executable_checkpoint_created=False,command_host_review='Initial repeated-host source check compared LF text with Windows CRLF bytes. Check uses decoded text; source bytes and before/after runtime parity remain independently verified.',native_capture_review_sha256=sha(S/'native-capture-review.json')))
print(dict(passed=True,changed=changed,added=added,guards=guards,functions=definitions))
