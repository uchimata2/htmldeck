---
id: T-203
title: Fix four chart defects in the portfolio-review deck that a green gate and an incomplete look both passed
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-113, T-204, T-206, T-207, T-208]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-21
updated: 2026-08-21
shipped_in: unreleased
deliverables: [tools/examples/portfolio_charts.py, examples/portfolio-review/portfolio-review.html]
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

**Re-specified 2026-08-21.** Every mechanism above was read against the source before planning,
and all four hold. One correction to the slide-6 row: the defect is not one wrong expression but
**three successive assignments to `yy` of which the first two are unreachable and the third is a
tautology** — `yy = nxt[2] if WATERFALL[i + 1][2] in ("up", "total") else nxt[2]` returns `nxt[2]`
on both arms. So the whole block is removed rather than patched, which is what the first acceptance
criterion asks for and would not have been satisfied by editing the surviving line.

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
- ~~Whether the connector fix belongs in `fig_waterfall` or in a shared helper.~~ **Settled
  2026-08-21: local to `fig_waterfall`.** No second waterfall is in prospect, and the reusable part
  is not a drawing helper but a *check* — whether a connector meets the bar it belongs to — which is
  [T-204](T-204-an-instrument-for-mark-collisions.md)'s subject, not a second call site's.

## 2. Plan

Eight steps. Steps 1 to 4 are the four fixes, one slide each and independent of each other; 5 makes
two of them checkable by the generator itself; 6 to 8 are the rebuild and the two bars this task is
closed against.

**1 — slide 6, the connector leaves at the running total.** `fig_waterfall` already computes `run`,
the running total after each bar, and then throws it away. Capture it per bar and draw connector *i*
at `linear(run_after_i, lo, hi, BASE, TOP)`. The three `yy` assignments go, all of them: the first
two are unreachable and the third returns `nxt[2]` on both arms. This is the acceptance criterion's
*running value rather than a rectangle edge* — the connector and the bar can no longer disagree,
because only one of them is now computed.

**2 — slide 7, labels are placed on the side away from the reference line.** The diagonal is
`irr = vol`, rising to the right. Today the side is chosen by `vol < 11.0`, which is unrelated to it,
so the two low-volatility labels run along the line. Choose the side by which side of the line the
point is on: **above the line, the label goes left; below it, right.** That moves every label away
from the diagonal instead of along it, and it fixes the binding at the same time — a label left of
its own dot cannot start nearer a neighbour's. The two groups are re-spread on their own, as now.

**3 — slide 9, the body is made to fit the row it has.** Measured, at the design scale where
`.body` is 543 px: `.sum` is **726 px, 183 px over**, so `$22.5M` crosses the bottom line and
`.sum-note` lands 56 px below it, inside the chrome. Two changes, both in this deck's own
`COMPOSITION`:
- the vertical rhythm tightens — `.sum` gap and the two component rows' padding to `--sp-1`, the
  voice and note margins to `--sp-2`, the total's rule spacing to `--sp-1` / `--sp-2`;
- the total takes `--fs-title` with `line-height:.9` instead of `--fs-figure` at `line-height:1`.

Measured result: **498 px in 543, 45 px of headroom.** The alternatives were measured and rejected —
tightening alone leaves it 59 px over, and keeping `--fs-figure` fits only by deleting the note,
and then by 19 px. **No authored word is removed.** The total still reads as the total: it keeps the
rule above it, the accent colour, the pulse and its label, which is what `.sum-total` distinguishes
itself by. A sum set twice the size of its parts is decoration; one set off by a rule is a ledger.
`line-height:.9` also matches `.two-fig-val` and `.stat-figure` — the total was the only figure in
this deck at `line-height:1`.

**4 — slide 11, the axis stops at the gate.** Draw it as two segments, `240 → gate_x - hw` and
`gate_x + hw → 1620`, meeting the rhombus at its left and right vertices, which sit on the axis `y`
by construction. A gate on a timeline interrupts the line.

**5 — three identities added to `selftest()`**, so two of the four cannot come back silently: each
connector's `y` equals the running total after its bar; no scatter label box meets the reference
diagonal; every scatter label's anchor is nearer its own node than any other. These are this deck's
own arithmetic, in the generator that already holds 22 such checks — **not** the instrument, which
stays [T-204](T-204-an-instrument-for-mark-collisions.md)'s, and they leave its four subjects intact.

**6 — rebuild, in the order the generator prints**: `portfolio_charts.py`, then `shell.py icons`,
`density.py write`, `preflight.py --write`, `check.py --sources`.

**7 — the gates**: `check_all.py` green, and `printgeom.py` PRINT-2 and PRINT-3 still passing.

**8 — look at all twelve slides**, offline, and say the count in §4. A look that covered ten of
twelve is what this task exists to correct, so the count is part of the result and not a footnote.

## 3. Implement

**Decisions & assumptions**

- **The connector fix is local to `fig_waterfall`** — the owner's ruling on the §1 open question,
  2026-08-21. The reusable part is a *check*, not a drawing helper, and it landed as one.
- **Slide 9 was fixed against a measurement, and §1's mechanism was wrong.** The report said `.sum`
  *spreads its rows to both ends of `.body`*; it does not. `.body` is a block box in the slide
  grid's `1fr` row carrying `min-height:0`, so its content overflows **downward** and nothing
  spreads — `align-content:center` on `.sum` was inert throughout. Measured at the design scale
  where `.body` is 543: the block was **726, 183 over**, the total crossed the bottom line, and the
  note sat **56 below it**, in the chrome. Four candidate fixes were measured rather than argued:
  tightening alone 602 *(59 over)*; tightening plus `line-height:.9` 583 *(40 over)*; tightening plus
  dropping the note 524 *(19 of headroom, one authored line deleted)*; **tightening plus the total at
  `--fs-title` 498 *(45 of headroom, nothing deleted)*** — which is what shipped.
- **Slide 7's side is chosen by the reference line, not by volatility.** `vol < 11.0` had no relation
  to the diagonal it was putting labels on.
- **The new identities read the emitted SVG rather than recomputing the placement**, because a check
  that re-derives what it checks shares its bug and passes. Written up as **L-127**.
- **Both new checks were proved by seeding the old code back.** The connector check fired on the
  first join; the diagonal check named **`Transmission 9.1 / 6.2` and `Water 7.4 / 4.8`** — the two
  labels the owner's report named, arrived at independently.
- **§1's second slide-7 claim is false as measured, and is corrected here.** It reads *"water's
  label starts nearer transmission's dot than its own"*. Before the fix, water's label anchor was
  **26.9 du from its own node and 75.5 from transmission's**; after it, 30.2 and 126.2. It was never
  nearer the wrong node. What was true, and is fixed, is the label running along the diagonal — the
  reading was ambiguous, the distance was not. The acceptance criterion built on the claim is
  therefore met but was never violated, and is marked so in §4 rather than counted as a fix.
- **The rebuild chain's third step did not run.** The generator printed
  `preflight.py <deck> --write`, which that tool has no such command for; the command that writes a
  deck's rows is `shell.py preflight`. The generator's line is corrected here because this task had
  to run the chain. The tool's own usage block, which also omits it, is
  [T-208](T-208-shell-py-does-not-list-the-command-its-own-error-names.md).
- **The self-test's printed total was under-reporting by one** — the constant read `+ 12` against 13
  relations, and had done since a fifth allocation year was added. Corrected while the four new
  checks were added, so the line now counts what it runs.

**Outputs produced**
- [`tools/examples/portfolio_charts.py`](../tools/examples/portfolio_charts.py) — the four fixes,
  five new identities with their SVG readers, and the corrected rebuild chain.
- [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html)
  — rebuilt through the chain, 397,241 bytes, 12 slides.
- [`docs/lessons/L-127.md`](../docs/lessons/L-127.md) — a figure can be arithmetically right and
  relationally wrong.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| Slide 6's connectors leave each bar at the running total after it, from the running value rather than a rectangle edge | met | The three assignments are gone. `bars` now carries the running total and the connector is `linear()` of it, so there is one number where there were two. Checked by *every waterfall connector sits on the edge both its bars share* — stated in the picture's terms, and it fires on the old code |
| Slide 7 has no label crossing the reference diagonal | met | Side chosen by which side of `irr = vol` the point sits on. Seeding the old rule back names `Transmission` and `Water`, the two the owner named |
| ... and every label is nearer its own node than any other node | met, **not violated before** | Measured both ways: worst margin before the fix 26.9 against 75.5, after it 26.6 against 70.2. §1's claim that water's label was nearer transmission's dot does not hold — corrected in §3 |
| Slide 9's body holds its rows from the top, and nothing reaches the bottom line or the chrome | met | 498 of 543, 45 of headroom. `render.py measure` reported *body content spills 99 / 312 / 275 du* on the committed deck at three resolutions and reports none on this one |
| Slide 11's axis breaks at the gate and resumes after it | met | Two segments meeting the rhombus's left and right vertices, which sit on the axis `y` by construction |
| `python tools/check_all.py` green, and `printgeom.py` PRINT-2 and PRINT-3 still pass | met, **on a gate that does not answer the same way twice** | `check_all.py`: 35 ran, 2 skipped with a reason, 0 failed, 0 unclassified, 0 stale, 389 s. `printgeom.py` PRINT-2 and PRINT-3 both pass. But DS-063 returned four different worst values across six runs of one command on one unchanged file — [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md). This green is real and it is also not repeatable, and the second half is the more useful fact |
| All twelve slides looked at, offline, and the count said out loud | met | **Twelve of twelve**, rendered by `render.py shots` and opened one at a time. Ten of twelve is what this task existed to correct. The look found the four fixes correct **and two more defects of the same class on slides 4 and 10** — [T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md) |

**Child fix tasks raised**
- [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) — DS-063 is
  non-deterministic. `PH1`: a defect in a published gate.
- [T-207](T-207-two-more-mark-collisions-the-twelve-slide-look-found.md) — two more mark collisions,
  on slides 4 and 10, both passed by two earlier human looks and by every gate.
- [T-208](T-208-shell-py-does-not-list-the-command-its-own-error-names.md) — `shell.py`'s usage block
  omits the command its own failure message tells you to run.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-21 | → proposed | Raised from the owner's review of the deck T-113 closed the same day. Four defects across slides 6, 7, 9 and 11; three are relational geometry — where a connector attaches, whether a label crosses a line, whether an axis stops at a node — and one is the body-spreading layout bug already fixed on two other slides and not carried to this one. Every gate was green on all four. |
| 2026-08-21 | proposed → specified | **Re-specified against the source before planning**, as the three-task order asks. All four mechanisms in §1 hold as written. One correction, recorded there: slide 6 is three dead assignments and a tautology rather than one wrong expression, so the fix deletes the block instead of editing it. The one open question is settled by the owner — the connector fix stays local, because the reusable part is a check rather than a helper. `deliverables` declared, which a task at `specified` owes (TOOLING §3). |
| 2026-08-21 | specified → planned | Eight steps, one per slide for the four fixes plus a self-test step, the rebuild chain and the two bars. **Slide 9 was planned against a measurement rather than a reading**: `.sum` is 726 px in a 543 px body, and the fix that fits without deleting any authored copy is the total at `--fs-title` with `line-height:.9` plus a tightened rhythm — 498 px, 45 px of headroom. Tightening alone leaves 59 px over, and keeping `--fs-figure` fits only by dropping the note. §1's *spreads its rows to both ends* is corrected there too: the body is a block in a `1fr` row with `min-height:0`, so the content simply overflows downward — there is no spreading, and `align-content:center` on `.sum` was inert. |
| 2026-08-21 | planned -> in_progress | The four fixes, the five identities and the rebuild. Two things the plan did not foresee: the chain's third step is a stale command, corrected in the generator; and §1's account of slide 9 is wrong about the mechanism, which the measurement settled and which changed the fix. |
| 2026-08-21 | in_progress -> done | **Closed. Four defects fixed, six criteria met, and the look that closes it covered twelve of twelve.** Both new relational checks were proved by seeding the old code back, and the scatter one independently named the two labels the owner had. Three children raised, and the two that matter are not about charts: **DS-063 answers differently on identical input** (T-206), so the green this task closes on is real but not repeatable; and **the twelve-slide look found two more collisions on slides that two earlier looks had passed** (T-207) - which is the argument T-204 was raised to make, now with six subjects rather than four. `shipped_in` is `unreleased`. |
