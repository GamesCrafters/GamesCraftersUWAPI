import json

from .models import AbstractGameVariant


class Minitoads(AbstractGameVariant):

    def __init__(self, variantId):
        name = variantId
        desc = variantId + " exploration"
        status = "stable"
        self.moves = {
            "positions": {
                "R_A_1_3_RL-": {
                  "remoteness": 1,
                  "value": "win" if variantId == "easy" else "lose",
                  "moves": {
                    "M_0_2": "R_A_1_3_-LR"
                  }
                },
                "R_A_1_3_-LR": {
                  "remoteness": 1,
                  "value": "win" if variantId == "easy" else "lose",
                  "moves": {
                    "A_L_1": "R_B_1_3_--R"
                  }
                },
                "R_B_1_3_--R": {
                  "remoteness": 0,
                  "value": "lose" if variantId == "easy" else "win",
                  "moves": {}
                }
        }
      }
        super(Minitoads, self).__init__(name, desc, status=status)

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
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = [{
                "move": move,
                **self.stat(position)
            } for move, position in moves.items()]
            return response
