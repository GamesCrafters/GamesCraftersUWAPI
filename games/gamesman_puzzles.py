import json, requests
from .models import DataProvider, Remoteness

class GamesmanPuzzlesDataProvider(DataProvider):
    # Use first url when running on a different machine,
    # use second when running on main gamesman server.
    #url = "http://nyc.cs.berkeley.edu:9001/"
    url = "http://localhost:9001/"

    @staticmethod
    def start_position(puzzle_id, variant_id):
        """Get starting position of game"""
        try:
            tempurl = f"{GamesmanPuzzlesDataProvider.url}{puzzle_id}/{variant_id}/start"
            response = requests.get(tempurl)
            response.raise_for_status()
        except Exception as err:
            print(f'Error occurred: {err}')
        else:
            return json.loads(response.content)['startPosition']

    @staticmethod
    def position_data(puzzle_id, variant_id, position):
        """Get position data """
        try:
            tempurl = f"{GamesmanPuzzlesDataProvider.url}{puzzle_id}/{variant_id}/positions/{position}"
            response = requests.get(tempurl)
            response.raise_for_status()
        except Exception as err:
            print(f'Error occurred: {err}')
        else:
            return json.loads(response.content)