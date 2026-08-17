---
id: T-175
title: The published example's colophon is filed as an argument slide, so it takes a stage's kicker, mark and census
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-128, T-108, T-123, T-068]
work_package: PH1
shipped_in: 0.3.0
owner: the project owner
business_value: high
effort: xs
created: 2026-08-17
updated: 2026-08-17
deliverables:
  - examples/measure-first/measure-first.html
  - examples/README.md
---

# T-175 — The published example's colophon is filed as an argument slide

## 1. Specify

**Outcome**
`examples/measure-first/measure-first.html`'s colophon presents the way this plugin presents back
matter, on the slide and on the printed contents sheet. Today it presents as a third *Decision*
slide.

**Found by looking at the printed contents sheet, 2026-08-17**, after
[T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) published the deck. Card 13 reads
`13 · DECISION` with the Decision stage's flag icon. The reference deck's card 13 reads
`13 · BACK MATTER` with no icon.

**The mechanism is one attribute, and the shell already states the rule.** The colophon declares
`data-stage="4"`, the same stage as slides 11 and 12:

| Deck | stages, in order |
| :--- | :--- |
| [`examples/reference-deck.html`](../examples/reference-deck.html) | `0 1 2 2 3 3 4 4 4 5 5 6 **back**` |
| [`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html) | `0 0 1 1 1 1 2 2 3 3 4 4 **4**` |

[`shell/deck.js`](../shell/deck.js) `manifest()` reads `data-stage="back"` and returns
`stageName: 'Back matter'`, `icon: null`, `stage: null`. Its comment is this defect written down
before it happened: *back matter was pushed into the nearest stage and every rendering of the census
inherited the miscount*. That is
[T-108](T-108-a-deck-has-no-back-matter-stage-so-the-colophon-is-labelled-with-the-last-argument-stage.md)'s
work, and the deck predates it — it was built on 0.2.2 and its author had no way to know.

**Three things follow from the one attribute, and the third is the one no reader would guess.**

1. the printed contents card takes `DECISION` and the flag icon;
2. the on-slide eyebrow carries a **mark** — `<use href="#i-sources">` — where DS-113/114 key the
   mark to the stage and back matter has none. The shell's comment: *it carries NO MARK … so the
   absence is the rule holding*;
3. **the Decision stage is credited with three slides when it argues two.** The ruler, the census
   and the stage runs all inherit it. This is the miscount, and it is invisible on the slide face.

**Why this is `PH1` and this project's to fix.** The owner ruled it 2026-08-17: the file is no
longer the adopter's, it is **this package's example deck**, and an example ships presenting the way
the plugin intends. A published example that files its colophon wrongly teaches every reader who
copies it to do the same.

**Scope**
- In: the colophon's `data-stage`, its eyebrow mark, and its eyebrow label.
- Out: the colophon's content — the five documents, their names and the bottom line all stay.
- Out: changing the shell. The mechanism exists and works; this deck did not use it.
- Watch: the eyebrow's `<span class="tick">` and the `rise` entrance classes the other slides carry —
  match the reference deck's colophon rather than inventing a third form.

**Inputs**
- [`examples/reference-deck.html`](../examples/reference-deck.html)'s slide 13 — the intended form.
- [`shell/deck.js`](../shell/deck.js) `manifest()` and `BACK_MATTER`.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) DS-113, DS-114.

**Acceptance criteria**
- [ ] The colophon declares `data-stage="back"`
- [ ] Its eyebrow carries no mark, and reads as the reference deck's does
- [ ] The printed contents card 13 reads `BACK MATTER` with no icon, **looked at** on paper
- [ ] The stage census credits Decision with two slides, not three
- [ ] `check_all.py` green, and the deck's own per-deck gates pass unchanged

**Open questions**
- Should a gate refuse a mark on back matter? Recorded below rather than answered here.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `data-stage="back"` on the colophon; drop the eyebrow's `<use>` mark; match the reference deck's eyebrow text | the deck change |
| 2 | Re-read the manifest out of the running deck — stage `null`, `Back matter`, no icon | the measurement |
| 3 | `check_all.py`, then print and **look** at the contents sheet | green, and the paper |

## 3. Implement

**Decisions & assumptions**
- 2026-08-17 — **the eyebrow takes the reference deck's exact form, `13 · Back matter`, rather than
  keeping `Colophon` without its icon.** Two reasons, and neither is taste. The shell's own constant
  is `Back matter` and [`shell/deck.js`](../shell/deck.js) says why — *`Back matter` is also true of
  all three of the things it names, where `Colophon` is true of one* — so a slide labelled one way
  and carded another would disagree with itself across two renderings. And the slide number was
  missing from this eyebrow where every other slide in the deck carries one.
- 2026-08-17 — **the `#i-sources` symbol stays in the sprite.** It is used twelve more times, in the
  provenance marks the deck's slides carry, so removing the eyebrow's `<use>` orphans nothing.
  Checked rather than assumed: `shell.py icons` still reports the same six symbols.
- 2026-08-17 — **the deck's own `.provenance` line is untouched.** DS-113/114 govern the **stage
  mark**, which is what the eyebrow carried; the upper-right *five documents above* is `.provenance`
  under DS-105 and is a different component with a different rule.

**What was done.** Three edits inside one `<section>` in
[`examples/measure-first/measure-first.html`](../examples/measure-first/measure-first.html):
`data-stage="4"` → `"back"`, the eyebrow's `<svg><use href="#i-sources"></svg>` removed, and the
label changed to `13 &middot; Back matter`. Two insertions, three deletions, and nothing else in the
file — the diff is the whole change.

**Measured in the running deck, not read off the markup:**

| | before | after |
| :--- | :--- | :--- |
| the colophon's `data-stage` | `4` | `back` |
| its eyebrow | `Colophon`, with a mark | `13 · Back matter`, **0** marks |
| the stage census | Decision **3** | Decision **2**, back matter 1 |
| printed contents card 13 | `DECISION` + flag icon | `BACK MATTER`, no icon |

**The `ARTIFACTS` entry [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) added earned
itself back within the hour.** Three deleted lines took the deck from 377 693 to 377 630 bytes, and
`figures.py` failed the run on the `examples/README.md` sentence stating the old figure — a page
published one commit earlier. Before that entry existed the same edit would have left a wrong number
on a public page with every gate green, which is the state T-129 was raised from. Corrected; the
`KB` and `slides` claims were unaffected.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The colophon declares `data-stage="back"` | **met** | Read back out of the running deck, not off the markup |
| Its eyebrow carries no mark, and reads as the reference deck's does | **met** | `13 · Back matter`, **0** `svg`/`use` inside `.eyebrow` |
| Printed contents card 13 reads `BACK MATTER` with no icon, looked at on paper | **met** | Printed and looked at. Card 13 is now identical in form to the reference deck's, which is the standard this task was set against |
| The stage census credits Decision with two slides | **met** | `{0:2, 1:4, 2:2, 3:2, 4:2, back:1}` — Decision was 3 |
| `check_all.py` green, per-deck gates unchanged | **met** | `0 failure(s), 0 unclassified, 0 stale`; `PRINT-1` 14 pages, `PRINT-2` and `PRINT-3` pass |

**The open question, answered here rather than sent back: no, a gate should not try to decide this.**
Whether a slide is back matter is an authoring judgement, and the only mechanical route to it is
binding on the words *sources*, *colophon* or *appendix* in `data-name` — which is the shape
[T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) measured at **30 false
alarms against 5 true** and settled against. DS-113 and DS-114 are already gate-decided by
`audit.py` and neither was breached: the sprite carries only icons the deck uses, and the eyebrow's
mark was hand-authored slide content rather than anything the shell emitted. **So this belongs to
the set a person asserts by looking**, and it is the second time in two days that the set has
returned something: T-168's popover, and now a card on a printed page.

**What that says about T-128's step 8, which passed.** Its criterion was *the contents sheet clean
at 13 entries*, and the sheet was clean — 13 cards, no collision, all clear of the footnote. The
criterion asked whether the cards **fit**. It did not ask what they **said**, and a printed page
answers both questions to anyone who reads it. The gap was in the criterion, not in the print.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-17 | → done | **Raised and closed the same hour: one attribute, one removed mark, one label.** The colophon now files as `back`, its eyebrow reads `13 · Back matter` with no mark, and the printed card 13 is identical in form to the reference deck's. The census correction is the part nothing could see on a slide face — Decision was credited with three slides and argues two. The open question is answered rather than sent back: a gate should **not** try to decide what is back matter, because the only mechanical route is binding on the words *sources* / *colophon*, which T-068 measured at 30 false alarms against 5 true. It belongs to the looked-at set, which has now returned two findings in two days. |
| 2026-08-17 | → proposed | **Found on the printed page, one commit after the deck was published.** T-128's step 8 print was looked at and passed — the contents sheet was clean at 13 entries, which is what that criterion asked. It did not ask what the thirteenth card *said*. The owner read it and ruled the file is this package's example now, so it ships presenting the way the plugin intends. One attribute, three consequences, and the third is a stage census nobody can see on a slide face. |
