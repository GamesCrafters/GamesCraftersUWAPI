#ifndef UWAPI_INTERFACE_H
#define UWAPI_INTERFACE_H

enum UWAPI_PositionValue;
struct UWAPI_PositionStats;
struct UWAPI_NextPositionStats;

/**
 * UWAPI_PositionValue
 * 
 * The possible values for a position.
 */
typedef enum UWAPI_PositionValue
{
    UWAPI_VALUE_WIN = 0,
    UWAPI_VALUE_LOSE = 1,
    UWAPI_VALUE_TIE = 2,
    UWAPI_VALUE_DRAW = 3
} UWAPI_PositionValue;

/**
 * UWAPI_PositionStats
 *
 * The stats for some position.
 * The next moves are available as a linked list.
 */
typedef struct UWAPI_PositionStats
{
    int remoteness;
    UWAPI_PositionValue position_value;
    struct UWAPI_NextPositionStats *next;
} UWAPI_PositionStats;

/**
 * UWAPI_NextPositionStats
 * 
 * The structure is very similar to the one above, except with an additional
 * property to store the move to take to arrive on the position.
 */
typedef struct UWAPI_NextPositionStats
{
    char *move;
    char *position;
    int remoteness;
    UWAPI_PositionValue position_value;
    struct UWAPI_NextPositionStats *next;
} UWAPI_NextPositionStats;

/**
 * UWAPI_GameVariantService
 */
typedef struct UWAPI_GameVariantService
{
    /**
     * Anything! You may use this to identify the variant or
     * point to some game configurations.
     */
    void *a;

    /**
     * The start position of the game.
     */
    char *(*start)(void *a);

    /**
     * The stats of the given game position.
     */
    UWAPI_PositionStats *(*stats)(void *a, char const *position);
} UWAPI_GameVariantService;

// Methods

extern UWAPI_GameVariantService *UWAPI_GetGameVariantService(char *game, char *variant);

#endif // UWAPI_INTERFACE_H