# R1 — Candidate rules and gaps register

The corpus reduced to rules that can be kept, dropped or amended. Deliverable of
[T-009](../../tasks/T-009-analyse-the-corpus-extract-my-deck-conventions.md); evidence is in
[R1-corpus-conventions.md](R1-corpus-conventions.md).

**These are candidates, not decisions.** Choosing what survives is [T-014](../../tasks/T-014-synthesise-research-into-the-design-system-reference.md),
after the external research lands. Nothing here is settled.

> ### ✔ Provenance resolved — see [R4](R4-prior-art.md)
>
> The concern this box used to raise was real: an unknown share of the rules below were **quoted
> from a general-purpose deck skill** the corpus decks were built with, not authored by the owner.
> [T-012](../../tasks/T-012-research-existing-html-deck-skills-and-libraries.md) read that skill
> from source and assigned every rule a verdict. **[R4 §9](R4-prior-art.md#9-per-rule-provenance-table)
> is the single home for those verdicts** — they are deliberately not duplicated here, because the
> Verdict column below belongs to T-014.
>
> **The result: 86 owner-authored · 42 inherited · 22 departures · 4 owned by the owner's own
> `humanize-writing` skill.** Two corrections matter when reading the tables below:
>
> - **G11 (the spine ribbon) is not a departure — it is owner-authored.** The skill has position
>   indicators, nothing that carries the argument. **F11 (the four-motion vocabulary) is only half
>   a departure**: the skill's "Choreography" section already names four motions by element role
>   with stagger, so the shape is inherited and only the content is the owner's.
> - **Seventeen departures were never flagged**, including the two sharpest: the skill *prescribes*
>   the card-grid and step-card-pipeline layout that E9/E10 class as a severity-H failure, and it
>   instructs the opposite of A2 — add slides rather than drop content, 18–25 from a 7-section
>   source.
>
> Three inherited clusters are worth knowing before assigning any keep/drop verdict: **navigation
> (G1–G7 is the skill's slide engine entire)**, **typography (D1–D6)**, and **colour discipline (C)**.

**Frequency** — `dominant` most decks or stated and unopposed · `variant` some decks · `one-off`
a single instance · `stated` written down but under-delivered.

**Verdict column filled 2026-08-06 by [T-014](../../tasks/T-014-synthesise-research-into-the-design-system-reference.md)** — keep · drop · amend · defer.

> ### The verdicts, counted
>
> **110 keep · 17 amend · 1 drop · 26 defer** — 154.
>
> **The single drop is C7** (one palette per deck), and it falls to a standing owner decision rather
> than to evidence. **The 26 defers are all boundary, not indecision:** 11 process rules to T-020,
> 5 check mechanics to T-005, 7 critique-format rules to T-004, and 4 pipeline rules from group A
> that belong with T-020's set. Nothing was deferred for want of an answer.
>
> **That a synthesis keeps 71% of an observed corpus is the expected result, not a soft one.** The
> tie-break only fires where an external principle is E1/E2 *and* contradicts a habit, and R2 found
> that combination in a handful of places. Most corpus rules were never in contention: no external
> principle addresses whether the mono layer carries the domain vocabulary.
>
> **Where the verdicts came from, in order of precedence** — this is the lookup, and it ran the same
> way for all 154:
>
> 1. **A standing owner decision in `BRIEF.md` § *Decisions taken* or a CLAUDE.md rule** overrides an
>    observed habit. This is a class the tie-break does not name, and it is what dropped C7 and
>    amended D1, J1 and J2.
> 2. **An E1/E2 external principle that contradicts the habit** — the owner's tie-break. It fired
>    once, on **L1**, and the result is a re-scoping proposal rather than a ruling.
> 3. **A named contradiction C-01…C-11** — resolved by its own entry below.
> 4. **Otherwise, keep.** An E3/E4 principle does not outrank a corpus habit, so it was never a
>    conflict — which is most of why the keep count is high.
>
> **Provenance was context, never a verdict.** No rule was dropped for being inherited: all seven of
> G1–G7 are the source skill's slide engine and all seven are kept. What R4's grading bought was
> knowing which rules may be cited as the owner's signature — not which to discard.

---

## A. Structure

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| A1 | `<section>` per slide | dominant | **keep** |
| A2 | Target 8 slides, hard ceiling 10; past 8 needs a stated reason | stated | **amend** — C-05 |
| A3 | Never fewer than 6 | dominant | **keep** |
| A4 | Specify slide-by-slide before building — structure, text, visuals, animations, interactions, title, bottom line | stated | **defer → T-020** |
| A5 | Build the specification page by page, explicitly not in one pass | stated | **defer → T-020** |
| A6 | Review the *specification* slide-by-slide before any HTML exists | stated | **defer → T-020** |
| A7 | Build slides in batches so feedback lands mid-build | stated | **defer → T-020** |
| A8 | Pages sit in a container giving each a boundary, resolution-independent | stated | **keep** — see L1/C-11 |
| A9 | One strong closing line plus one subtle supporting line — nothing else | stated | **keep** |
| A10 | No speaker notes, presenter markers or script. Deck only | stated | **keep** — *resolved 2026-08-21 by [T-211](../../tasks/T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md). This read **amend — BRIEF Q4** from the day it was written. The amendment is not needed: DS-088 governs the **shipped** deck, notes live in a presenter build that never ships, and the corpus's own reason — a self-contained file carries its notes to whoever receives it — is unchanged.* |

## A′. Process — the document pipeline

**The whole group defers to [T-020](../../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md)
by the boundary T-014 set during specify: the design system owns *what a good deck is*, not *how the
plugin works*.** The one exception is A′11, which is a rule about the design system itself.

Note for T-020: the sequencing decision of 2026-08-06 already narrows A′2 — under one theme, only
the narrative spine and the governing idea (A′1) are genuinely per-deck, so the nine-section spec is
a **selection sheet that cites `docs/DESIGN-SYSTEM.md`**, not nine authored sections.

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| A′1 | Write a **governing idea** in one line before anything else — one accent meaning one thing | one-off | **defer → T-020** |
| A′2 | Write a **Foundation Spec** in nine fixed sections: narrative spine · linguistic style · visual system · recurring elements · motion · interaction model · layout structures · technical stack · quality-bar checklist | dominant | **defer → T-020** |
| A′3 | No per-slide content in the foundation spec — that is the next document | stated | **defer → T-020** |
| A′4 | Review the specification **before any HTML exists**, slide-by-slide, against sources, requirements, and the other slides | stated | **defer → T-020** |
| A′5 | Build, then review the build, then owner review, then fix | stated | **defer → T-020** |
| A′6 | A rubric/requirement trace table proving nothing required is missing | variant | **defer → T-020** |
| A′7 | Per-slide **timing budget** for a timed presentation, with the handover point named | one-off | **defer → T-020** |
| A′8 | **Do not start if a referenced document is missing** | stated | **defer → T-020** |
| A′9 | **Ask, argue, do not guess** — the owner's notes may be contradictory by his own account | stated | **defer → T-020** |
| A′10 | Never implement in one step; fix findings one by one | stated | **defer → T-020** |
| A′11 | Keep the style guide only as long as it serves the message — **be brave to depart when a different idea communicates better** | stated | **keep** — as the reference's own override clause |

## B. Writing style and content

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| B1 | Keep text short; the message must still land hard | stated | **keep** |
| B2 | **Never justify a statement with sentences** — diagrams, lists, tables and structure carry the detail | stated | **keep** |
| B3 | Titles carry the decision, not the topic | stated | **amend** — upgraded to P-01: the heading must be a *claim*, and the check goes semantic |
| B4 | Headings short — corpus median 3 words, ceiling ~16 | dominant | **keep** |
| B5 | Professional business language, voiced as an enthusiastic business person | stated | **keep** |
| B6 | Respectful, positive, professional | stated | **keep** |
| B7 | Avoid AI-favoured terminology (the corpus names "friction"; a fuller list must be built) | stated | **amend** — point to `humanize-writing`, carry the list inline (R2 §3.1) |
| B8 | Embed the domain's key terms naturally throughout — demonstrate the language, don't refer to it | stated | **keep** |
| B9 | Mark assumptions subtly at the side; never as noise | stated | **keep** |
| B10 | Provenance label in the upper-right corner — plain text, never a link | stated | **amend** — C-07 |
| B11 | Grade honestly: solved / substantially / partial / deferred. Being explicit beats implying everything is solved | stated | **keep** |
| B12 | Visuals aid comprehension for non-expert audiences | stated | **keep** |
| B13 | **Sentence under 20 words**; paragraph 3–4 sentences; table cell one line | stated | **keep** |
| B14 | Per-slide budget: one headline ≤6 words plus ≤3 supporting fragments | stated | **keep** — departure, and P-01/P-02 back it |
| B15 | **Statement → description → challenge**, fixed order. Never open with a question or a build-up | stated | **keep** |
| B16 | Explain the result, not the road to it | stated | **keep** |
| B17 | Cut words, never findings — dropping a figure or a row is a failed edit | stated | **keep** |
| B18 | One dash per paragraph at most; active voice; no rhetorical questions | stated | **keep** |
| B19 | **Bold the fact, not the emphasis** — three bold things means none stands out | stated | **keep** |
| B20 | Delete "which is precisely why", "worth saying out loud", genuinely/actually/arguably/precisely | stated | **keep** |
| B21 | **The reader is bright and new to the field. Anything the owner would have to look up is a defect** | stated | **keep** |
| B22 | Ban the five AI-tell categories: empty phrases · inflated adjectives (crucial, pivotal, seamless, leverage, synergy, friction) · structural tells · syntactic patterns · voice absence | stated | **amend** — same pointer treatment as B7 |
| B23 | **A word-list check is not sufficient** — text can pass all five and still read as AI when it has no voice. Voice = a position, varied rhythm, ambivalence, first person where it fits, tolerated imperfection | stated | **keep** — and it binds T-005 (C-10) |
| B24 | Explain by example, not definition — show the model doing work on a real number | variant | **keep** |
| B25 | Honesty markers visible: `[est.]` preserved, every figure sourced, **no fabricated metrics** | variant | **keep** |

## C. Colour

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| C1 | Neutral ground plus **one** accent — "but NOT boring" | stated | **keep** |
| C2 | Interest comes from contrast, depth, typography, rhythm and motion — **not** from more colours | stated | **keep** |
| C3 | The accent carries meaning wherever it appears | stated | **keep** |
| C4 | Semantic role colours fixed for a whole deck | variant | **keep** |
| C5 | Calm colours; functional but attractive | stated | **keep** |
| C6 | Gradients only when functional (depth, progress), never decoration | stated | **keep** |
| C7 | One palette per deck, fitted to that deck's story | dominant | **drop** — contradicts CLAUDE.md rule 4 outright. See the note below |
| C8 | Both themes readable — no component that inverts into white-on-light | stated | **keep** |
| C9 | **Never pure white, never pure black** — warm paper ground, graphite or warm-charcoal ink | dominant | **keep** |
| C10 | **Light, not dark**, by default: lit rooms lose dark-deck contrast under a projector; management reads paper-white as considered; dark/violet dashboard is the generic cliché | stated | **keep** |
| C11 | Dark stays one block of custom-property overrides away, never a redesign | stated | **keep** |
| C12 | No full-page gradients, no gradient-blob backgrounds, no cyber/neon aesthetic | stated | **keep** |
| C13 | Semantic pro/con coding fixed deck-wide with a visible legend — green positive · red negative · amber caution | dominant | **keep** |
| C14 | The accent must survive a bad projector — muted, not neon, not a framework default | stated | **keep** |

> **C7 is the one dominant corpus rule this pass drops, so the reason is recorded here rather than
> only in the reference.** "One palette per deck, fitted to that deck's story" is `dominant` — it
> describes what the decks actually do. It is also the exact thing CLAUDE.md rule 4 rules out: *ship
> one fully-resolved look, not several and not a per-topic palette.* This is not the tie-break
> firing (no external principle is involved); it is a **standing owner decision overriding an
> observed habit**, which is a third resolution class the tie-break does not cover and the reference
> has to name. R4 also grades C7 inherited — one palette per deck is the source skill's four presets
> adapted per deck — so dropping it costs the owner's signature nothing.
>
> **What survives the drop:** C1–C6 and C8–C14 are all *within-palette* discipline and are
> unaffected. The variety C7 provided returns later from the template generator CLAUDE.md rule 4
> defers, not from per-deck improvisation.

## D. Typography

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| D1 | Deliberate pairing per deck: characterful display + one superfamily for body and label | dominant | **amend** — the three **roles** survive; the **per-deck rotation** goes, with C7 |
| D2 | **Never Inter, Roboto, Arial or system-ui** — named as generic tells; a system-font body is a severity-H audit failure. *(Inter is the most frequent face in the older decks; the refined specs reject it. Do not read frequency as intent.)* | stated | **keep** — and R5 §1 independently reaches the same verdict on Inter, on cost |
| D3 | Embed faces as base64 `@font-face` — demonstrated at 7 faces in one deck | one-off | **keep** — hardened by the Delivery decision from a demonstrated option to the only shipping mode |
| D4 | `clamp()` for fluid type — display `clamp(34px, 4.2vw, 56px)` | variant | **keep** |
| D5 | Body 18–24px, line-height 1.55; mono labels 11–13px uppercase, letter-spacing 1.4px | one-off | **keep** |
| D6 | `text-wrap: balance` and negative letter-spacing on display headings | one-off | **keep** |
| D7 | **The mono layer carries the domain vocabulary** — key terms set in mono with an accent underline at first use | stated | **keep** — owner-authored, and one of the few type rules that is |

> **D1's amendment is the same decision as C7's drop, in the other medium.** R4 grades D1 inherited:
> the "deliberate pairing per deck" reading came from the source skill's instruction to rotate
> pairings and never repeat one. Under CLAUDE.md rule 4 the project ships **one** trio — R5 §2
> recommends Instrument Serif · Space Grotesk · JetBrains Mono at 97.3 KB — so the rotation has
> nowhere to go. **The structural half of D1 is the valuable half and it is kept:** three named
> roles (display · text · mono), one face each, every one a token.

## E. Diagrams, icons, illustration

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| E1 | **Never hand-draw icons.** Complex objects come from an icon set | stated | **keep** |
| E2 | Draw particles, connectors and custom diagrams freely in SVG or canvas | stated | **keep** — and the Render-technique decision widens it to WebGL |
| E3 | Embed the icon set as its official SVG symbols — that is *using* the set, not drawing | stated | **keep** — C-02 |
| E4 | Diagrams as inline SVG; authoring source may keep them as separate files | dominant | **keep** — CLAUDE.md rule 3 prefers SVG where it is as good |
| E5 | No raster images | dominant | **keep** |
| E6 | Canvas particle/emission effects read as artificial — use only when extremely restrained | stated | **amend** — C-04: the restraint survives as the *encode* test, not as suspicion of canvas |
| E7 | An accumulation effect must actually accumulate, not fall through | stated | **keep** |
| E8 | Give `<canvas>` fixed pixel dimensions via HTML attributes; let CSS scale it | stated | **keep** |
| E9 | **"Boxes everywhere" is the rejected pattern** — card grids, stat strips, pill rows, tables and bulleted lists instead of diagrams is a severity-H failure | stated | **keep** — one of the seventeen unflagged departures; R2 P-01/P-02 back it |
| E10 | **Branch where the process branches.** Four boxes joined by arrow glyphs is not a flow diagram | stated | **keep** |
| E11 | Connector lines must have arrowheads and must actually meet their target | stated | **keep** — and R2 P-17 sharpens it: label the arrow too |
| E12 | Icon set: **Lucide primary, Font Awesome free fallback** | dominant | **keep** |
| E13 | Embed the icon set as an **SVG symbol sprite containing only the icons used**, referenced by `<use>` | one-off | **keep** — C-01, C-09: this is the general resolution, not a one-off |
| E14 | **One icon per concept, used consistently** — a repeated icon is a repeated idea | stated | **keep** |
| E15 | Every SVG and chart is **theme-aware** — a hard-coded `fill="#ffffff"` stays white in dark mode | stated | **keep** |
| E16 | Vary chart types deliberately across a deck | stated | **keep** — but subordinate to R2 P-16's encoding ranking; variety never buys a worse encoding |

## F. Interaction and motion

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| F1 | Push longer text behind interaction rather than onto the slide | stated | **keep** |
| F2 | When detail is unavoidable there are exactly two answers: hide behind interaction with smooth animation, or split to a new page | stated | **keep** |
| F3 | Hidden elements reveal by **opening, turning, scaling** | stated | **keep** |
| F4 | Flows use dashed arrows, slowly animated | stated | **keep** — survives F7 because the motion *encodes flow*. The test working as intended |
| F5 | Popovers drop **below** the element, never above | stated | **keep** — and WCAG 2.4.11 gives it a conformance reason |
| F6 | Motion only where it clarifies meaning; ease-in-out, subtle | stated | **keep** — this *is* the encode test, already in the corpus |
| F7 | **No continuous ambient glow/pulse/drift on static content** | stated | **keep** |
| F8 | Soft shadows, transparency, shaders allowed — "no overdose" | stated | **amend** — "no overdose" is not testable; replaced by the encode test |
| F9 | Always respect `prefers-reduced-motion` | stated (5/12) | **keep** — promoted from `stated` to hard; R2 §9 adopts WCAG 2.3.3 above the AA floor deliberately |
| F10 | Entrance animations with `fill-mode: forwards` keep their stacking context — raise the hovered holder, not the popover | stated | **keep** |
| F11 | **A named motion vocabulary of exactly four**: Rise (entry, 340 ms, `cubic-bezier(.22,1,.36,1)`, 60 ms stagger) · Current (flow, dasharray 7 6, 4.5 s linear infinite) · Open/Turn/Scale (reveals, 380/420/300 ms) · Pulse-once (1.2 s, never looping) | one-off | **keep** — C-03's resolution rests on it |
| F12 | **Animations max 500 ms**, ease-in-out; inter-slide transition 400–500 ms | stated | **keep** |
| F13 | Reduced motion degrades the motion but **keeps the semantics** — the dashed arrows stay dashed | stated | **keep** |
| F14 | **No 3D spins, no flashy zooms, no punchy cuts** — stated independently in two specs | stated | **amend** — C-08: forbids 3D *transitions between slides*, permits the 3D *reveal of a card*. Stated precisely so the ban is not read too widely |
| F15 | Charts draw in once; never re-animate on back-navigation | stated | **keep** |
| F16 | Count-up on headline statistics; one emphasis pulse on the key number per slide | variant | **keep** |
| F17 | **Interaction reveals otherwise-lost information — never decoration.** One meaningful interaction per slide where it adds signal | stated | **keep** |
| F18 | Interactions keyboard-reachable; the slide still reads if never touched | stated | **keep** — and R2 P-26 makes the second half the testable form: close everything and read the deck |
| F19 | **Disclosure is a judgement, not a reflex** — "show the details here, do not hide them under the click" | stated | **keep** — R2 P-23 gives it the criterion it lacked: would the argument survive without it? |
| F20 | Interaction patterns built once as components and reused, so the UX is learnable | stated | **keep** |
| F21 | Two simultaneous interactions need a defined **precedence rule** — undefined is a live failure under presentation pressure | stated | **keep** |
| F22 | When a diagram changes mode, animate nodes to their new size and position | stated | **keep** |

## G. UI controls and navigation

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| G1 | Prev/next arrows | stated | **keep** |
| G2 | Clickable carousel dots | stated | **keep** |
| G3 | Keyboard: ←/→/space/Home/End | dominant | **keep** — promoted to hard by WCAG 2.1.1 (R2 P-18) |
| G4 | Progress bar | stated | **keep** — R2 P-20 reclassifies it from habit to signalling, *provided it encodes real position* |
| G5 | Slide counter / page numbers | stated | **keep** |
| G6 | **Mouse-wheel navigation between slides** | stated | **keep** |
| G7 | Click-to-jump from the dots; touch/swipe | stated | **keep** |
| G8 | The page title and the nav-bar name for that page **must match** | stated | **keep** |
| G9 | Provenance mark upper-right. *Plain text on one deck, a working link on another — the owner praised the link. Per-deck decision.* | variant | **amend** — C-07 |
| G10 | Assumption marker on the right edge, silent until wanted | one-off | **keep** |
| G11 | **A spine ribbon showing the deck's argument with the current stage lit** — "the audience never loses the thread" | one-off | **keep** — owner-authored, and R2 P-06/P-20 support it as signalling. R3 A-02 is the structure it displays |
| G12 | Appendix pages named "Appendix", and the back link names where it goes | stated | **keep** |

> **G1–G7 are the source skill's slide engine entire (R4), and all seven are kept.** Worth stating,
> because the provenance work could be misread as an argument for discarding inherited rules. It is
> not: inheritance means a rule **cannot be cited as evidence of the owner's taste**, not that it is
> wrong. A navigation bar that works is kept on its merits. What the grading actually bought is
> knowing that the identity is carried by G8–G12 — and by the spine ribbon above all.

## L. Stage and layout archetypes

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| L1 | **Fixed 1600×900 stage scaled with `transform: scale()`** — nothing reflows, pixel-identical on any projector, and what was rehearsed is what appears | one-off | **amend** — C-11, and it carries a re-scoping proposal. See below |
| L2 | The stage floats on a darker field with a soft shadow and hairline edge, giving each page its boundary | one-off | **keep** |
| L3 | A named, reused set of slide archetypes — Hero/Statement · Stat focus · Split compare (ledger) · Process/flow · Chart focus · Timeline · Case file · Loop/chapter marker · Verdict | dominant | **amend** — superseded by R3's 14-archetype catalogue, with Case File promoted out of it as a modifier |
| L4 | One dominant accent per slide for rhythm | stated | **keep** |
| L5 | Consistent margins, one grid, left-aligned headlines, breathing room | stated | **keep** |
| L6 | Card style consistent: 12–16px radius, soft shadow, thin hairline, no heavy borders | variant | **keep** |

> **L1 is where the tie-break actually bit, and the answer is not clean.** The fixed stage is the
> strongest deck in the corpus and its argument is real — *what was rehearsed is what appears* is
> worth a great deal to a presenter, and the Target-browser decision (one engine) removes most of
> the cost.
>
> **But two AA criteria are measurable and they lose to nothing.** R2 §9 sets WCAG 2.2 AA as the
> floor; **1.4.4 Resize Text** (usable at 200%) and **1.4.10 Reflow** (no two-dimensional scrolling
> at 320 CSS px equivalent) are both AA, and a scale-to-fit stage defeats both by construction —
> zooming rescales the stage instead of enlarging the text. This is exactly the class the owner's
> tie-break assigns to principle: measurable, specified, E2.
>
> **The amendment, and it is a re-scope rather than a ruling.** The fixed stage stays as the
> **presentation view** and the default. The floor then requires a second view where the content
> reflows — which is the shape this project has already used once, for printing: *a mode the user
> can force on, never a constraint on the design.* **T-014 does not have the authority to add a
> mode**, so this goes to the owner in the reference's re-scoping section, with the alternative
> stated honestly: drop the fixed stage, or accept a documented deviation from the AA floor and stop
> claiming AA. Silently keeping both claims is the one option ruled out.
>
> C-11's other half — mobile (gap G-11) — is unaffected either way, since the Portability decision
> already makes mobile secondary.

## H. Layout

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| H1 | CSS grid and flexbox throughout | dominant | **keep** |
| H2 | **Align by construction, not coordinates** — correlated rows share a grid track | stated | **keep** |
| H3 | Boxes that read as a set must be siblings in one container | stated | **keep** |
| H4 | No duplicate emphasis — one marker per point | stated | **keep** |
| H5 | No box nested in a box with its own text | stated | **keep** |
| H6 | Reset **every** heading level, `h4` and `h5` included — a partial reset is worse than none | stated | **keep** |
| H7 | Never style a bare `<b>` inside a component | stated | **keep** |

## I. Theming

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| I1 | Theme driven entirely by CSS custom properties | dominant | **keep** — CLAUDE.md rule 4 promotes it from habit to hard: *every* value that could differ between themes is a token |
| I2 | Token vocabulary already stable: `--ink` 11/12, `--bg` 9/12, `--line` 8/12, `--shadow` 7/12, plus semantic colour roles | dominant | **amend** — extended: `--measure` (R2 §12.2) and a disclosure mark (R2 P-28) are token values the corpus never named |

## J. Portability

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| J1 | Ship one self-contained file for presenting; authoring source may be multi-file | stated | **amend** — hardened by the Delivery decision: `portable` is the default *and the only shipping mode*; `linked` is authoring-loop only and shipping it is a defect |
| J2 | **Quality is never traded for self-containment** — "maximize the quality at all cost, even in multiple files" | stated | **amend** — the premise is measured false. R5 found no quality/self-containment trade-off to make, so the multi-file escape hatch has nothing to buy |
| J3 | `<meta charset="utf-8">` is mandatory — a local file has no HTTP header to supply it | stated | **keep** |
| J4 | The `file://` unique-security-origin console warning is benign | stated | **keep** |

## K. Verification

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
**Split by the boundary set during specify.** K1 and K5 are claims about *what a check may assert* —
they are part of the standard and stay here. K2, K3, K4, K6 and K7 are check **mechanics** and go to
[T-005](../../tasks/T-005-build-check-the-gate-the-deck-must-pass.md).

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| K1 | **Structural checks say nothing about layout — always render and look** | stated | **keep** — CLAUDE.md rule 6 already binds it |
| K2 | Measure every slide's content height against available height; print a table | stated | **defer → T-005** |
| K3 | Run that at two viewport sizes — 1440×900 and 1280×800 | stated | **defer → T-005** |
| K4 | Suspect the SVG's aspect ratio before the text when a slide overflows | stated | **defer → T-005** |
| K5 | DOM measurement confirms geometry you suspect; it cannot find a defect you have not thought to measure | stated | **keep** — the epistemic limit the *say which half you ran* rule rests on |
| K6 | Re-verify grid alignment after any collapse/expand interaction | stated | **defer → T-005** |
| K7 | Sweep source documents for cross-document disagreement before writing the deck | stated | **defer → T-005** — the content half of the check, per BRIEF Q6 |

## M. Critique

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
**Same boundary.** The design system owns the **standard** a critique measures against and the
**severity vocabulary** it reports in; it does not own the report's format. The rest goes to
[T-004](../../tasks/T-004-critique-mode-blunt-section-by-section-review.md).

| ID | Rule | Freq | Verdict |
| :--- | :--- | :--- | :--- |
| M1 | **The standard:** a finding is anything a grader, a presenter under pressure, or a careful reader would trip on | stated | **keep** — it is the definition of a defect, which is the standard itself |
| M2 | Findings table: `ID · Severity · Slide · Finding · Fix`, severities **Major / Minor / Note** (spec review) or **H / M / L + principle violated** (design audit) | dominant | **amend** — the **severity scheme** is kept as shared vocabulary; the table format defers to T-004 |
| M3 | **Headline verdict first**, before any per-slide detail | stated | **defer → T-004** |
| M4 | Read each slide against the requirements, against the sources, **and against the other slides for consistency** | stated | **defer → T-004** |
| M5 | Fixes applied **one at a time, in order**, each recording *was* and *now* | stated | **defer → T-004** |
| M6 | An **"Open — needs a decision"** section for anything the reviewer must not settle alone | stated | **defer → T-004** |
| M7 | A stated requirement going unmet must be **an agreed deviation, not a silent omission** | stated | **keep** — it is the rule this task just applied to L1, and it governs more than critique |
| M8 | Close with counts and an explicit **keep vs rebuild** split | stated | **defer → T-004** |
| M9 | **Watch for missing content, not just errors** — "the failure mode a self-review most easily misses" | stated | **defer → T-004** |
| M10 | Named defect classes to hunt: invented numbers · a narrative conceit that breaks mid-deck · a wrong metric on the title slide · undefined interaction precedence · an element rendering so small it reads as a fault · two numbering schemes with no mapping · no timing budget | stated | **keep** — defect classes are statements about what a bad deck is. R3's 12 anti-patterns join them |
| M11 | Reviewing only the local files once caused a whole business case to be missed — **read the authoritative source, not the convenient one** | stated | **defer → T-004** |

---

## Gaps register — where the corpus is silent

The handoff to [T-010](../../tasks/T-010-research-external-deck-design-and-ux-principles.md) and
[T-011](../../tasks/T-011-research-exemplary-decks-and-why-they-work.md). Silence is a finding: on
these, the plugin has no inherited taste to encode and must import or invent one.

Revised after the second sweep. **Five of the original twelve are now closed from the corpus
itself** — they were not silences, they were documents I had not yet read.

| # | Gap | Status | Who fills it |
| :--- | :--- | :--- | :--- |
| G-2 | Slide archetype vocabulary | **Closed, but inherited** — L3's set maps almost one-to-one onto the skill's ten slide types. **Timeline, Case file and Verdict are the owner's three additions** ([R4 §3](R4-prior-art.md)) | — |
| G-4 | Type scale | **Closed, but inherited** — D4–D6 are the skill's scales and techniques; the owner's display values are smaller | — |
| G-8 | Banned-terminology list | **Closed by another of the owner's skills** — B22–B23 are `humanize-writing` steps 2–3. Defer to it; do not re-derive ([R4 §7](R4-prior-art.md)) | — |
| G-10 | Motion token vocabulary | **Closed, shape inherited** — the four-slot vocabulary is the skill's "Choreography"; the names, durations and easings are the owner's (F11) | — |
| G-12 | Content-length rule | **Closed** — sentence <20 words, headline ≤6 words, ≤3 fragments per slide (B13–B14) | — |
| G-3 | **Narrative framework.** Partly closed: a spine question, a through-line, an emotional arc and named rhetorical beats exist — but no general framework (pyramid, SCR, assertion-evidence) is stated | Partial | T-010 |
| G-1 | **No accessibility floor.** ARIA in 8/12 and "keyboard-reachable" is stated, but no contrast ratio, focus-visible rule, tab order or screen-reader position appears anywhere | Open | T-010 |
| G-5 | **No spacing system.** Grid-based layout, card radii and hairlines are specified, but no spacing scale — which is exactly why "inconsistent spacing with no spacing rule to blame" was a real defect | Open | T-010 |
| G-6 | **Dark mode is 1/12** yet theme-inversion is a known bug class and the strongest spec says dark is "one block of overrides". Wanted more than delivered; no rule states when it applies | Open | owner |
| G-7 | **No chart conventions.** No axis, label, legend or data-ink guidance. Chart.js is used but never configured to a standard | Open | T-010 → T-006 |
| G-9 | **3D is unexplored, and the corpus argues against it.** 3D transforms in 2/12, WebGL in 0/12, and two specs explicitly forbid 3D spins. The owner now wants 3D | Open | T-011, T-016, T-017 |
| G-11 | **No mobile position.** Nothing addresses small screens — and the fixed-stage technique (L1) has direct consequences here | Open | owner |
| G-13 | **No file-size ceiling.** The one self-contained deck is 282 KB with 7 embedded faces; nothing says what is too big | Open | owner → T-013 |
| G-14 | **Deck-length rule is genuinely contradictory**, not absent — see C-05 | Open | owner |

---

## Contradictions to resolve at T-014

> **Named `X-1`…`X-11` when this note was written, renamed to `C-nn` on 2026-08-09** by
> [T-047](../../tasks/T-047-give-the-rationale-conflicts-their-own-id-namespace.md). They collided
> with `DESIGN-SYSTEM.md` §6's anti-patterns, which are also `X-nn`. **The IDs were renamed here
> rather than left as written, because these are the same eleven objects
> [`DESIGN-RATIONALE.md`](../DESIGN-RATIONALE.md) §2 resolves** — leaving one document on the old
> name would have reproduced the two-names-for-one-thing defect in mirror image. Nothing else in
> this note changed; the findings and their evidence are as recorded.

| # | Tension | Between |
| :--- | :--- | :--- |
| C-01 | Use CDN libraries for eye-candy **vs** ship self-contained | E-rules / J1 — resolved once by embedding icons as SVG symbols; does it generalise to a 3D library? |
| C-02 | Never hand-draw icons **vs** no external references | E1 / J1 — same resolution, worth stating as a general principle |
| C-03 | "No overdose", "no ambient motion" **vs** the owner's new brief for rich 2D/3D animation | F7 / F8 vs the 2026-08-06 decisions. **The sharpest conflict in the set** |
| C-04 | Canvas effects read as artificial **vs** 3D effects now wanted | E6 vs the 2026-08-06 decisions |
| C-05 | **"Aim 8, max 10"** vs **"do not exceed 18"** vs **"completeness overwrites the size limitations"** — three different rulings, three different decks, all the owner's own | A2 — deck length is a **per-deck decision, not a house rule**. But "single clean messages per slide is more important than concision" holds across all three, and progressive disclosure is the stated reconciler: *"nothing is dropped; it is folded"* |
| C-06 | Stated rules run ahead of the artefacts | §7 of R1 — general policy needed, not case-by-case |
| C-07 | **Provenance: "plain label, no link, no dead links on an unfamiliar machine"** vs **"the upper right corner link made my day, it's so useful"** | Two decks, opposite rulings, both the owner's. Depends on whether the sources are reachable where the deck is presented |
| C-08 | **"No 3D spins, no flashy zooms"** and **"Turn: `rotateY` with `preserve-3d`"** | Not actually a conflict — 3D *transition* between slides is forbidden, 3D *reveal* of a card is prescribed. Worth stating precisely so the plugin does not read the ban too widely |
| C-09 | **Icons via CDN** (Lucide, Font Awesome) vs **self-containment** | Resolved once by embedding an SVG symbol sprite of only the icons used. Does that generalise to Lucide? |
| C-10 | **A word-list check for AI tells** vs **"text can pass all five and still sound like AI"** | B22 vs B23. Constrains what T-005 may claim: the check is necessary, not sufficient, and must say so |
| C-11 | **`100dvh` flex slides** (the general convention) vs **fixed 1600×900 scaled stage** (the strongest deck) | L1 — a real fork with consequences for mobile (G-11) and for how overflow is checked (K2–K3) |
