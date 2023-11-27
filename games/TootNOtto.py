import pickle, os

from .models import AbstractGameVariant

class TootNOtto(AbstractGameVariant):

    def pos_to_UWAPI(self, board, turn, Tsx, Osx, Tso, Oso):

        """
            The internal representation of a position is as follows.
            -  The first ROW*COLS characters are the pieces on the board from
               bottom left to top right in row-major order.
            -  The next character is whose turn it is ('x'=TOOT, 'o'=OTTO).
            -  The last four characters tell us how many pieces are left. '3241' means that 
               TOOT has 3 Ts and 4 Os left to place and that OTTO has 4 Ts and 1 O left to place.
            -  Example position representation in a 6-column game: OTTTTO-OO-TO--O-T-----O-o4124
            
            The UWAPI position string representation is as follows:
            -  R_{uwapi_turn}_0_0_{board}{Tsx}{Osx}{Tso}{Oso}_{internalrep}, where
            -  uwapi_turn is 'A' (TOOT) or 'B' (OTTO) indicating whose turn it is.
            -  board is ROW*COLS characters indicating the state of the board
            -  Tsx lists out how many Ts TOOT has remaining. IF TOOT has 3 Ts remaining in a 6-col game, then Tsx is 'TTT---'.
            -  Osx lists out how many Os TOOT has remaining. IF TOOT has 2 Ts remaining in a 6-col game, then Osx is 'OO----'.
            -  Tso lists out how many Ts OTTO has remaining. IF OTTO has 4 Ts remaining in a 6-col game, then Tso is 'TTTT--'.
            -  Oso lists out how many Os OTTO has remaining. IF OTTO has 1 Ts remaining in a 6-col game, then Oso is 'O-----'.
            -  internalrep is just the internal representation of the position appended at the end

        """

        ### HEADER and BOARD
        uwapi_turn = {'x':'A','o':'B'}[turn]
        s = f"R_{uwapi_turn}_0_0_{board}"
        
        ### PIECES LEFT TO PLACE
        s += Tsx * 'T' + (self.COLS - Tsx) * '-'
        s += Osx * 'O' + (self.COLS - Osx) * '-'
        s += Oso * 'O' + (self.COLS - Oso) * '-'
        s += Tso * 'T' + (self.COLS - Tso) * '-'
        
        ### Add internal representation to end of uwapi position string
        s += f'_{board}{turn}{Tsx}{Osx}{Tso}{Oso}'

        return s

    def UWAPI_to_pos(self, UWAPI_position):
        pos = UWAPI_position.split("_")[-1]
        return pos, list(pos[:self.ROWS*self.COLS]), pos[-5], int(pos[-4]), int(pos[-3]), int(pos[-2]), int(pos[-1])
    
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
 
        name   = "" + str(self.ROWS) + "x" + str(self.COLS) + " Toot-N-Otto"
        desc   = str(COLS) + "x4"
        status = "stable"
        gui_status = 'v2'

        super(TootNOtto, self).__init__(name, desc, status=status, gui_status=gui_status)

    def start_position(self):
        return self.pos_to_UWAPI("-" * self.ROWS * self.COLS, 'x', self.COLS, self.COLS, self.COLS, self.COLS)

    def position_data(self, UWAPI_position):
        size = self.ROWS * self.COLS
        position, board, turn, Tsx, Osx, Tso, Oso = self.UWAPI_to_pos(UWAPI_position)
        
        char_to_value = {'t':'tie','w':'win','l':'lose'}
        num_placed = self.ROWS * self.COLS - Tsx - Osx - Tso - Oso
        opp_turn = 'o' if turn == 'x' else 'x'
        parent_bottom_row = position[:self.COLS]
        parent_value_char, parent_remoteness = self.GetValueRemoteness(num_placed, parent_bottom_row, position)
        
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
                    next_UWAPI_position = self.pos_to_UWAPI(next_board, opp_turn, Tsx, Osx, Tso, Oso)
                    board[idx] = '-'
                    current_bottom_row = next_board[:self.COLS]
                    position_value_char, remoteness = self.GetValueRemoteness(
                        num_placed + 1, current_bottom_row, next_UWAPI_position.split('_')[-1]
                    )
                    position_value = char_to_value[position_value_char]
                    next_res = {
                        "move": self.MoveToUWAPI('t', col),
                        "moveName": 'T' + str(col),
                        "position": next_UWAPI_position,
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
                    next_UWAPI_position = self.pos_to_UWAPI(next_board, opp_turn, Tsx, Osx, Tso, Oso)
                    board[idx] = '-'
                    current_bottom_row = next_board[:self.COLS]
                    position_value_char, remoteness = self.GetValueRemoteness(
                        num_placed + 1, current_bottom_row, next_UWAPI_position.split('_')[-1]
                    )
                    position_value = char_to_value[position_value_char]
                    next_res = {
                        "move": self.MoveToUWAPI('o', col),
                        "moveName": 'O' + str(col),
                        "position": next_UWAPI_position,
                        "positionValue": position_value,
                        "remoteness": remoteness
                    }
                    moves.append(next_res)
        response = {
            "position": UWAPI_position,
            "positionValue": char_to_value[parent_value_char],
            "remoteness": parent_remoteness,
            "moves": moves
        }
        return response