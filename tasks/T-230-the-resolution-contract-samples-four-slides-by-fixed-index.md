---
id: T-230
title: Derive DS-063's slide sample from the deck instead of fixing it at four indices
type: fix
status: done
phase: review
parent: T-219
blocked_by: []
related: []
work_package: PH1
owner: the project owner
business_value: critical
effort: s
created: 2026-08-29
updated: 2026-08-29
deliverables: []
---

# T-230 — Derive DS-063's slide sample from the deck instead of fixing it at four indices

## 1. Specify

**Outcome**
DS-063 returns a verdict on a deck of any legal length. Today `contract.SAMPLE` is slides 1, 5, 8 and 12 and the probe clamps at the last slide, so **an eight-slide deck measures slide 8 twice**, the duplicate guard correctly refuses the comparison, and the row reports *undecided* while advising a re-run that will recur forever. DS-082's default length is 8-12 and DS-081's floor is 6, so most of the legitimate band loses the rule on every run.

**Closes** `PR-53` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3.

**Scope**
- In: `contract.SAMPLE`, derived from the deck's own slide count the way `render.py` already reads it and refuses to guess it
- In: **whether a duplicate the sampler caused should read differently from one a dropped render caused** - they need opposite fixes and the message today states only the second
- Out: DS-063's tolerances, which [T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) settled and this must not move

**Inputs**
- `PR-53` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) section 3
- [T-183](T-183-ds-063-failed-once-in-four-full-gate-runs-on-an-unchanged-tree.md) - the duplicate guard and why it exists

**Acceptance criteria**
- [ ] a six-slide and an eight-slide deck both get a **decided** DS-063 verdict, measured
- [ ] a genuinely dropped render still reads `undecided` with its own message, seeded
- [ ] `python tools/check_all.py` green on every shipped deck

**Open questions**
- None yet. The register's `Remedy` column carries a hypothesis for each finding, and the method's
  section 5 says it is a hypothesis: whoever implements this measures before committing to it, and
  records what the measurement said.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Replace `SAMPLE` with `SAMPLE_SIZE` and `sample_for(n)`, spreading four indices across `n` | `contract.py` |
| 2 | `scale_verdicts` takes the length from `render.slide_count`, which reads the file and treats zero as fatal rather than rendering a guess | `contract.py` |
| 3 | Refuse a caller-passed sample holding a repeat, **where the sample is known**, so the sampler's duplicate and the render's read differently | `contract.py` |
| 4 | Self-test: `sample_for(12) == [0, 4, 7, 11]`, and duplicate-free and in range for every length 1-60 | `contract.py`'s `self_test` |
| 5 | Measure a six- and an eight-slide deck, the old sample on the same deck, and a seeded dropped render | the table in section 3 |
| 6 | Reconcile the two live documents that state the sample as fixed | `examples/README.md`, `docs/PRE-RELEASE-AUDIT.md` |

**The derivation is `round(i * (n - 1) / (k - 1))` for `i` in `0..k-1`, `k = min(4, n)`.** It was
chosen for one property before any other: **on a twelve-slide deck it returns `[0, 4, 7, 11]`** -
the constant it replaces, exactly. That is the strongest evidence available that this derivation is
the right one rather than merely a different one, and the self-test asserts it so the two cannot
drift apart quietly. Every figure this repository quotes for a routine DS-063 run was measured on
those four slides.

## 3. Implement

`contract.py` only. `SAMPLE = [0, 4, 7, 11]` is now `SAMPLE_SIZE = 4` and `sample_for(n)`;
`scale_verdicts` derives the sample from `render.slide_count(deck)` when the caller passes none.

**The sample is duplicate-free and in range at every length by construction**, checked over 1-60 in
the self-test. That is what makes the duplicate the pairing guard reports unambiguously the
render's doing - which is the second half of the scope, and it is answered by making one of the two
causes impossible rather than by writing a longer message.

**The one case that survives is a caller passing a repeat**, and it is refused where the sample is
known rather than downstream where only its consequence is. The two messages now say opposite
things about what to do, because the two need opposite fixes:

| Cause | What DS-063 says |
| :--- | :--- |
| the sample repeats an index | *the sample asks for slide 3 twice ... This is the sample and not the render: re-running reproduces it exactly* |
| a render was dropped | *only one run measured 'Eleven minutes decides this'* |
| a render repeated a slide | *a run measured 'One transfer disappears' twice ... Re-run; if it recurs the probe is dropping or repeating a slide* |

**Measured on decks built by truncating the reference deck**, which is the acceptance criteria's
own test and not a fixture standing in for it:

| Deck | Sample | DS-063 |
| :--- | :--- | :--- |
| 6 slides | 1, 3, 4, 6 | **decided** - pass, worst 0.00 du non-text over 52 values, 1.53 du text over 104 |
| 8 slides | 1, 3, 6, 8 | **decided** - pass, worst 0.00 du non-text over 52 values, 1.07 du text over 104 |
| 8 slides, **old** sample `[0, 4, 7, 11]` | 1, 5, 8, 12 | **undecided** - *a run measured 'One transfer disappears' twice* |
| 8 slides, one row dropped from the 1280x634 run | 1, 3, 6, 8 | **undecided** - *only one run measured 'Eleven minutes decides this'* |
| 8 slides, sample `[0, 2, 2, 7]` | 1, 3, 3, 8 | **undecided** - *this is the sample and not the render* |

The third row is `PR-53` reproduced on demand, on the same deck as the second - so the before and
the after differ in the sample and in nothing else.

**One thing cost a round trip and is worth writing down.** The first seeded drop was taken from the
`720p` run and DS-063 **passed**: `geometry()` compares `3840x2000` against `1280x634` and `720p`
is DS-064's, a third label in the same results dict. A seed aimed at the wrong one of three
measures nothing, and it looks exactly like a fix that works.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| a six-slide and an eight-slide deck both get a **decided** DS-063 verdict, measured | met | Both decided and both pass; the table above carries the figures and the samples |
| a genuinely dropped render still reads `undecided` with its own message, seeded | met | *only one run measured ...*, distinct from both duplicate messages |
| `python tools/check_all.py` green on every shipped deck | met | Run on a frozen tree; the Log row carries the result |

**DS-063's tolerances were not touched**, which the scope puts out of bounds:
[T-206](T-206-ds-063-gives-a-different-verdict-on-identical-input.md) settled them and nothing here
reads them.

**Child fix tasks raised**
- none.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → proposed | Raised by cycle 40 of [T-219](T-219-pre-release-audit-of-the-whole-repository.md), the pre-release audit's triage. **`High`**: the method's section 4 gives that level one obligation beyond a child task — *the release does not go out while it is open*. |
| 2026-08-29 | → done | Batch B4. `contract.SAMPLE` is derived from the deck's own slide count and returns the constant it replaced on a twelve-slide deck. A six- and an eight-slide deck now get a decided DS-063; the old sample reproduces the defect on the same deck. The sampler's duplicate and the render's read differently. `examples/README.md` and cycle 20's claim about the tree reconciled. Both gates green, run separately. |
