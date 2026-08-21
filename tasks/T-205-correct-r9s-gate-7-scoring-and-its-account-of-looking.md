---
id: T-205
title: Correct R9's gate-7 scoring and its account of what looking found
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-113, T-203, T-204]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-205 — Correct R9's gate-7 scoring and its account of what looking found

## 1. Specify

**Outcome**
[R9](../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md) says what is now known
rather than what was known on the day it shipped, and its recommendation is re-read against the
evidence that arrived after it.

**Three corrections, each with the evidence behind it**

**1 — Gate 7 is six clauses and R9 scores it as one verdict.** The owner's wording is *free,
reliable, robust, simple, recently and continuously updated*. R9's summary says TanStack Charts
*"fails gate 7 on age"*, which is unfair to it in one direction and vague in the other. Scored per
clause on the same measurements:

| Candidate | free · simple | reliable · robust | recently · continuously updated |
| :--- | :--- | :--- | :--- |
| TanStack Charts | pass | **fail** | **pass — best of the four**, releases on 12 distinct days in 24 |
| Chart.js | pass | pass | thin — one release in twelve months |
| ECharts | pass | pass | pass |
| uPlot | pass | pass | **fail** — no release in twelve months |

Two libraries fail gate 7 for opposite reasons and the single verdict hid it. Reported by the owner
on 2026-08-21: *"a monthly release and 1-3 weeks old file still represent continuous maintenance and
improvements in my book"*, which is right and which R9 already supports in its body while denying in
its summary.

**2 — The better argument for *wait* is not the age, and R9 does not carry it.** Checked on
2026-08-21 against the GitHub API: `TanStack/charts` was created **2026-07-28**, so the 23 days is
real and is not a rename — the package is a new codebase, *"a tiny TypeScript visualization grammar
… powered by granular D3 primitives"*. But the same author's previous attempt at this problem,
`TanStack/react-charts`, is **archived**, last pushed 2025-03-10, and its npm package's last publish
was `2.0.0-beta.7` in November 2023. **That is a datum about this library's long-run odds and it
beats *23 days* as a reason.** R9 §3 should carry it.

**3 — R9 §6 says nine defects and the number is thirteen.** It reads as though the look was
complete. It covered **ten of twelve slides** and passed three of the ten; the owner found four more
([T-203](T-203-four-chart-defects-the-decks-look-missed.md)). The paragraph makes a real point — a
green gate is not a good chart — and it makes it on a coverage figure it does not state. **A claim
about an instrument owes the instrument's coverage.**

**And one thing to re-read rather than correct**
Three of the four new defects are **relational geometry** — where a connector attaches, whether a
label crosses a line, whether an axis stops at a node. R9 §7's threshold has one trigger, *the reader
interrogates the chart*, and these suggest a second: *the chart's geometry is relational*. **Do not
add it before [T-204](T-204-an-instrument-for-mark-collisions.md) reports.** If a hundred-line
checker catches the class, the trigger is a detection gap rather than a capability gap and the
threshold should not move — which is the whole reason that task is ranked ahead of this one.

**Scope**
- In: R9 §3, §5's gate-7 rows, §6 and §7, and the summary at the top.
- In: T-113's §4 review row for the deck criterion, which rests on the same incomplete look.
- Out: changing the recommendation. That is a re-read, and its input is T-204's report.
- Out: DS-122's amendment, which is
  [T-202](T-202-amend-ds-122-into-a-threshold-and-bind-its-check-on-structure.md).

**Inputs**
- [R9](../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md) — the document.
- [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) §3 and §4 — the
  measurements R9 was written from, and the review row to correct.
- [T-204](T-204-an-instrument-for-mark-collisions.md) — whose report decides whether §7's threshold
  moves.

**Acceptance criteria**
- [ ] Gate 7 is scored per clause wherever R9 states a verdict on it, and no summary line collapses
      six clauses into one word.
- [ ] The archived-predecessor datum is in §3, with its dates and where they were read.
- [ ] §6 states the look's **coverage** — how many slides, and how many defects each pass found —
      rather than a bare defect count.
- [ ] T-113's §4 row for the deck criterion says what the look actually covered. The task stays
      `done`; the criterion is restated honestly rather than the task reopened.
- [ ] §7's threshold either gains the relational-geometry trigger **or** records why T-204's result
      means it should not.
- [ ] `python tools/docs/refcheck.py` and `python tools/tasks/lint.py` green.

**Open questions**
- Whether a corrected research note is edited in place or gains a dated correction block. This
  project's precedent is in-place with the correction marked — R9 §1 already does that for T-113's
  own premise — so in-place, marked, unless the change gets large enough to bury the original
  finding.

## 2. Plan

*Not started.*

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
-

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised from the owner's review of T-113's output on the day it closed. Three corrections: gate 7 scored per clause rather than as one verdict, because two candidates fail it for opposite reasons; the archived predecessor as a better reason to wait than the 23 days; and R9 §6's defect count restated as a coverage figure, since the look it describes covered ten slides of twelve. Ranked behind T-203 and T-204 because the fourth change — whether the threshold gains a second trigger — is decided by what the checker turns out to catch. |
