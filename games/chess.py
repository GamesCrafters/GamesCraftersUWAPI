import json

import chess
from requests.exceptions import HTTPError
import requests

from .models import AbstractGameVariant


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


def makeUWAPIMoveString(move):
    return "M_{}_{}".format(8 * (8 - int(move[1])) + (ord(move[0]) - ord('a')),
                            8 * (8 - int(move[3])) + (ord(move[2]) - ord('a')))


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
    return 'draw' if data['dtm'] is None or data['dtm'] == 0 else 'lose' if data['dtm'] < 0 else 'win'


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
        response = {
            "position": position,
            "positionValue": positionValue(data),
            "remoteness": 0 if data['dtm'] is None else abs(data['dtm']),
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
        response = [{
            "move": makeUWAPIMoveString(move['uci']),
            "moveName": move['san'],
            "position": makeMove(position, move['uci']),
            "positionValue": positionValue(move),
            "remoteness": 0 if move['dtm'] is None else abs(move['dtm'])
        } for move in data['moves']]
        return response


class RegularChessVariant(AbstractGameVariant):

    def __init__(self):
        name = "Regular"
        desc = "Regular 7-man Chess"
        status = 'stable'
        super(RegularChessVariant, self).__init__(name, desc, status=status)

    def start_position(self):
        return "R_A_8_8_" + "--------" + "------R-" + "------k-" + "p--pB---" + "--------" + "--------" + "r-------" + "------K-" + "_b_-_-_0_1"

    def stat(self, position):
        return syz_stat(position)

    def next_stats(self, position):
        return syz_next_stats(position)
