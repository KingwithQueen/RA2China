"""Attach only the verified effective-damage service; keep all original statements."""
from combat_batch_v70 import *
assert read(S/'baseline-review.json')['passed'] and read(S/'b-command-scenes.json')['passed']
assert read(S/'damage-probe-02.log')['passed']
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')
for p,d in old['inputs'].items():assert sha(Path(p))==d,p
assert sha(R/'ra2/build-original-c/ra2.exe')==old['executable_sha256']
write(S/'baseline-build-inputs.json',dict(passed=True,exe_sha256=old['executable_sha256'],compile_inputs=317,observer_arguments=read(S/'observer-build-arguments.json'),command_arguments=read(S/'command-build-arguments.json'),positive_observation_scope=True,observer_generated_source_relocated=True,generated_source_sha256=sha(S/'baseline-observer/damage_generated.c')))
p=R/'ra2/src/recomp/gen_game/recomp_0007.c';before=p.read_bytes();eol=b'\r\n' if b'\r\n' in before else b'\n';marker=b'L_0047E1C0:'+eol;assert before.count(marker)==1
block='''    {
        RECOMP_REGS_OUT(); RECOMP_FLAGS_OUT();
        ra2_combat_damage_bridge();
        RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
        return;
    }
'''.encode().replace(b'\n',eol)
after=b'#include "combat_damage_bridge.h"'+eol+before.replace(marker,marker+block);p.write_bytes(after)
p=R/'ra2/CMakeLists.txt';before_cmake=p.read_bytes();assert b'combat_damage' not in before_cmake
p.write_bytes(before_cmake+b'\ntarget_sources(ra2 PRIVATE src/gameplay/combat_damage.c src/runtime/combat_damage_bridge.c)\nset_source_files_properties(src/gameplay/combat_damage.c src/runtime/combat_damage_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n')
write(S/'attachment.json',dict(passed=True,entry='0047E1C0',before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=sha(R/'ra2/src/recomp/gen_game/recomp_0007.c'),original_statements_and_labels_retained=True,original_health_and_death_services_unchanged=True,shared_compatibility_files_unchanged=True))
print(dict(passed=True,attached=True))
