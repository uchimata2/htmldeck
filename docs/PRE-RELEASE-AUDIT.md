# Pre-release audit — htmldeck

**The register.** One row per finding, and the only home for a finding's statement. The method is
[`AUDIT-METHOD.md`](AUDIT-METHOD.md); the run is
[T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md), whose §2 holds the cycle
program this document records the results of.

**Status: running.** Cycles 0 and 1 of 43 are done, and the baseline is below. The tables carry what one
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
| **1** | The human-facing set — `README.md`, `examples/README.md`, `LICENSE`, `shell/README.md`, `examples/sources/README.md`, and the two manifests under `.claude-plugin/` | 7 | 55,103 | `PR-02`, `PR-03`, `PR-04`, `PR-05` | none: all seven read whole. The plan's 54,585 was exact at its own commit; `README.md` and `examples/README.md` both grew on 2026-08-22 after it was measured, so the subject is **+518 bytes** and the re-measure is what caught it. [`PUBLISHING.md`](PUBLISHING.md) section 2 was *applied* as the authority on the covered set, not read — it stays cycle 4's file, and `PR-05` is recorded here so cycle 4 does not raise it twice | 2026-08-23 |

---

## 3. The ranked findings

Ranked by severity, then by the reader's cost. A closed row keeps its id and its statement; its rank
cell is struck through rather than deleted.

| # | Aspect | Sev | Finding | Evidence | Where the fix lives | Remedy — a hypothesis | Effort | Task | Status |
| :-- | :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `PR-01` | project method | **Med** | The plan counts the blindness fixture among *the five shipped decks* and hands it the deck gates as its instrument. `examples/reference-deck-seeded-defects.html` carries one seeded defect per evaluation dimension **on purpose**, at score 0; `check_all.py` classifies it `NOT_A_DECK` and gates it with `seed_defects.py --check`. Cycle 17 as written renders a fixture built to fail and reads the reds as findings. *Six* `.html` files are tracked, not five — `shell/shell.html` is the other exclusion | `python -c "import importlib.util;s=importlib.util.spec_from_file_location('c','tools/check_all.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(len(m.DECKS),sorted(m.NOT_A_DECK))"` prints `4 ['examples/reference-deck-seeded-defects.html', 'shell/shell.html']`, and `git ls-files '*.html'` lists six. The 1,773,568-byte figure is reached **only** by counting the fixture | [`AUDIT-METHOD.md`](AUDIT-METHOD.md) — section 2, and [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md) — section 1's grade table and section 2's cycle 17 | Cut cycle 17 to the four decks `DECKS` names, and give the fixture a row of its own instrumented by `seed_defects.py --check`. **A hypothesis**, per the skill's `pre-release-audit.md` section 5: the fixture may still be worth looking at, and its instrument may be the rubric rather than the deck gates — whoever implements this measures before committing to it | `xs` | — raised at cycle 40; `parent:` is the link, per section 3's decision in T-219 | open. **Must land before cycle 17 runs**, which is this row's *becomes High at the next change* clause |
| `PR-02` | product documentation | **High** | **A shipped deck is in neither human-facing document.** `examples/portfolio-review/` is tracked with its full specification pair, its sources and a per-deck line in `check_all.py`'s `DECKS`, and it is 397,867 bytes of gated deck. [`../examples/README.md`](../examples/README.md) opens *"Four decks."* and its table lists three decks plus the seeded-defects fixture — which the same table calls *"A test fixture, not an example to copy"*. [`../README.md`](../README.md)'s *What is actually here* table sends the reader there for **"Every shipped deck, with what was measured on each"**. That is a completeness claim the tree does not support, and `0.6.0` shipped with it already false | `grep -c portfolio README.md examples/README.md` prints `0` for both. `git ls-files examples/portfolio-review/` lists five tracked files. `figures.py` names three decks in its artifact manifest and not this one, so none of its properties is watched by any document | [`../README.md`](../README.md)'s *What is actually here* table, and [`../examples/README.md`](../examples/README.md) | Give the deck a section in `examples/README.md` and an artifact-manifest entry, and correct the front page's row. **A hypothesis**: the deck is `0.6.0`'s chart-engine example ([T-113](../tasks/T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md)) and the front page describes that feature without pointing at it, so the section may be worth writing from the feature's end rather than the deck's | `s` | — raised at cycle 40 | open |
| `PR-03` | product documentation | **Med** | [`../README.md`](../README.md)'s second paragraph says the repository holds *"plus two decks built strictly to them"*. Four decks ship. The same page's own table implies three — *"the hand-built one above, one assembled through build mode, one an adopter built elsewhere, and a fixture"* — so the front page disagrees with itself two screens apart. Section 2's plan predicted *it says two decks and three are shipped*; the gap has widened by one release since | `python -c "...print(len(m.DECKS))"` prints `4` (the command in `PR-01`'s row). `README.md` line 8 | [`../README.md`](../README.md) | One number. **A hypothesis**: *two* may have meant *built in this repository*, which is now three, so the sentence may need rewording rather than recounting | `xs` | — raised at cycle 40 | open |
| `PR-04` | product documentation | **Med** | **A wrong figure on the front page, in the one place the figure watcher does not look.** [`../README.md`](../README.md) line 206 states `sort-window` is **307 KB**; it is **305 KB**, 312,384 bytes, which is what [`../examples/README.md`](../examples/README.md) line 348 correctly says. 307 KB is the *reference deck's* figure. The durable half is the mechanism: `figures.py` binds `sort-window`'s KB claim to exactly one document and it is the correct one, so the front page's instance is bound to nothing and can drift with every rebuild | `python tools/docs/figures.py --values` reports `sort-window KB 1` against `reference-deck KB 2`, and `0 stale figure(s)` while line 206 is wrong. `stat -c %s examples/sort-window/sort-window.html` prints `312384` | [`../README.md`](../README.md), and the artifact manifest in [`../tools/docs/figures.py`](../tools/docs/figures.py) | Correct the value **and** bind the instance, not one or the other — fixing only the number leaves the next rebuild free to falsify it again. This is the class [T-060](../tasks/T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md) exists to prevent | `xs` | — raised at cycle 40 | open |
| `PR-05` | project method | **Low** | [`PUBLISHING.md`](PUBLISHING.md) section 2 says *"Today the test resolves to three things"*, lists three bullets, then closes *"The test is the rule; **those two** are only today's answer."* The closing sentence was not updated when the owner added `examples/README.md` to the set on 2026-08-11. Nothing depends on the word — the rule is the test, which the same sentence says — so this is a Low and is recorded rather than fixed | `grep -n "three things" docs/PUBLISHING.md; grep -n "those two are only" docs/PUBLISHING.md` prints lines 47 and 59 | [`PUBLISHING.md`](PUBLISHING.md) section 2 | One word. **Batch it** per the skill's `pre-release-audit.md` section 4 rather than raising a task for it. Found while cycle 1 applied section 2 as its authority; the file itself is cycle 4's subject | `xs` | — batched | open |

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
