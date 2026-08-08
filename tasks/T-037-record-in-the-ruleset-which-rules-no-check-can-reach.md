---
id: T-037
title: Record in the ruleset itself which rules no check can reach
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-005, T-014, T-021, T-022, T-033]
work_package: WP2
owner: maintainer
created: 2026-08-08
updated: 2026-08-08
deliverables: []
---

# T-037 — Record in the ruleset itself which rules no check can reach

## 1. Specify

**Outcome**
[`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) states, **per rule**, whether a check can reach it —
so that "which rules is the gate supposed to cover?" is answered by reading the ruleset rather than
by reading a tool's print statements. A rule that is labelled `auto` or `render` and that no check
can reach is currently indistinguishable from one nobody has got round to, and the distinction is
the whole basis of a coverage account.

**Why this one**
[T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s coverage criterion requires the account
of all 109 owned rules to be **derived from the ruleset when the gate runs**, never kept by hand
(**L-08**). That derivation is not possible today: the ruleset says `auto` or `render` and stops,
and the exceptions live in `audit.py`'s output as prose.

**The anchor that went stale, and how it survived**

This carve-out used to have a home. [T-014](T-014-synthesise-research-into-the-design-system-reference.md)
built `DESIGN-SYSTEM.md` **§11** — the hard rules restated as 26 numbered testable conditions, later
33 — precisely so T-005 could consume them without reading the whole reference, and it named the two
that **no check could reach** rather than dropping them to make the list look clean.

[T-022](T-022-split-the-design-system-from-its-rationale.md) then gave every rule a `DS-nnn` ID, and
§11 went with the renumbering. **The document now ends at §9.** What was lost was not the rules —
they all have IDs — but the *statement of which ones are unreachable*, which existed nowhere else.
Three consequences, all live:

- T-005's log cites "conditions 22 and 30 are not machine-checkable". **Those numbers resolve to
  nothing**, and which two rules they meant is not recoverable from the ruleset.
- [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) hit the same staleness and worked
  around it by hand, writing *"the rule the original text called condition 17"* → **DS-063** into its
  own criteria. That translation is correct and it is also the only one anybody did.
- `python tools/tasks/task.py check` **cannot see any of this.** It validates markdown links and
  repo-relative paths; a `§11` written in prose is neither. This is the gap that let a dead anchor
  sit in three task files across two months.

**Scope**
- In: a per-rule way to say *no check can reach this, and here is why* — a `Check` value, an extra
  column, or a footnote convention. Which one is the decision this task takes.
- In: applying it to the rules that are genuinely unreachable, starting with the four `audit.py`
  already excuses in print: **DS-033, DS-061, DS-065, DS-072**, whose reasons are already written
  and merely live in the wrong place.
- In: recovering, or explicitly writing off, the two rules §11 called 22 and 30.
- Out: **building or changing the gate.** T-005 consumes this; it does not depend on this task to
  be planned, and nothing here writes Python.
- Out: re-auditing the 64 silent rules to decide which are unreachable. Most are simply unbuilt, and
  T-005's triage is where that judgement belongs. This task provides the vocabulary, not the verdicts.
- Out: the 43 `judge` rules. Unreachable by a check is their normal condition, not an exception —
  they are [`EVALUATION.md`](../docs/EVALUATION.md)'s.

**Inputs**
- [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — 159 rule rows, `Check` values `auto` 65,
  `render` 44, `judge` 43.
- `tools/deck/audit.py` — its *"Not gated here, and why"* tail is the existing content, already
  written and already correct; this task decides where it belongs.
- [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) §1 — the consumer, and the reason the
  vocabulary has to be machine-readable rather than prose.
- [T-014](T-014-synthesise-research-into-the-design-system-reference.md) §4 and
  [T-022](T-022-split-the-design-system-from-its-rationale.md) — what §11 was for, and why it went.

**Acceptance criteria**
- [ ] Every rule row carries an unambiguous, machine-readable answer to *can a check reach this?* —
      readable by a program that has never heard of any individual rule
- [ ] A rule marked unreachable carries **its reason, in the ruleset**, not a cross-reference to a
      tool's output
- [ ] The four reasons currently printed by `audit.py` (DS-033, DS-061, DS-065, DS-072) are in the
      ruleset, and `audit.py` no longer holds the only copy of any of them
- [ ] §11's "conditions 22 and 30" are either identified as `DS-nnn` rules or **explicitly written
      off as unrecoverable**, in writing. Quietly dropping them is the failure this task exists to
      correct, so repeating it closes nothing
- [ ] A program can compute *"rules the gate is expected to cover"* from the ruleset alone, and the
      number it gets is stated here so T-005 can assert against it
- [ ] `DESIGN-RATIONALE.md` records why the distinction is carried per rule rather than in a list —
      the reason §11 could go stale is that it was a second, parallel structure
- [ ] No rule's `hard` / `default` / `guidance` label changes as a side effect. This task changes
      what is *knowable* about a rule, never how binding it is

**Open questions**
- **Which mechanism — a fourth `Check` value, a new column, or a marked reason in the rule text? —
  owner.** A fourth value (say `manual`) is the smallest change and keeps one column authoritative,
  but it loses the distinction between *unreachable in principle* and *unreachable by this gate*.
  A new column carries both and widens 159 rows. Decide in `plan`, not here.
- **Is a stale `§n` reference worth teaching `check` to catch? — owner.** Two months and three task
  files is the observed cost of not catching it. Out of scope here either way; raise separately if
  wanted, since it is tooling and this task is a ruleset decision.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-08 | → proposed | **Raised from [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s `specify`, and deliberately not fixed there** — a finding is not repaired where it is found. Working T-005's scope showed that the gate owns **109 rules** (65 `auto`, 44 `render`) of which **64 are silent**, and that its coverage account has to be *derived* from the ruleset rather than kept by hand (**L-08**). That derivation is impossible while the ruleset says only `auto` or `render`: an unreachable rule and an unbuilt one look identical. The reasons exist and are good — they are just in `audit.py`'s print statements. **The owner chose, 2026-08-08, that they belong per rule in the ruleset**, on [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent that a rule a shipped artifact contradicts is a defect in the ruleset rather than in the artifact. The task is `related` to T-005, not blocking it: T-005's §1 already assumes this field exists, so landing this later leaves that spec incomplete rather than wrong — [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md)'s test for whether an edge gates. |
