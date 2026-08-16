---
id: T-172
title: The shell sync falsified four published deck figures and nothing could see it
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-128, T-129, T-154]
work_package: PH3
owner: the project owner
business_value: high
effort: xs
created: 2026-08-16
updated: 2026-08-16
deliverables:
  - README.md
  - examples/README.md
  - docs/BRIEF.md
---

# T-172 — The shell sync falsified four published deck figures and nothing could see it

## 1. Specify

**Outcome**
`python tools/check_all.py` reaches green. The three documents that state the shipped decks' sizes
state the sizes those decks actually have, and the one numeral that no command is bound to either
gains a binding or is excused by name.

**What is wrong.** [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md)'s step 5 synced the
shell into all three decks — commit `745f6b8` — and both shipped decks grew. Nothing re-derived the
pages that quote their size, so five figures are now wrong or unwatched:

| Document | States | Actual |
| :--- | :--- | :--- |
| [`examples/README.md`](../examples/README.md) | `262 KB in one file`, `268 563 bytes` — the reference deck | 263 KB, 269 083 bytes |
| [`examples/README.md`](../examples/README.md) | `265 804 bytes` — `sort-window` | 266 324 bytes |
| [`docs/BRIEF.md`](../docs/BRIEF.md) | `262 KB` — the reference deck | 263 KB |
| [`README.md`](../README.md) | `262 KB in one file` — the reference deck | 263 KB, and **bound to nothing**: `figures.py` reports it as `UNDECLARED prose numeral 262` |

**Why it matters, and why it is not just four numbers.** Three of the four are on pages a stranger
reads before installing anything, which is the covered set
[`docs/PUBLISHING.md`](../docs/PUBLISHING.md) defines. The fourth is the finding: the root
`README.md` states the same measurement as the two bound pages and **no gate holds it to anything**,
so it can be right today and drift silently tomorrow — the exact hole
[T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md)
closed for `examples/README.md` and did not close here.

**Why nothing saw it.** `check_all.py` refused the undeclared `examples/measure-first/` deck and
exited **before running a single checker**, so the whole suite has been dark since `745f6b8`. The
`DECKS` entry that landed 2026-08-16 is what made these five visible; it did not cause them.

**Scope**
- In: correct the four stated figures against the manifest `figures.py` prints.
- In: decide the root `README.md` numeral — bind it to the artifact manifest as `examples/README.md`
  binds its own, or excuse it by name with the reason. Binding is the recommendation: an unbound
  figure on the front door is what T-129 was raised about.
- Out: `examples/measure-first/`'s own entry on `examples/README.md` and the figures that come with
  it. That is [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) step 7 and stays there.
- Out: any change to the decks themselves. The decks are correct; the prose about them is not.

**Inputs**
- `python tools/docs/figures.py` — prints both the findings and the artifact manifest they are
  compared against.
- [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) —
  the same defect on the same page, with the binding mechanism it introduced.

**Acceptance criteria**
- [ ] `python tools/docs/figures.py` exits 0
- [ ] `python tools/check_all.py` exits 0
- [ ] Every corrected figure was read off the manifest, not off a previous document
- [ ] The root `README.md` numeral is either compared or excused by name, and the record says which
      and why

**Open questions**
- none

## 2. Plan

_Not planned._

## 3. Implement

_Not started._

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-16 | → proposed | Raised out of the unattended batch's first item. Landing T-128's authorised `DECKS` entry let `check_all.py` past the undeclared deck for the first time since `745f6b8`; all three decks pass their per-deck gates and the run then fails at `figures.py` with five figures. Raised rather than fixed inside the batch, because the authorisation bounded that item to one line and the rest of T-128's step 7 touches the same page. |
