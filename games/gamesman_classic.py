import json

import requests
from requests.exceptions import HTTPError

from .models import DataProvider, Remoteness
from .multipart_handler import multipart_solve
import random

class GamesmanClassic(DataProvider):
    # Use first url when running on a different machine,
    # use second when running on main gamesman server.
    #url = "http://nyc.cs.berkeley.edu:8083/"
    url = "http://localhost:8083/"

    def convert_to_new(position_str):
        """
        TEMPORARY FUNCTION TO CONVERT POSITION STRING
        IN OLD AUTOGUI FORMAT TO NEW AUTOGUI FORMAT
        """
        if position_str and len(position_str) > 2 and position_str[:2] == 'R_':
            parts = position_str.split('_', 4)
            turn = '1' if parts[1] == 'A' else '2'
            return f"{turn}_{parts[4]}"
        return position_str
    
    def convert_to_old(position_str):
        if len(position_str) > 2 and position_str[1] == '_':
            parts = position_str.split('_', 1)
            turn = 'A' if parts[0] == '1' else 'B'
            return f"R_{turn}_0_0_{parts[1]}"
        return position_str

    @staticmethod
    def start_position(game_id, variant_id):
        if game_id == 'forestfox':
            """
            THIS IS A SPECIAL CASE FOR forestfox THAT WILL
            BE REMOVED IN THE GAMESMANCLASSIC-SIDE UWAPI CHANGES.
            """
            cards = 'abcdefghijklmno'
            shuffled = ''.join(random.sample(cards, len(cards)))
            first = ''.join(sorted(shuffled[:7]))
            second = ''.join(sorted(shuffled[7:14]))
            hands = first + second + shuffled[-1]
            position = f'R_A_0_0_{hands}--00'
        else:
            position = GamesmanClassic.getStart(game_id, variant_id)
        
        position = GamesmanClassic.convert_to_new(position)
        return {
            'position': position,
            'autoguiPosition': position
        }

    @staticmethod
    def position_data(game_id, variant_id, position):
        newf_position = position
        position = GamesmanClassic.convert_to_old(position)
        def wrangle_next_stat(next_stat):
            # Rename members
            board = GamesmanClassic.convert_to_new(next_stat.pop('board'))
            next_stat['position'] = board
            next_stat['autoguiPosition'] = board
            next_stat['positionValue'] = next_stat.pop('value')
            next_stat['autoguiMove'] = next_stat.pop('move')
            moveName = next_stat.pop('moveName')
            if not moveName:
                moveName = 'zzzz' + next_stat['autoguiMove']
            next_stat['move'] = moveName
            if next_stat['positionValue'] == 'tie' and next_stat['remoteness'] == 255:
                next_stat['positionValue'] = 'draw'
                next_stat['remoteness'] = Remoteness.INFINITY
            if 'from' in next_stat:
                next_stat.pop('from')
            return next_stat
        
        def filter_multipart_by_frompos(next_stat):
            return 'from' not in next_stat or next_stat['from'] == position
        
        stat = GamesmanClassic.getPosition(game_id, position, variant_id)
        if stat is None:
            return None
        
        if 'board' in stat:
            stat.pop('board')
        stat['position'] = newf_position
        stat['autoguiPosition'] = newf_position
        stat['positionValue'] = stat.pop('value')
        if stat['positionValue'] == 'tie' and stat['remoteness'] == 255:
            stat['positionValue'] = 'draw'
            stat['remoteness'] = Remoteness.INFINITY
        stat['moves'] = list(map(wrangle_next_stat,list(filter(filter_multipart_by_frompos, stat['moves']))))
        return stat

    @staticmethod
    def getStart(game, variation=-1):
        """Get starting position of game
        """
        try:
            tempurl = GamesmanClassic.url + game + "/start"
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
            tempurl = GamesmanClassic.url + game + \
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