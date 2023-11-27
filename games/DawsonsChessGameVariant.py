from .models import AbstractGameVariant

def dawsonschess_custom_start(variant_id):
    try:
        board_len = int(variant_id)
    except Exception as err:
        return None
    return DawsonsChessGameVariant(board_len, str(board_len), str(board_len))

class DawsonsChessGameVariant(AbstractGameVariant):

    def __init__(self, board_len, name = "Custom", desc = "Custom"):
        status = "stable"
        gui_status = "v3"
        self.board_len = board_len
        super(DawsonsChessGameVariant, self).__init__(name, desc, status, gui_status)

    def start_position(self):
        return "R_A_0_0_" + 'b' * self.board_len

    def stat(self, position):
        position_str = DawsonsChessGameVariant.get_position_str(position)

        response = {
            "position": position,
            "positionValue": DawsonsChessGameVariant.position_value(position_str),
            "remoteness": 1,
        }
        return response

    def position_data(self, position):
        position_str = DawsonsChessGameVariant.get_position_str(position)
        player = position[2]
        moves = DawsonsChessGameVariant.get_moves(position_str, player)

        response = self.stat(position)
        response['moves'] = [{
            "move": move,
            "moveName": moveName,
            **self.stat(next_position)
        } for move, (next_position, moveName) in moves.items()]
        return response

    def getUWAPIPos(board_str, player):
        return f"R_{player}_0_0_{board_str}"

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
            if position[i] == 'b' and (i == 0 or position[i - 1] == 'b') \
                and (i == (len(position) - 1) or position[i + 1] == 'b'):
                curr_pile += 1
            elif position[i] != 'b' and curr_pile != 0:
                pile_lengths.append(curr_pile)
                curr_pile = 0
        if curr_pile != 0:
            pile_lengths.append(curr_pile)
        return pile_lengths

    def get_moves(position_str, player):
        next_player = 'B' if player == 'A' else 'A'
        next_position = list(position_str)
        moves = {}
        for i in range(len(position_str)):
            if position_str[i] == 'b' and (i == 0 or position_str[i - 1] == 'b') \
                and (i == (len(position_str) - 1) or position_str[i + 1] == 'b'):
                next_position[i] = 'x'
                moves[f"A_t_{i}_x"] = (
                    DawsonsChessGameVariant.getUWAPIPos(''.join(next_position), next_player),
                    f"{i + 1}"
                )
                next_position[i] = 'b'
        return moves

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
