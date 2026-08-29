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
> | [`MOTION-GUIDE.md`](MOTION-GUIDE.md) | **How to design a motion, once the vocabulary stopped being a list.** The owner's motion principles of 2026-08-19, the starter set DS-140 still supplies, and what to check before adding a motion nobody has named. **Guidance, and it gates nothing** — where it and §5.2 disagree the rule wins. Added 2026-08-21 by [T-187](../tasks/T-187-open-the-motion-vocabulary-into-a-style-guide.md), which opened DS-140 and moved five of the six principles here; the sixth became DS-243. |
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
by either of them. **The remainder closed on 2026-08-22**:
[T-041](../tasks/T-041-implement-the-nine-glitch-free-conditions.md) built conditions 2 to 8 as
`GF-2` to `GF-8`, numbered off R6's table, and every deck this repository ships passes all
seven. So eight of the nine are a verdict and the ninth is condition 9 - *looked at*, by a
person - which the gate's closing text now names as its boundary rather than leaving implicit.

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

## Release phases

**Moved to [`RELEASE-PHASES.md`](RELEASE-PHASES.md) on 2026-08-14**, whole and unedited — the three
phase tables, the reasoning behind each of the two splits, and the execution order. This heading
stays so that every reference written as `BRIEF.md` § *Release phases* still resolves; the content
is one file away.

**What it holds:** which phase each task belongs to and why, with completed rows struck through
rather than removed. **What decides a new task's phase** is `../CLAUDE.md`'s rule, not that document.

*It was 69% of this file. A specification and a per-task decision record are two kinds of document,
and the second was growing with every closure — finding `CE-05`,
[T-145](../tasks/T-145-move-brief-mds-release-phases-to-its-own-document.md).*

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
   build later. **Split 2026-08-21 by the owner, and only one half moved.**
   ~~*Speaker notes*~~ **are scoped, and the answer amends nothing** —
   [T-211](../tasks/T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md), closed 2026-08-21.
   Notes live in a **presenter build**: a second artifact from the same specification, carrying a
   marker the gate fails on, so it cannot be the file that ships. DS-088 already said *in the
   shipped deck* and stands unchanged; R1's candidate rule **A10** carried the marker *amend —
   BRIEF Q4* from the day it was written and now reads **keep**. **Built 2026-08-22 by
   [T-213](../tasks/T-213-build-the-presenter-build-and-the-marker-that-keeps-it-unshippable.md)**:
   `python tools/deck/presenter.py <deck> <slug>.slides.md` writes `<slug>-presenter.html`
   from an optional tenth `Notes` field, and that artifact fails `check.py` on DS-088 and
   nothing else. **The marker turned out to be the notes themselves rather than a flag beside
   them**, which is the half of the scope nobody had written down: a build that lost a flag
   would have passed ([L-132](lessons/L-132.md)). Attaching a note to the *right* slide took a
   second task —
   [T-217](../tasks/T-217-notes-attach-by-position-and-position-is-not-identity.md) — because
   two of the three example decks number their slides differently from their specifications.
   *PDF export* is **unchanged and still deferred** — [R7](research/R7-printable-mode.md) covers
   the printed page, and an explicit export path was not raised.
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
  [`examples/reference-deck.html`](../examples/reference-deck.html) — 12 slides, 313 KB, zero
  external references, rendered in real Chrome with DNS black-holed and all three embedded faces
  reporting `loaded`.
- ~~The build check demonstrated failing on each class of problem it claims to catch.~~ **Met
  2026-08-09** by [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md).
  `python tools/deck/check.py <deck> [--sources <dir>] [--print-pages] [--json]` decides **93 of the
  122 rules** the ruleset puts in a gate's jurisdiction and **names the other 29 with a reason and a
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
