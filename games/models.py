from enum import Enum
from typing import TypedDict, Union

class StartPosition(TypedDict):
    position: str
    autoguiPosition: str

class Value(str, Enum):
    WIN = 'win'
    TIE = 'tie'
    DRAW = 'draw'
    LOSE = 'lose'
    UNDECIDED = 'undecided'
    UNSOLVED = 'unsolved'

class Remoteness(int, Enum):
    FINITE_UNKNOWN = -100 # finite unknown
    INFINITY = -200 # infinity
    MAX = 65536 # max

class AbstractVariant:
    """Abstract class for a variant of a game"""

    def __init__(self, name: str, gui: str = 'v0'):
        self.name = name
        self.gui = gui

    def start_position(self) -> StartPosition:
        return None

    def position_data(self, position: str):
        return None
    
    
class DataProvider:
    """Abstract class with methods for a data provider
    """

    def start_position(game_id, variant_id):
        return None

    def position_data(game_id, variant_id, position):
        """ Return an empty dict if error """
        return None
    

class Variant(AbstractVariant):
    """Record keeping for a variant of a game
    """

    def __init__(
            self,
            name: str,
            data_provider: DataProvider,
            data_provider_game_id: str,
            data_provider_variant_id: Union[int, str], 
            gui: str = 'v0'
        ):
        super(Variant, self).__init__(name, gui=gui)
        self.data_provider = data_provider
        self.data_provider_game_id = data_provider_game_id
        self.data_provider_variant_id = data_provider_variant_id

    def start_position(self) -> StartPosition:
        return self.data_provider.start_position(self.data_provider_game_id, self.data_provider_variant_id)

    def position_data(self, position: str):
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