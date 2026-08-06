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
| Which rules | 108 `hard` | 40 `default`, 6 `guidance`, and the dimensions in §3–§4 |
| Result | pass / fail, per rule ID | 0–4 per dimension |
| On failure | The deck is defective. Fix before scoring is meaningful. | A finding with a severity, entering the loop |

> **Every count in this document is derived from `DESIGN-SYSTEM.md` and goes stale when a rule is
> added.** These are as of 2026-08-06: 154 rules, counting DS-000. **Re-derive them, never adjust
> them by hand** — the previous set was wrong by six, having been written before the rules T-027 and
> T-025 added, and a hand-adjusted count is indistinguishable from a correct one.

---

## 2. The pipeline, cheapest first

Ordering is a cost decision. **Never spend a judgement pass on a deck with external references.**

| # | Stage | Covers | Cost |
| :--- | :--- | :--- | :--- |
| 1 | **Auto gate** | 65 `auto` rules — static analysis of the file | Near zero. Runs first, always. |
| 2 | **Render gate** | 39 `render` rules — measurement and a look at the rendered deck, **with motion pinned off** (DS-221) | One render, several measurements |
| 3 | **Per-slide score, by the author** | S3, S5, S6 (§3), per slide | Scales with slide count, but the author already holds the context |
| 4 | **The judgement pass, in fresh context** | S1, S2, S4 across every slide, and D1–D4 (§4) | One pass over the finished artifact |
| 5 | **Fix and re-enter** | §5 | Bounded by the iteration cap |

**The split between stages 3 and 4 is a ruling, not a convenience** — §8.1. The five dimensions no
mechanical check can reach all sit in stage 4, read without the build history, because a self-scoring
author is the one most likely to pass its own work.

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

**A slide's total spans two scorers** — S3/S5/S6 from the author, S1/S2/S4 from the judgement pass
(§8.1). Conditions 2 and 3 are evaluated once both have run; a threshold declared on the author's
half alone is not a threshold.

**The per-dimension floor is the important half.** Without it a slide reaches 18 on craft and motion
while scoring 1 on Claim — a beautiful slide that says nothing, which is the exact failure the
design system exists to prevent. **A dimension at 0 or 1 is a finding regardless of the total.**

---

## 6. The loop

```
  auto gate ─→ render gate ─→ author score ─→ judgement pass
                              (S3 S5 S6)      (S1 S2 S4 · D1–D4,
       ↑                                       fresh context)  │
       │                                                       ▼
       └───── fix (batched, §6.2) ←──── threshold met? ─────→ PASS

  One trip round the loop is one MEASUREMENT ROUND. The cap counts rounds,
  not fixes — a round carries as many fixes as the round found.
```

### 6.1 Four ways it stops, and they are different outcomes

| Outcome | Trigger | What it reports |
| :--- | :--- | :--- |
| **PASS** | Threshold met | What was fixed, and every remaining `Note`. A pass is not "no findings". |
| **CAP** | Iteration 3 completes below threshold | Remaining findings as **"Open — needs a decision"**. The loop does not get a fourth attempt. |
| **STALL** | Total score gained < 2 points in an iteration | *These are not defects the loop can fix.* Almost always design decisions wearing a finding's clothes. Escalate, do not retry. |
| **OSCILLATION** | A fix reverts an earlier fix | **Stop immediately and name the two rules in tension.** |

**No outcome prints the score** — §8.2. The trigger column above is how the loop decides; what
reaches the user is the outcome, the findings, and any dimension at 0 or 1 named as a finding.
STALL's "< 2 points" is an internal comparison, not something the report states.

**OSCILLATION is a finding about the ruleset, not about the deck.** Two rules that cannot both be
satisfied on one slide is exactly the kind of conflict `DESIGN-RATIONALE.md` §2 exists to record.
Report it there, do not paper over it with a third fix.

### 6.2 The fix ledger

Every fix records **rule ID · slide · was · now · iteration**. It is what makes oscillation
detectable — without it, a loop can alternate between two states forever and each individual
iteration looks like progress.

**Fixes are worked in order of severity, and batched within a round.** The cap in §6.4 counts
measurement rounds, not fixes — a round carries as many fixes as that round's measurement found.

**One at a time applies to fixes that interact**, which is the case the rule was written for: two
fixes that can move the same score, touch the same component (DS-136), or contend for the same space
on a slide. A batch of *those* whose combined effect is a lower score cannot be attributed to any one
of them. **Fixes that cannot interact are batched**, and the fix ledger keeps them attributable
anyway.

> **Why this is scoped rather than absolute.** Read literally alongside a cap of 3, the rule permits
> three fixes per deck. The reference deck needed **23** before it cleared its own gate, so the loop
> would have reported CAP with twenty defects outstanding — the cap firing on a deck that was
> converging perfectly well. Evidence:
> [T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md) §4.1.

### 6.3 The regression sweep — the part most likely to be skipped

**Each iteration re-runs the checks that passed, not only those that failed.** A fix that breaks
something previously fine is the failure mode a fix loop is most prone to and least likely to notice.

Re-run per iteration:

- **all `auto` gates, whole deck** — cheap, and a fix routinely reintroduces an external reference;
- **S3, S5 and S6 on touched slides**;
- **S3, S5 and S6 on slides sharing a component with a touched slide.** DS-136 requires interaction
  patterns to be built once and reused, so **a fix to a component silently touches every slide using
  it.** This is the non-obvious one and it is where regressions actually hide;
- **the whole judgement pass — S1, S2, S4 on every slide and all of D1–D4.** It re-runs entire, not
  on touched slides only: a slide fix routinely breaks D1 or D4, and it is one pass either way
  (§8.1), so there is nothing to save by narrowing it.

### 6.4 Cost

Per measurement round: one auto pass, one render pass, the author's per-slide scoring **for touched
and component-sharing slides only**, and **one fresh-context judgement pass** (§8.1). The two scoring
stages are **2 passes per round** — 4 for a deck that converges like T-024's, 6 at the cap.

**The cap is the cost control, and it counts measurement rounds.** It is set at 3 because R1's
pipeline runs build → review → owner review → fix, which is two machine iterations before a human
sees it, plus one. **Measured against a real deck, 2 rounds sufficed** — see §8.

**The cap does not bound the number of fixes, and must not.** A round's cost is one render plus the
scoring it triggers; applying twelve fixes inside that round costs one render, not twelve. Counting
fixes would price the cheap half of the loop and cap the deck on it.

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

## 8. Decisions taken

Three questions this document held open. **All three are now settled** — the two below by the owner
on 2026-08-06 ([T-026](../tasks/T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md)),
the third against measurement. They are rulings, not recommendations; a mode that departs from one
is defective, not merely unusual.

### 8.1 Who scores — the author, plus one fresh-context judgement pass

**Ruling.** The author scores **S3, S5 and S6** per slide against the anchors. **One fresh-context
pass** scores the five dimensions no mechanical check can reach — **S1, S2 and S4 across every
slide, and D1 to D4** — reading the finished artifact without the build history.

**Cost accepted: 2 passes per measurement round** — 4 for a deck like T-024's, which reached PASS in
two rounds; 6 at the cap of 3. The alternatives were 0 passes (author scores everything) and roughly
25 passes for T-024's deck at a fresh-context pass per slide.

**How the five judgement-only dimensions are covered.** They are the whole point of the ruling.
[T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md) §4.2 found that five of
ten dimensions — **S1 Claim, S2 Evidence, S4 Density, D1 Spine, D4 Consistency** — are invisible to
every static and measured check, so whoever scores *them* is the quality mechanism. All five are
assigned to the fresh-context pass and none is left with the author. The evidence for putting them
there is in the same task: **D4 scored 4 only after counting, and on reading alone it was a 2** —
the author had read past the contradiction repeatedly.

**Why one pass and not twelve.** S1, S2 and S4 are per-slide dimensions, but they are scored in a
single read of the whole deck rather than twelve isolated ones. That is not a cost compromise: S4's
"a first-time reader needs this" and S2's "one side argued and the other not" are both judgements
about the deck a reader actually meets, and a per-slide pass in isolated context cannot make them.
D1 and D4 require the whole deck by definition.

**The threshold in §5 is unchanged and combines both passes.** A slide's 24 points come from the
author's S3/S5/S6 and the judgement pass's S1/S2/S4; the per-dimension floor applies across both.

**The known limit.** Fresh context removes the build history, not the author. Where the same model
scores its own work without that history, this ruling buys independence of *memory*, not of
judgement — a real reduction in the failure T-024 exhibited, and not the same thing as review by
another party.

### 8.2 Does the score reach the user — no

**Ruling.** The report states the **outcome** (PASS · CAP · STALL · OSCILLATION) and **every
finding**. **The numbers are never shown** — not per-slide totals, not the whole-deck total, not
per-dimension scores.

**What the user sees instead.** The outcome, which is the decision the score exists to make; every
finding with its severity and the rule ID or dimension it came from; and, on a PASS, what was fixed
plus every remaining `Note`. A dimension at 0 or 1 reaches the user **as a finding naming the
dimension** (§5 makes it one regardless of the total) — so the actionable half survives without the
arithmetic.

**Cost accepted: none in passes.** The scoring runs either way; this governs only what is printed.
The cost is opacity — a user cannot see how close to threshold a deck sits, and cannot watch it
converge round by round.

**Why.** §0 of this document says the score is a stopping rule, not a quality claim. T-024's deck
passed at 18–22 per slide and 16/16, and those numbers imply a precision the rubric does not have;
its **findings**, by contrast, were all actionable. A visible number also invites fixes aimed at the
number rather than at the deck.

### 8.3 Is the cap 2 or 3 — 3

**Ruling: the cap stays at 3, counting measurement rounds.** Closed 2026-08-06 by
[T-025](../tasks/T-025-reconcile-the-twelve-ruleset-findings-from-the-reference-deck.md), **against a
real 12-slide deck rather than in the abstract** — this one was settled by measurement, not by the
owner.

[T-024](../tasks/T-024-build-the-reference-deck-and-validate-the-ruleset.md) §4.1 reached PASS in
**two measurement rounds** — round 1 found 23 defects across contrast, spill, clipping, the type
floor and the reflow view; round 2 found one, a cross-slide figure disagreement. The measured need
was 2, and a cap set at the measured need leaves a first-draft deck no margin at all.

**What the evidence settles is that 3 is not *low*** — the question §6.2 answered — rather than that
3 is exactly right. **One deck, one topic, one author.** A deck that needs a fourth round is a deck
the loop should hand back, and that claim has been tested once.
