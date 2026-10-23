"""Archive only proven pre-frame native graphics crashes; never discard a simulated delta."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=S/'investigations/startup-failures';out.mkdir(parents=True,exist_ok=True)
ledger=S/'startup-failures.json';entries=read(ledger)['attempts'] if ledger.exists() else []
for report in sorted((S/'runs').glob('*/comparison.json')):
 x=read(report)
 if x.get('passed') or x.get('comparison'):continue
 original=next(r for r in x['runs'] if r['mode']=='original')
 if original['exit_code']!=3221225477:continue
 source=report.parent;tag=source.name
 text=(source/'original/run.log').read_text(encoding='utf-8',errors='replace')
 assert text.rstrip().endswith('[game] Prep direct draw.'),tag
 assert not (source/'original/state.jsonl').exists(),tag
 assert all(r['save_before_sha256']==r['save_after_sha256'] for r in x['runs']),tag
 attempt=1+sum(e['tag']==tag for e in entries)
 destination=out/(tag+f'-attempt-{attempt:02d}')
 assert source.resolve().is_relative_to(S.resolve()) and destination.resolve().is_relative_to(S.resolve())
 assert not destination.exists() and source.is_dir()
 files=[p for p in source.rglob('*') if p.is_file() and (p.name in ['comparison.json','command.json','run.log','state.jsonl'])]
 manifest=[dict(path=p.relative_to(source).as_posix(),sha256=sha(p)) for p in files]
 source.rename(destination)
 for item in manifest:assert sha(destination/item['path'])==item['sha256']
 log=S/(tag+'.log')
 if log.exists():
  target=destination/'runner-attempt-01.log'
  assert log.resolve().is_relative_to(S.resolve()) and target.resolve().is_relative_to(S.resolve())
  assert not target.exists();log.rename(target);manifest.append(dict(path=target.relative_to(destination).as_posix(),sha256=sha(target)))
 entries.append(dict(tag=tag,original_exit_code=original['exit_code'],simulation_frames=0,
  original_source_path=str(source),preserved_path=str(destination),preserved_files=manifest,
  disposition='Retained original graphics-initialization crash, before state recording. Retry uses a new private farm; production code remains unchanged. Root cause is not established.'))
 (destination/'archive-receipt.json').write_text(json.dumps(entries[-1],indent=2)+'\n',encoding='utf-8')
value=dict(passed=True,attempts=entries,failed_records_preserved=True,simulated_differences_never_archived_by_this_recipe=True)
ledger.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,preserved=len(entries))))
