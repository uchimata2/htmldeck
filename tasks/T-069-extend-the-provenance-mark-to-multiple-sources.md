---
id: T-069
title: Extend the provenance mark to multiple sources, and decide where deck-wide sources go
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-016, T-070]
work_package: v0.2
owner: the project owner
business_value: high
effort: m
created: 2026-08-10
updated: 2026-08-10
deliverables: []
---

# T-069 — Extend the provenance mark to multiple sources, and decide where deck-wide sources go

## 1. Specify

**Outcome**
`DS-105` and the `.provenance` component carry **more than one source per slide**, and a deck-wide
source that belongs to no single slide has a stated home. What exists today handles exactly one
source and says nothing about the rest.

**Why this one**
Requested by the owner on 2026-08-10. **Most of the request is already a rule** — DS-105 puts the
mark upper-right, requires a working link where sources are reachable and plain text where they are
not, and forbids a dead link; `COMPONENT-CONTRACT.md` §3 contracts `.provenance` as a `p` inside
`.slide`, cardinality exactly `1`, author-supplied; the reference deck carries twelve. So this task
is the delta, and the delta is four things, three of which collide with a rule already in force.

**The delta**
1. **Multiple sources behind a disclosure** — an icon opening a box, one linked title per source.
   Nothing today: the cardinality is exactly `1` and the element is a paragraph.
2. **A link affordance on the title.** Constrained rather than free: **DS-112 forbids a hand-drawn
   icon and DS-113 allows only glyphs the sprite carries.** The sprite has no `link` and no
   `external-link`. It does carry `arrow-up-right`, which is Lucide's conventional external-link
   mark, and `file-text` for a document. Either is legal; a new glyph means adding it to the sprite
   and is a DS-113 question, not a free choice.
3. **A deck-wide source lands on the last slide if it was not cited earlier.** This is the collision
   below.
4. **The link target may be a local file, an external URL, or an embedded quick view.** The quick
   view is its own capability and its own task —
   [T-070](T-070-the-quick-view-for-a-source-document.md) — because it is a build-mode feature
   rather than a rule. **The local-file case is settled here**, because it is a rule question:
   see *Decided*, below.

**What it collides with**
- **DS-085** — *"The last slide is a **close, not a recap**: the ask as one action."* Putting a
  source list on the last slide contradicts it directly. This needs a decision, not a workaround.
- **DS-230** — tier-two disclosure is **four closed kinds** (`derivation`, `scope`, `condition`,
  `instances`), and *"content whose subject the face does not carry is a slide, not a panel"*. A
  multi-source box is arguably none of the four, and a deck-wide bibliography's subject is not on
  the close slide's face. So either the source box is **not** a `.disc` and is its own component, or
  DS-230 gains a fifth kind — which DS-000 says is a ruleset change with a stated reason, never a
  value invented in one deck.
- **`COMPONENT-CONTRACT.md` §3** — `.provenance` is cardinality exactly `1`. Any multi-source form
  changes that row, and **DS-229** requires every class the shared style block styles to have one.

**What is already true and must not regress**
- **The gate checks presence, not reachability.** `check.py`'s triage for DS-105 reads *"the
  provenance mark is present on every slide; never a dead link is excused"*. So the half this
  request cares most about — that the link works — is the half nothing gates today. Whatever this
  task produces, *never a dead link* should stop being excused.
- **DS-223** already gives the provenance line print behaviour as an absolutely positioned
  descendant of a relative slide. A disclosure box inherits that problem and does not inherit its
  answer.

**Decided here, on rule 1's existing precedent**
**A `file://` link to a local source document is an authoring form, not a shipping one** — the same
status a CDN reference already has. `CLAUDE.md` rule 1 says a deck is one file that renders with the
network disabled and that the recipient double-clicks; a link into the author's own filesystem is
dead the moment the deck is emailed, and DS-105 already says *never a dead link*. So it is legal
while authoring and **a defect in a delivered deck, and the critique pass says so**, exactly as
`linked` mode is today. An external URL stays legal: it needs network to *follow*, not to *render*,
and DS-001 is about rendering.

**Scope**
- In: DS-105's text, the `.provenance` contract row, and whichever new component the multi-source
  form needs.
- In: the DS-085 decision, and the DS-230 fifth-kind-or-own-component decision.
- In: un-excusing *never a dead link* in the gate, to whatever extent a check can reach it.
- Out: the quick view — [T-070](T-070-the-quick-view-for-a-source-document.md).
- Out: adding a glyph to the sprite, unless the decision in delta 2 requires one; then it is in.
- Out: DS-102, which is about figures being sourced and is a different rule with a different subject.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-105, DS-085, DS-230, DS-112, DS-113,
  DS-223, DS-229, and DS-000 on what changing a rule costs.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3 — the `.provenance` row.
- [`shell/icons.svg`](../shell/icons.svg) — the 37 glyphs available without a DS-113 change.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — twelve marks in the shipping
  form, which is what any change has to keep working.

**Acceptance criteria**
- [ ] DS-105 states the multi-source form, and the ruleset says which component carries it
- [ ] The DS-085 collision is resolved **in the ruleset**, not in a deck — either the close slide
      keeps its rule and deck-wide sources go somewhere named, or DS-085 is amended with a reason
      under DS-000
- [ ] Every class the new form styles has a `COMPONENT-CONTRACT.md` row (**DS-229**)
- [ ] *Never a dead link* is checked rather than excused, or the gate states in writing which part
      of it no check can reach and why
- [ ] The reference deck still passes with its twelve single-source marks unchanged — this extends
      the rule, it does not replace it
- [ ] A deck carrying the multi-source form renders glitch-free offline and prints without the box
      scattering across a page break (**DS-223**)

**Open questions**
- **Settled 2026-08-10 by the owner — a deck-wide source goes on a colophon slide *after* the close,
  exempt from DS-085 by name.** DS-085 keeps its rule and its subject: *the last slide is a close,
  not a recap* is a statement about where the **argument** ends, and a colophon is not part of the
  argument. So the amendment is an exemption naming the colophon, not a weakening of the rule — and
  the ask stays the last thing an audience is asked to act on, which is the property DS-085 exists
  to protect. Under DS-000 this is a ruleset change and carries this reason.
  **What the exemption must not become:** a second ending. The colophon carries sources and nothing
  else, or DS-085 has been repealed by the back door and every deck grows an appendix.
- **Settled 2026-08-10 by the owner — the multi-source box is its own component, not a `.disc`.**
  DS-230's four kinds (`derivation`, `scope`, `condition`, `instances`) describe an argument's tier
  two, and **provenance is not an argument** — it is what the argument rests on. Bending the
  vocabulary to admit it would cost the closed-vocabulary property that stops *behind the click*
  becoming *wherever it did not fit*, which is the whole reason DS-230 is closed. A separate
  component also keeps DS-230's gate honest: a source box counted as a panel would appear in every
  tier-two census and make the panel-kind distribution meaningless.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- none yet

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | (specify) | **Both open questions settled by the owner**, as recommended: a colophon slide after the close carries deck-wide sources under a named DS-085 exemption, and the multi-source box is its own component rather than a fifth DS-230 kind. Both reasons are written into §1 — the exemption is scoped so the colophon cannot become a second ending, and the separate component keeps DS-230's panel census meaningful. Specify is not closed: the criteria still need agreeing. |
| 2026-08-10 | → proposed | Raised from an owner request for upper-right source referencing. **Recorded as a delta rather than as the request**, because DS-105 already puts the mark upper-right, already requires a working link or plain text, and already forbids a dead link — the reference deck carries twelve. What is genuinely new is multiple sources, the disclosure that holds them, and where a deck-wide source lives. **Three collisions named before any work**: DS-085 on the last slide being a close, DS-230's closed four-kind panel vocabulary, and the `.provenance` cardinality of exactly 1. The local-file link is settled here on rule 1's existing precedent rather than left open. `v0.2`: nothing shipped is wrong, and this is a capability rather than a defect. |
