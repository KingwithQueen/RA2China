#pragma once
#include "ground_collision.h"
#include "ground_failure.h"

typedef enum Ra2GroundFailureDecision
{
    RA2_FAILURE_PLAN_CLEAR_PENDING,
    RA2_FAILURE_PLAN_RETRY_REVEALED,
    RA2_FAILURE_PLAN_RETRY_CLASSIFIED,
    RA2_FAILURE_PLAN_STOP_ONLY,
    RA2_FAILURE_PLAN_STOP_DIRECT,
    RA2_FAILURE_PLAN_STOP_SAVED
} Ra2GroundFailureDecision;

/* Classified but nonblocked obstacles clear pending even when retry is allowed.
   Pass already-read scalar values; entry may be inspected more than once. */
#define RA2_GROUND_FAILURE_DECISION_VALUE(entry, may_retry, classification) \
    ((entry) == RA2_FAILURE_CLASSIFIED_OBSTACLE \
        ? ((classification) != RA2_CELL_BLOCKED ? RA2_FAILURE_PLAN_CLEAR_PENDING \
            : (may_retry) ? RA2_FAILURE_PLAN_RETRY_CLASSIFIED : RA2_FAILURE_PLAN_STOP_SAVED) \
        : (entry) == RA2_FAILURE_REVEALED_OBSTACLE \
            ? ((may_retry) ? RA2_FAILURE_PLAN_RETRY_REVEALED : RA2_FAILURE_PLAN_STOP_DIRECT) \
            : (entry) == RA2_FAILURE_STOP_ONLY ? RA2_FAILURE_PLAN_STOP_ONLY \
            : ((entry) == RA2_FAILURE_CLEAR_SAVED_SEGMENT || (entry) == RA2_FAILURE_CLEAR_SAVED_TAIL) \
                ? RA2_FAILURE_PLAN_STOP_SAVED : RA2_FAILURE_PLAN_STOP_DIRECT)

/* Valid only for retry decisions: a classified retry discards the old heading. */
#define RA2_GROUND_FAILURE_RETRY_PATH_VALUE(decision, rejected_direction) \
    ((decision) == RA2_FAILURE_PLAN_RETRY_CLASSIFIED ? -1 : (int32_t)(rejected_direction))
