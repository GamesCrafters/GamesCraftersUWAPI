import json

from .models import AbstractGameVariant

def nim_custom_start(variant_id):
    try:
        piles = variant_id.split('_')
        for i in range(len(piles)):
            piles[i] = int(piles[i])
    except Exception as err:
        return None
    return NimGameVariant(piles)

class NimGameVariant(AbstractGameVariant):

    piece_char = 'l'

    def __init__(self, start_piles):
        name = "custom"
        desc = "custom"
        status = "stable"
        self.start_piles = start_piles
        self.board_rows = max(self.start_piles)
        self.board_cols = len(self.start_piles)
        super(NimGameVariant, self).__init__(name, desc, status)

    def start_position(self):
        return NimGameVariant.getUWAPIPos(self.board_rows, self.board_cols, self.start_piles, "A")

    def stat(self, position):
        try:
            position_arr = NimGameVariant.get_position_arr(position, self.board_rows, self.board_cols)
            position_value = NimGameVariant.position_value(position_arr)
            remoteness = 1
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = {
                "position": position,
                "positionValue": position_value,
                "remoteness": remoteness,
            }
            return response

    def next_stats(self, position):
        rows = self.board_rows
        cols = self.board_cols
        try:
            position_arr = NimGameVariant.get_position_arr(position, rows, cols)
            player = NimGameVariant.get_player(position)
            moves = NimGameVariant.get_moves(position_arr, rows, cols, player)
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = [{
                "move": move,
                **self.stat(position)
            } for move, position in moves.items()]
            return response

    def getUWAPIPos(rows, cols, position_arr, player):
        elements = ['R', player, rows, cols]
        board_str = ""
        for i in range(cols):
            num_pieces = position_arr[i]
            next_col = NimGameVariant.piece_char * num_pieces + "-" * (rows - num_pieces)
            board_str += next_col

        board_str = NimGameVariant.rotateBoardStr(board_str, rows, cols)
        elements.append(board_str)
        return "_".join(map(str, elements))

    def rotateBoardStr(board_str, rows, cols):
        new_board_str = ""
        for i in range(rows):
            for j in range(cols):
                start_index = j * rows
                offset = rows - i - 1
                new_board_str += board_str[start_index + offset]
        return new_board_str

    def get_player(position_str):
        return position_str.split('_')[1]

    def get_board_str(position_str):
        return position_str.split('_')[4]

    def position_value(position_arr):
        value = 0
        for pile in position_arr:
            value = value ^ int(pile)
        if value == 0:
            return "lose"
        return "win"

    def get_position_arr(position_str, rows, cols):
        board_str = NimGameVariant.get_board_str(position_str)
        assert(rows * cols == len(board_str))

        piles = []
        for i in range(cols):
            pile_sum = 0
            for j in range(rows):
                index = i + j * cols
                if board_str[index] == NimGameVariant.piece_char:
                    pile_sum += 1
            piles.append(pile_sum)
        return piles

    def get_moves(position_arr, rows, cols, player):
        move_arr = ["A", NimGameVariant.piece_char, 0]
        moves = {}
        for i in range(len(position_arr)):
            pile_amount = position_arr[i]
            for j in range(pile_amount):
                row_coord = rows - j - 1
                placement = row_coord * cols + i
                move_arr[2] = str(placement)
                move = '_'.join(move_arr)

                next_position = position_arr[:]
                next_position[i] = j
                next_position_str = NimGameVariant.getUWAPIPos(rows, cols, next_position, NimGameVariant.next_player(player))

                moves[move] = next_position_str
        return moves

    def next_player(player):
        return 'B' if player == 'A' else 'A'
