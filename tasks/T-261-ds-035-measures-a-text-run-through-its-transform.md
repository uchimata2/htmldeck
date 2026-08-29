---
id: T-261
title: Re-derive whether audit.PROBE can stay unpinned, on a deck whose entrance moves the axis
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225, T-254]
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-261 — Re-derive whether audit.PROBE can stay unpinned, on a deck whose entrance moves the axis

## 1. Specify

**Outcome**
`DS-035` decides legible type rather than mid-entrance geometry. Today the probe scales the computed font size by the element's screen CTM, so an ordinary `scaleY(0)` entrance with `fill-mode:both` puts the determinant at 0 and the rule fails three display-size headings at **0 du** — and the row says *text below 16 design units*, which sends a builder looking for a font size.

**From the adopter report** [`006`](../docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md).

**Scope**
- In: measuring the rest state, or naming the transform as the cause when `sqrt(|det|)` is under 1
- In: **`DS-035` saying when a CTM is degenerate**, deferred here by [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md) on 2026-08-29. Adopter record [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) item 3 is the source: a broken tag made the browser reparent a subtree, and three untouched labels came back at `0.0 du` — **not small type, no type**, reported as a type-size failure. It is the same measurement and the same row as the clause above, which is why one task owns both. **This task closes that record's item 3**
- In: **re-deriving [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md)'s verdict for `audit.PROBE`**, which is the part worth more than the fix — see the inputs
- In: the `DS-035` row saying the measurement is taken through the element's transform. Nothing in it hints that an entrance can fail a legibility rule
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`006`](../docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md) — each carries its evidence, its version and its own proposed fix
- **This finding refutes a measurement the audit recorded as settled.** T-209 left `audit.PROBE` unpinned and its comment in `tools/deck/audit.py` reads *its geometry rows were measured both ways on the portfolio deck and are identical, so pinning buys nothing here*. That was one deck, whose entrances happen not to move the axis `DS-035` reads; this deck's do. **The conclusion does not generalise and the comment states it as if it does.**
- the design problem underneath: the same probe must stay unpinned for `DS-140`, `DS-142` and `DS-218`, which read `animationIterationCount`, and settled for `DS-035`, which reads geometry. One probe cannot be both, so this is a split rather than a flag

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

**T-209's verdict, re-derived — the measurement this task was worth more for than the fix.**
`audit.PROBE` was run as it ships and again with `MOTION_PIN` forced in, and every `out.*` key
compared:

| Deck | Keys differing, pinned vs unpinned |
| :--- | :--- |
| [`examples/portfolio-review/portfolio-review.html`](../examples/portfolio-review/portfolio-review.html) | **0 of 65** |
| a seeded `scaleY(0)` entrance with `fill-mode:both` on `svg text.lab`, delay not yet elapsed | **3 of 66** — `underFloor` (`DS-035`), `connectorLabelGap` (`DS-117`), `infinite` (`DS-140`/`DS-142`/`DS-218`) |

**T-209 reproduces exactly and does not generalise.** Its own deck is identical both ways, which is
what its comment says; a deck whose entrance moves the axis moves **two geometry rows as well as the
motion row**, and in opposite directions — unpinned, `underFloor` reports three runs at `0 du` that
pinning empties; pinned, `infinite` loses the only looping subject it had. One probe cannot be both,
which is the split the specify section predicted. Six paired runs, all identical; the seed is
deterministic — a 60 s delay inside a 4 s virtual-time budget — so the rate is 1, not a sample
(**L-138**).

**The split is in time, not in a flag.** The probe's own header comment already prescribed it —
*pin locally after the motion facts are read* — and nothing had done it.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Re-derive T-209's verdict: `audit.PROBE` pinned and unpinned, on its own deck and on a deck whose entrance moves the axis | The table above. **Done** |
| 2 | Split `render.MOTION_PIN` into a definition and its call, so the pin's CSS keeps **one** home and a `MEASURES_MOTION` probe can apply it at a moment of its choosing | `render.py` |
| 3 | In `audit.PROBE`, read the motion facts first, apply the pin, then take every geometry measurement below it. Rewrite the header comment, which states T-209's conclusion as if it generalised | `audit.py` |
| 4 | Report a **degenerate** CTM as its own condition inside `DS-035`, with the raw `font-size` beside the design units — `0.0 du` is no type, not small type (record `015` item 3) | `audit.py` |
| 5 | Amend the `DS-035` row to say the measurement is taken through the element's transform, on a settled page | `docs/DESIGN-SYSTEM.md` |
| 6 | Prove both directions: the entrance stops failing, genuine small type still fails, a degenerate CTM is named as one, and `static_variants.py`'s `motion-stop-shut-inside-the-menu` is **still CAUGHT** — the regression the split could cost | seeded runs |
| 7 | `python tools/tasks/lint.py`, then `python tools/check_all.py`, run separately | green |

## 3. Implement

**Decisions & assumptions**
- **The split is in time, not in a flag — 2026-08-29.** `render.MOTION_PIN` is now an installer
  (`MOTION_PIN_FN`) plus a call (`MOTION_PIN_CALL`); the pin's CSS keeps one home. A probe declaring
  the new `PINS_LOCALLY` marker beside `MEASURES_MOTION` receives the installer alone and calls it
  when it chooses. `audit.PROBE` reads its motion facts, then calls it, then measures geometry. A
  `pin=False`-style parameter was rejected for T-209's own reason: an exemption a caller passes is
  not a guarantee (**L-128**).
- **Pinned, not `getAnimations().finish()` — 2026-08-29.** Record `006` proposed the sweep. The pin
  was taken instead because every other geometry probe in the package already settles that way, and
  two settling regimes in one package are two answers to *what is at rest*. The cost is stated rather
  than hidden: `animation:none` gives the element's **base** style, which equals the `to` keyframe
  for an entrance that animates from a hidden state to its natural one and not otherwise.
- **The forced reflow was refused by the measurement — 2026-08-29.** The installer first ended with
  `document.documentElement.offsetHeight` to flush layout. The seeded-variant suite took `GF-6` from
  CAUGHT to MISSED, **7 of 7 to 6 of 7**, because the pin runs in every probe and reading layout
  before the fonts settle hands `GF-6` a baseline it is supposed to take later. It bought nothing
  either — the first `getBoundingClientRect` forces the same layout. Removed, and the suite is back
  to 7 of 7. **This is the second consecutive batch in which a remedy was measured and refused**
  (B1's two, [T-272](T-272-render-py-motion-enumerates-a-different-animation-set-across-runs.md)).
- **`currentDasharray` moved up beside the other motion facts — 2026-08-29.** A dasharray a keyframe
  animates reverts to its base value under the pin, and `DS-140`'s subject is the default state.
- **The new self-test fixture writes its markers literally — 2026-08-29.** Built by interpolating
  `MEASURES_MOTION` and `PINS_LOCALLY`, the fixture and `make_probe` move together and the case can
  never fail: seeded by renaming `PINS_LOCALLY`, it stayed green. A real probe writes the literal
  into its own source, so a fixture that writes one is the case rather than a shortcut past it.

**Outputs produced**
- [`tools/deck/render.py`](../tools/deck/render.py) — `PINS_LOCALLY`, `MOTION_PIN_FN`,
  `MOTION_PIN_CALL`, `make_probe`'s three-way choice, and a fourth pin fixture in `self_test`
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the probe's motion-facts-then-pin-then-geometry
  order, the corrected header comment, `out.noGeometry`, the `DS-035` row and its raw rows
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the `DS-035` row
- [`docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md`](../docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md)
  and [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) — closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy **measured**, or deferred with the reason | **met** | `006` closed — both its proposals taken, the first by a different mechanism with the reason recorded. `015` item 3 closed, **and what it does not claim is written into the record**: re-seeding that record's own shape on `examples/reference-deck.html` produced no degenerate CTM at all, 0 of 258 runs, so the branch is proved on a directly seeded static `scale(0)` and the `0.0 du` it observed is covered by the pin rather than shown to be the degenerate case |
| Each fix proved by seeding the defect and watching the check fire, **both directions** (**L-125**) | **met** | Four seeds. *Entrance* — `scaleY(0)`, `fill-mode:both`, delay unelapsed: `DS-035` 3 FAIL → pass, while `DS-218` keeps its subject in the same run. *Genuine small type* — 9px prose: `DS-035` FAIL at 23, so the rule keeps its force. *Degenerate* — static `scale(0)`: FAIL, `36` runs named `NO GEOMETRY` at `font-size 22.5px`. *The regression the split could cost* — `static_variants.py`'s `motion-stop-shut-inside-the-menu` still **CAUGHT**, suite at 29/29, 10/10, 1/1, 2/2, 7/7, 1/1 |
| The new guard proved red before it was trusted | **met** | Both directions: installer withheld, and the call injected anyway. The first was **green on its first attempt** and the fixture was rewritten — see §3 |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **met** | Run in that order, never concurrently ([`TOOLING.md`](TOOLING.md) §1) |

**Child fix tasks raised**
- none

**Lesson written**
- [L-139](../docs/lessons/L-139.md) — a measurement taken on one subject and written down as general is a claim nothing will re-check. This task's correction of T-209 is its instance; the lesson is the class, and [L-138](../docs/lessons/L-138.md) is the same failure along the other axis.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | review → done | **The split shipped and the measurement refused one part of it.** `audit.PROBE` reads its motion facts, pins, then measures geometry; `DS-035` counts a degenerate CTM apart from small type and prints the raw `font-size`. Four seeds, both directions, and `DS-218` keeps its subject in every one. **A forced reflow in the pin was written and then removed** — it took `GF-6` from 7 of 7 to 6 of 7 and bought nothing. Both adopter records closed, `015` item 3 **with what the remedy does not claim written into it**. `lint.py` green with the standing eleven and no twelfth; `check_all.py` green — 0 failures, 0 unclassified, 0 stale, 284 s, run after it and never beside it. |
| 2026-08-29 | → planned | **T-209's verdict re-derived before anything was changed**, and it does not generalise: identical both ways on its own deck, three keys apart on a deck whose entrance moves the axis. §2 carries the measurement. The remedy is the split the probe's own header comment already prescribed. |
| 2026-08-29 | (no change) | **Gained `DS-035`'s degenerate-CTM question**, deferred here by [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md) while B1 ran, with the reasoning in that task's §1. Two tasks amending one probe is the rework [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) exists to avoid, so this task now closes adopter record `015` item 3 as well as `006`. Nothing else about its scope moved. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
