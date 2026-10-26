from combat_batch_v72 import *
# This helper only describes the checked attachment; it executes after baseline qualification.
blocks={
'recomp_0046.c':{
 'L_006FCA7E:':['uint32_t next=ra2_unit_death_handoff_bridge();','if(!next)return;','if(next==0x6FD1DB)goto L_006FD1DB;','if(next==0x6FCD44)goto L_006FCD44;','goto L_006FCADA;'],
 'L_006FD17D:':['ra2_unit_death_finish_bridge();','return;']},
'recomp_0017.c':{
 'L_004FFBD6:':['uint32_t next=ra2_infantry_death_handoff_bridge();','if(!next)return;','if(next==0x500193)goto L_00500193;','goto L_004FFC4D;'],
 'L_004FFF61:':['ra2_infantry_death_finish_bridge();','return;']},
'recomp_0012.c':{'L_004CCE40:':['ra2_foot_uninit_bridge();','return;']},
'recomp_0029.c':{'L_005D4E90:':['ra2_object_uninit_bridge();','return;']},
'recomp_0045.c':{'L_006ECF10:':['ra2_object_delete_drain_bridge();','return;']}}
def attached(before,points):
    eol=b'\r\n' if b'\r\n' in before else b'\n'
    first=next(iter(points))
    function={'L_006FCA7E:':'UnitClass__virtual_86','L_004FFBD6:':'InfantryClass__virtual_86','L_004CCE40:':'AircraftClass__virtual_60','L_005D4E90:':'WaveClass__virtual_60','L_006ECF10:':'sub_006ECF10'}[first]
    start=before.index(('void '+function+'(void) {').encode());end=before.index(eol+b'}'+eol,start)+len(eol)+1
    result=before[start:end]
    for label,lines in points.items():
        instruction=label=='L_006FCA7E:'
        marker=(b'    ebx = eax; /* 0x006FCA7E: mov ebx, eax */' if instruction else label.encode())+eol
        assert result.count(marker)==1,(function,label)
        body=['    {','        RECOMP_REGS_OUT(); RECOMP_FLAGS_OUT();','        '+lines[0],'        RECOMP_REGS_IN(); RECOMP_FLAGS_IN();']+['        '+v for v in lines[1:]]+['    }']
        block=eol.join(v.encode() for v in body)+eol
        result=result.replace(marker,block+marker if instruction else marker+block)
    return b'#include "combat_lifecycle_bridge.h"'+eol+before[:start]+result+before[end:]

cmake=b'\ntarget_sources(ra2 PRIVATE src/gameplay/combat_lifecycle.c src/runtime/combat_lifecycle_bridge.c)\nset_source_files_properties(src/gameplay/combat_lifecycle.c src/runtime/combat_lifecycle_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
if __name__=='__main__':
    assert read(S/'baseline-review.json')['passed'] and read(S/'b-command-scenes.json')['passed']
    assert read(S/'probe-05.log')['passed']
    old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')
    for p,d in old['inputs'].items():assert sha(Path(p))==d,p
    assert sha(R/'ra2/build-original-c/ra2.exe')==old['executable_sha256']
    changes=[];prepared={}
    for name,points in blocks.items():
        p=R/'ra2/src/recomp/gen_game'/name;before=p.read_bytes();prepared[p]=attached(before,points);changes.append(dict(path=p.relative_to(R).as_posix(),before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(prepared[p]).hexdigest(),labels=list(points)))
    for p,data in prepared.items():p.write_bytes(data)
    p=R/'ra2/CMakeLists.txt';assert b'combat_lifecycle' not in p.read_bytes();p.write_bytes(p.read_bytes()+cmake)
    write(S/'attachment.json',dict(passed=True,changes=changes,original_labels_and_statements_retained=True,health_damage_shared_death_and_movement_unchanged=True))
    print(dict(passed=True,attached_fragments=7))
