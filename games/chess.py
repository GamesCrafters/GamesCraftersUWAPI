"""
    Author: Anthony Ling
"""

import chess
from requests.exceptions import HTTPError
import requests

from .models import AbstractVariant, Remoteness

URL = "http://tablebase.lichess.ovh/standard"


def convertUWAPIRegular2DPositionStringToFEN(position):
    pieces, spaces, uri = 0, 0, ''
    position = position.split("_", 5)
    
    if len(position) != 6:
        return ""

    for c in position[4]:
        if c != '-' and spaces > 0:
            uri += str(spaces)
            spaces = 0
        if pieces == 8:
            if spaces > 0:
                uri += str(spaces)
                spaces = 0
            uri += '/'
            pieces = 0
        if c == '-':
            spaces += 1
        else:
            uri += c
        pieces += 1
    if spaces > 0:
        uri += str(spaces)
    
    return uri + "_" + position[5]


def convertFENToUWAPIRegular2DPositionBoardString(fen):
    board, extra = fen.replace(" ", "_").split("_", 1)
    board = board.replace("/", "")
    for i in range(10):
        board = board.replace(str(i), '-' * i)
    return board + "_" + extra


def makeUWAPIMoveString(next_position, move):
    src = 8 * (8 - int(move[1])) + (ord(move[0]) - ord('a'))
    dest = 8 * (8 - int(move[3])) + (ord(move[2]) - ord('a'))
    return "M_{}_{}_{}".format(src, dest, next_position[8 + dest].upper())

def makeMove(position, move):
    fen = convertUWAPIRegular2DPositionStringToFEN(position)
    board = chess.Board(fen.replace("_", " "))
    move = chess.Move.from_uci(move)
    board.push(move)
    fen = board.fen()
    turn = 'B' if position[2] == 'A' else 'A'
    return "R_{}_8_8_{}".format(turn, convertFENToUWAPIRegular2DPositionBoardString(fen))


def positionValue(data):
    if data['checkmate']:
        return 'lose'
    if data['stalemate']:
        return 'tie'
    # data['category'] is one of win, unknown, maybe-win, cursed-win, draw, 
    # blessed-loss, maybe-loss, loss
    if data['category'] in ('win', 'cursed-win'):
        return 'win'
    elif data['category'] in ('loss', 'blessed-loss'):
        return 'lose'
    elif data['category'] == 'unknown':
        return 'unsolved'
    return 'draw'

def positionRemoteness(data, value):
    if value == 'win' or value == 'lose':
        return Remoteness.FINITE_UNKNOWN if data['dtm'] is None else abs(data['dtm'])
    elif value == 'draw':
        return Remoteness.INFINITY
    else:
        return 1

def syz_stat(position):
    try:
        r = requests.get(url=URL, params={
                         'fen': convertUWAPIRegular2DPositionStringToFEN(position)})
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = r.json()
        value = positionValue(data)
        response = {
            "position": position,
            "positionValue": value,
            "remoteness": positionRemoteness(data, value),
        }
        return response


def syz_next_stats(position):
    try:
        r = requests.get(url=URL, params={
                         'fen': convertUWAPIRegular2DPositionStringToFEN(position)})
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = r.json()
        response = []
        for move in data['moves']:
            child_value = positionValue(move)
            next_position = makeMove(position, move['uci'])
            response.append({
                "move": move['san'],
                "autoguiMove": makeUWAPIMoveString(next_position, move['uci']),
                "position": next_position,
                "autoguiPosition": next_position,
                "positionValue": child_value,
                "remoteness": positionRemoteness(move, child_value)
            })
        return response


class RegularChessVariant(AbstractVariant):

    def __init__(self, fen, name = "Chess Endgame"):
        self.start_fen = fen
        super(RegularChessVariant, self).__init__(name, 'v2')

    def start_position(self):
        turn = '1' if self.start_fen.split(' ')[1] == 'w' else '2'
        return self.start_fen, "{}_{}".format(turn, convertFENToUWAPIRegular2DPositionBoardString(self.start_fen))

    def position_data(self, position):
        response = syz_stat(position)
        response['moves'] = syz_next_stats(position)
        return response
