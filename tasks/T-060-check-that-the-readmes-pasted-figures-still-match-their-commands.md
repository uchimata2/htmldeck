---
id: T-060
title: Check that the README's pasted figures still match the commands that produced them
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-050, T-056]
work_package: v0.2
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-060 — Check that the README's pasted figures still match the commands that produced them

## 1. Specify

**Outcome**
A check that runs each command `README.md` prints and compares its output to the block underneath it,
so a figure that has gone stale is a red run rather than something a reader finds. **The figures are
correct as of 2026-08-09** — [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md)
re-derived all of them. What does not exist is anything that keeps them that way.

**Why this one**
Raised by T-056, which found **six figures already wrong** before it edited anything: build mode and
critique mode grew the ruleset on 2026-08-09, and nothing re-derived the README afterwards. 161 rule
rows were 163, 115 hard rules were 117, 24 judge rules were 25. The README had also started
**contradicting itself** — its prose said the judgement half is 25 rules while a fenced block three
sections above printed 24. Every gate stayed green throughout and was right to: no gate owns a number
printed in prose in a document that is not a deck (**L-52**).

The obligation to re-derive now exists in [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §6, in
writing and unchecked. This repository's own position is that a rule with nothing behind it is a
claim, so the state this task ends is the one `check.py`'s account exists to make impossible
elsewhere.

**One figure is structurally unstable and needs a decision, not just a check.** The block from
`python tools/tasks/task.py check` counts **every document pointer in the repository**, so it moves
whenever any document is edited — including edits to the README itself. It went 968 → 980 → 992 → 995
within T-056's single session. A check comparing it byte-for-byte would fail on almost every
documentation commit, which is a check nobody keeps.

**Scope**
- In: a check that maps each fenced block in `README.md` to the command that produces it, runs it, and
  compares.
- In: a decision on the pointer-count block above — the candidates are dropping the volatile line from
  the pasted excerpt, comparing only its stable prefix, or regenerating the block in place rather than
  asserting it.
- In: the same treatment for figures stated in **prose**, which is where two of the six stale ones were
  and where the self-contradiction lived.
- Out: `examples/README.md` and the other document READMEs, unless the same mechanism reaches them for
  free.
- Out: deck figures, which are DS-102's and already gated.
- Out: re-deriving today's figures, which T-056 did.

**Inputs**
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §6 — the obligation this would enforce, and the
  list of commands behind the blocks.
- [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-52**, the finding; **L-03** on why the figures are
  pasted at all; **L-05** on what a check that cannot fail is worth.
- [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) §3, which lists all six stale
  figures with the command that re-derives each.

**Acceptance criteria**
- [ ] Every fenced block in `README.md` is either bound to a command and compared, or **listed as
      unbound with a reason** — the same partition `check.py` already requires of itself
- [ ] The check fails when a figure is stale, demonstrated against a deliberately staled copy rather
      than asserted
- [ ] The pointer-count block no longer produces a false failure on an unrelated documentation edit
- [ ] Figures stated in prose are covered, or excluded in writing with what would close the exclusion

**Open questions**
- **Does this run in `check_scaffold.py`, in `task.py check`, or as its own tool?** It is about a
  document rather than the package or the task record, which argues for its own tool; against that,
  a fourth command is a fourth thing nobody runs.

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
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → proposed | Raised by [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md), which re-derived the README's figures and found **six already stale** and one place where the document contradicted itself. **v0.2, not v0.1:** the figures are correct today, so a first release is not blocked by the absence of a check that keeps them correct — holding publication for it would be exactly the failure the release split exists to prevent. Carries one finding that shapes the work before it starts: the `task.py check` block counts every pointer in the repository and therefore moves on almost every documentation commit, so a naive byte-comparison would fail constantly and be turned off within a week. |
