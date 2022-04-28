import json

from .models import AbstractGameVariant

def kayles_custom_start(variant_id):
    try:
        board_len = int(variant_id)
    except Exception as err:
        return None
    return KaylesGameVariant(board_len)

class KaylesGameVariant(AbstractGameVariant):

    piece_char = 'l'

    def __init__(self, board_len):
        name = "custom"
        desc = "custom"
        status = "stable"
        self.board_str = ''.join(['-' for i in range(board_len)])
        super(KaylesGameVariant, self).__init__(name, desc, status)

    def start_position(self):
        return KaylesGameVariant.createUWAPIPos(1, len(self.board_str), self.board_str, "A")

    def stat(self, position):
        try:
            position_str = KaylesGameVariant.get_position_str(position)
            prev_move = KaylesGameVariant.get_prev_move(position)
            player = KaylesGameVariant.get_player(position)
            move_value = None
            if prev_move != None:
                moves = KaylesGameVariant.get_moves(position_str, player, prev_move)
                position_value = KaylesGameVariant.get_position_value_from_moves(moves)
                move_value = position_value
            else:
                position_value = KaylesGameVariant.position_value(position_str)
            remoteness = 1
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = {
                "position": position,
                "positionValue": position_value,
                "remoteness": remoteness,
                "moveValue": move_value,
            }
            return response

    def next_stats(self, position):
        try:
            position_str = KaylesGameVariant.get_position_str(position)
            prev_move = KaylesGameVariant.get_prev_move(position)
            player = KaylesGameVariant.get_player(position)
            moves = KaylesGameVariant.get_moves(position_str, player, prev_move)
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = [{
                "move": move,
                **self.stat(position)
            } for move, position in moves.items()]
            return response

    def createUWAPIPos(rows, cols, board_str, player):
        elements = ['R', player, rows, cols, board_str]
        return "_".join(map(str, elements))

    def get_player(position):
        return position.split('_')[1]

    def get_position_str(position):
        return position.split('_')[4]

    def get_prev_move(position):
        position_arr = position.split('_')
        if len(position_arr) >= 6:
            prev_move_str = position_arr[5]
            return int(prev_move_str.split('=')[1])
        else:
            return None

    def position_value(position):
        value = 0
        pile_lengths = KaylesGameVariant.get_pile_lengths(position)
        for pile_len in pile_lengths:
            pile_mex = KaylesGameVariant.get_mex(pile_len)
            value = value ^ pile_mex
        if value == 0:
            return "lose"
        return "win"

    def get_position_value_from_moves(moves):
        for _, position in moves.items():
            pos_value = KaylesGameVariant.position_value(position)
            if pos_value == "lose":
                return "win"
        return "lose"

    def get_pile_lengths(position):
        pile_lengths = []
        curr_pile = 0
        for i in range(len(position)):
            if position[i] == '-':
                curr_pile += 1
            elif position[i] != '-' and curr_pile != 0:
                pile_lengths.append(curr_pile)
                curr_pile = 0
        if curr_pile != 0:
            pile_lengths.append(curr_pile)
        return pile_lengths


    def get_moves(position, player, prev_move):
        move_arr = ["A", 'x', 0]
        moves = {}
        # If this is the second part of the multi-part move, you can only pick the piece adjacent to the first part of the multi-part move
        if prev_move != None:
            next_moves = [prev_move + 1, prev_move - 1]
            for move_idx in next_moves:
                if move_idx >= 0 and move_idx < len(position):
                    if position[move_idx] == '-':
                        move_arr[2] = str(move_idx)
                        move = '_'.join(move_arr)

                        next_position = list(position)
                        next_position[move_idx] = 'x'
                        next_position = ''.join(next_position)[:-1] # Exclude last character because it isn't used for first part of multi-part
                        next_position_uwapi = KaylesGameVariant.createUWAPIPos(1, len(next_position), next_position, KaylesGameVariant.next_player(player))

                        moves[move] = next_position_uwapi
            
            one_pin_only = ['A', '1', str(len(position) - 1)]
            one_pin_move = '_'.join(one_pin_only)
            next_position = position[:-1] # Exclude last character because it isn't used for first part of multi-part
            next_position_uwapi = KaylesGameVariant.createUWAPIPos(1, len(next_position), next_position, KaylesGameVariant.next_player(player))
            moves[one_pin_move] = next_position_uwapi
        
        else:
            for i in range(len(position)):
                if position[i] == '-':
                    move_arr[2] = str(i)
                    move = '_'.join(move_arr)

                    next_position = list(position)
                    next_position[i] = 'x'   
                    next_position.append('-')
                    next_position_len = len(next_position)
                    next_position = ''.join(next_position) + '_prevmove=' + str(i)

                    next_position_uwapi = KaylesGameVariant.createUWAPIPos(1, next_position_len, next_position, player)

                    moves[move] = next_position_uwapi

        return moves

    def next_player(player):
        return 'B' if player == 'A' else 'A'

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
