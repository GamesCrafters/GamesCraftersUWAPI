# GamesCrafters Universal Web API

GamesCraftersUWAPI (Gamescrafters Universal Web API) is a middleware that connects Gamesman frontend applications (e.g, GamesmanUni) to different backend game servers (e.g., GamesmanClassic, GamesmanPuzzles, Lichess Database (the Lichess Database is not a GamesCrafters Project)). It also contains Python scripts to generate response JSON for certain games directly without the need to send requests to other servers.

## Run the server locally
To clone this repo and run the server on your local machine, run the following commands.
```
git clone https://github.com/GamesCrafters/GamesCraftersUWAPI.git
cd GamesCraftersUWAPI
pip install -r requirements.txt
python server.py
```

## server.py
`server.py` holds the code for the request-routing implementation within the server from Universal Web API. It uses Flask for routing requests by link, and each route corresponds to specific functions that handles that request. The functions in this file use the definitions in the games folder.
This file sets up the server and runs it from the given port in main.

### Routes:

- `/` : 
    - Returns a list of all one-player (puzzle) games and two-player games available. This is used, for example, by GamesmanUni in order to load the list of games in the "Games" page and the list of puzzles in the "Puzzles" page.
    
      Each listed game object contains four fields:
        - `id`: (String) The ID of the game, which is used to specify a game in the other routes.
        - `name`: (String) The human-readable name of the game.
        - `type`: (String) Whether the game is one-player or two-player.
        - `gui`: (String) Used to indicate which GUI category the game should be listed under in the "Games" or "Puzzles" page. It is one of "v0" (bronze, no GUI), "v1" (silver, character AutoGUI), "v2" (gold, Image AutoGUI, not animated), and "v3" (purple, Animated Image AutoGUI).

      Below is the response for `/`, with many game objects omitted for brevity.

      ```json
      [
          "...",

          {"gui": "v3", "id": "npuzzle", "name": "Sliding Number Puzzle", "type": "onePlayer"},
          {"gui": "v3", "id": "snake", "name": "Snake", "type": "twoPlayer"},
          {"gui": "v3", "id": "squaredance", "name": "Square Dance", "type": "twoPlayer"},
          {"gui": "v3", "id": "tactix", "name": "TacTix", "type": "twoPlayer"},
          {"gui": "v3", "id": "tictactoe", "name": "Tic-Tac-Toe", "type": "twoPlayer"},

          "..."
      ]
        ```

- `/health/` : 
    - Returns the current health and status of the UWAPI middleware and its dependant backend services.
    
      UWAPI health fields:
        - `status`: (String) Always `"ok"`. Indicates that UWAPI is online.
        - `http_code`: (Integer) Always HTTP `200`. Indicates that UWAPI is online.
        - `timestamp`: (Integer) ISO 8601 UTC timestamp of when the health response was made (e.g., `"2025-05-16T20:25:55Z"`).
        - `uptime`: (String) Time UWAPI has been running in `Xd Yh Zm Ws` format.
        - `cpu_usage`: (String) The percentage of CPU currently being used by the UWAPI (e.g., `"21.2%"`).
        - `memory_usage`: (String) The percentage of total system memory currently used by UWAPI (e.g., `"10.1%"`).
        - `process_count`: (String) Number of processes currently running on the system.
        - `backend_services`: (Object) An object describing the status of each backend service UWAPI depends on.

        For each available backend service the following health fields are appended `backend_services`:
        - `status`: (String) `"ok"` if the service responded successfully; `"fail"` if it did not respond or returned an error.
         - `http_code`: (Integer) Service healthcheck response HTTP code.
        - `latency`: (Integer) Present only if the healthcheck succeeded. Round-trip latency in milliseconds to reach the service.

      Below is an example response from `/health/`:

      ```json
      {
        "backend_services": {
          "gamesmanclassic": {
            "http_code": 200,
            "latency_ms": 109,
            "status": "ok"
          },
          "gamesmanone": {
            "status": "fail"
          },
          "gamesmanpuzzles": {
            "http_code": 200,
            "latency_ms": 40,
            "status": "ok"
          }
        },
        "cpu_usage": "6.1%",
        "memory_usage": "58.5%",
        "process_count": 887,
        "status": "ok",
        "timestamp": "2025-05-16T20:47:47Z",
        "uptime": "0d 0h 0m 1s"
      }
      ```

- `/<game_id>/` : 

    - Returns general information about the game specified by `game_id`. This is used, for example, by GamesmanUni when a game is clicked in order to see which variants are available in order to render the list of available variants.

      The response contains the following fields:
        - `id`: (String) The game ID, i.e., whatever `game_id` was.
        - `allowCustomVariantCreation`: (Boolean) Indicates whether the user on GamesmanUni can play a custom variant outside the default list of variants. For example, for Dawson's Chess, `allowCustomVariantCreation` is `true` because the user can specify an arbitrary board length to play with.
        - `name`: (String), The human-readable name of the game.
        - `supportsWinBy`: (Boolean) Whether win-by information will be returned when requesting any position from any variant of this game.
        - `variants`: (Array) Return a list of variant objects, which each contains three fields:
            - `id`: (String) The ID of the variant, which is used to specify a variant in other routes.
            - `name`: (String) The human-readable name of the variant.
            - `gui`: (String) Used to indicate which GUI category the variant should be listed under in the Variants page of the game. It is one of "v0" (bronze, no GUI), "v1" (silver, character AutoGUI), "v2" (gold, Image AutoGUI, not animated), and "v3" (purple, Animated Image AutoGUI).
      
      Below is the response for Mū Tōrere (`/mutorere/`).

      ```json
      {
          "id": "mutorere",
          "name": "M\u016b T\u014drere",
          "allowCustomVariantCreation": false,
          "supportsWinBy": false,
          "variants": [
              {"gui": "v3", "id": "regular", "name": "Standard"},
              {"gui": "v3", "id": "misere", "name": "Misere"}
          ]
      }
      ```

- `/<game_id>/<variant_id>/` : 
    - Returns information about the variant specified by `variant_id` of the game specified by `game_id`. This is used, for example, by GamesmanUni when a game is clicked in order to see which variants of the game are available in order to render the list of available variants.

      The response contains the following fields:
        - `id`: (String) The ID of the variant, i.e., whatever `variant_id` was.
        - `name`: (String) The human-readable name of this variant.
        - `gui`: (String) Used to indicate which GUI category this variant should be listed under in the Variants page of the game. It is one of "v0" (bronze, no GUI), "v1" (silver, character AutoGUI), "v2" (gold, Image AutoGUI, not animated), and "v3" (purple, Animated Image AutoGUI).
        - `startPosition`: (String) The human-readable string representation of the starting position.
        - `autoguiPosition`: (String) The AutoGUI-formatted string for the starting position, which tells the frontend application how to render the starting position.
        - `imageAutoGUIData`: (Object) JSON data that GamesmanUni uses when rendering each position of this game variant. See `games/image_autogui_data.py` for more information.

      Below is the response for the Regular variant of Mū Tōrere (`/mutorere/regular/`), with the Image AutoGUI data object omitted for brevity.

      ```json
      {
          "id": "regular",
          "name": "Standard",
          "gui": "v3",
          "startPosition": "1_-ooooxxxx",
          "autoguiStartPosition": "1_-ooooxxxx",
          "imageAutoGUIData": { "..." }
      }
      ```

- `/<game_id>/<variant_id>/positions/?p=<position_string>` : 

    - Returns information about the position specified by `position_string` of the variant specified by `variant_id` of the game specified by `game_id`. This is used, for example, by GamesmanUni when it needs to load a new position every time a user makes a move.
    
      When using this route to get information about a position, `position_string` should be the human-readable string representation of the position, and NOT the AutoGUI-formatted position string corresponding to that position.
      
      The response contains the following fields:
      - `position`: (String) The human-readable string representation of the position (e.g., a FEN string in Chess).
      - `autoguiPosition`: (String) The AutoGUI-formatted string corresponding to the position, which tells the frontend application how to render the position.
      - `positionValue`: (String) The value of this position (one of `win`, `tie`, `draw`, `lose`). There is also the value "unsolved" if the value of this position is unknown.
      - `remoteness`: (Number) For non-draw positions whose remotenesses are known, this is a non-negative integer (e.g., `5` means the game will end in 5 moves in perfect play). We use special remoteness codes for certain scenarios. If the position is a draw or if the game is a puzzle and the player is unable to solve the puzzle from this position, the we use `-200` to signify an infinite remoteness. If we have a non-draw position but its remoteness is unknown (e.g., an obviously-winning but extremely high-remoteness position in chess), then we use the code `-100` to signify a finite unknown remoteness.
      - `winby`: (Number, may be undefined) Available if this variant of this game was winby-solved. It is an integer describing how much the player-to-move should win by if they use a strategy that prioritizes win-by.
      - `drawLevel`: (Number, may be undefined) Available if pure draw analysis was performed on this variant of this game. If the position is not known to be a pure draw, then this field is undefined.
      - `drawRemoteness`: (Number, may be undefined) Available if pure draw analysis was performed on this variant of this game. If the position is not known to be a pure draw, then this field is undefined.
      - `moves`: (Array): A list of move objects sorted from best to worst (according to value and remoteness). If there are no legal moves from this position, then this is an empty array. Each move object in this array contains the following fields:
        - `move`: (String) The human-readable string representation of the move.
        - `autoguiMove`: (String) An AutoGUI-formatted move string, which tells the frontend application how to render the button that the user can click to make this move.
        - `moveValue`: (String) The outcome of the game for the player-to-move if they make this move and both players play perfectly afterward. This is one of (one of `win`, `tie`, `draw`, `lose`, and `unsolved`).
        - `deltaRemoteness`: (Number) Suppose a move M has a `moveValue` (see above) of V. The `deltaRemoteness` of M is the magnitude of the difference between the remoteness of M and the remoteness of the best move out of all moves that have `moveValue` V. We treat `tie` and `draw` as different values and we set the `deltaRemoteness` to 0. See the Helper Functions in `server.py` for more information. GamesmanUni uses this information to set different opacities for move buttons corresponding to moves of the same value but different remoteness.
        - `position`, `autoguiPosition`, `positionValue`, `remoteness`, `winby`, `drawLevel`, and `drawRemoteness` of the child position reached after making this move.

      Below is the response for position `1_oxoooxxx-` of the Regular variant of Mū Tōrere (`/mutorere/regular/positions/?p=1_oxoooxxx-`). The position is a win in 5 with one winning move to a lose-in-4 child position and one losing move to a win-in-1 child position. In Mū Tōrere and some other games, the `position` and `autoguiPosition` fields are the same (because, for those games, we have decided that the AutoGUI-formatted position string happens to be a good human-readable position string as well), but for other games, this is not the case.
      ```json
      {
          "position": "1_oxoooxxx-",
          "autoguiPosition": "1_oxoooxxx-",
          "positionValue": "win",
          "remoteness": 5,
          "moves": [
              {
                  "position": "2_oxoooxx-x",
                  "autoguiPosition": "2_oxoooxx-x",
                  "move": "7",
                  "autoguiMove": "M_7_8_x",
                  "moveValue": "win",
                  "positionValue": "lose",
                  "remoteness": 4,
                  "deltaRemoteness": 0
              },
              {
                  "position": "2_o-oooxxxx",
                  "autoguiPosition": "2_o-oooxxxx",
                  "move": "1",
                  "autoguiMove": "M_1_8_x",
                  "moveValue": "lose",
                  "positionValue": "win",
                  "remoteness": 1,
                  "deltaRemoteness": 0
              }
          ]
      }
      ```

- `/<game_id>/<variant_id>/instructions/?locale=<locale>` : 
  - Returns a markdown string for the instructions of the game specified by `game_id` (for when a user clicks the "i" button in GamesmanUni to get the rules guide of the game they are playing).
    - It gets the data for the game instructions from the [master branch Explainers GitHub repo](https://github.com/GamesCrafters/Explainers/tree/master/instructions). If instructions are not available in the language code specified by `locale` or if the `locale` parameter is not provided, then it defaults to English instructions for the game.
    - The `locale` will be a locale string which is formatted as either `<language>`, `<language>-<region>`, or `<language>_<region>`. Examples include "en-US" for United States English or "es" for Spanish. The returned instructions will be based on the `language` part of the `locale` string.
    - The URL suggests that there are different instructions for different variants of the game, but currently all variants of a game have the same set of instructions. Supporting variant-specific instructions is a (probably difficult) todo.
    - Example Routes:
      - `/nqueens/4/instructions/` (Instructions for NQueens Puzzle, defaults to English)
      - `/nqueens/4/instructions/?locale=en-US` (English instructions for NQueens Puzzle)
      - `/nqueens/4/instructions/?locale=es` (Spanish instructions for NQueens Puzzle)

