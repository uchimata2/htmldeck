---
id: T-143
title: Split the release chronology out of CLAUDE.md
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130, T-134, T-144]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-14
updated: 2026-08-14
deliverables:
  - CLAUDE.md
---

# T-143 — Split the release chronology out of CLAUDE.md

## 1. Specify

**Outcome**
[`../CLAUDE.md`](../CLAUDE.md) carries the rules that must bind before a session knows what kind of
work it is doing, and nothing else. The dated narrative of what shipped when, which release carried
which fix and which task found which defect moves to a document nothing loads by default. **The
finding is `CE-01`**, stated in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8; it is not restated here.

**This is one of the two cuts [T-134](T-134-state-the-tier-model-and-bound-tier-1-as-a-relation.md)
was raised to make decidable**, and it is the larger of them. The bound now exists, the file reports
itself over it, and this task is what pays the debt down rather than arguing about it.

**Measured at the audit, 2026-08-13:** the chronology was **6,980 of 15,630 bytes — 45% of a tier-1
file paid on every turn**. The file is **18,642 bytes** now, so re-measure before claiming a saving
and again after (`docs/CONTEXT-AUDIT.md` §6.2, rule 1). The section T-134 added is a rule and stays.

**The extraction is the work, not the move.** Narrative paragraphs written over time embed real
rules — the phase-is-not-a-version paragraph is the clearest, and it is a rule wrapped in the
incident that produced it. A section moved wholesale takes those with it out of tier 1, where they
stop binding.

**Scope**
- In: naming every operative rule inside the paragraphs to be moved, **before** anything moves.
- In: the chronology's new home, its statement of its own tier, and the pointer to it from tier 1.
- In: re-measuring `CLAUDE.md` against its own bound and correcting the debt statement, which is the
  one sentence in the file that this task is expected to falsify.
- Out: `docs/BRIEF.md`'s *Release phases*. That is `CE-05`, a different document, and `m`.
- Out: rewording a rule while moving it. A move that also edits is two changes nobody can review.
- Out: the humanizer. `CLAUDE.md` is a plugin file and stays AI-optimized
  ([`../docs/PUBLISHING.md`](../docs/PUBLISHING.md)).

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — what a session working an audit
  finding owes beyond the finding. Read before starting
- [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
  §8 — `CE-01` in full; §9, P1 — the local precedent for the split
- [`../CLAUDE.md`](../CLAUDE.md) — *What loads every turn, and what bounds it*: the bound this task
  is measured against, and the command that measures it

**Acceptance criteria**
- [ ] Every operative rule inside the moved text is listed **before** the move, and each one ends in
      exactly one home
- [ ] Nothing that must bind before a session knows its kind of work leaves tier 1
- [ ] The new document states what tier it is and what loads it — nothing, by default
- [ ] `CLAUDE.md` is re-measured against the smallest document it defers to, and its debt statement is
      corrected to what is true after the move, including the case where the debt is cleared
- [ ] The saving is stated as before and after, dated, with the command that produced both
- [ ] `python tools/docs/refcheck.py` green — every reference into the moved text still resolves

**Open questions**
- **Its own document, or the one `CE-05` would create?** `CE-05` moves `BRIEF.md`'s *Release phases*
  out and is `m` and unraised, so waiting couples a `s` task to an unscheduled one. — the implementer,
  unless the owner rules otherwise; the recommendation is its own document now, folded later if
  `CE-05` lands.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
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
| 2026-08-14 | → proposed | Raised at the owner's direction, with [T-144](T-144-give-each-cumulative-rule-one-operative-home.md), the day after T-134 set the bound and reported the file 4,555 bytes over it. `CE-01` was a candidate at T-130's review and left unraised then; the debt statement in tier 1 names it, so the choice was a task or a citation, and the owner took the task. The larger of the two cuts T-134 enables. |
