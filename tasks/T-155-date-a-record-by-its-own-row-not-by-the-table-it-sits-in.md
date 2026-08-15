---
id: T-155
title: Date a record by its own row, not by the table it sits in
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-154, T-129, T-088]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-15
deliverables: [tools/docs/figures.py]
---

# T-155 — Date a record by its own row, not by the table it sits in

## 1. Specify

**Outcome**
A struck-through, dated row in [`figures.py`](../tools/docs/figures.py) excuses **itself** from
checking, not every live claim sharing its table or its paragraph.

**Raised 2026-08-14 by
[T-154](T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md)**, which wrote the
fix, measured it, and **did not ship it**. `blocks()` computes `dated` from `DONE_ROW.search(block)`,
where a block is anything between blank lines — so one `~~…~~ **done 2026-08-10**` row silently turns
off `claimed()` and the artifact binding for every other row in that table. `claim_scopes()` already
splits a block at table rows and list items, and is the split T-088 and T-129 settled for exactly this
question about a link's subject.

**Why it is a task and not an edit.** Measured over all six documents `figures.py` reads, the
per-scope and per-block versions **decide no verdict differently today**. Shipping an unmeasured
behaviour change inside a task about unmeasured claims was the wrong shape, and a latent defect
written into a code comment is one nobody schedules.

**Scope**
- In: `blocks()`, `declared()`'s block-level `DONE_ROW` guard, and `artifact_claims()`.
- In: a fixture that fails when a live claim beside a dated row goes unjudged — the defect has no
  instance today, so the fixture must build its own (**L-78**, **L-85**).
- Out: what marks a record. `DONE_ROW` stays `~~…~~ **done <date>**`; T-154 widened it, read
  `pipeline.md` 190, and reverted — the strike there is on the name of a **gap** and the sentence
  after it is a live claim in the shipped skill.

**Inputs**
- [T-154](T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md) §3 — the
  measurement, and why it was reverted
- **L-97** — a check anchored on the value that drifts goes blind exactly when it is needed
- [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) —
  the same block-versus-scope question, decided for the artifact binding

**Acceptance criteria**
- [ ] A live claim in a table that also holds a dated record is judged
- [ ] A dated record is still not judged, in the row it is written in
- [ ] The fixture fails when the guard is put back to block scope
- [ ] `python tools/docs/figures.py` and `python tools/check_all.py` green, with the `compared`
      count not falling

**Open questions**
- ~~**Does the same scope error exist in `stale_exclusions` or `audit`'s prose loop?**~~ **Answered
  2026-08-15: no, and the search was worth taking.** `DONE_ROW` is read in exactly two places —
  `blocks()` and `declared()`'s guard — which are the two this task names. `audit()`'s prose loop
  calls `sentences(prose(text))` and **discards** the flag (`for sentence, _dated in …`), so the
  README is judged without reference to records at all; `stale_exclusions()` never mentions it. The
  suspicion was right and it took one search rather than an assumption.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Search every use of `DONE_ROW` before changing any, so the open question is answered from the tree rather than from memory | two call sites, both named in §1 |
| 2 | `blocks()` computes `dated` per **scope** rather than per block, reusing `claim_scopes()` — the split T-088 and T-129 already settled for a link's subject. A second rule for the same question would be two answers to one (**L-13**) | a sentence carries its own row's date |
| 3 | Move `declared()`'s block-level guard into `artifact_claims()`, where it skips the dated **scope** and not the block | a record stops excusing its neighbours |
| 4 | Fixture 13: a two-row table, one dated record and one live claim about the same file, asserted at both layers — `artifact_claims` and `sentences` | a red under the old guard |
| 5 | Re-measure `compared` and `unanchored`; criterion 4 says the count must not fall | 23 and 410, unmoved |

## 3. Implement

**Decisions & assumptions**
- **`claim_scopes()` is reused rather than a new split written** — 2026-08-15. It is the same
  question T-088 and T-129 answered for a link's subject, and the task's own §1 names it. A second
  rule would drift from the first the day either moved.
- **The guard moved into `artifact_claims()`, not into `scope_claims()`** — 2026-08-15.
  `artifact_claims` is where the scopes are already enumerated, so the guard sits beside the loop it
  qualifies; `scope_claims` would have had to re-derive whether its own text was a record.
- **No verdict changed today, and that was the expected result.** T-154 measured this and the
  re-measurement agrees: `compared` 23 and `unanchored` 410, identical before and after. The fixture
  is the whole evidence that the fix does anything, which is why §1 required it to build its own
  instance.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `blocks()` dates per scope,
  `artifact_claims()` carries the guard, `declared()`'s block-level guard removed, self-test fixture
  13 added.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A live claim in a table that also holds a dated record is judged | met | Fixture 13's second row reports `[('7', 'compared')]`. |
| A dated record is still not judged, in the row it is written in | met | The same fixture asserts no row is returned for the record's `4`, and `sentences()` marks the two rows `[False, True]` rather than together. |
| The fixture fails when the guard is put back to block scope | met | Demonstrated, not asserted: with the guard restored to `[] if DONE_ROW.search(block) else …` the same input returns `[]` — the live `7 slides` goes unjudged — and the sentence marks collapse from `[False, True]` to `[True]`. Both fixture arms go red. |
| `python tools/docs/figures.py` and `python tools/check_all.py` green, with the `compared` count not falling | met | `figures.py` exits 0; `compared` **23** and `unanchored` **410**, identical to before the change, which is T-154's measurement reproduced. `check_all.py` green — run once over all three of this batch's changes. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → done | All four criteria met. **No verdict moved, which is the result T-154 predicted and the reason this was a task rather than an edit** — the fixture is the only thing that can tell the two versions apart today, so it carries the whole value of the change. The open question was answered from the tree in one search: `DONE_ROW` has exactly two readers and `audit()`'s prose loop discards the flag entirely. |
| 2026-08-15 | → in_progress | Implemented in three edits and one fixture; `claim_scopes()` reused rather than a second split written. |
| 2026-08-15 | → planned | §2 written. Step 1 is the open question, deliberately first: it decides whether the change has two call sites or four, and answering it after editing would have been an assumption dressed as a result. |
| 2026-08-15 | → specified | §1 was complete when T-154 raised it on 2026-08-14 — written, measured and argued — and the status was never advanced. |
| 2026-08-14 | → proposed | Raised by T-154, which wrote the fix and measured it as changing no verdict in any of the six documents `figures.py` reads. `PH3` because PH2 has shipped and this is not a defect in the published plugin — `figures.py` is a repository tool. |
