---
id: T-277
title: Put Motion back inside the More menu, and let DS-218 count a persistent menu button as reachable
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-114, T-257, T-180]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
shipped_in: 0.7.0
deliverables: []
---

# T-277 — Put Motion back inside the More menu, and let DS-218 count a persistent menu button as reachable

## 1. Specify

**Outcome**
*Motion* sits inside `.more-menu` on every deck, looping or not. `DS-218`'s **trigger** is unchanged
— motion that loops, or runs over 5 s, still ships with a persistent, keyboard-operable stop, and
the deck still reads with motion off — and its **placement clause** is what gives way: a control one
click inside a menu button that is itself persistent and keyboard-reachable counts as reachable.
The conditional placement `T-114` built goes with it, so the chrome tail has one form again.

**Where this came from.** The owner asked for it directly on 2026-08-29, having noticed the control
had moved out of the menu at some point and wanting it back. **It reverses one of §3's eight
rulings** — [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3, `B13`/`T-257`, *is a control
one click inside a shut menu genuinely disqualifying?*, answered **yes, keep the rule** earlier the
same day. The owner's word on the reversal: it was a misunderstanding of what the question was
asking — they read it as being about the example deck rather than about where the control lives.
**A ruling is reversible on the owner's word, and this is that**, recorded on the row rather than
rewritten out of it.

**What moved it in the first place**, for whoever implements this and wonders whether the reason
still applies: [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) step 7a, on
2026-08-18. Putting a `More` menu on the chrome row created the first way to satisfy `DS-218` in the
letter and break it in fact, so the rule gained *a looping deck's control must not sit inside
`.more-menu`*, and `CHROME_TAIL` became a slot carrying a **varying parent** rather than varying
content. **The hazard T-114 named is real and is not being denied** — a stop behind a click is worse
than one in the open. What the reversal decides is that it is not *disqualifying*, because WCAG
2.2.2 asks that the stop be reachable while the motion runs, not that it be zero clicks, and the
menu button satisfies that.

**Scope**
- In: `DS-218`'s row — the placement clause replaced with the reachability condition, under `DS-000`
  with the stated reason, **marked reversible**, and the §3 reversal cited
- In: [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.4, which makes the position a
  build-time fact and says explicitly that a control inside a shut menu is not persistent — that
  sentence is now wrong and is the one an author reads
- In: `shell/shell.html`'s `CHROME_TAIL` comment, which states the conditional rule in prose
- In: `tools/deck/shell.py` — `tail <deck> --loops|--still` and `new`; whether the two forms
  collapse to one is the implementer's call, but a flag that selects between identical forms is
  worse than no flag
- In: `tools/deck/audit.py` — `motionPersistent` currently fails a looping deck whose control is in
  the menu. It should instead decide **the condition the rule now states**: the control exists, and
  the button that opens it is persistent and keyboard-operable. **A check that decides nothing is
  not the fix** — if the new condition is true by construction on every deck the shell builds, say
  so and reach for the population, not the firing rate ([L-144](../docs/lessons/L-144.md))
- In: the four tracked decks, re-tailed and re-synced
- Out: `DS-218`'s trigger, the reduced-motion rule `DS-143`, and print collapse `DS-224`. None of
  them is in question
- Out: `T-257`'s own fix. Giving `portfolio-review` a looping motion so it passes for a reason is
  still owed and is now **independent** of this question — it was the example's defect, not the
  rule's

**Inputs**
- [`REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §3, the reversed ruling row, and §2's `B11`
- [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) — option **Y**, step 7a, and
  the reasoning for the slot being a region rather than a control
- [T-257](T-257-ds-218-passes-the-shipped-example-vacuously.md) — its third scope bullet asked
  exactly this question and can now cite the answer
- [T-180](T-180-seed-ds-218s-failing-branch-so-the-persistent-control-check-is-watched-failing.md) —
  the seeded failing branch for this check, which has to be re-seeded against the new condition or
  it is watching a branch that can no longer fire

**Acceptance criteria**
- [ ] every tracked deck carries *Motion* inside `.more-menu`, and `audit.py` passes each **for a
      stated reason** rather than by no longer looking
- [ ] `DS-218` and `COMPONENT-CONTRACT.md` §3.4 agree with the built markup and with each other; no
      document still says a control inside the menu is not persistent
- [ ] the check is **watched failing** on a seeded deck whose menu button is absent or not
      keyboard-reachable, and passing on the shipped ones (**L-125**), with `T-180`'s fixture
      updated rather than left pointing at the old branch
- [ ] the population the new condition would exempt is measured and recorded here, so a condition
      true on every deck by construction is caught before it ships ([L-144](../docs/lessons/L-144.md))
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- **Does the menu need to open on keyboard focus, or is click-to-open enough?** Not settled here.
  The rule's new condition says the *button* is keyboard-operable, which the shell already
  satisfies; whether the menu should also open on `Enter` without a pointer is a question for
  whoever measures it against the built markup. Decide it from the rule's own reason and record the
  decision rather than handing it back.

## 2. Plan

**The shape of it.** The reversal collapses a two-form slot back to one form, so most of the work is
deletion: two tail constants become one, a flag that would select between identical forms goes, and
three documents that describe the conditional stop describing it. What is *not* deletion is the
check — `motionPersistent` must decide the condition the rule now states rather than be removed,
which is the acceptance criterion `audit.py` passes **for a stated reason**.

**The measurement comes before the check is written** (L-144), not after, because if the new
condition holds on every deck by construction then what gets written is a report and a
recommendation rather than a guard.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the population the new condition would exempt, on all five built decks and on the shell: does `#moreBtn` exist, is it a real `button`, is it rendered, is it keyboard-reachable? Record the count in §3 before touching the check | the figure L-144 asks for, and the decision on whether step 5 is a guard or a report |
| 2 | `tools/deck/shell.py` — collapse `CHROME_TAIL_MENU` and `CHROME_TAIL_LOOPING` into one `CHROME_TAIL`; `tail(html)` loses its `looping` argument; the CLI's `--loops`/`--still` pair goes and `tail <deck> [--write]` normalises. `MIGRATIONS` and `new()` follow the single constant | one tail form; the command still exists, because three decks carry the old form and need moving back |
| 3 | `shell/shell.html` and `shell/README.md` — the `CHROME_TAIL` comment and the slot's description stop stating the conditional rule | prose matching the one form |
| 4 | `docs/DESIGN-SYSTEM.md` `DS-218` — the placement clause replaced by the reachability condition, under `DS-000`, **marked reversible**, citing §3's reversal. The trigger is untouched | the rule an author reads |
| 5 | `tools/deck/audit.py` — `motionPersistent` decides *the control exists, and if it sits inside a collapsed container, the button that opens that container is persistent and keyboard-operable*. Probe reads it off the built markup as before | a check bound to the rule's new words |
| 6 | `docs/COMPONENT-CONTRACT.md` §3.4 — the *Where `Motion` sits* paragraph rewritten: one build-time position, inside `.more-menu`. The sentence saying a control inside a shut menu is not persistent is the one that must go | no document contradicting the rule |
| 7 | `tools/deck/static_variants.py` — `T-180`'s variant re-seeded against the **new** condition: the old edit moves a button that is now where it belongs, so it can no longer fail. The replacement breaks the opener instead | the check watched failing (L-125) |
| 8 | Re-tail the four tracked decks, then `TOOLING.md` §1.14's four commands in order | decks carrying the one form, gates re-derivable |
| 9 | Both gates, run separately | `lint.py` and `check_all.py` green |

**Ordering that is not arbitrary.** Step 1 precedes step 5 for L-144's reason. Step 2 precedes step 8
because the decks are re-tailed by the tool this task changes. Step 7 follows step 5 because a
variant is seeded against the check as it will be, not as it was.

**The open question is decided in step 5 and recorded in §3**, not handed back: whether the menu must
open on keyboard focus. The rule's new condition names the *button*, so the test is whether the
button can be operated from the keyboard — `Enter` on a focused `<button>` fires its click. Opening
on focus without a press is a different interaction and DS-163 already rules against hover-open.

## 3. Implement

**Decisions & assumptions**

- **The population is 5 of 5, and the condition is still a guard** — 2026-08-29. L-144 asks for the
  population before the guard is written, so it was measured first, over every built deck this
  repository tracks: the opener is a persistent, keyboard-operable `<button>` on **5 of 5**. That is
  L-144's shape exactly, and it is **not** L-144's verdict, because point 3 is the discriminating
  test and it comes out the other way. DS-100's guard was mandated by two documents this project
  already owned; **nothing mandates this one.** `COMPONENT-CONTRACT.md` §3.4's table binds `.btn` to
  `.chrome` as `1+` and names no opener, and `PR-78` **measured** what a tail missing one of these
  buttons does — the deck reports `data-preflight="fail"` and renders 0 of 13 slides — while
  `shell.py check` and `component.py check` both pass it. A condition true today that nothing else
  guards is a guard; one another document mandates is not. Implemented as ruled.
- **The two tail forms collapsed rather than staying behind a flag** — 2026-08-29, as §1 left to the
  implementer. A flag selecting between identical forms is worse than no flag, so `CHROME_TAIL_MENU`
  and `CHROME_TAIL_LOOPING` became one `CHROME_TAIL` and `tail()` lost its `looping` argument.
  **`--loops` and `--still` are refused with a message rather than ignored**: a script still passing
  one is asking for a placement this tool no longer decides, and silently doing the right thing
  would leave it asking.
- **The `CHROME_TAIL` slot survives, for a different reason than the one that created it** —
  2026-08-29. T-114 made it a region because the control's *parent* varied, and that reason is gone.
  It stays because a deck may reword `More`, `Read` and `Motion`, so it is the one region
  `shell.py check`'s byte comparison must not own — which was T-114's stated cost and is now the
  whole justification.
- **The open question is decided: click-to-open is enough** — 2026-08-29. The rule's new condition
  names the *button*, and the test is whether that button can be operated from the keyboard.
  Measured on the built reference deck in Chrome: `#moreBtn` is a `BUTTON` with `tabIndex` 0, takes
  focus, and activating it flips `#moreMenu`'s `hidden` from `true` to `false`. Opening on focus
  without a press is a different interaction, and DS-163 already rules against hover-open.
- **The check reports the reason it passed, not just `True`** — 2026-08-29. A boolean over a
  condition nothing else guards is the shape L-144 warns about, so the probe emits `motionReach` and
  the DS-218 row prints it: *one click inside #moreMenu, opened by a persistent keyboard-operable
  button*. That is the acceptance criterion's *for a stated reason*, and it is checkable by eye.
- **The probe finds the opener by `aria-controls`, not by `#moreBtn`** — 2026-08-29. The rule is
  about a menu button, not about this shell's ids, and a check hard-coded to one id would pass a
  deck that renamed it. It walks `#motion` → nearest `[hidden]`/`[aria-hidden]` ancestor → whatever
  declares `aria-controls` for it, and reports which step failed.
- **`T-180`'s fixture was re-seeded rather than left pointing at the old branch** — 2026-08-29. Its
  edit moved the control into the menu, which this task makes a **passing** deck, so it would have
  gone on running and caught nothing: L-145's failure one batch on. It now sets `tabindex="-1"` on
  the opener. **`tabindex` rather than deleting the button**, because deleting it also moves
  `component.py`'s counts and triggers `PR-78`'s preflight crash, and a variant failing three ways
  proves nothing about which rule was watching. Measured: **CAUGHT, with `DS-218` the only rule
  failing** — `control reachable while motion runs: False - opener is not keyboard-operable`.
- **`PUBLISHING.md`'s `0.4.0` upgrade row lost its third command rather than having it corrected** —
  2026-08-29. It told an adopter to run `shell.py tail <deck> --loops --write`, which now exits with
  an error. The account of what `0.4.0` tightened is left standing, because what a release did is a
  fact; the *step* is dropped, because the migration's own result satisfies DS-218 now.
- **Two tool comments carried the old fixture's description into a dated measurement**
  (`audit.py`'s `PROBE`, `render.py`'s pin note) — 2026-08-29. T-209's reading is real and is kept;
  what the variant seeds is stated in the past tense beside it, because the mechanism the reading
  demonstrates is unchanged and only the fixture moved.

**Outputs produced**
- [`tools/deck/shell.py`](../tools/deck/shell.py) — one `CHROME_TAIL`, `tail(html)`, the flags
  refused, `new()`, `migrate()` and the slot table
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the DS-218 probe walks to the opener;
  `motionReach` added and printed in the verdict
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `T-180`'s variant re-seeded
  as `motion-stop-behind-an-unreachable-opener`
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — `DS-218`'s placement clause replaced, the
  reversal and the population recorded, reversible under `DS-000`
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.4 — one build-time position
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) — the `0.4.0` upgrade row's third command
- [`shell/shell.html`](../shell/shell.html), [`shell/README.md`](../shell/README.md) — the slot's prose
- [`tools/deck/render.py`](../tools/deck/render.py) — the stale fixture description in the pin note
- the four tracked decks, re-tailed and synced; the seeded fixture regenerated; five document
  figures re-derived across `examples/README.md`, `docs/BRIEF.md` and `README.md`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every tracked deck carries *Motion* inside `.more-menu`, and `audit.py` passes each for a stated reason | pass | 4 of 4 re-tailed and synced; the fifth built file, the seeded fixture, regenerated from the reference deck. The DS-218 row now prints its reason: *one click inside #moreMenu, opened by a persistent keyboard-operable button* |
| `DS-218` and `COMPONENT-CONTRACT.md` §3.4 agree with the built markup and with each other; no document still says a control inside the menu is not persistent | pass | Both rewritten. A sweep for the clause found three more statements outside the scope §1 listed — `PUBLISHING.md`'s `0.4.0` upgrade row, whose third command no longer exists, and dated comments in `audit.py` and `render.py` — and all three are corrected. `shell/README.md` and `shell/shell.html` with them |
| The check is watched failing on a seeded deck whose menu button is absent or not keyboard-reachable, and passing on the shipped ones (**L-125**), with `T-180`'s fixture updated | pass | `motion-stop-behind-an-unreachable-opener` → **CAUGHT**, and `DS-218` is the only rule failing on it, so the catch is this rule's own the way T-180 required. The old variant is replaced, not left running |
| The population the new condition would exempt is measured and recorded here (**L-144**) | pass | **5 of 5**, recorded in §3 with the reason it is still a guard rather than an off switch: no other contract mandates the opener, and `PR-78` measured what its absence does |
| `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately | pass | Run separately, never concurrently. Outcomes in the log row below |

**A look is owed and is written down**, [`OWED-LOOKS.md`](../docs/OWED-LOOKS.md) row 1. It was looked
at during implementation — the menu opens upward carrying `Read` and `Motion on` as two rows, clear
of the chrome and the bottom line — and the row still stands, because *does the chrome row balance*
is the judgement T-114 was raised over and the owner has reversed once.

**Child fix tasks raised**
- none

**Lesson kept beyond this task** - [L-146](../docs/lessons/L-146.md).
L-144 gave the alarm and not the verdict: a population of all-of-them is the signal to look, and
what decides an off switch from a guard is whether another contract mandates the condition.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | (no change) | **The owed look came back the same day, and it passed.** The owner opened the menu: *exactly how I wanted, perfect like this* - both questions answered, the two-row menu and the row's balance with only `More` outside the navigation box. **They ruled the wider point with it: *this is not an exception, it should be like this*** - so the menu placement is the norm `DS-218` states rather than a tolerance it extends, which is recorded on the rule's own row. `OWED-LOOKS.md` row 5; the queue is empty again. |
| 2026-08-29 | → done | Implemented as ruled. The L-144 population came back **5 of 5** and the clause was kept anyway, because no other contract mandates the opener and `PR-78` measured that its absence ships a deck that will not start - written up as `L-146`. Two tail forms collapsed to one, `--loops`/`--still` refused rather than ignored, and `T-180`'s variant re-seeded on the opener: **CAUGHT, `DS-218` the only rule failing**. The sweep found three statements of the reversed clause outside the scope `§1` listed, `PUBLISHING.md`'s broken upgrade command among them. **Both gates green, run separately** - `lint.py` all four checks, `check_all.py` 0 failures with 35 ran and 2 skipped with reasons, 272 s. A look is owed and written to `OWED-LOOKS.md` row 1. |
| 2026-08-29 | → proposed | Raised at the owner's request, reversing §3's `T-257` ruling the same day it was made — *it must be a misunderstanding*, their words. **`PH3`**: this is a design change the owner asked for, not a defect an adopter met in the published `0.6.0`, so `CLAUDE.md`'s one condition for reopening `PH1` does not apply. **Placed first in `B11`** because both of the order's ordering rules point there: it amends a rule, so `T-244` cannot derive the gate's coverage account until it lands, and it changes the chrome tail every deck carries, so it must precede `B12`'s single rebuild. |
