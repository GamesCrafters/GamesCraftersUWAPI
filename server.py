import os

from flask import Flask, escape, request
from flask_cors import CORS

from games import games, GamesmanClassicDataProvider
from games.image_autogui_data import *
from games.randomized_start import *
from games.models import EfficientGameVariant
from games.Ghost import Node, Trie

from md_api import read_from_link

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app)

# ID mapping from Uni to GC to get game instructions.
ids = {'1210': '1210', 'abalone': 'abalone', 'achi': 'achi', 'ago': 'atarigo',
       'baghchal': 'baghchal', 'chungtoi': 'chungtoi', 'dao': 'dao', 'dinododgem': 'dinododgem',
       'dnb': 'dotsandboxes', 'dragonsandswans': 'dragonsandswans', 'foxes': 'foxandgeese',
       'Lgame': 'lgame', 'mancala': 'mancala', 'ninemensmorris': 'ninemensmorris', 'topitop': 'topitop', 'ooe': 'oddoreven',
       'othello': 'othello', 'quickchess': 'quickchess', 'sim': 'sim', 'snake': 'snake', '3spot': 'threespot',
       'ttt': 'tictactoe', 'tilechess': 'tilechess', 'connect4c': 'connect4', 'dodgem': 'dodgem'}

# Helper methods


def get_link(game_id):
    if game_id in ids:
        gc_id = ids.get(game_id)
        link = "http://gamescrafters.berkeley.edu/games/" + gc_id + ".xml"
        return link
    return None


def md_instr(game_id):
    gc_link = get_link(game_id)
    if gc_link:
        return read_from_link(gc_link)
    return None


def format_response_ok(response):
    return {
        'status': 'ok',
        'response': response
    }


def format_response_err(error_message):
    return {
        'status': 'error',
        'error': error_message
    }


def get_game(game_id):
    return games.get(game_id, None)


def get_game_variant(game_id, variant_id):
    game = get_game(game_id)
    if not game:
        return None
    return game.variant(variant_id)


def wrangle_next_stats(position, next_stats):
    if not next_stats:
        return next_stats

    def next_stats_remoteness_where_position_value(position_value):
        return [next_stat['remoteness'] for next_stat in next_stats if next_stat['positionValue'] == position_value]

    def key_next_stat_by_move_value_then_delta_remoteness(next_stat):
        VALUES = ['win', 'tie', 'draw', 'lose', 'unsolved']
        move_value = next_stat['moveValue']
        delta_remotenesss = next_stat['deltaRemoteness']
        if (move_value == 'undecided'):
            return 1
        return (VALUES.index(move_value), delta_remotenesss)

    next_stats_remoteness_where_position_value_win = \
        next_stats_remoteness_where_position_value('win')
    next_stats_remoteness_where_position_value_lose = \
        next_stats_remoteness_where_position_value('lose')
    next_stats_remoteness_where_position_value_tie = \
        next_stats_remoteness_where_position_value('tie')

    best_next_stats_remoteness_where_move_value_win = \
        min(next_stats_remoteness_where_position_value_lose) if next_stats_remoteness_where_position_value_lose else 0
    best_next_stats_remoteness_where_move_value_lose = \
        max(next_stats_remoteness_where_position_value_win) if next_stats_remoteness_where_position_value_win else 0
    best_next_stats_remoteness_where_move_value_tie = \
        min(next_stats_remoteness_where_position_value_tie) if next_stats_remoteness_where_position_value_tie else 0

    def wrangle_next_stat(next_stat):
        position_value = next_stat['positionValue']
        remoteness = next_stat['remoteness']
        move_value = next_stat.get('moveValue', position_value)

        # If not using UWAPI position string, assume turn switching; otherwise, determine whether turn character changed. 
        if position[:2] != 'R_' or next_stat['position'][2] != position[2]:
            if position_value == 'win':
                move_value = 'lose'
            elif position_value == 'lose':
                move_value = 'win'
            
        next_stat['moveValue'] = move_value

        # Delta remoteness (grouped by move value)
        delta_remoteness = 0
        if move_value == 'win':
            delta_remoteness = remoteness - best_next_stats_remoteness_where_move_value_win
        elif move_value == 'lose':
            delta_remoteness = best_next_stats_remoteness_where_move_value_lose - remoteness
        elif move_value == 'tie':
            delta_remoteness = remoteness - best_next_stats_remoteness_where_move_value_tie
        
        next_stat['deltaRemoteness'] = delta_remoteness

        return next_stat

    return sorted(map(wrangle_next_stat, next_stats), key=key_next_stat_by_move_value_then_delta_remoteness)


# Routes


@app.route("/games/")
def handle_games():
    response = [
        {
            'gameId': game_id,
            'name': game.name,
            'status': game.status,
            'gui_status': game.gui_status
        }
        for (game_id, game) in games.items() if game.status == 'available'
    ]
    response.sort(key=lambda g: g['name'])
    return format_response_ok(response)


@app.route("/games/<game_id>/")
def handle_game(game_id):
    game = get_game(game_id)
    if not game:
        return format_response_err('Game not found')
    
    custom_variant = 'true' if game.custom_variant else None
    return format_response_ok({
        'gameId': game_id,
        'name': game.name,
        'instructions': md_instr(game_id),
        'variants': [
            {
                'variantId': variant_id,
                'description': variant.desc,
                'status': variant.status,
                'startPosition': variant.start_position(),
                'imageAutoGUIData': get_image_autogui_data(game_id, variant_id),
                'gui_status': variant.gui_status
            }
            for (variant_id, variant) in game.variants.items() if variant.status != 'unavailable'
        ],
        'custom': custom_variant
    })


@app.route('/games/<game_id>/variants/<variant_id>/')
def handle_variant(game_id, variant_id):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    return format_response_ok({
        'gameId': game_id,
        'variant': [
            {
                'variantId': variant_id,
                'description': variant.desc,
                'status': variant.status,
                'startPosition': variant.start_position(),
                'imageAutoGUIData': get_image_autogui_data(game_id, variant_id)
            }
        ]
    })


@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>/')
def handle_position(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    if (hasattr(variant, 'data_provider') and variant.data_provider == GamesmanClassicDataProvider):
        # Get all information from one API call instead of 2
        result = variant.next_stats(position)
        if result is None:
            return format_response_err('Passed in Invalid Game State')
        result['moves'] = wrangle_next_stats(position, result['moves'])
    elif isinstance(variant, EfficientGameVariant):
        result = variant.full_stats(position)
        if result is None:
            return format_response_err('Passed in Invalid Game State')
        result['moves'] = wrangle_next_stats(position, result['moves'])
    else:
        result = variant.stat(position)
        if result is None:
            return format_response_err('Passed in Invalid Game State')
        result['moves'] = wrangle_next_stats(position, variant.next_stats(position))
    if result['remoteness'] == 0:
        result['moves'] = []
    return format_response_ok(result)


@app.route('/games/<game_id>/<variant_id>/randpos/')
def game_randpos(game_id, variant_id):
    random_start = get_random_start(game_id, variant_id)
    if random_start is None:
        variant = get_game_variant(game_id, variant_id)
        if not variant:
            return format_response_err('Game/Variant not found')
        random_start = variant.start_position()
    response = {
        "position": random_start
    }
    return format_response_ok(response)


if __name__ == '__main__':
    port = os.environ.get('API_PORT', None)
    app.run(port=port)
