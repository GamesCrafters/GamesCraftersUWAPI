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

    def WORM(position):
        permutations = []
        p = position
        permutations.append(p)
        permutations.append(mirror(p))
        for i in range(3):
            p = rotateX(p)
            permutations.append(p)
            pm = mirror(p)
            permutations.append(pm)
        return min(permutations)

    def mirror(position):
        return position[0:2] + position[4] + position[3] + position[2] + position[7] + position[6] + position[5] + position[10] + position[9] + position[8] + position[11]+ position[14] + position[13] + position[12] + position[17] + position[16] + position[15] + position[20] + position[19] + position[18]

    def rotateX(position):
        return position[0:2] + position[8] + position[5] + position[2] + position[9] + position[6] + position[3] + position[10] + position[7] + position[4] + position[11] + position[18] + position[15] + position[12] + position[19] + position[16] + position[13] + position[20] + position[17] + position[14]

    def hashTTT(position):
        position = WORM(position)
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
