"""
    Author: Robert Shi, Haonan Huang, Yifan Zhou, Jiachun Li
"""

import copy
import os
from math import comb
from .models import AbstractVariant


class Piece:
    def __init__(self, color, type, row, col) -> None:
        self.color: int = color
        self.type: str = type
        self.row: int = row
        self.col: int = col


class Move:
    def __init__(self, srcRow, srcCol, destRow, destCol) -> None:
        self.srcRow: int = srcRow
        self.srcCol: int = srcCol
        self.destRow: int = destRow
        self.destCol: int = destCol

    def as_UWAPI(self, occupied) -> str:
        srcIdx = self.srcRow * 9 + self.srcCol
        destIdx = self.destRow * 9 + self.destCol
        soundChar = 'y' if occupied[self.destRow][self.destCol] else 'x'
        return "M_{}_{}_{}".format(srcIdx, destIdx, soundChar)


class Board:
    def __init__(self) -> None:
        self.occupied = [[False for _ in range(9)] for _ in range(10)]
        self.pieces = []

    def get_piece_at(self, row: int, col: int) -> Piece:
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        raise ValueError("unable to get piece at ({}, {})".format(row, col))

    def get_pieces(self, color: int) -> list:
        pieces = [piece for piece in self.pieces if piece.color == color]
        for i in range(len(pieces)):
            if pieces[i].type == 'K' or pieces[i].type == 'k':
                pieces[0], pieces[i] = pieces[i], pieces[0]
                break
        return pieces
    
    def get_layout(self) -> list:
        mapping = {
            'K': RED_K_IDX, 'k': BLACK_K_IDX, 
            'A': RED_A_IDX, 'a': BLACK_A_IDX, 
            'B': RED_B_IDX, 'b': BLACK_B_IDX, 
            'P': RED_P_IDX, 'p': BLACK_P_IDX, 
            'Q': RED_P_IDX, 'q': BLACK_P_IDX, 
            'N': RED_N_IDX, 'n': BLACK_N_IDX, 
            'C': RED_C_IDX, 'c': BLACK_C_IDX,
            'R': RED_R_IDX, 'r': BLACK_R_IDX
        }
        layout = [INVALID_IDX]*90
        for piece in self.pieces:
            layout[piece.row * 9 + piece.col] = mapping[piece.type]
        return layout


def get_board_default_starting() -> Board:
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


def is_legal_loc(row: int, col: int) -> bool:
    return row >= 0 and row < 10 and col >= 0 and col < 9


def is_valid_move(board: Board, piece: Piece, row: int, col: int) -> bool:
    '''
    Returns True if the given move can be carried out. Returns 
    False otherwise. Does not consider the flying general rule
    and whether the current player's king is mated after the
    move.
    '''
    if not is_legal_loc(row, col):
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
        # A red bishop must not cross the river and reach black's half board.
        if piece.type == 'B': return row >= 5
        # Similar for a black bishop.
        return row <= 4
    
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
        # Capture: three pieces encountered or no capture: one piece encountered.
        return (cnt == 3 and board.occupied[row][col]) or cnt == 1
    
    else:
        raise ValueError("unexpected Piece type [" + piece.type + "]")


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
        if board.occupied[i][redKing.col]:
            return False
    return True


def is_legal_board(board: Board, turn: int) -> bool:
    '''
    Returns False if current player can directly capture the opponent's king
    or if flying general is possible. Returns True otherwise.
    '''
    # Illegal if flying general is possible.
    if flying_general_possible(board):
        return False
    # Find opponent player's king.
    for piece in board.pieces:
        if piece.color != turn and (piece.type == 'K' or piece.type == 'k'):
            oppKing = piece
            break
    for piece in board.pieces:
        if piece.color != turn:
            continue
        # Illegal if can capture opponent's king directly.
        if is_valid_move(board, piece, oppKing.row, oppKing.col):
            return False
    return True


def is_legal_move(board: Board, piece: Piece, row: int, col: int) -> bool:
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
    newBoard.occupied[piece.row][piece.col] = False
    newBoard.occupied[row][col] = True
    return is_legal_board(newBoard, -piece.color)


def do_move(board: Board, move: Move):
    '''
    Returns the child position board after doing move.
    Raises ValueError if move is illegal.
    '''
    piece = board.get_piece_at(move.srcRow, move.srcCol)
    if not is_legal_move(board, piece, move.destRow, move.destCol):
        raise ValueError("illegal move")
    # Remove the piece at destination.
    for p in board.pieces:
        if p.row == move.destRow and p.col == move.destCol:
            board.pieces.remove(p)
            break
    board.occupied[piece.row][piece.col] = False
    # Move the given piece over.
    piece.row = move.destRow
    piece.col = move.destCol
    board.occupied[move.destRow][move.destCol] = True
    # Change pawn type if crossing the river.
    if piece.type == 'P' and piece.row <= 4:
        piece.type = 'Q'
    if piece.type == 'p' and piece.row >= 5:
        piece.type = 'q'
    return board


def is_primitive(board: Board, turn: int):
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


def generate_moves(board: Board, color: int):
    '''
    Returns a list of all possible moves.
    '''
    newList = []
    for piece in board.pieces:
        if piece.color == color:
            list = all_moves(piece)
            for (row, col) in list:
                if is_legal_move(board, piece, row, col):
                    newList.append(Move(piece.row, piece.col, row, col))
    return newList


def strcat(slist: list) -> str:
    new = ""
    for s in slist:
        new += s
    return new


def print_board(board: Board) -> None:    
    graph = [
        " - - - - - - - - ",
        "| | | |\\|/| | | |",
        " - - - - - - - - ",
        "| | | |/|\\| | | |",
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
        "| | | |\\|/| | | |",
        " - - - - - - - - ",
        "| | | |/|\\| | | |",
        " - - - - - - - - "
    ]
    for i in range(len(graph)):
        graph[i] = [c for c in graph[i]]
    for piece in board.pieces:
        graph[piece.row * 2][piece.col * 2] = str(piece.type)

    print("\n  0 1 2 3 4 5 6 7 8")
    for i in range(len(graph)):
        if (i & 1):
            print(" ", strcat(graph[i]))
        else:
            print(str(i // 2), strcat(graph[i]), str(i // 2))
    print("  0 1 2 3 4 5 6 7 8\n")


def boardToUWAPI(board: Board, turn: int) -> str:
    slots = ['-' for _ in range(90)]
    for piece in board.pieces:
        appending = piece.type
        if appending == 'Q': appending = 'P'
        if appending == 'q': appending = 'p'
        slots[piece.row * 9 + piece.col] = appending
    if turn == 1:
        turnChar = '1'
    else:
        turnChar = '2'
    return f"{turnChar}_{strcat(slots)}"


def UWAPIToBoard(position: str):
    # TODO: validate board before returning.
    turn_char, entity_string = position.split("_", 2)
    if turn_char == '1': turn = 1
    else: turn = -1
    board = Board()
    for i in range(90):
        if entity_string[i] != '-':
            row = i//9
            col = i%9
            board.occupied[row][col] = True
            if entity_string[i].isupper():
                color = 1
            else:
                color = -1
            if entity_string[i] == 'P' and 0 <= row <= 4:
                board.pieces.append(Piece(color, 'Q', row, col))
            elif entity_string[i] == 'p' and 5 <= row <= 9:
                board.pieces.append(Piece(color, 'q', row, col))
            else:
                board.pieces.append(Piece(color, entity_string[i], row, col))
    return board, turn


def EGTB_load(board: Board, turn: int):
    '''
    Returns value, remoteness of the given board position.
    Returns "unsolved", 255 if the given board position is
    not primitive and not found in the EGTB.
    '''
    if is_primitive(board, turn): # All primitive positions are losing.
        return "lose", 0

    dir_path = "../GamesmanXiangqi/data"
    if not os.path.exists(dir_path): # EGTB not found.
        return "unsolved", 1
    
    tier, h = hash_board(board, turn)
    file_path = "{}/{}/{}".format(dir_path, tier[:12], tier)
    stat_path = "{}.stat".format(file_path)
    if not os.path.exists(stat_path): # Given position not solved or corrupted in EGTB.
        return "unsolved", 1
    
    with open(file_path, "rb") as fo: # TODO: this probing code is subject to change.
        fo.seek(h * 2) # assuming 2-byte values
        value = int.from_bytes(fo.read(2), "little")

    if value == 0:
        raise ValueError("querying unreachable position")
    if value == 32768:
        return "draw", 1
    elif value < 32768:
        return "lose", value - 1
    return "win", 65535 - value


# Hashing algorithm adapted from EGTB probing code.

BOARD_RED_KING = RED_K_IDX = -2
BOARD_BLACK_KING = BLACK_K_IDX = -1
BOARD_RED_ADVISOR = RED_A_IDX = 0
BOARD_BLACK_ADVISOR = BLACK_A_IDX = 1
BOARD_RED_BISHOP = RED_B_IDX = 2
BOARD_BLACK_BISHOP = BLACK_B_IDX = 3
BOARD_RED_PAWN = RED_P_IDX = 4
BOARD_BLACK_PAWN = BLACK_P_IDX = 5
BOARD_RED_KNIGHT = RED_N_IDX = 6
BOARD_BLACK_KNIGHT = BLACK_N_IDX = 7
BOARD_RED_CANNON = RED_C_IDX = 8
BOARD_BLACK_CANNON = BLACK_C_IDX = 9
BOARD_RED_ROOK = RED_R_IDX = 10
BOARD_BLACK_ROOK = BLACK_R_IDX = 11
BOARD_EMPTY_CELL = INVALID_IDX = 12


def hash_board(board: Board, turn: int):
    '''
    Returns tier, hash.
    '''
    tier = board_to_tier(board)
    steps = board_to_steps(tier, board, turn)
    return tier, steps_to_hash(tier, steps)


def board_to_tier(board: Board) -> str:
    rems = [0]*12
    redP = []
    blackP = []
    layout = board.get_layout()
    for i in range(90):
        idx = layout[i]
        if idx < 0 or idx == INVALID_IDX:
            continue
        if idx == RED_P_IDX:
            redP.append(i // 9)
        if idx == BLACK_P_IDX:
            blackP.append(9 - i // 9)
        rems[idx] += 1
    redP.sort(reverse=True)
    blackP.sort(reverse=True)
    return strcat([str(x) for x in rems]) + "_" + strcat([str(x) for x in redP]) + "_" + strcat([str(x) for x in blackP])


def set_slots(layout: list, step: int, substep: bool = False):
    parity = step & 1
    if step == 0 or step == 1:
        slots = [66 - 63*step, 68 - 63*step, 76 - 63*step, 84 - 63*step, 86 - 63*step]
    elif step == 2 or step == 3:
        slots = [47 - 45*parity, 51 - 45*parity, 63 - 45*parity, 67 - 45*parity, 71 - 45*parity, 83 - 45*parity, 87 - 45*parity]
    elif step == 4 or step == 5 or step == 6 or step == 11 or step == 12 or step == 13:
        slots = [i + 9*(step - 4) for i in range(9)]
    elif step == 7 or step == 8 or step == 9 or step == 10:
        if (not substep):
            slots = [j + 9*(step - 4) for j in range(0, 9, 2)]
        else:
            slots = []
            for j in range(9):
                if layout[(step - 4)*9 + j] != BOARD_RED_PAWN + (step < 9):
                    slots.append(j + 9*(step - 4))
    elif step == 14:
        slots = []
        for i in range(90):
            if layout[i] >= BOARD_RED_KNIGHT:
                slots.append(i)
    else:
        raise RuntimeError()
    return [layout[i] for i in slots]


def get_pawn_begin_end(tier: str, pawnIdx: int):
    redPawnCount = int(tier[RED_P_IDX])
    blackPawnCount = int(tier[BLACK_P_IDX])
    if pawnIdx == RED_P_IDX:
        return 13, 13 + redPawnCount
    else:
        return 14 + redPawnCount, 14 + redPawnCount + blackPawnCount


def tier_get_pawns_per_row(tier: str) -> list:
    redPBegin, redPEnd = get_pawn_begin_end(tier, RED_P_IDX)
    blackPBegin, blackPEnd = get_pawn_begin_end(tier, BLACK_P_IDX)
    pawnsPerRow = [0]*20
    for i in range(redPBegin, redPEnd):
        pawnsPerRow[int(tier[i])] += 1
    for i in range(blackPBegin, blackPEnd):
        pawnsPerRow[19 - int(tier[i])] += 1
    return pawnsPerRow


def board_to_steps(tier: str, board: Board, turn: int):
    kingSlot = ((0, 0, 0),
                (1, 0, 2),
                (0, 3, 0))
    steps = [0]*16
    rems = [0]*7

    pawnsPerRow = tier_get_pawns_per_row(tier)
    layout = board.get_layout()

    # STEPS 0 & 1: KINGS AND ADVISORS.
    for step in range(2):
        pieces = board.get_pieces(1 if step == 0 else -1)
        slots = set_slots(layout, step)
        i = pieces[0].row - 7*(1 - step)
        j = pieces[0].col - 3
        if tier[RED_A_IDX + step] == '0': # No advisors.
            steps[step] = 3*i + j
        elif tier[RED_A_IDX + step] == '1':
            if ((i + j) & 1): # King does not occupy advisor slots, 20 possible configurations.
                rems[0] = 4; rems[1] = 0; rems[2] = 1
                steps[step] = 5 * kingSlot[i][j] + hash_cruncher(slots, BOARD_RED_KING, BOARD_BLACK_ADVISOR, rems, 3)
            else: # King occupies one of the advisor slots, 20 possible configurations.
                rems[0] = 3; rems[1] = 1; rems[2] = 1
                steps[step] = 20 + hash_cruncher(slots, BOARD_RED_KING, BOARD_BLACK_ADVISOR, rems, 3)
        elif tier[RED_A_IDX + step] == '2':
            if ((i + j) & 1): # King does not occupy advisor slots, 40 possible configurations.
                rems[0] = 3; rems[1] = 0; rems[2] = 2
                steps[step] = 10 * kingSlot[i][j] + hash_cruncher(slots, BOARD_RED_KING, BOARD_BLACK_ADVISOR, rems, 3)
            else: # King occupies one of the advisor slots, 30 possible configurations.
                rems[0] = 2; rems[1] = 1; rems[2] = 2
                steps[step] = 40 + hash_cruncher(slots, BOARD_RED_KING, BOARD_BLACK_ADVISOR, rems, 3)

    # STEPS 2 & 3: BISHOPS.
    for step in range(2, 4):
        slots = set_slots(layout, step)
        rems[1] = int(tier[RED_B_IDX + (step & 1)])
        rems[0] = 7 - rems[1]
        steps[step] = hash_cruncher(slots, BOARD_RED_BISHOP, BOARD_BLACK_BISHOP, rems, 2)

    # STEPS 4 - 6: RED PAWNS IN THE TOP THREE ROWS.
    for step in range(4, 7):
        slots = set_slots(layout, step)
        rems[1] = pawnsPerRow[step - 4] # number of red pawns in curr row.
        rems[0] = 9 - rems[1] # number of empty slots in curr row.
        steps[step] = hash_cruncher(slots, BOARD_RED_PAWN, BOARD_RED_PAWN, rems, 2)

    # STEPS 7 - 10: PAWNS IN ROW 3 THRU ROW 6.
    for step in range(7, 11):
        # Hash the more restricted pawns first.
        slots = set_slots(layout, step, False)
        rems[1] = pawnsPerRow[10 * (step < 9) + step - 4] # number of "more restricted" pawns in curr row.
        rems[0] = 5 - rems[1]                             # number of empty slots at the 5 locations above.
        steps[step] = hash_cruncher(slots, BOARD_RED_PAWN + (step < 9), BOARD_RED_PAWN + (step < 9), rems, 2)

        # Then hash the less restricted pawns.
        slots = set_slots(layout, step, True)
        rems[1] = pawnsPerRow[10 * (step >= 9) + step - 4] # number of "less restricted" pawns in curr row.
        rems[0] = len(slots) - rems[1]                     # number of remaining empty slots in curr row.
        steps[step] *= comb(len(slots), rems[1]) # Must calculate this first as hash_cruncher modifies rems.
        steps[step] += hash_cruncher(slots, BOARD_RED_PAWN + (step >= 9), BOARD_RED_PAWN + (step >= 9), rems, 2)

    # STEPS 11 - 13: BLACK PAWNS IN THE BOTTOM THREE ROWS.
    for step in range(11, 14):
        slots = set_slots(layout, step)
        rems[1] = pawnsPerRow[10 + step - 4] # number of black pawns in curr row.
        rems[0] = 9 - rems[1]                # number of empty slots in curr row.
        steps[step] = hash_cruncher(slots, BOARD_BLACK_PAWN, BOARD_BLACK_PAWN, rems, 2)

    # STEP 14: KNIGHTS, CANNONS, AND ROOKS.
    slots = set_slots(layout, 14)
    rems[0] = len(slots)
    for j in range(RED_N_IDX, BLACK_R_IDX + 1):
        rems[j - RED_N_IDX + 1] = int(tier[j])
        rems[0] -= int(tier[j])
    steps[14] = hash_cruncher(slots, BOARD_RED_KNIGHT, BOARD_BLACK_ROOK, rems, 7)

    # STEP 15: TURN BIT.
    steps[15] = int(turn == -1)
    return steps


def combi_count(counts: list, numPieces: int):
    sum = 0
    prod = 1
    for i in range(numPieces - 1, 0, -1):
        sum += counts[i]
        prod *= comb(sum + counts[i - 1], sum)
    return prod


def hash_cruncher(slots: list, pieceMin: int, pieceMax: int, rems: list, numPieces: int):
    pieceIdxLookup = (1,1,2,2,1,1,1,1,1,2,3,4,5,6,0)
    hash = 0
    for i in range(len(slots) - 1, 0, -1):
        piece = slots[i] if (slots[i] >= pieceMin and slots[i] <= pieceMax) else BOARD_EMPTY_CELL
        pieceIdx = pieceIdxLookup[piece + 2] # +2 to accommodate the kings.
        for j in range(pieceIdx):
            if rems[j]:
                rems[j] -= 1
                hash += combi_count(rems, numPieces)
                rems[j] += 1
        rems[pieceIdx] -= 1
    return hash


def steps_to_hash(tier: str, steps: list) -> int:
    res = 0
    stepsMax = tier_size_steps(tier)
    # Steps
    for i in range(15):
        res *= stepsMax[i]
        res += steps[i]
    # Turn bit
    res = (res << 1) | steps[15]
    return res


def tier_size_steps(tier: str):
    steps = [0]*15
    redPawnBegin, redPawnEnd = get_pawn_begin_end(tier, RED_P_IDX)
    blackPawnBegin, blackPawnEnd = get_pawn_begin_end(tier, BLACK_P_IDX)

    # King and advisors.
    for step in range(2):
        if tier[RED_A_IDX + step] == '0': # If there are no advisors, there are 9 slots for the king.
            steps[step] = 9
        elif tier[RED_A_IDX + step] == '1': # King takes one of the 5 advisor slots: 5*nCr(5-1, 1);
            # King is in one of the other 4 slots: 4*nCr(5, 1).
            steps[step] = 40
        elif tier[RED_A_IDX + step] == '2': # King takes one of the 5 advisor slots: 5*nCr(5-1, 2);
            # King is in one of the other 4 slots: 4*nCr(5, 2).
            steps[step] = 70
        else:
            raise RuntimeError()
        
    # Bishops.
    for step in range(2, 4): # There are 7 possible slots that a bishop can be in.
        steps[step] = comb(7, int(tier[RED_B_IDX + step - 2]))

    # Define row number to be 0 thru 9 where 0 is the bottom line of
    #  black side and 9 is the bottom line of red side.
    for step in range(4, 7):
        # Bottom three rows of black's half-board. No black pawns should be found.
        #  There are nCr(9, red) ways to place red pawns on the specified row.
        redPawnRow = 0
        for i in range(redPawnBegin, redPawnEnd):
            redPawnRow += (int(tier[i]) == step - 4)
        steps[step] = comb(9, redPawnRow)

    for step in range(7, 11):
        redPawnRow = blackPawnRow = 0
        for i in range(redPawnBegin, redPawnEnd):
            redPawnRow += (int(tier[i]) == step - 4)
        for i in range(blackPawnBegin, blackPawnEnd):
            blackPawnRow += (9 - int(tier[i]) == step - 4)
        if step < 9:
            # Top two rows of black's half-board. Any black pawn in these two rows
            #  can only appear in one of the 5 special columns. There are
            #  nCr(5, black)*nCr(9-black, red) ways to place all pawns on the
            #  specified row.
            steps[step] = comb(5, blackPawnRow) * comb(9 - blackPawnRow, redPawnRow)
        else:
            # Top two rows of red's half-board. Similar to the case above.
            #  nCr(5, red)*nCr(9-red, black).
            steps[step] = comb(5, redPawnRow) * comb(9 - redPawnRow, blackPawnRow)

    for step in range(11, 14):
        # Bottom three rows of red's half-board. No red pawns should be found.
        #  There are nCr(9, black) ways to place black pawns on the specified row.
        blackPawnRow = 0
        for i in range(blackPawnBegin, blackPawnEnd):
            blackPawnRow += (9 - int(tier[i]) == step - 4)
        steps[step] = comb(9, blackPawnRow)

    # Kights, cannons, and rooks can reach any slot. The number of ways
    #  to place k such pieces is nCr(90-existing_pieces, k).
    existing = 2
    for i in range(RED_N_IDX):
        existing += int(tier[i])
    steps[14] = 1
    for i in range(RED_N_IDX, BLACK_R_IDX + 1):
        steps[14] *= comb(90 - existing, int(tier[i]))
        existing += int(tier[i])
    return steps


class RegularChineseChessVariant(AbstractVariant):
    def __init__(self):
        super(RegularChineseChessVariant, self).__init__('Regular', 'v2')

    def start_position(self):
        pos = boardToUWAPI(get_board_default_starting(), 1)
        return {
            'position': pos,
            'autoguiPosition': pos
        }

    def stat(self, position: str):
        value, remoteness = EGTB_load(*UWAPIToBoard(position))
        return {
            "position": position,
            "autoguiPosition": position,
            "positionValue": value,
            "remoteness": remoteness
        }

    def position_data(self, position: str):
        board, turn = UWAPIToBoard(position)
        moves = generate_moves(board, turn)
        response = self.stat(position)
        response['moves'] = []
        for move in moves:
            newBoard = do_move(copy.deepcopy(board), move)
            value, remoteness = EGTB_load(newBoard, -turn)
            move_as_uwapi = move.as_UWAPI(board.occupied)
            response['moves'].append({
                "move": move_as_uwapi,
                "autoguiMove": move_as_uwapi, # TODO: come up with good move names.
                "position": boardToUWAPI(newBoard, -turn),
                "autoguiPosition": boardToUWAPI(newBoard, -turn),
                "positionValue": value,
                "remoteness": remoteness
            })
        return response


if __name__ == "__main__":
    print("type in UWAPI position string >", end=None)
    response = input()
    while response != "exit":
        board, turn = UWAPIToBoard(response)
        print_board(board)
        tier, h = hash_board(board, turn)
        print("tier:", tier)
        print("hash:", h)
        print("type in UWAPI position string >", end=None)
        response = input()
