"""
    Author: Dan Garcia
"""

import pickle, os

from .models import AbstractVariant

class TootAndOtto(AbstractVariant):

    def pos_to_autogui_pos(self, board, turn, Tsx, Osx, Tso, Oso):

        """
            The internal representation of a position is as follows.
            -  The first ROW*COLS characters are the pieces on the board from
               bottom left to top right in row-major order.
            -  The next character is whose turn it is ('x'=TOOT, 'o'=OTTO).
            -  The last four characters tell us how many pieces are left. '3241' means that 
               TOOT has 3 Ts and 4 Os left to place and that OTTO has 4 Ts and 1 O left to place.
            -  Example position representation in a 6-column game: OTTTTO-OO-TO--O-T-----O-o4124
            
            The UWAPI position string representation is as follows:
            -  {uwapi_turn}_{board}{Tsx}{Osx}{Tso}{Oso}, where
            -  uwapi_turn is '1' (TOOT) or '2' (OTTO) indicating whose turn it is.
            -  board is ROW*COLS characters indicating the state of the board
            -  Tsx lists out how many Ts TOOT has remaining. IF TOOT has 3 Ts remaining in a 6-col game, then Tsx is 'TTT---'.
            -  Osx lists out how many Os TOOT has remaining. IF TOOT has 2 Ts remaining in a 6-col game, then Osx is 'OO----'.
            -  Tso lists out how many Ts OTTO has remaining. IF OTTO has 4 Ts remaining in a 6-col game, then Tso is 'TTTT--'.
            -  Oso lists out how many Os OTTO has remaining. IF OTTO has 1 Ts remaining in a 6-col game, then Oso is 'O-----'.
        """

        ### HEADER and BOARD
        uwapi_turn = {'x':'1','o':'2'}[turn]
        autogui_position = f"{uwapi_turn}_{board}"
        
        ### PIECES LEFT TO PLACE
        autogui_position += Tsx * 'T' + (self.COLS - Tsx) * '-'
        autogui_position += Osx * 'O' + (self.COLS - Osx) * '-'
        autogui_position += Oso * 'O' + (self.COLS - Oso) * '-'
        autogui_position += Tso * 'T' + (self.COLS - Tso) * '-'

        return autogui_position
    
    def parse_position(self, pos):
        # return board, turn, Tsx, Osx, Tso, Oso
        return list(pos[:self.ROWS*self.COLS]), pos[-5], int(pos[-4]), int(pos[-3]), int(pos[-2]), int(pos[-1])
    
    def stringify(board, turn, Tsx, Osx, Tso, Oso):
        return f"{board}{turn}{Tsx}{Osx}{Tso}{Oso}"
    
    """
        The way the DB is structured is as follows:
          - There are separate directories for the number of pieces placed so far, e.g. (0, 1, ..., 24) for a 6-col game.
          - You can find the position based on its bottom row. However, you must identify
            what could have been the bottom row in the parent position. There could be multiple
            such parent-bottom-rows. There are multiple files with the same current bottom row
            different possible parent rows (but not all parent rows in combination with the
            current bottom row have a file!). We simply iterate through all such files and see
            which one has the position data.
    """
    def GetValueRemoteness(self, num_placed, current_bottom_row, position):
        possible_parent_bottom_rows = [current_bottom_row] + [
            current_bottom_row[:c] + '-' + current_bottom_row[c+1:] 
            for c in range(self.COLS) if current_bottom_row[c] != '-']
        for ppbr in possible_parent_bottom_rows:
            path = f'{os.getcwd()}/{self.DIRECTORY}/{num_placed}/DB{ppbr}_{current_bottom_row}_up.p'
            if os.path.exists(path):
                tierDB = pickle.load(open(path, "rb"))
                if position in tierDB:
                    return tierDB[position]
        return 'l', -1 # If we end up here, there's a problem.

    def MoveToUWAPI(self, char, col):
        return f"A_{char}_{self.COLS * 8 + col + (self.COLS if char == 'o' else 0)}_x"

    def __init__(self, COLS):

        self.COLS   = COLS
        self.ROWS   = 4
        self.NAME = "" + str(self.ROWS) + "x" + str(self.COLS) + "Toot-N-Otto"
        self.DIRECTORY = "data/" + self.NAME + "F"

        super(TootAndOtto, self).__init__(f'{COLS}x4', gui='v3')

    def start_position(self):
        board = '-' * self.ROWS * self.COLS
        position = f'{board}x' + str(self.COLS) * 4
        return {
            'position': position,
            'autoguiPosition': self.pos_to_autogui_pos(board, 'x', self.COLS, self.COLS, self.COLS, self.COLS)
        }

    def position_data(self, position):
        size = self.ROWS * self.COLS
        board, turn, Tsx, Osx, Tso, Oso = self.parse_position(position)
        
        char_to_value = {'t':'tie','w':'win','l':'lose'}
        num_placed = self.ROWS * self.COLS - Tsx - Osx - Tso - Oso
        opp_turn = 'o' if turn == 'x' else 'x'
        parent_bottom_row = position[:self.COLS]
        parent_value_char, parent_remoteness = self.GetValueRemoteness(num_placed, parent_bottom_row, position)
        
        response = {
            "position": position,
            "autoguiPosition": self.pos_to_autogui_pos(''.join(board), turn, Tsx, Osx, Tso, Oso),
            "positionValue": char_to_value[parent_value_char],
            "remoteness": parent_remoteness
        }
        moves = []
        if parent_remoteness > 0:
            num_T = {'x':Tsx,'o':Tso}[turn]
            num_O = {'x':Osx,'o':Oso}[turn]
            available_columns = [c for c in range(self.COLS) if position[((self.ROWS-1)*self.COLS)+c] == '-']
            idxs = [position[col : size : self.COLS].index('-') * self.COLS + col for col in available_columns]
            if num_T > 0:
                if turn == 'x':
                    Tsx -= 1
                else:
                    Tso -= 1
                for col, idx in zip(available_columns, idxs):
                    board[idx] = 'T'
                    next_board = ''.join(board)
                    next_autogui_position = self.pos_to_autogui_pos(next_board, opp_turn, Tsx, Osx, Tso, Oso)
                    next_position = TootAndOtto.stringify(next_board, opp_turn, Tsx, Osx, Tso, Oso)
                    board[idx] = '-'
                    current_bottom_row = next_board[:self.COLS]
                    position_value_char, remoteness = self.GetValueRemoteness(
                        num_placed + 1, current_bottom_row, next_position
                    )
                    position_value = char_to_value[position_value_char]
                    next_res = {
                        "autoguiMove": self.MoveToUWAPI('t', col),
                        "move": 'T' + str(col + 1),
                        "position": next_position,
                        "autoguiPosition": next_autogui_position,
                        "positionValue": position_value,
                        "remoteness": remoteness
                    }
                    moves.append(next_res)
                if turn == 'x':
                    Tsx += 1
                else:
                    Tso += 1
            if num_O > 0:
                if turn == 'x':
                    Osx -= 1
                else:
                    Oso -= 1
                for col, idx in zip(available_columns, idxs):
                    board[idx] = 'O'
                    next_board = ''.join(board)
                    next_autogui_position = self.pos_to_autogui_pos(next_board, opp_turn, Tsx, Osx, Tso, Oso)
                    next_position = TootAndOtto.stringify(next_board, opp_turn, Tsx, Osx, Tso, Oso)
                    board[idx] = '-'
                    current_bottom_row = next_board[:self.COLS]
                    position_value_char, remoteness = self.GetValueRemoteness(
                        num_placed + 1, current_bottom_row, next_position
                    )
                    position_value = char_to_value[position_value_char]
                    next_res = {
                        "autoguiMove": self.MoveToUWAPI('o', col),
                        "move": 'O' + str(col + 1),
                        "position": next_position,
                        "autoguiPosition": next_autogui_position,
                        "positionValue": position_value,
                        "remoteness": remoteness
                    }
                    moves.append(next_res)
        response['moves'] = moves
        return response