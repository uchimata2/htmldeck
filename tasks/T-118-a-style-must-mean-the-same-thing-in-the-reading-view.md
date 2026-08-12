---
id: T-118
title: A style that carries meaning on a slide must carry the same meaning in the reading view
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-070, T-109, T-115]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/DESIGN-SYSTEM.md
  - skills/htmldeck/references/critique.md
---

# T-118 — A style that carries meaning on a slide must carry the same meaning in the reading view

## 1. Specify

**Outcome**
A rule, and a critique step behind it: **a treatment that encodes something on the stage encodes the
same thing in the reading view, or it is not used.** Today nothing asks the question, and the reading
view is promised to be a *conforming alternate version* — DS-070 to DS-076 — which is exactly the
promise this breaks.

**The instance**
Slide 13 of the first adopting project's deck closes the argument, and its bottom line is centred —
`.bottom-line--center`, used once in the deck, on the closing slide. **On the stage that is a
deliberate gesture**: every other bottom line is left-anchored, so the last one centring reads as an
ending. In the reading view every section runs continuously down one column, and that same line
becomes **one centred paragraph among twelve left-aligned ones** — which reads as a mistake, not as
an ending, because the contrast it depended on is gone.

Nothing is broken. The deck validates, both renderings are correct, and the rule the treatment obeys
is satisfied in each. **What fails is the meaning, and only in the second rendering.**

**Why it is a rule and not a note about one slide**
The reading view is built by cloning slides ([`shell/deck.js`](../shell/deck.js) `buildDoc()`), so
**every** treatment crosses over automatically, and any treatment whose meaning comes from *contrast
with its neighbours* is at risk — a centred line among left ones, a colour used once, a size that is
large only relative to the slide it is on. The stage is twelve separate frames; the reading view is
one continuous column. Contrast that is local on the stage becomes global in the document.

**Scope**
- In: a rule in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md), at the altitude the ruleset uses for
  judgements — this is about meaning, and a program cannot decide it.
- In: a critique step that asks the question of any treatment used **once or rarely**, since rarity
  is what makes a treatment depend on contrast. That much *is* mechanical: a treatment's frequency is
  countable even where its meaning is not.
- In: the answer for `.bottom-line--center` specifically, either way. If the closing gesture is worth
  keeping, the reading view needs its own way to end; if not, the class goes.
- Out: **changing the reading view's construction.** Cloning is right and is what keeps the two from
  drifting (**L-08**); the question is which treatments survive the clone.
- Out: print. It is a third rendering with the same question, and it is out only because nothing has
  been found there yet — say so rather than implying it is exempt.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-070 to DS-076, the conforming-alternate
  promise this rule protects.
- [`shell/deck.js`](../shell/deck.js) — `buildDoc()`, and why every treatment crosses over.
- [`shell/components.css`](../shell/components.css) — `.bottom-line--center`, and the `.doc` block
  that already re-specifies some treatments for the reading view.
- [T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md) — same family: a
  claim that is true in one place and false in another, with nothing reading the two together.

**Acceptance criteria**
- [ ] A ruleset row exists, with the mechanism stated — local contrast becomes global in a continuous
      column.
- [ ] The critique pass reports treatments used once or rarely and asks the question of each.
- [ ] `.bottom-line--center` is decided, and the decision is recorded with its reason.
- [ ] Run against the adopting project's deck, the pass finds the centred bottom line. Regression case.
- [ ] False alarms counted against true hits on the two reference decks before the frequency check
      ships — a deck legitimately using a treatment once should not be nagged.

**Open questions**
- Whether print gets the same rule now or waits for an instance. Recommend waiting: a rule with no
  observed failure is a rule nobody can calibrate.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Count rarely-used treatments across both reference decks and the adopter's | the candidate set, and the false-alarm rate |
| 2 | Write the ruleset row | `DESIGN-SYSTEM.md` |
| 3 | Add the critique step | `critique.md` |
| 4 | Decide `.bottom-line--center` and record why | decision |
| 5 | Regression against the adopter's deck | the pass finds it |

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
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised by the owner from a finding made while looking at the reading view. Scoped around *rarity* rather than around alignment, because what makes a treatment fragile across the two renderings is that its meaning comes from contrast with its neighbours, and rarity is the countable half of that. |
