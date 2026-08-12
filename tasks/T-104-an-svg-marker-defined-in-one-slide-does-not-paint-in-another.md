---
id: T-104
title: An SVG marker defined in one slide does not paint in another, and four gates stay silent about it
type: admin
status: done
phase: review
shipped_in: 0.2.2
parent: null
blocked_by: []
related: [T-016, T-092]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - docs/DESIGN-SYSTEM.md
  - tools/deck/audit.py
  - tools/deck/check.py
  - tools/deck/static_variants.py
  - skills/htmldeck/references/build.md
---

# T-104 — An SVG marker defined in one slide does not paint in another, and four gates stay silent about it

## 1. Specify

**Where this came from.** The adopting project, re-authoring its deck on v0.2.1. It is `N-8` in that
project's feedback document. **Filed as feedback, not as a defect** — htmldeck does exactly what it
says, and the reader still loses. That distinction is the adopter's own and they keep the two kinds
apart deliberately, because a need filed under a title saying *defect* gets triaged as a bug and
closed by making code match documentation.

**What happened.** A `<marker>` defined inside one slide's `<svg>` and referenced from another slide's
`<svg>` does not render. **Four of five diagrams in the deck shipped with no arrowheads at all**, and
the deck passed every gate on the way out.

## The mechanism

`shell/components.css` sets `.slide{ opacity:0; visibility:hidden }`, with only `.slide[data-current]`
visible. A `<marker>` living inside a hidden slide's `<svg>` is not painted when a visible slide's
`<svg>` references it by `url(#id)`. Every slide but the current one is hidden, so a marker defined
once and reused across slides works on exactly one slide — whichever one happens to be open when the
author looks.

That is browser behaviour, not htmldeck's, and the shell's visibility rule is correct: it is what
makes the slide transition work.

## Why the gates cannot see it

`DS-117` says connectors are labelled always, arrowheads are for directional connectors only, and they
meet their target. It **bans** an arrowhead on an undirected edge. It does not **require** one on a
directed edge — so a flow diagram with no arrowheads anywhere is conformant by the letter, and
`check.py`, `component.py`, `shell.py` and `spec.py` all pass it.

**The failure is invisible to every automatic gate and visible instantly in a rendered shot.** The
adopter found all four only by reading the rendered slides, which is the same instrument that found
seven geometry defects on an earlier build.

## The need

Two things, and the second is the cheap one:

1. **Somewhere an author is told that a `<marker>` must be defined in the slide that uses it**, or
   in a scope that is never hidden. This costs a sentence and it is the whole fix for anyone who reads
   it before building.
2. **A directed connector with no arrowhead is worth a verdict.** DS-117 already knows the concept of
   a directional connector; the rule stops one step short of the case that actually shipped.

**Scope**
- In: deciding where the authoring note belongs — `build.md`, the design system beside DS-117, or the
  component contract.
- In: whether DS-117 gains a *requires* half, and whether it is `auto` or `render`.
- Out: changing the shell's visibility rule. It is correct and it is what makes the transition work.
- Out: the adopter's fix. They moved each marker into the slide that uses it and re-shot every slide.

**Acceptance criteria**
- [ ] An author following the documentation cannot define a cross-slide marker without being warned
- [ ] A decision is recorded on whether a directed connector with no arrowhead is a verdict, and if
      not, why the render gate is enough

**Open questions**
- **Whether this is checkable cheaply.** A marker referenced by `url(#id)` from one slide and defined
  in another is a static-text comparison, so it may be `auto` rather than `render`. — the project
  owner

## 2. Plan

**Phase: `PH3`.** Not a defect in the published plugin — nothing here behaves against what it says —
so by `CLAUDE.md`'s rule it is not `PH1`, and PH2 is shipped. Derived here; the task arrived with
`work_package: none`.

**The open question is answered: cheap, and `auto`.** A `url(#id)` in one slide and an `id=` in
another is a static text comparison over the file, so no render is needed.

**DS-117 stays as written.** Its *requires* half was the rival and was rejected: whether a connector
is directional is not decidable from markup, so requiring an arrowhead on one makes DS-117 a `judge`
rule and buys nothing mechanical. The rule that catches what shipped is a different claim — a
reference that resolves nowhere visible — and it is decidable exactly.

| # | Step | Where |
| :--- | :--- | :--- |
| 1 | The rule, `hard` / `auto` / gated | `DESIGN-SYSTEM.md`, after DS-231 |
| 2 | The check, with a denominator in its text | `audit.py` |
| 3 | Collect the row in the gate and in the variant suite | `check.py`, `static_variants.py` |
| 4 | Register the absent subject | `ABSENCE_IS_A_PASS` |
| 5 | The authoring sentence, which is the whole fix for anyone who reads it | `build.md` §2 |
| 6 | A seeded variant, so the rule is seen refusing a real deck | `static_variants.py` |

## 3. Implement

**DS-232**, `hard` / `auto` / gated: an SVG paint reference resolves inside the slide that paints it.
Its row names the mechanism — every slide but the current one is `visibility:hidden` — and the fix:
define it in the slide that uses it, or outside every slide where the sprite already lives.

**Only paint references count, and only cross-slide ones.** `url(#id)` and `<use href="#id">` are the
two ways an SVG names something to draw with; matching every `#` would report `<a href="#x">`, which
is navigation and resolves whatever is hidden. And the test is *defined in a **different** slide*
rather than *not defined here*, or every `<use href="#i-source">` in every deck would fail — the
sprite sits outside the slides on purpose.

**The row prints its own denominator**, like DS-231 and DS-105 beside it: `0 of 47` and `0 of none`
read identically as a bare boolean, and a deck with one slide has pointed nowhere.

**One collision, worth recording.** The new regexes shadowed `SLIDE_BLOCK`, which `split_data` uses
with a capture group, and DS-231 died with `IndexError: no such group` — caught by running the gate
rather than by reading. The existing pattern is now reused.

## 4. Review

| Criterion | Verdict | Evidence |
| :--- | :--- | :--- |
| An author following the documentation cannot define a cross-slide marker without being warned | **met** | `build.md` §2's third bullet, beside the token rule, and DS-232's own row |
| A decision is recorded on whether a directed connector with no arrowhead is a verdict | **met** | §2 above: no. *Directional* is not decidable from markup, so DS-117 would become `judge`. DS-232 catches the case that shipped, mechanically |

**Seen refusing.** `marker-defined-in-another-slide` points slide 4's arrow at slide 9's marker —
one string, nothing else moved, the connector still directional and labelled — and the suite reports
`marker-defined-in-another-slide breaks DS-232 -> CAUGHT`. 25 of 25 static variants caught, 7 of 7
rendered, 2 of 2 reduced-motion.

**The rule count moved and four pasted figures with it**: 164 rows to 165, 114 owned to 115, 83
checked to 84, 118 hard to 119. `figures.py` caught every one, which is the release sequence's step
3 working on the day the rule landed rather than at the next release.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Filed from the adopting project's feedback document, `N-8`. Kept as feedback rather than a defect: DS-117's letter is satisfied by a diagram with no arrowheads, so the plugin behaves as documented. Re-verified against `shell/components.css` on `master` before filing — `.slide` still carries `visibility:hidden`, and only `[data-current]` is visible. |
| 2026-08-12 | → done | Phase derived as `PH3` — feedback rather than a defect, and PH2 is shipped. The open question was answered *checkable cheaply*, so this shipped a rule and a check rather than only a sentence: **DS-232**, `auto`, with a seeded variant. DS-117 is unchanged, and §2 records why its *requires* half was rejected. |
| 2026-08-12 | (no change) | Shipped in `0.2.2`, 2026-08-12. Named in the release's *what stops conforming* row: `DS-232` newly fails a deck with a cross-slide marker. |
