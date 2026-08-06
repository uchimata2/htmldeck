# htmldeck — evaluation and the convergence loop

**How a deck is scored against [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md), and when it is good enough to
stop.**

Loaded by the build and critique modes. Rules are cited by their `DS-nnn`, `A-nn` and `X-nn` IDs; it
does not restate them.

> **The score is a stopping rule, not a quality claim.** It answers *"is there a known defect left
> that this loop can fix?"* — never *"is this deck good?"* A deck at threshold has run out of
> findings the rubric can see, which is a different and much smaller statement. **DS-191 applies to
> this document about itself:** the rubric confirms defects it was built to look for and cannot find
> ones nobody thought to measure.

---

## 1. Gate and score are different things

**`hard` rules are gates. They are never scored.**

A hard violation fails the deck outright, and no quality elsewhere compensates. Averaging a hard
failure into a score is how a deck ships with a wrong number on the title slide and an 84%.

**Only `default` and `guidance` rules and the judgement dimensions are scored** — the territory where
"better" and "worse" are meaningful and "broken" is not the right word.

| | Gate | Score |
| :--- | :--- | :--- |
| Which rules | 102 `hard` | 35 `default`, 6 `guidance`, and the dimensions in §3–§4 |
| Result | pass / fail, per rule ID | 0–4 per dimension |
| On failure | The deck is defective. Fix before scoring is meaningful. | A finding with a severity, entering the loop |

---

## 2. The pipeline, cheapest first

Ordering is a cost decision. **Never spend a judgement pass on a deck with external references.**

| # | Stage | Covers | Cost |
| :--- | :--- | :--- | :--- |
| 1 | **Auto gate** | 59 `auto` rules — static analysis of the file | Near zero. Runs first, always. |
| 2 | **Render gate** | 32 `render` rules — measurement and a look at the rendered deck | One render, several measurements |
| 3 | **Per-slide score** | S1–S6 (§3), per slide | The expensive stage. Scales with slide count. |
| 4 | **Whole-deck score** | D1–D4 (§4), once | One pass over the finished artifact |
| 5 | **Fix and re-enter** | §5 | Bounded by the iteration cap |

**Stage 4 is not optional and the report says whether it ran.** Defects that span slides are
invisible to per-slide review — this project has the evidence twice: a figure correct in one document
and wrong in the one quoting it, propagated to eight places across four documents, every one of
which had passed its own review.

---

## 3. Per-slide dimensions

Six dimensions, **0–4 each, maximum 24.** Anchors are given at 0, 2 and 4 because an unanchored scale
scored by the agent that wrote the deck drifts to the middle. **1 and 3 are between the anchors, not
separately defined.**

### S1 — Claim · *DS-090, DS-085, X-01, X-02*

| | |
| :--- | :--- |
| **0** | The heading is a topic label, or the slide is a bullet dump. The slide asserts nothing. |
| **2** | The heading states a claim, but the body does not clearly establish it. |
| **4** | The heading is a claim; everything on the slide is evidence for **that** claim; nothing else is present. |

### S2 — Evidence · *DS-102, DS-103, A-12, X-03, X-05, X-07*

| | |
| :--- | :--- |
| **0** | An unsourced figure, or a shape that misleads — two points as a trend, a rebased axis, a metric invented for the slide. |
| **2** | Figures are real and traceable, but the support is thin, or one side of a comparison is argued and the other is not. |
| **4** | Every figure sourced; the recommendation's real cost stated in the deck's own voice rather than left for the audience to find. |

### S3 — Encoding · *DS-116, DS-117, DS-121, DS-123, X-04, X-10, X-11*

| | |
| :--- | :--- |
| **0** | Boxes where a diagram belongs, or a diagram that does not do what its type promises — the Venn whose sets do not overlap. |
| **2** | Correct diagram type, but connectors unlabelled, or a weaker encoding than the data permits. |
| **4** | The visual carries the claim by itself; the encoding is the strongest the data allows; every connector meets its target and says what it means. |

### S4 — Density · *DS-091, DS-160, DS-161, DS-162, DS-167, X-06, X-08, X-09*

| | |
| :--- | :--- |
| **0** | The slide only resolves with narration, or only once something is opened. |
| **2** | Closed, it makes its point — but tier two holds something a first-time reader needs. |
| **4** | Closed, the argument is complete. Tier two is genuinely optional and earns its place. |

### S5 — Craft · *DS-034 to DS-037, DS-041 to DS-049, DS-101, X-12*

| | |
| :--- | :--- |
| **0** | Misalignment visible at a glance, text under the design-unit floor, or residue — branding, a typo on the most important slide. |
| **2** | Clean but unremarkable. Spacing inconsistencies that do not read as errors. |
| **4** | Aligned by construction, one emphasis per point, type on the scale, nothing left to remove. |

### S6 — Motion · *DS-140 to DS-150*

| | |
| :--- | :--- |
| **0** | Animation that encodes nothing, or continuous motion on static content. |
| **2** | Motion is from the four-slot vocabulary and harmless, but adds nothing the static slide lacked. |
| **4** | Every animation encodes something the static slide could not show, and reduced motion keeps the semantics. |

> **A slide with no motion scores S6 as `n/a`**, not 4 — and its threshold is prorated to 15/20.
> Scoring absence as perfection rewards doing nothing, which is the opposite of what this dimension
> is for.

---

## 4. Whole-deck dimensions

Four dimensions, **0–4 each, maximum 16.**

### D1 — Spine · *A-01, A-02, DS-134*

| | |
| :--- | :--- |
| **0** | Slides ordered by topic. The sequence has no argument in it. |
| **2** | A coherent order, but objections are not retired in any deliberate sequence. |
| **4** | Each slide kills a named objection; the reader runs out of doubts before the deck runs out of slides; the timing is made non-arbitrary somewhere. |

### D2 — Pacing · *DS-081, DS-082, DS-084, §3.2*

| | |
| :--- | :--- |
| **0** | One archetype repeated throughout, or length set by dumping rather than by decision. |
| **2** | Some variety, but two or three slides could merge or go without loss. |
| **4** | Archetypes vary with what the argument needs; every slide earns its place; the length has a reason. |

### D3 — Close · *DS-085, DS-086, A-14*

| | |
| :--- | :--- |
| **0** | Ends on a summary, a recap, or a thank-you. |
| **2** | Ends on an ask, but stated as several things. |
| **4** | One action, unambiguous, and the deck has earned the right to ask it. |

### D4 — Consistency · *DS-114, DS-135, X-07, and the source reconciliation*

| | |
| :--- | :--- |
| **0** | A figure disagrees with itself or with a source; two numbering schemes with no mapping; a conceit that breaks mid-deck. |
| **2** | Figures agree, but icon or term usage drifts across slides. |
| **4** | Every repeated figure agrees; one icon per concept throughout; the metaphor holds end to end. |

> **D4 is found by counting, not by reading.** Tally every figure, its origin, and every place it is
> reused. Reading each slide on its own passes all of these — five document-level reviews did.

---

## 5. The threshold

**All three conditions must hold. They are not averaged.**

1. **Zero `hard` violations.** The gate.
2. **Every slide ≥ 18/24, and no slide dimension below 2.**
3. **Deck ≥ 12/16, and no deck dimension below 2.**

**The per-dimension floor is the important half.** Without it a slide reaches 18 on craft and motion
while scoring 1 on Claim — a beautiful slide that says nothing, which is the exact failure the
design system exists to prevent. **A dimension at 0 or 1 is a finding regardless of the total.**

---

## 6. The loop

```
  auto gate ─→ render gate ─→ per-slide score ─→ whole-deck score
       ↑                                                │
       │                                                ▼
       └──────── fix (one at a time) ←──── threshold met? ──→ PASS
```

### 6.1 Four ways it stops, and they are different outcomes

| Outcome | Trigger | What it reports |
| :--- | :--- | :--- |
| **PASS** | Threshold met | What was fixed, and every remaining `Note`. A pass is not "no findings". |
| **CAP** | Iteration 3 completes below threshold | Remaining findings as **"Open — needs a decision"**. The loop does not get a fourth attempt. |
| **STALL** | Total score gained < 2 points in an iteration | *These are not defects the loop can fix.* Almost always design decisions wearing a finding's clothes. Escalate, do not retry. |
| **OSCILLATION** | A fix reverts an earlier fix | **Stop immediately and name the two rules in tension.** |

**OSCILLATION is a finding about the ruleset, not about the deck.** Two rules that cannot both be
satisfied on one slide is exactly the kind of conflict `DESIGN-RATIONALE.md` §2 exists to record.
Report it there, do not paper over it with a third fix.

### 6.2 The fix ledger

Every fix records **rule ID · slide · was · now · iteration**. It is what makes oscillation
detectable — without it, a loop can alternate between two states forever and each individual
iteration looks like progress.

**Fixes are applied one at a time, in order of severity.** A batch of fixes whose combined effect is
a lower score cannot be attributed to any one of them.

### 6.3 The regression sweep — the part most likely to be skipped

**Each iteration re-runs the checks that passed, not only those that failed.** A fix that breaks
something previously fine is the failure mode a fix loop is most prone to and least likely to notice.

Re-run per iteration:

- **all `auto` gates, whole deck** — cheap, and a fix routinely reintroduces an external reference;
- **all dimensions of touched slides**;
- **all dimensions of slides sharing a component with a touched slide.** DS-136 requires interaction
  patterns to be built once and reused, so **a fix to a component silently touches every slide using
  it.** This is the non-obvious one and it is where regressions actually hide;
- **all four deck dimensions** — a slide fix routinely breaks D1 or D4.

### 6.4 Cost

Per iteration: one auto pass, one render pass, per-slide scoring **for touched and component-sharing
slides only**, and one whole-deck pass. With a cap of 3, worst case is 3 full render passes and
roughly 1 + 2×(touched fraction) slide-scoring passes.

**The cap is the cost control.** It is set at 3 because R1's pipeline runs build → review → owner
review → fix, which is two machine iterations before a human sees it, plus one.

---

## 7. Validating the rubric itself

**A rubric that has never been tested is a rubric that passes everything.** This project has already
paid for that lesson once: a scan measuring one quality dimension under-reported by 15× and was
believed because it did not look like a tool.

**Requirement: a seeded-defect deck with one known defect per dimension at score 0.** The rubric must
find each and score it 0 or 1. **If it scores a seeded 0 as a 2, the anchors are wrong** — fix the
anchors, not the deck.

Re-run whenever a dimension or an anchor changes. It is the only evidence that the loop's numbers
mean anything.

---

## 8. Open — needs a decision

Recorded here rather than settled, per DS-191 and the project's own habit of not letting an
implementer quietly answer an owner's question.

- **Who scores?** A self-scoring author is cheap and is the one most likely to pass its own work —
  "watch for missing content, not just errors" names this as the failure a self-review most easily
  misses. **Recommendation: per-slide scoring by the author against the anchors, whole-deck scoring
  in fresh context.** The deck pass is one pass over a finished artifact, so the cost is small and it
  is precisely where self-review is weakest.
- **Does the score reach the user?** A visible number invites gaming and implies precision the rubric
  does not have; hiding it makes the loop opaque. **Recommendation: report findings and outcome
  (PASS/CAP/STALL/OSCILLATION), not the number.**
- **Is the cap 2 or 3?** Settle against a real 12-slide deck, not in the abstract.
