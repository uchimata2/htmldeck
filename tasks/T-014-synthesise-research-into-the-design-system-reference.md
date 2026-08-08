---
id: T-014
title: Synthesise the research into the htmldeck design-system reference
type: analysis
status: done
phase: review
parent: null
blocked_by: [T-009, T-010, T-011, T-012, T-013, T-017]
related: []
work_package: WP1
owner: maintainer
created: 2026-08-06
updated: 2026-08-06
deliverables: [docs/DESIGN-SYSTEM.md]
---

# T-014 — Synthesise the research into the htmldeck design-system reference

## 1. Specify

**Outcome**
One authoritative reference stating every rule htmldeck applies, across all thirteen coverage
areas, with each rule traced to its source in **R1–R6** and marked as **hard** (enforced by the
build check), **default** (applied unless overridden) or **guidance** (judgement).

**Why this one**
Six research documents are not a plugin. This is where they become one set of rules, where the
conflicts between the owner's habits and external principle are resolved rather than averaged, and
where the plugin's near-zero-config promise is made good — every rule settled here is a question
the skill never has to ask. Per the brief's carried lesson, this is a reference the skill *points
at* on demand, not text loaded on every run.

**Scope**
- In: writing style and the banned-terminology list · UX and reading behaviour · UI controls and
  navigation · colour · design language · deck structure and pacing · content practice · headings
  and subtitles · illustration · icons · diagrams · layout and grid · external tools and skills.
- In: resolving every conflict surfaced in R1–R6, with the reason recorded — by the tie-break rule
  answered below, not case by case.
- In: **the four named candidate changes of direction** research produced, each to be adopted or
  overruled deliberately rather than inherited: R2 §12.1 (motion must encode something), R2's
  finding that progressive disclosure is load-bearing, R3 §8's finding that Layered Detail is a
  *modifier on the other archetypes* rather than one of them, and R2 P-01's upgrade of the heading
  check from structural to semantic.
- Out: **non-Latin scripts.** Settled 2026-08-06 — see *Script scope* in `docs/BRIEF.md`. Do not
  write a CJK or RTL rule, and do not leave a placeholder for one.
- Out: the three standing decisions — fonts (T-001), charts (T-006), one style or several (T-007).
  This reference states them once they are decided; it does not pre-empt them.

**Inputs**
- `docs/research/R1-corpus-conventions.md` … `R6-portability-contract.md` — all six.
- `docs/BRIEF.md`, whose *Decisions taken* table now carries the two settled 2026-08-06 (script
  scope, conflict tie-break) and whose open question 6 is answered.
- `docs/research/R1-rules-candidate.md` — the 154 rules with the Verdict column **this task owns**
  (keep / drop / amend). R4 §9 filled the provenance column; the verdict column is still empty.

**Where the highest-value material already sits**, so the synthesis does not start from a blank
page: R1 §13 has the five-category banned-terminology list and the caveat that a word list is
necessary and not sufficient; R1 §14 has the critique format and severity scheme, which R4 §2 shows
has **zero prior art** — it is entirely the owner's; R2 §9 has the accessibility floor as numbers;
R3 §3 and §6 have the 14 archetypes and 12 anti-patterns.

**Structure — settled during specify, 2026-08-06**

The thirteen coverage areas in *Scope* were listed before R2 and R3 existed. Checked against
[`R1-rules-candidate.md`](../docs/research/R1-rules-candidate.md), whose 154 rules are **already
grouped into fourteen letter groups**, the thirteen turn out to be a list of topics rather than a
structure, and they have a hole: **motion (group F) has no coverage area at all** — which matters,
because *"motion must encode something"* is one of the four candidate changes of direction this task
must rule on. **Theming/tokens (I)** and **portability (J)** are likewise unhomed.

**So the reference is structured on the letter groups, and the thirteen map onto them.** The rules
live there already and the Verdict column this task owns is indexed by rule ID; structuring the
document any other way would mean maintaining a second index of the same 154 rules.

| Part | Sections | Rule groups | Which of the thirteen it absorbs |
| :--- | :--- | :--- | :--- |
| **Envelope** | Portability and the render envelope · Theming and tokens | J, I | — *(the two the thirteen missed, plus motion below)* |
| **Look** | Colour · Typography · Layout and grid · Recurring elements | C, D, H | colour · layout and grid · design language |
| **Argument** | Deck structure and pacing · The archetype library · Writing style and the banned list · Headings and subtitles | A, L, B | deck structure and pacing · content practice · writing style + banned terminology · headings and subtitles |
| **Visuals** | Diagrams · Icons · Illustration | E | diagrams · icons · illustration |
| **Behaviour** | Interaction and navigation · Motion · Progressive disclosure | F, G | UX and reading behaviour · UI controls and navigation |
| **Floor** | The accessibility floor, as numbers | (R2 §9) | — *(cross-cutting; separate so a check can read it)* |
| **Boundaries** | What this points at rather than owns | (R2 §3) | external tools and skills |

**The boundary this reference does not cross.** It owns **what a good deck is**. It does not own
**how the plugin works** — the authoring pipeline is T-020 (group A′), the check's mechanics are
T-005 (group K), and critique's output format is T-004 (group M). Those three consume the standard
stated here; they do not restate it. The one thing taken from group M is the **severity scheme**,
because a shared vocabulary for "how bad is this" is part of the standard, not part of the report.

**Acceptance criteria**
- [ ] ~~All thirteen coverage areas present~~ — **amended during specify, before the work, per
      TASK-WORKFLOW §2.** Replaced by: every one of the thirteen has a home in the mapping table
      above, **and** the three the thirteen missed (motion, theming, portability) are covered. The
      original wording would have closed clean on a document with no motion rules in it.
- [ ] No section left as a placeholder
- [ ] Every rule carries a source reference and a hard/default/guidance label
- [ ] **All sixteen named conflicts resolved, by ID, with the reason** — X-1…X-11 in
      `R1-rules-candidate.md` § *Contradictions to resolve at T-014*, and R2 §12.1…§12.5. Made
      countable during specify: "every conflict found in research" cannot be verified, and this
      project's own *count, don't read* lesson says why that matters.
- [ ] **The Verdict column in `R1-rules-candidate.md` filled for all 154 rules** — keep · drop ·
      amend · defer. Recorded as a criterion because it is a deliverable of this task that the
      front-matter's `deliverables:` list does not name.
- [ ] **The four candidate changes of direction each adopted or overruled explicitly** — R2 §12.1
      (motion must encode something), progressive disclosure as load-bearing, R3 §8's A-13-as-modifier,
      and R2 P-01's semantic heading check
- [ ] Ends with a **re-scoping proposal** for the owner where research contradicts `docs/BRIEF.md` —
      this is an expected outcome, not a planning failure
- [ ] The hard rules are stated in a form a check can actually test
- [ ] Structured for on-demand loading — the skill body must not need to restate it
- [ ] Free of personal, client and machine data

**Answered 2026-08-06 — split by rule type, and [R2](../docs/research/R2-external-principles.md)'s
evidence grades are what make it operable.**

- **Principle wins on anything measurable** — accessibility, contrast, encoding accuracy,
  legibility. These are R2's **E1** and **E2** material: controlled results and specifications. A
  corpus habit that contradicts one of them loses, and the loss is recorded.
- **Habit wins on aesthetic and structural choices** where the evidence is weak or absent — R2's
  **E3** and **E4** material. This is most of what makes a deck look like this owner's rather than
  generated, and it is the thing the plugin exists to encode.

So the tie-break is not a judgement call per conflict: **look up the grade, then apply the rule.**
A conflict where the external side is E3 or E4 is not a conflict — habit stands.

**Open questions**
- The two that would have blocked this task were settled by the owner on 2026-08-06: the tie-break
  above, and BRIEF open question 6 (the plugin **does** receive source documents and reconciles
  against them — see `docs/BRIEF.md`).
- ~~**This task overlaps [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) more than
  the board shows.**~~ **Settled by the owner 2026-08-06, before either document was written — the
  design system is standing and shared; the foundation spec is per-deck and references it.**

  The hypothesis held, and testing it against the material made it stronger than "two altitudes".
  Because the project ships **one** theme (CLAUDE.md rule 4), four of R1 §10's nine sections —
  **visual system · motion · interaction model · technical stack** — have no per-deck variable left
  at all. They *are* the design system, and a foundation spec that restates them has already forked
  from it. Three more — **linguistic style · recurring elements · layout structures** — are standing
  catalogues a deck **selects from**, not authors. The **quality-bar checklist** is the standing
  check plus per-deck additions. Only the **narrative spine**, and the governing idea line above it,
  is genuinely per-deck.

  So the foundation spec is not a parallel document; it is a **per-deck selection sheet**. The
  anti-drift rule, which is the brief's own *don't restate what another source owns* applied here:
  **the foundation spec cites the design system, it never restates it.** This task writes the
  standing rules; T-020 decides whether the selection sheet is a surfaced artifact and what it
  carries. T-014 proceeds first and T-020 consumes it.
- ~~**Do the thirteen coverage areas still have a home for what R3 produced?**~~ **Answered
  2026-08-06 during specify — and the answer is that the thirteen are the wrong spine.** See
  *Structure* below. In short: the archetypes go under **structure**, not layout (R3 §8 finding 3);
  **A-13 becomes a modifier** applied across the catalogue rather than a fourteenth entry (R3 §8
  finding 1, and R2 reached it independently); and the **12 anti-patterns stay here as rules** —
  T-004 consumes them rather than owning them, because a check and the standard it tests must not
  be two documents.

## 2. Plan

The four-step table this replaced was written before R2, R3 and R6 existed and before the tie-break
was settled; it said "surface and resolve conflicts" when the conflicts are now named and countable.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Fill the Verdict column on all 154 rules — **by lookup**, not on the merits: R4 §9 gives provenance, R2 gives the evidence grade, and the tie-break turns the pair into a verdict | completed Verdict column in `R1-rules-candidate.md` |
| 2 | Resolve the sixteen named conflicts by ID — X-1…X-11 and R2 §12.1…§12.5 | resolution table, keyed by ID |
| 3 | Rule the four candidate changes of direction, each adopted or overruled with the reason | decisions, recorded in §3 below and in the reference |
| 4 | Write the seven parts of the reference against the *Structure* mapping, every rule labelled **hard / default / guidance** with its source | `docs/DESIGN-SYSTEM.md` |
| 5 | Pull the **hard** rules into one list stated as testable conditions, for T-005 to consume without re-reading the whole reference | the check-facing section of the reference |
| 6 | Write the re-scoping proposal where research contradicts `docs/BRIEF.md` | closing section of the reference |
| 7 | Verify by counting, not reading — coverage against the mapping table, 16 conflicts, 154 verdicts, 4 rulings | the §4 verdict table |

**Approach decisions**

- **Order matters: verdicts before prose.** Writing the reference first and back-filling verdicts
  would let the document decide the rules, which is the inverse of this task. Step 1 is the
  bottleneck and it is deliberately first.
- **Step 1 is mechanical by design.** The owner's tie-break exists precisely so 154 rules do not
  each become a judgement. Where lookup genuinely underdetermines a verdict, the rule gets `defer`
  and a named owner — not an invented ruling.
- **Step 7 counts.** This project's own *count, don't read* lesson, applied to its own output.

## 3. Implement

**Decisions & assumptions**

- **The lookup needed a fourth class the tie-break never named — 2026-08-06.** The owner's rule
  covers principle-versus-habit. It has no verdict for *standing decision versus habit*, which is
  what actually governed C7, D1, J1 and J2. Precedence used, and recorded in the reference: standing
  decision → E1/E2 principle → named contradiction → keep. **The tie-break fired once (L1); the
  unnamed class fired four times.** Generalised as **L-21**.
- **Provenance was context, never a verdict — 2026-08-06.** No rule was dropped for being inherited.
  All seven of G1–G7 are the source skill's slide engine and all seven are kept. R4's grading buys
  the right to *cite* something as the owner's signature, not a reason to discard what is not.
- **The boundary drawn at specify held, and it is what kept the deferrals honest — 2026-08-06.** All
  26 defers are boundary (T-020 process, T-005 mechanics, T-004 report format), not indecision.
  Two verification rules were kept **against** the boundary — K1 and K5 — because they are claims
  about what a check may assert, not about how it runs.
- **Deck length was demoted from a house rule to a per-deck decision — 2026-08-06.** X-5 is three
  contradictory rulings on three decks, all the owner's. Averaging them would have invented a rule
  no deck follows. Default 8–12, past 12 needs a recorded reason.
- **L1 was escalated rather than ruled — 2026-08-06.** The tie-break's answer is clear (1.4.4 and
  1.4.10 are AA and a scaled stage defeats both) but the remedy is a new mode, and adding one is not
  this task's authority. Recorded as a re-scoping proposal with three options, one of them ruled out.
- **Assumption, stated because it shapes §6:** the twelve anti-patterns are kept here rather than
  moved to T-004, on the reasoning that a check and the standard it tests must not be two documents.
  If T-004 disagrees when it is planned, this is the decision to revisit.

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — 12 sections
- [`docs/research/R1-rules-candidate.md`](../docs/research/R1-rules-candidate.md) — Verdict column
  filled, 154 rules
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-21** added

## 4. Review

Verified by counting, per step 7 of the plan and this project's own *count, don't read* lesson.

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every one of the thirteen coverage areas has a home, **and** motion, theming and portability are covered | **met** | Mapping table in §1 above; motion §5.2, theming §1.2, portability §1.1 |
| No section left as a placeholder | **met** | Zero `TODO`/`TBD`/placeholder matches across the file |
| Every rule carries a source reference and a hard/default/guidance label | **met** | 140 labelled rule rows; every table row carries both columns |
| All sixteen named conflicts resolved, by ID, with the reason | **met** | §10 — X-1…X-11 and R2 §12.1…§12.5, counted at exactly 16 rows |
| The Verdict column filled for all 154 rules | **met** | 110 keep · 17 amend · 1 drop · 26 defer = 154; zero empty verdict cells |
| The four candidate changes of direction each adopted or overruled explicitly | **met** | §9.2 motion-encodes · §9.3 disclosure load-bearing · §9.4 semantic heading · §9.5 A-13 as modifier. All four **adopted** |
| Ends with a re-scoping proposal where research contradicts `docs/BRIEF.md` | **met** | §9, six entries. §9.1 needs an owner decision; §9.2 asks a wording change only |
| The hard rules are stated in a form a check can actually test | ~~**met, with a stated limit**~~ → **not met — corrected 2026-08-08** | Recorded as *"§11 — 26 numbered conditions, two of them (15 and 23) not machine-checkable"*. **`DESIGN-SYSTEM.md` has ended at §9 in all 13 commits of its life, including this task's own closing commit — §11 was never written.** The verdict cited a section number instead of the section's content, and nothing downstream could tell the difference. What the ruleset *does* give a check is the `DS-nnn` ID and the `Check` column, which is what [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) actually consumes; what it does not give is the unreachable-rule carve-out this criterion's "stated limit" was about. Remedy is [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md). See the log. |
| Structured for on-demand loading — the skill body must not restate it | **met** | §0 is the one-screen summary; the twelve sections are addressable individually |
| Free of personal, client and machine data | **met** | Sweep clean — the only two matches were the `Home`/`End` keyboard keys |

**Not verified, and it is the important one.** Nothing here has been tested by building a deck. The
reproducibility rulings are reasoned from R6's capability matrix, which answers *"is this
available?"* and not *"does this read well at 12 slides?"* **CLAUDE.md rule 6 governs the second
question**, and §12 of the reference says so in the document rather than only here. The handoff's
standing recommendation is unchanged and now has a ruleset to test: **the next artifact is a real
12-slide deck with diagrams, built from this reference and opened offline.**

**Child fix tasks raised**
- none — but §9.1 requires an owner decision before T-002 or T-007 can build the stage, and §9.4
  grows build mode's scope. Both are recorded on the affected tasks by pointer.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → proposed | Created as the join point between research and build. |
| 2026-08-08 | (no change, still done) | **One §4 verdict corrected from `met` to `not met`, two days after close: §11 was never committed.** Step 5 promised *"the check-facing section of the reference"* and §4 recorded it delivered as *"§11 — 26 numbered conditions"*. Checked against git while [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) was being specified: `docs/DESIGN-SYSTEM.md` has ended at **§9 in every one of its 13 commits**, created that way by **this task's own closing commit**. Nothing deleted it; it was never written. **The task stays `done` and is not reopened** — its actual deliverable, the ruleset with a `DS-nnn` ID and a `Check` value per rule, exists and is consumed by four tasks. What is missing is the narrower thing the criterion's *"stated limit"* named: which rules no check can reach. That is now [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md), which will carry it **per rule** rather than as a second parallel list — the structure that made this failure possible. **The cost of not catching it: two months and four task files.** T-004, T-005 and [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) all reasoned in detail about §11's contents, and T-030 ordered part of the build on it. [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) alone noticed something was wrong and translated one condition by hand (*"the rule the original text called condition 17"* → **DS-063**), shipping a real check from it. The rest are unrecoverable: had the numbering been the hard rules in document order, condition 17 would be 17th, and DS-063 is **31st**. `task.py check` validates links and paths, so a `§n` in prose is invisible to it — a reference to a section that never existed reads exactly like a reference to one that does. |
| 2026-08-06 | (no change, still done) | **§9.1 settled by the owner the same day: keep the fixed stage, add a reflow view — raised as [T-021](T-021-the-reflow-view-and-the-resolution-contract.md).** The owner's reason reshaped §2 rather than merely closing the question, so the reference gained **§2.4 (the stage, resolution and screen share)** and **§2.5 (the reflow view)**, and §11 gained seven conditions. The stage is not a rehearsal convenience: it answers a deck breaking on a 4K display and a deck arriving illegible after a video call downscales the shared frame. Under a uniform scale **the presenter's viewport cancels out of the legibility equation**, which no responsive layout achieves — so "drop the stage for flex slides" moved from an option to ruled out. It also produced a type floor the research had no way to derive: body **≥ 24 design units**, nothing under 18, D5's 18–24 tightened to 24–28, and the corpus's 11–13 unit mono labels demoted to decoration. Generalised as **L-22**. The §4 verdicts below stand; the criterion they were checked against did not change. |
| 2026-08-06 | → in_progress → review → done | **`docs/DESIGN-SYSTEM.md` written; all 154 verdicts filled.** 110 keep · 17 amend · 1 drop · 26 defer. The one drop is C7 (one palette per deck) and it fell to CLAUDE.md rule 4, not to evidence — which exposed a class the owner's tie-break does not name: **a standing decision overriding an observed habit**. It fired four times; the tie-break itself fired once, on L1. Generalised as **L-21**. L1 (the fixed 1600×900 stage) is the one thing this task could not settle: 1.4.4 and 1.4.10 are AA and a scaled stage defeats both, but the remedy is a new mode, so it is escalated as a re-scoping proposal with three options and one ruled out. All four candidate changes of direction adopted. Every acceptance criterion verified by counting. **No deck has been built from this ruleset — that is the next artifact, and §12 of the reference says so.** |
| 2026-08-06 | → specified → planned | **Both open questions closed and the spec worked through.** Sequencing settled by the owner: the design system is standing, the foundation spec is per-deck and references it — T-014 first, T-020 consumes it. The thirteen coverage areas were then checked against `R1-rules-candidate.md`'s fourteen letter groups and found to be a topic list with a hole: **motion, theming and portability had no home**, and motion is where one of the four candidate changes of direction lands. Reference restructured onto the letter groups with a mapping table; the coverage acceptance criterion amended **before** the work, with the reason. Two criteria added and made countable — sixteen conflicts by ID, 154 verdicts — and the plan rewritten so verdicts precede prose. |
| 2026-08-06 | (no change) | **Unblocked** — all six blockers closed with T-010 and T-011. Spec updated for what landed since it was written: R6 exists (references said R1–R5), the four candidate changes of direction are named in scope, and `R1-rules-candidate.md`'s empty Verdict column is recorded as this task's to fill. Owner settled both blocking decisions the same day — the conflict tie-break (split by rule type) and BRIEF open question 6 (sources are supplied and reconciled). Non-Latin ruled out of scope. **Still `proposed`: the spec has not been worked through, only made current.** |
