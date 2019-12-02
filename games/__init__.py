from .models import Game, GameVariant
from .gamesman_classic import GamesmanClassicDataProvider
from .gamesman_java import GamesmanJavaDataProvider
from .chess import RegularChessVariant


games = {

    'ttt': Game(
        name='Tic-Tac-Toe',
        desc="Place your piece onto an open square. Wins when you connect three in a row horizontally, vertically, or diagonally.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ttt',
                data_provider_variant_id=-1)
        }),

    'chess': Game(
        name='Chess',
        desc="Chess",
        variants={
            '7-man': RegularChessVariant()
        }),

    '1210': Game(
        name='0 to 10 by 1 or 2',
        desc="A player may either place 1 or 2 pieces on their turn. Wins when player reaches 10.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='1210',
                data_provider_variant_id=-1)
        }),

    'sim': Game(
        name='Sim',
        desc="Connect two dots with a line of your color. Wins when you force your opponent to complete a triangle.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='sim',
                data_provider_variant_id=-1)
        }),

    'ooe': Game(
        name='Odd or Even',
        desc="15 matches, take 1, 2, or 3 matches. Wins when you have even number of matches when 0 matches on board.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ooe',
                data_provider_variant_id=-1)
        }),

    'snake': Game(
        name='Snake',
        desc="Move one step up, left, or right. Wins when your opponent has no more moves given the current position.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='snake',
                data_provider_variant_id=-1)
        }),

    'foxes': Game(
        name='Fox & Geese',
        desc="Initially set up with seventeen geese G and one fox F. First player G, second player F. Players take turns moving a goose or fox to an adjacent spot. Geese are allowed to move one square left, right or down, while the fox can move either left, right, up, or down. The fox may also capture a goose on his turn by jumping over the goose that is in his immediate path.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='foxes',
                data_provider_variant_id=-1)
        }),

    'dnb': Game(
        name='Dots & Boxes',
        desc="Players take turns connecting horizontal or vertical lines between dots. Box has a designated owner once four sides have been connected. Wins when a player has the majority of the boxes.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='dnb',
                data_provider_variant_id=-1)
        }),

    'tilechess': Game(
        name='Tile Chess',
        desc="A chess variant (with slightly different valid moves). Wins when checkmate opponent's King.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='tilechess',
                data_provider_variant_id=-1)
        }),

    '1ton': Game(
        name='1 to n by 1 or 2',
        desc="A player may either place 1 or 2 pieces on their turn. Wins when player reaches n (n is chosen by the players).",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='1ton',
                data_provider_variant_id=-1)
        }),

    'swans': Game(
        name='Dragons & Swans',
        desc="Swan places a piece onto the board if there are remaining pieces from the initial pile, otherwise move piece to an orthogonally adjacent empty board position. Dragon can either move a piece to an orthogonally adjacent empty square, or captures a swan by jumping over it to an empty square the other side. Swans wins when they surround all the dragons and dragons win when they eat all the swans.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=-1)
        }),

    'quickchess': Game(
        name='Quick Chess',
        desc="Wins when you checkmate opponent's King.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='quickchess',
                data_provider_variant_id=-1)
        }),

    'othello': Game(
        name='Othello',
        desc="You can place a piece on any blank spot such that it has at least one of your opponent's pieces adjacent to that spot, and the line from the blank spot and the opponent's piece has, at the end of it, one of your own pieces, with all of your opponent's pieces in between. Wins if you have more pieces when the board is completely filled.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='othello',
                data_provider_variant_id=-1)
        }),

    'mancala': Game(
        name='Mancala',
        desc="Choose one of your bins (cannot be an empty bin or the mancala). This disperses your stones counterclockwise around the board from that bin. Game ends when all the stones are contained in the two mancalas, and the player whose mancala contains more stones wins.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='mancala',
                data_provider_variant_id=-1)
        }),

    'Lgame': Game(
        name='L-game',
        desc='The L game is played on a 4x4 board. Each player has a 3×2 L-shaped piece, and there are two 1×1 neutral pieces. On each turn, a player must first move their L piece to a new location (can rotate or flip) and then may optionally move one of the neutral pieces. Won when the opponent cannot move their L piece to a new location.',
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='Lgame',
                data_provider_variant_id=-1)
        }),

    'dinododgem': Game(
        name='Dino Dodgem',
        desc="Each player places their dinosaurs on the posts that match their dinosaur color. Each player takes turns moving their pieces forward by one space. They may not move backward, or diagonally. Blocking, however, is allowed and is considered a key part to winning the game. Players are not allowed to jump, move diagonally or move into the opponent's starting area. Wins when you are the first player to get all three of their dinosaurs off the other side of the board.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='dinododgem',
                data_provider_variant_id=-1)
        }),

    'dao': Game(
        name='Dao',
        desc="Each player moves their pieces (one per turn) as far as possible during each turn, till their pieces reach the end of the board or till their pieces reach another one of own pieces (in any direction). To win, the player can either form a straight line with 4 of their own pieces, occupy the four corners of the board, or forming a 2 x 2 square with their pieces anywhere on the playing board.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='dao',
                data_provider_variant_id=-1)
        }),

    'ctoi': Game(
        name='Chung-Toi',
        desc="In the first phase, each player alternates turns placing three pieces on the board. In the second phase, the pieces may be moved to different slots, rotated or both. Wins when player achieves three in a row, vertically, horizontally or diagonally.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ctoi',
                data_provider_variant_id=-1)
        }),

    'connect4': Game(
        name='Connect 4',
        desc='Tic Tac Toe with gravity',
        variants={
            '4x4x4': GameVariant(
                name='4x4x4',
                desc='4x4 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=4;height=4;pieces=4'),
            '4x5x4': GameVariant(
                name='4x5x4',
                desc='4x5 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=4;height=5;pieces=4'),
            '4x6x4': GameVariant(
                name='4x6x4',
                desc='4x6 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=4;height=6;pieces=4'),
            '5x4x4': GameVariant(
                name='5x4x4',
                desc='5x4 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=5;height=4;pieces=4'),
            '5x5x4': GameVariant(
                name='5x5x4',
                desc='5x5 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=5;height=5;pieces=4'),
            '5x6x4': GameVariant(
                name='5x6x4',
                desc='5x6 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=5;height=6;pieces=4'),
            '6x4x4': GameVariant(
                name='6x4x4',
                desc='6x4 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=6;height=4;pieces=4'),
            '6x5x4': GameVariant(
                name='6x5x4',
                desc='6x5 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=6;height=5;pieces=4'),
            # '6x6x4': GameVariant(
            #     name='6x6x4',
            #     desc='6x6 board with 4 in a row',
            #     data_provider=GamesmanJavaDataProvider,
            #     data_provider_game_id='connect4',
            #     data_provider_variant_id=';width=6;height=6;pieces=4'),
            '7x4x4': GameVariant(
                name='7x4x4',
                desc='7x4 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=7;height=4;pieces=4'),
            '7x5x4': GameVariant(
                name='7x5x4',
                desc='7x5 board with 4 in a row',
                data_provider=GamesmanJavaDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=';width=7;height=5;pieces=4'),
            # '7x6x4': GameVariant(
            #     name='7x6x4',
            #     desc='7x6 board with 4 in a row',
            #     data_provider=GamesmanJavaDataProvider,
            #     data_provider_game_id='connect4',
            #     data_provider_variant_id=';width=7;height=6;pieces=4'),
        }),

}
