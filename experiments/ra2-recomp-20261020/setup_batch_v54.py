"""Copy only the bounded current harness and retained native inputs for batch53."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;O=R/'evidence/movement-state-v53';S=R/'evidence/movement-state-v54'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'build-path-lifecycle-probe-v38.ps1'
(R/'build-path-lifecycle-probe-v54.ps1').write_text(p.read_text(encoding='utf-8-sig').replace('v38','v54'),encoding='utf-8',newline='\n')
for name in ['map_codec_v53.py']:
 (R/name.replace('v53','v54')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v53','v54'),encoding='utf-8',newline='\n')
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json','mission-table-proof.json']:
 shutil.copy2(O/name,S/name)
entries=[]
for name in ['bridge-catalog-observer.exe','bridge_catalog_observer.c']:
 d=S/'baseline-observer'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,d);shutil.copy2(O/name,S/name)
 entries.append(dict(path=name,sha256=sha(d)))
(S/'baseline-observer/manifest.json').write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,baseline_observer_sha256=sha(S/'bridge-catalog-observer.exe')))
