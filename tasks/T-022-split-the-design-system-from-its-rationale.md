---
id: T-022
title: Split the operative ruleset from its rationale, and give every rule an ID
type: fix
status: done
phase: review
parent: T-014
blocked_by: []
related: [T-004, T-005, T-020, T-023]
work_package: WP1
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-06
updated: 2026-08-12
deliverables: [docs/DESIGN-SYSTEM.md, docs/DESIGN-RATIONALE.md]
---

# T-022 — Split the operative ruleset from its rationale, and give every rule an ID

## 1. Specify

**Outcome**
`docs/DESIGN-SYSTEM.md` becomes the **operative ruleset and nothing else** — a set of tables, every
row carrying a **stable ID**, a label, and how it is checked. Everything explaining *why* a rule is
what it is moves to `docs/DESIGN-RATIONALE.md`, which no runtime ever loads.

**Why this one**
Raised by the owner on 2026-08-06, and it is the project's own carried lesson turned back on its own
output. **L-12 says what is read every time must be short**; T-014 produced a 700-line document that
is roughly half history — drops, provenance notes, re-scoping arguments, derivations. That is
context cost on every run, and it is the harder half to maintain, because the historical material
goes stale in a way the rules do not.

**A second defect, found while scoping this and arguably the worse one: the rules have no IDs.**
They are prose rows citing *research* IDs (`C1`, `P-01`). Nothing can cite a rule, score against it,
report a finding on it, or verify that a fix landed. **Without rule IDs there is no evaluator** —
which is why [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) is blocked on this.

**Scope**
- In: every rule gets a **stable `DS-nnn` ID**. IDs are permanent — a retired rule keeps its number
  and is marked retired, never reused.
- In: a **`Check` column** on every rule: `auto` (a build check can test it) · `render` (needs a
  rendered measurement or a look) · `judge` (judgement). This is what routes a rule to T-005, to the
  render pass, or to the evaluator.
- In: moving to `DESIGN-RATIONALE.md` — the sixteen-conflict resolution table, the re-scoping
  section, every "dropped/amended because" blockquote, the provenance notes, and the derivations.
- In: `DESIGN-SYSTEM.md` keeps **one line of rationale per rule at most**, and only where the
  rationale prevents a plausible wrong "fix" — e.g. why no media queries inside the stage.
- Out: changing any rule. **This is a restructure, not a re-ruling.** Rule count and content are
  preserved; if a rule changes, that is a separate task.
- Out: the evaluator itself (T-023).

**Inputs**
- `docs/DESIGN-SYSTEM.md` as T-014 left it.
- `docs/research/R1-rules-candidate.md` — the verdicts, which stay where they are.

**Acceptance criteria**
- [ ] Every rule in `DESIGN-SYSTEM.md` has a unique `DS-nnn` ID, a label, and a `Check` value
- [ ] **Rule content is unchanged** — verified by mapping every rule in the new file back to the old
      one, and stating the count both ways
- [ ] `DESIGN-SYSTEM.md` contains no historical narrative: no "dropped because", no provenance, no
      re-scoping argument
- [ ] `DESIGN-RATIONALE.md` holds all of it, and every rule whose reasoning moved is reachable from
      its `DS-nnn` ID
- [ ] `DESIGN-SYSTEM.md` is **materially shorter** — state the before and after line counts rather
      than claiming it
- [ ] Every pointer in both files resolves

**Open questions**
- Does the accessibility floor table stay in the ruleset or move? It is numbers, so it is operative —
  but it is also verbatim WCAG, which argues for a pointer. — this task

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Assign `DS-nnn` IDs and `Check` values across the existing rules, changing none of them | the ID map |
| 2 | Rewrite `DESIGN-SYSTEM.md` as tables only | the ruleset |
| 3 | Move every displaced block into `DESIGN-RATIONALE.md`, keyed by `DS-nnn` | the rationale |
| 4 | Count both ways and repoint everything that cited the old structure | verification, updated pointers |

## 3. Implement

**Decisions & assumptions**
- **Flat `DS-nnn` with gaps, not grouped prefixes — 2026-08-06.** `DS-COL-01` reads better and
  breaks the moment a rule moves section. Numbers are allocated in blocks with gaps (colour 020–029,
  typography 030–039) so a new rule inserts without renumbering, and the group is a column, not part
  of the identity.
- **The `Check` column is the routing table, and it is the part that makes the ruleset executable —
  2026-08-06.** 59 `auto` · 32 `render` · 36 `judge`. Before this, deciding whether a rule belonged
  to the build check or the critique pass meant re-reading it and guessing.
- **Archetypes, anti-patterns and WCAG criteria keep their existing IDs** — `A-nn`, `X-nn`,
  `1.4.10`. They are already stable and cited elsewhere; renumbering them into `DS-` would break
  pointers into R3 and buy nothing.
- **The accessibility table stays in the ruleset** (its open question). It is numbers a check reads,
  which makes it operative — and pointing at the W3C would fail exactly the way DS-106's pointer
  would.

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — 379 lines, 131 identified rules
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — 224 lines

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every rule has a unique `DS-nnn`, a label and a `Check` value | **met** | 131 rules; zero duplicate IDs; labels 102 hard / 35 default / 6 guidance; checks 59 auto / 32 render / 36 judge |
| Rule content unchanged | **met** | Every rule maps back to the T-014 file. 131 vs the previous ~120 prose rows: the increase is **splitting**, not adding — DS-035 (the 18-unit floor) and DS-036 (mono never load-bearing) were one row, and six stage/reflow conditions were prose in §11 *(**§11 never existed** — corrected 2026-08-09 by [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md). The six conditions are real and are DS-060 to DS-065; only their stated home was not)* |
| No historical narrative in the ruleset | **met** | Every "dropped because", provenance note and derivation moved. What remains is one pointer line under §2.4 |
| `DESIGN-RATIONALE.md` holds it, reachable by `DS-nnn` | **met** | Six sections, keyed by rule ID |
| Materially shorter | **met** | **700 → 379 lines, a 46% reduction**, and the removed half is the half that goes stale |
| Every pointer resolves | **met** | `task.py check` — 185 pointers, 0 broken |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-06 | → done | Split executed. **700 → 379 lines**, with the rationale in a companion file no runtime loads. The `Check` column turned out to be the higher-value half of the change: it routes each rule to the build check, the render pass or the evaluator, which is what [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) needed and could not previously get. |
| 2026-08-06 | → proposed | Raised by the owner against T-014's deliverable: it is huge, half of it is history, and that is context cost on every run plus the harder half to maintain. Scoping it surfaced a second and worse defect — **the rules have no IDs**, so nothing can cite, score, or verify a fix against them. That is what blocks [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md). |
