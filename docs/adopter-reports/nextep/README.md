# Adopter report — Nextep capstone deck, September 2026

Eighteen findings from one project that built a thirty-three page argument deck with htmldeck and
delivered it under a fixed date.

## Where this came from

The **AI Strategy Leader** training programme's capstone. The project designed and part-built a
service that decides whether a project's declared state matches its recorded work, and delivered it
as a set of documents, a report and one presentation deck. It ran from 2026-08-26 to 2026-09-08,
tracked as GitHub issues, and the deck was the last deliverable finished.

The deck was built with **htmldeck 0.7.0** — one finding predates the upgrade and is stamped
`0.6.0`. The project ran on **taskmd**, and the same project's findings against that tool were
collected separately.

Nothing here was a trial. The tools were used to do real work against a deadline that did not move,
and every record is something that work ran into.

## Why it was collected

The project's owner set the rule on day one: feedback to an upstream project is recorded as it is
found, and handed over in one batch. Findings were written the day they were met, each with the
command that proved it, and the batch waited so that the capstone's own clock was never spent on a
context switch into a plugin repository.

**The deck is good and the tool made it so.** These are the places where reaching that result cost
more than it needed to, and — in the four `request` records — the places where the design system has
no vocabulary for a decision the deck's owner made.

## No answer is expected

This is a one-way hand-over. The project that produced it is delivered and closed. Take what is
useful and discard the rest, including any record you judge wrong.

## How to read the set

- **Every record carries the command that proves it.** The project's rule was that a claim about a
  tool's behaviour without the command is a guess.
- **Every record names the version it was measured on**, in its own front matter or its opening
  lines. Seventeen on `0.7.0`, one on `0.6.0`.
- **`Severity` is what it cost the author who hit it**, never how hard it is to fix.
- **Paths inside the records — `deck/nextep.html`, `tools/deck.ps1`, `docs/` — are the adopting
  project's own**, and that repository is private. The records are written to stand without it: the
  evidence is quoted in the record, never linked out of it.
- **Cross-links between records resolve inside this folder.** Nothing links out.

## The findings

| # | Kind | Version | Title |
| :--- | :--- | :--- | :--- |
| [`01`](2026-09-01-nav-chrome-has-no-first-last-page-control.md) | suggestion | 0.6.0 | The nav chrome offers no clickable first-page or last-page control |
| [`02`](2026-09-06-a-synthetic-keydown-on-document-throws-in-the-shell-handler.md) | defect | 0.7.0 | A synthetic `keydown` dispatched on `document` throws inside the shell's handler |
| [`03`](2026-09-06-quickview-cannot-wire-an-icon-first-source-item.md) | defect | 0.7.0 | `quickview.py` cannot wire a source item whose icon comes before its id |
| [`04`](2026-09-07-a-deck-authored-content-motion-gets-no-motion-gate.md) | defect | 0.7.0 | A deck-authored content motion gets no `--m-on`, so it runs for 0s and only ever snaps |
| [`05`](2026-09-07-density-ranks-the-animating-rule-not-the-declaring-class.md) | suggestion | 0.7.0 | `density.py write` ranks only the rule that starts the motion, and says nothing when it finds none |
| [`06`](2026-09-07-measure-reports-no-overflow-while-a-figure-paints-over-the-prose.md) | gap | 0.7.0 | `render.py measure` reports zero overflow while a figure paints over the lines beneath it |
| [`07`](2026-09-07-motion-off-does-not-reach-a-deck-authored-motion.md) | defect | 0.7.0 | The reader's Motion control does not stop a motion the deck wrote |
| [`08`](2026-09-07-render-state-cannot-see-an-svg-fill-change.md) | defect | 0.7.0 | `render.py state` reports "nothing measured differs" for any SVG paint change |
| [`09`](2026-09-07-render-state-hover-fires-css-hover-but-no-mouseenter.md) | defect | 0.7.0 | `render.py state --hover` paints the CSS hover and never fires `mouseenter` |
| [`10`](2026-09-07-slidefacts-reports-no-control-on-any-slide.md) | defect | 0.7.0 | `slidefacts.py` reports "the slide carries none" under `Controls` on every slide |
| [`11`](2026-09-07-the-ruler-gives-no-slide-number-on-hover.md) | request | 0.7.0 | The chrome ruler has no hover readout, so a dot is a target you cannot aim at |
| [`12`](2026-09-07-the-shell-cancels-enter-and-space-before-a-deck-button-sees-them.md) | defect | 0.7.0 | A real `<button>` on a slide is not operable by Enter or Space |
| [`13`](2026-09-08-slidefacts-closes-an-element-at-the-first-matching-close-tag.md) | defect | 0.7.0 | `slidefacts.py` closes an element at the first matching close tag, so most of a page's face is invisible |
| [`14`](2026-09-08-readability-inherits-slidefacts-truncation-so-a-third-of-the-copy-is-unread.md) | defect | 0.7.0 | `readability.py` reads its lines through `slidefacts.py`, so a third of the copy is neither read nor named |
| [`15`](2026-09-08-shell-sync-is-silent-about-a-stale-chrome-tail.md) | friction | 0.7.0 | `shell.py sync` reports a deck fully up to date while its chrome tail is a release behind |
| [`16`](2026-09-08-the-condensed-ruler-drops-the-small-dots-as-targets.md) | request | 0.7.0 | When the ruler condenses, the small dots stop being targets |
| [`17`](2026-09-08-the-gate-has-no-route-for-a-deviation-the-owner-licensed.md) | request | 0.7.0 | The gate has no route for a deviation the deck's owner licensed, so every adopter wraps it |
| [`18`](2026-09-08-an-inline-term-tag-with-a-definition-bubble-has-no-contracted-form.md) | request | 0.7.0 | An inline term tag that opens a definition bubble has no contracted form |

## Four themes, if you want a shape

1. **No instrument can see an interaction.** `06`, `08`, `09` and `10` are four tools reporting
   confidently on states they never reached — a paint change invisible to `render.py state`, a
   `:hover` painted without a `mouseenter`, a control census that finds no controls, an overflow
   check green while a figure paints over the prose. Between them, acceptance of anything
   interactive came down to a person opening the file.
2. **A deck-authored motion lives outside the shell's contract.** `04` and `07` are the pair: a
   motion the deck writes inherits no `--m-on`, so it runs for zero seconds and snaps, and the
   reader's own Motion control never reaches it. Both pass every check. `05` is the instrument that
   could have said so.
3. **One defect, two consumers, and only the second one is loud.** `13` truncates a slide's body at
   the first matching close tag; `14` is `readability.py` inheriting it and reporting aggregates
   over two thirds of the copy, with a ledger that promises nothing goes missing quietly.
4. **The gate has no vocabulary for what the author decided.** `17` is the general case — three
   owner-ruled deviations, red on every run, and a forty-line wrapper written to hold the ruling.
   `18` is a pattern the owner asked for by name, approved, and which the component contract has no
   shape for. `11` and `16` are the same shape in the chrome: a control the reader cannot aim at,
   and the readout that would make it aimable.
