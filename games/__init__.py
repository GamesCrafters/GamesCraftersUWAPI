import os

from .models import Game, GameVariant
from .gamesman_classic import GamesmanClassicDataProvider
from .gamesman_java import GamesmanJavaDataProvider, GamesmanJavaConnect4GameVariant
from .json_game_variant import JSONGameVariant
from .chess import RegularChessVariant
from .TicTacToe3x3x2GameVariant import TicTacToe3x3x2GameVariant


dirname = os.path.dirname(__file__)

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
                data_provider_variant_id=-1,
                status='stable'),
            'misere': GameVariant(
                name='Misere',
                desc='Misere',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ttt',
                data_provider_variant_id=1,
                status='stable')
        }),

    'ttt3d': Game(
        name='3D Tic-Tac-Toe',
        desc='3D Tic-Tac-Toe',
        variants={
            '3x3x2': TicTacToe3x3x2GameVariant(
                name='3x3x2',
                desc='3x3x2',
                filepath=os.path.join(dirname, 'solutions/ttt3d/3x3x2.txt'),
                status='dev')
        }),

    'tttwo': Game(
        name='Tic-Tac-Two',
        desc="Add piece onto a square in the grid, move a piece on the board, or move the grid. Wins when you connect three in a row horizontally, vertically, or diagonally within the grid.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='tttwo',
                data_provider_variant_id=-1,
                status='stable')
        }),

    'stt': Game(
        name='Shift Tac Toe',
        desc='',
        variants={
            'default': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='stt',
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
        }),

    '0ton': Game(
        name='0 to n by 1 or 2',
        desc="A player may either place 1 or 2 pieces on their turn. Wins when player reaches n (n is chosen by the players).",
        variants={
            '10': GameVariant(
                name='10',
                desc='Wins when player reaches 10.',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='1ton',
                data_provider_variant_id=-1,
                status='dev')
        }),

    'nto0': Game(
        name='n to 0 by 1 or 2',
        desc='A player may either take 1 or 2 pieces on their turn. Wins when player reaches 0.',
        variants={
            '4': JSONGameVariant(os.path.join(dirname, 'solutions/nto0/4to0.json'))
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
        }),

    'swans': Game(
        name='Dragons & Swans',
        desc="Swan places a piece onto the board if there are remaining pieces from the initial pile, otherwise move piece to an orthogonally adjacent empty board position. Dragon can either move a piece to an orthogonally adjacent empty square, or captures a swan by jumping over it to an empty square the other side. Swans wins when they surround all the dragons and dragons win when they eat all the swans.",
        variants={
            '1': GameVariant(
                name='1 Dragon',
                desc='1 Dragon',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=-1,
                status='dev'),
            '2': GameVariant(
                name='2 Dragons',
                desc='2 Dragons',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=5,
                status='dev'),
            '3': GameVariant(
                name='3 Dragons',
                desc='3 Dragons',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=9,
                status='dev'),
            '4': GameVariant(
                name='4 Dragons',
                desc='4 Dragons',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=13,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
        }),

    'Lgame': Game(
        name='L-game',
        desc='The L game is played on a 4x4 board. Each player has a 3×2 L-shaped piece, and there are two 1×1 neutral pieces. On each turn, a player must first move their L piece to a new location (can rotate or flip) and then may optionally move one of the neutral pieces. Wins when the opponent cannot move their L piece to a new location.',
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='Lgame',
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
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
                data_provider_variant_id=-1,
                status='dev')
        }),

    'baghchal': Game(
        name='Bagh Chal',
        desc="In the first phase the goats are placed on the board while the tigers are moved. In the second phase both the goats and the tigers are moved. For the tigers, the objective is to 'capture' five goats to win. Capturing is performed as in alquerque and draughts, by jumping over the goats, although capturing is not obligatory. The goats win by blocking all the tigers' legal moves.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='baghchal',
                data_provider_variant_id=-1,
                status='dev')
        }),

    'ago': Game(
        name='Atari Go',
        desc="A move consists of the player putting one of their pieces on an empty intersection of the board. The first player to capture one or more pieces (depending on how many pieces you and your opponent want) wins. The rules are similar to those of regular Go. Black player makes first move. Players alternative placing stones onto the board. Pieces on the board cannot be moved unless captured. Capturing happens when one of your or your opponent's piece is surrounded.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ago',
                data_provider_variant_id=-1,
                status='dev')
        }),

    'achi': Game(
        name='Achi',
        desc="There are two types of moves in Achi: place moves and slide moves. In a place move, you place three pieces on a board. Once all of your three pieces are on the board, you make a slide move by selecting a piece to a connected and unoccupied spot. Win by getting three in a row either horizontally, vertically or diagonally.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='achi',
                data_provider_variant_id=-1,
                status='stable')
        }),

    'abalone': Game(
        name='Abalone',
        desc="A player may move either one, two or three pieces in any of the six directions as long as the space is moving to is empty. There are several types of moves. In line is a move forwards or backwards from one point to the next with 2 or 3 marbles. A broadside move involves moving the marbles parallel to an open adjacent spot.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='abalone',
                data_provider_variant_id=-1,
                status='dev')
        }),

    '3spot': Game(
        name='Three Spot',
        desc="4x4 board. Each player has a 3×2 L-shaped piece, and there are two 1×1 neutral pieces. During a player's turn, player must move his/her piece such that the piece must stay on the board and must cover at least one new square. Afterwards, the same player must move the neutral piece to a new position as well. Wins when you score 12 points when your opponent has scored at least 6.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='3spot',
                data_provider_variant_id=-1,
                status='dev')
        }),

    '369mm': Game(
        name='Three Six Nine Mens Morris',
        desc="Players first alternate placing pieces onto empty nodes on the board. Once all pieces have been placed, players take turns sliding their pieces to other empty nodes connected to it by a line. If a player's move completes a 'mill', three in a line, then that player gets removes one of the opponent's pieces from the board that is currently not in a mill. A mill may be broken and reformed. When a player is down to 3 pieces, that player may move his or her piece to any empty node on the board.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='369mm',
                data_provider_variant_id=-1,
                status='dev')
        }),

    'connect4': Game(
        name='Connect 4',
        desc='Tic Tac Toe with gravity',
        variants={
            '4x4x4': GamesmanJavaConnect4GameVariant(
                width=4,
                height=4,
                pieces=4,
                status='dev'
            ),
            '4x5x4': GamesmanJavaConnect4GameVariant(
                width=4,
                height=5,
                pieces=4,
                status='dev'
            ),
            '4x6x4': GamesmanJavaConnect4GameVariant(
                width=4,
                height=6,
                pieces=4,
                status='dev'
            ),
            '5x4x4': GamesmanJavaConnect4GameVariant(
                width=5,
                height=4,
                pieces=4,
                status='dev'
            ),
            '5x5x4': GamesmanJavaConnect4GameVariant(
                width=5,
                height=5,
                pieces=4,
                status='dev'
            ),
            '5x6x4': GamesmanJavaConnect4GameVariant(
                width=5,
                height=6,
                pieces=4,
                status='dev'
            ),
            '6x4x4': GamesmanJavaConnect4GameVariant(
                width=6,
                height=4,
                pieces=4,
                status='dev'
            ),
            '6x5x4': GamesmanJavaConnect4GameVariant(
                width=6,
                height=5,
                pieces=4,
                status='dev'
            ),
            '6x6x4': GamesmanJavaConnect4GameVariant(
                width=6,
                height=6,
                pieces=4,
                status='unavailable'
            ),
            '7x4x4': GamesmanJavaConnect4GameVariant(
                width=7,
                height=4,
                pieces=4,
                status='dev'
            ),
            '7x5x4': GamesmanJavaConnect4GameVariant(
                width=7,
                height=5,
                pieces=4,
                status='dev'
            ),
            '7x6x4': GamesmanJavaConnect4GameVariant(
                width=7,
                height=6,
                pieces=4,
                status='unavailable'
            ),
        }),

        'chomp': Game(
            name='Chomp',
            desc='Players take turn eating chocolate',
            variants={
                '3x2': JSONGameVariant(os.path.join(dirname, 'solutions/chomp/3x2.json')),
                '4x7': JSONGameVariant(os.path.join(dirname, 'solutions/chomp/4x7.json')),
        }),
}
