import os
from anim.alang import CustomAnimations, DodgemAnimations

dirname = os.path.dirname(__file__)

# mapping of animations to conditions checker
animations = {
    "dodgem": DodgemAnimations({"falling": os.path.join(dirname, "games", "dodgem", "fall.al")}),
    # * don't care
    # ~ position

    # Positions for 4x4:
    # (1) (2) (3) (4)
    # (*) (*) (*) (8)
    # (9) (10) (*) (12)
    # (13) (14) (*) (16)
}

def match(game_id) -> (bool, CustomAnimations):
    """ Matches game and variant id to determine if you need custom animations"""
    return game_id in animations.keys(), animations[game_id]
