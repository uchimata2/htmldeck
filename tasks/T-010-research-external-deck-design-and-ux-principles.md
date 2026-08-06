---
id: T-010
title: Research external deck-design and presentation UX principles
type: research
status: done
phase: review
parent: null
blocked_by: []
related: [T-014]
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/research/R2-external-principles.md]
---

# T-010 — Research external deck-design and presentation UX principles

## 1. Specify

**Outcome**
A digest of established, citable principles for presentation design and on-screen reading, filtered
to the ones that change a decision in this plugin — and explicitly listing the ones that do not, so
they are not re-litigated later.

**Why this one**
The corpus shows what the owner does; it cannot say whether it is right. External principle gives
the conventions a defensible basis, and supplies vocabulary and structure the plugin can point at
instead of paraphrasing.

**Scope**
- In: narrative and structure (pyramid principle, SCR, assertion-evidence), cognitive load and
  signalling, typographic scale and measure for projected and on-screen reading, colour theory and
  contrast, data-visualisation practice, accessibility (WCAG AA as the floor), and presentation-UX
  specifics — navigation affordances, progress indication, keyboard and touch control, and how a
  deck behaves when it is *read* rather than presented.
- Out: PowerPoint-specific and Markdown-slide-framework guidance except where it transfers.
- Out: anything that cannot be tied to a rule the plugin would enforce.

**Inputs**
- `docs/BRIEF.md` — "Decisions taken" is the constraint set the principles are filtered against.
- `docs/research/R1-corpus-conventions.md` — what the owner already does, measured.
- `docs/research/R4-prior-art.md` — which of those habits are inherited from the source deck skill
  rather than the owner's, so external principle is not credited to the wrong place.
- `docs/research/R5-assets-and-licences.md` — the asset budget any typographic rule has to fit.
- `docs/research/R6-portability-contract.md` — what the runtime actually permits; a principle the
  deck cannot execute from `file://` is not a principle for this project.
- The installed `artifact-design`, `dataviz` and `artifact-diagramming` skills — checked for rules
  they already own.
- External literature, cited by source.

**Acceptance criteria**
- [ ] Each principle recorded with source, and a one-line statement of what it changes here
- [ ] Conflicts between sources named rather than averaged away
- [ ] A "considered and rejected" list with reasons
- [ ] Accessibility floor stated concretely (contrast ratios, minimum sizes, focus behaviour)
- [ ] Cross-checked against the already-installed `artifact-design`, `dataviz` and
      `artifact-diagramming` skills — where they already own a rule, point at them (T-012 covers
      the reuse decision)

**Answered 2026-08-06 — presented live, with the detail hidden behind interaction.** The deck is
primarily presented, but supporting detail sits behind turning cards, toggles, tabs, floating
layers and tooltips so a recipient can consume it alone. That resolves the density conflict
by splitting the two audiences across an interaction layer rather than compromising between them,
and it makes **progressive disclosure a first-class research area for this task**: signalling
that something is hidden, disclosure affordances, and the cost of interaction during a live talk.
Build implications are T-016.

**Open questions**
- What does the research say about disclosure a *presenter* has to operate live? An affordance
  that reads well to a lone reader can be a liability on stage. — *answered by this research, not
  by the owner*; if the literature is silent, that silence is recorded as a finding and the rule is
  derived from the adjacent evidence rather than invented.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Read the installed `artifact-design`, `dataviz` and `artifact-diagramming` skills and record which rules they **already own** — before gathering sources, so the research does not re-derive rules the project can simply point at | ownership table (feeds T-012) |
| 2 | Gather external sources area by area: narrative structure · cognitive load and signalling · typography for projected and on-screen reading · colour and contrast · data-visualisation practice · accessibility · presentation-UX and navigation · progressive disclosure | source list, cited |
| 3 | Filter each candidate through the decision test — *name the rule this changes in this plugin, or reject it* | rule table with a "changes what" column |
| 4 | Record conflicts between sources as conflicts, with the position taken and why; average nothing | conflicts section |
| 5 | State the accessibility floor as numbers, not intent — contrast ratios, minimum sizes, focus behaviour — and check each against what R6 says the runtime permits | floor specification |
| 6 | Answer the live-disclosure open question explicitly; if the literature is silent, say so and derive from adjacent evidence | progressive-disclosure section |
| 7 | Write up, including the "considered and rejected" list | `docs/research/R2-external-principles.md` |

**Approach decisions**
- **Rules are filtered by consequence, not by pedigree — step 3 is the gate.** A well-cited
  principle that changes no decision here is *rejected and listed*, so it cannot be re-litigated
  later. This is what stops R2 becoming a literature review nobody acts on.
- **Ownership check runs first (step 1), not last.** Running it after the gathering would mean
  paraphrasing rules another skill already states — the "don't restate what another source owns"
  lesson in `docs/BRIEF.md`.
- **The corpus is not evidence of correctness.** R1 says what the owner does; where external
  principle contradicts it, the contradiction is recorded as a candidate change of direction for
  T-014, not resolved quietly in either direction.

## 3. Implement

**Decisions & assumptions**
- **Every principle carries an evidence grade (E1–E4), and grades decide conflicts** — 2026-08-06.
  The field's advice is mostly assertion repeated until it looks like a finding; without a grade
  the loudest rule wins. Generalised as **L-19**.
- **Rejected the pt-based slide-type minimum outright rather than adapting it** — 2026-08-06. It is
  the most repeated rule in the area and it has no measurement behind it, its sources disagree by
  more than 2×, and it is meaningless in a viewport-scaled deck. Replaced with distance-relative
  sizing (P-11), which is the same intent in a form this medium can execute.
- **Adopted two WCAG AAA criteria (2.4.13, 2.3.3) on top of the AA floor, and recorded it as a
  decision rather than folding them into "AA"** — 2026-08-06. A keyboard-driven deck makes the
  focus ring a primary interface, and a deck that wants animation and 3D is exactly the case
  reduced-motion exists for. Labelling them AA would have been quiet standard-inflation.
- **Took a position on richness vs. coherence; did not claim to resolve it** — 2026-08-06. The
  brief wants motion; Mayer's coherence principle is E1 with a large effect and cuts against it.
  R2 §12.1 proposes "motion must encode something" as the reconciliation and hands it to T-014 to
  adopt or overrule. Averaging the two into "use motion tastefully" would have hidden a real
  conflict.
- **Answered the live-disclosure open question from adjacent evidence, and recorded the silence** —
  2026-08-06. No study addresses presenter-operated disclosure directly. Rather than infer a rule
  and present it as sourced, R2 §11 states the gap, then derives P-26 from one E1 result on control
  availability plus the E3 practitioner literature on click-driven builds.
- **Assumption, stated: read evidence is weaker than the measured evidence this project usually
  produces** — 2026-08-06. Nothing in R2 came off a browser here, unlike R5 and R6. The grades are
  the mitigation, not a substitute.

**Outputs produced**
- `docs/research/R2-external-principles.md` — 28 principles across eight areas, five named
  conflicts, nine rejections with reasons, and the WCAG 2.2 AA floor as a table of numbers.
- `docs/LESSONS.md` — **L-19** added (repetition is not evidence; grade the source).
- An unplanned finding, recorded in R2 §3.1: the installed skills **cannot be referenced by path** —
  `artifact-design` and `artifact-diagramming` have no files on disk at all, and `dataviz` lives
  under a version-pinned temp directory. Established with Bash and the file tools rather than the
  shell, and across the application-data tree [R4 §1](../docs/research/R4-prior-art.md) identified,
  because that is precisely where the previous session drew a false negative (rule M11).
  **It raises no new decision** — it independently confirms R4 §7's capability-first contract from
  the opposite direction, and R2 §3.1 says so rather than restating the contract as if it were new.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Each principle recorded with source, and a one-line statement of what it changes here | **met** | R2 §4–§11. 28 principles, each with a *changes here* line naming the plugin rule it moves. Sources in §15, grouped by section; four cited by DOI. |
| Conflicts between sources named rather than averaged away | **met** | R2 §12 — five, each with the position taken and why. §12.1 (richness vs. coherence) is explicitly left unresolved and handed to T-014 rather than compromised. |
| A "considered and rejected" list with reasons | **met** | R2 §13 — nine entries, each with its grade and the reason it fails the decision test. Includes the two AAA criteria, listed so the deviation from "AA is the floor" is not read as an error. |
| Accessibility floor stated concretely (contrast ratios, minimum sizes, focus behaviour) | **met** | R2 §9 — 13 criteria as a table of numbers, levels verified against the W3C's own listing. Two criteria commonly cited as AA are AAA, and are adopted as a recorded decision; 4.1.1 Parsing is noted as retired. |
| Cross-checked against `artifact-design`, `dataviz` and `artifact-diagramming` — where they own a rule, point at them | **met, and it corrected the criterion's own premise** | R2 §3 — all three read in full, ownership tabled. §3.1 is the unplanned half: they cannot be pointed *at*, only pointed to by name, so "point at them" is not literally available. Confirms R4 §7 rather than reopening it. |

**Verified how.** Read evidence, not measured — stated as an assumption in §3 above and on R2's
first page, since this project's other research notes are measurements and the difference matters.
Citation records for the two load-bearing empirical claims were pulled from Crossref rather than
taken from search summaries; the W3C conformance levels were read from the W3C rather than from the
secondary sources that had them wrong. `python tools/tasks/task.py check` passes with 117 document
pointers resolving. Nothing in this task renders, so CLAUDE.md's "open it and look" bar does not
apply — it will apply to whatever T-014 builds from R2.

**Child fix tasks raised**
- none. The one finding that needs another task's attention (§3.1, the pointer problem) belongs to
  an existing task, T-012, and is recorded there rather than duplicated into a new one.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created from the owner's direction to research external principles. |
| 2026-08-06 | → specified | Added the `Inputs` block (R1, R4, R5, R6 and the installed skills) and assigned the live-disclosure open question to the research itself rather than the owner. Scope and the five acceptance criteria accepted unchanged. |
| 2026-08-06 | → planned | Plan expanded from three steps to seven, and three approach decisions recorded — chiefly that the ownership check against the installed skills runs *first*, so the research does not paraphrase rules another skill already owns. |
| 2026-08-06 | → in_progress | All seven steps run. Step 1 immediately returned a finding the plan had not anticipated: the installed skills have no citable path, which changes what "reuse" can mean for T-012. |
| 2026-08-06 | → done | `docs/research/R2-external-principles.md` written; all five acceptance criteria met. Three candidate changes of direction handed to T-014 — progressive disclosure is load-bearing rather than decorative, "richness" needs the test proposed in §12.1, and the heading check becomes semantic. **L-19** raised. |
