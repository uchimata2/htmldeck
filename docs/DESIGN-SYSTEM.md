# htmldeck — design system

**The operative ruleset. Nothing else.** Loaded on demand; the skill body must not paraphrase it.

**Why each rule is what it is lives in [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md)** — drops,
conflicts, provenance, derivations, re-scoping. No runtime loads that file. If a rule looks arbitrary,
the reason is there under its ID.

| Column | Meaning |
| :--- | :--- |
| **ID** | Permanent. A retired rule keeps its number and is marked retired; numbers are never reused. |
| **Label** | **hard** — enforced; breaking it is a defect, not a style choice. **default** — applied unless a recorded reason overrides. **guidance** — judgement, never checked mechanically. |
| **Check** | **auto** — a build check can test it. **render** — needs a rendered measurement or a look. **judge** — judgement; the evaluator's territory. |
| **Reach** | Whether a check can actually get at the rule, which `Check` does not say. **yes** — the gate is expected to check it, and saying nothing about it is a failure of the run. **never** — no program can decide it; the gate must not imply otherwise, and nobody should open a task to build it. **off-gate** — decidable in principle but not by this instrument, so it stays a named gap someone may close. **—** — outside the gate's jurisdiction, which is every `judge` rule; the evaluator owns those and `Reach` says nothing about them. |

**How to read a `Reach` cell.** **The value is the first word. Everything after it is a free-text
reason**, and `never` and `off-gate` must carry one. The em dash that introduces the reason is
punctuation, not structure — parse on the leading token, never on the dash, because `—` is itself a
value (the same null the `Check` column already uses at DS-007). Getting that backwards makes a
`judge` row parse as an empty value, which is how this contract was written the first time.

**Why `Reach` is a column and not a list.** Because the list was tried. A parallel section restating
the rules in a different order — which ones a check could reach, numbered separately — was recorded
as delivered and was never written, and four tasks reasoned about its contents for two months before
anyone opened the file (**L-39**). A fact carried on the rule's own row cannot go absent without the
row going absent. `Reach` also stays deliberately separate from `Check`: **auto** and **never** is a
coherent pair — a rule a program could test in principle, on input no program can produce — and
collapsing the two columns would lose it.

**Two of that list's conditions are gone and are not coming back.** It named two rules as beyond any
check, numbered **22 and 30**, and which rules those were cannot be recovered — the numbering was
not this document's order, and the account is in
[`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §5.5. Nothing is owed to them: every rule now states its
own `Reach`, which is what those two conditions were trying to say about themselves.

**`Reach` says whether a check can get at a rule. It never says which part of the gate does.**
*"Decided statically from the source rather than at render"* is a fact about how the gate is built
today and it changes whenever the gate is refactored; it belongs in the gate's own output, not here.
A rule checked in an unexpected stage is still `yes`.

**Override clause (DS-000, guidance).** *Keep this guide only as long as it serves the message; be
brave to depart when a different idea communicates better.* Licenses departure from **default** and
**guidance** with a stated reason. Never from **hard**.

---

## 0. The nine that decide everything else

0. **Every slide delivers one thing, and says it on the slide.** The audience must not have to wait
   for the presenter to reach the point. Everything below serves this (§3.4).
1. **One theme, every value a token.** Not a palette per deck.
2. **Neutral ground, one accent, and the accent means something.**
3. **The headline is a claim, not a topic.**
4. **Motion must encode something.** *What does this animation encode?* If "it looks good", remove it.
5. **Two tiers of detail, never three.** Tier one carries the argument with everything closed.
6. **WCAG 2.2 AA is the floor**, plus two AAA criteria adopted deliberately (§7).
7. **Portable or it does not ship.** One file, zero external references, opened from `file://`.
8. **One fixed 1920×1080 stage, uniformly scaled.** Body type stays at 24–28 design units; nothing
   anywhere goes below 16.

---

## 1. Envelope

### 1.1 Portability

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-001 | One self-contained file: every font, icon, script and style inlined. **Zero external references.** | hard | auto | yes |
| DS-002 | `portable` is the default and the only shipping mode. A deck delivered as `linked` (CDN) is a defect. | hard | auto | yes |
| DS-003 | `<meta charset="utf-8">` present. | hard | auto | yes |
| DS-004 | Renders glitch-free in recent Chrome/Edge. Other engines degrade gracefully; mobile is secondary. | default | render | yes — the Chrome/Edge half only; *other engines degrade gracefully* is unobservable from a single-engine harness and is not silently dropped by being recorded here |
| DS-005 | Script may not read a local file's bytes; the renderer may consume them. Design to element-like access, not fetch-like. | hard | auto | yes |
| DS-006 | A multi-file library needs its internal specifiers rewritten at build time. A relative specifier cannot resolve from a `blob:` base. | hard | auto | yes |
| DS-007 | The `file://` unique-security-origin console warning is benign. Do not chase it. | guidance | — | — |
| DS-008 | **Latin scripts only.** A non-Latin deck is not a supported case; do not half-support it. | hard | auto | yes |

### 1.2 Theming and tokens

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-010 | **Every value that could differ between themes is a CSS custom property** — including ones no current theme varies. | hard | auto | yes |
| DS-011 | Ship **one** fully-resolved theme. Never a palette generated per topic. | hard | auto | yes |
| DS-012 | Dark mode is one block of custom-property overrides, never a redesign. | hard | auto | yes |
| DS-013 | Core tokens: `--ink` · `--bg` · `--line` · `--shadow` · `--accent` · semantic role colours · **a data-series role and a UI-line role, both separate from `--line`** · `--measure` · the disclosure mark. Chart marks and interactive borders carry a 3:1 obligation (§7, 1.4.11) that a hairline does not, so a deck reusing `--line` for either fails a criterion no token in the list names. | default | auto | yes |

---

## 2. Look

### 2.1 Colour

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-020 | Neutral ground plus **exactly one** accent. | hard | auto | yes |
| DS-021 | The accent carries meaning wherever it appears. Decorative use anywhere devalues it everywhere. | hard | judge | — |
| DS-022 | Interest comes from contrast, depth, typography, rhythm and motion — not from more colours. | guidance | judge | — |
| DS-023 | Never pure white, never pure black. Warm paper ground; graphite or warm-charcoal ink. | default | auto | yes |
| DS-024 | Light by default, not dark. | default | auto | yes |
| DS-025 | The accent must survive a bad projector — muted, not neon, never a framework default. | default | judge | — |
| DS-026 | Semantic roles fixed deck-wide: green positive · red negative · amber caution, **with a visible legend**. | hard | render | yes |
| DS-027 | Both themes readable. No component that inverts into white-on-light. | hard | render | yes |
| DS-028 | Gradients only when functional (depth, progress). No full-page gradients, no gradient blobs, no neon. | hard | render | yes |
| DS-029 | Calm colours; functional but attractive. "Neutral" is not "boring". | guidance | judge | — |

### 2.2 Typography

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-030 | Three named roles, one face each, every one a token: **display · text · mono**. | hard | auto | yes |
| DS-031 | **Never Inter, Roboto, Arial or `system-ui`.** A system-font body is a severity-H failure. | hard | auto | yes |
| DS-032 | Faces embed as base64 `@font-face`, latin subset, licence permitting redistribution. **The licence travels with the font.** | hard | auto | yes |
| DS-033 | Type is sized in **design units on the 1920×1080 stage**. A design unit is not a unit CSS has, so the stage declares one — **once**, as a token — and every size derives from it. **No bare `px` anywhere else inside the stage, and no `vw`, `vh` or `clamp()` at all**: those are what fight the transform. | hard | auto | yes |
| DS-034 | **Body 24–28 design units**, at line-height **1.40–1.70**. Display ~67. Subhead ~34. *Amended 2026-08-09 by [T-007](../tasks/T-007-define-the-parametric-theme-layer.md): the line height was stated as the single value 1.55 and the check enforced it to ±0.01, so a theme that changes reading density failed the gate **for being a second theme** — the failure the parametric layer exists to prevent. The band is the rule; 1.55 is what [`themes/quarto.css`](../themes/quarto.css) sets inside it. [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §3 computes the type **floor** and argues no line height at all, so nothing in the rule's recorded reason is lost.* | hard | auto | yes |
| DS-035 | **Nothing below 16 design units, anywhere.** *Amended from 18 by the owner, 2026-08-06 — see [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §2.* | hard | auto | yes |
| DS-036 | Mono labels 16–18 units, uppercase, tracked ~1.4px. **The 16–17 band is reserved for marginalia and is never load-bearing**; at 18 the mono role is a *label* and may carry meaning — a table's row headers, a legend, a figure's annotation. Body type stays at DS-034's range. *Amended 2026-08-09 by [T-052](../tasks/T-052-two-hard-judge-failures-in-the-reference-deck.md): the never-load-bearing clause used to bind the whole 16–18 range, which collided with **DS-026**'s requirement that the deck show a visible legend.* | hard | judge | — |
| DS-037 | `text-wrap: balance` and slight negative tracking on display headings. | default | auto | yes |
| DS-038 | The mono layer carries the domain vocabulary — key terms in mono, accent underline at first use. | default | judge | — |
| DS-039 | Line length is a token (`--measure`), defaulting inside 45–75 characters. | default | render | yes |

### 2.3 Layout and grid

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-040 | CSS grid and flexbox throughout. | hard | auto | yes |
| DS-041 | **Align by construction, not by coordinates.** Correlated rows share a grid track. | hard | render | yes |
| DS-042 | Boxes that read as a set are siblings in one container. | hard | auto | never — which boxes *read as a set* is a reading of the content; the DOM records containment, not what a viewer groups |
| DS-043 | No box nested in a box with its own text. | hard | auto | yes |
| DS-044 | **Reset every heading level**, `h4` and `h5` included. A partial reset is worse than none. | hard | auto | yes |
| DS-045 | **Never style the bare `b` element selector.** A rule on `b` itself reaches every `<b>` in the deck, so one component's look silently becomes a global default nothing declared, and the next `<b>` written for in-sentence emphasis inherits it. **A `b` scoped inside a component — `.bottom-line b` — is not this rule**: the scope is what stops the leak, and it is how the deliverable is set. *Clarified 2026-08-09 by [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md), which found the old wording admitted two readings that disagreed about the reference deck; the narrow one is the one that matches the harm.* | hard | auto | yes |
| DS-046 | No duplicate emphasis — one marker per point. | default | judge | — |
| DS-047 | Consistent margins, one grid, left-aligned headlines, breathing room. | default | render | yes |
| DS-048 | One dominant accent per slide, for rhythm. | default | judge | — |
| DS-049 | Cards: 12–16px radius, soft shadow, thin hairline, no heavy borders. | default | auto | yes |
| DS-050 | The stage floats on a darker field with a soft shadow and hairline edge. | default | render | yes |

### 2.4 The stage and the resolution contract

*Why these are hard, and where the numbers come from:
[`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §3.*

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-060 | The presentation view is a **fixed 1920×1080 design space, uniformly scaled** with `transform: scale()`. | hard | auto | yes |
| DS-061 | **Exactly one layout.** No media queries, no breakpoints, no `max-width` containers inside the stage. | hard | auto | yes |
| DS-062 | Aspect ratio is 16:9 and fixed. A non-16:9 viewport letterboxes; it never reflows. | hard | render | yes |
| DS-063 | Rendered at 3840×2000 and at 1280×634, the stage is **identical up to a uniform scale factor, within a stated tolerance**. **The tolerance is split by element kind, not by axis:** a non-text box's whole rect ≤ **0.25 design units**; a **text run's whole rect** ≤ **2 device pixels at the smaller rendering**. Exact equality is unachievable for text — glyph advances round to device pixels, so any deck containing text fails an equality check — but that rounding moves a text run's *position and height too*, not only its width. **Two is where the mechanism puts it**: a whole-rect comparison folds two independent roundings, the run's edge and its extent, each up to one device pixel. *Measured 2026-08-07 over a full 12-slide deck: **116 non-text values disagreed by 0.000 du** and 336 text values by at most 1.17, at a scale ratio of 3.15. **A routine run samples four slides and reports 40 and 84** — same rule, smaller sample, and the reason two sets of figures are in circulation. [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §2 carries what the earlier figure got wrong and which run is which.* *Restated in device pixels 2026-08-09 by [T-007](../tasks/T-007-define-the-parametric-theme-layer.md): the bound was **2 design units**, a number measured over one deck **in one theme**, and the second theme reached 2.23 du without breaking anything — a tighter type scale fits more glyphs on a line and every one of them rounds. **A design-unit threshold is the wrong shape for a device-pixel effect**, because it silently encodes the scale factor of the deck it was measured on.* | hard | render | yes |
| DS-064 | Body text measures ≥ 16 px in a 720p capture of the presented deck. | hard | render | yes |
| DS-065 | No decorative element positioned in a **unit that does not ride the transform** — `vw`, `vh`, `vmin`, `vmax`, `pt`, `cm`, `in`. *Reworded 2026-08-07 by [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md), which tried to build the check and found the rule could not be false.* The old wording — *"absolute pixels rather than design units"* — names a distinction that **does not exist inside the stage**: a design unit *is* one CSS pixel before the transform (`--du:1px`), so a px offset and a design-unit offset compute to the same value and nothing at runtime can tell them apart. What actually breaks the stage is a length resolved against the **viewport** instead of the design space. DS-033 bans those units inside the stage already; this rule now says the same thing about decoration instead of stating something unfalsifiable. | hard | auto | yes |
| DS-200 | **Centre the scaled stage by a technique that survives the transform.** `transform: scale()` does not change layout size, so flex or grid centring positions the **unscaled** 1920×1080 box: the track sizes to 1920, start-aligns it, and the scaled stage lands off-centre and clips at the far edge. Anchor at 50%/50% and translate, or size the wrapper to the scaled dimensions. **Measure the stage's rect against the viewport at several widths — the bug is invisible at full size.** | hard | render | yes |

### 2.5 The reflow view

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-070 | Reachable by a **persistent, visible, keyboard-operable control.** This carries the conformance claim. | hard | render | yes |
| DS-071 | **Auto-engages when the stage's scale factor `min(vw/1920, vh/1080)` drops below 0.5** — the point where 24-design-unit body text renders under 12 CSS px. On a 16:9-or-taller viewport that is 960 CSS px of width, which is the number to quote; **width alone is a lossy proxy and short viewports are where it fails** — 1280 × 400 scales to 0.37 and puts body text at 8.9 px while a width test keeps the deck on the stage. *Amended 2026-08-07 by the owner via [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md); the caveat under F-06 in [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) had already named the case.* | default | render | yes |
| DS-072 | **Never engages in fullscreen**, or while a presentation control is active. | hard | render | off-gate — headless has no user gesture to enter fullscreen with; the check observes a defined-property double, so a person pressing F11 is the only real demonstration |
| DS-073 | Carries **all** content, tier-two disclosure included — and **carries it inlined**: every panel rendered open in normal flow, the disclosure control not rendered at all. A document rendering does not hide content behind an affordance, and a control printed or shown with nothing to reveal advertises something the reader cannot reach. The two-tier reading rhythm is the stage's, and §5.3's rules are written for the stage. *Settled 2026-08-07 by the owner via [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md), ratifying what the reference deck already did; [R7 §5](research/R7-printable-mode.md) decided the same question the same way for print.* | hard | auto | yes |
| DS-074 | A document rendering, not a responsive stage: one column, normal flow, type in `rem`, honouring user font size. | hard | auto | yes |
| DS-075 | No two-dimensional scrolling at 320 CSS px equivalent. | hard | render | yes |
| DS-076 | Switching views preserves position in both directions. | default | render | yes |

---

## 3. Argument

### 3.1 Structure and pacing

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-080 | `<section>` per slide. | hard | auto | yes |
| DS-081 | **Never fewer than 6 slides.** Under 6 is a memo. | hard | auto | yes |
| DS-082 | Deck length is a per-deck decision. Default 8–12; past 12 needs a recorded reason. | default | auto | yes |
| DS-083 | Single clean message per slide beats concision. | guidance | judge | — |
| DS-084 | **Nothing is dropped to fit a slide count — it is folded** behind disclosure. Cutting a figure or a row is a failed edit. | hard | judge | — |
| DS-085 | The last slide is a **close, not a recap**: the ask as one action. | hard | judge | — |
| DS-086 | One strong closing line plus one subtle supporting line. Nothing else. | default | judge | — |
| DS-087 | Appendix pages named "Appendix"; the back link names where it returns to. | default | auto | yes |
| DS-088 | No speaker notes, presenter markers or script in the shipped deck. | default | auto | yes |

### 3.2 Archetypes

**Thirteen archetypes plus one modifier.** A-13 Layered Detail is **not** an archetype — it is a
modifier available to all the others (§5.3).

| ID | Archetype | The move |
| :--- | :--- | :--- |
| A-01 | **Why-Now** | Name the *external* change making the timing non-arbitrary. Not "the opportunity is large". |
| A-02 | **Risk-Retirement Sequence** | Order slides by the objection each kills, not by topic. |
| A-03 | **Single Number** | One figure at display size, one line of interpretation. **The interpretation is the slide.** |
| A-04 | **Two-Column Ledger** | A comparison where **both** columns are genuinely argued. Fails more often than it works — X-03. |
| A-05 | **Animated Trajectory** | Time as an animated axis, so the shape of change is the message. |
| A-06 | **Small Multiple** | One chart repeated across a facet; every comparison positional. |
| A-07 | **Before / After** | The same diagram twice with **exactly one edge changed**, and the change marked. |
| A-08 | **Process / Flow** | 3–5 steps with **labelled** connectors. |
| A-09 | **Timeline with a Gate** | A sequence with one marked decision point. The gate is the information. |
| A-10 | **Architecture View** | Show the mechanism, not its name — only the parts the argument turns on. |
| A-11 | **Manifesto Line** | One declarative sentence, set large, no body. |
| A-12 | **Uncomfortable Truth** | State the **cost** of the recommendation in the deck's own voice, before anyone asks. |
| A-14 | **Verdict / Close** | Restate the ask as **one action**. Always the last slide. |

### 3.3 Writing

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-090 | **The headline is a claim, not a topic.** Checked semantically, not structurally. | hard | judge | — |
| DS-091 | Per slide: one headline ≤ 6 words plus ≤ 3 supporting fragments. | hard | auto | yes |
| DS-092 | Sentence under 20 words. Paragraph 3–4 sentences. Table cell one line. | hard | auto | yes |
| DS-093 | **Never justify a statement with sentences** — diagrams, lists, tables and structure carry detail. | hard | judge | — |
| DS-094 | Fixed order: **statement → description → challenge.** Never open with a question or a build-up. | default | judge | — |
| DS-095 | Explain the result, not the road to it. | default | judge | — |
| DS-096 | Explain by example, not definition — show the model doing work on a real number. | default | judge | — |
| DS-097 | **The reader is bright and new to the field.** Anything the author would look up is a defect. | hard | judge | — |
| DS-098 | Embed the domain's key terms naturally — demonstrate the language, don't refer to it. | default | judge | — |
| DS-099 | Respectful, positive, professional; voiced as an enthusiastic business person. | hard | judge | — |
| DS-100 | Active voice. One dash per paragraph at most. **No rhetorical questions.** | hard | auto | yes |
| DS-101 | **Bold the fact, not the emphasis.** Three bold things means none stands out. | hard | render | yes |
| DS-102 | **No fabricated metrics.** Every figure sourced; `[est.]` markers preserved. **An illustrative deck sources its figures from its own model**: say on the deck that the subject is illustrative, state the assumptions the numbers derive from, and attribute nothing to a real study. This is the provision that stops the alternative — quoting half-remembered real research, where a misremembered figure is a fabricated metric wearing a citation. | hard | judge | — |
| DS-103 | Grade honestly: solved / substantially / partial / deferred. | default | judge | — |
| DS-104 | Mark assumptions subtly at the side, never as noise. | default | render | yes |
| DS-105 | Provenance mark upper-right. A working link where sources are reachable from where the deck is presented; plain text where they are not. **Never a dead link.** | default | auto | yes |
| DS-106 | **No banned terminology** — five categories: empty phrases · inflated adjectives (*crucial, pivotal, seamless, leverage, synergy, friction*) · structural tells · syntactic patterns · voice absence. Also *"which is precisely why"*, *"worth saying out loud"*, *genuinely / actually / arguably / precisely*. | hard | auto | yes |
| DS-107 | **The word-list check is necessary and not sufficient, and must say so.** Text passes all five categories and still reads as machine-written when it has no voice. *`Check` moved from `judge` to `—` on 2026-08-09 by [T-052](../tasks/T-052-two-hard-judge-failures-in-the-reference-deck.md): this binds whoever builds the check, not the deck, which is what `—` means and what DS-190, DS-191, DS-220 and DS-221 already carry.* | hard | — | — |

> **DS-106 is owned by the `humanize-writing` skill.** Point at it; the list above is the inline
> fallback for machines where it is absent, because a pointer that resolves to nothing checks nothing.

### 3.4 The deliverable — what every slide owes its audience

**This is the section the rest of the argument rules serve.** A slide can satisfy every rule above —
claim headline, three fragments, a real diagram, no banned words — and still leave the audience
waiting for the presenter to say what the point was. That is a failure, and until now nothing here
named it.

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-201 | **Every slide delivers exactly one thing.** Name it before the slide is written. If it needs two sentences, the slide is two slides — or none. | hard | judge | — |
| DS-202 | **The deliverable appears on the slide as a bottom line**: one sentence, factual, no reasoning. Not the headline restated, not a summary of what is above it. | hard | auto | yes |
| DS-203 | **The bottom line is the most prominent text after the headline** — recognisable in about two seconds, with no presenter talking. Accent colour, weight, position, and at most one Pulse-once. | hard | render | yes |
| DS-204 | **Never bury the deliverable in a list, a paragraph or a table cell.** If it is one bullet among five, the audience has to find it, and they will find it after the presenter says it. | hard | judge | — |
| DS-205 | **The deliverable is never behind a disclosure.** DS-161 says a closed slide still makes its point; this says which part of the slide *is* the point. | hard | auto | yes |
| DS-206 | **Supporting detail stays visible and subordinate — do not hide it under the click.** Disclosure earns its place for depth, never for tidying a slide that is merely full. Judge it per slide. | default | judge | — |
| DS-207 | **The deliverable is stated factually and directly.** No analogy, no metaphor, no rhetorical framing. Wit is allowed in the headline and in the presenter's mouth; the bottom line carries none of it. | hard | judge | — |
| DS-208 | **No native-speaker idiom, unless it is asked for.** Idioms, phrasal verbs used figuratively, sporting and cultural metaphors. **The reader may not be a native speaker, and no sentence should need a second pass.** Distinct from DS-097, which governs jargon: a reader can look a term up, and cannot look up an idiom they have misread as literal. | hard | judge | — |
| DS-209 | **One emphasis per slide, and it belongs to the deliverable.** DS-101 at slide scale: three emphasised things means none is emphasised, and the one that loses is the point. | hard | render | yes |

### 3.5 The outline, before any slide exists

**Where the outline sits in the authoring pipeline is [T-020](../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md)'s.
What it must contain is a property of a good deck, so it is here.**

> **Settled 2026-08-07, and this section is what settled it.** T-020 §3.2 had placed outline
> sign-off *after* the specification review, which the DS-210 → DS-212 order below contradicts.
> The owner ruled for this order: the outline is signed off **before** it is expanded into the
> slide-by-slide specification. T-020 §3.2 carries the corrected pipeline; nothing in this table
> changed.

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-210 | **An outline exists before any slide does**, and covers every topic the deck is expected to carry. | hard | auto | off-gate — the outline is a pipeline artefact; nothing in the delivered HTML records whether one existed, and the standalone entry point is handed one file |
| DS-211 | Per slide the outline names, at minimum: **archetype · title · bottom line**. The bottom line in the outline is the same sentence that ships on the slide. | hard | auto | off-gate — needs the outline document alongside the deck to compare against; the gate is given the HTML only |
| DS-212 | The outline is expanded into a **slide-by-slide specification** — structure, text, visuals, motion, interaction, title, bottom line — **page by page, never in one pass.** | default | judge | — |
| DS-213 | **The specification is reviewed slide by slide before any HTML is written**, for missing points, unnecessary detail, inconsistency and inefficiency, and the findings are fixed one at a time. | default | judge | — |

---

## 4. Visuals

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-110 | **No raster images.** Ever. | hard | auto | yes |
| DS-111 | Diagrams are inline SVG. `<canvas>` and WebGL where they render better; prefer SVG where it is as good. | hard | auto | yes |
| DS-112 | **Never hand-draw icons.** Lucide primary, Font Awesome free fallback. | hard | judge | — |
| DS-113 | Embed the icon set as an SVG symbol sprite containing **only the icons used**, referenced by `<use>`. | hard | auto | yes |
| DS-114 | **One icon per concept, used consistently.** A repeated icon is a repeated idea. | hard | judge | — |
| DS-115 | Particles, connectors and custom diagrams may be drawn freely in SVG or canvas. | guidance | — | — |
| DS-116 | **Branch where the process branches.** Four boxes joined by arrow glyphs is not a flow diagram. | hard | judge | — |
| DS-117 | Connectors are **labelled**, always. Arrowheads are for **directional** connectors only, and they **meet their target**. An undirected edge gets no arrowhead: an arrow asserts a direction, and asserting one the data does not have is a wrong diagram rather than a tidy one. | hard | render | yes |
| DS-118 | **Every SVG and chart is theme-aware.** No hard-coded fill or stroke. | hard | auto | yes |
| DS-119 | `<canvas>` gets fixed pixel dimensions via HTML attributes; CSS scales it. | hard | auto | yes |
| DS-120 | An accumulation effect must actually accumulate, not fall through. | hard | render | yes |
| DS-121 | Charts obey the **encoding ranking** — position > length > area > hue. Variety never buys a worse encoding. | hard | judge | — |
| DS-122 | No chart library. Hand-written SVG, borrowing scale arithmetic as a few lines. | hard | auto | yes |
| DS-123 | **"Boxes everywhere" is the rejected pattern.** Card grids, stat strips, pill rows and bulleted lists **used instead of a diagram** are a severity-H failure. | hard | judge | — |
| DS-214 | **Colour an SVG through CSS, never through a presentation attribute.** A class rule outranks `fill=` and `stroke=` silently, so an element styled by both renders the CSS colour and the attribute is dead markup — how a 2.17:1 run shipped past a palette audit that reported zero failures. This is DS-118's mechanism: theme-aware means *styled*, not *attributed*. | hard | auto | yes |
| DS-215 | **Check the colour that renders, not the colour intended.** A palette audit compares token pairs an author nominates; it cannot see a pair nobody thought to nominate. Compare each text run's **computed** fill against the **computed** fill of whatever is painted behind it. DS-191, in the one place it has already cost this project a defect. | hard | render | yes |
| DS-219 | **Never set text on a data mark unless that mark's own pair is measured and clears both criteria.** To clear 1.4.11's 3:1 against the ground a **neutral** mark must be dark; to carry 1.4.3's 4.5:1 text it must be light. **No neutral does both** — which is why a value-inside-the-bar chart cannot be made conformant by choosing a better grey, and why the label normally goes outside the mark or on a plate that earns 4.5:1 in its own right. **A non-neutral mark can do both**, and an accent chosen against the ground usually does; that is a measurement, never an assumption, so a labelled mark owes **two** numbers — mark against ground ≥ 3:1, and text against mark ≥ 4.5:1. *Amended 2026-08-09 by [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md): the prohibition was wider than the argument it gives, and the rule is a consequence of the accessibility floor rather than a stylistic preference, so it now says what the floor actually requires.* | hard | render | yes |

---

## 5. Behaviour

### 5.1 Interaction and navigation

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-130 | **Every function keyboard-reachable**, including every disclosure control. | hard | auto | yes |
| DS-131 | **The navigation set: keyboard ←/→/space/Home/End; prev/next arrows; touch/swipe; wheel; and click-to-jump to a bounded set of named targets.** *Named* is the load-bearing word — a target the reader can identify before clicking, which the deck's stages already are. **Not one *unnamed* target per slide** — amended 2026-08-08 by the owner for [T-035](../tasks/T-035-the-ruler-navigator.md), and the moved word is the whole amendment: the objection was never the *count*, it was twelve unlabelled dots (T-028). One target per slide is admitted when every target names itself. **The naming is per target, never per group**, and that clause is the precondition rather than a detail: a ruler whose small ticks announce their *section* would give twelve targets seven labels, leaving a reader unable to name a tick before clicking it — the same defect in a new shape, and the amendment would have gutted this rule while appearing to preserve it. Dots remain one permitted implementation of a bounded set, never a requirement, and DS-217 bounds the count. **Where stages are uneven, or long enough that landing on one is not a useful jump**, the stage list has stopped being the right target set and the deck owes an on-demand slide index instead — offering neither is a departure from this rule and needs a reason. | default | render | yes |
| DS-132 | **Off-screen slides removed from the tab order.** | hard | auto | yes |
| DS-133 | Progress indicator, **provided it encodes real position.** | default | render | yes |
| DS-134 | **The spine**: the deck's argument shown as a persistent element, with the current position lit. **Reworded 2026-08-08 for [T-035](../tasks/T-035-the-ruler-navigator.md)**, which replaced the stage-name ribbon this rule used to name with a ruler — and the rewording is the same correction DS-131 needed for the same reason: *a rule that specifies the element instead of the need is the one that collides with the next composition rule*, because composition rules are written about elements. What is required is that the argument's structure is visible and the reader's place in it is marked; the ribbon was one way to spend that and the ruler is another, cheaper in width because its footprint does not depend on how the stages are named. | default | render | yes |
| DS-135 | The page title and the nav-bar name for that page **must match**. | hard | auto | yes |
| DS-136 | Interaction patterns built **once as components and reused**, so the UX is learnable. | hard | judge | — |
| DS-137 | Two simultaneous interactions need a **defined precedence rule.** | hard | judge | — |
| DS-138 | Popovers drop **below** the element, never above — **so the control sits high enough that its panel fits below it on the stage.** Panel placement constrains control placement, and the ruleset previously fixed only the first: a control near the foot of a 1080-unit stage cannot host a panel more than a row or two deep, and no styling of the panel repairs it. Choose the control's row from the panel's height. | hard | render | yes |
| DS-139 | Assumption marker on the right edge, silent until wanted. | default | render | yes |
| DS-216 | **One encoding of position, not three.** A spine ribbon, a dot per slide and a progress bar all answer *where am I*. Showing all three is noise competing with the slide. Pick one primary; a second is permitted when it encodes a **different fact** — stage versus slide — **or the same fact in a different register**, one read at a glance and one read exactly. **Never a third element, however well it is argued.** The register clause was added 2026-08-08 by the owner for [T-035](../tasks/T-035-the-ruler-navigator.md), so that a ruler carrying slide *and* stage can keep the numeric counter beside it — and **the hard cap of two is what pays for it**, because *register* is a far easier claim to make than *fact*: a progress bar reads as "approximate position" too, and under the old test alone it would have walked back in. Count elements, not arguments. A component's own inline caption — a label that names what the indicator points at and has nothing to say without it — is part of that indicator, not a third encoding; the test is whether it survives the others being removed. | default | render | yes |
| DS-217 | **Chrome has a budget: roughly 12 labelled or interactive items, and ~90 design units of height.** Past that the navigation reads as an interface rather than as a deck. Prefer a compact indicator plus click-to-jump over one target per slide. **A regular repeating scale counts as one item, not as *n*** — amended 2026-08-08 for [T-035](../tasks/T-035-the-ruler-navigator.md). The budget counts items because items are what make a frame noisy, and a tick array is perceived as one object the way a ruler is one object and not three hundred marks; the metric was wrong for that shape, not the intent, so raising the number would have been the worse fix. **A scale is: uniform mark, uniform pitch, no per-item label at rest** — the definition is enforced by `audit.py` rather than trusted, because undefined it is a loophole any evenly-spaced row of controls could claim, which would leave this budget enforceable against nothing. **The slide count at which per-slide targets stop fitting is measured, not guessed** — the earlier *"somewhere around ten"* was a guess the shipping twelve-slide deck already contradicted. On the reference deck's row it is **17**: 1726 usable units, less 546 for the controls and their gap, less the label's share, at a 52-unit target pitch. Past it the small ticks stop being **targets** and stay **marks**, which drops the affordance and keeps the information — so the number is where the indicator changes mode, not where it fails. **A mark has a size floor of its own: 4 design units**, which renders at 2.02 CSS px at the 0.5 scale hand-over (DS-071), below which the quiet colour stops registering — and the *inactive* marks are the binding constraint, not the current one, because at one to two pixels low contrast disappears well before the accent does. **Measured, and not yet confirmed on a 1× display:** the reading was taken through a screenshot, which is a poor instrument for a one-to-two pixel judgement (**L-15**), so the floor is a measurement carrying a stated doubt rather than a settled number. It binds only past the mode change, so no shipping deck depends on it yet; the first deck that does should check it on real hardware and either confirm 4 or raise it. | default | render | yes |
| DS-229 | **Every part of a deck is the element, place, count and attributes [`COMPONENT-CONTRACT.md`](COMPONENT-CONTRACT.md) gives it, and every class the shared style block styles has a row there.** This is the mechanical instance of **DS-136**, which requires patterns to be built once as components and reused — and which stays a judgement, because *whether two similar things should have been one component* is a design decision and *learnable* is not a property of the DOM. What a check can decide is whether the components a deck names are the components it emits: a disclosure control missing its `aria-controls`, a panel wired to a button on another slide, a second component invented for one slide. **Same shape as DS-228 under DS-137** — the general rule stays judgement and the one instance a check can decide is written down. The completeness half is what keeps it from decaying: a component is added by writing CSS, which is precisely when nobody remembers to write the contract row. *Added 2026-08-09 by [T-016](../tasks/T-016-the-interaction-and-motion-layer.md), which wrote the contract; before it there was nothing to conform to, and the measurement that opened the task recorded exactly that — no markup contract a generator could emit.* | hard | auto | yes |

### 5.2 Motion

**Governing rule: motion must encode something.** *What does this animation encode?* If the answer
is "it looks good", it is decoration and it goes.

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-140 | **A named vocabulary of exactly four motions, and nothing else:** Rise (entry, staggered) · Current (flow, dashed, looping) · Open/Turn/Scale (reveals) · Pulse-once (never looping). **Entries and reveals sit inside DS-141's 500 ms cap; Current runs 3–6 s and Pulse-once 0.8–1.6 s.** The shipping theme's values are 340 ms at `cubic-bezier(.22,1,.36,1)` with a 60 ms stagger, dasharray 7 6 over 4.5 s, 380 / 420 / 300 ms, and 1.2 s. *Amended 2026-08-09 by [T-007](../tasks/T-007-define-the-parametric-theme-layer.md): the durations **were** the rule, and the check admitted a long motion only at exactly 1.2 s or 4.5 s, so a theme that changed motion failed the gate for being a second theme. **The names and the closure are what this rule is for** — [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §4 argues that a named vocabulary is what stops animation becoming decoration, and argues nothing about the milliseconds. So the vocabulary stays fixed at four and the numbers become bands, with the shipping theme's inside them.* | hard | auto | yes |
| DS-141 | **Entry and transition animations max 500 ms**, ease-in-out. Inter-slide transition 400–500 ms. **DS-141 governs entry and transition only; DS-140's named vocabulary is the specific override** — Pulse-once and Current are conformant by name, inside the bands DS-140 states, not exceptions to be argued. A duration over 500 ms that is *not* one of DS-140's four is a defect. | hard | auto | yes |
| DS-142 | **No continuous ambient glow, pulse or drift on static content.** | hard | auto | yes |
| DS-143 | `prefers-reduced-motion` honoured, **and the semantics survive it** — the dashed arrows stay dashed. | hard | render | yes |
| DS-144 | **No 3D transitions between slides**, no flashy zooms, no punchy cuts. The 3D reveal of a card is permitted. | hard | auto | yes |
| DS-145 | Hidden elements reveal by opening, turning or scaling. Flows use dashed arrows, slowly animated. | default | render | yes |
| DS-146 | Charts draw in **once**; never re-animate on back-navigation. **The draw-in is DS-140's Rise applied to the chart's marks, staggered — not a fifth motion.** A stroke-dash draw would add one to a vocabulary DS-140 fixes at four, which is the trade this rule is not permitted to make. | hard | render | yes |
| DS-147 | Count-up on headline statistics; **one** emphasis pulse on the key number per slide. | default | render | yes |
| DS-148 | When a diagram changes mode, animate nodes to their new size and position. | default | render | yes |
| DS-149 | Entrance animations with `fill-mode: forwards` keep their stacking context. | hard | render | yes |
| DS-150 | **Every animation answers *what does this encode?*** Depth, shadow, transparency and shaders are subject to the same test. | hard | judge | — |
| DS-218 | **Motion that loops, or runs over 5 s, ships with a persistent, keyboard-operable control that stops it** — and the deck still reads with motion off. DS-140's `Current` is infinite, so **every deck with a flow diagram needs this control**, and §7's 2.2.2 stated the obligation without any rule here requiring the deck to build one. Distinct from DS-143: `prefers-reduced-motion` is what the reader's system asks for; this is what the reader can reach. | hard | auto | yes |

### 5.3 Progressive disclosure

**Not a feature of the deck — the reason the deck can be two things.** The modifier A-13 applies to
every archetype.

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-160 | **Two tiers, never three.** Slide → detail. Never slide → detail → further detail. | hard | auto | yes |
| DS-161 | **Closed, the slide still makes its point.** Opening may deepen the argument; it may never complete it. | hard | judge | — |
| DS-162 | The split test: **would the argument survive without it?** If no, it is tier one. | hard | judge | — |
| DS-163 | **Never hover-only.** Tooltips may supplement; never the only route to content. | hard | auto | yes |
| DS-164 | Every disclosure control has a **visible affordance with a real label.** A bare chevron does not qualify. | hard | render | yes |
| DS-165 | The disclosure mark is a **tokenised element of the theme**, not a per-slide invention. | hard | auto | yes |
| DS-166 | **Disclosure state never required to advance.** Arrows advance; a separate key toggles; the two do not interact. | hard | auto | yes |
| DS-167 | Every affordance **available and visible during the talk, never load-bearing in it.** | hard | judge | — |
| DS-168 | Targets ≥ 24 × 24 CSS px, or the spacing exception — which **inside the stage means ≥ 48 × 48 design units**. The stage scale bottoms out at 0.5 before DS-071 hands over to the reflow view, so a design unit is worth half a CSS pixel at the smallest size the stage is ever shown. **Sizing a control at 24 design units matches the number and fails the criterion.** | hard | auto | yes |
| DS-169 | One meaningful interaction per slide, where it adds signal. Never decoration. | default | judge | — |
| DS-170 | Push longer text behind interaction rather than onto the slide. When detail is unavoidable: hide it, or split to a new page. | default | judge | — |
| DS-227 | **On the stage, every disclosure panel is closed at load.** Stated because **two other rules already lean on it and neither says it**: DS-161 asks whether the slide still makes its point closed, a question with no content unless closed is the state the reader meets; and DS-073 requires the reflow view to render every panel **open**, a contrast that only means something against a stage that starts shut. DS-073's inverse is the tempting shortcut and it does not work — DS-073 governs a **different rendering**, and a rule about one rendering cannot carry an obligation on another by negation. *Added 2026-08-09 by [T-038](../tasks/T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md), which found the gate measuring this and reporting it as DS-161.* | hard | auto | yes |
| DS-228 | **At most one disclosure panel is open at a time.** Opening one closes any other, and leaving a slide closes its own — so a slide is never re-entered part-open and tier two cannot accumulate into tier one. This is the deck's **defined precedence rule** for the disclosure pair, which **DS-137 requires and does not supply**: DS-137 is a judgement about interaction precedence in general and stays one, and this is the single instance of it a check can decide. `default`, not `hard` — a slide genuinely arguing two details side by side is a coherent design, licensed by DS-000 with a stated reason, and DS-169 already treats more than one interaction on a slide that way. | default | render | yes |

### 5.4 The printable mode

**The printable mode is the paginated stage, preceded by a generated contents page — one slide per
page — and the reading view is not a print target.** Ruled by [`R7`](research/R7-printable-mode.md)
§4 against a measured alternative, and adopted in
[`examples/reference-deck.html`](../examples/reference-deck.html) by
[T-032](../tasks/T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md). Printing stays a
mode the user forces on, never a constraint on the design (§0): the reading view already serves the
read-alone case **on screen**, and reshaping it so it paginates well is exactly printing becoming a
constraint. What print does not preserve is stated to the user, never discovered on paper —
[`R7`](research/R7-printable-mode.md) §5 is the list.

**The contents page is a printed page that is not a slide**, which is why the sentence above needed
amending rather than merely extending: the printed artifact is now **`n` + 1 pages for `n` slides**.
Amended 2026-08-08 by the owner for
[T-034](../tasks/T-034-a-contents-page-for-the-printed-deck.md) (**L-37** — the answer that
required it was recognised as a rule change and taken as one, with a named side). The reason it
exists is that this stylesheet hides the chrome, so the spine (DS-134) that carries the structure on
screen reaches a paper reader nowhere; and it is the **only** surface that reaches the person
holding the pages, which is where R7 §5's loss is finally stated to them rather than to whoever was
about to print.

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-222 | **A print stylesheet asserts the view it wants, `display` included.** A deck that hands over to the reading view on a small stage scale (DS-071) hides the stage with `[hidden]`, and **printing is what makes it hand over** — printing changes the layout viewport. Overriding `position`, `transform` or `height` does not touch `display`, so the stage never reaches the page: it prints blank, or it prints the other view and looks fixed. Force `display` on both the element and its `[hidden]` state, and hide the view you did not choose. Two printed rounds were lost to this. **Corollary — check what a selector actually matches:** `:last-child` does not match the last slide, because the stage ends with the chrome, so the final slide keeps its `break-after` and emits an empty extra page. | hard | render | yes |
| DS-223 | **A slide stays a containing block for its own overlays in print.** `position: relative`, never `static`. A slide is the containing block for its absolutely positioned descendants — disclosure panels, the provenance line — and making it static hands them to the page, which scatters them across breaks. Relative keeps it in normal flow *and* keeps it a containing block. | hard | render | yes |
| DS-224 | **Entrance animations are disabled for print.** They hold their pre-animation state until played, so a slide the reader never advanced to prints blank or half-risen — the deck's own motion vocabulary (DS-140) turned into missing content on paper. This is DS-221's mechanism on a second medium: any rendering that captures the deck without playing it must pin motion off first. | hard | render | yes |
| DS-225 | **The contents page is generated from the deck, never authored, and it is placed first.** Every box reads its title and its one-sentence description off the slide it points at — the description **is** the bottom line (DS-211), so it cannot drift from the deck and costs nothing to write (**L-08**). An authored contents page is a second copy of the argument and rots. **First, not last**, and that is mechanical rather than aesthetic: `break-after` is cancelled on `section.slide:last-of-type`, which matches by *element type*, so a `<section>` placed after the final slide makes that selector match nothing and silently restores the blank trailing page — DS-222's corollary. The mark on each box is keyed to the **stage**, never to slide content, so an uneven deck cannot produce an uneven set of marks. | hard | render | yes |
| DS-226 | **Printed type has a floor in points, not in design units.** A design unit is a stage abstraction whose printed size depends on the paper: on A4 landscape the 1920 × 1080 page box scales by **0.5847**, so one design unit is **0.4385 pt** and the deck's smallest screen type (18 du) lands at 7.9 pt. Setting a print floor in design units therefore says nothing about legibility — the same number is a different size on different paper. **The floor is 9 pt on the target paper (21 du on A4 landscape), and any page number a reader navigates by is ≥ 14 pt (32 du).** Where a generated page must compress to fit, it yields whitespace first, then type down to the floor, then drops the description **outright** — and **it never drops an entry**, because a contents page that silently omits a slide is confidently wrong about the shape of the argument. **A description is shown at a full line or not at all:** shrinking one until a part-line survives puts a few units of clipped letterform on the page, which a reader takes for a rendering fault rather than a compact mode. The same rule runs in the other direction, and it was the direction nobody looked in first — **a page with too few entries must narrow its columns rather than stretch its boxes**, or a short deck prints as a grid of mostly-empty rectangles, which reads as content that failed to load. **Compression has a floor of its own, and past it the page continues onto a second sheet rather than clipping:** measured 2026-08-08, a 4-column contents page holds its full job to **16 entries** and holds number-and-title to **24**, beyond which a box has 89 du of height for 96 du of content and arithmetic decides the outcome. Confining the compression to the description — never to the number or the title — is what makes that boundary sharp instead of letting the entry erode across a range of deck sizes. The continuation itself is [T-036](../tasks/T-036-the-second-contents-page-for-long-decks.md); until it lands this rule is **implemented to 24 entries**, which is stated rather than left to be discovered. | hard | render | yes |

---

## 6. Anti-patterns

Stated here so the critique pass and the standard cannot drift apart. **T-004 consumes this list; it
does not own it.**

**`X-nn` means one of these twelve and nothing else.** `DESIGN-RATIONALE.md` §2's source conflicts
were also `X-n` until 2026-08-09, separated from these only by a leading zero and cited in the same
sentences, which produced a wrong citation in the gate's own output; they are `C-nn` now
([T-047](../tasks/T-047-give-the-rationale-conflicts-their-own-id-namespace.md)).

| ID | Anti-pattern | Label |
| :--- | :--- | :--- |
| X-01 | **The agenda slide** — carries no claim, costs attention. | hard |
| X-02 | **The bullet dump** — a topic label over a list. | hard |
| X-03 | **The lopsided comparison** — a two-column shape where one column is consistently weaker. | hard |
| X-04 | **The diagram that isn't** — a shape promising a relationship it does not show. | hard |
| X-05 | **Two points presented as a trend.** | hard |
| X-06 | **The Meeker pileup** — density justified by "it is meant to be read". | guidance |
| X-07 | **The misleading truth** — figures individually defensible, collectively deceptive. | hard |
| X-08 | **The presenter-dependent slide** — only resolves with narration. | hard |
| X-09 | **The click-built slide** — an argument that only completes once something is opened. | hard |
| X-10 | **The dual-axis chart** — two y-scales invite any correlation the author wants. | hard |
| X-11 | **The rainbow encoding** — hue used for magnitude. A-06 is the fix. | hard |
| X-12 | **Residue** — generator branding, a typo on the most important slide. | hard |

**Also hunt** (guidance): invented numbers · a narrative conceit that breaks mid-deck · a wrong
metric on the title slide · undefined interaction precedence · an element rendering so small it reads
as a fault · two numbering schemes with no mapping.

**What counts as a finding** (hard): anything a grader, a presenter under pressure, or a careful
reader would trip on.

**Severity vocabulary** (hard): **Major / Minor / Note** for a specification review; **H / M / L plus
the principle violated** for a design audit.

**A stated requirement going unmet is an agreed deviation, never a silent omission** (hard).

---

## 7. The accessibility floor

**WCAG 2.2 Level AA is the floor.** Every row `hard`. Criterion numbers are the IDs.

| Criterion | Level | The number |
| :--- | :---: | :--- |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 text; 3:1 large (≥18pt / 24px, or ≥14pt / 18.66px bold) |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components, focus indicators, meaningful graphics |
| 1.4.4 Resize Text | AA | Usable at 200% |
| 1.4.10 Reflow | AA | No two-dimensional scrolling at 320 CSS px equivalent |
| 1.4.12 Text Spacing | AA | No loss of content at the specified overrides |
| 2.1.1 Keyboard | A | Every function reachable by keyboard |
| 2.4.7 Focus Visible | AA | A visible focus indicator |
| 2.4.11 Focus Not Obscured | AA | The focused component at least partly visible |
| 2.5.8 Target Size (Minimum) | AA | 24 × 24 CSS px, or the spacing exception |
| 2.2.2 Pause, Stop, Hide | A | Control over motion lasting > 5s |
| 2.3.1 Three Flashes | A | Hard limit |
| **2.4.13 Focus Appearance** | AAA — **adopted** | ≥ 2 CSS px perimeter equivalent, 3:1 against unfocused |
| **2.3.3 Animation from Interactions** | AAA — **adopted** | Honour `prefers-reduced-motion` |

**Conform to WCAG 2, design with APCA, never report APCA as conformance.**

**The conformance claim is: AA via a conforming alternate version reachable by a persistent control**
(DS-070) — never a bare "this deck is AA".

**4.1.1 Parsing was removed in WCAG 2.2.** A check written against it checks a retired criterion.

---

## 8. Boundaries

**Other skills own these. Point at them by name and carry the consequence inline** — a pointer can
resolve to nothing, and a check that silently checks nothing is worse than a short one.

| Owned by | What |
| :--- | :--- |
| `humanize-writing` | DS-106, DS-107 — the AI-tell categories and the voice test |
| `dataviz` | DS-121 — the encoding ranking, recessive grid/axes, sequential palettes |
| `artifact-diagramming` | A-07 "draw the difference"; A-10 show the mechanism |

**Other tasks own these. This reference states what a good deck is, not how the plugin works.**

| Deferred to | What |
| :--- | :--- |
| [T-020](../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md) | The authoring pipeline and the convergence loop's placement |
| [T-023](../tasks/T-023-the-deck-evaluation-rubric-and-convergence-loop.md) | **How a deck is scored against these rules, and when it is good enough** |
| [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md) | Mechanics of every `auto` and `render` rule above |
| [T-004](../tasks/T-004-critique-mode-blunt-section-by-section-review.md) | The critique report's format |
| [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md) | ~~Building §2.5~~ — **done 2026-08-07.** Twelve of the fourteen §2.4 / §2.5 rules are gated by `tools/deck/contract.py`; DS-061 is static in `audit.py` and DS-065 is not checkable, which is why it was reworded |
| [T-001](../tasks/T-001-decide-the-font-strategy-embedded-subsets-or-a-syste.md) · [T-006](../tasks/T-006-decide-the-chart-strategy.md) · [T-007](../tasks/T-007-define-the-parametric-theme-layer.md) | The three standing decisions |

**Four rules about checking that stay here**, being claims about what a check may assert:

| ID | Rule | Label | Check | Reach |
| :--- | :--- | :--- | :--- | :--- |
| DS-190 | **Structural checks say nothing about layout — always render and look.** | hard | — | — binds whoever builds a check, not the deck; there is nothing here for a gate to test |
| DS-191 | **DOM measurement confirms geometry you suspect; it cannot find a defect you never thought to measure.** | hard | — | — binds whoever builds a check, not the deck; there is nothing here for a gate to test |
| DS-220 | **A box clamped by its grid track never reports an overflow.** Content taller than a `1fr` track spills silently: the box measures exactly the track, so comparing the box against the stage finds nothing wrong. **Compare `scrollHeight` against `clientHeight`** — the box is the wrong thing to measure. | hard | — | — binds whoever builds a check, not the deck; there is nothing here for a gate to test |
| DS-221 | **Pin motion off before capturing.** DS-140's infinite `Current` means a headless render never reaches a quiescent state, so the screenshot fires mid-transition and yields a convincing blank slide. A render gate that does not disable animation is measuring an arbitrary frame and reporting it as the deck. | hard | — | — binds whoever builds a check, not the deck; there is nothing here for a gate to test |

---

## 9. What is not covered

**Tested once, by building a deck** — [T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md)
built [`examples/reference-deck.html`](../examples/reference-deck.html) strictly to this document and
produced **thirteen findings**, four of them conflicts between two `hard` rules. All thirteen are
reconciled by [T-025](../tasks/T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md),
which amended nine rules and added four; **each conflicting pair now names which rule yields, in the
rule text.** What that reconciliation is worth is bounded by what produced it: **one deck**. Every
amendment is a correction from a single build, and a second deck would be expected to find more.

**What that build did not test.** It was one deck, one topic, one author, and it was scored by the
agent that wrote it. §3.4 and §3.5 arrived *after* it, from the owner's review. **That gap closed on
2026-08-07**: [T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md)
rewrote the reference deck to the deliverable contract, all twelve slides carry a bottom line, and
DS-202/203/205/216/217 are gated rather than asserted — `BRIEF.md` records the release gate as clear.
**The other half of that sentence still holds and is the part worth keeping: the rules that matter
most are the least exercised.** One conforming deck is one deck, and four of the nine
deliverable-contract rules are named nowhere in `EVALUATION.md`
([T-048](../tasks/T-048-gate-the-hard-rules-only-judgement-can-reach.md)). The reproducibility
rulings still come from R6's capability matrix, which answers *"is
this available?"* rather than *"does this read well?"* CLAUDE.md rule 6 governs the second question,
and it is answered by looking, not by this document.

Sources, verdicts, provenance and every "why": [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md).
