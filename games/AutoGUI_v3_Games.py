def animate_stt(variant_id, position, moves):
    turn = 'o' if position[2] == 'A' else 'x'
    pos = position[9:]
    if not moves or 'animationPhases' in moves[0]:
        return moves
    for move in moves:
        move_str = move['move'].split('_')
        p = int(move_str[1])
        q = int(move_str[2])
        if p < 3: # Dropping Move
            move['animationPhases'] = [['i_{}_{}_{}'.format(turn, p, p + 32 if pos[p + 32] == '-' else p + 21 if pos[p + 21] == '-' else p + 10)]]
        elif p == 15 or q == 15: # Shift top slider left
            move['animationPhases'] = [
                ['m_10_9', 'm_11_10', 'm_12_11', 'm_42_41', 'm_43_42'],
                ['m_10_39']
            ]
        elif p == 7 or q == 7: # Shift top slider right
            move['animationPhases'] = [
                ['m_10_11', 'm_11_12', 'm_12_13', 'm_41_42', 'm_42_43'],
                ['m_12_40']
            ]
        elif p == 26 or q == 26: # Shift middle slider left
            ap = [
                ['m_21_20', 'm_22_21', 'm_23_22', 'm_45_44', 'm_46_45'],
                ['m_21_39', 'm_12_23']
            ]
            if pos[23] == '-':
                ap[1].append('m_11_22')
            if pos[22] == '-':
                ap[1].append('m_10_21')
            move['animationPhases'] = ap
        elif p == 18 or q == 18: # Shift middle slider right
            ap = [
                ['m_21_22', 'm_22_23', 'm_23_24', 'm_44_45', 'm_45_46'],
                ['m_23_40', 'm_10_21']
            ]
            if pos[21] == '-':
                ap[1].append('m_11_22')
            if pos[22] == '-':
                ap[1].append('m_12_23')
            move['animationPhases'] = ap
        elif p == 37 or q == 37: # Shift bottom slider left
            ap = [
                ['m_32_31', 'm_33_32', 'm_34_33', 'm_48_47', 'm_49_48'],
                ['m_32_39', 'm_12_23', 'm_23_34']
            ]
            if pos[34] == '-':
                ap[1] += ['m_11_22', 'm_22_33']
            if pos[33] == '-':
                ap[1] += ['m_10_21', 'm_21_32']
            move['animationPhases'] = ap
        elif p == 29 or q == 29: # Shift bottom slider right
            ap = [
                ['m_32_33', 'm_33_34', 'm_34_35', 'm_47_48', 'm_48_49'],
                ['m_34_40', 'm_10_21', 'm_21_32']
            ]
            if pos[32] == '-':
                ap[1] += ['m_11_22', 'm_22_33']
            if pos[33] == '-':
                ap[1] += ['m_12_23', 'm_23_34']
            move['animationPhases'] = ap
        
    return moves

autoGUIv3DataFuncs = {
    'stt': animate_stt
}

def get_autoguiV3Data(game_id, variant_id, position, moves):
    if game_id in autoGUIv3DataFuncs:
        return autoGUIv3DataFuncs[game_id](variant_id, position, moves)
    return moves