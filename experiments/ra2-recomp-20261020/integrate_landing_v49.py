"""Advance connection keeps its ordered live service calls; share height arithmetic."""
from pathlib import Path
p=Path(__file__).resolve().parent/'ra2/src/gameplay/ground_landing.c'
t=p.read_text(encoding='utf-8');assert 'ground_exit_policy.h' not in t
t=t.replace('#include <string.h>','#include "ground_exit_policy.h"')
a=t.index('    uint32_t difference =');b=t.index('    s->finish_connection',a)
t=t[:a]+'''    /* 两次高度服务依次执行后才取整；不能缓存owner或合并查询。 */
    int32_t height = ra2_ground_connection_height(start, finish, duration);
'''+t[b:]
p.write_text(t,encoding='utf-8',newline='\n')
