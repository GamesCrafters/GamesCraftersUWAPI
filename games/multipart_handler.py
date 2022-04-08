import json

class Edge:
    def __init__(self, from_node, to_node, part_move, move, follow, move_name=None):
        self.from_node = from_node
        self.to_node = to_node
        self.part_move = part_move
        self.move = move
        self.follow = follow
        self.move_name = move_name

    def __str__(self):
        return "Edge %s %s %s %s %s %s" % (self.from_node.board, self.to_node.board, self.part_move, self.move,
                                           self.follow, self.move_name)

class Node:
    def __init__(self, board, value=None, remoteness=None, mp_remoteness=None, move_name=None, has_multipart=True):
        self.board = board
        self.value = value
        self.remoteness = remoteness
        self.mp_remoteness = mp_remoteness
        self.move_name = move_name
        self.has_multipart = has_multipart
        self.edges_in = []

    def score(self): # Used for sorting terminal nodes
        if self.value == 'win':
            return self.remoteness
        elif self.value == 'lose':
            return 200000 - self.remoteness
        else:
            return 100000 + self.remoteness

    def __str__(self):
        return "%s %s %s %s %s (%s)" % (self.board, self.value, self.remoteness, self.mp_remoteness,
                                      self.move_name, ','.join([('%s' % e) for e in self.edges_in]))


def multipart_solve(position, input_dict):
    node_dict = {}  # Useful to keep track of which nodes have been created
    terminal_nodes = []
    edge_list = []
    move_name_dict = {}

    # Get multipart edges
    mp_response = input_dict.get('multipart')
    for r in mp_response:
        from_pos = r.get('from')
        to_pos = r.get('to')
        part_move = r.get('partMove')
        move = r.get('move')
        follow = r.get('follow')
        if follow is None and move is not None:
            follow = True
        move_name = r.get('moveName')

        # Create nodes if needed
        if from_pos not in node_dict:
            node_dict[from_pos] = Node(from_pos)
        if to_pos not in node_dict:
            node_dict[to_pos] = Node(to_pos)

        edge = Edge(node_dict[from_pos], node_dict[to_pos], part_move, move, follow, move_name=move_name)

        # Add edges to nodes
        node_dict[to_pos].edges_in.append(edge)
        edge_list.append(edge)

    # Get terminal nodes
    response = input_dict.get('response')  # Responses is a list of dicts
    for r in response:
        board = r.get('board')
        remoteness = r.get('remoteness')
        value = r.get('value')

        # Flip value
        if value == 'win':
            value = 'lose'
        elif value == 'lose':
            value = 'win'
        #remoteness += 1

        move = r.get('move')
        move_name = r.get('moveName')
        move_name_dict[move] = move_name

        n = node_dict.get(board)
        if n:
            n.remoteness = remoteness
            n.mp_remoteness = 0
            n.value = value
            n.move_name = move_name
        else:
            node_dict[board] = Node(board, remoteness=remoteness, mp_remoteness=0, value=value, move_name=move_name, has_multipart=False)
            n = node_dict[board]
        if n not in terminal_nodes:
            terminal_nodes.append(n)
        if not n.has_multipart:
            edge = Edge(node_dict[position], node_dict[board], move, move, True, move_name=move_name)
            n.edges_in.append(edge)
            edge_list.append(edge)

    # Sort terminal nodes from best to worst
    terminal_nodes = sorted(terminal_nodes, key=lambda n: n.score())

    # Reverse DFS
    def dfs(n, mp_remoteness):
        mp_remoteness += 1
        for edge in n.edges_in:
            if not edge.follow:
                continue
            parent = edge.from_node
            
            if not parent.value or (parent.value == n.value and parent.mp_remoteness > n.mp_remoteness):
                parent.value = n.value
                parent.remoteness = n.remoteness
                parent.mp_remoteness = mp_remoteness
                dfs(parent, mp_remoteness)

    for n in terminal_nodes:
        dfs(n, 0)

    # Output
    moves = []
    for e in edge_list:
        move_name = move_name_dict.get(e.move) # Move name from edge
        if not move_name:
            move_name = e.to_node.move_name  # Move name from node
        move_dict = {
            'fromPos': e.from_node.board,
            'move': e.part_move,
            'position': e.to_node.board,
            # 'deltaRemoteness': 0 # Will be handled in server.py
            'moveValue': e.to_node.value,
            'positionValue': e.to_node.value if e.to_node.mp_remoteness else {'lose': 'win', 'tie': 'tie', 'win': 'lose'}[e.to_node.value],
            'remoteness': e.to_node.remoteness,
            'mp_remoteness': e.to_node.mp_remoteness,
            'follow': e.follow,
            'moveName': move_name
        }
        moves.append(move_dict)
    return moves


if __name__ == '__main__':
    # test input
    f = open('input2.json')
    input_d = json.load(f)
    f.close()

    result = multipart_solve("P0", input_d)
    print("\n\n====RESULT======")
    print(json.dumps(result, indent=2))