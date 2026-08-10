---
id: T-083
title: The generated example deck fails a hard rule and nothing recorded it
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-021, T-071, T-075]
work_package: v0.2
owner: the project owner
business_value: high
effort: s
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-083 — The generated example deck fails a hard rule and nothing recorded it

## 1. Specify

**Outcome**
`examples/sort-window/sort-window.html` passes the build check, or its failure is recorded as a known
and reasoned exception. Either way the repository stops shipping a red gate on the deck it points at
as proof the pipeline works.

**Why this one**
Found 2026-08-10 while working
[T-071](T-071-the-intermediate-specifications-carry-their-references.md). Run today:

    1 failure(s): DS-064
        DS-064   smallest body run in a 720p capture: 15.0 px (23 du) on 'Approve the slot by 19 Septe',
                 floor 16, 4 slide(s) sampled

**It is not new and it is not T-071's.** The same run against the file as it stood at `d80e0c3`
reports the identical row — same slide, same 15.0 px, same 23 du — so it predates that task and was
already true of the committed deck.

**Why `high`.** `CLAUDE.md` names this deck as **the first deck nobody authored by hand**, and the
repository is public. A generated example that fails a `hard` rule is the strongest available argument
against the generator, and it is sitting in the repository unremarked. The second half is worse than
the first: nothing in the task record says this was ever run, so the failure is not a known cost, it is
an unknown one.

**A second observation, which may be the more interesting half.** The reference deck passes the same
rule at 17.3 px on a four-slide sample. Both decks carry the **same shared component block**, so the
difference is either this deck's own composition or **which four slides the sample drew** — and if it
is the sample, a `hard` rule is being decided by a draw. Worth settling before the fix, because the two
answers lead to different fixes.

**Scope**
- In: what the 15.0 px run actually is — the ask lines on slide 12, the provenance mark, or something
  else. Read the element, do not infer it from the slide.
- In: whether DS-064's four-slide sample can return different verdicts for the same deck. If it can,
  that is a defect in the check and outranks the deck's.
- In: the fix, or the reasoned exception, and a line in the task record either way.
- In: why no task ran this check against this deck. The gate exists and is green elsewhere, so the gap
  is in when it runs, not in what it can see.
- Out: the reference deck, which passes.
- Out: DS-064's 16 px floor, which is settled ([T-021](T-021-the-reflow-view-and-the-resolution-contract.md)).

**Inputs**
- `python tools/deck/check.py examples/sort-window/sort-window.html --sources examples/sort-window/sources`
- [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) — where DS-064's floor and its 720p capture were
  settled, and the measurement it lifted into the gate.
- [T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md) — the last time this rule's
  own implementation was wrong, which is the reason to check the instrument before the deck.

**Acceptance criteria**
- [ ] The failing run is either green or recorded as a reasoned exception with the cost stated
- [ ] What the 15.0 px run is has been read off the deck, not inferred
- [ ] Whether the four-slide sample is deterministic is answered
- [ ] Whatever made this go unrun is named, and if it is a missing step it is written into the
      workflow rather than remembered

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → proposed | Raised from [T-071](T-071-the-intermediate-specifications-carry-their-references.md), which ran the build check on this deck as part of its own review and found a failure that task had not caused — confirmed against the committed file before recording, so the attribution is measured rather than assumed. `high` because the deck is the repository's own evidence that the generator works and it is public; `s` because the row names its slide and its number and the whole question is which of two things produced it. `v0.2`: a fix, not a capability. |
