# R7 — The printable mode: what printing a deck from `file://` actually costs

[R6](R6-portability-contract.md) §9 left printing as the one honest gap in the portability matrix:
`matchMedia('print')` is available, so a print stylesheet can be *authored and detected* — but
whether `window.print()` behaves from a double-clicked file, and whether a stylesheet reproduces
the deck faithfully at page size, was never tested. This note closes that gap and rules on what the
optional printable mode may promise.

**The ruling, first.** The printable mode is the **paginated stage**: one slide per page, on a page
sized to the slide. The reading view is not a print target. What a printed deck loses is in §5, and
it is not small.

---

## 1. Method, and the instrument that nearly wrote this note wrong

**Test, do not read** — R6's rule, for R6's reason: `file://` behaviour differs per browser and per
version, and documentation describes the HTTP case. Behaviour was measured by a probe page opened in
a real browser from a real file. Renderings were measured by printing to a file **through the
browser's own print dialog**.

**Headless was used only to diagnose, never to measure**, and the distinction earned its keep. A
headless `--print-to-pdf` is a different code path from the one a recipient uses, so
[T-018](../../tasks/T-018-measure-the-printable-mode-what-printing-from-fi.md) §1 put it out of
scope as an instrument. It then **disagreed with the real browser on the central question** (§3):
headless kept the deck in presentation view while the real print flipped it to the reading view, so
a headless check passed while the real print was producing blank pages. Had this note been written
from the headless run it would have described a printable mode that works, and it did not.

Generalised as **L-35**: *an instrument scoped out for being a different code path will eventually
prove it, and the run where it agrees is not evidence that it is equivalent.*

**Two corrections to the measurement of page quality**, both of which flattered the result before
they were caught:

- Chrome's default header and footer are **text at the page edges**, so a naive "how far down the
  page does content reach" metric reported 2.4% dead space on pages that were visibly half empty.
- A document's **last page is not full**, and counting it as dead space flagged a non-defect twice.
- Page **height** decides whether a large unbreakable block is ruinous, so measuring on Letter
  portrait while the deck is printed on **A4 landscape** made the breaks look far better than they
  were. The harness pins the real paper.

---

## 2. The behaviour matrix — Chrome 151 and Edge 151, offline, from `file://`

Identical on all nine rows.

| Row | Result |
| :--- | :--- |
| `window.print()` present | **PASS** |
| **Does it need a user activation?** | **No.** Called with no activation it opened a real dialog and blocked until dismissed — 116 s on Chrome, 29 s on Edge, both `threw=no`. With a live activation it behaves identically. |
| `beforeprint` / `afterprint` fire | **Both, in both browsers, in both attempts.** |
| `matchMedia('print').matches` **inside** `beforeprint` | **`false`** |
| `print-color-adjust: exact` | **PASS**, standard and `-webkit-` spellings both |
| `break-inside: avoid`, `break-after: page` | **PASS** |
| `@page` | Parses as `CSSPageRule`; the `size` descriptor is exposed on `.style` |
| `@page` margin boxes | Survive parsing — **not** tested for rendering |

Three of these matter more than the rest.

**Printing is not gesture-gated.** A deck can call `window.print()` from a button, a keyboard
shortcut, or on a timer, and the dialog opens. This is the one row that required measuring the same
call twice — with and without an activation — because either attempt alone is unattributable
(**L-17**).

**`beforeprint` and `afterprint` fire from a restricted origin.** R6 never measured them. They are
what makes a *cooperative* print mode possible at all: a deck can change itself for the page and
change back afterwards. §5 explains why this note still does not use that capability, and §7 says
who should.

**`matchMedia('print')` does not report printing at the moment a deck would act on it.** R6
recorded the query as "available", which is true and not useful: inside the `beforeprint` handler
it still reads `false`. **A deck must use the events, not the query.** This is the one place where
R6's wording could mislead a reader into building the wrong thing.

---

## 3. The finding: a deck changes its own view while printing

This is the load-bearing discovery, and it took three printed runs to see.

The reference deck switches to its reading view below 960 px and sets `viewport.hidden` when it
does. **Printing is what makes it switch**, because printing changes the layout viewport.
`.viewport[hidden]{display:none}` then hides the stage — and overriding `position` in a print
stylesheet does not touch `display`. The consequences ran in sequence:

| Run | What was printed | Why |
| :--- | :--- | :--- |
| 1 | **13 blank pages** | the reading view was hidden with `!important` *and* the stage was hidden by `[hidden]` — nothing was left |
| 2 | **the reading view** | the `.doc` rule was dropped, so the only visible thing printed. It looked like a fix; the paginated stylesheet had still never rendered a slide |
| 3 | the stage, correctly | `display` forced on **both** `.viewport` and `.viewport[hidden]` |

**The rule this yields is general, not specific to one deck.** Any deck that adapts its layout to
viewport width will adapt during printing. A print stylesheet must therefore *assert the view it
wants*, including overriding whatever the deck's own responsive logic did on the way into the print
— and asserting it means `display`, because that is what the deck used to hide things.

---

## 4. The two renderings, measured on the same twelve-slide deck

Both were built from `examples/reference-deck.html` by
[`tools/deck/print_variants.py`](../../tools/deck/print_variants.py), printed through the real
dialog, and **looked at page by page** (**L-01**).

### Paginated stage — the ruling

Twelve pages, one slide per page, **1920 × 1080 px** (1440 × 810 pt), fonts embedded, backgrounds
and rules intact. Three defects had to be fixed to get there, and each is a rule worth keeping:

- **`position:static` on a slide scatters its own overlays.** A slide is the containing block for
  its absolutely positioned descendants; making it static hands them to the page.
  `position:relative` keeps it in flow *and* keeps it a containing block.
- **`:last-child` did not match the last slide** — the stage ends with the nav and the progress
  bar — so the twelfth slide kept its page break and emitted an empty thirteenth page.
  `section.slide:last-of-type` is the fix.
- **Entrance animations hold their pre-animation state**, so an unplayed slide prints blank or
  half-risen unless the animation is disabled for print.

### Reflow document — measured, then rejected

The reading view prints, and it prints badly, and the badness is **structural rather than a bug**.
It is a document made of slide-sized chunks with atomic figures, so on a short page it strands
headings and leaves large gaps. Three rounds of fixes moved it and did not solve it:

| State | Pages | Interior pages >25% empty | Worst |
| :--- | :---: | :---: | :---: |
| whole sections unbreakable | 22 | 8 | 57% |
| sections breakable, whole panels protected | 18 | 4 | 48% |
| protection moved to row level | 16 | 2 | 29% |

Two attempted improvements were **measured and reverted**, which is why they are recorded here
rather than lost: chaining `break-after:avoid` through the standfirst forces a section's whole
opening onto the next page whenever the block after it is tall, and opens larger holes than it
closes (18 pages, five bad, worst 61%). It lost on both papers tested.

**Why it is rejected rather than pursued.** [`CLAUDE.md`](../../CLAUDE.md) rule 5 makes printing
*a mode the user can force on, never a constraint on the design*. Continuing to reshape the reading
view so it paginates well is precisely printing becoming a constraint on the design. The reading
view already serves the read-alone case **on screen**, where progressive disclosure works; print
does not have to carry that job, and doing it badly serves nobody.

**This answers the open question [T-021](../../tasks/T-021-the-reflow-view-and-the-resolution-contract.md)
carries — *do the reflow view and the print stylesheet share one document rendering?* — with a
measured **no**. They are separate concerns.**

---

## 5. What the printable mode does **not** preserve

Written for the user, because a printable mode whose limits are discovered on paper is worse than
one that states them.

1. **Everything behind progressive disclosure — 38.6% of the deck's text.** Ten panels, 3 543 of
   9 177 characters on the stage. The panels are absolutely positioned overlays on a fixed
   1920 × 1080 box, and opening them onto it covers the content they explain. **The affordance is
   hidden in print too**, deliberately: printing a "+ *show detail*" control onto paper advertises
   something the reader can see and cannot reach. Read the detail on screen.
2. **Motion, 3D and anything whose content is only reachable by interacting.** Unsurprising, and
   stated for completeness.
3. **The reader's paper choice, on this rendering.** `@page { size: 1920px 1080px }` pins the page,
   which greys out the print dialog's layout controls. Kept, because here the page shape *is* the
   design — a 16:9 slide letterboxed onto A4 is not the artifact — but it is a stated cost, not an
   accident. On any rendering where the page shape is *not* the design, do not pin `size`.
4. **The "Background graphics" checkbox.** `print-color-adjust: exact` overrides it, so toggling it
   changes nothing. Defensible — in this design the backgrounds are content, not decoration, and
   the property exists to say so — but it is one more decision the deck takes from the reader.
5. **Privacy of the file's location.** Chrome's default header/footer prints the deck's **absolute
   `file://` path** across the foot of every page. It is not reachable from CSS and it is a real
   disclosure: a recipient printing a deck puts their own directory layout on paper. The printable
   mode can warn; it cannot fix. Turn headers and footers off in the dialog.

---

## 6. Size cost, measured

| Rendering | Print CSS | Deck with it | Delta on a 178.2 KB deck |
| :--- | ---: | ---: | ---: |
| Paginated stage | **3 063 B** | 180.9 KB | +2.7 KB |
| Reflow document *(rejected)* | 2 422 B | 180.3 KB | +2.1 KB |

Under 2% of the deck either way, on a deck that already carries three embedded faces, icons and
SVG diagrams ([R5](R5-assets-and-licences.md)). **Cost is not a reason to refuse printing, and it
never was.** The reason to keep the printable mode narrow is what it cannot preserve (§5), not what
it weighs.

---

## 7. Does rule 5 survive?

**Yes, as written, and the measurement strengthens it.**

> *Printing is optional. A mode the user can force on, never a constraint on the design.*

Nothing in §2 threatens printing: the API works, the events fire, colour is faithful, pagination
control exists. Nothing about supporting it demanded a change to the deck's design — the paginated
rendering is 3 KB of stylesheet over a deck that was designed without print in mind.

The rule also **did work in this task**, which is the better argument for it. When the reading
view's pagination turned out to be structurally poor, rule 5 is what said to stop: reshaping the
deck's reading view to print better would have been printing constraining the design. The rendering
was dropped instead.

One clarification the rule now carries, which it did not before: **"optional" is a promise to the
user about what they get, so it obliges the mode to say what it does not do.** §5 is that
statement, and a printable mode that ships without its equivalent is not honouring rule 5, it is
hiding behind it.

**A candidate change of direction, not taken here.** `beforeprint` fires (§2), so a *cooperative*
printable mode is genuinely available: expand every panel and print each slide's detail on a
following page, preserving all 38.6%. It roughly doubles the page count and it is new design work,
so it is raised against
[T-028](../../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) rather than
smuggled into a measurement note.

---

## 8. What this note is *not* evidence about

- **Any browser other than Chrome 151 and Edge 151 on Windows.** No Firefox, no Safari, no mobile,
  no older version, no macOS or Linux. `file://` and print policy both differ between engines.
- **Physical printers.** Everything here was printed to a file. Nothing was measured about drivers,
  paper handling, duplexing or colour management on a real device.
- **`@page` margin boxes as a feature.** They survive parsing; whether they render page numbers or
  running heads was not tested, and the row says so.
- **PDF export through a headless renderer**, which is a different mechanism with a different
  dependency profile — scoped out with speaker notes in [BRIEF.md](../BRIEF.md) open question 4.
- **Whether the printed deck reads well as an argument.** Twelve pages of slides is a handout, not
  a document, and no matrix answers whether that serves the reader. That is **L-01**'s territory.
