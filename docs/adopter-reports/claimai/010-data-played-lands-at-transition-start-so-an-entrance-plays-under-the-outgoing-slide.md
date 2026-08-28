# `data-played` lands at the start of the transition, so a gated entrance plays under the outgoing slide

| Field | Value |
| :--- | :--- |
| **Target** | `htmldeck` — Gábor's own repository, cloned under `C:\Work\AgentPlugins` |
| **Kind** | Defect — small, and lower priority than [008](008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md) and [009](009-the-sources-box-does-not-dismiss-on-an-outside-click.md) |
| **Status** | `open` |
| **Found while** | Round 2 of the deck review on `D4 — Executive Board Presentation`, on 2026-08-25 |
| **Version seen** | `0.6.0` |

## What this note is not

The reviewer's original report was *animations trigger on load, not on page show*, and on the deck in
front of him that turned out to be the **deck's** defect, not htmldeck's: the entrance in question
was declared with no gate at all, so it ran at document load while its slide was off-screen. htmldeck
provides the hook; the deck had not used it. That half is fixed in the deck.

What is left is the narrower thing underneath, and it is real.

## What happens

`go()` marks the arriving slide in the same synchronous block that starts the outgoing slide leaving:

```js
slides.forEach(function(s){ s.removeAttribute('data-leaving'); });
if (prev !== i && slides[prev]) {
  slides[prev].setAttribute('data-leaving', i > prev ? 'fwd' : 'back');
}
idx = i;
...
/* charts and entrances draw in once, never on the way back (DS-146) */
if (!played[i]) { played[i] = true; slides[i].setAttribute('data-played',''); }
```

`shell/deck.js:455–472`.

So `[data-played]` becomes true at **t = 0** of the transition, not at its end. An entrance gated on
it — which is the gate DS-146 tells authors to use — begins while the previous slide is still
animating out. On a deck whose slide transition is long enough to see, the first part of the
entrance happens underneath it, and a staggered entrance loses its opening beat.

## What is missing

An author has one hook and it means *this slide has been reached*. There is no hook meaning *this
slide has arrived and the transition is over*, which is when an entrance should begin.

## Proposed fix

Either is small.

1. **Set the attribute on transition end.** Keep `played[i]` bookkeeping where it is, and move the
   `setAttribute('data-played','')` into the handler that already clears `data-leaving`
   (`deck.js:513–517` listens for the outgoing slide's animation ending). The gate then means what
   its name suggests.
2. **Add a second attribute** — `data-arrived` — set at transition end, and leave `data-played`
   exactly as it is. Nothing that exists changes behaviour, and an author who wants the later moment
   has it.

The second is safer for decks already in the field. Whichever is taken, `DESIGN-SYSTEM.md`'s DS-146
row should say **when** `data-played` lands, because *draw in once, never on the way back* describes
how often and says nothing about when.
