# Adopter report — ClaimAI board deck, August 2026

Twenty-seven findings from one project that built a twenty-five slide executive deck with htmldeck
and shipped it.

## Where this came from

The **AI Strategy Leader** training programme, Module 7 — Ethics, Governance, Risk, Compliance,
Standards, Regulation and Law. The closing exam is a full responsible-AI assessment of a fictional
insurer deploying a claims-scoring system, delivered as nine documents and a twenty-five slide
executive board presentation. It ran from 2026-08-23 to 2026-08-28 and produced 84 task records.

The deck was built with **htmldeck**. The project itself was run on **taskmd**. Neither tool was
chosen for a trial — they were used to do real work under a deadline, and everything here is
something that work ran into.

The deck was presented and the exam is delivered. **The verdict was that the deck is good**, which is
the frame for every criticism below: these are the places where a tool that produced a good result
made reaching it harder than it needed to be.

## Why it was collected

The project's owner asked for it in these words:

> *"Everything which is fixed, mitigated, improved, adjusted in this project, but should be
> universally applied to other downstream projects, so the htmldeck and taskmd should solve it, we
> have to collect them. This project ended up in an amazing deck. I want htmldeck not to limit but
> support such results."*

**That is the goal: not to relax htmldeck, but to close the gap between what it enforces and what it
helps with.** Six rules here caught real faults and are named as such inside the records that
criticise others.

## No answer is expected

This is a one-way hand-over. The project that produced it is finished and closed; there is nobody
waiting on a reply, no thread to keep alive, and no deadline attached to any of it.

So each record is written to stand on its own: the evidence is in the record, the version it was seen
on is in the record, and nothing asks a question back. **Take what is useful and discard the rest**
— including any record you judge wrong. Several of these argue against rules that caught real faults
here, and the records say so themselves.

## How to read the set

- **Every record carries its evidence.** A command and its output, a source line, or a verdict the
  tool itself printed. The staging project's rule was that a claim about a tool's behaviour without
  one is a guess.
- **Every record carries `Version seen`.** Fourteen of these were stamped rather than re-run, so
  treat the version as provenance, not as a fresh reproduction. One uncertainty is stated in the
  index: two versions were installed within the same hour, so a record found in that hour may have
  seen the earlier one.
  *[Editor's note, 2026-09-02: the index below is this document's findings table and carries no
  version column and no such statement, and the phrase appears nowhere else in the set. Every one
  of the 27 records stamps `Version seen` as `0.6.0`, and none names an earlier one, so the
  uncertainty cannot be resolved from what was sent and no record can be told from another by it.
  The sentence is kept because the sender knew of the uncertainty; the pointer does not resolve -
  `PR-117`.]*
- **`Severity` is what it costs the author who hits it**, never how hard it is to fix.
- **The `Target` rows are the staging project's own bookkeeping** and name a local clone path. They
  are left verbatim rather than edited, because editing an evidence record on the way out is worse
  than an odd line in it.

## The findings

| # | Kind | Severity | Title |
| :--- | :--- | :--- | :--- |
| [`001`](001-per-section-quick-view.md) | feature | — | htmldeck — a quick view scoped to a document section |
| [`002`](002-ruler-scale-claim-breaks-past-eighteen-sections.md) | defect | — | DS-217 fails on any deck past eighteen sections |
| [`003`](003-reading-view-never-unwraps-a-provenance-row.md) | defect | — | The reading view never unwraps a provenance row, so a long one fails DS-075 |
| [`004`](004-spec-py-cannot-read-a-sources-field-that-carries-a-section.md) | defect | — | spec.py cannot read a `Sources` field that carries anything but a bare slug |
| [`005`](005-a-deck-cannot-express-an-author-requested-duration.md) | defect | — | DS-141's `request` licence cannot be used, because no rule lets a deck state the duration |
| [`006`](006-ds-035-measures-text-through-its-transform.md) | defect | — | DS-035 measures a text run through its transform, so a scale-from-zero entrance fails it at 0 du |
| [`007`](007-quickview-leaves-bold-unconverted-across-a-line-break.md) | defect | — | A quick view leaves `**bold**` unconverted when the emphasis spans a line break |
| [`008`](008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md) | defect | — | The single-letter shortcuts have no modifier guard, so Ctrl-R toggles the view instead of reloading |
| [`009`](009-the-sources-box-does-not-dismiss-on-an-outside-click.md) | defect | — | The sources box does not dismiss on an outside click, though the More menu beside it does |
| [`010`](010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md) | defect | — | `data-played` lands at the start of the transition, so a gated entrance plays under the outgoing slide |
| [`011`](011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md) | feature | — | DS-110 cannot tell a rasterised diagram from a drawing, so front matter has to fail it |
| [`012`](012-ds-092-counts-a-sources-box-as-prose.md) | defect | — | DS-092 counts the provenance sources box as a paragraph of prose, so a fourth source fails the slide |
| [`013`](013-ds-244-sees-label-over-label-but-not-label-over-shape.md) | defect | — | DS-244 catches a label over a label, and never a label over the shape it labels |
| [`014`](014-a-deck-cannot-name-a-repeated-figure-treatment-once.md) | feature | — | A deck cannot name a repeated figure treatment once, and DS-229 does not say so |
| [`015`](015-density-py-write-corrupts-a-self-closing-svg-tag.md) | defect | High | `density.py write` corrupts every self-closing SVG tag it touches |
| [`016`](016-render-py-cannot-capture-a-decks-interactive-states.md) | feature | Medium | `render.py` cannot capture a deck's interactive states |
| [`017`](017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md) | defect | High | `render.py motion` seeks a fraction of duration and ignores the delay, so a working motion reads as dead |
| [`018`](018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md) | defect | High | DS-218 passes htmldeck's own example only because that example has no looping motion |
| [`019`](019-ds-219-cannot-see-a-painted-svg-ancestor.md) | defect | High | DS-219 cannot see a painted SVG ancestor, so a light label on a filled panel can never pass |
| [`020`](020-ds-229-keys-motion-rows-to-exact-selector-text.md) | defect | Medium | DS-229 keys the component contract's motion rows to exact selector text, so any prefix silently breaks them |
| [`021`](021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md) | defect | Medium | DS-239 re-derives --m-rank from the deck, so removing one motion silently invalidates every other rank |
| [`022`](022-ds-244-refuses-a-cross-fade-in-place.md) | defect | Medium | DS-244 refuses a cross-fade in place, because it cannot see that one of the pair is at opacity 0 |
| [`023`](023-ds-100-fires-on-any-question-mark-meeting-a-tag.md) | defect | Low | DS-100 fires on any `?` that meets a tag, including a question the slide answers |
| [`024`](024-ds-202-refuses-a-two-sentence-bottom-line-the-author-chose.md) | feature | Low | DS-202 refuses a two-sentence bottom line, including one the author chose in review |
| [`025`](025-the-gate-passes-copy-its-own-reader-calls-difficult.md) | feature | High | The gate passes copy its own reader calls difficult, and the project had to build an instrument for it |
| [`026`](026-nothing-prints-what-a-slide-actually-contains.md) | feature | High | Nothing prints what a slide actually contains, so a specification and its deck drift silently |
| [`027`](027-the-tools-are-unreachable-when-htmldeck-is-installed-as-a-plugin.md) | feature | Medium | The tools are unreachable when htmldeck is installed as a plugin, and the cache keeps every version |

## Four themes, if you want a shape

1. **Four rules the deck fails permanently** — `DS-110`, `DS-217`, `DS-218`, `DS-219`. A deck that
   can never pass four rules stops reading its own gate. `019` is the sharpest: `DS-219` is
   unsatisfiable for a whole class of correct diagrams, and this repository's own
   `DESIGN-RATIONALE.md` §5.7 already records the doubt.
2. **Rules that test a proxy for what they mean** — `022`/`013` on `DS-244` (proximity, not
   obstruction), `024` on `DS-202` (sentence count, not brevity), `023` on `DS-100` (a `?` before a
   tag, not rhetoric). Each has an escape hatch that teaches the wrong habit; `023`'s pushed a word
   out of the text layer entirely.
3. **The gate is green on things it does not look at** — `025` (copy the author called difficult),
   `026` (twenty-three of twenty-five specification entries had drifted), `016` and `017` (the
   instruments themselves). These are the most valuable, because nothing signals them.
4. **Packaging** — `027`. Installed as a plugin the tools are unreachable, and the obvious launcher
   silently picks a years-old cached version.
