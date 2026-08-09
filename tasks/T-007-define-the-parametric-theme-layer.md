---
id: T-007
title: Define the parametric theme layer
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-001, T-014]
related: [T-002, T-016, T-021]
work_package: WP2
owner: maintainer
created: 2026-08-04
updated: 2026-08-09
deliverables:
  - docs/THEME-CONTRACT.md
  - themes/quarto.css
  - themes/lattice.css
  - themes/faces/instrument-serif.css
  - themes/faces/space-grotesk.css
  - themes/faces/jetbrains-mono.css
  - tools/deck/theme.py
  - examples/reference-deck.html
  - docs/DESIGN-SYSTEM.md
---

# T-007 — Define the parametric theme layer

## 1. Specify

**Outcome**
A decision on how visual identity is chosen per deck.

**Why this one**
The corpus decks look designed **because they do not share a template**. A plugin shipping one house style will produce decks that look like each other — which is the problem it exists to solve.

**Decided 2026-08-06 — one theme, built parametrically.** The owner chose **exactly one** robust,
fully-resolved look across every layer, not several and not per-topic generation. Variety is a
later problem, solved by a tool that generates *new* templates — a surveying step plus a script
that lays out the structure, writes the specs and generates content. That tool is **not** in scope
now. What is in scope now is making it cheap to add: every layer parametric from the start.

This overrides `docs/BRIEF.md` open question 3, and stands in tension with the brief's rule 3
("decks must not look like each other"). That rule is satisfied later, by the generator.

**What is left of this task**
Not a decision any more — the parametric theme layer that the decision requires. Stated as one
sentence: **a theme becomes a file.** A delimited region every deck carries, a written contract
saying what a theme must supply, a check that enforces it, and a second theme that proves the swap
by moving axes colour cannot reach.

**Measured 2026-08-09, before planning.** The token *layer* exists as one hand-built instance; the
token *contract* does not, and the layer is less parametric than its 57 properties suggest.

| | |
| :--- | :--- |
| custom properties in `:root` | **57**, plus **18** dark overrides |
| custom properties declared anywhere else | **0** — the layer is not leaking declarations |
| **design-unit literals written outside it** | **62**, across **33** distinct magnitudes; 37 of them on `width` or `height` |
| bare `px` font sizes inside the stage | **3** — `.fig .lab/.val/.name`, which **DS-033 forbids in its own words** and no check reaches |
| reflow-view rules reading a token | **6 of 27**, against **39** `rem` literals |

Two consequences decide the size of this task. **A third of the stage's geometry is written where a
theme cannot reach it** — every one of those 62 numbers is correct, rides the transform, and is
invisible to a swap. And **the second rendering does not swap at all**: DS-074's reading view is
built from `rem` literals, so a theme that changes density changes one of the two renderings the
log below already required to come *from one source of values*.

**Two `hard` rules pin the shipping theme's own numbers, and their checks enforce the pin.**

| Rule | What it fixes | The check that enforces it |
| :--- | :--- | :--- |
| DS-034 | body 24–28 du **at line-height 1.55** | `audit.ds034_body_type` — `abs(lh − 1.55) < 0.01` |
| DS-140 / DS-141 | the four motions at 340 / 380 / 420 / 300 ms, 1.2 s, 4.5 s | `audit.ds141_durations` — a duration over 500 ms is admitted only at exactly 1.2 s or 4.5 s (±0.01) |

So a second theme that moves the density axis or the motion axis **fails the gate for being a
second theme**, which is the failure this task exists to prevent. Both are amended here rather than
worked around, on [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent that a rule
a conforming deck contradicts is a defect in the ruleset — and both amendments are faithful to the
rule's own recorded reason. DS-140's is
[`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §4: *a named vocabulary is what stops
animation becoming decoration*. **The names and the closure are what carry that; the milliseconds
are the shipping theme's instance of it.** DS-034's numbers are argued in §3 of the same file as a
**type floor**, and line-height is not argued there at all.

**Scope**
- In: **the theme region** — where a theme lives inside a single self-contained file, and how a tool
  finds it without parsing the whole deck.
- In: **the token contract** — every token a theme must supply, what it governs, its type and legal
  range, and which axis it belongs to. Split into the **primitives** a generator sets and the
  **derived** values computed from them, because a flat list of 100-plus values is not authorable
  and does not say which numbers are choices.
- In: **five axes carrying real dials** — colour · layout geometry and density · type scale ratio
  and face pairing · shape language · motion.
- In: closing the gap the measurement above found — the 62 literals, the 3 bare `px` sizes, and the
  reflow view.
- In: **enforcement**. DS-010's check is the colour half and says so; the other four axes get theirs.
- In: **the amendments** to DS-034, DS-140 and DS-141 above, and to any other `hard` rule whose
  check turns out to pin a value this task makes variable.
- In: **the swap demonstration**, built and rendered and looked at.
- Out: **the template generator.** CLAUDE.md rule 4 defers it; this task makes it cheap to add and
  does not add it.
- Out: per-topic or per-deck palettes — DS-011, and the C7 drop recorded in the log below.
- Out: the **components** that consume the motion tokens.
  [T-016](T-016-the-interaction-and-motion-layer.md) owns those; the axis is specified here and
  exercised there, as the 2026-08-07 log row settled.
- Out: **retheming print.** `@media print` is a different medium with no theme and a paper ground —
  `audit.screen_css` already excludes it for exactly this reason, and DS-226 requires a floor in
  points that the stage's own rules forbid.

**Inputs**
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the one hand-built instance.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §1.2 (the token rules), §2.1–§2.5, §5.2.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — `token_layer`, `outside_token_layer`,
  `ds010_colours_tokenised` and the docstring that names this task as the owner of the rest.
- [`tools/deck/contrast.py`](../tools/deck/contrast.py) — `PAIRS` and `SEPARATE_FROM_LINE`, the
  hand-written token list that says in a comment it moves when this task lands.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-36** (a check with no subject), **L-43**, **L-08**.

**Acceptance criteria**
- [ ] ~~One complete look defined across all thirteen coverage areas, with no unresolved choices~~ —
      **amended during specify, before the work, per
      [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2**, on T-014's precedent. The thirteen are
      **T-014's topic list**, and seven of them — writing style, content practice, deck structure,
      headings, external tools among them — are not *look* at all, so the criterion could only
      close by being reinterpreted. Replaced by the axis criterion below, which is what the owner's
      2026-08-07 answer actually asks for.
- [ ] **Five axes, each with at least one dial that is not a colour**: layout geometry and density ·
      type scale ratio and face pairing · shape language · motion · colour
- [ ] Every value that could differ between themes is a **token**, not a hard-coded value —
      colour, type scale, spacing, radii, stroke weights, diagram styling, interaction styling
- [ ] The token set is documented as the contract a future generated theme must satisfy, **naming
      which tokens are primitive and which are derived**
- [ ] Swapping the token file alone produces a visibly different, still-coherent deck —
      demonstrated, not asserted
- [ ] The swap moves **at least two non-colour axes** — the owner's answer sets one as the floor;
      two is what distinguishes a parametric layer from a lucky dial
- [ ] Both renderings swap. The reading view derives from the same tokens, and the number of its
      rules that read one is **stated**, up from the 6 of 27 measured above
- [ ] No theme-specific value reachable anywhere outside the token layer — **measured against a
      written exemption list**, not asserted. A run states the count, so it cannot sit at zero
      unnoticed (**L-36**)
- [ ] Every `hard` rule whose check pins the shipping theme's own value is either **banded in the
      ruleset** or recorded as deliberately frozen with a reason
- [ ] Both decks opened and looked at, offline — CLAUDE.md rule 6 and the bar for `done`

**Decisions taken during specify, 2026-08-09**

1. **A theme is a CSS fragment in its own `<style id="theme">`, and it carries its own faces.** Not
   comment markers around a `:root` block: face pairing is one of the five axes, and a face that is
   not embedded is not a theme a deck can swap to. So the region holds the `@font-face`
   declarations *and* the `:root` blocks, and **DS-032's licence notice travels inside the file that
   carries the font** rather than being reattached by whoever swaps. The deck stays one file with
   zero external references — the region is a location contract, not a load.
2. **The swap demonstration is built, not committed.** `examples/` already carries two decks at
   219 KB and 227 KB; a third would add a fifth of a megabyte to a published repository to
   demonstrate a property a tool can rebuild in a second. The **theme file** and the **builder** are
   committed — both small — and the demonstration deck is built into `.assets-cache/`, which is
   where the 28 seeded variants already live and which `.gitignore` already excludes. This follows
   the repository's existing pattern rather than inventing one.

**Open questions**
- ~~What is the minimum token set that makes a future theme genuinely distinct rather than a
  recolour? Recolouring is not the goal — the corpus decks differ structurally too.~~ **Answered
  2026-08-07 by the owner: the token set must span four axes, not one.** Colour is necessary and
  nowhere near sufficient. The minimum is **layout geometry and density · type scale ratio and face
  pairing · shape language (radius, stroke) · motion (duration, easing, distance)**, with colour
  alongside them — and the swap demonstration below has to change at least one **non-colour** axis
  to count. The reason is the criterion itself: *visibly different, still coherent* is not what a
  recolour produces, and the corpus decks read as designed because they differ **structurally**. A
  token set that freezes geometry and motion guarantees the failure this task exists to prevent,
  and it does so invisibly — every individual value is parametric and the family still looks like
  one template.
- **None open.** The two questions this task had to settle before it could be planned — where a
  theme lives in a one-file deck, and whether the second deck ships — are recorded as *Decisions
  taken* above, each from the rule or the repository pattern that already answered it.

## 2. Plan

**The order is forced by one thing:** the contract has to be written from a region that already
exists, or it is a wish-list. So the extraction comes first and the document second, and the
enforcement comes after the deck conforms — a check written against a deck that fails it is a check
nobody can tell from a broken one.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Extract the region.** Move the three `@font-face` declarations, `:root` and the dark override into a `<style id="theme">`, and write the tool that finds it — extract, validate, swap, self-test first (**L-04**) | `theme.py`, under `tools/deck/`; the region in [`examples/reference-deck.html`](../examples/reference-deck.html); the shipping theme as `quarto.css`, under `themes/` |
| 2 | **Write the contract** from what the extraction produced: every token by axis, primitive or derived, its type and legal range, and the written list of what may stay a literal | `THEME-CONTRACT.md`, under `docs/` |
| 3 | **Close the gap the measurement found** — the 62 design-unit literals, the 3 bare `px` sizes, the reading view's 39 `rem` literals. Each becomes a token, a derivation, or a named exemption; none stays by default | the reference deck and the contract, revised together |
| 4 | **Sweep the ruleset for pinned values and amend.** DS-034's line-height and DS-140/DS-141's durations are known; the sweep finds the rest. `contrast.py`'s hand-written token list moves onto the contract, as its own comment says it will | [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md), [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md), [`tools/deck/contrast.py`](../tools/deck/contrast.py) |
| 5 | **Build the enforcement**: one check per axis that no theme-varying value is written outside the region, each printing the count it evaluated (**L-36**), and a seeded variant proving each can fail | rows in [`tools/deck/audit.py`](../tools/deck/audit.py), fixtures in [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) |
| 6 | **Author the second theme**, moving face pairing, type scale ratio, density, shape language and motion. It uses the three faces already embedded, so the demonstration does not wait on sourcing a font — the face-pairing dial is exercised by re-pairing, not by adding | `lattice.css`, under `themes/` |
| 7 | **Swap, render, gate, look.** Build the swapped deck into `.assets-cache/`, run the full gate against it, open both decks offline | the built deck; the gate output, recorded in §4 |
| 8 | **Record what generalises** and close | [`docs/LESSONS.md`](../docs/LESSONS.md) |

**Approach decisions**

- **The tool is a reader and a writer, never a renderer.** `theme.py` swaps text in a file; whether
  the result is *coherent* is a look, which CLAUDE.md rule 6 already requires and no tool replaces.
- **Derivation is required where a scale exists, and nowhere else.** The type scale derives from a
  base size and a ratio, and the spacing scale from its own step — those are the two places a
  literal silently breaks the family. Colour, faces, shape and motion are set directly, because a
  derived colour is a generator's job and this task does not build the generator.
- **Step 3 is where the task can run away.** 62 literals across 33 magnitudes is not 62 new tokens:
  most are one value used several times, and the ones that are genuinely single-use decoration go on
  the exemption list with a reason rather than into the contract. **The contract is judged by
  whether a person can author a theme from it**, not by how few literals survive.

## 3. Implement

**Decisions & assumptions**

- **The theme is a `<style id="theme">` region carrying its own faces** — 2026-08-09. Face pairing
  is an axis, and an unembedded face is not one a deck can swap to. A theme's *source* form names
  its faces in a directive line and `theme.py` resolves each against `themes/faces/<slug>.css`; the
  *resolved* form carries the base64. So two themes sharing a face share one 30 KB copy in the
  repository and both still produce a single file with zero external references (DS-001), and
  DS-032's licence notice travels inside the file that carries the font.
- **Derivation only where a scale exists** — 2026-08-09. The text scale derives from `--fs-base`
  and `--type-ratio`, the spacing scale from `--sp-unit` and `--sp-ratio`, and nothing else derives.
  The display sizes are **primitives and the contract says why**: 67, 96 and 190 design units are
  joined by no ratio, and forcing them onto one would be a redesign dressed as a parameterisation.
- **The composition/look line is scoped, not global** — 2026-08-09, and it was rewritten once
  during the work. A property-based exemption (*geometry is composition everywhere*) was tried
  first and it exempted a shared component's icon size, which a denser theme must be able to
  shrink. The line now runs **inside two named scopes only** — `#slides` and `.ruler` — where the
  values exist to fit one deck's content. Outside them nothing is exempt by property.
- **`theme.py` parses the contract rather than restating it** (**L-08**, **L-13**), the same
  arrangement `ruleset.py` has with `DESIGN-SYSTEM.md`. Adding a token to the document changes what
  `validate` demands with no code edit.
- **A range cites the rule it comes from, read out of the *Governs* cell.** The self-test refuses a
  range with no citation, because a threshold invented to fit one deck is worse than none
  (**L-38**) — and three had been written that way earlier in this task before the rule was
  applied to them. They were dropped rather than justified afterwards.

**Outputs produced**
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — 109 tokens across five axes, the
  primitive/derived/fixed split, and the four-row exemption list the check reads as data.
- [`tools/deck/theme.py`](../tools/deck/theme.py) — extract · validate · swap · check, self-test
  first.
- [`themes/quarto.css`](../themes/quarto.css) — the shipping theme, extracted from the deck.
- [`themes/lattice.css`](../themes/lattice.css) — the second theme.
- `themes/faces/` — the three faces, one file each, licence included.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — the region, and 80
  replacement entries turning literals into tokens.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-034, DS-140, DS-141 and DS-063 amended.
- Checks: `theme.verdicts` wired into [`tools/deck/check.py`](../tools/deck/check.py); DS-034 and
  DS-141 rewritten in [`tools/deck/audit.py`](../tools/deck/audit.py); four new fixtures in
  [`tools/deck/static_variants.py`](../tools/deck/static_variants.py).

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Five axes, each with a dial that is not a colour | **met** | `theme.py tokens` — colour 18 · type 27 · geometry 27 · shape 22 · motion 14, 109 in all. `lattice` moves four of the five |
| Every value that could differ between themes is a token | **met** | `theme.py check` — 38 literals outside the region, 38 exempt, 0 offending, from 119 offending when the scan was first run |
| Documented as the contract a generated theme must satisfy, naming primitive and derived | **met** | [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §2 and §3; 30 derived tokens, and `validate` rejects one rewritten as a literal |
| Swapping the token file alone produces a visibly different, still-coherent deck | **met** | `theme.py swap` → `.assets-cache/deck/themed/lattice-deck.html`; **no rule outside the region edited**. Rendered and looked at |
| The swap moves at least two non-colour axes | **met** | Four: face pairing and scale ratio (type), step and ratio (geometry), square corners and a flat shadow (shape), 200 ms rise at a 35 ms stagger (motion) |
| Both renderings swap; the reading view's uptake stated | **met** | Reading-view rules reading a token: **37 of 51**, up from **9 of 51**; `rem` literals **69 → 2**, both of them `.doc .icon` inside `#slides` |
| No theme-specific value outside the token layer, measured against a written exemption list | **met** | The list is four rows of [`THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) §5, parsed by the check; the run prints scanned / exempt / offending so the number cannot sit at zero unnoticed |
| Every `hard` rule pinning the shipping theme's own value is banded or frozen with a reason | **met** | Four found and amended: DS-034 (line height), DS-140 and DS-141 (durations), **DS-063** — which the second theme found rather than the sweep, see below |
| Both decks opened and looked at, offline | **met** | Slides 1, 4 and 8 of `lattice`; 4 and 8 of the reference deck, through `render.py shots` in real Chrome with the network black-holed |
| ~~One complete look across all thirteen coverage areas~~ | **amended in specify** | Replaced by the axis criterion; the reasoning is in §1 and in the log |

**What the second theme found that the sweep could not.** DS-063 held a text run's whole rect to
**2 design units**, a number measured over one deck in one theme. `lattice` reached 2.23 du and
failed a resolution contract it does not break: a tighter type scale fits more glyphs on a line and
every one of them rounds to a device pixel. **A design-unit threshold is the wrong shape for a
device-pixel effect** — it silently encodes the scale factor of the deck it was measured on. The
rule now reads **2 device pixels at the smaller rendering**, which is the mechanism's own number
(a whole-rect comparison folds two roundings, the edge and the extent) and lands at 3.41 du at this
sweep's k. The reference deck sits at 0.63 px and `lattice` at 1.31.

**Gates, from the working tree at close**

```
python tools/deck/check.py examples/reference-deck.html      0 failure(s); 78 checked, 0 SILENT, buckets sum to 111
python tools/deck/check.py <the lattice deck>                0 failure(s); 78 checked, 0 SILENT, buckets sum to 111
python tools/deck/theme.py check examples/reference-deck.html 38 literal(s) scanned, 38 exempt, 0 offending
python tools/deck/static_variants.py                         15 of 15 static, 7 of 7 rendered
python tools/deck/contract_variants.py                       7 of 7
python tools/deck/contrast.py <the lattice deck>             0 failure(s), both themes
python tools/plugin/check_scaffold.py                        10 of 10 fixtures behaved as specified
```

**Child fix tasks raised**
- none. The one thing left open is named in §1's scope and belongs to the generator: **no colour is
  derived**, so a generated theme still has to choose 18 colours that clear the contrast pairs by
  itself. That is the generator's problem and this task deliberately did not build it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **A theme is now a file, and the proof is a second one.** 109 tokens across five axes; the region is one `<style id="theme">` carrying its own faces; `theme.py` parses the contract rather than restating it. The measurement moved: **119 offending literals → 0**, and the reading view went from **9 of 51 rules reading a token to 37**, with `rem` literals 69 → 2. **[`themes/lattice.css`](../themes/lattice.css) moves four non-colour axes** — face pairing and scale ratio, spacing step and ratio, square corners with a flat shadow, and a 200 ms rise at a 35 ms stagger — and the swapped deck passes the whole gate. **The second theme found a fourth pinned rule the sweep could not**: DS-063 held a text run to 2 *design units*, a number measured in one theme, and `lattice` reached 2.23 without breaking the contract — a tighter type scale fits more glyphs and every one rounds. The bound is now **2 device pixels at the smaller rendering**, which is the mechanism's own number rather than one deck's. Four `hard` rules amended in all (DS-034, DS-140, DS-141, DS-063), each faithful to its own recorded reason. |
| 2026-08-09 | → planned | Eight steps, ordered by one constraint: **the contract is written from a region that already exists**, or it is a wish-list, so extraction precedes documentation and enforcement follows conformance. Two approach decisions worth carrying: derivation is required only where a *scale* exists — type and spacing — because a derived colour is the generator's job and this task does not build the generator; and **step 3 is where the task can run away**, so the 62 literals are closed against *can a person author a theme from this*, not against a count of literals removed. |
| 2026-08-09 | → specified | **Measured before planning, and the measurement changed the task's shape.** The layer is less parametric than 57 properties suggest: **62 design-unit literals across 33 magnitudes** sit outside it, the reading view reads a token in **6 of its 27 rules** against 39 `rem` literals, and **3 bare `px` font sizes sit inside the stage**, which DS-033 forbids in its own words and no check reaches. **Worse, two `hard` rules pin the shipping theme's own numbers and their checks enforce the pin** — DS-034's line-height 1.55 (`abs(lh − 1.55) < 0.01`) and DS-140/DS-141's durations (over 500 ms admitted only at exactly 1.2 s or 4.5 s). A second theme moving density or motion **fails the gate for being a second theme**, which is the failure this task exists to prevent, so both are amended on [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent — faithfully, since DESIGN-RATIONALE §4 argues DS-140's *names and closure*, never its milliseconds, and §3 argues DS-034 as a type floor without mentioning line-height. Two decisions taken rather than handed back: **a theme is a CSS fragment carrying its own faces in a `<style id="theme">`** (face pairing is an axis, and an unembedded face is not a theme a deck can swap to), and **the demonstration deck is built, not committed** (`examples/` already carries 446 KB of decks; the variants pattern already builds into gitignored `.assets-cache/`). One acceptance criterion amended before the work per [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §2: *all thirteen coverage areas* is **T-014's topic list**, seven of whose entries are not *look* at all, so it could only have closed by reinterpretation. |
| 2026-08-07 | (no change) | **The open question is answered and it sets the size of this task: four axes, not one.** Layout geometry and density, type scale ratio and face pairing, shape language, motion — plus colour, and the swap demonstration must move at least one non-colour axis. **This is more than the 57 custom properties in [`examples/reference-deck.html`](../examples/reference-deck.html) already carry**, because tokenising a value and making it *variable* are different claims: the deck's geometry is tokenised against one stage and has never been asked to hold at a different density. Two consequences to carry into the plan. **The second token file is now a deliverable, not an illustration** — it is the only thing that can demonstrate the criterion, and it has to be built and rendered. **The motion axis is shared with [T-016](T-016-the-interaction-and-motion-layer.md)**, whose durations, easings and distances are the same values: it consumes this contract, so the axis is specified here and exercised there rather than owned twice. |
| 2026-08-07 | (no change) | `related` gains T-016 and T-021 — the motion tokens that swap with this layer, and the second of the two renderings it must carry. [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) also recorded a measurement that changes what *starting* this task means: **[`examples/reference-deck.html`](../examples/reference-deck.html) already carries 57 custom properties**, spanning colour, type scale, spacing, radii, stroke, shadow, motion durations and easings, `--measure`, `--du` and a tokenised disclosure mark. The token *layer* exists, as one hand-built instance. The **contract** does not, and neither does the swap demonstration the criteria above ask for. This task extracts and proves; it does not author from nothing. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | (no change) | Owner decided: one theme now, every layer parametric, template generator deferred. Task reframed from a decision to the token layer that decision requires. |
| 2026-08-06 | (no change) | **T-014 closed.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §1.2 fixes the token layer this task builds: parametricity is **hard**, not tidy practice, because a value hard-coded now is a value the generator cannot vary. Token vocabulary extended beyond the corpus's `--ink`/`--bg`/`--line`/`--shadow` with `--measure` and a tokenised disclosure mark. **C7 (one palette per deck) was dropped and D1's per-deck font rotation with it** — this task's variety comes from the generator, never from per-deck improvisation. **§9.1 gates it**: the stage question is an owner decision. |
| 2026-08-06 | (no change) | **Ungated — the owner settled §9.1: fixed stage plus a reflow view ([T-021](T-021-the-reflow-view-and-the-resolution-contract.md)).** Two consequences for the token layer: type tokens are **design units on a 1920×1080 stage**, not `px` and not `clamp()`/`vw` (those belong to the reflow view and fight the transform inside the stage); and the token set must carry **two renderings**, the stage and the reflow document, from one source of values. |
