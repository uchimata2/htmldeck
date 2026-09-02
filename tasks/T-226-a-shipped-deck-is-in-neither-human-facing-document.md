---
id: T-226
title: Give the portfolio-review deck a home in both human-facing documents
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-30
shipped_in: unreleased
deliverables: []
---

# T-226 — Give the portfolio-review deck a home in both human-facing documents

## 1. Specify

**Outcome**
`examples/portfolio-review/` is described where a reader is sent to find it. Today [`examples/README.md`](../examples/README.md) opens *Four decks* and lists three plus the seeded-defects fixture, and the front page sends a reader there for *every shipped deck*, which is a completeness claim the tree does not support and `0.6.0` shipped already false.

**Closes** `PR-02` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: the deck's section in `examples/README.md`, its artifact-manifest entry, and the front page's row
- In: **writing the section from the feature's end**, which is the register's hypothesis: the deck is `0.6.0`'s chart-engine example and the front page describes that feature without pointing at it
- Out: the other three decks' sections, which are correct
- Out: anything about the fixture's own row, which already says what it is

**Inputs**
- `PR-02` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) - what the deck was built to demonstrate

**Acceptance criteria**
- [ ] `examples/README.md` describes four decks and its count agrees with `check_all.py`'s `DECKS`, derived rather than typed
- [ ] the front page's *every shipped deck* row resolves to a page that has them all
- [ ] `python tools/check_all.py` green, and the figure watcher reports no new stale figure

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Make the count derivable before writing anything into it: a check in `check_all.py` asserting every deck in `DECKS` is linked from `examples/README.md` | the check, and its both-directions proof |
| 2 | Correct the opening count, add the deck's table row and write its section from the feature's end | `examples/README.md` |
| 3 | Add the deck to `figures.py`'s `ARTIFACTS` so the section's size, slide count and figure count are watched | `tools/docs/figures.py` |
| 4 | Correct the front page's *every shipped deck* row so its enumeration reaches four decks and the fixture | `README.md` |
| 5 | `python tools/tasks/lint.py` and `python tools/check_all.py`, run separately | two green runs |

## 3. Implement

**Decisions & assumptions**
- **The count is held to `DECKS` by a check, not by care** - 2026-08-30. The criterion asked for a
  count *derived rather than typed*, and none of `figures.py`'s three binders can produce *how many
  decks this repository ships*: `ARTIFACTS` watches properties of one named file, `ACCOUNTS` a
  part-of-whole from one command, `MEASURED` a fenced command in one named document. So the
  derivation went where the fact already lives. `decks_not_in_examples_readme()` in
  `tools/check_all.py` asserts **membership** rather than the numeral - a deck in `DECKS` that the
  page does not link fails the run. Binding the numeral instead would have tied the gate to one
  sentence's wording; binding membership ties it to the property a reader cares about, and it
  reaches the *next* deck as well as this one.
- **The opener counted the fixture as a deck.** *Four decks* was right about the table and wrong
  about the tree: the table listed three decks and `reference-deck-seeded-defects.html`, which the
  same table calls *a test fixture, not an example to copy*. It now reads *four decks and one test
  fixture*, which is what `DECKS` and `NOT_A_DECK` say.
- **The section is written from the feature's end**, which was the register's hypothesis and is
  correct: the deck's reason for existing is [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md)'s
  question, not its topic. The section leads with the question, prices the answer at the builder's
  1,351 lines for ten charts, and only then says what the deck is about.
- **The figure watcher caught this task's own sentence, and that is the entry earning its place.**
  The table row first read *ten of its figures are charts*; adding the deck to `ARTIFACTS` made
  `ten` bind to the `figures` property within three words and the run reported
  `STALE ... claims ten figures ... which is 18`. Reworded to *ten charts among its eighteen
  figures*, where `eighteen` binds and `ten` reaches no unit. **The manifest entry was written
  before the prose, so the first sentence written under it was the first sentence judged.**

**Outputs produced**
- `examples/README.md` - the opener, the table row, and the deck's own section
- `README.md` - the *What is actually here* row for `examples/`
- `tools/docs/figures.py` - the `ARTIFACTS` entry, watching size, slides and figures
- `tools/check_all.py` - `decks_not_in_examples_readme()`, and its call in `main`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `examples/README.md` describes four decks and its count agrees with `check_all.py`'s `DECKS`, derived rather than typed | pass | The page says four decks and one test fixture, and `decks_not_in_examples_readme()` holds it there. Proved in both directions: it returns `[]` on the tree, and returns exactly the seeded deck when `DECKS` is given a fifth entry the page does not link |
| the front page's *every shipped deck* row resolves to a page that has them all | pass | The row's enumeration is four decks and the fixture, and the page it links reaches all five |
| `python tools/check_all.py` green, and the figure watcher reports no new stale figure | pass | The watcher reported **one**, on a sentence this task wrote, and it was corrected before the gate - recorded in section 3. It exits 0 with `STALE 0` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
| 2026-08-30 | proposed → done | **B13.** The deck has a section, a table row, an artifact-manifest entry and a corrected front-page row. `PR-02`'s hypothesis held: the section is written from `T-113`'s question rather than from the deck's topic. **The count is now held to `DECKS` by a check** rather than by care — the remedy did not ask for that, and a section written today does not stop the next deck arriving unwritten. The opener had also been counting the **fixture** as one of its four decks. **The figure watcher caught this task's own first sentence**, which is the manifest entry earning its place on the run that added it. No look owed: nothing here changes what a reader sees in a deck. |
