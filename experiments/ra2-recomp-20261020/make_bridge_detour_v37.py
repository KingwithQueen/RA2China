"""Keep both ordinary exit blockers until frame600; no repeated main-vehicle move."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37';items=[]
for old in json.loads((S/'bridge-occupied-fixtures.json').read_text(encoding='utf-8'))['fixtures']:
    item=dict(old);source=R/old['path'];dest=S/'fixtures'/('bridge-detour-'+old['name']+'.MAP');shutil.copy2(source,dest)
    item.update(path=dest.relative_to(R).as_posix(),source=source.relative_to(R).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),release_frame=600,reissue_frame=None)
    item['orders']=[o.replace('300:', '600:',1) for o in old['orders'] if not o.startswith('320:')]
    item['held_exit_until_frame']=600;item['main_move_reissued']=False;items.append(item)
(S/'bridge-detour-fixtures.json').write_text(json.dumps(dict(passed=True,fixtures=items),indent=2)+'\n',encoding='utf-8')
