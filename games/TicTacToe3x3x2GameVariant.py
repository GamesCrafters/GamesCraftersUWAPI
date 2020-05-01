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
        self.filepath = filepath

        try:
            self.file = open(self.filepath, 'rb')
        except IOError:
            self.file = None
            self.status = 'unavailable'
        else:
            self.status = status

    def __del__(self):
        if self.file:
            self.file.close()

    def start_position(self):
        return "XO---------|---------"

    @staticmethod
    def WORM(position):
        permutations = []
        p = position
        permutations.append(p)
        permutations.append(TicTacToe3x3x2GameVariant.mirror(p))
        for i in range(3):
            p = TicTacToe3x3x2GameVariant.rotateX(p)
            permutations.append(p)
            pm = TicTacToe3x3x2GameVariant.mirror(p)
            permutations.append(pm)
        return min(permutations)

    @staticmethod
    def mirror(position):
        return position[0:2] + position[4] + position[3] + position[2] + position[7] + position[6] + position[5] + position[10] + position[9] + position[8] + position[11] + position[14] + position[13] + position[12] + position[17] + position[16] + position[15] + position[20] + position[19] + position[18]

    @staticmethod
    def rotateX(position):
        return position[0:2] + position[8] + position[5] + position[2] + position[9] + position[6] + position[3] + position[10] + position[7] + position[4] + position[11] + position[18] + position[15] + position[12] + position[19] + position[16] + position[13] + position[20] + position[17] + position[14]

    @staticmethod
    def hashTTT(position):
        position = TicTacToe3x3x2GameVariant.WORM(position)
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
        if not self.file:
            print('Database file not opened')
            return

        try:
            index = self.hashTTT(position)
            self.file.seek(index, 0)
            value = self.file.read(1).decode('ascii')
            value = int(value)
            
            if value >= 3:
                return None  # Unreachable position

            position_value = ["lose", "tie", "win"][value]
            return {
                "position": position,
                "positionValue": position_value,
                "remoteness": -1,  # The database doesn't store remoteness, fallback to -1 for now
            }
        except Exception as err:
            print(f'Other error occurred: {err}')

    def next_stats(self, position):
        try:
            next_stats = []
            for i in range(2, len(position)):
                if position[i] == "-":
                    next_position = position[1] + position[0] + \
                        position[2:i] + position[0] + position[i+1:]
                    next_stats.append({
                        "move": i,
                        **self.stat(next_position)
                    })
            return next_stats
        except Exception as err:
            print(f'Other error occurred: {err}')
