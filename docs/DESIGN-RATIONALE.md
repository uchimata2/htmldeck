# htmldeck — design rationale

**Why the rules are what they are.** Companion to [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md), which
holds the operative ruleset and nothing else.

**No runtime loads this file.** It is for whoever maintains the ruleset, argues with it, or needs to
know whether a rule was measured, inherited, or decided. Entries are keyed by `DS-nnn`.

**Sources.** `R1`–`R7` in [`research/`](research/); corpus rule IDs (`C1`, `F11`) and their verdicts
in [`research/R1-rules-candidate.md`](research/R1-rules-candidate.md); external principles (`P-01`)
with E1–E4 evidence grades in [`research/R2-external-principles.md`](research/R2-external-principles.md);
archetypes and anti-patterns in [`research/R3-exemplar-decks.md`](research/R3-exemplar-decks.md);
provenance in [`research/R4-prior-art.md`](research/R4-prior-art.md).

---

## 1. How a rule got its verdict

154 corpus rules were resolved into this ruleset: **110 keep · 17 amend · 1 drop · 26 defer.**

**The precedence used, and it ran the same way for all 154:**

1. **A standing owner decision** (`BRIEF.md` § *Decisions taken*, or a CLAUDE.md rule) overrides an
   observed habit. **This class is not in the owner's stated tie-break, and it fired four times** —
   DS-011, DS-030, DS-001, DS-002.
2. **An E1/E2 external principle contradicting the habit** — the stated tie-break. **Fired once**, on
   the stage (§3 below).
3. **A named contradiction C-01…C-11** — resolved individually, §2.
4. **Otherwise, keep.** An E3/E4 principle does not outrank a corpus habit, so it was never a
   conflict. This is most of why the keep count is high.

**Keeping 71% of an observed corpus is the expected result.** The tie-break only fires where an
external principle is E1/E2 *and* contradicts a habit, and that combination is rare. No external
principle addresses whether the mono layer carries the domain vocabulary.

**Provenance was context, never a verdict.** No rule was dropped for being inherited. All seven of
the source skill's navigation rules are kept (DS-130–DS-135). What R4's grading bought is knowing
which rules may be cited as the owner's signature — not which to discard.

**The 26 defers are boundary, not indecision:** 11 process rules to T-020, 5 check mechanics to
T-005, 7 critique-format rules to T-004, 4 pipeline rules from group A. Nothing was deferred for want
of an answer.

---

## 2. The conflicts

**Sixteen were found by reading the sources against each other. Thirteen more (F-01 to F-13) were
found by [T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md) building a deck
strictly to the finished ruleset**, and four of those are conflicts between two rules both labelled
`hard` — a compliant deck could not exist. They are recorded on T-024 §3.3 and reconciled in §2.1
below by [T-025](../tasks/T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md).

The generalisation is **L-24**: reading a ruleset tells you whether it is coherent, and building to
it tells you whether it is possible. These sixteen came from reading. Thirteen more were waiting.

> **These conflicts were `X-1`…`X-11` until 2026-08-09.** They were renamed to `C-nn` by
> [T-047](../tasks/T-047-give-the-rationale-conflicts-their-own-id-namespace.md), because
> `DESIGN-SYSTEM.md` §6's twelve **anti-patterns** are also `X-nn` and the two were cited in the
> same sentences, separated only by a leading zero. It had already produced a wrong citation in the
> gate's own output. The conflicts moved rather than the anti-patterns, by the *which side moves*
> test in §3: anti-patterns are cited from five documents and exist to stop the critique pass and
> the standard drifting apart, and these were cited from one. **An `X-n` in a document older than
> that date is a conflict, and `C-0n` is where it went.**

| # | The tension | Resolution |
| :--- | :--- | :--- |
| **C-01** | CDN libraries **vs** self-contained | Self-containment, and it generalises. The icon-sprite pattern is the general principle: embed only what is used. R5 measured a whole deck at 192 KB — no cost argument remains. → DS-001, DS-113 |
| **C-02** | Never hand-draw icons **vs** no external references | Not a conflict. Embedding an icon set's *official* symbols is using the set. → DS-112, DS-113 |
| **C-03** | "No overdose", "no ambient motion" **vs** the brief's rich animation | Resolved by §4 — motion must encode something. The four-motion vocabulary already implements it. *The sharpest conflict in the set, and it dissolved rather than being arbitrated.* → DS-140, DS-150 |
| **C-04** | Canvas effects read as artificial **vs** 3D now wanted | The restraint survives; the suspicion of canvas does not. A particle field that encodes nothing fails in SVG, canvas or WebGL alike. → DS-115, DS-150 |
| **C-05** | "Aim 8, max 10" **vs** "do not exceed 18" **vs** "completeness overwrites the size limitations" | Three rulings, three decks, all the owner's. **Deck length is a per-deck decision, not a house rule** — averaging would invent a rule no deck follows. What holds across all three is kept: single clean message per slide, and nothing is dropped, it is folded. → DS-082, DS-083, DS-084 |
| **C-06** | Stated rules run ahead of the artefacts | **Frequency is evidence of effort, not of intent.** A `stated` rule the corpus under-delivered is still a rule — the specs are the considered position, the decks are what time allowed. Applied: `prefers-reduced-motion` (5/12 in the corpus) is promoted to hard, not weakened. → DS-143 |
| **C-07** | Provenance mark: plain text, no dead links **vs** the owner praising the working link | Both, conditioned on reachability. The underlying rule is *never ship a dead link*; the two decks differ in circumstance, not principle. → DS-105 |
| **C-08** | "No 3D spins" **vs** "Turn: `rotateY` with `preserve-3d`" | Not a conflict. A 3D *transition between slides* is forbidden; a 3D *reveal of a card* is prescribed. Stated precisely so the ban is not read too widely. → DS-144 |
| **C-09** | Icons via CDN **vs** self-containment | As C-01. → DS-113 |
| **C-10** | A word-list check **vs** "text can pass all five and still sound like AI" | Both true. The check is necessary and not sufficient and **must say so** — a clean terminology pass may never be reported as "this reads as human-written". → DS-106, DS-107 |
| **C-11** | `100dvh` flex slides **vs** the fixed scaled stage | **The stage, and the alternative is ruled out rather than dispreferred** — see §3. |
| **R2 §12.1** | Richness **vs** Mayer's coherence principle | Motion must encode something. §4. |
| **R2 §12.2** | Line length: reading speed **vs** preference | Optimise for preference, make it a token. A deck is read voluntarily by a reader who can stop, so comfort dominates throughput. → DS-039 |
| **R2 §12.3** | WCAG 2 **vs** APCA | Conform to AA, design with APCA, never report APCA as conformance. |
| **R2 §12.4** | Redundancy **vs** the standalone file | Dissolved structurally by the disclosure layer, not by compromise. The two audiences are separated in time. → §5 |
| **R2 §12.5** | Sans-serif at distance **vs** R5's serif display face | Not a conflict once roles are separated. P-12 governs *projected* text; a display face at headline size is well above the angular size where serifs fail. Recorded so it is not re-derived. |

### 2.1 The thirteen the build found — F-01 to F-13, and how each was closed

**The shape of the set is the result, not any single row.** Four conflicts between two `hard` rules,
three rules that could not be built as written, two silences with a computable answer, one check that
was impossible as specified, two measurement traps, and one loop rule that could not coexist with its
own cost control. **Roughly one finding per ten rules, and none of them cosmetic** — which is the
argument that a design system has to be built against before it can be trusted.

**Where a conflict is resolved, the resolution names which rule yields, and that ruling is now in the
rule text itself.** A conflict resolved only here is a conflict a builder will hit again, because
nothing loads this file at runtime.

| # | Rules | Class | Resolution, and why |
| :-- | :--- | :--- | :--- |
| **F-01** | DS-035 × DS-036 | conflict | **DS-035 yields — the number, not the principle.** The floor moved from 18 to 16 on the owner's amendment (§3 below), which makes DS-036's mono range reachable. A floor that forbids the range another rule prescribes is the floor that is wrong: DS-036's band was derived from a role (marginalia, never load-bearing), DS-035's 18 was derived from arithmetic about a different role. Settled by [T-027](../tasks/T-027-specify-the-slide-deliverable-and-the-outline-contract.md) before T-025 opened. |
| **F-02** | DS-033 | unbuildable | **Rule clarified: the ban is on *bare* `px`.** "No `px` inside the stage" cannot hold literally — every CSS length resolves to an absolute unit, so a design unit has to be declared as one somewhere. The rule's real content is that `vw`, `vh` and `clamp()` fight the transform and bare `px` bypasses the scale; declaring `--du` once and deriving every size from it does neither. **The rule was right about the failure and wrong about the mechanism**, which is the failure mode of a rule written from a symptom. |
| **F-03** | DS-140 × §7 2.2.2 | silence | **New rule, DS-218** — owner's decision, 2026-08-06. `Current` is infinite, so DS-140 mandates the exact motion 2.2.2 requires a control for, and nothing required the deck to build one. The alternative — leaving it to §7, where the criterion already sits — was rejected because **the reference deck only got a control because the build happened to notice**, and a floor that reaches the builder as a criterion rather than an instruction produces non-conformant decks by default. A rule ID also gives the build check something to test by number, which §7's criterion rows do not offer. |
| **F-04** | DS-140 × DS-141 | conflict | **DS-141 yields, by scope.** Its 500 ms cap now governs entry and transition only, with DS-140's named vocabulary as the specific override. DS-141 was written about the class of animation that makes a deck feel slow; Pulse-once and Current are neither. **The general rule yields to the specific one, and the text now says so** rather than leaving each builder to infer it — which is what T-024 had to do. |
| **F-05** | DS-146 × DS-140 | conflict | **DS-146 says how, and it now says why on its own.** The draw-in is Rise applied to the chart's marks, staggered. The tempting fix — a stroke-dash draw — was rejected because it would be a fifth motion in a vocabulary closed at four. *That resolution died with the closure on 2026-08-21 ([T-187](../tasks/T-187-open-the-motion-vocabulary-into-a-style-guide.md)), and the conflict it settled did not: **this is no longer a conflict at all.** DS-140 admits a motion that passes its test, so nothing stops DS-146 reaching for a new one — and DS-146 still refuses the dash, on **DS-243**: a line drawing itself makes the reader watch the drawing rather than read the shape, which is a figure designed around its own animation. The outcome is identical and the reason is the rule's own, which is what the closure was standing in for here as everywhere.* |
| **F-06** | DS-168 × DS-071 | silence | **DS-168 amended with the design-unit floor: ≥ 48.** The number was always computable and never stated. `scale = min(vw/1920, vh/1080)`, and DS-071 hands over to the reflow view below 960 CSS px, so the stage bottoms out at scale 0.5 and a design unit is worth half a CSS pixel at the smallest size the stage is ever shown. 24 CSS px therefore needs 48 design units. **The unstated consequence is the trap: a builder reading "24" inside a stage measured in design units will write 24, match the number and fail the criterion.** The reference deck used 52. *Caveat, closed 2026-08-07: the 0.5 floor assumed width binds, and a short, wide viewport scales lower. **DS-071 now keys off the scale factor itself**, so 0.5 is the floor by construction rather than by assumption. DS-071 is still `default` — a deck that moves the reflow threshold still moves this floor with it.* |
| **F-07** | DS-117 | unbuildable | **Rule split: labels are universal, arrowheads are conditional.** The rule assumed every diagram is a directed flow, which is true of A-08 and false of a network graph. An arrowhead is not decoration — it asserts a direction — so applying the rule literally to an undirected edge makes the diagram *say something untrue* in order to satisfy a rule about tidiness. **The label half was right for every diagram; only the arrowhead half was over-generalised.** |
| **F-08** | DS-063 | check impossible | **Tolerance stated, and measured rather than guessed:** a non-text box's rect ≤ 0.25 du, a text run's rect ≤ 2 du. A check demanding exact equality fails every deck containing text — **the rule was unfalsifiable, which is worse than lax.** The two tolerances differ because the mechanisms differ: box geometry rounds once, a text run accumulates rounding per glyph, so the text figure carries headroom for runs longer than this deck's. **Corrected 2026-08-07 by [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md), and the correction is the interesting part** — see *What the first tolerance measurement did not measure*, below. |
| **F-09** | DS-013 | silence | **Token list extended with a data-series role and a UI-line role.** With neither present the natural move is to reuse `--line` for chart marks, and a hairline token is tuned for a hairline's job — the reference deck's landed at **1.79:1** against the ground, failing 1.4.11's 3:1 for meaningful graphics. **The token list is where a role either exists or gets improvised**, and an improvised role inherits the contrast obligation of whatever it was borrowed from. |
| **F-10** | §7 1.4.3 × 1.4.11 | conflict | **New rule, DS-219: text never goes on a data mark.** To clear 3:1 against the ground a neutral mark must be dark; to carry 4.5:1 text it must be light; no neutral is both. This is **not resolvable by picking a better grey** — it is arithmetic on the accessibility floor, and it rules out the value-inside-the-bar chart for neutral series generally. Recorded as a rule because it is a general consequence, and a builder meeting it slide-side will otherwise try to tune their way out of it. |
| **F-11** | DS-138 | unbuildable | **DS-138 extended to constrain the control, not only the panel.** "Panels drop below" is geometrically unsatisfiable when the control sits near the foot of a 1080-unit stage and the panel is more than a row or two — the panel has nowhere to go. **A rule that fixes one end of a relationship silently constrains the other**, and stating only the visible end leaves the builder to discover the invisible one by failing. |
| **F-12** | DS-190/DS-191 | measurement | **Two new rules, DS-220 and DS-221**, siblings of DS-190/191 because both are claims about what a check may assert. (a) Content taller than a `1fr` track is clamped by the track, so the box measures exactly right and the spill is invisible — `scrollHeight` vs `clientHeight` is the only view of it. (b) An infinite `Current` means a headless render never quiesces, so the screenshot fires mid-transition and **produces a convincing blank slide** — a false negative that looks like a result. Both were hit, not predicted. **DS-191 demonstrated on DS-191's own tooling.** |
| **F-13** | EVALUATION §6.2 × §6.4 | conflict | **The cap governs measurement rounds, not fixes.** One fix per iteration under a cap of 3 permits three fixes; the reference deck needed **23** before clearing its own gate, so the loop would have reported CAP with twenty defects outstanding — off by an order of magnitude. Run as two measurement rounds with fixes batched inside each, it reached PASS. The one-at-a-time discipline is **kept and scoped** to fixes that interact, which is the case it was written for: attribution only matters where a fix can move a score it was not aimed at. This also closes EVALUATION §8's *"is the cap 2 or 3?"* with evidence rather than reasoning — **2 rounds sufficed for a first-draft 12-slide deck.** |

**One row is not a finding but belongs with them: DS-102 and the illustrative deck.** "Every figure
sourced" cannot be met by a deck about a place that does not exist, and the plugin's own example deck
is exactly that case. T-024 resolved it in the build — the model is the source, said so on the deck —
and the rule now carries the provision. **The point is which alternative it forecloses:** a builder
who cannot satisfy DS-102 honestly will reach for real research quoted from memory, and a
misremembered elasticity is a fabricated metric wearing a citation. The rule is stricter with the
provision than without it.

### 2.2 The two real use found — U-01 and U-02, and neither is resolved

**A third provenance, and it is the one the other two cannot reach.** §2's sixteen came from reading
the corpus and §2.1's thirteen from building a deck against the ruleset. These two came from an
**adopting project presenting a finished deck to its owner** — from a reader saying the deck did not
serve them, on a build where every gate was green. Kept in their own subsection because the column
above is *Resolution* and these have none: they are recorded so the next person to open DS-092 or
DS-105 sees that the rule has a known cost, not so that a ruling can be inferred from the entry.

| # | The tension | State |
| :--- | :--- | :--- |
| **U-01** | DS-105 forbids a dead link in a shipped deck, and a `file://` link cannot be shown to be live **vs** a source line a reader can open | **Open.** A deck whose sources sit beside it on disk has no conformant way to reach them, so the mark degrades to a slug — `D5 §2` — which names a document the reader cannot identify or open. The rule is right about dead links; what it has no answer for is a live one it cannot verify. Owned by [T-070](../tasks/T-070-the-quick-view-for-a-source-document.md), whose overlay is the other way to satisfy the same need. |
| **U-02** | DS-092's four-sentence, twenty-word bound on the provenance mark **vs** a source line that says what each document *is* | **Open.** The mark is one `<p>`, so its items are counted together: give each source a full stop and the paragraph exceeds four sentences; leave them without one and they concatenate into a single sentence over twenty words. **Five sources cannot carry titles either way**, and the bound was written for a mark carrying one. Owned by nobody yet; it arrives with [T-092](../tasks/T-092-product-feedback-from-the-first-external-deck.md). |

**Both were hit weeks before they were reported**, and by the same project, which had written each
one into its own build log as a local deviation and moved on. That is the finding underneath the two
findings — see **L-66** in [`LESSONS.md`](LESSONS.md).

---

## 3. The stage — DS-060 to DS-065, and the numbers behind them

**The owner's reason is not the one the corpus recorded, and the difference reshaped the ruleset.**

The corpus rationale was *"what was rehearsed is what appears"* — a rehearsal guarantee, which reads
as presenter convenience. Weighed as convenience it **lost** to two WCAG criteria, and T-014
escalated it. **The actual reason is two observed failures:**

1. A deck built for small screens **breaks when opened on a 4K display** — breakpoints land in a
   bucket nobody designed, `max-width` containers leave dead gutters, absolute positioning drifts.
2. A deck presented from a high-resolution monitor **arrives illegible**, because a video call
   re-encodes the shared screen at 1080p or 720p and the text goes down with the frame.

### Why no responsive layout can solve the second

Text in the received stream measures:

```
stream_px  =  S  ×  (viewport_h / 1080)  ×  (F / viewport_h)
           =  S  ×  (F / 1080)
```

`S` = design-unit size, `F` = the call's frame height. **The presenter's viewport cancels.**

**Under a uniformly scaled stage, what the audience can read depends only on the design size and the
call's resolution — never on the machine it is presented from.** A responsive layout renders
different text fractions on different presenter monitors, so its legibility over a call is a
function of whichever machine is used. That is failure 2, exactly.

**This is why "drop the stage for flex slides" is ruled out rather than merely dispreferred**, and
why DS-061 forbids media queries inside the stage.

### The type floor, computed — DS-034, DS-035, DS-036

| Role | Design units | Share of frame | at 1080p | at 720p | at 540p |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Display | 67 | 6.2% | 67 px | 45 px | 33 px |
| Subhead | 34 | 3.1% | 34 px | 23 px | 17 px |
| **Body — the floor** | **24** | **2.2%** | **24 px** | **16 px** | 12 px |
| Below the floor | 18 | 1.7% | 18 px | 12 px | 9 px ✗ |
| Mono label (corpus value) | 16 | 1.5% | 16 px | **11 px ✗** | 8 px ✗ |

**720p is the binding case.** It sets body at 24 design units, **tightens the corpus's D5 range of
18–24 to 24–28** — its lower half does not survive a screen share — and **demotes the corpus's 11–13
unit mono labels to decoration** (DS-036), because they were never legible to a remote audience.

Neither number was derivable before the reason was stated. Generalised as **L-22**.

> **DS-035 amended from 18 to 16 design units by the owner, 2026-08-06**, after reviewing the
> reference deck: *"If it's min 18 now, I would accept a 16 too."*
>
> This also **settles F-01**, which was a conflict between two `hard` rules: DS-035's floor of 18
> made the 16–17 half of DS-036's mono range unreachable, so a compliant deck could not use the
> range the ruleset told it to use. The floor stays a floor; the number moved, and DS-036 became
> satisfiable.
>
> **What the table above still says, and the amendment does not overturn.** 16 design units is
> **11 px in a 720p screen share** — the row marked ✗. So the amendment widens what is *permitted*,
> not what is *readable at distance*: DS-036 already confines that band to marginalia that is never
> load-bearing, and DS-034 keeps body type at 24–28. **A deck that puts anything the audience must
> read at 16 units has obeyed DS-035 and failed the audience**, which is the distinction between a
> floor and a target.

### Where the deliverable rules came from — DS-201 to DS-213

**T-014 synthesised the corpus into 131 rules and dropped the one the owner cared about most.** The
design system could describe how a slide should look, argue, move and disclose, and had **nothing
about what a slide owes its audience**. The owner named it after reading the reference deck:

> *Each slide needs to deliver something. The key deliverable should not be hidden in a list or
> prose… So they don't need to wait for the presenter to finally say the essence.*

**This was recorded taste, not new taste.** The corpus carries it in three independent places, and
the synthesis passed over all three:

| Source | What it says |
| :--- | :--- |
| The build process for two separate decks | Each slide is specified by structure, text, visuals, animations, interactive elements, title **and bottom line**. The bottom line is a named, required per-slide element. |
| Owner feedback on a deck | *"Bottom line repeats content. Keep only the key message here, no reasoning."* — so the bottom line is the **deliverable**, not a summary. DS-202. |
| Owner feedback on another deck | *"Show the details here, do not hide them under the click."* — disclosure is for depth; the point does not live behind it. DS-205, DS-206. |

**Why the miss happened, and it is worth naming.** The synthesis read the corpus for *conventions* —
things stated as rules — and the bottom line appears in the corpus as a **field in a template** and
as **feedback on a specific slide**. Neither reads like a rule. **A convention that only ever appears
as a column heading is the easiest kind to lose**, and losing this one cost the ruleset its most
important rule until a human looked at a deck built from it.

### Idiom is not jargon — DS-208 beside DS-097

DS-097 already said *the reader is bright and new to the field; anything the author would look up is
a defect.* That is about **jargon**, and it has a remedy: the reader looks the term up.

**Idiom has no such remedy, because it does not announce itself.** A non-native reader who meets a
figurative phrasal verb or a sporting metaphor does not know a lookup is needed — the words are all
ordinary, and the sentence reads as literal and wrong. The corpus writing standard states the
constraint the owner restated: *plain, simple English… the reader may not be a native speaker and no
sentence should need a second pass.* Hence a separate rule with a separate check.

### Three encodings of one fact — DS-216, DS-217

The reference deck showed a spine ribbon, twelve dots and a progress bar: **23 labelled or
interactive items in 96 design units**, all answering *where am I*. Every one of them was individually
sanctioned — DS-131 asks for dots, DS-133 for a progress indicator, DS-134 for the spine ribbon —
and **nothing forbade showing all three at once.** The owner's verdict was *"extremely noisy."*

This is a composition failure rather than a rule failure, and it generalises: **a ruleset assembled
from individually-good requirements can specify a bad whole.** Rules that each permit an element say
nothing about how many such elements a frame can carry, which is why DS-217 states a budget rather
than another permission.

### Which side moved — DS-131 against DS-216 and DS-217

Adding the budget left a rule conflict behind it. DS-131 required *"clickable dots"*; DS-216 counts a
dot per slide among the three encodings of position it forbids stacking, and DS-217 says to prefer a
compact indicator plus click-to-jump over one target per slide. Obeying the two new rules in
[T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) meant deleting the
twelve dots, which left the ruleset's own worked example departing from DS-131. All three are
`default`, so the departure was legitimate; a flagship example that silently contradicts a rule is
not.

**DS-131 is the side that moved, and the reason generalises: it was the only one of the three that
named a widget rather than a requirement.** What the reader needs is a way to reach a part of the
deck without stepping through it. Dots are one way to spend that; the stage names are another and
cheaper — seven labelled targets already on screen, against twelve unlabelled ones that were not.
Rewording DS-131 to *a bounded set of named targets* keeps the requirement and drops only the
mandated implementation, and nothing in DS-216 or DS-217 had to weaken. **A rule that specifies the
element instead of the need is the one that will collide with the next composition rule**, because
composition rules are written about elements.

The rewording also states a limit the owner's ruling did not cover. *Per-stage* is the right target
set while stages are even and short enough that landing on one lands near what the reader wanted. A
jump into a nine-slide stage is barely a jump, and there the answer is an on-demand slide index —
a component rather than a chrome element, so it costs nothing against DS-217's budget until it is
asked for. Naming that limit in the rule is cheaper than leaving the next deck to discover it.

### Which side moved, second time — the ruler, and why four rules bent rather than one

[T-035](../tasks/T-035-the-ruler-navigator.md) replaced the stage-name ribbon with a ruler, and the
ribbon's problem was structural rather than aesthetic: **its footprint depended on how the stages
were named.** Measured, seven names cost 856 design units in a 1180-unit box, with the six flexible
connectors already compressed to absorb 69.5 units the row did not have. It rendered cleanly and had
nothing left to give — one more stage, or one longer name, and it wrapped into the second row DS-217
exists to prevent. Tick marks have a fixed width, so the element stops depending on the words.

Four rules had to move, and **the shape of each amendment is the point: three narrowed the rule's
*mechanism* while keeping its *intent*, and the fourth widened a test and paid for it with a cap.**

- **DS-217 counts a scale as one item.** The budget counts items because items make a frame noisy,
  and a tick array is one perceived object. The metric was wrong for the shape, not the intent —
  so the counting changed and the number did not. Raising 12 to 24 would have destroyed the budget
  for everything else to admit one component.
- **DS-217's slide bound became a measurement.** *"Somewhere around ten"* was a guess the shipping
  twelve-slide deck already contradicted, which is the worst state for a rule: contradicted by the
  artifact it governs, and by an amount nobody had checked.
- **DS-131 narrowed by one word — *unnamed*.** T-033 had already established that *named* was
  load-bearing; the amendment simply attached the prohibition to the right half of the phrase.
- **DS-216 widened, from *different fact* to *different fact or register*.** This is the one that
  did not narrow, and it is the one that needed a brake.

**The brake is worth stating on its own, because it is a reusable move.** A widened test invites
claimants the old test excluded: *register* is easy to assert, and a progress bar reads as
"approximate position" as readily as a ruler does. So the widening ships with a **hard cap of two
elements, however well a third is argued** — the cap does the work the old test used to, and it is
countable where the test was arguable. **When a rule's test is loosened, replace the rigour
somewhere it can still be counted**, or the loosening is unbounded in practice however narrow it
looked on paper. The seeded-defect suite carries the proof: a progress bar beside the ruler and the
counter is caught as a third encoding, which is the cap being enforced rather than merely written.

The same discipline applies to the scale exemption. **`data-scale` is verified, not trusted** —
uniform mark, uniform pitch, no per-item label at rest — because an unverified exemption is a
loophole any evenly-spaced row of controls could claim. In practice it defends itself: when a
variant stuffs the row with extra buttons, the ticks compress unevenly, the pitch stops being
uniform, and the exemption withdraws itself before the budget is breached.

### What the first tolerance measurement did not measure

DS-063 states two tolerances. When [T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md)
turned it into a gate on 2026-08-07, **the stricter of the two turned out to have a number and no
coverage**: the probe behind the original 384 values carried nine keys — headline, standfirst, body,
eyebrow, disclosure label, mono label and three SVG label roles — and **every one of them is a text
run**. Not one non-text box had ever been compared. F-08's *"positions agreed to 0.09 du"* was the
worst placement disagreement **among text elements**, recorded under a heading that says non-text.

Two corrections came out of measuring it properly, over the full 12-slide deck:

| | Values | Worst disagreement |
| :--- | ---: | ---: |
| Non-text boxes — figure, disclosure container, control, grid row *(newly measured)* | 116 | **0.000 du** |
| Text runs, whole rect | 336 | 1.170 du — `svgName / w` |

1. **Layout boxes agree exactly.** Zero, across a scale ratio of 3.15. The 0.25 du allowance is
   generous rather than tight, and for the first time something is actually inside it.
2. **The split is by element kind, not by axis.** The rule said *text-run widths*, which reads as
   though only the width is glyph-derived. It is not: a text run's `y` disagreed by up to 0.62 du
   and its height by 0.42. A gate that held a text run's placement to the non-text tolerance failed
   the reference deck on 27 of 336 values while its layout was provably identical — a false
   positive on a `hard` rule, which is the expensive kind.

**Which run these figures come from, since two sets are in circulation.** 116 non-text and 336 text
values are a sweep of **all twelve slides**. `contract.py`'s default samples **four** — slides 1, 5,
8 and 12, spanning the archetypes — and reports 40 and 84, which is what a routine
`check.py` run prints and what `examples/README.md` quotes. Neither figure contradicts the other;
they are different sample sizes, and the smaller one is a stated compromise rather than a
disagreement.

**The generalisable part is neither number.** A tolerance was stated, sourced, and cited for a
category the instrument could not see, and it survived review and a full ruleset split. That is
**DS-191** arriving from underneath: a measurement confirms geometry you suspect, and it says
nothing whatever about the geometry you never put in the probe. Recorded as **L-36**.

### Viewer scale — why scale 0.5 is the reflow threshold, and 960 CSS px is only its usual face

`scale = min(vw/1920, vh/1080)`:

| Viewer | CSS viewport | Scale | Body renders at |
| :--- | :--- | ---: | ---: |
| 4K monitor, 100% OS scaling | 3840 × 2000 | 1.85 | 44 px |
| FullHD laptop, 100% | 1920 × 950 | 0.88 | 21 px |
| FullHD laptop, 125% | 1536 × 760 | 0.70 | 17 px |
| FullHD laptop, 150% | 1280 × 634 | 0.59 | 14 px |
| Short and wide — a half-height window | 1280 × 400 | 0.37 | **8.9 px** |
| 16:9 or taller, below 960 CSS px wide | — | < 0.5 | reflow engages |

**Every laptop case stays on the stage and stays readable**, which is the requirement.

**The threshold is the scale, not the width** — amended 2026-08-07 by the owner via
[T-021](../tasks/T-021-the-reflow-view-and-the-resolution-contract.md). 12 CSS px of body text is
what the rule is protecting, and 24 design units reach it at scale 0.5; 960 px of width reaches
scale 0.5 **only when height does not bind**. The short-and-wide row is the case a width test misses
and it is not exotic — it is a browser window dragged short. The caveat under **F-06** had already
named it in one line; keying DS-071 off the scale factor is what removes it, and with it DS-168's
≥ 48-design-unit floor stops being an assumption about which dimension binds.

**Why 1920×1080 design units rather than the corpus's 1600×900:** purely a change of units — both
16:9, both scale, nothing renders differently. It buys **one design unit = one pixel in a 1080p
stream**, making every size directly checkable against what an audience receives.

### The accessibility trade, and how it was resolved

**1.4.4 Resize Text** and **1.4.10 Reflow** are both AA, and a scale-to-fit stage defeats both —
zooming rescales the stage instead of enlarging the text. **This is the one place the owner's
tie-break fired.** Settled by adding the reflow view (DS-070–DS-076) as a conforming alternate
version — the same shape as the printing decision.

**Ruled out and recorded so neither is revisited casually:** dropping the stage (re-introduces the
defect above), and claiming bare AA while shipping a scaled stage (a silent omission).

---

## 4. Motion — DS-140, DS-150, DS-243

**Adopted: motion must encode something.** The brief's *Richness* decision says "no JavaScript
budget" and reads as permission. Mayer's coherence principle is the best-supported result R2 found —
23 of 23 tests, median effect size 0.86 — and it cuts against decorative motion.

**The conflict is narrower than it looks.** The owner's own practice is already on the evidence's
side: the corpus's most developed spec defines exactly four motions and nothing else, for the stated
reason that a named vocabulary is what stops animation becoming decoration, and two specs
independently forbid 3D spins. **The conflict is between the brief's wording and a practice that
never took that permission.** No re-scope requested; a wording change proposed in `BRIEF.md`.

**Amended 2026-08-21 — the closure went, the position did not.** The owner ruled that any animation
aligned with the rules is admissible and the four names are a suggestion
([T-187](../tasks/T-187-open-the-motion-vocabulary-into-a-style-guide.md)), which overturns the
sentence this section leaned on: *a named vocabulary is what stops animation becoming decoration.*
**That sentence was a proxy, and it is worth saying what for.** A name tested nothing — it recorded
that a motion had once been considered, and the four were the corpus's four rather than anything
derived. It worked because the corpus's author had already done the thinking; it would not have
worked for a motion they never met, and a list cannot by construction.

**What replaces it is DS-243** — *the page is not designed around its own animation* — which is the
claim the closure was making indirectly. Mayer's coherence result is untouched and still the
best-supported thing R2 found; **it argues against decoration, and it never argued for a list.** The
adopted position is therefore unchanged in substance and better grounded: decorative motion is
rejected by DS-150 (does it encode anything?) and animation-led design by DS-243 (what shaped the
page?), and both reach a motion nobody has named. The five remaining principles the owner stated are
[`MOTION-GUIDE.md`](MOTION-GUIDE.md), which is guidance and gates nothing.

---

## 5. Progressive disclosure — DS-160 to DS-170

**Load-bearing, not a signature flourish.** R2 §12.4 finds it is the *only* structure that lets the
dual-audience decision survive the redundancy principle. R3 §8 reaches the same place from the
catalogue's shape: every archetype has a tier-one/tier-two form, and A-13 is what that means in
practice — so it belongs *across* the catalogue, not *beside* it.

**Two independent routes to one conclusion is the strongest signal in the research.** It is why the
catalogue is thirteen archetypes plus one modifier rather than fourteen archetypes, and why the
build must decide a tier split for **every** slide.

**The density trap is the failure mode this project is most exposed to.** The lone-reader half of
the *Use case* decision tempts every slide to carry everything. Meeker's Internet Trends is that
carried to its conclusion — genuinely authoritative, and a punishing read, because every slide pays
the full density cost whether or not the reader needs that slide. **X-06 is therefore a check, not
an observation: if the deck reads acceptably only because the reader is assumed to be diligent, the
split is wrong.**

---

> **There is no §5.1–§5.4, and there never was.** §5.5 to §5.7 were numbered that way so later
> sections could be added without renumbering §6 onward, which is cheap; the cost is that the
> sequence reads as four missing sections. **Stated rather than renumbered** (2026-08-09): §5.5 is
> cited from four task files, and a rename would break those pointers to fix an appearance — which
> is precisely the class of defect [T-042](../tasks/T-042-audit-the-whole-repository-against-itself.md)
> exists to remove.

## 5.5 The `Reach` column — why a rule carries this on its own row

**A rule's `Check` value says how it would be tested; it never said whether it can be.** Those are
different facts and the ruleset recorded only the first, so a rule labelled `auto` that no program
can decide was indistinguishable from one nobody had built yet. `Reach` records the second, per rule.

**It is a column and not a section because the section was tried and it failed silently.** The
original design was a check-facing list — the hard rules restated as numbered testable conditions,
naming the two no check could reach. It was recorded as delivered and **was never written**;
`DESIGN-SYSTEM.md` has ended at §9 in every commit of its life. Four tasks reasoned about the list's
contents for two months, one of them ordering part of the build on it, and the file was never
opened. The mechanism is **L-39**: a review verdict that cites an address rather than content
survives the content not existing, and `task.py check` validates links and paths, so a `§11` in
prose is invisible to it.

The general form is the part worth keeping: **a parallel structure can go absent without anything
breaking**, because everything else works off the originals. A fact carried on the rule's own row
cannot — the row would have to go missing too.

**Conditions 22 and 30 are written off, not lost.** The numbered list named two conditions as not
machine-checkable, and which rules they were is **unrecoverable**. The numbering was not the hard
rules in document order: the one condition anyone ever translated by hand, *condition 17* → DS-063,
puts DS-063 **31st** in that order. Nothing in the repository preserves the sequence, so the two are
recorded here as gone rather than left as a search for the next reader to re-run and abandon. Their
content is not lost with them — every rule now carries its own `Reach` value, which is what those
two conditions were trying to say about themselves.

**`Reach` stays separate from `Check` rather than becoming a fourth value of it.** `auto` with
`never` is a coherent pair — a rule a program could test in principle, on an input no program can
produce — and one column cannot hold both halves without losing it. The same argument decides the
null: every `judge` rule reads `—`, meaning *outside the gate's jurisdiction*, which is not the same
claim as `never` and must not be read as one. `judge` rules are decided by the evaluator, and
`Reach` says nothing about whether it can do so.

---

## 5.6 DS-227 and DS-228 — two rules the gate had been enforcing without them

**Both were added because a check already existed for them and cited someone else's rule.** That is
normally the wrong reason to write a rule, and the distinction is worth keeping because it will come
up again: **inventing a rule so a check has somewhere to live is backwards; writing down a rule the
system already depends on is not.** The test is whether anything breaks if the rule is deleted and
the check with it.

**DS-227 — closed at load.** Two rules lean on it. DS-161 asks whether the slide still makes its
point with everything closed, which is a question about the state the reader *arrives in*; if a panel
could be open at load, the question is about a state nobody sees. DS-073 requires the reflow view to
render every panel open and inlined, and that is a **contrast** — a document rendering does not hide
content behind an affordance, unlike the stage. Neither rule states the stage's side of it. Reading
it out of DS-073 by negation was considered and rejected: DS-073 governs a different rendering, so
the obligation would be derivable only by a reader who notices the inversion, which is the class of
unstated dependency the whole of [T-038](../tasks/T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md)
is about.

**DS-228 — one panel open at a time.** DS-137 requires that two simultaneous interactions have a
**defined precedence rule**; it does not define one, and it cannot, because it is a claim about every
interaction pair a deck might have. *One panel at a time* is the definition for the one pair every
deck in this system has. The two are different claims and a gate citing DS-137 for the measurement
was asserting the general from the particular — the reason DS-137 stays `judge` and un-gated while
DS-228 is checked.

**Why DS-228 is `default` and DS-227 is `hard`.** A panel open at load has no coherent design behind
it; it breaks the two rules above and there is nothing to argue. Two panels open together does have
one — a slide comparing two things, each with its own detail — so it is a departure DS-000 permits
with a stated reason, and DS-169 already treats more than one meaningful interaction on a slide as
exactly that. The labels record which of the two has a defensible other side.

**What this cost the coverage account.** Two rules with `Reach: yes` and a `Check` in {`auto`,
`render`} were added, so the number [T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md)
must account for moved from **105 to 107** on 2026-08-09 — derived from the ruleset, as that task
requires, and re-derivable rather than to be trusted from this line.

---

## 5.7 DS-045 and DS-219 — two rules that said more than they meant

**Both were found by building their checks, and neither was found by reading them.**
[T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md) wrote a check for each, ran it
against the reference deck, and got a failure that was not a defect — which is the signal that the
rule and its reason have come apart. Both were settled the same way: **the reason is the rule, and
the wording moves to match it.**

**DS-045 — the harm is the leak, not the element.** *Never style a bare `<b>` inside a component*
admits two readings. Under the wide one — any descendant `b` selector — the reference deck breaks it
four times, in a pattern [T-027](../tasks/T-027-specify-the-slide-deliverable-and-the-outline-contract.md)
and [T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) adopted across
twelve slides and that the gate's own DS-203 check depends on. The narrow one bans `b { … }` and
leaves `.bottom-line b` alone. **The narrow reading is the one that matches the harm the rule
describes:** a rule on the element itself reaches every `<b>` in the file, so a component's styling
becomes a default nothing declared, and the next `<b>` written for emphasis inside that component is
indistinguishable from the deliverable. A scoped selector cannot leak — the scope is the fix. The
wide reading would have cost every generated deck a class on every emphasis span and bought no
reader anything.

**DS-219 — the prohibition outran its own argument.** The rule says *never*, and the reason it gives
is that **no neutral** clears 3:1 against the ground and carries 4.5:1 text at the same time. That is
true and it is about neutrals. The reference deck sets three values inside **accent** bars, and the
accent clears both — `contrast.py` has been measuring that exact pair, *ground text on an accent
fill*, and passing it, on every run since the module existed. So the rule forbade something its own
mechanism permits, and the rule's last sentence rules out reading it as taste: *a consequence of the
accessibility floor, not a stylistic preference.*

The amendment makes the floor's requirement explicit and hands it to the gate: a labelled mark owes
**two** measurements rather than an exemption. **That is what stops the clause becoming a loophole**
— *the accent is fine* is an assumption, and `mark ≥ 3:1 against the ground, text ≥ 4.5:1 against the
mark` is a number. The check is stricter than the old blanket ban in one direction that matters: it
also catches a mark that is too *pale* to clear the ground, which *never set text on a mark* never
looked at because it assumed nobody would try.

**Both rules gained coverage by being corrected.** They were the last two of T-005's 31 written-off
rules that were written off for a reason other than *this needs a reading of the content*, and
closing them took the gate to 78 of the 111 rules owned at the time.

**DS-036 is the third, found the same way one layer up** —
[T-052](../tasks/T-052-two-hard-judge-failures-in-the-reference-deck.md), 2026-08-09, from the
hard-judge checklist's first run rather than from a mechanical check. *Mono labels 16–18 units …
**and never load-bearing***, read across the whole range, fails the reference deck everywhere the
mono role does its job: the ledger's row headers, the figure annotation reading `44% OF THE TRIP`,
and the legend.

**The legend is what settles it, because DS-026 requires one.** *Semantic roles fixed deck-wide …
**with a visible legend*** is `hard`. If mono at 18 may not carry meaning, the legend cannot be
mono; if the legend may not be mono it has to be body type, at which point the decoder for the
colour semantics is typographically indistinguishable from the content it decodes. **Two `hard`
rules binding against each other is the *"a compliant deck could not exist"* class from §2.1**, and
it is settled the same way: by the reason, not by the wording.

**The reason is in the rule's own second sentence.** *The 16–17 band is reserved for marginalia*
already names the band the load-bearing ban is about — marginalia is what may not carry the
argument. **18 is the label role**, and a label that carries no meaning is not a label. So the
amendment binds *never load-bearing* to 16–17 and lets 18 do what the deck has always used it for.

**The deck did not move, and that was the closer call of the two.** Changing it means taking the
row headers and the legend out of mono, which reshapes the archetype
[T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md) validated the whole
ruleset against, forces DS-035 and DS-063 to be re-measured, and solves a wording problem with a
design change. **DS-208 went the other way in the same task** — *Frequency has no ribbon* became
*The general fund carries this* — because there the rule's reason was intact and only the deck
breached it: a reader who takes "ribbon" literally gets nothing, and the slide loses only the joke.
**Two rules failed together and moved in opposite directions**, which is the point of asking which
side the reason is on rather than which side is cheaper.

---

## 5.8 The `hard` `judge` rules — gated, not demoted

`EVALUATION.md` §1 declares every `hard` rule a gate. Eighty-five are `auto` or `render` and the
mechanical gate owns them; four have `Check: —` and bind whoever builds a check rather than the deck.
**The remaining twenty-five were `judge`, and until 2026-08-09 nothing produced a verdict for any of
them** — twenty-four after DS-107 moved to `Check: —`, below — eleven were not named anywhere in `EVALUATION.md`, four of those being §3.4's deliverable
contract, the section this document's §3 records as the one the owner named after reading the deck.

**The choice was between gating them by judgement and dropping the word *gate*.** They are not the
same size of change, and the smaller-looking one is the one that loses something.

**Why not demote them into the dimensions.** The dimensions score 0–4, and §1 forbids scoring a
`hard` rule. So letting S1 or S4 carry DS-201, DS-204, DS-207 and DS-208 converts each from a
**defect** into *a point off a score* — a deck could bury its deliverable in a table cell, score 3 on
Density, clear the threshold, and ship. Those four rules are the reason the publishing gate and
[T-028](../tasks/T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) exist; demoting
them to make the bookkeeping tidy inverts the priority the ruleset was built around.

**Why §1's own reason does not license leaving them unobserved.** §1 justifies *`hard` rules are
never scored* with one sentence: *averaging a hard failure into a score is how a deck ships with a
wrong number on the title slide and an 84%.* That reason is about **dilution by arithmetic**. It says
nothing about who observes the failure — so it forbids scoring them and does not permit ignoring
them. The checklist emits rule IDs and no numbers, which is exactly what the reason asks for.

**What made it affordable.** Two dozen yes/no judgements inside a pass that already reads the whole
deck end to end, so §8.1's cost of two passes per measurement round is unchanged. A separate pass was
rejected for the reason §8.1 already gives against a pass per slide: the second read buys nothing the
first cannot see.

**The first run justified the machinery.** Applied to
[`examples/reference-deck.html`](../examples/reference-deck.html), twenty-three passed and **two
failed** — DS-036, whose mono role carries load-bearing labels and a legend DS-026 obliges the deck
to show, and DS-208, whose *no cultural metaphor* clause catches a ribbon-cutting headline. Neither
is reachable by any check in this repository, and the deck had passed every gate in it since
[T-040](../tasks/T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md).
[T-052](../tasks/T-052-two-hard-judge-failures-in-the-reference-deck.md) settles both.

---

## 5.9 DS-229 — the one thing a check can decide about a component

**Written the same way DS-228 was, and for the same reason.** DS-136 requires interaction patterns to
be *built once as components and reused, so the UX is learnable* — a judgement, and it stays one.
Whether two similar things ought to have been the same component is a design decision, and
*learnable* is a property of a person, not of a DOM. But there is one question inside it a program
can answer, and it is the one a generator gets wrong: **are the components a deck names the
components it emits?** DS-229 is that question and nothing wider, exactly as DS-228 is the single
instance of DS-137 a check can decide.

**Why it needed a rule at all rather than a row under DS-136.** T-038's discriminator: *the thing
measured is the thing cited, or the check does not ship and the rule is excused in writing instead.*
DS-136 sits on the hard-judge checklist with `Reach: —`, so the ruleset already says no mechanical
gate reaches it; a contract check citing DS-136 would be claiming a reach the ruleset denies, which
is the defect T-038 spent a task removing. The alternative — reclassifying DS-136 as `auto` — would
have moved a genuine judgement out of the evaluator's hands to make a check fit.

**The completeness half is the half that keeps it true, and it is not symmetrical with the rest.**
The other clauses ask whether the markup matches the document. That one asks whether the document
matches the CSS: every class the shared style block styles has a row. It exists because **a component
is added by writing a rule**, and that is precisely the moment nobody remembers a contract document
exists. Without it the contract decays into a description of the deck as it was on the day it was
written, and every check built on it keeps passing.

**What `vocabulary` is for.** Five rows are styled, emittable and unused by this deck — the figure's
three role classes, `.t-ink` and `.mono`. *Declared and unused* is otherwise an unfalsifiable label,
so the check reads it backwards: a `vocabulary` row with an instance in the deck is a **failure**,
and the row has to be reclassified. That makes the count of them a number a reader can watch, which
is what the deck's own stale `.ribbon button::before` selector cost T-035 — **a rule that matches
nothing looks exactly like a rule that passed.**

**What this cost the coverage account.** One rule with `Reach: yes` and `Check: auto`, so the number
[T-005](../tasks/T-005-build-check-the-gate-the-deck-must-pass.md) must account for moved from **111
to 112** on 2026-08-09, and the checked count from 79 to 80 — derived from the ruleset, and
re-derivable rather than to be trusted from this line.

**The easing clause, and the correction it needed within the day.** The first pass closed a real
gap — a `cubic-bezier` written inside a component was unreachable by every check here — and left
four of DS-140's motions with `ease-in-out` written into them, because DS-141 named that keyword.
The effect was a gate that read as *bespoke easing is forbidden*, which is not what any rule
argues and is not a position this project holds: a deliberate overshoot on a card reveal is a
design decision, and DS-000 exists precisely so the ruleset does not stand in the way of one.
**The fault was in DS-141, not in the check.** *Max 500 ms, ease-in-out* is one theme's curve
stated as the ruleset's — the third time that shape has been found here, after DS-034's line
height and DS-140's durations (**L-45**), and the first time on a value that is a word rather than
a number. What the cap and its rationale argue is that a transition is **short and eased**; nothing
argues *which* easing. So the rule now says *eased rather than linear*, **every named motion
carries an easing token**, and `themes/lattice.css` moves three of them — Turn overshoots, Scale
and the slide transition ease out — which is the second artefact proving the axis is real rather
than declared. `linear` survives in the two places the mechanism requires it: a looping dash
stutters at the seam under anything else, and a zero-duration `visibility` step has nothing to
ease.

---

## 5.10 DS-230 and DS-231 — the rule that says what tier two is *for*

**§5.3 had eleven rules and every one of them was a test to reject.** DS-162 says what must be tier
one, DS-161 says the slide must stand closed, DS-170 says long text goes behind rather than on,
DS-227 says a panel starts shut. Run them all and a deck can still put an appendix behind the click,
because **nothing said what should be there** — and a generator with a rule set that only rejects
will produce the thing no rule happened to name. That is the gap DS-230 closes, and it is the reason
[T-002](../tasks/T-002-build-mode-the-self-contained-deck-generator.md) needed it before it could
emit a panel: §5.3 gave it mechanics and no editorial test.

**Extracted, not authored, and the reference deck's ten panels are what it was read off.** Every one
of them answers a question its own slide provokes, and the questions fall into four shapes with no
remainder:

| Kind | What it answers | The deck's |
| :--- | :--- | :--- |
| `derivation` | How a figure on the face was produced | 3 — *How eleven minutes is computed* · *Why the wait is half the headway* · *Assumptions behind this curve* |
| `scope` | What a term or figure on the face includes and excludes | 3 — *What the grant will and will not fund* · *What each figure excludes* · *How the corridors are defined* |
| `condition` | What the claim needs to hold, and where it fails | 3 — *What the timed connection requires* · *What the gate measures* · *How each tripwire is measured* |
| `instances` | The named members of a total the face states as a count | 1 — *The three corridors that wait* |

**Two candidate rules were measured against those panels and thrown away**, which is what makes the
third one a finding rather than a preference. *The panel's label shares a word with the face* fails
on slide 5 — "What each figure excludes" names the ledger without naming anything in it — so
anchoring cannot be checked by vocabulary. *Every row key names something the face shows* fails on
three panels: the keys are roles in the panel's own argument (`Input` · `Step` · `Result`), not
labels borrowed from the slide. The pattern that survived is about the **question**, and a question
is a judgement, which is why DS-230 is `judge`.

**The kind is written into `data-disc` because a judgement with no trace has to be re-derived by
whoever judges it.** The attribute was required and valueless until this rule; filling it turns the
evaluator's question from *is this panel any good* into *is this claim true*, which is the same
trade the ruler's `data-scale` makes under DS-217. The gate verifies **closure only** — one of four,
never the right one of four — and DS-230 says so on its own row rather than leaving the reach to be
assumed.

**DS-231 is the one clause of DS-161 a program can settle**, on the DS-228 and DS-229 precedent. A
bottom line quoting a figure that exists only inside a panel is a slide asserting a number its
reader cannot see, and *closed, the slide still makes its point* is exactly the rule it breaks.
**The instrument had to be built asymmetrically and the reference deck is what proved it:** a
citation is read strictly, as `content.py`'s figure pattern, while support is any number visible
with the slide closed. Read strictly on both sides, slide 3 failed — the stat figure `11` and the
unit `minutes, average wait` are two elements, so "11 minutes" is never one figure on that face —
and the deck was right. **A gate row that over-reports blocks a conforming build**, which is the
opposite trade from the figure ledger's, where over-reporting is safe because a person reads the
output.

**What it is worth on this deck: 0 of 6.** Six figures are cited by a bottom line, and one of them —
slide 3's `11` — is also inside its panel and cleared by the face, so the subtraction is exercised
rather than merely defined. **Three of the ten panels hold no figure at all**, so the row is thin by
construction and says its own denominator for that reason.

**What the two cost the coverage account.** Owned rules **112 → 113**, checked **80 → 81**, and the
hard-judge checklist gains one — derived from the ruleset on every run, and re-derivable rather than
trusted from this line.

---

## 6. Drops and amendments worth knowing

### 6.0 The 2026-08-17 audit — four changes, and nothing deleted

**Every rule was tested against one question — does satisfying it make a deck better, or only
different — and the examination is [`RULESET-AUDIT.md`](RULESET-AUDIT.md).** This section is the
record of what moved. **165 examined, 161 untouched, 4 changed, 0 deleted.** The audit was raised
expecting to remove rules and removed none; what it found instead was rules nothing could apply,
which is a different defect with a cheaper fix.

**DS-042 — reclassified `auto` / `never` → `judge` / `—`. Cost: the gate owns one rule fewer.
Bought: the rule can be applied at all.** It was the ruleset's only `Reach: never` — a `hard` rule
assigned to a mechanism that could not decide it *in principle*, not merely today. That pair had
been defended in the `Reach` preamble as coherent, and it is: a program could test *boxes that read
as a set are siblings* if something told it which boxes read as a set, and nothing can. **Coherent
was doing the work that useful should have been doing.** `judge` puts it on
[`EVALUATION.md`](EVALUATION.md) §1.1's hard-judge checklist, where a person answers it — the first
instrument the rule has had since it was written. `check.py`'s deferral of DS-041 had asked for this
review by name and stated it as its own closing condition.

**DS-041 — split. Cost: the rule is two sentences where it was one. Bought: the gate stops deferring
a clause it can decide.** It carried a technique a check can see (*align by construction, not by
coordinates*) and a reading no program can produce input for (*correlated rows share a grid track*),
and the gate deferred the whole rule on the second. The reading half is DS-042's, which is now
`judge`; DS-041 keeps the half a check can reach. **The check itself is not written** — that is
`check.py`'s work and its deferral now says so.

**DS-138 — narrowed to tier two. Cost: chrome loses a rule that was protecting it by accident.
Bought: a rule that no longer forbids the only placement that fits.** *Popovers drop below the
element* has a stated reason — content a reader stops and reads must fit on the stage — and a scope
that reached every popover in the deck, so it blocked a two-item control menu on the chrome row,
which sits at the foot of the stage where *below* is the one direction with no room.
[T-114](../tasks/T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) had to argue an
exemption before writing a line of code. **The rule was right and its scope was wrong, which is the
expensive combination: it does not look like a defect, so it gets obeyed.** The obligation it exists
for — every panel opens fully inside the stage — is now stated generally and binds chrome too, so
narrowing the *direction* clause loses nothing.

**DS-007 — moved from §1.1 to §8. Cost: nothing; the ID is permanent and every citation still
resolves. Bought: §8's claim about itself is true.** *The `file://` console warning is benign, do not
chase it* binds whoever is debugging a deck, which is exactly the class §8 declares and holds — and
filed among the portability rules it read as something a deck must satisfy. §8 said there were four
such rules and there were five.

**Thirteen rules had no instrument at all, and none of them moved.** Not gated, not `hard` so not on
the hard-judge checklist, named by no rubric dimension and by no skill: DS-022, DS-025, DS-029,
DS-038, DS-083, DS-094 to DS-096, DS-098, DS-169, DS-170, DS-206 and DS-213. §1's remedy for a rule
that has never fired is *give it an instrument or demote it to `guidance`*, and an instrument was
available for every one, so the fix is five edits naming them — four to `EVALUATION.md`'s dimension
lists and one to the pipeline's stage 5. **How they got there is the part worth keeping**: those
lists name rules in ranges, `DS-034 to DS-037` stops one short of `DS-041 to DS-049`, and DS-038 fell
in the gap. **A rule goes missing by being numbered between two ranges**, which no reading of that
rule can catch and no gate can see.

**What was examined and deliberately left alone.** DS-115 — *particles, connectors and custom
diagrams may be drawn freely* — is a permission, cannot be violated, and duplicates DS-111. It was
**not** merged: the ID column promises a retired rule keeps its number and is marked retired,
`ruleset.py` has no notion of a retired row and would keep counting it, so the merge buys one
`guidance` row and costs a tooling convention. **That is the audit's own cost test turned on the
audit.** The near-duplicate emphasis rules — DS-046, DS-048, DS-101, DS-209, all saying *one
emphasis, not three* at four scales — were kept for the same reason plus one more: DS-209 states its
relationship to DS-101 in its own text rather than hiding it, and a ruleset that repeats itself and
says so is not the failure this audit was looking for.

**DS-011 — one palette per deck was dropped.** The corpus rule (C7) is `dominant`; it describes what
the decks actually do. It lost to CLAUDE.md rule 4, **not to evidence** — a standing decision
overriding an observed habit. R4 also grades C7 inherited (the source skill's four presets adapted
per deck), so dropping it costs the owner's signature nothing. Everything else in §2.1 is
*within-palette* discipline and is unaffected. The variety it provided returns from the template
generator, not from per-deck improvisation.

**DS-030 — the per-deck font rotation went with it.** R4 traced *"a deliberate pairing per deck"* to
the source skill's instruction to rotate pairings and never repeat one; it was never the owner's
signature. **The role structure was the valuable half and it is kept.** R5 recommends Instrument
Serif · Space Grotesk · JetBrains Mono at 97.3 KB.

**DS-031 — do not read corpus frequency as intent.** Inter is the most frequent face in the older
decks and the refined specs reject it by name. R5 adds the cost argument: Inter is the most
expensive of the four at 62.8 KB inlined and the least distinctive.

**DS-001/DS-002 — there is no quality/self-containment trade-off.** The corpus rule said *maximise
quality at all cost, even in multiple files*. R5 measured a full 12-slide deck with three embedded
faces, icons, a motion library and four SVG diagrams at **191.8 KB with zero external references**.
The escape hatch has nothing left to buy.

**DS-005 — nothing `file://` refuses costs the deck anything.** R6 measured 95 rows on Chrome 151 and
Edge 151: `file://` is a secure context, so `crypto.subtle`, view transitions, container queries,
popover, WebGL1/2 and a WebGPU adapter are all available, as are fullscreen, clipboard, audio resume,
download and every storage API. **Do not design around fears this research retired.**

**DS-123 — "boxes everywhere" is one of seventeen unflagged departures.** The source skill
*prescribes* the card grid and step-card pipeline as house style. This is where R2's best-supported
findings and the owner's sharpest instinct agree, which is rare enough to name.

**DS-090 — the heading check went semantic.** The brief's *every `<section>` has a heading* becomes
*every `<section>` has a heading that is a claim*. **That constrains the writing, not just the
markup** — tractable only because the brief already decided the plugin writes the words. It grows
build mode as well as the check.

**A-09, A-13, A-14 are the owner's signature.** They are the three archetypes added to an inherited
set, and the three that external practice independently arrives at. The other six corpus archetypes
match external exemplars only because both descend from the same design canon — **one source counted
twice, not convergence.** Where this project cites the owner's taste, it cites these three.

**A-01 and A-02 are admitted on external evidence alone.** The corpus never named them, probably
because a layout-oriented spec would not. Both are structural, and R2 says they carry the argument.
