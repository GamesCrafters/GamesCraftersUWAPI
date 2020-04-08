import re


TURN_A = 'A'
TURN_B = 'B'

REGEX_REGULAR2D_POSITION = re.compile(
    r"^R_(A|B)_([0-9]+)_([0-9]+)_([a-zA-Z0-9-\*]+)(?:_(.*))?$")


def board_regular2d_parse_position_string(string):
    m = REGEX_REGULAR2D_POSITION.match(string)
    if not m:
        return None

    turn, num_rows, num_columns, board = m.groups()[0:4]
    num_rows, num_columns = int(num_rows), int(num_columns)

    # The length of the board must match the number of rows and columns specified
    if len(board) != num_rows * num_columns:
        return None

    return turn, num_rows, num_columns, board


def board_regular2d_make_position_string(turn, num_rows, num_columns, board):
    return f"R_{turn}_{num_rows}_{num_columns}_{board}"
