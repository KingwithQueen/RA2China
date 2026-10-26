"""Attach only the verified damage tail, keeping every original statement and label."""
from combat_batch_v71 import *
assert read(S/'baseline-review.json')['passed'] and read(S/'input-qualification.json')['passed'] and read(S/'b-command-scenes.json')['passed']
assert read(S/'death-probe-04.log')['passed']
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')
for p,d in old['inputs'].items():assert sha(Path(p))==d,p
assert sha(R/'ra2/build-original-c/ra2.exe')==old['executable_sha256']
p=R/'ra2/src/recomp/gen_game/recomp_0029.c';before=p.read_bytes();eol=b'\r\n' if b'\r\n' in before else b'\n';marker=b'L_005D3E68:'+eol;assert before.count(marker)==1
block='''    {
        RECOMP_REGS_OUT(); RECOMP_FLAGS_OUT();
        ra2_combat_death_bridge();
        RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
        return;
    }
'''.encode().replace(b'\n',eol)
p.write_bytes(b'#include "combat_death_bridge.h"'+eol+before.replace(marker,marker+block))
p=R/'ra2/CMakeLists.txt';data=p.read_bytes();assert b'combat_death' not in data;p.write_bytes(data+b'\ntarget_sources(ra2 PRIVATE src/gameplay/combat_death.c src/runtime/combat_death_bridge.c)\nset_source_files_properties(src/gameplay/combat_death.c src/runtime/combat_death_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n')
write(S/'attachment.json',dict(passed=True,entry='005D3E68',before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=sha(R/'ra2/src/recomp/gen_game/recomp_0029.c'),original_labels_and_statements_retained=True,health_and_damage_services_unchanged=True))
print(dict(passed=True,attached=True))
