---
id: T-292
title: The docs gate is four fifths one render — decide what figures.py's coverage account binds to
type: fix
status: proposed
phase: specify
parent: T-287
blocked_by: []
related: [T-285, T-234]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
finding: CE-18
created: 2026-09-02
updated: 2026-09-02
deliverables: []
---

# T-292 — The docs gate is four fifths one render — decide what figures.py's coverage account binds to

## 1. Specify

**Outcome**
`python tools/check_all.py --docs` no longer spends most of its time rendering a deck. Measured
2026-09-02 on the frozen tree: **`figures.py` was 22.5 s of the 27.6 s** the docs gate spent in
commands (81.4%), because it resolves the README's *coverage of the ruleset* account by running
`check.py` on the reference deck — a render inside the documents gate, which `T-285` §3 named for this
audit rather than fixed. The finding is `CE-18` in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3. **The gain is seconds, not tokens** —
the run prints one line either way — and it ranks because the owner's question was about the cost of
a batch.

**The remedy is a hypothesis, and L-152 bounds it**: a count is bound or deleted, never refreshed. So
a cached figure is not an answer. Candidates to measure: bind the account to the ruleset table that
`check.py` itself reads, which is a document and not a render; or let `--docs` skip that one binding
with a printed reason, since the full gate still resolves it.

**Scope**
- In: one binding in `figures.py`; the docs-mode timing table re-taken after.
- Out: the full gate's behaviour; any figure other than the coverage account.

**Inputs**
- `../tools/docs/figures.py`, `T-285` §3, `../docs/lessons/L-152.md`

**Acceptance criteria**
- [ ] The docs gate's command time re-measured, before and after, on one tree.
- [ ] The coverage account is still bound to something live, or its deletion is argued from L-152.
- [ ] Full gate green.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the binding; find what `check.py` reads to produce the count | the source of truth |
| 2 | Rebind or skip under `--docs`; self-test | the change |
| 3 | Time both modes | the table |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `../tools/docs/figures.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287` from `CE-18`, the cost `T-285` §3 named for it. `PH3`. |
