"""
Game tags: typed vocabulary, derivation, and registry validation.

Tags come in four categories (see docs/tags.md for the full rationale):

- style   -- hand-assigned GameStyle members declared on each Game.
- solve   -- derived from what the game's backend actually provides
             (Game.supports_win_by, Game.supports_mex, ...). Never hand-entered.
- variant -- derived from the game's variants (one per variant, plus
             'Custom' when custom variants can be created). Never hand-entered.
- misc    -- hand-assigned MiscTag members declared on each Game.

`validate_registry` runs when `games` is imported, so an untagged or
mis-tagged game fails at registration (and in CI) instead of shipping.
"""

import logging
import os
from enum import Enum


class GameStyle(str, Enum):
    """Fundamental mechanics or player interactions of a two-player game."""
    BLOCKING = 'blocking'
    REARRANGER = 'rearranger'
    DARTBOARD = 'dartboard'
    CHASING = 'chasing'
    IMPARTIAL = 'impartial'
    PARTISAN = 'partisan'
    CONNECTION = 'connection'
    MAJORITY_CONTROL = 'majoritycontrol'


class SolveTag(str, Enum):
    """What solving data is available. Derived, never declared."""
    REMOTENESS = 'remoteness'
    WIN_BY = 'winby'
    MEX = 'mex'
    DRAW_ANALYSIS = 'drawanalysis'
    UNSOLVED = 'unsolved'


class MiscTag(str, Enum):
    EDUCATIONAL = 'educational'


LABELS = {
    GameStyle.BLOCKING: 'Blocking',
    GameStyle.REARRANGER: 'Rearranger',
    GameStyle.DARTBOARD: 'Dartboard',
    GameStyle.CHASING: 'Chasing',
    GameStyle.IMPARTIAL: 'Impartial',
    GameStyle.PARTISAN: 'Partisan',
    GameStyle.CONNECTION: 'Connection',
    GameStyle.MAJORITY_CONTROL: 'Majority Control',
    SolveTag.REMOTENESS: 'Remoteness',
    SolveTag.WIN_BY: 'Win By',
    SolveTag.MEX: 'Mex',
    SolveTag.DRAW_ANALYSIS: 'Draw Analysis',
    SolveTag.UNSOLVED: 'Unsolved',
    MiscTag.EDUCATIONAL: 'Educational',
}

DESCRIPTIONS = {
    GameStyle.BLOCKING: 'Players win by blocking opponent moves.',
    GameStyle.REARRANGER: 'Players only move existing pieces.',
    GameStyle.DARTBOARD: 'Players only add pieces to the board.',
    GameStyle.CHASING: 'One player is pursuing another.',
    GameStyle.IMPARTIAL: 'The same moves are available to both players.',
    GameStyle.PARTISAN: 'The players have different moves available.',
    GameStyle.CONNECTION: 'Players win by connecting their pieces.',
    GameStyle.MAJORITY_CONTROL: 'Players win by holding more pieces or territory than the opponent.',
    SolveTag.REMOTENESS: 'Remoteness (moves remaining under perfect play) was stored when solving.',
    SolveTag.WIN_BY: 'Win-by (final score margin under perfect play) was stored when solving.',
    SolveTag.MEX: 'Positions carry mex (nimber) values.',
    SolveTag.DRAW_ANALYSIS: 'Draw level and draw remoteness were stored when solving.',
    SolveTag.UNSOLVED: 'The game is not solved; only partial data (e.g. endgame tables) is available.',
    MiscTag.EDUCATIONAL: 'Used for teaching and demonstration.',
}

# Every current style describes two-player play; puzzles get none until a
# puzzle style vocabulary is agreed on (see docs/tags.md, "Open questions").
TWO_PLAYER_ONLY_STYLES = frozenset(GameStyle)
PARITY_STYLES = frozenset({GameStyle.IMPARTIAL, GameStyle.PARTISAN})
RESERVED_GAME_IDS = frozenset({'tags'})


def solve_tags(game) -> list:
    if not game.is_solved:
        return [SolveTag.UNSOLVED]
    tags = [SolveTag.REMOTENESS]
    if game.supports_win_by:
        tags.append(SolveTag.WIN_BY)
    if game.supports_mex:
        tags.append(SolveTag.MEX)
    if game.supports_draw_analysis:
        tags.append(SolveTag.DRAW_ANALYSIS)
    return tags


def variant_tags(game) -> list:
    names = list(dict.fromkeys(variant.name for variant in game.variants.values()))
    if game.custom_variant:
        names.append('Custom')
    return names


def game_tags(game) -> dict:
    """The API representation of a game's tags."""
    return {
        'style': [tag.value for tag in game.style],
        'solve': [tag.value for tag in solve_tags(game)],
        'variant': variant_tags(game),
        'misc': [tag.value for tag in game.misc],
    }


def vocabulary() -> dict:
    """Every tag value with its display label and description, by category."""
    def entries(enum):
        return [{'id': tag.value, 'label': LABELS[tag], 'description': DESCRIPTIONS[tag]} for tag in enum]
    return {
        'style': entries(GameStyle),
        'solve': entries(SolveTag),
        'variant': [],  # open set: one tag per variant name, plus 'Custom'
        'misc': entries(MiscTag),
    }


class TagValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__('Game tag validation failed:\n' + '\n'.join(f'  - {e}' for e in errors))


def registry_errors(games: dict) -> list:
    errors = []
    for game_id, game in games.items():
        where = f"'{game_id}'"
        if game_id in RESERVED_GAME_IDS:
            errors.append(f'{where}: game id is reserved for an API route')
        bad_style = [t for t in game.style if not isinstance(t, GameStyle)]
        bad_misc = [t for t in game.misc if not isinstance(t, MiscTag)]
        for tag in bad_style:
            errors.append(f'{where}: style tag {tag!r} is not a GameStyle (free-text tags are not allowed)')
        for tag in bad_misc:
            errors.append(f'{where}: misc tag {tag!r} is not a MiscTag (free-text tags are not allowed)')
        if len(set(game.style)) != len(game.style):
            errors.append(f'{where}: duplicate style tags')
        styles = set(game.style)
        if game.is_two_player_game:
            if not styles:
                errors.append(f'{where}: untagged; declare style=(GameStyle...) including IMPARTIAL or PARTISAN')
            elif len(styles & PARITY_STYLES) != 1:
                errors.append(f'{where}: style must include exactly one of GameStyle.IMPARTIAL / GameStyle.PARTISAN')
        else:
            two_player = sorted(t.value for t in styles & TWO_PLAYER_ONLY_STYLES)
            if two_player:
                errors.append(f'{where}: puzzle has two-player style tags {two_player}')
    return errors


def validate_registry(games: dict) -> None:
    """Raise TagValidationError on any registry tag error.

    Set UWAPI_TAG_VALIDATION=warn to log instead of raise. This is an
    emergency escape hatch for a production restart; CI always runs strict.
    """
    errors = registry_errors(games)
    if not errors:
        return
    if os.environ.get('UWAPI_TAG_VALIDATION', 'strict').lower() == 'warn':
        logging.getLogger(__name__).warning(str(TagValidationError(errors)))
        return
    raise TagValidationError(errors)
