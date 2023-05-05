from .models import AbstractGameVariant
from math import gcd

class EuclidsGame(AbstractGameVariant):

    p2Result = [('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 1), ('win', 3), ('win', 1), ('win', 53), ('win', 1), ('win', 5), ('win', 1), ('win', 3), ('win', 1), ('win', 59), ('win', 1), ('win', 61), ('win', 1), ('win', 3), ('win', 1), ('win', 5), ('win', 1), ('win', 67), ('win', 1), ('win', 3), ('win', 1), ('win', 71), ('win', 1), ('win', 73), ('win', 1), ('win', 3), ('win', 1), ('win', 7), ('win', 1), ('win', 79), ('win', 1), ('win', 9), ('win', 1), ('win', 83), ('win', 1), ('win', 17), ('win', 1), ('win', 29), ('win', 1), ('win', 89), ('win', 1), ('win', 13), ('win', 1), ('win', 31), ('win', 1), ('win', 19), ('win', 1), ('win', 97), ('win', 1), ('win', 99), ('win', 1)]

    def __init__(self):
        name = "Regular"
        desc = "Regular"
        status = "stable"
        super(EuclidsGame, self).__init__(name, desc, status=status, gui_status="v2")

    def start_position(self):
        """
            Return a UWAPI position string corresponding 
            to the initial position.
        """
        # pass
        return "R_A_4_4_" + '-' * 106

    def stat(self, position):
        """
            Get the value and remoteness of the input position.
        """
        selected, _, first_number, second_number = self.parse_position_string(position)
        if (first_number == 0):
            response = {
                "position": position,
                "positionValue": "lose",
                "remoteness": 100,
            }
        elif (second_number == 0):
            v, r = EuclidsGame.p2Result[first_number - 1]
            response = {
                "position": position,
                "positionValue": v,
                "remoteness": r,
            }
        else:
            total_moves = max(first_number, second_number)//gcd(first_number, second_number)
            moves_so_far = selected.count("X")
            
            #total number of selections made is the gcd(m,n). M and N are the first two numbers selected.
            remoteness = total_moves - moves_so_far
            position_value = "win" if remoteness % 2 else "lose"
            response = {
                "position": position,
                "positionValue": position_value,
                "remoteness": remoteness,
            }
        return response
    
    def parse_position_string(self, position):
        """
            Returns: 
                - Selected Numbers
                - Whose Turn
                - Second Number Selected (0 if not selected yet)
                - First Number Selected (0 if not selected yet)
        """

        first_number = int(position[-3:].replace('-', '0'))
        second_number = int(position[-6:-3].replace('-', '0'))
        return position[8:108], position[2], first_number, second_number

    def next_stats(self, position):
        """
            Assemble `moves`, a dictionary mapping each legal move 
            from the input position to the child position
            it leads to. 
        """
        selected, turn, first_number, second_number = self.parse_position_string(position)
        next_turn = 'B' if turn == 'A' else 'A'
        moves = {}
        response = []
        available = []

        if first_number == 0:
            available = list(range(1, 101))
        elif second_number == 0:
            available = [i for i in range(1, 101) if i != first_number]
        else:
            selected_numbers = [i + 1 for i in range(100) if selected[i] == 'X']
            differences = [
                abs(selected_numbers[i] - selected_numbers[j])
                for i in range(len(selected_numbers))
                for j in range(i + 1, len(selected_numbers))
                if i != j]
            available = [x for x in differences if x not in selected_numbers]

        for difference in available:
            trailing = position[-6:]
            if (first_number == 0):
                trailing = '---' + (str(difference).zfill(3))
            elif (second_number == 0):
                trailing = (str(difference).zfill(3)) + position[-3:]
            moves[difference] = "R_{}_4_4_{}{}".format(
                next_turn, 
                selected[:difference-1] + 'X' + selected[difference:],
                trailing
            )

        for move, position in moves.items():
            next_res = {
                "move": 'A_-_' + str(move - 1),
                "moveName": str(move),
                **self.stat(position)
            }
            response.append(next_res)
        return response