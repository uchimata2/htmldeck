---
id: T-129
title: The reference deck's figures in examples/README.md are bound to nothing, and two of them are wrong on the published page
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-127, T-088, T-085, T-128]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - examples/README.md
  - tools/docs/figures.py
---

# T-129 — The reference deck's figures in examples/README.md are bound to nothing, and two of them are wrong on the published page

## 1. Specify

**Outcome**
`examples/README.md` states the reference deck's size correctly, and a gate notices when it stops
doing so. Today it states neither: the figures are wrong, and nothing watches them.

**What was seen, and where**
Found 2026-08-13 while taking
[T-127](T-127-figures-py-refuses-to-report-a-drifted-figure-because-its-fixture-needs-an-undrifted-page.md)
through its lifecycle. The rebuilt fixture seeds every claim of two shapes and asks whether the tool
reports it, and it refused on the reference deck's sentence — because that sentence is bound to
nothing. Measured on a green run of `python tools/docs/figures.py`:

| | the page says | the manifest prints |
| :--- | ---: | ---: |
| `**N KB in one file**` | **250 KB** | **262 KB** |
| `N bytes` | **255 787** | **268 563** |
| `N hand-written SVG figures` | eight | 8, correct |
| slides | 12, correct | 12 |

**The tool prints the right answer two lines below the wrong one.** The artifact manifest in the same
report reads `examples/reference-deck.html 262 KB, 268563 bytes, 12 slides, 8 figures`, and the run
ends `0 stale figure(s)`. Nothing connects them, because the reference deck's sentence falls into the
**531 unanchored figures** — *in a sentence naming no field and in no block linking an artifact, so
not judged*.

**Why one deck's sentence binds and the other's does not**
The sort-window sentence sits in a section that links the artifact, so `declared()` anchors it and
watches all four of its figures. The reference deck's section states its size in a paragraph that
links nothing, three lines under the heading. Same page, same wording, same shape — different
binding. **This is exactly [T-088](T-088-a-figure-in-a-sentence-naming-no-field-goes-stale-unwatched.md)'s
defect class, on the other deck**, and T-088 fixed the instance it found rather than the class.

**Why it matters more than a number**
`examples/README.md` is human-facing: it is what a stranger reads to decide whether the examples are
worth opening, and it is in the humanizer's covered set under
[`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §2. A published page understating a shipped deck by
**12 KB and 12 776 bytes** is a claim about the product, not a stale internal count.

**Scope**
- In: correcting the two figures on the page.
- In: making the reference deck's sentence bind, so the correction cannot silently rot again — by
  the same mechanism sort-window's uses, not by an exception.
- In: whether any other declared document states an artifact property in an unanchored sentence.
- Out: the 531 unanchored figures as a whole. Most name no artifact and are correctly unjudged; this
  is about the ones that name one.
- Out: `figures.py`'s self-test, which is T-127 and is done.

**Inputs**
- [`examples/README.md`](../examples/README.md) — the two sentences, one bound and one not.
- `tools/docs/figures.py` — `declared()` and the manifest, and the `unanchored` count.
- [T-088](T-088-a-figure-in-a-sentence-naming-no-field-goes-stale-unwatched.md) — the same class,
  fixed once by instance.

**Acceptance criteria**
- [ ] The page states the reference deck's size and byte count as the manifest prints them
- [ ] Deliberately staling the reference deck's figure makes the run fail, measured rather than
      assumed (**L-05**)
- [ ] The binding is the mechanism sort-window's sentence already uses, with no per-sentence
      exception
- [ ] Every other artifact property stated in a declared document is either bound or listed with a
      reason

**Open questions**
- **Does the sentence move to where the anchor is, or does the anchor rule widen?** Recommended:
  widen the rule to a section that links the artifact, since the reference deck's own section does
  name the file in its heading and a page should not be written around its checker. The alternative
  — edit the sentence to link the deck — is one character and fixes only this instance, which is what
  T-088 did and is why this task exists. — whoever takes it, from `figures.py`'s own reason

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | (no change) | **The owner ruled this goes before [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md).** T-128 puts a third deck on the same page, and a binding hole that already swallows one deck's figures would swallow that one's too — so the coverage is worth closing while the page has two decks on it rather than three. `related` now names T-128 for that reason; it is not a `blocked_by`, because either could be done alone. |
| 2026-08-13 | → proposed | Raised out of [T-127](T-127-figures-py-refuses-to-report-a-drifted-figure-because-its-fixture-needs-an-undrifted-page.md), whose rebuilt fixture refused on a claim the page does not bind. Not folded into it: T-127 is about a self-test asserting repository state, and this is a live wrong figure on a human-facing page plus the coverage hole that let it sit there. `s` and `high` — the correction is a paste, the binding is the work, and the page is what a stranger reads before installing anything. |
