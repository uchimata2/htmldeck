---
tool: htmldeck
version: 0.7.0
date: 2026-09-08
severity: request
---

# An inline term tag that opens a definition bubble has no contracted form, and the nearest rule fixes the wrong direction

## What was asked for

A slide carried four coined terms in one dense argument, and the deck's owner asked for this by
name, 2026-09-08:

> *"What if we introduce a few term tags — Data leakage, TR-13, Drift. These tags can open a popup
> bubble on hover with the details. This way it can be clearer, the terms will be highlighted, and
> the specs can be displayed."*

Built, the verdict was *exactly how I imagined*. It is a good pattern, it belongs in a design
system, and htmldeck has no place to put it.

## Why `.disc` is not it

`.disc` is a block: a `div` on the slide, a labelled `button`, a panel of `.row`s. A term tag is a
**word inside a sentence** that opens a small bubble over the block. Three parts of the contract
push against it, and each one is right on its own terms.

| Rule | What it says | Why an inline term tag fights it |
| :--- | :--- | :--- |
| `DS-138` | A tier-two panel drops **below** its control | A bubble below a word covers the sentence that provoked it, and a term in the last line of a block has no room below at all. The owner's ruling here was **upward**, with a flip and a floor at the bottom line |
| `DS-230` | Tier two is one of four kinds, closed | A definition of a term the face carries is `scope` in substance, so the vocabulary is not the obstacle — the **shape** is |
| `DS-092` | Paragraph 3–4 sentences | A bubble written inline is read as part of the paragraph and spends its budget, so the definitions had to be moved out of the prose into a sibling list |

Because none of it is a `.disc`, no disclosure rule reached the result: the component check passes,
and `DS-138`'s direction, `DS-227`'s shut-at-load and `DS-137`'s one-at-a-time were satisfied by
the deck's own script rather than by the contract.

## What was built, and what it had to solve

The specification is 40 lines; the parts worth taking are these.

1. **Two parts, deliberately not adjacent.** `.termtag` is a real `<button type="button"
   aria-expanded="false">` sitting in the prose, its text the term itself. `.termbub` is the bubble
   it names through `aria-controls`, and the bubbles live together in a `.termlist` beside the
   block — outside the paragraphs, for `DS-092`'s reason above.
2. **The bubble overlays and never pushes.** `position:absolute`, never in flow, so opening one
   cannot reflow the argument under the reader's eye.
3. **Upward, with a measured floor.** The flip is decided against the **bottom line**, not the
   block: measured on the built page, one bubble needed 650 layout px against a 643 px floor, and
   flipping against the block fired a line early and put every bubble over quiet prose.
4. **A press pins it**, so a presenter can point at the definition while talking.
5. **The reading view prints every bubble as a parenthetical beside its term**, so nothing lives
   only behind a pointer.

Point 5 is what makes the pattern legal under `DS-163` (*never hover-only*), and it is the part a
deck is most likely to skip when inventing this alone.

## Suggested fix

Contract it: `.term` (an inline `button` in copy) and `.term-bub` (its panel), with `data-disc`
carrying the kind so the panel census stays meaningful. Two rules need one clause each:

- **`DS-138`** — the direction is *away from the reading line*, which is below for a control at the
  head of a block and **above** for a control inside the prose. The obligation the rule exists for
  is that the panel opens fully inside the stage; upward satisfies it where downward cannot.
- **`DS-092`** — subtract a term bubble's text from the paragraph it sits beside, exactly as the
  sources box is subtracted today (adopter report `012`, `T-262`). The precedent and the argument
  are already written.

## What it buys

The pattern is how a dense slide stays honest: the coined term stays in the sentence, the definition
is one press away, and the printed page carries both. Every deck that needs it currently invents it,
and the parts most likely to be got wrong — the flip floor, the pinned press, the printed
parenthetical — are the parts no rule currently asks for.
