---
id: T-290
title: Measure one batch run as a single session with compaction, against the session-per-task rhythm
type: research
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-285, T-286]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
finding: CE-16
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-290 — Measure one batch run as a single session with compaction, against the session-per-task rhythm

## 1. Specify

**Outcome**
A measured answer to whether the one-session-per-task rhythm costs tokens or saves them. `CE-16`
estimates from this run's transcript that a session boundary re-pays the start context and the
resume read path at the cache-write rate — about **190,000 weighted tokens** — while continuing at a
140,000-token context costs about 14,000 weighted per turn, so a restart pays back only after roughly
27 turns at the smaller context. **That is an estimate from one session and the remedy is a
hypothesis**; this task runs one B-batch both ways and reads the harness's own usage figures for
each. The estimate, its weights and the instrument are
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §11.2 and §11.5.

**It collides with settled practice and does not resolve the collision.** `docs/REMEDIATION-ORDER.md`
runs a batch per session and `docs/AUDIT-METHOD.md` makes a cycle a session boundary; the handoff
discipline is the owner's. The ecoctx method's fourth refusal applies: the project's rule stands
until the owner reads the measurement, and this task produces the measurement, not the change.

**Scope**
- In: one batch of two or three documentation tasks run as one session with `/compact` between
  tasks, and the usage read from the transcript by the same instrument `T-287` used; the same batch's
  figures from the per-task rhythm, taken from B17's or B18's transcripts, whichever the owner names.
- In: what a compaction loses — the second session must be able to find what the first knew, and
  a re-read after compaction is counted against the compaction.
- Out: changing `REMEDIATION-ORDER.md` §4 or the handoff config; that is the owner's, after the numbers.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §11.2, §11.5, `CE-16`

**Acceptance criteria**
- [ ] Both rhythms measured on comparable work, with the transcript instrument, and the weights stated once.
- [ ] The re-reads a compaction forced are counted, not assumed away.
- [ ] One paragraph for the owner: which rhythm costs less, by how much, and what it gives up.

**Open questions**
- Which batch to run twice — the owner. Recommended: the smallest documentation batch left in the order.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Take the per-task rhythm's figures from an existing batch's transcripts | baseline table |
| 2 | Run one batch in one session, compacting between tasks | the comparison table |
| 3 | Write the paragraph; strike or keep `CE-16`'s band | the owner's decision input |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `../docs/CONTEXT-AUDIT.md` §11.5, one line

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-16`, as a measurement and not a change, because the finding collides with a settled rhythm. `PH3`. |
