from .models import Value, Remoteness

class Node:
    def __init__(self, id, autogui_position, value=None, remoteness=None):
        self.id = id
        self.autogui_position = autogui_position
        self.value = value
        self.remoteness = remoteness
        self.outgoing_edges = {}

    def add_edge(src_node, dest_node, move_obj):
        src_node.outgoing_edges[move_obj['move']] = (dest_node, move_obj)

def multipart_solve(node):
    """
    Full-moves and part-moves to real child positions with value WIN are bad; and 
    full-moves and part-moves to real child positions with value LOSE are good.

    However, note that we are doing same-player/go-again solving here with the intermediate 
    states, so part-moves to intermediate states with value WIN are good, and part-moves to 
    intermediate states with value LOSE are bad.

    It is assumed that the input node and all other nodes reachable from it form a DAG. 
    No loopiness allowed! It is also assumed that the DAG has a small number of nodes.
    """
    if not node.outgoing_edges:
        # Reached if `node` is a real child position
        opposite_value = node.value
        if node.value == Value.WIN:
            opposite_value = Value.LOSE
        elif node.value == Value.LOSE:
            opposite_value = Value.WIN
        incremented_remoteness = node.remoteness + 1 if node.value != Value.DRAW else Remoteness.INFINITY
        return opposite_value, incremented_remoteness
    else: 
        # Reached if `node` is an intermediate state.
        # Note that we are doing same-player/go-again solving here, so moves to intermediate states with 
        # value WIN are good, and moves to intermediate states with value LOSE are bad.
        exists_win, exists_tie, exists_draw = False, False, False
        best_win_rem, best_tie_rem, best_lose_rem = Remoteness.MAX, Remoteness.MAX, 0

        for edge in node.outgoing_edges.values():
            value, remoteness = multipart_solve(edge[0])
            if value == Value.WIN:
                exists_win = True
                best_win_rem = min(remoteness, best_win_rem)
            elif value == Value.TIE:
                exists_tie = True
                best_tie_rem = min(remoteness, best_tie_rem)
            elif value == Value.DRAW:
                exists_draw = True
            else:
                best_lose_rem = max(remoteness, best_lose_rem)

        if exists_win:
            node.value = Value.WIN
            node.remoteness = best_win_rem
        elif exists_tie:
            node.value = Value.TIE
            node.remoteness = best_tie_rem
        elif exists_draw:
            node.value = Value.DRAW
            node.remoteness = Remoteness.INFINITY
        else:
            node.value = Value.LOSE
            node.remoteness = best_lose_rem
        
        return node.value, node.remoteness

def multipart_wrangle(requested_position, position_data):
    if position_data and 'partMoves' in position_data:
        intermediate_states = {}
        real_child_positions = {}
        move_name_to_real_child_position = {}

        # Step 1: Create Nodes

        # 1.1: Create Parent Real Position Node
        parent_real_position = Node(
            position_data['position'], 
            position_data['autoguiPosition'], 
            position_data['positionValue'], 
            position_data.get('remoteness', Remoteness.INFINITY)
        )

        # 1.2: Create Child Real Position Nodes
        for full_move_obj in position_data['moves']:
            position_string = full_move_obj['position']
            if position_string not in real_child_positions:
                real_child_positions[position_string] = Node(
                    position_string,
                    full_move_obj['autoguiPosition'],
                    full_move_obj['positionValue'], 
                    full_move_obj.get('remoteness', Remoteness.INFINITY)
                )
            move_name_to_real_child_position[full_move_obj['move']] = real_child_positions[position_string]
        
        # 1.3: Create Intermediate State Nodes
        for part_move_obj in position_data['partMoves']:
            if 'from' in part_move_obj:
                autogui_position_string = part_move_obj['from']
                if autogui_position_string not in intermediate_states:
                    intermediate_states[autogui_position_string] = Node(autogui_position_string, autogui_position_string)
            if 'to' in part_move_obj:
                autogui_position_string = part_move_obj['to']
                if autogui_position_string not in intermediate_states:
                    intermediate_states[autogui_position_string] = Node(autogui_position_string, autogui_position_string)

        # Step 2: Create Edges

        # 2.1: Create single-part move edges. A full-move is a single-part move if `autoguiMove` is defined.          
        for full_move_obj in position_data['moves']:
            if 'autoguiMove' in full_move_obj:
                Node.add_edge(parent_real_position, real_child_positions[full_move_obj['position']], full_move_obj)
        
        # 2.2: Create multi-part move edges.
        for part_move_obj in position_data['partMoves']:
            from_node, to_node = None, None
            if 'from' in part_move_obj:
                from_node = intermediate_states[part_move_obj['from']]
            else:
                from_node = parent_real_position
            
            if 'to' in part_move_obj:
                to_node = intermediate_states[part_move_obj['to']]
            else:
                to_node = move_name_to_real_child_position[part_move_obj['full']]
            Node.add_edge(from_node, to_node, part_move_obj)
        
        del move_name_to_real_child_position

        # Step 3: Solve the Multipart Move Graph
        multipart_solve(parent_real_position)

        # Step 4: Traverse the multipart move graph according to the sequence of partmoves given 
        #         by the original semicolon-delimited position string in the request.
        requested_node = parent_real_position
        for part_move in requested_position.strip().split(';')[1:]:
            requested_node = requested_node.outgoing_edges[part_move][0]
        
        # Step 5: Modify position_data to contain the correct data for the 
        # requested state, whether the state is an intermediate state or the real parent position
        position_data['autoguiPosition'] = requested_node.autogui_position
        position_data['position'] = requested_position
        position_data['positionValue'] = requested_node.value
        position_data['remoteness'] = requested_node.remoteness

        new_move_objs = []
        for edge in requested_node.outgoing_edges.values():
            out_neighbor, move_obj = edge
            next_position = ''
            move_name = ''
            if out_neighbor.outgoing_edges: # i.e., this edge does not go to a real child position
                move_name = '~' + move_obj['move']
                #move_name = move_obj['move']
                next_position = f'{requested_position};{move_obj["move"]}'
            else: # i.e., this edge goes to a real child position
                if 'full' in move_obj: # i.e., this edge is a part-move
                    move_name = move_obj['full']
                    #move_name = move_obj['move']
                else: # i.e., this edge is a full-move
                    move_name = move_obj['move']
                next_position = out_neighbor.id
            new_move_objs.append(
                {
                    'autoguiMove': move_obj['autoguiMove'],
                    'autoguiPosition': out_neighbor.autogui_position,
                    'move': move_name,
                    'position': next_position,
                    'positionValue': out_neighbor.value,
                    'remoteness': out_neighbor.remoteness
                }
            )

        del position_data['partMoves']
        position_data['moves'] = new_move_objs