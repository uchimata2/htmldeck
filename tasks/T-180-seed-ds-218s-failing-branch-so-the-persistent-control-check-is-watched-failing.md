---
id: T-180
title: Seed DS-218's failing branch, so the persistent-control check has been watched failing
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-005, T-051, T-114]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-18
updated: 2026-08-18
deliverables: [tools/deck/static_variants.py]
---

# T-180 — Seed DS-218's failing branch, so the persistent-control check has been watched failing

## 1. Specify

**Outcome**
A seeded variant that moves the motion control inside the More menu and leaves everything else
alone, and a suite run that reports DS-218 caught. Today the rule has only ever been seen to pass.

**The mechanism, measured**
`python tools/deck/check.py examples/reference-deck.html` on 2026-08-18:

```
DS-218   persistent control for motion over 5s: True (present: True, 1 looping)   pass
```

So the rule is **checked**, not excused, and it found its subject — `undecided, no subject` is 0.
What no run has shown is the rule objecting. Its predicate,
[`tools/deck/audit.py`](../tools/deck/audit.py) §DS-218, is
`len(data["infinite"]) == 0 or data["motionPersistent"]`, and **the first disjunct is the risk**: a
deck with no looping motion passes without the placement ever being read. A seed that removed the
deck's looping motion instead of moving the control would therefore pass, and look like a catch.

**This is L-36's shape and the file already names it twice.** `static_variants.py`'s own docstring:
*a check that has never been seen to fail is a claim about the instrument, not about the deck*. And
the comment beside DS-140 in `audit.py` records the same trap firing for real — `.current` *passed on
its own absence, and the seeded fixture that deletes the deck's only dashed flow reported the same
`pass` as the deck that has one* (**T-051**).

**Scope**
- In: one variant in `RENDER_VARIANTS`, because DS-218 is decided by `audit.render_verdicts` off a
  rendered DOM.
- In: the edit is the **smallest one that breaks this rule and nothing else** — the control moves,
  it is not deleted, and the looping motion is untouched. `motionControl` stays `True` and
  `infinite` stays 1, so only `motionPersistent` flips.
- Out: any change to DS-218, to `audit.py`'s predicate, or to the shipped decks. The rule is right
  and the decks obey it; what is missing is evidence that the check can object.
- Out: a variant for the `len(infinite) == 0` branch. A deck with no looping motion is legitimate
  and owes no control, so there is no failure to seed there — it is the *subject-absent* case, and
  `render_failures` already refuses to count a `None` row as a catch.

**Inputs**
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `RENDER_VARIANTS`, `build`,
  and `render_failures`.
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the DS-218 row and `motionPersistent`.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — every variant derives from it.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-218.

**Acceptance criteria**
- [ ] A variant exists that moves `#motion` inside `.more-menu` and changes nothing else
- [ ] The suite reports DS-218 caught on it, and the baseline deck stays green
- [ ] The variant breaks DS-218 **only** — any other rule it trips is reported and either designed
      out or recorded
- [ ] Removing the DS-218 branch from `audit.py` makes the suite say `MISSED`, proving the catch is
      the check's and not another rule's

**Open questions**
- None.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add the variant to `RENDER_VARIANTS` with the anchor asserted | `static_variants.py` |
| 2 | Run the suite; confirm caught, and read which rules the variant trips | the verdict |
| 3 | Prove the catch belongs to DS-218 by removing its branch | `MISSED` |
| 4 | Gates | green |

## 3. Implement

**Decisions & assumptions**
- **The seed moves the control; it does not delete it** — 2026-08-18. This is the whole design of
  the fixture. DS-218's predicate is `len(infinite) == 0 or motionPersistent`, so deleting the
  deck's looping motion satisfies the **first** disjunct and passes — a seed that would have been
  recorded as a catch while proving the opposite. Measured on the built variant:
  `motionControl=True  motionPersistent=False  infinite=1`, so exactly one input moved.
- **The catch was proven to be DS-218's own, not another rule's** — 2026-08-18. `render_verdicts`
  on the variant returns `['DS-218']` and nothing else; the same captured data judged by an `audit`
  whose DS-218 branch is forced `True` returns **nothing failing**. So the variant is minimal in one
  direction and the rule is load-bearing in the other, and neither is an inference from reading the
  predicate.
- **No variant for the `len(infinite) == 0` disjunct**, as §1 scoped. A deck with no looping motion
  owes no control, so there is no failure to seed — that is the subject-absent case, and
  `render_failures` already refuses to count a `None` row as a catch (T-051).

**Outputs produced**
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — `motion-stop-shut-inside-the-menu`
  in `RENDER_VARIANTS`. The variant deck itself is written to `.assets-cache/deck/variants/` and is
  gitignored; the suite regenerates it.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A variant exists that moves `#motion` inside `.more-menu` and changes nothing else | met | Read back from the built variant through the deck's own DOM: parent is `more-menu#moreMenu` |
| The suite reports DS-218 caught on it, and the baseline deck stays green | met | `8 of 8 rendered variants caught`; `self_test()` asserts the baseline is green before any variant runs |
| The variant breaks DS-218 **only** | met | `render_verdicts` returns `['DS-218']` — nothing else objects |
| Removing the DS-218 branch makes the suite say `MISSED` | met | The same data judged without that branch fails nothing at all |

**Looked at, offline** — `CLAUDE.md` rule 6, `TASK-WORKFLOW.md` §7 step 3. The variant rendered in
real Chrome: the chrome row carries `MORE` alone where the reference deck carries `MOTION ON` beside
it, the layout is otherwise untouched, and the button is present and operable once the menu is
opened. **That picture is the rule's subject, not decoration** — a reader watching a looping diagram
sees no way to stop it without opening a menu first, which is what *persistent* was written to
prevent.

*The browser pane read the DOM but could not screenshot — hidden, it composites no frames. The
picture came from `tools/deck/render.py`, which captures the stage reliably; it was only the
interactive opener that failed it earlier today.*

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → done | Specified, planned, implemented and reviewed in one sitting; `xs` and it stayed `xs`. The only thing that needed care was the shape of the seed: the lazy version — delete the looping motion — passes DS-218 legitimately and would have been filed as a catch. Both directions are now proven by running them rather than by reading the predicate: the variant trips DS-218 and nothing else, and with DS-218's branch neutralised the same data trips nothing. |
| 2026-08-18 | → proposed | Raised while answering a question about why the motion control sits outside the More menu. The answer was DS-218 and the gate decides it, but checking that turned up the narrower fact: the rule has only ever been observed passing, and its predicate has a disjunct that passes a deck whose subject is absent. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — the check works on every deck this repository ships, so this is an assurance gap rather than a defect in the published plugin. |
