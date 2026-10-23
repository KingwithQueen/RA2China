"""Recover exact prior producer bytes and verify the already recorded recipe hash."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v34';D=S/'investigations/south-initial-scan'
captured=D/'make_bridge_occupied_v34.py';t=captured.read_text(encoding='utf-8')
addition="        if direction=='south' and section=='[Infantry]' and line.startswith('2='):\n            k,v=line.split('=',1);fields=v.split(',');assert fields[1]=='E2';fields[3:6]=['61','64','4'];line=k+'='+','.join(fields)\n"
assert addition in t;t=t.replace(addition,'')
t=t.replace("'1023367':[60 if north else 61,61 if north else 72]","'1023367':[60,61 if north else 72]")
t=t.replace("f'5:1023367:2:{goals[\"1023367\"][0]}:{goals[\"1023367\"][1]}'","f'5:1023367:2:60:{goals[\"1023367\"][1]}'")
expected=next(x['sha256'] for x in json.loads((D/'recipe-byte-audit.json').read_text(encoding='utf-8'))['inputs'] if x['path']=='make_bridge_occupied_v34.py')
raw=t.encode('utf-8');assert hashlib.sha256(raw).hexdigest()==expected
dest=D/'make_bridge_occupied_producer_before_selection_v34.py';assert not dest.exists();dest.write_bytes(raw)
(D/'producer-recovery.json').write_text(json.dumps(dict(passed=True,producer_sha256=expected,path=dest.name,captured_copy_note='The existing captured source reflects the subsequent lane edit made immediately before preservation. The recovered prior producer matches the original recipe hash exactly; neither the captured copy nor the original preservation receipt was overwritten.'),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,prior_producer_hash_matched=True))
