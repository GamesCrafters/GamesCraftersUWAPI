from .models import AbstractGameVariant

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
        return "R_A_0_0_" + 'x' * self.cumsum[-1]

    def stat(self, position):
        position_arr = self.get_position_arr(position)

        response = {
            "position": position,
            "positionValue": NimGameVariant.position_value(position_arr),
            "remoteness": 1,
        }
        return response

    def next_stats(self, position):
        position_arr = self.get_position_arr(position)
        moves = self.get_moves(position_arr, position[2])
        response = [{
            "move": move,
            "moveName": moveName,
            **self.stat(next_position)
        } for move, (next_position, moveName) in moves.items()]
        return response

    def getUWAPIPos(self, position_arr, player):
        uwapi_str = f"R_{player}_0_0_"
        for i in range(len(position_arr)):
            uwapi_str += 'x' * position_arr[i] + '-' * (self.start_piles[i] - position_arr[i])
        return uwapi_str

    def get_board_str(position_str):
        return position_str.split('_')[4]

    def position_value(position_arr):
        value = 0
        for pile in position_arr:
            value ^= int(pile)
        return "lose" if value == 0 else "win"

    def get_position_arr(self, position_str):
        board_str = NimGameVariant.get_board_str(position_str)
        position_arr = []
        i, j = 0, 1
        while i < len(board_str) + 1:
            if i == self.cumsum[j] or board_str[i] == '-':
                position_arr.append(i - self.cumsum[j - 1])
                i = self.cumsum[j]
                j += 1
                if j == len(self.cumsum):
                    break
            else:
                i += 1
        return position_arr

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
                    f"{idx + 1}"
                )
                idx += 1
            idx = self.cumsum[k]
            k += 1
            next_position_arr[i] = pile_size
        return moves
