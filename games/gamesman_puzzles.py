import json

import requests
from requests.exceptions import HTTPError

from .models import DataProvider, Remoteness
from .randomized_start import *

class GamesmanPuzzlesDataProvider(DataProvider):
    # Use first url when running on a different machine,
    # use second when running on main gamesman server.
    #url = "http://nyc.cs.berkeley.edu:9001/"
    url = "http://localhost:9001/"

    @staticmethod
    def start_position(game_id, variant_id):
        if game_id in random_start_funcs:
            return get_random_start(game_id, variant_id)
        return GamesmanPuzzlesDataProvider.getStart(game_id, variant_id)

    @staticmethod
    def position_data(game_id, variant_id, position):
        
        stat = GamesmanPuzzlesDataProvider.getPosition(game_id, position, variant_id)
        if stat is None:
            return None
            
        stat['position'] = stat.pop('board')
        stat['positionValue'] = stat.pop('value')
        if stat['positionValue'] == 'tie' and stat['remoteness'] == 255:
            stat['positionValue'] = 'draw'
            stat['remoteness'] = Remoteness.INFINITY
        return stat

    @staticmethod
    def getStart(game, variation=-1):
        """Get starting position of game"""
        try:
            tempurl = GamesmanPuzzlesDataProvider.url + game + "/start"
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
    def getPosition(game, board, variation=-1):
        """Get values for the next moves"""
        try:
            tempurl = GamesmanPuzzlesDataProvider.url + game + \
                "/position" + "?board=" + board
            if variation != -1:
                tempurl += "&number=" + str(variation)
            response = requests.get(tempurl)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            content = json.loads(response.content)
            if "response" not in content:
                return None
            return content["response"]