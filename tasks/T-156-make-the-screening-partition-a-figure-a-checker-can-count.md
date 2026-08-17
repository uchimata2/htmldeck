---
id: T-156
title: Make the screening partition a figure a checker can count
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-136, T-154, T-130]
work_package: PH3
shipped_in: 0.3.0
owner: the project owner
business_value: medium
effort: s
created: 2026-08-14
updated: 2026-08-15
deliverables: [tools/docs/screening.py]
---

# T-156 — Make the screening partition a figure a checker can count

## 1. Specify

**Outcome**
The sentence *"the three verdicts partition the catalogue: N adopted, M rejected, K deferred, summing
to S"* stops being prose nobody checks. A command counts the rows of the screening table in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 and the catalogue rows in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§7, and a gate fails when either the four numbers in the sentence or the two documents' totals
disagree with what is actually there.

**Why this exists**
Found while re-running the research
([T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md)). **The claim has been
wrong twice and no gate said so** — first at nineteen entries with two missing, then at twenty-one
with fourteen missing. Both times the arithmetic inside the sentence was self-consistent, because the
sentence was checked against itself.

**It is a part-of-whole claim with no binding.** `tools/docs/figures.py` binds exactly this shape, but
only through a declared `ACCOUNTS` entry naming a command whose output carries the labels — and there
is no command that prints these counts. The claim is a *count of table rows the document itself
contains*, which is the easiest kind of figure to derive and the only one here still hand-maintained.
**L-97** is the general rule: a check anchored on the value that drifts goes blind exactly when it is
needed.

**Scope**
- In: a command that counts the two tables and prints the four numbers with their labels.
- In: an `ACCOUNTS` entry binding the §4 sentence to it, or a reason recorded for why the existing
  binding cannot serve and what does instead.
- In: the cross-document check — the size stated in `R8` §7 and in `CONTEXT-AUDIT.md` §4 must agree.
- Out: changing any verdict. This is a checker, not a re-screening.
- Out: generalising to every table in the tree. **Two documents, one claim.**

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §4 and §4.1 — the claim and how it was found
- `tools/docs/figures.py` — `ACCOUNTS`, and the module docstring's account of what a binding owes
- [T-154](T-154-bind-the-measurements-that-five-live-documents-state-in-prose.md) §3 — the false-alarm
  count that decides whether a binding of this shape is worth keeping
- **L-84**, **L-97**

**Acceptance criteria**
- [ ] A command prints the three verdict counts and the total, from the tables themselves
- [ ] A seeded wrong number in either document fails the gate, and the failure names which document
- [ ] A row added to `R8` §7 and left unscreened in §4 fails the gate — that is the case the partition
      never caught
- [ ] The check runs inside `python tools/check_all.py`, or its absence there is recorded with a reason
- [ ] No verdict text is edited by this task

**Open questions**
- ~~**Does this belong in `figures.py` or beside it?**~~ **Answered 2026-08-15: beside it, and the
  reason is the claim's own.** `ACCOUNTS` was the obvious route and it cannot serve. `figures.py`
  binds a prose numeral by finding a field whose **value** matches and whose label the sentence
  names — so a figure that has *drifted* matches no field, binds to nothing, and falls into
  `unanchored` among four hundred numerals that are not figures at all. It would read `compared` for
  exactly as long as the number was already right. That is **L-97**, which §1 already cites, and it
  disqualifies the binding rather than merely making it awkward. A partition has to be asserted the
  other way round — count the rows, then require the page to state that number (**L-104**, the same
  inversion T-158 reached from the other end).

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the open question against `figures.py`'s actual binding rule, not its docstring's summary of it | `ACCOUNTS` disqualified by **L-97** |
| 2 | `tools/docs/screening.py` — read §4's table and §7.2's catalogue by **heading**, never by line number, so an edit above either cannot move what is counted | the two row sets |
| 3 | Match the sentence on its own vocabulary, and **fail when it cannot be read**: a reworded claim is an unchecked claim, which is `ARTIFACTS`' condition applied to a sentence | the four stated numbers |
| 4 | Compare three ways: stated against counted, id set against id set in both directions, and any row carrying no verdict | the complaints, each naming its document |
| 5 | Self-test on a synthetic document pair — the live numbers are the subject, so a fixture quoting them asserts today and reddens tomorrow (**L-78**, **L-85**) | seven seeded cases |
| 6 | Add to `tools/check_all.py`'s `WIDE`; the manifest names every tracked tool exactly once, so a new tool wired nowhere goes red by construction | criterion 4 |

## 3. Implement

**Decisions & assumptions**
- **A tool beside `figures.py`, not an `ACCOUNTS` entry inside it** — 2026-08-15. See the open
  question: value-anchored binding goes blind exactly when the figure is wrong.
- **Sections are found by heading, not by line number** — 2026-08-15. `CONTEXT-AUDIT.md` §4 sits
  after 200 lines that change often; anchoring on the heading means an edit above it cannot silently
  change what the tool counts.
- **An unreadable partition sentence fails the run** — 2026-08-15. The alternative is a tool that
  quietly checks nothing after somebody rewrites the sentence, which is the shape `missing_artifacts`
  and `missing_measurements` both exist to refuse.
- **Two directions of id comparison, not one.** A catalogued technique nobody screened is the case
  the sum cannot see, and it is why this task exists; a screened id the catalogue does not carry is
  the mirror, and leaving it silent would let the screening table invent techniques.
- **A row with no verdict is reported.** It sits in the total and in no part, so the three counts
  stop summing to it — a way for the partition to be false that neither the sentence nor the id sets
  would catch.

**Outputs produced**
- [`tools/docs/screening.py`](../tools/docs/screening.py) — the checker, standard library only.
- [`tools/check_all.py`](../tools/check_all.py) — one `WIDE` entry.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A command prints the three verdict counts and the total, from the tables themselves | met | `python tools/docs/screening.py` prints `adopted 12 / rejected 10 / deferred 13 / total 35`, counted from §4's rows, beside the sentence's own four numbers and the catalogue's 35. |
| A seeded wrong number in either document fails the gate, and the failure names which document | met | Demonstrated on the real documents, in memory. `12 adopted → 13 adopted` gives `docs/CONTEXT-AUDIT.md says 13 adopted and its own table holds 12`. Every complaint carries the path of the document at fault, and the cross-document ones carry both. |
| A row added to `R8` §7 and left unscreened in §4 fails the gate — that is the case the partition never caught | met | Seeding a `T36` row into §7.2 gives `…R8… catalogues T36 and docs/CONTEXT-AUDIT.md screens none of them`. The stated partition still sums to 35 throughout, which is precisely why the sum was never the check. |
| The check runs inside `python tools/check_all.py`, or its absence there is recorded with a reason | met | Added to `WIDE`, after `figures.py`. The manifest names every tracked tool exactly once, so it could not have been left out silently. |
| No verdict text is edited by this task | met | The only documents touched are the tool, the manifest and this record. `docs/CONTEXT-AUDIT.md` and `R8` are unchanged — the claim was **already true** at 12/10/13/35, so nothing needed correcting and the check landed green. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → done | All five criteria met. **The claim was true on the day it became checkable**, so this buys nothing today and everything on the next edit — which is the point of a figure that has been wrong twice. The open question turned on a property of `figures.py` rather than on taste: value-anchored binding reports `compared` only while the number is already right, so it is blind in the one state that matters (**L-97**). The partition therefore had to be asserted from the rows toward the page, the same inversion T-158 reached from the other end (**L-104**). |
| 2026-08-15 | → in_progress | Written as `tools/docs/screening.py`, standard library only, with seven seeded self-test cases on a synthetic document pair and one `WIDE` entry. |
| 2026-08-15 | → planned | §2 written. Step 1 is the open question, because the answer decides whether this task edits `figures.py` or adds a file beside it — and it was settled by reading `bound()` rather than the docstring's account of it. |
| 2026-08-15 | → specified | §1 was complete when T-136 raised it on 2026-08-14 and the status was never advanced. |
| 2026-08-14 | → proposed | Raised by [T-136](T-136-re-run-the-external-research-with-a-recorded-search-record.md) while re-running the research. **The partition sentence has been wrong twice and is checked by nobody**: it is a part-of-whole claim over rows the document itself contains, and `figures.py` binds that shape only through a declared `ACCOUNTS` entry pointing at a command — which does not exist for it. `PH3` because PH2 has shipped and this is not a defect in the published plugin. |
