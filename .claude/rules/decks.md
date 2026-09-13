---
paths:
  - "examples/**"
  - "tools/deck/**"
  - "shell/**"
  - "themes/**"
  - "skills/htmldeck/**"
---

# htmldeck — deck rules

The harness appends this file after a session reads a file one of the paths above names. It holds the
rules that bind deck work, cut from [`CLAUDE.md`](../../CLAUDE.md) by
[T-295](../../tasks/T-295-complete-t-288s-observation-and-decide-the-move.md). **Rule 6 stays in `CLAUDE.md`**, and every number here is
the one a citation uses.

## The rules that must survive

1. **Self-contained or it doesn't ship.** One `.html` that renders correctly with the network
   disabled. Most of the source corpus failed this, mostly on web fonts, and the decks that passed
   are the precedent — the measurement is [R1](../../docs/research/R1-corpus-conventions.md)'s, and no
   figure from it lives here (**L-96**).
   *Measured and settled 2026-08-06:* this is no longer the main technical problem. A full
   12-slide deck with three embedded faces, icons, a motion library and SVG diagrams is **192 KB
   with zero external references** (`docs/research/R5-assets-and-licences.md`). Embedding is
   cheap, so `portable` is the default and the only shipping mode. A `linked` (CDN) mode exists
   **for the authoring loop only**; a deck delivered that way is a defect, and the critique pass
   says so.
2. **Portability is the constraint, not restraint.** No installation, no special privileges — the
   recipient double-clicks the file. It must render **glitch-free in recent Chrome/Edge**; other
   browsers degrade gracefully and mobile is secondary. Within that envelope, richness is wanted:
   interaction, animation and 3D. There is no JavaScript budget. The corpus habit of 1–3 script
   tags describes past work, not this.
3. **Use whatever renders best.** SVG, `<canvas>` and WebGL are all permitted, for diagrams
   included. Still never a rasterised diagram (DS-110), and never an *external* library — rule 1
   settles that. When SVG is as good, prefer it: it scales, themes and diffs.
4. **One theme, every layer parametric.** Ship one fully-resolved look, not several and not a
   per-topic palette. Every value that could differ between themes is a token. Variety comes later,
   from a tool that generates new templates — design for it now, do not build it yet.
5. **Printing is optional.** A mode the user can force on, never a constraint on the design.

Rule 6 is `CLAUDE.md`'s.

7. **Critique is a first-class mode**, not a footnote. It is what turns a first draft into
   something worth presenting, and it is the part users cannot do for their own work.

## Voice

The critique mode is blunt on purpose — bottom line up front, then section by section, no
diplomatic padding. A review that opens with three compliments is one nobody acts on. This is a
deliberate choice carried from the corpus, where the harshest review was the most useful
artifact in it.

That applies to the critique output. The **decks** themselves stay respectful, positive and
professional, and avoid the terminology that marks text as machine-written — ship that list and
enforce it at build time rather than hoping.

## Verifying

Test the generator on a **real 12-slide deck with diagrams**, not a three-slide toy — the corpus
decks are the target case, and that is the size where layout and pacing problems appear. State
results as what was actually produced, not as "works".

**12 is the floor, not the target.** Only the contents page has been built and printed above 13 —
at 17, 25 and 43 — and what is still known to bite above it is the ruler, which degrades to dense
mode past 16 and then marks where you are more quietly than it marks anything else
([T-178](../../tasks/T-178-dense-mode-drops-the-position-mark-below-the-section-marks.md)). Treat a long deck as
**untested territory** rather than as a longer version of a tested one, and say which length a
result was measured at. How the target moved, and off what evidence, is
[`docs/RELEASE-HISTORY.md`](../../docs/RELEASE-HISTORY.md) §4.

**And print it. One thing here can read the paper, and it reads two numbers.**
`tools/deck/printgeom.py` reads the card rectangles out of the printed PDF and asserts `PRINT-2` *no
two cards intersect* and `PRINT-3` *no card reaches the footnote*, on any deck it is pointed at,
standard library only. **It is two numbers and nothing wider**, and the fault it was written for
lives only in paged layout, which no screen measurement reaches (**L-76**). Whether the page reads as
a compact mode rather than as damage is still a person's, which is the 2026-08-08 ruling on DS-222 to
DS-226 and is untouched. `CLAUDE.md` rule 6 is not satisfied by a screen render at any length, nor by a green
`PRINT-2`.

## Publishing constraint that binds deck work

- **Font-licence aware.** If fonts are embedded, only ones whose licence permits redistribution.
  Record the licence next to each.
