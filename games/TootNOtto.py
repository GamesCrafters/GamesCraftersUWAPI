import json

from .models import AbstractGameVariant


class TootNOtto(AbstractGameVariant):

    def __init__(self, COLS):

        self.COLS = COLS

        name = str(COLS) + "x4 Toot-N-Otto name"
        desc = str(COLS) + "x4 Toot-N-Otto desc"
        status = "stable"
        self.moves = {
            "positions": {
                "R_A_1_3_RL-": {
                  "remoteness": 1,
                  "value": "win" if variantIdNum == 4 else "lose",
                  "moves": {
                    "M_0_2": "R_A_1_3_-LR"
                  }
                },
                "R_A_1_3_-LR": {
                  "remoteness": 1,
                  "value": "win" if variantIdNum == 4 else "lose",
                  "moves": {
                    "A_L_1": "R_B_1_3_--R"
                  }
                },
                "R_B_1_3_--R": {
                  "remoteness": 0,
                  "value": "lose" if variantIdNum == 4 else "win",
                  "moves": {}
                }
            }
        }
        super(TootNOtto, self).__init__(name, desc, status=status)

    def start_position(self):
        return "R_A_1_3_RL-"

    def stat(self, position):
        try:
            stat = self.moves["positions"][position]
            position_value = stat["value"]
            remoteness = stat["remoteness"]
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
            moves = self.moves["positions"][position]["moves"]
            current_player = self.get_player(position)
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = []
            for move, position in moves.items():
                next_res = {
                    "move": move,
                    **self.stat(position)
                }
                next_player = self.get_player(position)
                if current_player == next_player:
                    next_res['moveValue'] = next_res['positionValue']
                response.append(next_res)
            return response

    def get_player(self, position_str):
        position = position_str.split('_')
        return position[1]
