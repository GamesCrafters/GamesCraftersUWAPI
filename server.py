import os

from flask import Flask, escape, request

from games import games, GamesmanClassicDataProvider

app = Flask(__name__)


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
    result['moves'] = variant.next_stats(position)
    return format_response_ok(result)


@app.route('/games/<game_id>/variants/<variant_id>/positions/<position>/moves')
def handle_position_moves(game_id, variant_id, position):
    variant = get_game_variant(game_id, variant_id)
    if not variant:
        return format_response_err('Game/Variant not found')
    return format_response_ok(variant.next_stats(position))


@app.route('/internal/classic-games')
def handle_classic_games():
    return GamesmanClassicDataProvider.getGames()


if __name__ == '__main__':
    port = os.environ.get('API_PORT', None)
    app.run(port=port)
