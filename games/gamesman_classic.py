import json, requests
from .models import DataProvider, Remoteness
from .multipart_handler import multipart_solve

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

    @staticmethod
    def start_position(game_id, variant_id):
        tempurl = f"{GamesmanClassic.url}{game_id}/{variant_id}/start/"
        data = GamesmanClassic.read_from_url(tempurl)
        return {
            'position': data.get('position', ''),
            'autoguiPosition': data.get('autoguiPosition', '')
        }
    
    @staticmethod
    def position_data(game_id, variant_id, position):
        def wrangle_next_stat(next_stat):
            # Rename members
            if next_stat['positionValue'] == 'draw':
                next_stat['remoteness'] = Remoteness.INFINITY
            if 'from' in next_stat:
                next_stat.pop('from')
            return next_stat
        
        def filter_multipart_by_frompos(next_stat):
            return 'from' not in next_stat or next_stat['from'] == position
        
        tempurl = f"{GamesmanClassic.url}{game_id}/{variant_id}/positions/{position}/"
        stat = GamesmanClassic.read_from_url(tempurl)

        if "multipart" in stat: # Response includes multipart move data.
            v, r, m = multipart_solve(position, stat)
            stat["value"] = v
            stat["remoteness"] = r
            stat["moves"] = m
            stat.pop("multipart")

        if stat['positionValue'] == 'draw':
            stat['remoteness'] = Remoteness.INFINITY
        stat['moves'] = list(map(wrangle_next_stat,list(filter(filter_multipart_by_frompos, stat['moves']))))
        return stat