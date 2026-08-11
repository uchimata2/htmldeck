---
id: T-069
title: Extend the provenance mark to multiple sources, and decide where deck-wide sources go
type: decision
status: done
phase: review
parent: null
blocked_by: []
related: [T-016, T-070]
work_package: v0.2
owner: the project owner
business_value: high
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables: [docs/DESIGN-SYSTEM.md, docs/COMPONENT-CONTRACT.md, shell/components.css, shell/deck.js, tools/deck/audit.py, examples/reference-deck.html]
---

# T-069 — Extend the provenance mark to multiple sources, and decide where deck-wide sources go

## 1. Specify

**Outcome**
`DS-105` and the `.provenance` component carry **more than one source per slide**, and a deck-wide
source that belongs to no single slide has a stated home. What exists today handles exactly one
source and says nothing about the rest.

**Why this one**
Requested by the owner on 2026-08-10. **Most of the request is already a rule** — DS-105 puts the
mark upper-right, requires a working link where sources are reachable and plain text where they are
not, and forbids a dead link; `COMPONENT-CONTRACT.md` §3 contracts `.provenance` as a `p` inside
`.slide`, cardinality exactly `1`, author-supplied; the reference deck carries twelve. So this task
is the delta, and the delta is four things, three of which collide with a rule already in force.

**The delta**
1. **Multiple sources behind a disclosure** — an icon opening a box, one linked title per source.
   Nothing today: the cardinality is exactly `1` and the element is a paragraph.
2. **A link affordance on the title.** Constrained rather than free: **DS-112 forbids a hand-drawn
   icon and DS-113 allows only glyphs the sprite carries.** The sprite has no `link` and no
   `external-link`. It does carry `arrow-up-right`, which is Lucide's conventional external-link
   mark, and `file-text` for a document. Either is legal; a new glyph means adding it to the sprite
   and is a DS-113 question, not a free choice.
3. **A deck-wide source lands on the last slide if it was not cited earlier.** This is the collision
   below.
4. **The link target may be a local file, an external URL, or an embedded quick view.** The quick
   view is its own capability and its own task —
   [T-070](T-070-the-quick-view-for-a-source-document.md) — because it is a build-mode feature
   rather than a rule. **The local-file case is settled here**, because it is a rule question:
   see *Decided*, below.

**What it collides with**
- **DS-085** — *"The last slide is a **close, not a recap**: the ask as one action."* Putting a
  source list on the last slide contradicts it directly. This needs a decision, not a workaround.
- **DS-230** — tier-two disclosure is **four closed kinds** (`derivation`, `scope`, `condition`,
  `instances`), and *"content whose subject the face does not carry is a slide, not a panel"*. A
  multi-source box is arguably none of the four, and a deck-wide bibliography's subject is not on
  the close slide's face. So either the source box is **not** a `.disc` and is its own component, or
  DS-230 gains a fifth kind — which DS-000 says is a ruleset change with a stated reason, never a
  value invented in one deck.
- **`COMPONENT-CONTRACT.md` §3** — `.provenance` is cardinality exactly `1`. Any multi-source form
  changes that row, and **DS-229** requires every class the shared style block styles to have one.

**What is already true and must not regress**
- **The gate checks presence, not reachability.** `check.py`'s triage for DS-105 reads *"the
  provenance mark is present on every slide; never a dead link is excused"*. So the half this
  request cares most about — that the link works — is the half nothing gates today. Whatever this
  task produces, *never a dead link* should stop being excused.
- **DS-223** already gives the provenance line print behaviour as an absolutely positioned
  descendant of a relative slide. A disclosure box inherits that problem and does not inherit its
  answer.

**Two things found while specifying, which change what this task has to produce**
- **Nothing in the repository cites a source, and both decks could.** `examples/sources/` and
  `examples/sort-window/sources/` each hold **three** source documents, and
  `check.py --sources` already reconciles every figure on a slide against them — but all twenty-four
  provenance marks read `Illustrative model` and not one names a document. So DS-105's *working link
  where sources are reachable* clause has **no instance anywhere**, and the multi-source case has no
  subject either. `check.py`'s DS-105 triage says *"there are no links to test, **DS-001 having
  banned them**"* — which is the misreading *Decided*, below, corrects: DS-001 is about **rendering**,
  and an anchor renders offline. The excuse has to go whether or not a link is ever added.
- **A colophon slide fails the component gate as markup, not as content.** Five
  [`COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.2 rows are `Count 1` per `.slide` —
  `.eyebrow`, `.headline`, `.body`, `.bottom-line`, `.provenance` — and
  [`tools/deck/component.py`](../tools/deck/component.py) enforces the count **per host slide**. A
  colophon *carrying sources and nothing else* is five failures the moment it exists. The owner's
  decision stands; what it costs was not stated, and it is the second open question below.

**Decided here, on rule 1's existing precedent**
**A `file://` link to a local source document is an authoring form, not a shipping one** — the same
status a CDN reference already has. `CLAUDE.md` rule 1 says a deck is one file that renders with the
network disabled and that the recipient double-clicks; a link into the author's own filesystem is
dead the moment the deck is emailed, and DS-105 already says *never a dead link*. So it is legal
while authoring and **a defect in a delivered deck, and the critique pass says so**, exactly as
`linked` mode is today. An external URL stays legal: it needs network to *follow*, not to *render*,
and DS-001 is about rendering.

**Decided while specifying — detail questions settled from the rules' own reasons, not carried to the owner**
- **No sprite change: `file-text` opens the box, `arrow-up-right` marks a source that leaves the
  deck.** Both are in [`shell/icons.svg`](../shell/icons.svg) already, so DS-112 and DS-113 are
  satisfied without a glyph being added, and delta 2's *"unless the decision requires one"* resolves
  to **no**. The split follows what each mark means: the control opens something **in** the deck and
  its subject is documents; only a link that actually navigates away earns the external mark.
- **`.provenance` keeps `Count 1`; what changes is what the mark may contain.** The multi-source
  component is the paragraph's content, not a sibling of it — which keeps the contract row untouched,
  keeps one mark per slide, and inherits **DS-223**'s print placement instead of needing a second
  answer to the same question. Recorded as an **assumption**: it survives being wrong at `plan`,
  where the alternative is `.provenance` dropping to `0-1` with the box as its sibling.
- **The dead-link check is written to what is decidable offline**: empty, `#`, `file://`, and an
  in-document fragment with no target are all failures a static check settles. Whether a live
  `https://` URL answers is not decidable from the file, and that half is **named in writing**
  rather than excused — the difference between a rule nothing checks and a rule whose unchecked part
  is stated.

**Scope**
- In: DS-105's text, the `.provenance` contract row, and whichever new component the multi-source
  form needs.
- In: the DS-085 decision, and the DS-230 fifth-kind-or-own-component decision.
- In: un-excusing *never a dead link* in the gate, to whatever extent a check can reach it.
- Out: the quick view — [T-070](T-070-the-quick-view-for-a-source-document.md).
- Out: adding a glyph to the sprite, unless the decision in delta 2 requires one; then it is in.
- Out: DS-102, which is about figures being sourced and is a different rule with a different subject.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-105, DS-085, DS-230, DS-112, DS-113,
  DS-223, DS-229, and DS-000 on what changing a rule costs.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3 — the `.provenance` row.
- [`shell/icons.svg`](../shell/icons.svg) — the 37 glyphs available without a DS-113 change.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — twelve marks in the shipping
  form, which is what any change has to keep working.

**Acceptance criteria**
- [ ] DS-105 states the multi-source form and names the component that carries it, and **the
      single-source plain-text mark stays conformant** — a one-source slide emits what it emits
      today. This extends the rule; it does not replace it.
- [ ] **DS-085 carries a named colophon exemption whose scope is written into the rule** — sources
      only, after the close, never a second ending — so a deck that grows an appendix behind it
      still fails. Amended under DS-000 with the reason recorded in the ruleset, not here.
- [ ] Every class the new form styles has a `COMPONENT-CONTRACT.md` row, and
      `python tools/deck/check.py <deck>` reports **no contract departure** (**DS-229**)
- [ ] The gate **fails** a provenance link that is empty, `#`, `file://`, or an in-document fragment
      with no target — and `check.py`'s DS-105 entry no longer claims *there are no links to test,
      DS-001 having banned them*. Either it checks, or it names live `https://` reachability as the
      one part no offline check reaches, with that reason.
- [ ] `python tools/deck/check.py examples/reference-deck.html --sources examples/sources` is green,
      and so is `tools/deck/critique.py --self-test` and `tools/plugin/check_scaffold.py` — the
      seeded-defect twin included, since it is derived from the deck this task moves
- [ ] **The reference deck cites its three source documents**: every slide's mark names what its
      figures came from, the multi-slide case uses the new form, and the colophon lists all three.
      No `href` anywhere in it, and DS-082's *past 12 needs a recorded reason* is answered in the
      deck for the thirteenth slide.
- [ ] **The reference deck has been opened and looked at, offline**, and printed: the box does not
      scatter across a page break (**DS-223**) and the colophon prints as one page.
      `examples/reference-deck.pdf` and the README's figures are regenerated to match

**Open questions**
- None. The four that existed are below, all answered by the owner.

**Settled**
- **Settled 2026-08-10 by the owner — the reference deck is the carrier.** The slides drawing on two
  or more of `examples/sources/`'s three documents get the box, and the colophon lists all three.
  **Plain text, no `href`, until [T-070](T-070-the-quick-view-for-a-source-document.md) lands the
  quick view** — which is what keeps *never a dead link* true of a deck that is emailed, and what
  makes the linked form T-070's demonstration rather than this task's. DS-102 is satisfied without
  special pleading: the sources **are** the illustrative model, not a real study quoted from memory,
  which is exactly the provision DS-102 writes for an illustrative deck.
  **What moves with it, and belongs in `plan` rather than being discovered at `implement`:**
  `examples/reference-deck.html`, `examples/reference-deck.pdf`, the seeded-defect twin derived from
  it, and the README figures `tools/docs/figures.py` gates. **And the deck becomes thirteen slides**
  — DS-082 defaults to 8–12 and *past 12 needs a recorded reason*, so the colophon exemption has to
  be that recorded reason, in the deck. It is `default`, not `hard`, so this is a reason to write
  down and not a rule to amend.
- **Settled 2026-08-10 by the owner — the colophon is an ordinary slide.** It keeps the five
  standard parts, and *"sources and nothing else"* binds its **content**: no new argument, no second
  ending, judged by the critique pass. **No contract row moves and no tool changes** — the rejected
  alternative was a `.slide--colophon` modifier dropping those five rows to `0-1`, which would have
  needed conditional cardinality in [`tools/deck/component.py`](../tools/deck/component.py) and would
  have handed every future slide kind the same argument to make. DS-085's exemption stays one
  sentence in the ruleset. It is a colophon and **not an appendix**: naming it one would pull it
  under DS-087, which is a different rule about a different thing.
- **Settled 2026-08-10 by the owner — a deck-wide source goes on a colophon slide *after* the close,
  exempt from DS-085 by name.** DS-085 keeps its rule and its subject: *the last slide is a close,
  not a recap* is a statement about where the **argument** ends, and a colophon is not part of the
  argument. So the amendment is an exemption naming the colophon, not a weakening of the rule — and
  the ask stays the last thing an audience is asked to act on, which is the property DS-085 exists
  to protect. Under DS-000 this is a ruleset change and carries this reason.
  **What the exemption must not become:** a second ending. The colophon carries sources and nothing
  else, or DS-085 has been repealed by the back door and every deck grows an appendix.
- **Settled 2026-08-10 by the owner — the multi-source box is its own component, not a `.disc`.**
  DS-230's four kinds (`derivation`, `scope`, `condition`, `instances`) describe an argument's tier
  two, and **provenance is not an argument** — it is what the argument rests on. Bending the
  vocabulary to admit it would cost the closed-vocabulary property that stops *behind the click*
  becoming *wherever it did not fit*, which is the whole reason DS-230 is closed. A separate
  component also keeps DS-230's gate honest: a source box counted as a panel would appear in every
  tier-two census and make the panel-kind distribution meaningless.

## 2. Plan

**Ordered so the two steps that could invalidate the rest come first.** The ruleset decides what the
component is allowed to be, and the contract decides what it must look like in markup; building
either before those are written is how a value gets invented in one deck, which is what DS-000
forbids.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Amend DS-105 with the multi-source form and the component that carries it, and DS-085 with the named colophon exemption. Both under DS-000, with the reasons in the ruleset rather than in this task. | Two amended rows in `docs/DESIGN-SYSTEM.md` |
| 2 | Contract the component before it exists, so DS-229's completeness half is satisfied by construction rather than remembered. | Six new rows in `docs/COMPONENT-CONTRACT.md` §3 |
| 3 | Build it in the shell, so a deck the pipeline generates can emit it and not only the deck edited by hand. | A `.sources*` block in `shell/components.css`; the toggle and its precedence in `shell/deck.js` |
| 4 | Check *never a dead link*: every `href` inside a provenance mark, judged against what a static read can settle. Rewrite `check.py`'s DS-105 entry from an excuse into a verdict plus the named part no offline check reaches. | A new verdict row in `tools/deck/check.py`, and one fewer undecided rule in its account |
| 5 | Cite the sources in the reference deck: eight marks name one document, four carry the box, the sprite gains the glyph, and the shared style block gains the component. | `examples/reference-deck.html` |
| 6 | Add the colophon as slide 13, carrying DS-082's recorded reason in the file — the rule permits past twelve *on a reason*, and the gate's own account says that reason is not in the HTML at all today. | `examples/reference-deck.html` |
| 7 | Propagate to the seeded-defect twin, so the proof of what the gate cannot see still runs against the deck it was derived from. | `examples/reference-deck-seeded-defects.html` |
| 8 | Regenerate the PDF and the README's figures, which are derived from the deck and go stale the moment it changes. | `examples/reference-deck.pdf`, and the README values `tools/docs/figures.py` gates |
| 9 | Open it and look — offline, then printed. | The observation recorded in §3, which is `implement`'s exit criterion |

**The shape, and what was rejected**
- **The box is `<span>`s inside the `.provenance` `<p>`.** A `<div>` inside a `<p>` is closed by the
  HTML parser, which would move the box out of the mark **silently** — the deck would look right in
  the file and be wrong in the DOM. Rejected: promoting `.provenance` to a `<div>`, which changes the
  contract row for all twelve marks and for every deck that already has one.
- **The component is `.sources*`, named in parallel with `.disc*` and separate from it** — the
  owner's settled decision, and the naming makes the parallel legible without making it a `.disc`.
- **The glyph is `file-text`, added to the sprite as `i-source`.** `arrow-up-right` is **not** added:
  nothing in this deck links out, and DS-113 says the sprite carries only the icons used. It goes in
  when the first deck links out, which is [T-070](T-070-the-quick-view-for-a-source-document.md).
- **The source box shares the disclosure precedence rule** — opening one closes any open panel and
  vice versa (DS-137) — while staying outside DS-230's census. A reader has one attention; the census
  is about what tier two is for. Those are different questions and only the second was decided.

**Output paths**
- `docs/DESIGN-SYSTEM.md`
- `docs/COMPONENT-CONTRACT.md`
- `shell/components.css`
- `shell/deck.js`
- `tools/deck/check.py`
- `examples/reference-deck.html`
- `examples/reference-deck-seeded-defects.html`
- `examples/reference-deck.pdf`
- `README.md`

## 3. Implement

**Decisions & assumptions**
- **`DS-001`'s check had to be narrowed, and that — not DS-001 — is what had banned links.** The
  seeded variant proved it: a `file://` link in a provenance mark failed **DS-001**, not DS-105, so
  the new check could never have fired on a real one. DS-001's predicate swept every `href` in the
  file, while the rule it implements enumerates *fonts, icons, scripts and styles* — subresources
  the renderer fetches. An `<a>` is not one. **The exemption is cut to exactly the width of the rule
  that takes over**: only anchors inside a provenance mark, because DS-105 judges those and
  `provenance_verdicts` fails a dead one. An `<a href>` anywhere else in a deck still fails DS-001.
  *This was not in the plan, and the plan could not have found it — only seeding the defect did.*
- **The check reads anchors, not every `href`.** A bare sweep counted the `<use href="#i-source">`
  that draws the mark's own glyph, and reported `1 of 1 examined` on a deck with no links in it —
  making dishonest the exact denominator the row exists to keep honest (**L-36**).
- **The single-source mark is unchanged plain text, and eight of the thirteen marks are one.** What
  the rule gained is a second form, not a replacement.
- **The title slide's mark carries two lines** — `Illustrative model` over `Cost model`. DS-102
  requires the deck to say its subject is illustrative, and a reader who never reaches the colophon
  must still be told, on the one slide everybody sees.
- **The colophon's stage is its own** (`Colophon`, an eighth entry in `STAGES`). Leaving it on `The
  ask` would have had the ruler tell the room the colophon is part of the argument, which is the
  precise thing DS-085's exemption says it is not. DS-217's budget is unaffected: a ruler is one
  item however many stages it names.
- **Assumption from `plan`, held:** `.provenance` kept `Count 1` and the box became the paragraph's
  content rather than its sibling. It inherited DS-223's print placement for free, and the print
  rules below then made even that moot.

**What looking at it found, which no gate did** — three defects, all in rendering:
1. **The colophon's icons filled the figure.** A nested `<svg class="icon sm">` inside `svg.fig` has
   no intrinsic size, so each one scaled to the viewport: one enormous glyph across the middle of
   the slide. Fixed with an explicit `width`/`height`/`viewBox` on each.
2. **The source box rendered as inline debris in the reading view.** On the stage it is absolutely
   positioned, so it computes to a block whatever its element is; static in `.doc`, a `<span>` falls
   back to `inline` and paints its padding and background in fragments across the line boxes.
   `display:block` in the `.doc` rule.
3. **The reading view never opened it.** `buildDoc` opens `.disc-panel` for DS-073 and knew nothing
   about a second component; the box travelled shut, so the reading view showed a hidden list behind
   a control it also hides. Both halves fixed.
- **Print inverts the disclosure's ruling, for the disclosure's own reason.** T-032 hides `.disc`
  entirely on paper because *a control the reader cannot click advertises what it cannot reach* —
  which applies to a `3 SOURCES` button exactly. But three titles fit under the mark where a ten-row
  panel did not, and paper is where provenance matters most: **the button goes and the list stays**,
  set static in the mark's own type. Static also settles **DS-223** for this component — nothing
  absolutely positioned means nothing to scatter across a break.

**Deviations from the plan, reported rather than decided back**
- **`examples/reference-deck.pdf` is not an output.** `.gitignore:18` excludes `examples/*.pdf`; the
  PDF is a local artifact, so it was printed and looked at, not committed. The plan listed it in
  error.
- **Four files the plan did not name were required**: `docs/THEME-CONTRACT.md` and both themes (the
  box needed a width token, and a `var()` with no declaration fails DS-013);
  `tools/deck/static_variants.py` (the seeded proof, which is where the DS-001 finding came from);
  and `examples/sort-window/sort-window.html`, which is held to the same token contract.
- **A defect was raised and withdrawn.** `shell/components.css` appeared to carry a corrupted comment
  opener that would swallow the rule beneath it; the mechanism was right and the character was not
  there — a search tool's escaping, not a byte. T-072 was deleted and the trap recorded as
  **L-56**.

**Outputs produced**
- `docs/DESIGN-SYSTEM.md` — DS-105 extended, DS-085 amended with the named colophon exemption
- `docs/COMPONENT-CONTRACT.md` §3.2 — six rows, and why the box is spans inside the `<p>`
- `docs/THEME-CONTRACT.md`, `themes/lattice.css`, `themes/quarto.css` — `--sources-box-w`
- `shell/components.css`, `shell/deck.js` — the component, its toggle, its reading view, its print
- `tools/deck/audit.py` — `provenance_verdicts`, and DS-001 narrowed to its own rule
- `tools/deck/check.py` — DS-105 wired in and struck from the excused list
- `tools/deck/static_variants.py` — two seeded dead links, both caught
- `examples/reference-deck.html` — thirteen cited marks and the colophon
- `examples/reference-deck-seeded-defects.html` — regenerated from it
- `docs/LESSONS.md` — L-56
- `README.md` — the three figures the deck's growth moved

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-105 states the multi-source form and names its component; the single-source mark stays conformant | met | Eight of thirteen marks are still plain text and unchanged in form |
| DS-085 carries a named colophon exemption, scoped in the rule | met | *Sources and nothing else*, and *colophon not appendix* are both in the rule, not beside it |
| Every new class has a contract row, and `check.py` reports no contract departure | met | `DS-229 · 74 styled, 0 uncontracted` |
| The gate fails a dead provenance link, or names what it cannot reach | met | Two seeded variants caught; `http(s)` reachability is named in the row's own text and printed every run |
| `check.py --sources` green, with the critique and scaffold self-tests and the seeded twin | met | `0 failure(s)`, `24 of 24`, `12 of 12`, `14 of 14`; twin regenerated and `--check` clean |
| The reference deck cites its three source documents, no `href`, DS-082's reason in the deck | met | Mapping taken from `content.py`'s ledger, not invented; the reason is in the colophon's own comment |
| Opened and looked at offline, and printed: no scattering, colophon one page | met | Three rendering defects found this way and fixed; 14 pages counted, pages 6 and 14 looked at |

**Child fix tasks raised**
- none. [T-071](T-071-the-intermediate-specifications-carry-their-references.md) is unblocked by this
  and was raised before it, not from it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (no change) | **N-1's origin, from the first external deck**, routed by [T-092](T-092-product-feedback-from-the-first-external-deck.md). This task gave the mark multiple sources and left them as slugs, deliberately and with the linked form assigned to [T-070](T-070-the-quick-view-for-a-source-document.md). Real use says the slug alone does not serve a reader who is not the author: `D5 section 2` names a document they cannot identify. The need is recorded against T-070, which owns it; it is noted here because this is where the shape of the mark was decided, and the two rules that now block a better line - **U-01** and **U-02** in [`../docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) section 2.2 - are both about that shape. |
| 2026-08-10 | → done | All seven criteria met. **The finding that mattered came from seeding the defect, not from writing the check**: a `file://` link in a provenance mark failed **DS-001**, so the new check could never have fired — DS-001's predicate swept every `href` while the rule it implements enumerates subresources, and *that*, not the rule, was what the old excusal meant by "DS-001 having banned them". Narrowed to anchors inside a provenance mark and no further. **Three more defects came from looking rather than from any gate** — nested icons with no intrinsic size filling the figure, the box rendering as inline debris in the reading view, and `buildDoc` never opening it — and the print treatment inverts T-032's ruling on the disclosure for T-032's own reason, since three titles fit under the mark where a ten-row panel did not. Deck at 13 slides, 82 of 113 rules checked, `0 failure(s)`. |
| 2026-08-10 | → planned | Nine steps, **ordered so the ruleset and the contract come before anything is built** — a component built first is a value invented in one deck, which is what DS-000 forbids. Three shape decisions recorded with what they rejected: the box is `<span>`s **inside** the provenance `<p>` because a `<div>` there is closed by the parser and the deck would be wrong in the DOM while looking right in the file; the sprite gains `file-text` and **not** `arrow-up-right`, since nothing links out yet and DS-113 carries only icons used; and the box shares the disclosure precedence rule while staying outside DS-230's census, because *what a reader can have open* and *what tier two is for* are different questions. Found while surveying: a corrupted comment opener in `shell/components.css` swallows the rule beneath it — raised as **T-072**, not fixed here. |
| 2026-08-10 | → specified | **Both remaining questions answered by the owner, as recommended: the reference deck is the carrier, and the colophon is an ordinary slide.** So the rule ships with a subject rather than repeating DS-087's blind check, and it costs no contract row and no tool change. Two consequences were recorded rather than left for `implement` to find: the deck goes to **thirteen slides**, which DS-082 permits on a recorded reason that the colophon exemption supplies; and the deck's PDF, its seeded-defect twin and the README figures move with it. Seven acceptance criteria, agreed. |
| 2026-08-10 | (specify) | Criteria sharpened and **two findings raised that the earlier pass missed**. First: **no deck in the repository cites a source**, though both ship three source documents and `check.py --sources` already reconciles figures against them — so DS-105's link clause and the whole multi-source case have no subject, and `check.py`'s excuse for not checking (*"DS-001 having banned them"*) rests on the misreading this task already corrected. Second: **a colophon slide fails the component gate as markup** — five contract rows are `1` per `.slide` and `component.py` enforces them per host — so the owner's settled colophon carries an unstated cost. Both became open questions and were **asked, not guessed**; `specify` stays open on them. Three detail questions were settled here instead of carried up, per their rules' own reasons: no sprite glyph is added (`file-text` opens, `arrow-up-right` leaves), `.provenance` keeps `Count 1` with the box as its content (assumption, revisited at `plan`), and the dead-link check is written to what a static read can decide with the rest named in writing. |
| 2026-08-10 | (specify) | **Both open questions settled by the owner**, as recommended: a colophon slide after the close carries deck-wide sources under a named DS-085 exemption, and the multi-source box is its own component rather than a fifth DS-230 kind. Both reasons are written into §1 — the exemption is scoped so the colophon cannot become a second ending, and the separate component keeps DS-230's panel census meaningful. Specify is not closed: the criteria still need agreeing. |
| 2026-08-10 | → proposed | Raised from an owner request for upper-right source referencing. **Recorded as a delta rather than as the request**, because DS-105 already puts the mark upper-right, already requires a working link or plain text, and already forbids a dead link — the reference deck carries twelve. What is genuinely new is multiple sources, the disclosure that holds them, and where a deck-wide source lives. **Three collisions named before any work**: DS-085 on the last slide being a close, DS-230's closed four-kind panel vocabulary, and the `.provenance` cardinality of exactly 1. The local-file link is settled here on rule 1's existing precedent rather than left open. `v0.2`: nothing shipped is wrong, and this is a capability rather than a defect. |
