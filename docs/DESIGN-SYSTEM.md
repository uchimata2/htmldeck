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

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-001 | One self-contained file: every font, icon, script and style inlined. **Zero external references.** | hard | auto |
| DS-002 | `portable` is the default and the only shipping mode. A deck delivered as `linked` (CDN) is a defect. | hard | auto |
| DS-003 | `<meta charset="utf-8">` present. | hard | auto |
| DS-004 | Renders glitch-free in recent Chrome/Edge. Other engines degrade gracefully; mobile is secondary. | default | render |
| DS-005 | Script may not read a local file's bytes; the renderer may consume them. Design to element-like access, not fetch-like. | hard | auto |
| DS-006 | A multi-file library needs its internal specifiers rewritten at build time. A relative specifier cannot resolve from a `blob:` base. | hard | auto |
| DS-007 | The `file://` unique-security-origin console warning is benign. Do not chase it. | guidance | — |
| DS-008 | **Latin scripts only.** A non-Latin deck is not a supported case; do not half-support it. | hard | auto |

### 1.2 Theming and tokens

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-010 | **Every value that could differ between themes is a CSS custom property** — including ones no current theme varies. | hard | auto |
| DS-011 | Ship **one** fully-resolved theme. Never a palette generated per topic. | hard | auto |
| DS-012 | Dark mode is one block of custom-property overrides, never a redesign. | hard | auto |
| DS-013 | Core tokens: `--ink` · `--bg` · `--line` · `--shadow` · `--accent` · semantic role colours · **a data-series role and a UI-line role, both separate from `--line`** · `--measure` · the disclosure mark. Chart marks and interactive borders carry a 3:1 obligation (§7, 1.4.11) that a hairline does not, so a deck reusing `--line` for either fails a criterion no token in the list names. | default | auto |

---

## 2. Look

### 2.1 Colour

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-020 | Neutral ground plus **exactly one** accent. | hard | auto |
| DS-021 | The accent carries meaning wherever it appears. Decorative use anywhere devalues it everywhere. | hard | judge |
| DS-022 | Interest comes from contrast, depth, typography, rhythm and motion — not from more colours. | guidance | judge |
| DS-023 | Never pure white, never pure black. Warm paper ground; graphite or warm-charcoal ink. | default | auto |
| DS-024 | Light by default, not dark. | default | auto |
| DS-025 | The accent must survive a bad projector — muted, not neon, never a framework default. | default | judge |
| DS-026 | Semantic roles fixed deck-wide: green positive · red negative · amber caution, **with a visible legend**. | hard | render |
| DS-027 | Both themes readable. No component that inverts into white-on-light. | hard | render |
| DS-028 | Gradients only when functional (depth, progress). No full-page gradients, no gradient blobs, no neon. | hard | render |
| DS-029 | Calm colours; functional but attractive. "Neutral" is not "boring". | guidance | judge |

### 2.2 Typography

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-030 | Three named roles, one face each, every one a token: **display · text · mono**. | hard | auto |
| DS-031 | **Never Inter, Roboto, Arial or `system-ui`.** A system-font body is a severity-H failure. | hard | auto |
| DS-032 | Faces embed as base64 `@font-face`, latin subset, licence permitting redistribution. **The licence travels with the font.** | hard | auto |
| DS-033 | Type is sized in **design units on the 1920×1080 stage**. A design unit is not a unit CSS has, so the stage declares one — **once**, as a token — and every size derives from it. **No bare `px` anywhere else inside the stage, and no `vw`, `vh` or `clamp()` at all**: those are what fight the transform. | hard | auto |
| DS-034 | **Body 24–28 design units** at line-height 1.55. Display ~67. Subhead ~34. | hard | auto |
| DS-035 | **Nothing below 16 design units, anywhere.** *Amended from 18 by the owner, 2026-08-06 — see [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §2.* | hard | auto |
| DS-036 | Mono labels 16–18 units, uppercase, tracked ~1.4px — **and never load-bearing.** The 16–17 band is reserved for marginalia; body type stays at DS-034's range. | hard | judge |
| DS-037 | `text-wrap: balance` and slight negative tracking on display headings. | default | auto |
| DS-038 | The mono layer carries the domain vocabulary — key terms in mono, accent underline at first use. | default | judge |
| DS-039 | Line length is a token (`--measure`), defaulting inside 45–75 characters. | default | render |

### 2.3 Layout and grid

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-040 | CSS grid and flexbox throughout. | hard | auto |
| DS-041 | **Align by construction, not by coordinates.** Correlated rows share a grid track. | hard | render |
| DS-042 | Boxes that read as a set are siblings in one container. | hard | auto |
| DS-043 | No box nested in a box with its own text. | hard | auto |
| DS-044 | **Reset every heading level**, `h4` and `h5` included. A partial reset is worse than none. | hard | auto |
| DS-045 | Never style a bare `<b>` inside a component. | hard | auto |
| DS-046 | No duplicate emphasis — one marker per point. | default | judge |
| DS-047 | Consistent margins, one grid, left-aligned headlines, breathing room. | default | render |
| DS-048 | One dominant accent per slide, for rhythm. | default | judge |
| DS-049 | Cards: 12–16px radius, soft shadow, thin hairline, no heavy borders. | default | auto |
| DS-050 | The stage floats on a darker field with a soft shadow and hairline edge. | default | render |

### 2.4 The stage and the resolution contract

*Why these are hard, and where the numbers come from:
[`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §3.*

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-060 | The presentation view is a **fixed 1920×1080 design space, uniformly scaled** with `transform: scale()`. | hard | auto |
| DS-061 | **Exactly one layout.** No media queries, no breakpoints, no `max-width` containers inside the stage. | hard | auto |
| DS-062 | Aspect ratio is 16:9 and fixed. A non-16:9 viewport letterboxes; it never reflows. | hard | render |
| DS-063 | Rendered at 3840×2000 and at 1280×634, the stage is **identical up to a uniform scale factor, within a stated tolerance**: non-text geometry ≤ **0.25 design units**, text-run widths ≤ **2 design units**. Exact equality is unachievable — glyph advances round to device pixels, so any deck containing text fails an equality check. *The tolerance is measured rather than guessed: 384 values, worst case 0.09 and 1.17 — [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) §2.* | hard | render |
| DS-064 | Body text measures ≥ 16 px in a 720p capture of the presented deck. | hard | render |
| DS-065 | No decorative element positioned in absolute pixels rather than design units. | hard | auto |
| DS-200 | **Centre the scaled stage by a technique that survives the transform.** `transform: scale()` does not change layout size, so flex or grid centring positions the **unscaled** 1920×1080 box: the track sizes to 1920, start-aligns it, and the scaled stage lands off-centre and clips at the far edge. Anchor at 50%/50% and translate, or size the wrapper to the scaled dimensions. **Measure the stage's rect against the viewport at several widths — the bug is invisible at full size.** | hard | render |

### 2.5 The reflow view

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-070 | Reachable by a **persistent, visible, keyboard-operable control.** This carries the conformance claim. | hard | render |
| DS-071 | Auto-engages below 960 CSS px of viewport width. | default | render |
| DS-072 | **Never engages in fullscreen**, or while a presentation control is active. | hard | render |
| DS-073 | Carries **all** content, tier-two disclosure included. | hard | auto |
| DS-074 | A document rendering, not a responsive stage: one column, normal flow, type in `rem`, honouring user font size. | hard | auto |
| DS-075 | No two-dimensional scrolling at 320 CSS px equivalent. | hard | render |
| DS-076 | Switching views preserves position in both directions. | default | render |

---

## 3. Argument

### 3.1 Structure and pacing

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-080 | `<section>` per slide. | hard | auto |
| DS-081 | **Never fewer than 6 slides.** Under 6 is a memo. | hard | auto |
| DS-082 | Deck length is a per-deck decision. Default 8–12; past 12 needs a recorded reason. | default | auto |
| DS-083 | Single clean message per slide beats concision. | guidance | judge |
| DS-084 | **Nothing is dropped to fit a slide count — it is folded** behind disclosure. Cutting a figure or a row is a failed edit. | hard | judge |
| DS-085 | The last slide is a **close, not a recap**: the ask as one action. | hard | judge |
| DS-086 | One strong closing line plus one subtle supporting line. Nothing else. | default | judge |
| DS-087 | Appendix pages named "Appendix"; the back link names where it returns to. | default | auto |
| DS-088 | No speaker notes, presenter markers or script in the shipped deck. | default | auto |

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

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-090 | **The headline is a claim, not a topic.** Checked semantically, not structurally. | hard | judge |
| DS-091 | Per slide: one headline ≤ 6 words plus ≤ 3 supporting fragments. | hard | auto |
| DS-092 | Sentence under 20 words. Paragraph 3–4 sentences. Table cell one line. | hard | auto |
| DS-093 | **Never justify a statement with sentences** — diagrams, lists, tables and structure carry detail. | hard | judge |
| DS-094 | Fixed order: **statement → description → challenge.** Never open with a question or a build-up. | default | judge |
| DS-095 | Explain the result, not the road to it. | default | judge |
| DS-096 | Explain by example, not definition — show the model doing work on a real number. | default | judge |
| DS-097 | **The reader is bright and new to the field.** Anything the author would look up is a defect. | hard | judge |
| DS-098 | Embed the domain's key terms naturally — demonstrate the language, don't refer to it. | default | judge |
| DS-099 | Respectful, positive, professional; voiced as an enthusiastic business person. | hard | judge |
| DS-100 | Active voice. One dash per paragraph at most. **No rhetorical questions.** | hard | auto |
| DS-101 | **Bold the fact, not the emphasis.** Three bold things means none stands out. | hard | render |
| DS-102 | **No fabricated metrics.** Every figure sourced; `[est.]` markers preserved. **An illustrative deck sources its figures from its own model**: say on the deck that the subject is illustrative, state the assumptions the numbers derive from, and attribute nothing to a real study. This is the provision that stops the alternative — quoting half-remembered real research, where a misremembered figure is a fabricated metric wearing a citation. | hard | judge |
| DS-103 | Grade honestly: solved / substantially / partial / deferred. | default | judge |
| DS-104 | Mark assumptions subtly at the side, never as noise. | default | render |
| DS-105 | Provenance mark upper-right. A working link where sources are reachable from where the deck is presented; plain text where they are not. **Never a dead link.** | default | auto |
| DS-106 | **No banned terminology** — five categories: empty phrases · inflated adjectives (*crucial, pivotal, seamless, leverage, synergy, friction*) · structural tells · syntactic patterns · voice absence. Also *"which is precisely why"*, *"worth saying out loud"*, *genuinely / actually / arguably / precisely*. | hard | auto |
| DS-107 | **The word-list check is necessary and not sufficient, and must say so.** Text passes all five categories and still reads as machine-written when it has no voice. | hard | judge |

> **DS-106 is owned by the `humanize-writing` skill.** Point at it; the list above is the inline
> fallback for machines where it is absent, because a pointer that resolves to nothing checks nothing.

### 3.4 The deliverable — what every slide owes its audience

**This is the section the rest of the argument rules serve.** A slide can satisfy every rule above —
claim headline, three fragments, a real diagram, no banned words — and still leave the audience
waiting for the presenter to say what the point was. That is a failure, and until now nothing here
named it.

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-201 | **Every slide delivers exactly one thing.** Name it before the slide is written. If it needs two sentences, the slide is two slides — or none. | hard | judge |
| DS-202 | **The deliverable appears on the slide as a bottom line**: one sentence, factual, no reasoning. Not the headline restated, not a summary of what is above it. | hard | auto |
| DS-203 | **The bottom line is the most prominent text after the headline** — recognisable in about two seconds, with no presenter talking. Accent colour, weight, position, and at most one Pulse-once. | hard | render |
| DS-204 | **Never bury the deliverable in a list, a paragraph or a table cell.** If it is one bullet among five, the audience has to find it, and they will find it after the presenter says it. | hard | judge |
| DS-205 | **The deliverable is never behind a disclosure.** DS-161 says a closed slide still makes its point; this says which part of the slide *is* the point. | hard | auto |
| DS-206 | **Supporting detail stays visible and subordinate — do not hide it under the click.** Disclosure earns its place for depth, never for tidying a slide that is merely full. Judge it per slide. | default | judge |
| DS-207 | **The deliverable is stated factually and directly.** No analogy, no metaphor, no rhetorical framing. Wit is allowed in the headline and in the presenter's mouth; the bottom line carries none of it. | hard | judge |
| DS-208 | **No native-speaker idiom, unless it is asked for.** Idioms, phrasal verbs used figuratively, sporting and cultural metaphors. **The reader may not be a native speaker, and no sentence should need a second pass.** Distinct from DS-097, which governs jargon: a reader can look a term up, and cannot look up an idiom they have misread as literal. | hard | judge |
| DS-209 | **One emphasis per slide, and it belongs to the deliverable.** DS-101 at slide scale: three emphasised things means none is emphasised, and the one that loses is the point. | hard | render |

### 3.5 The outline, before any slide exists

**Where the outline sits in the authoring pipeline is [T-020](../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md)'s.
What it must contain is a property of a good deck, so it is here.**

> **Settled 2026-08-07, and this section is what settled it.** T-020 §3.2 had placed outline
> sign-off *after* the specification review, which the DS-210 → DS-212 order below contradicts.
> The owner ruled for this order: the outline is signed off **before** it is expanded into the
> slide-by-slide specification. T-020 §3.2 carries the corrected pipeline; nothing in this table
> changed.

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-210 | **An outline exists before any slide does**, and covers every topic the deck is expected to carry. | hard | auto |
| DS-211 | Per slide the outline names, at minimum: **archetype · title · bottom line**. The bottom line in the outline is the same sentence that ships on the slide. | hard | auto |
| DS-212 | The outline is expanded into a **slide-by-slide specification** — structure, text, visuals, motion, interaction, title, bottom line — **page by page, never in one pass.** | default | judge |
| DS-213 | **The specification is reviewed slide by slide before any HTML is written**, for missing points, unnecessary detail, inconsistency and inefficiency, and the findings are fixed one at a time. | default | judge |

---

## 4. Visuals

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-110 | **No raster images.** Ever. | hard | auto |
| DS-111 | Diagrams are inline SVG. `<canvas>` and WebGL where they render better; prefer SVG where it is as good. | hard | auto |
| DS-112 | **Never hand-draw icons.** Lucide primary, Font Awesome free fallback. | hard | judge |
| DS-113 | Embed the icon set as an SVG symbol sprite containing **only the icons used**, referenced by `<use>`. | hard | auto |
| DS-114 | **One icon per concept, used consistently.** A repeated icon is a repeated idea. | hard | judge |
| DS-115 | Particles, connectors and custom diagrams may be drawn freely in SVG or canvas. | guidance | — |
| DS-116 | **Branch where the process branches.** Four boxes joined by arrow glyphs is not a flow diagram. | hard | judge |
| DS-117 | Connectors are **labelled**, always. Arrowheads are for **directional** connectors only, and they **meet their target**. An undirected edge gets no arrowhead: an arrow asserts a direction, and asserting one the data does not have is a wrong diagram rather than a tidy one. | hard | render |
| DS-118 | **Every SVG and chart is theme-aware.** No hard-coded fill or stroke. | hard | auto |
| DS-119 | `<canvas>` gets fixed pixel dimensions via HTML attributes; CSS scales it. | hard | auto |
| DS-120 | An accumulation effect must actually accumulate, not fall through. | hard | render |
| DS-121 | Charts obey the **encoding ranking** — position > length > area > hue. Variety never buys a worse encoding. | hard | judge |
| DS-122 | No chart library. Hand-written SVG, borrowing scale arithmetic as a few lines. | hard | auto |
| DS-123 | **"Boxes everywhere" is the rejected pattern.** Card grids, stat strips, pill rows and bulleted lists **used instead of a diagram** are a severity-H failure. | hard | judge |
| DS-214 | **Colour an SVG through CSS, never through a presentation attribute.** A class rule outranks `fill=` and `stroke=` silently, so an element styled by both renders the CSS colour and the attribute is dead markup — how a 2.17:1 run shipped past a palette audit that reported zero failures. This is DS-118's mechanism: theme-aware means *styled*, not *attributed*. | hard | auto |
| DS-215 | **Check the colour that renders, not the colour intended.** A palette audit compares token pairs an author nominates; it cannot see a pair nobody thought to nominate. Compare each text run's **computed** fill against the **computed** fill of whatever is painted behind it. DS-191, in the one place it has already cost this project a defect. | hard | render |
| DS-219 | **Never set text on a data mark.** To clear 1.4.11's 3:1 against the ground a neutral mark must be dark; to carry 1.4.3's 4.5:1 text it must be light. **No neutral does both.** The label goes outside the mark, or on a plate that earns 4.5:1 in its own right. A consequence of the accessibility floor, not a stylistic preference — and the reason a value-inside-the-bar chart cannot be made conformant by choosing a better grey. | hard | render |

---

## 5. Behaviour

### 5.1 Interaction and navigation

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-130 | **Every function keyboard-reachable**, including every disclosure control. | hard | auto |
| DS-131 | Keyboard ←/→/space/Home/End; prev/next arrows; clickable dots; click-to-jump; touch/swipe; wheel. | default | render |
| DS-132 | **Off-screen slides removed from the tab order.** | hard | auto |
| DS-133 | Progress indicator, **provided it encodes real position.** | default | render |
| DS-134 | **The spine ribbon**: the deck's argument shown with the current stage lit. | default | render |
| DS-135 | The page title and the nav-bar name for that page **must match**. | hard | auto |
| DS-136 | Interaction patterns built **once as components and reused**, so the UX is learnable. | hard | judge |
| DS-137 | Two simultaneous interactions need a **defined precedence rule.** | hard | judge |
| DS-138 | Popovers drop **below** the element, never above — **so the control sits high enough that its panel fits below it on the stage.** Panel placement constrains control placement, and the ruleset previously fixed only the first: a control near the foot of a 1080-unit stage cannot host a panel more than a row or two deep, and no styling of the panel repairs it. Choose the control's row from the panel's height. | hard | render |
| DS-139 | Assumption marker on the right edge, silent until wanted. | default | render |
| DS-216 | **One encoding of position, not three.** A spine ribbon, a dot per slide and a progress bar all answer *where am I*. Showing all three is noise competing with the slide. Pick one primary; a second is permitted only when it encodes a **different** fact — stage versus slide — and never a third. | default | render |
| DS-217 | **Chrome has a budget: roughly 12 labelled or interactive items, and ~90 design units of height.** Past that the navigation reads as an interface rather than as a deck, and per-slide dots stop scaling somewhere around ten slides. Prefer a compact indicator plus click-to-jump over one target per slide. | default | render |

### 5.2 Motion

**Governing rule: motion must encode something.** *What does this animation encode?* If the answer
is "it looks good", it is decoration and it goes.

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-140 | **A named vocabulary of exactly four motions, and nothing else:** Rise (entry, 340 ms, `cubic-bezier(.22,1,.36,1)`, 60 ms stagger) · Current (flow, dasharray 7 6, 4.5 s linear infinite) · Open/Turn/Scale (reveals, 380/420/300 ms) · Pulse-once (1.2 s, never looping). | hard | auto |
| DS-141 | **Entry and transition animations max 500 ms**, ease-in-out. Inter-slide transition 400–500 ms. **DS-141 governs entry and transition only; DS-140's named vocabulary is the specific override** — Pulse-once at 1.2 s and Current at 4.5 s are conformant by name, not exceptions to be argued. A duration over 500 ms that is *not* one of DS-140's four is a defect. | hard | auto |
| DS-142 | **No continuous ambient glow, pulse or drift on static content.** | hard | auto |
| DS-143 | `prefers-reduced-motion` honoured, **and the semantics survive it** — the dashed arrows stay dashed. | hard | render |
| DS-144 | **No 3D transitions between slides**, no flashy zooms, no punchy cuts. The 3D reveal of a card is permitted. | hard | auto |
| DS-145 | Hidden elements reveal by opening, turning or scaling. Flows use dashed arrows, slowly animated. | default | render |
| DS-146 | Charts draw in **once**; never re-animate on back-navigation. **The draw-in is DS-140's Rise applied to the chart's marks, staggered — not a fifth motion.** A stroke-dash draw would add one to a vocabulary DS-140 fixes at four, which is the trade this rule is not permitted to make. | hard | render |
| DS-147 | Count-up on headline statistics; **one** emphasis pulse on the key number per slide. | default | render |
| DS-148 | When a diagram changes mode, animate nodes to their new size and position. | default | render |
| DS-149 | Entrance animations with `fill-mode: forwards` keep their stacking context. | hard | render |
| DS-150 | **Every animation answers *what does this encode?*** Depth, shadow, transparency and shaders are subject to the same test. | hard | judge |
| DS-218 | **Motion that loops, or runs over 5 s, ships with a persistent, keyboard-operable control that stops it** — and the deck still reads with motion off. DS-140's `Current` is infinite, so **every deck with a flow diagram needs this control**, and §7's 2.2.2 stated the obligation without any rule here requiring the deck to build one. Distinct from DS-143: `prefers-reduced-motion` is what the reader's system asks for; this is what the reader can reach. | hard | auto |

### 5.3 Progressive disclosure

**Not a feature of the deck — the reason the deck can be two things.** The modifier A-13 applies to
every archetype.

| ID | Rule | Label | Check |
| :--- | :--- | :--- | :--- |
| DS-160 | **Two tiers, never three.** Slide → detail. Never slide → detail → further detail. | hard | auto |
| DS-161 | **Closed, the slide still makes its point.** Opening may deepen the argument; it may never complete it. | hard | judge |
| DS-162 | The split test: **would the argument survive without it?** If no, it is tier one. | hard | judge |
| DS-163 | **Never hover-only.** Tooltips may supplement; never the only route to content. | hard | auto |
| DS-164 | Every disclosure control has a **visible affordance with a real label.** A bare chevron does not qualify. | hard | render |
| DS-165 | The disclosure mark is a **tokenised element of the theme**, not a per-slide invention. | hard | auto |
| DS-166 | **Disclosure state never required to advance.** Arrows advance; a separate key toggles; the two do not interact. | hard | auto |
| DS-167 | Every affordance **available and visible during the talk, never load-bearing in it.** | hard | judge |
| DS-168 | Targets ≥ 24 × 24 CSS px, or the spacing exception — which **inside the stage means ≥ 48 × 48 design units**. The stage scale bottoms out at 0.5 before DS-071 hands over to the reflow view, so a design unit is worth half a CSS pixel at the smallest size the stage is ever shown. **Sizing a control at 24 design units matches the number and fails the criterion.** | hard | auto |
| DS-169 | One meaningful interaction per slide, where it adds signal. Never decoration. | default | judge |
| DS-170 | Push longer text behind interaction rather than onto the slide. When detail is unavoidable: hide it, or split to a new page. | default | judge |

---

## 6. Anti-patterns

Stated here so the critique pass and the standard cannot drift apart. **T-004 consumes this list; it
does not own it.**

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
| [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md) | Building §2.5 |
| [T-001](../tasks/T-001-decide-the-font-strategy-embedded-subsets-or-a-syste.md) · [T-006](../tasks/T-006-decide-the-chart-strategy.md) · [T-007](../tasks/T-007-define-the-parametric-theme-layer.md) | The three standing decisions |

**Four rules about checking that stay here**, being claims about what a check may assert:

| ID | Rule | Label |
| :--- | :--- | :--- |
| DS-190 | **Structural checks say nothing about layout — always render and look.** | hard |
| DS-191 | **DOM measurement confirms geometry you suspect; it cannot find a defect you never thought to measure.** | hard |
| DS-220 | **A box clamped by its grid track never reports an overflow.** Content taller than a `1fr` track spills silently: the box measures exactly the track, so comparing the box against the stage finds nothing wrong. **Compare `scrollHeight` against `clientHeight`** — the box is the wrong thing to measure. | hard |
| DS-221 | **Pin motion off before capturing.** DS-140's infinite `Current` means a headless render never reaches a quiescent state, so the screenshot fires mid-transition and yields a convincing blank slide. A render gate that does not disable animation is measuring an arbitrary frame and reporting it as the deck. | hard |

---

## 9. What is not covered

**Tested once, by building a deck** — [T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md)
built [`examples/reference-deck.html`](../examples/reference-deck.html) strictly to this document and
produced **thirteen findings**, four of them conflicts between two `hard` rules. All thirteen are
reconciled by [T-025](../tasks/T-025-reconcile-the-twelve-ruleset-findings-from-the-reference-deck.md),
which amended nine rules and added four; **each conflicting pair now names which rule yields, in the
rule text.** What that reconciliation is worth is bounded by what produced it: **one deck**. Every
amendment is a correction from a single build, and a second deck would be expected to find more.

**What that build did not test.** It was one deck, one topic, one author, and it was scored by the
agent that wrote it. §3.4 and §3.5 arrived *after* it, from the owner's review, so **no deck in this
repository yet satisfies the deliverable contract** — the rules that matter most are the least
exercised. The reproducibility rulings still come from R6's capability matrix, which answers *"is
this available?"* rather than *"does this read well?"* CLAUDE.md rule 6 governs the second question,
and it is answered by looking, not by this document.

Sources, verdicts, provenance and every "why": [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md).
