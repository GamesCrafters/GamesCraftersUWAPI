import json
from .models import AbstractVariant


class JSONVariant(AbstractVariant):

    def __init__(self, filepath, gui='v0'):
        with open(filepath) as json_file:
            self.data = json.load(json_file)
        name = self.data["name"]
        super(JSONVariant, self).__init__(name, gui=gui)

    def start_position(self):
        return self.data["startPosition"]

    def stat(self, position):
        try:
            stat = self.data["positions"][position]
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

    def position_data(self, position):
        try:
            moves = self.data["positions"][position]["moves"]
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = self.stat(position)
            json_moves = []
            for move, position in moves.items():
                move_name = move
                move_button_data = move.split('_')
                if len(move_button_data) >= 2:
                    if move_button_data[0] == 'A': 
                        move_name = move_button_data[2]
                    else:
                        move_name = move_button_data[1] + ' ' + move_button_data[2]
                json_moves.append(
                    {
                        "move": move,
                        "moveName": move_name,
                        **self.stat(position)
                    }
                )
            
            response['moves'] = json_moves
            return response
