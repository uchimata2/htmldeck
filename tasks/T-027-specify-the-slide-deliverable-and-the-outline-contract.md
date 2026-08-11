---
id: T-027
title: Specify the slide deliverable and the outline contract, and the rules the owner's deck review implies
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-002, T-003, T-005, T-020, T-024, T-025]
work_package: WP2
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables:
  - docs/DESIGN-SYSTEM.md
  - docs/DESIGN-RATIONALE.md
---

# T-027 — Specify the slide deliverable and the outline contract

## 1. Specify

**Outcome**
`docs/DESIGN-SYSTEM.md` gains the two things the owner's review showed it was missing: a **content
contract for what a slide must deliver**, and the **outline** that has to exist before any slide
does. Plus the rules implied by four defects the owner found by looking at the reference deck that
every mechanical check had passed.

**Why this one**
The ruleset had 131 rules about how a deck should *look* and *argue*, and **nothing at all about the
one thing every slide owes its audience.** The owner's phrasing is the specification:

> *Each slide needs to deliver something. The key deliverable should not be hidden in a list or
> prose. Make it stand out… So they don't need to wait for the presenter to finally say the essence,
> the point of the current page.*

**This is not new taste — it is recorded taste the synthesis dropped.** The corpus knowledgebase
carries it in three independent places, and T-014 carried none of them into the design system:

- The build process specifies each slide by **structure, text, visuals, animations, interactive
  elements, title, and _bottom line_.** The bottom line is a named, required element per slide.
- Feedback on a real deck: ***"Bottom line repeats content. Keep only the key message here, no
  reasoning."*** So the bottom line is the deliverable, not a summary.
- Feedback on another: ***"Show the details here, do not hide them under the click."*** Disclosure is
  for depth. It may not be where the point lives.
- The writing standard: plain, simple English, because ***"the reader may not be a native speaker and
  no sentence should need a second pass."*** This is the source of the owner's "avoid English native
  expressions", and the design system had only the jargon half of it (DS-097).

**The four defects, all confirmed by measurement**

| # | The owner saw | Measured |
| :-- | :--- | :--- |
| 1 | *"decreasing window size pushes the slide out of the visible area"* | **Confirmed, and worse than described.** At a 1578 px viewport the stage renders at `left:171, width:1578` — it overflows the right edge by exactly its left margin. `transform: scale()` does not change layout size, so the grid track sizes to the **unscaled** 1920 px box and start-aligns it; the scale then happens about a centre that is no longer the viewport's. |
| 2 | *"the bottom navigation area … extremely noisy with that many dots"* | **Confirmed.** Three separate encodings of position — spine ribbon, one dot per slide, progress bar — 23 labelled or interactive items in 96 design units of chrome. |
| 3 | *"texts colliding or overflown each other"* | **Not reproduced as text-on-text collision.** A pairwise overlap test over every rendered text run on all 12 slides found none. What the owner saw is almost certainly defect 1 clipping content at the right edge. Recorded as unreproduced rather than fixed silently. |
| 4 | *"Slide 11 — texts are almost invisible … black on dark blue"* | **Confirmed at 2.17:1.** `--ink` on `--accent`. The colour was written as an SVG **presentation attribute** (`fill="var(--paper)"`) and silently overridden by a CSS class rule (`.fig .val{fill:var(--ink)}`) — **CSS always outranks presentation attributes.** |

**Defect 4 is the important one, because of how it escaped.** `tools/deck/contrast.py` passed the
deck with zero failures while a 2.17:1 run was on screen: it audits **the token pairs the palette
intends**, not the colours that actually render. That is DS-191 word for word — *DOM measurement
confirms geometry you suspect; it cannot find a defect you never thought to measure.*

**Scope**
- In: a **deliverable contract** — one deliverable per slide, stated as a bottom line, visually
  dominant, factual, never behind a disclosure.
- In: the **outline** and what it must name per slide, as a property of a good deck. Where the
  outline sits in the pipeline stays [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md)'s.
- In: the **non-native-reader constraint on idiom**, which DS-097 covers only for jargon.
- In: rules for defects 1, 2 and 4; defect 3 recorded as unreproduced.
- In: the owner's ruling on the type floor — **16 design units is acceptable** — which settles
  [T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md)'s F-01.
- In: extending `tools/deck/` to check rendered colour rather than intended colour.
- In: repairing the two defects in the shipped reference deck that make it a poor example (1 and 4).
  The owner did not ask for this; a published example failing the project's own hard rules is not
  one worth shipping.
- Out: rewriting the reference deck's content to the new contract. The deck predates it, and
  retrofitting a bottom line to twelve slides is a separate piece of work — raised as T-028.
- Out: the remaining F-02 to F-13 findings. Those stay T-025's.

**Inputs**
- The owner's review, this session — the four defects and the deliverable requirement
- The corpus knowledgebase, `sources/written-conventions.md` §S2 and `written-conventions-2.md`
  §S5, §S7, §S10 — **local, gitignored, and not quotable into the repository beyond the patterns
  above**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) · [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md)
- [`T-024`](T-024-build-the-reference-deck-and-validate-the-ruleset.md) §3.3 — the findings this sits beside

**Acceptance criteria**
- [ ] A deliverable contract exists in `DESIGN-SYSTEM.md`, with IDs, labels and a `Check` column
- [ ] The outline's required contents are stated, and the pipeline question is left to T-020
- [ ] The idiom rule is stated separately from the jargon rule, and says why
- [ ] Defects 1, 2 and 4 each produce a rule; defect 3 is recorded as unreproduced with its evidence
- [ ] The type floor is amended to 16 design units and F-01 marked settled on T-025
- [ ] `tools/deck/` checks **rendered** foreground against **rendered** backdrop, and catches defect 4
- [ ] The reference deck passes its own gate again after the repairs
- [ ] `python tools/tasks/task.py check` passes

**Open questions**
- None blocking. The owner's review settled the type floor and the deliverable requirement directly.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Mine the knowledgebase for every recorded note on per-slide content structure | the bottom-line evidence, above |
| 2 | Measure all four reported defects rather than accepting or dismissing them | the table in §1 |
| 3 | Write the deliverable contract and the outline contract into `DESIGN-SYSTEM.md` | new rule block |
| 4 | Write the four defect rules, and amend the type floor | amended ruleset |
| 5 | Record every "why" in `DESIGN-RATIONALE.md` | the rationale |
| 6 | Extend the audit to rendered colour, and repair the deck's two real defects | a passing gate |

## 3. Implement

**Decisions & assumptions**
- **New rules take a fresh `DS-200` block rather than squeezing into their section's number
  range — 2026-08-06.** IDs are permanent and unique; contiguity per section is a nicety, and the
  ranges around §3 and §5 have no room. A fresh block also makes it obvious at a glance which rules
  arrived after the first deck was built.
- **The type floor moves to 16, not to "whatever DS-036 said" — 2026-08-06.** The owner's ruling is
  explicit. The floor stays a floor; it is the number that changes. DS-036's mono range becomes
  reachable, which is what made F-01 a conflict.
- **Defect 3 is recorded as unreproduced, not fixed — 2026-08-06.** Reporting a fix for something
  never observed would be inventing a result, and the likely cause (defect 1) is being fixed anyway.

**Outputs produced**
- `docs/DESIGN-SYSTEM.md` — §2.4 DS-200, §3.4 and §3.5 DS-201–DS-211, §4 DS-212, §5.1 DS-213–DS-214,
  amended DS-035 and DS-036
- `docs/DESIGN-RATIONALE.md` — the reasoning and the provenance for each
- `tools/deck/audit.py` — rendered-colour contrast check
- `examples/reference-deck.html` — defects 1 and 4 repaired

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deliverable contract exists, with IDs, labels and a `Check` column | **met** | `DESIGN-SYSTEM.md` §3.4, DS-201–DS-209. Promoted into §0 as principle 0, because the rest of §3 serves it. |
| The outline's required contents stated, pipeline left to T-020 | **met** | §3.5, DS-210–DS-213, with the pipeline question pointed at T-020 in the section header |
| The idiom rule is separate from the jargon rule, and says why | **met** | DS-208 beside DS-097. The reason is in `DESIGN-RATIONALE.md`: a reader can look a term up and cannot look up an idiom they have misread as literal. |
| Defects 1, 2 and 4 each produce a rule; 3 recorded as unreproduced | **met** | DS-200 (stage centring) · DS-216, DS-217 (chrome) · DS-214, DS-215 (rendered colour). Defect 3 recorded in §1 with the evidence that it was looked for. |
| Type floor amended to 16, F-01 marked settled | **met** | DS-035 amended; rationale §3 carries the ruling and the 11 px caveat; T-025's open question closed. |
| `tools/deck/` checks rendered colour, and catches defect 4 | **met** | DS-214 and DS-215 checks added. Against the deck before repair they reported **28 dead `fill=` attributes** and the 2.17:1 run; after, both report 0. |
| The reference deck passes its own gate again | **met** | `audit.py`: 0 mechanical failures. Stage measured at `left:0` at six viewport widths from 1898 down to 978, previously clipping at every one. |
| `task.py check` passes | **met** | see the log row |

**What the fix turned up that the owner's report did not.** Defect 4 looked like one bad slide. It
was **28 dead `fill=` attributes across seven slides** — every accent-coloured label in every diagram
had been rendering as plain ink since the deck was built. Slide 11 was simply the only place where
the backdrop was dark enough to make it visible. **A rule the deck appeared to follow (DS-021, the
accent carries meaning wherever it appears) it had never once followed**, and three separate review
passes plus a palette audit reporting zero failures had all missed it.

**Child fix tasks raised**
- [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) — retrofit the reference
  deck to the deliverable contract

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → done | All eight criteria met. **The four defects produced six rules; the missing deliverable contract produced thirteen.** The repair found the real scope of defect 4: not one bad slide but 28 dead `fill=` attributes across seven, so no accent emphasis in any diagram had ever rendered. Chrome density is a `default` rule and a rewrite rather than a fix, so it goes to [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) with the bottom-line retrofit. |
| 2026-08-06 | → in_progress | Raised from the owner's review of the reference deck. Four defects, all measured — three confirmed, one unreproduced and recorded as such. **The larger finding is not a defect: the ruleset had 131 rules and none of them said what a slide owes its audience.** The corpus had that recorded in three places as the per-slide *bottom line*, and the synthesis dropped it. |
