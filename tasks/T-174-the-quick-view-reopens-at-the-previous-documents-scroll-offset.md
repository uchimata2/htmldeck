---
id: T-174
title: The quick view reopens at the previous document's scroll offset, so a source opens 82% of the way down
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-122, T-168, T-128]
work_package: PH1
owner: the project owner
business_value: high
effort: xs
created: 2026-08-17
updated: 2026-08-17
deliverables:
  - shell/deck.js
---

# T-174 — The quick view reopens at the previous document's scroll offset

## 1. Specify

**Outcome**
The quick view opens at the top of the document it was asked for, every time. Today it opens
wherever the *previous* document was left, including when the reader has never seen the new one.

**Found by looking, 2026-08-17.** The owner opened the source list and the quick view on
`examples/measure-first/measure-first.html` and reported that the viewer keeps its scroll position
between openings. Reproduced and measured in the same session, on the same deck:

| Step | `.qv-body` `scrollTop` | `scrollHeight` |
| :--- | ---: | ---: |
| D5 open, reader scrolls down | 9,624 | 10,816 |
| `qvClose` clicked | 0 | 0 |
| **D2 opened — a different document, first time** | **9,774.7** | 11,920 |

So the reader asks for D2 and lands **82% of the way down** a document they have not seen. The first
screenful they get is the middle of somebody else's table.

**The clear at close is not the bug, and that is why it survived.**
[`shell/deck.js`](../shell/deck.js) `closeQuick()` already empties the surface —
`qvBody.textContent = ''`, commented *the surface holds nothing between openings* — and the measured
`scrollTop` after that line **is** 0. The offset comes back when `openQuick()` appends the next
article into the same scroll container: the browser restores the scroll position of an element whose
content returns. Neither function ever assigns `scrollTop`, so nothing contradicts the restore.

The two figures differ (9,624 → 9,774.7) because the restore is against the new document's height,
which is further evidence it is the browser acting rather than a value the deck carried.

**Why this is `PH1`.** It is behaviour in the shipped shell, in the published plugin, reachable by
every deck any adopter builds — the quick view is how a deck shows the source its argument rests on
(DS-105). A reader who cannot see the top of a quoted source cannot tell what they are being shown.

**Why nothing here could have caught it.** No gate opens the quick view twice. `check.py` reads
structure, `theme.py` reads tokens, `audit.py` measures a rendered slide — a stale scroll offset
exists only in the second interaction, which is `CLAUDE.md` rule 6's territory and nothing else's.
Same shape as [T-168](T-168-sources-open-ships-with-no-minimum-target-size.md), found in the same
deck, on the same afternoon: the two defects a person found by opening the thing.

**Scope**
- In: the quick view opens at the top of its document, in the stage and in the reading view.
- Out: remembering a per-document position deliberately — that is a feature, and not one asked for.
- Watch: `openQuick()` focuses `#qvClose` at the end; a scroll reset must not fight that focus, and
  focusing a control inside a scroll container can itself scroll it.
- Watch: the reading view clones the controls, so the fix must hold for the clones — the delegated
  listener is shared and the map is keyed off the stage's templates.

**Inputs**
- [`shell/deck.js`](../shell/deck.js) — `openQuick()` / `closeQuick()`.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-105, what the quick view is for.

**Acceptance criteria**
- [ ] Opening any source after any other source starts at `scrollTop` 0, measured rather than assumed
- [ ] The same holds in the reading view, where the controls are clones
- [ ] `#qvClose` still holds focus when the view opens
- [ ] All three shipped decks are re-synced and `shell.py check` passes on each; the seeded-defects
      fixture is **regenerated, not synced** (**L-77**)
- [ ] The quick view is opened twice in a row and **looked at**, offline

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reset the offset in `openQuick()`, after the article is appended and around the focus call | the shell change |
| 2 | Re-measure the three-step sequence above — expect `0` at the third row | the evidence |
| 3 | `shell.py sync --write` on the three shipped decks; regenerate the seeded-defects fixture (**L-77**) | four files in step |
| 4 | Open two sources in a row and **look**, in the stage and in the reading view, offline | the judgement |

## 3. Implement

**Decisions & assumptions**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-17 | → proposed | **Found by the owner looking at the deck, while [T-168](T-168-sources-open-ships-with-no-minimum-target-size.md) was being looked at for the same reason.** Reproduced and measured the same session: D2 opens at `scrollTop` 9,774.7 of 11,920 having never been opened. The clear in `closeQuick()` works and is not the fault — the browser restores the offset when `openQuick()` refills the container, and neither function assigns `scrollTop`. `PH1` because it is shipped behaviour in the published shell; `xs` because the fix is an assignment, and the cost is the sync and the second look rather than the change. |
