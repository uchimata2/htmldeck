---
id: T-311
title: Keep a deck's chart-engine declaration through a shell sync
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-308, T-202]
work_package: PH1
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: []
---

# T-311 — Keep a deck's chart-engine declaration through a shell sync

## 1. Specify

**Outcome**
A deck that declares its chart engine keeps the declaration after `shell.py sync --write`. Today
[`../docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) places
`<meta name="htmldeck-chart-engine">` in `head` for DS-122, and `sync` rewrites every byte of the
head outside the deck's regions, which are `SLOTS` in `tools/deck/shell.py`. So the first sync
deletes the line, and DS-122 then fails a deck that draws its charts at run time for declaring no
engine.

**Found by** [T-308](T-308-decide-how-a-deck-records-a-deviation-its-owner-licensed-and-what-the-gate-reports-for-it.md),
whose first licence design used the same place. Measured 2026-09-14 on a copy of the reference deck:
one `htmldeck-chart-engine` line after the viewport `meta`, then `python tools/deck/shell.py sync
<copy> --write`, and the count of that line went from 1 to 0. No tracked deck declares an engine,
which is why no gate has met it.

**Scope**
- In: a place for the declaration that `sync` keeps, with DS-122's reader in `tools/deck/audit.py`,
  the contract row and DS-122's own text moved to it together
- In: a deck built on `0.7.0` with the `meta` in its old place, which is told where the declaration
  moved rather than failing DS-122 with no reason
- Out: DS-122's four keys and its SVG rule, which do not change

**Inputs**
- T-308 §3, which put the licence in the deck's head comment for this reason

**Acceptance criteria**
- [ ] a deck declaring an engine keeps the declaration through `shell.py sync --write`, proved on a
      seeded copy in both directions (**L-125**)
- [ ] DS-122 still passes a declared engine and fails an undeclared one
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The head comment is the place T-308 chose, and whether a new head region serves better is
  this task's to decide.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
<!-- One bullet per decision: what was decided, why in one sentence, and whether it is reversible.
Measurements go in a table, and how they were found does not. There is no byte cap, so a reason is
never cut to fit (T-301). -->
- <what was decided>: <why, in one sentence>. <Reversible | Not reversible>. — YYYY-MM-DD

**Outputs produced**
- `deliverables/...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | (no change) | Batched by the owner into B27, first, after PR #14 merged. Still `proposed`. |
| 2026-09-14 | -> proposed | Raised by T-308. `PH1`: the published contract places a declaration where the published `sync` deletes it. Not batched: which batch carries it is the owner's call, and B27 is the shell batch. |
