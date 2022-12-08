import json

class Edge:
    def __init__(self, from_node, to_node, part_move, move, move_name=None):
        self.from_node = from_node
        self.to_node = to_node
        self.part_move = part_move
        self.move = move
        self.move_name = move_name

    def __str__(self):
        return "Edge %s %s %s %s %s" % (
        self.from_node.board, self.to_node.board, self.part_move, self.move, self.move_name)


class Node:
    def __init__(self, board, value=None, remoteness=None, mp_remoteness=None, move_name=None, has_multipart=True):
        self.board = board
        self.value = value
        self.remoteness = remoteness
        self.mp_remoteness = mp_remoteness
        self.move_name = move_name
        self.has_multipart = has_multipart
        self.edges_in = []

    def score(self):  # Used for sorting terminal nodes
        if self.value == 'win':
            return self.remoteness
        elif self.value == 'lose':
            return 200000 - self.remoteness
        else:
            return 100000 + self.remoteness

    def __str__(self):
        return "%s %s %s %s %s (%s)" % (self.board, self.value, self.remoteness, self.mp_remoteness,
                                        self.move_name, ','.join([('%s' % e) for e in self.edges_in]))


def multipart_solve(position, input_dict, output_type=0):
    if not input_dict:
        return None
    position_is_intermediate = False
    node_dict = {}  # Useful to keep track of which nodes have been created
    terminal_nodes = []
    edge_list = []
    move_name_dict = {}

    # Get multipart edges
    mp_response = input_dict['multipart']
    if output_type == 1 and not mp_response:
        return None
    for r in mp_response:
        from_pos = r.get('from')
        to_pos = r.get('to')
        if to_pos == position:
            position_is_intermediate = True
        part_move = r.get('partMove')
        move = r.get('move')
        move_name = r.get('moveName')

        # Create nodes if needed
        if from_pos not in node_dict:
            node_dict[from_pos] = Node(from_pos)
        if to_pos not in node_dict:
            node_dict[to_pos] = Node(to_pos)

        edge = Edge(node_dict[from_pos], node_dict[to_pos], part_move, move, move_name=move_name)

        # Add edges to nodes
        node_dict[to_pos].edges_in.append(edge)
        edge_list.append(edge)

    # Get terminal nodes
    response = input_dict['moves']  # Response is a list of dicts
    for r in response:
        board = r.get('board')
        remoteness = r.get('remoteness')
        value = r.get('value')

        # Flip value
        if value == 'win':
            value = 'lose'
        elif value == 'lose':
            value = 'win'

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
            node_dict[board] = Node(board, remoteness=remoteness, mp_remoteness=0, value=value, move_name=move_name,
                                    has_multipart=False)
            n = node_dict[board]
        if n not in terminal_nodes:
            terminal_nodes.append(n)
        if not n.has_multipart and not position_is_intermediate:
            edge = Edge(node_dict[position], node_dict[board], move, move, move_name=move_name)
            n.edges_in.append(edge)
            edge_list.append(edge)

    # Sort terminal nodes from best to worst
    terminal_nodes = sorted(terminal_nodes, key=lambda n: n.score())

    # Reverse DFS
    def dfs(n, mp_remoteness):
        mp_remoteness += 1
        for edge in n.edges_in:
            parent = edge.from_node
            remoteness_increment = 1 if n in terminal_nodes else 0

            if not parent.value:
                parent.value = n.value
                parent.remoteness = n.remoteness + remoteness_increment
                parent.mp_remoteness = mp_remoteness
                dfs(parent, mp_remoteness)
            elif parent.value != n.value:
                if parent.value == 'tie' and n.value == 'win' or parent.value =='lose':
                    parent.value = n.value
                    parent.remoteness = n.remoteness + remoteness_increment
                    parent.mp_remoteness = mp_remoteness
                    dfs(parent, mp_remoteness)
            elif parent.remoteness != n.remoteness + remoteness_increment:
                if parent.value == 'lose' and n.remoteness + remoteness_increment > parent.remoteness:
                    parent.remoteness = n.remoteness + remoteness_increment
                    parent.mp_remoteness = mp_remoteness
                    dfs(parent, mp_remoteness)
                elif parent.value != 'lose' and n.remoteness + remoteness_increment < parent.remoteness:
                    parent.remoteness = n.remoteness
                    parent.mp_remoteness = mp_remoteness
                    dfs(parent, mp_remoteness)

    for n in terminal_nodes:
        dfs(n, 0)

    if output_type == 0:
        moves = []
        for e in edge_list:
            move_name = move_name_dict.get(e.move)  # Move name from edge
            if not move_name:
                move_name = e.to_node.move_name  # Move name from node
            move_dict = {
                'fromPos': e.from_node.board,
                'move': e.part_move,
                'board': e.to_node.board,
                'moveValue': e.to_node.value,
                'value': e.to_node.value if e.to_node.mp_remoteness else {'lose': 'win', 'tie': 'tie', 'win': 'lose', 'draw': 'draw'}[e.to_node.value],
                'remoteness': e.to_node.remoteness,
                'moveName': move_name
                #'isTerminal': move_name != None
            }
            moves.append(move_dict)
        return moves
    else:
        pos_dict = {
            'board': position, 
            'remoteness': node_dict.get(position).remoteness,
            'value': node_dict.get(position).value
        }
        return pos_dict