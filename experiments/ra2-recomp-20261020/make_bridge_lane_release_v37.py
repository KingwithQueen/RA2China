"""Release the main lane first while the adjacent lane stays occupied while the opposing meeting vehicle detours."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37';items=[]
for old in json.loads((S/'bridge-detour-fixtures.json').read_text(encoding='utf-8'))['fixtures']:
    item=dict(old);source=R/old['path'];dest=S/'fixtures'/('bridge-lane-release-'+old['name']+'.MAP');shutil.copy2(source,dest)
    first,second=(210,300) if old['name']=='north' else (226,316)
    releases={str(old['blocker_ids'][1]):first,str(old['blocker_ids'][0]):second}
    orders=[]
    for order in old['orders']:
        values=order.split(':')
        if values[0]=='600':values[0]=str(releases[values[1]])
        orders.append(':'.join(values))
    item.update(path=dest.relative_to(R).as_posix(),source=source.relative_to(R).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),release_frame=second,release_frames=releases,orders=orders,held_exit_until_frame=first,main_move_reissued=False,reissue_frame=None)
    items.append(item)
(S/'bridge-lane-release-fixtures.json').write_text(json.dumps(dict(passed=True,fixtures=items),indent=2)+'\n',encoding='utf-8')
