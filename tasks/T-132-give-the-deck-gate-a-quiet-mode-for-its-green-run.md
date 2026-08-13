---
id: T-132
title: Give the deck gate a quiet mode for its green run
type: deliverable
status: proposed
phase: specify
parent: T-130
blocked_by: []
related: [T-130]
work_package: PH3
owner: the project owner
business_value: high
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - tools/deck/check.py
---

# T-132 — Give the deck gate a quiet mode for its green run

## 1. Specify

**Outcome**
`check.py` can report a passing deck in a line instead of 169. **The finding is `CE-03`**, stated in
full in
[`../docs/research/R8-context-economy-for-coding-agents.md`](../docs/research/R8-context-economy-for-coding-agents.md)
§8 and ranked second in [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6; it is not restated
here.

**The measurement, because it is the argument**
On 2026-08-13, `python tools/deck/check.py examples/sort-window/sort-window.html` printed **17,391
bytes, 169 lines, in 16.7 seconds — on a run that passed.** The whole release gate over the whole
repository printed 8,233. A deck session runs this repeatedly.

**The default does not change.** A person reading a green run's per-rule listing is why it exists,
and [`check_all.py`](../tools/check_all.py) already demonstrates the shape: children are quiet unless
`--verbose` asks otherwise. This is the same choice one altitude down, with the polarity that suits
who calls it — the agent passes the flag.

**Scope**
- In: a flag that prints failures plus one summary line.
- In: the summary line carrying **how many rules were evaluated**, so a quiet green run cannot hide a
  rule that silently stopped being checked — that is the risk `CE-03` names.
- In: [`../skills/htmldeck/references/`](../skills/htmldeck) wherever it tells an adopter to run the
  gate, since an adopter pays this too.
- Out: changing the default, changing any verdict, or changing `--json`, which already exists for a
  consumer that parses.
- Out: the other gates. Their green output is 1,073 bytes and under; this one is the outlier.

**Inputs**
- [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §2.3 — the measured table, and `CE-03`
- [`../tools/deck/check.py`](../tools/deck/check.py) — `main()` already parses `--sources`,
  `--print-pages`, `--skip-contract` and `--json`
- [`../tools/check_all.py`](../tools/check_all.py) — the precedent for quiet-by-default with an opt-in

**Acceptance criteria**
- [ ] A passing deck reports in one line plus a rule-evaluated count; a failing deck still reports
      every failure in full
- [ ] The default output is byte-identical to today's, verified rather than assumed
- [ ] The flag composes with `--sources`, `--print-pages` and `--skip-contract`, and `--json` is
      unaffected
- [ ] Measured after the change: green-run bytes, against 17,391
- [ ] Wherever the skill tells an adopter to run the gate, it says which form to use and why

**Open questions**
- None.

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
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, second of four. `CE-03`: **one gate on one deck prints more on a green run than the entire release gate prints over the whole repository** — 17,391 bytes against 8,233. The default stays; the risk the audit names is a quiet green run hiding a rule that stopped being checked, so the summary line carries the count of rules evaluated and that is a criterion rather than a note. |
