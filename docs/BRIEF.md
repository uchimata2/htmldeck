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
"Decisions taken".)*

Those are all presentation checks. **When the user supplies source documents, the check also
reconciles content:** every figure on a slide appears in a source with the same value, and every
figure used more than once in the deck agrees with itself. A deck can pass every presentation
check and still put a wrong number in front of a board.

**The check must say which half it ran.** Presentation-only is a legitimate result; presented as a
clean pass, it is a false one.

---

## Carried lessons

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

**Three consequences worth stating plainly.**

*Progressive disclosure was absent from this brief entirely.* It is the owner's signature technique
and the mechanism that lets one file serve both a live audience and a lone reader. Scoped as T-016.

*Portability replaces restraint as the constraint,* and the two are not the same thing. The real
hazard is that **`file://` is a restricted origin**: ES modules, `fetch`, XHR and some worker and
WebGL texture paths fail on a double-clicked file even though they work when served over HTTP.
"Rich JavaScript" and "no installation" collide exactly there, and it is the most likely way a
deck ships broken. Scoped as T-017.

*The rules in `../CLAUDE.md` have been updated to match.* The old rule 2 (inline SVG only) and rule
3 (decks must not look like each other) both predated these decisions and were rewritten on the
owner's instruction — SVG is now a preference rather than a requirement, and one parametric theme
replaces enforced variety, with the template generator satisfying it later.

---

## Open questions

1. **Fonts.** Embedded subsets (large files, licensing questions) or a curated system stack
   (smaller, safer, less distinctive)? This is the identity/self-containment trade-off and it
   decides how the decks look. **Answer first.**
2. **Charts.** Hand-authored inline SVG scales badly to real data; a charting library is an
   external dependency. A minimal built-in SVG chart generator for the three or four chart types
   a business deck actually uses is the likely answer.
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
