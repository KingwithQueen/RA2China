"""Attach the health prefix once, retaining all original labels and the death tail."""
from combat_batch_v69 import *
assert read(S/'baseline-effects.json')['passed'] and read(S/'b-command-scenes.json')['passed']
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')
for p,d in old['inputs'].items():assert sha(Path(p))==d,p
assert sha(R/'ra2/build-original-c/ra2.exe')==old['executable_sha256']
dst=S/'baseline-command';dst.mkdir()
for n in ['combat_command.c','combat-command.exe']:shutil.copy2(S/n,dst/n)
write(S/'baseline-command.json',dict(passed=True,exe_sha256=sha(dst/'combat-command.exe'),source_sha256=sha(dst/'combat_command.c')))
p=R/'ra2/src/recomp/gen_game/recomp_0029.c';before=p.read_bytes();eol=b'\r\n' if b'\r\n' in before else b'\n'
marker=b'L_005D3D20:'+eol;assert before.count(marker)==1
block='''    {
        RECOMP_REGS_OUT(); RECOMP_FLAGS_OUT();
        uint32_t health_resume=ra2_combat_health_bridge();
        RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
        if(!health_resume)return;
        goto L_005D3E68;
    }
'''.encode().replace(b'\n',eol)
after=b'#include "combat_health_bridge.h"'+eol+before.replace(marker,marker+block)
resume=b'    if (TEST_G(_flag_a, _flag_b)) goto L_005D3F39; /* 0x005D3E68: jg 0x5d3f39 */'
assert after.count(resume)==1
after=after.replace(resume,b'L_005D3E68:'+eol+resume)
p.write_bytes(after)
p=R/'ra2/CMakeLists.txt';before_cmake=p.read_bytes();assert b'combat_health' not in before_cmake
addition='''
target_sources(ra2 PRIVATE src/gameplay/combat_health.c src/runtime/combat_health_bridge.c)
set_source_files_properties(src/gameplay/combat_health.c src/runtime/combat_health_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")
'''.encode();p.write_bytes(before_cmake+addition)
write(S/'attachment.json',dict(passed=True,entry='005D3D20',resume='005D3E68',returns_early=True,original_labels_and_death_tail_retained=True,modified_generated_chunk='ra2/src/recomp/gen_game/recomp_0029.c',before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest(),cmake_only_appended=True))
print(dict(passed=True,attached=True))
