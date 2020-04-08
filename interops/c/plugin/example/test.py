import os
from ctypes import *
from ctypes.util import find_library


UWAPI_LIBRARY = "./libUWAPI.so"
GAME_VARIANT_SERVICES_LIBRARY = "./example.so"


#
# Interfacing with libc for freeing things
#


libc = CDLL(find_library("c"))

libc_free = libc.free
libc_free.argtypes = (c_void_p,)


#
# Interfacing with user library
#


POSITION_VALUES_TEXT = {
    0: "win",
    1: "lose",
    2: "tie",
    3: "draw"
}

# We avoid receiving c_char_p when interop'ing with the library as function return type
# for "easier" memory management.
# Otherwise, we don't know the char pointers that we need to free the returned string


libUWAPI = CDLL(UWAPI_LIBRARY)

free_nonnull_position_stats = libUWAPI.UWAPI_free_nonnull_position_stats
free_nonnull_position_stats.argtypes = (c_void_p,)


class NextPositionStats(Structure):
    pass


# To workaround imcomplete types
NextPositionStats._fields_ = [
    ("move", c_char_p),
    ("position", c_char_p),
    ("remoteness", c_int),
    ("position_value", c_int),
    ("next", POINTER(NextPositionStats))
]


class PositionStats(Structure):
    _fields_ = [
        ("remoteness", c_int),
        ("position_value", c_int),
        ("next", POINTER(NextPositionStats))
    ]


class GameVariantService(Structure):
    start_type = CFUNCTYPE(c_void_p, c_void_p)
    stats_type = CFUNCTYPE(POINTER(PositionStats), c_void_p, c_char_p)

    _fields_ = [
        ("a", c_void_p),
        ("_start", start_type),
        ("_stats", stats_type)
    ]

    @property
    def start(self):
        raw_ptr = self._start(self.a)
        c_str = cast(raw_ptr, c_char_p)

        # Copy out the value
        start_position = c_str.value

        # Free the memory
        libc_free(c_str)

        # Return the Python string
        return start_position

    def stats(self, position):
        position_stats_ptr = self._stats(self.a, position)
        if not bool(position_stats_ptr):
            return  # Unexpected NULL pointer
        position_stats = position_stats_ptr.contents

        # Format response
        response = {
            'position': position,
            'remoteness': position_stats.remoteness,
            'position_value': POSITION_VALUES_TEXT[position_stats.position_value],
            'moves': [],
        }

        next_position_stats_ptr = position_stats.next
        while bool(next_position_stats_ptr):
            next_position_stats = next_position_stats_ptr.contents
            response['moves'].append({
                'move': next_position_stats.move,
                'position': next_position_stats.position,
                'remoteness': next_position_stats.remoteness,
                'position_value': POSITION_VALUES_TEXT[next_position_stats.position_value]
            })
            next_position_stats_ptr = next_position_stats.next

        # Free the memory
        free_nonnull_position_stats(position_stats_ptr)

        return response


lib = cdll.LoadLibrary(GAME_VARIANT_SERVICES_LIBRARY)

GetGameVariantService = lib.UWAPI_GetGameVariantService
GetGameVariantService.argtypes = (c_void_p, c_void_p)
GetGameVariantService.restype = POINTER(GameVariantService)

#
# Now, try an actual game
#

game = b"nto0"
variant = b"1or2"

# Get game-variant service
game_variant_service_ptr = lib.UWAPI_GetGameVariantService(game, variant)
game_variant_service = game_variant_service_ptr.contents

print("Start", game_variant_service.start)
print("Stats", game_variant_service.stats(b"C_4"))
print("Stats", game_variant_service.stats(b"C_3"))
print("Stats", game_variant_service.stats(b"C_2"))
print("Stats", game_variant_service.stats(b"C_1"))
print("Stats", game_variant_service.stats(b"C_0"))

# Free game-variant service when finished
libc_free(game_variant_service_ptr)
