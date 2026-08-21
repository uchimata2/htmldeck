---
id: T-211
title: Scope speaker notes, and decide what DS-088 becomes
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-211 — Scope speaker notes, and decide what DS-088 becomes

## 1. Specify

**Outcome**
Speaker notes have a written scope: what they are, where they live in a shipped `.html`, what a
presenter does with them, and what the gate says about them. Today the project holds two statements
that cannot both stand. **DS-088** forbids speaker notes, presenter markers and script in the
shipped deck, `auto` and gated. **R1's candidate rule A10** carries the marker *amend — BRIEF Q4*
and has since it was written. `docs/BRIEF.md` open question 4 said *scope now, build later* and was
never revisited. The owner ruled on 2026-08-21 that speaker notes get a task; this is it. What comes
out is a scope and a decision on DS-088 — **not** an implementation.

**Why it is a decision rather than a fix.** DS-088 is not wrong. It is a rule the corpus supports:
R1 measured *no speaker notes, no presenter markers, no script — decided explicitly*. Amending it is
a ruleset change with a stated reason under DS-000, and the reason has to survive the thing DS-088
was protecting: a deck that ships with a presenter's private text inside it, readable by anyone the
file reaches. **Self-containment cuts both ways here** — rule 1 says the file carries everything,
which is exactly why notes inside it are not private.

**Scope**
- In: what a speaker note is, and whether it ships inside the deck at all.
- In: what DS-088 becomes — unchanged, narrowed, or amended — and the reason, per DS-000.
- In: clearing R1's A10 marker either way, so the candidate rule stops pointing at an open question.
- In: closing the speaker-notes half of `docs/BRIEF.md` open question 4.
- Out: building it. A scope that names the mechanism is the deliverable; the mechanism is a later
  task.
- Out: PDF export, the other half of BRIEF Q4. The owner left it deferred on 2026-08-21.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-088, and DS-000 for what amending costs.
- [`docs/BRIEF.md`](../docs/BRIEF.md) open question 4 — the scope-now-build-later statement.
- [`docs/research/R1-corpus-conventions.md`](../docs/research/R1-corpus-conventions.md) — the
  measurement behind A10, and the 2026-08-21 ruling that a stated rule beats the artefacts.
- [`docs/research/R1-rules-candidate.md`](../docs/research/R1-rules-candidate.md) — A10 and its
  marker.
- [`docs/research/R7-printable-mode.md`](../docs/research/R7-printable-mode.md) — it scoped speaker
  notes out alongside PDF export, and says why.

**Acceptance criteria**
- [ ] A written scope exists saying what a speaker note is and where it lives, or a written decision
      that speaker notes stay out — either is a pass, an unresolved *maybe* is not.
- [ ] DS-088 is either unchanged with the reason restated, or amended under DS-000 with the reason
      recorded in its row.
- [ ] The privacy consequence is addressed explicitly: a self-contained file carries its notes to
      whoever receives it, and the scope says what that means for the presenter.
- [ ] R1's A10 marker no longer says *amend — BRIEF Q4*, whichever way it went.
- [ ] `docs/BRIEF.md` open question 4's speaker-notes half is struck through and points here.
- [ ] `python tools/check_all.py` is green, since DS-088 is gated and a rule edit moves counts six
      documents quote.

**Open questions**
- Whether a note that never ships — a sidecar the generator emits and the deck does not carry -
  satisfies what was wanted. It would leave DS-088 untouched, and it breaks the one-file promise for
  the presenter rather than for the audience. Decide in section 2.

## 2. Plan

*Not started.*

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- *Not started.*

**Outputs produced**
- *Not started.*

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised on the owner's ruling against `docs/BRIEF.md` open question 4, which had said *scope now, build later* and was never revisited. The question was surfaced by a resume sweep asking every remaining open question in the project rather than only the ones a handoff named. `PH3` because PH2 has shipped and this is not a defect in the published plugin. The PDF-export half of Q4 was left deferred in the same ruling and is not in this task. |
