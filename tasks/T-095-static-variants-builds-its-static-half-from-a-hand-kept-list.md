---
id: T-095
title: static_variants builds its static half from a hand-kept list, so a new producer is outside the suite
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-066, T-075, T-093]
work_package: PH3
owner: maintainer
business_value: medium
effort: s
created: 2026-08-11
updated: 2026-08-13
deliverables:
  - tools/deck/check.py
  - tools/deck/static_variants.py
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
- ~~Does `check.py` grow a `static_rows(html)` the suite imports, or does the suite derive the list
  the way `audit.self_test` does?~~ **Answered 2026-08-13 — both, and they answer different
  questions.** The recommendation is right about the composition and does not reach the half this
  task grew on 2026-08-13:
  - **`static_rows(html)` is the composition**, imported by the suite, so the two cannot disagree
    the way they did when T-093 moved DS-005 and the suite reported `MISSED`;
  - **the derivation is the classifier, not a second composition.** Every verdict producer under
    `tools/deck/` must be *reached by* `static_rows` or *declared outside it with a reason*, or the
    run fails. Importing alone would have left `printgeom.verdicts` silently absent exactly as the
    hand-kept list did — the composition would be correct, and nothing would say whether the absence
    was a judgement or an oversight. The reason is the whole of what the third producer added.

  The classifier declares the **complement**, never the membership: a list of what is *in* is the
  hand-kept list this task exists to delete, and a list of what is *out* cannot go stale in silence
  because a producer in neither list fails the run. That is `audit.self_test`'s `DELEGATING_PRODUCERS`
  discipline with the subject changed.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Split `gather`'s browserless half into `static_rows(html)`, comments and order intact | `check.py` |
| 2 | `NOT_STATIC` — every producer outside that half, with why it cannot run on markup | `check.py` |
| 3 | `producer_split()` — read `static_rows`'s own source, fail on a producer in neither | `check.py` |
| 4 | Point `static_failures` at `static_rows` and delete the list; run the guard in the suite's self-test; print the producers it ran | `static_variants.py` |
| 5 | Add a producer, do not wire it, watch both fail — then restore by hand (**L-04**, **L-80**) | evidence |
| 6 | Re-run the whole suite and both example decks, and confirm 24 of 24 for a reason | evidence |

## 3. Implement

**Decisions & assumptions**
- **The table declares the complement, never the membership** — 2026-08-13. `NOT_STATIC` names the
  producers that are *outside* the static half. A list of what is *in* is the hand-kept list this
  task deletes; a list of what is *out* cannot go stale in silence, because a producer in neither
  fails the run. Same discipline as `audit.DELEGATING_PRODUCERS`, one scope out.
- **`static_rows` keeps `gather`'s order and its per-producer comments** — 2026-08-13. `report`
  prints verdict rows in composition order, so deriving the order from a set would have reordered
  the gate's own output for no gain. Membership is derived; sequence is written.
- **`static_producers()` reads `static_rows`'s source rather than a list beside it** — 2026-08-13.
  `inspect.getsource` plus the producer names `audit.verdict_producers()` already derives. A second
  list agreeing with the code is a list that agrees until somebody edits one of them (**L-13**).
- **The guard runs in both files** — 2026-08-13. In `check.py` because the composition is its own and
  a producer arrives there first; in `static_variants.py` because that is the suite the question is
  about, and a run of it must not depend on somebody having run the other.

**Outputs produced**
- [`tools/deck/check.py`](../tools/deck/check.py) — `static_rows`, `NOT_STATIC`, `static_producers`,
  `producer_split`, and `gather` reduced to one call; `producer_split()` in `self_test`.
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `static_failures` imports the
  composition, the guard runs in `self_test`, and `main` prints both halves of the split.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A producer `check.py` gathers without a browser is reached by this suite without being named here | met | `static_failures` is `check.static_rows(html)` and nothing else. No producer name is left in `static_variants.py`, and `check.py:196` is the only composition of the static half in the repository |
| Adding a producer and not wiring it fails this suite, demonstrated by doing it (**L-04**) | met | `theme.stray_verdicts` appended, wired nowhere: the suite exits 1 naming it and both remedies. `check.py` exits 1 on the same producer through `audit.self_test`'s older guard. Restored by writing the saved text back and asserting the bytes equal (**L-80**) |
| All 24 static variants still caught, and the count is unchanged for a reason rather than by luck | met, with the number corrected | **25 of 25**, not 24 — a variant was added between this task being written and taken. Unchanged *for a reason*: the producers `static_rows` calls are the same set the deleted list named — `audit.STATIC`, `split`, `provenance`, `marker`, `fetch`, `contrast`, `theme`, `component` — so the same predicates run over the same variants |
| The suite says which producers it ran, so *n of n caught* is readable against a denominator | met | The static section now prints both halves of the split before the variants |

**Verification run**

```
=== static (no browser)
  producers run:  audit.fetch_verdicts, audit.marker_verdicts, audit.provenance_verdicts,
                  audit.split_verdicts, component.verdicts, contrast.verdicts, theme.verdicts
  outside this half, with a reason in check.NOT_STATIC:
    audit.reduced_verdicts, audit.render_verdicts, contract.scale_verdicts,
    contract.scale_verdicts_from, contract.verdicts, printgeom.verdicts,
    printpages.verdicts, spec.verdicts
  25 of 25 static variants caught.
```

`python tools/check_all.py` — **19 ran, 1 skipped with its reason, 0 FAILED, 0 unclassified,
0 stale**, over 36 tracked tools and both example decks. The rendered and reduced-motion halves and
both decks are inside that run.

**What this does not close.** The suite covers *producers*, not rules: a producer inside the static
half with no seeded variant for one of its rules is still absent from both numerator and
denominator, and this task deliberately left that alone. What changed is that the producer cannot
be absent — only the variant can, and the printed list is where a reader sees which.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | Specified, planned, built and reviewed in one pass. **The 2026-08-13 row below is what changed the answer**: importing the composition closes the drift and says nothing about a producer that is outside the static half on purpose, so the fix is an imported composition *plus* a declared complement. The acceptance criteria's `24` is `25` — a variant was added between the writing and the taking — and the count held for a reason: the producer sets are identical. |
| 2026-08-13 | → planned | Specified and planned in one pass; the open question is about this repository's own precedent and was settled from it. |
| 2026-08-11 | → proposed | Raised from the closed-record sweep run before the post-`0.2.1` handoff, on evidence produced the same day: T-093 moved a rule between producers and the suite said `MISSED`. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — not a defect an adopter can hit, and PH2 has shipped, so everything that is not such a defect goes there whatever its size. |
| 2026-08-13 | (no change) | **A third producer, and this one raises a question the first two did not.** [T-123](T-123-nothing-can-see-a-print-only-layout-fault.md) added `printgeom.verdicts`; `check.py` and the fixture's `exercised` set were edited, and `static_variants.static_failures` was **not** — because that suite seeds markup and this producer needs a real Chrome print, exactly as `printpages.verdicts` does. **So the list now has a deliberate exclusion in it and no way to tell it from a forgotten one.** Deriving the producers is not enough on its own: whatever replaces the list has to carry *why* a producer is outside the static half, or it will either sweep two producers that cannot run there or drop them silently again. Raises the value of this task and slightly widens it. |
| 2026-08-12 | (no change) | **A second instance, and this time the hand-edit was remembered.** T-104 added `audit.marker_verdicts` and the same three lines had to be edited by hand — `check.py`, `static_variants.static_failures`, and the fixture's `exercised` set. The suite caught the DS-232 variant only because the middle one was not forgotten. |
