# Game tags

UWAPI is the source of truth for game tags. GamesmanUni's `src/models/gameTags.ts`
was a stopgap and should shrink to display concerns only (chip colors, ordering,
tooltip copy) once the frontend reads tags from the API.

Based on Alvaro Estrella's spec, *Game Tagging System and Tag-Based Search in
GamesmanUni* (GamesmanUni25, 2025). This design keeps the spec's four categories
and makes two changes: style and misc tags are typed enums rather than free text,
and solve and variant tags are generated from registry metadata rather than typed
by hand.

## Categories

| Category | Type | Populated by | Source of truth | Why |
|---|---|---|---|---|
| **style** | `GameStyle` enum | Hand-assigned on each `Game(style=...)` | The game's author | Mechanics (Blocking, Chasing, ...) are a judgment call; no metadata can infer them. The enum stops typos and one-off spellings. |
| **solve** | `SolveTag` enum | **Derived** by `games/tags.py:solve_tags` | Capability flags on `Game` and variants | A solve tag promises the UI will show that data. Hand-entered solve tags drifted: Mancala claimed Win By and Euclid's Game claimed Mex, but neither backend sends that data. |
| **variant** | strings | **Derived** by `variant_tags` | `Game.variants` names, plus `Custom` if `custom_variant` | Enables search by variant (the spec's goal) with zero maintenance; adding a variant adds its tag. |
| **misc** | `MiscTag` enum | Hand-assigned on each `Game(misc=...)` | The group | Editorial labels (Educational). |

### Solve tag rules

| Tag | Applied when |
|---|---|
| `remoteness` | The game is solved (any variant has `solved = True`, the default). Every backend returns remoteness. |
| `winby` | `Game.supports_win_by` (existing flag, already used by `/<game_id>/`). |
| `mex` | `Game.supports_mex`. Must mirror the backend: `gSupportsMex = TRUE` in GamesmanClassic, or a native variant that returns `mex`. |
| `drawanalysis` | `Game.supports_draw_analysis`. No game sets it yet (see open questions). |
| `unsolved` | No variant is solved (`AbstractVariant.solved = False`; set on the chess and Chinese chess tablebase variants). Replaces every other solve tag. |

## API

Additive only: existing fields are unchanged, so the current GamesmanUni keeps working.

- `GET /`: each game gains `tags`.
- `GET /<game_id>/`: gains `tags`.
- `GET /tags/`: the vocabulary (id, label, description per tag), so the
  frontend can build chips and the glossary without hard-coding them.

```json
"tags": {
  "style":   ["impartial"],
  "solve":   ["remoteness", "mex"],
  "variant": ["1 Board", "2 Boards", "3 Boards"],
  "misc":    ["educational"]
}
```

Tag values are stable lowercase ids; use `/tags/` for display labels.

## Validation

`validate_registry(games)` runs at the end of `games/__init__.py`, so a bad
registration fails at import, both on server start and in CI
(`.github/workflows/tags.yml` → `scripts/check_tags.py` + `tests/`).

Rejected:
- a two-player game with no style tags (**untagged**)
- a two-player game without exactly one of `IMPARTIAL` / `PARTISAN`
- a puzzle with two-player style tags
- any style/misc value that isn't the enum (free text)
- duplicate style tags; a game id that collides with an API route (`tags`)

Escape hatch: `UWAPI_TAG_VALIDATION=warn` logs instead of raising. It exists
so a production restart is never blocked by a tag; CI always runs strict.

## Migration from gameTags.ts (ui-update @ 5cbc0e9)

Style and misc tags were carried over for the 81 two-player games that had
entries; puzzles kept misc tags (lightsout, toadsandfrogspuzzle). Solve tags were **not** migrated. They are now derived, which changes:

| Game(s) | Before (gameTags.ts) | Now (derived) | Why |
|---|---|---|---|
| mancala | Win By | Remoteness | `supports_win_by` is False, so Uni never shows win-by for it |
| euclidsgame, oddoreven | Mex | Remoteness | No backend returns mex for them |
| notakto | Remoteness | Remoteness, Mex | `gSupportsMex = TRUE` in mnotakto.c |
| nim, kayles, dawsonschess, 0to10by1or2, chomp, graphgame, tactix | Mex | Remoteness, Mex | They return remoteness too |
| sevenpennies | Impartial / Mex | (no style) / Remoteness | Registered as a puzzle |
| eightball, squirrels, tantrix, tiltago | two-player styles | (no style) | Registered as puzzles |
| abalone, rubiksmagic | none | Partisan + `TODO(tags)` | Needed a parity tag; mechanic still unassigned |
| 3spot, abrobad, change, ghost, horses, jan, jenga, legrec | as entered | as entered + `TODO(tags)` | Marked uncertain by the author |

## Adding a game

```python
'mygame': Game(
    name='My Game',
    style=(GameStyle.BLOCKING, GameStyle.PARTISAN),
    misc=(MiscTag.EDUCATIONAL,),   # optional
    supports_mex=False,            # True only if the backend returns mex
    variants={...}),
```

Then run `python scripts/check_tags.py`.

## Open questions

1. **Puzzle styles.** Every current style describes two-player play, so puzzles
   carry only derived tags and "untagged" can't be enforced for them. Agreeing
   on a puzzle vocabulary (e.g. sliding, placement, path-drawing) would let the
   validator require one.
2. **Draw analysis.** Which backends store draw level/remoteness per game isn't
   recorded anywhere UWAPI can read. A one-time probe of each game's start
   position (does the response carry `drawLevel`?) would populate
   `supports_draw_analysis`; the same probe could verify `supports_mex`.
3. **Win-by per variant.** The unmerged `ae/specify-win-by-by-variant` branch
   moves win-by to variants. When it lands, `solve_tags` should read it per
   variant.
4. **Variant tag volume.** Marble Circuit has 64 variants, so 64 variant tags.
   The frontend should collapse variant tags rather than render them all as chips.
5. **Popular** (spec, dynamic) is deferred until site analytics exist.
6. **Suspect entries** carried over as-is: `tsoroyematatu` is tagged Impartial
   (each player has their own pieces, which suggests Partisan).
