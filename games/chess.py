"""
    Author: Anthony Ling
"""

import chess
from requests.exceptions import HTTPError
import requests

from .models import AbstractVariant, Remoteness

URL = "http://tablebase.lichess.ovh/standard"

SLASH_REPLACEMENT = '.'
SPACE_REPLACEMENT = '_'

def fenToURLFriendly(fen):
    return fen.replace(" ", SPACE_REPLACEMENT).replace("/", SLASH_REPLACEMENT)

def URLFriendlyToFen(urlFriendlyFen):
    return urlFriendlyFen.replace(SLASH_REPLACEMENT, "/").replace(SPACE_REPLACEMENT, " ")

def convertFENToUWAPIRegular2DPositionBoardString(fen):
    board, extra = fen.replace(" ", "_").split("_", 1)
    board = board.replace("/", "")
    for i in range(10):
        board = board.replace(str(i), '-' * i)
    turn_char = '1' if extra.split('_')[0] == 'w' else '2'
    return f'{turn_char}_{board}'

def makeUWAPIMoveString(autogui_position_str, move):
    src = 8 * (8 - int(move[1])) + (ord(move[0]) - ord('a'))
    dest = 8 * (8 - int(move[3])) + (ord(move[2]) - ord('a'))
    sound = 'x' if autogui_position_str.split('_')[-1][dest] == '-' else 'y'
    return "M_{}_{}_{}".format(src, dest, sound)

def makeMove(urlFriendlyFen, move): # returns a proper fen
    board = chess.Board(URLFriendlyToFen(urlFriendlyFen))
    move = chess.Move.from_uci(move)
    board.push(move)
    return board.fen()

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

def syz_stat(url_fen):
    try:
        fen = URLFriendlyToFen(url_fen)
        r = requests.get(url=URL, params={'fen': fen})
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data = r.json()
        value = positionValue(data)
        response = {
            "position": url_fen,
            "autoguiPosition": convertFENToUWAPIRegular2DPositionBoardString(fen),
            "positionValue": value,
            "remoteness": positionRemoteness(data, value),
        }
        return response


def syz_next_stats(autoguiPosition, url_fen):
    try:
        r = requests.get(url=URL, params={'fen': URLFriendlyToFen(url_fen)})
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
            next_position_fen = makeMove(url_fen, move['uci'])
            response.append({
                "move": move['san'],
                "autoguiMove": makeUWAPIMoveString(autoguiPosition, move['uci']),
                "position": fenToURLFriendly(next_position_fen),
                "autoguiPosition": convertFENToUWAPIRegular2DPositionBoardString(next_position_fen),
                "positionValue": child_value,
                "remoteness": positionRemoteness(move, child_value)
            })
        return response


class RegularChessVariant(AbstractVariant):

    def __init__(self, fen, name = "Chess Endgame"):
        self.start_fen = fen
        super(RegularChessVariant, self).__init__(name, 'v2')

    def start_position(self):
        return {
            'position': fenToURLFriendly(self.start_fen),
            'autoguiPosition': convertFENToUWAPIRegular2DPositionBoardString(self.start_fen)
        }

    def position_data(self, url_fen):
        response = syz_stat(url_fen)
        autogui_position = response['autoguiPosition']
        response['moves'] = syz_next_stats(autogui_position, url_fen)
        return response
