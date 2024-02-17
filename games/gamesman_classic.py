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

    def read_from_url(tempurl):
        try:
            response = requests.get(tempurl)
            response.raise_for_status()
        except Exception as err:
            print(f'Error occurred: {err}')
            return {}
        return json.loads(response.content)

    #def start_position(game_id, variant_id):
        # if game_id == 'forestfox':
        #     """
        #     THIS IS A SPECIAL CASE FOR forestfox THAT WILL
        #     BE REMOVED IN THE GAMESMANCLASSIC-SIDE UWAPI CHANGES.
        #     """
        #     cards = 'abcdefghijklmno'
        #     shuffled = ''.join(random.sample(cards, len(cards)))
        #     first = ''.join(sorted(shuffled[:7]))
        #     second = ''.join(sorted(shuffled[7:14]))
        #     hands = first + second + shuffled[-1]
        #     position = f'R_A_0_0_{hands}--00'
        # else:
        #     position = GamesmanClassic.getStart(game_id, variant_id)
        
        #position = GamesmanClassic.convert_to_new(position)


        # return {
        #     'position': position,
        #     'autoguiPosition': position
        # }

    def start_position(game_id, variant_id):
        tempurl = f"{GamesmanClassic.url}{game_id}/{variant_id}/start/"
        data = GamesmanClassic.read_from_url(tempurl)
        return {
            'position': data.get('position', ''),
            'autoguiPosition': data.get('autoguiPosition', '')
        }

    def position_data(game_id, variant_id, position):
        def wrangle_next_stat(next_stat):
            # Rename members
            #if not moveName:
            #    moveName = 'zzzz' + next_stat['autoguiMove']
            if next_stat['positionValue'] == 'tie' and next_stat['remoteness'] == 255:
                next_stat['positionValue'] = 'draw'
            if next_stat['positionValue'] == 'draw':
                next_stat['remoteness'] = Remoteness.INFINITY
            if 'from' in next_stat:
                next_stat.pop('from')
            return next_stat
        
        def filter_multipart_by_frompos(next_stat):
            return 'from' not in next_stat or next_stat['from'] == position
        
        stat = GamesmanClassic.getPosition(game_id, variant_id, position)
        if stat:        
            if stat['positionValue'] == 'tie' and stat['remoteness'] == 255:
                stat['positionValue'] = 'draw'
            if stat['positionValue'] == 'draw':
                stat['remoteness'] = Remoteness.INFINITY
            stat['moves'] = list(map(wrangle_next_stat,list(filter(filter_multipart_by_frompos, stat['moves']))))
        return stat

    def getPosition(game_id, variant_id, position):
        """Get values for the next moves
        """
        tempurl = f"{GamesmanClassic.url}{game_id}/{variant_id}/positions/?p={position}"
        data = GamesmanClassic.read_from_url(tempurl)
        if "multipart" in data: # Response includes multipart move data.
            v, r, m = multipart_solve(position, data)
            data["value"] = v
            data["remoteness"] = r
            data["moves"] = m
            data.pop("multipart")
        return data