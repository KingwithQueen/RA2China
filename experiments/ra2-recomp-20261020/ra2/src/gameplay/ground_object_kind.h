#pragma once
#include "ground_objects.h"

/* 已经过自身/关联对象检查的内部接续，仍按原顺序重复查询类别。 */
Ra2ObjectPassageOutcome ra2_ground_filter_object_kind(const Ra2ObjectPassageServices *services);
