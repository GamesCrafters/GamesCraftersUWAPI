"""
    Author: Cameron Cheung
"""

from .models import AbstractVariant
import sys, pickle, os

dirname = os.path.dirname(__file__)

class Ghost(AbstractVariant):
#class Ghost:
    def __init__(self, minimum_length=4):
        self.minimum_length = minimum_length
        super(Ghost, self).__init__(f"Min Length = {minimum_length}", 'v3')

    def start_position(self):
        return {'position': '-', 'autoguiPosition': '1_.~'}
    
    def position_data(self, position):
        with open(f'{dirname}/../data/ghost/ghost{self.minimum_length}.pkl', 'rb') as trie_file:
            trie_root_node = pickle.load(trie_file)

        word = Ghost.position_to_word(position)
        remoteness = get_remoteness(trie_root_node, word)
        moves = []

        if remoteness > 0:
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                child_remoteness = get_remoteness(trie_root_node, word + letter)
                autogui_coord_id = ord(letter) - 64
                moves.append({
                    'move': letter,
                    'autoguiMove': f'T_{letter}_{autogui_coord_id}_x',
                    'position': word + letter,
                    'autoguiPosition': Ghost.word_to_autogui_pos_str(word + letter),
                    'positionValue': 'lose' if child_remoteness & 1 else 'win',
                    'remoteness': child_remoteness,
                })

        response = {
            'position': position,
            'autoguiPosition': Ghost.word_to_autogui_pos_str(position),
            'positionValue': 'lose' if remoteness & 1 else 'win',
            'remoteness': remoteness,
            'moves': moves
        }
        return response
    
    def position_to_word(position):
        return '' if position == '-' else position

    def word_to_autogui_pos_str(word):
        if word == '-':
            word = ''
        return f"{'2' if len(word) & 1 else '1'}_.~{word}"

# New TrieNode Definition: [remoteness, children] = [None, {}]

def insert(node, word):
    """
        For assembling the trie. All trie nodes will have a stored remoteness of None
        initially EXCEPT for nodes signifying ends of words at least as long as
        `minimum_length`, whose remoteness we initially set to 0 (Win in 0) because the
        player who completes a valid word loses. In solve_trie we prune the trie and find
        the remoteness values of all trie nodes.
    """
    for letter in word:
        if letter in node[1]:
            node = node[1][letter]
        else:
            new_node = [None, {}]
            node[1][letter] = new_node
            node = new_node
    if len(word) >= minimum_length:
        node[0] = 0

def get_remoteness(node, prefix):
    """
        If `prefix` cannot be found in the trie, return remoteness 0 (Win in 0) because
        the player who completes this invalid prefix loses. Otherwise, return the
        remoteness at the trie node.
    """
    for letter in prefix:
        if letter in node[1]:
            node = node[1][letter]
        else:
            return 0
    return node[0]

def solve_trie(trie_root_node):
    """
        1. Prune subtries of any nodes with 0 remoteness. Such nodes arise when
           for a word w longer than `minimum_length` there exists another word
           w' with the first word as a prefix.
        2. For each node without children but whose remoteness is not set to 0,
           set its remoteness to 1. Such nodes arise for ends of valid words
           that are shorter than `minimum_length`.
        3. For each other node, recursively compute its remoteness, keeping
           in mind that there only exist Win in Even Remoteness and Lose in
           Odd Remoteness in this game.
    """
    REMOTENESS_MAX = 999 # Should be fine unless your vocabulary includes some weird long chemical name
    def solve_node(node, prefix):
        if node[0] == 0:
            node[1] = {}
        elif not node[1] and node[0] is None:
            node[0] = 1
        else:
            min_lose_child_remoteness = REMOTENESS_MAX
            max_win_child_remoteness = 0
            for letter in node[1]:
                child_remoteness = solve_node(node[1][letter], prefix + letter)
                if child_remoteness & 1:
                    min_lose_child_remoteness = min(child_remoteness, min_lose_child_remoteness)
                else:
                    max_win_child_remoteness = max(child_remoteness, max_win_child_remoteness)
            if min_lose_child_remoteness < REMOTENESS_MAX:
                node[0] = min_lose_child_remoteness + 1
            else:
                node[0] = max_win_child_remoteness + 1
        return node[0]

    solve_node(trie_root_node, '')

if __name__ == '__main__':
    """
        USAGE: python Ghost.py <words list filepath> <minimum length>
        If running this directly, make sure to first comment out any references 
        to AbstractVariant.

        Assemble a trie from the words listed in the file.
        Solve the trie (according to minimum valid word length)
        and store it in a pickle file.
    """
    word_list_path, minimum_length = sys.argv[1:3]
    minimum_length = int(minimum_length)
    trie_root_node = [None, {}]
    max_length, argmax_length = 0, ''
    with open(word_list_path) as words_file:
        for word in words_file:
            cleaned_word = word.rstrip().upper()
            if cleaned_word.isalpha():
                if len(cleaned_word) > max_length:
                    max_length = len(cleaned_word)
                    argmax_length = cleaned_word
                insert(trie_root_node, cleaned_word)

    print(f'Max Length: {max_length}; Argmax Length: {argmax_length}')
    solve_trie(trie_root_node)

    with open(f'{dirname}/../data/ghost/ghost{minimum_length}.pkl', 'wb') as trie_file:
        pickle.dump(trie_root_node, trie_file, pickle.HIGHEST_PROTOCOL)