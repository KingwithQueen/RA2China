#include <string.h>
#include "ground_transition_rules.h"
#include "ground_bridge_plane.h"

static int32_t signed_bits(uint32_t bits)
{ int32_t result; memcpy(&result,&bits,sizeof(result)); return result; }

int32_t ra2_ground_layer_reference(int32_t level, unsigned upper)
{ return signed_bits((uint32_t)level+(upper?4u:0u)); }

int32_t ra2_ground_check_height_step(int32_t from_level, int32_t to_level,
    int32_t reference, uint32_t from_flags, uint32_t to_flags,
    unsigned from_ramp, unsigned to_ramp, uint8_t *changing_layer)
{
    unsigned bridge=from_flags&0x100u;
    int32_t difference=signed_bits((uint32_t)(bridge?from_level:reference)-(uint32_t)to_level);
    uint32_t magnitude=difference<0?0u-(uint32_t)difference:(uint32_t)difference;
    switch(magnitude)
    {
        case 0:
            if((to_flags&0x300u)==0x300u && bridge) return 0;
            return reference==-1 || reference==to_level ? 0 : 7;
        case 1:
            return (difference>0?to_ramp:from_ramp) ? 0 : 7;
        case 4:
            if(ra2_ground_bridge_height_matches(to_level,from_level)
                && (reference!=to_level || !bridge)) return 7;
            if(ra2_ground_bridge_height_matches(from_level,to_level))
            {
                if((to_flags&0x300u)!=0x300u) return 7;
                *changing_layer=1;
            }
            return 0;
        default: return 7;
    }
}
