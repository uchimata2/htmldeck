---
id: T-217
title: Speaker notes attach by position, and the second example proves position is not identity
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-213, T-211]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-22
updated: 2026-08-22
shipped_in: unreleased
deliverables: []
---

# T-217 — Speaker notes attach by position, and the second example proves position is not identity

## 1. Specify

**Outcome**
`presenter.py` attaches a note to the slide the specification wrote it for, or refuses to build. It
never attaches one to a different slide.

**Why this one**
[T-213](T-213-build-the-presenter-build-and-the-marker-that-keeps-it-unshippable.md) shipped an hour
ago and attaches notes **by position**: specification slide `n` goes to the deck's `n`th slide. That
held on the one example it was built against and **fails on the very next one.**

| Deck | Deck slides | Specification slides | Spec slide 9 lands on |
| :--- | ---: | ---: | :--- |
| `sort-window` | 12 | 12 | slide 9, correctly |
| `portfolio-review` | 12 | 12 | slide 9, correctly |
| `measure-first` | **14** | **12** | **slide 9, which is the wrong slide** |

`measure-first.html` opens with a title slide and closes with a `Sources` slide, and the
specification numbers neither. So its specification slide 1 is the deck's slide 2, and every note is
one slide early from there on: a note written for *€450k in, €1.2m a year out* would appear under
*Each answer needs the one before*.

**Nothing reports it.** The build succeeds, the panel shows a note, the note is real, the slide is
wrong — and the only guard in the tool is a count check that passes here, because 9 is less than 14.
**This is L-131 in a second place inside one day**: the mechanism is correct and its subject is not,
which is the failure mode that survives every check because nothing about it is broken.

**Why `high` and why now.** The wrongness is invisible in exactly the situation the artifact exists
for — a person presenting, reading a note that belongs to a slide they are not on. It is also
`unreleased`, so fixing it now costs one commit and no adopter ever sees it.

**Scope**
- In: attach a note by **matching the slide's title** against the deck's own `data-name`, and refuse
  to build when a note's slide cannot be resolved to exactly one.
- In: normalise before comparing. The deck's `data-name` for that slide is `450k in, 1.2m a year
  out` where the specification says `€450k in, €1.2m a year out` — the currency symbols do not
  survive into the attribute, so an exact string compare would fail on a slide that plainly matches.
- In: **no silent position fallback.** Falling back is what this task is fixing; an unresolvable
  note is an error naming the note, the title it looked for, and the deck's slide names.
- In: the two remaining example specifications get a `Notes` field, which is what surfaced this.
- Out: changing how notes are authored, the marker, or anything in `check.py`. T-213's design is
  unaffected — this is the lookup, not the mechanism.

**Inputs**
- [`tools/deck/presenter.py`](../tools/deck/presenter.py) — `notes_of`, and `main`'s count guard,
  which is the guard that was not enough.
- [`examples/measure-first/measure-first.slides.md`](../examples/measure-first/measure-first.slides.md)
  and [`examples/portfolio-review/portfolio-review.slides.md`](../examples/portfolio-review/portfolio-review.slides.md).
- **L-131** — a correct measurement of the wrong subject passes every check you have.

**Acceptance criteria**
- [ ] A note attaches to the slide whose title it was written under, on all three example decks —
      including the one whose numbering is offset
- [ ] A note whose title matches no deck slide **fails the build**, naming the note and what it
      looked for; it never lands on a neighbour
- [ ] A title that matches more than one deck slide fails the same way
- [ ] Currency symbols and punctuation do not break a match that a reader would call obvious
- [ ] All three example specifications carry a `Notes` field, and each presenter build shows it on
      the right slide
- [ ] Each presenter build still fails `check.py` on **DS-088 and nothing else**
- [ ] `python tools/check_all.py` green

**Settled during specify**
- **Title, not position, and not an authored id.** An id in the specification would be a third thing
  to keep in sync with the two that already exist, which is the argument
  [L-132](../docs/lessons/L-132.md) made about markers one task ago. The title is already written in
  both documents, and a title that has drifted between them is a finding worth an error rather than
  a mismatch worth guessing through.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Parse the specification's slide **titles** alongside its notes, from the `## Slide n — title` heading | `tools/deck/presenter.py` |
| 2 | Read the deck's slides as `(index, data-name)` and match on a normalised form — lowercase, alphanumerics only — so `€450k in, €1.2m a year out` resolves to `450k in, 1.2m a year out` | same |
| 3 | Refuse to build on zero or multiple matches, naming the note's slide, its title, and the deck's slide names. Replace the count guard, which cannot see this | same |
| 4 | Print the resolved mapping on every run, so the attachment is visible rather than assumed | same |
| 5 | Extend the self-test with the offset case, the no-match case and the ambiguous case | same |
| 6 | Author a note in the two remaining example specifications | `examples/measure-first/…`, `examples/portfolio-review/…` |
| 7 | Build all three, confirm each note lands on its own slide, and re-run `check.py` on each | recorded in §3 |

**Step 4 is not decoration.** The defect was invisible because the tool reported a count and never
what it had decided. A build that prints *slide 9 → deck slide 10 · €450k in, €1.2m a year out* can
be checked by reading it.

## 3. Implement

**Decisions & assumptions**
- **Match on the slide title, normalised to lowercase alphanumerics** — 2026-08-22. The deck's
  `data-name` for the offset slide is `450k in, 1.2m a year out` where the specification says
  `€450k in, €1.2m a year out`; the currency symbols do not survive into the attribute, and an exact
  compare would refuse a match a reader would call obvious. Refusing is expensive here, because it
  stops the build.
- **No position fallback, at all** — 2026-08-22. Zero matches or several both stop the build and
  print the note, the title it looked for, and every slide name in the deck. A fallback is the
  defect being fixed.
- **The tool prints its mapping on every run** — 2026-08-22. `spec slide 9 -> deck slide 10` is
  checkable by reading it; a count is not. The original defect survived because the tool reported
  how many notes it had placed and never where.

**Two more defects, both found by reading the output rather than by any check**
- **The horizontal rule between slides was inside the note.** `measure-first` separates its slides
  with `---`, so the last field on a slide ran into it and the rendered note ended in three hyphens.
  Visible in the first screenshot, invisible to everything else.
- **The last slide's section had no end, so its note swallowed the rest of the file.** A slide was
  bounded by the next `## Slide`, and the final slide is followed by `## Open — needs a decision`
  and its table — all of which became part of the note. `portfolio-review`'s note came back 40
  characters of intent followed by an open-questions table. Sections are now bounded by the next
  heading of any level.

**Both were the same mistake as the one this task was raised for**: a parse that is correct on the
example it was written against, and silently wrong on the next one. Three examples found three
defects; one example found none of them.

**Outputs produced**
- [`tools/deck/presenter.py`](../tools/deck/presenter.py) — `resolve`, title matching, the two
  parse bounds, the printed mapping, and five new self-test cases
- [`examples/measure-first/measure-first.slides.md`](../examples/measure-first/measure-first.slides.md)
  — a note on slide 9, the offset case
- [`examples/portfolio-review/portfolio-review.slides.md`](../examples/portfolio-review/portfolio-review.slides.md)
  — a note on slide 12, the close

**Verification**

| Deck | Deck slides | Note authored on | Lands on | `check.py` |
| :--- | ---: | :--- | :--- | :--- |
| `sort-window` | 12 | spec slide 3 | deck slide 3 | 1 failure, DS-088 |
| `measure-first` | 14 | spec slide 9 | **deck slide 10** | 1 failure, DS-088 |
| `portfolio-review` | 12 | spec slide 12 | deck slide 12 | 1 failure, DS-088 |

All three shipped decks byte-identical across the task — `20a45a40…`, `363cd051…`, `756d0350…`.
`presenter.py` self-test passes, including the offset, no-match, ambiguous, horizontal-rule and
trailing-section cases. `python tools/check_all.py` green.

**Looked at** (CLAUDE.md rule 6): rendered deck slide 10 of the `measure-first` presenter build —
the offset case, and the only one where a position-based attachment would have been wrong. The
banner reads correctly, the panel names slide 10, and the note is the one written under
*€450k in, €1.2m a year out*. That render is what surfaced the trailing `---`.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A note attaches to the slide it was written under, on all three decks including the offset one | met | `measure-first` spec slide 9 → deck slide 10, printed by the tool and confirmed in the render |
| A note matching no deck slide fails the build, naming what it looked for | met | Self-tested; the message also lists every deck slide name |
| A title matching more than one deck slide fails the same way | met | Self-tested |
| Currency symbols and punctuation do not break an obvious match | met | `€450k in, €1.2m a year out` resolves to `450k in, 1.2m a year out` |
| All three specifications carry a `Notes` field, each shown on the right slide | met | Three notes, three correct placements |
| Each presenter build fails `check.py` on DS-088 and nothing else | met | 1 failure on each of the three |
| `python tools/check_all.py` green | met | 0 failures, 0 unclassified, 0 stale |

**Child fix tasks raised**
- none

**What this task found that it was not looking for**
- **Two further parse defects**, both of the same species as the one it was raised for, and both
  found by *looking at the output* rather than by any check: a slide separator inside a note, and a
  final slide with no section end.
- **T-213's argument that one worked example was enough was wrong**, and it is worth stating
  plainly: a single instance cannot demonstrate that a mapping is a mapping. The second example
  found the defect within minutes of being written.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | → done | **Three examples, three defects; one example had found none of them.** Notes now attach by title with no position fallback, a slide section ends at the next heading of any level, and a separator between slides stays out of the note. All three presenter builds place their note correctly and fail `check.py` on DS-088 alone; all three shipped decks are byte-identical. **The generalisable part is already written down** - this is **L-131** in a second place inside one day, so no new lesson was raised for it. |
| 2026-08-22 | → proposed | **Found by doing the thing T-213 declined to do.** That task authored one worked note and argued that three would be copy; the owner asked for the other two, and the second deck it touched has a title slide and a `Sources` slide its specification does not number. `high` because a presenter reading the wrong slide's note is the exact situation the artifact exists to serve, and `s` because the fix is a lookup. **The argument for one worked instance was wrong in a way worth recording**: a single example cannot show that a mapping is a mapping. |
