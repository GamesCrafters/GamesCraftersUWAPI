from .models import AbstractGameVariant, Remoteness

def nim_custom_start(variant_id):
    try:
        piles = variant_id.split('_')
        for i in range(len(piles)):
            piles[i] = int(piles[i])
    except Exception as err:
        return None
    return NimGameVariant(piles, variant_id, variant_id)

class NimGameVariant(AbstractGameVariant):

    def __init__(self, start_piles, name = "Custom", desc = "Custom"):
        status = "stable"
        gui_status = "v3"
        self.start_piles = start_piles
        self.cumsum = [0]
        total = 0
        for pile in start_piles:
            total += pile
            self.cumsum.append(total)

        super(NimGameVariant, self).__init__(name, desc, status, gui_status)

    def start_position(self):
        return self.getUWAPIPos(self.start_piles, 'A')

    def stat(self, position):
        position_arr = self.get_position_arr(position)
        moves = self.get_moves(position_arr, position[2])
        position_value, mex = NimGameVariant.position_value(position_arr)
        mex_str = '0'
        if mex == 1:
            mex_str = '*'
        elif mex != 0:
            mex_str = f'*{mex}'

        response = {
            "position": position,
            "positionValue": position_value,
            "remoteness": Remoteness.FINITE_UNKNOWN if moves else 0,
            "mex": mex_str,
        }
        return response

    def position_data(self, position):
        position_arr = self.get_position_arr(position)
        moves = self.get_moves(position_arr, position[2])
        response = self.stat(position)
        response['moves'] = [{
            "move": move,
            "moveName": moveName,
            **self.stat(next_position)
        } for move, (next_position, moveName) in moves.items()]
        return response

    def getUWAPIPos(self, position_arr, player):
        uwapi_str = f"R_{player}_0_0_"
        for i in range(len(position_arr)):
            uwapi_str += 'x' * position_arr[i] + '-' * (self.start_piles[i] - position_arr[i])
        uwapi_str += '.' * len(self.start_piles)
        for pile_size in position_arr:
            uwapi_str += f'~{pile_size}' 
        return uwapi_str

    def position_value(position_arr):
        value = 0
        for pile in position_arr:
            value ^= int(pile)
        return "lose" if value == 0 else "win", value

    def get_position_arr(self, position_str):
        return [int(pile_size) for pile_size in position_str.split('_')[4].split('~')[1:]]
        
    def get_moves(self, position_arr, player):
        next_player = 'B' if player == 'A' else 'A'
        moves = {}
        idx = 0
        next_position_arr = position_arr[:]
        k = 1
        for i in range(len(position_arr)):
            pile_size = position_arr[i]
            for j in range(pile_size):
                next_position_arr[i] = j
                moves[f"A_t_{idx}_x"] = (
                    self.getUWAPIPos(next_position_arr, next_player),
                    f"{pile_size - j} from Pile {i + 1}"
                )
                idx += 1
            idx = self.cumsum[k]
            k += 1
            next_position_arr[i] = pile_size
        return moves
