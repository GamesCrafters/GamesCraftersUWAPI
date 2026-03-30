"""
File: sokoban.py
Puzzle: Sokoban
Author: Doris Chang, Kshitij Tomar
Date: 2026-03-18
"""

from . import ServerPuzzle
from ..util import *

class Sokoban(ServerPuzzle):

    id = 'sokoban'
    variants = ["1", "2", "3", "4", "5"]
    startRandomized = False

    def __init__(self, variant_id: str, state=None):
        """
        Your constructor can have any signature you'd like,
        because it is only called by the other methods of this class.
        If your puzzle supports multiple variants, it should
        receive some information on the variant as input.

        An instance of the puzzle class represents a self.state
        in the puzzle, so the constructor should take in information
        that sufficienctly defines a self.state as input.
        """
        if variant_id not in Sokoban.variants:
            raise ValueError("Variant not defined")
        
        self.variant_id = variant_id
        
        # Directions: Right, Down, Left, Up
        self.dxdy = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.dirs = {(1, 0): "R", (0, 1): "D", (-1, 0): "L", (0, -1): "U"}

        match self.variant_id:
            case "1": # equivalent to Level 1 from the online Sokoban player
                self.column_size = 6
                self.row_size = 7
                self.starting_pos = (
                    "##   #"
                    ".@$  #"
                    "## $.#"
                    ".##$ #"
                    " # . #"
                    "$ *$$."
                    "   .  "
                )
            case "2":
                self.column_size = 8
                self.row_size = 8
                self.starting_pos = (
                    "  ###   "
                    "  # #   "
                    "  #.#   "
                    "###$#   "
                    "#. $@###"
                    "####   #"
                    "   #   #"
                    "   #####"
                )

            case "3":
                self.column_size = 11
                self.row_size = 10
                self.starting_pos = (
                    "########## "
                    "#        # "
                    "# $$ $   # "
                    "#      ### "
                    "####   #   "
                    "   # @ #   "
                    "   # $ #   "
                    "####   ####"
                    "#....     #"
                    "###########"
                )
            case "4":
                self.column_size = 9
                self.row_size = 9
                self.starting_pos = (
                    "  #####  "
                    "  #   #  "
                    "###$  #  "
                    "#   $ #  "
                    "#   @ ###"
                    "##### $ #"
                    "  ### $ #"
                    "  #.... #"
                    "  #######"
                )
            #"                      "
            case "5":
                self.column_size = 23
                self.row_size = 12
                self.starting_pos = (
                    "    #####              "
                    "    #   #              "
                    "    #$  #              "
                    "  ###  $###            "
                    "  #  $  $ #            "
                    "### # ### #            "
                    "#   # ### #      ######"
                    "#   # ### ########  ..#"
                    "# $  $              ..#"
                    "##### ####  #@####  ..#"
                    "    #       ###  ######"
                    "    #########          "
                )
            
        self.state = state if state is not None else self.starting_pos


    def generateMoves(self, movetype="all", **kwargs):
        """
        Returns a list of only the moves that push a box: (box_idx, dx, dy)
        
        """
        moves = []
        
        p_idx = self.get_pos_idx(self.state)
            
        px, py = p_idx % self.column_size, p_idx // self.column_size
        
        # 1. BFS to find all spaces the player can currently reach
        reachable = set()
        queue = [(px, py)]
        
        while queue:
            curr_x, curr_y = queue.pop(0)
            if (curr_x, curr_y) not in reachable:
                reachable.add((curr_x, curr_y))
                
                for dx, dy in self.dxdy:
                    nx, ny = curr_x + dx, curr_y + dy
                    if 0 <= nx < self.column_size and 0 <= ny < self.row_size:
                        n_idx = ny * self.column_size + nx
                        if self.state[n_idx] in [' ', '.']:
                            queue.append((nx, ny))
        
        # 2. Check all boxes to see if they can be pushed
        for y in range(self.row_size):
            for x in range(self.column_size):
                idx = y * self.column_size + x
                if self.state[idx] in ['$', '*']: # Found a box
                    for dx, dy in self.dxdy:
                        player_req_x, player_req_y = x - dx, y - dy
                        push_target_x, push_target_y = x + dx, y + dy
                        
                        if (player_req_x, player_req_y) in reachable:
                            if 0 <= push_target_x < self.column_size and 0 <= push_target_y < self.row_size:
                                target_idx = push_target_y * self.column_size + push_target_x
                                if self.state[target_idx] in [' ', '.', '@', '+']:
                                    moves.append((idx, dx, dy))
        return moves

    def doMove(self, move):
        box_idx, dx, dy = move
        pos_list = list(self.state)
        
        # 1. Remove player from old self.state
        p_idx = self.get_pos_idx(self.state)
        pos_list[p_idx] = '.' if pos_list[p_idx] == '+' else ' '
        
        # 2. Calculate new coordinates for the pushed box
        bx = box_idx % self.column_size
        by = box_idx // self.column_size
        nx, ny = bx + dx, by + dy 
        n_idx = ny * self.column_size + nx
        
        # 3. Place the box in its new location
        if pos_list[n_idx] == '.':
            pos_list[n_idx] = '*'
        else:
            pos_list[n_idx] = '$'
            
        # 4. Move the player into the tile the box just vacated
        if self.state[box_idx] == '*': 
            pos_list[box_idx] = '+'
        else:
            pos_list[box_idx] = '@'
            
        new_state = "".join(pos_list)
        return Sokoban(self.variant_id, new_state)

    def primitive(self, **kwargs):
        """
        Returns PuzzleValue.SOLVABLE if all boxes are on goals.
        Returns PuzzleValue.Lose if any box is deadlocked in a corner.
        Otherwise returns None.
        """
        # 1. Win Condition
        if self.state.find('$') == -1:
            return PuzzleValue.SOLVABLE

        # 2. Corner Deadlock Detection
        for y in range(self.row_size):
            for x in range(self.column_size):
                idx = y * self.column_size + x
                if self.state[idx] == '$':
                    up = (y == 0) or (self.state[(y - 1) * self.column_size + x] == '#')
                    down = (y == self.row_size - 1) or (self.state[(y + 1) * self.column_size + x] == '#')
                    left = (x == 0) or (self.state[y * self.column_size + (x - 1)] == '#')
                    right = (x == self.column_size - 1) or (self.state[y * self.column_size + (x + 1)] == '#')

                    if (up or down) and (left or right):
                        return PuzzleValue.IMPOSSIBLE

        return PuzzleValue.UNDECIDED

    @property
    def variant(self):
        """ No need to change this. """
        return self.variant_id
    

    def toString(self, mode: StringMode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the puzzle self.state -- String
        """
        # Note: Playing this puzzle on the command-line is not supported,
        # so we can expect that `mode` is not StringMode.HUMAN_READABLE_MULTILINE
        if mode == StringMode.AUTOGUI:
            # Replaces floor spaces with dashes to map perfectly to Image AutoGUI
            return self.state.replace(' ', '-')
        else:
            # Human readable: splits the 1D string into a multiline 2D grid
            board = [self.state[idx * self.column_size : (idx + 1) * self.column_size] for idx in range(self.row_size)]
            return "\n".join(board)
        
    
    def moveString(self, move, mode):
        """
        Inputs:
            mode -- See StringMode in util.py.
        
        Outputs:
            String representation of the move -- String
        """
        # Note: Playing this puzzle on the command-line is not supported,
        # so we can expect that `mode` is not StringMode.HUMAN_READABLE_MULTILINE
        box_idx, dx, dy = move
        
        if mode == StringMode.AUTOGUI:
            dest_idx = box_idx + (dy * self.column_size) + dx
            return f"M_{box_idx}_{dest_idx}_y"
        else:
            # Human readable move string like "12R" (Push box at index 12 Right)
            direction = self.dirs.get((dx, dy), "?")
            return f"{box_idx}{direction}"
    
    def get_pos_idx(self, position: str):
        p_idx = position.find('@')
        if p_idx == -1:
            p_idx = position.find('+')
        return p_idx; 
    

    @classmethod
    def generateStartPosition(cls, variant_id, **kwargs):
        return cls(variant_id)

    @classmethod
    def fromString(cls, variant_id, position_str):
        clean_state = position_str.replace("\n", "")
        return cls(variant_id, clean_state)
            
    @classmethod
    def isLegalPosition(cls, position_str):
        return '@' in position_str or '+' in position_str