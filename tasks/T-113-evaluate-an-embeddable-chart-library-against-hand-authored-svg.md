---
id: T-113
title: Evaluate an embeddable chart library against hand-authored SVG, and settle where each is used
type: research
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-057, T-112]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-12
updated: 2026-08-12
deliverables: []
---

# T-113 — Evaluate an embeddable chart library against hand-authored SVG, and settle where each is used

## 1. Specify

**Outcome**
A recommendation with a number behind it: build charts from an embeddable library, from hand-authored
SVG, or from both with a stated rule for which is used when. Whatever the answer, the threshold that
decides it is written down so the next chart does not re-argue it.

**The premise the request came with is false, and correcting it is the first finding**
The feedback asked to *"compare it with your built-in capabilities."* There are none:

```
grep -c -i "chart" shell/components.css        →  0
grep -i  "chart" docs/COMPONENT-CONTRACT.md    →  1 hit, incidental prose inside another rule
```

**DS-146** and **DS-147** both legislate chart behaviour — draw in once, never re-animate on
back-navigation, count up on headline statistics, one emphasis pulse. ~~The component they govern was
never built.~~ **Corrected 2026-08-17 by
[T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md), which was raised on
this same reading and withdrew it.** Both rules are implemented by name in `shell/deck.js` — 410 for
DS-146, 825 for DS-147 — and `examples/reference-deck.html` draws a line chart in hand-authored SVG.
The greps above are right and they are pointed at a stylesheet and a contract, where behaviour is
not (**L-115**). **What is true is that no chart *component* exists, and DS-122 already says one
must not**: *no chart library, hand-written SVG, borrowing scale arithmetic as a few lines.* So the
comparison is not blocked for want of a subject — **it is mostly already decided, against the
library**, and the live remainder is narrower than this task was scoped for: whether *borrowing
scale arithmetic* has a form worth writing down, and what the reference deck's chart already shows
about it. **Re-specify before planning; the honest shape of the question has moved twice.**

**The owner's steer, recorded 2026-08-12**
*"In the recent days I spent too much time on implementing htmldeck's new features, and I learned how
costly the development of a single feature is. So, it's very likely we use some existing embeddable
lib than we start implementing from the scratch. Still, where a single SVG + a little highlight or
anim can be used, we don't need to use a more costly, rich library."*

That is a two-part instruction and both parts are the deliverable: **default to an existing library**,
and **name the threshold below which SVG wins**. A recommendation that answers only the first half
would leave every future chart an argument.

**The gates a candidate has to clear**
Not preferences — each is an existing rule of this project, and a candidate failing any one is out
with a reason rather than a score:

1. **Inlines with zero external references** and keeps the deck inside the measured size bound
   (rule 1, DS-001). 192 KB is what a full 12-slide deck costs today; a library is measured against
   what is left, not against nothing.
2. **A licence that permits redistribution**, recorded next to it — CLAUDE.md, *Publishing
   constraints*.
3. **Drags no framework in.** A charting layer that needs React needs React embedded in every deck.
   This is the gate most likely to decide the answer and it is checked first.
4. **Driven by the theme tokens**, not by its own palette. Rule 4 makes every layer parametric, and a
   chart that themes itself is a second design system inside the deck.
5. **Can be pinned off for capture and honours reduced motion** — DS-221, DS-224, DS-143.
6. **Executes nothing it was not given.** Same posture as T-070's admission tests.

**Scope**
- In: **TanStack Charts**, named in the request. Its documentation, its own comparison page and its
  catalogue are the starting points, and **nothing about it is asserted from memory** — it postdates
  or barely predates the assistant's knowledge cutoff and a recalled fact about it would be a guess.
  <https://tanstack.com/charts/latest> · <https://tanstack.com/charts/latest/docs/comparison> ·
  <https://tanstack.com/charts/catalog>
- In: at least two alternatives, so the recommendation is a comparison rather than a verdict on one
  candidate.
- In: hand-authored SVG as a full candidate, costed honestly — including the interaction the reporter
  actually wants, which is *values appearing on hover*.
- In: the threshold rule. What makes a chart simple enough that SVG wins.
- In: a measured size figure per candidate, inlined, against a real chart — not the vendor's number.
- Out: **building the chart component.** That is this task's expected child, and its shape depends on
  the answer.
- Out: amending DS-146 or DS-147. They stand until something is built that cannot satisfy them.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-001, DS-110, DS-143, DS-146, DS-147,
  DS-221, DS-224.
- [`docs/research/R5-assets-and-licences.md`](../docs/research/R5-assets-and-licences.md) — the
  192 KB measurement and the licence method this reuses.
- [`tools/assets/chart_probe.py`](../tools/assets/chart_probe.py) — an existing probe; establish what
  it measures before writing a second one.
- [`CLAUDE.md`](../CLAUDE.md) rule 3 — *"When SVG is as good, prefer it: it scales, themes and
  diffs."* The threshold rule is that sentence made operable.

**Acceptance criteria**
- [ ] Every candidate has a verdict against all six gates, with the failing gate named where it fails.
- [ ] A measured inlined size for each surviving candidate, against the same real chart.
- [ ] A recommendation, and the threshold rule stated so a future chart can be decided without
      reopening this.
- [ ] The false premise is recorded as a finding, not silently corrected.
- [ ] Nothing about any candidate is stated without a source that was actually fetched.
- [ ] Written to a new research note under `docs/research/` — **R8**, the next free number — and
      referenced from the brief if it changes direction. Declared in `deliverables:` at `specified`,
      per [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6.2.
- [ ] `python tools/docs/refcheck.py` green.

**Open questions**
- Whether the answer changes the brief. If a library is adopted, rule 3's *"never an external
  library"* needs its inline-versus-external distinction restated explicitly, because it currently
  reads as a flat ban and is not one. Surfaced to the owner if it happens.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Record the false premise and the grep behind it | finding 1 |
| 2 | Fetch the three TanStack pages and establish what it actually is | facts, sourced |
| 3 | Pick two alternatives and apply gate 3 first to all three | the shortlist |
| 4 | Inline each survivor against one real chart and measure | size table |
| 5 | Licences, recorded next to each | licence table |
| 6 | Cost hand-authored SVG with hover values, honestly | the fourth candidate |
| 7 | Recommendation and the threshold rule | the R8 note |

## 3. Implement

**Decisions & assumptions**
- 2026-08-12 — owner: default to an existing embeddable library over building from scratch, but keep
  SVG where a chart is simple. Both halves are deliverables.

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- expected: the chart component itself, raised from this task's recommendation

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Created from the first adopting project's feedback on published `0.2.2`. The request assumed a built-in chart capability to compare against; there is none, and the correction is scoped as the first finding rather than as a footnote. |
