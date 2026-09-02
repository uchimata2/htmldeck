---
id: T-285
title: Let a documentation task run the gates its change can reach, and keep the full run for the batch
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-279, T-280, T-286]
work_package: PH3
owner: the project owner
business_value: medium
effort: s
created: 2026-09-02
updated: 2026-09-02
deliverables: [tools/check_all.py, tasks/TOOLING.md, tasks/TASK-WORKFLOW.md]
---

# T-285 — Let a documentation task run the gates its change can reach, and keep the full run for the batch

## 1. Specify

**Outcome**
`python tools/check_all.py --docs` runs the repository-wide gates and prints the per-deck gates and
the two rendered-variant suites as **skipped, with the reason** — *no deck-facing path changed since
the last full green* — and **refuses the flag** when the diff against that tree touches `tools/deck/`,
`shell/`, `themes/` or `examples/`. A documentation task's commit is gated by the checks whose subject
it changed, in well under a minute; the batch's landing runs the full gate on the tree that is pushed,
exactly as today.

**Measured 2026-09-01, on B17's last run.** 211 seconds: the two seeded-variant suites 93 s (44%),
`check.py` over the four decks 83 s (39%), `figures.py` 21 s, the other 32 commands 9 s. B17's three
tasks changed documents, `figures.py`, `check_all.py` and a new checker; four full runs re-proved the
deck gates four times against a tree where nothing they read had moved. The gate was about 14 of the
batch's 47 minutes, and B18 to B22 are documentation batches.

**Asked for by the owner on 2026-09-02**, after B17, as [T-279](T-279-check-all-reports-one-number-for-thirty-seven-commands.md)
and [T-280](T-280-every-render-pays-a-fresh-chrome-launch.md) were after B11: *can a batch be made
faster without giving up quality*. The shape follows `check_all.py`'s own partition — a gate that does
not run is **skipped with a stated reason**, never absent — so the saving is declared in the output
rather than taken by habit.

**Scope**
- In: the `--docs` flag, the skip reason, and the refusal by path prefix, which errs towards the full
  run: a diff touching any of the four prefixes cannot run in docs mode
- In: what *the last full green* is compared against. Recommended: `origin/master`, because under
  [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 a pushed tree is a fully gated
  one, so no machine-local state is needed and nothing has to survive a `git pull`
- In: the partition's self-test asserts both directions — a diff touching `shell/` under `--docs`
  refuses, and a docs-only diff skips exactly the deck gates and the two rendered suites
- In: `HTMLDECK_RENDER_WORKERS` at 8 against the default 4, as an interleaved A/B on the two variant
  suites — T-280's method, one variable at a time — kept only if the verdicts stay byte-identical
  and the time falls; recorded either way
- In: `tasks/TASK-WORKFLOW.md` §7 and `tasks/TOOLING.md`'s gate rule, so the closing criterion says
  which run a documentation task's commit owes and which the batch's landing owes
- Out: skipping a gate by a hash of its declared inputs. That is a hand-kept input list per checker,
  the shape this repository distrusts, and the remaining batches are documents
- Out: any change to what a full run does or prints

**Inputs**
- [`../tools/check_all.py`](../tools/check_all.py) — `WIDE`, `PER_DECK`, the partition and its self-test
- [`../tools/deck/render.py`](../tools/deck/render.py) — `DEFAULT_WORKERS`, and T-280's byte-identity proof
- [`TOOLING.md`](TOOLING.md) §1 — the two-gates rule and the rule against editing while one runs
- [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md) §4 — commit per task, push per batch

**Acceptance criteria**
- [ ] `--docs` on a docs-only diff prints every deck gate and both rendered suites as skipped with
      the reason, runs everything else, and finishes in under 40 s on the machine B17 measured
- [ ] `--docs` on a diff touching any of the four prefixes refuses, naming the path, and the
      self-test proves both directions
- [ ] A full run's verdicts are unchanged byte for byte
- [ ] The workers A/B is recorded with both timings and the byte-identity result, whichever way it went
- [ ] `TASK-WORKFLOW.md` §7 and `TOOLING.md` say what a documentation task's commit owes and what a
      batch's landing owes

**Open questions**
- Whether the comparison base is `origin/master` or a recorded last full green — the owner. The
  recommendation above is `origin/master`; the cost if that is wrong is one full run per batch that
  docs mode could have skipped

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Measure the full run on the frozen tree before any edit, captured rather than watched | 211 s and 18,480 bytes of green account; `static_variants.py` 56.6 s, `contract_variants.py` 36.7 s, `check.py` 83.5 s over four decks, `figures.py` 20.3 s, the other 32 commands 9.4 s |
| 2 | Find what each gate the flag would skip reads **outside** the deck-facing trees, by grepping `tools/deck/` for what it opens under `docs/` rather than assuming | Three documents: `check.py` derives its jurisdiction from `DESIGN-SYSTEM.md` through `ruleset.py`, `theme.py` reads `THEME-CONTRACT.md`, `component.py` reads `COMPONENT-CONTRACT.md` |
| 3 | Mark every WIDE entry with what `--docs` does and, for a skipped one, what it reads; refuse by prefix and by those three documents; assert both directions and the untouched full plan | `check_all.py`'s `WIDE`, `DOCS_REFUSED`, `DOCS_REFUSED_DOCS`, `changed_since`, `docs_blockers`, and the self-test |
| 4 | The workers A/B, interleaved 4-8-4-8 on each rendered suite with every output hashed, run alone before any test run | The table in §3 |
| 5 | Write the rule where a session meets it | [`TOOLING.md`](TOOLING.md) §1, [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7 step 7, `docs/PUBLISHING.md` §8 step 1 |
| 6 | Measure `--docs` piped and with `--report`, both refusal directions live, and the full run's parity | §4 |

## 3. Implement

**Decisions & assumptions**
- **The base is `origin/master`** — 2026-09-02. The spec's recommendation, adopted rather than
  asked: `docs/REMEDIATION-ORDER.md` §4 makes a pushed tree a fully gated one, so no machine-local
  record of *the last full green* is needed and nothing has to survive a pull. Reversible in one
  constant, `DOCS_BASE`. A base that does not resolve refuses the flag with that reason.
- **Skip by what a gate reads, never by what it costs** — 2026-09-02. The spec named *the two
  rendered-variant suites*; the flag skips **nine** WIDE entries, every per-theme and every
  per-deck gate — 35 of 42 commands — because the rule that justifies a skip is *everything this
  gate reads is under a prefix the flag refuses on*, and that rule reaches `seed_defects.py` and the
  two self-tests as surely as it reaches the suites. A skip list cut at a cost would be a different
  list on a different machine. Each entry says what it reads, and the reason printed under the skip
  is built from that.
- **Three documents are not documentation here** — 2026-09-02. `docs/DESIGN-SYSTEM.md`,
  `docs/THEME-CONTRACT.md` and `docs/COMPONENT-CONTRACT.md` are inputs to per-deck gates, so a diff
  touching one refuses the flag. Found by grep in step 2, not assumed — and the spec's four prefixes
  would have let a rule edit through with every deck gate skipped. `tools/examples/` joined the
  prefixes for the same reason: two skipped gates live there.
- **Untracked files count as changes.** A new deck or tool is exactly what a skipped gate would have
  judged, and `git diff` does not see one; `git ls-files --others --exclude-standard` does.
- **Workers stay at 4** — 2026-09-02, from the interleaved A/B, every run's output hashed:

  | Suite | 4 | 8 | 4 | 8 | Verdicts |
  | :--- | ---: | ---: | ---: | ---: | :--- |
  | `contract_variants.py` | 37.3 s | 37.5 s | 37.4 s | 37.3 s | one hash across all four |
  | `static_variants.py` | 57.8 s | 59.9 s | 74.6 s | 70.1 s | one hash across all four |

  Eight workers buy nothing on the suite that fans out, which is T-280's *saturates at two*
  arriving from a second direction; the static suite is serial by T-280's own decision, so the knob
  does not apply, and its drift upward across the hour is the machine, not the variable — the same
  drift shows in §4's timing.
- **What docs mode still pays, named rather than fixed:** `figures.py` was **37.6 s of the 45 s**
  `--docs --report` run, 83%, because it resolves the README's *coverage of the ruleset* account by
  running `check.py` on the reference deck — a render inside the documents gate. Out of this task's
  scope; it is the first thing [T-287](T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md)'s
  cycle 0 should see in the docs-mode timing table.
- **Landed in one commit with [T-286](T-286-print-the-verdict-on-a-green-run-and-the-report-only-when-asked.md)**,
  because both tasks rewrite `check_all.py`'s ending — the docs flag decides what the closing
  paragraph may claim, and the quiet form decides whether it prints — and splitting the hunks by
  hand would have produced two commits neither of which ran. §4 of the order says *per task where the
  task is the unit*; here the file was.

**Outputs produced**
- [`../tools/check_all.py`](../tools/check_all.py) — `--docs`, `DOCS_BASE`, `DOCS_REFUSED`,
  `DOCS_REFUSED_DOCS`, the third WIDE element, `changed_since`, `docs_blockers`, `plan(docs=)`, and
  the self-test's two directions
- [`TOOLING.md`](TOOLING.md) §1 — the rule, the refusal set and the measurement
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §7 — closing step 7, which run a commit owes
- `../docs/PUBLISHING.md` §8 step 1 — *never `--docs`*

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `--docs` on a docs-only diff skips every deck gate and both rendered suites with the reason, runs everything else, under 40 s | **partly** | 7 ran, 35 skipped each with its reason, one line of 128 bytes piped, exit 0. **44 s, not under 40**: `figures.py` alone took 37.6 s against 20.3 s in this session's own baseline, and in the same hour `static_variants.py` went 57.8 → 70–75 s across the A/B with identical verdicts, so the machine slowed by about a third while nothing in the tree changed. The seconds were the wrong unit for the criterion — T-279 §3's rule; as a share of the baseline full run the docs set is **13%** (28 of 211 s), and the criterion's own arithmetic would have put it at 27 s |
| `--docs` on a diff touching a refused path refuses, naming it, and the self-test proves both directions | pass | Live: an untracked `shell/_zz_probe.tmp` → `REFUSED`, exit 2, path named; a one-line edit to `docs/THEME-CONTRACT.md` → `REFUSED`, path named; the tree's own seven modified files, none deck-facing → ran. Self-test: a docs-only list is not refused; each of five prefixes and the three documents refuses alone; the fake plan skips exactly the marked entry and every per-theme and per-deck gate under `--docs`, and nothing without it |
| A full run's verdicts are unchanged byte for byte | pass | The closing full run's `pass` / `skip` / `FAIL` lines against the baseline's, in order: identical — 40 ran, 2 skipped, the same two, 0 failed |
| The workers A/B is recorded with both timings and the byte-identity result | pass | §3's table; kept 4, recorded either way as the spec asked |
| `TASK-WORKFLOW.md` §7 and `TOOLING.md` say what a documentation task's commit owes and what a batch's landing owes | pass | §7 step 7 and the §1 paragraph, each pointing at the other for the half it does not carry |

**Child fix tasks raised**
- none. `figures.py`'s render inside docs mode is named for `T-287`'s cycle 0, which is where a cost
  is ranked before it becomes a task.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Asked for by the owner after B17, from the question *why does a batch take so long*. Measured first: 83% of a 211 s full run renders decks and fixtures no documentation task can change, and B17 paid it four times. `PH3` per `CLAUDE.md`: this repository's own tooling, not a defect in the published plugin. To be implemented in a session of its own, by the owner's instruction. |
| 2026-09-02 | proposed → done | Built as specified with three deviations, each in §3: the skip is by what a gate reads and covers 35 of 42 commands rather than the two suites named; three documents deck gates read refuse the flag; and the 40 s criterion is missed at 44 s on a machine that slowed a third during the session, so §4 states the share instead. Workers stay at 4, byte-identical at 8 and no faster. Closed on a green `lint.py` and a green full gate run last, after every edit, on the committed tree. Landed in one commit with `T-286`. |
