"""Drive checkpoint: reuse refresh/usability without importing Arrival close-out policy."""
from pathlib import Path
import sys
assert sys.argv[1:]==['drive']
R=Path(__file__).resolve().parent;p=R/'ra2/src/gameplay/ground_drive.c'
s=p.read_text(encoding='utf-8');assert 'ground_owner_boundary.h' not in s
s=s.replace('#include "ground_failure_transition.h"','#include "ground_failure_transition.h"\n#include "ground_owner_boundary.h"')
marker='/* Prepare/Advance 都可移除单位'
adapter='''static void refresh_after_turn(void *context)
{
    const Ra2DriveServices *s=context;
    s->refresh_owner_after_turn(s->context);
}
static int usable_after_turn(void *context)
{
    const Ra2DriveServices *s=context;
    return query(s,RA2_DRIVE_OWNER_USABLE);
}

'''
assert marker in s;s=s.replace(marker,adapter+marker)
old='''        services->refresh_owner_after_turn(services->context);
        if (!query(services, RA2_DRIVE_OWNER_USABLE))'''
new='''        const Ra2OwnerRefreshServices refresh={(void *)services,refresh_after_turn,usable_after_turn};
        if (!ra2_ground_refresh_owner(&refresh))'''
assert old in s;s=s.replace(old,new)
p.write_text(s,encoding='utf-8',newline='\n')
print('Integrated Drive refresh boundary; Arrival stop/update policy remains separate')
