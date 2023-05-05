import random

def get_forestfox(variant_id):
    cards = 'abcdefghijklmno'
    shuffled = ''.join(random.sample(cards, len(cards)))
    return f'R_A_0_0_{shuffled}--00'


random_start_funcs = {
    "forestfox": get_forestfox,
}

def get_random_start(game_id, variant_id):
    if game_id in random_start_funcs:
        return random_start_funcs[game_id](variant_id)
    return None