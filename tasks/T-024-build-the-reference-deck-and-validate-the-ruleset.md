---
id: T-024
title: Build the reference deck by hand and find out whether the ruleset works
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-001, T-002, T-006, T-007, T-014, T-016, T-021, T-023]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: []
---

# T-024 — Build the reference deck by hand and find out whether the ruleset works

## 1. Specify

**Outcome**
A real **12-slide deck with diagrams**, on a neutral topic, built by hand from
[`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) alone — opened offline and looked at. Plus a
**seeded-defect variant** of it, carrying one known defect per evaluation dimension, which is what
[`docs/EVALUATION.md`](../docs/EVALUATION.md) needs to prove its rubric detects anything.

**Why this one**
**Nothing in this project has ever been tested by building a deck.** Six research notes, 131 rules,
an evaluation rubric and a convergence loop, and the only HTML anyone has written was R5's probe —
built to be weighed, not read.

This is the task CLAUDE.md rule 6 exists for, and it is **overdue rather than new**: it has been the
standing recommendation in two consecutive handoffs and has never had a task file, which is why it
kept not happening. It now blocks three things concretely:

- **[T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) cannot close.** Its one unmet
  criterion is the seeded-defect validation, and an unvalidated rubric passes everything.
- **Two of `BRIEF.md`'s definition-of-done criteria** name an artifact that does not exist.
- **T-002 has no target to be judged against.** A generator with no reference output is a generator
  nobody can review.

**What is actually being tested — this is not a demo**

| Question | How this deck answers it |
| :--- | :--- |
| Does the ruleset produce a deck worth presenting? | Build to it strictly, then look. **The failure mode to watch for is a deck that satisfies all 131 rules and is dull** — that is a finding about the ruleset, not about the deck. |
| Is the type floor right? | DS-034/035 predict body text ≥ 16 px in a 720p capture. **Capture it and measure.** The floor was derived arithmetically and has never been observed. |
| Does the stage hold? | DS-063 — render at 3840×2000 and 1280×634 and diff up to a uniform scale factor. |
| Do the rules conflict in practice? | A rule that cannot be satisfied alongside another shows up here first. Record it in [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2, which is where conflicts live. |
| Does the rubric detect anything? | The seeded variant. |
| Can the three standing decisions be made? | Building forces T-001 (fonts), T-006 (charts) and T-007 (tokens) into the open. **This task informs them; it is not blocked by them.** |

**Scope**
- In: **12 slides, with diagrams**, per CLAUDE.md's verification rule — not a three-slide toy. That
  is the size where layout and pacing problems appear.
- In: a **neutral topic written fresh.** Nothing from the corpus. See *Publishing constraints* in
  CLAUDE.md — this deck ships in a public repository.
- In: `portable` mode, opened from `file://` with the **network disabled**, and looked at.
- In: the **720p capture measurement** and the **two-resolution diff**.
- In: the **seeded-defect variant** — one defect per dimension (S1–S6, D1–D4) at score 0, documented
  so the rubric's result can be graded against a known answer.
- In: running the deck through the convergence loop and recording which outcome it reaches.
- Out: **the generator.** This deck is built by hand. T-002 automates what this proves is worth
  automating, and cannot sensibly be specified before it.
- Out: changing rules to make the build easier. **A rule that is painful is a finding to record, not
  a rule to quietly soften.**

**Inputs**
- `docs/DESIGN-SYSTEM.md` — and **only** this, for the build itself. If something needed is not in
  it, that absence is the finding.
- `docs/EVALUATION.md` — for the loop and the seeded variant.
- `docs/research/R5-assets-and-licences.md` — the recommended font trio, icon sprite approach, sizes.
- `docs/research/R6-portability-contract.md` — what `file://` permits.

**Acceptance criteria**
- [ ] 12 slides with diagrams exist as one `.html` file, **zero external references**
- [ ] **Opened offline, with the network disabled, and looked at** — CLAUDE.md rule 6, and stated as
      what was seen rather than as "works"
- [ ] Rendered at 3840×2000 and 1280×634; the two are identical up to a uniform scale factor (DS-063)
- [ ] **Body text measured in a 720p capture**, with the number recorded — whether or not it clears 16 px
- [ ] Every font embedded carries its licence
- [ ] The deck run through the convergence loop, with its outcome (PASS/CAP/STALL/OSCILLATION) and
      per-dimension scores recorded
- [ ] The seeded-defect variant exists, its defects documented, and **the rubric scores each 0 or 1**
      — or the anchors are corrected and the reason recorded
- [ ] **Every rule that proved wrong, unbuildable, or in conflict with another is recorded** — this
      is an expected output, not a sign the build went badly
- [ ] No personal, client or machine data anywhere in either file

**Open questions**
- **What topic?** It must be neutral, publishable, and rich enough to need diagrams, a real
  trade-off (A-04), a decision (A-01) and an ask (A-14). A weak topic makes the deck untestable on
  half its dimensions. — owner
- **Does the seeded variant derive from the good deck, or is it built separately?** Deriving keeps
  everything else constant so the rubric's response is attributable; building separately avoids the
  good deck's own blind spots. — this task

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the topic; write the argument before any HTML — the ruleset's own DS-090/D1 discipline applied to itself | the deck's spine and governing idea |
| 2 | Build 12 slides against `DESIGN-SYSTEM.md` alone, recording every point where the ruleset was silent, painful or self-contradictory | the deck, plus a findings list |
| 3 | Open it offline and **look at it**. Measure: two-resolution diff, 720p capture | the measurements |
| 4 | Run the convergence loop; record the outcome and scores | loop result |
| 5 | Seed the defect variant and score it against the known answer | rubric validation, and any anchor corrections |
| 6 | Route findings — rule conflicts to `DESIGN-RATIONALE.md` §2, rule changes as tasks, lessons to `LESSONS.md` | the corrections |

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
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created at handoff, after the board showed the artifact CLAUDE.md rule 6 has been demanding since T-014 had **no task file** — which is why two handoffs recommended it and neither produced it. It now blocks T-023's closure and two of BRIEF's done criteria. Written so the deck is a **test**, not a demo: the interesting outcomes are a rule that cannot be built, two rules that conflict, or a deck that satisfies all 131 rules and is still dull. |
