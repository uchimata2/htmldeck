---
id: T-205
title: Correct R9's gate-7 scoring and its account of what looking found
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-113, T-203, T-204]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-21
updated: 2026-08-21
shipped_in: 0.6.0
deliverables: [docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md]
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

**3 — R9 §6 says nine defects and the number is fifteen.** It reads as though the look was
complete. It covered **ten of twelve slides** and passed three of the ten; the owner found four more
([T-203](T-203-four-chart-defects-the-decks-look-missed.md)), and T-203's own closing look — twelve
of twelve this time — found **two more on slides 4 and 10, which that owner review had also
passed** ([T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md)). The paragraph
makes a real point — a green gate is not a good chart — and it makes it on a coverage figure it does
not state. **A claim about an instrument owes the instrument's coverage.**

*Corrected from thirteen 2026-08-21, and the correction is the argument.* The number moved twice in
one day without a line of the deck changing between the second and third look. So **the figure to
write into R9 is not a total at all** — any total is a reading of the last look's reach. Write what
each look covered and what it found, and let the total be derived. A defect count stated as a fact
about a deck will be wrong again the next time somebody looks.

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
- ~~Whether a corrected research note is edited in place or gains a dated correction block.~~
  **In place, marked**, as the precedent said. Every correction below carries its date and the task
  that made it, and none of them grew large enough to bury the finding it corrects — the longest is
  §6's coverage table, which replaces a sentence with a table and states *why* no total is given.
## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Score gate 7 per clause in §3, on the measurements already there — nothing re-fetched | a four-row table |
| 2 | Correct the recommendation, which said *fails on age* while §3 said otherwise | the summary agrees with the body |
| 3 | Put the archived-predecessor datum in §3 with its dates and where they were read | the better reason to wait |
| 4 | Replace §6's defect total with what each look covered and what it found | coverage, and no total |
| 5 | Read [T-204](T-204-an-instrument-for-mark-collisions.md)'s calibration and decide §7's second trigger either way | a recorded decision |
| 6 | Restate T-113's two §4 rows that rest on the same two errors, without reopening the task | an honest review table |
| 7 | `python tools/docs/refcheck.py`, then `python tools/tasks/lint.py` | green |

## 3. Implement

**Decisions & assumptions**
- **The recommendation was wrong in both halves, not one.** It read *"it fails gate 7 on one thing
  that time fixes by itself: it was 23 days old"*. §3 already said it fails on the missing track
  record, so the summary contradicted its own body — and *time fixes it by itself* is exactly what
  the archived predecessor argues against. Both are corrected in place and marked. — 2026-08-21
- **§7 keeps one trigger, and the second was tested rather than waved off.** The test set in §1 was
  *if a small checker catches the class, it is a detection gap rather than a capability gap*.
  [T-204](T-204-an-instrument-for-mark-collisions.md) settles it: `markhits.py` named the slide-4
  collision **unseeded** on its first run, the same defect a third human look had just filed.
  Calibration across four decks and 30 diagram slides — text-against-text 1 fire, 1 real, gates;
  text-against-line 16 fires, 1 real, reports. **The half that cannot gate is our own precision
  problem and no library gates it either**, so it argues for a better checker rather than a
  different default. — 2026-08-21
- **§6 states no total, and that is the correction.** The number was nine, then thirteen, then
  fifteen, and the deck did not change between the second look and the third. A total is a reading
  of the last look's reach. The section now carries a table of what each pass covered and found, and
  says why the total is left to be derived. — 2026-08-21
- **T-113 is restated, not reopened.** Both rows stay **met**; each gains a dated note saying what
  the claim was actually worth. Reopening a closed task to fix the wording of a criterion it did
  meet would make the record less true, not more. — 2026-08-21

**Outputs produced**
- [`docs/research/R9-...`](../docs/research/R9-embeddable-chart-library-versus-hand-authored-svg.md)
  — the recommendation, §3's per-clause table and archived-predecessor datum, §6's coverage table,
  §7's threshold decision, and §9's open item closed.
- [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) §4 — two rows
  restated.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Gate 7 is scored per clause wherever R9 states a verdict, and no summary line collapses six clauses into one word | **met** | §3 gains a four-row per-clause table on the measurements already there; the recommendation and §9's open item both restated. Two candidates fail gate 7 for opposite reasons — TanStack on `reliable`/`robust`, uPlot on `recently`/`continuously updated` — which the single verdict hid. |
| The archived-predecessor datum is in §3, with its dates and where they were read | **met** | `TanStack/react-charts` archived, last pushed 2025-03-10, npm `2.0.0-beta.7` in November 2023, read from the GitHub API and the npm registry on 2026-08-21. Stated as the better reason to wait, because age repairs itself and an abandoned predecessor does not. |
| §6 states the look's coverage rather than a bare defect count | **met** | A table: 10 of 12 slides and 9 found; the owner's review and 4 more; T-203's closing look at 12 of 12 and 2 more on slides the owner's review had passed. **No total**, with the reason stated. |
| T-113's §4 row for the deck criterion says what the look actually covered; the task stays `done` | **met** | Two rows restated, both still **met**. The second — *gate 7 eliminated TanStack Charts on age alone* — carried the same collapse and is corrected with it. |
| §7's threshold either gains the relational-geometry trigger **or** records why T-204's result means it should not | **met** | It does not gain it, and §7 records why with T-204's calibration figures. |
| `python tools/docs/refcheck.py` and `python tools/tasks/lint.py` green | **met** | refcheck: **3,187 pointers, 0 broken**; 924 section references resolved, 0 dead. lint: all four checks. |
| *(closing checklist step 3)* | **n/a** | This task produced no rendered artifact. Its output is four sections of a research note. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-21 | → proposed | Raised from the owner's review of T-113's output on the day it closed. Three corrections: gate 7 scored per clause rather than as one verdict, because two candidates fail it for opposite reasons; the archived predecessor as a better reason to wait than the 23 days; and R9 §6's defect count restated as a coverage figure, since the look it describes covered ten slides of twelve. Ranked behind T-203 and T-204 because the fourth change — whether the threshold gains a second trigger — is decided by what the checker turns out to catch. |
| 2026-08-21 | (no change) | **The count in correction 3 moves thirteen to fifteen, and that changes what the correction should say.** T-203's closing look covered all twelve slides and found two more defects on slides 4 and 10 — slides the owner's review had also passed (T-207). Two moves in one day on an unchanged deck means a total is a reading of the last look's reach, not a property of the deck, so R9 should carry coverage-and-yield per look and derive any total. The fourth change is still held for T-204. |
| 2026-08-21 | proposed → done | All three corrections made in place and marked, which is what the open question predicted. **The recommendation was wrong in both halves**: it said gate 7 failed on age while §3 said the missing track record, and *time fixes it by itself* is what the archived predecessor refutes — `TanStack/react-charts`, last pushed 2025-03-10, npm `2.0.0-beta.7` in November 2023. **§6 now states no total at all**, because the number moved nine → thirteen → fifteen in one day without the deck changing, so a total reads the last look's reach rather than the deck. **§7 keeps one trigger**, decided against T-204 rather than assumed: a checker caught the class unseeded, so it is a detection gap in our instruments, not a capability only a library supplies. T-113 restated, not reopened. |
