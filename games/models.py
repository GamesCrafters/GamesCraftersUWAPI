from enum import Enum

class Remoteness(int, Enum):
    FINITE_UNKNOWN = -100 # finite unknown
    INFINITY = -200 # infinity


class AbstractVariant:
    """Abstract class for a variant of a game"""

    def __init__(self, name: str, gui: str = 'v0'):
        self.name = name
        self.gui = gui

    def start_position(self) -> str:
        return None

    def position_data(self, position: str):
        return None
    
    
class DataProvider:
    """Abstract class with methods for a data provider
    """

    @staticmethod
    def start_position(game_id, variant_id) -> str:
        return None

    @staticmethod
    def position_data(game_id, variant_id, position):
        return None
    

class Variant(AbstractVariant):
    """Record keeping for a variant of a game
    """

    def __init__(
            self,
            name: str,
            data_provider: DataProvider,
            data_provider_game_id: str,
            data_provider_variant_id: int | str,
            gui: str = 'v0'
        ):
        super(Variant, self).__init__(name, gui=gui)
        self.data_provider = data_provider
        self.data_provider_game_id = data_provider_game_id
        self.data_provider_variant_id = data_provider_variant_id

    def start_position(self) -> str:
        return self.data_provider.start_position(self.data_provider_game_id, self.data_provider_variant_id)

    def position_data(self, position):
        return self.data_provider.position_data(self.data_provider_game_id, self.data_provider_variant_id, position)


class Game:
    """Record keeping for a game"""

    def __init__(
            self,
            name: str,
            variants: dict[str, AbstractVariant],
            is_two_player_game: bool = True,
            custom_variant: bool = False,
            supports_win_by: bool = False,
            gui: str = 'v0'
        ):
        self.name = name
        self.variants = variants
        self.is_two_player_game = is_two_player_game
        self.custom_variant = custom_variant
        self.gui = gui
        self.supports_win_by = supports_win_by

    def variant(self, variant_id):
        variant_val = self.variants.get(variant_id, None)
        if not variant_val:
            if self.custom_variant:
                return self.custom_variant(variant_id)
        return variant_val