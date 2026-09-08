---
tool: htmldeck
version: 0.7.0
date: 2026-09-08
severity: request
---

# When the ruler condenses, the small dots stop being targets — give them back, once a hover readout says where they jump

## Expected

The ruler is the deck's only random-access control. A presenter answering a question mid-talk should
be able to jump to any slide from it, at any width. When the chrome condenses, the small dots should
stay reachable, and the reader should be able to see which slide is under the cursor **before**
committing to the press.

## Actual

Past the layout bound the shell disables every per-slide tick. `fitRuler()`:

```js
var isMark = lay.dense && li.dataset.section === undefined;
b.disabled = isMark;
if (isMark) b.tabIndex = -1;
```

with the comment stating the intent plainly: *Past the bound the small ticks are marks, not targets,
so they leave the tab order and stop being clickable. Section ticks stay targets at full pitch.*

**Measured on a 33-page deck at 1150x720, where the chrome is visible and `data-dense` is on:**

| | Small ticks | Section ticks |
| :--- | :--- | :--- |
| count | 30 | 3 |
| `button.disabled` | `true` | `false` |
| `button.tabIndex` | `-1` | default |
| `document.elementFromPoint` over the dot | `LI` | `BUTTON` |
| hit box | 4.8 x 15.6 px | 31 px wide |

`elementFromPoint` returning the `LI` is the part that matters: a disabled button is not a hit-test
target, so **no pointer event of any kind reaches it** — not a click, and not a hover. The reader is
left with three targets out of thirty-three, and the keyboard route is gone with them.

## Why the trade was made, and why it can be reversed

Disabling was the right call on its own terms. At 4.8 px a dot is not something a person can aim at,
and a control you cannot aim at is worse than no control: the miss is a whole slide and the recovery
is a second press in front of the room.

**A hover readout removes exactly that objection.** If pointing at a dot says which slide it is,
aiming stops being guesswork — the reader sweeps the ruler, reads, and presses when the right name
appears. The small target then costs a moment rather than a mistake, and the dots can be targets
again.

**Half the readout already exists.** The shell wires `previewLabel(b.dataset.label)` on `mouseenter`
and `focus` for every tick, writing the slide's name into `.ruler-label` beside the ticks. Verified
2026-09-08 by dispatching `mouseenter` on a tick and watching `#rulerLabel` change from a sentinel to
the slide's name. It is wired on the disabled dots too, and unreachable there for the same reason the
click is.

## Suggested fix

Two changes that only work together.

1. **Keep the small ticks as targets in dense mode.** Drop the `disabled` and the `tabIndex = -1`;
   keep the 4 du dot, which is a rendering decision and a good one. The `<li>` already has the wider
   box the pointer lands on, so the hit area can come from the `li` without changing the drawing.
2. **Put the readout where the eye is.** The label slot is beside the ticks; at dense pitch the eye
   is on the dot. A small overlay above the mark under the cursor, in `--ink-faint` at `--fs-mono` —
   the slide number, and the `data-name` where it fits — closes the loop between pointing and
   reading. That is the request already filed as
   [2026-09-07-the-ruler-gives-no-slide-number-on-hover.md](2026-09-07-the-ruler-gives-no-slide-number-on-hover.md),
   and this finding is the reason it is worth more than a nicety: it is the precondition that makes
   the dots usable again.

`DS-217`'s rest-state claim is untouched by either change, because nothing new is painted until a
pointer or focus arrives.

## What it buys

The ruler becomes a control at every width instead of a progress bar with three shortcuts. A
presenter taking a question about *the page with the three bars* points at it rather than paging to
it, and a keyboard user gets thirty targets back.

Raised by the deck's owner, 2026-09-08, from presenting practice.
