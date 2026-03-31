from games.server_puzzle import ServerPuzzle

class Sokoban(ServerPuzzle):
    def __init__(self):
        super().__init__("sokoban", engine_url="http://localhost:9004")
