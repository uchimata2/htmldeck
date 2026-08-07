---
id: T-019
title: Build the capability preflight every deck ships with
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: [T-002]
related: [T-005, T-017]
work_package: WP3
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables: []
---

# T-019 — Build the capability preflight every deck ships with

## 1. Specify

**Outcome**
Every generated deck carries a short feature-detection block that runs before it renders, names
precisely which capability is missing when one is, and leaves the recipient with a legible document
instead of a blank page. This is the mechanism that makes
[R6](../docs/research/R6-portability-contract.md)'s version-floor position real: the deck's floor
is *whatever browser passes the preflight*, and without the preflight that position is just a
refusal to name a number.

**Why this one**
T-017 measured Chrome 151 and Edge 151 and nothing else, so it declined to invent a floor like
"Chrome 125+" — that would have been reading rather than testing (**L-05**). R6 §7 argues the
preflight is the better contract regardless of what testing old builds would have shown, for three
reasons worth restating in one line each: a version number is a lossy proxy for the capability you
actually care about; **a recipient cannot act on a version number** in a deck that has already
failed to render; and asking a browser what it can do fails in the safe direction for browsers
nobody tested.

The deck is delivered by double-click to someone who did not build it and cannot debug it. A blank
slide is the worst possible failure for that recipient. This task is what stands between them and
one.

**Scope**
- In: the preflight itself — what it checks, when it runs, and how little it costs.
- In: **emitting only the checks the deck actually uses.** A deck with no 3D must not fail on a
  missing WebGL context; a deck that inlines no ESM library must not test `import(blob:)`.
- In: the degraded state. What a recipient sees when a check fails, which must be the deck's
  content in a legible static form, never a diagnostic screen with no content behind it.
- In: proving the preflight fails when it should (**L-04**) — a preflight that has only ever been
  seen passing is not evidence of anything.
- Out: choosing a numeric version floor. R6 §7 settled that this should not be done, and this task
  implements that ruling rather than reopening it.
- Out: the rest of the build check. T-005 gates the deck **at build time**, on the author's
  machine; this runs **at open time**, on the recipient's. Different moment, different audience,
  different failure. Neither replaces the other.

**Inputs**
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §7 —
  the position, the reasoning, and a first list of load-bearing checks.
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) §2 —
  which capabilities are actually load-bearing, measured.

**Acceptance criteria**
- [ ] A deck built by build mode carries a preflight, and it runs before first paint
- [ ] The preflight contains **only** the checks that deck's content needs — demonstrated by
      building two decks with different feature use and diffing what each emits
- [ ] Demonstrated **failing on a known case** (**L-04**) — a capability is suppressed and the
      preflight names it, rather than the deck rendering blank or rendering wrong
- [ ] On failure the recipient still gets the deck's content in a legible static form
- [ ] Zero false positives on the tested browsers — a deck that works must never show the warning
- [ ] Size cost measured, not estimated
- [ ] The failure state **looked at** (**L-01**), offline, in a real browser

**Open questions**
- ~~Should a failed preflight be silent for the *author* and loud for the *recipient*, or the same
  for both?~~ **Answered 2026-08-07 by the owner: the same for both, always visible.** A deck
  opened by double-click cannot know who opened it, so "silent for the author" would have to be
  compiled in — and the shipped file would then differ from the file that was tested, which is the
  one thing a portability contract cannot afford. The author's separate signal already exists and
  runs at a different moment on a different machine:
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s build check.
- ~~Does `isSecureContext` belong in the emitted preflight at all, given that every route by which a
  deck is opened satisfies it? It may be a build-check row rather than a runtime one.~~ **Answered
  2026-08-07 by the owner: no — make it a build-check row.** `file://` is already a secure context
  in Chrome, so a runtime test can only ever pass: bytes in every deck, plus the false reassurance
  that something was verified. **This is the general rule this task should apply to the whole check
  set, not a one-off** — a preflight row earns its place only if there is a real opening route on
  which it fails, and the scope line above already forbids emitting checks the deck does not use.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Decide the check set per deck feature, from R6 §2's load-bearing rows | mapping |
| 2 | Design the degraded state — content first, diagnosis second | design note |
| 3 | Implement emission in build mode, restricted to the features used | code |
| 4 | Build two decks with different feature use and diff the emitted preflights | evidence |
| 5 | Suppress a capability and confirm the preflight names it (**L-04**) | evidence |
| 6 | Measure the size cost and look at the failure state offline | figures + a look |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <part of build mode; paths land when T-002 does>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-07 | (no change) | **Both open questions answered by the owner; §1 has none left.** *One behaviour, always visible* — the file cannot know who opened it, and an author-silent build would ship a different artifact from the one that was tested. *`isSecureContext` becomes a build-check row* — it is true for `file://`, so at runtime it can only pass. **The second answer generalises into the design step this task starts with**: step 1 selects checks per deck feature, and the selection rule is now stated — a row earns its place only where a real opening route makes it fail. That is testable against [R6](../docs/research/R6-portability-contract.md) §2's load-bearing list, and it will remove more than one candidate. |
| 2026-08-06 | → proposed | Created. R6 §7 defines the deck's version floor as a capability preflight rather than a number; that position is only real if something emits the preflight. Blocked on T-002 because the preflight is emitted **by** build mode and cannot be built before it — the design work in steps 1–2 could start earlier if the owner wants it pulled forward. |
