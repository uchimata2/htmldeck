---
id: T-071
title: The intermediate specifications carry the sources they rest on
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-069]
related: [T-070]
work_package: PH2
shipped_in: 0.1.5
owner: the project owner
business_value: high
effort: m
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - skills/htmldeck/references/artifacts.md
  - skills/htmldeck/references/build.md
  - tools/deck/spec.py
  - tools/deck/audit.py
  - examples/sort-window/sort-window.foundation.md
  - examples/sort-window/sort-window.slides.md
  - examples/sort-window/sort-window.html
---

# T-071 — The intermediate specifications carry the sources they rest on

## 1. Specify

**Outcome**
The two documents build mode produces before any HTML exists — `<slug>.foundation.md` and
`<slug>.slides.md` — **name the source documents the deck rests on**: the foundation carries the
full list once, and each slide names the ones it used. Today neither does, so the provenance mark
the build emits cannot be true of the slide it sits on, and it is not: both example decks say
`Illustrative model` on every slide while three real source documents sit beside each of them.

**Why this one**
Requested by the owner on 2026-08-10. It is the **upstream** of
[T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md): that task makes the reference deck
cite its three source documents, and a build that has never been told which slide rests on which
document can only invent a uniform mark or reverse-engineer one. **What is measured today:**

- **`<slug>.foundation.md` names a count and a folder.** `examples/sort-window/`'s reads *"Three
  source documents, in `sources/`"* and then a **figure ledger** — `Figure | Value | Origin | Used
  on` — where `Origin` is a bare slug. There is no list of the documents themselves: no title, no
  path, nothing saying what each carries. That list exists for the reference deck only, as
  [`examples/sources/README.md`](../examples/sources/README.md), **hand-written outside the
  pipeline.**
- **`<slug>.slides.md` has eight fields per slide and none of them is a source.** Archetype, Title,
  Bottom line, Structure, Text, Visuals, Animations, Interactive elements. A slide says what it
  claims and never what it rests on.

**The objection this has to answer**
The figure ledger already maps origin to slide, so a per-slide source list looks like **a second
copy of a fact that has a home** — which METHOD rule 3 forbids and this project enforces. The
argument that it is not: **the ledger covers figures, and a slide can rest on a source without
quoting a number.** A date, a definition, a threshold, a quoted phrase, a diagram redrawn from a
source document — none of those is a ledger row, and all of them are things DS-105's mark is
supposed to be true about. Where the two overlap the ledger stays authoritative and the slide field
is checked **against** it rather than trusted, which is the difference between a derived fact and a
duplicated one.

**Scope**
- In: the reference list in `<slug>.foundation.md` — one row per source document, with whatever
  identifies it, where it lives and what it carries.
- In: a source field per slide in `<slug>.slides.md`, and what an **empty** one means — a title or a
  close slide rests on nothing external and that is a legitimate answer, not an omission.
- In: [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md), which is
  where both document shapes are defined, and whatever in `shell/` emits the mark from them.
- In: a check — every slug a slide names resolves to a row in the foundation's list, and every
  listed document is used by at least one slide. **An unused source is either a missing citation or
  a stale file**, and both are findings.
- Out: the mark's own form, its multi-source disclosure and the colophon —
  [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) decides all three, which is why
  this task is blocked by it.
- Out: the quick view — [T-070](T-070-the-quick-view-for-a-source-document.md).
- Out: regenerating `examples/sort-window/`, unless the review finds the new fields change what the
  pipeline would have produced. Then it is in, because a worked example that predates the format is
  the format's first counter-example.

**Inputs**
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — the definition
  of both intermediate documents, and the deviation rule that says a build writes a departure back
  into them — so the format has to hold what a deviation would be written *as*.
- [`examples/sort-window/sort-window.foundation.md`](../examples/sort-window/sort-window.foundation.md)
  and [`sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) — the only worked pair
  in the repository, and the case any format change has to keep working.
- [`examples/sources/README.md`](../examples/sources/README.md) — the reference list this task moves
  into the pipeline, written by hand for the deck that has no foundation document.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-105 on the mark, DS-102 on every figure
  being sourced.

**Acceptance criteria**
- [ ] `<slug>.foundation.md` carries a reference list, and `build.md` defines it — a reader of the
      foundation alone can say what the deck rests on without opening `sources/`
- [ ] Every slide in `<slug>.slides.md` names its sources, and an empty answer is **defined** rather
      than absent
- [ ] The build emits each slide's provenance mark **from that field**, so a deck resting on two
      documents does not say what a deck resting on one says
- [ ] A slug a slide names and the foundation does not list is **reported**; so is a listed document
      no slide uses
- [ ] Where a slide's sources and the figure ledger's `Origin` disagree, the ledger wins and the
      disagreement is reported — the field is checked against it, never a second copy of it
- [ ] `examples/sort-window/` is regenerated or explicitly ruled unchanged, with the reason recorded

**Open questions**
- **Does the reference list replace [`examples/sources/README.md`](../examples/sources/README.md),
  or coexist with it?** Recommended: coexist for now and revisit. The README explains *why* those
  documents exist and what DS-102 requires of an illustrative deck, which is prose a generated
  reference list has no place for; but the three-row table inside it becomes a second copy the day
  the foundation carries one. The reference deck has no foundation document at all, which is what
  makes this awkward rather than obvious. ~~**The project owner decides.**~~ **Settled 2026-08-10:
  coexist, as recommended, and the duplication the question feared did not arise** — see §3.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add the source list to the foundation template, and the `Sources` field to the slide template | [`artifacts.md`](../skills/htmldeck/references/artifacts.md) |
| 2 | Say in build mode that the mark is rendered from the field and never invented | [`build.md`](../skills/htmldeck/references/build.md) |
| 3 | Write the check — four verdicts over the two documents | `spec.py`, under `tools/deck/` |
| 4 | Fill both fields in for the worked example, and reconcile whatever that surfaces | the `examples/sort-window/` pair |
| 5 | Rebuild the example deck's marks from the field, and look at it | `examples/sort-window/sort-window.html` |
| 6 | Run every gate the change can reach | this file §4 |

## 3. Implement

**Decisions & assumptions**

- **The list carries `Slug`, `Source` and *what it carries*, and no path** — 2026-08-10. The slug is
  the join key the ledger's `Origin` already uses; `Source` is the display title the mark needs, and
  without it the build invents one. **The path is not a column**: the file is `<slug>.md` inside the
  directory the section already names once, so a per-row path would be a stored copy of a derivable
  fact (**L-08**). §1's scope asked for *where it lives*, and this answers it once instead of per row.
- **`Sources` is the ninth field and it sits last** — 2026-08-10. Provenance is what the argument rests
  on, not part of the slide's composition, so it does not interrupt the Structure → Text → Visuals run.
  **`none` is a defined answer**, which is the half §1 asked for: a title slide or a close resting on
  nothing external is a state, not a blank.
- **Both templates said *Seven fields per slide* and there were eight** — corrected while editing,
  along with the same sentence in `build.md`. It is now nine. A stated count next to the thing it
  counts is checkable by eye and this one had not been.
- **`examples/sources/README.md` coexists, and the fear behind the question did not materialise.**
  The three-row table there names the *reference* deck's sources; the list added here is the
  *sort-window* deck's. They are different decks, so there is no second copy of anything. The
  reference deck still has no foundation document, which is what made the question look hard — and
  that is a fact about the reference deck rather than a reason to change either file.
- **The build check's absent-subject discipline caught the new tool the same afternoon it was
  written**, and it was right to. `audit.py` enumerates every `*verdicts*` producer under
  `tools/deck/` from the **source**, so `spec.verdicts` failed the run for sitting outside the
  fixture. All four rows are of the form *every X is Y*, so each now reports **None** on an absent
  subject rather than a vacuous pass, and the fixture exercises the producer against an empty pair.
  **This is the first producer in that fixture `check.py` does not consume**, which is the right
  reading of the rule: the discipline is about rows nobody makes choose between undecided and
  satisfied, not about which command prints them.
- **The ledger had to be corrected before it could be checked against.** SPEC-4 makes the ledger
  authoritative, and two `Used on` cells were wrong: `Sort rate` and `Proposed second cut-off` both
  omitted slide 10, which cites each. Calibrating a check against cells known to be wrong is how a
  check learns to agree with a defect, so both were fixed here. Three further figures reach slides
  with no ledger row at all — a completeness gap rather than a wrong cell — and that is
  [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md).

**Outputs produced**
- [`artifacts.md`](../skills/htmldeck/references/artifacts.md) — both templates.
- [`build.md`](../skills/htmldeck/references/build.md) — the `spec.py` step before the first slide,
  and the rule that the mark comes from the field.
- `tools/deck/spec.py` — SPEC-1 to SPEC-4, with a self-test that seeds each of the four defects and
  requires each row to report `False` rather than merely something falsy.
- `tools/deck/audit.py` — the new producer in the absent-subject fixture.
- The `examples/sort-window/` pair — a three-row source list, twelve `Sources` answers, two corrected
  `Used on` cells.
- `examples/sort-window/sort-window.html` — twelve provenance marks rebuilt from the field, and the
  shared shell resynced.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The foundation carries a reference list, and `build.md` defines it | met | Defined in `artifacts.md`, which is where both templates live — `build.md` consumes them and §1 named the wrong file. |
| Every slide names its sources, and an empty answer is defined | met | Twelve answers in the worked example, one of them `none`, and the template says what `none` means. |
| The build emits the mark from that field | met | `build.md` §2 says so, and the worked example is the instance: one source renders as its title, two as the `.sources` control, `none` as the illustrative note. |
| A slug a slide names and the foundation does not list is reported; so is a listed document no slide uses | met | SPEC-2 and SPEC-3, both seeded to fail in the self-test. |
| Where slides and the ledger disagree, the ledger wins and it is reported | met | SPEC-4. The seed that breaks it also breaks SPEC-3, and the self-test says so rather than leaving the overlap unremarked. |
| `examples/sort-window/` is regenerated or explicitly ruled unchanged | met | **Regenerated**, on the review finding §1 allowed for. It needed more than the new fields: the deck had been failing `shell.py check` since T-069 landed, so its component block and script were resynced from `shell/` with the three per-deck declarations preserved. |

**The runs.** `spec.py` on the pair: SPEC-1 to SPEC-4 all pass. `shell.py check`, `component.py check`
and `theme.py check` on the deck: green, the first of them having been red before this task touched it.
`check.py --sources`: **one failure, DS-064**, which is not this task's — the same run against the file
at `d80e0c3` reports the identical row. Raised as
[T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md) rather than
absorbed here.

**Looked at, offline**, per CLAUDE.md rule 6: slides 1, 7 and 12 rendered at 720p. The `.sources`
control sits upper-right as a file glyph and *2 SOURCES*, quiet at rest and not competing with the
eyebrow opposite it. Slide 12 is the one carrying the DS-064 run and it reads cleanly at size; the
15 px is the ask lines under the headline, which is the reading T-083 has to confirm against the
element rather than the picture.

Generalised as **L-61** in [`LESSONS.md`](../docs/LESSONS.md): a check tuned against an unverified
record learns to agree with its gaps.

**Child fix tasks raised**
- [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) — three figures
  reach slides with no ledger row.
- [T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md) — the example
  deck fails DS-064, and did before this task.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | Six criteria met, and the sixth is the one that changed shape: the example needed regenerating for a reason §1 had not anticipated, since it had been failing `shell.py check` since T-069 landed earlier the same day and nothing had said so. Two defects found on the way out are raised rather than absorbed — an incomplete figure ledger (**T-082**) and a `hard` rule failing on the deck before this task touched it (**T-083**). The open question closed as recommended and the duplication it feared was a misreading: the two source lists belong to two different decks. |
| 2026-08-10 | → in_progress | Written formats first, then the check, then the example — so the worked pair was filled in against a definition rather than the definition written to match what the pair happened to have. Two things came back that the specification did not predict. **The build check's absent-subject fixture rejected the new tool**, correctly: it enumerates verdict producers from the source of every module in the directory, so a new one is red the same afternoon, and all four rows now report `None` on an absent subject instead of a vacuous pass. **And the ledger it checks against was wrong in two cells**, both omitting slide 10 — fixed here, because a check calibrated against a record known to be wrong learns to agree with the defect. |
| 2026-08-10 | → proposed | Raised from an owner request that the intermediate specifications list the references used. **Recorded as the gap that was measured, not as the request**: the foundation names a count and a folder and carries a figure ledger whose `Origin` is a bare slug, and the slide specification's eight fields include nothing about sources at all. The reference list that does exist — `examples/sources/README.md` — is hand-written outside the pipeline for the one deck that has no foundation document. **The one-home objection is answered in §1 rather than left for review to find**: the ledger covers figures, a slide can rest on a source it quotes no number from, and where the two overlap the ledger stays authoritative and the slide field is checked against it. Blocked by T-069, which decides the mark's form — this task is what makes that form reproducible from a specification rather than hand-authored. `PH2`: nothing shipped is wrong. |
