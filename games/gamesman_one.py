import json, requests
from .models import DataProvider, Remoteness

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
        tempurl = f"{GamesmanOne.url}{puzzle_id}/{variant_id}/start/"
        data = GamesmanOne.read_from_url(tempurl)
        return {
            'position': data.get('position', ''),
            'autoguiPosition': data.get('autoguiPosition', '')
        }

    def position_data(puzzle_id, variant_id, position):
        tempurl = f"{GamesmanOne.url}{puzzle_id}/{variant_id}/positions/{position}/"
        return GamesmanOne.read_from_url(tempurl)