import json

import requests
from requests.exceptions import HTTPError

from .models import DataProvider

class GamesmanJavaDataProvider(DataProvider):
    # Use top url when running on a different machine,
    # use bottom when running on main gamesman server.
    url = "https://nyc.cs.berkeley.edu/gcweb/service/gamesman/puzzles/"

    @staticmethod
    def start_position(game_id, variant_id):
        return GamesmanJavaDataProvider.getStart(game_id, variant_id)

    @staticmethod
    def stat(game_id, variant_id, position):
        stat = GamesmanJavaDataProvider.getMoveValue(
            game_id, position, variant_id)
        stat['position'] = stat.pop('board')
        stat['positionValue'] = stat.pop('value')
        return stat

    @staticmethod
    def next_stats(game_id, variant_id, position):
        def wrangle_next_stat(next_stat):
            # Rename members
            next_stat['position'] = next_stat.pop('board')
            next_stat['positionValue'] = next_stat.pop('value')
            return next_stat

        return list(map(wrangle_next_stat,
                        GamesmanJavaDataProvider.getNextMoveValues(game_id, position, variant_id)))


    @staticmethod
    def getStart(game, variation):
        """Get starting position of game
        """
        if (game == "connect4" or game == "ttt"):
            width = int(variation[7])
            height = int(variation[16])
            str = ""
            for i in range(width*height):
                str += "%20"
            return str



    @staticmethod
    def getNextMoveValues(game, board, variation):
        """Get values for the next moves
        """
        try:
            tempurl = GamesmanJavaDataProvider.url + \
                game + "/getNextMoveValues" + ";board=" + board + \
                variation
            response = requests.get(tempurl)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]

    @staticmethod
    def getMoveValue(game, board, variation):
        """Check move value of current position
        """
        try:
            tempurl = GamesmanJavaDataProvider.url + \
                game + "/getMoveValue" + ";board=" + board + \
                variation
            response = requests.get(tempurl)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]
