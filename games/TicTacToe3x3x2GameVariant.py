from .models import AbstractGameVariant


class TicTacToe3x3x2GameVariant(AbstractGameVariant):
    """Class for 3x3x2 Tic Tac Toe
    """

    def __init__(self, name, desc, filepath, status='stable'):
        assert isinstance(name, str), 'name must be a string'
        assert isinstance(desc, str), 'desc must be a string'
        assert isinstance(filepath, str), 'filepath must be a string'

        self.name = name
        self.desc = desc
        self.status = status
        self.filepath = filepath

    def start_position(self):
        return "XO---------|---------"

    def hashTTT(position):
        index = 0
        s = position[2:11] + position[12:21]
        for i in range(len(s)):
            if s[i] == "-":
                index += (3**i) * 0
            elif s[i] == "X":
                index += (3**i) * 1
            elif s[i] == "O":
                index += (3**i) * 2
        return index

    def stat(self, position):
        try:
            index = hashTTT(position)
            f = open(self.filepath, "rb")
            f.seek(index, 1)
            value = f.read(1).decode("utf-8")
            f.close()
            value = int(value)
            position_value = ["lose", "tie", "win"][value]
            return value
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = {
                "position": position,
                "positionValue": position_value,
                "remoteness": -1,
            }
            return response

    def next_stats(self, position):
        try:
            moves = []
            for i in range(2, len(position)):
                if position[i] == "-":
                    moves.append(position[1] + position[0] + position[2:i] + position[0] + position[i+1:])
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            response = [{
                "move": move,
                **self.stat(position)
            } for move, position in moves.items()]
            return response
