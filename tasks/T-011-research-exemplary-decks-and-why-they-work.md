---
id: T-011
title: Research exemplary decks and what makes them work
type: research
status: proposed
phase: specify
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
| 1 | Collect candidate decks and slides | shortlist |
| 2 | Reduce each to a transferable move | archetype entries |
| 3 | Test reproducibility in HTML/SVG | feasibility column |
| 4 | Write up | `docs/research/R3-exemplar-decks.md` |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created from the owner's direction to research best-in-class decks. |
| 2026-08-06 | (no change) | Owner answered the exemplar question: no shortlist, selection is ours — but do not confuse a deck's success with its presenter's quality. Added the lone-reader test as a scope exclusion and a fifth acceptance criterion. |
