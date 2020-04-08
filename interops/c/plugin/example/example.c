#include <stdlib.h>
#include <string.h>

#include <UWAPI_plugin.h>
#include <UWAPI_boardstrings.h>
#include <UWAPI_helpers.h>

BOOLEAN nto0_1or2_fill_stats(int position, int *remoteness, UWAPI_PositionValue *position_value)
{
    // Ideally, we're reading from a database
    // Here we hard-code some results
    switch (position)
    {
    default:
        return FALSE; // Unexpected position
    case 0:
        *remoteness = 0;
        break;
    case 1:
        *remoteness = 1;
        break;
    case 2:
        *remoteness = 1;
        break;
    case 3:
        *remoteness = 2;
        break;
    case 4:
        *remoteness = 3;
        break;
    }
    *position_value = position % 3 == 0 ? UWAPI_VALUE_LOSE : UWAPI_VALUE_WIN;
    return TRUE;
}

char *nto0_1or2_start(void *a)
{
    return UWAPI_Board_Custom_MakePositionString("4");
}

UWAPI_PositionStats *nto0_1or2_stats(void *a, char const *str)
{
    char *position_string;
    if (!UWAPI_Board_Custom_ParsePositionString(str, &position_string))
    {
        return NULL; // Failed to parse position_string
    }

    int position = atoi(position_string);
    free(position_string); // Got the number, don't need the position_string anymore

    UWAPI_PositionStats *position_stats = calloc(1, sizeof(*position_stats));
    if (!position_stats)
        return NULL; // Failed to allocate memory

    if (!nto0_1or2_fill_stats(
            position,
            &(position_stats->remoteness),
            &(position_stats->position_value)))
    {
        // Failed to fill stats
        UWAPI_free_nonnull_position_stats(position_stats);
        return NULL;
    }

    for (int move = 1; move <= 2; move++)
    {
        if (position - move < 0)
            continue; // Skip invalid moves

        int next_position = position - 1;

        UWAPI_NextPositionStats *next_position_stats = calloc(1, sizeof(*next_position_stats));
        if (!next_position_stats)
        {
            // Failed to allocate memory
            UWAPI_free_nonnull_position_stats(position_stats);
            return NULL;
        }

        // Add to linked list of next positions
        next_position_stats->next = position_stats->next;
        position_stats->next = next_position_stats;

        // Add move to stats
        next_position_stats->move = UWAPI_ToStringi(move);

        // Add position to stats
        char *next_position_string = UWAPI_ToStringi(next_position);
        next_position_stats->position = UWAPI_Board_Custom_MakePositionString(next_position_string);
        free(next_position_string);

        if (!nto0_1or2_fill_stats(
                position,
                &(next_position_stats->remoteness),
                &(next_position_stats->position_value)))
        {
            // Failed to fill stats
            UWAPI_free_nonnull_position_stats(position_stats);
            return NULL;
        }
    }

    return position_stats;
}

UWAPI_GameVariantService *UWAPI_GetGameVariantService(char *game, char *variant)
{
    if (strcmp(game, "nto0") == 0 && strcmp(variant, "1or2") == 0)
    {
        UWAPI_GameVariantService *service = calloc(1, 100 + sizeof(*service));
        if (service == NULL)
            return service;
        service->a = NULL;
        service->start = nto0_1or2_start;
        service->stats = nto0_1or2_stats;
        return service;
    }
    return NULL;
}
