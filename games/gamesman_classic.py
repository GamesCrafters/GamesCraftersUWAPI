import json

import requests
from requests.exceptions import HTTPError

from .models import DataProvider
from .multipart_handler import multipart_solve


class GamesmanClassicDataProvider(DataProvider):
    # Use first url when running on a different machine,
    # use second when running on main gamesman server.
    # url = "http://nyc.cs.berkeley.edu:8083/"
    url = "http://localhost:8083/"

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
            next_stat['positionValue'] = next_stat.pop('value')
            return next_stat

        return list(map(wrangle_next_stat,
                        GamesmanClassicDataProvider.getNextMoveValues(game_id, position, variant_id)))

    @staticmethod
    def getGames():
        """Gets dictionary of all games (not fully implemented, try loading it)
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
            if variation != -1:
                tempurl += "&number=" + str(variation)
            response = requests.get(tempurl)

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
            if "multipart" in content: # Response includes multipart move data.
                return multipart_solve(board, content)
            else:
                return json.loads(response.content)["response"]

    @staticmethod
    def getMoveValue(game, board, variation=-1):
        """Check move value of current position
        """
        try:
            tempurl = GamesmanClassicDataProvider.url + \
                game + "/getMoveValue" + "?board=" + board
            if variation != -1:
                tempurl += "&number=" + str(variation)
            response = requests.get(tempurl)

            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]
