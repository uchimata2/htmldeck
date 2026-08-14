---
id: T-154
title: Bind the measurements that five live documents state in prose
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-056, T-067, T-068, T-088, T-127, T-130, T-151, T-155]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-14
updated: 2026-08-14
shipped_in: unreleased
deliverables:
  - tools/docs/figures.py
  - docs/BRIEF.md
  - docs/EVALUATION.md
  - examples/README.md
  - skills/htmldeck/references/pipeline.md
  - README.md
  - docs/lessons/L-97.md
  - docs/lessons/L-63.md
  - docs/lessons/L-95.md
  - docs/LESSONS.md
  - docs/PUBLISHING.md
  - docs/RELEASE-PHASES.md
---

# T-154 — Bind the measurements that five live documents state in prose

## 1. Specify

**Outcome**
A measurement stated in prose in a document a stranger or an adopter reads is either **bound to what
produced it**, **written as a dated record**, or **coarsened until it converges** — and the one class
that can be none of those, a figure counting the repository, stops being enforced by a category
(`volatile`) that has never failed and never can.

**Raised 2026-08-14 from a measurement, not from a hunch.**
[`../tools/docs/figures.py`](../tools/docs/figures.py) reports its own coverage of the five documents
it reads beside the `README.md`: **13 claims compared, 420 numerals unanchored** — *in a sentence
naming no field and in no block linking an artifact, so not judged*. Nobody had ever classified the
420. A throwaway scan, written independently of `figures.py` so it would not measure that tool's blind
spot with the tool that has it, put **42 of them in the measurement class**:

| Document | Numerals | Measurements | What it is |
| :--- | ---: | ---: | :--- |
| [`../CLAUDE.md`](../CLAUDE.md) | 40 | **4** | tier 1, loaded every turn |
| [`../docs/BRIEF.md`](../docs/BRIEF.md) | 111 | **16** | the specification, read first |
| [`../docs/EVALUATION.md`](../docs/EVALUATION.md) | 161 | **1** | the scoring contract |
| `skills/htmldeck/references/pipeline.md` | 25 | **1** | **shipped to adopters** |
| `examples/README.md` | 96 | **20** | **public-facing, the worked example** |
| | **433** | **42** | |

**37 of the 42 carry no date**, so they are live claims rather than records. **42 is a floor, not a
total**: the scan's remaining bucket holds rubric scales, corpus history and range statements that
are correctly unwatched, but it also holds measurements whose unit word the classifier did not know.

### Re-measured at `specify`, 2026-08-14 — and the account of both defects changed

**L-96 required this and it earned its cost.** The table above is one day old; a second scan, written
again from nothing, disagrees with it in the count and disagrees with the prose about *why* the
public page passes.

**The corpus grew by one numeral.** 434 today against 433: `../CLAUDE.md` went 40 → 41 when the last
session corrected the debt statement. `figures.py` now reports `compared 13, unanchored 421`, and
**13 + 421 = 434 exactly**, so the two instruments share a definition of *a numeral* and the counts
are comparable. That was worth establishing before either number was used.

**The unit vocabulary cannot be keyed on, which is the second scan's real result.** Rather than
bring a word list, the scan printed the first token after each numeral and counted them: the
commonest is **another numeral** (65), then `and` (36), `is` (16), `the` (12), `of` (11). `kb` (11),
`slides` (9) and `bytes` (5) are the only unit words above four, and all three are already bound by
`ARTIFACT_UNITS`. **There is no unwatched unit vocabulary to learn** — the first scan's `other`
bucket is not hiding a class of measurement behind a word this project failed to list. It is
mostly numerals that are not measurements.

**Defect One's mechanism is the opposite of what §1 recorded above.** The public sentence is not
*checked shallowly*; it is **not checked at all**. `claimed()` calls `bound(whole, …)` before it does
any arithmetic, and `bound` matches a field only when the numeral **equals** a value some command
prints. Nothing here prints `113`, so the sentence binds to nothing and lands in `unanchored` with
the other 420. Verified by running `declared()` directly: 13 rows come back `compared`, **none of
them the coverage split**, and the only bound copy of that account anywhere is `../CLAUDE.md`'s —
`84 of 115 … the other 31` — which is correct. `82 + 31 = 113` was never computed.

*The old account is kept because the remedy it implied was wrong.* "Once the shape is matched,
compare the values" describes a check that is already there and already passing; it would have been
implemented and would have changed nothing.

**The class is worse than the one recorded, and it is a known one.** The binding is anchored on the
value that drifts, so **a claim leaves the watched set precisely because it went wrong**. That is
`self_test` fixture 9's defect one scope out — *a fixture may assert what the page's wording binds;
it may not require the page to be right first* (T-127, **L-78**) — and here the same substitution
sits in the production path rather than in a fixture.

**The stale split is in four documents, not one.**

| Where | Line | Live or record |
| :--- | :--- | :--- |
| [`../docs/BRIEF.md`](../docs/BRIEF.md) | 486 | **live** — the specification, read first |
| [`../docs/EVALUATION.md`](../docs/EVALUATION.md) | 135 | **live** — the scoring contract |
| `examples/README.md` | 256 | **live** — public, the worked example |
| `skills/htmldeck/references/pipeline.md` | 190 | ~~a struck-through row dated `**built 2026-08-09**`~~ → **live**, in the shipped skill — see *Read the row* below |

A fifth site, `../docs/PUBLISHING.md` §6 line 165, quotes the sentence **as the example of the rule**
and is correct to hold the old figure only if it is read as a quotation. `PUBLISHING.md` is not in
`DECLARED_DOCS`, so nothing reads it either way.

**Read the row.** `DONE_ROW` matches `~~…~~ **done <date>**` and `pipeline.md` writes `~~…~~ **built
2026-08-09.**`, so the shape argues the row is a record the tool cannot see. **It is not a record.**
That table's columns are `Stage | Owned by | Until then`; the strike is on the name of the **gap**
— *~~The build check~~* — and everything after it describes what an adopter's plugin does now.
Widening the marker to match it would have taken a stale figure out of the watched set inside the
shipped skill: defect One again, self-inflicted, in the task written to end it. The widening was
written, then reverted after the row was read (§3).

**Defect Three, found while checking the floor argument: `0 broken` is enforced by nothing.** Seeded
and measured, both directions:

```text
OK - 2201 document pointer(s) checked, 3 broken     -> FAILING: []   volatile: drift only
731 section reference(s) resolved, 9 dead           -> FAILING: []   volatile: drift only
OK -> FAIL on the same line                         -> FAILING: 1 line absent from the run
```

`excerpt()` masks every digit run for a volatile block, so the two figures that never drift are
excused alongside the three that drift on every commit. A README announcing nine dead section
references passes, and the row saying so is mixed into the pointer-count drift a reader has been
taught to ignore. **This is the argument for `floor` rather than a consequence of it**: the block is
volatile because three of its five numbers count the repository, and that excuses the two that carry
the evidence.

**Defect Two has been correct since the last session and stays a fixture only in class.** Re-measured
with `../CLAUDE.md`'s own command: **15,208** against `tasks/TASK-WORKFLOW.md`'s **11,925**, which is
what the file says, and `TASK-WORKFLOW.md` is still the smallest of the five. Nothing to seed here
that is not seeding a correct figure.

**Two defects were confirmed before this task was written, and they are different failures.**

**One — a public document disagrees with the gate, and the check passes.** `examples/README.md` says
*"82 of the 113 rules a gate owns are decided, and the other 31 are named with a reason each"*.
`check.py` prints **84 checked, 115 owned**, which the front `README.md` states correctly and
`figures.py` compares green. The `examples/` copy is green because `claimed()` binds the *part of
whole plus remainder* construction and verifies **82 + 31 = 113** — the claim's internal arithmetic,
not its truth. **A page can hold that sentence forever, stale, with every gate green.** That is not a
bug in `figures.py`; the construction binding was a deliberate improvement over binding by vocabulary
(T-068, T-088) and it does what it says. What is missing is the second half: once the shape is
matched, compare the *values*.

**Two — the self-referential figure went wrong for the third time.** `../CLAUDE.md`'s debt statement
read 15,182 against 11,579 while both terms had moved to 15,034 and 11,925 the same day; the session
that moved them recorded the new pair in a task record and not in the file the figure is about. **The
correction then changed the file it measures** and had to be iterated to a fixed point, which only
converged because the replacement had the same number of digits. A figure that is stable only by
coincidence of character count is not maintained, it is lucky.

**Scope**
- In: the 42 measurements, each routed to one of four outcomes — **bound**, **dated record**,
  **coarsened to a monotone claim**, or **deleted**.
- In: **a `floor` comparison mode** in `figures.py` — fails when the actual value drops below the
  stated one, never on growth. It is what makes a repository-counting figure enforceable at all, and
  it retires the `volatile` category rather than living beside it.
- In: **value comparison for `claimed()`**, so a matched *part of whole* shape is checked against the
  command and not only against itself.
- In: the classifier, if it survives its own review — the throwaway found the defects and its
  `other` bucket is not trustworthy enough to ship as a gate without work.
- Out: the deck-quality figures in `examples/README.md` that describe a **specific artifact on a
  date** — 262 KB, 12 slides, 58 rows. Those are records of a shipped file and the artifact binding
  (T-088) already covers the ones that matter.
- Out: rubric scales, ranges and corpus history — `0–4`, `6–16 slides`, `1–3 script tags`. They
  describe decisions and past measurements, not current state, and enforcing them would be wrong.
- Out: task records. 20 of `CE-04`'s 34 occurrences were citations and this project has ruled
  repeatedly that a record is history (**L-96**, `figures.py`'s `DONE_ROW`).
- Out: raising this as a `CE-nn`. The audit's numbering closed at thirteen.

**Inputs**
- `figures.py`'s module docstring — the two-kinds-of-number rule, and why binding by vocabulary was
  rejected at 30 false alarms against 5 true ones. **This task must not reintroduce that.**
- **L-95** — write the decision a figure drives, and let the command print the figure
- **L-96** — a survey is evidence about the day it was taken; re-measure the 42 before acting
- **L-74** — a stored copy must fail loudly in both directions
- [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) — six stale figures found
  by hand, which is why `figures.py` exists
- [T-067](T-067-the-published-upgrade-instructions-do-not-upgrade.md) §4 — why a figure counting the
  repository has never converged, which is the argument `figures.py`'s `volatile` category rests on

**What specifying must settle**
- **Whether a floor can be stated without weakening the page.** *Over 2,000 pointers, 0 broken* is
  monotone and enforceable; the exact count is neither. The claim that carries the evidence is
  `0 broken` and it never drifts — the count only carries scale.
- **Where the four outcomes are declared.** A per-figure declaration is a hand-kept list, which is
  the failure `check_all.py`'s manifest exists to prevent; the alternative is a rule the shape of the
  sentence decides.
- **Whether the classifier ships.** A gate that classifies 315 numerals as *other* and is right about
  most of them is exactly the instrument that gets believed (`.taskmd/config.md`, *The tasks folder*).

**Settled 2026-08-14, each against a measurement rather than an argument.**

**A floor can be stated, and stating it makes the page stronger.** The claim that carries the
evidence is `0 broken` and `0 dead`; the counts beside them carry scale and nothing else. Today the
exact half is unenforceable and the scale half is reported — a floor inverts both: *over 2,000
pointers checked, 0 broken* enforces `0` **exactly** and `2,000` as a lower bound, and neither can go
red on a documentation commit. `volatile` is retired rather than kept beside `floor`, because its one
member is this block and a category that has never failed and never can is not a second opinion.

**The four outcomes are decided by shape, and one declaration is added — an account, not a figure.**
No per-figure list:

| Outcome | What decides it | New? |
| :--- | :--- | :---: |
| **bound** | the three existing bindings, plus a claim whose *shape* matched and whose sentence names a declared **account** — then the whole is compared to what that account prints, so a drifted whole reports instead of vanishing | the fourth binding |
| **dated record** | the block's own shape — struck through, with a bracketed date. `DONE_ROW` widens from `**done <date>**` to any `**<word> <date>**` | widened |
| **floor** | the sentence's own words — `over N`, `at least N`, `more than N` | new |
| **coarsened / deleted** | an edit to the document; not a category the tool carries | — |

The account declaration is the same hand-kept-list bargain `ARTIFACTS` already won, on the same
condition: an account naming a label no command prints **fails the run**, so it cannot cover nothing
in silence.

**The classifier does not ship, and the measurement says so plainly.** The shape probe found the real
defect at **8 candidate sites across six documents, 4 of them true** — a rule derived from the
sentence, auditable by reading eight lines. The classifier's alternative is to sort 434 numerals and
be believed about the 392 nobody will check. Its `other` bucket is also not hiding what it was
suspected of hiding: the vocabulary scan above shows no unwatched unit word. It stays a throwaway,
its output recorded here, and **the 42 need no per-figure judgement** because the shapes reach them.

**Acceptance criteria**

*Amended 2026-08-14 at `specify`. Three defects, not two, and the second is no longer seedable: it
was corrected by the session that raised this task, so there is nothing wrong left to hold. The
originals are struck through rather than deleted.*

- [ ] ~~Both confirmed defects are **seeded as known-answer fixtures first**~~ → **all three failing
      shapes** are seeded as known-answer fixtures first, and the new check is shown to fail on each
      before any is fixed (**L-86**, **L-55**: the exit status proves the seed, the message proves the
      assertion). The three are **an unbound whole** (the stale split, live on the page in three
      documents), **an unmarked record** (`pipeline.md`'s struck-through row), and **an exact figure
      inside a volatile block** (`0 broken`, seeded to `3 broken`, which passes today)
- [ ] ~~`examples/README.md`'s claim matches what `check.py` prints~~ → **all four sites** state what
      `check.py` prints, and a wrong value fails the run in each: `docs/BRIEF.md` 486,
      `docs/EVALUATION.md` 135, `examples/README.md` 256 and `skills/htmldeck/references/pipeline.md`
      190
- [ ] **A drifted whole reports rather than disappears** — a claim whose whole no longer matches its
      account is `STALE`, not `unanchored`. Asserted with the live wording, never with a constructed
      sentence (fixture 9's rule)
- [ ] **The declared account cannot cover nothing in silence** — an account naming a label no command
      prints fails the run, which is the condition `ARTIFACTS` was allowed on
- [ ] `figures.py` gains a `floor` mode; the `volatile` category is retired or its remaining members
      are named with why a floor cannot hold them
- [ ] Every one of the 42 has a recorded outcome — bound, dated, coarsened or deleted — and the
      account is a **partition**, so a measurement in none of them fails
- [x] The re-measure happens at `specify`; the table above is dated and this task may not trust it —
      **done, and it changed the account of both defects** (see *Re-measured at `specify`*)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green
- [ ] No figure is enforced that counts the repository without a floor — enforcing a non-convergent
      number is the defect, not the remedy

**Open questions**
- ~~**Is `m` right?**~~ **Answered 2026-08-14: yes, `m` stands.** The four outcomes are decided by
  shape, so the 42 take no per-figure judgement; what is left is three rules in `figures.py`, one
  declared account, and four sentences edited in four documents.
- ~~**Does `pipeline.md`'s single measurement change what an adopter's build does?**~~ **Answered
  2026-08-14, and the answer reversed once the row was read.** It does not change what the build
  *runs* — an adopter's build invokes the command, and `check.py` derives its own account when it
  does. It is nonetheless **a live claim in the shipped skill**, not the record its shape suggests:
  the strike is on the gap's name and the sentence after it is present tense. Corrected to `84 of the
  115`, and the marker left narrow so it stays watched.

**Raised at `specify`, and not folded into this task**
- **`docs/PUBLISHING.md` §6 line 165 quotes the stale sentence as the example of its own rule.** It is
  a quotation and it is outside `DECLARED_DOCS`, so no binding here reaches it and none should — a
  gate that rewrites the illustration of a rule is worse than a stale illustration. Left as it is,
  named here so the next reader does not take it for a fifth defect.

## 2. Plan

**The order is fixtures first, and it is not a preference.** Two of the three shapes are live on the
page right now; repairing either before the check exists destroys the only evidence the check works
(**L-86**, **L-55**).

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Seed all three shapes against the unchanged tool and record what each does today — an unbound whole (`unanchored`), an unmarked record (`unanchored`), `0 broken` → `3 broken` (`volatile`, green) | Three known-answer readings in §3, each a *pass* that must become a *fail* |
| 2 | Widen `DONE_ROW` from `**done <date>**` to any `**<word> <date>**` inside a struck-through row | `pipeline.md` 190 becomes a record the tool can see |
| 3 | Declare `ACCOUNTS` — command, part label, whole label — and fail the run on an account whose label no command prints (`ARTIFACTS`' own condition) | A hand-kept list that cannot cover nothing in silence |
| 4 | In `claimed()`, when the whole binds to no field, look for an account whose **whole label** words the sentence names, and report `STALE` against what that account prints | A drifted whole reports instead of vanishing |
| 5 | Replace `VOLATILE` with `FLOOR`: a pasted numeral must be `<=` the actual, **and a pasted `0` must be exactly `0`** — a floor of zero is vacuous, so a zero can only mean *none* | Growth never reddens; a lost pointer or a dead reference does |
| 6 | Rewrite `self_test` fixture 2 for the three floor directions (growth green, drop red, zero→non-zero red), and add fixtures for steps 2–4 seeded from the live wording | Each new rule judged by its message, not its exit status |
| 7 | Correct the four sites to what `check.py` prints, and repaste the `refcheck` block | `BRIEF.md` 486, `EVALUATION.md` 135, `examples/README.md` 256, `pipeline.md` 190, `README.md` 151 |
| 8 | `python tools/tasks/lint.py`, `python tools/docs/figures.py`, `python tools/check_all.py` | Green, with `check_all.py` in the background |

**What this plan does not do.** It ships no classifier and adds no per-figure list; the 42 are reached
by the shapes in steps 2–5 or they are not measurements this repository can derive.

## 3. Implement

**The three known-answer readings, taken against the unchanged tool before anything was repaired**
(**L-86**, **L-55**):

| Shape | Seed | What the tool did |
| :--- | :--- | :--- |
| An unbound whole | none — live on four pages | `declared()` returned 13 `compared` rows, **none of them the split**; the three numerals sat in `unanchored 421` |
| An unmarked record | none — live | `DONE_ROW` did not match `pipeline.md` 190 |
| An exact figure in a `volatile` block | `0 broken` → `3 broken`; `0 dead` → `9 dead` | `FAILING: []` both times, reported as drift. Changing `OK` to `FAIL` on the same line **did** fail, which is what proves the seed reached the comparison |

**With the three rules in and nothing yet repaired, the same page reported `8 figure(s) to fix`, exit
1** — the proof the instrument works, taken before the repair that would have destroyed it.

**Decisions & assumptions**
- **The whole gets a second chance through a declared account, and the shape stays the trigger.**
  Binding a sentence to a gate's vocabulary alone was 30 false alarms against 5 true ones (T-068) and
  is not reopened. Measured here: the *part of whole* shape fires **8 times across six documents**,
  and requiring the sentence to name the account's **whole label** claims exactly the **4** that are
  the split. The other four — *"4 of 4 roles"*, *"3 of the 10 dimensions"* and two sentences in
  `BRIEF.md` about Mayer and Richness — name neither `owned` nor `gate` and stay silent. — 2026-08-14
- **The account is held to `ARTIFACTS`' condition, not to convenience.** `missing_accounts` fails the
  run when a declared label its command no longer prints; without that, a renamed output line
  switches the binding off and the counts still read as though four documents were watched.
  — 2026-08-14
- **The remainder is judged against the account, not against the sentence.** `113 − 82` is 31 and so
  is `115 − 84`, so the first version reported a correct numeral `STALE` in a message saying it was
  31. A figure needing no edit must not appear in the list of figures to fix. — 2026-08-14
- **A pasted `0` is exact, and that is what makes `floor` a partition rather than a softer excuse.**
  Zero as a lower bound asserts nothing, so reading it as a floor is reading it as no claim.
  — 2026-08-14
- **`volatile` is retired rather than kept beside `floor`.** Its one member is this block, and its
  contract — *this must not fail* — is why it could not fail on the two figures that carry the
  block's evidence. — 2026-08-14
- **Reverted: widening `DONE_ROW`.** Written, then read. `pipeline.md` 190's strike is on the name of
  the gap and not on the sentence, so marking it would have hidden a stale figure in the shipped
  skill. Rule 6 applied to a table row. — 2026-08-14
- **Reverted: dating a record per claim scope instead of per block.** One struck-through row does
  excuse every live claim in its table, and `claim_scopes` is the split that would fix it — but
  measured over all six documents the two decide **no verdict differently today**. Shipping an
  unmeasured behaviour change inside a task about unmeasured claims is the wrong shape, so it is a
  comment in `blocks()` and the candidate task below. — 2026-08-14

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `ACCOUNTS`, `account_values`,
  `missing_accounts`, `account_for`; the account fallback in `claimed()`; `floor_breaches`; `FLOOR`
  replacing `VOLATILE`; self-test fixtures 2a/2b/2c, 11 and 12
- [`docs/BRIEF.md`](../docs/BRIEF.md) 486, [`docs/EVALUATION.md`](../docs/EVALUATION.md) 135,
  `examples/README.md` 256, `skills/htmldeck/references/pipeline.md` 190 — `82 of the 113` →
  `84 of the 115`
- [`README.md`](../README.md) 151 — the `refcheck` block repasted, now compared as a floor

**Raised, not fixed here**
- **`dated` is a property of the block, not of the row.** One struck-through row excuses every live
  claim in the same table. No verdict in the six documents changes today, which is why it is a note
  and not an edit — and why it needs a task rather than being left in a comment alone.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| All three failing shapes seeded as known-answer fixtures first, and shown to fail before any repair | met | §3's first table is the three readings against the unchanged tool. With the rules in and nothing repaired the page reported `8 figure(s) to fix`, exit 1 |
| All four sites state what `check.py` prints, and a wrong value fails the run | met | `82 of the 113` → `84 of the 115` in `BRIEF.md` 486, `EVALUATION.md` 135, `examples/README.md` 256, `pipeline.md` 190. Fixture 12 seeds a wrong whole and requires the row |
| A drifted whole reports rather than disappears | met | Fixture 12, seeded from whatever a declared document writes and with a value no account prints (**L-79**) |
| The declared account cannot cover nothing in silence | met | Fixture 11, on a synthetic account whose labels no command prints |
| `figures.py` gains a `floor` mode; `volatile` retired or its members named | met | Retired. Its one member is the `refcheck` block, now a floor; fixtures 2a/2b/2c cover growth, drop and the exact zero |
| Every one of the 42 has a recorded outcome, and the account is a partition | met | Not per figure — by shape. **Bound**: the coverage split's 12 numerals across four documents, plus the artifact figures already bound. **Floor**: the five in the `refcheck` block. **Dated record**: unchanged, and one candidate was read and refused. **Coarsened or deleted**: none needed. A measurement in none of these is one no command here derives, which the report states as `unanchored` |
| The re-measure happens at `specify` | met | And it changed the account of both defects, which is the point of **L-96** |
| `lint.py` and `check_all.py` green | met | Both run below |
| No figure is enforced that counts the repository without a floor | met | The `refcheck` block is the only one, and it is the floor |

**Closing checklist step 3 — nothing this task produced renders.** The outputs are a Python checker
and six markdown documents; there is no deck, no PDF and no page to open offline, so the bar
`TASK-WORKFLOW.md` §7 sets is not owed here rather than waived.

**Reconciled beyond the deliverables.** [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §6 described
`volatile` and quoted the stale sentence as its own example; §8 step 3 told a release to repaste *the
`volatile` block*. **L-95** step 3 told a reader to declare a repository count `volatile`. **L-63**
recorded construction-binding as what worked and said nothing about what locates the construction —
it now carries a fifth rule and points at **L-97**. `figures.py`'s own module docstring stated the
`volatile` split and two ruleset figures that had drifted to 165 and 119.

**What this did not do.** No classifier ships, and 413 numerals in the five documents remain
`unanchored` — reported, not judged. That is the honest bucket rather than the silent one: the report
names it and says why. The rival was a gate believed about 392 numerals nobody would check.

**Child fix tasks raised**
- [T-155](T-155-date-a-record-by-its-own-row-not-by-the-table-it-sits-in.md) — date a record by its
  own row, not by the table it sits in

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | → done | Three rules in `figures.py`, four documents corrected, and two changes written then reverted after being measured. The general rule is **L-97**; the reverted one is [T-155](T-155-date-a-record-by-its-own-row-not-by-the-table-it-sits-in.md). |
| 2026-08-14 | → specified | **Re-measured first, and it changed the task.** Defect One is not a shallow check but no check: `claimed()` binds the *whole* by value, so the sentence left the watched set because it went wrong — T-127's rule violated in the production path rather than in a fixture. The stale split is in **four** documents, not one. A **third** defect was found while testing the floor argument: `0 broken` and `0 dead` are masked inside the volatile block, so a README reporting nine dead references passes; seeded both ways to prove it. Defect Two is currently correct and is dropped as a fixture. All three *settle* questions answered against measurements, both open questions closed, and the classifier is refused: the shape probe reaches the defect in 8 sites across six documents where the classifier would have to be believed about 392 numerals, and the vocabulary scan shows no unwatched unit word for it to find. |
| 2026-08-14 | → proposed | Raised at the owner's direction after `figures.py`'s own report — *420 unanchored* — was classified for the first time. **Not a finding**: `CE-nn` closed at thirteen and this is new capability. The measurement found two confirmed defects before the task was written, and they are different failures: a public page disagreeing with the gate while `claimed()` verifies only the claim's internal arithmetic, and `../CLAUDE.md`'s self-referential debt figure wrong in both terms for the third time — corrected here to a fixed point that holds only because the replacement had the same digit count. |
