# R4 — Prior art, and where the corpus rules actually came from

Deliverable of [T-012](../../tasks/T-012-research-existing-html-deck-skills-and-libraries.md).
Companion to [R1](R1-corpus-conventions.md) and its
[rules register](R1-rules-candidate.md).

**Status: partial.** Sections 1–4 and 7 are complete and evidenced. Sections 5–6 — the wider
ecosystem survey, the deck frameworks, and the motion/3D libraries — are **not done**; see
§8. The provenance pass that gates
[T-014](../../tasks/T-014-synthesise-research-into-the-design-system-reference.md) is complete,
so T-014 is unblocked regardless of §8.

---

## Bottom line

**The corpus decks were built on top of a general-purpose deck skill, and roughly a quarter of
what R1 recorded as "the owner's conventions" is that skill's default showing through.** Of the
154 candidate rules, 42 (27%) restate something the skill already says, several of them
near-verbatim.

That is the expected finding, and it is not the important one. Two things are:

**1. The owner's taste is real, and it is concentrated.** 86 rules (56%) have no counterpart in
the skill at all, and they are not scattered — they cluster hard in exactly four places: the
**critique mode** (11 of 11 rules, zero prior art), the **document process** (10 of 11), **writing
and content discipline** (18 of 25), and the **semantics of interaction** as opposed to its
mechanics (F17–F22). These are the areas where htmldeck is building something that does not
exist, and they are the areas the plugin should be *about*.

**2. R1's list of departures was wrong in both directions, and the errors matter.** R1 flagged
five departures. One of them is not a departure, one is only half of one, and **seventeen
departures went unflagged** — including the two sharpest conflicts in the whole corpus. Details
in §3.

The single most consequential correction: **the skill prescribes, as its house style, the exact
pattern the owner's design audit classes as a severity-H failure.** The skill's answer to a
complex system is "CSS grid cards", a "hybrid overview + detail cards" pattern, KPI card rows and
a "CSS Pipeline Slide" of step-cards joined by arrow glyphs. Rule E9 calls card grids and pill
rows in place of diagrams the rejected pattern; rule E10 says in as many words that "four boxes
joined by arrow glyphs is not a flow diagram". The owner did not drift from the skill here. They
looked at its central layout recommendation and ruled against it.

---

## 1. What was read, and how

The skills the corpus names as its authorities do not appear in any of the obvious places —
`~/.claude/skills`, the plugin marketplace cache, or the project. They ship as an installed
plugin bundle whose payload sits in the desktop app's application-data tree.

**Two environment facts worth carrying, because each cost time here:**

- **The sandboxed PowerShell tool cannot see that tree, and reports it as non-existent rather
  than as denied.** `Get-ChildItem` on the skill directory returns "Cannot find path"; a
  recursive search returns nothing at all, with no error. Bash and the file-reading tools read
  the same path without trouble. A session that trusts the shell here concludes the skills have
  no files on disk, which is false. This is rule M11 with a new costume — the convenient source
  answered confidently and wrongly, twice in one sitting.
- **A skill's own body is only half of it.** `SKILL.md` is a routing table; the substance is in
  `references/` and `templates/`, which are several times longer and are where nearly all of the
  rules below were actually found. Reading the skill body alone would have missed most of the
  matches.

Read in full for this pass: the deck skill's `SKILL.md`, `references/slide-patterns.md`,
`references/css-patterns.md`, `references/libraries.md`; and `humanize-writing/SKILL.md`.

## 2. The provenance verdicts

Four verdicts, one per rule. The full per-rule table is §9.

| Mark | Meaning | Count | Share |
| :--- | :--- | ---: | ---: |
| **O** | **Owner-authored.** No counterpart in the skill | 86 | 56% |
| **I** | **Inherited.** The skill states substantially the same thing | 42 | 27% |
| **D** | **Departure.** The skill states a different default, and the owner overrode it | 22 | 14% |
| **O/S** | Owner-authored, but **already shipped in the owner's other skill** (`humanize-writing`) | 4 | 3% |

`O/S` is a category T-012 did not anticipate and needs. Rules B22 and B23 — the five AI-tell
categories, and the argument that a word-list check is insufficient — are not inherited from a
third party's skill. They are the owner's own writing, in the owner's own skill, reproduced into
the corpus specs. B22's five categories are the five numbered headings of that skill's step 2;
B23's definition of voice is its step 3, bullet for bullet. The consequence is the opposite of
the `I` rules: htmldeck should not re-derive these **and should not vendor them either** — it
should defer to the skill that already owns them, with a fallback for when it is absent.

### Where each verdict clusters

| Section | O | I | D | O/S | Reading |
| :--- | ---: | ---: | ---: | ---: | :--- |
| M — Critique | **11** | 0 | 0 | 0 | Wholly the owner's. The skill has no critique mode |
| A′ — Process | **10** | 1 | 0 | 0 | Wholly the owner's |
| B — Writing | **18** | 2 | 1 | **4** | The owner's, with the AI-tell rules owned by their other skill |
| F — Interaction & motion | **11** | 6 | 5 | 0 | Split: mechanics inherited, semantics owner's |
| E — Diagrams & icons | 9 | 3 | **4** | 0 | The icon discipline is the owner's; the diagram stance is a fight |
| H — Layout | 6 | 1 | 0 | 0 | The owner's |
| K — Verification | 5 | 1 | 1 | 0 | The owner's |
| G — Navigation | 5 | **7** | 0 | 0 | **G1–G7 are the skill's slide engine, entire** |
| C — Colour | 1 | **8** | 5 | 0 | Mostly inherited discipline, with a sharp fork on ground and accent count |
| D — Typography | 1 | **5** | 1 | 0 | **The typography is largely the skill's** |
| A — Structure | 5 | 3 | 2 | 0 | Mixed |
| L — Stage & archetypes | 1 | 3 | 2 | 0 | The archetype *idea* is inherited; the stage is a departure |
| J — Portability | 3 | 0 | 1 | 0 | Short section, but J1 is the load-bearing departure |
| I — Theming | 0 | 2 | 0 | 0 | Inherited, with the tokens renamed |

**The three inherited clusters are the finding.** Navigation (G1–G7), typography mechanics
(D1–D6) and colour discipline (C) are not where this project's taste lives — they are where it
has been quietly restating a dependency. Together they are 20 of the 42 inherited rules.

Two of them are near-verbatim rather than merely similar:

- **G3** (keyboard: ←/→/space/Home/End) is the skill's `SlideEngine` key bindings exactly —
  `ArrowDown`/`ArrowRight`/space/`PageDown` forward, `ArrowUp`/`ArrowLeft`/`PageUp` back, plus
  `Home` and `End`. G1, G2, G4, G5, G7 are the chrome that engine builds: prev/next, dots,
  progress bar, counter, click-to-jump and touch swipe.
- **D2** (never Inter, Roboto, Arial or system-ui) is the skill's forbidden-font list, including
  its reasoning. The skill calls Inter "the single most overused AI default font"; R1 records the
  same four faces as "generic tells".

D1's "deliberate pairing per deck" is the skill's pairing table plus its instruction to rotate
and never repeat a pairing. R1 already noticed that Bricolage Grotesque, IBM Plex and Fraunces
recur across the corpus and read it as the owner's signature. **They are three rows of that
table.**

## 3. The departures — corrected

R1 flagged L1, J1–J2, D3, F11 and G11. Checked against the source:

| R1's flag | Holds? | What the evidence actually shows |
| :--- | :--- | :--- |
| **L1** — fixed 1600×900 scaled stage | **Yes** | The skill's slide is `height: 100dvh` in a scroll-snap container. The owner's fixed stage is a considered override, and L2 (the stage floating on a darker field) follows from it |
| **J1** — self-containment | **Yes, and sharper than R1 states** | The skill *also* says "complete self-contained HTML document" — but its `references/libraries.md` is titled **"External Libraries (CDN)"** and loads Mermaid, Chart.js, anime.js and Google Fonts from jsDelivr. The skill means *one file*; the owner means *no network*. The words are inherited and the meaning is the departure — which is exactly how a rule gets restated without being re-decided |
| **D3** — embedded base64 faces | **Yes** | The skill loads fonts via `<link>` to Google Fonts with `display=swap`. Embedding is a direct override, and the only mechanism by which D1/D2's inherited typography can survive rule 1 |
| **F11** — the four-motion vocabulary | **Half** | The skill's `css-patterns.md` has a **"Choreography"** section that names four motions by element role — `fadeUp` for cards, `fadeScale` for KPIs, `drawIn` for connectors, `countUp` for hero numbers — with `calc(var(--i) * 0.06s)` stagger and an instruction not to use one animation for everything. **The four-slot shape is inherited.** The owner's names, durations and easings are their own, and one of the four (*Current*, `4.5s linear infinite`) directly violates the skill's ban on continuous motion. Departure in content, not in concept |
| **G11** — the spine ribbon | **No — reclassify as owner-authored** | The skill has dots, a progress bar and a counter: position indicators. None of them carries the argument. A ribbon showing the deck's *reasoning* with the current stage lit has no counterpart to depart from. This is invention, and R1 filed it under the wrong heading |

### The seventeen that were not flagged

Ordered by how much they change what htmldeck builds.

| # | Rule | The skill's default | The owner's ruling |
| :--- | :--- | :--- | :--- |
| 1 | **E9, E10** | Card grids, KPI rows, "hybrid overview + detail cards", and a **CSS Pipeline Slide** of step-cards joined by arrow SVGs — prescribed as the house layout, and *preferred over a diagram* for linear flows | **Severity-H failure.** "Boxes everywhere" is the rejected pattern; "four boxes joined by arrow glyphs is not a flow diagram"; branch where the process branches |
| 2 | **A2** | "Do not drop content to fit a fixed slide count. **Add slides instead.**" A 7-section source "typically produces 18–25 slides, not 10–13" | Target 8, hard ceiling 10; past 8 needs a stated reason. **The exact opposite instruction** |
| 3 | **E4** | Mermaid — a CDN module — is the default for flowcharts, sequence, ER, state, class and C4. Inline SVG is for decorative accents and sparklines | Diagrams are inline SVG. (Compounds J1: the skill's diagram engine *is* a network dependency) |
| 4 | **E5** | Generated raster images are permitted and encouraged — hero banners, inline illustrations, full-bleed backgrounds, base64-embedded. "Generate 2–4 images minimum" for decks over 10 slides | **No raster images**, anywhere |
| 5 | **C1, C2** | 3–5 accents, plus semantic `--node-a/b/c` roles | Neutral ground plus **one** accent; interest comes from contrast, depth, typography, rhythm and motion — not more colour |
| 6 | **C9, C10** | Presets use pure white (`#ffffff`) and near-black grounds; two of four are dark-first | Never pure white, never pure black. **Light by default**, argued from projector contrast in lit rooms |
| 7 | **C6** | "Flat backgrounds feel dead." Gradient mesh, radial glows, per-slide background variation | Gradients only when functional — depth or progress — never decoration |
| 8 | **F12, F13** | Durations to 0.8s (`drawIn`) and 1.2s (`countUp`); reduced-motion collapses everything to `0.01ms !important` on `*` | Animations max 500 ms; and reduced motion must **keep the semantics** — the dashed arrows stay dashed rather than stopping |
| 9 | **F1, F4** | Collapsible details in a source "are not optional in the deck — **they become their own slides**" | Push longer text behind interaction. And flows use *continuously* animated dashed arrows, which the skill's F7-equivalent forbids |
| 10 | **B14** | 1 heading + 5–6 bullets, max 2 lines each | Headline ≤6 words plus ≤3 supporting fragments. Roughly half |
| 11 | **A8** | Slides fill the viewport | Pages sit in a container that gives each a boundary, resolution-independent |
| 12 | **K2** | `autoFit()` — a runtime script that shrinks overflowing content after render | Measure every slide's content height against available height and **print a table**. Detection, not concealment |

**A note on #7 that is worth carrying to T-014.** The skill contradicts itself here: its `SKILL.md`
bans "gradient-mesh blobs" among generic defaults, while its `css-patterns.md` supplies a
**"Gradient mesh"** recipe under "Background Atmosphere". The owner's C6/C12 land on the
`SKILL.md` side. So one apparent departure is really the owner picking a side in the skill's own
unresolved argument — which is a reason to state C6 as a rule with its reasoning attached, not to
assume the skill would disagree.

### What this does to R1's gaps register

- **G-2 (slide archetypes) was recorded as "Closed" from the corpus.** It is closed by an
  inherited rule: L3's archetype set maps nearly one-to-one onto the skill's ten slide types
  (Hero/Statement≈Title, Loop/chapter≈Section Divider, Split compare≈Split, Stat focus≈Dashboard,
  Chart focus≈Dashboard, Process/flow≈Diagram). **Timeline, Case file and Verdict are the
  owner's three additions.** The gap is closed, but by a dependency, and T-014 should know which
  three rows carry the taste.
- **G-10 (motion vocabulary) likewise** — closed by F11, whose four-slot shape is the skill's.
- **G-8 (banned terminology) is closed by `O/S` rules**, meaning it is closed by a skill htmldeck
  can call rather than by anything it needs to build.

## 4. What the skill owns that the corpus never wrote down

The reverse question, and it turns out to matter: the skill carries hard-won defect knowledge
that R1 has no rule for, because the corpus never hit the failure or never recorded it.

- **Overflow protection.** Grid and flex children default to `min-width: auto` and will blow out
  their container; `display: flex` on an `<li>` creates an anonymous flex item that **cannot** be
  given `min-width: 0`, so a line with several inline code badges overflows with no CSS fix
  available. R1's H section has nothing on this.
- **List markers overlapping container borders** — any list inside a bordered card needs
  `list-style-position: inside` or `padding-left: 2em`; the usual 20px is not enough.
- **Namespace collision** — never use `.node` as a page-level class, because Mermaid uses it
  internally on its SVG groups and page styles leak in and break the layout. Generalises: a deck
  that vendors any diagram renderer needs a namespace discipline.
- **Theme-hostile static config** — never set `color:` in a Mermaid `classDef`, because it
  hardcodes a value that breaks in the opposite scheme. R1's E15 states the principle; the skill
  states the specific trap.

These belong in htmldeck's build check, and none of them came from the corpus. Sourcing them is
legitimate — they are defect knowledge, not taste.

## 5. Deck frameworks — NOT DONE

See §8.

## 6. Motion and 3D libraries — NOT DONE

See §8. One data point landed incidentally: the skill uses **anime.js 3.2.2** from jsDelivr for
orchestrated entrances, staggered reveals, path drawing and count-up numbers, and explicitly
treats CSS `animation-delay` staggering as sufficient below ~10 elements. That is a licence and
inlined-size question for T-012's remaining work, not an answer.

## 7. Detecting another skill — answered

T-012's open question was how a skill establishes that another is installed without failing
noisily when it is not.

**Do not probe the filesystem.** §1 shows why: the paths are installation-specific, they sit
outside every documented skill location, and the one shell tool that would normally check them
reports a readable directory as non-existent. Any detection built on file probing is wrong on at
least one supported configuration, and wrong *silently*.

**The workable contract is capability-first, not presence-first.** htmldeck should:

1. **Never branch on whether a skill exists.** Branch on whether the *artefact* it would have
   produced is present. The build proceeds identically either way.
2. **Ship the fallback as the primary path.** The self-contained core produces a complete deck
   with no other skill installed. An enhancement path is an improvement applied to a finished
   artefact, never a step the deck needs to reach "done".
3. **Let the user's invocation be the signal.** The one reliable indicator that another skill is
   available is that the user, or the agent acting for them, invoked it. Invocation is
   observable; installation is not.
4. **State the degradation in the output.** The build check already has to say which half it ran
   (BRIEF, *What to build*). Which enhancements were unavailable belongs in the same report.

This generalises a pattern the skill already uses and states plainly: it checks for an optional
image generator, and instructs that when it is missing the page must "degrade gracefully to CSS
gradients and SVG decorations… **Never error on missing** [it]", leaving an HTML comment
recording the fallback. The mechanism is worth copying; the specific tool is not.

**Consequence for the two `O/S` rules.** `humanize-writing` is the right owner of B22/B23, and
htmldeck should defer to it — but under rule 2 above, the terminology check cannot *depend* on
it. htmldeck ships its own word-list check as the primary path, states in the output that a word
list is necessary and not sufficient (which is B23, and which R1 records as contradiction X-10),
and treats a fuller voice pass as the enhancement.

## 8. What is still outstanding

Plan steps 4, 5 and 6 are not done: the published HTML-deck skills and plugins in the wider
ecosystem, the deck frameworks (reveal.js, Slidev, Marp, Spectacle, impress.js) against
self-containment, the motion and 3D libraries (GSAP, Motion, anime.js, three.js) on licence,
inlined size and `file://` behaviour, and the plugin packaging survey that feeds T-015 and T-008.

They are outstanding because the provenance pass consumed the session, and provenance was
sequenced first deliberately: it is what gates T-014, and the remaining steps do not.

**None of them blocks T-014.** They block T-001 (fonts), T-006 (charts), T-016 (motion) and
T-015/T-008 (packaging). The packaging survey has a cheap local source that was located but not
read: the `plugin-dev` plugin installed in this environment ships skills for plugin structure,
skill development, command development and plugin settings — a first-party worked example rather
than documentation about one.

## 9. Per-rule provenance table

`O` owner-authored · `I` inherited · `D` departure · `O/S` owner's own, in `humanize-writing`

### A. Structure

| Rule | | Evidence |
| :--- | :---: | :--- |
| A1 `<section>` per slide | I | The skill's deck is `<section class="slide">`, one per slide |
| A2 Target 8, ceiling 10 | **D** | The skill: add slides rather than drop content; 18–25 from a 7-section source |
| A3 Never fewer than 6 | O | No minimum stated in the skill |
| A4 Specify slide-by-slide before building | I | "Map source to slides"; assign a composition to each before writing HTML. The owner extends it to animations, interactions and a bottom line |
| A5 Build the spec page by page, not in one pass | O | — |
| A6 Review the spec before any HTML exists | I | "Verify before writing HTML" |
| A7 Build slides in batches | O | — |
| A8 Pages sit in a bounded, resolution-independent container | **D** | The skill's slide fills the viewport |
| A9 One strong closing line plus one supporting | O | The skill has no closing-slide type |
| A10 No speaker notes or presenter markers | O | — |

### A′. Process

| Rule | | Evidence |
| :--- | :---: | :--- |
| A′4 Review the specification before any HTML | I | "Verify before writing HTML" |
| A′1–A′3, A′5–A′11 | O | The skill has no specification-document concept at all — no governing idea, no foundation spec, no review cycle, no trace table, no timing budget |

A′11 deserves note: *"be brave to depart when a different idea communicates better"* is a
meta-rule licensing exactly the departures catalogued in §3. The owner wrote down the permission
to override the skill.

### B. Writing style and content

| Rule | | Evidence |
| :--- | :---: | :--- |
| B7 Avoid AI-favoured terminology | **O/S** | `humanize-writing` step 2 |
| B12 Visuals aid non-expert comprehension | I | The skill's founding premise |
| B14 Headline ≤6 words + ≤3 fragments | **D** | The skill allows 5–6 bullets of up to 2 lines |
| B17 Cut words, never findings | I | "Do not drop content to fit a fixed slide count" |
| B19 Bold the fact, not the emphasis | **O/S** | `humanize-writing` names habitual bold-label bullets a structural tell |
| B22 The five AI-tell categories | **O/S** | The five numbered headings of `humanize-writing` step 2, in order |
| B23 A word-list check is not sufficient; voice = position, varied rhythm, ambivalence, first person, tolerated imperfection | **O/S** | `humanize-writing` step 3, bullet for bullet, plus its opening argument that chasing a detector produces worse writing |
| B1–B6, B8–B11, B13, B15, B16, B18, B20, B21, B24, B25 | O | — |

### C. Colour

| Rule | | Evidence |
| :--- | :---: | :--- |
| C1 One accent | **D** | The skill: 3–5 accents plus semantic node roles |
| C2 Interest from contrast, not more colour | **D** | Follows from C1 |
| C3 The accent carries meaning | I | Semantic accent roles |
| C4 Semantic role colours fixed deck-wide | I | Fixed status colours |
| C5 Calm colours | O | — |
| C6 Gradients only when functional | **D** | "Flat backgrounds feel dead"; gradient mesh and per-slide radial variation prescribed — though its own `SKILL.md` bans gradient-mesh blobs |
| C7 One palette per deck | I | Four presets, each adapted per deck |
| C8 Both themes readable | I | "Always define both light and dark palettes" |
| C9 Never pure white or black | **D** | Presets use `#ffffff` and near-black |
| C10 Light, not dark, by default | **D** | Two of four presets are dark-first. The violet-cliché half of the rule is inherited; the projector argument is the owner's |
| C11 Dark is one block of overrides | I | `data-theme` toggle |
| C12 No gradient blobs, no neon | I | Near-verbatim from the skill's generic-defaults ban |
| C13 Green/red/amber, fixed, with a legend | I | `status--match/gap/warn`. The visible legend is the owner's addition |
| C14 The accent must survive a bad projector | I | The framework-default ban is the skill's; the projector reasoning is the owner's |

### D. Typography

| Rule | | Evidence |
| :--- | :---: | :--- |
| D1 Deliberate pairing per deck | I | The skill's pairing table, plus "never use the same pairing twice in a row" |
| D2 Never Inter, Roboto, Arial, system-ui | I | The skill's forbidden-body-font list, with the same reasoning |
| D3 Embed faces as base64 `@font-face` | **D** | The skill loads Google Fonts by `<link>` |
| D4 `clamp()` for fluid type | I | Used throughout the skill; the owner's values are smaller |
| D5 Body 18–24px/1.55; mono labels uppercase, tracked | I | The skill's `__body` and `__label` scales, near-identical |
| D6 `text-wrap: balance`, negative tracking on display | I | The skill's `.slide__display` verbatim |
| D7 The mono layer carries the domain vocabulary | O | The skill uses mono for labels and captions only |

### E. Diagrams, icons, illustration

| Rule | | Evidence |
| :--- | :---: | :--- |
| E4 Diagrams as inline SVG | **D** | The skill's default diagram engine is Mermaid, over CDN |
| E5 No raster images | **D** | The skill permits and encourages generated raster imagery |
| E8 Fixed pixel dimensions on `<canvas>` | I | Its Chart.js canvas |
| E9 "Boxes everywhere" is the rejected pattern | **D** | The skill prescribes card grids, KPI rows and hybrid overview+cards as house style |
| E10 Branch where the process branches | **D** | The skill's CSS Pipeline Slide is step-cards joined by arrow SVGs, *preferred over a diagram* for linear flows |
| E11 Arrowheads that meet their target | I | Its connector example carries an arrowhead |
| E15 Every SVG and chart theme-aware | I | Its `classDef` colour warning is the same defect |
| E1–E3, E6, E7, E12–E14, E16 | O | The skill says nothing about icon sets, sprites, particle restraint or chart variety |

### F. Interaction and motion

| Rule | | Evidence |
| :--- | :---: | :--- |
| F1 Push longer text behind interaction | **D** | The skill: collapsibles in the source "become their own slides" |
| F4 Continuously animated dashed flow arrows | **D** | Violates the skill's own ban on continuous motion (F7) |
| F6 Motion only where it clarifies | I | "Use entrance/hover animation only when it clarifies hierarchy" |
| F7 No continuous glow/pulse/drift | I | Near-verbatim |
| F8 Depth allowed, no overdose | I | "Use depth sparingly" |
| F9 Respect `prefers-reduced-motion` | I | Throughout |
| F11 Four named motions | **D** (shape I) | The skill's "Choreography" section names four by element role, with stagger. Concept inherited, content departed |
| F12 Max 500 ms | **D** | The skill runs to 800 ms and 1.2 s |
| F13 Reduced motion keeps the semantics | **D** | The skill collapses all animation to `0.01ms !important` |
| F15 Charts draw in once | I | "Animate in once and stay visible when scrolling back" |
| F16 Count-up on headline statistics | I | Its `countUp`. The single emphasis pulse is the owner's |
| F2, F3, F5, F10, F14, F17–F22 | O | The interaction *semantics* — disclosure as judgement, precedence rules, one meaningful interaction per slide, reuse as components — have no counterpart |

### G. UI controls and navigation

| Rule | | Evidence |
| :--- | :---: | :--- |
| G1 Prev/next | I | `SlideEngine` chrome |
| G2 Carousel dots | I | `.deck-dot`, clickable |
| G3 Keyboard ←/→/space/Home/End | I | Its key bindings exactly |
| G4 Progress bar | I | `.deck-progress` |
| G5 Slide counter | I | `.deck-counter` |
| G6 Wheel navigation | I | Scroll-snap; its own hint text says "or scroll to navigate" |
| G7 Click-to-jump, touch/swipe | I | `goTo(i)` on dot click; touchstart/touchend |
| G8–G12 | O | Title/nav agreement, provenance mark, assumption marker, **spine ribbon**, appendix naming |

### L. Stage and layout archetypes

| Rule | | Evidence |
| :--- | :---: | :--- |
| L1 Fixed 1600×900 scaled stage | **D** | `height: 100dvh` in a scroll-snap container |
| L2 The stage floats on a darker field | **D** | Follows from L1 |
| L3 Named, reused slide archetypes | I | Its ten slide types. Timeline, Case file and Verdict are the owner's additions |
| L4 One dominant accent per slide | O | — |
| L5 Consistent margins, one grid | I | Consistent padding clamps |
| L6 12–16px radius, soft shadow, hairline | I | `.ve-card` at 10px radius with the same shadow tiers |

### H. Layout · I. Theming · J. Portability · K. Verification · M. Critique

| Rule | | Evidence |
| :--- | :---: | :--- |
| H1 Grid and flexbox throughout | I | Throughout |
| H2–H7 | O | Align by construction, sibling sets, no duplicate emphasis, no nested text boxes, full heading reset, no bare `<b>` |
| I1 Theme via custom properties | I | Its palette variables |
| I2 Stable token vocabulary | I | Same concept, renamed — `--ink` for its `--text`, `--line` for its `--border` |
| J1 One self-contained file | **D** | Its "self-contained" means one file; its library reference loads four CDN dependencies |
| J2–J4 | O | Quality over self-containment, mandatory charset, the benign `file://` warning |
| K4 Suspect the SVG's aspect ratio first | I | Its `autoFit()` treats diagram SVG sizing as the known overflow cause |
| K2 Measure content height, print a table | **D** | Its `autoFit()` shrinks at runtime instead of reporting |
| K1, K3, K5–K7 | O | Render and look, two viewport sizes, the limits of DOM measurement, re-verify after interaction, cross-document sweep |
| M1–M11 | O | **The skill has no critique mode.** Its final checklist is self-verification against its own invariants — no severity scheme, no headline verdict, no keep-vs-rebuild split, no named defect classes, no "open — needs a decision" |
