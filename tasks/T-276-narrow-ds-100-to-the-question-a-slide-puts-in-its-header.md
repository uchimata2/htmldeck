---
id: T-276
title: Narrow DS-100 to the question a slide puts in its header
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-270, T-225]
work_package: PH3
owner: the project owner
business_value: low
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-276 — Narrow DS-100 to the question a slide puts in its header

## 1. Specify

**Outcome**
`DS-100` fails a rhetorical question and passes a question a slide answers. Today it fires on any
`?` that meets a tag, which is every question anywhere in slide text — so the adopter drew the word
*Why?* as SVG shapes to get a deck to build, and that word is now invisible to every text
instrument in the toolchain. **The rule's escape hatch teaches a worse habit than the rule
prevents**, which is the finding, and it is unchanged by this task's mechanism.

**Ruled by the owner, 2026-08-29.** [T-270](T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md)
took report [`023`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md)'s
proposal 1 as ruled, **measured it, and refused it**: its condition — a `?` followed within the
slide by a declarative bottom line — holds on **38 of 38** slides, because the component contract
puts one bottom line on every slide and `DS-202` requires it to be one plain sentence. That is an
off switch, not a narrowing ([L-144](../docs/lessons/L-144.md)). The question went back with a
recommendation and its stated limit; **the owner took the recommendation.**

**The ruling: narrow by where the question sits.** A `?` in a slide's **header** — its `.eyebrow`,
`.headline` or `.standfirst` — fails. A `?` anywhere else in the slide's own copy passes.

**Scope**
- In: the check, bound on the three contracted header parts rather than on the `<header>` element
- In: the `DS-100` row, saying what it now measures and why
- In: closing report `023`, which is `deferred` rather than open
- Out: `reviewable rather than fatal`, report `023`'s other proposal. Refused by the owner in the
  same pass that ruled `DS-202` — *reviewable* is how a rule quietly stops being enforced
- Out: any second rule about questions. A question in body copy is now unpoliced, and that is the
  decision rather than an oversight

**Inputs**
- report [`023`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md)
- [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3, which carries the question and
  the ruling
- **The recommendation's own limit, and it stands as a limit on this task.** All three tracked
  decks carry **zero** `?` in copy, so there is no firing rate to calibrate against. This rests on
  the argument — a rhetorical question on a slide is a headline device — and not on a count.

**Acceptance criteria**
- [x] a `?` in a headline fails and a `?` in body copy passes, both seeded on a real deck (**L-125**)
- [x] no tracked deck's verdict moves, and it is checked rather than assumed
- [x] report `023` closed
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The mechanism is ruled and its limit is recorded above.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Bind the check on `.eyebrow`, `.headline`, `.standfirst` | `tools/deck/audit.py` |
| 2 | Repair the T-167 self-test, whose own fixture puts its question in `.body` and would now pass | `tools/deck/audit.py` |
| 3 | Seed both directions on a shipped deck | the measurement |
| 4 | Say what the rule measures and why | `docs/DESIGN-SYSTEM.md` |
| 5 | Close the record and the order's open question | `docs/adopter-reports/claimai/023…`, `docs/REMEDIATION-ORDER.md` |

## 3. Implement

**Decisions & assumptions**

- **The check binds on the three contracted classes, not on `<header>` — 2026-08-29.** The element
  is not reliable: this repository's own reference deck wraps the three parts in `<header>` on slide
  5 and does not on slide 11, so a check bound on the wrapper would decide half a deck and pass the
  other half in silence. `.eyebrow`, `.headline` and `.standfirst` are contracted parts, which makes
  them the structure. The self-test asserts the wrapper case explicitly.
- **All three header parts are the subject, not the headline alone.** A question moved from a
  headline into the standfirst above it is the same device; the self-test carries one case per part.
- **The scope cut is unchanged and still tested.** T-167's quoted-source narrowing runs first, so a
  question a source's own heading asks is not the deck's. Its fixture had to move: it put the
  question in `.body`, where the rule deliberately no longer looks, so the boundary would have
  passed for the wrong reason. The pair is now built on headlines.

**The limit, which is the honest half of this task.** It is not calibrated. All three tracked decks
carry **zero** `?` in copy, so there is no firing rate and no false-alarm rate to compare — the
narrowing rests on the argument that a rhetorical question on a slide is a headline device. That
limit was put to the owner with the recommendation and accepted rather than waved past.

**Outputs produced**
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `HEADER_PART`, the rewritten
  `ds100_no_rhetorical_questions`, and six self-test assertions
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-100` row
- [`docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3 — the question answered
- [`docs/adopter-reports/claimai/023-…`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md) — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A `?` in a headline fails and a `?` in body copy passes, both seeded on a real deck | pass | On `measure-first.html`: headline → `1 failure(s): DS-100`; the same question in a `.lobbyline` inside `.body` → `0 failure(s)`; untouched control → `0 failure(s)` |
| No tracked deck's verdict moves, and it is checked rather than assumed | pass | The control above, and the batch's closing `check_all.py`, which runs the gate on all four decks |
| Report `023` closed | pass | With what was refused, what replaced it, and the stated limit |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Recorded in this task's closing run |

**A look is owed: no.** A rule and its checker. No deck's rendering changes, and no tracked deck's
verdict moves.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Implemented the day it was raised. `DS-100` now reads the three contracted header parts rather than any `?` meeting a tag, and it is bound on the classes because this repository's own deck wraps them in `<header>` on one slide and not on another. Both directions seeded on `measure-first.html`. **The uncalibrated limit is recorded in the rule row, the record and the code**, because the owner accepted it rather than it being waved past. |
| 2026-08-29 | → proposed | Raised on the owner's ruling, which followed [T-270](T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md)'s refusal of the previous one. **A task is what follows a ruling** — the same route [T-274](T-274-build-the-card-reveal-so-turns-two-dials-have-a-reader.md) and [T-275](T-275-retire-accent-ink-from-the-contract-the-themes-and-the-decks.md) took from `PR-36` and `PR-77`. **`PH3`**: a rule change on the main line, not a defect in the published plugin. |
