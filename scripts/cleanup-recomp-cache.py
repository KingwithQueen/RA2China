"""Reversible allowlist cleanup: protect baselines, receipts, games and live build."""
from pathlib import Path
import hashlib,json,os,zipfile,datetime
P=Path(__file__).resolve().parent.parent;R=P/'experiments/ra2-recomp-20261020'
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S');out=P/'.local-archives'/('cleanup-'+stamp)
out.mkdir(parents=True,exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
skip={'.git','.agents','.codex','baseline','final-source','parts','investigations','game','work','__pycache__-preserved'}
extensions={'.obj','.pdb','.ilk','.exp','.pyc','.pyo','.tmp'}
items=[]
for folder,dirs,files in os.walk(R,followlinks=False):
    base=Path(folder)
    dirs[:]=[d for d in dirs if d not in skip and not (base/d).lstat().st_file_attributes&0x400
             and (base/d).resolve()!=(R/'ra2/build-original-c').resolve()]
    for name in files:
        p=base/name
        if p.suffix.lower() not in extensions or 'fixture' in name.lower():continue
        if p.lstat().st_file_attributes&0x400:continue
        resolved=p.resolve();assert resolved.is_relative_to(R.resolve())
        items.append(dict(path=p.relative_to(P).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
plan=dict(scope='Only reproducible compiler/cache file extensions; all baseline, rollback, failure, game, work and current production build directories excluded.',
          files=items,logical_bytes=sum(x['bytes'] for x in items))
(out/'manifest.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
archive=out/'compiler-cache.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for x in items:z.write(P/x['path'],x['path'])
with zipfile.ZipFile(archive) as z:
    for x in items:assert hashlib.sha256(z.read(x['path'])).hexdigest()==x['sha256']
for x in items:
    p=P/x['path'];assert p.resolve().is_relative_to(R.resolve()) and sha(p)==x['sha256']
    for parent in [p,*p.parents]:
        if parent==R.parent:break
        assert not parent.lstat().st_file_attributes&0x400,parent
    p.unlink()
# Accepted generation 14's source/EXE copies remain untouched.
S=R/'evidence/movement-state-v15';entries=json.loads((S/'source-manifest.json').read_text(encoding='utf-8'))
for x in entries:assert sha(R/x['path'])==sha(S/'final-source'/x['path'])==x['sha256'],x['path']
receipt=dict(passed=True,removed_files=len(items),removed_logical_bytes=plan['logical_bytes'],archive=str(archive),
             archive_sha256=sha(archive),archive_bytes=archive.stat().st_size,manifest=str(out/'manifest.json'),
             accepted_source_files_verified=len(entries),baselines_and_rollbacks_preserved=True)
(P/'docs/清理记录-20261022.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
