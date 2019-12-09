## Adding Games for GamesmanClassic Games

#### I. Retrieving List of Games

List of games can be found [here](http://nyc.cs.berkeley.edu:8081/getGames).


List of already added games can be found [here](https://docs.google.com/spreadsheets/d/1-V9lE1N1Y-E-0Oi1uOnjEEdIwRwyy4cHzBKxb3h9MHw/edit?usp=sharing) (UC Berkeley log-in required).

#### II. Adding Games in games.py File

In games.py file, add games into the `games` dictionary as below:

```python
'ttt': Game(
    name='Tic-Tac-Toe',
    desc='Achieve three in a row horizontally, vertically, or diagonally',
    variants={
        'regular': GameVariant(
            name='Regular',
            desc='Regular',
            data_provider=GamesmanClassicDataProvider,
            data_provider_game_id='ttt',
            data_provider_variant_id=-1)
    })
```

- The key in the `games` dictionary for this entry is the abbreviated name as in the GamesmanClassic directory.
In the example above, 'ttt' is the key

- The instance variable  `name` should be the full name of the game ('Tic-Tac-Toe' in the example above).

- `desc` is a very brief description of the game. Information and details about the game can be retrieved
from the [GamesCrafters website](http://gamescrafters.berkeley.edu/games.php) or the c file in the GamesmanClassic repository.

- In the initial stage of adding games, can simply add the regular variant (user does not need to change anything other than the
`data_provider_game_id`)

#### III. Documenting the Game in Google Spreadsheet

Add the game information to the [spreadsheet](https://docs.google.com/spreadsheets/d/1-V9lE1N1Y-E-0Oi1uOnjEEdIwRwyy4cHzBKxb3h9MHw/edit?usp=sharing) (UC Berkeley log-in required).
In order to retrieve the starting position, go to http://nyc.cs.berkeley.edu:8081/sim/getStart (replace 'sim' with the abbreviated name of the game
you are adding). Copy and paste everything after `'response:'` and add a meaning to the starting position (which can be found either in the .c files in 
[GamesmanClassic repository](https://github.com/GamesCrafters/GamesmanClassic/tree/master/src) or the
[GamesCrafters Website](http://gamescrafters.berkeley.edu/games.php))

