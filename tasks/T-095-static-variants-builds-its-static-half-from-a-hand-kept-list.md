---
id: T-095
title: static_variants builds its static half from a hand-kept list, so a new producer is outside the suite
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-066, T-075, T-093]
work_package: v0.3
owner: maintainer
business_value: medium
effort: s
created: 2026-08-11
updated: 2026-08-11
deliverables: []
---

# T-095 — static_variants builds its static half from a hand-kept list, so a new producer is outside the suite

## 1. Specify

**Outcome**
The seeded-defect suite runs the same static half `check.py` does, derived rather than listed, so a
verdict producer added tomorrow is inside the suite the day it exists.

**Why this one**
`static_variants.static_failures` composes the static half by naming its producers:

```
rows = ([(r, w, bool(fn(html))) for r, w, fn in audit.STATIC]
        + audit.split_verdicts(html) + audit.provenance_verdicts(html)
        + audit.fetch_verdicts(html)
        + contrast.verdicts(html) + theme.verdicts(html) + component.verdicts(html))
```

`check.py:gather` composes it differently, in its own order, with its own list. **Two descriptions of
one thing, which is L-13's subject and L-08's**, and they disagreed on 2026-08-11:
[T-093](T-093-ds-005s-check-bans-the-one-esm-route-r6-measured-as-working.md) moved DS-005 out of
`STATIC` into a producer, `check.py` picked it up, and the suite reported

```
MISSED - the gate does not check what it says it checks:
  script-reads-a-file          DS-005 not among []
```

**It was loud, and that is luck rather than design.** The suite noticed because a seeded variant for
DS-005 happened to exist. A producer added for a rule with **no** seeded variant leaves no trace at
all: the suite's own count still reads *n of n caught*, because the rules it never had a variant for
are not in its denominator either.

**The precedent is in the same repository, one file over.** `audit.self_test` stopped naming its
producers after [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) and
[T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md), because a
name nobody adds is a name nobody misses — it reads every module's source through
`verdict_producers()` and fails the run when one is unexercised. This suite is the same discipline
with the derivation still to be done.

**Scope**
- In: `static_failures` obtaining its rows from the one composition `check.py` uses, or from the same
  derivation `audit.self_test` already performs.
- In: a failure when a producer `check.py` gathers statically is not reached by this suite, in the
  shape `audit.self_test` already fails an unexercised producer.
- Out: the rendered and reduced-motion halves. They take a measurement rather than markup and are a
  different composition; naming them here would widen this into a refactor of the gate.
- Out: seeding a variant for every rule. Coverage of *rules* is `check.py`'s account; this is
  coverage of *producers*.

**Inputs**
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `static_failures`.
- [`tools/deck/check.py`](../tools/deck/check.py) — `gather`, the composition this must not restate.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `verdict_producers`, and the self-test that fails
  on one it does not exercise.

**Acceptance criteria**
- [ ] A producer `check.py` gathers without a browser is reached by this suite without being named here
- [ ] Adding a producer and not wiring it fails this suite, demonstrated by doing it (**L-04**)
- [ ] All 24 static variants still caught, and the count is unchanged for a reason rather than by luck
- [ ] The suite says which producers it ran, so *n of n caught* is readable against a denominator

**Open questions**
- Does `check.py` grow a `static_rows(html)` the suite imports, or does the suite derive the list the
  way `audit.self_test` does? *Recommend the first: one composition, imported, is the shape that
  cannot drift; the derivation is a second mechanism that agrees with it only as long as both are
  right.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Split `gather`'s browserless half into something both callers use | `check.py` |
| 2 | Point `static_failures` at it and delete the list | `static_variants.py` |
| 3 | Add a producer, do not wire it, watch the suite fail (**L-04**) | evidence |
| 4 | Re-run the whole suite and both example decks | evidence |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | → proposed | Raised from the closed-record sweep run before the post-`0.2.1` handoff, on evidence produced the same day: T-093 moved a rule between producers and the suite said `MISSED`. `v0.3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — not a defect an adopter can hit, and v0.2 has shipped, so everything that is not such a defect goes there whatever its size. |
