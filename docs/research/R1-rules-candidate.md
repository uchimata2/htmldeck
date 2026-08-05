# R1 — Candidate rules and gaps register

The corpus reduced to rules that can be kept, dropped or amended. Deliverable of
[T-009](../../tasks/T-009-analyse-the-corpus-extract-my-deck-conventions.md); evidence is in
[R1-corpus-conventions.md](R1-corpus-conventions.md).

**These are candidates, not decisions.** Choosing what survives is [T-014](../../tasks/T-014-synthesise-research-into-the-design-system-reference.md),
after the external research lands. Nothing here is settled.

> ### ⚠ Provenance is unresolved, and it is load-bearing
>
> An unknown share of the rules below labelled `stated` are **quoted from a general-purpose deck
> skill** that the corpus decks were built with, not authored by the owner. The specs cite it as an
> authority — *"the skill names those as generic tells"*, *"the skill explicitly forbids continuous
> glow"*, *"a deliberate departure from the skill's default"* — and one requirements document says
> plainly **"use the Visual Explainer skill"**.
>
> This project exists to encode **the owner's** taste. Building in rules that belong to an existing
> skill re-derives something that already ships, which is the failure the owner explicitly asked to
> avoid. Every rule therefore needs a provenance verdict before T-014 can act on it:
> **owner-authored · inherited from the skill · owner's deliberate departure from the skill.**
>
> **The departures are the highest-value rows in this file.** L1 (fixed scaled stage), J1–J2
> (self-containment), D3 (embedded faces), F11 (the four-motion vocabulary) and G11 (the spine
> ribbon) are all positions argued *against* a default — which is exactly where taste is visible.
> Scoped to [T-012](../../tasks/T-012-research-existing-html-deck-skills-and-libraries.md).

**Frequency** — `dominant` most decks or stated and unopposed · `variant` some decks · `one-off`
a single instance · `stated` written down but under-delivered.

**Verdict column** is left blank on purpose. T-014 fills it: keep · drop · amend · defer.

---

## A. Structure

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| A1 | `<section>` per slide | dominant | |
| A2 | Target 8 slides, hard ceiling 10; past 8 needs a stated reason | stated | |
| A3 | Never fewer than 6 | dominant | |
| A4 | Specify slide-by-slide before building — structure, text, visuals, animations, interactions, title, bottom line | stated | |
| A5 | Build the specification page by page, explicitly not in one pass | stated | |
| A6 | Review the *specification* slide-by-slide before any HTML exists | stated | |
| A7 | Build slides in batches so feedback lands mid-build | stated | |
| A8 | Pages sit in a container giving each a boundary, resolution-independent | stated | |
| A9 | One strong closing line plus one subtle supporting line — nothing else | stated | |
| A10 | No speaker notes, presenter markers or script. Deck only | stated | |

## A′. Process — the document pipeline

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| A′1 | Write a **governing idea** in one line before anything else — one accent meaning one thing | one-off | |
| A′2 | Write a **Foundation Spec** in nine fixed sections: narrative spine · linguistic style · visual system · recurring elements · motion · interaction model · layout structures · technical stack · quality-bar checklist | dominant | |
| A′3 | No per-slide content in the foundation spec — that is the next document | stated | |
| A′4 | Review the specification **before any HTML exists**, slide-by-slide, against sources, requirements, and the other slides | stated | |
| A′5 | Build, then review the build, then owner review, then fix | stated | |
| A′6 | A rubric/requirement trace table proving nothing required is missing | variant | |
| A′7 | Per-slide **timing budget** for a timed presentation, with the handover point named | one-off | |
| A′8 | **Do not start if a referenced document is missing** | stated | |
| A′9 | **Ask, argue, do not guess** — the owner's notes may be contradictory by his own account | stated | |
| A′10 | Never implement in one step; fix findings one by one | stated | |
| A′11 | Keep the style guide only as long as it serves the message — **be brave to depart when a different idea communicates better** | stated | |

## B. Writing style and content

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| B1 | Keep text short; the message must still land hard | stated | |
| B2 | **Never justify a statement with sentences** — diagrams, lists, tables and structure carry the detail | stated | |
| B3 | Titles carry the decision, not the topic | stated | |
| B4 | Headings short — corpus median 3 words, ceiling ~16 | dominant | |
| B5 | Professional business language, voiced as an enthusiastic business person | stated | |
| B6 | Respectful, positive, professional | stated | |
| B7 | Avoid AI-favoured terminology (the corpus names "friction"; a fuller list must be built) | stated | |
| B8 | Embed the domain's key terms naturally throughout — demonstrate the language, don't refer to it | stated | |
| B9 | Mark assumptions subtly at the side; never as noise | stated | |
| B10 | Provenance label in the upper-right corner — plain text, never a link | stated | |
| B11 | Grade honestly: solved / substantially / partial / deferred. Being explicit beats implying everything is solved | stated | |
| B12 | Visuals aid comprehension for non-expert audiences | stated | |
| B13 | **Sentence under 20 words**; paragraph 3–4 sentences; table cell one line | stated | |
| B14 | Per-slide budget: one headline ≤6 words plus ≤3 supporting fragments | stated | |
| B15 | **Statement → description → challenge**, fixed order. Never open with a question or a build-up | stated | |
| B16 | Explain the result, not the road to it | stated | |
| B17 | Cut words, never findings — dropping a figure or a row is a failed edit | stated | |
| B18 | One dash per paragraph at most; active voice; no rhetorical questions | stated | |
| B19 | **Bold the fact, not the emphasis** — three bold things means none stands out | stated | |
| B20 | Delete "which is precisely why", "worth saying out loud", genuinely/actually/arguably/precisely | stated | |
| B21 | **The reader is bright and new to the field. Anything the owner would have to look up is a defect** | stated | |
| B22 | Ban the five AI-tell categories: empty phrases · inflated adjectives (crucial, pivotal, seamless, leverage, synergy, friction) · structural tells · syntactic patterns · voice absence | stated | |
| B23 | **A word-list check is not sufficient** — text can pass all five and still read as AI when it has no voice. Voice = a position, varied rhythm, ambivalence, first person where it fits, tolerated imperfection | stated | |
| B24 | Explain by example, not definition — show the model doing work on a real number | variant | |
| B25 | Honesty markers visible: `[est.]` preserved, every figure sourced, **no fabricated metrics** | variant | |

## C. Colour

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| C1 | Neutral ground plus **one** accent — "but NOT boring" | stated | |
| C2 | Interest comes from contrast, depth, typography, rhythm and motion — **not** from more colours | stated | |
| C3 | The accent carries meaning wherever it appears | stated | |
| C4 | Semantic role colours fixed for a whole deck | variant | |
| C5 | Calm colours; functional but attractive | stated | |
| C6 | Gradients only when functional (depth, progress), never decoration | stated | |
| C7 | One palette per deck, fitted to that deck's story | dominant | |
| C8 | Both themes readable — no component that inverts into white-on-light | stated | |
| C9 | **Never pure white, never pure black** — warm paper ground, graphite or warm-charcoal ink | dominant | |
| C10 | **Light, not dark**, by default: lit rooms lose dark-deck contrast under a projector; management reads paper-white as considered; dark/violet dashboard is the generic cliché | stated | |
| C11 | Dark stays one block of custom-property overrides away, never a redesign | stated | |
| C12 | No full-page gradients, no gradient-blob backgrounds, no cyber/neon aesthetic | stated | |
| C13 | Semantic pro/con coding fixed deck-wide with a visible legend — green positive · red negative · amber caution | dominant | |
| C14 | The accent must survive a bad projector — muted, not neon, not a framework default | stated | |

## D. Typography

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| D1 | Deliberate pairing per deck: characterful display + one superfamily for body and label | dominant | |
| D2 | **Never Inter, Roboto, Arial or system-ui** — named as generic tells; a system-font body is a severity-H audit failure. *(Inter is the most frequent face in the older decks; the refined specs reject it. Do not read frequency as intent.)* | stated | |
| D3 | Embed faces as base64 `@font-face` — demonstrated at 7 faces in one deck | one-off | |
| D4 | `clamp()` for fluid type — display `clamp(34px, 4.2vw, 56px)` | variant | |
| D5 | Body 18–24px, line-height 1.55; mono labels 11–13px uppercase, letter-spacing 1.4px | one-off | |
| D6 | `text-wrap: balance` and negative letter-spacing on display headings | one-off | |
| D7 | **The mono layer carries the domain vocabulary** — key terms set in mono with an accent underline at first use | stated | |

## E. Diagrams, icons, illustration

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| E1 | **Never hand-draw icons.** Complex objects come from an icon set | stated | |
| E2 | Draw particles, connectors and custom diagrams freely in SVG or canvas | stated | |
| E3 | Embed the icon set as its official SVG symbols — that is *using* the set, not drawing | stated | |
| E4 | Diagrams as inline SVG; authoring source may keep them as separate files | dominant | |
| E5 | No raster images | dominant | |
| E6 | Canvas particle/emission effects read as artificial — use only when extremely restrained | stated | |
| E7 | An accumulation effect must actually accumulate, not fall through | stated | |
| E8 | Give `<canvas>` fixed pixel dimensions via HTML attributes; let CSS scale it | stated | |
| E9 | **"Boxes everywhere" is the rejected pattern** — card grids, stat strips, pill rows, tables and bulleted lists instead of diagrams is a severity-H failure | stated | |
| E10 | **Branch where the process branches.** Four boxes joined by arrow glyphs is not a flow diagram | stated | |
| E11 | Connector lines must have arrowheads and must actually meet their target | stated | |
| E12 | Icon set: **Lucide primary, Font Awesome free fallback** | dominant | |
| E13 | Embed the icon set as an **SVG symbol sprite containing only the icons used**, referenced by `<use>` | one-off | |
| E14 | **One icon per concept, used consistently** — a repeated icon is a repeated idea | stated | |
| E15 | Every SVG and chart is **theme-aware** — a hard-coded `fill="#ffffff"` stays white in dark mode | stated | |
| E16 | Vary chart types deliberately across a deck | stated | |

## F. Interaction and motion

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| F1 | Push longer text behind interaction rather than onto the slide | stated | |
| F2 | When detail is unavoidable there are exactly two answers: hide behind interaction with smooth animation, or split to a new page | stated | |
| F3 | Hidden elements reveal by **opening, turning, scaling** | stated | |
| F4 | Flows use dashed arrows, slowly animated | stated | |
| F5 | Popovers drop **below** the element, never above | stated | |
| F6 | Motion only where it clarifies meaning; ease-in-out, subtle | stated | |
| F7 | **No continuous ambient glow/pulse/drift on static content** | stated | |
| F8 | Soft shadows, transparency, shaders allowed — "no overdose" | stated | |
| F9 | Always respect `prefers-reduced-motion` | stated (5/12) | |
| F10 | Entrance animations with `fill-mode: forwards` keep their stacking context — raise the hovered holder, not the popover | stated | |
| F11 | **A named motion vocabulary of exactly four**: Rise (entry, 340 ms, `cubic-bezier(.22,1,.36,1)`, 60 ms stagger) · Current (flow, dasharray 7 6, 4.5 s linear infinite) · Open/Turn/Scale (reveals, 380/420/300 ms) · Pulse-once (1.2 s, never looping) | one-off | |
| F12 | **Animations max 500 ms**, ease-in-out; inter-slide transition 400–500 ms | stated | |
| F13 | Reduced motion degrades the motion but **keeps the semantics** — the dashed arrows stay dashed | stated | |
| F14 | **No 3D spins, no flashy zooms, no punchy cuts** — stated independently in two specs | stated | |
| F15 | Charts draw in once; never re-animate on back-navigation | stated | |
| F16 | Count-up on headline statistics; one emphasis pulse on the key number per slide | variant | |
| F17 | **Interaction reveals otherwise-lost information — never decoration.** One meaningful interaction per slide where it adds signal | stated | |
| F18 | Interactions keyboard-reachable; the slide still reads if never touched | stated | |
| F19 | **Disclosure is a judgement, not a reflex** — "show the details here, do not hide them under the click" | stated | |
| F20 | Interaction patterns built once as components and reused, so the UX is learnable | stated | |
| F21 | Two simultaneous interactions need a defined **precedence rule** — undefined is a live failure under presentation pressure | stated | |
| F22 | When a diagram changes mode, animate nodes to their new size and position | stated | |

## G. UI controls and navigation

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| G1 | Prev/next arrows | stated | |
| G2 | Clickable carousel dots | stated | |
| G3 | Keyboard: ←/→/space/Home/End | dominant | |
| G4 | Progress bar | stated | |
| G5 | Slide counter / page numbers | stated | |
| G6 | **Mouse-wheel navigation between slides** | stated | |
| G7 | Click-to-jump from the dots; touch/swipe | stated | |
| G8 | The page title and the nav-bar name for that page **must match** | stated | |
| G9 | Provenance mark upper-right. *Plain text on one deck, a working link on another — the owner praised the link. Per-deck decision.* | variant | |
| G10 | Assumption marker on the right edge, silent until wanted | one-off | |
| G11 | **A spine ribbon showing the deck's argument with the current stage lit** — "the audience never loses the thread" | one-off | |
| G12 | Appendix pages named "Appendix", and the back link names where it goes | stated | |

## L. Stage and layout archetypes

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| L1 | **Fixed 1600×900 stage scaled with `transform: scale()`** — nothing reflows, pixel-identical on any projector, and what was rehearsed is what appears | one-off | |
| L2 | The stage floats on a darker field with a soft shadow and hairline edge, giving each page its boundary | one-off | |
| L3 | A named, reused set of slide archetypes — Hero/Statement · Stat focus · Split compare (ledger) · Process/flow · Chart focus · Timeline · Case file · Loop/chapter marker · Verdict | dominant | |
| L4 | One dominant accent per slide for rhythm | stated | |
| L5 | Consistent margins, one grid, left-aligned headlines, breathing room | stated | |
| L6 | Card style consistent: 12–16px radius, soft shadow, thin hairline, no heavy borders | variant | |

## H. Layout

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| H1 | CSS grid and flexbox throughout | dominant | |
| H2 | **Align by construction, not coordinates** — correlated rows share a grid track | stated | |
| H3 | Boxes that read as a set must be siblings in one container | stated | |
| H4 | No duplicate emphasis — one marker per point | stated | |
| H5 | No box nested in a box with its own text | stated | |
| H6 | Reset **every** heading level, `h4` and `h5` included — a partial reset is worse than none | stated | |
| H7 | Never style a bare `<b>` inside a component | stated | |

## I. Theming

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| I1 | Theme driven entirely by CSS custom properties | dominant | |
| I2 | Token vocabulary already stable: `--ink` 11/12, `--bg` 9/12, `--line` 8/12, `--shadow` 7/12, plus semantic colour roles | dominant | |

## J. Portability

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| J1 | Ship one self-contained file for presenting; authoring source may be multi-file | stated | |
| J2 | **Quality is never traded for self-containment** — "maximize the quality at all cost, even in multiple files" | stated | |
| J3 | `<meta charset="utf-8">` is mandatory — a local file has no HTTP header to supply it | stated | |
| J4 | The `file://` unique-security-origin console warning is benign | stated | |

## K. Verification

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| K1 | **Structural checks say nothing about layout — always render and look** | stated | |
| K2 | Measure every slide's content height against available height; print a table | stated | |
| K3 | Run that at two viewport sizes — 1440×900 and 1280×800 | stated | |
| K4 | Suspect the SVG's aspect ratio before the text when a slide overflows | stated | |
| K5 | DOM measurement confirms geometry you suspect; it cannot find a defect you have not thought to measure | stated | |
| K6 | Re-verify grid alignment after any collapse/expand interaction | stated | |
| K7 | Sweep source documents for cross-document disagreement before writing the deck | stated | |

## M. Critique

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| M1 | **The standard:** a finding is anything a grader, a presenter under pressure, or a careful reader would trip on | stated | |
| M2 | Findings table: `ID · Severity · Slide · Finding · Fix`, severities **Major / Minor / Note** (spec review) or **H / M / L + principle violated** (design audit) | dominant | |
| M3 | **Headline verdict first**, before any per-slide detail | stated | |
| M4 | Read each slide against the requirements, against the sources, **and against the other slides for consistency** | stated | |
| M5 | Fixes applied **one at a time, in order**, each recording *was* and *now* | stated | |
| M6 | An **"Open — needs a decision"** section for anything the reviewer must not settle alone | stated | |
| M7 | A stated requirement going unmet must be **an agreed deviation, not a silent omission** | stated | |
| M8 | Close with counts and an explicit **keep vs rebuild** split | stated | |
| M9 | **Watch for missing content, not just errors** — "the failure mode a self-review most easily misses" | stated | |
| M10 | Named defect classes to hunt: invented numbers · a narrative conceit that breaks mid-deck · a wrong metric on the title slide · undefined interaction precedence · an element rendering so small it reads as a fault · two numbering schemes with no mapping · no timing budget | stated | |
| M11 | Reviewing only the local files once caused a whole business case to be missed — **read the authoritative source, not the convenient one** | stated | |

---

## Gaps register — where the corpus is silent

The handoff to [T-010](../../tasks/T-010-research-external-deck-design-and-ux-principles.md) and
[T-011](../../tasks/T-011-research-exemplary-decks-and-why-they-work.md). Silence is a finding: on
these, the plugin has no inherited taste to encode and must import or invent one.

Revised after the second sweep. **Five of the original twelve are now closed from the corpus
itself** — they were not silences, they were documents I had not yet read.

| # | Gap | Status | Who fills it |
| :--- | :--- | :--- | :--- |
| G-2 | Slide archetype vocabulary | **Closed** — two specs name and reuse archetype sets (rule L3) | — |
| G-4 | Type scale | **Closed** — display `clamp(34px,4.2vw,56px)`, body 18–24px/1.55, mono 11–13px (D4–D6) | — |
| G-8 | Banned-terminology list | **Closed** — five AI-tell categories with examples, plus the caveat that a word list is insufficient (B22–B23) | — |
| G-10 | Motion token vocabulary | **Closed** — four named motions with exact durations and easings (F11) | — |
| G-12 | Content-length rule | **Closed** — sentence <20 words, headline ≤6 words, ≤3 fragments per slide (B13–B14) | — |
| G-3 | **Narrative framework.** Partly closed: a spine question, a through-line, an emotional arc and named rhetorical beats exist — but no general framework (pyramid, SCR, assertion-evidence) is stated | Partial | T-010 |
| G-1 | **No accessibility floor.** ARIA in 8/12 and "keyboard-reachable" is stated, but no contrast ratio, focus-visible rule, tab order or screen-reader position appears anywhere | Open | T-010 |
| G-5 | **No spacing system.** Grid-based layout, card radii and hairlines are specified, but no spacing scale — which is exactly why "inconsistent spacing with no spacing rule to blame" was a real defect | Open | T-010 |
| G-6 | **Dark mode is 1/12** yet theme-inversion is a known bug class and the strongest spec says dark is "one block of overrides". Wanted more than delivered; no rule states when it applies | Open | owner |
| G-7 | **No chart conventions.** No axis, label, legend or data-ink guidance. Chart.js is used but never configured to a standard | Open | T-010 → T-006 |
| G-9 | **3D is unexplored, and the corpus argues against it.** 3D transforms in 2/12, WebGL in 0/12, and two specs explicitly forbid 3D spins. The owner now wants 3D | Open | T-011, T-016, T-017 |
| G-11 | **No mobile position.** Nothing addresses small screens — and the fixed-stage technique (L1) has direct consequences here | Open | owner |
| G-13 | **No file-size ceiling.** The one self-contained deck is 282 KB with 7 embedded faces; nothing says what is too big | Open | owner → T-013 |
| G-14 | **Deck-length rule is genuinely contradictory**, not absent — see X-5 | Open | owner |

---

## Contradictions to resolve at T-014

| # | Tension | Between |
| :--- | :--- | :--- |
| X-1 | Use CDN libraries for eye-candy **vs** ship self-contained | E-rules / J1 — resolved once by embedding icons as SVG symbols; does it generalise to a 3D library? |
| X-2 | Never hand-draw icons **vs** no external references | E1 / J1 — same resolution, worth stating as a general principle |
| X-3 | "No overdose", "no ambient motion" **vs** the owner's new brief for rich 2D/3D animation | F7 / F8 vs the 2026-08-06 decisions. **The sharpest conflict in the set** |
| X-4 | Canvas effects read as artificial **vs** 3D effects now wanted | E6 vs the 2026-08-06 decisions |
| X-5 | **"Aim 8, max 10"** vs **"do not exceed 18"** vs **"completeness overwrites the size limitations"** — three different rulings, three different decks, all the owner's own | A2 — deck length is a **per-deck decision, not a house rule**. But "single clean messages per slide is more important than concision" holds across all three, and progressive disclosure is the stated reconciler: *"nothing is dropped; it is folded"* |
| X-6 | Stated rules run ahead of the artefacts | §7 of R1 — general policy needed, not case-by-case |
| X-7 | **Provenance: "plain label, no link, no dead links on an unfamiliar machine"** vs **"the upper right corner link made my day, it's so useful"** | Two decks, opposite rulings, both the owner's. Depends on whether the sources are reachable where the deck is presented |
| X-8 | **"No 3D spins, no flashy zooms"** and **"Turn: `rotateY` with `preserve-3d`"** | Not actually a conflict — 3D *transition* between slides is forbidden, 3D *reveal* of a card is prescribed. Worth stating precisely so the plugin does not read the ban too widely |
| X-9 | **Icons via CDN** (Lucide, Font Awesome) vs **self-containment** | Resolved once by embedding an SVG symbol sprite of only the icons used. Does that generalise to Lucide? |
| X-10 | **A word-list check for AI tells** vs **"text can pass all five and still sound like AI"** | B22 vs B23. Constrains what T-005 may claim: the check is necessary, not sufficient, and must say so |
| X-11 | **`100dvh` flex slides** (the general convention) vs **fixed 1600×900 scaled stage** (the strongest deck) | L1 — a real fork with consequences for mobile (G-11) and for how overflow is checked (K2–K3) |
