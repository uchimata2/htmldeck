---
id: T-021
title: Build the reflow view and enforce the resolution contract
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-002, T-005, T-007, T-014, T-016, T-018]
work_package: WP2
owner: maintainer
created: 2026-08-06
updated: 2026-08-07
deliverables: []
---

# T-021 — Build the reflow view and enforce the resolution contract

## 1. Specify

**Outcome**
The **reflow view** exists as a second rendering of the same deck — off by default, reachable by a
persistent control, carrying every piece of content the stage carries — and the **resolution
contract** in [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §2.4 is enforced rather than
merely written down. Together they close the one thing T-014 could not settle alone.

**Why this one**
Two failures the owner has actually hit, and neither is hypothetical:

1. **A deck built for small screens breaks when opened on a 4K display.** Breakpoints land in a
   bucket nobody designed, `max-width` containers leave dead gutters, absolutely-positioned
   decoration drifts.
2. **A deck presented from a high-resolution monitor arrives illegible**, because Zoom, Meet and
   Discord re-encode the shared screen at 1080p or 720p and the text goes down with the frame.

§2.4 shows the second has an arithmetic answer: **under a uniformly scaled stage the presenter's
viewport cancels out**, so stream legibility depends only on the design size and the call's
resolution. That is why the stage is `hard` and why no responsive presentation layout is acceptable.
**This task is the other half** — the floor is met by a view the presenter never sees.

**Scope**

- In: the **reflow view** — a one-column document rendering in `rem`, honouring user font size and
  `--measure`, with no two-dimensional scrolling at 320 CSS px.
- In: the **switch** — persistent, visible, keyboard-operable, position-preserving in both
  directions, and **never engaging in fullscreen or while a presentation control is active**.
- In: **auto-engage below 960 CSS px** of viewport width, where the stage puts body text under 12 px.
- In: **tier-two content is present in the reflow view.** A view missing the disclosure content is
  not a conforming alternate version; it is a lossy summary.
- In: the **resolution-contract checks** — §11 conditions 13–19, and condition 17 above all: render
  at 3840×2000 and 1280×634 and diff up to a uniform scale factor.
- In: confirming the conformance wording the deck ships with — *AA via a conforming alternate
  version reachable by a persistent control*, never a bare "this deck is AA".
- Out: the stage itself. That is T-002's, built to §2.4.
- Out: printing. A separate opt-in mode, and **not** the same thing as the reflow view — though the
  two may share the document rendering, and whether they should is an open question below.
- Out: mobile as a first-class target. The Portability decision keeps mobile secondary; auto-engage
  is what a phone gets, and that is deliberate.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §2.4, §2.5, §7, §9.1, and §11 conditions 13–19.
- [`docs/research/R6-portability-contract.md`](../docs/research/R6-portability-contract.md) — what
  `file://` permits, including view transitions.
- [`docs/BRIEF.md`](../docs/BRIEF.md) open question 7, which this task closes.

**Acceptance criteria**
- [ ] The reflow view renders every slide's tier-one **and tier-two** content, verified by counting
      elements against the stage rendering — not by reading
- [ ] No two-dimensional scrolling at 320 CSS px equivalent
- [ ] The switch is keyboard-operable, visible without hover, and preserves position both ways
- [ ] The switch **cannot** fire in fullscreen, demonstrated
- [ ] Auto-engage triggers below 960 CSS px and **not** at 1280 CSS px — the 150%-scaled FullHD
      laptop stays on the stage
- [ ] **Condition 17 demonstrated:** the same deck rendered at 3840×2000 and 1280×634 is identical
      up to a uniform scale factor
- [ ] **A real 12-slide deck opened offline on a large display and on a 1080p display**, and looked
      at in both — CLAUDE.md rule 6, and the whole point of this task
- [ ] Body text measured at ≥ 16 px in a 720p capture of the presented deck, or the design-unit floor
      revised with the measurement that showed why
- [ ] The shipped conformance wording states the alternate-version route explicitly

**Open questions**
- **Do the reflow view and the print stylesheet share one document rendering?** They want most of
  the same things — one column, normal flow, all content present. Sharing halves the work and
  couples two modes with different owners. — this task, once the reflow view exists
- **Does the reflow view need the interaction layer at all, or does it inline tier two?** Inlining is
  simpler and matches "a document rendering"; keeping the disclosure preserves the reading rhythm
  and the two-tier structure. §5.3's rules are written for the stage. — this task, with T-016
- **Is 960 CSS px the right threshold, or should it key off the computed scale factor instead?**
  Scale is the thing that actually matters and width is a proxy for it. — this task

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle the three open questions above against a real deck, not in the abstract | decisions recorded in §3 |
| 2 | Build the document rendering and the switch | the reflow view |
| 3 | Implement §11 conditions 13–19 as checks, condition 17 first — it is the cheapest and catches the whole "broken on my monitor" class | checks, handed to T-005 |
| 4 | Verify on a real 12-slide deck at both resolutions, offline, and in a 720p capture | measurements in §4 |

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
| 2026-08-07 | (no change) | `related` gains [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md), the measurement that answers this task's shared-rendering open question. [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) also **flags this specification as partly satisfied**: the row below records a reflow view already carrying all tier-two content, `scrollWidth` 320 at 320 CSS px and position preserved both ways, so three of the acceptance criteria are demonstrated on one deck. What remains is the fullscreen suppression, the auto-engage threshold, condition 17, the 720p body-text measurement, the conformance wording — and the **enforcement**, which is the half the title names and the half that does not exist. Flagged, not rewritten; the rewrite is the owner's call. |
| 2026-08-06 | (no change) | **A working reflow view now exists** in [`examples/reference-deck.html`](../examples/reference-deck.html), built by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) because without it the deck fails its own hard rules and the convergence loop is meaningless. Measured: 12 sections carrying all tier-two content, `scrollWidth` **320** at 320 CSS px with zero elements overflowing, position preserved in both directions, panels open and their controls removed. **This task now specifies against a real implementation rather than in the abstract** — and two defects it already surfaced are worth carrying: the stage's absolutely-positioned, fixed-width disclosure panel cannot reflow until both are undone, and an inline `font-size` on a headline outranks the reading view's own type scale. |
| 2026-08-06 | → proposed | Raised out of [T-014](T-014-synthesise-research-into-the-design-system-reference.md) §9.1, which the owner settled the same day: keep the fixed stage, add a reflow view. Created because a mode is built, not asserted. **The owner's reason for the stage reshaped the design system rather than only answering the question** — the screen-share arithmetic in §2.4 produced a type floor (body ≥ 24 design units) that no research note had, tightened D5's 18–24 range to 24–28, and demoted the corpus's mono labels to decoration because they are illegible at 720p. |
