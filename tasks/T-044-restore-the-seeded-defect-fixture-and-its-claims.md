---
id: T-044
title: Restore the seeded-defect fixture, and re-measure everything examples/README claims
type: fix
status: done
phase: review
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
  - tools/deck/audit.py
  - tools/deck/render.py
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
- ~~**Do DS-141 and DS-075 belong in the ledger, or are they seeder bugs?**~~ **Answered 2026-08-09,
  by measuring first as the question asked.** Both are collateral and neither is a seeder bug:
  applying the **S3** seed alone moves DS-075's reflow width from 320 to 851, because the card row
  is a four-item flex row with `flex:1` and no wrap; and the **S6** throb is declared at 2.4 s,
  which is what trips DS-141's 500 ms cap. **Neither becomes a ledger row** — the ledger is one
  seeded defect *per dimension* and a row for a side effect breaks the property that makes the
  fixture attributable. Both are named in the README with the seed that causes them, which carries
  more information than a row would. DS-075 is worth the paragraph it gets: it says the S3
  anti-pattern is also an accessibility failure, found by a rule aimed elsewhere.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Regenerate the fixture and commit it | A fixture that derives from the deck as it stands — 601 lines back in agreement |
| 2 | Trace each unexplained failure to the seed that causes it, by applying seeds in isolation rather than reasoning about them | DS-075 → the S3 card row; DS-141 → the S6 throb, both proven not argued |
| 3 | Answer the open question from what the ledger *is*: one row per dimension | Collateral explained in the README, ledger left at ten rows |
| 4 | Re-run every tool that owns a figure in the README, and rewrite each figure from the run | Nine measurements replaced, four of them materially wrong |
| 5 | Re-derive the mechanical-catch table from a real two-deck comparison instead of inheriting it | 3 dimensions caught, not 5 — and two of the misses are not `judge` rules |
| 6 | Rewrite the navigator and keyboard sections against the shipped markup | The ruler, its focus precedence, and two keys the table omitted |
| 7 | Build `seed_defects.py --check`, and prove it fails by editing the reference deck | Staleness becomes a red run instead of an audit finding |
| 8 | Put `check.py` at the head of *Reproducing the measurements* and say what it subsumes | A reader runs the gate first, which is what everything else now feeds |
| 9 | Open both decks offline and look at every slide | Verdicts in §4, and two instrument defects found doing it |

## 3. Implement

**Decisions & assumptions**
- **DS-141 and DS-075 stay out of the ledger** — the open question, answered by what the ledger is
  for. It carries **one seeded defect per dimension**; a row for a rule that fires as a side effect
  of another dimension's seed breaks the one property that makes the fixture evidence. Both are
  named in the README as collateral **with the seed that causes them**, which is what the criterion
  asks for and is strictly more informative than a ledger row. — 2026-08-09
- **Neither is a seeder bug, and that was measured rather than assumed.** Applying the S3 seed alone
  to a clean reference deck moves DS-075's reflow width from 320 to 851, and `seededThrob` is
  declared at 2.4 s against DS-141's 500 ms cap. — 2026-08-09
- **`DS-168` was made to report the smallest target, not just the count.** The README quoted
  *"30.5 CSS px at 1280×634"* and **no command in the repository printed it**, so the figure could
  only ever be re-measured by hand — which is how it went stale. The gate already computed the
  minimum; it now prints it (43.3 CSS px at 1622 × 1054). — 2026-08-09
- **Two instrument defects were found by looking, and only by looking.** They are recorded in §4;
  one is fixed here because the *look at it* criterion could not otherwise be met, and the other is
  raised as [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md). — 2026-08-09
- **The reference deck was not edited.** It was edited twice during step 7 to prove `--check` fails,
  and restored both times; `git status` shows it unmodified. A task that fixes a fixture by changing
  its parent has proved nothing. — 2026-08-09

**Outputs produced**
- [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html)
  — regenerated, 227 482 bytes
- [`examples/README.md`](../examples/README.md) — every figure re-measured; the navigator, catch
  table and reproduction sections rewritten
- [`tools/examples/seed_defects.py`](../tools/examples/seed_defects.py) — `build()`/`ledger()` split
  out, `--check`, and a `self_test()` that mutates a deck to prove the comparison works
- [`tools/deck/audit.py`](../tools/deck/audit.py) — DS-168 reports the smallest target
- [`tools/deck/render.py`](../tools/deck/render.py) — `slide_count()`; `shots` and `measure` no
  longer default to twelve

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `seed_defects.py` produces **no diff** against the committed fixture | **met** | `OK - examples\reference-deck-seeded-defects.html is exactly what regenerating produces (227482 bytes)` |
| Every rule the fresh fixture fails is a ledger row or is explained as collateral, with its seed | **met** | Four failures. DS-035 → S5, DS-142 → S6 are ledger rows; DS-075 → S3 and DS-141 → S6 are collateral, each traced to its seed by isolating it, and both are in the README with the mechanism |
| Every figure re-measured by running the tool that owns it, using the command the README tells a reader to run | **met, after one change to make it true** | Nine figures re-measured. The smallest-target row was the exception — no listed command printed it — so `DS-168` now reports the minimum alongside the count rather than the README quoting a hand measurement |
| The navigator section describes the ruler, and the keyboard table matches the shipped deck | **met** | Ruler, its ticks, its jump targets and its arrow-key precedence over the document handler (DS-137). The table gained `PageUp`/`PageDown`, and `Esc` also leaves the reading view |
| `check.py` appears in *Reproducing the measurements*, and the section says which commands it subsumes | **met** | Placed first, with what it subsumes (`audit.py`, the contrast audit, `contract.py`) and why the other four still stand alone |
| Something fails when the fixture stops deriving from the reference deck, demonstrated by editing the deck (**L-04**) | **met** | `STALE: … no longer derives from … regenerating would change 1 line(s) (+1/-0)`, exit 1, from a one-line edit to the reference deck. Also caught the other way: an edit that moves a seed anchor fails in the seeder's own assertion first |
| Both decks opened from `file://` with the network off and **looked at** (**L-01**) | **met** | 12 + 14 shots through `render.py shots`, real Chrome, DNS black-holed. Reference deck: ruler, counter, bottom line and both SVG figure types render correctly. Seeded deck: the S3 card row, the D2 padding to 14 and the D3 *Thank you* close are all visibly present |

**Two instrument defects, both found by looking rather than by any check**

| What | Where | Disposition |
| :--- | :--- | :--- |
| `render.py shots` and `measure` defaulted to **`range(12)`** — the reference deck's length, not any deck's. The 14-slide fixture rendered 12 shots and said nothing about the two it dropped | `tools/deck/render.py` | **Fixed here.** The *look at it* criterion is unsatisfiable while the tool silently omits slides, so this was in scope by necessity. `slide_count()` reads the deck; a deck it cannot read is fatal rather than a guess |
| **DS-140 passes on a deck with no dashed flow**, because `None != "none"`. The S3 seed removes the deck's only flow, so the rule passes on its own absence | `tools/deck/audit.py` | **Raised as [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md).** Not fixed here: it is the third instance of the pattern — DS-130 was fixed in place by T-038 and DS-087 is excused for it — and fixing a third instance one at a time is what the task exists to stop |

**One thing the fixture does that is expected and is not a defect.** On the seeded deck the printed
eyebrow reads `12 · THE ASK` while the counter reads `14 / 14`, because D1 reorders and D2 pads
while the eyebrow number is baked into the slide's own markup. That is the seeding showing through,
not a deck fault, and it is the kind of thing a rubric should notice rather than a gate.

**Child fix tasks raised**
- [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) — a check whose subject is
  absent must not report a pass

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Regenerating was one command; everything worth recording came from the other three halves.** The corrected mechanical-catch table is the headline: the README claimed five of ten dimensions caught, the real figure is **three**, and the two lost are **not** the `judge` rules the document's argument rests on. A 14-slide deck passes DS-081, which only forbids fewer than six; a close slide reading *Thank you* passes everything, because DS-203 and DS-205 ask whether a bottom line exists and is not hidden, and a recap satisfies both. So the README's own thesis — the gate is necessary and nowhere near sufficient — was **understated**, and the old table was internally inconsistent besides, marking five dimensions caught against three reported failures. **The open question was answered by measurement, as it asked to be:** the S3 seed alone moves the reflow width 320 → 851, and the S6 throb is declared at 2.4 s. Both stay out of the ledger, because a ledger of one defect per dimension stops being attributable the moment it also carries side effects. DS-075 earned a paragraph anyway — it says the card-row anti-pattern is an accessibility failure as well as a worse encoding, caught by a rule aimed at something else. **Two instrument defects were found by looking at the decks and by nothing else.** `render.py shots` defaulted to twelve slides, so the fixture had been *looked at* two slides short every time anyone did it — fixed here, since the criterion is otherwise unsatisfiable. And DS-140 passes on a deck with no dashed flow: [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md), raised rather than patched because it is the third instance of one pattern and the previous two were each fixed in place. Staleness is now `seed_defects.py --check`, proven to fail on a one-line edit. |
| 2026-08-09 | → planned | §1 accepted as written; the six stale claims and both failure sets were already measured when [T-042](T-042-audit-the-whole-repository-against-itself.md) raised them. Nine steps, ordered so the fixture is current before anything is measured against it, and with *look at both decks* last rather than folded into the measuring — which is what surfaced the two instrument defects. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), findings F-1, F-4 and F-11. **The fixture the rubric was validated against is four reference-deck revisions behind it and still carries the ribbon T-035 deleted**, so the "everything else held constant" claim that gives it its evidential value is false by 601 lines. It fails DS-092 and DS-113 for reasons its ledger does not name — and fresh, it fails DS-141 and DS-075, which the ledger does not name either, so the ledger has never been complete. **It has now gone stale twice**, which is why the task includes something that notices rather than a resolution to remember. |
