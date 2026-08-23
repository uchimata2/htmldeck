# Pre-release audit — htmldeck

**The register.** One row per finding, and the only home for a finding's statement. The method is
[`AUDIT-METHOD.md`](AUDIT-METHOD.md); the run is
[T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md), whose §2 holds the cycle
program this document records the results of.

**Status: not started.** No cycle has run. The tables below are empty because nothing has been
audited, not because nothing was found.

---

## 1. The run

| | |
| :--- | :--- |
| Requested | 2026-08-22, by the owner |
| Target release | **the next one.** Reordered by the owner on 2026-08-22: cut the release first, audit afterward. That release was `0.6.0`, cut 2026-08-23. The number the audit's own release takes is [`PUBLISHING.md`](PUBLISHING.md) §8's to decide at the time, not this document's to predict |
| Baseline | to be recorded by cycle 0 — `python tools/check_all.py` and `python tools/tasks/lint.py`, both green, on a frozen tree |
| Id space | `PR-nn`, never reused, never renumbered |

---

## 2. Coverage ledger

One row per cycle, written when the cycle ends. Every tracked file lands in exactly one of **read**,
**skipped with a stated reason** or **produced a finding**; a file in none of the three is a gap in
the audit ([`AUDIT-METHOD.md`](AUDIT-METHOD.md) §2).

| Cycle | Subject | Files | Bytes read | Findings | Skipped, and why | Session |
| :--- | :--- | ---: | ---: | :--- | :--- | :--- |
| — | *no cycle has run* | | | | | |

---

## 3. The ranked findings

Ranked by severity, then by the reader's cost. A closed row keeps its id and its statement; its rank
cell is struck through rather than deleted.

| # | Aspect | Sev | Finding | Evidence | Where the fix lives | Remedy — a hypothesis | Effort | Task | Status |
| :-- | :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| | | | *none recorded* | | | | | | |

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
