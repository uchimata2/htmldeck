---
id: T-234
title: Correct the front page's figures and its two false claims
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-09-01
deliverables: [README.md, tools/docs/figures.py, docs/lessons/L-152.md]
shipped_in: unreleased
---

# T-234 — Correct the front page's figures and its two false claims

## 1. Specify

**Outcome**
[`README.md`](../README.md) states what the tree holds. Today its second paragraph says *two decks*, its own table implies three and four ship; line 206 states a size that is wrong by 2 KB in the one place the figure watcher does not look; and the section written so nobody has to infer this project's state says the sample is one project when a second has reported.

**Closes** `PR-03`, `PR-04`, `PR-124` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `README.md`, and the artifact manifest in `tools/docs/figures.py` that decides which of its figures are watched
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-03`, `PR-04`, `PR-124`
- `DECLARED_DOCS` in [`tools/docs/figures.py`](../tools/docs/figures.py)

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `PR-04` — seed the page before touching it: a wrong value, then another deck's value, and read what the run says of each | The mechanism, measured |
| 2 | `PR-04` — run the link binding over the README, take its numerals out of the word-bound path, derive a fixture from the page in both directions | `figures.py` |
| 3 | `PR-03` — decide *bound or deleted* from B16's measurement and apply it to the deck count | `README.md`, and the rule as a lesson |
| 4 | `PR-124` — read `T-225`'s outcome, then write the second project as a record beside the first, with no total | `README.md` |
| 5 | `figures.py`, then `lint.py`, then `check_all.py`, run separately | Green |

## 3. Implement

**Decisions & assumptions**

- **The rule B16 asked this task to decide: a count is bound or deleted, never refreshed.** `T-227`
  corrected the front page's fixture count and `T-235` made it wrong again three commits later, so a
  refreshed total is measured to buy a few commits. A count now has two honest states — a command
  prints it and a check compares it, or it is deleted and the sentence points at the count's home —
  and the test is whether adding one more of the thing would falsify the sentence with nothing
  reading it. Applied here three ways: `PR-03` deleted, `PR-04` bound, `PR-124` rewritten as a
  per-item record. Recorded as [L-152](../docs/lessons/L-152.md). 2026-09-01.
- **`PR-04`: the value was already right, and the binding was a coincidence.** B12's rebuild had
  corrected the page to 316 KB against a file of 323,129 bytes, so the durable half was the whole
  task — and it was measured before it was fixed. Seeded to 307, `figures.py` went red, so the row's
  *bound to nothing* overstated it; the message named `portfolio-review` as the nearest field.
  Seeded to **317, the reference deck's size, the run exited 0** and reported the figure `compared`
  against `examples/reference-deck.html`. The mechanism is `bound()`: a numeral is held to a printed
  label by shared words, every deck's label shares the word `examples`, and so the built deck's size
  was held to whichever deck happened to be that size.
- **The fix is the binding that already existed one scope out.** `artifact_claims` — a block must
  link exactly one manifest artifact, and a numeral followed by a unit is a claim about that file —
  ran over the five declared documents and not over the README. It now runs over the README's blocks
  first, and a numeral it judged is taken out of the word-bound path, which is the `spoken` rule
  `declared()` already applies. `audit()` returns the README's watched counts and the report folds
  them into the table that used to say *no declared document binds a claim*: the built deck's KB is
  now watched twice and its slide count three times where the register measured one.
- **Proved both ways, by a fixture derived from the page rather than quoted from it.** The self-test
  finds the README block linking the built deck, moves its size to the reference deck's, and requires
  a `STALE` row naming the built deck — then requires the live page to bind the same figure to the
  built deck's file, or the fixture proved a message and not a binding. A live drift now stops the
  self-test naming the file and both sizes, which is the convention the tool's first check already
  follows for a failing fence.
- **One README sentence gave way to the instrument.** *Authored three slides at a time* sits in the
  block that links the built deck and would have been read as a slide count of three. It now reads
  *in batches of three*, which says the same thing with no unit after the numeral.
- **`PR-03`: the row's hypothesis is refused by the tree.** *Two* cannot have meant *built in this
  repository* — three were, and the fourth was built elsewhere — so no reading of the sentence was
  true and recounting it would have been a fourth. The sentence now says *the decks under
  `examples/`, each built to them and gated on every run*, and the page that lists them is held to
  `check_all.py`'s `DECKS` by the gate since `PR-02` closed.
- **`PR-124`: the question the row left open is answered by the tree.** It asked whoever took it to
  decide first whether the second report belongs on the front page while untriaged; `T-225` closed
  on 2026-08-29 with every record accepted, eighteen tasks raised and three merged, so the page can
  name it as judged. The bullet is now a record per project with no total — a third adopter adds a
  sentence and falsifies nothing — and the dependent bullet, *that project's deck is now the third
  example here*, names the first project and drops the ordinal (**L-133**).
- **The refcheck floor moved by two** for the two links the second project's sentence added, and was
  pasted from `--values` before the gate ran.

**Outputs produced**

- [`tools/docs/figures.py`](../tools/docs/figures.py) — the link binding over the README, the
  watched counts it adds to the report, and fixture 0
- [`README.md`](../README.md) — the opening paragraph, the built deck's paragraph, the two adopter
  bullets, and the refcheck floor
- [`docs/lessons/L-152.md`](../docs/lessons/L-152.md) and the index in
  [`docs/LESSONS.md`](../docs/LESSONS.md)
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the three rows

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy measured, or deferred with the reason recorded | pass | `PR-03` closed with the row's hypothesis refused and the count deleted; `PR-04` closed with the coincidence measured by two seeds and the binding proved both ways; `PR-124` closed as the row proposed, its open question answered by `T-225`'s closure |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Three rows updated |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Lint's four checks pass. `figures.py` 0 stale with the README's deck figures bound by link; `refcheck.py` 4,994 pointers 0 broken |

**No look is owed.** This task changed two documents, one checker and a lesson, and no deck.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-01 | → done | Three findings closed, and the rule B16 left to this task decided: **a count is bound or deleted, never refreshed** ([L-152](../docs/lessons/L-152.md)). `PR-04`'s value was already right after B12's rebuild and its binding was a coincidence — seeded to the reference deck's size the run exited 0 and named the wrong file — so the link binding the declared documents already had now runs over the README first, with a fixture derived from the page proving both directions. `PR-03`'s hypothesis is refused by the tree and the count is deleted; `PR-124` is a record per project with no total, its open question answered by `T-225`'s closure. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
