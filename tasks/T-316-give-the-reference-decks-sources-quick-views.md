---
id: T-316
title: Give the reference deck's sources quick views
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-233]
work_package: PH3
shipped_in: 1.0.0
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: [examples/reference-deck.html, tools/deck/quickview.py]
---

# T-316 — Give the reference deck's sources quick views

## 1. Specify

**Outcome**
Every source the reference deck names opens its document in the quick view. Today its provenance
marks list `Cost model`, `Ridership model` and the programme timetable as plain text:
`quickview.py list examples/reference-deck.html` reports 0 quick views, while `examples/sources/`
holds all three documents.

**Why it was passive.** Not a token saving. The deck was built by hand before the quick view existed
([T-070](T-070-the-quick-view-for-a-source-document.md)), and no later task attached them;
the three decks built afterwards all carry them.

**Raised by** the owner's observation beside the B27 looks, 2026-09-14: sources should almost never be
passive text.

**Scope**
- In: attach the three sources with `quickview.py add`, and whatever the addition costs the gates and
  the fixture derived from this deck
- Out: a rule that a source with a file must open it, which is a wider question than one deck

**Acceptance criteria**
- [x] `quickview.py list` names three quick views, and `quickview.py check` passes against
      `examples/sources/`
- [x] the look is recorded as owed
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `quickview.py plan` the three sources | §3 |
| 2 | `quickview.py add` them, then `list` and `check` | `examples/reference-deck.html` |
| 3 | Regenerate the fixture, correct the figures, record the look, lint, gate | §3 |

## 3. Implement

**Decisions & assumptions**
- The three sources are embedded with `quickview.py add`, the tool the other three decks were built
  with, rather than wired by hand. Reversible. — 2026-09-14
- The rule the owner's observation suggests, that a deck whose source file was supplied must open it,
  is not written here. It would bind every adopter's deck on a question the scope keeps out.
  Reversible. — 2026-09-14
- **Found and fixed in place: `quickview.py add` left the deck failing DS-009.** An embedded
  `<template>` is a capability the preflight has to test, and `add` wrote the templates without
  rewriting the preflight, so `check.py` failed the deck until `shell.py preflight` ran by hand. `add`
  and `refresh` now rewrite the preflight in the same write. It is a small fix to the tool this task
  used, so it is made here rather than raised. Reversible. — 2026-09-14
- **Found and fixed in place: `add` left two of the deck's items unwired.** `ITEM_HEAD` read a source's
  glyph as `.*?</svg>` under `re.S`, so a match that failed on one item's title stretched to the next
  `</svg>` in the file and carried every item between as its head. On the Ridership model pass it ran
  from line 1869 to line 1986 and left the one-source marks `src20` and `src21` plain inside it. The
  glyph now ends at its own `</svg>`, a self-test case wires a source cited by a plain item between
  two glyph items, and the deck was restored and wired again. Three seeded variants anchored on the
  plain items and are re-anchored on the wired ones: `provenance-link-to-a-fragment-that-is-not-there`,
  `provenance-link-into-the-authors-disk`, and `slide-is-not-a-section` through `MARK21`. Reversible.
  — 2026-09-14

| Step | Result |
| :--- | :--- |
| `quickview.py plan` | Cost model 2844 bytes, Programme timetable 3563, Ridership model 4025; the deck 336195 → 348645 at plan time, bound 2097152 |
| the unfixed `add` | the deck 339349 → 351799 bytes; 17 openers, and 2 items still plain text |
| `check.py` after it | `1 failure(s): DS-009`, the preflight not the rows the deck needs |
| the preflight fix, `add` run on the committed deck into a scratch copy | DS-009's preflight comparison `True` |
| both fixes, `add` run again on the restored deck | the deck 339349 → 352105 bytes; 19 openers, 0 items plain |
| `quickview.py list` | 3 quick views |
| `quickview.py check` against `examples/sources/` | 3 of 3 carried: 3 match, 0 drifted |
| `check.py` on the tracked deck | `0 failing`, exit 0 |

The seeded fixture derived from this deck was regenerated, and the size figures corrected.

**The look is owed**: [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 22.

**Outputs produced**
- `examples/reference-deck.html`: three embedded sources, their openers, and the preflight they need
- `tools/deck/quickview.py`: `add` and `refresh` rewrite the preflight, and a glyph ends at its own
  `</svg>`, with a self-test case
- `tools/deck/static_variants.py`: three variants re-anchored on the wired items

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `quickview.py list` names three, and `check` passes | **pass** | §3 |
| the look is recorded as owed | **pass**, look owed | `OWED-LOOKS.md` row 22 |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | The reference deck's three sources open in the quick view, embedded with `quickview.py add` and checked against `examples/sources/`. The look is owed as `OWED-LOOKS.md` row 22. |
| 2026-09-14 | -> proposed | Raised from the owner's observation beside the B27 looks. `PH3`. Batched into B28 first by the owner's ruling. |
