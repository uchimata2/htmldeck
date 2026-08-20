---
id: T-194
title: spec.py cannot express a figure derived from two sources, so a cross-check deck fails SPEC-4
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-069]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: high
effort: s
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-194 - spec.py cannot express a figure derived from two sources, so a cross-check deck fails SPEC-4

## 1. Specify

**Outcome**
A figure ledger can say a number came from comparing two sources. Today it cannot, and the deck that
does the comparison fails its own specification check.

**The defect**
[`../tools/deck/spec.py`](../tools/deck/spec.py) line 212:

    origin = row[2].strip("`")

One slug. A ledger row citing two - `` `exercise`, `notes` `` - is read as a single slug
whose name is that whole string, matches nothing named, and `SPEC-4` fails.

**Why this is a defect and not a limitation.** `CLAUDE.md` states the test: a published gate failing
a deck for using a class the contract defines is a defect, whatever the contract says. A deck whose
job is to cross-check two documents produces two-source rows *by construction* - the adopter deck of
2026-08-19 is nine such rows, and its red-flag slide is nothing but them. The author's only recourse
was to pick one origin and put the truth in prose, which is the ledger lying to keep the gate quiet.

**Scope**
- In: the ledger's origin column accepting a list, and `SPEC-4`/`SPEC-5` reading it as one.
- In: a third origin kind - *derived by this deck* - argued rather than assumed. A cross-check
  finding is stated in neither source, so *both sources* and *neither source* are different claims
  and the ledger should be able to make each.
- In: the ledger's documented form in `build.md`, which must show the multi-origin row.

**Acceptance criteria**
- [ ] The adopter deck's nine cross-check rows validate with their real origins, unedited.
- [ ] A single-origin ledger is byte-identical to what it produces today.
- [ ] A fixture holds a two-source row and is watched failing first.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read `Origin` with the same parser the slide's `Sources` cell uses | `slugs()` |
| 2 | Decide the third origin kind | `derived`, reserved |
| 3 | Fixture both, seeded failing first | `self_test` |

## 3. Implement

**Decisions & assumptions**
- **`derived` is reserved rather than free text**, so the check can tell a claim from a typo - and it composes: `` `exercise`, `notes`, derived `` is *these two documents, and the number is ours*.
- **A second origin the slide does not cite still fails.** Asserted in both directions, because a vocabulary widened by one value is one step from one that admits anything.

**Outputs produced**
- `tools/deck/spec.py`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A ledger row citing two sources validates unedited | **pass** | seeded into the fixture pair: SPEC-4 `False` with the old parser, `True` with the new one |
| A single-origin ledger is unchanged | **pass** | the three shipped decks' SPEC rows are identical |
| Watched failing first | **pass** | recorded above |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | One parser, shared. |
| 2026-08-20 | -> done | Three criteria met. |
