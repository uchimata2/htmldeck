---
id: T-253
title: Correct the audit's forty-nine Low findings, or accept each with a reason and a date
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: low
effort: l
created: 2026-08-29
updated: 2026-09-02
shipped_in: unreleased
deliverables:
  - docs/PRE-RELEASE-AUDIT.md
  - tools/docs/severity.py
---

# T-253 — Correct the audit's forty-nine Low findings, or accept each with a reason and a date

## 1. Specify

**Outcome**
Every `Low` finding in the register is corrected, or carries an accepted row with a reason and a date. **Batching is the method's own rule for this level** and not a convenience: forty-nine task records for forty-nine one-line corrections is a cost the tracker pays and nobody recovers, and batching keeps every finding in the record while stopping the tracker from becoming the audit's byproduct.

**Closes** the whole `Low` band in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the whole band, worked in register order, each finding either fixed or moved to the register's section 4 with a reason and a date
- In: **stating how many were accepted rather than fixed**, because a batch that accepts most of its band is evidence the severity threshold was set too low - which the method says is the thing to fix, not the batch
- Out: any `High` or `Med` finding - each of those has its own task
- Out: re-ranking. A finding that turns out worse than `Low` is said so on its row and raised as its own task; it is not quietly fixed at this level

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3, the `Low` rows
- the method's section 4, served by the installed taskmd plugin - *severity has to oblige something*
- section 4 of the register, *Accepted without action*, where an accepted row goes

**Acceptance criteria**
- [ ] every `Low` row is fixed, or has an accepted row carrying a reason and a date
- [ ] the fixed-to-accepted split is stated as two numbers
- [ ] no `Low` row is left `open` with neither disposition
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

**The band is 49 rows, and that is a query rather than a figure this record keeps**: the `Low` rows in [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 whose `Task` cell names this task and whose `Status` reads `open`. It is written here once because the plan's shape depends on it, and it is re-derived rather than trusted at step 1.

**Worked in register order inside each wave, and the waves are by home** - a document opened once is worked once. Every row is measured before it is touched: the register's `Remedy` column is a hypothesis and so is the finding's own account of the mechanism, which is `T-239`'s worked example one batch back.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-derive the band from the register and re-measure every row's claim against today's tree - a row already true, already fixed, or wrong about its subject is said so and not "fixed" | a verdict per row, carried into section 3 |
| 2 | **Wave 1 - the method records**: `PR-05`, `PR-18` (PUBLISHING), `PR-22` (audit umbrella template), `PR-23` (TOOLING), `PR-28` (the register itself), `PR-69`, `PR-107`, `PR-110` (T-219), `PR-82` (AUDIT-METHOD), `PR-94`, `PR-95` (RULESET-AUDIT) | the eleven rows disposed |
| 3 | **Wave 2 - the product documents**: `PR-40`, `PR-41` (COMPONENT-CONTRACT), `PR-99`, `PR-100`, `PR-111` (DESIGN-RATIONALE and R1), `PR-113` (R2), `PR-116` (upstream/harness), `PR-117` (the adopter README), `PR-118` (the chrome-row sketch) | nine rows disposed |
| 4 | **Wave 3 - the lessons**: `PR-105`, `PR-106`, `PR-108`, `PR-109` | four rows disposed |
| 5 | **Wave 4 - the tools**: `PR-47`, `PR-51`, `PR-52`, `PR-60`, `PR-61`, `PR-62`, `PR-63`, `PR-64`, `PR-68`, `PR-73`, `PR-74`, `PR-75`, `PR-76`, `PR-93`, `PR-125` | fifteen rows disposed, self-tests still green |
| 6 | **Wave 5 - the shell and the examples**: `PR-79`, `PR-87`, `PR-88`, `PR-89` | four rows disposed; a deck-facing change here owes a rebuild and an owed look |
| 7 | **Wave 6 - the records and the ignored surface**: `PR-119`, `PR-121`, `PR-123`, `PR-126`, `PR-127`, `PR-128` | six rows disposed |
| 8 | Write each row's disposition into the register - the rank struck through for a fix, or a section 4 row with a reason and a date for an acceptance - and state the fixed-to-accepted split as two numbers | the register current |
| 9 | `python tools/tasks/lint.py`, then `python tools/check_all.py` - separately, never at once, and the full run because the batch is landing | two green runs |

**The one thing this batch may not do is look** ([`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) section 4). A row that changes what a deck renders records the look as owed in [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) and closes.

**And the trap this band is full of** - **L-161**: a derived figure written into a document that is inside its own subject cannot converge. Most of these rows are a typed number in the document that holds the rows it counts, so *restamp it* is the remedy that brings the finding back. Before writing any measured value, ask whether the document holding it is part of what it measures.

## 3. Implement

**48 fixed, 1 accepted.** The one acceptance is `PR-123`, and the split is the answer to the
question section 1 asks with it: **a band that accepts one row of forty-nine was not banded too
low**. The method's section 4 says a batch accepting most of its band is evidence the severity
threshold wants fixing rather than the batch; this one is the opposite reading.

**Every row was measured before it was touched, and eight came back differently from the row.**
That is the point of the rule rather than a tally - the register's `Remedy` column is a hypothesis
and so is the finding's own account of the mechanism (`T-239`, one batch back).

| Row | What the measurement said | What it changed |
| :--- | :--- | :--- |
| `PR-61` | **27** bare `assert` statements across the two files, not the 8 the row counted | all 27 rewritten, not eight |
| `PR-69` | cycle 14 holds **seven** files today, not the five the row measured four days earlier | the count was deleted rather than corrected to five - it was already wrong again |
| `PR-74` | the fixture failed on `chunks[0]`, and **the fixture was wrong**: `build_probes.py` emits `k % chunks.length`, so the index is zero-based against a one-based total | the off-by-one the code's own comment warns about was in the test, and the tool held |
| `PR-95`, `PR-108`, `PR-109`, `PR-125` | every quoted line number and every quoted figure had moved **again** since the row was written - DS-146 at 482 against the row's 471 and the document's 410 | four rows fixed by deleting the value and quoting the shape, not by restamping |
| `PR-110` | the cells were correct; the `Open` column was stale by **74** | the instrument found in its first run what the row predicted correcting the cells would not prevent |
| `PR-113` | the population is 28 and five headings carry a compound grade | the prior question - *one grade or a set?* - had to be answered before any tally could be right |
| `PR-123` | `control/` and `dist/` still appear in no commit; the two leftovers are the owner's local files | accepted, with the gate refused and the reason stated |
| `PR-79` | the shell comment is embedded verbatim in all five tracked decks | a comment-only fix cost five `shell.py sync --write` runs and a re-derived fixture |

**Decisions & assumptions**
- **A figure inside its own subject is deleted, never restamped** — the batch's default, and **L-161**
  is why. `PR-05`, `PR-18`, `PR-47`, `PR-52`, `PR-69`, `PR-87`, `PR-109` and `PR-125` all lost a
  number rather than gaining a corrected one, and each names what derives it instead — 2026-09-02.
- **`PR-107`'s backward half is decided, not deferred a second time.** The ledger is the record and
  the log is commentary on it, so cycles 13 to 17 get no reconstructed row. Cycle 40 left this open;
  a batch that leaves it open again is the third session to read the same gap — 2026-09-02.
- **`PR-110` is closed by building the command rather than by correcting the cells**, which is the
  one row in the band whose remedy is machinery. The judgement `PR-110` says a script cannot take —
  what a struck rank means — is taken once, in
  [`tools/docs/severity.py`](../tools/docs/severity.py)'s docstring, and stated rather than inferred
  — 2026-09-02.
- **`PR-79` is fixed by saying it, and the colour question is queued.** Choosing literals is an eye's
  judgement, which `REMEDIATION-ORDER.md` §4 forbids an unattended session; the block now states
  whose palette it is and why it is fixed, and [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row
  12 carries the rest — 2026-09-02.
- **`PR-88`'s OTIF half is answered by scoping the bar, not by editing the sources.** Editing a
  carried source stops it being what the deck was built from, which is the argument the adopter
  README already makes one directory over — 2026-09-02.
- **Two things this batch found were absorbed in place**, per `REMEDIATION-ORDER.md` §4. Three closed
  rows struck their **id** where §3 says the **rank** is struck, so no count over the table could
  read them — normalised, and `severity.py` now refuses a struck id rather than tolerating it. And
  `T-219`'s log read in two directions, nine rows prepended above a block running the other way —
  moved back into date order, same 37 rows — 2026-09-02.

**Outputs produced**
- [`../docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — 49 dispositions, §4's first
  accepted row, and §3's ordering claim replaced
- [`../tools/docs/severity.py`](../tools/docs/severity.py) — new, and in `check_all.py`'s wide list
- Tools: `check.py`, `check_all.py`, `contents_bound.py`, `critique.py`, `cycles.py`, `figures.py`,
  `fps.py`, `presenter.py`, `printgeom.py`, `quickview.py`, `ruleset.py`, `audit.py`,
  `portfolio_charts.py`, `run_probes.py`, `kb/extract.py`
- Documents: `AUDIT-METHOD.md`, `COMPONENT-CONTRACT.md`, `DESIGN-RATIONALE.md`, `LESSONS.md`,
  `OWED-LOOKS.md`, `PUBLISHING.md`, `RULESET-AUDIT.md`, `R1`, `R2`, `upstream/harness.md`, the
  adopter README, the chrome-row sketch, `.gitignore`, and 24 lesson files
- Records: `T-219`, `T-188`, `T-200`, `T-213`, `T-214`, `T-217`, `TASK-WORKFLOW.md`, `TOOLING.md`,
  `_audit-umbrella-template.md`
- Decks: `shell/components.css` and the five tracked decks re-synced; `measure-first`'s carried copy
  of `D1` refreshed
- Memory: `a-traceback-after-the-write-still-wrote`, `derive-a-path-never-reconstruct-it`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every `Low` row is fixed, or has an accepted row carrying a reason and a date | **met** | 48 closed on a change, 1 accepted with both. `python tools/docs/severity.py` derives `Low 49 raised · 49 tasked · 1 accepted · 0 open` from the rows themselves |
| The fixed-to-accepted split is stated as two numbers | **met** | **48 and 1**, in §3's first line, and the reading it obliges is stated with it |
| No `Low` row is left `open` with neither disposition | **met** | The same command fails if one is: `Open` is derived, not typed, and it reads 0 in every band |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | Run in that order, never concurrently (`TOOLING.md` §1.2), on the tree as committed |

**Child fix tasks raised**
- none. **Three rows leave a stated open question rather than a task**, on `PR-78`'s precedent:
  `PR-75` on whether a recompose of the portfolio deck should be caught by anything, `PR-89` on
  whether `SPEC-1` should learn a final-section boundary, and `PR-116` on whether the three upstream
  registers want the reader `severity.py` now is. Each is a rule question `REMEDIATION-ORDER.md` §4
  does not cover, and cycle 41 reads all three.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Low`**, batched, which is the method's own rule for the level rather than a convenience — its reason is that the tracker must not become the audit's byproduct. |
| 2026-09-02 | → planned | **B22 opened, the last batch of the remediation.** The band was re-derived rather than trusted - the register's `Low` rows naming this task and still `open` - and came back at 49, which is what the title says. Worked in six waves by home so a document is opened once. |
| 2026-09-02 | → done | **48 fixed, 1 accepted, and eight rows came back differently from what they said.** The most useful of those is `PR-110`: its remedy is an instrument, and building [`../tools/docs/severity.py`](../tools/docs/severity.py) found the `Open` column stale by 74 on its first run, where correcting the cells - which the row itself says buys one cycle - would have left the same table unwatched. `PR-74`'s fixture failed on its own off-by-one and the tool held. `PR-69` was already wrong again by two files four days after it was written, which is why the figure was deleted rather than corrected. **Two things were absorbed in place** per `REMEDIATION-ORDER.md` §4 - three rows striking their id instead of their rank, and `T-219`'s log reading in two directions. **One look is owed**: `PR-79` is fixed by stating whose palette the degraded state uses, and whether it should be neutral is row 12 of [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md). |
