class Game:
    """Record keeping for a game
    """

    def __init__(self, name, desc, variants, custom_variant=None, status='available', gui_status='v0', supports_win_by=0):
        assert isinstance(name, str), 'name must be a string'
        assert isinstance(desc, str), 'desc must be a string'
        assert isinstance(variants, dict), 'variants must be a dict'

        self.name = name
        self.desc = desc
        self.variants = variants
        self.custom_variant = custom_variant
        self.status = status
        self.gui_status = gui_status
        self.supports_win_by = supports_win_by

    def variant(self, variant_id):
        variant_val = self.variants.get(variant_id, None)
        if not variant_val:
            if self.custom_variant:
                return self.custom_variant(variant_id)
        return variant_val


class AbstractGameVariant:
    """Abstract class for a variant of a game
    """

    def __init__(self, name, desc, status='stable', gui_status='v0'):
        assert isinstance(name, str), 'name must be a string'
        assert isinstance(desc, str), 'desc must be a string'

        self.name = name
        self.desc = desc
        self.status = status
        self.gui_status = gui_status

    def start_position(self):
        return None

    def position_data(self, position):
        return None
    
    
class DataProvider:
    """Abstract class with methods for a data provider
    """

    @staticmethod
    def start_position(game_id, variant_id):
        return None

    @staticmethod
    def position_data(game_id, variant_id, position):
        return None
    

class GameVariant(AbstractGameVariant):
    """Record keeping for a variant of a game
    """

    def __init__(self, name, desc, data_provider, data_provider_game_id, data_provider_variant_id, status='stable', gui_status='v0'):
        super(GameVariant, self).__init__(name, desc, status=status, gui_status=gui_status)
        self.data_provider = data_provider
        self.data_provider_game_id = data_provider_game_id
        self.data_provider_variant_id = data_provider_variant_id

    def start_position(self):
        return self.data_provider.start_position(self.data_provider_game_id, self.data_provider_variant_id)

    def position_data(self, position):
        return self.data_provider.position_data(self.data_provider_game_id, self.data_provider_variant_id, position)