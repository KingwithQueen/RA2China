#include <stdint.h>
#include <string.h>
#include "ground_collision.h"

int ra2_ground_uses_bridge_occupation(unsigned has_bridge, int32_t reference_level, int32_t cell_level)
{
    if (!has_bridge)
    {
        return 0;
    }
    if (reference_level == -1)
    {
        return 1;
    }
    uint32_t difference = (uint32_t)reference_level - (uint32_t)cell_level;
    if (difference & 0x80000000u)
    {
        difference = 0u - difference;
    }
    int32_t distance;
    memcpy(&distance, &difference, sizeof(distance));
    return distance > 1;
}

uint8_t ra2_ground_remove_self_occupation(uint8_t flags)
{
    /* 自己也会出现在目标格链表中；只排除自己的车辆占格位，保留五个步兵子格位。 */
    return (uint8_t)(flags & 0xDFu);
}

Ra2CellPassage ra2_ground_resolve_occupation(const Ra2CellOccupation *occupation, void *context, Ra2OccupationQueryFunction query)
{
    if (occupation->previous_result != RA2_CELL_CLEAR)
    {
        return (Ra2CellPassage)occupation->previous_result;
    }
    if (occupation->crushable_enemy_seen)
    {
        if (occupation->vehicle_present && !query(context, RA2_OCCUPATION_VEHICLE_CRUSHABLE))
        {
            return RA2_CELL_MOVING_OBSTACLE;
        }
        return RA2_CELL_CLEAR;
    }
    if (!(occupation->occupation_flags & 0x3Fu))
    {
        return RA2_CELL_CLEAR;
    }
    if (occupation->vehicle_present)
    {
        return RA2_CELL_MOVING_OBSTACLE;
    }
    if (occupation->infantry_owner_index != -1 && query(context, RA2_OCCUPATION_INFANTRY_ALLIED))
    {
        return RA2_CELL_MOVING_OBSTACLE;
    }
    if (occupation->actor_is_crusher || query(context, RA2_OCCUPATION_CRUSHER_ABILITY))
    {
        return RA2_CELL_CLEAR;
    }
    if (occupation->actor_is_train)
    {
        return RA2_CELL_DESTROYABLE;
    }
    if (!query(context, RA2_OCCUPATION_HAS_WEAPON) || !query(context, RA2_OCCUPATION_WEAPON_CAN_CLEAR))
    {
        return RA2_CELL_BLOCKED;
    }
    return RA2_CELL_DESTROYABLE;
}
