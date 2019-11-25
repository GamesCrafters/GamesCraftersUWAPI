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


def wrangle_next_stats(next_stats, curr_position_value):
    if not next_stats:
        return next_stats

    best_remoteness_evaluator = max if curr_position_value == "lose" else min
    best_remoteness = best_remoteness_evaluator(
        [next_stat['remoteness'] for next_stat in next_stats])

    def wrangle_next_stat(next_stat):
        position_value = next_stat['positionValue']
        remoteness = next_stat['remoteness']
        delta_remoteness = abs(remoteness - best_remoteness)

        # Get move value from next position value
        if position_value == 'win':
            move_value = 'lose'
        elif position_value == 'lose':
            move_value = 'win'
        else:
            move_value = position_value
        next_stat['moveValue'] = move_value

        # Delta remoteness
        next_stat['deltaRemoteness'] = delta_remoteness

        return next_stat

    return sorted(map(wrangle_next_stat, next_stats), key=lambda next_stat: next_stat['deltaRemoteness'])


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
    result['moves'] = wrangle_next_stats(
        variant.next_stats(position), result['positionValue'])
    return format_response_ok(result)


@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>/moves')
def handle_position_moves(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    curr_stat = variant.stat(position)
    return format_response_ok(wrangle_next_stats(variant.next_stats(position), curr_stat['positionValue']))


@app.route('/internal/classic-games')
def handle_classic_games():
    return GamesmanClassicDataProvider.getGames()


if __name__ == '__main__':
    port = os.environ.get('API_PORT', None)
    app.run(port=port)
