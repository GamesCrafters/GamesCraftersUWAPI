"""
    Author: Avery Liou
"""

from .models import AbstractVariant, Remoteness

def dawsonschess_custom_start(variant_id):
    try:
        board_len = int(variant_id)
    except Exception as err:
        return None
    return DawsonsChessVariant(board_len, str(board_len))

class DawsonsChessVariant(AbstractVariant):

    def __init__(self, board_len, name = "Custom"):
        self.board_len = board_len
        super(DawsonsChessVariant, self).__init__(name, 'v3')

    def start_position(self):
        return {
            'position': '1_' + '-' * self.board_len,
            'autoguiPosition': '1_' + 'b' * self.board_len
        }

    def position_data(self, position):
        response = self.stat(position)
        response['moves'] = [{
            'move': move,
            'autoguiMove': autogui_move,
            **self.stat(child_position)
        } for move, autogui_move, child_position in DawsonsChessVariant.get_moves(position)]
        return response
    
    def stat(self, position):
        mex = 0
        pile_lengths = [len(contiguous_blanks) - 2 for contiguous_blanks in ('-' + position[2:] + '-').split('x') if len(contiguous_blanks) > 2]
        for pile_length in pile_lengths:
            mex ^= DawsonsChessVariant.get_mex(pile_length)
        
        return {
            'position': position,
            'autoguiPosition': ''.join(['b' if c == '-' else c for c in position]),
            'positionValue': "lose" if mex == 0 else "win",
            'remoteness': Remoteness.FINITE_UNKNOWN if DawsonsChessVariant.get_moves(position) else 0,
            'mex': '*' if mex == 1 else f'*{mex}' if mex > 0 else '0'
        }

    def get_moves(position):
        player, board = position.split('_')
        next_player = '2' if player == '1' else '1'
        next_board = list(board)
        moves = []
        for i in range(len(board)):
            if board[i] == '-' and (i == 0 or board[i - 1] == '-') and (i == (len(board) - 1) or board[i + 1] == '-'):
                next_board[i] = 'x'
                moves.append([f'{i + 1}', f'A_t_{i}_x', f"{next_player}_{''.join(next_board)}"])
                next_board[i] = '-'
        return moves

    def get_mex(pile_length):
        if pile_length in [0, 14, 34]:
            return 0
        elif pile_length in [16, 17, 31, 51]:
            return 2
        periodic = [8, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 9, 3, 3, 0, 1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 3, 7, 4]
        return periodic[pile_length % 34]