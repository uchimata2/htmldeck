---
id: T-129
title: The reference deck's figures in examples/README.md are bound to nothing, and two of them are wrong on the published page
type: fix
status: done
phase: review
shipped_in: unreleased
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

**The repository already states the right answer, in the document that outranks this one.**
`docs/BRIEF.md` *Definition of done* links the deck and says *12 slides, 262 KB* — bound, judged and
correct on every run. So the two figures are not merely unwatched: the specification and the examples
page disagree about the same file, and only one of them is being checked.

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
- ~~**Does the sentence move to where the anchor is, or does the anchor rule widen?**~~
  **Answered 2026-08-13 — both, and the recommendation as written binds nothing.** Measured before
  choosing: `examples/README.md` links a manifest artifact in exactly three places — the intro
  table's two rows, and the paragraph that opens *The generated deck*. **The `## The reference deck`
  section links the deck nowhere**, so widening the anchor to section scope leaves this sentence
  exactly as unbound as it is today. The recommendation rested on the section "naming the file in its
  heading", and the heading says *The reference deck*, not the file name. So:
  - **the anchor rule widens where widening is worth something** — a **table row** becomes a claim
    scope, as a list item already is. The intro table links two artifacts in one block and is
    therefore judged not at all; per row it links one each, and two more true figures bind with no
    new false alarm;
  - **and the sentence gains the link**, because nothing else can bind it. That is not the
    per-sentence exception the criteria forbid: it is the mechanism `sort-window/`'s paragraph
    already uses, and the reference deck's paragraph is the only one on the page that does not.
- **Should an unbound claim of artifact shape fail the run?** **Answered 2026-08-13 — no, reported.**
  Swept all five declared documents for the shape `scope_claims()` judges (a numeral or count word
  followed within four tokens by `KB`/`bytes`/`slides`/`figures`): **81 occurrences, 6 bound today
  and 75 not.** Of the 75, **5 are a manifest deck's own property in a scope that can bind** — the
  two intro-table rows, and the three figures in the reference deck's paragraph — 2 more mention a
  manifest deck's count in passing and are correct, and **68 are not about a manifest artifact at
  all**: rule thresholds (*6–16 slides*), research probes (*192 KB*), other files (*Chart.js is
  203.6 KB*), rubric scores, the seeded-defect deck at 14 slides, and parts of a file rather than the
  file (*97 KB of it as base64*). Failing on the shape would be 68 wrong alarms against 7 right ones,
  which is worse than the 30-against-5 that
  [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) rejected for binding by
  vocabulary. The count is printed per document instead, and the anti-recurrence device is in the
  self-test: **every** claim of these shapes the page carries must bind, not one of each shape, which
  is the assertion that would have failed on the day this defect appeared.

## 2. Plan

**Order matters: the binding goes in before the correction.** Correcting the figures first would
leave nothing to measure — a page that is already right cannot demonstrate that the run now fails on
it being wrong, which is the trap **L-79** §5 and **T-127** were both paid for.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | A table row becomes a claim scope, as a list item already is | `claim_scopes` in `figures.py` |
| 2 | A numeral in a partitive construction (*97 KB **of it***) is not the whole's property | `scope_claims` in `figures.py` |
| 3 | The reference deck's paragraph links the deck, so its own claim binds | `examples/README.md` |
| 4 | Run, and require the two figures to report `STALE` **before** they are corrected | evidence |
| 5 | Paste the manifest's values onto the page | `examples/README.md` |
| 6 | The self-test asserts every claim of these shapes binds, not one per shape | `figures.py` |
| 7 | Seed the drift back, by hand and restored by hand, and watch the run fail (**L-04**, **L-80**) | evidence |
| 8 | Report the unbound-claim count per document, so the bucket is not silent (**L-05**) | `figures.py` |

## 3. Implement

**Decisions & assumptions**
- **A table row is a claim scope, exactly as a list item is** — 2026-08-13. The index table links
  three decks in one block, so it linked two manifest artifacts and `scope_claims` declined the
  whole of it. Per row it links one each. Two true figures bound and no false one appeared.
- **`of` directly after the unit means the numeral is a part, not the property** — 2026-08-13.
  *"97 KB of it as base64"* sits in the same sentence and the same shape as the deck's own size, and
  once the paragraph linked the deck it would have been reported `STALE` against 262. The signal is
  the construction, not the word, which is what `claimed()` binds on for the same reason.
- **The page gains the link rather than the rule gaining an exception** — 2026-08-13, and the
  measurement behind it is in §1's answered question. Nothing else could have bound it.
- **An unbound claim of artifact shape is reported, never failed** — 2026-08-13. 68 of the 75
  unbound occurrences are not about a manifest artifact at all. The alternative was measured, not
  imagined.

**What the widening exposed, which was not in the plan**
`artifact_claims` merged its scopes into a **dict keyed by the written figure**. The index table's
two rows both say `12 slides` — about different decks — so the second row's verdict replaced the
first's, and the reference deck's row went unwatched while the count read as though both were
judged. **Both verdicts were `compared`, so nothing looked wrong**; it surfaced only because the
rows were being counted. It is now a list, one entry per occurrence, and the ordering became document
order. Nothing had triggered it before because no two bullets of one block had ever linked different
files.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `TABLE_ROW` in `claim_scopes`, the partitive
  guard and the occurrence list in `scope_claims` / `artifact_claims`, the strengthened fixture 9,
  and the per-property watch counts in `report`.
- [`examples/README.md`](../examples/README.md) — the reference deck's paragraph links the deck and
  states 262 KB / 268 563 bytes.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The page states the reference deck's size and byte count as the manifest prints them | met | Page: *262 KB in one file, 268 563 bytes*. Manifest: `262 KB, 268563 bytes`. Both now `compared` |
| Deliberately staling the figure makes the run fail, measured rather than assumed (**L-05**) | met | **Not seeded — the drift was real.** With the link in and the figures still wrong the run printed both `STALE` rows and exited 1. The seed that *was* built is the harder one: taking the link back off exits with the new fixture's message, and the page was restored by hand and the bytes asserted equal (**L-80**) |
| The binding is the mechanism sort-window's sentence already uses, with no per-sentence exception | met | A link in the claim's own scope. No sentence, numeral or file is named anywhere in the tool |
| Every other artifact property stated in a declared document is either bound or listed with a reason | met | Swept all five: **81 occurrences of the shape, 11 judged, 1 declined as partitive (*97 KB of it*), 69 unbound** — of which 2 mention a manifest deck's count in passing and are correct, and 67 are not about a manifest artifact. The classes are in §1's second answered question |

**Verification run**

```
0 stale figure(s) - 1 volatile block(s) drifted, which is reported rather than failed
  compared      13        (was 8)
  unanchored   560
  where each property is watched - a zero means no declared document binds a claim to it
    examples/reference-deck.html               KB 2, bytes 1, slides 2, figures 1
    examples/sort-window/sort-window.html      KB 1, bytes 1, slides 2, figures 1
```

`python tools/tasks/lint.py` — all three passed, with the expected `DUPLICATE INDEX docs/BRIEF.md`.
`python tools/docs/refcheck.py` — 1634 pointers, 0 broken.
`python tools/check_all.py` — 19 ran, 1 skipped with its reason, 0 FAILED, 0 unclassified, 0 stale.

**What this does not close.** The `unanchored` bucket is still 560 figures and still silent one
figure at a time; what changed is that a *property of a manifest artifact* now has a number that
reads zero when nobody watches it. A page could still state a deck's size about a file the manifest
does not carry, and nothing would ask.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | Both figures corrected and both now bound. **The recommendation in §1's open question was wrong and was measured before it was followed**: widening the anchor to section scope binds nothing, because the reference deck's section links the deck nowhere. What worked was widening to the *table row* — which the recommendation did not consider and which the other defect on this page needed — plus the link the sentence lacked. Widening the scope then exposed a dict keyed by the written figure, merging two rows' verdicts into one; §3 has it. |
| 2026-08-13 | → planned | Specified and planned in one pass. The two open questions were settled here rather than carried to the owner: both are questions about a checker's own reason, and the sweep that answers the second is 40 lines. |
| 2026-08-13 | (no change) | **The owner ruled this goes before [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md).** T-128 puts a third deck on the same page, and a binding hole that already swallows one deck's figures would swallow that one's too — so the coverage is worth closing while the page has two decks on it rather than three. `related` now names T-128 for that reason; it is not a `blocked_by`, because either could be done alone. |
| 2026-08-13 | → proposed | Raised out of [T-127](T-127-figures-py-refuses-to-report-a-drifted-figure-because-its-fixture-needs-an-undrifted-page.md), whose rebuilt fixture refused on a claim the page does not bind. Not folded into it: T-127 is about a self-test asserting repository state, and this is a live wrong figure on a human-facing page plus the coverage hole that let it sit there. `s` and `high` — the correction is a paste, the binding is the work, and the page is what a stranger reads before installing anything. |
