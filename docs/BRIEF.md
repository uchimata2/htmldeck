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
the plugin should ~~elicit~~ **assemble** exactly these:

> **Amended 2026-08-07 by [T-020](../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md).
> The six sections survive; the elicitation does not.** With brief mode absorbed, these are the
> **internal shape of the requirements stage** — filled from the two questions plus any supplied
> sources, then feeding the foundation spec. Nothing here is asked of the user section by section.

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

> **Challenged 2026-08-06 — this section predates the corpus research and was never reconciled with
> it.** [R1 §10](research/R1-corpus-conventions.md) records the owner's actual pipeline as
> *requirements → foundation spec → slide-by-slide spec → **review of the spec** → build → review of
> the build → owner review → fix*, with the deck built **page by page, in batches**, and two of the
> reviews happening **before any HTML exists**. [R4 §9](research/R4-prior-art.md) grades that whole
> structure as owner-authored with **zero prior art** — the source deck skill has no
> specification-document concept at all.
>
> **The three modes below model none of it.** There is no foundation spec, no slide-by-slide spec,
> no spec review, no batching, no approval gate and no iteration loop; critique mode reviews a built
> deck only, though R1 §14 proves two formats. Raised as
> [T-020](../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md), which also has to
> resolve this against the *Interface* decision above — a process with three approval gates and a
> promise to ask exactly two questions need reconciling, and the distinction to argue from is that
> **a question is something the user must answer in advance; a gate is an artifact they react to.**

> **Resolved 2026-08-07 by [T-020](../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md).
> The pipeline is adopted, and the three-mode list below is superseded by the one under it.** The
> correction R4 §9 forces on the challenge above is worth keeping: **A4 and A6 are graded `I`, not
> `O`** — specifying slide-by-slide before building, and reviewing before any HTML exists, are both
> inherited. What has zero prior art is **the specification as a written document**. The sequence is
> table stakes; the artifact is the departure.

~~Three modes, in build order:~~

1. ~~**Brief** — elicit the six-section prompt above from whatever the user has.~~ **Absorbed
   2026-08-07.** The six sections survive as the internal shape of the requirements the skill
   assembles from the two answers plus any sources; there is no separate elicitation mode.
   `T-003` is cancelled.
2. **Build** — generate the single-file deck. **Its input is a reviewed slide-by-slide
   specification, not a brief.**
3. **Critique** — blunt review with a BLUF verdict, in **two formats**: a **specification review**
   before any HTML exists, and a **design audit** of the built deck. R1 §14 proves both.

**The pipeline, which is what the modes sit inside**

```
governing idea (one line)
    └─→ requirements ─→ foundation spec ─→ outline ─→ OUTLINE SIGN-OFF
                                                            │
                    ┌───────────────────────────────────────┘
                    ▼
        slide-by-slide spec ─→ spec review ─→ DETAILED-SPEC SIGN-OFF
                                                            │
                    ┌───────────────────────────────────────┘
                    ▼
              build, in batches ─→ build review ─→ owner review ─→ fix
```

> **Corrected 2026-08-07.** This diagram had no **outline** in it, although
> [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) DS-210 makes one `hard` and DS-212 says the slide-by-slide
> spec is expanded from it — and it placed neither gate. Raised by
> [T-015](../tasks/T-015-plugin-scaffold-and-the-two-question-interface.md), which had to wire the
> gates and could not wire a contradiction. **The rule the owner settled: each gate immediately
> follows the artifact it gates**, so the outline is signed off before it is expanded, and the spec
> review's open decisions land at the gate directly after it. T-020 §3.2.

**Two of the four reviews happen before any HTML exists, and that is the point.** Six of the ten
rubric dimensions are checkable against a specification — S1 Claim, S2 Evidence, D1 Spine, D2
Pacing, D3 Close, and the source-reconciliation half of D4. **Three of those are among the five no
mechanical check can reach**, so the most expensive defects are catchable at the cheapest possible
moment. T-020 §3.3 has the mapping and R1 §14's own findings as the evidence.

**The specification files are always written; the gates are optional** — settled by the owner
2026-08-07. Both gates, one, or neither, at the user's request; the files exist either way. See the
*Interface* row in "Decisions taken" for why that is not a breach of the two-question promise.

> **Three documents now carry what the modes build against**, written 2026-08-06:
>
> | | |
> | :--- | :--- |
> | [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) | **The operative ruleset.** **163 rules as of 2026-08-09** — table rows; `EVALUATION.md` says **164** and both are right, the extra being **DS-000**, the override clause stated as prose in §0 rather than as a row. It is the sixth `guidance` rule, and the only figure the two totals disagree on. `python tools/deck/ruleset.py --counts` prints both. Each rule carries a stable `DS-nnn` ID, a **hard/default/guidance** label, a **Check** value — `auto` (68) · `render` (45) · `judge` (43) · none (7) — and a **Reach** value, added 2026-08-09 by [T-037](../tasks/T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md). `Check` routes a rule to the build check, the render pass or the evaluator; **`Reach` says whether a check can get at it at all**, which `Check` never did: `yes` (109) · `off-gate` (3) · `never` (1) · `—` (50 — the 43 `judge` rules **plus** the 7 whose `Check` is `—`, not "every `judge` rule" as this line read until 2026-08-09). *Re-derived after [T-038](../tasks/T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) added DS-227 and DS-228 the same day — which is the second time in one day these figures went stale, and the reason `tools/deck/ruleset.py` now computes them.* Loaded on demand; the skill body must not paraphrase it. **Counts are derived and go stale when a rule is added — re-derive, never adjust by hand** (`EVALUATION.md` §1). *The previous figures were `render` (39) against a stated total of 154, which did not sum — the instruction above was already there and had not been followed.* |
> | [`DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) | **Why each rule is what it is** — drops, provenance, derivations, and **twenty-nine conflicts**: sixteen found by reading the sources against each other, thirteen more found by building a deck strictly to the finished ruleset. **No runtime loads it.** |
> | [`EVALUATION.md`](EVALUATION.md) | **How a deck is scored and when it is good enough.** Ten dimensions with anchors, a threshold, and a convergence loop with four distinct stop conditions. **§8 is settled**: the author scores three per-slide dimensions, one fresh-context pass scores the five no check can reach, and **the user is shown the outcome and the findings, never the numbers.** |
>
> **The evaluator is what makes the ruleset operate rather than decorate.** Before it, nothing in
> this repository stated what *good enough* meant, so the loop terminated when the agent felt
> finished. **`hard` rules are gates and are never scored** — averaging a hard failure into a total
> is how a deck ships with a wrong number on the title slide and a respectable percentage.

Plus a **check** the build must pass: no external references, no banned terminology, every
`<section>` has a heading — **now semantic: the heading must be a *claim*, not a topic label
(DS-090, [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §3.3), which grows build mode as well as the check** —
contrast meets WCAG AA, and it renders glitch-free from `file://` in
the target browser. *(Printing was on this list; it is now an opt-in mode, not a gate — see
"Decisions taken".)* **"Glitch-free" is now defined as nine testable conditions** in
[R6 §8](research/R6-portability-contract.md) — two of the nine exist because this project has
watched a font check and a WebGL check both pass on a broken render. **R6 proposed them *for T-005
to implement* and T-005's own §1 never adopted them**, so it closed on 2026-08-09 having built
condition 1 and the restricted-origin half of condition 2 (DS-001, DS-005, DS-006) and having said
nothing about the other seven. Caught reconciling the two documents against each other rather than
by either of them; the remainder is
[T-041](../tasks/T-041-implement-the-nine-glitch-free-conditions.md).

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
| **Interface** | The skill asks exactly two questions: content length (max and/or min), and whether there is anything to align to. Nothing else. Extension deferred. **Refined 2026-08-07 — the promise constrains questions, and questions are not gates.** A *question* is something the user must answer **in advance**; a *gate* is a generated artifact they **react to**. The two questions stand. The pipeline adds two gates — outline sign-off and detailed-spec sign-off — and **each is independently skippable**, so a user who wants one shot says so once. **The specification files are written unconditionally**, because a file costs the user nothing until they open it and it is the only trace of what was decided when the deck later turns out wrong. Gates default to **on**. [T-020](../tasks/T-020-model-the-authoring-pipeline-not-just-the-modes.md) §3.5. |
| **Authorship** | The plugin **writes the words** from source material — it decides the narrative and the slide copy, not just the design around supplied text. Answers open question 5. |
| **Use case** | Primarily **presented live**, but the supporting detail is hidden behind interactive elements — turning cards, toggles, tabs, floating information layers, tooltips — so the same file is consumable by a recipient reading it alone. |
| **Dependencies** | **Self-contained core, optional enhancement.** Works standalone for a user who installed nothing else; uses other skills when present, with a stated fallback for each. |
| **Visual identity** | **One** theme, fully resolved on every layer — not several, not generated per topic. But **every layer parametric from the start**, because the planned next step is an in-plugin tool that generates new templates. Answers open question 3. |
| **Richness** | Interaction, smooth visuals, 2D animation and 3D effects are **wanted**. The corpus's "1–3 script tags" is a description of past work, not a target. There is no JavaScript budget. **Contested 2026-08-06 — see the note below the table.** |
| **Portability** | The binding constraint. No installation, no special privileges — the recipient double-clicks a file. **One browser must render it with no glitch**; that beats working everywhere adequately. Mobile is secondary. |
| **Printing** | **Not a requirement.** An optional mode the user can force on to make a deck printable. It must never shape the interaction design. **Measured — [R7](research/R7-printable-mode.md) — and shipped since 2026-08-08.** The mode is the **paginated stage**, one slide per page; the reading view is not a print target. [T-032](../tasks/T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) adopted it in the reference deck at a measured cost of **4.0 KB**, printed it and looked at all twelve pages; DS-222 to DS-224 carry the three rules it depends on. It constrains nothing, so the position holds — but "optional" obliges it to say what it drops, and it drops **38.6% of a deck's text** (everything behind progressive disclosure) plus the reader's paper choice. R7 §5 is the list, and the plugin now states it at handover. |
| **Target browser** | **Recent Chrome/Edge.** One engine, tested. Firefox and Safari degrade gracefully but are not the bar. |
| **Render technique** | **Full exemption from the SVG-only rule** — SVG, `<canvas>` and WebGL are all permitted, for data-carrying diagrams included. Raster images and external libraries stay banned. |
| **Script scope** | **Latin only. Non-Latin is out of scope** — settled 2026-08-06, and it is a real exclusion rather than an oversight. R5's "embedding is cheap" result rests on latin-subset faces at 27–76 KB each; a CJK face runs to megabytes even subsetted, which would reopen the delivery-mode decision below. Nothing in R1–R6 covers CJK or RTL typography, and nothing needs to. **A deck in a non-Latin script is not a supported case** — do not half-support it. |
| **Conflict tie-break** | **Split by rule type** — settled 2026-08-06, answering T-014's open question. **Principle wins on anything measurable**: accessibility, contrast, encoding accuracy, legibility. **Habit wins on aesthetic and structural choices** where the evidence is weak or absent — which is most of what makes a deck look like this owner's rather than generated. The [R2](research/R2-external-principles.md) evidence grades are what make this operable: E1/E2 material is measurable and wins; E3/E4 material does not outrank a corpus habit. |
| **Release gate** | **[T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) lands before the first published version** — settled 2026-08-06. The deliverable contract (§3.4, DS-201 to DS-209) is the rule the owner cared about most and the one no deck here satisfies, so **the plugin does not ship with a reference deck that fails it.** The example deck is the plugin's argument for itself; one that leaves its audience waiting for the presenter argues the opposite. This is a gate on publishing, not on any other work. |
| **Who scores a deck** | **The author scores S3/S5/S6 per slide; one fresh-context pass scores the five dimensions no mechanical check can reach** — S1, S2, S4, D1, D4 — settled 2026-08-06 ([T-026](../tasks/T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md)). Cost accepted: 2 scoring passes per measurement round. The decisive evidence is T-024's split — five of ten dimensions are invisible to every static and measured check, so whoever scores those *is* the quality mechanism, and a self-scoring author is the one most likely to pass its own work. [`EVALUATION.md`](EVALUATION.md) §8.1. |
| **What the user sees** | **The outcome and the findings. Never the score** — settled 2026-08-06. No per-slide total, no whole-deck total, no per-dimension number; a dimension at 0 or 1 reaches the user as a *finding naming the dimension*. The numbers imply a precision the rubric does not have (§0 of [`EVALUATION.md`](EVALUATION.md) says the score is a stopping rule, not a quality claim) and a visible number invites fixes aimed at the number. The cost accepted is opacity: the user cannot see how close to threshold a deck sits. §8.2. |
| **Delivery mode** | **Embed by default.** Two modes, not three: `portable` (everything inlined, zero external references, ~190 KB typical) is the default and the only shipping mode; `linked` (CDN) exists **for the authoring loop only** and a deck built with it is a defect the critique pass flags. No local-files mode. Settled 2026-08-06 on [R5 §4](research/R5-assets-and-licences.md) — see below. |

> **The Richness decision is contested by the strongest evidence in the field, and
> [R2 §12.1](research/R2-external-principles.md) does not pretend to have settled it.** Mayer's
> coherence principle — inessential material measurably *reduces* comprehension, 23 of 23 tests,
> median effect size 0.86 — is the best-supported result R2 found, and it cuts against decorative
> motion. This project's own rules say evidence overturns taste, so the conflict is recorded rather
> than smoothed into "use motion tastefully".
>
> **The position R2 proposes, for T-014 to adopt or overrule deliberately: motion must be
> subordinate to signalling.** Animation that marks structure — staging an argument, showing where
> you are, animating a diagram's own mechanism — *is* signalling, which the same body of work
> supports. Ambient motion that only decorates is what the evidence rules against. So the rule is
> not "less motion" but **"motion that encodes something"**, and it comes with a question a build
> check can ask: *what does this animation encode?* If the answer is "it looks good", it is the
> case the evidence is about. The Richness decision stands until T-014 rules; it no longer stands
> unexamined.
>
> **T-014 ruled, 2026-08-06: adopted.** *Motion must encode something* is now
> [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §5.2's governing rule, and §9.2 records the reasoning.
> **No re-scope is requested** — R2's reading was right that the conflict is between this row's
> *wording* and a practice that never took the permission. The corpus's four-motion vocabulary is
> kept as the mechanism, and it is what makes the rule hold rather than merely be stated.
>
> **One wording change is proposed, and it is the owner's to accept:** the Richness row's *"There is
> no JavaScript budget"* → *"There is no JavaScript budget, and every animation encodes something."*
>
> **And the owner already holds this position.** [R1 §11](research/R1-corpus-conventions.md) records
> that the corpus's most developed spec defines exactly four motions and nothing else — because *a
> named vocabulary is what stops animation becoming decoration* — and that two specs independently
> forbid 3D spins and flashy zooms. So the conflict is narrower than it looks: it is between the
> *wording* of Richness above, which reads as permission, and a practice that never took that
> permission. T-014's likely job is to notice that, not to arbitrate.

**Three consequences worth stating plainly.**

*Progressive disclosure was absent from this brief entirely.* It is the owner's signature technique
and the mechanism that lets one file serve both a live audience and a lone reader. Scoped as T-016.

> **Upgraded 2026-08-06 by [R2](research/R2-external-principles.md): it is load-bearing, not a
> signature flourish.** The *Use case* decision — presented live, detail behind interaction —
> collides directly with the best-replicated result in multimedia learning. Mayer's **redundancy**
> principle finds that on-screen text competing with a speaker reduces comprehension, and the
> **coherence** principle finds the same of anything inessential on the slide (23 of 23 tests,
> median effect size 0.86). By that literature, a deck that is also a document carries extraneous
> material by construction.
>
> **The interaction layer is what dissolves the conflict**, by separating the two audiences in time
> rather than compromising between them: hidden detail is not in the live channel during the talk,
> and is available once the speaker is gone. That makes T-016 the reason the deck can be two
> things, not a feature of it — a priority change, and R2 §12.4 is the argument.
>
> R2 §11 also answers the question T-010 left open about disclosure a presenter must operate live,
> and the answer is not the intuitive one. The availability of control measurably helped viewers
> **whether or not they used it**, while the documented harm of click-driven builds is specific and
> avoidable. The rule: **available and visible during the talk, never load-bearing in it** — a slide
> must make its point with every panel closed. Testable, and now a critique-pass check.

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

## Release phases — set 2026-08-09, split into three 2026-08-10

**Three, drawn by two questions, both the owner's.** The first, on 2026-08-09: *is this between here
and a plugin someone can install and use?* Everything it separated out shipped as **PH1**. The
second, on 2026-08-10, once PH1 had closed and all fourteen remaining tasks sat under one label:
*is this a dependency, or a minor-to-moderate fix — or is it a big piece of new capability?* The
first is **PH2**, the second **PH3**. The board is [`../tasks/README.md`](../tasks/README.md),
grouped by these names; this section is the decision, that page is its current state.

**What made the second split necessary, and where the line actually fell.** A phase every open task
belongs to has stopped sorting anything. Worse, **seven of the fourteen carried no estimate at all**,
so the board's own ranking — value, then effort — was ordering half a backlog and leaving the rest in
id order. Estimating those seven first is what made the line drawable, and it fell in one place:
**at `l`.** Every task estimated `l` or `xl` is PH3; everything `m` or below is PH2. Size and the
fix-versus-feature reading named the same five tasks, and where they could have disagreed — T-036 and
T-071, both `m` and both arguably new behaviour rather than repair — **size won, because it is the
half of the rule that can be checked.**

**What made the first split necessary.** The backlog had reached ten open tasks with no ordering except
dependency edges, and dependency order does not distinguish *needed* from *wanted*. Three of the
four steps left in [T-016](../tasks/T-016-the-interaction-and-motion-layer.md) were capabilities the
interaction layer does not reach — 3D, a frame-rate figure, the ruleset amendment the first forces —
and every one of them was between the project and a release for no reader's benefit.

### PH1 — a working plugin, published

**The whole of it is: a deck gets written, a deck gets critiqued, and a stranger can install it.**
Everything below is load-bearing for that sentence and nothing else is in.

| | Why it is in PH1 |
| :--- | :--- |
| ~~[T-016](../tasks/T-016-the-interaction-and-motion-layer.md) — the editorial split rule, its last step~~ **done 2026-08-09** | §5.3 gave build mode the mechanics of progressive disclosure and no editorial test, so without it the generator had to guess what belongs behind a click. **DS-230** now names the four kinds tier two comes in and closes the list, and **DS-231** is the one clause of DS-161 a check can decide. Struck through rather than deleted: what a release phase contained is a fact about the decision, and an item that vanishes is one nobody can check was delivered. |
| ~~[T-002](../tasks/T-002-build-mode-the-self-contained-deck-generator.md) — build mode~~ **done 2026-08-09** | The gate, the ruleset, both contracts and the reference deck all existed to serve a generator that did not. It does now: [`shell/`](../shell) is the reference deck with its content cut out, `tools/deck/shell.py` instantiates it, and `skills/htmldeck/references/build.md` is stage 6. [`examples/sort-window/`](../examples/sort-window) is a 12-slide deck built through it, with both specification files and its sources beside it. |
| ~~[T-004](../tasks/T-004-critique-mode-blunt-section-by-section-review.md) — critique mode~~ **done 2026-08-09** | CLAUDE.md makes it first-class, and the reason is that it is *the part users cannot do for their own work*. `skills/htmldeck/references/critique.md` fixes both report formats and `tools/deck/critique.py` assembles the half a program can — the spine, the figure ledger, and the 25-rule hard-judge worksheet it refuses to accept incomplete. Run against the seeded-defect deck it found **all ten** dimensions; run against the parent it found none. |
| ~~[T-056](../tasks/T-056-humanize-the-human-facing-documents-before-publishing.md) — humanize the front door~~ **done 2026-08-09** | A standing publishing constraint in CLAUDE.md, not a task's preference. It binds every release, which is why the rule now lives in [`PUBLISHING.md`](PUBLISHING.md) — the covered-set test, the exclusions, the owner's verbatim exception and the DS-106 boundary — rather than on a `blocked_by` edge that closing T-008 would spend. `README.md` has been through the pass and the repository description is drafted for T-008 to copy. Running it also caught **six figures that were already stale**: the ruleset grew when the two rows above landed and nothing re-derived the README, so 161 rows were 163 and 115 hard rules were 117. |
| ~~[T-061](../tasks/T-061-the-scaffold-check-passed-a-manifest-the-installer-rejects.md) — the manifest the installer rejected~~ **done 2026-08-09** | `v0.1.0` did not install: `plugin.json` declared `author` as a string where the schema requires an object. The smaller half. `check_scaffold.py` had called that manifest valid, because it tested whether four fields were *present* and never what they held, and the README ends its install section with that command as the proof the package is sound. Shipped as **`v0.1.1`**, which is the release to install. |
| ~~[T-064](../tasks/T-064-the-tools-crash-when-the-deck-is-on-another-drive.md) — the gates could not run off-drive~~ **done 2026-08-10** | A deck on any drive but the plugin's crashed every tool, because a display-only `relpath` cannot cross Windows drives. Fifteen sites. Shipped in **`v0.1.2`**. |
| ~~[T-065](../tasks/T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md) — the gate failed decks for what they lacked~~ **done 2026-08-10** | Four rules read *no disclosures* as *broken disclosures*. The account gained an `undecided` bucket. Shipped in **`v0.1.2`**, and its sweep criterion was later downgraded to `not met` — see T-066. |
| ~~[T-066](../tasks/T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) — make that rule a fixture~~ **done 2026-08-10** | The fixture asked only which rows *pass* on an absent subject, so the mirror question went unwatched through two fixes. `ABSENCE_IS_A_FAIL` is that mirror. Measuring rather than sweeping found **three** defects wearing one symptom: three rows genuinely absent-subject (DS-113, DS-160, DS-143), one measurement parked in the wrong block (DS-135, hoisted), and one rule the fixture's own eight-name model of a forty-key probe was failing for nothing (DS-217). Shipped in **`v0.1.3`**. Generalised as **L-54**. |
| ~~[T-067](../tasks/T-067-the-published-upgrade-instructions-do-not-upgrade.md) — the upgrade instructions do not upgrade~~ **done 2026-08-10** | Two release notes told an affected user to run a command that leaves them on the broken version. `marketplace update` refreshes the catalog and nothing else, because third-party marketplaces have auto-update off by default; `claude plugin update htmldeck@htmldeck` is what moves it. Both published notes were edited in place, and the README gained an *Upgrade it* section. Shipped in **`v0.1.3`**. |
| ~~[T-074](../tasks/T-074-the-documented-render-command-does-not-exist.md) — the documented render command does not exist~~ **done 2026-08-10** | `build.md` told every build to run `render.py shots --out <dir>`; there was no such flag and the argument was parsed as a slide list, so the step that closes the **visual** gate crashed. Underneath it, every tool anchored its output to `__file__` — an adopter's shots, PDFs, themed decks **and a copy of their deck** were written into the installed plugin. `paths.output_root` follows the deck now. The rule-level half is **check 7**: every command a skill documents names a tool, a subcommand and flags that tool's source knows. Shipped in **`v0.1.4`**. Generalised as **L-58**. |
| ~~[T-075](../tasks/T-075-ds-064-probes-for-the-reference-decks-own-class-names.md) — DS-064 probes for the reference deck's own classes~~ **done 2026-08-10** | Two of the three class names DS-064's probe looked for belonged to the reference deck and to no contract, so a conforming deck failed a rule it passes. The probe now finds the run by contracted component, and a deck it cannot find one on is undecided. **The seventh instance of the absent-subject defect, and the fixture built to end it could see two of the package's eight verdict producers** — `audit.self_test` derived them from `globals()`, one module. Moving that to the directory found four more modules and nine further rows passing on an absent subject, six of them in `theme.py`. Shipped in **`v0.1.4`**. Generalised as **L-54**'s successor, **L-57**. |
| ~~[T-083](../tasks/T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md) — the shipped example fails a `hard` rule~~ **done 2026-08-10** | `examples/sort-window/` is what `README.md` points at as the deck nobody authored by hand, and its close list set the ask at `--fs-small`: **15.0 CSS px against a 16 px floor**, since `--fs-small` is `--fs-base/1.155` and the floor is 24 du at k=0.667. Found by running the gate list T-078 had just written down. The transferable half is the token's, not the slide's, and is in `THEME-CONTRACT.md` beside `--fs-small`. Shipped in **`v0.1.5`**. |
| ~~[T-085](../tasks/T-085-the-reference-deck-does-not-carry-the-shell-it-defines.md) — the reference deck did not carry the shell it defines~~ **done 2026-08-10** | `shell/` is cut losslessly out of this deck, so the two are one fact in two files, and nothing watched the pair except a command nobody ran. T-069 reworded a comment in `shell/components.css` and edited the deck two commits later without writing the shell back. Two lines, neither able to render differently, which is why it survived. **Three decks-worth of the same failure in one day says the routine was the defect**, and `PUBLISHING.md` §8 now names both examples. Shipped in **`v0.1.5`**. |
| ~~[T-090](../tasks/T-090-spec5-cannot-parse-a-descriptive-slide-label.md) — SPEC-5 reports `NO SUBJECT` on a deck it was given~~ **done 2026-08-11** | The ledger-to-deck check identified slides by an `aria-label` of *Slide N* and nothing else, so a deck labelled *Slide 1 of 12: …* parsed to no slides and the rule reported the same verdict as a run with no deck at all — a whole gate skipped with no signal to the author. **The fourth finding of one shape**, the reference deck's own conventions encoded as though they were the contract, after `build.md`'s `--out` flag, DS-064's probe and `theme.py`'s self-test. Measured rather than reasoned: **0 pattern matches against 12** on one file. *Deck supplied and unreadable* is now a FAIL naming the cause, and it stayed inside the three verdict values because a fourth would fall outside the partition `audit.py`'s absent-subject fixture makes — the trade [T-076](../tasks/T-076-a-verdict-producer-that-exits-instead-of-reporting.md) settled the same way. Shipped in **`0.2.1`**. |
| ~~[T-091](../tasks/T-091-build-md-documents-icons-set-as-a-single-pair.md) — `build.md` documents `icons --set` in a form that fails past one icon~~ **done 2026-08-11** | `--set` takes one comma-separated argument and §2 showed a single pair, so an author with three icons followed the documentation and got an error naming an icon rather than the argument shape that lost it. [T-074](../tasks/T-074-the-documented-render-command-does-not-exist.md)'s shape exactly: **a documented procedure nobody had executed**, found by an adopter because the maintainer's own runs use the form that works. Repaired one level above the report — `option()` reads `argv.index`, so **every** flag this parser takes was dropping a repeat in silence, and refusing it there covers four more flags than the one that was reported. |
| ~~[T-008](../tasks/T-008-package-document-and-publish.md) — package and publish~~ **done 2026-08-09** | The deploy, and PH1 is closed by it: public at `github.com/uchimata2/htmldeck`, released as `v0.1.0`, `master` as the default branch. Three things were not as recorded. `master` was never divergent, so publishing was a fast-forward that discarded nothing. The marketplace entry did not exist, so the install route promised in 2026-08-07 was half-built. And 119 of 121 commits carried a personal email, rewritten to a noreply address before the first push, which is irreversible afterwards. |

| ~~[T-094](../tasks/T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md) — `render.py shots --out` with a relative path writes nothing~~ **done 2026-08-11** | Three call sites wrote `out = out or out_dir(deck)`, which reads as resolution and is not: the `or` takes the override verbatim, so only the *default* reached the function where `abspath` lives, and `--screenshot=` arrived at Chrome as a relative path. Two shots printed `FAILED` and named the file rather than the cause, at the step that closes the visual gate. Fixed by deleting two of the three resolutions — `make_probe` is the only one now, and everything downstream takes its directory off the probe it returns, which is also what lets a fixture reach it with no browser. **[T-074](../tasks/T-074-the-documented-render-command-does-not-exist.md)'s flag one layer down**: that task made `--out` parse. Found by looking at a deck, which is the step CLAUDE.md rule 6 exists for. Shipped in **`0.2.1`**. |

**`0.2.1` shipped all three on 2026-08-11**, and the version number is the thing worth recording:
this table had them *awaiting `v0.1.6`*, which is a **phase** name. As a **version** `0.1.6` is lower
than the published `0.2.0`, and plugin updates compare versions — the tag would have reached no
adopter at all. **A patch takes the next patch number on the published line whatever phase its tasks
belong to.** Caught at the release it would have broken, and written into
[`../CLAUDE.md`](../CLAUDE.md) where the next person decides a version.

| ~~[T-101](../tasks/T-101-theme-py-self-test-fails-for-every-plugin-install.md)~~ **done 2026-08-12, `0.2.2`** | `theme.py` refused to report anything from an installed plugin: its self-test compared the destination `output_root(deck)` decides against a constant anchored on the tool's own `ROOT`, and the two agree only where htmldeck is itself a git clone. So the assertion passed for the maintainer and failed for **every adopter**, and a failing self-test produces no verdict for any deck. The expectation now comes from the same deck the answer does, and the installed case — a deck with no repository above it — is one of the two it asserts. |
| ~~[T-102](../tasks/T-102-data-stage-is-an-index-and-the-contract-does-not-say-so.md)~~ **done 2026-08-12, `0.2.2`** | `data-stage` is an index into the deck's `STAGES`, `deck.js` subscripts it, and §3.2's row said nothing about the value. A deck built strictly from the contract carried `data-stage="Problem"`, opened, rendered, passed four gates and had **no ruler and no arrow keys**. The contract now says it, in a notation §2 gained for the purpose — a deck-relative range no closed set can express — and `component.py` decides it against the deck's own array. |
| ~~[T-103](../tasks/T-103-build-md-drops-ds-105s-link-clause-for-a-single-source-slide.md)~~ **done 2026-08-12, `0.2.2`** | DS-105 conditions the link on **reachability**; `build.md` conditioned it on **count**, so a slide resting on one source got a bare uppercase title that the first adopting deck's owner read as a subtitle. The one-source mark now carries the glyph and is itself the route — a link where the source is reachable, the quick view where it is a local document — which also gives `n = 1` the quick view built for exactly that case and reachable only through a control it did not get. |
| ~~[T-105](../tasks/T-105-fig-pos-neg-caution-are-vocabulary-so-a-real-deck-fails-for-using-them.md)~~ **done 2026-08-12, `0.2.2`** | §3.6 classified `.fig .pos`, `.neg` and `.caution` as `vocabulary` — *the contract styles it and no deck authors it* — and wrote down that a figure encoding a loss was the obvious next deck. That deck arrived and had to choose between drawing the loss in red and passing the gate. The sweep the fix asked for found `.t-ink` and `.mono` in the same position, so **all five rows moved to `author`** and the source now has no members: every one of them was a class this contract defines for a deck to use. |

*The phase has reopened eight times, and **the sixth was the first from outside this repository**:
T-090 and T-091 were raised on 2026-08-11 by htmldeck's first adopting project, against the published
`0.2.0`. Both arrived labelled `PH3` and were moved, because the phase a defect belongs to is decided
by where it was hit and not by its size — the effort line at `l` sorts the two phases that are not the
published one. The five before them were the project's own: `v0.1.1` through `v0.1.5`. **The seventh
is T-094, and it is the project's own again** — found on 2026-08-11 while rendering a deck to look at
it, which is where a defect in the looking step would have to be found.*

**The eighth reopening is four tasks, not one, and all four came from the adopting project on
2026-08-12** — T-101, T-102, T-103 and T-105. Three arrived as defect reports and the fourth as
feedback; the owner ruled T-105 into this phase on the ground that a published gate failing a deck
for using a documented class is a defect in the check, whatever the report calls it.

All four went out in **`0.2.2`** on 2026-08-12, by [`PUBLISHING.md`](PUBLISHING.md) §8 and nothing
else — the first release run under §8's new step 5, so it is also the first whose note names what an
upgrade stops accepting.

**The ninth reopening is three tasks, also from the adopting project, also 2026-08-12** — and it is
the first that came from a **finished deck rather than a failing command**. The project built an exam
presentation on `0.2.2`, presented it, and reported on what it was like to read:

| | |
| :--- | :--- |
| ~~[T-106](../tasks/T-106-the-quick-view-sheet-is-sized-to-the-prose-measure.md)~~ **done 2026-08-13** — `--qv-measure`, swept to `80rem`: 52 of 127 table cells wrapped at the prose measure, 0 at the chosen one, and nothing gained above it. |
| ~~[T-107](../tasks/T-107-quickviews-markdown-renderer-drops-thematic-breaks.md)~~ **done 2026-08-13** — the audit was the deliverable. Every block construct counted across **355 corpus documents**, counts only: three were one branch each and landed (thematic breaks in 119 documents, ordered lists rendered as `<ul>` in 161, front matter rendered as body text in 130), two went to **T-121**, and the `---`-versus-setext ambiguity was settled by counting rather than arguing — one setext underline in 355 documents. |
| ~~[T-108](../tasks/T-108-a-deck-has-no-back-matter-stage-so-the-colophon-is-labelled-with-the-last-argument-stage.md) — a deck has no back-matter stage~~ **done 2026-08-13** | `data-stage` was mandatory and held only argument stages, so a colophon was pushed into the nearest one and the ruler named it at rest — *Decision*, on a slide in no stage. Fixed as the missing vocabulary value it was, not the label bug it looked like: **`data-stage="back"`**, and the four renderings of the one manifest all follow. **This repository had it worse than the deck that reported it.** The reference deck had invented an eighth stage, `Colophon`, and left `STAGE_ICON` at seven — so its contents box drew `<use href="#undefined">` and printed with no mark, and its Decision-stage census ran a slide long. The census now reads **7 section ticks where it read 8**. Two rules moved with it: DS-225 had said the marks cannot be uneven, which back matter makes false, and `shell.py check` gained a `STAGE TABLE` gate so the two halves of that one table can never differ in length again. |

**All three shipped as `0.2.3` on 2026-08-13**, the ninth PH1 reopening, together with T-120 below.
Two of the three were found by looking at a rendered deck rather than by running anything, and both
were in this repository's own reference deck as well as in the adopter's.

**A fourth joined them on 2026-08-13, and it is the only one nobody reported.**

| | |
| :--- | :--- |
| ~~[T-116](../tasks/T-116-the-printed-contents-page-collides-at-thirteen-entries.md) — the printed contents page collides at 13 entries~~ **done 2026-08-13** | The **generated contents page collided at 13 entries** against a stated limit of 24: on paper the fourth row printed through the footnote and rows two and three had touching card borders. **The diagnosis in this row was the second cause, not the first.** The entry height is real, but the fault exists **only in paged layout** — Chrome gives a grid item its own content height there where the screen zeroes it, so a 267 du card sat in a 201 du pitch. `contents_bound.py`, which measures the print rules lifted onto screen, called the same deck clean on the same day; a taller fixture alone would not have caught it, verified by running exactly that. Fixed by stating both bounds — `max-height:min(268du,100%)` — plus a per-row-band description clamp, because holding the cards to their rows exposed a cut second line underneath. **It was in this repository's reference deck too**, the same 13 entries, printing with two overlapping row pairs and its footnote inside a card (**T-083**'s pattern again, **L-76**). The instrument gap is [T-123](../tasks/T-123-nothing-can-see-a-print-only-layout-fault.md). |

**A sixth joined the same day, found while verifying the second.**

| | |
| :--- | :--- |
| ~~[T-122](../tasks/T-122-the-quick-views-contracted-article-is-never-created-so-seventeen-rules-are-dead.md)~~ **done 2026-08-13** | [`COMPONENT-CONTRACT.md`](COMPONENT-CONTRACT.md) gives `.qv-doc` as an `<article>` the **script** creates inside `.qv-body`, and `openQuick()` never created it — so **seventeen style rules matched nothing in every deck this project has shipped**. A quoted source rendered at slide scale with uncollapsed table borders because the rules that say otherwise were dead. **Nothing could have caught it**: the placement check reads static markup, and the contract's own `origin: script` column is read by no check at all. **It changes [T-110](../tasks/T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md)'s premise** — that task reads the complaint as values chosen for a slide, and half of it was no values at all. |

**A fifth joined on 2026-08-13, and it is the only one a command found.**

| | |
| :--- | :--- |
| ~~[T-120](../tasks/T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md) — a hardcoded slide count in the standalone entry point~~ **done 2026-08-13** | `printpages.py`'s **own entry point** defaulted the slide count to a hardcoded `12`, so it reports `FAIL` on a 13-slide deck that prints correctly, while `check.py` — which passes the rendered count to the same function — reports `pass` on the same file. A stored copy of a derivable fact (**L-08**). `PH1` by [T-105](../tasks/T-105-fig-pos-neg-caution-are-vocabulary-so-a-real-deck-fails-for-using-them.md)'s rule: a shipped gate failing a conforming deck is a defect in the check. **This is a different caller from the one T-116's row credits** — that row is right about `check.py` and this one is about the standalone `__main__`. Found by [T-096](../tasks/T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md)'s first run. **Fixed by deriving the count from the deck and deleting the override argument**, which also required `render.slide_count` to match `slide` as a class *token* rather than a prefix — otherwise the two callers would have agreed on today's decks and disagreed on one writing `class="close slide"`. |

**These six are `0.2.3`, and the owner committed to the release on 2026-08-12** — four of them then,
**T-120 added to it by the owner on 2026-08-13**, the day the rule put it in `PH1`, and
**T-122 found the same day while closing T-107**. Open `PH1` is therefore exactly the release's
contents, which is the phase doing the job it was split for. **Three of the six are closed**: T-106,
T-107 and T-122.

**Four of the five came from *looking*, not from a failing command** — three from an adopter reading a
finished deck, and T-116 from opening the PDF that deck was printed to. No gate in this repository
could have produced any of those four, and CLAUDE.md rule 6 is the only step that would. **T-120 is
the exception and it needed a new instrument**: no command in the sixteen the last two releases were
cut on ever ran the checker that was wrong.

### PH2 — the dependencies, and every minor and moderate fix

**None of these is a shipping defect** — an adopter's deck cannot hit one, or it would be a PH1
patch by the rule in [`../CLAUDE.md`](../CLAUDE.md). They are the cheap half of what is already
known: defects in the project's own tooling, items that sharpen its record, and the two moderate
gaps in capability it already ships. Each is written up well enough to be picked up cold.

**PH2 ships on the two tasks this project can close, and the other two stay open behind it — the
owner's decision, 2026-08-10.** Of the four open when the phase was last counted,
[T-086](../tasks/T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md) and
[T-087](../tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md) are
closable here. [T-036](../tasks/T-036-the-second-contents-page-for-long-decks.md) is parked on
purpose — it bites past 24 slides and the target case is 12 — and
[T-080](../tasks/T-080-check-resolves-a-markdown-link-inside-a-code-fence.md) waited on a proposal
this project does not get to schedule, upstream's own item being `proposed` as of that date. **Both
keep the `PH2` label rather than moving to PH3**, because the line between the two phases is drawn
on effort and both are `m`: a task reassigned for being inconvenient would cost the one half of the
rule that can be checked. So the release states what it ships without, as PH1's did, and the phase
stays open behind the release that carries most of it.

**Shipped as `v0.2.0` on 2026-08-11**, carrying T-086 and T-087. T-036 and T-080 kept the `PH2`
label and stayed open behind it, exactly as decided above. **T-080 closed on 2026-08-12**, once
upstream's half had shipped and the remaining change was this project's own; **T-036 closed on
2026-08-13, and PH2 has nothing open behind it.** The phase was open for two days past its release
and both tasks in it closed on their own terms rather than being folded into the next thing, which
is what the decision above was for.

**T-036 was unparked on 2026-08-12 and re-valued `low` → `high`.** Nothing about the task changed;
its premise did. The `low` rested on one sentence — *it bites past 24 slides and the target case is
12* — and the owner has said the next deck is not limited to 12. **16 is the bound and 24 the hard
limit**, so a deck of the size now planned crosses the first and can reach the second, where DS-226's
invariant clips an entry. It keeps `PH2`: the reason it sits in that phase is unchanged, and only its
value moved. Running §8's sequence for the `v0.2.0` release
found three things no gate reports: two stale figures in [`../examples/README.md`](../examples/README.md)
(the built deck's size and its figure count, both in a sentence naming no field, so `figures.py`
leaves them unanchored), and a `README.md` tally of the preview pane's wrong answers that counted a
proof withdrawn on 2026-08-06. **Step 4 is the whole reason all three were caught**, which is the
third release in a row where the step no gate covers is the step that found something.

**One open task now blocks another, and until 2026-08-10 none did.** Every `blocked_by` edge in the
backlog used to point at closed work — T-019's on T-002, T-070's and T-071's on T-069 — so *add all
dependencies* selected nothing beyond what size already did. That stopped being true when
[T-084](../tasks/T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md) was raised:
`contents_bound.py` refuses to start, and it is the only instrument that can verify
[T-036](../tasks/T-036-the-second-contents-page-for-long-decks.md). Recorded as a change rather than
edited away, because a rule that was vacuous and then was not is worth knowing about in both states.

| | What it adds |
| :--- | :--- |
| ~~[T-036](../tasks/T-036-the-second-contents-page-for-long-decks.md)~~ **done 2026-08-13** | Built for `k` sheets rather than two: the title said *second* because 24 was the number in front of it in August, and a presented deck of 43 makes two sheets of 16 eleven entries short. Past 16 the page continues, the cut falls at a stage boundary, the sheets are balanced — 17 entries print 9 and 8, never 16 and 1 — and every sheet takes the largest sheet's grid so they cannot disagree about box height. Printed at 17, 25 and 43 and read out of the PDFs' own rectangles (**L-76**); the page count is now `n` + `k`, with `k` counted in the deck's DOM rather than recomputed. **`ceil(n / 16)` turned out to be a floor and not the answer** — 43 entries in seven even stages take four sheets, because no three contiguous stage runs fit — which is the answered question preferring the boundary to the paging. One thing was not fixed and is [T-125](../tasks/T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md): a 25-entry deck lands in the four-row band and clamps every description to one line where a 17-entry deck prints three. **What it closes is DS-226's unimplementable range**, which is why the task existed. *Why it sat in this phase, unchanged:* a **capability** for decks past the bound, `low` while the target deck was 12 slides and **`high` since 2026-08-12**, when the owner said the next one is not. Split rather than merged on 2026-08-13 — the owner asked for it in `0.2.3`, and what a patch release owes is the defect, not the capability — and built against the 16 / 24 that [T-116](../tasks/T-116-the-printed-contents-page-collides-at-thirteen-entries.md) re-measured with a three-line description in every entry. |
| ~~[T-055](../tasks/T-055-a-variant-that-leaves-malformed-markup.md)~~ **done 2026-08-10** | One seeded variant tested Chrome's parser repair, not the tag it names. Closing its `<div>` took the collateral from four rules to none: DS-091 had been reporting a slide with no headline whose headline the parser had moved. |
| ~~[T-058](../tasks/T-058-the-seeded-defect-generator-reports-edits-that-never-matched.md)~~ **done 2026-08-10** | Every seed now asserts it landed. Three edits appended to the ledger unconditionally, not the one the task named -- the S2 assumption-marker removal had never matched since the day it was written, and D1 and D2 could no-op in silence. |
| ~~[T-059](../tasks/T-059-theme-swap-overwrites-its-input-when-o-is-omitted.md)~~ **done 2026-08-10** | `swap` defaults to `.assets-cache/deck/themed/` and refuses its own input by resolved path. Requiring `-o` was the rival and lost: four shipped copy sites print the bare command, so the flag would have made all four document a command that errors. |
| ~~[T-060](../tasks/T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md)~~ **done 2026-08-10** | `tools/docs/figures.py` runs each command the README prints and partitions all 17 fences and 9 prose numerals. A figure is `compared` and fails on drift, or `volatile` — declared, reported, not enforced — because a count of the repository is stale in the commit that corrects it. |
| ~~[T-081](../tasks/T-081-the-installed-taskmd-is-two-minor-versions-behind.md)~~ **done 2026-08-10** | Updated 0.1.1 to 0.3.0. The new release's template checks found three defects here in one run, including an umbrella template `create` would never have offered. It also settled T-079 by measurement and left T-080 open by the same means. |
| ~~[T-082](../tasks/T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md)~~ **done 2026-08-10** | Three expected, 26 found, and the ledger goes 29 rows to 58. The stated pattern — figures leak behind a disclosure — was half right: five additions are tier one, including the hinge slide's own diagram labels. **Eleven values were in no source at all**, so the sources gained them; the owner ratified that direction over cutting them from the deck. Two slides declared fewer sources than they cite and were corrected in SPEC-4's direction. Completeness does not become a gate, because FIG-1 read `0 unsourced of 69` throughout (**L-62**). |
| ~~[T-086](../tasks/T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md)~~ **done 2026-08-10** | `SPEC-5`, and `spec.py` now takes the built deck as an optional third argument — optional because the tool's own instructions say to run it before a slide exists. The specification pointed at `content.py`, which does already read a deck per slide; it lost anyway, on **which ledger each tool holds**, since `content.py` builds its own precisely so as not to trust the authored one. It was red on the deck it was calibrated against: a **fifth** `Used on` over-claim, after the four T-082 found by hand, and the first no sweep caught. A literal search left 19 of 89 pairs undecided and exactly one was the defect — **L-64**. Shipped in **`v0.2.0`**. |
| ~~[T-087](../tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md)~~ **done 2026-08-11** | The reference deck, on T-082's terms — and the answer is not the one the title assumed. There is **no ledger here to sweep**: this deck was built by hand before the format existed and records provenance at source level, a colophon plus a mark per slide. It does not owe a ledger, and retrofitting one would make it claim to be a build-mode output. What the sweep found is that the record was **self-consistent and wrong** — colophon and marks agreed exactly, while three slides cited sources they never declared, one of them the timetable slide declaring only the cost model (**L-65**). Twenty values sourced, one model statement corrected, four scale marks and a build date excused with reasons. `FIG-1` read `0 unsourced of 69` throughout, the second deck to measure **L-62**. Shipped in **`v0.2.0`**. |
| ~~[T-084](../tasks/T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md)~~ **done 2026-08-10** | The fixture counted twelve contents boxes for a deck that builds thirteen — twelve slides and T-069's colophon — so the tool refused to start rather than measure. Re-baselined and left hard-coded on purpose: an assertion that exists to trip when the deck moves would agree with everything if it were derived. The bound came back **16 / 24**, unchanged, so T-036's specification stands and its edge is released. |
| ~~[T-068](../tasks/T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md)~~ **done 2026-08-10** | A prose figure is bound to the label its command prints beside it, which closed two live false passes — `12 slides`, covered twice by `8-12` inside a `DS-082` note. The owner's clause, the same figure in documents `figures.py` does not read, is bound by the claim's own construction — *part of whole*, plus the remainder — after binding by vocabulary produced 30 false alarms against 5 true ones (**L-63**). Five documents, the drift caught in each. |
| ~~[T-069](../tasks/T-069-extend-the-provenance-mark-to-multiple-sources.md)~~ **done 2026-08-10** | Multiple sources behind a mark that is its own component, and a colophon after the close under a named DS-085 exemption. The reference deck now cites the three source documents it always shipped and never named. Seeding the defect found that **DS-001's check**, not DS-001, was what had banned links — it swept every `href` while the rule enumerates subresources — so it is narrowed to anchors inside a provenance mark and DS-105 judges those. 82 of 113 rules checked. |
| ~~[T-071](../tasks/T-071-the-intermediate-specifications-carry-their-references.md)~~ **done 2026-08-10** | The foundation carries a source list and every slide a ninth field naming what it rests on; the build renders the provenance mark from that field. `tools/deck/spec.py` decides the four things the two documents can only get wrong together. The example deck was regenerated -- its shared shell had been stale since T-069 landed. |
| ~~[T-073](../tasks/T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md)~~ **done 2026-08-10** | Kept, and running. The 31 alarms behind the case for retiring it belong to the wider rule upstream tried and rejected: refcheck matches `.md` only and reports 0 broken here. A figure inherits the instrument that produced it (**L-60**). |
| ~~[T-076](../tasks/T-076-a-verdict-producer-that-exits-instead-of-reporting.md)~~ **done 2026-08-10** | The refusal moved to `main`. A themeless deck now gets 113 rules owned, 81 checked and 18 failing instead of one sentence. The open question closed against its own recommendation, because `ABSENCE_IS_A_FAIL` already held the opposite decision with a better reason. |
| ~~[T-077](../tasks/T-077-report-a-figure-exclusion-that-outlived-its-numeral.md)~~ **done 2026-08-10** | `figures.py` reports an excusal whose numeral has left the page, and fails on it. Four of the five prose exclusions were dead the minute the check existed. |
| ~~[T-078](../tasks/T-078-write-down-the-release-sequence.md)~~ **done 2026-08-10** | `PUBLISHING.md` retitled, and section 8 is the seven steps with what proves each. Writing the gate list meant running it, and three of eleven were red -- all outside the five commands the README prints. |
| ~~[T-079](../tasks/T-079-the-boards-dependency-columns-list-closed-tasks.md)~~ **done 2026-08-10** | Accepted upstream as taskmd's T-111 and shipped in 0.3.0: `index` now filters closed tasks out of both dependency columns. Verified on this board, not from a release note -- T-019's *Blocked by* is empty where it read T-002, and T-084's *Blocks* names an open task and nothing closed. |
| ~~[T-080](../tasks/T-080-check-resolves-a-markdown-link-inside-a-code-fence.md)~~ **done 2026-08-12** | Link syntax inside a fence or a span is a picture of a link: nobody can follow it, so nothing can break it. Both checkers agreed by the end — upstream shipped the proposal in taskmd 0.4.0, and `refcheck.py` followed here. **The half worth keeping is what the defect was**: the checker did not find a problem, it required the evidence to be edited, and this project's method is to paste what a tool actually printed. **Bare paths inside a fence stay checked** — a tool's own output is a promise like any other, which is why blanket fence-skipping was never the ask. The rule is in `TASK-WORKFLOW.md` §6.1 beside the `§`-in-code paragraph it generalises, and the transferable half is **L-70**. |
| ~~[T-062](../tasks/T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md)~~ **done 2026-08-09** | Retired the pre-split task tool for taskmd, keeping the two reference checks taskmd does not have as `tools/docs/refcheck.py`. |
| ~~[T-063](../tasks/T-063-improvements-to-propose-upstream-to-taskmd.md)~~ **done 2026-08-10** | Five proposals sent upstream to taskmd, from what the migration measured. |

*This table stopped listing everything in the phase it named twice, and both times a sweep found it
rather than anyone remembering: T-058 through T-063 on 2026-08-09 and 2026-08-10, then T-068 through
T-070 on 2026-08-10 — **the same drift, caught the same way**, which is the argument for the sweep.
T-071 and T-073 followed later that day, and T-076 through T-080 on 2026-08-10 from work done rather
than from planning — T-080 while writing T-079's proposal, which is the shortest that gap has ever been. The five rows that left for PH3 are below, not deleted: what a phase contained
is a fact about the decision.*

### PH3 — the bigger tasks and the new capabilities

**Each is a capability the system does not reach, and each is `l` or `xl`.** They sat in PH2 until
2026-08-10 and moved on size, not on merit: batching ten cheap items behind the largest five would
delay all ten for the benefit of none. **Two of the five — T-057 and T-041 — are things PH1 was
explicitly announced without**, which is the same judgement reached twice by different routes. The
third item on that announcement, printed contents past 24 slides, stayed in PH2: it is `m`, and the
line is drawn on size rather than on which release last mentioned something.

**The first sentence stopped being true on 2026-08-11 and is kept rather than rewritten.** Two rows
below are here **against** the size rule — T-089 at `xs` and T-092 at `s` — because PH2 has shipped,
and reopening a shipped phase is reserved for defects an adopter hit. Size still draws the line
between PH2 and PH3 while both are open; what changed is that only one of them still is. The rule a
new task is placed by is [`../CLAUDE.md`](../CLAUDE.md)'s.

| | What it adds |
| :--- | :--- |
| [T-057](../tasks/T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) | The 3D visual class, a frame-rate figure with its machine, and DS-140's fifth motion. Split out of T-016, and `xl` because it is three deliverables wearing one title. |
| ~~[T-019](../tasks/T-019-build-the-capability-preflight-the-deck-ships-wit.md)~~ **done 2026-08-11** | The capability preflight a deck ships with, as DS-009. Portability was already gated at build time; this is what the deck does on a machine that surprises it. **R6 §7's proposed check list did not survive being measured** — four of its six rows have no subject in any deck this project can build, so a deck emits two rows, or three with quick views, and the floor it declines to name turns out to be roughly *engines that shipped CSS grid*. Two things R6 did not anticipate are in the shipped mechanism: the degraded state **ships switched on**, so a blank page cannot happen by a check running too late; and the same marker covers **a browser that runs no script at all**, which no preflight can catch and which was the deck's real worst case all along. |
| [T-041](../tasks/T-041-implement-the-nine-glitch-free-conditions.md) | The seven of R6's nine glitch-free conditions nothing adopted. The gate names the gap today rather than hiding it. |
| [T-054](../tasks/T-054-record-which-clauses-of-a-rule-the-gate-decides.md) | Coverage recorded per *clause* rather than per rule — a sharper account, not a missing one. `l` because `DEFERRED` is keyed by rule ID and every producer writing into it moves with the key. |
| ~~[T-096](../tasks/T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md) — one command instead of the gate list~~ **done 2026-08-13** | [`PUBLISHING.md`](PUBLISHING.md) §8 specified it as its own excusal on 2026-08-10 and nothing claimed it; `0.2.1` was cut by running sixteen commands by hand, which is the hand-kept list one step slower rather than one step gone. `tools/check_all.py` discovers what `git` says a clone receives — **35 tools, 2 decks** — and ends with the partition: **19 ran, 1 skipped with its reason, 0 failed, 0 unclassified, 0 stale.** A tool no table names fails the run, demonstrated by adding one. **Its first run paid for itself**: three variant suites nobody had wired (all green, now gates), and `PRINT-1` — the printed page count — reached by no command at all, with the checker behind it red on a correct deck (**T-120**). |
| [T-095](../tasks/T-095-static-variants-builds-its-static-half-from-a-hand-kept-list.md) | The seeded-defect suite names its verdict producers instead of deriving them, so a producer added tomorrow sits outside it. Found by T-093 moving a rule between producers and getting `MISSED` — loudly, because a variant for that rule happened to exist. |
| [T-097](../tasks/T-097-ds-004s-excusal-says-degrade-gracefully-is-unobservable-and-ds-009-gave-it-an-instrument.md) | DS-004's excusal calls *other engines degrade gracefully* unobservable. DS-009 gave the degradation half of it an instrument, and the account cannot notice an excusal that goes stale without its rule becoming checked. |
| [T-109](../tasks/T-109-one-source-reference-component-rendered-in-three-places.md) | **One source-reference component, four kinds, three render sites** — the mark, the list behind it, and the colophon. Authoring the colophon separately is what let it drift into bare titles with a footnote pointing backwards, so rendering one component three times is DS-136 applied where it most obviously was not. Carries the ruling that **a local file never ships as a `file://` link**: DS-105 already says so, the reason is that the recipient's machine has never seen the author's paths, and the request will be made again. |
| [T-110](../tasks/T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md) | A quoted source inherits the deck's projection typography and is read at arm's length. The contract's promise that `.qv-body` styles every element it may contain is **kept** — the values are simply the deck's. Blocked on T-106 and T-107: the measure and the element set are both inputs, and choosing a scale before either is settled is choosing twice. |
| [T-111](../tasks/T-111-a-named-slide-transition-chosen-per-deck.md) | **`slide` and `immediate`**, a closed pair. DS-141 already reserved 400–500 ms for an inter-slide transition, so this builds the thing the rule was written for. The outgoing slide animates and the incoming one does not — two slides moving at once is the mush that reads as cheap. The owner cut a book-page curl and an explosion on the day it was raised; **their DS-144 and DS-150 collisions are recorded in the task** so the later brainstorm starts from the constraints instead of rediscovering them. |
| [T-112](../tasks/T-112-motion-density-and-the-split-between-content-and-affordance-motion.md) | **Motion density, 0–100, default 10** — and the split that makes one parameter coherent. **Affordance** motion says *this is a control and you just touched it* and always runs; **content** motion animates the argument and is what density selects. Every exemption the owner listed is an affordance, which is how the line was found. Density decides **how much conformant motion runs** and never invents an effect: the deck's best moment, a `0` that pulses under *"Nothing here measures the forecast"*, is DS-147 applied mechanically to a figure that happened to be zero, and nobody designed it. Selection must be **deterministic**, or the deck stops being diffable. |
| [T-113](../tasks/T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) | Research, and **its first finding is that the question cannot be asked as posed**: there is no chart component to compare a library against — `0` chart classes in the shell, one incidental mention in the contract — while DS-146 and DS-147 both legislate chart behaviour. Six gates decide a candidate, all of them existing rules, and **framework weight is checked first** because it is the one most likely to settle it. Two deliverables, not one: a recommendation, and the threshold below which hand-authored SVG wins. |
| [T-117](../tasks/T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) | Two diagram gaps, both **worked around silently by a careful build**, which is why neither was ever reported. The **decision diamond has no label slot**, so two slides render an empty rhombus with its caption floating beneath — and the deck's specification asked for the label *inside*, which the component cannot do. And **diagrams are centred in the body rather than placed on the slide's column grid**, so on three slides the diagram's left edge and the text's left edge disagree while text sits directly beneath. A gap a good build routes around is a gap nobody files. |
| [T-118](../tasks/T-118-a-style-must-mean-the-same-thing-in-the-reading-view.md) | **A treatment whose meaning comes from contrast with its neighbours changes meaning in the reading view**, because the stage is twelve separate frames and the reading view is one continuous column. The instance: a centred bottom line that reads as a closing gesture on the last slide and as one stray centred paragraph among twelve left-aligned ones in the document. Nothing is broken and both renderings are correct — what fails is the meaning, in the second one. Scoped around **rarity**, which is the countable half of "depends on contrast", and guarding DS-070–076's conforming-alternate promise. |
| [T-114](../tasks/T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) | **The container is for navigation.** The ruler, the counter and the pager are one thing and share a box; *Read* and *Motion* are not and leave it. That principle explains the complaint without appealing to weight at all — the pager was not under-styled, it was in the wrong company. **Option Y chosen 2026-08-12**: a standalone `More` control whose menu opens **upward**, knowingly against DS-138, for the room to take a third item later. So **DS-138 is step one and gates every line of chrome code** — either the exemption is argued and written into the rule with its boundary, or the rule is amended. The boundary's test is that the multi-source mark is content and stays bound. Drawing the first sketch is what found the collision, which is the argument for sketching before building. |
| ~~[T-070](../tasks/T-070-the-quick-view-for-a-source-document.md)~~ **done 2026-08-11** | A source rendered inside the deck, as an overlay. **The format set is decided by three admission tests rather than enumerated** — embeds with no external reference, executes no script, stays inside the size bound — after the owner extended it past Markdown and plain text on 2026-08-10. Unblocked the same day: it owns the linked form T-069 deliberately left as plain text. |
| ~~[T-088](../tasks/T-088-a-figure-in-a-sentence-naming-no-field-goes-stale-unwatched.md)~~ **done 2026-08-11** | A figure stating a property of a **named artifact** becomes decidable, so it stops living in `figures.py`'s `unanchored` bucket. Raised 2026-08-11 from the `v0.2.0` release, which found **three** stale figures in there by hand. `l` because the deliverable is a false-alarm measurement over every document the gate reads, in the shape [T-068](../tasks/T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) used to *reject* the wider rule — a recorded rejection meets its criteria too. The owner allowed a manifest on the day it was raised, which removes the inference half and leaves the measurement. |
| ~~[T-089](../tasks/T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md)~~ **done 2026-08-11** | The disposal a withdrawn task gets, written down, and **T-072 reconstituted as the `cancelled` stub the rule then requires**. Raised 2026-08-11 from the pre-`PH3` audit, which found the ID hole by counting index rows against filenames. **`xs`, and here against the size rule** — the owner placed it, because PH2 has shipped and reopening a shipped phase is reserved for adopter defects, which this is not. |
| ~~[T-093](../tasks/T-093-ds-005s-check-bans-the-one-esm-route-r6-measured-as-working.md)~~ **done 2026-08-11** | DS-005's predicate matched the call rather than the argument, so it forbade `import(blob:)` — the one route R6 §6 measured as working, and the one DS-006 exists to make work. Raised and closed the same day out of T-019, which found it by writing a preflight row that probes `import()` and noticing the row could never ship. The rule was right and is unamended. |
| ~~[T-098](../tasks/T-098-check-reports-briefs-phase-tables-as-a-second-index.md)~~ **done 2026-08-12** | taskmd 0.5.0's new `DUPLICATE INDEX` advisory fires on **this section**, and correctly: the three tables here name a **majority** of every known task id, which is the threshold upstream chose so it scales instead of needing a number. The document is right too — a row per task with a rationale the generated board does not hold. **Accepted and recorded, and the line is ignored by the file it names rather than by its rule** — so a `DUPLICATE INDEX` against any other document still reads as new. The decision lives in [`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) §6, where the checker's output is documented, and not in the release checklist, which runs a few times a month against a gate that runs on every task edit. No upstream exclusion was asked for: an opt-out marker is a silencer for an advisory whose value is that it cannot be silenced. |
| ~~[T-099](../tasks/T-099-rename-the-release-phases-so-they-cannot-be-read-as-versions.md)~~ **done 2026-08-12** | **The phases stopped being called `v0.1`–`v0.3`.** L-69 had declined this rename the day before, having priced the edit and not the reading; the owner then reported confusing a phase for a version repeatedly in conversation, which is a cost no gate here can see. 282 mentions across 60 files, and it could not be a blind substitution — `v0.1` is a prefix of `v0.1.5`, so the pattern that finds the phase finds five real versions. `shipped_in` is the other half: the version a task's work first reached an installed copy in, derived from the first tag containing the commit that closed it, so this phase's tasks can read `PH3` and `0.2.1` at once without contradiction. |
| ~~[T-100](../tasks/T-100-a-release-adds-a-required-part-and-conforming-decks-fail-silently.md)~~ **done 2026-08-12, `0.2.2`** | Two releases running added a required part and told adopters through failure output: `0.2.0`'s per-slide `Sources` field, then `0.2.1`'s capability preflight, six failures across three gates against a deck nobody had edited. The requirement is documented before it is enforced both times, so this is about **arrival**, not about what is asked. `PUBLISHING.md` §8 gained a step and §8.1 a table: what newly fails, and the smallest edit, per version. The expensive half was never the reading — an adopter who has not baselined cannot tell a new requirement from a regression. |
| ~~[T-104](../tasks/T-104-an-svg-marker-defined-in-one-slide-does-not-paint-in-another.md)~~ **done 2026-08-12, `0.2.2`** | A `<marker>` defined in one slide and used in another paints nothing — every slide but the current one is `visibility:hidden` — so an adopting deck shipped **four of five diagrams with no arrowheads** past every gate here. DS-117 bans an arrowhead the data does not support and never required one it does, which is why nothing saw it. **DS-232** is the new rule and it is `auto`: a paint reference resolving in another slide is a static comparison. DS-117 is unchanged — *directional* is not decidable from markup. |
| ~~[T-092](../tasks/T-092-product-feedback-from-the-first-external-deck.md)~~ **done 2026-08-11** | Six things a real deck owner found wanting after presenting-quality review, routed to the tasks that own them — **four of the six to tasks that are `done`**, each of which built exactly what it specified. Raised 2026-08-11 by the first adopting project, and kept apart from its defect reports on purpose: filed together, the interesting half gets triaged as bugs and closed by making code match documentation. It carries two named collisions it does not rule on — DS-105 forbids the `file://` link a deck needs to reach its own sources, and DS-092's four-sentence mark cannot hold a descriptive source line — and one reusable lesson: **a workaround recorded as a local deviation is a product finding nobody has reported yet.** `s`, and here by T-089's placement rather than by size. |
| ~~[T-124](../tasks/T-124-an-adopter-cannot-refresh-a-decks-shell-after-an-upgrade.md) — an adopter cannot refresh a deck's shell after an upgrade~~ **done 2026-08-13** | Every release changed the shell and **no deck already built could receive the change** — the choice was rebuilding the deck or hand-patching two regions of a 250 KB file, which is why the first adopter's deck sat two releases behind. `shell.py sync <deck> --write` is the one command that closes it, and it is the reason a migration is now a step in a release rather than a discovery. `m`, so under the size rule it would have been PH2 work; it is here because PH2 had shipped and this is not a defect an adopter hit, which is `../CLAUDE.md`'s placement rule doing what it was written for. |
| ~~[T-125](../tasks/T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md) — a split contents page still clamps its descriptions to one line~~ **done 2026-08-13** | T-036 let the contents page continue onto further sheets and left each sheet's capacity at 16 — the same number that triggers the split, so a continued page still printed the four-row band and its one-line clamp. **Two caps rather than one**: a lone sheet holds 16, a sheet of a continued page holds 12, which is the largest that still shows a three-line description. Printed and measured at 13, 17, 25 and 43 entries. `s` and a `decision` — the capacity was a ruling to take, not a bug to fix. |
| ~~[T-126](../tasks/T-126-shell-py-refuses-every-command-while-a-tracked-deck-is-behind-the-shell.md) — shell.py refuses every command while a tracked deck is behind the shell~~ **done 2026-08-13** | One self-test fixture asserted that `examples/reference-deck.html` is **already** in step, so editing `shell/deck.js` disabled the tool that carries the edit to the decks — and every other `shell.py` command with it. The tool went down at the exact moment its purpose applied. `xs`, and the lesson is bigger than the fix: **L-78**, a self-test may not assert the state of a tracked file. Here by the same post-PH2 placement rule as T-124. |
| ~~[T-127](../tasks/T-127-figures-py-refuses-to-report-a-drifted-figure-because-its-fixture-needs-an-undrifted-page.md) — figures.py refuses to report a drifted figure~~ **done 2026-08-13** | **L-78's second instance, found the same afternoon.** `figures.py` seeds fixture 9 against the *correct* value of a figure in `examples/README.md`; when that page has drifted the string is not there, nothing is seeded, and the tool exits saying the tool is wrong — with the drift it exists to report sitting in the failure message. `xs`, and it announces itself loudly, so it costs a moment rather than a session. |
| [T-129](../tasks/T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) — the reference deck's figures are unwatched and two are wrong | **A published page understates a shipped deck by 12 KB, and no gate can see it.** `examples/README.md` states 250 KB / 255 787 bytes for a deck that is 262 KB / 268 563; the manifest prints the right answer two lines below the wrong one and the run ends `0 stale figure(s)`, because that sentence is bound to nothing while sort-window's is bound. **T-088's defect class on the other deck** — that task fixed the instance it found rather than the class. Found by T-127's rebuilt fixture refusing on a claim the page does not bind. `s`, and it goes **before T-128**, which would otherwise add a third deck to the same page and the same hole. |
| [T-128](../tasks/T-128-publish-the-adopter-deck-as-a-worked-example.md) — publish the adopter deck as a third worked example | **The only deck here nobody wrote to pass these gates.** Both existing examples were authored inside this repository against its own rules; this one was built elsewhere by someone reading the published skill, which makes it the only honest test of the ruleset — and it is 13 slides, where the contents page first collided. It also exercises the upgrade path end to end, since the copy is two releases behind. `l` because the sanitizing is editorial work across a 13-slide deck and its documents rather than a substitution. It carries **the one scoped exception** to *never copy deck content in*, ruled 2026-08-13 and recorded in `../CLAUDE.md`. |
| ~~[T-123](../tasks/T-123-nothing-can-see-a-print-only-layout-fault.md) — nothing can see a print-only layout fault~~ **done 2026-08-13** | The fault T-116 fixed had reached **three printed decks with every gate green**, because the only tool aimed at that page measures a screen simulation of print (**L-76**). The owner narrowed the 2026-08-08 ruling twice: gate the printed geometry, and gate **any deck the tool is pointed at** — which made the dependency question unavoidable, since an adopter has to be able to run it. `l` on the instrument, and the instrument turned out to be ~330 lines of standard library: the tens-of-thousands coordinates that had defeated two earlier attempts were a missing graphics-state stack, not a property of Chrome's writer. **`printgeom.py` reads card rectangles out of the printed PDF; `contents_bound.py` keeps the bands and loses the claim about paper.** DS-222 to DS-225 stay with the person who prints — this narrows the ruling only where the property is arithmetic. |

*The largest thing on the board is T-070 and the least certain to be worth it is also T-070 — its own
raising note says so. That pair is why the phase exists rather than an ordering within one.*

**What PH1 shipped without, stated rather than discovered.** No 3D. No frame-rate figure on any
machine. Seven of R6's nine glitch-free conditions unimplemented, and a console error that does not
stop a deck still invisible to the gate. Printed contents pages that do not continue past 24 slides.
Those belong in the release notes, not in a list of things to fix first. **The last of them was
built after all** — T-036 on 2026-08-13, and T-125 capped its sheets the same day; the rest of this
list still stands.

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
7. ~~**The fixed stage versus the accessibility floor.**~~ **Answered 2026-08-06 by the owner: keep
   the stage, add a reflow view.** Built and **enforced** by
   [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md), closed 2026-08-07; the
   rules are [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) §2.4 and §2.5, and twelve of the fourteen are
   now gated by `tools/deck/contract.py`. Building the gate amended three of them — the tolerance
   in DS-063 had never been measured for the category it names, and DS-065 could not be false.

   **The owner's reason for the stage is the part worth recording, because it changed the design
   system rather than only closing the question.** The stage was on the record as a rehearsal
   guarantee — *what was rehearsed is what appears* — which reads as presenter convenience. It is
   not. It answers two observed failures: **a deck built for small screens breaks when opened on a
   4K display**, and **a deck presented from a high-resolution monitor arrives illegible** after
   Zoom, Meet or Discord re-encode the shared screen at 1080p or 720p.

   The second has an arithmetic answer. Under a uniformly scaled stage, **the presenter's viewport
   cancels out of the legibility equation** — what the audience receives depends only on the design
   size and the call's resolution, never on the machine it is presented from. **No responsive layout
   has that property**, which is why "drop the stage for flex slides" moved from *cheaper but worse*
   to *ruled out*: it re-introduces the defect.

   **It also produced a type floor the research could not have derived.** 720p is the binding case,
   body text lands at **24 design units**, the corpus's 18–24 range loses its lower half, and the
   corpus's 11–13 unit mono labels are demoted to decoration because they are illegible in a
   downscaled stream.

   **The conformance claim is now stated precisely** — AA *via a conforming alternate version
   reachable by a persistent control*, never a bare "this deck is AA".
5. ~~**Content vs. design split.**~~ **Answered above:** the plugin writes the words. It is the
   harder path and the acceptance criteria for build mode must reflect that.
6. ~~**Do brief, build and critique get the source documents?**~~ **Answered 2026-08-06 by the
   owner: ask for them, and reconcile when they are given.** The check has two halves, and the
   content half is the one that catches what an audience actually gets hurt by. Consequences, all
   of which are now requirements rather than options:
   - **The sources are asked for.** They join the `## Resources` section of the six-part structure,
     which already has a slot for them. *(Was "brief mode asks for the sources" — that mode was
     absorbed 2026-08-07 by T-020. **The requirement is unchanged**; it now belongs to the
     two-question interface, [T-015](../tasks/T-015-plugin-scaffold-and-the-two-question-interface.md),
     whose second question is exactly "anything to align to".)*
   - **Absence is a legitimate state, not a failure.** When they are not supplied the check runs
     presentation-only and **says so in its output** — the "say which half you ran" rule, which
     exists precisely for this case.
   - **The reconciliation technique is already known and cheap:** one table listing every figure in
     the material, its origin, and every place it is reused. The corpus audit found nine defects
     that way which five document-level reviews had passed.
   - The context cost is accepted. It buys the only check that can stop a wrong number reaching a
     board.

---

## Definition of done

*Three of seven met by [T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md),
2026-08-06. The seventh was added by the owner the same day as a **gate on publishing** — see
"Decisions taken", Release gate — and was met 2026-08-07. **Five of seven now met; the two that
remain are both about the build and critique modes, not about the deck.***

- ~~A deck renders correctly with the network disabled.~~ **Met.**
  [`examples/reference-deck.html`](../examples/reference-deck.html) — 12 slides, 262 KB, zero
  external references, rendered in real Chrome with DNS black-holed and all three embedded faces
  reporting `loaded`.
- ~~The build check demonstrated failing on each class of problem it claims to catch.~~ **Met
  2026-08-09** by [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md).
  `python tools/deck/check.py <deck> [--sources <dir>] [--print-pages] [--json]` decides **82 of the
  113 rules** the ruleset puts in a gate's jurisdiction and **names the other 31 with a reason and a
  closing condition**; a rule in neither state fails the run, so silent coverage is now impossible
  rather than merely discouraged. **41 seeded defects across four suites, all caught** — and the
  exercise keeps catching checks that were passing decks they should have failed: two on the day
  they were written (**L-42**), and **six in one sweep** when
  [T-051](../tasks/T-051-a-check-with-no-subject-must-not-report-a-pass.md) asked what every verdict
  does when its subject is absent, plus DS-091 when
  [T-053](../tasks/T-053-enforce-the-headline-ds-091-requires.md) read the rule that sweep had
  misdiagnosed (**L-44**). *The running total this sentence used to carry was recorded nowhere and
  could not be checked; the attributions can be.* What is *not* met and is named: a console error
  that does not stop the deck is still invisible to it.
- The critique mode run against a deck with known defects, and found them. *Open —
  [T-004](../tasks/T-004-critique-mode-blunt-section-by-section-review.md). The seeded-defect deck it
  needs now exists.*
- ~~**The evaluation rubric run against a deck with one seeded defect per dimension, and scored each
  0 or 1.**~~ **Met.** Ten defects seeded, all scored 0 or 1, no anchor corrected —
  [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html).
  **Five of the ten dimensions proved uncatchable by any mechanical check**, which is the result that
  matters more than the pass.
- ~~**A real 12-slide deck taken through the convergence loop to a PASS**, and looked at offline.~~
  **Met**, in two measurement rounds and 24 fixes.
- No personal, client, or machine data anywhere in the repository. *Holds — re-checked at each commit.*
- ~~**A deck in this repository satisfies the deliverable contract** — every slide states its point
  on the slide, per §3.4, DS-201 to DS-209.~~ **Met** by
  [T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md), 2026-08-07. All
  twelve slides carry a bottom line, and DS-202, DS-203 and DS-205 are gated rather than asserted —
  as are DS-216 and DS-217, which the same task found unenforced. **The publishing gate is clear.**

**The last criterion was the publishing gate**, added by the owner 2026-08-06 and met 2026-08-07.
It existed because a deck can pass every other check on this list and still leave its audience
waiting for the presenter to say what the slide was for — the failure the design system exists to
prevent, shipped as the plugin's own example. That is precisely what the reference deck was doing
while the gate reported zero failures, which is the argument for the criterion and for T-028's other
finding: **five rules were labelled machine-checkable and nothing checked them** (L-36).
