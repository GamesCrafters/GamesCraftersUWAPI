"""Fail (exit 1) if any registered game is untagged or mis-tagged.

Run from the repository root: python scripts/check_tags.py
This is the same check the server runs at startup; CI runs it on every PR.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
os.environ['UWAPI_TAG_VALIDATION'] = 'strict'

try:
    # Importing the package runs validate_registry, so the error type can't be
    # imported beforehand; recognize it by its `errors` list instead.
    from games import games
except Exception as e:
    if not hasattr(e, 'errors'):
        raise
    print(f'Tag validation failed for {len(e.errors)} problem(s):')
    for error in e.errors:
        print(f'  - {error}')
    print('\nSee docs/tags.md for how to tag a game.')
    sys.exit(1)

from games.tags import game_tags  # noqa: E402

solve = Counter(tag for game in games.values() for tag in game_tags(game)['solve'])
two_player = sum(game.is_two_player_game for game in games.values())
print(f'OK: {len(games)} games validated ({two_player} two-player, {len(games) - two_player} puzzles).')
print('Derived solve tags: ' + ', '.join(f'{tag}={n}' for tag, n in sorted(solve.items())))
