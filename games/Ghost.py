from .models import EfficientGameVariant
import sys, pickle, os

dirname = os.path.dirname(__file__)

class Ghost(EfficientGameVariant):
#class Ghost:
    def __init__(self, minimum_length=4):
        name, desc = "Regular", f"Min Length = {minimum_length}"
        self.minimum_length = minimum_length
        super(Ghost, self).__init__(name, desc, status="stable", gui_status="v2")

    def start_position(self):
        return "R_A_0_0_-"
    
    def uwapi_pos_str_to_word(self, position):
        return position[8:].replace('-', '')

    def word_to_uwapi_pos_str(self, word):
        turn, first_part, second_part = 'A', None, None
        s = len(word)
        if s & 1:
            turn = 'B'
            sides = '-' * ((25 - s) // 2)
            first_part = sides + word + sides
            second_part = '-' * 24
        else:
            sides = '-' * ((24 - s) // 2)
            first_part = '-' * 25
            second_part = sides + word + sides
        
        return f'R_{turn}_0_0_{first_part}{second_part}'
    
    def full_stats(self, position):
        with open(f'{dirname}/../data/ghost/ghost{self.minimum_length}.pkl', 'rb') as trie_file:
            trie = pickle.load(trie_file)

        word = self.uwapi_pos_str_to_word(position)
        moves = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            remoteness = trie.get_remoteness(word + letter)
            autogui_coord_id = ord(letter) - 16
            next_res = {
                "move": f'A_{letter.lower()}_{autogui_coord_id}',
                "moveName": letter,
                "position": self.word_to_uwapi_pos_str(word + letter),
                "positionValue": 'lose' if remoteness & 1 else 'win',
                "remoteness": remoteness,
            }
            moves.append(next_res)

        remoteness = trie.get_remoteness(word)
        response = {
            "position": position,
            "positionValue": 'lose' if remoteness & 1 else 'win',
            "remoteness": remoteness,
            "moves": moves
        }
        return response

    def stat(self, position):
        return

    def next_stats(self, position):
        return
    

class Node:
    def __init__(self, letter):
        self.letter = letter
        self.remoteness = None
        self.children = {}

class Trie:

    def __init__(self, minimum_length):
        self.minimum_length = minimum_length
        self.root = Node('')
    
    def insert(self, word):
        """
            For assembling the trie. All trie nodes will have a stored remoteness of None
            initially EXCEPT for nodes signifying ends of words at least as long as
            `minimum_length`, whose remoteness we initially set to 0 (Win in 0) because the
            player who completes a valid word loses. In solve_trie we prune the trie and find
            the remoteness values of all trie nodes.
        """
        node = self.root
        for letter in word:
            if letter in node.children:
                node = node.children[letter]
            else:
                new_node = Node(letter)
                node.children[letter] = new_node
                node = new_node
        if len(word) >= self.minimum_length:
            node.remoteness = 0
        
    def get_remoteness(self, prefix):
        """
            If `prefix` cannot be found in the trie, return remoteness 0 (Win in 0) because
            the player who completes this invalid prefix loses. Otherwise, return the
            remoteness at the trie node.
        """
        node = self.root
        for letter in prefix:
            if letter in node.children:
                node = node.children[letter]
            else:
                return 0
        return node.remoteness

def solve_trie(trie):
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
    REMOTENESS_MAX = 999
    def solve_node(node, prefix):
        if node.remoteness == 0:
            node.children = {}
        elif not node.children and node.remoteness is None:
            node.remoteness = 1
        else:
            min_lose_child_remoteness = REMOTENESS_MAX
            max_win_child_remoteness = 0
            for letter in node.children:
                child_remoteness = solve_node(node.children[letter], prefix + letter)
                if child_remoteness & 1:
                    min_lose_child_remoteness = min(child_remoteness, min_lose_child_remoteness)
                else:
                    max_win_child_remoteness = max(child_remoteness, max_win_child_remoteness)
            if min_lose_child_remoteness < REMOTENESS_MAX:
                node.remoteness = min_lose_child_remoteness + 1
            else:
                node.remoteness = max_win_child_remoteness + 1
        return node.remoteness

    solve_node(trie.root, '')

if __name__ == '__main__':
    """
        USAGE: python Ghost.py <words list filepath> <minimum length>

        Assemble a trie from the words listed in the file.
        Solve the trie (according to minimum valid word length)
        and store it in a pickle file.
    """
    word_list_path, minimum_length = sys.argv[1:3]
    trie = Trie(int(minimum_length))
    max_length, argmax_length = 0, ''
    with open(word_list_path) as words_file:
        for word in words_file:
            cleaned = word.rstrip().upper()
            if len(cleaned) > max_length and cleaned.isalpha():
                max_length = len(cleaned)
                argmax_length = cleaned
            trie.insert(cleaned)

    print(f'Max Length: {max_length}; Argmax Length: {argmax_length}')
    solve_trie(trie)

    with open(f'{dirname}/../data/ghost/ghost{minimum_length}.pkl', 'wb') as trie_file:
        pickle.dump(trie, trie_file, pickle.HIGHEST_PROTOCOL)