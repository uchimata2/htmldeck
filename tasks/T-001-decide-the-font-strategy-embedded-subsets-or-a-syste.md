---
id: T-001
title: Decide the font strategy: embedded subsets or a system stack
type: decision
status: done
phase: review
parent: null
blocked_by: [T-013]
related: []
work_package: WP2
owner: maintainer
created: 2026-08-04
updated: 2026-08-06
deliverables: []
---

# T-001 — Decide the font strategy: embedded subsets or a system stack

## 1. Specify

**Outcome**
A decided approach to typography that keeps decks self-contained.

**Why this one**
**This decides how the decks look and blocks the build mode.** Every deck in the source corpus carries 2–7 external references, mostly web fonts — none renders correctly offline. Typography is also what makes those decks look designed rather than generated, so the trade-off is identity against self-containment.

**Acceptance criteria**
- [x] Option chosen with the reason recorded
- [x] If embedding: licences permit redistribution, and each is recorded next to its font
- [x] A deck built with the chosen approach renders correctly **with the network disabled**
- [x] File size of a 12-slide deck measured and stated

**Open questions**
- ~~Is a curated system-font stack distinctive enough to avoid the template look?~~
  **Answered 2026-08-06: no, and the question stopped mattering.** A system stack *is* the
  template look — it resolves to Segoe UI, San Francisco or Roboto depending on the machine, which
  means the deck's typography is decided by the recipient's OS rather than by the author, and
  changes between viewers. It was only ever a candidate because embedding was assumed expensive.
  [R5 §1](../docs/research/R5-assets-and-licences.md) measured that assumption false.

## 2. Plan

The decision was already evidenced by T-013 before this task started, so the plan is to rule on
it, not to re-research it.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Rule on the option, against R5's measurements | the decision below |
| 2 | Confirm each acceptance criterion against evidence that already exists | §4 |

## 3. Implement

**Decisions & assumptions**
- **Embedded subsets. Decided 2026-08-06.** The trade-off this task was created to resolve —
  identity against self-containment — **does not exist at the measured prices.** Both premises
  behind "or a system stack" were wrong: the files are not large (27–76 KB inlined per face, 97 KB
  for a three-face identity, in a 192 KB deck) and the licences are not doubtful (every candidate
  is SIL OFL 1.1, which permits redistribution). A system stack gives up authored typography to
  save bytes that were never scarce.
- **The face set: Instrument Serif (display) · Space Grotesk (text) · JetBrains Mono (figures).**
  97.3 KB inlined, measured in the probe deck. Fallback if a lighter identity is wanted: Figtree +
  Instrument Serif, 53.6 KB.
- **Inter is rejected, deliberately** — 2026-08-06. It is the most expensive text face measured
  (62.8 KB, more than twice Instrument Serif) and the least distinctive: it is the face every
  generated deck already uses. R4 found the corpus's named faces were rows of the source deck
  skill's pairing table rather than the owner's choices, so there is nothing to preserve by
  keeping it. Buying ubiquity is the opposite of this project's purpose.
- **Prefer variable fonts** — 2026-08-06. One file covers a whole weight range: Space Grotesk is
  400–700 in 29 KB, while static IBM Plex Sans needs 59.5 KB for two weights. This removes the
  size argument for a single-weight design.
- **No deck-specific subsetting yet** — 2026-08-06. Below Google's latin subset it needs a
  font-tooling dependency, which L-07 forbids in project tooling. At 97 KB there is no incentive.
  Revisit only if a deck ever approaches a size that matters.
- **The OFL notice is emitted by the build, not remembered by the author** — 2026-08-06. OFL 1.1
  requires the licence to travel with the font; for a `data:` URI that means an HTML comment
  carrying the copyright line and licence reference beside each `@font-face`. This is a build-check
  item, so it becomes an input to T-005.

**Outputs produced**
- No document of its own — this task is a decision, and its evidence is
  [`docs/research/R5-assets-and-licences.md`](../docs/research/R5-assets-and-licences.md) §1.
  The decision is recorded here and carried into `docs/DESIGN-SYSTEM.md` by T-014.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Option chosen with the reason recorded | **Met** | Embedded subsets; §3. The reason is that the trade-off the option list assumed is not real at measured prices |
| If embedding: licences permit redistribution, and each is recorded next to its font | **Met, with a build obligation** | All candidates are SIL OFL 1.1, verified from source (R5 §1). Recording the notice beside each `@font-face` is specified above and handed to T-005 as a build-check item |
| A deck built with the chosen approach renders correctly **with the network disabled** | **Met** | The probe deck opened from `file://`, no server: 0 external references, `document.fonts.status === "loaded"` with all 3 embedded faces, 12 slides looked at (R5 §7) |
| File size of a 12-slide deck measured and stated | **Met** | **191.8 KB** total, of which 97.3 KB is the three faces. Itemised in R5 §7 |

**Child fix tasks raised**
- none. One obligation is handed on rather than raised as a task: **T-005** (build check) must
  verify the OFL notice is present beside every embedded face, since a licence condition that
  depends on the author remembering is a licence condition that will be breached.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-06 | → done | Unblocked and answered in the same session that closed T-013 — the evidence was produced by that task, so this one ruled rather than researched. **Embedded subsets**, three faces at 97.3 KB in a 192 KB deck, all OFL 1.1. The task's own framing turned out to be the finding: "identity against self-containment" was a false trade-off, resting on an unmeasured assumption that embedding is expensive. Inter rejected on cost *and* distinctiveness. |
