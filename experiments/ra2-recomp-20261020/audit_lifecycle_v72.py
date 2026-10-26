from combat_batch_v72 import *
from integrate_lifecycle_v72 import blocks,attached,cmake
import re
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==190 and len(receipt['inputs'])==329 and receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
old=read(S/'baseline/ra2/build-original-c/source-content-receipt.json')['inputs'];changed=[];added=[]
for p,d in receipt['inputs'].items():
    assert sha(Path(p))==d,p;rel=Path(p).relative_to(R).as_posix()
    if p not in old:added.append(rel)
    elif old[p]!=d:changed.append(rel)
assert set(changed)=={'ra2/src/recomp/gen_game/'+n for n in blocks}
assert set(added)=={'ra2/src/'+n for n in ['gameplay/combat_lifecycle.c','gameplay/combat_lifecycle.h','runtime/combat_lifecycle_bridge.c','runtime/combat_lifecycle_bridge.h']}
for name,points in blocks.items():
    rel='ra2/src/recomp/gen_game/'+name;assert (R/rel).read_bytes()==attached((S/'baseline'/rel).read_bytes(),points)
rel='ra2/CMakeLists.txt';assert (R/rel).read_bytes()==(S/'baseline'/rel).read_bytes()+cmake
for phase,root in [('baseline',S/'baseline'),('final',R)]:
    before=(root/'ra2/src/recomp/gen_game/recomp_0029.c').read_bytes();p=S/('baseline-observer/death_generated.c' if phase=='baseline' else 'observer-build/death_generated.c');assert p.read_bytes()==before.replace(b'void WaveClass__virtual_86(void) {',b'void observed_health_original(void) {')
guards=defs=0
for name in receipt['inputs']:
    p=Path(name)
    if p.parent==R/'ra2/src/recomp/gen_game' and re.fullmatch(r'recomp_[0-9]+\.c',p.name):
        t=p.read_text(encoding='utf-8');guards+=len(re.findall(r'ra2_recovery_unimplemented\(0x[0-9A-Fa-f]+',t));defs+=len(re.findall(r'(?m)^void [A-Za-z_0-9]+\(void\)\s*\{',t))
assert (guards,defs)==(37,23117)
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256']
probe=read(S/'probe-05.log');assert probe['passed'] and probe['lifecycle_cases']==229376
write(S/'native-validation.json',dict(passed=True,result=probe,exe_sha256=sha(S/'lifecycle_probe.exe'),original_sha256=sha(R/'ra2/game/game.exe'),inputs=[dict(path=str(p),sha256=sha(p)) for p in [S/'lifecycle_probe.c',S/'native_probe_host.h',R/'ra2/src/gameplay/combat_lifecycle.c',R/'ra2/src/gameplay/combat_lifecycle.h',R/'ra2/src/runtime/combat_lifecycle_bridge.c',R/'ra2/src/runtime/combat_lifecycle_bridge.h']],actual_original_fragments=True,engine_callbacks_mocked=True,typeid_and_destructor_callbacks_mocked=True))
write(S/'source-preservation.json',dict(passed=True,changed_compile_inputs=changed,added_compile_inputs=added,c_sources=190,headers=139,compile_inputs=329,guard_sites=guards,generated_definitions=defs,attachment_labels=[k for points in blocks.values() for k in points],original_statements_and_labels_retained=True,health_damage_shared_death_movement_numeric_and_recorder_sources_unchanged=True,internal_entries_removed=False,protected_files=28,parent_archive_files=len(read(O/'source-manifest.json'))))
# Verify names against the locked image's real vtables, rather than shared RTTI aliases.
sys.path.insert(0,str(R/'python_lib'))
import pefile,struct
image=pefile.PE(str(R/'ra2/game/game.exe'));tables=[]
for kind,address,damage,destructor in [('Unit',0x7ADDF8,0x6FCA30,0x70A330),('Infantry',0x7A3540,0x4FFB70,0x509810)]:
    slots={hex(slot):struct.unpack('<I',image.get_data(address-0x400000+slot,4))[0] for slot in [0x20,0xF0,0x158]}
    assert slots['0x20']==destructor and slots['0xf0']==0x4CCE40 and slots['0x158']==damage
    tables.append(dict(kind=kind,address=hex(address),slots={k:hex(v) for k,v in slots.items()}))
write(S/'lifecycle-layout.json',dict(passed=True,original_sha256=sha(R/'ra2/game/game.exe'),vtables=tables,foot_uninit='004CCE40 (generated alias AircraftClass__virtual_60)',object_uninit='005D4E90 (generated alias WaveClass__virtual_60)',deferred_drain='006ECF10',death_frames_read={'key_push':'0070AE04','ini_global':'008397F0','kind':'ART.INI','unit_type_offset':'0xBB8'},engine_aliases_not_new_class_implementations=True))
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:shutil.copy2(O/n,S/n)
print(dict(passed=True,c_sources=190,inputs=329,native_cases=229376))
