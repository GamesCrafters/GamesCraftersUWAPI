from .models import Game, Variant
from .gamesman_classic import GamesmanClassic
from .gamesman_puzzles import GamesmanPuzzles
from .gamesman_one import GamesmanOne
from .chess import RegularChessVariant
from .tootandotto import TootAndOtto
from .nim import NimVariant, nim_custom_start
from .dawsonschess import DawsonsChessVariant, dawsonschess_custom_start
from .kayles import KaylesVariant, kayles_custom_start
from .chinesechess import RegularChineseChessVariant
from .Jenga import Jenga
from .EuclidsGame import EuclidsGame
from .Ghost import Ghost

"""
    All one-player (puzzle) games and two-player games should be 
    listed in the `games` dict.

    Note: All keys of the `games` dict (i.e., game ids) should
    only contain lowercase letters and numbers. No underscores,
    spaces, or uppercase letters.
"""

games = {
  
    '0to10by1or2': Game(
        name='0 to 10 by 1 or 2',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='1210',
                data_provider_variant_id=1,
                gui='v3')
        },
        gui='v3'),

    '1dchess': Game(
        name='1D Chess',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='1dchess',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'),
    
    '3spot': Game(
        name='3-Spot',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='3spot',
                data_provider_variant_id=690,
                gui='v3')
        },
        gui='v3'),
    
    'abalone': Game(
        name='Abalone',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='abalone',
                data_provider_variant_id=1)
        }
    ),
    
    'achi': Game(
        name='Achi',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='achi',
                data_provider_variant_id=2,
                gui='v3')
        },
        gui='v3'),
    
    'adugo': Game(
        name='Adugo',
        variants={
            '5x5': Variant(
                name='5x5',
                data_provider=GamesmanClassic,
                data_provider_game_id='adugo',
                data_provider_variant_id=1,
                gui='v2'),
        },
        gui='v2'),
    
    'allqueenschess': Game(
        name='All Queens Chess',
        variants={
            'standard': Variant(
                name='Standard',
                data_provider=GamesmanClassic,
                data_provider_game_id='allqueenschess',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'
    ),
    
    'baghchal': Game(
        name='Bagh-Chal',
        variants={
            'regular': Variant(
                name='Standard',
                data_provider=GamesmanClassic,
                data_provider_game_id='baghchal',
                data_provider_variant_id=5,
                gui='v3')
        },
        gui='v3'),

    'beeline': Game(
        name='Beeline',
        variants={
            'regular': Variant(
                name='Standard',
                data_provider=GamesmanClassic,
                data_provider_game_id='beeline',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'),

    'bishoppuzzle': Game(
        name='Bishop Puzzle',
        variants={
            v: Variant(
                name='Standard',
                data_provider=GamesmanPuzzles,
                data_provider_game_id='bishoppuzzle',
                data_provider_variant_id=v,
                gui='v3'
            ) for v in ('4x5_8', '4x7_4', '6x7_6')
        },
        is_two_player_game=False,
        gui='v3'
    ),
    
    'change': Game(
        name='Change!',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='change',
                data_provider_variant_id=3,
                gui='v3'
            )
        },
        gui='v3'),
    
    'chess': Game(
        name='Chess',
        variants={
            'endgame1': RegularChessVariant('K1k1B3/8/8/8/8/8/7N/8 w - - 0 1', name='Endgame 1'),
            'endgame2': RegularChessVariant('8/6R1/6k1/p2pB3/8/8/r7/6K1 b - - 0 1', name='Endgame 2'),
            'start': RegularChessVariant('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', name='Start')
        },
        gui='v2'),

    'chinesechess': Game(
        name='Chinese Chess',
        variants={
            'regular': RegularChineseChessVariant()
        },
        gui='v3'),
    
    'chomp': Game(
        name='Chomp',
        variants={
            '4x7': Variant(
                name='4 Rows, 7 Columns',
                data_provider=GamesmanClassic,
                data_provider_game_id='chomp',
                data_provider_variant_id=36,
                gui='v3'),
            '5x8': Variant(
                name='5 Rows, 8 Columns',
                data_provider=GamesmanClassic,
                data_provider_game_id='chomp',
                data_provider_variant_id=47,
                gui='v3'),
            '8x10': Variant(
                name='8 Rows, 10 Columns',
                data_provider=GamesmanClassic,
                data_provider_game_id='chomp',
                data_provider_variant_id=79,
                gui='v3')
        },
        gui='v3'),

    'chopsticks': Game(
        name='Chopsticks',
        variants={
            '0': Variant(
                name='[Standard] Neither pass-equivalent transfers nor full transfers allowed.',
                data_provider=GamesmanClassic,
                data_provider_game_id='chopsticks',
                data_provider_variant_id=0,
                gui='v3'),
            '1': Variant(
                name='Pass-equivalent transfers allowed. Full transfers not allowed.',
                data_provider=GamesmanClassic,
                data_provider_game_id='chopsticks',
                data_provider_variant_id=1,
                gui='v3'),
            '2': Variant(
                name='Pass-equivalent transfers not allowed. Full transfers allowed.',
                data_provider=GamesmanClassic,
                data_provider_game_id='chopsticks',
                data_provider_variant_id=2,
                gui='v3'),
            '3': Variant(
                name='Both pass-equivalent transfers and full transfers allowed.',
                data_provider=GamesmanClassic,
                data_provider_game_id='chopsticks',
                data_provider_variant_id=3,
                gui='v3'),
        },
        gui='v3'),
    
    'chungtoi': Game(
        name='Chung-Toi',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='ctoi',
                data_provider_variant_id=62,
                gui='v3')
        },
        gui='v3'),
    
    'connect4': Game(
        name='Connect 4',
        variants={
            '6x6': Variant(
                name='6x6',
                data_provider=GamesmanClassic,
                data_provider_game_id='connect4',
                data_provider_variant_id=1,
                gui='v3'),
            '6x7': Variant(
                name='6x7',
                data_provider=GamesmanClassic,
                data_provider_game_id='connect4',
                data_provider_variant_id=2,
                gui='v3')
        },
        gui='v3'),
    
    'dao': Game(
        name='Dao',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='dao',
                data_provider_variant_id=0,
                gui='v3'),
        },
        gui='v3'),
        
    'dawsonschess': Game(
        name='Dawson\'s Chess',
        variants={
            str(i): DawsonsChessVariant(i, str(i)) for i in range(5, 10)
        },
        custom_variant=dawsonschess_custom_start,
        gui='v3'),
    
    'dinododgem': Game(
        name='Dino Dodgem',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='dinododgem',
                data_provider_variant_id=151,
                gui='v3')
        },
        gui='v3'),
    
    'dodgem': Game(
        name='Dodgem',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='dodgem',
                data_provider_variant_id=2,
                gui='v3')
        },
        gui='v3'),

    'domineering': Game(
        name='Domineering',
        variants={
            '4': Variant(
                name='4x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='domineering',
                data_provider_variant_id=0,
                gui='v3'),
            '5': Variant(
                name='5x5',
                data_provider=GamesmanClassic,
                data_provider_game_id='domineering',
                data_provider_variant_id=1,
                gui='v3'),
            '6': Variant(
                name='6x6',
                data_provider=GamesmanClassic,
                data_provider_game_id='domineering',
                data_provider_variant_id=2,
                gui='v3')
        },
        gui='v3'),

    'dragonsandswans': Game(
        name='Dragons & Swans',
        variants={
            '1': Variant(
                name='1 Dragon',
                data_provider=GamesmanClassic,
                data_provider_game_id='swans',
                data_provider_variant_id=1,
                gui='v3'),
            '2': Variant(
                name='2 Dragons',
                data_provider=GamesmanClassic,
                data_provider_game_id='swans',
                data_provider_variant_id=5,
                gui='v3'),
            '3': Variant(
                name='3 Dragons',
                data_provider=GamesmanClassic,
                data_provider_game_id='swans',
                data_provider_variant_id=9,
                gui='v3'),
            '4': Variant(
                name='4 Dragons',
                data_provider=GamesmanClassic,
                data_provider_game_id='swans',
                data_provider_variant_id=13,
                gui='v3')
        },
        gui='v3'),
    
    'dshogi': Game(
        name='Dōbutsu shōgi',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanOne,
                data_provider_game_id='dshogi',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'),
    
    'euclidsgame': Game(
        name="Euclid's Game",
        variants={
            'regular': EuclidsGame()
        },
        gui='v2'),

    'fivefieldkono': Game(
        name='Five Field Kono',
        variants={
            'regular': Variant(
                name="Tie if you can't move",
                data_provider=GamesmanClassic,
                data_provider_game_id='fivefieldkono',
                data_provider_variant_id=0,
                gui='v3'),
            'delta': Variant(
                name="Lose if you can't move",
                data_provider=GamesmanClassic,
                data_provider_game_id='fivefieldkono',
                data_provider_variant_id=1,
                gui='v3'),
            'omega': Variant(
                name="Win if you can't move",
                data_provider=GamesmanClassic,
                data_provider_game_id='fivefieldkono',
                data_provider_variant_id=2,
                gui='v3')
        },
        gui='v3'),

    'fourfieldkono': Game(
        name='Four Field Kono',
        variants={
            'standard': Variant(
                name='Standard',
                data_provider=GamesmanClassic,
                data_provider_game_id='kono',
                data_provider_variant_id=1096,
                gui='v3')
        },
        gui='v3'),

    'forestfox': Game(
        name='Forest Fox',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='forestfox',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'),

    'foxandhounds': Game(
        name='Fox and Hounds',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='foxes',
                data_provider_variant_id=1,
                gui='v3')
        },
        gui='v3'),

    'ghost': Game(
        name='Ghost',
        variants = {
            str(c): Ghost(minimum_length = int(c)) for c in range(3, 7)
        },
        gui='v3'
    ),

    'graphgame': Game(
        name='Graph',
        variants={
            '0': Variant(
                name='10 to 0 by 1 or 2',
                data_provider=GamesmanClassic,
                data_provider_game_id='graphgame',
                data_provider_variant_id=1,
                gui='v3'),
            '1': Variant(
                name='Pure Draw Example',
                data_provider=GamesmanClassic,
                data_provider_game_id='graphgame',
                data_provider_variant_id=0,
                gui='v3'),
            '2': Variant(
                name='Various Primitives',
                data_provider=GamesmanClassic,
                data_provider_game_id='graphgame',
                data_provider_variant_id=2,
                gui='v3'),
        },
        gui='v3'),
    
    'towersofhanoi': Game(
        name="Towers of Hanoi",
        variants= {
            v: Variant(
                name=f"{v.split('_')[0]} Rod{'' if v.split('_')[0] == '1' else 's'} & {v.split('_')[1]} Disk{'' if v.split('_')[1] == '1' else 's'}",
                data_provider=GamesmanPuzzles,
                data_provider_game_id='towersofhanoi',
                data_provider_variant_id=v,
                gui='v3'
            ) for v in (f'{x}_{y}' for x in range(3, 5) for y in range(1, 9))
        },
        is_two_player_game=False,
        gui='v3'
    ),

    'hareandhounds': Game(
        name='Hare and Hounds',
        variants={
            's-hounds-first': Variant(
                name='Small, Hounds First',
                data_provider=GamesmanClassic,
                data_provider_game_id='haregame',
                data_provider_variant_id=1,
                gui='v3'),
            's-hare-first': Variant(
                name='Small, Hare First',
                data_provider=GamesmanClassic,
                data_provider_game_id='haregame',
                data_provider_variant_id=2,
                gui='v3'),
            'm-hounds-first': Variant(
                name='Medium, Hounds First',
                data_provider=GamesmanClassic,
                data_provider_game_id='haregame',
                data_provider_variant_id=3,
                gui='v3'),
            'm-hare-first': Variant(
                name='Medium, Hare First',
                data_provider=GamesmanClassic,
                data_provider_game_id='haregame',
                data_provider_variant_id=4,
                gui='v3'),
            'l-hounds-first': Variant(
                name='Large, Hounds First',
                data_provider=GamesmanClassic,
                data_provider_game_id='haregame',
                data_provider_variant_id=5,
                gui='v3'),
            'l-hare-first': Variant(
                name='Large, Hare First',
                data_provider=GamesmanClassic,
                data_provider_game_id='haregame',
                data_provider_variant_id=6,
                gui='v3')
        },
        gui='v3'),
    
    'hopndrop': Game(
        name="Hop N' Drop",
        variants= {
            "map1": Variant(
                name="Map 1",
                data_provider=GamesmanPuzzles,
                data_provider_game_id='hopndrop',
                data_provider_variant_id="map1",
                gui='v3'
            )
        },
        is_two_player_game=False
    ),

    'jan': Game(
        name="Jan",
        variants={
            '4x4': Variant(
                name='4x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='jan',
                data_provider_variant_id='1',
                gui='v3',
            ),
        },
        gui='v3',
    ),

    'jenga': Game(
        name='Jenga',
        variants={
            "regular" : Jenga()
        },
        gui='v3'),

    'joust': Game(
        name='Joust',
        variants={
            '4x4': Variant(
                name='4x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='joust',
                data_provider_variant_id=288751,
                gui='v3'),
            '5x4': Variant(
                name='5x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='joust',
                data_provider_variant_id=297501,
                gui='v3')
        },
        gui='v3'),
    
    'kayles': Game(
        name='Kayles',
        variants={
            str(i): KaylesVariant(i, str(i)) for i in range(5, 10)
        },
        custom_variant=kayles_custom_start,
        gui='v3'),

    'konane': Game(
        name='Kōnane',
        variants={
            '4x4': Variant(
                name='4x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='konane',
                data_provider_variant_id=0,
                gui='v3'),
            '4x5': Variant(
                name='4x5',
                data_provider=GamesmanClassic,
                data_provider_game_id='konane',
                data_provider_variant_id=1,
                gui='v3'),
            '5x5': Variant(
                name='5x5',
                data_provider=GamesmanClassic,
                data_provider_game_id='konane',
                data_provider_variant_id=2,
                gui='v3'),
            '5x6': Variant(
                name='5x6',
                data_provider=GamesmanClassic,
                data_provider_game_id='konane',
                data_provider_variant_id=3,
                gui='v3'),
        },
        gui='v3'),
    
    'lgame': Game(
        name='L-game',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='Lgame',
                data_provider_variant_id=2,
                gui='v3')
        },
        gui='v3'),

    'lewthwaitesgame': Game(
        name="Lewthwaite's Game",
        variants={
            'standard': Variant(
                name='Standard',
                data_provider=GamesmanClassic,
                data_provider_game_id='lewth',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'),
    
    'lightsout': Game(
        name='Lights Out',
        variants={
            v: Variant(
                name=f'{v}x{v}',
                data_provider=GamesmanPuzzles,
                data_provider_game_id='lightsout',
                data_provider_variant_id=v,
                gui='v3'
            ) for v in '2345678'
        },
        is_two_player_game=False,
        gui='v3'
    ),
    
    'lite3': Game(
        name='Lite 3',
        variants={
            'three-in-a-row': Variant(
                name='Three-In-A-Row Wins',
                data_provider=GamesmanClassic,
                data_provider_game_id='lite3',
                data_provider_variant_id=1,
                gui='v3'),
            'surround': Variant(
                name='Surround Wins',
                data_provider=GamesmanClassic,
                data_provider_game_id='lite3',
                data_provider_variant_id=2,
                gui='v3'),
            'both': Variant(
                name='Three-In-A-Row and Surround BOTH win',
                data_provider=GamesmanClassic,
                data_provider_game_id='lite3',
                data_provider_variant_id=3,
                gui='v3')
        },
        gui='v3'),
    
    'mancala': Game(
        name='Mancala',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='mancala',
                data_provider_variant_id=1)
        }
    ),
    
    'mutorere': Game(
        name='Mū Tōrere',
        variants={
            'regular': Variant(
                name='Standard',
                data_provider=GamesmanClassic,
                data_provider_game_id='tore',
                data_provider_variant_id=2,
                gui='v3'),
            'misere': Variant(
                name='Misere',
                data_provider=GamesmanClassic,
                data_provider_game_id='tore',
                data_provider_variant_id=1,
                gui='v3')
        },
        gui='v3'),
    
    'nim': Game(
        name='Nim',
        variants={
            s: NimVariant(p, s) for p, s in (
                ((2, 3, 5, 7), '2_3_5_7'),
                ((3, 3, 3), '3_3_3'),
                ((1, 2, 3, 4, 5), '1_2_3_4_5'),
                ((7, 8, 11, 13, 15), '7_8_11_13_15'),
                ((1, 3, 5, 7, 9, 10), '1_3_5_7_9_10')
            )
        },
        custom_variant=nim_custom_start,
        gui='v3'),
    
    'ninemensmorris': Game(
        name="Nine Men's Morris",
        variants={
            'regular': Variant(
                name="Nine Men's Morris",
                data_provider=GamesmanClassic,
                data_provider_game_id='369mm',
                data_provider_variant_id=12,
                gui='v3'
            ),
            '6mmNoFly': Variant(
                name="Six Men's Morris",
                data_provider=GamesmanClassic,
                data_provider_game_id='369mm',
                data_provider_variant_id=6,
                gui='v3'
            )
        },
        gui='v3'),

    'notakto': Game(
        name='Notakto',
        variants={
            'regular': Variant(
                name='1 Board',
                data_provider=GamesmanClassic,
                data_provider_game_id='notakto',
                data_provider_variant_id=0,
                gui='v3'),
            'board2': Variant(
                name='2 Boards',
                data_provider=GamesmanClassic,
                data_provider_game_id='notakto',
                data_provider_variant_id=1,
                gui='v3'),
            'board3': Variant(
                name='3 Boards',
                data_provider=GamesmanClassic,
                data_provider_game_id='notakto',
                data_provider_variant_id=2,
                gui='v3')
        },
        gui='v3'),
    
    'npuzzle': Game(
        name='Sliding Number Puzzle',
        variants={
            '3': Variant(
                name='8-Puzzle',
                data_provider=GamesmanPuzzles,
                data_provider_game_id='npuzzle',
                data_provider_variant_id='3',
                gui='v3')
        },
        is_two_player_game=False,
        gui='v3'
    ),

    'nqueens': Game(
        name='N Queens Puzzle',
        variants={
            v: Variant(
                name=f'{v} Boards',
                data_provider=GamesmanPuzzles,
                data_provider_game_id='nqueens',
                data_provider_variant_id=v,
                gui='v3'
            ) for v in '4567879'
        },
        is_two_player_game=False,
        gui='v3'
    ),

    'nutictactoe': Game(
        name='Nu Tic-Tac-Toe',
        variants={
            'regular': Variant(
                name='5x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='nuttt',
                data_provider_variant_id=1740,
                gui='v3')
        },
        gui='v3'),

    'oddoreven': Game(
        name='Odd or Even',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='ooe',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'
    ),
    
    'othello': Game(
        name='Othello',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='othello',
                data_provider_variant_id=136,
                gui='v3')
        },
        gui='v3',
        supports_win_by=True
    ),
    
    'pegsolitaire': Game(
        name='Peg Solitaire',
        variants= {
            v: Variant(
                name=v.title(),
                data_provider=GamesmanPuzzles,
                data_provider_game_id='pegsolitaire',
                data_provider_variant_id=v,
                gui='v3'
            ) for v in ('triangle', 'star', 'trapezoid')
        },
        is_two_player_game=False,
        gui='v3'
    ),

    'ponghauki': Game(
        name="Pong Hau K'i",
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='horse',
                data_provider_variant_id=1,
                gui='v3'),
        },
        gui='v3'),
    
    'quarto': Game(
        name='Quarto',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='quarto',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'),
    
    'quickchess': Game(
        name='Quick Chess',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='quickchess',
                data_provider_variant_id=1,
                gui='v3')
        },
        gui='v3'),

    'quickcross': Game(   
       name='Quick Cross',
       variants={
           'regular': Variant(
               name='Regular',
               data_provider=GamesmanClassic,
               data_provider_game_id='qx',
               data_provider_variant_id=9,
               gui='v3',
            ),
       }, 
       gui='v3'),

    'quixo' : Game(
        name = 'Quixo' ,
        variants={
            '5x5': Variant(
                name = '5x5',
                data_provider=GamesmanOne,
                data_provider_game_id = 'quixo' ,
                data_provider_variant_id = '0' ,
                gui = 'v3',
            ),
            '4x4': Variant(
                name = '4x4',
                data_provider=GamesmanOne,
                data_provider_game_id = 'quixo' ,
                data_provider_variant_id = '1' ,
                gui = 'v3',
            ),
            '3x3': Variant(
                name = '3x3',
                data_provider=GamesmanOne,
                data_provider_game_id = 'quixo' ,
                data_provider_variant_id = '2' ,
                gui = 'v3',
            ),
        },
    gui = 'v3'),
    
    'rubikscube': Game(
        name="Rubik's Cube",
        variants={
            '2x2x2': Variant(
                name='2x2x2',
                data_provider=GamesmanPuzzles,
                data_provider_game_id='rubikscube',
                data_provider_variant_id='2x2x2',
                gui='v2'
            )
        },
        is_two_player_game=False,
        gui='v2'
    ),

    'rubiksmagic': Game(
        name="Rubik's Magic",
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='rubiksmagic',
                data_provider_variant_id=0,
                gui='v3')
            },
        gui='v3'),
    
    'rushhour': Game(
        name="Rush Hour",
        variants={
            v: Variant(
                name=v.title(),
                data_provider=GamesmanPuzzles,
                data_provider_game_id='rushhour',
                data_provider_variant_id=v,
                gui='v3'
            ) for v in ('basic', 'easy', 'medium', 'hard', 'expert')
        },
        is_two_player_game=False,
        gui='v3'
    ),

    'sim': Game(
        name='Sim',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='sim',
                data_provider_variant_id=1,
                gui='v3')
        },
        gui='v3'),
    
    'shifttactoe': Game(
        name='Shift Tac Toe',
        variants={
            'default': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='stt',
                data_provider_variant_id=2,
                gui='v2')
        },
        gui='v2'),
    
    'slide5': Game(
        name="Slide-5",
        variants={
            'regular': Variant(
                name="[Standard] Creating a 5-in-a-Row for both players counts as a win for the player who did so.",
                data_provider=GamesmanClassic,
                data_provider_game_id='slide5',
                data_provider_variant_id=0,
                gui='v3'
            ),
            'ties': Variant(
                name="Creating a 5-in-a-Row for both players results in the game ending in a tie.",
                data_provider=GamesmanClassic,
                data_provider_game_id='slide5',
                data_provider_variant_id=1,
                gui='v3'
            )
        },
        gui='v3'),

    'snake': Game(
        name='Snake',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='snake',
                data_provider_variant_id=1,
                gui='v3')
            },
        gui='v3'),

    'squaredance': Game(
        name='Square Dance',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='squaredance',
                data_provider_variant_id=7,
                gui='v3')
            },
        gui='v3'),
    
    'tactix': Game(
        name='TacTix',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='tactix',
                data_provider_variant_id=1,
                gui='v3')
            },
        gui='v3'
        ),

    'teeko' : Game(
        name = 'Teeko' ,
        variants={
            'standard': Variant(
                name = 'Standard',
                data_provider=GamesmanOne,
                data_provider_game_id = 'teeko',
                data_provider_variant_id = '0',
                gui = 'v3',
            ),
            'advanced': Variant(
                name = 'Advanced',
                data_provider=GamesmanOne,
                data_provider_game_id = 'teeko',
                data_provider_variant_id = '1',
                gui = 'v3',
            ),
        },
    gui = 'v3'),
    
    'tictactoe': Game(
        name='Tic-Tac-Toe',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='ttt',
                data_provider_variant_id=3,
                gui='v3'),
            'misere': Variant(
                name='Misere',
                data_provider=GamesmanClassic,
                data_provider_game_id='ttt',
                data_provider_variant_id=1,
                gui='v3')
        },
        gui='v3'),

    'tictactwo': Game(
        name='Tic-Tac-Two',
        variants={
            'regular': Variant(
                name='Regular',
                data_provider=GamesmanClassic,
                data_provider_game_id='tttwo',
                data_provider_variant_id=0,
                gui='v3')
        },
        gui='v3'),
    
    'toadsandfrogspuzzle': Game(
        name='Toads and Frogs Puzzle',
        variants={
            str(v): Variant(
                name=f'{v >> 1} Frogs, {v >> 1} Toads',
                data_provider=GamesmanPuzzles,
                data_provider_game_id='toadsandfrogspuzzle',
                data_provider_variant_id=str(v),
                gui='v3'
            ) for v in (4, 6, 8, 10)
        },
        is_two_player_game=False,
        gui='v3'
    ),
    
    'tootandotto': Game(
        name='Toot and Otto',
        variants={
            '4': TootAndOtto(4),
            '5': TootAndOtto(5),
            '6': TootAndOtto(6)
        },
        gui='v3'),
    
    'topitop': Game(
        name="Topitop",
        variants={
            'regular':  Variant(
                name="Standard Topitop",
                data_provider=GamesmanClassic,
                data_provider_game_id='topitop',
                data_provider_variant_id=0,
                gui='v3'
            )
        },
        gui='v3'),
    
    'topspin': Game(
        name="Top Spin",
        variants= {
            "6_2": Variant(
                name="6 Disks",
                data_provider=GamesmanPuzzles,
                data_provider_game_id='topspin',
                data_provider_variant_id="6_2",
                gui='v3'
            )
        },
        is_two_player_game=False
    ),
    
    'y': Game(
        name='Y',
        variants={
            'dim4': Variant(
                name='Dimension 4',
                data_provider=GamesmanClassic,
                data_provider_game_id='gameofy',
                data_provider_variant_id=0,
                gui='v3'),
            'dim5': Variant(
                name='Dimension 5',
                data_provider=GamesmanClassic,
                data_provider_game_id='gameofy',
                data_provider_variant_id=1,
                gui='v3'),
            'dim4-misere': Variant(
                name='Dimension 4 Misère',
                data_provider=GamesmanClassic,
                data_provider_game_id='gameofy',
                data_provider_variant_id=4,
                gui='v3'),
            'dim5-misere': Variant(
                name='Dimension 5 Misère',
                data_provider=GamesmanClassic,
                data_provider_game_id='gameofy',
                data_provider_variant_id=5,
                gui='v3'),
        },
        gui='v3'),

    'yote': Game(
        name='Yoté',
        variants={
            '3x3': Variant(
                name='3x3',
                data_provider=GamesmanClassic,
                data_provider_game_id='yote',
                data_provider_variant_id=0,
                gui='v2'),
            '3x4': Variant(
                name='3x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='yote',
                data_provider_variant_id=1,
                gui='v2'),
            '4x4': Variant(
                name='4x4',
                data_provider=GamesmanClassic,
                data_provider_game_id='yote',
                data_provider_variant_id=2,
                gui='v2'),
        },
        gui='v2')
}
