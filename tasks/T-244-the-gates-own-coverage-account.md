---
id: T-244
title: Derive the clause-level account, and correct two excusals that name the wrong decider
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-244 — Derive the clause-level account, and correct two excusals that name the wrong decider

## 1. Specify

**Outcome**
The gate's account of what it decides is derived from the gate. Today `check.py`'s `CLAUSES` table is hand-kept with a dated sweep behind it and two `hard` rules report `checked` on a clause nothing reads; and two excusals in the coverage account are wrong about what decides the clause they excuse.

**Closes** `PR-43`, `PR-46` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `check.py`'s `CLAUSES` table and the sweep behind it, and its `DEFERRED` entries for DS-226 and DS-145
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-43`, `PR-46`
- `ruleset.py`, which derives rather than tabulates and is the precedent for the first half

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

**`PR-46` is two sentences and goes first**, because it is `xs` and independent — and because
reading what those two excusals actually claim is the cheapest way into the same question `PR-43`
asks at scale: *does this account describe the gate it belongs to?*

**`PR-43`'s remedy is a hypothesis with a prose parser hidden in it.** *Every `hard` rule whose text
carries more than one testable assertion needs a row or an excusal* is a rule about English, and no
program decides it. What a program **can** decide is whether every `hard` rule has been **read** —
and that is the whole of the defect, because the failure here was not a bad judgement about a rule,
it was 24 rules nobody had judged at all. So the sweep becomes a record rather than a sentence, and
the judgement stays where it was.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce both `PR-46` sentences on a default run before touching either | the claims, in the run's own words |
| 2 | Correct the two excusals, DS-226's conditionality and DS-145's cited decider | an account that describes this gate |
| 3 | Measure `PR-43`'s gap as it stands, not as the row states it | the current figure, which is what the row's own defect predicts will have moved |
| 4 | `SWEPT` — one digest per `hard` rule of the row that was read; `sweep_faults` reporting UNSWEPT and CHANGED | a sweep that cannot go stale silently |
| 5 | Watch it failing in both directions, and leave both as fixtures | L-36, and L-125 |
| 6 | Run the sweep the dated sentence had stopped covering: read every unswept rule and judge it | the honest population, whatever size it is |
| 7 | Rows for the two the register named; whatever else the sweep found recorded rather than buried | `PR-43`'s stated scope, plus what step 6 turns up |
| 8 | Close both rows; both gates, separately | register and task agreeing, green |

## 3. Implement

**Decisions & assumptions**

- **The remedy's prose-parser half was refused; its *tie the sweep to the ruleset* half was
  built** — 2026-08-29. *More than one testable assertion* is a judgement about English and no
  check decides it. But the defect was never a misjudged rule — it was **24 rules nobody had
  judged**, which is decidable. So `SWEPT` records, per `hard` rule, a digest of the row somebody
  read; `sweep_faults` reports **UNSWEPT** (arrived since) and **CHANGED** (the row moved since it
  was read). The judgement stays human and the *obligation* is derived.
- **The digest covers the whole row, amendment notes included** — 2026-08-29. A rule acquires a
  second testable assertion in exactly that prose — `DS-218` gained one earlier the same day — so
  hashing some tidier slice would go quiet at the moment the question matters. The cost is that any
  edit re-opens a rule, which is the intended friction: an edit is when to re-ask.
- **There is no `--sweep` writer, deliberately** — 2026-08-29. The failure prints the line to paste.
  A command that re-recorded the digest would let a rule be swept **by running it**, which is the
  dated sentence again behind a nicer interface.
- **The sweep's population is every `hard` rule, not the ones this gate owns** — 2026-08-29. The two
  differ by **34**. The sweep asks *is this statement a conjunction*, which is a question about the
  rule; whether a check reaches it is `CLAUSES`'s question. Scoping the sweep to the jurisdiction
  would excuse a conjunction from being noticed because nothing checks it — the reasoning this whole
  account exists to refuse. The first draft did scope it that way and reported 34 phantom faults,
  which is what surfaced the distinction.
- **The register's figure had moved before anyone read it, which is the finding restating itself** —
  2026-08-29. `PR-43` says **15** `hard` rows carry a date on or after 2026-08-19. Measured today:
  **24**. Nothing went wrong; the row was written days earlier and the set kept moving, which is
  precisely why a dated sentence was the wrong instrument.
- **The sweep found eleven conjunctions, not two, and nine of them are a backlog rather than an
  afternoon** — 2026-08-29, and this is the decision worth arguing with. Reading all 24 unswept
  rules gave: `DS-092` and `DS-100` (already had rows), `DS-242` and `DS-073` (the two the register
  named, written here), and **`DS-110`, `DS-122`, `DS-141`, `DS-146`, `DS-202`, `DS-218`, `DS-229`,
  `DS-230`, `DS-238`**. That is roughly twenty further clauses, each needing somebody to decide
  whether a check reaches it and to defend a closing condition where none does. Written fast they
  would be nine excusals reading *not checked*, which **inflates the account rather than sharpening
  it** — the exact failure the `CLAUSES` preamble warns about. So they are
  [T-278](T-278-write-the-clause-rows-the-sweep-found-owing.md).
- **`SWEPT` alone would have laundered them, so `CONJUNCTIONS_OWED` exists** — 2026-08-29, and it is
  the correction I owe most. A record saying *somebody read this* is read as *and found it states
  one thing*; nine rules known to be conjunctions would then have been swept into silence **by the
  record built to prevent exactly that**. The set names them, prints on every run, and is checked
  against `CLAUSES` and `SWEPT` for contradiction.
- **The backlog does not fail the run** — 2026-08-29. It is work with a named owner, in the shape
  [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) already uses. Failing on it would hold the gate red for
  as long as the queue is non-empty, which turns an honest count into a reason to stop counting.
  What *does* fail is a contradiction between the two records.
- **DS-145's excusal contradicted itself, which the register did not name** — 2026-08-29. It called
  the dashed-arrow clause covered by DS-140 while its **closing condition asked for work on that
  same clause**. DS-140's `Current renders dashed` row does decide it; the *reveal* clause is
  decided by nothing, and its old ground — DS-140's starter set — stopped existing when T-187 opened
  the vocabulary on 2026-08-21. The closing condition now names the reveal clause.

**Outputs produced**
- [`tools/deck/check.py`](../tools/deck/check.py) — `SWEPT`, `rule_rows`, `rule_digest`,
  `sweep_faults`, `CONJUNCTIONS_OWED`, `sweep_debt`; the two new `CLAUSES` rows; the two corrected
  `DEFERRED` excusals; the report block and the two self-test fixtures
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — `PR-43` and `PR-46` closed
- [T-278](T-278-write-the-clause-rows-the-sweep-found-owing.md) — the nine conjunctions owing rows

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy measured, or explicitly deferred with the reason on its register row | pass | `PR-46` closed as stated, and one of its two sentences was worse than the row said. `PR-43`'s mechanism built as proposed; **its sizing refused by the sweep it asked for** — eleven conjunctions against a predicted two. The two named rows are written and the other nine are recorded, counted and printed, with `T-278` carrying them. Both the refusal and the deferral are on the register row |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Both cells already named `T-244`; both `Status` cells now carry what was measured, including the figure that had moved from 15 to 24 before anyone read it |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Run separately, never concurrently. Outcomes in the log row below |

**Child fix tasks raised**
- [T-278](T-278-write-the-clause-rows-the-sweep-found-owing.md) — the nine conjunctions the sweep
  found owing clause rows

**Nothing rendered, so no look is owed.** Every change is to the gate's account of itself and to
two register rows; no deck, theme or shell file is touched, and `check.py`'s own verdicts on the
five decks are unchanged — the clause block gained lines, and no rule's pass or fail moved.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | `PR-46` and `PR-43` both closed, and **each turned out worse than its row stated**. DS-145's excusal was wrong twice *and* contradicted its own closing condition, which the register had not caught. `PR-43`'s remedy hid a prose parser - *more than one testable assertion* is a judgement about English - so the half that was built is the half that is decidable: **`SWEPT` records a digest of the exact row somebody read**, per `hard` rule, and an arriving or edited rule re-opens the question. Watched failing in both directions. **Then the sweep ran and refused the remedy's sizing**: the register's 15 unswept rules had already become **24**, and reading them found **eleven** conjunctions rather than two. The two named rows are written; the other nine are `CONJUNCTIONS_OWED`, printed on every run and carried by `T-278`, because `SWEPT` alone would have read as *found it states one thing* and laundered them. Both gates green, run separately. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
