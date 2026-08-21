---
id: T-209
title: Six more probes measure a page whose entrance animation never ran, and none of them says so
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-185, T-206]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-21
updated: 2026-08-21
deliverables: []
---

# T-209 — Six more probes measure a page whose entrance animation never ran, and none of them says so

## 1. Specify

**Outcome**
Every probe that measures geometry either measures a settled page, or states in its own text why an
unsettled one is the right subject for it. Today six of them do neither, by omission rather than by
a decision anyone took.

**How it was found**
Closing [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) on 2026-08-21. That
task fixed `render.PROBE`, which is the probe `measure` and `shots` share. Every other consumer
builds its own and passes it through `make_probe(..., extra=…)`, so the fix reaches none of them:

| Probe | Built in | Pins motion |
| :--- | :--- | :--- |
| `PROBE` | [`tools/deck/audit.py`](../tools/deck/audit.py) `:1832` | no |
| `REDUCED_PROBE` | [`tools/deck/audit.py`](../tools/deck/audit.py) `:1889` | no |
| `PROBE` | [`tools/deck/chrome_row.py`](../tools/deck/chrome_row.py) `:256` | no |
| probe source | [`tools/deck/contents_bound.py`](../tools/deck/contents_bound.py) `:370` | no |
| `PROBE` | [`tools/deck/figgrid.py`](../tools/deck/figgrid.py) `:95` | no |
| `SHEET_PROBE` | [`tools/deck/printgeom.py`](../tools/deck/printgeom.py) `:263`, [`tools/deck/printpages.py`](../tools/deck/printpages.py) `:101` | no |

**The subject is present, which is what makes this worth a task.** In the portfolio-review deck the
figure wrapper and the headline both carry the entrance class — `class="body figwrap rise"` — and
`figgrid` measures `.body svg.fig` and `.headline` by name. T-206 measured the offset that class
produces at exactly **18.00 du**, the full `--rise-dist`, on a page read at frame zero.

**What is NOT established, and must not be assumed.** Whether each probe's particular comparison
actually reads an axis the entrance moves. `.rise` is `translateY`, so a check that compares `left`
offsets is untouched by it while one comparing `top` or `height` is not — and `figgrid`'s visible
comparison is a left offset, which may well be immune. **Six probes lacking the pin is six subjects
to measure, not six defects.** Filing it as six defects would be the same error T-206 corrected in
its own §1: writing down the lead as the finding.

**Why it is not folded into T-206.** That task's scope is *"making DS-063's verdict a function of
the deck's bytes"* and explicitly nothing wider. A fix that swept six more probes on the same day
would have made its ten-run evidence a statement about a much larger change than the one it argued
for.

**Scope**
- In: determining, per probe, whether any quantity it compares is moved by an entrance animation.
- In: pinning motion in the probes where it is, and recording the reason in the ones where it is
  not.
- Out: `MOTION_PROBE`. Measuring motion is its declared subject and it has its own name for exactly
  this reason (T-185).
- Out: re-opening DS-063 or any tolerance. T-206 settled that row.

**Inputs**
- [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) §3 — the measurement, the
  18.00 du offset, and the argument for an unconditional pin over a per-caller flag.
- [`docs/lessons/L-128.md`](../docs/lessons/L-128.md) — why two readings agreeing said nothing, and
  the general rule about a guarantee a caller can decline.
- **L-26** and [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) — a CSS animation's
  clock under `--virtual-time-budget` is frame production, not time.

**Acceptance criteria**
- [ ] For each of the six, a stated verdict: *pinned*, or *unpinned with the reason it is correct
      here*. No probe is left unexamined.
- [ ] Where a probe is pinned, its rule's verdict is shown before and after, so a changed number is
      visible rather than absorbed.
- [ ] The seeded-variant suites covering these rules still behave as specified.
- [ ] A guard, in the shape T-206 used: browser-free, structural, and failing if a pin is removed.

**Open questions**
- Whether the print probes are already settled by the print stylesheet, which may disable animation
  on its own. If so that is a *reason*, and the criteria above want it written down rather than
  inferred.
- Whether the pin belongs in `make_probe` — applied to every probe unless the caller is
  `MOTION_PROBE` — rather than copied into six probe sources. That is the T-206 argument applied one
  level up, and it is the likelier right answer, but it changes a shared function and should be
  decided in §2 rather than assumed here.

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
| 2026-08-21 | → proposed | Raised by [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md), which fixed the same fault in `render.PROBE` and found the other six by asking what else builds a probe. The subject is present — the deck's figures and headlines carry `.rise`, worth 18.00 du at frame zero — but whether each probe reads an axis that class moves is unmeasured, so this is six subjects rather than six defects. `PH3`: no adopter is affected, the exposure is this repository's confidence in its own instruments. |
