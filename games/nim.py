"""
    Author: Avery Liou
"""

from .models import AbstractVariant, Remoteness

def nim_custom_start(variant_id):
    try:
        piles = variant_id.split('_')
        for i in range(len(piles)):
            piles[i] = int(piles[i])
    except Exception as err:
        return None
    return NimVariant(piles, variant_id)

class NimVariant(AbstractVariant):

    def __init__(self, start_piles, name = "Custom"):
        self.start_piles = start_piles
        self.cumsum = [0]
        total = 0
        for pile in start_piles:
            total += pile
            self.cumsum.append(total)

        super(NimVariant, self).__init__(name, 'v3')

    def start_position(self):
        return {
            'position': '1_' + ','.join(str(p) for p in self.start_piles),
            'autoguiPosition': self.get_autogui_pos_str(self.start_piles, '1')
        }

    def position_data(self, position):
        pile_sizes, player = NimVariant.parse_pos_str(position)
        response = self.stat(position)
        response['moves'] = [{
            'move': move,
            'autoguiMove': autogui_move,
            **self.stat(child_position)
        } for move, autogui_move, child_position in self.get_moves(pile_sizes, player)]
        return response
    
    def stat(self, position):
        pile_sizes, player = NimVariant.parse_pos_str(position)
        moves = self.get_moves(pile_sizes, player)

        mex = 0
        for pile_size in pile_sizes:
            mex ^= pile_size

        return {
            'position': position,
            'autoguiPosition': self.get_autogui_pos_str(pile_sizes, player),
            'positionValue': 'lose' if mex == 0 else 'win',
            'remoteness': Remoteness.FINITE_UNKNOWN if moves else 0,
            'mex': '*' if mex == 1 else f'*{mex}' if mex > 0 else '0'
        }
    
    def parse_pos_str(position):
        return [int(i) for i in (position[2:].split(','))], position[0] 

    def get_autogui_pos_str(self, position_arr, player):
        autogui_pos_str = f"{'1' if player == '1' else '2'}_"
        for i in range(len(position_arr)):
            autogui_pos_str += 'x' * position_arr[i] + '-' * (self.start_piles[i] - position_arr[i])
        autogui_pos_str += '.' * len(self.start_piles)
        for pile_size in position_arr:
            autogui_pos_str += f'~{pile_size}' 
        return autogui_pos_str
        
    def get_moves(self, pile_sizes, player):
        next_player = '1' if player == '2' else '2'
        moves = []
        idx = 0
        next_pile_sizes = pile_sizes[:]
        k = 1
        for i in range(len(pile_sizes)):
            pile_size = pile_sizes[i]
            for j in range(pile_size):
                next_pile_sizes[i] = j
                moves.append([
                    f"{pile_size - j} from Pile {i + 1}",
                    f"A_t_{idx}_x",
                    f"{next_player}_{','.join([str(p) for p in next_pile_sizes])}"
                ])
                idx += 1
            idx = self.cumsum[k]
            k += 1
            next_pile_sizes[i] = pile_size
        return moves
