"""Second checkpoint: bridge-layer service order, including post-set flag requery."""
from pathlib import Path
import sys
assert sys.argv[1:]==['layer']
R=Path(__file__).resolve().parent;p=R/'ra2/src/gameplay/ground_template_transition.c'
s=p.read_text(encoding='utf-8');assert 'ground_bridge_plane.h' not in s
s=s.replace('#include "ground_template_transition.h"','#include "ground_template_transition.h"\n#include "ground_bridge_plane.h"')
a=s.index('    void *context = services->context;',s.index('void ra2_ground_template_layer('))
s=s[:a]+'''    /* set_layer 后重新查询标志的约定由共享边界保持，不能预先缓存下一格标志。 */
    ra2_ground_transition_bridge(services->context,services->level,services->flags,services->set_layer);
}
'''
p.write_text(s,encoding='utf-8',newline='\n')
print('Integrated live bridge layer service transition')
