---
id: T-203
title: Fix four chart defects in the portfolio-review deck that a green gate and an incomplete look both passed
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-113, T-204]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-203 — Fix four chart defects in the portfolio-review deck that a green gate and an incomplete look both passed

## 1. Specify

**Outcome**
The four defects below are fixed in
[`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py), the deck is rebuilt,
and every gate stays green.

**How they were found, which is the part worth keeping**
Reported by the owner on 2026-08-21, reading the deck
[T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) closed the same day.
That task's closing look covered **ten of twelve slides** and passed three of the ten. So the deck
was recorded as *looked at* on a look that missed four defects, and `check.py`, `check_all.py` and
`printgeom.py` were green throughout. The instrument gap this exposes is
[T-204](T-204-an-instrument-for-mark-collisions.md)'s; this task is only the four fixes.

**The four, with the mechanism rather than the symptom**

| Slide | Symptom | Mechanism |
| :--- | :--- | :--- |
| **6** — the waterfall | the steps do not join at the ends they should | `fig_waterfall` draws each connector at **the next bar's top** instead of at the running total after the current bar. Three successive assignments to `yy` and the last one wins, so a down bar's connector leaves from the wrong edge. The running totals themselves are right — the self-test proves the waterfall closes on 2,400 — which is why it reads as decoration rather than as an error |
| **7** — the scatter | node and label conflict | Labels overprint the *equal return per unit of risk* diagonal, and the label-to-node binding is ambiguous: water's label starts nearer transmission's dot than its own. `spread()` separated them vertically and nothing tests whether a label crosses a line |
| **9** — the cost sum | bottom line, content and the nav bar all collide | The `.sum` grid spreads its rows to both ends of `.body`, so `$22.5M` at `--fs-figure` overruns the bottom line and `.sum-note` lands **inside the chrome**. This is the same class as slides 3 and 8, fixed there on 2026-08-21 with `.limitwrap` and not carried to 9 — because 9 was never looked at |
| **11** — the gated timeline | the diamond and its text conflict with the axis | The timeline's horizontal axis is drawn as one line across the full width, straight **through** the gate node and its second label. A gate on a timeline interrupts the line; it is not overdrawn by it |

**Scope**
- In: the four fixes, in the generator, and the rebuild chain the generator prints.
- In: a look at **all twelve** slides afterwards, not ten.
- Out: the checker. That is [T-204](T-204-an-instrument-for-mark-collisions.md).
- Out: R9's account of what looking found. That is
  [T-205](T-205-correct-r9s-gate-7-scoring-and-its-account-of-looking.md).

**Inputs**
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — `fig_waterfall`,
  `fig_scatter`, `fig_timeline`, and the `COMPOSITION` block's `.sum` rules.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.6 — the figure vocabulary, and the
  decision node's rule that the label sits inside the group.
- [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) §4 — the review
  row this task corrects the evidence for.

**Acceptance criteria**
- [ ] Slide 6's connectors leave each bar at the running total after it, and the fix is the running
      value rather than a rectangle edge, so the two cannot disagree again.
- [ ] Slide 7 has no label crossing the reference diagonal, and every label is nearer its own node
      than any other node.
- [ ] Slide 9's body holds its three rows from the top, and nothing on it reaches the bottom line or
      the chrome.
- [ ] Slide 11's axis breaks at the gate and resumes after it.
- [ ] `python tools/check_all.py` green, and `printgeom.py` PRINT-2 and PRINT-3 still pass.
- [ ] **All twelve slides looked at**, offline, and the count said out loud in the review — a look
      that covers ten of twelve is what this task exists to correct.

**Open questions**
- Whether the connector fix belongs in `fig_waterfall` or in a shared helper. A second waterfall is
  not in prospect, so local is probably right — but the running-total-versus-edge distinction is the
  reusable part.

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
| 2026-08-21 | → proposed | Raised from the owner's review of the deck T-113 closed the same day. Four defects across slides 6, 7, 9 and 11; three are relational geometry — where a connector attaches, whether a label crosses a line, whether an axis stops at a node — and one is the body-spreading layout bug already fixed on two other slides and not carried to this one. Every gate was green on all four. |
