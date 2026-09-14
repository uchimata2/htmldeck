---
id: T-311
title: Keep a deck's chart-engine declaration through a shell sync
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-308, T-202]
work_package: PH1
shipped_in: 1.0.0
owner: the project owner
business_value: medium
effort: s
created: 2026-09-14
updated: 2026-09-14
deliverables: [tools/deck/audit.py, tools/deck/shell.py, tools/deck/check.py, docs/COMPONENT-CONTRACT.md, docs/DESIGN-SYSTEM.md]
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
- [x] a deck declaring an engine keeps the declaration through `shell.py sync --write`, proved on a
      seeded copy in both directions (**L-125**)
- [x] DS-122 still passes a declared engine and fails an undeclared one
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. The head comment is the place T-308 chose, and whether a new head region serves better is
  this task's to decide. **Decided in §3: the head comment.**

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Decide the place: the head comment, or a new head region in `SLOTS` | §3 |
| 2 | Read the declaration from the head comment, fail one anywhere else with the reason, and print that reason | `tools/deck/audit.py`, `tools/deck/shell.py`, `tools/deck/check.py` |
| 3 | Self-test each outcome, and add a static variant for the old `<meta>` | `tools/deck/audit.py`, `tools/deck/static_variants.py` |
| 4 | Move the contract row and DS-122's text, and re-sweep DS-122 | `docs/COMPONENT-CONTRACT.md`, `docs/DESIGN-SYSTEM.md`, `tools/deck/check.py` |
| 5 | Prove it on seeded copies through a sync, then lint, then the full gate | §3 |

## 3. Implement

**Decisions & assumptions**
- The declaration is a line in the head comment, not a new head region: the head comment already
  survives a sync and holds T-308's licences, and a new region would change `SLOTS`, every deck and
  `shell.py check`'s byte comparison for one optional line. Reversible. — 2026-09-14
- The line is `htmldeck-chart-engine:` followed by DS-122's four keys, the form of T-308's licence
  line. Reversible. — 2026-09-14
- A declaration outside the head comment fails DS-122, on a deck that draws nothing too, and the
  failure names the line and where it goes. It binds on structure, the `<meta>` element or a
  declaration line, so prose naming the key does not fail. Reversible. — 2026-09-14
- Two declarations fail, because the contract's count is `0-1`. Reversible. — 2026-09-14
- DS-122 moves out of `STATIC` into `audit.chart_verdicts`, because a boolean row cannot print the
  reason. It is declared in `ABSENCE_IS_A_PASS` as a conditional. Reversible. — 2026-09-14
- `head_note` moves from `check.py` to `shell.py`, beside `SLOTS`, so the licence reader and DS-122
  read one definition. Reversible. — 2026-09-14
- DS-122's row is amended and re-swept: a new digest in `SWEPT`, and a third clause row for the
  placement, which `ds122_charts` tests before it reads a declaration. Reversible. — 2026-09-14

Each deck below is a copy of the reference deck outside the repository. The engine is a `<canvas>`
inside the slides region, which `sync` keeps.

| Case | DS-122 before the sync | Declaration lines through `sync --write` | DS-122 after the sync |
| :--- | :--- | :--- | :--- |
| head-comment line, `<canvas>` | pass: declares the engine | 1 → 1 | pass: declares the engine |
| head-comment line, no engine | pass | 1 → 1 | pass |
| the old `<meta>`, `<canvas>` | fail: outside the head comment, names the line | 1 → 0 | fail: declares no engine |
| no declaration, `<canvas>` | fail: declares no engine | 0 → 0 | fail: declares no engine |

The `audit`, `check` and `shell` self-tests pass. DS-122's fixture holds 14 cases, and 5 of them are
new: declared twice, the old `<meta>` with and without an engine, a declaration in a later comment,
and a deck with no head comment.

**Outputs produced**
- `tools/deck/audit.py`: `ds122_charts` reads the head comment; `chart_verdicts`; the fixture cases;
  DS-122 in `ABSENCE_IS_A_PASS`
- `tools/deck/shell.py`: `head_note`, moved from `check.py`
- `tools/deck/check.py`: `chart_verdicts` in `static_rows`; DS-122's digest and third clause
- `tools/deck/static_variants.py`: `chart-engine-declared-in-a-meta`
- `docs/COMPONENT-CONTRACT.md` and `docs/DESIGN-SYSTEM.md`: the declaration's place

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| a deck declaring an engine keeps the declaration through a sync, both directions | **pass** | §3's table: the line 1 → 1, the `<meta>` 1 → 0 |
| DS-122 still passes a declared engine and fails an undeclared one | **pass** | §3's table and the fixture |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Lint, then the full gate on the finished tree, since the diff reaches `tools/deck/` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-14 | -> done | The declaration is a line in the head comment, and a `<meta>` fails with the reason. Proved through a sync on seeded copies. No look is owed: no deck in the repository changed. |
| 2026-09-14 | (no change) | Batched by the owner into B27, first, after PR #14 merged. Still `proposed`. |
| 2026-09-14 | -> proposed | Raised by T-308. `PH1`: the published contract places a declaration where the published `sync` deletes it. Not batched: which batch carries it is the owner's call, and B27 is the shell batch. |
