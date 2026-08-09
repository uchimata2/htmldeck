---
id: T-040
title: Fix the three reference-deck defects the completed gate found
type: fix
status: done
phase: review
parent: T-005
blocked_by: []
related: [T-024, T-028]
work_package: WP3
owner: maintainer
created: 2026-08-09
updated: 2026-08-09
deliverables:
  - examples/reference-deck.html
---

# T-040 — Fix the three reference-deck defects the completed gate found

## 1. Specify

**Outcome**
[`examples/reference-deck.html`](../examples/reference-deck.html) carries none of the three defects
[T-005](T-005-build-check-the-gate-the-deck-must-pass.md)'s completed gate found, and the gate
reports zero failures against it.

**Why this one**
**T-005 does not fix anything — that boundary is written into its scope** and restated there as the
one most likely to erode: *a gate that edits what it is measuring cannot be trusted to have
measured it.* So the defects its new checks found need a separate task, and this is it. All three
had been in the deck since it was built and no previous run could see them, which is the whole
argument for closing a silent rule rather than leaving it labelled.

**The three, with the rule each breaks**

| | Rule | What the gate found |
| :--- | :--- | :--- |
| **DS-092** | *Sentence under 20 words* | The title slide's illustrative-model note runs to **29 words** in one sentence |
| **DS-092** | *Sentence under 20 words* | Slide 2's bottom line runs to **21 words** |
| **DS-113** | *A sprite containing **only** the icons used* | `i-corridor` is in the sprite and referenced by no `<use>`, in the markup or from the printed contents page |

**Scope**
- In: the three edits above, and nothing else in the deck.
- Out: **rewriting anything for style.** Slide 2's bottom line is one sentence by DS-202 and must
  stay one, so it is shortened rather than split; the note is two sentences already and gains a
  third.
- Out: the two ambiguities the same run surfaced — DS-045's two readings and DS-219's wording
  against its own reason. Those are ruleset questions for the owner, they are excused in writing in
  the gate, and neither is a deck defect until the owner says which way the rule falls.

**Inputs**
- The gate's own output: `python tools/deck/check.py examples/reference-deck.html`
- [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-092, DS-113, DS-202

**Acceptance criteria**
- [ ] No sentence on any slide exceeds 20 words
- [ ] Every symbol in the sprite is referenced by at least one `<use>` at run time
- [ ] Slide 2's bottom line is still **one** sentence, and still says which meeting and which date
- [ ] The deck still passes every other rule it passed before — no new failure anywhere in the gate

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Split the illustrative-model note's second sentence in two at its natural join | `examples/reference-deck.html` |
| 2 | Shorten slide 2's bottom line to one sentence under 20 words, keeping both dates | same |
| 3 | Delete the `i-corridor` symbol from the sprite | same |
| 4 | Re-run the whole gate, both variant suites and the content suite | a green run |

## 3. Implement

**Decisions & assumptions**
- **The bottom line was shortened, not split — 2026-08-09.** DS-202 requires one sentence, so
  splitting it would have traded a DS-092 failure for a DS-202 one. *The grant closes on 31 March
  2027, and the 12 March budget vote is the only meeting that can commit it* became *The 12 March
  budget vote is the only meeting that can commit the grant before 31 March 2027* — 19 words, both
  dates kept, and the deadline moved from the subject to the qualifier where it reads as the
  constraint it is.
- **The note gained a sentence rather than losing a clause — 2026-08-09.** Its content is DS-102's
  illustrative provision, which is load-bearing: dropping *none is drawn from a real agency, study
  or place* to fit a word count would remove the sentence that stops a reader taking the figures
  for research.
- **`i-corridor` was deleted, not wired to something — 2026-08-09.** The obvious alternative was to
  find a use for it; that is designing to satisfy a check. DS-113's reason is weight and honesty
  about what the file carries, and an icon nothing refers to is neither.

**Outputs produced**
- [`examples/reference-deck.html`](../examples/reference-deck.html)

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| No sentence on a slide over 20 words | **met** | `DS-092  sentences over 20 words: 0, paragraphs over 4 sentences: 0` |
| Every sprite symbol referenced at run time | **met** | `DS-113  sprite icons never used: 0 of 9` |
| Slide 2's bottom line is still one sentence with both dates | **met** | 19 words; `DS-202 bottom lines that are not one sentence: 0` |
| No new failure anywhere in the gate | **met** | `0 failure(s): none` across all four stages, the content half and the page count; both variant suites 7/7 and the content suite 3/3 |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Three defects, all of them years-old in a twelve-slide deck that had passed every previous run.** That is the finding worth keeping, not the edits: the deck was built strictly to the ruleset, reviewed, and re-reviewed by two later tasks, and a 44-check gate reported it clean the whole time. What changed is not the deck's quality but the gate's reach — 44 rules checked became 77 — and the three it caught are exactly the kind nobody re-reads for: a note that grew a clause, a bottom line one word over, and an icon left behind by an edit. |
| 2026-08-09 | → proposed | Raised by [T-005](T-005-build-check-the-gate-the-deck-must-pass.md), whose scope puts fixing out and whose new checks found these three. Opened rather than fixed in place, because a gate that edits what it measures cannot be trusted to have measured it. |
