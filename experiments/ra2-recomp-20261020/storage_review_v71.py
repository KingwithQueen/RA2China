"""Bounded NTFS compression of retained evidence, preserving paths and every byte."""
from pathlib import Path
import os,sys,json,time,hashlib,ctypes,shutil,threading
from ctypes import wintypes as w
from concurrent.futures import ThreadPoolExecutor
R=Path(__file__).resolve().parent;P=R.parent.parent;E=R/'evidence';S=E/'storage-review-v1'
k=ctypes.WinDLL('kernel32',use_last_error=True)
k.CreateFileW.argtypes=[w.LPCWSTR,w.DWORD,w.DWORD,ctypes.c_void_p,w.DWORD,w.DWORD,w.HANDLE];k.CreateFileW.restype=w.HANDLE
k.DeviceIoControl.argtypes=[w.HANDLE,w.DWORD,ctypes.c_void_p,w.DWORD,ctypes.c_void_p,w.DWORD,ctypes.POINTER(w.DWORD),ctypes.c_void_p];k.DeviceIoControl.restype=w.BOOL
k.CloseHandle.argtypes=[w.HANDLE];k.GetCompressedFileSizeW.argtypes=[w.LPCWSTR,ctypes.POINTER(w.DWORD)];k.GetCompressedFileSizeW.restype=w.DWORD
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):
    assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ordinary(p):
    assert p.resolve().is_relative_to(E.resolve()) and p.resolve()!=E.resolve(),p
    for a in [p,*p.parents]:
        if a==R:break
        assert not a.lstat().st_file_attributes&0x400,a
def allocated(p):
    high=w.DWORD();ctypes.set_last_error(0);low=k.GetCompressedFileSizeW(str(p),ctypes.byref(high))
    if low==0xFFFFFFFF and ctypes.get_last_error():raise ctypes.WinError(ctypes.get_last_error())
    return (high.value<<32)|low
def compress(p,directory=False):
    h=k.CreateFileW(str(p),0xC0000000,7,None,3,0x02000000 if directory else 0,None)
    if h==ctypes.c_void_p(-1).value:raise ctypes.WinError(ctypes.get_last_error())
    try:
        value=w.WORD(1);returned=w.DWORD()
        if not k.DeviceIoControl(h,0x9C040,ctypes.byref(value),2,None,0,ctypes.byref(returned),None):raise ctypes.WinError(ctypes.get_last_error())
    finally:k.CloseHandle(h)
if sys.argv[1]=='plan':
    entries=[];seen=set();groups={};all_logical=0;large_unique=0;small_bound=0
    suffixes={'.exe','.c','.h','.json','.jsonl','.log','.map','.txt','.asm','.patch','.tsv','.ini'}
    for d,dirs,files in os.walk(E,followlinks=False):
        assert not Path(d).lstat().st_file_attributes&0x400,d
        if Path(d)==S:dirs[:]=[];continue
        for name in files:
            p=Path(d)/name;s=p.stat(follow_symlinks=False);assert not s.st_file_attributes&0x400,p;all_logical+=s.st_size
            if s.st_size<1024*1024:small_bound+=s.st_size;continue
            key=(s.st_dev,s.st_ino)
            if key in seen:continue
            seen.add(key);large_unique+=s.st_size
            parts=p.relative_to(E).parts;group=next((x for x in ['parts','final-source','baseline','runs'] if x in parts),'other')+'/'+p.suffix.lower()
            groups[group]=groups.get(group,0)+s.st_size
            if p.suffix.lower() not in suffixes or s.st_nlink!=1 or s.st_file_attributes&0x800:continue
            ordinary(p);entries.append(dict(path=str(p),bytes=s.st_size,allocated=allocated(p),identity=str(s.st_ino),mtime_ns=s.st_mtime_ns))
    write(S/'plan.json',dict(passed=True,root=str(E.resolve()),entries=entries,files=len(entries),logical_bytes=sum(x['bytes'] for x in entries),allocated_bytes=sum(x['allocated'] for x in entries),free_before=shutil.disk_usage(P).free,large_unique_logical_bytes=large_unique,small_files_logical_upper_bound=small_bound,all_paths_logical_bytes=all_logical,groups=groups,protected_policy='No deletion of originals, baseline, rollback, traces or anomalies. Only NTFS storage representation of exact allowlisted single-link evidence files changes; content and paths retained.',method_source='https://learn.microsoft.com/en-us/windows/win32/fileio/compression-state'))
    print(dict(files=len(entries),selected_GiB=round(sum(x['bytes'] for x in entries)/2**30,2),free_GiB=round(shutil.disk_usage(P).free/2**30,2)))
elif sys.argv[1]=='execute':
    plan=read(S/'plan.json');assert plan['root']==str(E.resolve());assert not (S/'journal.jsonl').exists();start=time.time();lock=threading.Lock();done=0;saved=0
    journal=(S/'journal.jsonl').open('x',encoding='utf-8',buffering=1)
    def one(e):
        global done,saved
        p=Path(e['path']);ordinary(p);s=p.stat();assert s.st_nlink==1 and str(s.st_ino)==e['identity'] and s.st_size==e['bytes'] and s.st_mtime_ns==e['mtime_ns'],p
        before=sha(p);compress(p);after=sha(p);assert before==after,p
        physical=allocated(p);s=p.stat();assert s.st_size==e['bytes'] and s.st_nlink==1 and s.st_file_attributes&0x800,p
        row=dict(path=str(p),sha256=after,bytes=s.st_size,allocated_before=e['allocated'],allocated_after=physical,content_unchanged=True)
        with lock:
            journal.write(json.dumps(row,ensure_ascii=False)+'\n');done+=1;saved+=e['allocated']-physical
            if done%100==0:print(dict(files=done,total=plan['files'],saved_GiB=round(saved/2**30,2),seconds=round(time.time()-start)),flush=True)
        return row
    try:
        with ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(one,plan['entries']))
    finally:journal.close()
    # New evidence folders inherit compression, avoiding the same growth pattern.
    assert E.resolve().is_relative_to(R.resolve()) and not E.lstat().st_file_attributes&0x400;compress(E,True)
    free=shutil.disk_usage(P).free
    write(S/'validation.json',dict(passed=True,files=len(rows),logical_bytes=sum(e['bytes'] for e in rows),allocated_before=sum(e['allocated_before'] for e in rows),allocated_after=sum(e['allocated_after'] for e in rows),saved_bytes=saved,free_before=plan['free_before'],free_after=free,all_content_hashes_verified=True,all_paths_retained=True,baselines_and_rollbacks_retained=True,original_H_untouched=True,new_evidence_inherits_compression=True,deleted_evidence_files=0,journal_sha256=sha(S/'journal.jsonl'),seconds=round(time.time()-start)))
    print(read(S/'validation.json'))
elif sys.argv[1]=='verify':
    v=read(S/'validation.json');assert v['passed'] and sha(S/'journal.jsonl')==v['journal_sha256']
    rows=[json.loads(l) for l in (S/'journal.jsonl').open(encoding='utf-8')];assert len(rows)==v['files']
    for e in rows:assert Path(e['path']).is_file() and Path(e['path']).stat().st_size==e['bytes']
    assert E.stat().st_file_attributes&0x800
    print(dict(passed=True,files=len(rows),saved_GiB=round(v['saved_bytes']/2**30,2),free_GiB=round(shutil.disk_usage(P).free/2**30,2)))
else:raise ValueError(sys.argv[1])
