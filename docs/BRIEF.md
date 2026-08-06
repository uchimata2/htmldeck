# htmldeck — brief

What to build, why it exists, and what the evidence says. Read `../CLAUDE.md` first.

---

## The problem

Asked for a presentation, agents reach for PowerPoint libraries or a Markdown slide framework.
Both produce something that looks like a template filled in. A single-file HTML deck can be
genuinely well designed — custom typography, real diagrams, considered layout — but building one
well takes a lot of prompting, and the result is not repeatable.

This plugin makes that repeatable: a **prompt structure** that produces good briefs, a **build
process** that produces good decks, and a **critique pass** that catches what is wrong before an
audience does.

---

## Evidence: what the corpus actually shows

Grounded in real decks produced across a training programme, not invented. **The authoritative
measurements now live in [R1](research/R1-corpus-conventions.md)** — 12 decks, 346 files, extracted
mechanically by `tools/kb/extract.py`. The sample below is the original hand-read estimate, kept
only to show what changed.

| Deck | Slides | Inline SVG | `<canvas>` | External refs |
| :--- | :---: | :---: | :---: | :---: |
| Data-strategy exam deck | 9 | 22 | 0 | 2 |
| Executive smart-factory deck | 16 | 6 | 0 | 7 |
| Product pitch deck | 11 | 12 | 2 | 6 |
| Data-architecture deck | 12 | 5 | 1 | 4 |

**What the good ones have in common**

- **Single file.** One `.html`, opens by double-clicking, e-mails as an attachment.
- **Section-per-slide.** `<section>` per slide; 6–16 slides. Under 6 is a memo, over 16 loses a
  board.
- **Diagrams are inline SVG, never images.** 5–22 per deck. They scale, they theme, they diff.
- **Typography carries the identity.** Bricolage Grotesque, IBM Plex Mono, Fraunces, Inter — a
  deliberate pairing per deck, driven by CSS custom properties. **The decks do not share a
  template**, and that is why they don't look generated.
  > **Contradicted 2026-08-06 by [R4](research/R4-prior-art.md).** Those faces are three rows of
  > the deck skill's own font-pairing table, and its instruction to rotate pairings and never
  > repeat one is where "a deliberate pairing per deck" comes from. Five of the seven typography
  > rules (D1–D6) are inherited. The decks not sharing a template is real; reading the *typography*
  > as the owner's signature is not. **Candidate change of direction for T-014:** if the type
  > choices are the skill's, the identity has to be carried by something else — and R4 §2 says
  > where the owner's taste actually concentrates.
  >
  > **[R5 §1](research/R5-assets-and-licences.md) adds a cost argument to the same conclusion.**
  > Of the four faces named above, **Inter is the most expensive and the least distinctive** —
  > 62.8 KB inlined, more than twice Instrument Serif, and the face every generated deck already
  > uses. If the pairing is inherited anyway, there is no reason to inherit the costly generic
  > half of it. R5 recommends Instrument Serif · Space Grotesk · JetBrains Mono at 97.3 KB.
- **Minimal JavaScript.** 1–3 script tags: keyboard navigation, progress, occasionally a chart.
  **This is an observation, not a target** — see "Decisions taken". Richness is now wanted.

> **Superseded 2026-08-06 by [R1](research/R1-corpus-conventions.md).** This section was written
> from a partial sample of ~10 decks, read by hand. T-009 measured **12 decks mechanically** and two
> of its claims are wrong: external references range **0–21, not 2–7**, and **three decks are
> already fully self-contained** — one of them with seven faces embedded as base64 `@font-face`,
> zero external references and 22 inline SVGs, at 282 KB. **The font problem is solved precedent,
> not an open problem.** Use R1's numbers, not the table above.

**Self-containment is still the first requirement**, and the corpus proves it is reachable without
giving up the typography.

> **Raised and resolved, 2026-08-06 — the sentence above stands.** When T-013 asked whether a
> per-deck size ceiling was acceptable, the owner's answer made delivery a configuration parameter
> with **CDN references as the default** and embedding on request. That would have reversed this
> sentence, CLAUDE.md rule 1, and the position [R4](research/R4-prior-art.md) identified as the
> owner's sharpest departure from the source deck skill (J1 — *the skill means one file, the owner
> means no network*).
>
> [R5 §4](research/R5-assets-and-licences.md) argued against it on the measurement — the premise
> was that embedding is expensive, and a full deck is 192 KB — and **the owner accepted that
> recommendation the same day**. Delivery is now a decision, not an open question: see *Delivery
> mode* in "Decisions taken". The episode is kept on the record because it is the only place the
> project has reversed a stated owner direction on evidence, and because CLAUDE.md asks for
> exactly that to be visible rather than quiet.

---

## The prompt structure that works

The corpus contains a prompt that produced one of the better decks. Its shape generalises, and
the plugin should elicit exactly these:

```
## Role         — who the author is being, in strong terms
## Context      — what happened before this deck; where the content came from
## Goal         — one sentence, transformational not descriptive
## Requirements — what the audience must believe or do afterwards
## Format       — file type, length, tone, and what to avoid
## Resources    — the source documents, by path
```

Two details from the real prompt are worth keeping verbatim as defaults:

- *"Keep it short in text, but it must send a very strong message."*
- *"Avoid typical AI-favored terminologies."* — the corpus author lists offenders explicitly.
  Ship a list, make it configurable, and apply it as a build-time check rather than a hope.

**Format defaults observed:** single-file HTML · 6–9 pages · respectful, positive, professional ·
visuals to aid non-expert comprehension.

---

## The critique pass

The corpus includes a deck critique that is the most useful artifact in it — a section-by-section
review, explicitly "no diplomatic padding", opening with a bottom-line-up-front verdict and then
grading each slide. Real findings from it, all of which generalise:

- A structural gap in the argument (two data points presented as a trend).
- A recurring format that only lands on one side (a two-column comparison where one column is
  consistently weaker).
- A diagram that does not do what its type promises (a "Venn diagram" whose sets do not overlap).
- A metaphor used four times where twice would be elegant.
- A typo on the most important slide.
- Generator branding left in the corner.

**Build this as a first-class mode**, not an afterthought. It is what turns a first draft into a
deck, and it is the part users cannot do for their own work. Its voice should be direct: a
critique that opens with three compliments is one nobody acts on.

### The findings above are all inside one deck

A second source shows a class that is not. A five-document analytical set was audited as one body
of work before its deck was built, and the audit found nine defects that no single-document review
had caught — after every document had passed its own review:

- A figure correct in the document that stated it, and wrong in the document that quoted it. The
  wrong version had propagated to eight places across four documents, including the one cell a
  board actually signs.
- A summary paragraph contradicting the table printed directly above it: two rows carried one
  verdict, the sentence under them claimed three.
- A count of process steps that had drifted from the model it described, repeated in three
  documents and quoted in a writing standard.

**Every one was found by counting, not by reading** — tallying a table's own verdict column,
counting nodes in the source model a sentence described. Reading each document on its own passed
all of them, five times.

**This shapes the mode.** A deck assembled from source documents inherits their disagreements and
adds its own, and slide-by-slide review cannot see either. When the user supplies the sources, the
critique should reconcile the deck against them *and* the sources against each other. The
technique that worked is cheap: one table listing every figure in the material, its origin, and
every place it is reused.

---

## What to build

Three modes, in build order:

1. **Brief** — elicit the six-section prompt above from whatever the user has.
2. **Build** — generate the single-file deck: self-contained, section-per-slide, inline SVG,
   keyboard navigation, print/PDF stylesheet.
3. **Critique** — section-by-section review against the standard, blunt, with a BLUF verdict.

Plus a **check** the build must pass: no external references, no banned terminology, every
`<section>` has a heading, contrast meets WCAG AA, and it renders glitch-free from `file://` in
the target browser. *(Printing was on this list; it is now an opt-in mode, not a gate — see
"Decisions taken".)* **"Glitch-free" is now defined as nine testable conditions** in
[R6 §8](research/R6-portability-contract.md) — T-005 implements them; two of the nine exist
because this project has watched a font check and a WebGL check both pass on a broken render.

Those are all presentation checks. **When the user supplies source documents, the check also
reconciles content:** every figure on a slide appears in a source with the same value, and every
figure used more than once in the deck agrees with itself. A deck can pass every presentation
check and still put a wrong number in front of a board.

**The check must say which half it ran.** Presentation-only is a legitimate result; presented as a
clean pass, it is a false one.

---

## Carried lessons

What the corpus research carried into this project. The durable, citable form of these — plus the
ones this project has since paid for itself — lives in [`LESSONS.md`](LESSONS.md), which is where
new ones go.

| | Lesson |
| :--- | :--- |
| **Look at the output** | Every automated check can pass on something visually broken. A deck that validates is not a deck that reads well — render it and look before claiming done. |
| **What is read every time must be short** | Applies to the skill itself: a design system belongs in a reference file loaded on demand, not in the always-loaded skill body. |
| **Verify on the real case** | Test the generator on a real 12-slide deck with diagrams, not a three-slide toy. The corpus decks are the target case. |
| **Don't restate what another source owns** | If the plugin ships a design reference, the skill points at it rather than paraphrasing it. |
| **Count, don't read** | Defects that span documents are invisible to reading and obvious to counting. Tally a table's own column; count the nodes in the model a sentence describes. Reviewing each artefact on its own passes every one of them. |
| **Say which half is checked** | A check that looks complete is worse than no check. State in the output what was *not* checked, so nobody reads a pass as "this deck is right". |
| **Verify the checker on a known case** | The scan that measured one quality dimension in that audit was wrong — it split sentences line by line against hard-wrapped Markdown, and under-reported by 15×. It was believed because it did not look like a tool. Any check ships with a self-test on a case whose answer is known. |

---

## Decisions taken — 2026-08-06

Set by the owner when the project was re-scoped around researching their existing work.

| | Decision |
| :--- | :--- |
| **Purpose** | Not a generic tool. It encodes *this owner's* conventions so tightly that any topic needs almost no input. |
| **Interface** | The skill asks exactly two questions: content length (max and/or min), and whether there is anything to align to. Nothing else. Extension deferred. |
| **Authorship** | The plugin **writes the words** from source material — it decides the narrative and the slide copy, not just the design around supplied text. Answers open question 5. |
| **Use case** | Primarily **presented live**, but the supporting detail is hidden behind interactive elements — turning cards, toggles, tabs, floating information layers, tooltips — so the same file is consumable by a recipient reading it alone. |
| **Dependencies** | **Self-contained core, optional enhancement.** Works standalone for a user who installed nothing else; uses other skills when present, with a stated fallback for each. |
| **Visual identity** | **One** theme, fully resolved on every layer — not several, not generated per topic. But **every layer parametric from the start**, because the planned next step is an in-plugin tool that generates new templates. Answers open question 3. |
| **Richness** | Interaction, smooth visuals, 2D animation and 3D effects are **wanted**. The corpus's "1–3 script tags" is a description of past work, not a target. There is no JavaScript budget. |
| **Portability** | The binding constraint. No installation, no special privileges — the recipient double-clicks a file. **One browser must render it with no glitch**; that beats working everywhere adequately. Mobile is secondary. |
| **Printing** | **Not a requirement.** An optional mode the user can force on to make a deck printable. It must never shape the interaction design. |
| **Target browser** | **Recent Chrome/Edge.** One engine, tested. Firefox and Safari degrade gracefully but are not the bar. |
| **Render technique** | **Full exemption from the SVG-only rule** — SVG, `<canvas>` and WebGL are all permitted, for data-carrying diagrams included. Raster images and external libraries stay banned. |
| **Delivery mode** | **Embed by default.** Two modes, not three: `portable` (everything inlined, zero external references, ~190 KB typical) is the default and the only shipping mode; `linked` (CDN) exists **for the authoring loop only** and a deck built with it is a defect the critique pass flags. No local-files mode. Settled 2026-08-06 on [R5 §4](research/R5-assets-and-licences.md) — see below. |

**Three consequences worth stating plainly.**

*Progressive disclosure was absent from this brief entirely.* It is the owner's signature technique
and the mechanism that lets one file serve both a live audience and a lone reader. Scoped as T-016.

*Portability replaces restraint as the constraint,* and the two are not the same thing. The real
hazard is that **`file://` is a restricted origin**: ES modules, `fetch`, XHR and some worker and
WebGL texture paths fail on a double-clicked file even though they work when served over HTTP.
"Rich JavaScript" and "no installation" collide exactly there, and it is the most likely way a
deck ships broken. Scoped as T-017.

> **Measured 2026-08-06 by [R6](research/R6-portability-contract.md), and the paragraph above draws
> the line in the wrong place.** It is not "inline works, external fails" — a sibling file loads
> perfectly well as a stylesheet, font, image, script or audio source. The boundary is between
> **fetch-like access and element-like access**: script may not read a local file's bytes, the
> renderer may consume them. Across 95 rows on Chrome 151 and Edge 151 that single sentence covers
> every refusal.
>
> Most of what this paragraph feared is available. `file://` is a **secure context**, so
> `crypto.subtle`, view transitions, container queries, popover, WebGL1/2 and a WebGPU adapter are
> all present; fullscreen, clipboard, audio resume, download and every storage API work. ES modules
> are usable via `import()` of a `blob:` or `data:` URL — but a library shipping as more than one
> file needs its internal specifiers rewritten at build time, because a relative specifier cannot
> resolve from a `blob:` base and an import map does not rescue it. **No refused capability costs
> the deck anything**; each has a working substitute. The design layer is unconstrained.

*The rules in `../CLAUDE.md` have been updated to match.* The old rule 2 (inline SVG only) and rule
3 (decks must not look like each other) both predated these decisions and were rewritten on the
owner's instruction — SVG is now a preference rather than a requirement, and one parametric theme
replaces enforced variety, with the template generator satisfying it later.

---

## Open questions

1. ~~**Fonts.** Embedded subsets (large files, licensing questions) or a curated system stack?~~
   **Answered 2026-08-06 by [R5](research/R5-assets-and-licences.md): embedded subsets, and the
   trade-off the question assumed does not exist.** Both premises were wrong. The files are not
   large — a latin-subset woff2 is 27–76 KB inlined, and a three-face identity is 97 KB. The
   licensing is not questionable — every candidate is OFL 1.1, which permits redistribution
   provided the licence travels with the font. A complete 12-slide deck with three faces, icons,
   a motion library and four SVG diagrams measured **191.8 KB, zero external references**, opened
   offline. There is no identity/self-containment trade-off to make.
2. ~~**Charts.** Hand-authored inline SVG scales badly to real data; a charting library is an
   external dependency.~~ **Answered 2026-08-06 by [R5 §5](research/R5-assets-and-licences.md):
   no chart library.** Chart.js is 203.6 KB and d3 is 273.2 KB, against a hand-written SVG chart
   that fits inside the 9.1 KB covering the probe deck's entire markup, CSS, script and four
   diagrams. Borrow d3's scale arithmetic as a few lines; do not vendor d3. The "minimal built-in
   SVG chart generator" the question guessed at is the right answer — T-006 builds it.
3. ~~**One template or many?**~~ **Answered above:** one theme, parametric, generator later.
4. **Speaker notes and PDF export.** Both wanted eventually; neither in the corpus. Scope now,
   build later.
5. ~~**Content vs. design split.**~~ **Answered above:** the plugin writes the words. It is the
   harder path and the acceptance criteria for build mode must reflect that.
6. **Do brief, build and critique get the source documents?** Reconciling a deck against the
   material it was built from is the highest-value check available, and it needs those documents
   in context — which costs context budget on every run. Ask for them and reconcile, or degrade to
   presentation-only when they are absent? This decides whether the check in *What to build* has
   one half or two.

---

## Definition of done

- A deck renders correctly with the network disabled.
- The build check demonstrated failing on each class of problem it claims to catch.
- The critique mode run against a deck with known defects, and found them.
- No personal, client, or machine data anywhere in the repository.
