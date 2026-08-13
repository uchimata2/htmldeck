# examples

Three decks. All are single self-contained `.html` files with **zero external references**; open any
of them by double-clicking, with the network off.

| File | What it is |
| :--- | :--- |
| [`reference-deck.html`](reference-deck.html) | The reference deck. 12 slides and a colophon, built **by hand** against [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) by [T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md); the colophon and the source citations are [T-069](../tasks/T-069-extend-the-provenance-mark-to-multiple-sources.md)'s. |
| [`reference-deck-seeded-defects.html`](reference-deck-seeded-defects.html) | The same deck with **one deliberate defect per evaluation dimension**. A test fixture, not an example to copy. |
| [`sort-window/`](sort-window) | *Move the window, not the fleet*, 12 slides, built **through build mode** by [T-002](../tasks/T-002-build-mode-the-self-contained-deck-generator.md), with its two specification files and its sources beside it. |

**The difference between the first and the third is the whole point of T-002.** One was authored;
the other was assembled from [`shell/`](../shell) and then authored into, three slides at a time,
with the gate run per batch. They share a runtime because the shell *is* the first deck with its
content cut out.

**Riverbend is an illustrative city. It does not exist.** Every figure in either deck is an output
of the assumptions stated on the slide that uses it. Nothing is attributed to a real agency, study
or place. See *Provenance*, below.

---

## The reference deck

*Buy frequency before bikes*, a mid-size city choosing between building a bike-share network and
raising bus frequency, with one capital grant that closes in March.

**250 KB in one file**, 255 787 bytes. Three embedded typefaces (97 KB of it as base64), ten
Lucide icons in one sprite, eight hand-written SVG figures, and the deck shell. No libraries, no
build step, no network.

The theme is a **region**, not a habit: one `<style id="theme">` holds every `@font-face` and every
`:root` block, and [`themes/quarto.css`](../themes/quarto.css) is what it contains. Swapping it is
one command and edits no other rule.
[`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) is the contract a theme answers to.

Every slide carries a **bottom line**: one factual sentence, at the foot of the slide, second in
prominence only to the headline. It is what the slide delivers, and it is there so the deck reads
without a presenter. [T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md)
added it to all twelve; before that the deck had one on none of them, and passed the gate anyway.

### Using it

| | |
| :--- | :--- |
| `←` `→` `space` `PageUp` `PageDown` `Home` `End` | Move between slides |
| `d` | Open or close this slide's detail |
| `r` | Switch between the presentation and the reading view |
| `m` | Motion on or off |
| `t` | Light or dark |
| `f` | Fullscreen |
| `Esc` | Close an open detail panel, or leave the reading view |

The navigator is a **ruler**: one small tick per slide, a large tick at each stage start, every
tick a named jump target. Click one to go there, hover or focus one to see where it lands.
Prev/next, swipe and the mouse wheel all work too. While a tick holds focus the ruler owns the
arrow keys and `Home`/`End` for moving *between ticks*; everywhere else they move between slides.
That precedence is stated in both handlers on purpose, because a rule that depends on which
listener was registered first is not a rule (DS-137). Disclosure never interacts with advancing:
arrows move, `d` toggles, and neither affects the other.

The ruler replaced a stage-name ribbon in [T-035](../tasks/T-035-the-ruler-navigator.md), because
seven text labels cost 856 design units inside a 1180-unit box and a longer deck or a longer stage
name would have wrapped the row onto a second line, the exact failure DS-217 exists to prevent.
There used to be a dot per slide as well; T-028 removed those under DS-216 and DS-217, since a
navigator, twelve dots and a progress bar are three answers to *where am I*, all competing with the
slide. What remains is two, and they answer different questions: the ruler says where in the
deck, the `05 / 12` counter says how far through.

### The reading view

The **Read** control switches to a conforming alternate version: one column, normal flow, type in
`rem`, every detail panel already open. It auto-engages when the stage scales below 0.5, which is 960 CSS
px of width on a 16:9-or-taller window and sooner on a short one, and never in fullscreen.
Position is preserved in both directions.

**The conformance claim, stated in full:** *WCAG 2.2 Level AA, via a conforming alternate version
reachable by a persistent control.* Not "this deck is AA". The presentation view is a scaled
fixed stage and does not meet 1.4.4 Resize Text or 1.4.10 Reflow on its own. The reading view is
what conforms, the **Read** control is the persistent route to it, and the claim is only true while
both hold. [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §7 owns the wording.

### Provenance

Every figure derives from assumptions printed on the deck, and each slide's disclosure shows the
derivation, the exclusions, and what the model holds constant. Figures the model estimates rather
than derives carry an `[est.]` marker.

This is a deliberate reading of DS-102 (*no fabricated metrics; every figure sourced*). An example
deck about a place that does not exist cannot satisfy that rule by citing anyone, so **the
arithmetic is the source and the deck says so**. Quoting real transit research from memory would
have been the actual violation: a misremembered elasticity is a fabricated metric wearing a
citation.

**The two decks discharge DS-102 differently, and the difference is a fact about them rather than a
defect in either** ([T-087](../tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md)).
`sort-window/` was built through build mode, so it carries a `.foundation.md` whose **figure ledger**
binds each value to its source *and to the slides it appears on*, 58 rows, one per figure. This deck
was built by hand before that format existed, and its record is **source-level**: the colophon names
three model documents, says what each carries, and lists the slides that rest on it, with a
per-slide provenance mark saying the same thing from the other end. Both are complete records; only
the ledger is fine-grained enough for a program to check a figure against a slide, which is why
`spec.py`'s `SPEC-5` runs on the worked example and not on this one.

**Swept against its sources on 2026-08-10, and the source documents gained what it found.** The
colophon's three slide lists match the twelve slides' provenance marks exactly, in both directions.
The figures did not: the six-corridor comparison on slides 6 and 10 asserted twelve new-daily-trip
values of which the ridership model carried one, and named three corridors the model called
something else. The model now carries all twelve and the deck's names, and its statement that *the
six trunk routes carry 36,000* is corrected to the three corridors that actually sum to it. **Four
figure occurrences remain unsourced on purpose** and are listed in the task: the deck's own build
date, and three axis scale marks.

### What was measured

In real Chrome, from `file://`, with every DNS lookup black-holed:

| | |
| :--- | :--- |
| External references | **0** |
| Embedded faces | 3, all reporting `loaded` offline |
| Body text at 720p | **17.3 px** (26 design units × 0.667) on *Buy frequency before bikes*, over 3 sampled slides — clears the 16 px floor |
| Two-resolution diff, non-text boxes | **40 values at 3840×2000 vs 1280×634; worst disagreement 0.00 design units** |
| Two-resolution diff, text runs | 84 values, worst **1.07 design units** on an SVG mono-label height |
| Reflow at 320 CSS px | `scrollWidth` **320**, zero elements overflowing, zero internal scrollers |
| Reflow auto-engage | correct at all four sweep viewports, including 1280 × 400 (scale 0.37) |
| Reading-view type | 4 of 4 roles scale with the root font size (WCAG 1.4.4) |
| Smallest interactive target | **43.3 CSS px** at 1622 × 1054; zero targets under the 24 px floor |
| Chrome | **5 labelled or interactive items, 52 design units tall** — was 23 and 96 before T-028, and 11 until T-035 replaced seven stage names with one ruler, which DS-217 counts as a single item |
| Encodings of position | **2** — the ruler and the slide counter — and they answer different questions (DS-216 permits a second only then) |

**Both two-resolution figures come from a four-slide sample**, not the whole deck: slides 1, 5, 8
and 12, chosen to span the archetypes. `contract.py` names the sample in its own source and it is
a compromise, so a larger figure quoted elsewhere for the same rule is a different run over more
slides rather than a contradiction.

The layout is identical across a 3.15× scale ratio: every box lands on the same design-unit
coordinate. The 1.07-unit disagreement is text, and it is glyph-advance rounding rather than
layout, since a run's width, position *and* height all shift as glyphs round to device pixels. A check
demanding exact equality would fail every deck that contains text.

*The first two rows were measured for the first time on 2026-08-07.* Until then the probe carried
nine keys and **all nine were text runs**, so the earlier line here, *384 values, positions agree
to 0.09*, described text placement under a heading that said geometry, and DS-063's non-text
tolerance had never had a value in it (**L-36**).

---

## The seeded-defect deck

[`docs/EVALUATION.md`](../docs/EVALUATION.md) §7: *a rubric that has never been tested is a rubric
that passes everything.* This file is the test. It is generated, never hand-edited:

```bash
python tools/examples/seed_defects.py
```

It **derives** from the reference deck, so everything except the seeded defect is held constant and
the rubric's response is attributable to the defect rather than to two decks differing in a hundred
ways. Every edit asserts that it matched; a seed that silently no-ops would produce a deck with
fewer defects than this ledger claims.

**That claim is only true while the file is regenerated**, and it has twice stopped being true:
once before T-028 and once before [T-044](../tasks/T-044-restore-the-seeded-defect-fixture-and-its-claims.md),
by which point the fixture was four reference-deck revisions behind and differed from its parent in
601 lines. It is no longer left to habit. **`seed_defects.py --check` fails if the committed fixture
is not what regenerating would produce**, and `check.py` is not the gate that notices, because the
stale fixture passed every gate in the repository the whole time it was wrong.

### The ledger

| Dim | Seeded defect | Where |
| :--- | :--- | :--- |
| **S1** Claim | The headline becomes a topic label — "Wait times". The slide asserts nothing. | Single Number slide |
| **S2** Evidence | A modelled projection is restated as observed fact, and the assumption marker that qualified it is deleted. | Trajectory slide |
| **S3** Encoding | The before/after network diagram is replaced by four cards joined by arrow glyphs. | Before / After slide |
| **S4** Density | The sentence that decides the slide is moved into tier two, so the argument only completes once something is opened. | Ledger slide |
| **S5** Craft | One panel's type is set to 11 design units, below the 18-unit floor, and another panel is knocked 17 units off its grid track. | Small Multiple slide |
| **S6** Motion | The aside gets a looping ambient pulse that encodes nothing. | Uncomfortable Truth slide |
| **D1** Spine | Slides are reordered so the comparison opens the deck and the Why-Now arrives ninth. The sequence stops retiring objections. | whole deck |
| **D2** Pacing | The small multiple is split across three near-identical slides. Same archetype three times, length set by dumping. | whole deck, now 14 slides |
| **D3** Close | The ask becomes a recap and a thank-you. | Close slide |
| **D4** Consistency | The reserve is restated as $2.2M, contradicting the $1.5M the ledger established. | Gate slide |

### What the mechanical gate caught

`python tools/deck/check.py` over both decks. The good deck reports **0 failures**; the seeded deck
reports **4**, across **3 of the 10 dimensions**:

| Dim | Good deck | Seeded deck | Rule that fired | Caught |
| :--- | :--- | :--- | :--- | :--- |
| **S3** | reflow `scrollWidth` 320 | **851** | DS-075 | **only as collateral** — see below |
| **S5** | 0 runs below the floor | **12 runs at 11 units** | DS-035 | yes |
| **S6** | 0 looping motions on static content | **1**, at 2400 ms | DS-142, DS-141 | yes |
| S1, S2, S4, D1, D2, D3, D4 | — | — | — | **no** |

**Seven of ten seeded defects are invisible to every check in this repository.** Five of them are
`judge` rules and `EVALUATION.md` predicts exactly that. **The other two are not, and they are the
ones worth knowing about:**

- **D2, and 14 slides passes.** DS-081 only forbids *fewer than six*. DS-082 is the rule that says
  past 12 needs a recorded reason, and it is `default` and excused by the gate in writing, because
  *"past 12 needs a recorded reason"* is not a fact the HTML records.
- **D3, and a close slide reading *Thank you* passes.** Nothing measures whether the last slide asks
  for anything. DS-203 and DS-205 check that a bottom line exists and is not behind a disclosure,
  and the seed leaves both true while replacing the ask with a recap.

**And the two failures the ledger does not claim are collateral, not seeder bugs.** Both were
traced to a single seed:

| Extra failure | Caused by | Why |
| :--- | :--- | :--- |
| **DS-075** — reflow `scrollWidth` 851 at 320 CSS px | the **S3** seed | The card row is a four-item flex row with `flex:1` and no wrap, so at 320 px it cannot compress below its content and the reading view scrolls sideways. Verified by applying the S3 seed alone: 320 → 851 |
| **DS-141** — a duration over 500 ms outside DS-140's vocabulary | the **S6** seed | `seededThrob` runs at **2.4 s**, so the same animation trips both the *looping motion on static content* rule and the duration cap |

They stay out of the ledger deliberately: the ledger is **one seeded defect per dimension**, and
adding a row for a rule that fires as a side effect would break the property that gives the fixture
its evidential value. DS-075 is worth noticing on its own account, though. It says the S3
anti-pattern is not only a worse encoding but an accessibility failure, found by a rule aimed at
something else entirely.

**One thing the S3 seed exposed, and the fixture is the only deck that could.** It replaces the
deck's only dashed `Current` flow, so DS-140's subject stops existing, and until
[T-051](../tasks/T-051-a-check-with-no-subject-must-not-report-a-pass.md) the rule **passed on its
own absence**, reporting *"no dashed flow in this deck"* beside the same `pass` the conforming deck
earned. It now reports `NO SUBJECT`, the rule falls to `SILENT`, and the seeded deck's account reads
**77 checked, 1 silent** against the good deck's 78 and 0:

```
  checked               77
  SILENT                 1   DS-140
      of which NO SUBJECT  DS-140
```

That is not one of the ten seeded defects and is not counted among the four failures. It is the
gate declining to make a claim, which is the point. **This is what a fixture built to be missing
things is for**: no deck that has everything can show a check passing on nothing.

**The gate is necessary and nowhere near sufficient**, and this is sharper than the earlier count
suggested: a pipeline stopping at the gate would ship a deck whose headline is a topic label, whose
figures disagree with each other, whose slides are ordered by topic, whose length was set by
dumping, and which ends by thanking the room instead of asking it for anything.

---

## Reproducing the measurements

The deck is built by hand. Everything asserted about it above is reproducible. **Start here**, since the
gate subsumes the first three commands below and adds the coverage account:

```bash
python tools/deck/check.py examples/reference-deck.html
```

It runs the auto gate, the contrast audit, the render gate and the resolution contract in one pass,
then declares what it did **not** check: 82 of the 113 rules a gate owns are decided, and the other
31 are named with a reason each. The four commands after it still exist because each is useful
alone. `audit.py` and `contract.py` are for when you want one stage's output without the account, and the
two variant suites are separate because they build decks rather than read one.

```bash
python tools/deck/audit.py examples/reference-deck.html
```

```bash
python tools/deck/render.py measure examples/reference-deck.html
```

```bash
python tools/deck/contract.py examples/reference-deck.html
```

```bash
python tools/deck/contract_variants.py
```

```bash
python tools/deck/deliverable_variants.py
```

```bash
python tools/examples/seed_defects.py
```

`audit.py` runs the auto gate, the contrast audit, the render gate and the resolution contract:
**83 verdict rows against 77 distinct `DS-nnn` rules**, some rules carrying more than one row.
`contract.py` is that last stage on its own. It sweeps four
viewports and two resolutions, because §2.4 and §2.5 are claims about what happens *between*
viewports and no single render can decide them. **`contract_variants.py` and
`deliverable_variants.py` break each of those rules on purpose and require the gate to notice.**
A check that has only ever passed is not evidence that it checks anything, and three of the
resolution checks were caught measuring nothing the first time they ran. The second suite covers
the deliverable and chrome rules (DS-202, DS-203, DS-205, DS-216, DS-217), which were written with
`auto` and `render` labels and then went a whole task unenforced. `render.py measure` produces the
720p and two-resolution numbers. `render.py shots`
writes one PNG per slide so the deck can be *looked at*, which is the check none of the others
replace. Both drive **real Chrome with a clean throwaway profile and every DNS lookup black-holed**,
because a preview pane is not a faithful `file://` environment: it allowed a local `fetch()` that a
real restricted origin denies, and it drew a diagram as broken whose DOM geometry was correct to the
pixel (**L-06**, **L-15**).

Running `check.py` over both decks is what produced the table above: the good deck reports **0
failures**; the seeded deck reports **4**, spread across three dimensions, and the other seven
seeded defects are invisible to it.

```bash
python tools/examples/seed_defects.py --check
```

Regenerates into a temporary file and compares it with the committed fixture, so a reference deck
edited without regenerating is a red run rather than a discovery two audits later.

---

## The generated deck

[`sort-window/`](sort-window) holds all four artifacts a build run leaves behind: the deck, the
foundation spec with its outline, the slide-by-slide specification, and the sources the figures were
reconciled against. It is **252 KB in one file**, 258 211 bytes, 12 slides, six hand-written SVG figures, ten
disclosure panels, zero external references.

```bash
python tools/deck/check.py examples/sort-window/sort-window.html --sources examples/sort-window/sources
```

That runs the content half as well as the presentation half, which is the point of keeping the
sources: `0 failure(s)`, `82 checked`, and the figure ledger reconciled against three model
documents. Two more checks belong to this deck and not to the hand-built one:

```bash
python tools/deck/shell.py check examples/sort-window/sort-window.html
```

The half nobody rewrites is still the shipped shell, and this is the check that notices when a batch edit
strayed out of the slides. The print mode counts **13 pages, 12 slides plus a contents sheet**,
under `--print-pages`.

### The sources open inside the deck

Click a source in any provenance mark and the document opens over the slide. All three are in the
file: Marnfield's service calendar, its throughput model, its fleet and cost model. They open with
the network off, on a machine that has never seen the folder they came from. Press `Escape`, or
move to the next slide, and you are back in the argument. It works in the reading view too, which is
where someone reads the deck alone.

They cost **9 556 bytes, 4.1% of the file**. That is what three Markdown documents come to once
rendered; you can see the arithmetic before committing to it:

```bash
python tools/deck/quickview.py list examples/sort-window/sort-window.html
```

Nothing is embedded unless you ask for it by name. `quickview.py plan` prints what each source would
add and what the deck would weigh, and writes nothing at all. The version that writes is `add`. A
deck built from a client's internal document would carry that document to everyone who receives the
deck, and no amount of convenience is worth making that the default.

Each quick view says what it is in its own header: a rendering carried in the deck, not the original
file. A source that arrives as HTML has its scripts, styles and ids taken out before it goes in, and
the run tells you how many of each it removed.

**What the batch loop caught that a final pass would not have.** The specification failed DS-091 on
nine of twelve headlines and DS-092 on four bottom lines, and both were found and rewritten *before
any HTML existed*. After that, three defects came out of looking at rendered slides rather than out
of any check: a figure label set in paper on a `--data-quiet` fill at 2.6:1, exit text clipped by the
stage edge, and a delta arrow drawn across the time axis instead of along it. **The gate saw the
first one. Nothing but a person saw the other two.**
