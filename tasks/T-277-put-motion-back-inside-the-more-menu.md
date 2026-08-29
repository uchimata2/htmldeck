---
id: T-277
title: Put Motion back inside the More menu, and let DS-218 count a persistent menu button as reachable
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-114, T-257, T-180]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-29
updated: 2026-08-29
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

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised at the owner's request, reversing §3's `T-257` ruling the same day it was made — *it must be a misunderstanding*, their words. **`PH3`**: this is a design change the owner asked for, not a defect an adopter met in the published `0.6.0`, so `CLAUDE.md`'s one condition for reopening `PH1` does not apply. **Placed first in `B11`** because both of the order's ordering rules point there: it amends a rule, so `T-244` cannot derive the gate's coverage account until it lands, and it changes the chrome tail every deck carries, so it must precede `B12`'s single rebuild. |
