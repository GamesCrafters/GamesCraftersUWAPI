"""
    Author: Avery Liou
"""

from .models import AbstractVariant, Remoteness

def kayles_custom_start(variant_id):
    try:
        board_len = int(variant_id)
    except Exception as err:
        return None
    return KaylesVariant(board_len, str(board_len), str(board_len))

class KaylesVariant(AbstractVariant):

    def __init__(self, board_len, name = "Custom"):
        self.board_len = board_len
        super(KaylesVariant, self).__init__(name, 'v3')

    def start_position(self):
        return "R_A_0_0_" + 'x' * self.board_len

    def stat(self, position):
        moves = self.get_moves(position)
        position_value, mex = KaylesVariant.position_value(position)

        mex_str = '0'
        if mex == 1:
            mex_str = '*'
        elif mex != 0:
            mex_str = f'*{mex}'

        response = {
            "position": position,
            "positionValue": position_value,
            "remoteness": Remoteness.FINITE_UNKNOWN if moves else 0,
            "mex": mex_str
        }
        return response

    def position_data(self, position):
        moves = self.get_moves(position)
        response = self.stat(position)
        response['moves'] = [{
            "move": move,
            "moveName": moveName,
            **self.stat(next_position)
        } for move, (next_position, moveName) in moves.items()]
        return response

    def get_position_str(position):
        return position.split('_')[4]

    def position_value(position):
        board = KaylesVariant.get_position_str(position)
        value = 0
        pile_lengths = KaylesVariant.get_pile_lengths(board)
        for pile_len in pile_lengths:
            pile_mex = KaylesVariant.get_mex(pile_len)
            value = value ^ pile_mex
        return "lose" if value == 0 else "win", value

    def get_pile_lengths(board):
        pile_lengths = []
        curr_pile = 0
        for i in range(len(board)):
            if board[i] == 'x':
                curr_pile += 1
            elif board[i] != 'x' and curr_pile != 0:
                pile_lengths.append(curr_pile)
                curr_pile = 0
        if curr_pile != 0:
            pile_lengths.append(curr_pile)
        return pile_lengths

    def get_moves(self, position):
        next_turn = 'B' if position[2] == 'A' else 'A'
        moves = {}
        
        board = list(KaylesVariant.get_position_str(position))
        for i in range(len(board)): # Single pin removals
            if board[i] == 'x':
                board[i] = '-'
                moves[f"A_-_{self.board_len + i}_x"] = (
                    f"R_{next_turn}_0_0_{''.join(board)}",
                    f"{i + 1}"
                )
                board[i] = 'x'
        for i in range(len(board) - 1): # Double pin removals
            if board[i] == 'x' and board[i + 1] == 'x':
                board[i] = '-'
                board[i + 1] = '-'
                fromIdx, toIdx = self.board_len * 2 + i, self.board_len * 3 + i
                moves[f"L_{fromIdx}_{toIdx}_x"] = (
                    f"R_{next_turn}_0_0_{''.join(board)}",
                    f"{i + 1}-{i + 2}"
                )
                board[i] = 'x'
                board[i + 1] = 'x'

        return moves

    def get_mex(board_len):
        periodic = [4, 1, 2, 8, 1, 4, 7, 2, 1, 8, 2, 7]
        exceptions = {
            0: 0,
            3: 3,
            6: 3,
            9: 4,
            11: 6,
            15: 7,
            18: 3,
            21: 4,
            22: 6,
            28: 5,
            34: 6,
            39: 3,
            57: 4,
            70: 6,
        }
        if board_len in exceptions:
            return exceptions[board_len]
        else:
            return periodic[board_len % len(periodic)]