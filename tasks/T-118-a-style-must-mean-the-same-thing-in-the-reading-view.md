---
id: T-118
title: A style that carries meaning on a slide must carry the same meaning in the reading view
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-070, T-109, T-115]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-13
updated: 2026-08-18
shipped_in: unreleased
deliverables:
  - docs/DESIGN-SYSTEM.md
  - skills/htmldeck/references/critique.md
  - shell/components.css
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

**Step 1's answer: the candidate set, and the false-alarm rate**
Measured 2026-08-18 over the three shipped decks. A *treatment* is a modifier class
(`block--modifier`), because that is what a deck applies to say **this one is different**; a base
class is the component and says nothing by contrast.

| | reference-deck | sort-window | measure-first | total |
| :--- | ---: | ---: | ---: | ---: |
| slides | 13 | 12 | 13 | 38 |
| modifier classes | 3 | 2 | 4 | 9 |
| used on one slide | 2 | 1 | 3 | **6** |
| …of those, contrast **across** slides | 1 | 1 | 1 | **3** |

**Rarity alone was not good enough, and the second test costs nothing.** Six rare treatments split
exactly three/three. The three kept are all `bottom-line--center`, one per deck. The three dropped —
`disc--edge`, `listi--out`, `sources--list` — contrast with siblings **on their own slide**, and
`buildDoc()` clones the slide whole, so those neighbours travel with them. The discriminator is
countable: a modifier whose base component appears at most twice per slide is borrowing meaning from
the *other* slides. **False alarms after it: zero.** That is criterion 5, answered with a number
rather than an impression.

*The first run of the counter reported nine, including `btn--pager` in all three decks. Slicing each
slide from its own start to the next slide's start swept the chrome row into the last one, so a
**control** was being reported as a rare treatment. The artifact was in the instrument; slides are
cut at their own `</section>` now.*

**Decisions & assumptions**
- **`.bottom-line--center` is kept on the stage and reverted in the reading view** — 2026-08-18.
  Alignment carries no information, and DS-070–076 promise a *conforming alternate*, not an
  identical one: the document ends by ending, and it does not need to reproduce a stage gesture. All
  three decks use the class exactly once, on their closing slide, so it is the shell's idiom rather
  than one deck's habit and deleting it would cost every deck its ending.
- **The rule's home is the shared shell, and that is the finding this task did not expect** —
  2026-08-18. `reference-deck` and `sort-window` **already carried a hand-copied per-deck
  `.doc .bottom-line--center` override**, in a per-deck region; `shell/components.css` had none, and
  `measure-first` had no reading-view bottom-line styling at all. So the fix existed twice by hand
  and was missing from the third deck — **which is exactly why the defect was observed on the
  adopter's deck and nowhere else**. The rule now lives once, in the shell, and the two per-deck
  copies are deleted (**L-08**: a stored copy of a derivable fact drifts). Had they been left, a
  later change to the shell's rule would have been silently overridden in two decks.
- **Print waits for an instance**, as §1 recommended — 2026-08-18. A rule with no observed failure
  cannot be calibrated, and DS-233 says what to look for if one turns up.
- **DS-233 is `hard` / `judge` / `—`.** Same shape as DS-021: the meaning is a person's call, so no
  gate may imply it decides this. It joins the hard-judge checklist, 26 → 27.

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-233, in §2.5 *The reflow view*.
- [`skills/htmldeck/references/critique.md`](../skills/htmldeck/references/critique.md) — the
  fourth by-hand test in §4, with the two-step count.
- [`shell/components.css`](../shell/components.css) — `.doc .bottom-line--center`, one home.
- The three shipped decks, re-synced; the seeded-defects deck regenerated (**L-77**); and the
  figures a shell sync always moves — `README.md`, `docs/BRIEF.md`, `examples/README.md`.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A ruleset row exists, with the mechanism stated | met | DS-233. The mechanism is the row's first sentence: `buildDoc()` clones every slide, so local contrast becomes global |
| The critique pass reports treatments used once or rarely and asks the question of each | met | `critique.md` §4, and it carries the second test — without it the pass would raise three false alarms out of six |
| `.bottom-line--center` is decided, and the decision is recorded with its reason | met | Kept on the stage, reverted in the document; §3 has the reason and what it would have cost to delete instead |
| Run against the adopting project's deck, the pass finds the centred bottom line. Regression case | met | `measure-first` is that deck. The pass flags one treatment on it, and it is the right one |
| False alarms counted against true hits on the two reference decks before the frequency check ships | met | 6 rare, 3 true, 3 false on rarity alone; **0 false** once the second test is applied. Counted before the step was written, not after |

**Looked at, offline** — `CLAUDE.md` rule 6, `TASK-WORKFLOW.md` §7 step 3. The adopter's deck, before
and after, in a pane that runs page script: the reading view opened through the deck's own `toDoc`
control, scrolled to the closing section. **Before**: 13 bottom lines, twelve computing `start` and
one `center` — and it reads as a mistake in a continuous column, exactly as §1 says. **After**: all
thirteen align, the accent rule above the closing line still marks it, and the stage's copy still
computes `center`. Both states were read back from the DOM as well as looked at.

*The first attempt captured through `render.py` and produced the same picture of slide 11 whichever
slide was asked for — the probe was inert and my injected opener never fired. That picture would have
been the instrument's answer dressed as the deck's, which is **L-110** exactly; the tell was that the
image did not change when the input did.*

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → done | Specified, planned, implemented and reviewed in one sitting. The scope held: rarity is the countable half, and the count decided the shape — six rare treatments, but **half of them contrast within their own slide**, which the clone preserves, so the check needed a second test to be worth shipping. It went from zero to a `shell/` edit for a reason §1 could not have known: the fix already existed as a **hand-copied per-deck override in two of the three decks**, with nothing in the shared shell, which is precisely why only the adopter's deck showed the defect. One home now, two copies deleted. Print waits for an instance, as recommended. |
| 2026-08-13 | → proposed | Raised by the owner from a finding made while looking at the reading view. Scoped around *rarity* rather than around alignment, because what makes a treatment fragile across the two renderings is that its meaning comes from contrast with its neighbours, and rarity is the countable half of that. |
