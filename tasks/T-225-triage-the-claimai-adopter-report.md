---
id: T-225
title: Triage the ClaimAI adopter report and decide each of its twenty-seven findings
type: analysis
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-063]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-28
updated: 2026-08-28
deliverables: []
---

# T-225 — Triage the ClaimAI adopter report and decide each of its twenty-seven findings

## 1. Specify

**Outcome**
Every finding in [`docs/adopter-reports/claimai/`](../docs/adopter-reports/claimai/README.md) has a
decision against it — accepted and raised as a fix, accepted and deferred, or rejected with a reason.
Nothing in the set is left unjudged. This task produces the judgement; the fixes it accepts become
tasks of their own.

**Where it came from**

An outside project used htmldeck to build a twenty-five slide executive board presentation, under a
deadline, as the deliverable of a formal training exam. It ran from 2026-08-23 to 2026-08-28, kept 84
task records, and shipped. Twenty-seven findings came out of that work and were staged as they were
found rather than written up afterwards.

**The deck was presented and judged good.** That is the frame for the whole set: these are the places
where a tool that produced a good result made reaching it harder than it needed to be. The report's
own covering note puts the goal as *not to limit but to support such results*.

**Nobody is waiting for an answer.** The project that produced this is closed. There is no thread, no
deadline and no reply expected — the set is a one-way hand-over, written to stand alone. Take what is
useful and discard the rest, including any record judged wrong.

**What makes this set worth the time**

- **It is evidence, not opinion.** Every record carries the command and its output, the source line,
  or the verdict the tool itself printed. The staging project's standing rule was that a claim about
  a tool's behaviour without one is a guess.
- **It is not one-sided.** Six rules are named as having caught real faults — `DS-091`, `DS-143`,
  `DS-215`, `DS-236`, `DS-239` and `DS-202` — inside the records that criticise others. `022` says
  plainly that `DS-244` improved the slide three times while being wrong.
- **It reports what the gate cannot see.** The four records with the highest value here are the ones
  where `check` was green and something was wrong anyway: `025`, `026`, `016` and `017`.

**Four things worth knowing before reading**

1. **The deck fails four rules permanently** — `DS-110`, `DS-217`, `DS-218`, `DS-219` — and has since
   the build. An author who cannot ever reach zero stops reading the gate, and that is the cost
   behind several of these records rather than the rules themselves.
   [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md) is the
   sharpest of them: `DS-219` is unsatisfiable for a whole class of correct diagrams, and
   `docs/DESIGN-RATIONALE.md` §5.7 already records this repository's own doubt about the rule.
2. **`DS-244` is reported twice, deliberately, from opposite directions.**
   [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md)
   says it is too blind;
   [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) says it is too
   strict. Read together they say the rule tests proximity where it means obstruction — which neither
   record says alone. **Triage them as a pair, not separately.**
3. **One finding is a note about this repository's own examples.**
   [`018`](../docs/adopter-reports/claimai/018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md)
   shows `portfolio-review` passing `DS-218` with `0 looping` — the rule never fires, so the example
   models a control placement that is safe only for want of a subject. The adopter's first reading was
   that the example contradicted the rule, and running the gate on the example is what corrected it.
   **An example that satisfies a rule vacuously is worth finding elsewhere in the set of four.**
4. **`density.py write` is currently refused outright by that project's launcher**, because it
   corrupts self-closing SVG tags —
   [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md).
   It is the tool `DS-239` makes necessary, so the rule and the broken writer compound: see
   [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md).
   That pair is the one place in the set where a rule and a defect together produce an adopter
   editing generated markup by hand.

**Scope**
- In: all twenty-seven records; one decision each; a fix task for every accepted finding.
- Out: fixing anything here. A triage that turns into an implementation stops being a triage, and
  three of these records touch rules rather than code.
- Out: replying to the adopter. There is no channel and none is expected.

**Inputs**
- [`docs/adopter-reports/claimai/README.md`](../docs/adopter-reports/claimai/README.md) — the covering
  note, the index and four suggested themes
- The twenty-seven records beside it
- `docs/DESIGN-SYSTEM.md` and `docs/DESIGN-RATIONALE.md` — the rules under discussion, and §5.7, which
  already doubts `DS-219`

**Acceptance criteria**
- [ ] Every one of the twenty-seven records carries a decision: accepted and raised, accepted and deferred, or rejected with a reason
- [ ] `013` and `022` are decided together, as one question about what `DS-244` is testing
- [ ] Each accepted finding names the task that will do it
- [ ] Each rejected finding says why, in a sentence an adopter would accept — the records are evidence-led, so a rejection needs a reason of the same kind
- [ ] The four permanently-failing rules are looked at as a group, and the outcome says whether a deck failing four rules by design is acceptable
- [ ] `Version seen` is checked before any record is actioned: fourteen were stamped rather than re-run, so a finding may already be fixed

**Open questions**
- None for the adopter — the report is closed and expects nothing. Every open question here is this
  repository's own.

## 2. Plan

Not planned.

## 3. Implement

**Decisions & assumptions**

**Outputs produced**

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |

**Child fix tasks raised**

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-28 | → proposed | Created when the adopter report was handed over. The report was collected during the project rather than written up afterwards, and every claim in it was verified against `0.6.0` before it was staged. Nothing is expected in return. |
