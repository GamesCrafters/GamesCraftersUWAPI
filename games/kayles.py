"""
    Author: Avery Liou
"""

from .models import AbstractVariant, Remoteness

def kayles_custom_start(variant_id):
    try:
        board_len = int(variant_id)
    except Exception as err:
        return None
    return KaylesVariant(board_len, str(board_len))

class KaylesVariant(AbstractVariant):

    def __init__(self, board_len, name = "Custom"):
        self.board_len = board_len
        super(KaylesVariant, self).__init__(name, 'v3')
    
    def start_position(self):
        return {
            'position': '1_' + 'x' * self.board_len,
            'autoguiPosition': '1_' + 'x' * self.board_len
        }
    
    def position_data(self, position):
        response = self.stat(position)
        response['moves'] = [{
            'move': move,
            'autoguiMove': autogui_move,
            **self.stat(child_position)
        } for move, autogui_move, child_position in self.get_moves(position)]
        return response
    
    def stat(self, position):
        mex = 0
        for pile_length in KaylesVariant.get_pile_lengths(position[2:]):
            mex ^= KaylesVariant.get_mex(pile_length)
        
        return {
            'position': position,
            'autoguiPosition': position,
            'positionValue': "lose" if mex == 0 else "win",
            'remoteness': Remoteness.FINITE_UNKNOWN if self.get_moves(position) else 0,
            'mex': '*' if mex == 1 else f'*{mex}' if mex > 0 else '0'
        }

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
        next_player = '2' if position[0] == '1' else '1'
        next_board = list(position[2:])

        moves = []
        for i in range(len(next_board)): # Single pin removals
            if next_board[i] == 'x':
                next_board[i] = '-'
                moves.append([
                    f"{i + 1}",
                    f"A_-_{self.board_len + i}_x",
                    f"{next_player}_{''.join(next_board)}"])
                next_board[i] = 'x'
        for i in range(len(next_board) - 1): # Double pin removals
            if next_board[i] == 'x' and next_board[i + 1] == 'x':
                next_board[i] = '-'
                next_board[i + 1] = '-'
                from_idx, to_idx = self.board_len * 2 + i, self.board_len * 3 + i
                moves.append([
                    f"{i + 1}-{i + 2}",
                    f"L_{from_idx}_{to_idx}_x",
                    f"{next_player}_{''.join(next_board)}"
                ])
                next_board[i] = 'x'
                next_board[i + 1] = 'x'
        return moves

    def get_mex(pile_length):
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
        if pile_length in exceptions:
            return exceptions[pile_length]
        else:
            return periodic[pile_length % len(periodic)]
