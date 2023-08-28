import json

from .models import AbstractGameVariant

def dawsonschess_custom_start(variant_id):
    try:
        board_len = int(variant_id)
    except Exception as err:
        return None
    return DawsonsChessGameVariant(board_len)

class DawsonsChessGameVariant(AbstractGameVariant):

    def __init__(self, board_len):
        name = "custom"
        desc = "custom"
        status = "stable"
        gui_status = "v2"
        self.board_str = ''.join(['b' for i in range(board_len)])
        super(DawsonsChessGameVariant, self).__init__(name, desc, status, gui_status)

    def start_position(self):
        return DawsonsChessGameVariant.getUWAPIPos(1, len(self.board_str), self.board_str, "A")

    def stat(self, position):
        try:
            position_str = DawsonsChessGameVariant.get_position_str(position)
            position_value = DawsonsChessGameVariant.position_value(position_str)
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
        try:
            position_str = DawsonsChessGameVariant.get_position_str(position)
            player = DawsonsChessGameVariant.get_player(position)
            moves = DawsonsChessGameVariant.get_moves(position_str, player)
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = [{
                "move": move[0],
                "moveName": move[1],
                **self.stat(position)
            } for move, position in moves.items()]
            return response

    def getUWAPIPos(rows, cols, board_str, player):
        elements = ['R', player, rows, cols, board_str]
        return "_".join(map(str, elements))

    def get_player(position):
        return position.split('_')[1]

    def get_position_str(position):
        return position.split('_')[4]

    def position_value(position):
        value = 0
        pile_lengths = DawsonsChessGameVariant.get_pile_lengths(position)
        for pile_len in pile_lengths:
            pile_mex = DawsonsChessGameVariant.get_mex(pile_len)
            value = value ^ pile_mex
        if value == 0:
            return "lose"
        return "win"

    def get_pile_lengths(position):
        pile_lengths = []
        curr_pile = 0
        for i in range(len(position)):
            if position[i] == 'b':
                curr_pile += 1
            elif position[i] != 'b' and curr_pile != 0:
                pile_lengths.append(curr_pile)
                curr_pile = 0
        if curr_pile != 0:
            pile_lengths.append(curr_pile)
        return pile_lengths


    def get_moves(position, player):
        move_arr = ["A", '-', 0, 'x']
        moves = {}
        for i in range(len(position)):
            if position[i] == 'b':
                move_arr[2] = str(i)
                move = '_'.join(move_arr)

                next_position = list(position)
                next_position[i] = 'x'
                if i > 0:
                    next_position[i-1] = 'o'
                if i < len(position) - 1:
                    next_position[i+1] = 'o'
                next_position = ''.join(next_position)

                next_position_uwapi = DawsonsChessGameVariant.getUWAPIPos(1, len(position), next_position, DawsonsChessGameVariant.next_player(player))

                moves[(move, i)] = next_position_uwapi
        return moves

    def next_player(player):
        return 'B' if player == 'A' else 'A'

    def get_mex(board_len):
        periodic = [8, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 9, 3, 3, 0, 1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 3, 7, 4]
        zero_exceptions = [0, 14, 34]
        two_exceptions = [16, 17, 31, 51]

        if board_len in zero_exceptions:
            return 0
        elif board_len in two_exceptions:
            return 2
        else:
            return periodic[board_len % 34]
