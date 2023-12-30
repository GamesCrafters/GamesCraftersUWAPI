import random

def sortString(str) :
    str = ''.join(sorted(str))

def get_forestfox(variant_id):
    cards = 'abcdefghijklmno'
    shuffled = ''.join(random.sample(cards, len(cards)))
    first = ''.join(sorted(shuffled[:7]))
    second = ''.join(sorted(shuffled[7:14]))
    hands = first + second + shuffled[-1]
    return f'R_A_0_0_{hands}--00'


random_start_funcs = {
    "forestfox": get_forestfox,
}

def get_random_start(game_id, variant_id):
    if game_id in random_start_funcs:
        return random_start_funcs[game_id](variant_id)
    return None