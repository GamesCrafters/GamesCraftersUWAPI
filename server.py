import os

from flask import Flask
from flask_cors import CORS

from games import games, GamesmanClassicDataProvider
from games.image_autogui_data import *
from games.randomized_start import *
from games.models import Remoteness
from games.Ghost import Node, Trie

from md_api import md_instr

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app)

# Helper methods

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
    """
    Given a position and next-move data, this function
    1) Calculates the delta-remoteness of all legal moves AND
    2) Returns the moves sorted from best-to-worst.

    Delta Remoteness is an integer that helps to rank moves of the same value
    based on their remotenesses. (Lower delta remoteness is better.)
    - The delta remoteness of a winning move is the remoteness of the move's
    child position minus the minimum remoteness of all lose child positions 
    of `position`.
    - The delta remoteness of a tying mvoe is the remoteness of the move's
    child position minus the minimum remoteness of all tie child positions
    of `position`.
    - The delta remoteness of a losing move is the maximum remoteness of all
    (win) child positions minus the remoteness of the move's child position.
    - The delta remoteness of draw moves is infinite, however here we just say
    that it is 0 because we treat tie and draw as different values.

    This function also handles the case in which a move's child position has a
    known value but a finite unknown remoteness. For the sake of calculating
    delta remoteness, we treat the position as though it has a remoteness 1
    higher than the maximum-remoteness child position of the same value. And
    if all child posiitons of that value have an unknown finite remoteness, we
    treat it as though the min and max remotenesses of child positions of that
    value are 1.
    """
    if not next_stats:
        return next_stats

    def key_next_stat_by_move_value_then_delta_remoteness(next_stat):
        VALUES = ['win', 'tie', 'draw', 'lose', 'unsolved']
        move_value = next_stat['moveValue']
        delta_remotenesss = next_stat['deltaRemoteness']
        if move_value == 'undecided':
            return 1
        return (VALUES.index(move_value), delta_remotenesss)
    
    lose_children_remotenesses = []
    win_children_remotenesses = []
    tie_children_remotenesses = []
    win_finite_unknown_child_remoteness_exists = False
    lose_finite_unknown_child_remoteness_exists = False
    tie_finite_unknown_child_remoteness_exists = False

    for child in next_stats:
        child_value = child['positionValue']
        child_remoteness = child['remoteness']
        if child_value == 'win':
            if child_remoteness != Remoteness.FINITE_UNKNOWN:
                win_children_remotenesses.append(child_remoteness)
            else:
                win_finite_unknown_child_remoteness_exists = True
        elif child_value == 'lose':
            if child_remoteness != Remoteness.FINITE_UNKNOWN:
                lose_children_remotenesses.append(child_remoteness)
            else:
                lose_finite_unknown_child_remoteness_exists = True
        elif child_value == 'tie':
            if child_remoteness != Remoteness.FINITE_UNKNOWN:
                tie_children_remotenesses.append(child_remoteness)
            else:
                tie_finite_unknown_child_remoteness_exists = True

    max_win_child_remoteness = max(win_children_remotenesses) if win_children_remotenesses else 0
    if win_finite_unknown_child_remoteness_exists:
        max_win_child_remoteness += 1
    
    min_lose_child_remoteness = 1
    max_lose_child_remoteness = 1
    if lose_children_remotenesses:
        min_lose_child_remoteness = min(lose_children_remotenesses)
        if lose_finite_unknown_child_remoteness_exists:
            max_lose_child_remoteness = max(lose_children_remotenesses) + 1

    min_tie_child_remoteness = 1
    max_tie_child_remoteness = 1
    if tie_children_remotenesses:
        min_tie_child_remoteness = min(tie_children_remotenesses)
        if tie_finite_unknown_child_remoteness_exists:
            max_tie_child_remoteness = max(tie_children_remotenesses) + 1

    def wrangle_next_stat(next_stat):
        position_value = next_stat['positionValue']
        remoteness = next_stat['remoteness']
        move_value = next_stat.get('moveValue', position_value)

        # If not using UWAPI position string, assume turn switching; otherwise, decide 
        # whether to switch the turn based on the current and next turn character. 
        if position[:2] != 'R_' or next_stat['position'][2] != position[2]:
            if position_value == 'win':
                move_value = 'lose'
            elif position_value == 'lose':
                move_value = 'win'
            
        next_stat['moveValue'] = move_value

        # Delta remoteness (grouped by move value)
        delta_remoteness = 0         
        if move_value == 'win':
            if remoteness == Remoteness.FINITE_UNKNOWN:
                remoteness = max_lose_child_remoteness
            delta_remoteness = remoteness - min_lose_child_remoteness
        elif move_value == 'lose':
            if remoteness == Remoteness.FINITE_UNKNOWN:
                remoteness = max_win_child_remoteness
            delta_remoteness = max_win_child_remoteness - remoteness
        elif move_value == 'tie':
            if remoteness == Remoteness.FINITE_UNKNOWN:
                remoteness = max_tie_child_remoteness
            delta_remoteness = remoteness - min_tie_child_remoteness
        
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
            'gui': game.gui
        }
        for (game_id, game) in games.items()
    ]
    response.sort(key=lambda g: g['name'])
    return format_response_ok(response)

@app.route("/games/instructions/<type>/<game_id>/<language>/")
def handle_instructions(type, game_id, language):
    response = {
        'instructions': md_instr(game_id, type, language)
    }
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
        'variants': [
            {
                'variantId': variant_id,
                'description': variant.desc,
                'startPosition': variant.start_position(),
                'imageAutoGUIData': get_image_autogui_data(game_id, variant_id),
                'gui': variant.gui
            }
            for (variant_id, variant) in game.variants.items()
        ],
        'custom': custom_variant,
        'supportsWinBy': game.supports_win_by
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
                'startPosition': variant.start_position(),
                'imageAutoGUIData': get_image_autogui_data(game_id, variant_id),
                'gui': variant.gui
            }
        ]
    })


@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>/')
def handle_position(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    
    position_data = variant.position_data(position)
    if position_data is None:
        return format_response_err('Passed in Invalid Game State')
    if position_data['remoteness'] == 0:
        position_data['moves'] = []
    else:
        position_data['moves'] = wrangle_next_stats(position, position_data['moves'])
    return format_response_ok(position_data)


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
    app.run(port=8082)
