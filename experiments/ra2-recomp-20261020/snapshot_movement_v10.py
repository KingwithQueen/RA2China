"""保存已验证节点；第一节点还原尚未编译接入的后续候选声明，不混淆源码与程序。"""
from pathlib import Path
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v10'
name, run = sys.argv[1:3]
report = json.loads((STAGE/'runs'/run/'comparison.json').read_text(encoding='utf-8'))
exe = ROOT/'ra2/build-original-c/ra2.exe'
assert report['passed'] and report['exe_sha256'] == hashlib.sha256(exe.read_bytes()).hexdigest()
dest = STAGE/'parts'/name
assert dest.resolve().parent == (STAGE/'parts').resolve()
dest.mkdir(parents=True,exist_ok=False)
paths = {e['path'] for e in json.loads((STAGE/'baseline/source-manifest.json').read_text(encoding='utf-8'))}
cmake = (ROOT/'ra2/CMakeLists.txt').read_text(encoding='utf-8')
for folder in ('gameplay','runtime'):
    for p in (ROOT/'ra2/src'/folder).glob('ground_*'):
        if p.with_suffix('.c').relative_to(ROOT/'ra2').as_posix() in cmake:
            paths.add(p.relative_to(ROOT).as_posix())
manifest = []
for relative in sorted(paths):
    data = (ROOT/relative).read_bytes()
    if name == 'wait-terrain-verified':
        if relative == 'ra2/src/runtime/ground_prepare_bridge.c':
            text = data.decode('utf-8').replace('#include "ground_reaction.h"\n','')
            text = text[:text.index('\nstatic int reaction_sound_pending')].rstrip()+'\n'
            data = text.encode('utf-8')
        if relative == 'ra2/src/runtime/ground_prepare_bridge.h':
            data = data.replace(b'void ra2_ground_reaction_bridge(unsigned entry);\n',b'')
    target = dest/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
    manifest.append(dict(path=relative,sha256=hashlib.sha256(data).hexdigest()))
(dest/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(dest/'validation-source.json').write_text(json.dumps(dict(run=run,exe_sha256=report['exe_sha256'],
    later_uncompiled_reaction_excluded=name=='wait-terrain-verified'),indent=2),encoding='utf-8')
print('Verified snapshot',name,len(manifest),report['exe_sha256'])
