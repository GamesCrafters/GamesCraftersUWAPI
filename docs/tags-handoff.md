# Tag system handoff

For Nahee, picking up the tagging workload. Written 2026-09-22 by Allena.
The design and rationale are in [tags.md](tags.md); this is state, ownership
and the work queue.

## Progress (Nahee)

- **2026-09-25**: Branch `feature/typed-tags` is now on `origin` (pushed since
  this doc was written; local branch is up to date with it, HEAD at `002b0b3`,
  one commit past this doc's `fbb4622`). No remote-add/bundle step was needed.
  Re-ran verification locally: `check_tags.py` → `OK: 112 games validated (83
  two-player, 29 puzzles)`, derived tags `mex=8, remoteness=110, unsolved=2,
  winby=1` (matches this doc's expected numbers); `pytest tests -q` → 10/10
  pass. Still open: whether the GitHub Action has run now that the branch is
  pushed, and the live-backend checks (need campus network/VPN).
  Next: work queue item 1 (review the 10 `TODO(tags)` games).

## Status

| | |
|---|---|
| Branch | `feature/typed-tags`, commit `fbb4622`, cut from `master` `cd25c7b` |
| Pushed? | **Yes**, as of 2026-09-25 (was no, as of 2026-09-22, when this doc was written) |
| Verified | `scripts/check_tags.py` passes on all 112 games; 10 tests pass; the check exits 1 on a deliberately untagged game. Re-confirmed by Nahee on 2026-09-25. |
| Not verified | Whether the GitHub Action has run now that the branch is pushed (check `gh`/Actions tab). No live-backend checks yet: `nyc.cs.berkeley.edu` is unreachable off campus |

~~Nothing you forked contains this branch. Get it before writing any tag code,
or you will rebuild it.~~ Done — branch is pulled and pushed to origin.

```bash
# after Allena pushes:
git remote add upstream https://github.com/GamesCrafters/GamesCraftersUWAPI.git
git fetch upstream feature/typed-tags && git checkout -b typed-tags upstream/feature/typed-tags
# or, from the bundle file Allena sends:
git fetch ../uwapi-typed-tags.bundle feature/typed-tags:typed-tags
```

Run it (macOS/Linux: `bin/` instead of `Scripts/`):

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt pytest
.venv/bin/python scripts/check_tags.py
.venv/bin/python -m pytest tests -q
```

## Who owns what

Proposed, so we don't collide:

| Area | Owner |
|---|---|
| UWAPI tags: schema, validation, CI, backfill | **Nahee** |
| Reviewing the 10 `TODO(tags)` entries | **Nahee** (game-by-game judgment) |
| Merging `ui-update` into Uni `main` | Allena |
| Uni reading tags from the API (week 10) | Allena |
| The `/tags/` response shape | Joint: it's the contract between us. Change it in a PR we both look at. |

## Already decided — please don't redo

- **Four categories** from Alvaro's spec: style, solve, variant, misc.
- **style and misc are typed enums** (`GameStyle`, `MiscTag`), declared per game.
  Free text is rejected. This is what stops the typo drift.
- **solve and variant tags are derived, never hand-entered.** Solve tags come
  from capability flags (`supports_win_by`, `supports_mex`,
  `supports_draw_analysis`, `AbstractVariant.solved`); variant tags come from
  variant names plus `Custom`. Hand-entered solve tags are exactly what broke
  nine games (Mancala tagged Win By with win-by off, Notakto missing Mex, and so on).
- **The API is additive**: `tags` on `/` and `/<game_id>/`, plus `/tags/` for
  the vocabulary. The current frontend is unaffected, so this can merge before
  any Uni change.
- **Validation runs at import**, so a bad registration fails on server start and
  in CI. `UWAPI_TAG_VALIDATION=warn` downgrades it to a log line; CI is always strict.

## Open decisions

1. **Puzzle style vocabulary.** Every current style describes two-player play,
   so puzzles carry only derived tags and "untagged" cannot be enforced for
   them. Until the group picks a vocabulary (sliding? placement? path-drawing?),
   10 untagged puzzles stay untagged and filters can't tell puzzles apart.
   This is the biggest open item and it needs the group, not a coder.
2. **Should validation block server startup?** It does now, with the `warn`
   escape hatch. If people deploy by hand, consider requiring the check via
   branch protection so `master` can't get a bad game in the first place.
3. **Variant tag volume.** Marble Circuit has 64 variants, so 64 variant tags.
   The frontend needs to collapse them; they shouldn't all render as chips.
4. **Popular** (from the spec) stays deferred until site analytics exist.

## Work queue

### 1. Review the 10 `TODO(tags)` entries

Eight were marked uncertain by the original author; two (Abalone, Rubik's Magic)
had no entry at all and were given `PARTISAN` because that much is certain.
Each needs a mechanic tag, or confirmation that what's there is right. For a
GamesmanClassic game, `GamesmanClassic/src/m<id>.c` has the rules in its header
comment. Note `kPartizan` in those files is unreliable — several clearly
partisan games declare `kPartizan = FALSE`, which is why parity isn't derived.

| Game | Current style | What to check |
|---|---|---|
| 3-Spot | dartboard, partisan | Is it really placement-only? |
| Abrobad | blocking, partisan | Confirm the win condition is blocking |
| Change! | partisan | No mechanic tag yet |
| Ghost | partisan | Word game; may need no mechanic tag |
| Horses | rearranger, partisan | GamesmanPy game; confirm pieces only move |
| Jan | partisan | No mechanic tag yet |
| Jenga | impartial | Verify impartial: are both players' moves identical? |
| Le Grec | partisan | No mechanic tag yet |
| Abalone | partisan | Needs a mechanic tag; likely majority control |
| Rubik's Magic | partisan | Needs a mechanic tag |

### 2. Verify the capability flags against live backends

Needs the campus network or VPN. For each game, request the start position and
look at the response keys:

- `mex` present → `supports_mex=True`. Expected: exactly 8 games
  (0to10by1or2, chomp, dawsonschess, graphgame, kayles, nim, notakto, tactix).
  Anything else means the flag list is wrong.
- `drawLevel` present → `supports_draw_analysis=True`. **No game sets this
  today**, and it isn't recorded anywhere UWAPI can read, so Draw Analysis is
  on 0 games and the chip in Uni's filter bar does nothing. A probe is the only
  way to populate it.

A script that walks `games` and reports the diff between flags and reality is
worth writing once; it can then run each semester.

### 3. Tag the 11 games that have none

Abalone (a two-player game) needs a mechanic tag. The other 10 are puzzles and
are blocked on decision 1: Stormy Seas, Flow Free, Hashi, Klotski, Lunar
Lockout, Marble Circuit, Snake's Tale, Sokoban (all Spring 2026), plus Hop N'
Drop and Sliding Number Puzzle (2024).

### 4. When `ae/specify-win-by-by-variant` merges

That branch moves win-by from the game to the variant. `solve_tags()` in
`games/tags.py` reads `game.supports_win_by`; it should then read per variant.
The Othello work (UWAPI #99) is waiting on that branch too.

## The files

| File | What it holds |
|---|---|
| `games/tags.py` | The enums, `solve_tags` / `variant_tags` / `game_tags`, `vocabulary()`, and `registry_errors` / `validate_registry` |
| `games/models.py` | `style` / `misc` and the capability flags on `Game`; `solved` on `AbstractVariant`; `Game.is_solved` |
| `games/__init__.py` | Per-game `style=` / `misc=` / `supports_mex=`; `validate_registry(games)` at the bottom |
| `server.py` | `tags` on `/` and `/<game_id>/`; the `/tags/` route |
| `scripts/check_tags.py` | The CI entry point; prints the errors and exits 1 |
| `tests/test_tags.py` | 10 tests: validation rules, derivation, API shape |
| `.github/workflows/tags.yml` | Runs the check and the tests on every PR |
| `docs/tags.md` | The schema, migration notes, open questions |

## Gotchas

- **`games/__init__.py` conflicts easily.** The tags are new kwargs inserted
  after each game's `name=` line. Every in-flight game branch touches this file,
  so merge it early rather than late.
- **The repo is CRLF.** Write files with a tool that preserves it; a whole-file
  ending flip makes the diff unreadable.
- **`import games` runs validation**, so a broken registry raises before
  anything else imports. `scripts/check_tags.py` catches it by the `errors`
  attribute rather than the exception type, since the type lives in the package
  that's failing to import.
- **Run tests from the repo root** (`python -m pytest tests -q`), which puts the
  root on `sys.path`.
- **`tags` is a reserved game id** now that `/tags/` exists; validation rejects it.

## Baseline to measure against

From the Week 5 coverage audit, against `gameTags.ts` before this branch:

- 112 registered games: 83 two-player, 29 puzzles.
- 88% had complete tags; 73% had complete tags that survived verification.
- 11 had none; 8 of the 13 games added in 2026 had none.
- 9 games carried tags that contradicted the registry or the backends. Deriving
  solve tags fixes all 9.

Re-running the audit after the backfill is the honest way to show progress.
