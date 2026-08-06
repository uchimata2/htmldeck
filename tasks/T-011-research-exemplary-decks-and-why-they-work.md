---
id: T-011
title: Research exemplary decks and what makes them work
type: research
status: done
phase: review
parent: null
blocked_by: []
related: [T-014]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/research/R3-exemplar-decks.md]
---

# T-011 — Research exemplary decks and what makes them work

## 1. Specify

**Outcome**
A catalogue of widely-regarded decks and individual slides, each reduced to the reusable move that
makes it work — expressed as something the plugin can actually produce.

**Why this one**
Principle (T-010) says what to aim for; exemplars show what hitting it looks like. This is the
source of the slide archetype library — the shapes the build mode reaches for — and the main
defence against the plugin producing competent, forgettable decks.

**Scope**
- In: the canonical business and startup decks, conference and technical talks known for their
  visual work, and individual slides that solve a recurring problem well — the single-number
  slide, the before/after, the timeline, the architecture view, the uncomfortable-truth slide, the
  close.
- In: for each, the *transferable* move, stated as a rule, and whether the corpus (T-009) already
  does it.
- Out: aesthetics that depend on a brand, a photographer, or a budget the plugin cannot reproduce.
- Out: copying any deck's content or visual identity — this feeds archetypes, not templates.
- Out: moves that only work because of who was delivering them — see the answered question below.

**Inputs**
- `docs/research/R2-external-principles.md` — the principles an archetype has to satisfy; P-01/P-02
  in particular decide what an archetype *is* here (a shape of evidence under a claim).
- `docs/research/R1-corpus-conventions.md` §10 — the 13 layout archetypes the corpus already names,
  which is what the overlap map is drawn against.
- `docs/research/R4-prior-art.md` §9 — provenance, so a corpus archetype inherited from the deck
  skill is not counted as convergent evidence.
- `docs/research/R6-portability-contract.md` — the reproducibility column is a claim about what a
  double-clicked file can do, and R6 is the measured answer.

**Acceptance criteria**
- [ ] At least 12 archetypes catalogued, each with exemplar, the move, and when to use it
- [ ] Each archetype marked reproducible in single-file HTML with inline SVG, or noted as not
- [ ] Overlap with the corpus archetypes from T-009 mapped
- [ ] Anti-patterns catalogued too — the slide shapes that consistently fail
- [ ] Every candidate put through the lone-reader test, and the ones that fail it recorded as
      presenter-carried with a reason, rather than dropped silently

**Answered 2026-08-06 — no owner shortlist; the exemplars are selected here. But the owner
attached a condition that is a selection filter, not a footnote: _do not mix the success of a deck
with the quality of the presenter._**

Most canonically-cited decks are famous because of who delivered them, in what year, to what
outcome. That reputation says nothing about whether the artifact works. So every candidate is
admitted only against the **lone-reader test**: would the move still land for a stranger opening
the file with no speaker, no context and no reputation attached? A move that needs the room, the
delivery or the founder's story is recorded as **presenter-carried** and excluded from the
archetype library — it is not reproducible by a plugin, which ships the file and never the person.

This cuts both ways and both directions are useful:
- A celebrated deck whose slides are weak on their own is an **anti-pattern source**, not an
  exemplar. Its fame is evidence about the presenter.
- An obscure deck whose slides carry themselves unaided is a better exemplar than a famous one.

**Open questions**
- None outstanding.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Collect candidate decks and slides, from the canonical business/startup set, conference and technical talks, and recurring single-slide problems | shortlist |
| 2 | **Apply the lone-reader test to every candidate before reducing it** — would the move land for a stranger with no speaker and no context? | admitted list, plus a **presenter-carried** list with reasons |
| 3 | Reduce each admitted candidate to one transferable move, stated as a rule the build mode could execute | archetype entries |
| 4 | Rule each archetype against `file://` reproducibility, using R6 rather than assumption | feasibility column |
| 5 | Map against R1 §10's 13 corpus archetypes, checking R4 §9 provenance before counting an overlap as agreement | overlap map |
| 6 | Catalogue anti-patterns — including the ones the presenter-carried list produces | anti-pattern table |
| 7 | Write up | `docs/research/R3-exemplar-decks.md` |

**Approach decisions**
- **The lone-reader test runs at step 2, before the reduction, not as a filter afterwards.** Reducing
  a deck to its move first and then asking whether it survives without its presenter invites
  rationalising a famous exemplar into the catalogue. Screening first keeps fame out of the
  admission decision.
- **A corpus overlap only counts as convergence if R4 §9 says the corpus rule is owner-authored.**
  If the corpus archetype was inherited from the deck skill, two sources agreeing is one source
  counted twice — the trap this project has already recorded once.
- **Exemplars are named and described, never reproduced.** The catalogue records the move, not the
  slide; nothing from a source deck's content or visual identity is copied. This is CLAUDE.md's
  publishing constraint applied to external material as well as to the corpus.

## 3. Implement

**Decisions & assumptions**
- **The owner's condition was implemented as an admission test, not a caveat** — 2026-08-06. Applied
  before the reduction step, it disqualifies a large part of the canon (§2) and admits two decks
  that were never presented at all. It changed the catalogue's contents materially rather than
  adding a disclaimer to it.
- **Rosling was split rather than admitted or excluded** — 2026-08-06. Excluding it whole would have
  lost a real encoding; admitting it whole would have credited the artifact with the delivery's
  effect. The split produced the general rule in §2.1 — the move is usually in the encoding, the
  fame usually in the delivery.
- **The provenance filter was applied to the overlap map and it cut it in half** — 2026-08-06. Six
  corpus archetypes match external practice; R4 §9 rules the archetype set inherited except
  Timeline, Case File and Verdict. Counting the inherited six as convergence would have been one
  source counted twice. Only three overlaps are reported as meaningful, and they are exactly the
  owner's three additions.
- **Reproducibility was ruled from R6, and its limit is stated** — 2026-08-06. R6 answers "is this
  capability available from `file://`"; it does not answer "does this layout read well at 12
  slides". §8 says so rather than letting the column imply more than it checked.
- **Assumption, stated: no archetype was built and looked at** — 2026-08-06. This is a catalogue,
  not a deck, so CLAUDE.md rule 6 does not bite here — but it will bite on whatever T-014 and the
  build tasks produce from it, and §8 hands that on explicitly rather than leaving it implied.

**Outputs produced**
- `docs/research/R3-exemplar-decks.md` — 14 archetypes with exemplar, move, use-when and a
  reproducibility ruling; 5 presenter-carried exclusions with reasons; 12 anti-patterns; the
  provenance-filtered overlap map.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| At least 12 archetypes catalogued, each with exemplar, the move, and when to use it | **met** | R3 §3 — 14, each stated as something the build mode could execute. Two (A-01 Why-Now, A-02 Risk-Retirement) are additions the corpus set does not contain. |
| Each archetype marked reproducible in single-file HTML with inline SVG, or noted as not | **met** | R3 §4 — ruled against [R6](../docs/research/R6-portability-contract.md)'s measured matrix, not assumed. **None rejected**, which agrees with R6's own conclusion that no refused capability costs the deck anything. The reduced-motion degradation for A-05 is specified rather than left open. |
| Overlap with the corpus archetypes from T-009 mapped | **met, and the provenance filter halved it** | R3 §5. Six naive matches; [R4 §9](../docs/research/R4-prior-art.md) rules the archetype set inherited except Timeline, Case File and Verdict, so only three overlaps are independent evidence — and they are exactly the owner's own additions. |
| Anti-patterns catalogued too — the slide shapes that consistently fail | **met** | R3 §6 — 12. Four are from this project's own corpus critique rather than the outside world, and are marked as such. |
| Every candidate put through the lone-reader test; failures recorded as presenter-carried with a reason | **met** | R3 §2 — five exclusions tabled with reasons, plus §2.1 where Rosling splits into an excluded delivery and an admitted encoding. |

**Verified how.** Read and reasoned, like T-010 — no deck was built. Exemplar claims were grounded
in published analyses rather than recollection, and the two load-bearing structural claims (Airbnb's
objection-ordered sequence, Netflix reaching its audience as a document) were checked against
sources rather than asserted. The overlap map was gated on R4 §9 before any convergence was claimed.
`python tools/tasks/task.py check` passes with 124 document pointers resolving. R3 §8 states plainly
what the reproducibility rulings do *not* cover, so a later session does not read them as a layout
verdict.

**Child fix tasks raised**
- none. The findings all land on T-014, which is where the synthesis belongs, and R3 §8 addresses
  them to it directly.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created from the owner's direction to research best-in-class decks. |
| 2026-08-06 | (no change) | Owner answered the exemplar question: no shortlist, selection is ours — but do not confuse a deck's success with its presenter's quality. Added the lone-reader test as a scope exclusion and a fifth acceptance criterion. |
| 2026-08-06 | → specified | `Inputs` added (R1 §10, R2, R4 §9, R6). No open questions remain. |
| 2026-08-06 | → planned | Plan expanded from four steps to seven. The lone-reader test is sequenced *before* the reduction, so fame cannot enter through a rationalised move; a corpus overlap only counts as convergence once R4 §9 confirms the corpus rule is owner-authored. |
| 2026-08-06 | → in_progress | All seven steps run. The admission test proved to be the method rather than a filter — it excluded most of the celebrated canon and admitted two decks that were never presented, which is the owner's condition validating itself. |
| 2026-08-06 | → done | `docs/research/R3-exemplar-decks.md` written; all five acceptance criteria met. Three results for T-014: Layered Detail should be a **modifier on the other thirteen archetypes, not a fourteenth**; the three archetypes external evidence supports are exactly the three the owner added to an inherited set; and the catalogue is structural more than visual, so it is a briefing input as much as a layout one. |
