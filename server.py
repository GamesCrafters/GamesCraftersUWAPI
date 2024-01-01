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

def error(a):
    return {'error': f'Invalid {a}'}

def wrangle_next_stats(position, next_stats):
    """
    Given a position and next-move data, this function
    1) Calculates the move value and delta-remoteness of all legal moves AND
    2) Returns the moves sorted from best-to-worst.
    (Note: A "move value" is the value of the move for the person
    making the move, and a "position value" is the value of the position
    for the player whose turn it is at that position.)

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

@app.route("/")
@app.route("/games/")
def get_games() -> dict[str, list[dict[str, str]]]:
    one_player_games, two_player_games = [], []
    for game_id, game in games.items():
        game_obj = {
            'id': game_id,
            'name': game.name,
            'gui': game.gui
        }
        if game.is_two_player_game:
            two_player_games.append(game_obj)
        else:
            one_player_games.append(game_obj)

    sort_by_name = lambda g: g['name']
    one_player_games.sort(key=sort_by_name)
    two_player_games.sort(key=sort_by_name)
    
    return {
        'onePlayerGames': one_player_games,
        'twoPlayerGames': two_player_games
    }

@app.route("/games/<game_id>/")
def get_game(game_id):
    if game_id in games:
        game = games[game_id]
        return {
            'id': game_id,
            'name': game.name,
            'variants': [
                {
                    'id': variant_id,
                    'name': variant.name,
                    'startPosition': variant.start_position(),
                    'imageAutoGUIData': get_image_autogui_data(game_id, variant_id),
                    'gui': variant.gui
                }
                for (variant_id, variant) in game.variants.items()
            ],
            'allowCustomVariantCreation': bool(game.custom_variant),
            'supportsWinBy': game.supports_win_by
        }
    return error('Game')

@app.route('/games/<game_id>/<variant_id>/')
def get_variant(game_id, variant_id):
    if game_id in games:
        variant = games[game_id].variant(variant_id)
        if variant:
            return {
                'id': variant_id,
                'name': variant.name,
                'startPosition': variant.start_position(),
                'imageAutoGUIData': get_image_autogui_data(game_id, variant_id),
                'gui': variant.gui
            }
        return error('Variant')
    return error('Game')

@app.route('/games/<game_id>/<variant_id>/<position>/')
def get_position(game_id, variant_id, position):
    if game_id in games:
        variant = games[game_id].variant(variant_id)
        if variant:
            position_data = variant.position_data(position)
            if position_data:
                position_data['moves'] = wrangle_next_stats(position, position_data['moves'])
                return position_data
            return error('Position')
        return error('Variant')
    return error('Game')
    
@app.route("/instructions/<type>/<game_id>/<language>/")
def get_game_instructions(type, game_id, language) -> dict[str: str]:
    return {'instructions': md_instr(game_id, type, language)}

if __name__ == '__main__':
    app.run(port=8082)
