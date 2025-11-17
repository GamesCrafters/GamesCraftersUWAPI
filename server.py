from flask import Flask, request, jsonify
from flask_cors import CORS

from games import games
from games.image_autogui_data import *
from games.models import Value, Remoteness
from md_api import md_instr

app = Flask(__name__)
CORS(app)

# Helper Functions

def error(a):
    return {'error': f'Invalid {a}'}

def key_move_obj_by_move_value_then_delta_remoteness(move_obj):
    """
    Return a sort key for the input move object.
    As a reminder, value/remoteness tuples are listed from best to worst as follows:
    Low-Remoteness Win, High-Remoteness Win, Low-Remoteness Tie, High-Remoteness Tie, 
    Draw, High-Remoteness Lose, Lower Remoteness Lose
    """
    VALUES = (Value.WIN, Value.TIE, Value.DRAW, Value.LOSE, Value.UNSOLVED, Value.UNDECIDED)
    move_value = move_obj['moveValue']
    print(move_value)

    delta_remotenesss = move_obj['deltaRemoteness']
    return (VALUES.index(move_value), delta_remotenesss)

def wrangle_move_objects_1Player(position_data):
    if 'remoteness' not in position_data: # Means not possible to solve puzzle from this state
        position_data['remoteness'] = Remoteness.INFINITY
    current_position_remoteness = position_data['remoteness']
    move_objs = position_data.get('moves', [])
    for move_obj in move_objs:
        if 'remoteness' not in move_obj: # Not possible to solve puzzle from this state
            move_obj['remoteness'] = Remoteness.INFINITY
            move_obj['deltaRemoteness'] = 0
            move_obj['moveValue'] = Value.LOSE
        else: # Possible to solve puzzle from this state.
            delta_remoteness = current_position_remoteness - move_obj['remoteness']
            move_obj['deltaRemoteness'] = delta_remoteness
            # Set moveValue to win, lose, or tie based on how we want to color the move buttons.
            # Moves that reduce remoteness should be green. Moves that increase remoteness should
            # be red. Moves that neither reduce nor increase remoteness should be yellow.
            move_obj['moveValue'] = Value.WIN if delta_remoteness > 0 else Value.LOSE if delta_remoteness < 0 else Value.TIE
    move_objs.sort(key=key_move_obj_by_move_value_then_delta_remoteness)

def wrangle_move_objects_2Player(position_data):
    """
    Given a position and next-move data, this function
    1) Calculates the move value and delta-remoteness of all legal moves AND
    2) Returns the moves sorted from best-to-worst.
    (Note: A "move value" is the value of the move for the person
    making the move, and a "position value" is the value of the position
    for the player whose turn it is at that position.)

    Suppose a move M has a move-value of V (V is one of win, tie, draw, lose).
    The delta-remoteness of M is the magnitude of the difference between the 
    remoteness of M and the remoteness of the best move out of all moves 
    that have move-value V.
    - The delta remoteness of a winning move is the remoteness of the move's
    child position minus the minimum remoteness of all lose child positions 
    of `position`.
    - The delta remoteness of a tying move is the remoteness of the move's
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
    if all child positions of that value have an unknown finite remoteness, we
    treat it as though the min and max remotenesses of child positions of that
    value are 1.
    """
    if position_data['positionValue'] == Value.DRAW:
        position_data['remoteness'] = Remoteness.INFINITY

    move_objs = position_data.get('moves', [])    
    lose_children_remotenesses = []
    win_children_remotenesses = []
    tie_children_remotenesses = []
    win_finite_unknown_child_remoteness_exists = False
    lose_finite_unknown_child_remoteness_exists = False
    tie_finite_unknown_child_remoteness_exists = False

    for move_obj in move_objs:
        child_value = move_obj['positionValue']
        child_remoteness = move_obj.get('remoteness', Remoteness.INFINITY)
        if child_value == Value.WIN:
            if child_remoteness != Remoteness.FINITE_UNKNOWN:
                win_children_remotenesses.append(child_remoteness)
            else:
                win_finite_unknown_child_remoteness_exists = True
        elif child_value == Value.LOSE:
            if child_remoteness != Remoteness.FINITE_UNKNOWN:
                lose_children_remotenesses.append(child_remoteness)
            else:
                lose_finite_unknown_child_remoteness_exists = True
        elif child_value == Value.TIE:
            if child_remoteness != Remoteness.FINITE_UNKNOWN:
                tie_children_remotenesses.append(child_remoteness)
            else:
                tie_finite_unknown_child_remoteness_exists = True
        elif child_value == Value.DRAW:
            move_obj['remoteness'] = child_remoteness

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
    
    autogui_position = position_data['autoguiPosition']
    not_in_autogui_format = not ((autogui_position[0] == '1' or autogui_position[0] == '2') and autogui_position[1] == '_')

    for move_obj in move_objs:
        position_value = move_obj['positionValue']
        remoteness = move_obj['remoteness']
        move_value = move_obj.get('moveValue', position_value)

        # If not using autogui-formatted position string, assume turn switching; otherwise, decide 
        # whether to switch the turn based on the current and next turn character. 
        if not_in_autogui_format or move_obj['autoguiPosition'][0] != autogui_position[0]:
            if position_value == Value.WIN:
                move_value = Value.LOSE
            elif position_value == Value.LOSE:
                move_value = Value.WIN
            
        move_obj['moveValue'] = move_value

        # Delta remoteness (grouped by move value)
        delta_remoteness = 0         
        if move_value == Value.WIN:
            if remoteness == Remoteness.FINITE_UNKNOWN:
                remoteness = max_lose_child_remoteness
            delta_remoteness = remoteness - min_lose_child_remoteness
        elif move_value == Value.LOSE:
            if remoteness == Remoteness.FINITE_UNKNOWN:
                remoteness = max_win_child_remoteness
            delta_remoteness = max_win_child_remoteness - remoteness
        elif move_value == Value.TIE:
            if remoteness == Remoteness.FINITE_UNKNOWN:
                remoteness = max_tie_child_remoteness
            delta_remoteness = remoteness - min_tie_child_remoteness
        
        move_obj['deltaRemoteness'] = delta_remoteness
    
    move_objs.sort(key=key_move_obj_by_move_value_then_delta_remoteness)
    

# Routes

@app.route("/")
def get_games() -> list[dict[str, str]]:
    all_games = [{
        'id': game_id,
        'name': game.name,
        'type': 'twoPlayer' if game.is_two_player_game else 'onePlayer',
        'gui': game.gui
    } for game_id, game in games.items()]
    all_games.sort(key=lambda g: g['name'])
    return jsonify(all_games)

@app.route("/<game_id>/")
def get_game(game_id: str):
    if game_id in games:
        game = games[game_id]
        return {
            'id': game_id,
            'name': game.name,
            'variants': [
                {
                    'id': variant_id,
                    'name': variant.name,
                    'gui': variant.gui
                }
                for variant_id, variant in game.variants.items()
            ],
            'allowCustomVariantCreation': bool(game.custom_variant),
            'supportsWinBy': game.supports_win_by
        }
    return error('Game')

@app.route('/<game_id>/<variant_id>/')
def get_variant(game_id: str, variant_id: str):
    if game_id in games:
        variant = games[game_id].variant(variant_id)
        if variant:
            start_position_data = variant.start_position()
            return {
                'id': variant_id,
                'name': variant.name,
                'startPosition': start_position_data.get('position', ''),
                'autoguiStartPosition': start_position_data.get('autoguiPosition', ''),
                'imageAutoGUIData': get_image_autogui_data(game_id, variant_id),
                'gui': variant.gui
            }
        return error('Variant')
    return error('Game')

@app.route('/<game_id>/<variant_id>/positions/')
def get_position(game_id: str, variant_id: str):
    if game_id in games:
        variant = games[game_id].variant(variant_id)
        if variant:
            position = request.args.get('p', None)
            if position:
                position_data = variant.position_data(position)
                if position_data:
                    if games[game_id].is_two_player_game:
                        wrangle_move_objects_2Player(position_data)
                    else:
                        wrangle_move_objects_1Player(position_data)
                    return position_data
            return error('Position')
        return error('Variant')
    return error('Game')
    
@app.route("/<game_id>/<variant_id>/instructions/")
def get_instructions(game_id: str, variant_id: str) -> dict[str: str]:
    # We currently give the same instruction markdown string for all
    # variants of a particular game. Variant-specific instructions
    # are not supported yet.
    if game_id in games:
        game_type = 'games' if games[game_id].is_two_player_game else 'puzzles'
        locale = request.args.get('locale', 'en')
        return {'instructions': md_instr(game_type, game_id, locale)}
    return error('Game')

if __name__ == '__main__':
    app.run(port=8082)