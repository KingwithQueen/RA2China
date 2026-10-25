"""Freeze observed reference outcomes before production changes; no success reclassification."""
from run_batch_v67 import *
assert read(S/'channel-observer-baseline-parity.json')['passed']
initial=read(S/'traffic-baseline-scenes.json');write(S/'traffic-baseline-initial-matrix.json',initial)
for row in initial['results']:row['acceptance_kind']='original-behavior-boundary'
initial.update(scope='Four fixed original/unchanged-parent comparisons before production edits. Exact, near-goal and stationary outcomes are frozen; not all-request recovery successes.',positive_recovery_pairs=0,boundary_pairs=4)
(S/'traffic-baseline-scenes.json').write_text(json.dumps(initial,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cases={}
for r in read(S/'traffic-fixtures.json')['fixtures']:
 for tag in [r['baseline_tag'],r['observer_baseline_tag']]:
  proof=read(S/'runs'/tag/'traffic-acceptance.json');assert proof['acceptance_kind']=='original-behavior-boundary' and not proof['positive_recovery_acceptance']
  assert proof['modes']['original']['effects']==proof['modes']['generated-c']['effects']
  cases[tag]=dict(acceptance_sha256=sha(S/'runs'/tag/'traffic-acceptance.json'),modes=proof['modes'])
write(S/'traffic-boundary-contract.json',dict(passed=True,cases=cases,positive_recovery_acceptance=False,source_exe_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),checker_review_sha256=sha(S/'traffic-checker-review.json'),scope='Reference contract for this no-mechanism-change service batch. A future deliberate mechanism improvement may accept explained differences rather than reproduce these original failures.'))
print(dict(passed=True,frozen_boundary_cases=len(cases),positive_recovery_cases=0))
