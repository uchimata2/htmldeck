---
id: T-090
title: SPEC-5 reports NO SUBJECT on a fully built deck whose slides carry a descriptive aria-label
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-051, T-065, T-066, T-086]
work_package: v0.1
owner: the project owner
business_value: high
effort: s
created: 2026-08-11
updated: 2026-08-11
deliverables:
  - tools/deck/spec.py
  - tools/deck/audit.py
---

# T-090 — SPEC-5 reports NO SUBJECT on a fully built deck whose slides carry a descriptive aria-label

## 1. Specify

**Outcome**
`spec.py` decides SPEC-5 on any deck whose slides carry an accessible name, whatever its wording; and
where it genuinely cannot read a deck it was given, it says so in a way nobody can mistake for *not
applicable*.

**This is [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) arriving through a
door T-051 did not cover.** Leading with the regular expression would undersell it: as *the pattern
is too strict* this is a one-line fix and reads cosmetic. What actually happens is that **a check
reports NO SUBJECT while its subject sits in front of it** — a complete, valid, twelve-slide deck
passed as the third argument. T-051 settled that a check with no subject must not report a pass;
this is the same principle meeting a case where *absent* and *unparsed* are being collapsed into one
verdict, and only one of the two is benign.

**What is wrong**

```python
SLIDE_NUMBER = re.compile(r'aria-label="Slide\s+(\d+)"', re.I)
```

The closing quote sits immediately after the digits, so the pattern matches only an accessible name
that is **nothing but** *Slide N*. Any other form makes `slide_text()` return `{}`, SPEC-5's subject
count stays at zero, and the rule reports `NO SUBJECT` — the identical output to the two-argument run
where no deck was supplied at all.

**Reproduction**

A deck of twelve slides labelled `aria-label="Slide 1 of 12: Too much stock and too little"`:

```
python tools/deck/spec.py <deck>.foundation.md <deck>.slides.md <deck>.html
  SPEC-1   every slide answers Sources                          pass
  SPEC-2   every named slug is listed                           pass
  SPEC-3   every listed source is used                          pass
  SPEC-4   slides agree with the ledger                         pass
  SPEC-5   every ledger row reaches the slides it names         NO SUBJECT
```

Four rules pass, so the deck is plainly being read. Only SPEC-5's own slide parse returns nothing.

**Checked before being called a defect, and then checked again a different way.** The source was read
first, which gave the mechanism. It was then confirmed by **comparing inputs rather than by reading
alone**: `examples/reference-deck.html` carries `aria-label="Slide 1"`, the bare form the pattern was
written against. Reading the source explains a mechanism and cannot tell you which input you are
supplying to it.

**Why the deck is not at fault**
- Neither `DESIGN-SYSTEM.md` nor `COMPONENT-CONTRACT.md` §3.2 constrains the *form* of the
  `aria-label`. §3.2 requires only that a slide carries one.
- A bare *Slide 7* is a **weaker** accessible name than one saying which slide and what is on it. The
  pattern rewards the worse of the two, for a reason unrelated to accessibility.
- The failure is silent in the direction that matters. `NO SUBJECT` reads as *not applicable*, so a
  deck can clear its whole gate with the ledger-to-deck check never having run — and the author has
  no signal that anything was skipped.

**This is the fourth finding of one shape**, after `build.md`'s `--out` flag, `DS-064`'s probe for
the reference deck's composition classes, and `theme.py`'s self-test: **the reference deck's own
conventions encoded as though they were the contract.** Worth naming as a family rather than as four
unrelated bugs — the common repair is to measure what the contract says and not what the example
happens to do.

**Scope**
- In: SPEC-5's slide identification, and the reporting distinction between *no deck given* and *deck
  given, no slide parsed*.
- Out: requiring a particular `aria-label` wording in the design system. That would fix the symptom
  by constraining decks, and would make the accessible name worse.

**Inputs**
- `tools/deck/spec.py`, `SLIDE_NUMBER` and `slide_text()`.
- `examples/reference-deck.html`, which carries the bare form.
- [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md), the rule
  SPEC-5 implements; [T-065](T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md) and
  [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md), the absent-subject family and its fixture.

**Acceptance criteria**
- [x] A deck whose slides are labelled `Slide N of M: <title>` is parsed, and SPEC-5 decides pass or
      fail on it
- [x] `aria-label="Slide 1"` still parses — the reference deck does not regress
- [x] *Deck supplied but no slide parsed* is reported as its own state, distinct from the
      two-argument run's `NO SUBJECT`, and its wording cannot be read as *not applicable*
- [x] A fixture in the T-066 family covers both, so the next widening of the pattern cannot silently
      re-collapse the two states

**Open questions**

| # | The question | Recommendation |
| :-- | :--- | :--- |
| O-1 | Widen the pattern, or stop identifying slides by their accessible name at all? | **Widen it** to a number-bearing prefix — `aria-label="Slide\s+(\d+)\b` — as the small fix. Identifying a slide by `data-name` or by section order would be more robust and is a larger change than this finding justifies on its own |
| O-2 | What does the third state say? | Something that names the cause: `UNREADABLE — deck supplied, 0 slides parsed`. The requirement is only that no reader can take it for *not applicable*, which is the whole of the T-051 principle |

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Settle both open questions before touching the pattern, since O-2 decides whether this adds a fourth verdict value | The decisions, in §3 |
| 2 | Widen `SLIDE_NUMBER` to a number-bearing prefix, and give the unparsed deck its own verdict | `tools/deck/spec.py` |
| 3 | Seed both states in `spec.self_test`, and the collapse itself in the absent-subject fixture | `tools/deck/spec.py`, `tools/deck/audit.py` |
| 4 | Measure the reproduction: the adopter's label form against both patterns, and the built deck before and after | The runs, in §4 |

## 3. Implement

**Decisions & assumptions**
- **O-1 taken as recommended.** `SLIDE_NUMBER` becomes `aria-label="Slide\s+(\d+)\b` — a prefix that
  bears a number, rather than an accessible name that is nothing else. Identifying slides by
  `data-name` or by section order is the more robust design and remains untaken: it is a larger change
  than one adopter's report justifies, and this pattern is the only thing standing between a deck and
  a rule that runs.
- **O-2 closed against its own recommendation**, which is the note worth keeping. §1 proposed a third
  label — `UNREADABLE — deck supplied, 0 slides parsed` — as a value beside `pass`, `FAIL` and
  `NO SUBJECT`. It is a **FAIL whose text opens `DECK UNREADABLE`** instead, because
  [`../tools/deck/audit.py`](../tools/deck/audit.py)'s absent-subject fixture partitions every
  producer's rows on `True in oks` and `False in oks`: a fourth value falls in neither, and this
  family would leave the fixture that exists to hold it. The requirement in §1 is only that no reader
  can take the state for *not applicable*, and a `FAIL` naming the cause satisfies it while keeping
  the run's exit status non-zero — which is the half that stops a skipped gate reading as a green one.
  The precedent is [T-076](T-076-a-verdict-producer-that-exits-instead-of-reporting.md), where a
  declaration already in the file held the better reason.
- **The bare form is not deprecated.** Both decks in this repository carry it and the fix widens what
  is accepted rather than moving it.

**Looked at and withdrawn, which is the note worth keeping.** A grep put
`sec.setAttribute('aria-label', (i+1) + '. ' + s.dataset.name)` in
[`../shell/deck.js`](../shell/deck.js) next to this rule's pattern, and it reads like the shell
overwriting the very attribute `SLIDE_NUMBER` matches — a second finding of the same shape, and it
was a line away from being raised as one. It is not. That `sec` is a **new** `<section>` built for
the reading view a few lines below; the slide keeps the accessible name its author wrote. The two
views label differently and neither contradicts the other.

Recorded because the near miss is the transferable part: this task's own §1 says the repair for this
family is *measure what the contract says, not what the example does*, and a task raised off one grep
line would have been the same error wearing the opposite clothes. Reading the six lines after the
match cost nothing;
[T-089](T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md) is the record of what a task
withdrawn on a false premise costs instead.

**Outputs produced**
- [`../tools/deck/spec.py`](../tools/deck/spec.py) — the widened pattern with the reason beside it;
  `unreadable` as its own verdict; the docstring's account of the deck argument now names three
  states, not two; `self_test` seeds three label forms and the unparsed deck.
- [`../tools/deck/audit.py`](../tools/deck/audit.py) — the fixture asserts that *no deck* and *a deck
  that parsed to nothing* do not arrive at one verdict.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck labelled `Slide N of M: <title>` is parsed, and SPEC-5 decides on it | met | The reproduction, rebuilt from the shipped example: all 12 labels rewritten to `Slide N of 12: …`. `SPEC-5 … pass`, exit 0. The two patterns measured on that same file — **old 0 matches, new 12** — which is the mechanism rather than an inference from reading the source. |
| `aria-label="Slide 1"` still parses — no regression | met | `examples/sort-window/` unchanged: five rows pass, exit 0, and `check.py` on it reports `0 failure(s)`. Both decks in this repository carry the bare form, and `spec.self_test` now holds all three label shapes rather than the run holding one. |
| *Deck supplied, no slide parsed* is its own state, unmistakable for *not applicable* | met | Same deck with every label stripped: `SPEC-5 … - DECK UNREADABLE: a deck was supplied and no slide parsed from it, so this rule did not run. Every slide needs aria-label="Slide N ..."` — **FAIL**, exit 1. The two-argument run still prints `NO SUBJECT` and exits 0. |
| A fixture in the T-066 family covers both, so a later widening cannot re-collapse them | met | Two, at both altitudes. `spec.self_test` fails if any of the three label forms stops deciding, or if the unparsed deck reports anything but `False` with a cause-naming text. `audit.self_test` asserts the pair directly — `None` with no deck, `False` with an unreadable one — in the file that holds every producer to what an absent subject means. |

**Child fix tasks raised**
- none. The `deck.js` line §3 describes is not a defect - it labels the reading view's own section,
  not the slide - and the check that established that was made before anything was raised.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (shipped) | **Shipped in `0.2.1`.** **One of the three fixes this release is for**, and one of the two raised from outside the repository. It was `Awaiting v0.1.6` here, which is a phase name and was never a version anyone could install. |
| 2026-08-11 | → done | All four criteria met. **The one-line pattern was the smaller half.** `SLIDE_NUMBER` closed on the quote, so it accepted only the accessible name both decks here happen to ship, and the adopter's better name parsed to nothing — measured as **0 matches against 12** on the same file rather than read out of the source. The half worth keeping is the second state: *deck supplied and unreadable* now FAILs with the cause in its text, where it used to print the words a two-argument run prints. It stayed inside the three verdict values on purpose — `audit.py`'s fixture partitions rows on `True in oks` and `False in oks`, so a fourth value would have taken this family straight back outside the fixture built to hold it (T-066, T-075), which is the same trade T-076 settled the same way. Awaiting a `v0.1.6` patch release with [T-091](T-091-build-md-documents-icons-set-as-a-single-pair.md); the sequence is `docs/PUBLISHING.md` section 8. |
| 2026-08-11 | (specify) | **Moved to `v0.1`**, arriving labelled `v0.3` from the reporting project, which does not hold htmldeck's phase rule. An adopter's deck hit this on the published `0.2.0`, and [`../CLAUDE.md`](../CLAUDE.md) makes that a `v0.1` patch rather than a later improvement — [`../docs/BRIEF.md`](../docs/BRIEF.md) *v0.2* states the same line from the other side: an adopter cannot hit a v0.2 item, or it would be a v0.1 patch. Size does not enter it; the effort line at `l` sorts the phases that are not the published one. Sixth reopening of v0.1, and the first from outside this repository. |
| 2026-08-11 | → proposed | Raised by the AI Training 06 (DentalPro) project, htmldeck's first adopter outside this repository — the sixth defect it has found and the second raised here rather than as a GitHub issue. Found while building a twelve-slide board deck on 0.2.0: the rebuild was expected to settle SPEC-5, and with the deck supplied it was still `NO SUBJECT`. The adopting project deliberately did **not** shorten its slide labels to suit the pattern, on the grounds that nothing in the ruleset asks for the bare form and shortening them would trade accessibility for a regular expression. |
