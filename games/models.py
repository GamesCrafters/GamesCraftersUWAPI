class Game:
    """Record keeping for a game
    """

    def __init__(self, name, desc, variants, status='available'):
        assert isinstance(name, str), 'name must be a string'
        assert isinstance(desc, str), 'desc must be a string'
        assert isinstance(variants, dict), 'variants must be a dict'

        self.name = name
        self.desc = desc
        self.variants = variants
        self.status = status

    def variant(self, variant_id):
        return self.variants.get(variant_id, None)


class AbstractGameVariant:
    """Abstract class for a variant of a game
    """

    def __init__(self, name, desc, status='stable'):
        assert isinstance(name, str), 'name must be a string'
        assert isinstance(desc, str), 'desc must be a string'

        self.name = name
        self.desc = desc
        self.status = status

    def start_position(self):
        return None

    def stat(self, position):
        return None

    def next_stats(self, position):
        return None


class GameVariant(AbstractGameVariant):
    """Record keeping for a variant of a game
    """

    def __init__(self, name, desc, data_provider, data_provider_game_id, data_provider_variant_id, status='stable'):
        super(GameVariant, self).__init__(name, desc, status=status)
        self.data_provider = data_provider
        self.data_provider_game_id = data_provider_game_id
        self.data_provider_variant_id = data_provider_variant_id

    def start_position(self):
        return self.data_provider.start_position(self.data_provider_game_id, self.data_provider_variant_id)

    def stat(self, position):
        return self.data_provider.stat(self.data_provider_game_id, self.data_provider_variant_id, position)

    def next_stats(self, position):
        return self.data_provider.next_stats(self.data_provider_game_id, self.data_provider_variant_id, position)


class DataProvider:
    """Abstract class with methods for a data provider
    """

    @staticmethod
    def start_position(game_id, variant_id):
        return None

    @staticmethod
    def stat(game_id, variant_id, position):
        return None

    @staticmethod
    def next_stats(game_id, variant_id, position):
        return None
