---
id: T-178
title: In dense mode the current-position mark is half the size of the section marks, and the ring is gone
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-035, T-114]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-18
updated: 2026-08-18
deliverables:
  - shell/components.css
---

# T-178 — In dense mode the current-position mark is half the size of the section marks, and the ring is gone

## 1. Specify

**Outcome**
Past the ruler's capacity bound, *where am I* is still the loudest thing on the ruler. Today it is
one of the quietest, and the ruler's whole reason for existing degrades exactly at the length that
made it necessary.

**The mechanism, measured 2026-08-18**
Rendered in real Chrome, offline, at 1920x1234, on a throwaway 25-slide deck built by splicing
twelve minimal slides into `examples/reference-deck.html`. Both themes, `data-ticks="dot"`, which
is the shipped default:

| Deck length | Mode | What marks the current slide | Rendered width |
| :--- | :--- | :--- | ---: |
| 13 slides | normal | `.ruler-ring` around the lit dot | **30 px** |
| 25 slides | dense | the lit dot alone, `7 du` | **7 px** |

In the same dense row a **section** mark renders at **14 px** — `.ruler[data-dense]` shrinks
`li:not([data-section])` and leaves the seven section cells at their full `14 du`. So past the bound
the mark that *changes* is half the width of the eleven marks that do not, and hue is the only
property left telling them apart.

**Why the two rules that produce it are each defensible**
Neither is a mistake on its own, which is why no review caught the pair:

- `.ruler[data-dense] .ruler-ring{display:none}` — the cells stop being uniform in dense mode and a
  30-unit ring would cover its neighbours. True.
- `.ruler[data-ticks="dot"] .ruler-ticks li[data-lit] button::before{background:var(--accent)}` sets
  colour and deliberately **not** size, so a lit slide cannot be misread as a stage start. Also
  true, and the CSS says so in its own comment.

Together they leave dense mode with no size channel for position at all: the ring carried it, the
ring is gone, and the replacement was explicitly forbidden from growing.

**Scope**
- In: how the current position reads in `[data-dense]`, both tick styles, both themes.
- Out: the capacity bound itself (16, `rulerAvailableDu()` — that is T-114's and is correct), and
  the decision to drop targets past the bound.

**The constraint any answer has to clear**
The size channel is spoken for: size means *section versus slide* and DS-216 forbids inventing a
third encoding of position. So the answer is a treatment that is neither a bigger dot nor a new
element — a ring sized to the dense cell, a bracket, or an underline the label already implies.
Whichever it is, it has to survive the `0.5` stage hand-over (DS-071), where a design unit renders
at `0.506` CSS px.

**Acceptance criteria**
- [ ] At 25 slides, the current-position mark is the most prominent mark on the ruler, in both
      themes, and a person says so from a render rather than a measurement.
- [ ] Position stays distinguishable from a stage start — the two encodings do not merge.
- [ ] The treatment survives the 0.5 scale floor; the rendered size is stated.
- [ ] Both tick styles (`dot`, `bar`) covered, since the theme parameter must not fork the
      component (CLAUDE.md rule 4).
- [ ] `check_all.py`, `tasks/lint.py` and `docs/figures.py` clean.

**Open questions**
- Which treatment — the project owner, from a rendered strip of two or three candidates, not from
  prose. This is the same shape of question `chrome_row.py` refuses to answer for the mark floor.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Build a repeatable long-deck fixture rather than a hand-spliced throwaway — the fixture this was found with lived in a scratch directory and dies with the session | a tool or a checked-in fixture |
| 2 | Render two or three candidate treatments at 17, 25 and 43 slides, both themes, both tick styles | a strip to look at |
| 3 | Owner rules | a decision in §3 |
| 4 | Build it in `shell/`, sync the three shipped decks, regenerate the seeded-defects deck (L-77) | shell, css |
| 5 | Gates, then `figures.py` last because a shell change moves every deck's byte size | green |

## 3. Implement

**Decisions & assumptions**
- (none yet)

**Outputs produced**
- (none yet)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Found by [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md)'s post-build look, doing the half that had never been done: the chrome row **in dark mode**, at 13 slides and at 25. The defect is not dark-specific and shows in both themes, which is the part worth keeping — it had been rendered in light at 25 during T-114 step 10 and read as *a compact mode* rather than as a loss, because nothing put the two lengths side by side. `contrast.py` passes it, and correctly: every pair clears its ratio. The failure is one of **rank**, not of contrast, and no gate here owns rank (**L-05**). Not a tag blocker for the release T-114 ships in — the two rules that produce it both predate T-114 and neither moved — but this release lowers the capacity bound 17 → 16, so one more deck length falls into dense mode than before, and that is why it is filed now rather than noticed later. |
