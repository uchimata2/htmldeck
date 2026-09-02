---
id: T-273
title: Give the owed looks a queue, so the pass before the release has something to run
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-219]
work_package: PH3
owner: the project owner
business_value: high
effort: xs
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables: []
---

# T-273 — Give the owed looks a queue, so the pass before the release has something to run

## 1. Specify

**Outcome**
The owner can read every look this programme of work owes in one place.
[`docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 says a task owing a look records it as
**owed**, that the owed looks **accumulate as a queue**, and that the owner runs **one looking pass**
over it before the release is cut. The first two happen and the third has nothing to run: the record
lives in whichever of 273 task files wrote it, findable only by grepping for a phrase nobody
standardised. **`CLAUDE.md` rule 6 is deferred, not kept, by a queue that cannot be enumerated.**

**Scope**
- In: one document listing the owed looks, and §4 pointing at it
- In: the looks B1 to B7 already owe
- Out: **running** the looks. That is the owner's, and it is the whole reason the queue exists
- Out: a checker. The obligation is on a person, and a gate that counted rows here would be
  measuring whether the document was edited rather than whether anybody looked

**Inputs**
- [`docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 — *the one thing a session may not
  do is look*
- `../CLAUDE.md` rule 6, which §4 is implementing
- The seven task records of B1 to B7

**Acceptance criteria**
- [ ] every look B1 to B7 owes is in the queue, naming the deck, the slide and what to look for
- [ ] §4 names the document, so a session closing a task knows where to write
- [ ] `python tools/tasks/lint.py` green

**Open questions**
- None. The shape is fixed by §4's own sentence; what is missing is the file it describes.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sweep B1 to B7's records for the ones that state a look | One: [T-229](T-229-ds-106s-check-omits-a-word-the-rule-names.md). B1 to B4 changed no deck; B5, B6 and T-242 say so in as many words |
| 2 | Write the queue, one row per look, with what to look for rather than what changed | [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) |
| 3 | Point §4 at it, so the next task to owe one has somewhere to write | The sentence in §4's *may not look* block |

## 3. Implement

**Decisions & assumptions**
- **A document, not a field on the task.** 2026-08-29. The task record is where the look is *decided*
  and it stays there; what was missing is the index, and the same argument that gives lessons a
  generated index applies — a fact spread across 273 files is a fact nobody can read at once.
- **Not generated, and that is the point.** 2026-08-29. A generated index would need a machine-readable
  marker in every task record, which is a convention to enforce before the first pass runs. The queue
  is short — it holds what a release's worth of work owes — and it is hand-kept for the same reason
  the exemption tables are read as data: a row nobody wrote is a look nobody owed.
- **No checker.** 2026-08-29. §4's obligation is on a person, and the only thing a gate could decide
  here is whether the file was edited. **This is one of the two places this repository has where the
  discipline is a habit rather than a check**, and saying so is better than a green row that means
  nothing.
- **The queue holds *what to look for*, never *what changed*.** A diff says what moved; a look
  answers whether it reads. The row that says *one SVG label is now one line where it was two — does
  it read as well against its three siblings?* is a question a person can answer in ten seconds, and
  *changed a text element* is not.

**Outputs produced**
- [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) — the queue
- [`docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 — the pointer
- [`README.md`](../README.md) — the pasted `refcheck.py` output, which every document added to this tree moves

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every look B1 to B7 owes is in the queue, naming the deck, the slide and what to look for | pass | One row, from `T-229`. The other six records state *no look is owed* and say why, which is the same discipline answering in the negative |
| §4 names the document | pass | The *may not look* block points at it |
| `python tools/tasks/lint.py` green | pass | Run at the end of B7 |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised while closing **B7** and worked in it, under [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4's *absorb what a batch finds*. **It has impact on other work rather than being a fix in place**: every remaining batch writes into the queue at close. `PH3` because it is not a defect in the published plugin. |
| 2026-08-29 | → done | Batch **B7**. The queue exists and §4 points at it. It holds one row, which is the honest count after seven batches: six of the seven tasks that could have owed a look changed no deck. |
