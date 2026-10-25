"""Readable map limits, shared stop boundaries and one occupation decision tree."""
from run_batch_v68 import *
import re
assert read(S/'b-scenes.json')['passed'] and read(S/'baseline-native.json')['passed']
for p,d in read(S/'baseline/ra2/build-original-c/source-content-receipt.json')['inputs'].items():assert sha(Path(p))==d,p
def replace(rel,old,new):
    p=R/rel;t=p.read_text(encoding='utf-8');assert t.count(old)==1,(rel,old[:80]);p.write_text(t.replace(old,new),encoding='utf-8',newline='\n')
def append(rel,body):
    p=R/rel;t=p.read_text(encoding='utf-8');p.write_text(t.rstrip()+'\n\n'+body.strip()+'\n',encoding='utf-8',newline='\n')
append('ra2/src/gameplay/ground_cell_services.h','''
typedef struct Ra2MapArea
{
    int32_t width, local_x, local_y, local_width, local_height;
} Ra2MapArea;
/* 可用地图是等距投影的菱形，不是有地形数据就能接收移动目标。
   adjust_height关闭时传0高度/坡度；开启时由适配层读取真实格或备用格。 */
typedef enum Ra2MapAreaEdge {
    RA2_MAP_AREA_INSIDE, RA2_MAP_AREA_ABOVE, RA2_MAP_AREA_BELOW,
    RA2_MAP_AREA_RIGHT, RA2_MAP_AREA_LEFT
} Ra2MapAreaEdge;
Ra2MapAreaEdge ra2_cell_area_boundary(const Ra2MapArea *area,Ra2ServiceCell cell,
    int32_t level,unsigned slope);
int ra2_cell_usable_area(const Ra2MapArea *area, Ra2ServiceCell cell,
    int32_t level, unsigned slope);
''')
append('ra2/src/gameplay/ground_cell_services.c','''
static int32_t signed_bits(uint32_t bits)
{
    int32_t value; memcpy(&value,&bits,sizeof(value)); return value;
}

Ra2MapAreaEdge ra2_cell_area_boundary(const Ra2MapArea *area,Ra2ServiceCell cell,
    int32_t level,unsigned slope)
{
    int32_t sum=(int32_t)cell.x+cell.y;
    uint32_t top=(uint32_t)area->width+2u*(uint32_t)area->local_y;
    /* 坡面靠近上边时再补一层；边界比较仍是原版严格/非严格组合。 */
    if(slope && sum<signed_bits(top+4u+(uint32_t)level))
        level=signed_bits((uint32_t)level+1u);
    int32_t bottom=signed_bits((uint32_t)area->width
        +2u*((uint32_t)area->local_y+(uint32_t)area->local_height)+2u+(uint32_t)level);
    int32_t right=signed_bits(2u*((uint32_t)area->local_x+(uint32_t)area->local_width)-(uint32_t)area->width);
    int32_t left=signed_bits((uint32_t)area->width-2u*(uint32_t)area->local_x);
    if(sum<=signed_bits(top+(uint32_t)level))return RA2_MAP_AREA_ABOVE;
    if(sum>bottom)return RA2_MAP_AREA_BELOW;
    if((int32_t)cell.x-cell.y>=right)return RA2_MAP_AREA_RIGHT;
    if((int32_t)cell.y-cell.x>=left)return RA2_MAP_AREA_LEFT;
    return RA2_MAP_AREA_INSIDE;
}
int ra2_cell_usable_area(const Ra2MapArea *area,Ra2ServiceCell cell,int32_t level,unsigned slope)
{
    return ra2_cell_area_boundary(area,cell,level,slope)==RA2_MAP_AREA_INSIDE;
}
''')
append('ra2/src/runtime/ground_services_bridge.h','void ra2_cell_map_area_bridge(void);')
p=R/'ra2/src/runtime/ground_map_bounds_bridge.c';assert not p.exists()
p.write_text('''#include <stdint.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_cell_services.h"
#include "ground_services_bridge.h"

/* 仅适配1.006的布局、AL返回、易失寄存器和ret 8；菱形规则在gameplay。 */
void ra2_cell_map_area_bridge(void)
{
    uint32_t stack=g_esp,map=g_ecx,input=MEM32(stack+4);
    Ra2ServiceCell point;memcpy(&point,(void *)(uintptr_t)ADDR(input),sizeof(point));
    Ra2MapArea area={(int32_t)MEM32(map+0xF0),(int32_t)MEM32(map+0xF8),
        (int32_t)MEM32(map+0xFC),(int32_t)MEM32(map+0x100),(int32_t)MEM32(map+0x104)};
    int32_t level=0;unsigned slope=0;
    if(MEM8(stack+8))
    {
        Ra2CellGrid grid={(const uint32_t *)(uintptr_t)ADDR(MEM32(0x832618)),262144,
            0xA6F9F8,(Ra2ServiceCell *)(uintptr_t)ADDR(0xA6FA1C)};
        uint32_t cell=(uint32_t)ra2_cell_at_point(&grid,point);
        level=(int8_t)MEM8(cell+0x11B);slope=MEM8(cell+0x11C);
    }
    Ra2MapAreaEdge edge=ra2_cell_area_boundary(&area,point,level,slope);
    g_eax=(uint32_t)area.width;g_edx=(uint32_t)(int32_t)point.y;
    if(edge==RA2_MAP_AREA_RIGHT)
        g_ecx=2u*((uint32_t)area.local_x+(uint32_t)area.local_width)-(uint32_t)area.width;
    else if(edge==RA2_MAP_AREA_LEFT || edge==RA2_MAP_AREA_INSIDE)
    {
        g_ecx=2u*(uint32_t)area.local_x;
        g_edx=(uint32_t)(int32_t)point.y-(uint32_t)(int32_t)point.x;
        g_eax=(uint32_t)area.width-g_ecx;
    }
    if(edge==RA2_MAP_AREA_INSIDE)
    {
        g_flag_k=FK_CMP;g_flag_a=g_edx;g_flag_b=g_eax;g_flag_cf=g_edx<g_eax;
        g_eax=(g_eax&0xFFFFFF00u)|1u;
    }
    else
    {
        g_eax&=0xFFFFFF00u;
        g_flag_k=FK_TEST;g_flag_a=0;g_flag_b=0;g_flag_cf=0;
    }
    g_esp=stack+12;
}
'''.replace('\n+','\n'),encoding='utf-8',newline='\n')
append('ra2/CMakeLists.txt','''
target_sources(ra2 PRIVATE src/runtime/ground_map_bounds_bridge.c)
set_source_files_properties(src/runtime/ground_map_bounds_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")
''')
p=R/'ra2/src/recomp/gen_game/recomp_0023.c';text=p.read_text(encoding='utf-8')
match=re.search(r'void sub_0055A660\(void\) \{.*?\n\}',text,re.S);assert match
functions=read(R/'ra2/work/game/functions.json')['functions']
assert not [f for f in functions if 0x55A660<f['address']<0x55A737], 'Do not remove an alias entry'
before=match[0];(S/'map-area-generated-before.c').write_text(before+'\n',encoding='utf-8')
after='void sub_0055A660(void) {\n    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;\n    RECOMP_ENTER(0x0055A660u);\n    ra2_cell_map_area_bridge();\n}'
text=text[:match.start()]+after+text[match.end():]
assert '#include "ground_services_bridge.h"' not in text
p.write_text('#include "ground_services_bridge.h"\n'+text,encoding='utf-8',newline='\n')
append('ra2/src/gameplay/ground_failure_transition.h','''
/* CloseEnough与两层高度均采用严格小于；无符号计算保留32位差值位模式。 */
int ra2_ground_within_stop_distance(int32_t distance,int32_t close_enough);
int32_t ra2_ground_axis_distance(int32_t left,int32_t right);
int ra2_ground_within_stop_height(int32_t left,int32_t right,int32_t level_height);
''')
replace('ra2/src/gameplay/ground_failure_transition.c','#include "ground_failure_transition.h"','#include "ground_failure_transition.h"\n#include <string.h>')
append('ra2/src/gameplay/ground_failure_transition.c','''
int ra2_ground_within_stop_distance(int32_t distance,int32_t close_enough)
{
    return distance<close_enough;
}
int32_t ra2_ground_axis_distance(int32_t left,int32_t right)
{
    uint32_t bits=(uint32_t)left-(uint32_t)right;
    if(bits&0x80000000u)bits=0u-bits;
    int32_t value;memcpy(&value,&bits,sizeof(value));return value;
}
int ra2_ground_within_stop_height(int32_t left,int32_t right,int32_t level_height)
{
    uint32_t bits=2u*(uint32_t)level_height;
    int32_t threshold;memcpy(&threshold,&bits,sizeof(threshold));
    return ra2_ground_axis_distance(left,right)<threshold;
}
''')
replace('ra2/src/gameplay/ground_prepare.c','if (distance >= threshold)','if (!ra2_ground_within_stop_distance(distance,threshold))')
p=R/'ra2/src/gameplay/ground_obstacle.c';t=p.read_text(encoding='utf-8')
t,n=re.subn(r'static int32_t wrapped_absolute_difference\(.*?\n\}\n', '',t,count=1,flags=re.S);assert n==1
t=t.replace('int close_to_destination = distance < close_enough;','int close_to_destination = ra2_ground_within_stop_distance(distance,close_enough);')
t=t.replace('        int32_t two_levels = (int32_t)((uint32_t)height * 2u);\n','')
t=t.replace('wrapped_absolute_difference(state->destination.z, position.z) < two_levels','ra2_ground_within_stop_height(state->destination.z,position.z,height)')
t=t.replace('wrapped_absolute_difference(position.z / height, level)','ra2_ground_axis_distance(position.z / height,level)');assert 'wrapped_absolute_difference' not in t
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_arrival.c';t=p.read_text(encoding='utf-8')
t,n=re.subn(r'static int32_t signed_bits\(.*?\n\}\n\nstatic int32_t wrapped_distance\(.*?\n\}\n','',t,count=1,flags=re.S);assert n==1
t=t.replace('        int32_t tolerance=signed_bits((uint32_t)level_height*2u);\n','')
t=t.replace('wrapped_distance(owner_z,state->destination.z)<tolerance','ra2_ground_within_stop_height(owner_z,state->destination.z,level_height)')
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/ground_collision.c';t=p.read_text(encoding='utf-8').replace('#include "ground_collision.h"','#include "ground_collision.h"\n#include "ground_outcome_policy.h"')
a=t.index('    if (occupation->previous_result != RA2_CELL_CLEAR)');b=t.index('    if (occupation->infantry_owner_index',a)
t=t[:a]+'''    Ra2PassageFinishState state={occupation->previous_result,(uint8_t)!!occupation->crushable_enemy_seen,
        occupation->occupation_flags,(uint8_t)!!occupation->vehicle_present,occupation->infantry_owner_index};
    int32_t result;
    Ra2OccupationRoute route=ra2_ground_occupation_route(state,&result);
    if(route==RA2_OCCUPATION_RESOLVED)return (Ra2CellPassage)result;
    if(route==RA2_OCCUPATION_CRUSH_TARGET)
        return query(context,RA2_OCCUPATION_VEHICLE_CRUSHABLE) ? RA2_CELL_CLEAR:RA2_CELL_MOVING_OBSTACLE;
'''+t[b:];p.write_text(t,encoding='utf-8',newline='\n')
write(S/'implementation.json',dict(passed=True,map_service='0x0055A660',new_map_rule=False,new_fairness_scheduler=False,stop_comparisons='strict distance and strict wrapped height',occupation_decision_shared=True,callback_order_preserved=True,generated_change_only_one_nonalias_function=True,compiler_inputs_added=1))
print(dict(passed=True,map_bounds=True,shared_stop_rules=True,shared_occupation=True))
