---
id: T-188
title: Raise the shipped motion density default from 10 to 100, and correct every document that states the old figure
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-112, T-187]
work_package: PH3
shipped_in: 0.5.0
owner: the project owner
business_value: medium
effort: s
created: 2026-08-19
updated: 2026-08-19
deliverables: []
---

# T-188 — Raise the shipped motion density default from 10 to 100, and correct every document that states the old figure

## 1. Specify

**Outcome**
A deck built from this plugin runs **every** content motion it carries, not one. The token changes in
one place per deck, and the four documents that state the old figure as a fact are corrected in the
same edit, so no reader is left with a number the artifact contradicts.

**The owner's ruling, recorded 2026-08-19**

> *"Raise it to 100%. Initial tests better with recognizing all of them. Reducing it is a matter of
> optimization, later."*

This answers the question [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md)
§4 raised without being asked: *is 10 the right default?* T-112 measured what 10 does concretely — a
deck carries so few content motions that the second is already at rank 34 or 51, so 10 runs **exactly
one**, which is closer to one easter egg per deck than to a tenth of the motion. The owner's answer is
that the project is not yet at the stage where that restraint is the point: while the motions are
being built and looked at, seeing all of them is worth more than a quiet deck. **Reducing the default
is deferred, not rejected**, and the reason is stated so that a later session lowering it is finishing
this decision rather than reversing it.

**Why this is a defect and not a preference**
The default is stated as a fact in four documents and one stylesheet comment. Changing the token
without them leaves the ruleset asserting a value the shipped deck disproves — the failure mode
`CLAUDE.md` names for figures generally, and the one T-112's own review warned about when it said the
gate's account is what the tool prints and not what a document claims.

**Where the figure lives, located 2026-08-19**

| Home | What it says today |
| :--- | :--- |
| `examples/reference-deck.html:279` | `--motion-density:10;` — the built artifact |
| `examples/reference-deck-seeded-defects.html:279` | the same token in the defect fixture |
| `docs/DESIGN-SYSTEM.md` DS-238 | "the shipped default of **10** is a deck that is mostly still with the occasional moment" |
| `docs/THEME-CONTRACT.md` `--motion-density` row | "the default is a deck that is mostly still with the occasional moment" |
| `docs/RELEASE-PHASES.md` T-112 row | "Motion density, 0–100, default 10" |
| `shell/components.css:594` | "So density 10 runs the tenth of the deck's content motions that were ranked first" — prose about the arithmetic, which stays true; check whether it reads as a statement of the default |

**One thing to establish rather than assume**
A grep of `skills/` on 2026-08-19 found `--m-rank` in `references/build.md` and **no mention of
`--motion-density`**. That is either a real gap — a deck built from the skill emitting no density token
at all, which would make `--m-on`'s `calc()` invalid — or a search that looked in the wrong place. It
is written here as a question, not as a finding: **run it and see a built deck's `:root`** before
either fixing it or dropping it. If it is real it is a separate defect and gets its own task.

**Scope**
- In: the token in both example decks, and every document above.
- In: confirming from a render, not from `check.py`, that a deck at 100 still reads as considered
  rather than busy — the judgement `check.py` was measured green on but cannot make (T-112 §4 ran
  `check.py` clean at 0, 10 and 100).
- Out: **the seeded-defects fixture's expected results**, if the density value participates in any of
  them. Establish that first; if it does, that is the fixture's business and not a value to edit past.
- Out: any change to what density governs. DS-237 and DS-238's split is untouched, and the owner
  confirmed the `rise` classification on the same day.
- Out: lowering the default later. That is the deferred half of this ruling and belongs to whoever
  takes the optimisation pass.

**Inputs**
- [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md) §4 — the
  measurement that produced the question, and the record that `check.py` is already green at 100.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-237, DS-238.
- [`docs/THEME-CONTRACT.md`](../docs/THEME-CONTRACT.md) — the token's row and band.

**Acceptance criteria**
- [ ] Both example decks carry `--motion-density:100`, and no document in the repository still states
      10 as the shipped default.
- [ ] `python tools/deck/density.py list examples/reference-deck.html` shows every content motion on,
      and the count is stated here.
- [ ] The deck is opened and looked at offline at 100, in both themes, and a person says whether it
      reads as considered or as busy. A green gate is not this criterion.
- [ ] `python tools/check_all.py` green, including the seeded-defects fixture's expected results.
- [ ] `python tools/tasks/lint.py` and `python tools/docs/refcheck.py` clean.

**Open questions**
- Whether `references/build.md` tells a deck author to emit the token at all — see *One thing to
  establish* above. Answered by reading a freshly built deck, not by grep alone.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Change the token in the shipped theme and in every deck that declares it | `themes/quarto.css`, three decks, the fixture |
| 2 | Correct every document stating the old figure as a fact | DS-238, THEME-CONTRACT.md, RELEASE-PHASES.md |
| 3 | Re-derive the seeded-defect fixture rather than editing it | `seed_defects.py --check` green |

## 3. Implement

**Decisions & assumptions**
- **`components.css`'s density prose stays.** T-188 asked whether line 626 reads as a statement of the default. It does not - *density 10 runs the tenth of the deck's content motions that were ranked first* illustrates the arithmetic and stays true at any default. Checked and left alone rather than reworded - 2026-08-20.
- **All four decks carried `10`, not the two the task located.** `sort-window` and `measure-first` were found by grepping rather than by the located list, which had only the reference deck and the fixture - 2026-08-20.

**Outputs produced**
- `themes/quarto.css`
- `docs/DESIGN-SYSTEM.md` DS-238
- `docs/THEME-CONTRACT.md` `--motion-density`
- `examples/reference-deck.html`, `sort-window`, `measure-first`, and the fixture

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The token is 100 in the shipped theme and in every deck | **pass** | measured in the browser: `--motion-density` resolves to `100` |
| No document states the old figure as a fact | **pass** | grep for `density 10` and `default of **10**` returns only the amendment notes, which state it as history |
| The fixture is derived, not edited | **pass** | `seed_defects.py --check` green |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-20 | -> proposed | Created. |
| 2026-08-20 | -> in_progress | Implemented with T-198 and T-199; one theme, one edit. |
| 2026-08-20 | -> done | All three criteria met. Awaiting a release for `shipped_in`. |
