---
id: T-168
title: .sources-open ships with no minimum target size, so DS-168 holds only by luck of the type scale
type: fix
status: review
phase: review
parent: null
blocked_by: []
related: [T-128, T-103, T-166]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - shell/components.css
---

# T-168 — .sources-open ships with no minimum target size

## 1. Specify

**DS-168 requires every target to be at least 24 × 24 CSS px.** The shared block's
[`shell/components.css`](../shell/components.css) styles `.sources-open` — the control that opens a
quoted source — as `display:block; width:100%; padding:0; font:inherit`. **There is no
`min-height`.** Its height is therefore one inherited line box, and whether it clears the floor is
decided by whatever type scale the surrounding slide happens to set.

**Measured 2026-08-16, two decks carrying the same shell:**

| Deck | smallest target | DS-168 |
| :--- | ---: | :--- |
| `examples/sort-window/sort-window.html` | 43.3 px | pass |
| [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md)'s adopter deck | **23.2 px** | **FAIL** |

Confirmed on a second instrument: measured in the browser, the smallest target is a `.sources-open`
button at **23.3 px** high, in the colophon's source rows. The two readings agree to a rounding.

**Every other hit target in the deck is governed and this one is not.** `--disc-hit` and `--doc-hit`
are declared, banded, and checked by `theme.py`; `.sources-open` reads neither. So the one control
that is sized by inheritance is the one that fell under the floor, and nothing short of a
browser-driven measurement can see it.

**Why this is `PH1`.** An accessibility floor the plugin states in its own design system, breached
by markup the plugin ships, in a deck built by an adopter who did nothing wrong. The deck author
cannot reasonably be expected to know that the control's target size depends on their type scale.

**Scope**
- In: `.sources-open` gets a minimum target size from the same token family as the other hit
  targets, so the floor holds whatever the surrounding type scale is.
- Out: changing DS-168's threshold, and re-styling the sources box.
- Watch: the control is `display:block; width:100%`, so a `min-height` must not open a gap between
  adjacent rows in the colophon — the rows are a list and must still read as one.

**Acceptance criteria**
- [ ] T-128's deck passes DS-168 with no change to the deck
- [ ] `examples/sort-window/sort-window.html` and `examples/reference-deck.html` are unchanged in
      appearance, and `shell.py check` passes on both after the shell moves
- [ ] A fixture sets a small type scale around a `.sources-open` and the target still clears 24 px

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Give `.sources-open` a minimum target size in [`shell/components.css`](../shell/components.css) | the shell change |
| 2 | `shell.py sync --write` on all three shipped decks; regenerate the seeded-defects fixture rather than syncing it (**L-77**) | four files in step |
| 3 | `audit.py` on all three — the adopter deck clears the floor and neither deck written here moves | the measurement |
| 4 | Open a sources box and **look at it**, offline | the judgement |

## 3. Implement

**Decisions & assumptions**
- 2026-08-16 — **the floor is `var(--disc-hit)`, not the bare 48 du.** `chrome_row.py` states the
  reason for the ruler's ticks and it applies unchanged here: a target sized at the bare floor is a
  different size from every other target in the deck. Consistency is the point of a token family.
- 2026-08-16 — **`display:flex; align-items:center` comes with the `min-height`.** A minimum height
  on a `display:block` button leaves the label sitting at the top of a taller box, which reads as a
  broken row rather than a bigger target.
- 2026-08-16 — **the blast radius was smaller than the estimate assumed, and the estimate is
  corrected to `s` rather than left at `xs`.** The control was expected to be the colophon's five
  source rows; the colophon does not use it. `.sources-open` lives only in the provenance popover,
  which is closed until a reader opens it — so the change is invisible on every slide face.

**What was done.** One rule in `shell/components.css`, then `sync --write` on
`examples/reference-deck.html`, `examples/sort-window/sort-window.html` and
`examples/measure-first/measure-first.html`; `shell.py check` green on all three.
`examples/reference-deck-seeded-defects.html` is **generated** and was regenerated with
`seed_defects.py` instead — syncing it left its sprite disagreeing with its icons, which is L-77's
caution arriving in practice.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| T-128's deck passes DS-168 with no change to the deck | **met** | `targets under 24 CSS px: 0 (smallest 43.3)`, up from 23.2. Nothing in the deck was edited |
| The two shipped decks are unchanged in appearance, `shell.py check` passes on both | **partly met** | `shell.py check` green on both, and both still measure `smallest 43.3` — i.e. **unmoved**, since neither had a `.sources-open` below the floor. *Unchanged in appearance* is asserted from the measurement, not from looking |
| A fixture sets a small type scale around a `.sources-open` and the target still clears 24 px | **not met** | No fixture was written. The regression that would catch this is a type scale nothing here sets; the adopter deck is currently the only case, and it is a deck rather than a fixture |

**Outstanding before this can close.** §7 step 3 — the sources popover has not been **opened and
looked at**, offline. The preview available in this session renders the deck as a static snapshot, so
the box never opened and the row height measured 0. A green `audit.py` is not this step
(`CLAUDE.md` rule 6), and the task stays at `review` until somebody looks.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → review | Fixed and measured the same day. `min-height:var(--disc-hit)` on `.sources-open`, all four decks brought into step, DS-168 now `0 targets under 24 px` on all three shipped decks with neither of the two written here moving. **Two things this cost that the estimate did not carry**, which is why `effort` is corrected `xs`→`s`: syncing the seeded-defects fixture was wrong and it had to be regenerated (**L-77**), and the acceptance criterion asking for a fixture is **not met** rather than quietly dropped. Held at `review` because §7 step 3 is unsatisfied — nothing has looked at the opened popover. |
| 2026-08-16 | → proposed | Found by [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) step 6. The first hypothesis was the ruler at 13 sections, and it was wrong — the browser named `.sources-open` instead, which is why the element was identified rather than reasoned about. Second defect of the day where a shell-owned thing depends on a per-deck value nothing checks; [T-166](T-166-shell-sync-leaves-an-upgraded-deck-failing-the-theme-gate.md) is the other. |
