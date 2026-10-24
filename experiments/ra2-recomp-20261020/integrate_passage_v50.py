"""Keep live target/owner/ability/weapon services after the pure occupation route."""
from pathlib import Path
p=Path(__file__).resolve().parent/'ra2/src/gameplay/ground_passage_finish.c';t=p.read_text(encoding='utf-8')
assert 'ground_outcome_policy.h' not in t
t=t.replace('#include "ground_passage_finish.h"','#include "ground_passage_finish.h"\n#include "ground_outcome_policy.h"')
t=t.replace('    if (state.passage) return state.passage;\n    if (state.crush_enemy) {\n        if (!state.occupied_by_vehicle) return 0;', '''    int32_t result;
    Ra2OccupationRoute route = ra2_ground_occupation_route(state, &result);
    if (route == RA2_OCCUPATION_RESOLVED) return result;
    if (route == RA2_OCCUPATION_CRUSH_TARGET) {''')
t=t.replace('    if (!(state.occupation & 0x3Fu)) return 0;\n    if (state.occupied_by_vehicle) return 2;\n','')
p.write_text(t,encoding='utf-8',newline='\n')
