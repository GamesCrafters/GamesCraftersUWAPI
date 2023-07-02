import json

import requests
from requests.exceptions import HTTPError

from .models import DataProvider, AbstractGameVariant
from .uwapi import TURN_A, TURN_B, \
    board_regular2d_parse_position_string, \
    board_regular2d_make_position_string
from .utils import wrap


class GamesmanJavaDataProvider(DataProvider):
    # Use top url when running on a different machine,
    # use bottom when running on main gamesman server.
    url = "https://nyc.cs.berkeley.edu/gcweb/service/gamesman/puzzles/"
    # url = "https://localhost/gcweb/service/gamesman/puzzles/

    @staticmethod
    def start_position(game_id, variant_id):
        return GamesmanJavaDataProvider.getStart(game_id, variant_id)

    @staticmethod
    def stat(game_id, variant_id, position):
        stat = GamesmanJavaDataProvider.getMoveValue(
            game_id, position, variant_id)
        stat['position'] = stat.pop('board')
        stat['positionValue'] = stat.pop('value')
        return stat

    @staticmethod
    def next_stats(game_id, variant_id, position):
        def wrangle_next_stat(next_stat):
            next_stat['position'] = next_stat.pop('board')

            move_value = next_stat.pop('value')
            next_stat['moveValue'] = move_value

            if move_value == 'win':
                position_value = 'lose'
            elif move_value == 'lose':
                position_value = 'win'
            else:
                position_value = move_value
            next_stat['positionValue'] = position_value

            return next_stat

        return list(map(wrangle_next_stat,
                        GamesmanJavaDataProvider.getNextMoveValues(game_id, position, variant_id)))

    @staticmethod
    def getStart(game, variation):
        """Get starting position of game
        """
        if game == "connect4" or game == "ttt":
            width = int(variation[7])
            height = int(variation[16])
            return " " * (width * height)

    @staticmethod
    def getNextMoveValues(game, board, variation):
        """Get values for the next moves
        """
        try:
            tempurl = GamesmanJavaDataProvider.url + \
                game + "/getNextMoveValues" + ";board=" + board + \
                variation
            response = requests.get(tempurl)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]

    @staticmethod
    def getMoveValue(game, board, variation):
        """Check move value of current position
        """
        try:
            tempurl = GamesmanJavaDataProvider.url + \
                game + "/getMoveValue" + ";board=" + board + \
                variation
            response = requests.get(tempurl)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return json.loads(response.content)["response"]


class GamesmanJavaConnect4GameVariant(AbstractGameVariant):
    """
    Special game variant for connect 4
    """

    game_id = 'connect4'

    def __init__(self, width, height, pieces, status='stable', gui_status='v0'):
        super(GamesmanJavaConnect4GameVariant, self).__init__(
            name=f"{width}x{height}x{pieces}",
            desc=f"{width}x{height} board with {pieces} pieces in a row",
            status=status,
            gui_status=gui_status
        )
        self.width = width
        self.height = height
        self.pieces = pieces

    @staticmethod
    def get_turn(board):
        num_placed_pieces = len(board) - board.count(' ')
        return TURN_A if num_placed_pieces % 2 == 0 else TURN_B

    def convert_to_position(self, board):
        turn = self.get_turn(board)
        board = board.replace(' ', '-')
        board = ''.join(wrap(board, self.width)[::-1])  # Vertical flip
        return board_regular2d_make_position_string(turn, self.height, self.width, board)

    def convert_to_board(self, position):
        match = board_regular2d_parse_position_string(position)
        if not match:
            return None

        _, num_rows, num_columns, board = match
        
        # Check width & height
        if num_rows != self.height or num_columns != self.width:
            return None

        board = ''.join(wrap(board, self.width)[::-1])  # Vertical flip
        board = board.replace('-', ' ')
        return board

    def start_position(self):
        position = GamesmanJavaDataProvider.start_position(
            self.game_id,
            f";width={self.width};height={self.height};pieces={self.pieces}"
        )
        return self.convert_to_position(position)

    def stat(self, position):
        # Get board from UWAPI position string
        board = self.convert_to_board(position)
        if not board:
            return None

        stat = GamesmanJavaDataProvider.stat(
            self.game_id,
            f";width={self.width};height={self.height};pieces={self.pieces}",
            board
        )

        # Convert board to UWAPI position string
        stat['position'] = self.convert_to_position(stat['position'])

        return stat

    def next_stats(self, position):
        # Get board from UWAPI position string
        board = self.convert_to_board(position)
        if not board:
            return None

        next_stats = GamesmanJavaDataProvider.next_stats(
            self.game_id,
            f";width={self.width};height={self.height};pieces={self.pieces}",
            board
        )
        if next_stats is None:
            return None

        turn = self.get_turn(board)
        piece = 'X' if turn == TURN_A else 'O'

        def wrangle_next_stat(next_stat):
            # Convert board to UWAPI position string
            next_stat['position'] = self.convert_to_position(
                next_stat['position'])

            # Convert move string
            column = int(next_stat['move'])
            rows = board[column::self.width]
            empty_row = self.height - 1 - rows.index(' ')
            next_stat['move'] = f"A_{piece}_{empty_row * self.width + column}"

            return next_stat

        return list(map(wrangle_next_stat, next_stats))
