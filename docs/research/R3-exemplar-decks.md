# R3 — Exemplar decks: the moves that survive without the presenter

Deliverable of [T-011](../../tasks/T-011-research-exemplary-decks-and-why-they-work.md). Where
[R2](R2-external-principles.md) says what to aim for, this says what hitting it looks like — reduced
to moves the build mode can actually execute. It is the source of the slide archetype library.

**Nothing here reproduces a source deck's content or visual identity.** The catalogue records the
*move*, never the slide. That is CLAUDE.md's publishing constraint applied to external material as
well as to the corpus.

---

## Bottom line

**The owner's condition on this task turned out to be the method, not a caveat.** The instruction was
not to confuse a deck's success with its presenter's quality. Applied as an admission test, it does
most of the work in this note, and it disqualifies a large part of the canon:

**1. The most celebrated presentation artifacts are mostly not artifacts.** The reveal keynote, the
single-photograph TED slide, the stage demo — their slides are close to empty, and what people
remember is a person in a room. There is nothing in them for a plugin to reproduce, because the
plugin ships the file and never the person. §2.

**2. The best exemplars for *this* project are the decks that were never presented at all.** Airbnb's
2008 seed deck was read by investors without its founders in the room and is famous for structure
over polish. The Netflix culture deck reached its audience as a document. Both are exemplary
precisely under the condition that disqualifies the keynotes — which is the strongest possible
validation of the owner's rule. §3.

**3. But the read-alone case has its own failure mode, and it is the one this project is most
exposed to.** Meeker's Internet Trends is the extreme of "meant to be read": ~200–300 slides,
famously informative, and just as famously punishing to get through. **The lone-reader audience is
not a licence to increase density** — it is the argument for progressive disclosure, which is how
this project gets the reference-document's completeness without its wall. §7.

**4. The corpus overlap is smaller than it looks, and the provenance filter is why.** Six of the
corpus's archetypes match external practice — but [R4 §9](R4-prior-art.md) rules the corpus archetype
set **inherited** from the deck skill, *except* Timeline, Case File and Verdict. So external
agreement with the inherited six is two descendants of the same canon agreeing, not independent
convergence. Only three overlaps are real. §5.

**14 archetypes admitted, 5 moves excluded as presenter-carried, 12 anti-patterns.**

---

## 1. The admission test

> **The lone-reader test.** Would this move still land for a stranger who opens the file with no
> speaker, no context, and no knowledge of whose deck it is?

Applied **before** reducing a candidate to its move, not after. That ordering is deliberate: reduce
first and you will find yourself rationalising a famous deck into the catalogue, because the move
you extracted is your own and reads well. Screening first keeps reputation out of the admission
decision.

Two consequences, and both are useful:

- **A celebrated deck whose slides are weak alone is an anti-pattern source, not an exemplar.** Its
  fame is evidence about its presenter.
- **An obscure deck whose slides carry themselves is the better exemplar.**

A candidate that fails is recorded as **presenter-carried** with its reason, never dropped silently
— §2. Several failures are instructive, and one of them splits.

---

## 2. Excluded as presenter-carried

| Excluded move | Where it comes from | Why it fails the test |
| :--- | :--- | :--- |
| **The staged reveal** — withholding the product to a scripted beat | The launch-keynote tradition | The slide is a word or an image. The effect is timing, anticipation and a room. Alone, the file contains nothing. |
| **The single full-bleed photograph** | TED-style delivery | It works because a trained speaker is talking over it. Read alone it is a photograph with no claim. Also raster, which CLAUDE.md bans independently. |
| **The live demo as the argument** | Product launches | Not a slide. Its risk profile and its payoff both belong to the person driving it. |
| **The theatrical prop or gesture** | Advocacy presentations | Explicitly not reproducible in a file. |
| **Showmanship over an animated chart** | Rosling's TED talks | **Splits — see below.** The performance is his; the encoding is not. |

### 2.1 The split case, which is the one worth understanding

Rosling's talks are the hardest case for the owner's rule, because they are genuinely famous *and*
genuinely well-made. Pulling them apart gives the cleanest demonstration of what the test is for:

- **Presenter-carried, excluded:** narrating a moving chart like a sports commentary, physically
  gesturing at the data, the pacing and the personality. Commentary on his work says plainly that
  the talks would be far less impactful without him. That half is not available to a file.
- **Transferable, admitted as A-05:** *time as an animated axis, so the shape of change is the
  message rather than a number.* This survives him entirely — the underlying tool has been used by
  people who cannot present at all, and the encoding is the reason it works.

**The general rule this produces:** when a famous presentation contains a real move, the move is
usually in the *encoding*, and the fame is usually in the *delivery*. Separate them and admit only
the first.

---

## 3. The archetype catalogue

Fourteen. Each states the move as something the build mode could execute.

| # | Archetype | Exemplar it is drawn from | The move | Use when |
| :--- | :--- | :--- | :--- | :--- |
| **A-01** | **Why-Now** | Airbnb 2008, slide 3 | Name the *external* change that makes the timing non-arbitrary — a market shift, a regulation, a cost curve. Not "the opportunity is large". | Any deck asking for a decision. It is the Complication in SCR (R2 P-04). |
| **A-02** | **Risk-Retirement Sequence** | Airbnb 2008, whole-deck structure | Order slides by the **objection each one kills**, not by topic. The reader should run out of doubts before the deck runs out of slides. | Persuasive decks with a known sceptical audience. A structural archetype, not a layout. |
| **A-03** | **Single Number** | Airbnb's early revenue figure; standard practice | One figure at display size, one line of interpretation. **The interpretation is the slide** — a number alone is a fact, not a claim (R2 P-01). | One metric carries the argument. |
| **A-04** | **Two-Column Ledger** | Consulting practice; corpus "Ledger" | A comparison where **both columns are genuinely argued**. | A real trade-off exists. See anti-pattern X-03 — this shape fails more often than it works. |
| **A-05** | **Animated Trajectory** | Rosling / Gapminder (encoding only — §2.1) | Time as an animated axis, so the *shape of change* is the message. Motion here encodes data, which is exactly the licence R2 §12.1 grants. | Change over time is the point and the endpoints alone would mislead. |
| **A-06** | **Small Multiple** | Tufte; standard practice | Repeat one chart across a facet so every comparison becomes positional. Directly supported by the encoding ranking (R2 P-16). | Comparing many series that a single chart would tangle — and the honest alternative to a rainbow. |
| **A-07** | **Before / After** | `artifact-diagramming`'s "draw the difference" | The same diagram twice with **exactly one edge changed**, and the change marked. | Proposing a structural change. The reader should be able to point at what they are choosing. |
| **A-08** | **Process / Flow** | Corpus L4; near-universal | 3–5 steps with **labelled** connectors. An unlabelled arrow means "related somehow" (R2 P-17). | A sequence with real ordering. |
| **A-09** | **Timeline with a Gate** | Corpus L6 — **owner's addition** | A horizontal sequence with one marked decision point. The gate is the information; the timeline is the frame. | A plan whose value is *when the commitment happens*. |
| **A-10** | **Architecture View** | Corpus "Instrument"; `artifact-diagramming` | Show the mechanism, not its name — only the parts the argument turns on. | Explaining a system whose behaviour, not whose inventory, is at issue. |
| **A-11** | **Manifesto Line** | Netflix culture deck | One declarative sentence, set large, no supporting body. The whole slide is a claim. | A position that must be unambiguous and quotable. Exceptionally strong on the lone-reader test — that deck reached most of its audience as a document. |
| **A-12** | **Uncomfortable Truth** | Netflix culture deck; corpus "Statement" | State the **cost** of the recommendation in the deck's own voice, before anyone asks. | The proposal has a real downside. Omitting it is what makes a deck read as sales collateral. |
| **A-13** | **Layered Detail** | Corpus "Case File" — **owner's addition** | Headline claim visible; evidence behind a disclosure affordance. **Closed, the slide still makes its point** (R2 P-26). | The default for this plugin. It is the mechanism, not a variation — see §8. |
| **A-14** | **Verdict / Close** | Corpus "Verdict" — **owner's addition** | Restate the ask as **one action**, not a summary of the deck. | The last slide, always. A recap is not a close. |

---

## 4. Reproducibility, ruled against R6 rather than assumed

Every archetype is reproducible in a single self-contained file. The column is not decorative —
[R6](R6-portability-contract.md) is what makes it a ruling rather than a hope.

| Archetype | Technique | Ruling |
| :--- | :--- | :--- |
| A-01, A-03, A-11, A-12, A-14 | Type and layout only | **Yes** — trivially. |
| A-02 | Document structure | **Yes** — not a rendering question at all. |
| A-04, A-08, A-09, A-10 | CSS grid + inline SVG, labelled | **Yes.** SVG preferred per CLAUDE.md rule 3. |
| A-06, A-07 | Inline SVG, repeated / paired | **Yes.** |
| A-05 | Animated SVG or `<canvas>` | **Yes.** R6 measured both as available from `file://`; no fetch-like access is involved, since the data is inlined. Must degrade under `prefers-reduced-motion` to a static end-state that still carries the claim — the corpus pattern of keeping the dashed arrows dashed ([R1 §11](R1-corpus-conventions.md)). |
| A-13 | CSS disclosure + minimal JS | **Yes**, with the constraints from R2 §11: two tiers only, ≥ 24 × 24 px targets, keyboard-operable, never hover-only. |

**No archetype was rejected on reproducibility.** That is worth stating plainly, because the
brief's original worry was that richness and portability would collide — and across the whole
catalogue they do not, which agrees with R6's own conclusion that no refused capability costs the
deck anything.

---

## 5. Overlap with the corpus — after the provenance filter

R1 §10 names 13 layout archetypes across two corpus specs. Naively, six of them match archetypes
above and that looks like strong convergence between the owner's practice and external exemplars.

**It is not, and [R4 §9](R4-prior-art.md) is why.** R4 rules rule L3 — named, reused slide
archetypes — as **inherited** from the deck skill's own slide-type list, *except* Timeline, Case
File and Verdict, which are the owner's additions. An external exemplar agreeing with an inherited
archetype is two descendants of the same design canon agreeing. That is one source counted twice,
which is the trap this project has already recorded once.

| Corpus archetype (R1 §10) | R3 archetype | Provenance (R4 §9) | Does the overlap mean anything? |
| :--- | :--- | :--- | :--- |
| Statement / L1 Hero | A-11, A-12 | Inherited | No — shared ancestry. |
| L2 Stat focus | A-03 | Inherited | No. |
| Ledger / L3 Split compare | A-04 | Inherited | No. |
| L4 Process / flow | A-08 | Inherited | No. |
| Instrument / L5 Chart focus | A-10, A-05 | Inherited | No. |
| **L6 Timeline** | **A-09** | **Owner's addition** | **Yes — genuine convergence.** |
| **Case File** | **A-13** | **Owner's addition** | **Yes — and it is the important one.** |
| **Verdict** | **A-14** | **Owner's addition** | **Yes.** |
| Loop (chapter marker) | — | Inherited | No external match. Kept as a corpus-only device. |

**Three real convergences, and they are not a random three.** Timeline-with-a-gate, Case File and
Verdict are exactly the three the owner added to an inherited set — the places where taste is
visible, in R4's framing. That external practice independently arrives at all three is the single
most useful result in this note for T-014: **the archetypes the owner invented are the ones
external evidence supports, and the ones inherited are the ones it is silent on.**

**Two gaps the corpus does not cover**, both admitted here on external evidence alone: **A-01
Why-Now** and **A-02 Risk-Retirement**. Both are structural rather than visual, which is probably
why a layout-oriented spec never named them, and both are the parts R2's P-03/P-04 says carry the
argument.

---

## 6. Anti-patterns

The shapes that consistently fail. Sources marked where they come from this project's own evidence
rather than the outside world.

| # | Anti-pattern | Why it fails |
| :--- | :--- | :--- |
| **X-01** | **The agenda slide** | Carries no claim and costs attention. Mayer's coherence principle (R2 P-05) is about exactly this class. |
| **X-02** | **The bullet dump** | A topic label over a list. The best-supported finding in the field is against it (R2 P-01/P-02). |
| **X-03** | **The lopsided comparison** | A two-column shape where one column is consistently the weaker, so the "comparison" is a verdict wearing a comparison's clothes. *From the corpus critique (BRIEF).* |
| **X-04** | **The diagram that isn't** | A shape that promises a relationship it does not show — the Venn whose sets do not overlap. *From the corpus critique.* |
| **X-05** | **Two points presented as a trend** | The line implies a rate the data cannot support. *From the corpus critique.* |
| **X-06** | **The Meeker pileup** | Density justified by "it is meant to be read". See §7 — this is the one this project is most exposed to. |
| **X-07** | **The misleading truth** | Figures that are individually defensible and collectively deceptive — a custom metric, a rebased axis, a window chosen after the fact. The WeWork pattern, and the reason the brief's figure-reconciliation check exists. |
| **X-08** | **The presenter-dependent slide** | Only resolves with narration. Fails the lone-reader test by construction, and this plugin cannot ship the narration. |
| **X-09** | **The click-built slide** | An argument that only completes once the presenter opens something. Directly against R2 P-26. |
| **X-10** | **The dual-axis chart** | Two y-scales invite any correlation the author wants. `dataviz` names this its single most common mistake. |
| **X-11** | **The rainbow encoding** | Hue used for magnitude. Bottom of the encoding ranking (R2 P-16) and against `dataviz`'s sequential rule; A-06 is the fix. |
| **X-12** | **Residue** | Generator branding in the corner, a typo on the most important slide. *From the corpus critique — and it is on this list because it is the cheapest defect to find and the most expensive to leave.* |

---

## 7. The density trap — the finding this project should be most careful about

The lone-reader half of the *Use case* decision creates a specific temptation: if the file must
stand alone, put everything on the slide.

**Meeker's Internet Trends is what that looks like carried to its conclusion.** It is genuinely
authoritative, genuinely useful, and has been described by reviewers as a punishing read — a deck
where the value is real and extracting it is the problem. The criticism is not that it is long. It
is that every slide pays the full density cost whether or not the reader needs that slide.

**Amazon's position is the opposite pole, and it is instructive rather than adoptable.** Narrative
memos replaced slide decks internally on the stated grounds that bullets let you hide sloppy
thinking and flatten the relative importance of ideas, and meetings open with silent reading. That
is a real answer to the same problem — but it answers it by *abandoning the deck*, which is not
available to this project.

**Between the two poles sits the thing this project already chose.** Progressive disclosure gets the
memo's completeness and the deck's pacing at once: tier one carries the argument at presentation
density, tier two carries the detail that a reference document would carry, and the reader chooses.
Meeker's deck is what this plugin produces if A-13 is treated as decoration; Amazon's memo is what
it produces if A-13 is treated as insufficient.

**So X-06 is a check, not an observation:** if the deck reads acceptably only because the reader is
assumed to be diligent, the split is wrong.

---

## 8. What this changes, and what T-014 gets

**Direct inputs to the archetype library.** The 14 entries in §3 with their reproducibility rulings,
and the 12 anti-patterns in §6 as critique-pass checks. A-01 and A-02 are additions to the corpus
set, not restatements of it.

**Three findings that change how the library should be built:**

1. **A-13 Layered Detail is not one archetype among fourteen.** Every other entry has a
   tier-one/tier-two form, and A-13 is what that means in practice. It should be built as a
   *modifier* available to the other thirteen, not as a slide type sitting alongside them. This is
   the same conclusion R2 reached from the evidence side (progressive disclosure is load-bearing),
   arrived at here from the catalogue's shape — two independent routes to the same structural
   decision.
2. **The three owner-added archetypes are the ones with external support, and the inherited six are
   the ones without.** §5. When T-014 decides which corpus conventions to keep, that split is
   evidence, and it points the same way R4 §2 did about where the owner's taste actually
   concentrates.
3. **The catalogue is structural more than visual.** A-01, A-02, A-12 and A-14 are about *what the
   slide claims and where it sits*, not about how it looks. Given the brief's decision that the
   plugin writes the words, the archetype library is as much a briefing input as a layout one —
   which affects where it lives in the plugin, and is worth settling in T-014 rather than in the
   build.

**One thing deliberately not done.** No archetype was tested by building it. The reproducibility
rulings in §4 are reasoned from R6's measured matrix, which is solid for the question *"is this
capability available?"* and does not answer *"does this layout read well at 12 slides?"* That second
question is T-014's and the build tasks', and CLAUDE.md's rule 6 governs it: it is answered by
opening a real deck and looking, not by this note.

---

## 9. Sources

**Exemplars**
- Airbnb 2008 seed deck — structure and slide-by-slide analyses:
  https://mypitchdecks.com/case-studies/airbnb-pitch-deck and
  https://www.failory.com/pitch-deck/airbnb
- Netflix culture deck (2009), Patty McCord with Reed Hastings — original posting and commentary:
  https://www.slideshare.net/slideshow/culture-2009/8469957 and
  https://fieldnotesbynick.substack.com/p/netflixs-famous-culture-deck-2009
- Rosling / Gapminder, on what the animation does and what the delivery does:
  https://www.presentationzen.com/presentationzen/2010/07/hans-rosling-tips-on-presenting-data.html
  and https://chezvoila.com/blog/rosling2/

**The density pole (§7)**
- Meeker, Internet Trends — scale and the criticism of it:
  https://www.fastcompany.com/40579187/here-are-all-294-slides-of-mary-meekers-internet-trends-report
  and https://bernoff.com/blog/worst-slides-mary-meekers-trends-report
- Amazon's narrative memo and the reasoning given for replacing decks:
  https://www.cnbc.com/2018/04/23/what-jeff-bezos-learned-from-requiring-6-page-memos-at-amazon.html
  and https://slab.com/blog/jeff-bezos-writing-management-strategy/

**Anti-patterns (§6)**
- WeWork and Theranos, on defensible-but-deceptive presentation of metrics:
  https://www.howtheygrow.co/p/why-wework-died and
  https://investorplace.com/venturecapitaldigest/2022/01/what-we-can-learn-from-the-theranos-and-wework-stories/
- X-03, X-04, X-05 and X-12 come from the corpus critique recorded in [`BRIEF.md`](../BRIEF.md), not
  from external sources.

**Internal**
- [R1 §10, §11](R1-corpus-conventions.md) — the corpus archetypes and the motion vocabulary.
- [R2](R2-external-principles.md) — the principles each archetype is checked against.
- [R4 §9](R4-prior-art.md) — the provenance verdicts that make §5's overlap map meaningful.
- [R6](R6-portability-contract.md) — the measured basis for §4.
