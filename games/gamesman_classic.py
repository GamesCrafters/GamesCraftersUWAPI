import json, requests
from .models import DataProvider
from .multipart_handler import multipart_wrangle

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

    def start_position(game_id, variant_id):
        tempurl = f"{GamesmanClassic.url}{game_id}/{variant_id}/start/"
        data = GamesmanClassic.read_from_url(tempurl)
        return {
            'position': data.get('position', ''),
            'autoguiPosition': data.get('autoguiPosition', '')
        }
    
    def position_data(game_id, variant_id, position):
        """
        For games with multipart moves, a position string representing an intermediate state 
        is formatted as "<real_position>;<partmove_0>;<partmove_1>;...;<partmove_N>;"

        GamesmanClassic only accepts real positions, not intermediate states, so extract
        the first part of splitting by ';'.
        """        
        real_position = position.split(';')[0]
        tempurl = f"{GamesmanClassic.url}{game_id}/{variant_id}/positions/?p={real_position}"
        data = GamesmanClassic.read_from_url(tempurl)

        if data['positionValue'] == 'tie' and data['remoteness'] == 255:
            data['positionValue'] = 'draw'
        for move in data.get('moves', []):
            if move['positionValue'] == 'tie' and move['remoteness'] == 255:
                move['positionValue'] = 'draw'

        multipart_wrangle(position, data)
        return data