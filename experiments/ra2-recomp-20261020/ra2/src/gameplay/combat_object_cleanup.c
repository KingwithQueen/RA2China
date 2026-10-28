#include "combat_object_cleanup.h"

void ra2_cleanup_object_registry(const Ra2ObjectCleanupServices *s)
{
    s->begin(s->context);
    if (s->find(s->context) == -1) return;
    if (!s->can_remove(s->context)) return;
    if (!s->shrink_has_following(s->context)) return;
    while (s->shift_next(s->context)) {}
}
