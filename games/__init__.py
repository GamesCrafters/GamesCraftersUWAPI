from .models import Game, GameVariant
from .gamesman_classic import GamesmanClassicDataProvider
from .chess import RegularChessVariant


games = {
    'ttt': Game(
        name='Tic Tac Toe',
        desc='3 in a row',
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ttt',
                data_provider_variant_id=-1)
        })
}
