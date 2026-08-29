# The reading view never unwraps a provenance row, so a long one fails DS-075

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect |
| **Status** | `closed` |
| **Found while** | Building `D4 — Executive Board Presentation` at htmldeck stage 6, on 2026-08-24 |
| **Version seen** | `0.6.0` |

## What happens

`shell/components.css` sets `white-space:nowrap` on `.sources-item`, which is right on the stage:
the box is absolutely positioned at a fixed design-unit width and a wrapped row would read as two.
The reading view undoes the box —

```
.doc .sources-box{position:static;display:block;min-width:0;…;white-space:normal}
```

— but never the **item**, and `white-space` does not inherit past a descendant that sets its own.
So every row keeps `nowrap` in a document that has to fold to 320 CSS px, and one row longer than
about forty characters holds the whole page open.

## Evidence

Measured on the ClaimAI deck, whose provenance rows carry a deliverable section and the article or
clause it was verified against.

```
python tools/deck/check.py <deck> --quiet
```

```
DS-075   reflow scrollWidth at 320 CSS px: 514 (overflowing: 0)
```

`overflowing: 0` is the tell, and it is what made this expensive to find: the probe scans
`#docBody *`, and the wide element is the `.sources-item` inside `#doc` rather than inside
`#docBody`, so the failure names a number with nothing beside it. Removing every `.provenance`
from the deck takes `scrollWidth` to 320; removing the figures or any slide body does not.

## What is missing

One rule. The reading view is a document, and a provenance row in a document should wrap like every
other run in it.

## Proposed fix

```
.doc .sources-item{white-space:normal}
```

beside the `.doc .sources-box` rule it belongs with. The deck can and did add this to its own
`<style id="slides">`, but a deck should not have to repair the reading view.

**Consider the failure message too.** `_widest()` prints nothing when `at320Overflowing` is zero, so
a failure caused outside `#docBody` gives a builder a bare number. Widening the probe's scan to
`#doc *`, or naming the widest element whatever the count says, would have made this a one-line
diagnosis.

## Still true after round one of the owner's review

2026-08-24. The deck's round-one feedback asked for a related but separate thing — that in a table,
only a verbose column wraps, and a single label, id or number never breaks — and the deck now
classifies every table cell at build time and carries `td.nb,th.nb{white-space:nowrap}`. That change
does **not** overlap this one: it governs cells inside a quick view, where the browser was splitting
`CR-03` at the hyphen and `ISO/IEC` at the slash. The `.doc .sources-item` repair this note reports
is still carried by the deck and still belongs in the shared block.

## Closed

**2026-08-29 by [T-269](../../../tasks/T-269-three-build-path-defects-the-adopter-worked-around.md),
both halves, remedy as proposed.** `.doc .sources-item{white-space:normal}` sits beside the
`.doc .sources-box` rule it belongs with, so a deck no longer has to repair the reading view.

**And the failure message, which is the half that cost the time.** The probe scanned `#docBody *`
while the number it reported was `scrollWidth` read off `#doc` - so a wide element between the two
failed the rule while the row said `overflowing: 0` and `_widest` printed nothing beside it. The
scan is now taken over the same subtree as the measurement. **A count over a smaller subtree than
the number it accompanies can contradict it, which is worse than not counting at all**, and that is
the general form of this record rather than one selector.
