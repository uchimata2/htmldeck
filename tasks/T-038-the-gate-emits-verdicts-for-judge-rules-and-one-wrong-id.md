---
id: T-038
title: Stop the gate reporting judge rules, and one verdict under the wrong rule ID
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-005, T-014, T-037]
work_package: WP3
owner: maintainer
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-038 — Stop the gate reporting judge rules, and one verdict under the wrong rule ID

## 1. Specify

**Outcome**
Every verdict `tools/deck/audit.py` emits cites a rule that the ruleset says a check may decide, and
cites the rule it is actually testing. Where the gate is measuring a *proxy* for a rule rather than
the rule, either the rule gains an ID for the proxy or the gate stops claiming it.

**Why this one**
Found while populating [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md)'s
`Reach` column, which forced a row-by-row reading of what the gate claims against what the ruleset
says. Two rules labelled `judge` — the evaluator's territory, explicitly *"judgement"* — are gated
mechanically, and one of the two reports under an ID whose rule it does not test.

**The two, with the evidence**

| | Ruleset says | `audit.py` emits |
| :--- | :--- | :--- |
| **DS-137** | *"Two simultaneous interactions need a **defined precedence rule**."* `hard` / `judge` | `panels open at once: <n>`, passing when `<= 1` (`audit.py` ~line 428) |
| **DS-161** | *"**Closed, the slide still makes its point.**"* `hard` / `judge` | `panels closed by default: <n> open`, passing when `0` (`audit.py` ~line 426) |

DS-137 is the milder case: at most one panel open is *evidence of* a precedence rule for one
interaction pair, not the rule, which is about precedence in general. **DS-161 is the real defect.**
Its rule is a judgement about whether the argument survives with everything closed; *"panels are
closed at load"* is a **precondition** of asking that question and is not the question. The check is
worth keeping — it is just not DS-161, and the source comment says as much, reading
`// DS-160/161 - closed by default` while DS-160 is *"Two tiers, never three."* So the comment names
a third rule that is also not what is being measured.

**Scope**
- In: the two verdicts above — decide for each whether the rule's `Check` value is wrong, the gate
  should stop claiming it, or a new rule ID is owed for the mechanical fact.
- In: a sweep of the rest of `audit.py`'s verdicts for the same mismatch, since two were found
  without looking for them.
- In: whatever `Reach` values the outcome implies, written into the ruleset.
- Out: **building any new check.** This task corrects what existing verdicts claim.
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) owns coverage.
- Out: the `judge` rules' own home — `docs/EVALUATION.md` is unaffected either way.
- Out: `audit.py`'s *"Not gated here, and why"* tail, which
  [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) found conflates *"checked
  in another stage"* with *"cannot be checked"*. Same file, different defect, and it belongs with
  T-005's coverage work.

**Inputs**
- `tools/deck/audit.py` — the verdict list, and the `// DS-160/161` comment above the probe.
- [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-137, DS-160, DS-161, and the `Check` and
  `Reach` column definitions.
- [`EVALUATION.md`](../docs/EVALUATION.md) §1 — `judge` rules are scored, not gated, which is the
  boundary being crossed.

**Acceptance criteria**
- [ ] Every verdict `audit.py` emits names a rule whose `Check` value permits a check to decide it
- [ ] No verdict cites a rule it does not test; where a proxy is being measured, the thing measured
      and the rule cited are the same thing, or the proxy has its own ID
- [ ] The DS-160/161 comment names the rule actually being probed
- [ ] The rest of the verdict list is swept for the same mismatch, and the count found is stated —
      including if it is zero
- [ ] Whatever changes, `audit.py` still reports **0 mechanical failures** on
      `examples/reference-deck.html`, or the new failure is a real defect and is written down as one
- [ ] Any rule whose `Check` value changes gets its `Reach` value reviewed in the same edit, so the
      two columns cannot disagree

**Open questions**
- **Does *"closed by default"* deserve its own rule ID, or is it already DS-073's inverse? — owner.
  *Recommended: give it its own ID*, and the owner indicated support for this reading on
  2026-08-09; it is recorded as the recommendation rather than as the answer, because the rule's
  actual wording is this task's work and not a thing to settle in a sentence.**

  The objection to inventing a rule so a check has somewhere to live is real, but it does not apply
  here, and the distinction is worth stating because it will come up again. **It is backwards when
  the check is the reason the rule exists.** Here the rule is load-bearing and simply was never
  written down: *on the stage, every disclosure panel is closed at load* is a **precondition that
  two other rules already depend on**. DS-161 asks whether the slide still makes its point with
  everything closed — a question with no content unless closed-at-load is guaranteed. DS-073
  requires the reflow view to render every panel **open** and inlined, which is only a meaningful
  contrast against a stage that starts closed. So two rules lean on a fact the ruleset never
  states, and the check that happens to exist is evidence the fact matters, not the motive.

  DS-073's inverse is the tempting shortcut and it is not sufficient: DS-073 governs the **reflow
  view**, and a rule about a different rendering cannot carry an obligation on the stage by
  negation. Reading it that way would leave the stage's behaviour derivable only by someone who
  notices the inversion — which is the class of unstated dependency this whole task is about.

  What this implies for the rest of the task: DS-161 keeps its judgement and stays `judge`, the new
  rule takes the mechanical fact as `hard` / `auto` / `Reach: yes`, and `audit.py`'s existing probe
  moves to it unchanged — a re-pointing rather than new work, which is what keeps this inside §1's
  *"out: building any new check"*.

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
| 2026-08-09 | (no change) | **The owner sequenced this ahead of [T-005](T-005-build-check-the-gate-the-deck-must-pass.md), and the reason is worth keeping because it works in one direction only.** T-005's coverage account asserts a number derived from the ruleset — **105** when this was written, being `Reach: yes` with `Check` in {`auto`, `render`}. This task's last acceptance criterion requires any rule whose `Check` value changes to have its `Reach` reviewed in the same edit, so **landing this can move that number**. Running T-005 first would have it build an account that counts DS-137 and DS-161 as covered, one of them under an ID whose rule the gate does not test, and then need re-deriving anyway. Recorded here rather than only in the handoff: a handoff is consumed once, and this ordering has a reason that outlives it. Whoever plans T-005 should **re-derive the count after this task closes** rather than carrying 105 across. |
| 2026-08-09 | → proposed | **Raised from [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md)'s implement, and deliberately not fixed there.** Populating the `Reach` column forces a row-by-row comparison of what the ruleset says a rule is against what the gate claims about it, and that comparison found two `judge` rules being gated mechanically — **DS-137** and **DS-161** — with DS-161's verdict measuring *"panels closed at load"*, which is a precondition of its rule rather than its rule. The source comment above the probe reads `// DS-160/161 - closed by default` and DS-160 is *"Two tiers, never three"*, so it names a third rule that is also not what is measured. **Both were found without looking for them**, which is why §1 puts a sweep of the remaining verdicts in scope. Not fixed in T-037 because re-labelling a rule and editing the gate are both outside that task's scope, and it would have meant changing the column it was in the middle of populating on the strength of its own reading. |
