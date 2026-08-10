---
id: T-085
title: The reference deck does not carry the shell it defines, and its sprite is out of sync
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-069, T-071, T-078, T-083]
work_package: v0.1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-10
updated: 2026-08-10
deliverables:
  - examples/reference-deck.html
  - examples/reference-deck-seeded-defects.html
---

# T-085 — The reference deck does not carry the shell it defines, and its sprite is out of sync

## 1. Specify

**Outcome**
`python tools/deck/shell.py check examples/reference-deck.html` is green, so the deck the repository
calls its structural reference is the deck `shell/` describes.

**Why this one**
Found 2026-08-10 while running [`PUBLISHING.md`](../docs/PUBLISHING.md) §8's gate list to ship
`v0.1.5`. Two problems, both on the deck every other deck is assembled from:

    COMPONENTS    examples/reference-deck.html: differs from shell/components.css
    ICONS         examples/reference-deck.html: the sprite is not the icons this deck uses (DS-113)

**The third instance of one failure in one day, and the third deck-facing gate nobody ran.**
[T-071](T-071-the-intermediate-specifications-carry-their-references.md) found `examples/sort-window/`
stale against the same file; [T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md)
found a `hard` rule failing on it. All three were invisible for the same structural reason: the
README prints repository-wide commands, and the per-deck gates were in nobody's routine until §8
listed them.

**How it happened is worth stating, because it is not carelessness.** `shell/` is cut losslessly out
of this deck, so the two are meant to be one fact in two files.
[T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) reworded a comment in
`shell/components.css` and then, two commits later, edited the deck's markup — without writing the
shell back into it. The divergence is a comment, which changes no rendering and is exactly why
nothing looked wrong.

**Scope**
- In: writing `shell/components.css` back into the deck's component region, and syncing its sprite.
- In: the direction of truth, stated. `shell/` is the home and the deck is an instance of it, on
  `shell.py`'s own account of itself — the deck is what gets rewritten.
- Out: `examples/sort-window/`, resynced in T-071 and green.
- Out: the missing routine, which is [`PUBLISHING.md`](../docs/PUBLISHING.md) §8 and already written.

**Inputs**
- `python tools/deck/shell.py check examples/reference-deck.html` — the two problems, by name.
- [`tools/deck/shell.py`](../tools/deck/shell.py) — `cut`, `fill` and `SCRIPT_SLOTS`; the per-deck
  declarations have to survive the rewrite.

**Acceptance criteria**
- [ ] `shell.py check` is green on the reference deck, and its three per-deck declarations are unchanged
- [ ] The sprite holds the icons the deck uses and no others
- [ ] Every other gate that reads this deck stays green, including the seeded-defect fixture that
      derives from it
- [ ] Nothing in the deck's rendering changed — the divergence was a comment, and if anything visible
      moves, that is a different finding

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Write `shell/components.css` into the deck, preserving `DECK_NAME`, `STAGES` and `STAGE_ICON` | the deck |
| 2 | Sync the sprite | the deck |
| 3 | Re-run every gate that reads this deck, the seeded fixture included | this file §4 |

## 3. Implement

**Decisions & assumptions**
- **`shell/` is the home and the deck is rewritten from it** — 2026-08-10, as scoped. `shell.py`'s own
  `cut` docstring settles the direction: filling the skeleton reproduces the deck exactly, *"and that
  property is what makes calling `shell/` the deck's one home rather than a description of it."* The
  deck is an instance; the instance loses.
- **The per-deck declarations were asserted identical, not assumed.** `DECK_NAME`, `STAGES` and
  `STAGE_ICON` were cut out of the deck's script before the rewrite and cut back out afterwards and
  compared; the resync refuses if they differ. Those three are the only per-deck facts inside a
  region otherwise made of shell, which is exactly the class of thing a wholesale overwrite loses.

**What actually changed — two lines**

    -/* provenance, upper right, plain text because the source is the model itself (DS-105) */
    +/* provenance, upper right; plain text where one source carries the slide (DS-105) */
    -<symbol id="i-source" …>
    +<symbol id="i-source" …>

**A comment and a sprite entry.** Nothing rendered differently before the fix and nothing does after
it, which is the whole reason it survived: there was no symptom, only a gate nobody ran. The sprite
line is a normalisation, not a new icon — the deck holds the same ten it used.

**Outputs produced**
- `examples/reference-deck.html` — the shipped component block and a synced sprite.
- `examples/reference-deck-seeded-defects.html` — regenerated, since it derives from the deck. Four
  lines, the same two changes seen twice.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `shell.py check` is green, and the three per-deck declarations are unchanged | met | `OK - examples/reference-deck.html carries the shipped shell unchanged, and its sprite is the icons it uses.` The declarations were compared programmatically either side of the rewrite. |
| The sprite holds the icons the deck uses and no others | met | `sprite now holds 10 icon(s): i-wait, i-bike, i-bus, i-source, i-cost, i-window, i-gate, i-choice, i-growth, i-ask`. |
| Every other gate that reads this deck stays green, the seeded fixture included | met | `component.py`, `theme.py` and `check.py --sources` all green — `0 failure(s): none`. The fixture regenerated and `--check` reports it is exactly what regenerating produces. |
| Nothing in the deck's rendering changed | met | The diff is two lines: a CSS comment and a normalised `<symbol>` attribute order. Neither can move a pixel, which is why nothing had noticed. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | Two commands, two changed lines, and neither could render differently — which is the finding rather than the fix. **`shell/` and this deck are one fact in two files by design, and the design has no watcher except a command nobody ran.** Three decks-worth of the same failure in one day says the routine was the defect, not the deck: `PUBLISHING.md` §8 now lists the per-deck gates and names both examples, since running them against the deck being worked on is what let this one sit. Shipped in **`v0.1.5`**. |
| 2026-08-10 | → proposed | Raised while running §8's gate list for the `v0.1.5` release. `v0.1` rather than `v0.2`: the deck is in the published repository, `README.md` points at it as the structural reference, and an adopter running the documented command on it gets a red run — CLAUDE.md's own test. `high` because it is the deck every other deck is assembled from; `xs` because the fix is the same two commands T-071 used on the other example. |
