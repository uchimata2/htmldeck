---
id: T-132
title: Give the deck gate a quiet mode for its green run
type: deliverable
status: done
phase: review
shipped_in: unreleased
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
| 1 | Capture today's green output to a file **before touching anything**. A criterion that says *byte-identical* needs a baseline that predates the edit | The before-bytes |
| 2 | Add `summary(res)` — one line carrying the coverage account as the sum it has to be, so `checked` falling while `owned` holds is visible | The line `CE-03`'s risk needs |
| 3 | Add `--quiet` to `report`, taken only when `res["ok"]`. A run that is not green prints exactly what it prints today | The flag |
| 4 | Keep the header notes under `--quiet`. They say which halves ran, and `--print-pages` moves no count in the summary — the note is the only thing that distinguishes those two runs, in the default report as well | A quiet run that cannot hide a skipped half |
| 5 | Assert in the self-test that `--quiet` on a failing run still exits 1 and still names the failure. The whole objection to a quiet gate is that it hides something | The one assertion that matters |
| 6 | Verify: default byte-identical against step 1, red path identical to red default, `--json` untouched, and composition with `--sources`, `--print-pages`, `--skip-contract` | The §4 table |
| 7 | Say which form to use in [`build.md`](../skills/htmldeck/references/build.md) §3 and [`pipeline.md`](../skills/htmldeck/references/pipeline.md), where an adopter meets the command | The two skill edits |

## 3. Implement

**Decisions & assumptions**
- **`--quiet` is a promise about green runs only, and about nothing else** — 2026-08-13. A failing
  run prints byte-for-byte what it prints today, verified on the seeded-defect deck. This is the
  narrowest thing that answers `CE-03`, and it means the flag can be passed by default by a caller
  who cannot know in advance whether the run will pass.
- **The header notes survive the flag** — 2026-08-13. `--print-pages` moves **no count** in the
  summary line: the run is `115 owned = 84 checked + …` with the flag and without it. The only thing
  that distinguishes those two runs, in the default report as much as here, is the note
  *printed page count and geometry: NOT RUN*. Dropping the notes to reach a literal one line would
  have made a quiet run unable to say which halves of the check ran, which is the same class of
  concealment the criterion's rule count exists to prevent. The cost is three lines, 345 bytes rather
  than about 160.
- **`report(verbose=False)` already existed and nothing ever passed it** — 2026-08-13. It drops the
  verdict table and the excusal list and keeps the entire coverage account, so it was never the mode
  this task wanted. Left alone rather than repurposed: `--quiet` is a different question, and
  overloading the older parameter would have made one flag mean two things.
- **`check_all.py` was left calling the default** — 2026-08-13. It already captures child output and
  prints it only for a failure, so `--quiet` would save it nothing and would change what a failing
  release run has to show. The outlier this task is about is a person or an agent running the gate
  directly, in a loop.

**Outputs produced**
- [`tools/deck/check.py`](../tools/deck/check.py) — `summary()`, `--quiet`, the self-test assertion,
  and the usage block
- [`build.md`](../skills/htmldeck/references/build.md) §3 — which form to run and why
- [`pipeline.md`](../skills/htmldeck/references/pipeline.md) — the flag in the command's signature

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A passing deck reports in one line plus a rule-evaluated count; a failing deck still reports every failure in full | met, with a deviation | The summary is one line and carries `115 owned = 84 checked + 27 excused here + 4 excused in the rules + 0 undecided + 0 SILENT, 0 failing`. **It is preceded by the two header notes rather than standing alone** — §3 records why, and it is a deliberate departure from the literal wording, not a rewording of the criterion. The failing path is **byte-identical** to today's on the seeded-defect deck, 18,253 bytes and exit 1 either way |
| The default output is byte-identical to today's, verified rather than assumed | met | Captured before the first edit and compared afterwards: **17,581 bytes, equal** |
| Composes with `--sources`, `--print-pages` and `--skip-contract`; `--json` unaffected | met | `--sources` in every run above. `--print-pages --quiet` passes in **250** bytes. `--skip-contract` exits 1 on this deck with the flag and without it, and the two outputs are identical — the flag changes no verdict. `--json --quiet` parses, 33,959 bytes, exit 0 |
| Measured after the change: green-run bytes, against 17,391 | met | **345 bytes, 4 lines**, against a default that has grown to **17,581** since the audit measured 17,391 — **51×**. With `--print-pages`, 250 bytes |
| Wherever the skill tells an adopter to run the gate, it says which form to use and why | met | `build.md` §3 puts `--quiet` in the per-batch loop and says to drop it when you want the listing; `pipeline.md` carries it in the signature |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | 345 bytes against 17,581 on a green run, 51×, with the default proved byte-identical against a baseline captured before the first edit. **One criterion is met with a stated deviation**: the summary line is preceded by the two header notes, because `--print-pages` moves no count in the account and the note is the only thing distinguishing a run that printed from one that did not. **The flag was made safe by assertion rather than by review** — the self-test drives a failing result through the quiet path and requires exit 1 and the failure's id in the output. |
| 2026-08-13 | → in_progress | Built in the planned order. Two things found on the way: `report()` already had an unreachable `verbose=False` that was never this mode, and `check_all.py` gains nothing from the flag because it already suppresses child output. Both recorded in §3 rather than acted on. |
| 2026-08-13 | → planned | Seven steps, and step 1 is *capture the before-bytes first* — a byte-identical criterion has no instrument once the edit is in. |
| 2026-08-13 | → specified | §1 arrived written, with the deliverable declared, the measurement stated as the argument, and no open question. |
| 2026-08-13 | → proposed | Raised from [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md)'s ranking at the owner's review, second of four. `CE-03`: **one gate on one deck prints more on a green run than the entire release gate prints over the whole repository** — 17,391 bytes against 8,233. The default stays; the risk the audit names is a quiet green run hiding a rule that stopped being checked, so the summary line carries the count of rules evaluated and that is a criterion rather than a note. |
