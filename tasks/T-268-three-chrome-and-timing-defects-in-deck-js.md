---
id: T-268
title: Guard the single-letter shortcuts, dismiss the sources box, and land data-played on arrival
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-225]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-268 — Guard the single-letter shortcuts, dismiss the sources box, and land data-played on arrival

## 1. Specify

**Outcome**
The shell's chrome behaves the way its own comments say. Today **every browser chord built on one of six letters is captured** — Ctrl-R enters the reading view and cancels the reload, Ctrl-F goes fullscreen instead of opening find, and `grep -n "ctrlKey|metaKey|altKey" shell/deck.js` returns nothing; the **sources box does not dismiss on an outside click** though the More menu beside it does, with the More menu's own comment arguing the case; and **`data-played` lands at `t = 0` of the transition**, so an entrance gated on it — the gate `DS-146` tells authors to use — begins under the outgoing slide.

**From the adopter report** [`008`](../docs/adopter-reports/claimai/008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md), [`009`](../docs/adopter-reports/claimai/009-the-sources-box-does-not-dismiss-on-an-outside-click.md), [`010`](../docs/adopter-reports/claimai/010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md).

**Scope**
- In: the modifier guard, one line, with Shift deliberately excluded because the handler already accepts `R` as well as `r`
- In: the same three-line document listener for the sources root, keyed to `.sources` rather than to the button so the toggle does not close what the click just opened
- In: **a second attribute, `data-arrived`, rather than moving `data-played`** — the record's own safer option, because nothing already in the field changes behaviour
- In: the rule rows: the keyboard section saying the shortcuts are unmodified only, and `DS-146` saying *when* `data-played` lands
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the records above, [`008`](../docs/adopter-reports/claimai/008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md), [`009`](../docs/adopter-reports/claimai/009-the-sources-box-does-not-dismiss-on-an-outside-click.md), [`010`](../docs/adopter-reports/claimai/010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md) — each carries its evidence, its version and its own proposed fix
- all three were reported by the presenter using the deck, which is the one instrument this repository cannot run
- `010`'s own note that the reviewer's original report was the **deck's** defect and not htmldeck's; what is left is the narrower thing underneath

**Acceptance criteria**
- [x] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [x] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [x] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None yet. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | The modifier guard, one line, Shift excluded | `shell/deck.js` |
| 2 | The document listener for the sources root, keyed to `.sources` | `shell/deck.js` |
| 3 | `data-arrived` as a second attribute, `data-played` untouched | `shell/deck.js` |
| 4 | **Prove all three in a real browser on a real deck**, both directions each — they are behaviours, and no static check can see one | the probe |
| 5 | The rule rows: `DS-131` on unmodified shortcuts, `DS-146` on when each mark lands | `docs/DESIGN-SYSTEM.md` |
| 6 | Close the three adopter records | `docs/adopter-reports/claimai/008…`, `009…`, `010…` |

## 3. Implement

**Decisions & assumptions**

- **Shift is not in the guard — 2026-08-29.** `Ctrl`, `Meta` and `Alt` are the three that build a
  browser chord. The handler accepts `R` as well as `r`, so Shift is already part of how these
  shortcuts are typed, and guarding on it would break the capital form of all six.
- **The sources listener is keyed to `.sources`, not to `.sources-btn` — 2026-08-29.** The button's
  own handler runs first and opens the box; a listener sparing only the button would then read the
  same click as outside and shut what it had just opened. This is the More menu's rule applied to
  the component beside it, and that menu's own comment already argues the case.
- **`data-arrived` waits on the OUTGOING slide, and that is the whole of the fix — 2026-08-29, and
  it was got wrong first.** The first implementation asked the *arriving* slide what it was running.
  Measured on a built deck: **0**. Every transition rule in `components.css` is keyed to
  `[data-leaving]`, and `.slide[data-current]` only sets `opacity` and `visibility` — the arriving
  slide animates nothing. So that version marked arrival at t = 0 and was `data-played` under a
  second name, which is the defect wearing the fix's clothes.
- **And the second implementation lost a race this file creates.** Waiting on
  `Animation.finished` never resolved: the deck's own `animationend` listener removes
  `data-leaving` the moment the animation ends, which unmatches the CSS rule and **cancels** the
  animation — and a cancelled animation rejects `finished`. Measured: `data-arrived` never landed
  at all. It now lands from that same `animationend`, which is the signal without the race.
- **`data-played` is unchanged**, which is report `010`'s own safer option: decks in the field gate
  on it, and a second attribute changes nothing that does not ask for it.

**A limit of the measurement, stated.** Under `--virtual-time-budget` the harness advances **timers**
and not the frame clock, so a 420 ms CSS animation is still `running` after a 1500 ms `setTimeout`
and `animationend` never fires — measured, and the reason the probe calls `finish()` on the leaving
slide instead of sleeping. Finishing the animation *is* the event under test. **What is not measured
is the wall-clock delay**, and nothing in this repository can measure that without a person.

**Outputs produced**
- [`shell/deck.js`](../shell/deck.js) — the modifier guard, the sources dismissal, `arrived`,
  `land`, `markArrived`, and one line in the `animationend` listener
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — `DS-131` and `DS-146`
- the three adopter records, closed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every record closed with its remedy measured | pass | `008`, `009` and `010`. `010`'s remedy was taken in its own safer form; the other two as proposed |
| Each fix proved by seeding the defect and watching the check fire, in both directions (**L-125**) | pass | A browser probe on a deck built from the edited shell, **twelve assertions, all passing**: Ctrl-R and Ctrl-F neither prevented nor acted, bare `r` still enters and leaves the reading view; the sources box survives the click that opens it and closes on a click outside; `data-played` still lands at t = 0, `data-arrived` is absent while the slide is arriving and present once the outgoing slide has gone. Two earlier implementations were **refused by this probe** before the third passed |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Recorded in the batch's closing run, with B9's expected shell drift named |

**A look is owed: no.** Three behaviours, all measured in a browser rather than judged by eye, and
nothing any deck renders differs at rest. What a person would add is the wall-clock feel of the
entrance, which is the limit stated above rather than a queued row.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | Landed in **B9**. All three fixes are in `shell/deck.js` and all three are proved by a browser probe rather than by the diff. **Two implementations of `data-arrived` were refused by that probe before the third passed**: the first asked the arriving slide what it was running, and the answer is 0 because every transition rule is keyed to `[data-leaving]`; the second waited on `Animation.finished`, which the deck's own `animationend` cleanup cancels. It lands from that listener now. `data-played` is unchanged, which is report `010`'s own safer option. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH1`**: a defect an adopter met in the published `0.6.0`, which is `CLAUDE.md`'s one condition for reopening the phase. Verified against this tree before the record was actioned — the report's `Version seen` was stamped rather than re-run on fourteen of the twenty-seven. |
