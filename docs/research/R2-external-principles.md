# R2 — External principles: what the evidence supports, what it only asserts, and what it changes here

Deliverable of [T-010](../../tasks/T-010-research-external-deck-design-and-ux-principles.md). Its
job is to give the conventions measured in [R1](R1-corpus-conventions.md) a defensible basis, and
to supply vocabulary the plugin can point at instead of paraphrasing.

**This is read evidence, not measured evidence.** Everything in [R6](R6-portability-contract.md)
came off a browser in this repository; nothing here did. That difference is carried explicitly in
an evidence grade on every principle (§2), because most published presentation advice is assertion
wearing the clothes of research, and this project has already been burned once by believing a
result whose failure mode looked exactly like a success (**L-17**, **L-18**).

---

## Bottom line

**Four things, and the second is the one that costs money.**

**1. The strongest evidence in the field contradicts the corpus habit that looks most professional.**
The assertion-evidence structure — a full-sentence claim as the slide headline, and visual evidence
under it — beats topic-plus-bullets on comprehension, on delayed recall, and on the audience's own
reported cognitive load. It is the best-supported single finding available, and it makes the slide
*headline* a piece of argument rather than a label. This is a build rule, not a style preference.

**2. This project's dual-audience decision — presented live, detail behind interaction — collides
head-on with the best-replicated result in multimedia learning.** Mayer's redundancy principle says
that on-screen text competing with a speaker *reduces* learning; the coherence principle says the
same about anything inessential on the slide. A deck that is also a document is, to that
literature, a deck carrying extraneous material by construction. **The interaction layer is what
resolves it, and that is a stronger argument for progressive disclosure than the brief currently
makes.** Hidden detail is not on screen during the talk, so it is not redundant during the talk;
it becomes available when the speaker is gone. The disclosure layer is not a nice affordance — it
is the mechanism that lets one artifact serve two audiences without violating the evidence. §11.

**3. The live-presenter open question has a real answer, and it is not the intuitive one.** The
worry was that interactive elements are a liability on stage. The controlled study that bears on it
found the opposite of the naive reading: the *availability* of control improved outcomes **whether
or not viewers used it**. Combined with the practitioner literature on click-driven builds — where
the harm is real and specific — the rule is: **disclosure must be available and visible, never
required to advance the argument.** A slide whose point only lands after the presenter opens
something is a broken slide. §11.

**4. The accessibility floor is stateable as numbers, and one of the numbers in common use is
wrong for this project.** WCAG 2.2 AA gives a concrete floor (§9). But the pt-based slide-typography
advice everyone repeats — "never below 24pt" — does not transfer to a browser deck at all, because
a deck that scales to the viewport has no fixed pt size. The transferable form is angular: size
type against *viewing distance*, not against a point value. §6.

One more, smaller: **three of this task's areas are already owned by installed skills**, and the
right move is to point at them by name — never by path. Two of the three have no files on disk at
all, and the third is in a temp directory. This does not reopen T-012; it independently confirms
what [R4 §7](R4-prior-art.md) already ruled, from the opposite direction. §3.1.

---

## 1. How a principle earned its place

The gate from the task plan: **name the rule this changes in this plugin, or reject it.** A
well-cited principle that changes no decision here is listed in §13 with its reason, so it cannot
be re-litigated later.

Two consequences worth stating:

- **Pedigree does not admit a principle.** Tufte on PowerPoint is the most-cited text in the field
  and appears only in §13, because its actionable content is either already covered by
  assertion-evidence or is a claim about a tool this plugin does not use.
- **The corpus is not evidence of correctness.** [R1](R1-corpus-conventions.md) says what the owner
  does. Where external principle contradicts it, the contradiction is recorded in §14 as a candidate
  change of direction for [T-014](../../tasks/T-014-synthesise-research-into-the-design-system-reference.md),
  not resolved quietly in either direction.

---

## 2. Evidence grades

Every principle below carries one. The grade is about **how much weight the claim can bear**, not
how much it is repeated.

| Grade | Means |
| :--- | :--- |
| **E1** | Controlled experiment, replication, or systematic review with reported effect sizes. |
| **E2** | A standards body or a measurable specification — checkable, not arguable. |
| **E3** | Practitioner consensus **with a stated mechanism** — no experiment, but the reason it works is articulated and falsifiable. |
| **E4** | Assertion. Widely repeated, no mechanism and no measurement behind it. |

The generic form of why this column exists is **L-19** in [`LESSONS.md`](../LESSONS.md).

**E4 material is not automatically rejected — it is automatically demoted.** Where an E4 rule
conflicts with an E1 or E2 one, it loses without discussion. Where nothing better exists, it may
still become a default, but it is labelled so a later session knows the default is unsupported and
may be changed cheaply.

Counted across §4–§11: **7 principles at E1, 8 at E2, 9 at E3, 2 at E4.** The two E4s are both
about visual pacing, and both are flagged in §14 as cheap to overturn.

---

## 3. What another skill already owns — point, do not restate

Run before gathering sources, per the plan, so the research does not re-derive rules the project
can reference. Three skills were read in full.

| Skill | What it owns, that this project would otherwise write | Do |
| :--- | :--- | :--- |
| `dataviz` | Colour assigned by job (categorical / ordinal / sequential / diverging / status); a six-check palette test with a **runnable validator**; mark specifications; the one-axis rule; the hover/tooltip layer; a catalogue of chart anti-patterns. | **Point.** This is more rigorous than anything R2 would produce for colour-in-charts, and it is executable rather than advisory. |
| `artifact-design` | Typeface pairing as a first-class decision; token-level theming across light/dark with the `data-theme` override; layout by flex/grid `gap`; a named list of AI-generated design tells to avoid. | **Point, with one local override.** Its warning against Space Grotesk and Inter as "safe" faces is directly relevant to [R5](R5-assets-and-licences.md)'s recommendation — see §14. |
| `artifact-diagramming` | When a diagram earns its place at all; label the arrows; `viewBox` sizing; `currentColor` theming; `<figure>`/`<figcaption>`/`role="img"` structure; the no-script-inside-SVG rule. | **Point.** It agrees with CLAUDE.md rule 3 and is more specific. |

### 3.1 The pointer problem — a finding for T-012

**These three skills cannot be referenced by path**, and the reason differs per skill:

| Skill | Files on disk? | Where |
| :--- | :--- | :--- |
| `dataviz` | Yes — `SKILL.md`, seven `references/`, one runnable script | A **version-numbered directory under the machine's temp area**. Machine-local, version-pinned, in a location designed to be cleared. |
| `artifact-design` | **No** | Injected prompt text only. Nothing to point at. |
| `artifact-diagramming` | **No** | Injected prompt text only. Nothing to point at. |

**Method, because this is exactly where the last session went wrong.** [R4 §1](R4-prior-art.md)
records that the sandboxed PowerShell tool reports the desktop app's application-data tree as
*non-existent* rather than as denied, and that a session trusting it concludes there are no files
when there are — rule M11, and it produced two wrong conclusions in one sitting. So the negative
above was established with Bash and the file tools, not the shell, and the search covered the
application-data tree R4 identified as well as `~/.claude`, the plugin marketplace cache and the
bundled-skills area. The corpus skills R4 read *are* there and were found; these two are not.

**And the tree R4 found is not a way out.** It is scoped by a session identifier, which makes it
less stable than the temp path, not more.

**This does not change T-012's answer — it independently confirms it, from a different direction.**
[R4 §7](R4-prior-art.md) already ruled: *do not probe the filesystem*, branch on the artefact rather
than on the skill, and ship the fallback as the primary path. R4 reached that from detection being
unreliable. R2 arrives at the same place from referencing being impossible — for two of these three
skills there is no file to probe *at all*, which is the strongest possible form of R4's argument.

The one thing R2 adds is a constraint on **this document and its successors**, not on the build:

> A pointer to another skill can only ever be **by name and by rule** — *"colour in charts follows
> `dataviz`"* — never by path, and it must carry its fallback inline, because the skill may simply
> not be there and nothing will say so.

That is why §4–§11 restate a rule's *consequence* even where they defer its detail: a reference that
resolves to nothing has to still leave the reader with the rule.

---

## 4. Narrative and structure

**P-01 — The slide headline is a full-sentence claim, not a topic label. [E1]**
Garner, Alley, Wolfe, Zappe & Sawarynski (2011); Alley et al. (2006). Against topic-plus-bullets,
the assertion-evidence structure produced better comprehension, fewer misconceptions, stronger
recall at delayed post-test, and **lower reported cognitive load** — the last is the interesting
one, because it means the denser-looking slide felt easier.
*Changes here:* build mode writes a sentence headline per slide and the check verifies every
`<section>` has one. This upgrades the brief's existing "every `<section>` has a heading" check from
a structural test to a semantic one — a heading that is a noun phrase now fails it.

**P-02 — Evidence under the claim is visual, not a restatement of it. [E1]**
The other half of the same structure: the assertion is carried by the headline, the body is the
graphic that supports it. A bulleted paraphrase of the headline is the failure mode.
*Changes here:* the archetype library (T-011) is a library of *evidence* shapes. A slide whose body
is prose repeating its own headline is an anti-pattern the critique pass names.

**P-03 — Lead with the answer; structure the support beneath it. [E3]**
Minto's pyramid, and the SCR/SCQA entry it pairs with. No controlled evidence, but the mechanism is
explicit and matches how the audience this project targets reads: conclusion first, support
underneath, grouped so the groups do not overlap.
*Changes here:* two things. Brief mode elicits the Goal as one transformational sentence — the
brief already asks for this, and P-03 is why. And the critique pass keeps its BLUF verdict
structure, which is the same principle applied to the review.

**P-04 — Complication before resolution, once, at the top. [E3]**
SCR's value is the *complication*: the deck earns its recommendation by naming what changed. Decks
that open with a resolution nobody asked for read as unmotivated.
*Changes here:* a structural check available to critique mode — if no slide in the first third
states a tension, the deck is a status report, and the review says so.

---

## 5. Cognitive load and signalling

Mayer's programme is the most heavily replicated body of work touching this project. Four of its
principles change something here; the rest are in §13.

**P-05 — Remove the inessential; the effect is large. [E1]**
The coherence principle held in 23 of 23 experimental tests, median effect size 0.86. That is an
unusually clean result, and it is about *removal* — decorative additions measurably cost
comprehension.
*Changes here:* this is the evidential basis for the whole no-decoration position, and it outranks
taste. Where the design layer wants ambient motion or a background flourish "because it looks
considered", P-05 is the counter-argument, and it is E1. See the conflict in §12.1 — this project
explicitly wants richness.

**P-06 — Signal the structure. [E1]**
The signalling principle: cues that mark the organisation of the material improve learning.
*Changes here:* licenses exactly the structural devices `artifact-design` warns against using
decoratively — eyebrows, section markers, progress — **on the condition that they encode something
true**. The two sources agree; the condition is the whole rule.

**P-07 — On-screen text competing with a speaker costs learning. [E1]**
The redundancy principle.
*Changes here:* this is the project's central design tension, not a small rule. It says the live
deck should be sparse; the dual-audience decision says the file must also stand alone. Resolved in
§11 by the interaction layer, and that resolution is the strongest justification the progressive
disclosure work (T-016) has.

**P-08 — Segment, and let the pace be controlled. [E1]**
The segmenting principle: learner-paced segments beat a continuous stream.
*Changes here:* the deck is already segmented — one `<section>` per slide is segmentation. What
P-08 adds is that **pacing control must be in the audience's hands when the deck is read alone**,
which is an argument for keyboard/touch navigation being real rather than decorative. Reinforced by
P-21.

---

## 6. Typography and measure

**P-09 — Running text sits at roughly 45–75 characters per line. [E3]**
Bringhurst's range, ~66 as the common target. Widely repeated; the eye-movement mechanism is
articulated. Not E1 — see the conflict at §12.2, where measured reading *speed* and reader
*preference* disagree.
*Changes here:* a token, not a hard rule — `--measure` in the theme, defaulting inside the range.
Applies to the disclosure layer's prose, which is where this deck type actually has running text;
slide headlines are not running text and are not governed by it.

**P-10 — The pt-based slide minimums do not transfer, and should not be carried over. [E4 → rejected as stated]**
"Body text never below 24pt", "30pt is the real minimum" — this is the single most repeated piece
of slide-typography advice, and it is E4: no measurement, and the numbers disagree with each other
across sources by more than 2×.
It also does not survive contact with the medium. A browser deck scaling to the viewport has no
fixed pt size; the same file is a laptop screen at arm's length and a projected wall at ten metres.
*Changes here:* **rejected in that form, replaced by P-11.**

**P-11 — Size type against viewing distance, not against a point value. [E3]**
The transferable version of P-10, from signage practice: legible letter height scales with viewing
distance (the common rule of thumb being about one inch of cap height per ten feet, with
comfortable reading needing 1.5–2× the bare-legibility minimum).
*Changes here:* the type scale is defined in **viewport-relative units against a stated reference
condition** — the theme declares what viewing distance its default scale assumes, and the scale is
one token away from being re-based for a large room. This is a design-system requirement, so it
belongs in T-014's tokens, and it is exactly the kind of thing the brief's "every layer parametric"
decision exists for.

**P-12 — Sans-serif is more legible at distance. [E3]**
Consistent in signage practice; the mechanism (stroke contrast and fine serifs disappearing at
angular size) is stated.
*Changes here:* constrains the *projected* roles only. It does not govern the disclosure layer's
body text, read at arm's length, and it must not be over-applied — see §14, where it interacts with
R5's font recommendation.

---

## 7. Colour and contrast

**P-13 — Colour in charts is `dataviz`'s, and its checks are runnable. [E2]**
Not restated here (§3). The material point is that its palette test is a **script**, not advice —
which fits this project's habit of shipping a check rather than a hope.
*Changes here:* the build check delegates chart-palette validation rather than reimplementing it,
and states in its output when it could not (the "say which half you ran" lesson).

**P-14 — WCAG 2 contrast is the conformance floor and is known to misbehave in dark mode. [E2 + E3]**
The 4.5:1 / 3:1 ratios are E2 — a specification, checkable. The criticism is E3 but well-argued and
comes with worked cases: the ratio formula overstates contrast when both colours are dark, so it is
a poor *design* guide for dark themes, and it produces pass/fail cliffs between greys no one can
tell apart.
*Changes here:* **conform to WCAG 2.2 AA as the floor, and do not use the ratio as the design
instrument.** Both statements are needed. This matters because the brief already commits to
`prefers-color-scheme` awareness through `artifact-design`, and the one place WCAG 2's formula is
weakest is exactly the dark theme.

**P-15 — APCA is a better perceptual model and is not a conformance target. [E3]**
Lc values track perceived readability across the range where the WCAG 2 ratio does not.
*Changes here:* usable as a *tiebreaker* when choosing between candidate token values that both
clear AA. It does **not** replace the AA check, and the build check must not report an APCA result
as conformance. Recorded because the temptation to swap them is real and would be a false pass.

---

## 8. Data visualisation

**P-16 — Encoding accuracy has a known ranking. [E1]**
Cleveland & McGill (1984): position on a common scale, then position on non-aligned scales, then
length/direction/angle, then area, then volume/curvature, then shading and colour saturation.
*Changes here:* the built-in SVG chart generator ([R5 §5](R5-assets-and-licences.md) settled that
there is one, and that it is hand-written) picks its default form from this ranking, and the
critique pass has an objective basis for calling out a pie chart where a bar would carry the
comparison.

**P-17 — A diagram earns its place by showing a mechanism prose cannot. [E3]**
`artifact-diagramming`'s opening rule.
*Changes here:* pointed at, not restated. Worth naming in R2 only because it is the rule that
decides *whether to draw at all*, and the corpus's 5–22 inline SVGs per deck ([R1](R1-corpus-conventions.md))
mean this project's failure mode is drawing too much, not too little.

---

## 9. The accessibility floor, as numbers

Acceptance criterion: concrete. **WCAG 2.2 Level AA is the floor.** Levels verified against the
W3C's own listing — two criteria commonly cited as AA are not.

| Criterion | Level | The number |
| :--- | :---: | :--- |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 text; 3:1 for large text (≥18pt / 24px, or ≥14pt / 18.66px bold) |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components, focus indicators, and meaningful graphical parts |
| 1.4.4 Resize Text | AA | Usable at 200% |
| 1.4.10 Reflow | AA | No two-dimensional scrolling at 320 CSS px equivalent |
| 1.4.12 Text Spacing | AA | No loss of content at the specified spacing overrides |
| 2.1.1 Keyboard | A | Every function reachable by keyboard |
| 2.4.7 Focus Visible | AA | A visible focus indicator |
| 2.4.11 Focus Not Obscured (Minimum) | **AA** | The focused component is at least partly visible |
| 2.4.13 Focus Appearance | **AAA — not the floor** | ≥ 2 CSS px perimeter equivalent, 3:1 against the unfocused state |
| 2.5.8 Target Size (Minimum) | **AA** | 24 × 24 CSS px, or the spacing exception |
| 2.2.2 Pause, Stop, Hide | A | Control over motion lasting > 5s |
| 2.3.1 Three Flashes | A | Hard limit |
| 2.3.3 Animation from Interactions | **AAA — not the floor** | Honour `prefers-reduced-motion` |

**Three notes that change what gets built.**

- **2.4.13 and 2.3.3 are AAA, and both are adopted anyway.** Focus appearance because a deck is
  keyboard-driven by design, so the focus ring is a primary interface and not an edge case; reduced
  motion because the brief wants animation and 3D, which is precisely the case that harms people
  with vestibular disorders. **Adopting an AAA criterion is a decision, so it is recorded as one** —
  claiming them as "the AA floor" would be the kind of quiet inflation this project's own lessons
  warn about.
- **2.5.8's 24 × 24 px is the number that constrains the disclosure layer.** Every toggle, tab and
  card-flip affordance is a target, and 24 px is larger than the icon-sized controls this pattern
  invites.
- **4.1.1 Parsing was removed in WCAG 2.2.** Any check written against it is checking a retired
  criterion.

---

## 10. Presentation UX: navigation, progress and control

**P-18 — Keyboard operation is a conformance requirement, not an affordance. [E2]**
2.1.1, Level A.
*Changes here:* confirms the corpus habit (keyboard navigation in nearly every deck) as
non-negotiable rather than customary, and extends it: every disclosure control must be operable and
focusable, not just the slide advance.

**P-19 — Focus order follows the visual flow. [E2/E3]**
*Changes here:* on a deck this is sharper than on a page, because slides are absolutely positioned
and off-screen slides are still in the document. **Off-screen slides must be removed from the tab
order**, or the first Tab press lands somewhere invisible — a defect a validating deck passes
cleanly, which puts it squarely in the "look at the rendered deck" category.

**P-20 — Progress indication is signalling, and is therefore justified. [E1 via P-06]**
*Changes here:* the corpus's progress indicator stops being a decorative habit and becomes a
signalling device — provided it encodes real position. This is the `artifact-design` condition
again: structure that encodes something true.

**P-21 — Offer control over pacing; the offer itself is worth something. [E1]**
Sage, Bonacorsi, Izzo & Quirk (2015). Across four pausing conditions, availability of control
benefited learners **regardless of whether they used it**, and the click-to-pause version was also
the best liked.
*Changes here:* the single most useful finding for this project's dual-use case, and it carries
directly into §11.

---

## 11. Progressive disclosure — and the open question, answered

This is the project's signature technique and the mechanism that lets one file serve two audiences.
It is also the area where the task's open question sat.

**P-22 — Two tiers, not three. [E3]**
Nielsen (2006): a primary display carrying the few most important things, a secondary display on
request. Three or more levels typically produce poor usability — people lose track of where they
are.
*Changes here:* a hard structural constraint on T-016. **Slide → detail. Never slide → detail →
further detail.** Given the pattern set the brief lists — turning cards, toggles, tabs, floating
layers, tooltips — nesting is the obvious temptation and this is the rule that forbids it.

**P-23 — The split is by frequency of need, and getting it wrong is the main failure. [E3]**
The tier-two content should be what a minority needs on a minority of occasions. Nielsen's stated
risk is precisely poor task analysis — hiding what people actually need.
*Changes here:* the test for what goes behind an affordance is *"would the argument survive without
it?"* If no, it is tier one. This makes the split checkable rather than aesthetic, and it is the
criterion the critique pass applies.

**P-24 — Hiding costs discoverability, and the cost is paid by default. [E3]**
NN/g on accordions: collapsing content lowers cognitive load *and* measurably risks the content
being missed entirely.
*Changes here:* every disclosure control needs a visible affordance with a real label — an
information scent strong enough to say what is behind it. **A bare chevron or a plain icon does not
qualify.** Combined with P-28 below, this is the difference between the technique working and the
detail simply never being read.

**P-25 — Hover-only disclosure is not disclosure. [E2/E3]**
It fails touch, fails keyboard, and fails 2.1.1.
*Changes here:* tooltips may *supplement*; they may never be the only route to content. Any
tooltip's content must also be reachable by a focusable, clickable control. This one rules out a
pattern the brief explicitly lists, so it is a genuine narrowing.

**P-26 — The live-presenter answer: available and visible, never required. [E1 + E3]**
*The open question was:* what does the research say about disclosure a presenter has to operate
live?

The literature does not address this case directly — **and that silence is itself the finding**,
recorded here rather than papered over. What exists is two adjacent bodies of evidence pointing the
same way:

- **From P-21 (E1):** the availability of control helped, whether or not it was exercised. The
  affordance does not have to be *used* to pay for itself.
- **From the practitioner literature on click-driven builds (E3):** the harm is specific and
  well-described — a presenter tied to the clicker, tracking what has and has not been revealed,
  breaking delivery to operate the slide, and an audience anticipating the next reveal instead of
  listening. The mechanism is clear enough to act on even without an experiment.

**The rule those two produce:**

> Every disclosure affordance is **available and visible during the talk, and never load-bearing in
> it.** A slide must make its point fully with every panel closed. Opening one may deepen the point;
> it may never complete it.

That is a testable build rule and a critique-pass check: **close everything, and read the deck. If a
slide no longer makes its argument, the split is wrong** — the hidden content was tier one, and
P-23 was violated.

It also resolves the presenter's risk without removing the capability, which the naive answer
("avoid interaction on stage") would have done — and that would have cost this project its
signature technique on no evidence at all.

**P-27 — Disclosure state must not be required to advance. [E3, derived]**
Corollary of P-26 and the segmenting principle: slide navigation and disclosure are independent
axes. Moving to the next slide must never depend on having opened anything, and opening something
must never advance the deck.
*Changes here:* a keyboard-model constraint for T-016 — arrows advance, a separate key toggles, and
the two do not interact.

**P-28 — Signal that something is hidden, at the point it is hidden. [E1 via P-06, E3 via P-24]**
Signalling and discoverability meeting at the same requirement.
*Changes here:* the disclosure affordance is part of the visual language of the theme — a
consistent, tokenised mark meaning *there is more here* — not a per-slide invention. Belongs in
T-014's token set.

---

## 12. Conflicts, named rather than averaged

### 12.1 Richness versus coherence — unresolved, and it is the real one

**Mayer's coherence principle (P-05, E1, 23/23 tests, median d = 0.86)** says inessential material
measurably reduces comprehension. **The brief's Richness decision** says interaction, animation and
3D are wanted, with no JavaScript budget.

These do not reconcile by compromise, and it would be dishonest to average them into "use motion
tastefully".

- The evidence is about *comprehension of instructional material*. A deck that must also persuade,
  hold a room, and not look generated has objectives that experiment did not measure.
- But it is E1 and the effect is large, and this project's own rules say evidence overturns taste.

**Position taken:** motion must be **subordinate to signalling**. Animation that marks structure —
a transition that shows where you are, a reveal that stages an argument, a diagram that animates
its own mechanism — is signalling (P-06) and is supported by the same body of work. Ambient motion
that decorates is what P-05 rules against. So the rule is not "less motion", it is **"motion that
means something"**, and the check is answerable: *what does this animation encode?* If the answer
is "it looks good", it is the case P-05 is about.

**This is a position, not a resolution**, and it is flagged for T-014. It is also the place where a
finding contradicts the brief hardest, which CLAUDE.md asks to be visible rather than quiet.

**It is, however, a position the owner already holds.** [R1 §11](R1-corpus-conventions.md) records
that the corpus's most developed spec defines **exactly four motions and nothing else**, for a
stated reason — a named vocabulary is what stops animation becoming decoration — and that two specs
independently forbid 3D spins and flashy zooms. It also shows the right degradation: under reduced
motion the four collapse to instant states, **but the dashed flow arrows stay dashed, so the meaning
survives when the animation does not.**

That is the same rule arrived at from the other end, and it changes the standing of §12.1
considerably. The conflict is between the *brief's* Richness wording — "no JavaScript budget",
which reads as permission — and the evidence. The owner's own practice is already on the evidence's
side. So T-014's likely job is not to choose between them but to notice that the brief overstated a
freedom the corpus never took, and that "degrade the motion, keep the semantics" is the mechanism
for doing it.

### 12.2 Line length: speed versus preference

Typographic convention says 45–75 characters. Measured reading studies complicate it — longer lines
can be read *faster* while being *preferred less*, and skilled readers tolerate up to ~80 CPL where
novices do best nearer 45.
**Position taken:** optimise for preference, and make it a token. This deck type is read
voluntarily by a reader who can stop, so comfort dominates throughput. `--measure` defaults inside
the conventional range and is one value away from changing.

### 12.3 WCAG 2 versus APCA

A conformance standard that is checkable but perceptually wrong in places, against a perceptual
model that is better but is not a standard. **Position taken:** P-14 and P-15 — conform to AA,
design with APCA, never report APCA as conformance.

### 12.4 Redundancy versus the standalone file

Mayer says on-screen text alongside a speaker costs learning (P-07). The brief requires the file to
be consumable alone. **Position taken:** resolved structurally, not by compromise — §11. The
interaction layer moves the text out of the live channel without removing it from the file. This is
the cleanest outcome in R2 and it is worth noting *why*: the conflict dissolved because the project
had already chosen a mechanism that separates the two audiences in time.

### 12.5 Sans-serif at distance versus R5's font recommendation

P-12 favours sans-serif for projected text. [R5](R5-assets-and-licences.md) recommends Instrument
Serif · Space Grotesk · JetBrains Mono, with a serif in the display role.
**Position taken:** not a conflict once the roles are separated — P-12 governs the *projected*
roles, and a display face at headline size is well above the angular size where serifs fail.
Recorded because it looks like a conflict, and the next session should not spend time re-deriving
that it is not.

---

## 13. Considered and rejected

Listed so they are not re-litigated. Rejection is on the decision test in §1, not on quality.

| Considered | Grade | Why it is not a rule here |
| :--- | :---: | :--- |
| Tufte, *The Cognitive Style of PowerPoint* | E4 | Its actionable content is P-01/P-02, better supported by Alley. The rest is a critique of a tool this plugin does not use, and its central claims are contested with no experiment on either side. |
| "6×6 rule", "one idea per slide", and similar bullet-count limits | E4 | No measurement, and they conflict with each other. P-01 supersedes: the constraint is that the headline is a claim, not that bullets are counted. |
| Mayer: modality, voice, personalisation, embodiment principles | E1 | Genuinely supported, but all concern *narrated* multimedia. This plugin generates a file, not a narration. Would become relevant if speaker-audio were ever in scope. |
| Mayer: pre-training principle | E1 | Real, but it is a content-authoring instruction to the deck's author about their audience, not something the plugin can enforce or check. |
| Slide-count guidance (10/20/30 and similar) | E4 | Prescribes what the corpus already answers with measurement — [R1](R1-corpus-conventions.md) gives the observed range. Measured beats asserted. |
| Data-ink ratio as a maximisation target | E3, contested | Taken literally it strips the signalling P-06 supports. The useful half is already in `dataviz`'s recessive grid/axes rule. |
| Golden-ratio and modular-scale typography systems | E4 | A scale is needed; the specific ratio changes nothing checkable. Left as a token value. |
| Colour psychology (blue = trust, etc.) | E4 | No reliable effect, culture-dependent, and the theme is fixed by decision anyway. |
| Fixed pt minimums for slide type | E4 | Rejected as stated; replaced by P-11. See §6. |
| 2.4.13 Focus Appearance, 2.3.3 Animation from Interactions | E2 | *Not* rejected — adopted above the AA floor as a recorded decision (§9). Listed here so the deviation from "AA is the floor" is not read as an error. |

---

## 14. What this changes, and what T-014 has to settle

**Direct build rules, ready to carry forward.** P-01 and P-02 (headline as claim, evidence below);
the §9 floor as a table of checkable numbers; P-19's off-screen tab-order defect; P-22's two-tier
limit; P-25's ban on hover-only; P-26/P-27's disclosure keyboard model; P-11's distance-relative
type scale.

**Three candidate changes of direction**, in the sense CLAUDE.md means — findings that push against
the brief rather than filling it in:

1. **Progressive disclosure is load-bearing, not a signature flourish.** The brief introduces it as
   the owner's technique and scopes it as T-016. R2 finds it is the *only* structure that lets the
   dual-audience decision survive contact with the redundancy principle (§12.4). That raises its
   priority: it is not a feature of the deck, it is the reason the deck can be two things.
2. **"Richness" needs a defensible test, and R2 proposes one.** §12.1. The brief asserts no
   JavaScript budget and wants animation; the strongest evidence in the field cuts the other way.
   The proposed reconciliation — *motion must encode something* — is a position T-014 should either
   adopt or overrule deliberately.
3. **The check's semantic upgrade.** The brief's "every `<section>` has a heading" becomes "every
   `<section>` has a heading that is a claim" (P-01). That is a real increase in what build mode must
   do, because it constrains the writing and not just the markup — and the brief already decided the
   plugin writes the words.

**Two open items handed on:**

- **The pointer problem (§3.1)** needs no decision — [R4 §7](R4-prior-art.md) already made it. What
  it needs is *applying to the documents*: R2, and the design-system reference T-014 writes, must
  reference other skills by name and carry the rule's consequence inline, since the pointer can
  resolve to nothing without saying so.
- **The two E4 principles (P-09's exact range, P-12's scope)** are defaults with no measurement
  behind them. Both are single token values. Flagged as cheap to overturn if anything better turns
  up — which is the point of grading them.

---

## 15. Sources

Grouped by the section that uses them.

**Narrative and structure (§4)**
- Garner, J., Alley, M., Wolfe, K., Zappe, S., & Sawarynski, L. (2011). *Assertion-Evidence Slides
  Appear to Lead to Better Comprehension and Recall of More Complex Concepts.* ASEE Annual
  Conference & Exposition. DOI 10.18260/1-2--17510 —
  https://peer.asee.org/assertion-evidence-slides-appear-to-lead-to-better-comprehension-and-recall-of-more-complex-concepts.pdf
- Alley, M., et al. — assertion-evidence research programme, Penn State:
  https://writing.engr.psu.edu/research.html and https://writing.engr.psu.edu/ae_comprehension.pdf
- Minto pyramid / SCR / SCQA: https://modelthinkers.com/mental-model/minto-pyramid-scqa

**Cognitive load and signalling (§5)**
- Mayer, R. E., & Fiorella, L. *Principles for Reducing Extraneous Processing in Multimedia
  Learning: Coherence, Signaling, Redundancy, Spatial Contiguity, and Temporal Contiguity.* In *The
  Cambridge Handbook of Multimedia Learning*, ch. 12 —
  https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E
- Summary of the twelve principles: https://www.digitallearninginstitute.com/blog/mayers-principles-multimedia-learning

**Typography (§6)**
- Line length review: https://baymard.com/blog/line-length-readability and
  https://journals.uc.edu/index.php/vl/article/view/5765
- Viewing distance and letter height: https://digitalsignage.com/digital_signage/docs/guides/typography-viewing-distance/
  and https://www.signs.com/blog/signage-101-letter-height-visibility/

**Colour and contrast (§7)**
- W3C WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- APCA rationale and criticism of WCAG 2 contrast:
  https://github.com/Myndex/SAPC-APCA/blob/master/documentation/WhyAPCA.md and
  https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell.html

**Data visualisation (§8)**
- Cleveland, W. S., & McGill, R. (1984). *Graphical Perception: Theory, Experimentation, and
  Application to the Development of Graphical Methods.* JASA. Summary of the encoding ranking:
  https://flowingdata.com/2010/03/20/graphical-perception-learn-the-fundamentals-first/

**Accessibility (§9, §10)**
- W3C, *What's New in WCAG 2.2*: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- W3C, *Understanding SC 2.4.13 Focus Appearance*: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- WebAIM, *Keyboard Accessibility*: https://webaim.org/techniques/keyboard/

**Pacing, control and disclosure (§10, §11)**
- Sage, K., Bonacorsi, N., Izzo, S., & Quirk, A. (2015). *Controlling the slides: Does clicking help
  adults learn?* Computers & Education, 81. DOI 10.1016/j.compedu.2014.10.007
- Nielsen, J. (2006). *Progressive Disclosure.* NN/g: https://www.nngroup.com/articles/progressive-disclosure/
- NN/g, *Accordions on Desktop: When and How to Use*: https://www.nngroup.com/articles/accordions-on-desktop/
- Practitioner literature on click-driven builds: https://24slides.com/presentbetter/bad-powerpoint-examples-you-should-avoid

**Rejected material (§13)**
- Tufte, E. *The Cognitive Style of PowerPoint*, and responses:
  https://files.eric.ed.gov/fulltext/EJ1000695.pdf and https://ubiquity.acm.org/article.cfm?id=1972563

**Installed skills read in full (§3)**
- `artifact-design`, `artifact-diagramming`, `dataviz` — bundled with the runtime; see §3.1 on why
  no path is cited.
