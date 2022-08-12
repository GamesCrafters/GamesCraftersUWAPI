import os

from flask import Flask, escape, request
from flask_cors import CORS

from games import games, GamesmanClassicDataProvider
from games.AutoGUI_v2_Games import autogui_v2_games

from md_api import read_from_link

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
default_autogui_v2_theme_id = "default"

CORS(app)

# ID mapping from Uni to GC to get game instructions.
ids = {'1210': '1210', 'abalone': 'abalone', 'achi': 'achi', 'ago': 'atarigo',
       'baghchal': 'baghchal', 'ctoi': 'chungtoi', 'dao': 'dao', 'dinododgem': 'dinododgem',
       'dnb': 'dotsandboxes', 'swans': 'dragonsandswans', 'foxes': 'foxandgeese',
       'Lgame': 'lgame', 'mancala': 'mancala', '369mm': 'ninemensmorris', 'topitop': 'topitop', 'tttwo': 'topitop', 'ooe': 'oddoreven',
       'othello': 'othello', 'quickchess': 'quickchess', 'sim': 'sim', 'snake': 'snake', '3spot': 'threespot',
       'ttt': 'tictactoe', 'tilechess': 'tilechess', 'connect4': 'connect4', 'dodgem': 'dodgem'}

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

def get_variant_themes(game_id, variant_id):
    game = get_game(game_id)
    if game and game.autogui_v2:
        v2_themes = autogui_v2_games[game_id]
        theme_ids = [variant_id, default_autogui_v2_theme_id]
        for theme_id in theme_ids:
            if theme_id in v2_themes:
                return v2_themes[theme_id]
    return None

def wrangle_next_stats(next_stats):
    if not next_stats:
        return next_stats

    def next_stats_remoteness_where_position_value(position_value):
        return [next_stat['remoteness'] for next_stat in next_stats if next_stat['positionValue'] == position_value]

    def key_next_stat_by_move_value_then_delta_remoteness(next_stat):
        VALUES = ['win', 'tie', 'draw', 'lose']
        move_value = next_stat['moveValue']
        delta_remotenesss = next_stat['deltaRemoteness']
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
        move_value = next_stat.get('moveValue', None)

        # Get move value from next position value
        if not move_value:
            if position_value == 'win':
                move_value = 'lose'
            elif position_value == 'lose':
                move_value = 'win'
            else:
                move_value = position_value
            next_stat['moveValue'] = move_value

        # Delta remoteness (grouped by move value)
        if move_value == 'win':
            delta_remoteness = remoteness - best_next_stats_remoteness_where_move_value_win
        elif move_value == 'lose':
            delta_remoteness = best_next_stats_remoteness_where_move_value_lose - remoteness
        elif move_value == 'tie':
            delta_remoteness = remoteness - best_next_stats_remoteness_where_move_value_tie
        else:
            delta_remoteness = 0
        next_stat['deltaRemoteness'] = delta_remoteness

        return next_stat

    return sorted(map(wrangle_next_stat, next_stats), key=key_next_stat_by_move_value_then_delta_remoteness)


# Routes


@app.route("/games/")
def handle_games():
    return format_response_ok([
        {
            'gameId': game_id,
            'name': game.name,
            'status': game.status
        }
        for (game_id, game) in games.items() if game.status == 'available'
    ])


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
                'startPosition': variant.start_position()
            }
            for (variant_id, variant) in game.variants.items() if variant.status != 'unavailable'
        ],
        'custom': custom_variant,
        'autogui_v2': game.autogui_v2
    })

@app.route('/games/<game_id>/variants/<variant_id>/')
def handle_variant(game_id, variant_id):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    themes = get_variant_themes(game_id, variant_id)["themes"]
    return format_response_ok({
        'gameId': game_id,
        'variant': [
            {
                'variantId': variant_id,
                'description': variant.desc,
                'status': variant.status,
                'startPosition': variant.start_position(),
                'themes': themes
            }
        ]
    })

@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>/')
def handle_position(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    result = variant.stat(position)
    result['moves'] = wrangle_next_stats(variant.next_stats(position))
    return format_response_ok(result)

@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>/moves/')
def handle_position_moves(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    return format_response_ok(wrangle_next_stats(variant.next_stats(position)))


@app.route('/internal/classic-games/')
def handle_classic_games():
    return GamesmanClassicDataProvider.getGames()


if __name__ == '__main__':
    port = os.environ.get('API_PORT', None)
    app.run(port=port)
