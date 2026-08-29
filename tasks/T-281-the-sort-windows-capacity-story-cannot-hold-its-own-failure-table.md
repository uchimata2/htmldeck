---
id: T-281
title: The sort-window deck's capacity story cannot hold its own failure table, and the fix changes its headline
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-248]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-08-30
updated: 2026-08-30
deliverables: []
---

# T-281 — The sort-window deck's capacity story cannot hold its own failure table, and the fix changes its headline

## 1. Specify

**Outcome**
`examples/sort-window/` states one capacity story and every figure derived from it follows. Today it
states three that cannot all be true, and the settlement is a decision about what the deck argues
rather than a number to correct — which is why [T-248](T-248-four-content-errors-in-three-shipped-decks.md)
deferred it rather than taking it.

**Carries** `PR-84` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3, deferred there
2026-08-30 with the arithmetic recorded. **The statement stays in the register** and is not restated
here (the method's umbrella condition 2); what is below is only the decision and what each answer
costs.

**The three statements, and why no two of them hold together.** Measured 2026-08-30 while working
`T-248`:

| Stated | Where | What it implies |
| :--- | :--- | :--- |
| One sorter line at **3,100/hr** | `throughput-model.md`, and the deck's own headline | At most **16,533** parcels sorted between 19:40 and the 01:00 cut-off |
| Peak night **27,600** parcels, peak miss **12.4%** | the volume and failure tables | About **24,700** sorted by the cut-off |
| Overlap of the first trunk's sort into the second's is a **future** limit, above 31,900 a day | slide 10's tripwire | The first trunk clears before **23:40** |

Row 1 and row 2 differ by 8,200 parcels — a **40%** miss where the deck observes 12.4%. Rows 2 and 3
pull opposite ways at **every** constant rate: a rate high enough to leave the ~3,000 unsorted at
01:00 that 84% of a 12.4% miss implies puts the first trunk past 23:40, so the overlap is already
happening; a rate low enough to keep the overlap in the future clears the night before the cut-off
and leaves nothing unsorted to miss.

**Scope**
- In: the capacity statement in
  [`examples/sort-window/sources/throughput-model.md`](../examples/sort-window/sources/throughput-model.md),
  and everything derived from it — the trunk table's finish times, the ledger row in
  `sort-window.foundation.md`, slide 5's night-flow diagram and derivation panel, and slide 10's
  tripwire
- In: the deck's headline, **if the answer is the two-line one**. That is the whole reason this is a
  separate task
- Out: the failure tables. `12.4%`, the 84/16 split and the district table are the deck's observed
  evidence; a model is fitted to them, not the other way round
- Out: any other finding on this deck

**Inputs**
- `PR-84` in [`docs/PRE-RELEASE-AUDIT.md`](../docs/PRE-RELEASE-AUDIT.md) §3 — the statement, the
  evidence and the deferral, which carries the full arithmetic
- [T-248](T-248-four-content-errors-in-three-shipped-decks.md) §3 — what was measured and what was
  refused

**Acceptance criteria**
- [ ] one capacity statement, and every derived figure re-derived from it rather than edited toward
      it — the trunk finishes, the ledger row, slide 5's working and slide 10's tripwire
- [ ] the deck's own arithmetic reproduces its failure table to within the sampling the source
      already states, and the reproduction is shown
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately
- [ ] the rebuilt slides **looked at**, per `CLAUDE.md` rule 6 — recorded in
      [`docs/OWED-LOOKS.md`](../docs/OWED-LOOKS.md) if this task cannot look

**Open questions**
- **Does the depot have one sorter line or two?** — the owner. **The recommendation is two, running
  until the evening shift ends and one through the night**, because it is the only arrangement found
  that reproduces the deck's existing working rather than replacing it: the first trunk's 20,400 at
  6,200/hr finishes **22:57**, the second trunk's 7,200 at 3,100/hr still finishes **01:59** exactly
  as slide 5 derives today, **3,067** are unsorted at the cut-off for a **13.2%** miss against the
  stated 12.4%, and the tripwire moves from 31,900 to about **33,500 a day**. What it costs is the
  headline — *One depot, one sorter line, and a nightly window that closes at 01:00* — which is the
  title slide's standfirst and a sentence `sort-window.slides.md` discusses as a term. The
  alternative is to keep one line and rewrite the failure tables to about 40%, which keeps the
  headline and changes what the deck is about: a depot that misses two parcels in five at peak is a
  different argument from one that misses one in eight.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <the files this task changed>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- <T-NNN or "none">

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-30 | → proposed | Raised out of [T-248](T-248-four-content-errors-in-three-shipped-decks.md) in **B12**, which measured `PR-84`'s three candidate answers and refused all three as number fixes. **A `decision` rather than a `fix`**: the arithmetic is settled and recorded on the register row, and what is left is whether the depot has one sorter line or two — which changes the deck's headline either way it is answered. `PH3` by `CLAUDE.md`'s rule: the published `0.6.0` ships this deck, but no adopter met this as a defect in the plugin, and it is an example's content rather than the product's behaviour. |
