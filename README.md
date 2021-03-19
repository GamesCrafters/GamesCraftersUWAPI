# GamesCrafters Universal Web API

This is the back end team code for the internal request-routing server framework for requests to the GamesCrafters website from the Universal Web API implemented this semester by the front end team.

### UWAPI backend link
https://nyc.cs.berkeley.edu/universal/v1/games

## Run the server locally
To run the server on your local machine, first clone this repository and run these following commands.
```
git clone https://github.com/GamesCrafters/GamesCraftersUWAPI.git
pip install -r requirements.txt
python server.py
```
These commands have been found to work on Python 3.6, 3.7, and 3.8.

## games folder
The games folder has four essential files and each has its own purpose.

\_\_init__.py: Initializes all the games with their gameinfo that have been added to the universal web API. It forms the games dict, indexed by the name of the game, and each game containing the name, description, and the details of each game variant.

gamesman_classic.py: Implements the GamesmanClassicDataProvider based on the abstract DataProvider class. 

models.py: Creates abstract model classes for Game, AbstractGameVariant, GameVariant, and DataProviderthat have been added to the web API 

chess.py: Implementation of chess for visualization in universal web API
Note: This is a separate project from the server code itself. 

## server.py
This file holds the code for the request-routing implementation within the server from Universal Web API. It uses Flask for routing requests by link, and each route corresponds to specific functions that handles that request. The functions in this file use the definitions in the games folder.
This file sets up the server and runs it from the given port in main.

Routes:
- "/games" : 
    - Calls handle_games()
    - Returns dictionary of all games available, gameId and name

- "/games/<game_id>" : 

    - Calls handle_game(game_id)
    - Finds game if exists and returns gameId, name, and all variants with corresponding variant info 

- "/games/<game_id>/variants/<variant_id>/positions/<position>" : 

    - Calls handle_position(game_id, variant_id, position)
    - Finds game and variant if exists. Gets response of current position value from GamesCrafters website (with 'board', 'value', and remoteness), renames 'board' and 'value' fields to 'position' and 'positionValue', adds a new field 'moves' containing next wrangled moves (sorted), and returns modified response
    
- "/games/<game_id>/variants/<variant_id>/positions/<position>/move"

    - Calls handle_position_moves(game_id, variant_id, position)
    - Similar to handle_position (above) but only returns "moves" field of the response
    
- "/internal/classic-games"

    - Calls handle_classic_games()
    - Gets json dictionary of all games (not fully implemented. List is present, but no data)
