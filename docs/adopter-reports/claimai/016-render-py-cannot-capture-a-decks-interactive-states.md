# `render.py` cannot capture a deck's interactive states

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Feature |
| **Status** | `closed` — closed 2026-08-30 by [T-267](../../../tasks/T-267-render-py-cannot-capture-a-decks-interactive-states.md). **All four items built; one of this record's own premises was refused by measurement, and it is the one that mattered most.** `render.py state` presses a named control (`--click`, repeatable, with `--watch` naming what the press should change), opens a named quick view (`--qv`), reaches `:hover` (`--hover`) and hit-tests (`--probe`, `--at`); `--shot` turns any of them into a picture. **The refusal is item 4.** This record calls hit-testing *the half with no workaround at all* and says two paragraphs earlier why — *a pane that is not displayed does not composite … hit-testing does not work*. That is true of the pane and not of the capability: measured in headless Chrome before a line was designed, `elementFromPoint` at `#next`'s centre returns `span.chev.r` and `elementsFromPoint` returns the whole stack. So item 4 was the **cheapest** of the four — six lines of probe, no mechanism — while item 2, which this record treats as merely inconvenient, is the only one no DOM write can reach and needs the CSS rewritten. Believing the sentence would have mis-ranked the whole design; kept as [L-150](../../lessons/L-150.md). **Two things this record did not ask for.** `--probe` samples **five** points rather than a centre, because a seeded cover over the pager's lower third leaves the centre clear and takes 2 of 5 — a centre-only test reports that control fully reachable. And `--hover` says *substituted trigger* on every run: it re-inserts the deck's own `:hover` rules against an attribute, into **each rule's own parent** so a rule inside `@media`/`@supports` inherits its conditions rather than having them rebuilt, proved on a deck whose only `:hover` rule is nested two groups deep. **One limit, stated:** a state *in motion* is still out of reach and deliberately so — the probe is pinned, so a disclosure is photographed settled rather than part-way through the transition that revealed it. |
| **Severity** | Medium — two workarounds exist and were used through a whole feedback round, but both are hand-built and neither reaches motion or hit-testing |
| **Found while** | Reviewing `E39 — Move the motion control into the More menu` on `D4 — Executive Board Presentation`, on 2026-08-26. Narrowed on 2026-08-28 after three more slides were built and reviewed |
| **Version seen** | htmldeck `0.6.0` |

## What is missing

`render.py` has three subcommands — `measure`, `shots` and `motion`. Every one of them captures a
slide in its **resting** state. A deck's progressive disclosure — the More menu, a hover detail box,
a quick view, a toggle — has no capture path at all.

The only element the tool ever presses is the deck's own navigation:

```
$ grep -n "click()" tools/deck/render.py
239:      for (var n = 0; n < want; n++) next.click();
556:      for (var m = 0; m <= into; m++) { next.click(); }
561:    if (back) { prev.click(); }
562:    else { for (var n = 0; n < into; n++) { next.click(); } }
```

`#next` and `#prev`, four times. There is no option to press a named control, hover a named target,
or open a named quick view.

**So the part of a deck that cannot be printed is also the part that cannot be reviewed by picture.**
htmldeck's own gate says the ninth condition is a person looking at the deck. Where the thing to look
at exists only after a click, the tool does not help that person.

## Three routes tried first, and what each produced

On 2026-08-26, with a task whose entire visible result was a menu:

| Route | What happened |
| :--- | :--- |
| Open the deck in the agent's browser pane | It cannot open a `file://` URL |
| Copy the deck to a local temp folder and open that | Same refusal |
| Un-set `hidden` on `#moreMenu` in a throwaway copy, then `render.py shots` | The bar still rendered closed. The CSS gates the menu on more than that attribute |

That task was accepted on its markup rather than on a picture.

## Two workarounds found later, and what they cost

Three further slides were built with hover boxes, a toggle and an animated matrix. Both routes below
were found while building them, and every interactive state in those three was reviewed one of these
two ways. **They are why this is a feature request rather than a defect.**

**One — render the state.** Copy the deck, replace the hover pseudo-class with an ordinary class and
pin that class on one element, or write `checked` on the toggle's input, then render normally. This
is the real CSS with a substituted trigger, so what comes back is a true picture of that state.

**Two — measure the state.** Serve the deck over HTTP and drive it in a browser: `file://` is refused
where `http://127.0.0.1` is not. Two things bite. A pane that is not displayed does not composite, so
transitions freeze at their start value and hit-testing does not work; `document.getAnimations()` and
`.finish()` settle them, and computed `transition-duration` and `transition-delay` carry the timing.

Each one is roughly twenty minutes of setup per state, has to be rebuilt from memory next time, and
neither is written down anywhere the tool can find.

## What is left after both

- **No capture of a state in motion.** Workaround one photographs a state that has already settled;
  workaround two cannot composite, so a transition never runs. A menu opening, a matrix crossfading
  or a detail box arriving cannot be seen at all.
- **No hit-testing.** Neither route answers *is this control reachable, and does it cover what it
  should*. That is the question an author most wants a picture for.

## What a capture path would need to reach

Stated as behaviour rather than as an implementation:

1. **Press a named control** — a selector, pressed before the capture, so a menu, a disclosure or a
   tab panel can be photographed open.
2. **Hover a named target** — the same for `:hover` and `:focus-visible` states, which today need the
   CSS edited to reach.
3. **Open a named quick view** — the deck's own reading view for one section, which is a state the
   deck ships and the tool cannot show.
4. **Capture what is under a point.** Hit-testing is the half neither workaround reaches, and it is
   the half that catches a control a decoration has covered.

Items 1 to 3 would each replace one of the workarounds above with a flag. Item 4 has no workaround at
all.

## Related

- [`013-ds-244-sees-label-over-label-but-not-label-over-shape.md`](013-ds-244-sees-label-over-label-but-not-label-over-shape.md)
  — the gate's own blind spot to overlap, which item 4 would help close.
- [`017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md`](017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md)
  — the other `render.py` finding from this project. That one is a defect in a motion the tool
  *does* enumerate; this one is a state it cannot reach.
