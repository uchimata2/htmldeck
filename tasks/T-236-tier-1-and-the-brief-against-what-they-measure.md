---
id: T-236
title: Correct tier 1's three figures and settle the tier-2 set the owner already ruled on
type: decision
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
updated: 2026-09-01
deliverables: [CLAUDE.md, docs/BRIEF.md, docs/EVALUATION.md]
shipped_in: unreleased
---

# T-236 — Correct tier 1's three figures and settle the tier-2 set the owner already ruled on

## 1. Specify

**Outcome**
[`CLAUDE.md`](../CLAUDE.md) and [`BRIEF.md`](../docs/BRIEF.md) state figures that are re-derivable and currently wrong: the shipped decks' size by one deck and 640,565 bytes, the ruleset counts stale inside the paragraph that says to re-derive them, and rule 1's two figures which the specification records as measured false. **The tier-2 set is the decision half** - the owner ruled on 2026-08-23 that a tier-2 document is entered at the start of work of a kind, which makes `AUDIT-METHOD.md` a term and tier 1's debt 9,810 rather than the 2,248 the file states.

**Closes** `PR-11`, `PR-12`, `PR-14`, `PR-112` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `CLAUDE.md`'s tier section, rules 1 and 6, and `BRIEF.md`'s three-documents table
- In: **nothing else** - every finding this task closes is named above, and each statement stays in the register rather than being restated here (the method's umbrella condition 2)
- Out: any finding not in the list above
- Out: committing to a remedy before measuring it. A remedy is a hypothesis (the method's section 5); a fix that the measurement refuses is reported here and its finding stays open

**Inputs**
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3 - the rows for `PR-11`, `PR-12`, `PR-14`, `PR-112`
- `PR-14`'s status cell, which carries the owner's ruling and the corrected figures
- [T-143](T-143-split-the-release-chronology-out-of-claude-md.md) and [T-144](T-144-give-each-cumulative-rule-one-operative-home.md) - the two cuts this bound was written to make decidable, both spent

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
| 1 | `PR-14` — apply the ruling: state the tier-2 set as the test, enumerate what meets it today, add the sixth term to the fence, and decide what the test excludes | `CLAUDE.md`'s tier section |
| 2 | `PR-11`, `PR-112` — replace the deck total and the corpus figures with what the rows propose, a bound and a pointer | Rules 6 and 1 |
| 3 | `PR-12` — delete the ten ruleset figures and point at `ruleset.py --counts`, in the brief's row and in the evaluation note the row names | `BRIEF.md`, `EVALUATION.md` |
| 4 | Re-measure both terms with the digits in place — the figure is inside the file it measures — and write the pair in the same edit | The debt paragraph |
| 5 | `figures.py`, then `lint.py`, then `check_all.py`, run separately | Green |

## 3. Implement

**Decisions & assumptions**

- **`PR-14`, the decision half: the test replaces the list, and the six documents are its
  enumeration.** The owner's definition — a tier-2 document is entered *at the start of work of a
  kind* — is now the sentence the bound is stated in, and `docs/AUDIT-METHOD.md` joins the five
  because `TASK-WORKFLOW.md` §8 loads it when an audit is asked for, which is work of a kind. What the
  test excludes is named so the next reader does not re-derive it: `RELEASE-PHASES.md` and
  `RELEASE-HISTORY.md` answer a question during work; `REMEDIATION-ORDER.md` is a schedule for one
  programme, opened to answer *what next* and expiring at B24. **One question the ruling leaves was
  decided here rather than handed back**: the skill's reference documents load when deck work starts,
  but they are the plugin's tier 2 for an adopter and not documents split out of this file, which is
  what the bound compares against — and nothing rides on it today, since the smallest of them is
  7,005 bytes against the audit method's 6,438. 2026-09-01.
- **The pair is measured with the figure in place, to a fixed point.** The size `CLAUDE.md` states is
  the size of the file with that figure written in it, so the patch holds the figure's width constant
  and re-measures until the file agrees with itself: **15,581 bytes against 6,438, debt 9,143**. The
  register's `PR-14` row said 5,762 and 9,810 at cycle 39; the audit method grew 676 bytes since, and
  this task cut 16 from the file it measures. `figures.py`'s `MEASURED` grant holds both terms to the
  fence, so this third correction of the pair is the first a gate reads.
- **The debt paragraph was cut to what a reader needs.** The two spent cuts, the rule to re-measure
  both terms, and now the instrument that does. The play-by-play of the floor's earlier moves went;
  the register row and the task records keep it. Two unbound section references went with it, which
  is why the README's refcheck floor fell by two and was re-pasted from the command.
- **`PR-11`: a bound in place of a total, as the row proposed.** *Every shipped deck is over 300 KB*,
  with the command that prints each size named beside it. The smallest deck is 323,085 bytes, so the
  bound holds by 15 KB; it is a claim about magnitude, not a measurement, and a deck rebuilt below it
  is a change to the sentence rather than a stale figure. Nothing watches it, but nothing watched
  the total either, and the total moved on every rebuild.
- **`PR-12`: the ten figures are deleted and the row points at the command.** Measured first:
  `ruleset.py --counts` prints 177 rows and 178 declared, `auto` 75, `render` 47, `judge` 48, `—` 7,
  `yes` 119, `off-gate` 3, `never` 0, `—` 55 — seven of the row's ten were wrong, which is the row's
  own count. The brief's row keeps what the fields are and what the command prints, including why
  the two totals differ by DS-000 and why `Reach —` is not every `judge` rule, with no count in it.
  **The scope line of this task was narrower than the row**: it named the brief's table, and the row
  names `EVALUATION.md`'s note as well, recorded there so cycle 8 would not raise it twice. The note
  was treated the same way — its pasted set became the dated record of the last set that went stale —
  and the figures outside that note are `PR-32`'s, which stays with `T-240`.
- **`PR-112`: the corpus figure is deleted and rule 1 points at R1**, citing **L-96** for why no
  figure from a survey lives in the file paid for every turn. *Every deck failed* and *2–7* were not
  corrected to *nine of twelve* and *0–21*, which would have been a second copy of R1's numbers.
- **Hypotheses taken: four of four.** Every row's proposal survived measurement here; what this task
  refused was the register's own figures for `PR-14`, which had moved under it.

**Outputs produced**

- [`CLAUDE.md`](../CLAUDE.md) — the tier section and its fence, the debt paragraph, rules 1 and 6
- [`docs/BRIEF.md`](../docs/BRIEF.md) — the ruleset row of the three-documents table
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — the two paragraphs of the counts note
- [`README.md`](../README.md) — the refcheck floor
- [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) — the four rows

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every finding closed with its remedy measured, or deferred with the reason recorded | pass | Four rows closed on their own hypotheses, each measured first: the ruleset counts against `--counts`, the deck sizes against the manifest, the pair against the fence to a fixed point |
| Each register row's `Task` cell names this task and its `Status` cell says what happened | pass | Four rows updated |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Lint's four checks pass; `figures.py` 0 stale with both measured terms compared |

**No look is owed.** This task changed four documents and no deck.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-01 | → done | Four findings closed, every remedy as the row proposed. The owner's 2026-08-23 ruling is applied: the tier-2 set is the test — entered at the start of work of a kind — and `AUDIT-METHOD.md` is its sixth term, so the bound now reads **15,581 against 6,438, debt 9,143**, measured with the figure inside the file it measures and held to the fence by `figures.py`. Tier 1's deck total is a bound, its corpus figures are a pointer to R1, and the brief's ten ruleset counts left the row with the evaluation note's pasted set, each pointing at `ruleset.py --counts`. |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`Med`**, grouped: the owner ruled on 2026-08-29 that a severity obliges a disposition before the release rather than a file count, on the precedent that the method already accepts many findings to one task at `Low`. Every finding keeps its id and its statement in the register. |
