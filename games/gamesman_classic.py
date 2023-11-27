import json

import requests
from requests.exceptions import HTTPError

from .models import DataProvider
from .multipart_handler import multipart_solve
from .randomized_start import *

class GamesmanClassicDataProvider(DataProvider):
    # Use first url when running on a different machine,
    # use second when running on main gamesman server.
    #url = "http://nyc.cs.berkeley.edu:8083/"
    url = "http://localhost:8083/"

    @staticmethod
    def start_position(game_id, variant_id):
        if game_id in random_start_funcs:
            return get_random_start(game_id, variant_id)
        return GamesmanClassicDataProvider.getStart(game_id, variant_id)

    @staticmethod
    def position_data(game_id, variant_id, position):
        def wrangle_next_stat(next_stat):
            # Rename members
            next_stat['position'] = next_stat.pop('board')
            next_stat['positionValue'] = next_stat.pop('value')
            if next_stat['positionValue'] == 'tie' and next_stat['remoteness'] == 255:
                next_stat['positionValue'] = 'draw'
            if 'fromPos' in next_stat:
                next_stat.pop('fromPos')
            return next_stat
        
        def filter_multipart_by_frompos(next_stat):
            return 'fromPos' not in next_stat or next_stat['fromPos'] == position
        
        stat = GamesmanClassicDataProvider.getPosition(game_id, position, variant_id)
        if stat is None:
            return None
            
        stat['position'] = stat.pop('board')
        stat['positionValue'] = stat.pop('value')
        if stat['positionValue'] == 'tie' and stat['remoteness'] == 255:
            stat['positionValue'] = 'draw'
        stat['moves'] = list(map(wrangle_next_stat,list(filter(filter_multipart_by_frompos, stat['moves']))))
        return stat


    @staticmethod
    def getStart(game, variation=-1):
        """Get starting position of game
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + game + "/start"
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
        """Get values for the next moves
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + game + \
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
            if "multipart" in content["response"]: # Response includes multipart move data.
                v, r, m = multipart_solve(board, content["response"])
                content["response"]["value"] = v
                content["response"]["remoteness"] = r
                content["response"]["moves"] = m
                content["response"].pop("multipart")
            return content["response"]