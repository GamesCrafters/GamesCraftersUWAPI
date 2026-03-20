# GamesCraftersUWAPI/games/sokoban.py
from games.server_puzzle import ServerPuzzle

class Sokoban(ServerPuzzle):
    def __init__(self):
        # Tells the UWAPI to forward all logic requests to your local GamesmanPy server
        super().__init__("sokoban", engine_url="http://localhost:9004")