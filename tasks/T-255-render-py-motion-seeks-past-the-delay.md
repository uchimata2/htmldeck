---
id: T-255
title: Add the delay in the report branch and drop the subtraction in the capture branch
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225, T-272]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: unreleased
deliverables:
  - tools/deck/render.py
---

# T-255 — Add the delay in the report branch and drop the subtraction in the capture branch

## 1. Specify

**Outcome**
`render.py motion` samples an animation's own life. Today two branches write a seek and both are off by the delay: the report branch takes a fraction of duration from a clock that already includes the delay, and the capture branch subtracts the delay from an absolute clock that was already correct. **A working motion reads as dead** — *the computed style DOES NOT MOVE* is printed as a finding about the deck when it is a finding about the seek. Any non-zero delay shifts the whole report invisibly, and `rise` at delays 0, 60, 120, 180 and 240 is htmldeck's own reference stagger.

**From the adopter report** [`017`](../docs/adopter-reports/claimai/017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md).

**Scope**
- In: both branches, `render.py` `:597-598` and `:602`
- In: **the verdict line naming which it is** — an animation that interpolates to nothing and one whose sampled range never left the delay are different findings, and the second is the tool's own fault
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`017`](../docs/adopter-reports/claimai/017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md) — each carries its evidence, its version and its own proposed fix
- the adopter's reproduction: at `delay 600, duration 300` the five offsets are `0, 75, 150, 225, 300` and every one falls inside the delay
- the 100% offset reading `opacity 0.99902` on a staggered entrance — the report stops at 340 where the animation's real end is 400, so the frame labelled 100% is not the settled state

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce **on this repository's own deck**, not on the adopter's. `render.py motion examples/reference-deck.html --into 3`, saved | The baseline, and how many of its animations are sampled inside their own delay |
| 2 | Add the delay in the report branch and drop the subtraction in the capture branch | `tools/deck/render.py`, `MOTION_PROBE` — the two seeks the record names |
| 3 | Put the arithmetic in **pure Python** as well, so it can be seeded without a browser (**L-07**): `report_seeks` and `capture_seek` | Two functions the self-test can drive in both directions |
| 4 | Have the report **cross-check the browser's reads against that model** and say so when they disagree — the JS and the Python are two statements of one rule, and only a run can tell whether they still agree | A tool that reports its own seek going wrong instead of reporting it as the deck's |
| 5 | Print the sampled window on the header line, the way `motion_span` already names its clock | `delay 240, iterations 1, sampled 240-580 ms` |
| 6 | Split the verdict: an animation that interpolates to nothing is a finding about the deck; one whose sampled range never left the delay is the tool's own fault and says so | Record `017` item 3 |
| 7 | Re-run step 1 and diff. Then `python tools/tasks/lint.py`, and `python tools/check_all.py` at the end of the batch | Before and after, on the same deck |

## 3. Implement

**Decisions & assumptions**
- **The comment was half the defect and is corrected with it.** `MOTION_PROBE`'s header stated the
  right goal — *where it would be if the page had been photographed at `t`* — and the wrong
  arithmetic, `t - delay`, in the same sentence. `currentTime` is that absolute clock already. A
  comment that endorses the code beside it is why this read as correct for as long as it did —
  2026-08-29.
- **The seek is stated twice, in two languages, and the tool checks one against the other.**
  `report_seeks` is the same rule as the probe's, in Python where it can be seeded (**L-07**);
  `cmd_motion` compares the offsets the page reports back and prints `SEEK DISAGREES` when they
  part. Without it this fix would rest on one green browser run, because the arithmetic lives in a
  JavaScript string — 2026-08-29.
- **The verdict is a function, not an expression.** `motion_verdict` takes three answers where
  there were two, so the case that costs a reviewer a session — *DOES NOT MOVE* printed about the
  deck for a fault in the seek — is seedable without a browser. The reference deck has no
  animation whose delay exceeds its duration, so a run here could not have proved it — 2026-08-29.
- **`capture_seek` earns a caller rather than existing for its test.** The `--shots` loop uses it
  to print how many animations are past their delay at each frame; a frame where none is
  photographs as a page that has not started, which is what the defect produced five times —
  2026-08-29.

**Outputs produced**
- `tools/deck/render.py` — both seeks in `MOTION_PROBE`, its header comment, `report_seeks`,
  `motion_verdict`, `capture_seek`, the sampled-window line, the cross-check, the shots counter,
  and nine `self_test` assertions

**What was measured**

| Measurement | Result |
| :--- | :--- |
| `render.py motion examples/reference-deck.html --into 3`, before | 17 animations, **12 of them sampled inside their own delay**. The delay-240 rise spent three of five offsets at the FROM keyframe; the delay-60 rise ended at opacity `0.99902`, so the frame labelled 100% was not the settled state |
| The same command, after | 17 animations, **0 sampled inside their delay**. Every staggered rise now reads the same curve — `0 → 0.764865 → 0.961383 → 0.996894 → 1` — and the 100% offset is the settled state, `matrix(1, 0, 0, 1, 0, 0)` |
| **Seeded, both directions (L-125)** — the replaced report arithmetic restored in the probe and the real tool run | `SEEK DISAGREES` fires on **12 of 12** affected animations, naming what it wanted and what the probe sought. It catches the regression **even where the row still says MOVES**, which is the record's point: any non-zero delay shifts the report invisibly |
| The verdict's three answers, seeded on the adopter's own figures (delay 600, duration 300) | Sampled entirely inside the delay → *this is the seek's reading and not the deck's*; delay 0 and genuinely still → the plain verdict, so a real finding is not excused |
| One animation still reads `DOES NOT MOVE` after the fix — `(effect) on button`, delay 0 | Correct and left alone. Its seek window is right, so the verdict is about the deck. It is not this task's |
| `--shots`, end to end | Five frames written; the new line reads `0, 8, 12, 12, 12 of 12 animation(s) past their delay` and the images grow 39 → 94 → 168 KB before settling. That is a transition rather than five settled pages |

**Look owed — taken by the owner 2026-08-29, and it passed**

- **Deck** `examples/reference-deck.html`, **navigation** into slide 4, *Waiting is the trip*
  (`--into 3`), the five frames `motion-000.png` … `motion-100.png` written by `--shots` into
  `.assets-cache/deck/`.
- **What was looked for**, and both answers were *fine*:
  1. **A stagger rather than a fade** — the eyebrow, then the headline, then the standfirst, then
     the figure, then the bottom line, arriving one after another rather than together.
  2. **`075` against `100` specifically.** Their file sizes are 113,183 and 113,082 bytes, a
     hundred apart, and the arithmetic puts the bottom line still 57% risen at 435 ms — so two
     frames that looked identical would have been a real finding about the tail of the stagger.
     They did not.
- **This is the thing the machines could not answer.** The counts (`0, 8, 12, 12, 12 of 12 past
  their delay`) and the sizes (39 → 94 → 168 KB) both said the seek was landing in the right
  place; whether it *reads* as a transition is `CLAUDE.md` rule 6's, and
  [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 is why this session recorded
  it as owed and closed rather than deciding it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured, or explicitly deferred with the reason recorded | met | Record [`017`](../docs/adopter-reports/claimai/017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md) items 1, 2 and 3 are all implemented and measured above. Nothing deferred |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | met | Rows 3 and 4 of *What was measured*. The report arithmetic was restored in the probe and the real tool run against this repository's own deck |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | met | `lint.py` all four steps green with the baselined **eleven** advisories and no more. `check_all.py` **0 failures, 0 unclassified, 0 stale** over 37 commands and all 50 tracked tools, 278 s, run separately and after the last edit |

**Child fix tasks raised**
- [T-272](T-272-render-py-motion-enumerates-a-different-animation-set-across-runs.md) — found while
  diffing two post-fix runs of the same command on the same deck: the animation count came back
  `18` once in six runs and `17` the other five. Raised under
  [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4's *absorb what a batch finds*
  and added to B1. It does not affect the measurements above — every animation in question carries
  `delay 0`, so none of them is in the twelve.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | (no change) | **The owed look was taken by the owner and passed.** Both questions answered *fine*: the five frames read as a stagger rather than a fade, and `motion-075.png` and `motion-100.png` are distinguishable — the one place the numbers left room for a real finding, since they differ by 101 bytes. `T-255` closed on 2026-08-29 with this outstanding under [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4, and **the queue that section describes is now empty for this task**. The verdict is unchanged; what changes is that rule 6 is satisfied rather than deferred. |
| 2026-08-29 | → done | Every criterion met, all three of record `017`'s items implemented. **12 of 17 animations sampled inside their own delay before, 0 after**, on this repository's own reference deck; the seeded arithmetic is caught on 12 of 12 even where the row still says MOVES. One look is **owed** and recorded in §3 — the five `--shots` frames, which this session may not open. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
| 2026-08-29 | → specified | Batch B1 of [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md). **Reproduced on this repository's own `examples/reference-deck.html` before anything was written**, which the record could not do: **12 of its 17 animations were sampled inside their own delay**. The reference stagger is htmldeck's, so the adopter's deck was not a special case — this deck has been measured this way since the stagger existed. |
| 2026-08-29 | → in_progress | Both seeks corrected, and the header comment with them — it stated the right goal and the wrong arithmetic in one sentence. `report_seeks`, `motion_verdict` and `capture_seek` put the rule in Python where it can be seeded without a browser (**L-07**), and `cmd_motion` now checks the probe's offsets against `report_seeks` on every run. On this repository's own deck, **12 of 17 animations sampled inside their delay before, 0 after**. One finding absorbed into the batch as [T-272](T-272-render-py-motion-enumerates-a-different-animation-set-across-runs.md). |
| 2026-08-29 | → planned | Seven steps. Step 3 exists because the seek lives in a JavaScript string: without a pure statement of the same arithmetic there is nothing to seed, and **L-07** would have left this fix provable only by a browser run. |
