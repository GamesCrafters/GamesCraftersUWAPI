import json

import chess
from requests.exceptions import HTTPError
import requests

from .models import AbstractGameVariant


ROW_LENGTH = 8
URL = "http://tablebase.lichess.ovh/standard"


def makeMove(fen, move):
    board = chess.Board(FENParse(fen).replace("_", " "))
    move = chess.Move.from_uci(move)
    board.push(move)
    return board.fen().replace("/", "").replace(" ", "_")


def FENParse(code):
    pieces, uri = 0, ''
    code = code.split("_", 1)
    if len(code) != 2:
        return ""
    fen1, fen2 = code[0], code[1]
    for i in fen1:
        if i == "_":
            break
        if pieces == ROW_LENGTH:
            uri += '/'
            pieces = 0
        uri += i
        if i.isdigit():
            pieces += int(i)
        else:
            pieces += 1
    return uri + "_" + fen2


def positionValue(data):
    if data['checkmate']:
        return 'lose'
    if data['stalemate']:
        return 'tie'
    return 'draw' if data['dtm'] is None or data['dtm'] == 0 else 'lose' if data['dtm'] < 0 else 'win'


def syz_stat(fen):
    try:
        r = requests.get(url=URL, params={'fen': FENParse(fen)})
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = r.json()
        response = {
            "position": fen,
            "positionValue": positionValue(data),
            "remoteness": 0 if data['dtm'] is None else abs(data['dtm']),
        }
        return response


def syz_next_stats(fen):
    try:
        r = requests.get(url=URL, params={'fen': FENParse(fen)})
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = r.json()
        response = [{
            "move": move['uci'],
            "position": makeMove(fen, move['uci']),
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
        return "4k388888P6R4K3_b_-_-_0_1"

    def stat(self, position):
        return syz_stat(position)

    def next_stats(self, position):
        return syz_next_stats(position)
