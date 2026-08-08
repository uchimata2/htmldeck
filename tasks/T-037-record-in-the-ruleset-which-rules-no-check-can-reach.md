---
id: T-037
title: Record in the ruleset itself which rules no check can reach
type: decision
status: specified
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

**The anchor never existed — established 2026-08-08, from git, not from memory**

This carve-out was supposed to have a home.
[T-014](T-014-synthesise-research-into-the-design-system-reference.md) step 5 promised *"the
check-facing section of the reference"* — the hard rules pulled into one list stated as testable
conditions, so T-005 could consume them without re-reading the whole document — and T-014's §4
recorded it **met**: *"§11 — 26 numbered conditions. Two (15 and 23) are not machine-checkable and
say so, rather than being dropped to make the list look clean."*

**`docs/DESIGN-SYSTEM.md` has ended at §9 in every one of the 13 commits of its life.** It was
created that way, by the same commit that closed T-014. There is no §10 and no §11, in any revision,
under any heading level. So this is not a section that went stale in a later refactor: **the
deliverable was recorded as met and was never committed**, and the evidence cited for it was a
section number rather than the section's content.

What followed is the part worth keeping, because nothing caught it for two months:

- Two of T-005's log rows consume §11 — first *"26 numbered testable conditions"*, then an
  elaboration to 33 with *"the two not machine-checkable are 22 and 30"*. Both reason in detail
  about a document that does not exist.
- [T-004](T-004-critique-mode-blunt-section-by-section-review.md)'s log assigns itself *"§11
  conditions 15 and 23"*.
- [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) §3 ordered the build partly on
  *"finishing it produces §11 conditions 13–19 as checks"*.
- [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) is the one that noticed something was
  off and worked around it by hand, writing *"the rule the original text called condition 17"* →
  **DS-063** into its own criteria. It shipped a real check from it. Nobody did the other 32.

**The numbering is not reconstructible, and that is now settled rather than assumed.** If the
conditions had been the hard rules in document order, condition 17 would be the 17th; DS-063 is the
**31st**. The ordering existed only in the list that was never written, so *which* rules 22 and 30
were cannot be recovered from anything in the repository. This task therefore writes them off
explicitly instead of hunting for them — see the acceptance criteria.

**Why nothing caught it.** `python tools/tasks/task.py check` validates markdown links and
repo-relative paths. A `§11` written in prose is neither, so a reference to a section that never
existed reads exactly like a reference to one that does. Generalised as **L-39** — cite the content,
not the address — which also carries the second half of the diagnosis and the reason this task
records the carve-out **per rule**: the missing §11 was a *parallel list*, the same rules restated
in a different order, and a parallel list is the structure that can go absent without anything
breaking.

**Scope**
- In: a per-rule way to say *no check can reach this, and here is why* — a `Check` value, an extra
  column, or a footnote convention. Which one is the decision this task takes.
- In: applying it to the rules that are genuinely unreachable, starting with the four `audit.py`
  already excuses in print: **DS-033, DS-061, DS-065, DS-072**, whose reasons are already written
  and merely live in the wrong place.
- In: **writing off** the two rules §11 called 22 and 30, in the ruleset, as unrecoverable — and
  saying why, so the next reader does not re-run the search.
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
- [ ] §11's "conditions 22 and 30" are **written off as unrecoverable, in the ruleset, with the
      reason** — the numbering existed only in a list that was never committed, and DS-063 sitting
      31st rather than 17th is the evidence that it was not document order. Quietly dropping them is
      the failure this task exists to correct, so repeating it closes nothing
- [ ] Every surviving `§11` reference in `tasks/` is corrected — T-004, T-005 and T-030 each cite it,
      and a reader who follows one today lands on a document that ends at §9
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
| 2026-08-08 | → specified | **§1 corrected on evidence, and the correction makes this task's case stronger rather than smaller.** It was written saying [T-022](T-022-split-the-design-system-from-its-rationale.md) replaced §11's numbered conditions with `DS-nnn` IDs and the section went with the renumbering. **Checked against git before accepting the spec: that is wrong. §11 was never committed** — `docs/DESIGN-SYSTEM.md` has ended at §9 in all 13 commits of its life, created that way by the commit that closed [T-014](T-014-synthesise-research-into-the-design-system-reference.md) recording §11 as **met**. So this is not a stale-reference problem to tidy; it is a deliverable recorded as delivered on the evidence of a section number, which four task files then consumed for two months. **One acceptance criterion is settled by that check rather than left for `implement`:** the numbering is unrecoverable, proven — had the conditions been the hard rules in document order, condition 17 would be the 17th, and DS-063, the only one [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) ever translated, is the **31st**. Conditions 22 and 30 are therefore written off in the ruleset with the reason, not hunted for. A criterion was also added for the surviving `§11` references in T-004, T-005 and [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md). T-014's §4 verdict is corrected to `not met` and its log carries the account; **it is not reopened**, because its real deliverable exists and only the carve-out is missing — which is this task. The mechanism question stays open for `plan`, as written. |
| 2026-08-08 | → proposed | **Raised from [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s `specify`, and deliberately not fixed there** — a finding is not repaired where it is found. Working T-005's scope showed that the gate owns **109 rules** (65 `auto`, 44 `render`) of which **64 are silent**, and that its coverage account has to be *derived* from the ruleset rather than kept by hand (**L-08**). That derivation is impossible while the ruleset says only `auto` or `render`: an unreachable rule and an unbuilt one look identical. The reasons exist and are good — they are just in `audit.py`'s print statements. **The owner chose, 2026-08-08, that they belong per rule in the ruleset**, on [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent that a rule a shipped artifact contradicts is a defect in the ruleset rather than in the artifact. The task is `related` to T-005, not blocking it: T-005's §1 already assumes this field exists, so landing this later leaves that spec incomplete rather than wrong — [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md)'s test for whether an edge gates. |
