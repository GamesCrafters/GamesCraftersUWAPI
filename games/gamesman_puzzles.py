import json, requests
from .models import DataProvider

class GamesmanPuzzles(DataProvider):
    # Use first url when running on a different machine,
    # use second when running on main gamesman server.
    #url = "https://nyc.cs.berkeley.edu/puzzles/"
    url = "http://localhost:9001/"

    def read_from_url(tempurl):
        try:
            response = requests.get(tempurl)
            response.raise_for_status()
        except Exception as err:
            print(f'Error occurred: {err}')
            return {}
        return json.loads(response.content)

    def start_position(puzzle_id, variant_id):
        tempurl = f"{GamesmanPuzzles.url}{puzzle_id}/{variant_id}/start"
        data = GamesmanPuzzles.read_from_url(tempurl)
        return {
            'position': data.get('position', ''),
            'autoguiPosition': data.get('autoguiPosition', '')
        }

    def position_data(puzzle_id, variant_id, position):
        tempurl = f"{GamesmanPuzzles.url}{puzzle_id}/{variant_id}/positions/?p={position}"
        return GamesmanPuzzles.read_from_url(tempurl)