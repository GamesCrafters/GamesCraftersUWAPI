import copy

import numpy as np


class ChessBoard:
    def __init__(self) -> None:
        self.board = np.empty((9, 10))
        self.board.fill(0)
        self.chessPieces = []


class ChessPiece:
    def __init__(self, color, type, row, col) -> None:
        self.color = color
        self.type = type
        self.row = row
        self.col = col


def init_chess_board() -> ChessBoard:
    chessBoard = ChessBoard()
    colors = [-1] * 16 + [1] * 16
    types = [0, 1, 2, 3, 4, 3, 2, 1, 0, 5, 5, 6, 6, 6, 6, 6,
             8, 9, 10, 11, 12, 11, 10, 9, 8, 13, 13, 14, 14, 14, 14, 14]
    rows = [0]*9+[2]*2+[3]*5+[9]*9+[7]*2+[6]*5
    cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 1, 7, 0, 2, 4, 6, 8] * 2
    for i in range(16*2):
        chessBoard.chessPieces.append(ChessPiece(
            color=colors[i], type=types[i], row=rows[i], col=cols[i]))
        chessBoard.board[cols[i]][rows[i]] = 1
    return chessBoard

    # 8 9 10 11 12 11 10 9 8
    #    13          13
    # 14  14   14   14  14

    # 6   6   6   6   6
    #     5       5
    # 0 1 2 3 4 3 2 1 0


def legal_loc(col, row) -> bool:
    return row >= 0 and row < 10 and col >= 0 and col < 9


def legal_move(chessBoard, chessPiece, col, row) -> bool:
    if not legal_loc(col, row):
        return False
    if chessBoard.board[col, row] != 0:
        for cp in chessBoard.chessPieces:
            if cp.row == row and cp.col == col and cp.color == chessPiece.color:
                return False
    if chessPiece.type == 6 or chessPiece.type == 14:
        return ((chessPiece.col == col) and (chessPiece.type == 6 or chessPiece.row == row + 1) and (chessPiece.type == 14 or chessPiece.row == row - 1))
    if chessPiece.type == 7 or chessPiece.type == 15:
        if chessPiece.row == row and abs(chessPiece.col - col) == 1:
            return True
        if abs(chessPiece.col - col) != 0 or abs(chessPiece.row - row) != 1:
            return False
        return (chessPiece.type == 7 and chessPiece.row == row - 1) or (chessPiece.type == 15 and chessPiece.row == row + 1)
    if chessPiece.type == 0 or chessPiece.type == 8:
        if chessPiece.row != row and chessPiece.col != col:
            return False
        cnt = 0
        if chessPiece.row == row:
            for i in range(min(chessPiece.col, col), max(chessPiece.col, col)+1):
                if chessBoard.board[i][row]:
                    cnt += 1
        else:
            for i in range(min(chessPiece.row, row), max(chessPiece.row, row)+1):
                if chessBoard.board[col][i]:
                    cnt += 1
        return (cnt == 2 and chessBoard.board[col][row] != 0) or cnt == 1
    if chessPiece.type == 1 or chessPiece.type == 9:
        if abs(chessPiece.row - row) + abs(chessPiece.col - col) != 3:
            return False
        if abs(chessPiece.row - row) > abs(chessPiece.col - col):
            drow = row - chessPiece.row
            return chessBoard.board[chessPiece.col][chessPiece.row + int(drow/abs(drow))] == 0
        else:
            dcol = col - chessPiece.col
            return chessBoard.board[chessPiece.col + int(dcol/abs(dcol))][chessPiece.row] == 0
    if chessPiece.type == 2 or chessPiece.type == 10:
        if (abs(chessPiece.col - col) != 2) or (abs(chessPiece.row - row) != 2):
            return False
        dcol = col - chessPiece.col
        drow = row - chessPiece.row
        if chessBoard.board[chessPiece.col + int(dcol/abs(dcol))][chessPiece.row + int(drow/abs(drow))]:
            return False
        return (chessPiece.type == 2 and chessPiece.row <= 4) or (chessPiece.type == 10 and chessPiece.row >= 5)
    if chessPiece.type == 3 or chessPiece.type == 11:
        if col < 3 or col > 5:
            return False
        if (chessPiece.type == 3 and row > 2) or (chessPiece.type == 11 and row < 7):
            return False
        return abs(chessPiece.row - row) == 1 and abs(chessPiece.col - col) == 1
    if chessPiece.type == 4 or chessPiece.type == 12:
        if col < 3 or col > 5:
            return False
        if (chessPiece.type == 4 and row > 2) or (chessPiece.type == 12 and row < 7):
            return False
        return abs(chessPiece.row - row) + abs(chessPiece.col - col) == 1
    if chessPiece.type == 5 or chessPiece.type == 13:
        if chessPiece.row != row and chessPiece.col != col:
            return False
        cnt = 0
        if chessPiece.row == row:
            for i in range(min(chessPiece.col, col), max(chessPiece.col, col)+1):
                if chessBoard.board[i][row]:
                    cnt += 1
        else:
            for i in range(min(chessPiece.row, row), max(chessPiece.row, row)+1):
                if chessBoard.board[col][i]:
                    cnt += 1
        return (cnt == 3 and chessBoard.board[col][row] != 0) or cnt == 1

def board_legal(chessBoard,currentPlayer) -> bool:
    for piece in chessBoard.chessPieces:
        if piece.color == currentPlayer & (piece.type == 4 | piece.type == 12):
            for otherPiece in chessBoard.chessPieces:
                if piece.color == currentPlayer: continue
                if legal_move(chessBoard,otherPiece,piece.col,piece.row): 
                    return False
                if otherPiece.type == 4 | otherPiece.type == 12:
                    if piece.col == otherPiece.col: 
                        flag = 0
                        for i in chessBoard.chessPieces:
                            if i.type != 4 & i.type != 12: flag = 1
                        if flag == 0: return False
    return True

def check_legal2(chessBoard,chessPiece,col,row) -> bool:
    newBoard = copy.deepcopy(chessBoard)
    for cp in newBoard.chessPieces:
        if cp.row == row and cp.col == col:
            newBoard.chessPieces.remove(cp)
            break
    for i in range(len(newBoard.chessPieces)):
        if newBoard.chessPieces[i].col == chessPiece.col & newBoard.chessPieces[i].row == chessPiece.row:
            newBoard.chessPieces[i].row = row
            newBoard.chessPieces[i].col = col
            break
    if not board_legal(newBoard, chessPiece.color):
        return False
    return True


def do_move(chessBoard, chessPiece, col, row):
    if not legal_move(chessBoard, chessPiece, col, row):
        return chessBoard, None, False
    removedChess = None
    for cp in chessBoard.chessPieces:
        if cp.row == row and cp.col == col:
            removedChess = cp
            chessBoard.chessPieces.remove(cp)
    chessBoard.board[chessPiece.col][chessPiece.row] = 0
    chessPiece.row = row
    chessPiece.col = col
    chessBoard.board[col, row] = 1
    return chessBoard, removedChess, True


# True for end
def check_end(chessBoard):
    r = b = False
    for cp in chessBoard.chessPieces:
        if cp.type == 4:
            r = True
        if cp.type == 12:
            b = True
    return not r == b == True


def all_move(chessPiece):
    list = []
    if chessPiece.type == 0 or chessPiece.type == 5 or chessPiece.type == 8 or chessPiece.type == 13:
        for i in range(10):
            list.append((chessPiece.col, i))
        for i in range(9):
            list.append((i, chessPiece.row))
    if chessPiece.type == 2 or chessPiece.type == 10:
        list.append((chessPiece.col+2, chessPiece.row+2))
        list.append((chessPiece.col-2, chessPiece.row+2))
        list.append((chessPiece.col+2, chessPiece.row-2))
        list.append((chessPiece.col-2, chessPiece.row-2))
    if chessPiece.type == 1 or chessPiece.type == 9:
        dx = [1, 2, 2, 1, -1, -2, -2, -1]
        dy = [-2, -1, 1, 2, 2, 1, -1, -2]
        for i in range(8):
            list.append((chessPiece.col + dx[i], chessPiece.row + dy[i]))
    if chessPiece.type == 3 or chessPiece.type == 11:
        list.append((chessPiece.col+1, chessPiece.row+1))
        list.append((chessPiece.col-1, chessPiece.row+1))
        list.append((chessPiece.col+1, chessPiece.row-1))
        list.append((chessPiece.col-1, chessPiece.row-1))
    if chessPiece.type == 4 or chessPiece.type == 12 or chessPiece.type == 6 or chessPiece.type == 7 or chessPiece.type == 14 or chessPiece.type == 15:
        list.append((chessPiece.col+1, chessPiece.row))
        list.append((chessPiece.col-1, chessPiece.row))
        list.append((chessPiece.col, chessPiece.row+1))
        list.append((chessPiece.col, chessPiece.row-1))
    return list


def all_legal_move(chessBoard, color):
    newList = []
    for chessPiece in chessBoard.chessPieces:
        if chessPiece.color == color:
            list = all_move(chessPiece)
            for (col, row) in list:
                if legal_move(chessBoard, chessPiece, col, row):
                    if check_legal2(chessBoard,chessPiece,col,row):
                        newList.append((chessPiece, col, row))
    return newList


def to_string(chessBoard):
    c = np.empty((9, 10))
    c.fill(0)
    for cp in chessBoard.chessPieces:
        c[cp.col][cp.row] = cp.type
    print(c)


if __name__ == "__main__":
    chessBoard = init_chess_board()
    color = 1
    while not check_end(chessBoard):
        to_string(chessBoard)
        move = all_legal_move(chessBoard, color)
        index = np.random.randint(low=0, high=len(move))
        chessBoard, _, ok = do_move(
            chessBoard, move[index][0], move[index][1], move[index][2])
        if not ok:
            break
        color = -color
