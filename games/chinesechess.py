import copy
from .models import AbstractGameVariant

class Board:
    def __init__(self) -> None:
        self.occupied = [[False for _ in range(9)] for _ in range(10)]
        self.pieces = []


class Piece:
    def __init__(self, color, type, row, col) -> None:
        self.color: int = color
        self.type: str = type
        self.row: int = row
        self.col: int = col


def init_chess_board() -> Board:
    '''
    Returns the default starting position of a Chinese Chess game.
    '''
    board = Board()
    colors = [-1] * 16 + [1] * 16
    types = ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r', 'c', 'c', 'p', 'p', 'p', 'p', 'p',
             'R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R', 'C', 'C', 'P', 'P', 'P', 'P', 'P']
    rows = [0]*9+[2]*2+[3]*5+[9]*9+[7]*2+[6]*5
    cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 1, 7, 0, 2, 4, 6, 8] * 2
    for i in range(16*2):
        board.pieces.append(Piece(colors[i], types[i], rows[i], cols[i]))
        board.occupied[rows[i]][cols[i]] = True
    return board


def legal_loc(row, col) -> bool:
    return row >= 0 and row < 10 and col >= 0 and col < 9


def is_valid_move(board: Board, piece: Piece, row, col) -> bool:
    '''
    Returns True if the given move can be carried out. Returns 
    False otherwise. Does not consider the flying general rule
    and whether the current player's king is mated after the
    move.
    '''
    if not legal_loc(row, col):
        return False
    
    if board.occupied[row][col]:
        # Capturing a friendly piece or not moving is not allowed.
        for cp in board.pieces:
            if cp.row == row and cp.col == col and cp.color == piece.color:
                return False
    
    if piece.type == 'P' or piece.type == 'p':
        # Pawn cannot move horizontally before crossing the river.
        if (piece.col != col): return False
        # Red pawns must move towards the black side.
        if (piece.type == 'P'): return piece.row == row + 1
        # Black pawns must move towards the red side.
        return piece.row == row - 1

    elif piece.type == 'Q' or piece.type == 'q':
        # Horizontal moves are allowed if distance equals 1.
        if piece.row == row: return abs(piece.col - col) == 1
        # Vertical moves must be of distance 1.
        if abs(piece.row - row) != 1: return False
        # Diagonal moves are not allowed.
        if piece.col != col: return False
        if (piece.type == 'Q'): return piece.row == row + 1
        return piece.row == row - 1
    
    elif piece.type == 'R' or piece.type == 'r':
        # No diagonal moves are allowed.
        if piece.row != row and piece.col != col:
            return False
        cnt = 0
        # Horizontal.
        if piece.row == row:
            for j in range(min(piece.col, col), max(piece.col, col)+1):
                cnt += board.occupied[row][j]
        # Vertical.
        else:
            for i in range(min(piece.row, row), max(piece.row, row)+1):
                cnt += board.occupied[i][col]
        # Capture with 2 pieces encountered, or no capture with 1 piece encountered.
        return (cnt == 2 and board.occupied[row][col] != 0) or cnt == 1
    
    elif piece.type == 'N' or piece.type == 'n':
        delta = (row - piece.row, col - piece.col)
        vertical = ((-2, -1), (-2, 1), (2, -1), (2, 1))
        horizontal = ((-1, -2), (-1, 2), (1, -2), (1, 2))
        # The knight must not be blocked in the given direction.
        if delta in vertical:
            return not board.occupied[piece.row + delta[0]//2][piece.col]
        elif delta in horizontal:
            return not board.occupied[piece.row][piece.col + delta[1]//2]
        else:
            return False
    
    elif piece.type == 'B' or piece.type == 'b':
        delta = (row - piece.row, col - piece.col)
        if delta not in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
            return False
        # The bishop must not be blocked in the given direction.
        if board.occupied[piece.row + delta[0]//2][piece.col + delta[1]//2]:
            return False
        # A red bishop must not reach cross the river and reach black's half board.
        if piece.type == 'B': return piece.row >= 5
        # Similar for a black bishop.
        return piece.row <= 4
    
    elif piece.type == 'A' or piece.type == 'a':
        # Advisors must stay in their corresponding palace.
        if col < 3 or col > 5:
            return False
        if piece.type == 'A' and row < 7:
            return False
        if piece.type == 'a' and row > 2:
            return False
        return abs(piece.row - row) == 1 and abs(piece.col - col) == 1
    
    elif piece.type == 'K' or piece.type == 'k':
        # Kings must stay in their corresponding palace.
        if col < 3 or col > 5:
            return False
        if piece.type == 'K' and row < 7:
            return False
        if piece.type == 'k' and row > 2:
            return False
        return abs(piece.row - row) + abs(piece.col - col) == 1
    
    elif piece.type == 'C' or piece.type == 'c':
        if piece.row != row and piece.col != col:
            return False
        cnt = 0
        if piece.row == row:
            for i in range(min(piece.col, col), max(piece.col, col)+1):
                cnt += board.occupied[row][i]
        else:
            for i in range(min(piece.row, row), max(piece.row, row)+1):
                cnt += board.occupied[i][col]
        # Capture: three pieces encountered; or no capture: one piece encountered.
        return (cnt == 3 and board.occupied[row][col]) or cnt == 1
    
    else:
        raise ValueError("is_legal_move: unexpected Piece type [" + piece.type + "]")


def flying_general_possible(board: Board) -> bool:
    # Find two kings.
    for piece in board.pieces:
        if piece.type == 'K':
            redKing = piece
        elif piece.type == 'k':
            blackKing = piece
    # Not possible if the two kings are in different columns.
    if redKing.col != blackKing.col:
        return False
    # Not possible if there exists at least one piece in between.
    for i in range(min(redKing.row, blackKing.row)+1, max(redKing.row, blackKing.row)):
        if board.occupied[i][piece.col]:
            return False
    return True


def is_legal_board(board: Board, currentPlayer) -> bool:
    '''
    Returns False if current player can directly capture the opponent's king
    or if flying general is possible. Returns True otherwise.
    '''
    # Illegal if flying general is possible.
    if flying_general_possible(board):
        return False
    # Find opponent player's king.
    for piece in board.pieces:
        if piece.color != currentPlayer and (piece.type == 'K' or piece.type == 'k'):
            oppKing = piece
            break
    for piece in board.pieces:
        if piece.color != currentPlayer:
            continue
        # Illegal if can capture opponent's king directly.
        if is_valid_move(board, piece, oppKing.row, oppKing.col):
            return False
    return True


def is_legal_move(board: Board, piece: Piece, row, col) -> bool:
    '''
    Returns True if the given move is legal according to the rule.
    Returns False otherwise.
    '''
    # Move is illegal if it cannot be carried out.
    if not is_valid_move(board, piece, row, col):
        return False
    
    # Create a new board corresponding to the position after
    # making the given move.
    newBoard = copy.deepcopy(board)
    for p in newBoard.pieces:
        if p.row == row and p.col == col:
            newBoard.pieces.remove(p)
            break
    for i in range(len(newBoard.pieces)):
        if newBoard.pieces[i].col == piece.col and newBoard.pieces[i].row == piece.row:
            newBoard.pieces[i].row = row
            newBoard.pieces[i].col = col
            break
    return is_legal_board(newBoard, -piece.color)


def do_move(board: Board, piece: Piece, row: int, col: int):
    '''
    Returns the child position board, and True if the given
    move is legal according to the rule.
    Returns the original board, False otherwise.
    '''
    if not is_legal_move(board, piece, row, col):
        return board, False
    # Remove the piece at destination.
    for p in board.pieces:
        if p.row == row and p.col == col:
            board.pieces.remove(p)
            break
    board.occupied[piece.row][piece.col] = False
    # Move the given piece over.
    piece.row = row
    piece.col = col
    board.occupied[row][col] = True
    return board, True


def is_primitive(board: Board, turn):
    '''
    Returns True if the position represented by board is primitive.
    Returns False otherwise.
    '''
    return len(generate_moves(board, turn)) == 0


def all_moves(piece: Piece):
    '''
    Returns a list of all possible moves of the given piece.
    Does not take into account whether the moves are blocked
    or rendered illegal by the rule. It is the user's
    responsibility to check for their validity.
    '''
    list = []
    if piece.type == 'R' or piece.type == 'r' or piece.type == 'C' or piece.type == 'c':
        for i in range(10):
            list.append((i, piece.col))
        for j in range(9):
            list.append((piece.row, j))
    if piece.type == 'B' or piece.type == 'b':
        list.append((piece.row+2, piece.col+2))
        list.append((piece.row+2, piece.col-2))
        list.append((piece.row-2, piece.col+2))
        list.append((piece.row-2, piece.col-2))
    elif piece.type == 'N' or piece.type == 'n':
        dx = [1, 2, 2, 1, -1, -2, -2, -1]
        dy = [-2, -1, 1, 2, 2, 1, -1, -2]
        for i in range(8):
            list.append((piece.row + dy[i], piece.col + dx[i]))
    elif piece.type == 'A' or piece.type == 'a':
        list.append((piece.row+1, piece.col+1))
        list.append((piece.row+1, piece.col-1))
        list.append((piece.row-1, piece.col+1))
        list.append((piece.row-1, piece.col-1))
    elif piece.type == 'K' or piece.type == 'k' or \
            piece.type == 'P' or piece.type == 'p' or \
            piece.type == 'Q' or piece.type == 'q':
        list.append((piece.row, piece.col+1))
        list.append((piece.row, piece.col-1))
        list.append((piece.row+1, piece.col))
        list.append((piece.row-1, piece.col))
    return list


def generate_moves(board: Board, color):
    '''
    Returns a list of all possible moves. Each move is represented
    as a length-3 tuple of the format
    ({piece_to_move}, {dest_row}, {dest_col}).
    '''
    newList = []
    for piece in board.pieces:
        if piece.color == color:
            list = all_moves(piece)
            for (row, col) in list:
                if is_legal_move(board, piece, row, col):
                    newList.append((piece, row, col))
    return newList


def strcat(slist: list) -> str:
    new = ""
    for s in slist:
        new += s
    return new


def print_board(board: Board) -> None:    
    graph = [
        " - - - - - - - - ",
        "| | | |\|/| | | |",
        " - - - - - - - - ",
        "| | | |/|\| | | |",
        " - - - - - - - - ",
        "| | | | | | | | |",
        " - - - - - - - - ",
        "| | | | | | | | |",
        " - - - - - - - - ",
        "|     RIVER     |",
        " - - - - - - - - ",
        "| | | | | | | | |",
        " - - - - - - - - ",
        "| | | | | | | | |",
        " - - - - - - - - ",
        "| | | |\|/| | | |",
        " - - - - - - - - ",
        "| | | |/|\| | | |",
        " - - - - - - - - "
    ]
    for i in range(len(graph)):
        graph[i] = [c for c in graph[i]]
    for piece in board.pieces:
        graph[piece.row<<1][piece.col<<1] = str(piece.type)

    print("\n  0 1 2 3 4 5 6 7 8")
    for i in range(len(graph)):
        if (i & 1):
            print(" ", strcat(graph[i]))
        else:
            print(str(i>>1), strcat(graph[i]), str(i>>1))
    print("  0 1 2 3 4 5 6 7 8\n")


def boardToUWAPI(board: Board, turn: int) -> str:
    slots = ['-' for _ in range(90)]
    for piece in board.pieces:
        slots[piece.row * 9 + piece.col] = piece.type
    if turn == 1:
        turnChar = 'A'
    else:
        turnChar = 'B'
    return "R_" + turnChar + "_10_9_" + strcat(slots)


def UWAPIToBoard(position: str):
    position = position.split("_", 5)
    if position[1] == 'A': turn = 1
    else: turn = -1
    board = Board()
    for i in range(90):
        if position[4][i] != '-':
            row = i//9
            col = i%9
            board.occupied[row][col] = True
            if position[4][i].isupper():
                color = 1
            else:
                color = -1
            board.pieces.append(Piece(color, position[4][i], row, col))
    return board, turn

def moveToUWAPI(piece: Piece, row: int, col: int) -> str:
    srcIdx = piece.row * 9 + piece.col
    destIdx = row * 9 + col
    return "M_{}_{}".format(srcIdx, destIdx)


class RegularChineseChessVariant(AbstractGameVariant):
    def __init__(self):
        name = "Regular"
        desc = "Regular Chinese Chess with default initial position."
        status = 'stable'
        gui_status = 'v2'
        super(RegularChineseChessVariant, self).__init__(
            name, desc, status=status, gui_status=gui_status
        )

    def start_position(self):
        return boardToUWAPI(init_chess_board(), 1)

    def stat(self, position):
        return {
            "position": position,
            "positionValue": "draw", # TODO: connect EGTB here.
            "remoteness": 255
        }

    def next_stats(self, position):
        board, turn = UWAPIToBoard(position)
        moves = generate_moves(board, turn)
        return [{
            "move": moveToUWAPI(*move), # TODO: come up with good move names.
            "position": boardToUWAPI(do_move(copy.deepcopy(board), move[0], move[1], move[2])[0]),
            "positionValue": "draw", # TODO: connect EGTB here.
            "remoteness": 255
        } for move in moves]


if __name__ == "__main__":
    board = init_chess_board()
    color = 1
    while not is_primitive(board, color):
        print_board(board)
        print(boardToUWAPI(board, color))
        move = generate_moves(board, color)
        for i in range(len(move)):
            print(str(i) + ": from [", move[i][0].row, move[i][0].col, "] to [", move[i][1], move[i][2], "]")
        index = int(input())
        board, ok = do_move(
            board, move[index][0], move[index][1], move[index][2])
        if not ok:
            break
        color = -color
