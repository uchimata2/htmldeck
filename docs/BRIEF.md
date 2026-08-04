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

Grounded in ~10 real decks produced across a training programme, not invented. Representative
sample:

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

**The finding that matters most:** every deck in the corpus carries **2–7 external references**
(web fonts, chart libraries). That means none of them renders correctly offline, on a locked-down
machine, or in five years. **Self-containment is the first requirement**, and meeting it while
keeping the typography is the plugin's main technical problem — subsetted fonts embedded as
base64 `@font-face`, or a curated pairing of high-quality system-stack fonts.

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

---

## What to build

Three modes, in build order:

1. **Brief** — elicit the six-section prompt above from whatever the user has.
2. **Build** — generate the single-file deck: self-contained, section-per-slide, inline SVG,
   keyboard navigation, print/PDF stylesheet.
3. **Critique** — section-by-section review against the standard, blunt, with a BLUF verdict.

Plus a **check** the build must pass: no external references, no banned terminology, every
`<section>` has a heading, contrast meets WCAG AA, and it prints without clipping.

---

## Carried lessons

| | Lesson |
| :--- | :--- |
| **Look at the output** | Every automated check can pass on something visually broken. A deck that validates is not a deck that reads well — render it and look before claiming done. |
| **What is read every time must be short** | Applies to the skill itself: a design system belongs in a reference file loaded on demand, not in the always-loaded skill body. |
| **Verify on the real case** | Test the generator on a real 12-slide deck with diagrams, not a three-slide toy. The corpus decks are the target case. |
| **Don't restate what another source owns** | If the plugin ships a design reference, the skill points at it rather than paraphrasing it. |

---

## Open questions

1. **Fonts.** Embedded subsets (large files, licensing questions) or a curated system stack
   (smaller, safer, less distinctive)? This is the identity/self-containment trade-off and it
   decides how the decks look. **Answer first.**
2. **Charts.** Hand-authored inline SVG scales badly to real data; a charting library is an
   external dependency. A minimal built-in SVG chart generator for the three or four chart types
   a business deck actually uses is the likely answer.
3. **One template or many?** The corpus decks look good *because* they don't share a template.
   A plugin that ships one house style will produce decks that look like each other. Ship several
   distinct, complete looks, or generate the palette and type pairing per deck from the topic?
4. **Speaker notes and PDF export.** Both wanted eventually; neither in the corpus. Scope now,
   build later.
5. **Content vs. design split.** Should the plugin write the words, or only the deck around words
   the user supplies? The corpus prompt implies the former; that is much harder to do well.

---

## Definition of done

- A deck renders correctly with the network disabled.
- The build check demonstrated failing on each class of problem it claims to catch.
- The critique mode run against a deck with known defects, and found them.
- No personal, client, or machine data anywhere in the repository.
