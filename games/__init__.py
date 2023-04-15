import os

from .models import Game, GameVariant
from .gamesman_classic import GamesmanClassicDataProvider
from .gamesman_java import GamesmanJavaDataProvider, GamesmanJavaConnect4GameVariant
from .json_game_variant import JSONGameVariant
from .chess import RegularChessVariant
from .TicTacToe3x3x2GameVariant import TicTacToe3x3x2GameVariant
from .TootNOtto import TootNOtto
from .NimGameVariant import NimGameVariant, nim_custom_start
from .DawsonsChessGameVariant import DawsonsChessGameVariant, dawsonschess_custom_start
from .KaylesGameVariant import KaylesGameVariant, kayles_custom_start
from .chinesechess import RegularChineseChessVariant

dirname = os.path.dirname(__file__)

games = {
    

   'quickcross': Game(   
       name='Quick Cross',
       desc="Place your piece (vertically/horizontally) onto an open square (looks like a + sign) or rotate an existing piece. " +
       "Wins when you connect 4 in a row horizontally, vertically, or diagonally.",
       variants={
           'regular': GameVariant(
               name='Regular',
               desc='Regular',
               data_provider=GamesmanClassicDataProvider,
               data_provider_game_id='qx',
               data_provider_variant_id=9,
               gui_status='v2',
               status='stable'),
       }, 
       gui_status='v2'),
  

    
    '0to10by1or2': Game(
        name='0 to 10 by 1 or 2',
        desc="A player may either place 1 or 2 pieces on their turn. Wins when player reaches 10.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='1210',
                data_provider_variant_id=-1,
                status='dev',
                gui_status='v0')
        },
        gui_status='v0'),

    '1dchess': Game(
        name='1D Chess',
        desc="A miniature version of chess played on a single line.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='1dchess',
                data_provider_variant_id=0,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'ttt3d': Game(
        name='3D Tic-Tac-Toe',
        desc='3D Tic-Tac-Toe',
        variants={
            '3x3x2': TicTacToe3x3x2GameVariant(
                name='3x3x2',
                desc='3x3x2',
                filepath=os.path.join(dirname, 'solutions/ttt3d/3x3x2.txt'),
                status='dev',
                gui_status='v0')
        },
        gui_status='v0'),
    
    '3spot': Game(
        name='3-Spot',
        desc="4x4 board. Each player has a 3×2 L-shaped piece, and there are two 1×1 neutral pieces. During a player's turn, player must move his/her piece such that the piece must stay on the board and must cover at least one new square. Afterwards, the same player must move the neutral piece to a new position as well. Wins when you score 12 points when your opponent has scored at least 6.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='3spot',
                data_provider_variant_id=-1,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
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
                status='dev',
                gui_status='v0')
        },
        gui_status='v0'),
    
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
                status='stable',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'baghchal': Game(
        name='Bagh-Chal',
        desc="In the first phase the goats are placed on the board while the tigers are moved. In the second phase both the goats and the tigers are moved. For the tigers, the objective is to 'capture' five goats to win. Capturing is performed as in alquerque and draughts, by jumping over the goats, although capturing is not obligatory. The goats win by blocking all the tigers' legal moves.",
        variants={
            'regular': GameVariant(
                name='Standard',
                desc='Standard',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='baghchal',
                data_provider_variant_id=5,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),

    'beeline': Game(
        name='Beeline',
        desc="Trap your opponents bees.",
        variants={
            'regular': GameVariant(
                name='Standard',
                desc='Standard',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='beeline',
                data_provider_variant_id=0,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'chess': Game(
        name='Chess',
        desc="Chess",
        variants={
            '7-man': RegularChessVariant()
        },
        gui_status='v2'),

    'chinesechess': Game(
        name='Chinese Chess',
        desc="Checkmate the enemy general to win the battle.",
        variants={
            'regular': RegularChineseChessVariant()
        },
        gui_status='v2'),
    
    'chomp': Game(
        name='Chomp',
        desc='Players take turn eating chocolate',
        variants={
            '3x2': JSONGameVariant(os.path.join(dirname, 'solutions/chomp/3x2.json'), gui_status='v2'),
            '4x7': JSONGameVariant(os.path.join(dirname, 'solutions/chomp/4x7.json'), gui_status='v2'),
        },
        gui_status='v2'),
    
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
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'connect4c': Game(
        name='Connect 4',
        desc="4-in-a-row with gravity.",
        variants={
            '6x6': GameVariant(
                name='6x6',
                desc='6x6',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=1,
                status='dev',
                gui_status='v2'),
            '6x7': GameVariant(
                name='6x7',
                desc='6x7',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='connect4',
                data_provider_variant_id=2,
                status='dev',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'connect4': Game(
        name='Connect 4 (Java)',
        desc='Tic Tac Toe with gravity',
        variants={
            '4x4x4': GamesmanJavaConnect4GameVariant(
                width=4,
                height=4,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '4x5x4': GamesmanJavaConnect4GameVariant(
                width=4,
                height=5,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '4x6x4': GamesmanJavaConnect4GameVariant(
                width=4,
                height=6,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '5x4x4': GamesmanJavaConnect4GameVariant(
                width=5,
                height=4,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '5x5x4': GamesmanJavaConnect4GameVariant(
                width=5,
                height=5,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '5x6x4': GamesmanJavaConnect4GameVariant(
                width=5,
                height=6,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '6x4x4': GamesmanJavaConnect4GameVariant(
                width=6,
                height=4,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '6x5x4': GamesmanJavaConnect4GameVariant(
                width=6,
                height=5,
                pieces=4,
                status='dev',
                gui_status='v1'
            ),
            '6x6x4': GamesmanJavaConnect4GameVariant(
                width=6,
                height=6,
                pieces=4,
                status='unavailable',
                gui_status='v0'
            ),
            '7x4x4': GamesmanJavaConnect4GameVariant(
                width=7,
                height=4,
                pieces=4,
                status='dev',
                gui_status='v0'
            ),
            '7x5x4': GamesmanJavaConnect4GameVariant(
                width=7,
                height=5,
                pieces=4,
                status='dev',
                gui_status='v0'
            ),
            '7x6x4': GamesmanJavaConnect4GameVariant(
                width=7,
                height=6,
                pieces=4,
                status='unavailable',
                gui_status='v0'
            ),
        },
        gui_status='v1'),
    
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
                status='dev',
                gui_status='v1')
        },
        gui_status='v1'),
        
    'dawsonschess': Game(
        name='Dawson\'s Chess',
        desc='Players take turns blocking out spaces on the board.',
        variants={},
        custom_variant=dawsonschess_custom_start,
        gui_status='v2'),
    
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
                status='dev',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'dodgem': Game(
        name='Dodgem',
        desc="Players alternate moving pieces, and the goal is to move your pieces off the board in the designated locations.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='dodgem',
                data_provider_variant_id=-1,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),

    'gameofy': Game(
        name='Game of Y',
        desc="Place your piece onto an open space. Wins when you connect three in a row horizontally, vertically, or diagonally.",
        variants={
            'dim4': GameVariant(
                name='Dimension 4',
                desc='Dimension 4',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='gameofy',
                data_provider_variant_id=0,
                status='stable',
                gui_status='v2'),
            'dim5': GameVariant(
                name='Dimension 5',
                desc='Dimension 5',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='gameofy',
                data_provider_variant_id=1,
                status='stable',
                gui_status='v2'),
            'dim4-misere': GameVariant(
                name='Dimension 4 Misère',
                desc='Dimension 4 Misère',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='gameofy',
                data_provider_variant_id=4,
                status='stable',
                gui_status='v2'),
            'dim5-misere': GameVariant(
                name='Dimension 5 Misère',
                desc='Dimension 5 Misère',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='gameofy',
                data_provider_variant_id=5,
                status='stable',
                gui_status='v2'),
        },
        gui_status='v2'),

    'haregame': Game(
        name='Hare and Hounds',
        desc="One player controls the three hounds. The other player controls the hare. The hound player can move one of the three hounds to an empty spot each turn with the restriction of no backward moves. The hare player can move the hare to any adjacent empty spot. The hare wins by reaching the left-most cell. The hounds win if the hare is unable to move on their turn.",
        variants={
            's-hounds-first': GameVariant(
                name='Small, Hounds First',
                desc='Small, Hounds First',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='haregame',
                data_provider_variant_id=1,
                status='stable',
                gui_status='v2'),
            's-hare-first': GameVariant(
                name='Small, Hare First',
                desc='Small, Hare First',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='haregame',
                data_provider_variant_id=2,
                status='stable',
                gui_status='v2'),
            'm-hounds-first': GameVariant(
                name='Medium, Hounds First',
                desc='Medium, Hounds First',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='haregame',
                data_provider_variant_id=3,
                status='stable',
                gui_status='v2'),
            'm-hare-first': GameVariant(
                name='Medium, Hare First',
                desc='Medium, Hare First',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='haregame',
                data_provider_variant_id=4,
                status='stable',
                gui_status='v2'),
            'l-hounds-first': GameVariant(
                name='Large, Hounds First',
                desc='Large, Hounds First',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='haregame',
                data_provider_variant_id=5,
                status='stable',
                gui_status='v2'),
            'l-hare-first': GameVariant(
                name='Large, Hare First',
                desc='Large, Hare First',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='haregame',
                data_provider_variant_id=6,
                status='stable',
                gui_status='v2')
        },
        gui_status='v2'),
    
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
                status='dev',
                gui_status='v1'),
            '2': GameVariant(
                name='2 Dragons',
                desc='2 Dragons',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=5,
                status='dev',
                gui_status='v1'),
            '3': GameVariant(
                name='3 Dragons',
                desc='3 Dragons',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=9,
                status='dev',
                gui_status='v1'),
            '4': GameVariant(
                name='4 Dragons',
                desc='4 Dragons',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='swans',
                data_provider_variant_id=13,
                status='dev',
                gui_status='v1')
        },
        gui_status='v1'),
    
    'kayles': Game(
        name='Kayles',
        desc='Players take turns blocking out one or two adjacent spaces on the board.',
        variants={},
        custom_variant=kayles_custom_start,
        gui_status='v1'),
    
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
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'lite3': Game(
        name='Lite 3',
        desc="Place your piece onto an open square. When the piece of any side comes to 3, the least recently placed piece of that side will disappear as that side placing new piece. Wins when you connect three in a row horizontally, vertically, or diagonally.",
        variants={
            'three-in-a-row': GameVariant(
                name='Three-in-a-row',
                desc='Three-In-A-Row Wins',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='lite3',
                data_provider_variant_id=1,
                status='stable',
                gui_status='v2'),
            'surround': GameVariant(
                name='Surround',
                desc='Surround Wins',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='lite3',
                data_provider_variant_id=2,
                status='stable',
                gui_status='v2'),
            'both': GameVariant(
                name='Both',
                desc='Three-In-A-Row and Surround BOTH win',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='lite3',
                data_provider_variant_id=3,
                status='stable',
                gui_status='v2')
        },
        gui_status='v2'),
    
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
                status='dev',
                gui_status='v0')
        },
        gui_status='v0'),
    
    'mutorere': Game(
        name='Mu Torere',
        desc='Mu Torere',
        variants={
            'regular': GameVariant(
                name='Standard',
                desc='Standard',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='tore',
                data_provider_variant_id=2,
                status='available',
                gui_status='v2'),
            'misere': GameVariant(
                name='Misere',
                desc='Misere',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='tore',
                data_provider_variant_id=1,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'nim': Game(
        name='Nim',
        desc='Players take turns taking sticks from a pile',
        variants={
            '3_3_3': JSONGameVariant(os.path.join(dirname, 'solutions/nim/3_3_3.json'), gui_status='v1'),
        },
        custom_variant=nim_custom_start,
        gui_status='v1'),

    'notakto': Game(
        name='NoTakTo',
        desc='TicTacToe on N boards with only X being placed',
        variants={
            'regular': GameVariant(
                name='1 Board',
                desc='1 Board',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='notakto',
                data_provider_variant_id=0,
                status='available',
                gui_status='v2'),
            'board2': GameVariant(
                name='2 Boards',
                desc='2 Boards',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='notakto',
                data_provider_variant_id=1,
                status='available',
                gui_status='v2'),
            'board3': GameVariant(
                name='3 Boards',
                desc='3 Boards',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='notakto',
                data_provider_variant_id=2,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
    '369mm': Game(
        name="Nine Men's Morris",
        desc="Players first alternate placing pieces onto empty nodes on the board. Once all pieces have been placed, players take turns sliding their pieces to other empty nodes connected to it by a line. If a player's move completes a 'mill', three in a line, then that player gets removes one of the opponent's pieces from the board that is currently not in a mill. A mill may be broken and reformed. When a player is down to 3 pieces, that player may move his or her piece to any empty node on the board.",
        variants={
            'regular':  GameVariant(
                name="Standard 9 Men's Morris",
                desc="Standard",
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='369mm',
                data_provider_variant_id=12,
                status='available',
                gui_status='v2'
            ),
            '6mmNoFly':  GameVariant(
                name="Standard 6 Men's Morris",
                desc="6mmNoFly",
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='369mm',
                data_provider_variant_id=6,
                status='available',
                gui_status='v1'
            )
        },
        gui_status='v2'),
    
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
                status='dev',
                gui_status='v0')
        },
        gui_status='v0'),
    
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
                status='stable',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'quarto': Game(
        name='Quarto',
        desc='Make a four-in-a-row of pieces with common attributes.',
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='quarto',
                data_provider_variant_id=-1,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
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
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
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
                status='dev',
                gui_status='v0')
        },
        gui_status='v0'),
    
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
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
    
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
                status='available',
                gui_status='v2')
            },
        gui_status='v2'),
    
    'tactix': Game(
        name='Tac Tix',
        desc="2D Nim",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Regular',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='tactix',
                data_provider_variant_id=1,
                status='available',
                gui_status='v2')
            },
        gui_status='v2'
        ),
    
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
                status='stable',
                gui_status='v2'),
            'misere': GameVariant(
                name='Misere',
                desc='Misere',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='ttt',
                data_provider_variant_id=1,
                status='stable',
                gui_status='v2')
        },
        gui_status='v2'),

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
                status='stable',
                gui_status='v2')
        },
        gui_status='v2'),
    
    'tootnottopy': Game(
        name='Toot-N-Otto',
        desc='Toot-N-Otto, get 4-in-a-row of TOOT (player 1) or OTTO (player 2) first',
        variants={
            '4': TootNOtto(4),
            '5': TootNOtto(5),
            '6': TootNOtto(6)
        },
        gui_status='v2'),
    
    'topitop': Game(
        name="Topitop",
        desc="Building sandcastles has never been so much fun.",
        variants={
            'regular':  GameVariant(
                name="Standard Topitop",
                desc="Regular",
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='topitop',
                data_provider_variant_id=-1,
                status='available',
                gui_status='v2'
            )
        },
        gui_status='v2'),
    
    'fivefieldkono': Game(
        name='Five Field Kono',
        desc="Largest game in GamesmanUni that can't be separated into tiers.",
        variants={
            'regular': GameVariant(
                name='Regular',
                desc='Stalemate=Tie',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='fivefieldkono',
                data_provider_variant_id=0,
                status='available',
                gui_status='v2'),
            'delta': GameVariant(
                name='Delta',
                desc='Stalemate=Lose',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='fivefieldkono',
                data_provider_variant_id=1,
                status='available',
                gui_status='v2'),
            'omega': GameVariant(
                name='Omega',
                desc='Stalemate=Win',
                data_provider=GamesmanClassicDataProvider,
                data_provider_game_id='fivefieldkono',
                data_provider_variant_id=2,
                status='available',
                gui_status='v2')
        },
        gui_status='v2'),
}
