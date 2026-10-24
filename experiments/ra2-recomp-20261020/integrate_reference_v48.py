"""Prepare approach still re-reads owner/position/offset/cell after the first service group."""
from pathlib import Path
import sys
assert sys.argv[1:]==['approach']
R=Path(__file__).resolve().parent;p=R/'ra2/src/gameplay/ground_internal_next.c'
s=p.read_text(encoding='utf-8');assert 'ground_transition_rules.h' not in s
s=s.replace('#include "ground_internal_next.h"','#include "ground_internal_next.h"\n#include "ground_transition_rules.h"')
s=s.replace('services->cell_level(context, cell) + (services->upper_layer(context) ? 4 : 0)','ra2_ground_layer_reference(services->cell_level(context, cell),services->upper_layer(context))')
p.write_text(s,encoding='utf-8',newline='\n')
print('Integrated live approach reference; repeated world-service reads preserved')
