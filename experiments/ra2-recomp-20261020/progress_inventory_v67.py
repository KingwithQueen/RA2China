"""Current compile/source inventory; counts are not a gameplay completion percentage."""
from run_batch_v67 import *
from collections import Counter
import re,bisect
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');groups=Counter();suffixes=Counter();guards=[];definitions=0
for path,digest in receipt['inputs'].items():
 p=Path(path);assert sha(p)==digest;suffixes[p.suffix]+=1
 if p.suffix=='.c':groups['/'.join(p.relative_to(R).parts[:3])]+=1
 if p.parent==R/'ra2/src/recomp/gen_game' and p.suffix=='.c':
  text=p.read_text(encoding='utf-8');defs=list(re.finditer(r'(?m)^void ([A-Za-z_][A-Za-z_0-9]*)\(void\)\s*\{',text));definitions+=len(defs) if re.fullmatch(r'recomp_[0-9]+\.c',p.name) else 0;positions=[d.start() for d in defs]
  for m in re.finditer(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',text):
   i=bisect.bisect_right(positions,m.start())-1;guards.append(dict(path=p.relative_to(R).as_posix(),line=text.count('\n',0,m.start())+1,enclosing_function=defs[i][1] if i>=0 else None,target=m[1]))
assert receipt['source_count']==181 and len(receipt['inputs'])==312 and len(guards)==37
stats_path=R/'ra2/work/game/lift_stats.json';stats=read(stats_path);assert stats['input_sha256']==sha(R/'ra2/game/game.exe')
write(S/'progress-inventory.json',dict(passed=True,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),compile_receipt_sha256=sha(R/'ra2/build-original-c/source-content-receipt.json'),production_c_sources=181,compile_inputs=312,input_suffix_counts=dict(suffixes),compiled_c_groups=dict(groups),generated_function_definitions=definitions,historical_lift_stats=stats,historical_lift_stats_path=str(stats_path),historical_lift_stats_sha256=sha(stats_path),unimplemented_guard_sites=len(guards),unique_guard_targets=len({g['target'] for g in guards}),guard_inventory=guards,whole_game_equivalence_verified=False,completion_percentage=None,scope='Current compiled source counts and generated definition/guard inventory. 74 gameplay files and lifted function counts are not counts of fully accepted features; old x64 handwritten-engine milestones are not merged into this x86 recompilation status.'))
print(dict(passed=True,c_groups=dict(groups),generated_definitions=definitions,guard_sites=len(guards),unique_targets=len({g['target'] for g in guards})))
