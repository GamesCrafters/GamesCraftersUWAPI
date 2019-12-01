import os

from flask import Flask, escape, request
from flask_cors import CORS

from games import games, GamesmanClassicDataProvider

app = Flask(__name__)
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

        # Get move value from next position value
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


@app.route("/games")
def handle_games():
    return format_response_ok([
        {
            'gameId': game_id,
            'name': game.name
        }
        for (game_id, game) in games.items()
    ])


@app.route("/games/<game_id>")
def handle_game(game_id):
    game = get_game(game_id)
    if not game:
        return format_response_err('Game not found')
    return format_response_ok({
        'gameId': game_id,
        'name': game.name,
        'variants': [
            {
                'variantId': variant_id,
                'description': variant.desc,
                'startPosition': variant.start_position()
            }
            for (variant_id, variant) in game.variants.items()
        ]
    })


@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>')
def handle_position(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    result = variant.stat(position)
    result['moves'] = wrangle_next_stats(variant.next_stats(position))
    return format_response_ok(result)


@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>/moves')
def handle_position_moves(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    curr_stat = variant.stat(position)
    return format_response_ok(wrangle_next_stats(variant.next_stats(position)))


@app.route('/internal/classic-games')
def handle_classic_games():
    return GamesmanClassicDataProvider.getGames()


if __name__ == '__main__':
    port = os.environ.get('API_PORT', None)
    app.run(port=port)
