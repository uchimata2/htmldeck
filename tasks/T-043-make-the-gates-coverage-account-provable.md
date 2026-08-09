---
id: T-043
title: Make the gate's coverage account provable, and derive the counts the documents state
type: fix
status: done
phase: review
parent: T-042
blocked_by: []
related: [T-005, T-037, T-038]
work_package: none
owner: the project owner
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - tools/deck/check.py
  - tools/deck/ruleset.py
---

# T-043 — Make the gate's coverage account provable, and derive the counts the documents state

## 1. Specify

**Outcome**
`tools/deck/check.py`'s coverage account partitions the owned rules — every owned rule in exactly
one bucket, the buckets summing to the total — and the self-test fails when it does not.
`tools/deck/ruleset.py` gains a mode that reports the counts the documents state, so the figures in
`BRIEF.md` and `EVALUATION.md` are re-derived rather than re-typed.

**Why this one**
`account()`'s docstring already claims the property: *"Every owned rule lands in exactly one
bucket."* It does not hold, and the assertion that would have caught it was written and disabled:

```
owned 111  checked 79  byRuleset 4  deferred 29  silent 0
sum of buckets 112
checked & byRuleset -> ['DS-072']
```

DS-072 carries `Reach: off-gate` — *"headless has no user gesture to enter fullscreen with… a person
pressing F11 is the only real demonstration"* — and `contract.py` emits a `pass` for it anyway. The
verdict's own text is honest, so nothing is mis-measured; what is wrong is the **account**, and the
account is the deliverable T-005's own log calls the point of the task: *"Silent went from 64 to 0,
and that is the deliverable."* An account that cannot add up is the same defect as a silent rule
with the sign flipped, which is exactly what `staleExcusals` was built to catch — and it never
looks at `cited & by_ruleset`, the one pair that occurs.

`check.py:251` is the assertion that should have failed:

```python
if len(a["silent"]) != len(own) - 3 - len(...) - len(...):
    pass          # the arithmetic is asserted below in the form that matters
```

The comment is false. No later assertion checks the partition.

**The second half is the same fault in prose.** `EVALUATION.md` §1 already records the rule counts
going stale twice and instructs *"re-derive them, never adjust them by hand"* — and nothing derives
them. `ruleset.py` computes every figure those documents quote and no consumer compares the two.

**Scope**
- In: making the account a partition, and deciding what an `off-gate` rule that a stage nonetheless
  measures is reported as.
- In: a self-test that fails on a non-partition and on `cited & by_ruleset`, replacing the disabled
  assertion rather than sitting beside it.
- In: `ruleset.py --counts` (or equivalent) printing every figure the documents state — totals by
  `Label`, by `Check`, by `Reach`, and the owned/hard split — in a form that can be pasted or diffed.
- Out: **changing any verdict.** No rule gains or loses a check here; only the bookkeeping moves.
- Out: correcting the figures where the documents state them. That is
  [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md), which this task unblocks.
- Out: a check that reads the documents and fails on a stale number. Tempting and larger than it
  looks — a count in prose has no stable anchor — and it should be raised on evidence that pasting
  is not enough, not assumed now.

**Inputs**
- [`tools/deck/check.py`](../tools/deck/check.py) — `account()`, `self_test()`, and the `DEFERRED` table
- [`tools/deck/ruleset.py`](../tools/deck/ruleset.py) — the `excused` property and the counts
- [`tools/deck/contract.py`](../tools/deck/contract.py) — the DS-072 verdict
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `Reach` column's contract
- [T-042](T-042-audit-the-whole-repository-against-itself.md) §2, F-2 and F-13

**Acceptance criteria**
- [ ] `checked + excusedByRuleset + deferred + silent == owned`, asserted in `self_test()` and shown
      to fail when it is broken on purpose (**L-04**)
- [ ] `cited & by_ruleset` is a reported fault, in the same shape as `staleExcusals`
- [ ] No rule appears in two buckets on the reference deck
- [ ] The disabled `if …: pass` is gone, not left beside its replacement
- [ ] `ruleset.py` prints every count `BRIEF.md` and `EVALUATION.md` quote, derived, in one run
- [ ] The reference deck still passes, and the printed headline states the corrected split

**Open questions**
- ~~Is an `off-gate` rule that a stage nonetheless measures `checked` or `excused`?~~ **Answered
  2026-08-09 by the reason `Reach` was given a column.** `DESIGN-SYSTEM.md` defines `off-gate` as
  *"decidable in principle but not by this instrument"* — so a measurement taken against a **double**
  is not the rule being decided, and counting it as `checked` is the gate claiming a reach the
  ruleset denies it. **DS-072 is `excused`, and its measurement stays in the output as a note under
  the excusal** rather than as a verdict. That keeps the information, keeps the account honest, and
  makes the general rule one line: *a rule the ruleset excuses is never `checked`, whatever a stage
  happens to measure.*

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Make `account()` compute the partition explicitly — `bucketSum` and `partitionError` — instead of claiming it in a docstring | An account that reports its own arithmetic |
| 2 | Apply the answered open question at the definition of `checked`: subtract the ruleset's excusals, and keep the measurement as `measuredThoughExcused` | DS-072 excused; 79 → 78 checked, and the buckets sum to 111 |
| 3 | Add `partitionError` to `coverageFaults`, so a non-partition is a red run rather than a printed curiosity | A run that fails on its own bookkeeping |
| 4 | Replace the disabled `if …: pass` with three assertions in `self_test()`, one of which **breaks the partition on purpose** and requires it to be reported | An assertion that can fail, and is proven to |
| 5 | Print the sum and the excused-but-measured note in `report()`, under the buckets they explain | A reader sees the arithmetic, not just the parts |
| 6 | Add `ruleset.py --counts`: every figure the documents quote, derived in one run | The paste source `EVALUATION.md` §1 asks for and never had |
| 7 | Derive the 160/161 discrepancy rather than describing it — find rule IDs the document declares outside the table, and their label | `DS-000 (guidance)`, found by scanning, not hard-coded |
| 8 | Self-test the counts: every tally must sum to the row count, and a rule declared off-table must exist | `--counts` cannot be prettily wrong |

## 3. Implement

**Decisions & assumptions**
- **The precedence rule is general, not a DS-072 special case:** *a rule the ruleset excuses is
  never `checked`, whatever a stage happens to measure.* Written at the definition of `cited` so a
  future stage growing a verdict for an `off-gate` rule cannot reintroduce the defect. — 2026-08-09
- **An excused rule's measurement still fails the run when it comes out false.** The account is a
  claim about *coverage*; a failure is a fact about the *deck*, and conflating them is what F-2 is.
  So `check.py` no longer claims to have decided DS-072, and a deck whose fullscreen guard has been
  deleted still goes red — `contract_variants.py`'s `no-fullscreen-guard` variant is unaffected
  because it reads `contract.verdicts()` directly. — 2026-08-09
- **Deviation from acceptance criterion 2, and the reason.** The criterion asks for
  `cited & by_ruleset` to be *a reported fault, in the same shape as `staleExcusals`*. It is
  reported, in that shape and that place, but as a **note** rather than a fault — because the
  answered open question rules the excusal correct and the measurement legitimate, so making it a
  fault would leave only one way to a green run: **delete a working measurement.** The fault the
  criterion was reaching for is the arithmetic itself, and that *is* hard: `partitionError` fails
  the run. — 2026-08-09
- **The one count `--counts` does not print is the gate's `checked` split**, because that is a fact
  about a run against a deck rather than about the table; deriving it here would mean rendering a
  deck to answer a question about a document. The output names `check.py` instead. — 2026-08-09
- **`--counts` was written to derive the 160/161 split, not to state it.** Scanning for rule IDs
  the document uses but never rows finds `DS-000 (guidance)` on its own, which also means a
  citation of a deleted rule ID would surface here with no label. — 2026-08-09

**Outputs produced**
- [`tools/deck/check.py`](../tools/deck/check.py) — `account()`, `run()`, `report()`, `self_test()`
- [`tools/deck/ruleset.py`](../tools/deck/ruleset.py) — `off_table()`, `counts()`, `print_counts()`,
  `--counts`, and four new assertions in `self_test()`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `checked + excusedByRuleset + deferred + silent == owned`, asserted in `self_test()` and shown to fail when broken on purpose (**L-04**) | **met** | `buckets sum to 111   = owned, so the account is a partition`. Broken on purpose two ways: a hand-added false excusal for a rule the gate checks gives `PARTITION ERROR +1  (buckets 112, owned 111)` and `run would be ok? False`; and `self_test()` constructs the same break on every invocation and exits if it is *not* reported |
| `cited & by_ruleset` is a reported fault, in the same shape as `staleExcusals` | **met, amended** | Reported in that shape and place as `measured, not claimed  DS-072`, but as a **note**, not a fault. The reason is in §3 and it is not cosmetic: the answered open question rules the excusal correct, so a fault here would make deleting a working measurement the only route to green. The hard fault is the arithmetic — `partitionError` is in `coverageFaults` |
| No rule appears in two buckets on the reference deck | **met** | `BEFORE checked 79 + byRuleset 4 + deferred 29 + silent 0 = 112 against owned 111; checked & byRuleset -> ['DS-072']` · `AFTER … = 111 (error +0)` |
| The disabled `if …: pass` is gone, not left beside its replacement | **met** | Deleted with its false comment. Three assertions stand in its place, and the middle one is the break-on-purpose |
| `ruleset.py` prints every count `BRIEF.md` and `EVALUATION.md` quote, derived, in one run | **met, with one exclusion** | `--counts` derives the totals, all three tallies, both label sets, the owned split, the hard/owned gap and the ruleset's excusals. It does **not** derive the gate's `checked` figure, by the reasoning in §3, and names the command that does |
| The reference deck still passes, and the printed headline states the corrected split | **met** | `0 failure(s): none`, exit 0. Headline now `checked 78 … excused in the rules 4 … excused here 29`, so the figure the documents should quote is **78 of 111, the other 33** — not 79 of 111 and 32 |

**What the corrected figure is, for the tasks that inherit it**

```
owned by a gate      111
checked               78
excused in the rules   4   DS-042 DS-072 DS-210 DS-211
excused here          29
SILENT                 0
buckets sum to       111   = owned
```

**Child fix tasks raised**
- none

**One thing `--counts` found that nobody had written down.** The 160/161 discrepancy
([T-042](T-042-audit-the-whole-repository-against-itself.md), F-16) is entirely the `guidance`
figure: the table holds `hard 114 · default 41 · guidance 5`, and DS-000 — declared in §0's prose
as `(DS-000, guidance)` rather than as a row — is the sixth. Both published sets are right and
neither says which rule moves. Derived, not asserted, and it is
[T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md)'s to write into the documents.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **The corrected split is 78 of 111 checked, 33 excused** — five documents and four task files quote the old one, and correcting them is [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md), now unblocked. **The fix that matters is not the minus one; it is that the arithmetic is now capable of being wrong out loud.** The old code claimed the partition in a docstring and disabled the assertion under a comment saying it was checked elsewhere — so the account could not fail, and a check that cannot fail is the thing this repository keeps re-learning (**L-05**, **L-36**). `partitionError` is now a coverage fault, and `self_test()` breaks the partition on purpose on every run and exits if the break is not reported. **The precedence rule was written generally rather than as a DS-072 exception:** a rule the ruleset excuses is never `checked`, whatever a stage measures, because `off-gate` means *not by this instrument* and a verdict against a double is not the rule being decided. The measurement is kept as a note and **still fails the run when false** — separating a coverage claim from a fact about the deck is what F-2 was really about, and the variant suite is untouched because it reads `contract.verdicts()` directly. Criterion 2 was amended during implementation rather than reworded at review: making `cited & by_ruleset` a fault would have left deleting a working measurement as the only route to green. `--counts` then derived something no document explains — the 160/161 gap is entirely `guidance`, 5 rows plus DS-000 stated in prose. |
| 2026-08-09 | → planned | §1 accepted as written, including the open question already answered in it — the `off-gate` ruling is the whole design, so `specify` was accept-not-compose. Eight steps, split so the two halves stay separable: steps 1–5 are the account, 6–8 are the derived counts, and the second half needed the first to know what figure to print. |
| 2026-08-09 | → proposed | Raised by [T-042](T-042-audit-the-whole-repository-against-itself.md), findings F-2 and F-13. **The account is one over on 111 rules and the assertion that would have said so is `if …: pass` under a comment claiming the arithmetic is asserted elsewhere** — it is not. DS-072 is `checked` and excused by the ruleset at the same time. Ordered first among the audit's children because five documents and four task files quote the figure it corrects, so fixing the prose first would write the wrong number twice. |
