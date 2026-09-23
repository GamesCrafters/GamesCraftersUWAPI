import pytest

from games import games
from games.models import Game, Variant
from games.tags import (GameStyle, MiscTag, SolveTag, TagValidationError,
                        game_tags, registry_errors, validate_registry)


def make_game(**kwargs):
    kwargs.setdefault('name', 'Dummy')
    kwargs.setdefault('variants', {'regular': Variant('Regular', None, 'dummy', 'regular')})
    return Game(**kwargs)


def test_registry_is_valid():
    assert registry_errors(games) == []


def test_untagged_two_player_game_is_rejected():
    with pytest.raises(TagValidationError) as exc:
        validate_registry({'dummy': make_game()})
    assert "'dummy': untagged" in str(exc.value)


def test_free_text_tags_are_rejected():
    errors = registry_errors({'dummy': make_game(style=('Blocking', GameStyle.PARTISAN), misc=('educational',))})
    assert any('not a GameStyle' in e for e in errors)
    assert any('not a MiscTag' in e for e in errors)


def test_two_player_game_needs_exactly_one_parity_tag():
    assert registry_errors({'dummy': make_game(style=(GameStyle.BLOCKING,))})
    assert registry_errors({'dummy': make_game(style=(GameStyle.IMPARTIAL, GameStyle.PARTISAN))})
    assert registry_errors({'dummy': make_game(style=(GameStyle.BLOCKING, GameStyle.PARTISAN))}) == []


def test_puzzle_cannot_have_two_player_styles():
    puzzle = make_game(is_two_player_game=False, style=(GameStyle.CHASING,))
    assert any('puzzle has two-player style tags' in e for e in registry_errors({'dummy': puzzle}))
    assert registry_errors({'dummy': make_game(is_two_player_game=False)}) == []


def test_reserved_game_id_is_rejected():
    assert registry_errors({'tags': make_game(style=(GameStyle.PARTISAN,))})


def test_warn_mode_logs_instead_of_raising(monkeypatch):
    monkeypatch.setenv('UWAPI_TAG_VALIDATION', 'warn')
    validate_registry({'dummy': make_game()})


def test_solve_tags_are_derived_from_capabilities():
    assert game_tags(games['othello'])['solve'] == [SolveTag.REMOTENESS, SolveTag.WIN_BY]
    assert SolveTag.MEX in game_tags(games['nim'])['solve']
    assert SolveTag.MEX in game_tags(games['notakto'])['solve']
    assert game_tags(games['chess'])['solve'] == [SolveTag.UNSOLVED]
    assert game_tags(games['mancala'])['solve'] == [SolveTag.REMOTENESS]


def test_variant_tags_are_derived_from_variants():
    assert game_tags(games['nim'])['variant'][-1] == 'Custom'
    tags = game_tags(games['stormyseas'])['variant']
    assert tags == [v.name for v in games['stormyseas'].variants.values()]


def test_api_exposes_tags():
    from server import app
    client = app.test_client()
    listing = client.get('/').get_json()
    assert len(listing) == len(games)
    assert all(set(g['tags']) == {'style', 'solve', 'variant', 'misc'} for g in listing)
    assert client.get('/nim/').get_json()['tags']['misc'] == [MiscTag.EDUCATIONAL]
    vocab = client.get('/tags/').get_json()
    assert {t['id'] for t in vocab['style']} == {s.value for s in GameStyle}
