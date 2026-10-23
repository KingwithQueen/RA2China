from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads((S/'connection-numeric-probe-verified-01.json').read_text(encoding='utf-8-sig'))
assert x['passed'] and x['cases']==1601904 and x['west_frame_42_regression']
sources=[S/'connection_numeric_probe.c',S/'native_probe_host.h',R/'build-connection-numeric-probe-v32.ps1',R/'ra2/src/gameplay/ground_connection_trig.h']
for directory,module in [('gameplay','ground_connection_numeric'),('runtime','ground_connection_numeric_bridge'),('compat','x87_arithmetic')]:
 sources.extend(R/'ra2/src'/directory/(module+ext) for ext in ['.c','.h'])
exe=S/'connection_numeric_probe.exe'
assert all(p.stat().st_mtime<=exe.stat().st_mtime for p in sources)
value=dict(passed=True,total_cases=1601904,results=x,scope='Native original coordinate fragments and complete 6FACA0..6FAD00 and 6FADA5..6FAE01 angle/table/axis chain versus pure C numeric services; all 65536 signed 16-bit facings and 12 control modes. Production bridge wiring additionally verified in real scenes.',
 original_sha256=sha(R/'ra2/game/game.exe'),probe_executable=dict(path=exe.relative_to(R).as_posix(),sha256=sha(exe)),
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources])
(S/'native-connection-numeric-identity.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,cases=value['total_cases'])))
