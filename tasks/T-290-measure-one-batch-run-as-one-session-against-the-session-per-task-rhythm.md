---
id: T-290
title: Measure one batch run as a single session with compaction, against the session-per-task rhythm
type: research
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-285, T-286]
work_package: PH3
shipped_in: 1.0.0
owner: the project owner
business_value: medium
effort: m
finding: CE-16
created: 2026-09-02
updated: 2026-09-14
deliverables: [docs/CONTEXT-AUDIT.md]
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
  *Superseded 2026-09-13: neither transcript survives — the oldest on disk is dated 2026-09-04 — so
  both rhythms are measured fresh; see the open question.*
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
  **Answered by the owner 2026-09-13, on a changed premise**: every batch in the order has landed.
  Both rhythms are measured on the first two to four `s` tasks
  [T-299](T-299-triage-the-third-adopters-report.md) raises, alternating the boundary between
  neighbouring tasks — `/compact` and continue, or a fresh session. The owner types `/compact`.
- Whether one pair is enough, or a second runs — the owner. Recommended: a second, because `T-310`
  needed the owner's key presses and `T-306` did not. **Answered by the owner 2026-09-14: one pair.**
  This task closes on the `T-310` and `T-306` readings.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | ~~Take the per-task rhythm's figures from an existing batch's transcripts~~ Superseded 2026-09-13: no transcript survives | none |
| 2 | Read the fresh-session arm on `T-310` and the `/compact` arm on `T-306`, each before task work and at pull request open | the readings in §3 |
| 3 | Write the paragraph, and leave `CE-16`'s band to `T-294` | the owner's decision input |

## 3. Implement

**Decisions & assumptions**
- The instrument is `../docs/CONTEXT-AUDIT.md` §11.2's: main-thread API calls deduplicated by
  message id, weighted input 1, cache write 2, cache read 0.1, output 5. Context is the last call's
  input plus cache write plus cache read. — 2026-09-14
- The compact arm counts only calls after the transcript's `compact_boundary` record. The
  compaction's own call is not in the transcript, so the instrument does not weigh it. Its record
  gives 188,489 tokens before, 12,493 after, and 70.8 seconds. — 2026-09-14
- Re-reads the compaction forced on `T-306`: one, the instrument script written before it (30 lines).
  The harness re-attached two task files unasked, `T-310` (125 lines, not needed by `T-306`) and this
  one, and named three files as too large to re-attach. No project document was re-read, because
  `T-306` changed no shell and needed no deck sync. — 2026-09-14
- The compaction's own call is bounded, not measured. If its 188,489 tokens of input were read from
  the cache and all 12,493 tokens after it were its output, it weighed about 81,000. The transcript
  cannot show either. — 2026-09-14
- `CE-16`'s band is left to `T-294`, which grades every band in the register. Grading it here as
  well would give one verdict two homes. — 2026-09-14

**Readings**

| Arm | Task | Point | Calls | Context | Fresh | Own output | Carried | Weighted |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| fresh session | `T-310` | after the resume read path, before task work | 8 | 124,978 | 152,310 | 39,635 | 73,206 | 265,151 |
| fresh session | `T-310` | pull request open, before the merge; the owner merges | 20 | 181,204 | 265,146 | 207,990 | 255,194 | 728,330 |
| `/compact` and continue | `T-306` | after the compaction, before task work | 4 | 84,010 | 59,368 | 14,410 | 29,702 | 103,480 |
| `/compact` and continue | `T-306` | pull request open, before the merge; the owner merges | 22 | 134,558 | 160,684 | 162,675 | 237,716 | 561,075 |

**For the owner.** On one pair, `/compact` and continue cost less than a fresh session: 561,075
weighted tokens to an open pull request, against 728,330. The whole difference is at the boundary.
The task work cost about the same in both, 457,595 and 463,179, and the start did not, 103,480 and
265,151. The compaction's own call is not in the transcript. Counted at its bound, the compact arm is
about 86,000 cheaper, 12%; left out, 167,000, 23%. **The compacted session also stayed smaller**:
84,010 tokens of context at the start against 124,978, and 134,558 at the pull request against
181,204. So `CE-16`'s payback, a restart earning its cost back after about 27 turns at a smaller
context, does not arise against a compaction, which starts smaller than a fresh session. What it
gives up is the handoff. No file is written at the boundary, so the continuity lives in the harness's
summary and not in a durable home, and a session that ends between tasks leaves no handoff to resume
from. In re-reads it cost one 30-line script. This is one pair of dissimilar tasks, since `T-310`
needed the owner's key presses, and the owner ruled one pair enough.

**Outputs produced**
- `../docs/CONTEXT-AUDIT.md` §11.5, one line, and a measured note under `CE-16`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Both rhythms measured on comparable work, with the transcript instrument, and the weights stated once | met | `T-310` and `T-306`, both `s` fixes from `T-299`, read at the same two points. The weights are the first decision in §3. Comparable in size, not in kind: `T-310` needed the owner's key presses |
| The re-reads a compaction forced are counted, not assumed away | met | One, a 30-line script. The task files the harness re-attached are named in §3 |
| One paragraph for the owner | met | §3, *For the owner* |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-16`, as a measurement and not a change, because the finding collides with a settled rhythm. `PH3`. |
| 2026-09-13 | (no change) | The owner's ruling on the open question: the named baseline no longer exists, so both rhythms are measured fresh on `T-299`'s first small tasks. `blocked_by` gains `T-299`. |
| 2026-09-14 | (no change) | One pair measured, `T-310` in a fresh session and `T-306` after `/compact`, and the owner ruled one pair is enough. `blocked_by` loses `T-299`, which is closed. |
| 2026-09-14 | → in_progress | Both arms read: `T-310` in a fresh session, `T-306` after `/compact`. |
| 2026-09-14 | in_progress → done | `/compact` and continue cost 561,075 weighted to a pull request against 728,330, all of the difference at the boundary. The compaction's own call is bounded, not measured. `CE-16`'s band is left to `T-294`. |
