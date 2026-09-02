---
id: T-267
title: Give render.py a capture path for a deck's disclosed states
type: fix
status: done
phase: specify
parent: null
blocked_by: []
related: [T-225]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-29
updated: 2026-08-30
shipped_in: unreleased
deliverables:
  - tools/deck/render.py
  - skills/htmldeck/references/build.md
  - docs/lessons/L-150.md
---

# T-267 — Give render.py a capture path for a deck's disclosed states

## 1. Specify

**Outcome**
A state that exists only after a click can be reviewed by picture. Today `measure`, `shots` and `motion` all capture a slide at rest, and the only element the tool ever presses is `#next` / `#prev`. **So the part of a deck that cannot be printed is also the part that cannot be reviewed by picture** — and the ninth gate condition is a person looking at it.

**From the adopter report** [`016`](../docs/adopter-reports/claimai/016-render-py-cannot-capture-a-decks-interactive-states.md).

**Scope**
- In: pressing a named control, hovering a named target, and opening a named quick view before the capture — each replaces one hand-built workaround with a flag
- In: **hit-testing: capture what is under a point.** It is the half neither workaround reaches and the question an author most wants a picture for
- Out: anything the records above do not name. The report is a closed one-way hand-over — there is no
  channel back and none is expected, so a question this task cannot answer is settled here rather
  than asked.

**Inputs**
- the record above, [`016`](../docs/adopter-reports/claimai/016-render-py-cannot-capture-a-decks-interactive-states.md) — each carries its evidence, its version and its own proposed fix
- the two workarounds the adopter found and their cost — roughly twenty minutes of setup per state, rebuilt from memory each time. **They are why this is a feature rather than a defect**
- what is left after both: no capture of a state *in motion*, because a pane that does not composite freezes a transition at its start value
- [T-260](T-260-ds-244-tests-proximity-where-it-means-obstruction.md) — hit-testing is what would close the gate's own blind spot to overlap

**Acceptance criteria**
- [ ] every record named above is **closed with its remedy measured**, or explicitly deferred with the
      reason recorded in this task
- [ ] each fix is proved by seeding the defect and watching the check fire, in both directions where
      the record's own evidence is a verdict (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Every record carries its own evidence and its own proposed fix; the proposal is a
  hypothesis and whoever implements it measures before committing to it. **Three of the report's
  premises were measured before planning** — see the Plan's step 0 — and one of them is wrong.

## 2. Plan

**Step 0 — measured first, 2026-08-30, before a line was designed.** A throwaway probe built through
`render.py`'s own `make_probe`, run against `examples/reference-deck.html` at 1600x1000. Three
premises, one refused:

| Premise, as the record states it | Measured | Consequence for the design |
| :--- | :--- | :--- |
| *hit-testing does not work* | **Refused.** `elementFromPoint` at `#next`'s centre returns `span.chev.r`, and `elementsFromPoint` returns the whole stack — `span.chev.r`, `button#next`, `div.navbox`, `nav.chrome`, `section.slide` | The record's sentence is about **the adopter's own non-compositing pane**, not about headless Chrome. Item 4 needs no new mechanism at all: it is a probe away, and it is the cheapest of the four rather than the one with no workaround |
| *un-setting `hidden` on `#moreMenu` still renders closed* | **Held**, and the cause is now named: the real control works. `#moreBtn.click()` moves `#moreMenu` from `hidden=true`, rect `0x0`, to `hidden=false`, rect `180x114` at `(1285,638)`, `display:flex`, `visibility:visible`, `opacity:1` | Item 1 is `el.click()` and nothing more. Pressing the deck's own control is also the only route that exercises what an audience triggers — the same argument `MOTION_PROBE` already makes for `#next` |
| *`:hover` needs the CSS edited to reach* | **Held.** `document.querySelectorAll(':hover')` returns `0` and does not throw; there is no DOM write that reaches the pseudo-class. But all 4 stylesheets read back with `cssRules` — `0` blocked — and **11 top-level `:hover` rules** are visible | Item 2 must rewrite CSS, which is workaround one automated. It is a **substituted trigger**, and the output has to say so on every run rather than let a picture imply a real pointer |

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add a `state` subcommand to `render.py`: drive one slide into a disclosed state, then report and optionally photograph it. Its probe declares neither `MEASURES_MOTION` nor `PINS_LOCALLY`, so `make_probe` pins motion off — a disclosed state is captured settled, which is what the other capture path already guarantees | `tools/deck/render.py` |
| 2 | Item 1 — `--click SEL`, repeatable and applied in order. Report per selector: found, and what the press changed (`hidden`, rect, `display`/`visibility`/`opacity`) | as above |
| 3 | Item 2 — `--hover SEL`. Walk every stylesheet, nested groups included, and re-insert each `:hover` rule with the pseudo-class swapped for `[data-htmldeck-hover]`; set that attribute on the target. Print the rule count and the words *substituted trigger* every run | as above |
| 4 | Item 3 — `--qv NAME`, pressing `[data-qv="NAME"]` and asserting `#qv` un-hides. A name the deck does not carry is refused with the names it does | as above |
| 5 | Item 4 — `--at X,Y` prints the stack under a point; `--probe SEL` takes an element's own centre and answers *reachable* or *covered by …*. This is the half with no workaround, and step 0 says it is a probe rather than a mechanism | as above |
| 6 | `--shot` writes the PNG, so items 1 to 3 become captures rather than reports. Uncalibrated, for `cmd_shots`'s stated reason | a PNG beside the other shots |
| 7 | Extend `self_test()` structurally, in the idiom T-206/T-209/T-261 established: assert the state probe is pinned by `make_probe`, and that the hover rewrite still names both the pseudo-class and its replacement. No browser | `tools/deck/render.py` |
| 8 | Seed each of the four in both directions (**L-125**): a control that opens versus one that does not, a hover rule present versus removed, a quick view named versus misnamed, a covered control versus a clear one | recorded in section 3 |
| 9 | Document the command where `render.py`'s other three are documented, and run `tools/docs/figures.py` before the gate — a new documented command moves a README count | the skill's documents |
| 10 | `python tools/tasks/lint.py`, then `python tools/check_all.py`, run separately | green |

## 3. Implement

**Decisions & assumptions**
- **`state` is a fourth subcommand, not flags on `shots`** - 2026-08-30. `shots` renders a list of
  slides at rest and takes a positional slide list; this drives ONE slide into a state and needs
  repeatable, ordered options. Bolting them together would give `shots` a mode where its positional
  argument means something else.
- **The probe declares neither motion marker, so `make_probe` pins motion off** - 2026-08-30. Same
  guarantee `shots` gets (T-209), and it matters more here: an unpinned capture freezes the
  transition that did the disclosing, which photographs a menu half-open and reads as a menu that
  renders wrong.
- **The result travels by `document.title`, guarded by `quiet`** - 2026-08-30. The first draft
  appended a result element to the body, which would have put a paragraph of JSON in every `--shot`.
  Proved fixed by measurement, not by reading: a no-op `state --shot` is **byte-identical** to
  `shots` of the same slide (sha256 `3991fdd14ec4aa0e`, 68,670 bytes), and the disclosed capture is
  250,047 bytes. Guarded in `self_test` so it cannot go quietly false.
- **`--hover` rewrites CSS and says so on every run** - 2026-08-30. It is the one item of four that
  does not use the deck's own trigger. The rules are re-inserted into **their own parent rule**
  rather than re-serialised into a new sheet, so a rule inside `@media`/`@supports` inherits its
  conditions instead of having them rebuilt by hand - a rebuilt condition that is subtly wrong
  applies the state under the wrong circumstances and looks exactly like a correct one.
- **`--probe` samples five points, not the centre** - 2026-08-30, and this was measured rather than
  assumed. Seeded a cover over the pager's lower third: the **centre stays clear** and 2 of 5 points
  are covered, so a centre-only hit test reports that control fully reachable.
- **`--qv` binds on `.sources-open`, never on `[data-qv]`** - 2026-08-30, **L-149**. The source
  `<template>` carries `data-qv` too, so the obvious selector presses a template.
- **Two blind spots were closed after the first run**, both found by running the thing rather than
  by reading it: a hover that only changes colour printed two identical lines - and so does a hover
  that never fired - and `--qv` pressed an opener nine slides away without saying so, because the
  deck's handler is delegated on `document`. The first added a deep computed-style read (`outline`
  included, which no other field can see); the second reports the opener's own slide.
- **One stale line fixed in place**, under `REMEDIATION-ORDER.md` §4: `build.md` told authors the
  `<slides>` argument was `0,4,6`, zero-based. It has counted from **one** since T-196.

**Outputs produced**
- [`../tools/deck/render.py`](../tools/deck/render.py) - the `state` subcommand, its probe, its
  report and four self-test guards
- [`../skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) - the command
  documented where the other five are, and T-196's stale line corrected
- [`../README.md`](../README.md) - `check_scaffold.py`'s documented-command figure, 19 -> 23
- [`../docs/lessons/L-150.md`](../docs/lessons/L-150.md) and its index row
- [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) - row 11

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| every record named above is closed with its remedy measured, or explicitly deferred with the reason recorded | **pass** | `016` closed. All four items built. **Its hit-testing premise was refused by measurement** and the item re-ranked from *no workaround at all* to the cheapest of the four - [L-150](../docs/lessons/L-150.md). Nothing deferred |
| each fix is proved by seeding the defect and watching the check fire, in both directions (**L-125**) | **pass** | Eight seeded pairs, all on throwaway copies of the reference deck. `--probe`: clear -> *reachable at all 5*; wholly covered -> *NOT REACHABLE*, naming `div#seeded-cover`; **centre clear, corners covered** -> *REACHABLE, but 2 of 5 covered*, which is the case a centre-only test passes. `--hover`: 11 rules -> the button's background, border and transform move; every `:hover` renamed away -> *this deck declares no `:hover` rule*; an element no rule reaches -> *nothing measured differs*, listing what was compared; **the only `:hover` rule nested inside `@media > @supports`** -> found and applied, `outline` and `filter` both move. `--qv`: a wrong name -> refused, listing the five the stage offers, exit 1; an opener on another slide -> reported by name. `--click`: `#moreBtn` -> `#moreMenu` `0x0` -> `230x146`. `--at` off-viewport -> refused. **The four self-test guards were seeded too**, and the marker guard was proved non-vacuous with a `pins-locally` seed the pin guard cannot see |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | **pass** | Run separately on a frozen tree, 2026-08-30. `lint.py`: all four checks, 4,956 document pointers, 0 broken. `check_all.py`: **0 failure(s), 0 unclassified, 0 stale** in 226 s — 39 commands ran, 2 skipped with their reasons printed, across 52 tracked tools. Neither result survives an edit; re-run rather than cite |

**Child fix tasks raised**
- none. Nothing found in code this task had to read.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-30 | look taken | The owed look is **discharged**: the owner opened `.assets-cache/deck/more-menu-open.png` and confirmed the menu is visible. Recorded in [`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 11, which also corrects a figure this task put there — it carried `measure-first`'s 250/69 KB quick-view pair on a row about a 230x146 menu on `reference-deck`. The right pair is **112 KB against 105 KB**, and the 7 KB margin is the argument for the look rather than against it. |
| 2026-08-30 | → done | All four items built and seeded in both directions. **The record's hit-testing premise was refused** and the item re-ranked — [L-150](../docs/lessons/L-150.md). Two blind spots the first run exposed were closed in place, and one stale `build.md` line fixed under §4. **One look owed** ([`../docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 11): no measurement here says the capture is a picture a reviewer can use. |
| 2026-08-30 | → planned | Step 0 measured the record's three premises before anything was designed. **Hit-testing was refused**: it works in headless Chrome, so the item the record calls *the half with no workaround* is the cheapest of the four. The other two held, and the `:hover` one fixes the shape of item 2 — a substituted trigger that must say so. |
| 2026-08-29 | → proposed | Raised by [T-225](T-225-triage-the-claimai-adopter-report.md), the triage of the ClaimAI adopter report. **`PH3`**: not a defect in the published plugin's behaviour, so `CLAUDE.md`'s rule puts it in the main line rather than reopening a shipped phase. |
