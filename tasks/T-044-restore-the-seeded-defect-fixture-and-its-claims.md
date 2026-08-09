---
id: T-044
title: Restore the seeded-defect fixture, and re-measure everything examples/README claims
type: fix
status: proposed
phase: specify
parent: T-042
blocked_by: []
related: [T-023, T-024, T-028, T-032, T-034, T-035, T-040]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - examples/reference-deck-seeded-defects.html
  - examples/README.md
  - tools/examples/seed_defects.py
---

# T-044 — Restore the seeded-defect fixture, and re-measure everything examples/README claims

## 1. Specify

**Outcome**
`examples/reference-deck-seeded-defects.html` derives from the current reference deck again; its
ledger names every rule it actually breaks; `examples/README.md` states only figures re-measured
against the two files as they are now; and the fixture cannot silently go stale a third time.

**Why this one**
The fixture is the **only** evidence the evaluation rubric works — `EVALUATION.md` §7 and
`BRIEF.md`'s definition of done both rest on *"one seeded defect per dimension, scored 0 or 1"*. It
was last committed at `0265e57` ([T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md),
2026-08-07) and the reference deck has moved four commits since: the print mode
([T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md)), the contents page
([T-034](T-034-a-contents-page-for-the-printed-deck.md)), the ruler
([T-035](T-035-the-ruler-navigator.md)) and three defect fixes
([T-040](T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md)). The fixture still
contains the ribbon T-035 deleted.

`examples/README.md` states the fixture's whole purpose, and it is the sentence that has stopped
being true: *"It **derives** from the reference deck, so everything except the seeded defect is held
constant and the rubric's response is attributable to the defect rather than to two decks differing
in a hundred ways."* Regenerating rewrites **601 lines**, and the stale copy fails two rules the
ledger does not claim:

```
stale fixture   6 failures   DS-141 DS-035 DS-142 DS-075 DS-092 DS-113
fresh fixture   4 failures   DS-141 DS-035 DS-142 DS-075
```

**Regenerating is one command. The task exists for the other three halves.** DS-092 and DS-113 are
drift; DS-141 and DS-075 are present in the *fresh* fixture and appear in no ledger row, so the
ten-row ledger has never been the list of rules this file breaks. And **it has gone stale twice
now** — T-028 regenerated it once — so a fixture derived from a file that is edited by other tasks
needs something that notices, not a habit.

**Six stale claims in `examples/README.md`, re-measured 2026-08-09:**

| Claim | Measured |
| :--- | :--- |
| *"183 KB in one file"* | **219 083 bytes — 214 KB** |
| *"The seven stage names in the ribbon are buttons"*; *"the ribbon says which stage"* | The ribbon was replaced by the ruler (T-035); the deck contains no `.ribbon` |
| *"Chrome — 11 labelled or interactive items, 52 design units tall"* | **5 items, 52 du** — DS-217 counts a scale as one item |
| *"`audit.py` … 50 checks against `DS-nnn` rules"* | **82 rows** |
| *"What the mechanical gate caught"* — S3, D2, D3 marked **yes** | Not re-derived since the gate was rebuilt; `check.py` on a fresh fixture fails DS-141, DS-035, DS-142, DS-075 and none of those is S3, D2 or D3 |
| *"Reproducing the measurements"* — six commands | `check.py` is absent, though it is the gate the others now feed |

**Scope**
- In: regenerating the fixture and committing it.
- In: reconciling the ledger with the fixture's real failure set — either the ledger gains the rows
  or the seeds stop producing them, decided per rule rather than in bulk.
- In: re-measuring and rewriting every figure in `examples/README.md`, including the navigator
  description and the keyboard table.
- In: making staleness visible. A check that the fixture is derivable from the current reference
  deck, wherever that is cheapest — `seed_defects.py` refusing to no-op, or a `check.py` row, or a
  line in the closing checklist.
- Out: changing any seeded defect's *design*. The ten dimensions and what each seeds are
  [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md)'s and are not reopened here.
- Out: re-running the rubric scoring. This restores the fixture; scoring against it is the
  convergence loop's, and is only meaningful once the fixture is sound.
- Out: `BRIEF.md`'s and T-008's copies of the 183 KB figure —
  [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) sweeps those, from the
  measurement this task takes.

**Inputs**
- [`tools/examples/seed_defects.py`](../tools/examples/seed_defects.py) — the generator and its
  assert-it-matched discipline
- [`examples/README.md`](../examples/README.md) — every claim under audit
- [`tools/deck/check.py`](../tools/deck/check.py) — the gate that produces the real failure set
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-1, F-4 and F-11

**Acceptance criteria**
- [ ] `python tools/examples/seed_defects.py` produces **no diff** against the committed fixture
- [ ] Every rule the fresh fixture fails is either a ledger row or is explained in the README as
      collateral, with which seed causes it — no unexplained failure survives
- [ ] Every figure in `examples/README.md` re-measured by running the tool that owns it, and the
      command that produced each is the one the README already tells a reader to run
- [ ] The navigator section describes the ruler, and the keyboard table matches the shipped deck
- [ ] `check.py` appears in *Reproducing the measurements*, and the section says which of the listed
      commands it subsumes
- [ ] Something fails when the fixture stops deriving from the reference deck, demonstrated by
      editing the reference deck and watching it fail (**L-04**)
- [ ] Both decks opened from `file://` with the network off and **looked at** (**L-01**)

**Open questions**
- **Do DS-141 and DS-075 belong in the ledger, or are they seeder bugs?** DS-141 is plausibly
  collateral from the S6 throb; DS-075's reflow overflow has no obvious owner. Measure before
  deciding — whoever implements.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

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
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), findings F-1, F-4 and F-11. **The fixture the rubric was validated against is four reference-deck revisions behind it and still carries the ribbon T-035 deleted**, so the "everything else held constant" claim that gives it its evidential value is false by 601 lines. It fails DS-092 and DS-113 for reasons its ledger does not name — and fresh, it fails DS-141 and DS-075, which the ledger does not name either, so the ledger has never been complete. **It has now gone stale twice**, which is why the task includes something that notices rather than a resolution to remember. |
