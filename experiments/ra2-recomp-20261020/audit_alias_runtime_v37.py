"""Keep static legal edges, resolver observations and production parity separate."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ordered(rs):return [r for r in rs if r['kind'] in ['submit','execute','movement-audit'] or r['kind'].startswith('fixture-')]
static=read(S/'internal-alias-sources.json');assert static['passed'] and static['alias_count']==29
assert not static['direct_call_candidates'] and not static['noncode_literal_candidates'] and not static['direct_c_reference_candidates']
outside=[]
for e in static['entries']:
    if e['entry_kind']!='alias':continue
    a=int(e['entry'],16);lo,hi=(0x4A1000,0x4A2670) if a<0x4A2670 else (0x4A2670,0x4A4740) if a<0x700000 else (0x703040,0x703BD0)
    outside += [dict(entry=e['entry'],edge=edge) for edge in e['decoded_incoming'] if not lo<=int(edge['address'],16)<hi]
assert not outside
records=[];examined=set();inputs=[Path(__file__),R/'run_alias_probe_v37.py',R/'run_alias_scenes_v37.py',S/'internal-alias-sources.json']
for group,name in [('a','enemy-traffic-ai3-north'),('b','enemy-traffic-ai3-south'),('c','enemy-mixed-north'),('d','enemy-mixed-south')]:
    tag='al-'+group;plain_tag='ep-'+name;report=read(S/'runs'/tag/'comparison.json');c=report['comparison']
    production_report=read(S/'runs'/plain_tag/'comparison.json')
    assert report['scenario_sha256']==production_report['scenario_sha256'] and report['seed']==production_report['seed']==12345
    assert report['passed'] and report['exe_sha256']==sha(S/'connection-fixture-probe.exe')
    assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
    assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
    assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
    assert all(r['passed'] and r['exit_code']==0 and r['save_is_private_copy'] and r['save_before_sha256']==r['save_after_sha256'] for r in report['runs'])
    native=rows(tag,'original');lifted=rows(tag,'generated-c');assert ordered(native)==ordered(lifted)
    for mode,observed in [('original',native),('generated-c',lifted)]:
        plain=rows(plain_tag,mode)
        assert [r for r in observed if r['kind']=='state']==[r for r in plain if r['kind']=='state']
        assert [r for r in ordered(observed) if r['kind'] not in ['fixture-internal-hit','fixture-connection-hit']]==ordered(plain)
    command=read(S/'runs'/tag/'generated-c/command.json')
    configured={f'{int(command[i+1],0):08X}' for i,x in enumerate(command) if x=='--probe'}
    text=(S/'runs'/tag/'generated-c/run.log').read_text(encoding='utf-8',errors='replace')
    hits=Counter(re.findall(r'^\[probe\] sub_([0-9A-F]{8}) from ',text,re.M));assert hits['00703040']>0
    aliases=configured-{'004A1000','004A2670','00703040'};assert aliases and all(hits[a]==0 for a in aliases)
    examined.update(aliases);records.append(dict(tag=tag,frames=901,first_call_record_counts={a:hits[a] for a in sorted(configured)}))
    inputs += [S/'runs'/tag/'comparison.json',S/'runs'/tag/'generated-c/run.log',S/'runs'/tag/'generated-c/command.json']
assert examined==set(static['new_aliases'])-{'004A24F0'} and len(examined)==19
old=read(S/'bridge-mixed-real-scenes.json');old_aliases={a for v in old['scenes'].values() for a in v['configured_aliases']}
assert len(old_aliases)==9 and len(old_aliases|examined)==28
value=dict(passed=True,static_aliases=29,byte_checked_edges=static['unique_native_edges'],new_runtime_probe_targets=19,
    prior_runtime_probe_targets=9,all_configured_aliases_without_first_call_record=True,external_jump_candidates=outside,
    additional_observer_scenes=4,additional_observer_frames=3604,production_observer_state_identity=True,
    records=records,nonprimary_natural_entry_proved=False,
    limits='Natural ordinary moves only. All 28 configured aliases lack their first-call record in the examined bridge scenes, with primary703040 positive controls. Fixed-frame termination provides no full-run counters. Arbitrary computed targets, runtime-built pointers and unrun scenes remain unresolved.',
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
out=S/'alias-natural-scenes.json';assert not out.exists();out.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,aliases=28,new_probe_targets=19,additional_frames=3604)))
