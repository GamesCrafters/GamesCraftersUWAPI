#include "UWAPI_helpers.h"

#include <stdlib.h>

void UWAPI_free_nonnull_position_stats(UWAPI_PositionStats *position_stats)
{
    // NULL check
    if (!position_stats)
        return;

    UWAPI_NextPositionStats *ptr = position_stats->next;
    free(position_stats);

    while (ptr != NULL)
    {
        UWAPI_NextPositionStats *next_position_stats = ptr;
        ptr = ptr->next;

        if (next_position_stats->move)
            free(next_position_stats->move);
        if (next_position_stats->position)
            free(next_position_stats->position);
    }
}