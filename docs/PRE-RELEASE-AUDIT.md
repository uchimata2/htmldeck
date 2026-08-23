# Pre-release audit — htmldeck

**The register.** One row per finding, and the only home for a finding's statement. The method is
[`AUDIT-METHOD.md`](AUDIT-METHOD.md); the run is
[T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md), whose §2 holds the cycle
program this document records the results of.

**Status: running.** Cycle 0 of 43 is done and its baseline is below. The tables carry what one
cycle found and nothing more — a subject with no row has not been audited, it has not been
reached.

---

## 1. The run

| | |
| :--- | :--- |
| Requested | 2026-08-22, by the owner |
| Target release | **the next one.** Reordered by the owner on 2026-08-22: cut the release first, audit afterward. That release was `0.6.0`, cut 2026-08-23. The number the audit's own release takes is [`PUBLISHING.md`](PUBLISHING.md) §8's to decide at the time, not this document's to predict |
| Baseline | **Both green on a frozen tree at `62c3ab3`, 2026-08-23.** `python tools/check_all.py` — exit 0; 35 commands ran, 2 skipped with their reasons, 0 failed; 49 tracked tools, 0 unclassified, 0 stale; 294.5 s. `python tools/tasks/lint.py` — exit 0, all four steps, 3.3 s, with eleven advisories `taskmd check` prints and does not fail on (a duplicate index in [`RELEASE-PHASES.md`](RELEASE-PHASES.md), ten unresolved section references), baselined here so a later cycle can tell a new one from an old one. **The seconds are a dated record, not a stated figure** (**L-95** point 4) — re-run the command, never cite this cell |
| Id space | `PR-nn`, never reused, never renumbered |

---

## 2. Coverage ledger

One row per cycle, written when the cycle ends. Every tracked file lands in exactly one of **read**,
**skipped with a stated reason** or **produced a finding**; a file in none of the three is a gap in
the audit ([`AUDIT-METHOD.md`](AUDIT-METHOD.md) §2).

| Cycle | Subject | Files | Bytes read | Findings | Skipped, and why | Session |
| :--- | :--- | ---: | ---: | :--- | :--- | :--- |
| **0** | Instruments and baseline — `check_all.py`, `findings.py`, `lint.py`, `query.py` | 4 | 61,356 | `PR-01` | none: all four read whole, and the file list re-measured to the planned 61,356 bytes exactly | 2026-08-23 |

---

## 3. The ranked findings

Ranked by severity, then by the reader's cost. A closed row keeps its id and its statement; its rank
cell is struck through rather than deleted.

| # | Aspect | Sev | Finding | Evidence | Where the fix lives | Remedy — a hypothesis | Effort | Task | Status |
| :-- | :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `PR-01` | project method | **Med** | The plan counts the blindness fixture among *the five shipped decks* and hands it the deck gates as its instrument. `examples/reference-deck-seeded-defects.html` carries one seeded defect per evaluation dimension **on purpose**, at score 0; `check_all.py` classifies it `NOT_A_DECK` and gates it with `seed_defects.py --check`. Cycle 17 as written renders a fixture built to fail and reads the reds as findings. *Six* `.html` files are tracked, not five — `shell/shell.html` is the other exclusion | `python -c "import importlib.util;s=importlib.util.spec_from_file_location('c','tools/check_all.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(len(m.DECKS),sorted(m.NOT_A_DECK))"` prints `4 ['examples/reference-deck-seeded-defects.html', 'shell/shell.html']`, and `git ls-files '*.html'` lists six. The 1,773,568-byte figure is reached **only** by counting the fixture | [`AUDIT-METHOD.md`](AUDIT-METHOD.md) — section 2, and [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md) — section 1's grade table and section 2's cycle 17 | Cut cycle 17 to the four decks `DECKS` names, and give the fixture a row of its own instrumented by `seed_defects.py --check`. **A hypothesis**, per the skill's `pre-release-audit.md` section 5: the fixture may still be worth looking at, and its instrument may be the rubric rather than the deck gates — whoever implements this measures before committing to it | `xs` | — raised at cycle 40; `parent:` is the link, per section 3's decision in T-219 | open. **Must land before cycle 17 runs**, which is this row's *becomes High at the next change* clause |

---

## 4. Accepted without action

A `Low` row may close here instead of in a task, with a reason and a date. A `High` or `Medium` row
may not.

| # | Reason | Date |
| :-- | :--- | :--- |
| | *none* | |

---

## 5. Phase 2 — predicted against measured

Written after the remedies exist, never at ranking time — the taskmd skill's `pre-release-audit.md`
owns that rule.

| # | Predicted sev / effort | Measured | What the difference was |
| :-- | :--- | :--- | :--- |
| | | *not run* | |
