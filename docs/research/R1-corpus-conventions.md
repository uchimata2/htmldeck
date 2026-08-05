# R1 — Corpus conventions

What the owner's existing decks and written specifications actually do, measured. Deliverable of
[T-009](../../tasks/T-009-analyse-the-corpus-extract-my-deck-conventions.md).

**Scrubbed.** Decks are identified as **D1–D12**; the mapping to real files, along with the
full-fidelity extraction, lives in the gitignored `.kb/` and never publishes. Numbers come from
`tools/kb/extract.py`, which passes a 20-assertion self-test on a hand-counted case before it is
believed — the corpus itself contains a scan that was trusted and wrong by 15×.

---

## 0. What was measured

346 unique files after collapsing duplicates and excluding Notion exports, backup trees and
third-party source pages: **291 Markdown, 26 SVG, 23 HTML, 3 Python**. Of the HTML, **12 are
decks** (≥4 slide containers, ≥4 KB); 11 are diagram fragments or document exports.

The corpus also contains something better than artefacts: **written specifications of the owner's
own taste** — a durable style guide, a requirements specification with IDs, feedback prompts, and a
cross-document consistency sweep. Where those and the decks disagree, §7 says so.

---

## 1. Three findings that correct `docs/BRIEF.md`

**1. Self-containment is already solved, not merely aspired to.** The brief states every deck
carries 2–7 external references. Measured across 12 decks the range is **0–21**, and **three decks
have none at all**. One of them, **D9**, is the strongest artefact in the corpus: 9 slides, **22
inline SVGs, 7 `@font-face` rules with all 7 faces embedded as base64 data URIs**, zero external
references, 282 KB. The identity-versus-self-containment trade-off in open question 1 was already
resolved once, by embedding — and the file size it cost is known.

**2. A token vocabulary already exists and is stable across decks.** Every deck drives its theme
from CSS custom properties (8–26 per deck). The naming recurs independently of topic: `--ink`
**11/12**, `--bg` 9/12, `--line` 8/12, `--shadow` 7/12, plus semantic colour roles (`--amber`,
`--blue`, `--green`, `--red`). T-007's parametric token layer is not a new invention; it is the
formalisation of something the owner already does by habit.

**3. The JavaScript minimalism was never a principle.** Script tags run 0–5, usually 1 — but that
reflects what CSS could already do, not restraint. The written spec asks for CDN libraries "to
boost visuals with neat, eye-candy elements" and for shaders, transparency and soft shadows. The
brief read a capability ceiling as a design value.

---

## 2. Structure and pacing

| | Measured |
| :--- | :--- |
| Slides per deck | **6–18**, median **10** |
| Written target | **8 slides, 10 ceiling**; going past 8 requires a stated reason |
| Prompt default | 6–9 pages |
| Slide container | `<section>` per slide, universally |

The stated target (8–10) and the actual median (10) agree; the two decks at 15 and 18 are the
outliers, both built for a longer analytical brief rather than an executive audience. **Under 6
does not occur.**

Process convention, stated explicitly and followed: **specification before implementation**, built
**page by page and explicitly not in one pass**, each slide specified for structure · text ·
visuals · animations · interactive elements · title · bottom line. Then a slide-by-slide review of
the *specification* listing issues, inefficiencies, inconsistencies, unnecessary detail and missing
points — before any HTML exists. Then build in **batches**, so feedback lands before the whole deck
is built out.

---

## 3. Typography

| | Measured |
| :--- | :--- |
| Sans | Inter in 6/12, then Manrope, Plus Jakarta Sans, Segoe UI, Helvetica |
| Serif / display | Fraunces in 3/12, Source Serif Pro, Bricolage Grotesque |
| Mono | IBM Plex Mono, JetBrains Mono, Space Mono, Consolas |
| Pairing | Deliberate, per deck: a sans for body, a display face for headings, a mono for labels and data |
| Embedded | **1/12** (D9, 7 faces as data URIs) |
| Heading length | median **2–7 words**, max 16 across the whole corpus |

> **Correction.** An earlier reading of this table called Inter "the clear default". It is the most
> *frequent* face, and the written specs reject it: **"No Inter, Roboto, Arial or system-ui — the
> skill names those as generic tells."** A design audit grades a system-font body as a severity-H
> quality failure. Inter is the legacy default the refined decks moved away from, not the target.
> The mature pairing is a characterful display face plus **one superfamily** for body and label
> (Bricolage Grotesque + IBM Plex Sans/Mono), so body and label read as a single register rather
> than a third font.

**Type scale, from the most developed spec:** display `clamp(34px, 4.2vw, 56px)`, letter-spacing
−1.5px, `text-wrap: balance` · body 18–24px, line-height 1.55 · mono labels 11–13px, uppercase,
letter-spacing 1.4px.

Headings are short by consistent habit — the median deck's median heading is **3 words**. The
written rule behind it: titles carry the **decision**, not the topic ("Why Velocity dominates"),
and the justification never appears as a sentence. The stated per-slide budget is **one headline of
six words or fewer plus at most three supporting fragments.**

**The mono layer does real work.** Domain key terms are set in mono with a subtle accent underline
where each first appears, making the vocabulary *visible* — the stated purpose being to demonstrate
command of the language rather than merely referring to the topic.

---

## 4. Colour

Distinct hex values per deck run **12–49**, which overstates the palettes: most decks resolve to a
ground, an ink, a line, and 2–4 semantic accents. The stated rule is tighter than the practice:

- **"Neutral — graphite plus one accent, but NOT boring!"** Interest is required to come from
  **contrast, depth, typography, rhythm and motion — explicitly not from more colours.**
- **One accent, used with enough discipline that it carries meaning wherever it appears.**
- **Semantic role colours held across a whole deck** — one deck fixes AI = blue · Human = amber ·
  Code = green and never varies it.
- **Calm colours; functional but attractive.**
- **Gradients only when functional** (depth, progress), never as generic decoration.
- One palette per deck, chosen to fit that deck's story — the style guide instructs a reader to
  copy its principles and *not* its palette.

Dark mode appears in only **1/12**, but the style guide treats theme-inversion bugs as a known
defect class, which implies it is wanted more often than it is delivered.

---

## 5. Diagrams, icons and illustration

| | Measured |
| :--- | :--- |
| Inline SVG per deck | **0–23**, median **6.5**; only one deck has none |
| `<img>` | Effectively absent — one deck pulls placeholder photos from a stock host |
| `<canvas>` | 3/12 |
| WebGL | 0/12 |

The division of labour is stated flatly and is the most transferable rule in the corpus:

> **Complex objects — servers, people, systems — come from an icon set. Never draw icons.
> Particles, connectors and custom diagrams are drawn freely in SVG or canvas.**

The icon set is Font Awesome. In the self-contained deck it is **embedded as its official SVG
symbols**, which the owner explicitly ruled *is* using the icon set rather than hand-drawing —
resolving the offline conflict without weakening the rule.

Two hard-won lessons carry directly into T-016: **canvas particle effects read as artificial and
confuse the audience** unless extremely restrained — a static illustration with animated dashed
connectors usually communicates the same thing more clearly; and an accumulation effect **must
actually accumulate**, not fall through and leave an empty container.

---

## 6. Interaction and motion — the signature layer

Detected across the 12 decks:

| Signal | Decks | Signal | Decks |
| :--- | :---: | :--- | :---: |
| CSS grid | 12/12 | flip / `rotateY` / backface | 4/12 |
| flexbox | 12/12 | tooltip | 3/12 |
| CSS transition | 11/12 | `<canvas>` | 3/12 |
| CSS animation / keyframes | 10/12 | `<details>` / `<summary>` | 2/12 |
| Keyboard navigation | 9/12 | accordion / collapse | 2/12 |
| ARIA attributes | 8/12 | 3D transform / perspective | 2/12 |
| `clamp()` | 6/12 | dark mode, tabs, modal, scroll-snap | 1/12 each |
| `prefers-reduced-motion` | 5/12 | **`@media print`** | **1/12** |

**Print appears in one deck of twelve.** That independently confirms the owner's instruction that
printing overrides nothing — it was never part of the practice.

The stated rules for this layer are unusually specific, and they are the ones the plugin should
carry verbatim:

- **Visuals over text; push longer text behind interaction** — click-to-reveal or hover popover.
- **When detail is unavoidable: hide it behind an interactive element revealed with smooth
  animation, or split it to a new page.** Those are the only two permitted answers.
- **For hidden elements: opening, turning, scaling.** For flows: **dashed arrows, slowly animated.**
- **Popovers drop below the element, never above** — above reads awkwardly against the pointer.
- **Motion only where it clarifies meaning.** Ease-in-out, subtle. **No continuous ambient
  glow/pulse/drift on static content** — it reads as noise, not signal.
- **Soft shadows, transparency and shaders are allowed. "No overdose."**
- **Real navigation chrome:** prev/next arrows, clickable carousel dots, keyboard
  (←/→/space/Home/End), progress bar, slide counter.
- **Pages sit in a container that gives each page a boundary, resolution and screen-size
  independent.**
- **No speaker notes, no presenter markers, no script.** Deck only — decided explicitly.

---

## 7. Where the stated conventions and the decks disagree

| Stated | Actual | Reading |
| :--- | :--- | :--- |
| Ship self-contained | 9/12 carry external refs (fonts, CDN icons, one stock-photo host) | The rule is recent and won an argument; the older decks predate it |
| 8 slides, 10 ceiling | Median 10, two decks at 15 and 18 | Holds for executive decks; analytical briefs overrun it |
| Always respect `prefers-reduced-motion` | 5/12 | Stated as absolute, delivered half the time |
| Never draw icons | Honoured — no counter-example found | Genuinely dominant |
| Real navigation chrome | Keyboard nav in 9/12 | Dominant, not universal |

The pattern: **the written conventions run ahead of the artefacts.** They are the owner's
considered position, refined over 7–8 feedback rounds on one deck and then deliberately carried
forward to the next. Where the two conflict, the stated rule is the better source for the plugin —
with the caveat in the open question below.

---

## 8. Verification practice

The corpus is unusually strong here and the method transfers wholesale:

- **Structural checks say nothing about layout — always render.** Tag balance, JS syntax checks and
  grep consistency checks all passed on slides that were visibly broken: a chart 558 px tall that
  pushed its own title off screen, an SVG label clipped by its viewBox, a connector arrow stopping
  47 px short of its target.
- **Deck-wide overflow measurement**: in a headless browser, measure each slide's content height
  against available height and print a table. Run at **two viewport sizes** — a slide can fit at
  1440×900 and overflow at 1280×800. Cheaper than eyeballing, and it catches the failure that
  matters most on a projector.
- **A slide's height is usually driven by an SVG's aspect ratio, not its text.** Trimming copy to
  fix an overflow often changes nothing.
- Serving over `http://127.0.0.1` gives full DOM access for measurement — **but it confirms
  geometry you already suspect; it cannot find a defect you have not thought to measure.**

Two portability findings for T-017, already paid for:

- **A single-file deck needs `<meta charset="utf-8">`.** Opened as a local file there is no HTTP
  header to supply the encoding; a deck full of `—`, `·`, `€`, `×` survived only on Chrome's
  auto-detection.
- The `file://` console warning about unique security origins is **benign**.

---

## 9. Cross-document reconciliation

Before one deck was written, its source deliverables were swept for disagreement and sorted into
**confirmed consistent** (with where each was checked), **cosmetic standardisations** (same meaning,
different rendering — an em-dash in published documents against a hyphen in notes), and **honest
verdicts** grading each claim *solved / substantially / partial / deferred by choice*.

The stated position is worth carrying into critique mode verbatim: **being explicit about the two
that are partial or deferred is stronger than implying everything is solved.**

---

## 10. The Foundation Spec — a template the corpus already uses

Two foundation specs, written for unrelated projects, share the **same nine sections**. This is the
single most reusable structure found, and it is what the plugin should generate before it writes any
HTML:

**1** narrative spine · **2** linguistic style · **3** visual system (atmosphere, palette,
typography, iconography) · **4** recurring elements · **5** motion and transitions · **6**
interaction model · **7** page/layout structures · **8** technical stack · **9** quality-bar
checklist.

Both state explicitly that **no per-slide content belongs here** — that is the next document. The
pipeline is therefore: requirements → foundation spec → slide-by-slide spec → review of the spec →
build → review of the build → owner review → fix. Two of those reviews happen **before any HTML
exists**.

A third document adds the layer above: a **governing idea in one line**, written before anything
else. *"Graphite is the paper. Amber is the current."* One accent meaning one thing, stated as a
sentence a reader could act on. The rationale is worth quoting: **"A deck with six colours is
decorated. A deck with one accent used with total discipline is designed."**

### Layout archetypes — the gap in §5 is closed

Both specs name and reuse a small set of slide skeletons:

| Foundation spec A | Foundation spec B |
| :--- | :--- |
| Statement — act opener, huge line, breathing room | L1 Hero — wordmark, one-line value statement |
| Instrument — a model/diagram centred and interactive | L4 Process / flow — 3–4 steps with connectors |
| Ledger — two-column pros/cons, colour-coded | L3 Split compare — pro/con columns |
| Case File — artifact plus a reveal stamp | L2 Stat focus — one giant number, short interpretation |
| Data — interactive chart, count-up stat, one callout | L5 Chart focus — one chart centre-stage |
| Loop — recurring method motif, also chapter marker | L6 Timeline — horizontal steps with a gate |
| Verdict — synthesis, clean and decisive | — |

---

## 11. Motion — a named vocabulary, not a set of effects

The most developed spec defines **exactly four motions and nothing else**, with the stated reason:
**"A named vocabulary is what stops animation becoming decoration."**

| Name | Where | Spec |
| :--- | :--- | :--- |
| **Rise** | Slide entry | opacity 0→1 + translateY 14px→0, **340 ms**, `cubic-bezier(.22,1,.36,1)`, children staggered **60 ms** |
| **Current** | Flow arrows | `stroke-dasharray: 7 6`, dashoffset 0→−130 over **4.5 s linear infinite** |
| **Open / Turn / Scale** | Reveals | Open `grid-template-rows 0fr→1fr` **380 ms** · Turn `rotateY(−90deg→0)` `preserve-3d` **420 ms** · Scale `.94→1` + fade **300 ms** |
| **Pulse-once** | Accent emphasis on first reveal | single 1.2 s ring, **never looping** |

Reduced motion collapses all four to instant states — but **the dashed arrows stay dashed, so the
meaning survives when the animation does not.** That is the pattern to copy: degrade the motion,
keep the semantics.

Corroborating numbers elsewhere: inter-slide transitions **400–500 ms ease-in-out**, staged reveals
as fade plus an 8–12 px rise, and an explicit owner instruction of **"animations max 500 ms, ease in
and out"**. Two specs independently forbid **3D spins and flashy zooms**.

---

## 12. The fixed stage — resolution independence

The strongest deck does not use `100dvh` flex slides. It uses a **fixed 1600×900 stage scaled to the
viewport with `transform: scale()`**, centred, with a soft elevation shadow and a 1px edge.

| `100dvh` flex slides | Fixed scaled stage |
| :--- | :--- |
| Content reflows per viewport | **Nothing ever reflows** |
| Looks different on every machine | Pixel-identical everywhere |
| Fine for a deck you scroll yourself | Correct for a deck presented once, on an unknown projector |

**What the presenter rehearses is exactly what appears.** This also supplies the "great boundary"
per page that the requirements ask for, and it eliminates the overflow-at-1280×800 failure that §8's
two-viewport check exists to catch.

### Standing page furniture

Provenance upper-right (mono, 11px) · assumption marker on the right edge, silent until wanted ·
slide number lower-right · nav bar lower-centre with dots, an accent pill for the current slide,
chevrons and full keyboard support · and **a spine ribbon lower-left showing the deck's argument
with the current stage lit** — described as *"the single most valuable piece of furniture in the
deck… the examiner never loses the thread."*

---

## 13. Writing style — a complete standard already exists

A dedicated writing style guide states five rules, with target lengths that are directly testable:

1. **Shorter, without losing content.** Cut words, not findings. A shorter version that drops a
   figure, a row or a conclusion has failed.
   **Targets:** section under one screen · paragraph 3–4 sentences · **sentence under 20 words** ·
   table cell one line.
2. **Explain the result, not the road to it.** Leave out how the option was chosen and why the
   alternative was dropped. Reasoning a reader needs in order to *trust* the result stays.
3. **Statement first, then description, then challenge** — a fixed order. **Never open with a
   question, a build-up, or a clause that delays the point.**
4. **Plain, simple English.** One dash per paragraph at most · active voice · **bold the fact, not
   the emphasis** — if three things in a paragraph are bold, none stands out · no rhetorical
   questions · delete "which is precisely why", "worth saying out loud", genuinely/actually/
   arguably/precisely.
5. **Keep the domain's own terms** — give the term, one line of plain meaning at first use, list it.

**The reader standard, stated:** *"The reader is bright and new to the field. Anything the owner
would have to look up is a defect."*

### The banned-terminology gap is closed

The corpus's one-example note ("friction, etc") is backed by a full five-category list:

| Category | Examples |
| :--- | :--- |
| Empty phrases | "I hope this message finds you well" · "Going forward" · "Not made lightly" |
| Inflated adjectives | crucial · pivotal · seamless · leverage · synergy · **friction** |
| Structural tells | exactly three points · same-length paragraphs · bold-label bullets |
| Syntactic patterns | "Not only… but also" · "serves as" · "it was determined that" |
| Voice absence | "Certainly!" · "Great question!" |

**And the caveat that matters more than the list:** *"A text can avoid all five patterns and still
sound like AI — when it has no personality."* Voice comes from having a position, varying rhythm,
allowing ambivalence, first person where it fits, and tolerating small imperfections. A word-list
check is necessary and not sufficient — which constrains how much T-005 can claim.

---

## 14. Critique — two formats already proven

**Specification review** (before any HTML exists): each slide read against the rubric, against the
sources, against the requirements, **and against the other slides for consistency**. Standard
applied: *"a finding is anything a grader, a presenter under pressure, or a careful reader would
trip on."* Output is `ID · Severity · Slide · Finding · Fix` with **Major / Minor / Note**, then
fixes applied **one at a time** showing *was* and *now*, then an **"Open — needs a decision"**
section, then counts.

**Design audit** (after a build): headline verdict first, then a coverage table proving nothing
required is missing, then findings as `Finding · Severity H/M/L · Principle violated`, then an
explicit **keep vs rebuild** split.

The defect classes these found generalise completely: an **invented number** in a title supported by
no source · a **narrative conceit that silently breaks** at step two · a **wrong metric on the title
slide** · **missing content rather than error** — half a stated goal absent, four items counted but
never named · **a stated requirement silently unmet** rather than raised as a deviation · **two
interactions with undefined precedence**, live failure under presentation pressure · a bar rendering
at 1.4 px that reads as a rendering fault · **two numbering schemes with no mapping** · **no timing
budget** for a timed presentation.

The closing observation is the one to carry: *"The four Major findings were all substance, not
polish. Two of them were missing content rather than errors, which is the failure mode a self-review
most easily misses."*

**The rejected visual pattern, named at severity H:** *"Boxes everywhere — card grids, stat strips,
pill rows, tables, bulleted lists."* And *"A→B→C→D is four boxes joined by arrow glyphs; the process
forks, but this is never drawn."* The principle: **diagrams instead of boxes; branch where the
process branches.**

**The most repeated defect in the entire corpus** is z-order on hover popovers — raised in three
separate feedback rounds, alongside a hard-coded `fill="#ffffff"` that stays white in dark mode.
Both are cheap to check and were missed by every review that was not a rendered one.

---

## 15. Working method, in the owner's own words

These recur across feedback documents and are stated as instructions, not preferences:

- **"My thoughts might be messy and contradictory. Please ask, argue, do not accept and guess
  blindly."**
- "In case of inconsistency, missing information, contradiction, or just for a better result, ask
  your questions."
- **"Do not start if any of the referenced document is missing."**
- "Keep the style guides as long as it supports the message, but **be brave to implement a different
  visual and structural idea if it better communicates the content.**"
- **"Do not implement it in a single step. Think thoroughly, iterate."** Fix findings one by one.

---

## Open question for the owner

**Where a written rule and the decks disagree, which wins?** §7 shows the specs consistently run
ahead of the artefacts — they read as the owner's refined intent, and the older decks as work that
predates them. R1 assumes **stated beats actual**, and flags the one case where that assumption is
load-bearing: `prefers-reduced-motion` is stated as absolute and delivered in 5/12. If the stated
rules win, the plugin enforces it always.
