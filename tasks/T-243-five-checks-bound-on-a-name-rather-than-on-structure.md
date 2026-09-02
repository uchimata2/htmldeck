---
id: T-243
title: Re-bind five checks on what is true at run time instead of on a name
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
shipped_in: unreleased
deliverables: []
---

# T-243 — Re-bind five checks on what is true at run time instead of on a name

## 1. Specify

**Outcome**
Five checks decide a property rather than recognise a spelling - the shape [T-214](T-214-ds-142s-checker-is-an-allow-list-of-one-class-name.md) and [T-202](T-202-amend-ds-122-into-a-threshold-and-bind-its-check-on-structure.md) each fixed once. Today DS-239's ranking finds its subject by class name; the figure ledger recognises one deck's vocabulary so `FIG-1`'s denominator is what the pattern admits; DS-032's check names one licence where the rule names a class; `theme.py`'s self-test builds its negative fixtures out of the **tracked theme's current text**, so a legitimate edit breaks the test; and two variant suites accept an anchor matching more than once.

**Closes** `PR-44`, `PR-45`, `PR-49`, `PR-54`, `PR-57` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `density.py`'s class lists, `content.py`'s `UNITS`, `audit.py`'s `STATIC` entry for DS-032, `theme.py`'s `self_test` fixtures, and the two variant suites' anchors
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- In: **from the ClaimAI adopter report, [`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md)** — `DS-229` keys the contract's motion rows to **exact selector text**, so `:where(.slide[data-played]) .pulse` no longer has a row the contract can find — the tokens are declared, the motion works, and the gate reports the row unsatisfied. Scoping a motion to a state is the ordinary way to say *this plays on arrival*, and the rule makes the natural construction fail and the awkward one pass
- In: **from the ClaimAI adopter report, [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md)** — `DS-239` re-derives `--m-rank` **from the deck**, so ranks are properties of the set rather than of a motion: removing two of five content motions left the other three wrong with nothing in the edit touching them. `PR-44` already names this rule. The record's added half is that **the gate should print the value it derives, per motion** — it knows it, and printing it turns a bisection into an edit
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-44`, `PR-45`, `PR-49`, `PR-54`, `PR-57`
- **L-125** - before amending a rule, read what its gate actually tests
- the memory entry *a self-test must not assert repo state*, which `PR-54` is an instance of
- [`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md), [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md) — the adopter records merged into this task by [T-225](T-225-triage-the-claimai-adopter-report.md), because this task already owns the class. Each carries its own evidence and version.

**Acceptance criteria**
- [ ] every finding above is **closed with its remedy measured**, or explicitly deferred with the reason recorded on its register row - the method's obligation for `Med`
- [ ] each register row's `Task` cell names this task and its `Status` cell says what happened
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

**Every remedy below was measured before it was written down** (the method's section 5). What each
measurement said is recorded in the step that used it, and two of them changed the remedy the
register proposed.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **`PR-49`** - read DS-032's licence class rather than one licence's notice string. `audit.REDISTRIBUTABLE` is SPDX identifiers and the three shipped faces carry a *notice* (`SIL Open Font License 1.1`), so the row cannot simply read the list: the two forms are different alphabets for the same class | `audit.py`'s `STATIC` entry for DS-032, and one table pairing each redistributable licence with the notice text that names it |
| 2 | **`PR-54`** - build the negative fixtures instead of editing the tracked theme's current text. The assertion that the shipped theme conforms stays; the two `.replace` fixtures become a minimal `:root` nothing can move under | `theme.py`'s `self_test` |
| 3 | **`PR-57`** - tighten both suites to the siblings' exact-count form, then re-anchor the DS-143 variant on `:root[data-motion="off"] .current`, which is the path the seed already took and now says so | `content_variants.py` and `static_variants.py`, `build()` and `self_test()` |
| 4 | **`PR-44`** - derive the content-motion vocabulary from the deck's own `--motion-kind` declarations. Two things had to be fixed first, and both were found by measuring rather than by reading (below) | `density.py` |
| 5 | **`PR-45`** - derive the unit vocabulary from the pair being compared, so a figure is a numeral followed by a word the sources also use beside a numeral | `content.py`'s `UNITS` and `FIGURE` |
| 6 | **Adopter [`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md)** - match a contract motion row on the compound selector, exact match first and a scoped match reported when it is what satisfied the row | `component.py`'s `motion_gaps` |
| 7 | **Adopter [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md)** - print the derived rank per motion, which the gate already knows | `density.py`'s `report` |

**What the measurements said, and what they changed.**

- **`motion_rules` was reporting comment text as its selector.** `CSS_RULE` runs over the CSS with
  its comments intact, so a rule preceded by a block comment gets the comment as the head of its
  selector: **7 of the reference deck's 14 motion rules**, including two of the three content ones.
  Nothing had failed, because DS-237 and DS-238 only ask whether a *kind* is declared - but a
  vocabulary derived from those selectors would have been derived from prose. Stripping CSS
  comments is a precondition of step 4 rather than a separate finding, and DS-237's diagnostic
  stops printing 44 characters of comment.
- **The mapping is decidable, under a reading that has to be stated.** The three content rules are
  `.pulse`, `.arrow-pop marker path` and `.dot-pop circle`: the animation runs on the *inner*
  element and the ranked element is the figure that contains it. So the ranked class is the
  selector's **leading** class, not its subject - which is what the three-name table already
  encoded without saying so.
- **`AFFORDANCE_CLASSES` is dead.** It is defined and read by nothing in the tree. Half of `PR-44`'s
  stated subject is therefore a deletion rather than a re-binding.
- **The tier table survives as an ordering and stops being the denominator.** A derived class with
  no tier row ranks after every named one, so a motion conforming to the vocabulary
  [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md) opened is ranked rather than
  ignored - which is the failure `PR-44` predicts.
- **The exact-match half of `020` is kept.** Matching every contract row on the compound alone would
  let `.rise` be satisfied by `.slide[data-played] .rise`, which is a different rule with different
  tokens. Exact first, scoped second, and the row says when the second is what answered.

## 3. Implement

**All seven items landed. Each register row's statement stays in the register** - what follows is
what happened, not what was found.

| Item | File | What changed |
| :--- | :--- | :--- |
| `PR-49` | `audit.py` | `ds032_faces`, `face_window`, `LICENCE_NOTICES`; the `STATIC` row calls it |
| `PR-54` | `theme.py` | `set_token`, and the two negative fixtures built through it |
| `PR-57` | `content_variants.py`, `static_variants.py` | exact-count `build()` and `self_test()`; the DS-143 anchor |
| `PR-44` | `density.py` | `content_classes`, `ranked_classes`, `switched_off`, `CSS_COMMENT`; `AFFORDANCE_CLASSES` deleted |
| `PR-45` | `content.py` | `SHAPE_UNITS`/`FALLBACK_UNITS`, `units_from`, `figure_pattern`; `build_ledger` derives |
| `020` | `component.py` | `selector_covers`, `compounds`, `scoped_rows`; `rules()` strips comments |
| `021` | `density.py` | `check` prints the derived rank per motion |

**Three remedies were changed by their own measurement**, which is the method's section 5 doing its
work rather than an exception to it.

- **`PR-49`'s stated remedy was refused.** *The fix is a move rather than an edit* - have the row
  read `audit.REDISTRIBUTABLE`. That list is SPDX identifiers; the three shipped faces carry the
  notice `SIL Open Font License 1.1`, which matches none of its nine strings. A move would have
  failed every deck in the tree. Both alphabets are read instead, which also answers the row's own
  open question - *identifier or notice* is **either**, because *the licence travels with the font*
  is a claim about the deck naming its licence and both forms name it.
- **`PR-49` then failed a second measurement, of my own remedy.** Searching the whole deck for a
  redistributable licence passed `reference-deck.html` on the word `MIT` - the Lucide icons'
  licence, four hundred lines from any font. Right verdict, wrong evidence, and it would have gone
  on being right after the fonts changed. Each face is now read in the window of comments attached
  to it, bounded by walking back over whitespace and whole comments and stopping at anything else -
  no character count to justify, and nothing to re-tune when a face gains a line.
- **`PR-45`'s remedy widened the denominator and cost three rounds of measurement to do it.**
  Deriving the units from the sources produced, in turn: `30 cut-off` out of `02:30 cut-off`, a
  numeral preceded by a colon; `380 against` out of a source writing `18, against 22`, the deriver
  swallowing a trailing comma; and `5 cannot` out of `Phase 2 cannot start early`, which the
  release gate caught and the four deck runs had not. The first two are fixed in the pattern. The
  third is a **list**, and the reason it is allowed to be one is the argument of the row read
  precisely: unit nouns are an **open** class, which is why a table of them is always one deck's
  domain and the derivation exists; English function words are a **closed** class, finite and the
  same for every deck. `STOP` was already exactly that list, and `FUNCTION_WORDS` extends it to the
  words that can stand after a numeral. The module's own comment already states this principle for
  the numeral's other side - *`Route 3` and `Phase 1` name a thing rather than measure one* - and
  this is that principle one word to the right.

**Two defects were found in code this task had to read, and both are fixed here**, because a
re-binding that reads a lying function inherits the lie.

- **`motion_rules` was reporting comment text as its selector.** `CSS_RULE` runs over the CSS with
  comments intact, so the text between one rule's `}` and the next rule's `{` includes any comment
  written there: **7 of the reference deck's 14 motion rules**, two of the three content ones among
  them. DS-237's diagnostic was printing 44 characters of comment where it means to name a
  selector. `component.py`'s `rules()` had the identical defect and is fixed in the same change.
- **`switched_off` read `.rstrip("!important")`, which takes a character SET and not a suffix.**
  `"pop"` is three characters all drawn from those nine letters, so it stripped to the empty
  string, `"" in ("none", "")` was true, and a rule reading `animation:pop 1s` was classified as
  one switching motion **off** - dropped from the motion set entirely, taking its `--motion-kind`
  declaration with it. Nothing in the tree animates a name that spells out of `!important` today,
  which is why it had never fired. Found by a self-test fixture written for the comment defect.

**`AFFORDANCE_CLASSES` was dead** - defined at `density.py:62` and read by nothing in the tree - so
half of `PR-44`'s stated subject was a deletion rather than a re-binding.

**What the shipped decks do is unchanged, and that is the intended result.** A re-binding replaces
the reason a check reaches its verdict, not the verdict. The behaviour that moves is on decks the
old bindings could not see, and each of those is proved by a fixture rather than asserted:

| Measurement | Before | After |
| :--- | :--- | :--- |
| `density.py check examples/reference-deck.html` | 2 content motions, 0 wrong | 2 content motions, 0 wrong |
| `component.py check examples/reference-deck.html` | 17 rules, 0 gaps | 17 rules, 0 gaps, 0 scoped |
| the same deck with its `.pulse` motion rule scoped | 3 token gaps | 0 gaps, 1 row named as scoped |
| `content.py` on `examples/sort-window/` | `FIG-1` 0 of 73 | `FIG-1` 0 of 86 |
| `content.py` on `examples/reference-deck.html` | `FIG-1` 0 of 82 | `FIG-1` 0 of 87 |
| `content.py` on `examples/measure-first/` | `FIG-1` 0 of 34 | `FIG-1` 0 of 35 |
| `content.py` on `examples/portfolio-review/` | `FIG-1` 0 of 93 | `FIG-1` 0 of 96 |
| `theme.py` fixture, `--lh-body` legally moved to 1.60 | caught nothing | catches it, names DS-034 |
| `static_variants.py --self-test` | 29/29 10/10 1/1 2/2 7/7 1/1 | 29/29 10/10 1/1 2/2 7/7 1/1 |

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every finding closed with its remedy **measured**, or deferred with the reason recorded on its register row | met | All five closed. Three had their remedy changed by the measurement, and each row records which |
| each register row's `Task` cell names this task and its `Status` cell says what happened | met | `PR-44`, `PR-45`, `PR-49`, `PR-54`, `PR-57` each read `closed 2026-08-29` |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | Run separately on a frozen tree; the Log row carries the result |

**The two adopter records are closed in their own files** -
[`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md) and
[`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md) -
each recording what was implemented, and for `020` the thing the report could not see, which is why
a first attempt at it failed: a deck keeps several rules on one class, so `.pulse` matched exactly,
read none of the motion tokens, and a fallback guarded on *no exact match* never ran.

**Child fix tasks raised**
- none. The two defects found in passing are fixed in this task rather than deferred: both are in
  functions this task re-binds, and a re-binding that reads a lying function inherits the lie.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
| 2026-08-29 | → done | Batch B4. Five register rows and two adopter records closed across six files. Three remedies were changed by their own measurement and two further defects were found in code the task had to read - a CSS comment reaching a selector, and an `rstrip` taking a character set rather than a suffix. `AFFORDANCE_CLASSES` was dead and is deleted. The shipped decks are unchanged; what moves is proved by fixtures. Both gates green on the frozen tree, run separately: `lint.py` all four checks passed, `check_all.py` 0 failures, 0 unclassified, 0 stale in 261 s. **`check_all.py` caught the third `PR-45` boundary defect that four deck runs had missed**, which is the gate earning its place in the checklist rather than confirming it. |
