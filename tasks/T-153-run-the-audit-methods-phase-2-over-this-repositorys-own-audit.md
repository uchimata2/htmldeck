---
id: T-153
title: Run the audit method's phase 2 over this repository's own audit
type: audit
status: proposed
phase: specify
parent: T-130
blocked_by: [T-138]
related: [T-130, T-137]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-14
updated: 2026-08-14
deliverables: []
---

# T-153 — Run the audit method's phase 2 over this repository's own audit

## 1. Specify

**Outcome**
The context-economy audit stops at its own last closure and instead **grades itself**: every finding's
predicted band paired against what it actually bought, what the remedies cost, the method's rubric fed
from how it behaved, and standing policy written into the documents that already govern. **The method
is [`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§3.1, steps 12–16**; it is not restated here.

**Why it exists as a task at all.** Phase 2 runs **once**, after the raised work is implemented, and
until 2026-08-14 nothing scheduled it — the obligation was a paragraph in
[`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §9 depending on the next session reading §9.
That is the shape that became [T-152](T-152-give-look-at-the-rendered-deck-one-operative-home.md) the
day before, and this project does no work without a task file.

**The trigger fired on 2026-08-14: every finding in §6 now has a closed task.**
[T-148](T-148-give-a-measured-figure-a-durable-home.md),
[T-149](T-149-prune-the-memory-index-of-spent-entries.md) and T-152 closed in one session, and
`python tools/docs/findings.py` is what reports it rather than a count anyone keeps.

**What it is blocked on, and what it is deliberately not blocked on.** `T-136` re-runs the external
research with a recorded search record and **can still raise a finding**, which would change the
ranking phase 2 grades; `T-138` repairs the portable half phase 2 reasons from. Those two, and nothing
else. **The rest of the execution order is ordinary backlog** — the ruler, the source cluster, the
motion tasks — and reading it as the condition would park this behind eighteen tasks it has no
relation to. *§9 said "blocked behind six" against the old, wider reading; corrected the same day.*

**Scope**
- In: the five things `R8` §3.1 steps 12–16 name. That document is the operative statement.
- In: the correction record. Four findings in this audit had their band or shape refused by the
  measurement — `CE-07` `L`→`S`, `CE-02` understated twentyfold, `CE-06` saved no bytes and bought a
  gate, `CE-12` measured a unit that did not exist — and phase 2 is where that becomes rubric input
  rather than four separate notes.
- In: what the remedies **cost**, including the case this audit has already met twice: the repository
  ends *larger* while the load path ends smaller.
- Out: raising new findings. `CE-nn` closed at thirteen; anything phase 2 turns up is an ordinary task
  or a `T-136` finding, not a fourteenth row.
- Out: T-137's packaging. Phase 2 produces the evidence; that task carries it outward — and what this
  teaches the *method* goes to [T-137](T-137-package-the-context-economy-method-as-a-skill.md) §1,
  which is the only home that survives these sessions.
- Out: step 16's temptation. **An audit is a guest**: a policy names its governing document, carries an
  extends/narrows/replaces verdict, and yields to the project's own with the collision reported. `R8`
  §3.1 says so and this task does not soften it.

**Inputs**
- `R8` §3.1 — the five steps, which are the specification
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.2 — read before starting, as every audit
  task does; it is the **per-closure** half of this phase rather than a substitute for it
- `python tools/docs/findings.py` — the ranking and its outcomes, derived; do not re-assemble it
- The fourteen closed task records' §3 and §4 — where each band met its measurement

**What specifying must settle**
- Whether the band-versus-outcome pairing is a table in `CONTEXT-AUDIT.md` or a new document. It is
  the audit grading itself, so the audit's own document is the obvious home and the obvious way to
  make that document grow past what anyone reads.
- Whether the `m` band survives its own `specify` pass. It is a first estimate over sixteen closed
  records and **a band moved without a measurement is L-90**.

**Acceptance criteria**
- [ ] Written at `specify`, from `R8` §3.1 rather than from this section
- [ ] Every finding's band is paired against what it bought, **with the original band kept legible**
      (§6.2's correction rule)
- [ ] The remedies' cost is stated, including where the repository grew
- [ ] Any standing policy names its governing document and carries an extends/narrows/replaces verdict
- [ ] What the method learned is in T-137 §1, not only here

**Open questions**
- **Is `m` right?** — the implementer, at `specify`, after reading `R8` §3.1 against the sixteen closed
  records rather than estimating from the step count.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <none yet>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-14 | (blocker cleared) | **`T-136` closed and raised no finding**, so the ranking this task grades has stopped moving — the exact condition §1 named. `blocked_by` is `T-138` alone now. The catalogue it will price is larger than the one that was ranked: 21 → 35, with fourteen techniques screened for the first time, so phase 2 grades a screening whose denominator moved even though no band did. `CONTEXT-AUDIT.md` §4.1 is the argument for the null result. |
| 2026-08-14 | → proposed | Raised at the owner's direction once the trigger fired: the last three findings closed in one session, so every row in `CONTEXT-AUDIT.md` §6 has a closed task. **Not a finding** — `CE-nn` closed at thirteen and this is the method's own phase, so it takes an ordinary task id. Blocked on `T-136` and `T-138` alone; the wider reading in §9, *blocked behind six*, counted ordinary backlog as the condition and was corrected the same day. It sorts last while blocked, so raising it changes nothing about what to work on next — it stops the obligation depending on a paragraph being re-read. |
