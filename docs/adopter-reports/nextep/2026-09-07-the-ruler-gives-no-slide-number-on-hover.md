---
tool: htmldeck
version: 0.7.0
date: 2026-09-07
severity: request
---

# The chrome ruler has no hover readout, so a dot is a target you cannot aim at

## Expected

The ruler (`T-035`) draws one mark per slide and is the deck's only random-access control. Pointing
at a mark should say which slide it is — a dimmed number above the dot under the cursor — so a
presenter answering a question mid-talk can jump to the right page instead of the page beside it.

## Actual

The marks carry no readout **at the mark**. *Corrected 2026-09-08: they are not silent. The shell wires `previewLabel(b.dataset.label)` on `mouseenter` and `focus` for every tick, which writes the slide name into `.ruler-label` beside the ticks — verified by dispatching `mouseenter` on a tick and watching `#rulerLabel` change from a sentinel to the slide name. What is missing is a readout where the eye is, above the dot under the cursor. The request below is unchanged; the sentence it rested on was too strong.* `DS-217` counts a regular repeating scale as one item
rather than *n*, and the gate verifies that claim by requiring **no per-item label at rest** — which
is right, and is not the same thing as no label on hover. The result is a control with 33 targets
and no way to tell them apart before committing to one.

Measured on a 33-page deck at 1920 wide: the marks sit at roughly 11 px pitch, so the miss is a
whole slide, and the recovery is a second press in front of the room.

## Why it matters

It is the difference between the ruler being a progress indicator and being a control. A presenter
taking a question about *the page with the three bars* currently pages there; with a readout they
point at it.

## Suggested fix

A hover and focus readout above the mark under the cursor, in the deck's `--ink-faint` at
`--fs-mono`: the slide number, and the slide's `data-name` where it fits. `DS-217`'s rest-state
claim is untouched, because nothing new is painted until a pointer or focus arrives — the same
footing on which `DS-163` allows a hover state that is not the only route to content, since the
pager and the counter still say where the reader is.

Raised by the deck's owner, 2026-09-07, from presenting practice rather than from a check.
