---
id: T-165
title: Give a deferred entry a closing condition a check can read
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-097, T-019, T-051]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-08-15
updated: 2026-08-16
deliverables:
  - tools/deck/check.py
  - docs/lessons/L-109.md
---

# T-165 — Give a deferred entry a closing condition a check can read

## 1. Specify

**Outcome**
Every entry in [`tools/deck/check.py`](../tools/deck/check.py)'s `DEFERRED` carries its **closing
condition** as a field a check can read, so an excusal that has stopped being true is reported rather
than found by a person sweeping the record after a release.

**Why it exists**
Raised at [T-097](T-097-ds-004s-excusal-says-degrade-gracefully-is-unobservable-and-ds-009-gave-it-an-instrument.md)'s
review, against its fifth acceptance criterion — *a note on whether an excusal can be held to its own
closing condition mechanically, or a task raised saying it cannot*. **It cannot, and the instance is
the task that raised this one.**

**The gap, stated precisely.** `staleExcusals` fires when a rule is **excused and checked** — the two
halves contradicting each other. DS-004 was excused and **not** checked, so the partition stayed
intact for nine months while the excusal quietly stopped being true: T-019 shipped DS-009's preflight,
which made *degrade gracefully* observable, and nothing anywhere could notice that half of DS-004's
reason had died. The account was not wrong; it was **silent by construction**, which is the harder
case and the one **L-54** names — an excusal outlives its subject and its stated reason goes false
with it.

**Why a closing condition is the right field.** Most `DEFERRED` entries already end with one in prose
— *CLOSES WHEN a second engine is in the harness*, *closed by the harness exposing it*. A sentence
cannot be evaluated; a field can be pointed at the thing that would close it. The shape this
repository already trusts for a hand-kept declaration is `figures.py`'s `ARTIFACTS` and `ACCOUNTS`,
and `audit.py`'s `ABSENCE_IS_A_PASS`: **a declaration that comes to cover nothing fails the run**.

**Scope**
- In: a closing-condition field on each `DEFERRED` entry, and a check that reads it.
- In: deciding what a closing condition may be **bound to** — another rule's id, a tool that must not
  exist, a capability the harness must gain. An entry whose condition binds to nothing is the defect
  this task is about, so it must fail rather than be accepted.
- In: the sweep — every existing `DEFERRED` entry gets one, or is reported.
- Out: re-deciding any excusal. This makes them answerable, it does not answer them.
- Out: the same question for the ruleset's `Reach` cells. One home at a time; `Reach` is prose in a
  table and a different problem.

**Inputs**
- [T-097](T-097-ds-004s-excusal-says-degrade-gracefully-is-unobservable-and-ds-009-gave-it-an-instrument.md)
  §1 and §4 — the instance, and why the account cannot see it
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED`, and `account`
- [`tools/deck/audit.py`](../tools/deck/audit.py) `ABSENCE_IS_A_PASS` — a hand-kept table whose claims
  are **verified rather than trusted**, which is the pattern to copy
- **L-54**, **L-84**, **L-97**

**Acceptance criteria**
- [ ] Every `DEFERRED` entry carries a closing condition in a form a check reads, or is reported
- [ ] A condition that binds to nothing fails the run, demonstrated on a seeded entry
- [ ] An excusal whose condition is **already satisfied** is reported — that is DS-004's case, and the
      one nothing can see today
- [ ] The coverage account's arithmetic is unchanged, or its change is stated
- [ ] The self-test builds its own entries and does not assert the live table's contents (**L-78**)

**Open questions**
- **Can a closing condition be checked without running the thing that would close it?** DS-004's was
  *a second engine in the harness*; nothing can test that cheaply. A condition naming another **rule
  id** is decidable from the ruleset alone, which suggests two kinds and only one of them
  enforceable. — the implementer, at `specify`.

## 2. Plan

**The open question is answered at `specify`, as §1 asked: two kinds of condition, and the split is
not where the question put it.** It is not *rule ids are enforceable and the rest are not*. Every
condition can be held to **binding** — its subject must resolve to something — and only one kind can
be held to **satisfaction**. Binding is where the defect was: an entry that points at nothing is
what nobody could report.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `DEFERRED` values become `(reason, (kind, subject))`, every reason string byte-identical | one table, not two — a closing condition in a second dict is one fact in two homes |
| 2 | `CLOSING_KINDS` — a closed vocabulary of six, each saying what its subject must be | the kinds are a declaration a check reads, not a comment |
| 3 | `closing_faults()` — binding for all six kinds, satisfaction for `rule` | one function, and it is what `run` folds into `coverageFaults` |
| 4 | Fixtures that build their own entries, one per way a condition breaks, plus the satisfied case | **L-78**: never an assertion about the live table's contents |
| 5 | The live table asserted to **bind** — a property, not its contents — and the verbose report prints the count per kind, zeroes included | **L-36** |

## 3. Implement

**Decisions & assumptions**
- **One table, not two** — 2026-08-16. A parallel `CLOSES = {rid: …}` would have been a two-line
  diff instead of a rewrite of 27 entries; it is also one fact in two hand-kept homes, which is the
  failure this repository keeps paying for. The rewrite was scripted and asserted: every reason
  string comes out byte-identical, checked by `ast.literal_eval` on the block before and after.
- **Six kinds, and only `rule` is decidable** — 2026-08-16, answering §1's open question. `rule` (a
  named rule's check closes it), `amendment` (the rule's own text), `deck` (no deck here ships the
  subject), `work` (the measurement has not been built), `harness` (a capability not ours to write),
  `look` (a person, CLAUDE.md rule 6, subject `None`).
- **A satisfied condition fails the run, at the same weight as `staleExcusals`** — 2026-08-16. It is
  the same defect one step earlier, and a softer verdict would let it accumulate.
- **Two entries were NOT classified as `rule`, and the reason is recorded rather than buried.**
  DS-131's prose says *checked in substance by DS-217's scale verdict* and DS-145's says *flows use
  dashed arrows is the DS-140 row*. Read as `rule` conditions, both are satisfied today and the gate
  goes red on all three decks. But both entries **open** with `Triage: default` — the owner's triage
  order is what holds them, and the citation is offered as why holding them is safe. Classifying
  them as `rule` would manufacture the result this task hoped for, on a reading that is the owner's.
  They are `work`, and this paragraph is the candidate.

**Outputs produced**
- [`tools/deck/check.py`](../tools/deck/check.py) — `DEFERRED` restructured, `CLOSING_KINDS`,
  `closing_faults`, the fold into `coverageFaults`, the verbose report, and eleven fixtures.
- [`docs/lessons/L-109.md`](../docs/lessons/L-109.md) and its index row.

**What the live table turned out to be.**

```
by what would close it: amendment 10  deck 2  harness 1  look 7  rule 0  work 7
```

**All 27 bind. None is satisfied. The one decidable kind is the one at zero** — nothing here waits on
another rule's check today, which is the honest measurement and is [`L-109`](../docs/lessons/L-109.md).

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every `DEFERRED` entry carries a closing condition in a form a check reads, or is reported | met | All 27, as `(kind, subject)` in the same table as the reason. `self_test` asserts the live table binds — a property, not its contents — so an entry added without one fails the run |
| A condition that binds to nothing fails the run, demonstrated on a seeded entry | met | Five seeded breakages, each its own fixture: no condition at all, an unknown kind, a rule id the ruleset does not own, a `look` that also names a subject, a phrase too short to act on. Three sound entries alongside them, so the check is shown refusing *and* accepting |
| An excusal whose condition is **already satisfied** is reported | met, on a fixture, and **no live entry is in this state** | The fixture says `DS-000` closes when a real rule is checked, and the account says it is: reported. The mirror fixture — some *other* rule checked — is not, so the field cannot fire on every run. Live: `rule 0`, and the two entries that could have been read that way are the decision recorded in §3 |
| The coverage account's arithmetic is unchanged, or its change is stated | met, unchanged | `buckets sum to 115 = owned, so the account is a partition`, on the reference deck before and after. `closing_faults` adds to `coverageFaults`, which is the failure list — it touches no bucket |
| The self-test builds its own entries and does not assert the live table's contents (**L-78**) | met | Every fixture passes its own one-entry dict and its own `owned` set. The one assertion about the live table is that it **binds**, which survives any edit that keeps the property — which is exactly what L-78 asks for |

**Nothing this task produced renders.** It is a declaration and a check over it; no deck changed and
no browser was launched. `TASK-WORKFLOW.md` §7 step 3 is not owed.

**Regression surface.** `python tools/check_all.py`: **25 checkers ran, 1 failed** — `figures.py`,
which is [T-172](T-172-the-shell-sync-falsified-four-published-deck-figures.md) and predates this.
`DEFERRED` has exactly one reader outside `check.py`: none. Every in-file reader was updated —
the account's key sets are unaffected, the `< 40` prose-length fixture unpacks the tuple, and the
verbose report prints the kind beside the reason.

**Child fix tasks raised**
- none. The DS-131 / DS-145 reading in §3 is a candidate for the owner, recorded there rather than
  raised: it is a re-decision of two excusals, and §1 puts that explicitly out of scope.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → done | Specified, planned, implemented and reviewed in one unattended pass, closing the batch. **All five criteria met**, the third on a fixture because **no live entry is in the state it names**. The open question was answered at `specify` and the answer moved the line: the split is not *rule ids versus the rest* but **binding versus satisfaction** — all six kinds bind, one is decidable, and it is the one at zero across 27 entries. That is [`L-109`](../docs/lessons/L-109.md), and the temptation it names — reading two `Triage: default` entries as `rule` conditions to make the branch cover something — is recorded in §3 as the owner's to take. **§7 step 3 is not owed**: nothing here renders. |
| 2026-08-15 | → proposed | Raised at T-097's review against its fifth acceptance criterion, which asked for exactly this decision: an excusal **cannot** be held to its closing condition mechanically today. **The evidence is T-097 itself** — DS-004's reason half-died when T-019 shipped DS-009's preflight, and `staleExcusals` could not see it because it only fires on a rule that is excused *and* checked. `s`, `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
