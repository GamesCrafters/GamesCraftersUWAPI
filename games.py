import json

import requests
from requests.exceptions import HTTPError


# Definitions


class Game:
    """Record keeping for a game
    """

    def __init__(self, name, desc, variants):
        assert isinstance(name, str), 'name must be a string'
        assert isinstance(desc, str), 'desc must be a string'
        assert isinstance(variants, dict), 'variants must be a dict'

        self.name = name
        self.desc = desc
        self.variants = variants

    def variant(self, variant_id):
        return self.variants.get(variant_id, None)


class GameVariant:
    """Record keeping for a variant of a game
    """

    def __init__(self, name, desc, data_provider, data_provider_game_id, data_provider_variant_id):
        assert isinstance(name, str), 'name must be a string'
        assert isinstance(desc, str), 'desc must be a string'

        self.name = name
        self.desc = desc
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


class GamesmanClassicDataProvider(DataProvider):
    url = "http://nyc.cs.berkeley.edu/classic/"

    @staticmethod
    def start_position(game_id, variant_id):
        return GamesmanClassicDataProvider.getStart(game_id, variant_id)

    @staticmethod
    def stat(game_id, variant_id, position):
        stat = GamesmanClassicDataProvider.getMoveValue(
            game_id, position, variant_id)
        stat['position'] = stat.pop('board')
        stat['positionValue'] = stat.pop('value')
        return stat

    @staticmethod
    def next_stats(game_id, variant_id, position):
        def wrangle_next_stat(next_stat):
            # Rename members
            next_stat['position'] = next_stat.pop('board')
            position_value = next_stat.pop('value')
            next_stat['positionValue'] = position_value

            # Get move value from next position value
            if position_value == 'win':
                move_value = 'lose'
            elif position_value == 'lose':
                move_value = 'win'
            else:
                move_value = position_value
            next_stat['moveValue'] = move_value

            return next_stat

        return list(map(wrangle_next_stat,
                        GamesmanClassicDataProvider.getNextMoveValues(game_id, position, variant_id)))

    @staticmethod
    def getGames():
        """Get starting position of game
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + "getGames"
            response = requests.get(tempurl)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]

    @staticmethod
    def getStart(game, variation=-1):
        """Get starting position of game
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + game + "/getStart"
            if variation != -1:
                tempurl += "?number=" + str(variation)
            response = requests.get(tempurl)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]

    @staticmethod
    def getEnd(game, board, variation=-1):
        """Check ending position of game
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + game + "/getEnd" + "?board=" + board
            response = requests.get(tempurl)
            if variation != -1:
                tempurl += "?number=" + str(variation)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]

    @staticmethod
    def getNextMoveValues(game, board, variation=-1):
        """Get values for the next moves
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + game + \
                "/getNextMoveValues" + "?board=" + board
            response = requests.get(tempurl)
            if variation != -1:
                tempurl += "?number=" + str(variation)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]

    @staticmethod
    def getMoveValue(game, board, variation=-1):
        """Check move value of current position
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + \
                game + "/getMoveValue" + "?board=" + board
            response = requests.get(tempurl)
            if variation != -1:
                tempurl += "?number=" + str(variation)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]


# Collection of games


games = {
    'ttt': Game(
        name='Tic Tac Toe',
        desc='3 in a row',
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ttt',
                data_provider_variant_id=-1)
        })
}
