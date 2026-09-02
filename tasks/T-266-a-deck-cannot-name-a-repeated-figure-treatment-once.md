---
id: T-266
title: Say what to do when a class fails DS-229, and decide whether a deck gets a local prefix
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-266 — Say what to do when a class fails DS-229, and decide whether a deck gets a local prefix

## 1. Specify

**Outcome**
A deck can name a repeated figure treatment once, or is told plainly that it cannot. Today `DS-229` reports `.ico` as *uncontracted* — and the contract lives in the plugin, so a builder reads *not yet in the contract*, goes looking for where to add the row, and the search ends nowhere. Eleven marks then repeat three presentation attributes each.

**From the adopter report** [`014`](../docs/adopter-reports/claimai/014-a-deck-cannot-name-a-repeated-figure-treatment-once.md).

**Scope**
- In: **the message, which is a string change and removes the whole dead-end search**: a deck may not add a class; carry the properties as presentation attributes on the element
- In: **a reserved deck-local prefix** — the record's second proposal and the real gap. `DS-229` keeps its job of stopping a deck redefining a *component* and stops policing a deck's own figure internals, which no component contract can anticipate
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`014`](../docs/adopter-reports/claimai/014-a-deck-cannot-name-a-repeated-figure-treatment-once.md) — each carries its evidence, its version and its own proposed fix
- the record explicitly does **not** ask to weaken `DS-229` over components — holding `.slide` or `.sources-box` to a contract is the rule earning its keep
- its third proposal, a figure-internals contract section, which the record itself calls probably wrong because the set of treatments a hand-built figure needs is open

**Acceptance criteria**
- [x] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [x] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Reproduce on this repository's own deck** (**L-141**): put the report's own rule into `measure-first.html`'s shared block, unprefixed and prefixed, with the untouched deck as control | the four verdicts, and the numbers that make them readable |
| 2 | Skip a deck-local class in `missing_rows`, and **return the count** so the verdict says what it measured (**L-36**) | `tools/deck/component.py` |
| 3 | Name the remedy in the failure message | `tools/deck/component.py` |
| 4 | Assert the allowance, the opt-in, the prefix boundary and the component case in the self-test | `tools/deck/component.py` |
| 5 | Reserve the prefix in the contract, and record the amendment | `docs/COMPONENT-CONTRACT.md`, `docs/DESIGN-SYSTEM.md` |
| 6 | Close the adopter record | `docs/adopter-reports/claimai/014…` |

## 3. Implement

**Decisions & assumptions**

- **The prefix is `d-`, the report's own proposal — 2026-08-29.** Checked before taking it: no row
  in the contract and no rule in `shell/`'s stylesheets begins with it. It is short because it is
  typed on every figure-internal class a deck writes, and it is the string the adopter will already
  have in mind.
- **The count travels with the verdict — 2026-08-29, not asked for.** `missing_rows` now returns
  the deck-local classes as well as the uncontracted ones, and the verdict prints both. **L-36**'s
  reason applies exactly: *0 uncontracted* over a deck naming nothing of its own and over one naming
  eleven treatments are the same boolean and not the same fact. Without it, the escape would be
  invisible in the only output anybody reads.
- **The prefix reserves a name, and the record says what that does not cover — 2026-08-29.** My
  first draft of the code comment claimed the prefix *cannot be used to redefine a component*.
  Fixture C measured otherwise: `.d-x .headline{color:red}` passes where `.x .headline{color:red}`
  fails, so a deck does gain an ancestor of its own to scope such a rule from. **It is a small
  change and it is stated rather than glossed**: `.slide .headline{…}` scoped from a *contracted*
  ancestor has always passed, so the deck could already restyle a component and this only spares it
  borrowing a name. What the check decides — whether a component nobody contracted was invented —
  is unchanged, and a contracted class stays contracted however it is reached.
- **The report's third proposal was refused, as the report itself recommends.** A figure-internals
  section in the contract would chase an open set forever. Recorded in the contract beside the
  prefix, so the next reader finds the refusal where the decision is.

**A defect in the reproduction, kept because it is the more useful half.** The first run injected
before the file's **first** `</style>` and reported an unchanged *100 styled* in all four cases —
`shared_css` reads the first block carrying **no** `id`, and the first one in the file has one. That
is **L-143**'s shape exactly: a number that had to move and did not, behind four green verdicts. It
was caught by asking why the control and the seeded case agreed, which is the same question L-143
says to ask.

**Outputs produced**
- [`tools/deck/component.py`](../tools/deck/component.py) — `DECK_LOCAL`, `missing_rows` returning
  both lists, the four callers, the verdict text, and five self-test assertions
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §1 — the reserved prefix, its two
  limits, and the refusal of proposal 3
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-229` amendment note
- [`docs/adopter-reports/claimai/014-…`](../docs/adopter-reports/claimai/014-a-deck-cannot-name-a-repeated-figure-treatment-once.md) — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured | pass | Adopter record `014`. Proposals 1 and 2 taken, proposal 3 refused with the report's own reason recorded in the contract |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | On `measure-first.html` itself. Control `100 styled, 0 deck-local, 0 uncontracted` pass; the report's own `.fig .ico` rule `101 styled, 0 deck-local, 1 uncontracted` **FAIL** — the adopter's verdict reproduced here; the same rule as `.fig .d-ico` `101 styled, 1 deck-local, 0 uncontracted` pass. Five self-test assertions carry the allowance, the opt-in, the `.d`/`.drop` boundary and the contracted-class case |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Recorded in the batch's closing run |

**A look is owed: no.** This task changes a check, a message and two documents. No deck's rendering
changes and no tracked deck gained a deck-local class, so
[`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) takes no row.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Ruled by the owner and implemented in **B8**. Proposals 1 and 2 of report `014` taken - the message names the remedy, and `.d-` is reserved for a deck's own repeated treatments; proposal 3 refused, with the report's own reason recorded in the contract beside the prefix. **Two things beyond the ruling**: the verdict now prints the deck-local count, because the escape would otherwise be invisible in the only output anybody reads (**L-36**); and a code comment claiming the prefix cannot be used to redefine a component was **refused by the reproduction's own fixture C** and rewritten to what was measured. The reproduction's first run was itself an **L-143** - four green verdicts over a count that never moved, because the injection went into the wrong `<style>` block. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
