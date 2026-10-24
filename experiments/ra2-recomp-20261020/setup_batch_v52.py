"""Copy only the bounded current harness and retained native inputs for batch51."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;O=R/'evidence/movement-state-v51';S=R/'evidence/movement-state-v52'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,old in [('prepare',43),('advance',47)]:
 p=R/f'build-{name}-probe-v{old}.ps1';t=p.read_text(encoding='utf-8-sig').replace(f'v{old}','v52')
 extra=['ground_rebuild_result','ground_bridge_plane','ground_segment_admission','ground_cell_placement'] if name=='prepare' else ['ground_segment_admission']
 for source in extra:
  arg='..\\..\\ra2\\src\\gameplay\\'+source+'.c'
  if arg not in t:t=t.replace(' /Fe:', ' '+arg+' /Fe:')
 (R/f'build-{name}-probe-v52.ps1').write_text(t,encoding='utf-8',newline='\n')
for name in ['map_codec_v51.py']:
 (R/name.replace('v51','v52')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v51','v52'),encoding='utf-8',newline='\n')
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json','mission-table-proof.json']:
 shutil.copy2(O/name,S/name)
entries=[]
for name in ['bridge-catalog-observer.exe','bridge_catalog_observer.c']:
 d=S/'baseline-observer'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,d);shutil.copy2(O/name,S/name)
 entries.append(dict(path=name,sha256=sha(d)))
(S/'baseline-observer/manifest.json').write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,baseline_observer_sha256=sha(S/'bridge-catalog-observer.exe')))
