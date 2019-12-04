import json

from .models import AbstractGameVariant


class JSONGameVariant(AbstractGameVariant):

    def __init__(self, filepath, status='stable'):
        with open(filepath) as json_file:
            self.data = json.load(json_file)
        name = self.data["name"]
        desc = self.data["desc"]
        super(JSONGameVariant, self).__init__(name, desc, status=status)

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

    def next_stats(self, position):
        try:
            moves = self.data["positions"][position]["moves"]
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = [{
                "move": move,
                **self.stat(position)
            } for move, position in moves.items()]
            return response
