---
id: T-174
title: The quick view reopens at the previous document's scroll offset, so a source opens 82% of the way down
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-122, T-168, T-128, T-172]
work_package: PH1
shipped_in: 0.3.0
owner: the project owner
business_value: high
effort: xs
created: 2026-08-17
updated: 2026-08-17
deliverables:
  - shell/deck.js
  - examples/reference-deck.html
  - examples/sort-window/sort-window.html
  - examples/measure-first/measure-first.html
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
- 2026-08-17 — **the reset goes in `openQuick()`, not in `closeQuick()`.** The owner's report asked
  for it on close *or* on open; measurement decides between them. `closeQuick()`'s existing
  `qvBody.textContent = ''` already takes `scrollTop` to 0 — there is nothing left to scroll — and
  the offset comes back anyway, because the browser restores it when content returns to the same
  element. **A second reset on close would have measured green in isolation and fixed nothing.**
  Placed after `qv.hidden = false`, because a hidden element has no scroll height to assign against.
- 2026-08-17 — **§1's focus *Watch* is answered by the markup, not by ordering.** Focusing a control
  can scroll its scrollable ancestors, but `qvClose` sits in `.qv-head`, a **sibling** of
  `.qv-body` rather than a descendant ([`shell/shell.html`](../shell/shell.html) lines 100–106), so
  it cannot scroll the body whichever order the two lines take. Verified anyway:
  `document.activeElement` is `qvClose` after the sequence below.
- 2026-08-17 — **`shell.py check` on the seeded-defects fixture is not that file's gate, and its two
  reports were read as noise rather than as a regression.** It reports `COMPONENTS differs` and an
  `ICONS` mismatch, and the same two are reported against the pre-change copy from `HEAD`. That file
  is an **output**; its gate is `seed_defects.py --check`, which passes. This is **L-77** read in the
  other direction — the check that only owns part of a file should not be believed about the rest.

**What was done.** One assignment and its comment in [`shell/deck.js`](../shell/deck.js)
`openQuick()`, then `sync --write` on the three shipped decks — `SCRIPT` 847 → 861 lines on each,
one region synced and twelve per-deck regions untouched in every case. The seeded-defects fixture was
**regenerated** with `seed_defects.py`, not synced (**L-77**), and `seed_defects.py --check` passes.

**Measured on `examples/measure-first/measure-first.html`, the deck that raised it.** Same three-step
sequence as §1, re-run against the fix:

| Step | before | after |
| :--- | ---: | ---: |
| D5 open, scrolled to the end | 9,624 | 9,779 |
| **D2 opened — a different document** | **9,774.7** | **0** |
| **D5 opened again — the same document** | not measured | **0** |
| the reading view's 20 cloned controls | not measured | **0** |
| `document.activeElement` after opening | — | `qvClose` |

The reading view was measured separately rather than argued from the delegated listener: the clones
are made by `buildDoc()` after the handler binds, which is the case the handler's own comment says it
exists for, and a fix that held only on the stage would fail exactly the reader who is alone with the
deck.

**The sync falsified seven published figures, and they were corrected here rather than sent onward.**
`check_all.py` went red at `figures.py` — the three decks changed size again, so the pages quoting
them went stale again. This is
[T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md)'s defect a second time, five
numerals in the same three files plus two the root `README.md` states without binding. It was a
separate task then because T-128's authorisation was bounded to one line; nothing bounds this one,
and a task whose entire content is *re-run the correction T-172 already made* is a record with no
reader. Corrected: `README.md` 263→264 KB and 260→261 KB, `docs/BRIEF.md` 263→264 KB,
`examples/README.md` 263→264 KB / 269 083→270 230 bytes and 260→261 KB / 266 324→267 471 bytes. Every
value read off `figures.py`'s own report, not off another document.

**Worth saying because it is now twice:** every shell change falsifies these figures, `figures.py`
catches all of them, and correcting them is manual each time. The gate is doing its job — this is a
note about cost, not a defect, and not this task's to solve.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Opening any source after any other starts at `scrollTop` 0, measured | **met** | D2 after a scrolled D5: **0** of 11,920, against 9,774.7 before. The same document reopened is **0** too |
| The same holds in the reading view, where the controls are clones | **met** | Measured separately across its 20 cloned controls: **0** |
| `#qvClose` still holds focus when the view opens | **met** | `document.activeElement` is `qvClose` after the sequence. The markup settles it — `qvClose` is a sibling of `.qv-body`, not a descendant |
| Three decks re-synced, `shell.py check` passes on each; the fixture regenerated, not synced | **met** | `SCRIPT` 847→861 lines on each, one region synced, twelve per-deck regions untouched. Fixture regenerated; `seed_defects.py --check` passes |
| The quick view is opened twice in a row and **looked at**, offline | **met** | Both cases, with real clicks on the stage: D2 scrolled deep then reopened — top. D5 opened after it — top. Each showed its own first heading and its scrollbar at the top |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-17 | → done | **Raised, fixed, synced and looked at the same day.** One assignment in `openQuick()`; the owner's report offered *close or open* and measurement picked open, because the clear on close already reaches 0 and the browser restores the offset when content returns — **a reset on close would have gone green in isolation and fixed nothing.** D2 after a scrolled D5 goes 9,774.7 → **0**, the reading view's 20 clones with it, focus unmoved. Looked at twice on the stage with real clicks: each document opened showing its own first heading. Two costs recorded in §3 rather than passed on — the sync falsified seven published figures for the second time (T-172's defect again, corrected here), and `shell.py check` on the seeded fixture reports two problems that are **L-77** in the other direction, present on the pre-change copy too. |
| 2026-08-17 | → proposed | **Found by the owner looking at the deck, while [T-168](T-168-sources-open-ships-with-no-minimum-target-size.md) was being looked at for the same reason.** Reproduced and measured the same session: D2 opens at `scrollTop` 9,774.7 of 11,920 having never been opened. The clear in `closeQuick()` works and is not the fault — the browser restores the offset when `openQuick()` refills the container, and neither function assigns `scrollTop`. `PH1` because it is shipped behaviour in the published shell; `xs` because the fix is an assignment, and the cost is the sync and the second look rather than the change. |
