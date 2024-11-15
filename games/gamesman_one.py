import json, requests
from .models import DataProvider
from .multipart_handler import multipart_wrangle

class GamesmanOne(DataProvider):
    # Use first url when running on a different machine,
    # use second when running on main gamesman server.
    #url = "http://nyc.cs.berkeley.edu:8084/"
    url = "http://localhost:8084/"

    def read_from_url(tempurl):
        try:
            response = requests.get(tempurl)
            response.raise_for_status()
        except Exception as err:
            print(f'Error occurred: {err}')
            return {}
        return json.loads(response.content)

    def start_position(puzzle_id, variant_id):
        tempurl = f"{GamesmanOne.url}{puzzle_id}/{variant_id}/"
        data = GamesmanOne.read_from_url(tempurl)
        return {
            'position': data.get('position', ''),
            'autoguiPosition': data.get('autoguiPosition', '')
        }

    def position_data(puzzle_id, variant_id, position):
        # Copied from games/gamesman_classic.py
        real_position = position.split(';')[0]
        tempurl = f"{GamesmanOne.url}{puzzle_id}/{variant_id}/{real_position}"
        data = GamesmanOne.read_from_url(tempurl)
        
        multipart_wrangle(position, data)
        return data
