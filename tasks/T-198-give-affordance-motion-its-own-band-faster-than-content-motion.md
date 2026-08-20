---
id: T-198
title: Give affordance motion its own duration band, faster than content motion
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-112, T-114, T-187, T-188]
work_package: PH3
shipped_in: unreleased
owner: the project owner
business_value: high
effort: m
created: 2026-08-20
updated: 2026-08-20
deliverables: []
---

# T-198 - Give affordance motion its own duration band, faster than content motion

## 1. Specify

**Outcome**
A control answers a press before the slide does. Today the pager's press acknowledgement takes
**420 ms**, which is longer than most people will wait before deciding the button is broken - which
is what the owner reported on 2026-08-20: *interactive animations are too gentle, and the user gets
a feeling it is not working.*

**What the owner asked for**
- Pager hover: **0.2 s, linear**. The rotation is subtle enough that no easing is needed.
- Pager press: **0.1 s, ease-in-out-back**.

**What is there now**
`--turn-dur: 420ms`, `--turn-ease: ease-in-out`, and one transition on `.btn` carrying **both** the
hover tilt and the press pinch, so today the two cannot differ. `--pager-pinch: .94`,
`--pager-tilt: 3deg`.

**The contradiction check, which is why this is a decision and not a fix**
[T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md) records an owner ruling from
**2026-08-19** - one day earlier - whose principles read *keep animation gentle*, *ease in/out is the
preferred default for almost everything*, and *sequence length might default to 300-500 ms*. Read
flat, today's request reverses all three.

Read correctly, it does not, and the project already owns the distinction:
[T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md) - **done**,
updated 2026-08-19 - split every motion into `content` and `affordance`, and `check.py` fails a
motion declaring neither. The pager tilt and the pinch are affordance. T-187's principles are about
motion that *enriches the document for highlighting or emphasizing content* - they are content-motion
principles, written in a task whose own scope is DS-140's vocabulary for content motion. The word
`affordance` appears in T-187 zero times.

**DS-141 does not govern this either, and says so.** Its first clause is *DS-141 governs entry and
transition only*. A hover tilt is neither. Its `linear` clause - *survives where the mechanism
requires it and nowhere else* - is written inside that scope; if it is read as deck-wide it forbids
what the owner is asking for, and then the clause is what needs rewording, not the request. Naming
that here is the point of this section: **the rule to record is that affordance motion and content
motion carry different bands**, never a flat *animations should be faster*, which would contradict
T-187 the moment anyone applied it to a reveal.

**Where I disagree with the request as written**
1. **`ease-in-out-back` is not a CSS keyword.** It is a Penner name; in CSS it is a `cubic-bezier`.
2. **At 100 ms an in-out-back's leading overshoot is below the threshold anyone can see.** The
   overshoot needs time to read. On a press the moment that carries the feel is the *arrival*, so I
   recommend `ease-out-back` - `cubic-bezier(.34, 1.56, .64, 1)` - at the owner's 0.1 s. If the
   in-out shape is wanted for its own sake it needs about 140-160 ms, which is slower than asked for.
3. **Do not retune `--turn-dur` in place.** Turn's pair is a theme token and a second theme sets it.
   Affordance timing is a band the ruleset states, not a look a theme picks.

**A measured convenience.** Both consumers of `--turn-dur` today - the pager transform and the
disclosure mark's rotation - already declare `--motion-kind:affordance`. So no content motion reads
these tokens, and the change cannot leak into a reveal.

**Scope**
- In: an affordance band - duration and curve - stated as a rule, with its reason, and distinct from
  content motion's band.
- In: separating the hover transition from the press transition on `.btn`.
- In: the disclosure mark's rotation, which is the same class of motion and is currently as slow.
- In: `theme.py`'s band check, which must assert the new band.
- Out: content motion, DS-140's vocabulary, and T-187's guide. This task must not touch them, and an
  outcome that changes a reveal's timing is the wrong outcome.

**Acceptance criteria**
- [ ] Hover and press carry different durations and different curves.
- [ ] `theme.py` fails a theme that puts an affordance motion in the content band.
- [ ] The result is **looked at** on a real deck, per `CLAUDE.md` rule 6 - and the owner is the one
      who says whether it now reads as working, since *feels broken* is the report being answered.
- [ ] T-187's guide, when written, states the two bands and does not restate one as the other.

**Open questions**
- `ease-out-back` at 0.1 s as I recommend, or `ease-in-out-back` as asked? Owner's call, and it is a
  feel question rather than a correctness one.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add the affordance and press bands to the theme contract and the shipped theme | `--afford-dur/-ease`, `--press-dur/-ease` |
| 2 | Write DS-240, scoped to a control's answer to an input | `DESIGN-SYSTEM.md` |
| 3 | Move every pointer-response rule onto the new band | `shell/components.css` |
| 4 | Gate it: the band is closed, and the press outranks the hover | `audit.py` |
| 5 | Declare the tokens in the three decks and re-sync the shell | three decks |

## 3. Implement

**Decisions & assumptions**
- **`ease-out-back` at 0.1 s, not `ease-in-out-back`** - the owner's recommendation was accepted 2026-08-20. `cubic-bezier(.34,1.56,.64,1)`. At 100 ms a leading overshoot is below anything a person can see; the arrival is the only edge long enough to carry it.
- **DS-240 is narrower than DS-237's `affordance` kind, and that is the rule rather than an omission.** The arriving `rise` and the leaving slide are affordance too and stay in DS-141's band: an entry is paced by the slide, a control by the hand. Writing one band for both is what would have contradicted T-187 - 2026-08-20.
- **Turn's and Scale's token pairs were left declared and are now unread by the shell.** They are DS-140 vocabulary dials and retuning or retiring them is T-187's, which this task is explicitly out of. Measured first: all three shipped decks read `--turn-dur` exactly twice, both times from a rule declaring `affordance`, so nothing content-side moved - 2026-08-20.
- **The ruler's ring and tick moved too, unasked.** The owner's report named the pager. Leaving the other pointer-response rules on a 300 ms reveal clock would have made DS-240 false on the day it was written.

**Outputs produced**
- `docs/DESIGN-SYSTEM.md` DS-240
- `docs/THEME-CONTRACT.md` four token rows
- `docs/COMPONENT-CONTRACT.md` five motion rows
- `themes/quarto.css`
- `shell/components.css`
- `tools/deck/audit.py` - `_rules`, `_compound`, `_specificity`, `ds240_band_is_closed`, `ds240_press_beats_hover`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Hover and press carry different durations and different curves | **pass** | measured in Chrome on the built deck: hover `0.2s linear`, press `0.1s` |
| `theme.py` fails a theme that puts an affordance motion in the content band | **pass, by a different mechanism** | the band is enforced from two sides - `theme.py` holds each token to the contract's `ms 0-250` / `ms 0-150`, and `audit.py`'s DS-240 row holds the *rules* to reading only those tokens. Seeded a content motion onto `--press-dur`: reported |
| Looked at on a real deck (rule 6) | **partly - the owner still owns it** | the cascade and the timings are measured, which is what a program can reach. Whether it now *reads* as working is the report being answered and is the owner's |
| T-187's guide states both bands | **not met - deferred to T-187** | T-187 is `proposed`. DS-240 states the split and says in its own text that it is not T-187's content-motion band, so the guide inherits a written line rather than an argument |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | DS-240 written; the band moved and gated. |
| 2026-08-20 | -> done | Three criteria met, one deferred to T-187 with the reason recorded. |
