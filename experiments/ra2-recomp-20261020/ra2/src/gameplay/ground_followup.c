#include "ground_followup.h"
#include "ground_rebuild_result.h"

static unsigned highest_bit(uint64_t bits)
{
    unsigned result = 0;
    while (bits >>= 1) ++result;
    return result;
}

/* 有限原版数值的精确比较，不先舍入到 double；零的符号不影响相等。 */
static int real_compare(Ra2LegacyReal left, Ra2LegacyReal right)
{
    if (!left.significand && !right.significand) return 0;
    if (!left.significand) return right.negative ? 1 : -1;
    if (!right.significand) return left.negative ? -1 : 1;
    if (left.negative != right.negative) return left.negative ? -1 : 1;
    unsigned lb = highest_bit(left.significand), rb = highest_bit(right.significand);
    int32_t le = left.exponent + (int32_t)lb, re = right.exponent + (int32_t)rb;
    uint64_t lm = left.significand << (63 - lb), rm = right.significand << (63 - rb);
    int result = le != re ? (le > re ? 1 : -1) : (lm > rm) - (lm < rm);
    return left.negative ? -result : result;
}

void ra2_ground_prepare_speed(const Ra2GroundSpeedServices *services)
{
    void *context = services->context;
    double factor = services->value(context, RA2_SPEED_TERRAIN_FACTOR);
    if (factor > 1.0) factor = 1.0;
    services->store_factor(context, factor);

    int32_t target = services->query(context, RA2_SPEED_TARGET_SURFACE);
    int32_t current = services->query(context, RA2_SPEED_CURRENT_SURFACE);
    if (target != current && services->query(context, RA2_SPEED_OWNER_KIND) == 1)
    {
        int class_one = services->query(context, RA2_SPEED_CLASS) == 1;
        Ra2SpeedValue slope = target > current
            ? (class_one ? RA2_SPEED_UPHILL_CLASS_1 : RA2_SPEED_UPHILL_OTHER)
            : (class_one ? RA2_SPEED_DOWNHILL_CLASS_1 : RA2_SPEED_DOWNHILL_OTHER);
        double multiplier = services->value(context, slope);
        Ra2LegacyReal product = ra2_real_multiply(ra2_real_from_f64(factor),
            ra2_real_from_f64(multiplier), services->control_word(context));
        factor = ra2_real_store_f64(product, services->control_word(context));
        services->store_factor(context, factor);
    }
    if (factor == 0.0)
    {
        factor = 0.5;
        services->store_factor(context, factor);
    }
    double ratio = services->value(context, RA2_SPEED_OWNER_RATIO);
    double limit = services->value(context, RA2_SPEED_SLOW_RATIO_LIMIT);
    Ra2LegacyReal speed = ra2_real_from_f64(factor);
    if (!(ratio > limit))
    {
        speed = ra2_real_multiply(speed, ra2_real_from_f64(0.75), services->control_word(context));
        factor = ra2_real_store_f64(speed, services->control_word(context));
        services->store_factor(context, factor);
    }
    if (services->query(context, RA2_SPEED_TEMPLATE_SELECTOR) < 64)
    {
        services->apply_speed(context, factor, 1);
    }
    else
    {
        double current_speed = services->value(context, RA2_SPEED_CURRENT_UNIT_SPEED);
        if (real_compare(speed, ra2_real_from_f64(current_speed)))
        {
            services->apply_speed(context, factor, 0);
        }
    }
}

Ra2FollowupResult ra2_ground_prepare_followup(const Ra2FollowupServices *services)
{
    void *context = services->context;
    services->prepare_candidate(context);
    Ra2FollowupResult result = { services->next_direction(context), 0, 0 };
    if (result.next_direction != -1) return result;
    if (services->distance_to_destination(context) <= 512)
    {
        result.force_straight = 1;
        return result;
    }
    int train = services->is_train(context);
    int rebuilt = services->rebuild_path(context, train);
    Ra2RebuildResultServices checks = { context, services->owner_exists, services->write_aborted,
        services->destination_accepted, services->stop_navigation };
    if (ra2_ground_check_rebuild_result(rebuilt, 0, &checks) == RA2_REBUILD_NO_OWNER)
    {
        result.aborted = 1;
        return result;
    }
    /* 拒绝目标并停止后仍重取第二方向；与Prepare计时出口的直接返回不同。 */
    result.next_direction = services->next_direction(context);
    return result;
}
