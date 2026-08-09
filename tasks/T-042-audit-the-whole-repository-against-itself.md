---
id: T-042
title: Audit the repository against itself — stale claims, unreachable rules, and unchecked references
type: audit
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-004, T-005, T-008, T-036, T-037, T-039, T-041]
work_package: none
owner: maintainer
created: 2026-08-09
updated: 2026-08-09
deliverables: []
---

# T-042 — Audit: the whole repository against itself

## 1. Specify

**Audit scope**

Everything tracked in the repository, plus the session memory that governs how it is worked on:
`CLAUDE.md` · `docs/` including `docs/research/` · `tasks/` (all 41 files, open and closed) ·
`skills/htmldeck/` · `.claude-plugin/` · `examples/` · `tools/` · `.handoff/config.md` ·
`.gitignore` / `.gitattributes` · the memory directory at
`~/.claude/projects/C--Work-AgentPlugins-htmldeck/memory/`.

Read against the artifacts rather than against each other alone: every count re-derived by running
the tool that owns it, every measurement re-taken against the deck it describes.

**Review dimensions**
- [x] Factual accuracy — every stated number re-measured against the artifact it describes
- [x] Internal consistency — no contradiction across deliverables, or between a doc and a tool
- [x] Completeness — every rule the ruleset declares a gate has something that gates it
- [x] Standard compliance — task files follow `TASK-WORKFLOW.md`; tools follow **L-04**, **L-05**, **L-07**
- [x] Link and file hygiene — pointers, section references, stray and stale generated files
- [x] Deprecated information — statements true when written and false now, in live prose
- [x] Anti-patterns and inefficiency — duplication, dead code, reports that cannot fail

**What was run, and what it said**

```
python tools/tasks/task.py check --closing   OK - 41 tasks, 614 document pointer(s), 0 broken
python tools/deck/check.py examples/reference-deck.html   0 failure(s); 79 checked, 0 SILENT
python tools/deck/ruleset.py                 160 rules, 111 owned (66 auto, 45 render)
python tools/plugin/check_scaffold.py        OK - 10 of 10 fixtures behaved as specified
python tools/deck/contract.py <deck>         0 failure(s)
python tools/deck/audit.py <deck>            0 mechanical failure(s)
python tools/deck/chrome_row.py              12 tick(s) drawn, dense mode off
python -m compileall tools                   all compile; no non-stdlib import (L-07 holds)
```

**Every gate in this repository is green.** All twenty-one findings below sit in the space those
gates do not reach, which is the result worth stating first: the tooling is sound and the *record
around it* has drifted. Two findings (F-2, F-3) are about a gate reporting more coverage than it
has, which is the one class that green runs actively hide.

**Out of scope**
- Fixing anything. This task raises and ranks; children fix.
- The quality of any deck, specification or research conclusion. This audit checks whether the
  repository agrees with itself and with its own instruments, not whether it is right.
- `.kb/` and `.assets-cache/`, which `.gitignore` excludes by design.

## 2. Findings

**Severity** — High: a stated claim is false in a way a reader would act on, or a rule the ruleset
calls a gate has no gatekeeper. Med: a contradiction or a gap that costs a later session time.
Low: an inaccuracy with no consequence beyond tidiness.

**Effort** — S: under an hour, mechanical. M: one session, needs a decision. L: more than one session.

| # | Dimension | Finding | Severity | Effort | Child task | Status |
| :-- | :--- | :--- | :---: | :---: | :--- | :--- |
| F-1 | Factual accuracy | **The seeded-defect deck is four reference-deck revisions stale** and its "held constant" claim is false. Regenerating it produces a 601-insertion diff, and the stale copy fails **two rules its own ledger does not claim** — DS-092 and DS-113. | High | S | [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) | **resolved** |
| F-2 | Completeness | **The gate's coverage account does not add up: 79 + 4 + 29 = 112 against 111 owned rules.** DS-072 is reported as `checked` *and* as excused by the ruleset. The self-test that would catch it is dead code. Every published figure inherits the error. | High | S | [T-043](T-043-make-the-gates-coverage-account-provable.md) | **resolved** |
| F-3 | Completeness | **25 `hard` rules are declared gates and nothing gates them**, and 11 of the 25 are named nowhere in `EVALUATION.md` at all — including four of the nine deliverable-contract rules. | High | M | [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) | **resolved** |
| F-4 | Deprecated info | **`examples/README.md` is stale in six places** — the deck size, the navigator, the chrome count, `audit.py`'s check count, the mechanical-catch table, and it never names `check.py`. It is the first file a visitor reads. | High | S | [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) | **resolved** |
| F-5 | Link hygiene | **1141 `§n` references, none validated, and the dead ones are not confined to the `§11` case T-037 swept.** `DESIGN-SYSTEM.md §9.1`–`§9.5` and `EVALUATION.md §0` are cited from live prose and do not exist. | Med | M | [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) | **resolved** |
| F-6 | Internal consistency | **`X-nn` is two ID namespaces**, and `tools/deck/check.py:303` already mis-cites across them. | Med | S | [T-047](T-047-give-the-rationale-conflicts-their-own-id-namespace.md) | **resolved** |
| F-7 | Standard compliance | **All eight open tasks declare `deliverables: []`**, so `task.py deliverables` reports *"0 not on disk yet"* — a complete-looking report that can only ever measure closed work (**L-05**). | Med | S | [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) | **resolved** |
| F-8 | Internal consistency | **Session memory contradicts itself and carries research this project retired.** Two memories say *ask the owner*; the newest says *decide it yourself*. One still lists `file://` fears R6 measured away. | Med | S | [T-049](T-049-reconcile-the-session-memory-with-the-research.md) | **resolved** |
| F-9 | Deprecated info | **`DESIGN-SYSTEM.md` §9 still says no deck here satisfies the deliverable contract.** T-028 met it 2026-08-07 and `BRIEF.md` records the publishing gate as clear. | Med | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-10 | Deprecated info | **`CLAUDE.md`'s status line names an outstanding WP1 measurement that does not exist**, and repeats F-2's arithmetic. | Med | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-11 | Factual accuracy | **The seeded deck's ledger is not the list of rules it breaks.** Freshly generated it fails DS-141 and DS-075, neither of which the ten-row ledger claims. | Med | S | [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) | **resolved** |
| F-12 | Completeness | **No `README.md` at the repository root**, for a repository stated to be published. T-008 owns it and is blocked by two modes the README does not depend on. | Med | M | [T-050](T-050-write-the-repository-readme.md) | **resolved** |
| F-13 | Internal consistency | **Nothing derives the rule counts the documents state.** `EVALUATION.md` §1 records them going stale twice and asks for re-derivation; `ruleset.py` computes them and no check compares the two. | Low | S | [T-043](T-043-make-the-gates-coverage-account-provable.md) | **resolved** |
| F-14 | Factual accuracy | **`BRIEF.md`'s `Reach` summary reads *"`—` (49, every `judge` rule)"***. 49 is 43 `judge` rules plus the 6 whose `Check` is `—`. | Low | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-15 | Link hygiene | **`DESIGN-RATIONALE.md`'s Sources line reads `R1`–`R6`.** R7 exists and the document depends on it. | Low | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-16 | Internal consistency | **Two rule totals in circulation** — `BRIEF.md` says 160, `EVALUATION.md` says 161 counting DS-000. Both correct; neither says why they differ. | Low | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-17 | Deprecated info | **`.handoff/config.md` describes `reference/` as a working prior-art codebase.** It holds one 1.2 KB prompt. | Low | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-18 | Standard compliance | **`check --closing`'s leftover-working-file check is a silent no-op in a fresh clone**, because git carries no empty directory (**L-05**). | Low | S | [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) | **resolved** |
| F-19 | Factual accuracy | **DS-063's two-resolution figures appear as 40/84 and as 116/336 in different documents** and neither says the first is a four-slide sample. | Low | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-20 | Standard compliance | **`DESIGN-RATIONALE.md` numbers §5 → §5.5 → §5.6 → §5.7 → §6**, with no §5.1–§5.4. | Low | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |
| F-21 | Link hygiene | **T-025's filename slug says "twelve"**; its title, its own body and `DESIGN-RATIONALE.md` say thirteen. | Low | S | [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | **resolved** |

### The findings that need their evidence

**F-1 — the seeded-defect deck is stale, and it is the only evidence the rubric works.**
`examples/reference-deck-seeded-defects.html` was last committed at `0265e57` (T-028, 2026-08-07).
`examples/reference-deck.html` has moved four commits since: T-032 added the print mode, T-034 the
contents page, T-035 replaced the ribbon with the ruler, T-040 fixed three defects the new gate
found. The fixture still contains a `.ribbon` and contains no `ruler`.

`examples/README.md` states the fixture's purpose exactly: *"It **derives** from the reference deck,
so everything except the seeded defect is held constant and the rubric's response is attributable to
the defect rather than to two decks differing in a hundred ways."* That is now false — running
`python tools/examples/seed_defects.py` rewrites 601 lines. Measured consequence, both decks through
`check.py`:

```
stale fixture   6 failures   DS-141 DS-035 DS-142 DS-075 DS-092 DS-113
fresh fixture   4 failures   DS-141 DS-035 DS-142 DS-075
```

DS-092 and DS-113 are drift, not seeds. The fix is one command; the reason it is High is that the
"one seeded defect per dimension, scored 0 or 1" result in `BRIEF.md`'s definition of done rests on
this file, and a fixture that differs from its parent in a hundred ways is the exact confound the
design guards against. **A regeneration step belongs wherever the reference deck is edited**, or
this recurs — the file was already regenerated once inside T-028 and has gone stale again since.

**F-2 — the coverage account claims more coverage than it has, and the assertion that would catch
it was written and disabled.** `tools/deck/check.py`'s `account()` docstring says *"Every owned rule
lands in exactly one bucket."* It does not:

```
owned 111  checked 79  byRuleset 4  deferred 29  silent 0
sum of buckets 112
checked & byRuleset -> ['DS-072']
```

DS-072 carries `Reach: off-gate` in the ruleset — *"headless has no user gesture to enter fullscreen
with… a person pressing F11 is the only real demonstration"* — and `contract.py` emits a `pass` for
it anyway. The verdict's own text is honest (*"tested against a double, not a real fullscreen"*), so
this is a bookkeeping defect rather than a false measurement, but it means **the gate reports a pass
on a rule the ruleset says it cannot reach**, and the headline is wrong by one in both directions:
79 checked against 33 excused does not partition 111.

`check.py:251` is the assertion that would have caught it:

```python
if len(a["silent"]) != len(own) - 3 - len(...) - len(...):
    pass          # the arithmetic is asserted below in the form that matters
```

The comment is not true — no later assertion checks that the buckets sum to `owned`. And
`stale = deferred & (cited | by_ruleset)` deliberately hunts excusals that outlived their rule, but
never looks at `cited & by_ruleset`, which is the pair that actually occurs. **The remedy is three
lines**: assert the partition, decide whether an `off-gate` rule may also be `checked` (recommend:
no — it is excused, and the verdict becomes a note), and let the self-test fail on the overlap.

Downstream, the same figure is stated in `CLAUDE.md`, `docs/BRIEF.md`, `docs/EVALUATION.md` §2,
`skills/htmldeck/references/pipeline.md` and four task files, always as *"79 of 111 … the other 32"*.

**F-3 — 25 `hard` rules are gates with no gatekeeper.** `EVALUATION.md` §1 is unambiguous: `hard`
rules are gates, the result is *"pass / fail, per rule ID"*, and the gate covers **114 `hard`**
rules. The pipeline in §2 assigns stage 1 to the 66 `auto` rules and stage 2 to the 45 `render`
rules. Derived from the ruleset:

```
hard = 114   of which  auto|render 85   judge 25   Check '—' 4 (they bind the checker, not the deck)
```

So **25 `hard` rules are `judge`**, and nothing in the pipeline produces a pass/fail for any of them.
Stages 3 and 4 produce 0–4 dimension *scores*, and §1 says in the same breath that `hard` rules are
**never scored** — so those 25 are simultaneously declared gates and excluded from the only
machinery that touches them.

Fourteen are at least reachable through a dimension's rule list. **Eleven appear nowhere in
`EVALUATION.md`:**

```
DS-021  the accent carries meaning wherever it appears
DS-093  never justify a statement with sentences
DS-097  the reader is bright and new to the field
DS-099  respectful, positive, professional
DS-107  the word-list check is necessary and not sufficient, and must say so
DS-112  never hand-draw icons
DS-137  two simultaneous interactions need a defined precedence rule
DS-201  every slide delivers exactly one thing
DS-204  never bury the deliverable in a list, a paragraph or a table cell
DS-207  the deliverable is stated factually and directly
DS-208  no native-speaker idiom
```

DS-136 is a twelfth in substance — it appears only in a §6.3 aside about regression sweeps, never as
a gate or a dimension.

**This is L-41's shape one layer up.** L-41 says a check with no rule is as wrong as a rule with no
check; T-005 closed the mechanical half by making a silent rule a red run. The judgement half has no
equivalent: a `hard` `judge` rule can be added and nothing anywhere notices it is unowned. Four of
the eleven are §3.4's deliverable contract — the section `DESIGN-RATIONALE.md` §3 records as *the
one the owner cared about most*, and the reason T-028 and the publishing gate exist. **Deciding what
owns them is the work; it is not obviously more rows in the rubric** — the alternative is a
`hard`-judge checklist the fresh-context pass answers pass/fail, separate from the 0–4 scoring, which
is what §1's own wording already implies.

**F-4 — `examples/README.md`, six stale claims, re-measured:**

| Claim in the README | Measured now |
| :--- | :--- |
| *"183 KB in one file"* | **219 083 bytes — 214 KB** |
| *"The seven stage names in the ribbon are buttons"*, and *"the ribbon says which stage"* | The ribbon was **replaced by the ruler** by T-035. The deck contains no `.ribbon`. |
| *"Chrome — 11 labelled or interactive items, 52 design units tall"* | **5 items, 52 du** — DS-217 now counts a scale as one item |
| *"`audit.py` … 50 checks against `DS-nnn` rules"* | **82 rows** |
| *"What the mechanical gate caught"*: S3, D2, D3 marked **yes** | Not re-derived since the gate was rebuilt. `check.py` on a fresh fixture fails **DS-141, DS-035, DS-142, DS-075** — none of which is S3, D2 or D3. |
| *"Reproducing the measurements"* lists six commands | **`check.py` is not among them**, though it is the gate everything else now describes |

The same 183 KB figure is in `docs/BRIEF.md`'s definition of done and twice in T-008's log.

**F-5 — dead section pointers, and no instrument that can see one.** `task.py check` validates
markdown links and repo-relative paths and reports *"614 document pointer(s) checked, 0 broken"*.
It does not resolve `§n`, and the repository contains **1141 of them**. This is the mechanism
L-39 was written for, and T-037 swept only the `§11` instance:

- `docs/BRIEF.md:243` cites `DESIGN-SYSTEM.md §9.4` for the semantic-heading rule. §9 is *"What is
  not covered"* and has no subsections; the rule is DS-090 in §3.3.
- `docs/BRIEF.md:324` cites `DESIGN-SYSTEM.md §9.2`. The reasoning is in `DESIGN-RATIONALE.md` §4.
- `§9.1`, `§9.3`, `§9.5` are cited the same way from T-002, T-007, T-014 and T-016. All five are
  T-014's old re-scoping section, which no commit of `DESIGN-SYSTEM.md` has ever contained — the
  same failure as `§11`, in a family nobody swept.
- **`EVALUATION.md` §0 is cited five times** — `BRIEF.md:304`, `EVALUATION.md:369`, T-023, T-024,
  T-026 — and `EVALUATION.md` has no §0. Its unnumbered preamble is what everyone means.
- `R3 §5.2`, `§5.3`, `§9.2` from T-016:131 resolve to nothing.

**Two conventions are colliding and that is worth settling once**: `R7 §5.3` means *item 3 of
section 5*, and `DESIGN-SYSTEM §0.8` means *item 8 of section 0* — both legible, both
indistinguishable from a subsection reference to a checker and to a reader. The remedy is a rule
plus a check: `task.py check` resolves `<named doc> §n`, and item references get a different form.

**F-6 — `X-nn` names two different things.** `DESIGN-SYSTEM.md` §6 defines twelve anti-patterns
`X-01`–`X-12`. `DESIGN-RATIONALE.md` §2 uses `X-1`–`X-11` for the conflicts found by reading the
sources against each other. They are cited in the same sentences. It has already cost one
mis-citation, in the gate's own closing paragraph:

```
tools/deck/check.py:303
"…so a clean DS-106 is never 'reads as human-written' (DS-107, X-10)."
```

The intended reference is the *conflict* X-10 (*a word-list check vs "text can pass all five and
still sound like AI"*). `X-10` in the ruleset is **the dual-axis chart**. Recommend renaming the
rationale's conflicts to `C-nn`; they are cited from one document and the anti-patterns are cited
from five.

**F-8 — the memory directory, four entries:**

| Memory | Problem |
| :--- | :--- |
| `research-before-building.md`, `research-may-reshape-the-project.md` | Both close on *ask the owner rather than guess*. `decide-detailed-questions-yourself.md`, written 2026-08-09 from the owner's own words, says the opposite and is the newer instruction. Neither older memory links to it, so a fresh session can read either half first. |
| `portability-not-minimalism.md` | Still lists *"ES modules, `fetch`, XHR, some worker and WebGL texture paths fail"* as **the gotcha to design around**, and points at T-017 as unfinished. R6 measured 95 rows and found the boundary is fetch-like versus element-like access, that `file://` is a secure context, and that **no refused capability costs the deck anything**. `DESIGN-RATIONALE.md` §6 says in terms: *"Do not design around fears this research retired."* |
| `research-may-reshape-the-project.md` | *"Keep WP2 and WP3 tasks lightly specified until T-014 lands"* and *"expect T-014 to end with a re-scoping proposal"*. T-014 closed 2026-08-06; all ten WP1 tasks are `done`. |
| `one-parametric-theme.md` | *"this sits in tension with the brief's rule 3 ('decks must not look like each other')"*. `CLAUDE.md` rule 3 is now *Use whatever renders best*; the parametric-theme rule is rule 4, so the tension it records was resolved by the rewrite it predates. |

**F-11 — the seeded fixture breaks more rules than its ledger names.** Freshly generated, it fails
DS-141 (a duration over 500 ms outside the vocabulary) and DS-075 (reflow `scrollWidth` 851 at
320 CSS px). The ledger in `examples/README.md` lists ten defects, one per dimension, and neither of
these is among them. DS-141 is plausibly collateral from the S6 seed; DS-075 has no obvious owner.
A fixture whose real failure set is larger than its documented one is the same confound as F-1 in
miniature: **either the ledger gains the rows, or the seeds stop producing them.**

## 3. Resolution

The umbrella closes only when every finding is resolved via a `done` child task, or explicitly
accepted with a recorded reason below.

**All twenty-one findings were approved by the owner on 2026-08-09, and eight children carry them.**
Grouped by the file each edits rather than by theme, so two children never contend for one document:

| Child | Carries | Effort |
| :--- | :--- | :---: |
| [T-043](T-043-make-the-gates-coverage-account-provable.md) — the gate's account | F-2, F-13 | S |
| [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) — `examples/` | F-1, F-4, F-11 | S |
| [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) — the stale-prose sweep | F-9, F-10, F-14, F-15, F-16, F-17, F-19, F-20, F-21 | S |
| [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) — `task.py`'s three blind spots | F-5, F-7, F-18 | M |
| [T-047](T-047-give-the-rationale-conflicts-their-own-id-namespace.md) — the `X-nn` collision | F-6 | S |
| [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) — the 25 ungated `hard` rules | F-3 | M |
| [T-049](T-049-reconcile-the-session-memory-with-the-research.md) — session memory | F-8 | S |
| [T-050](T-050-write-the-repository-readme.md) — the repository README | F-12 | M |

**One `blocked_by` edge, and only one.** T-045 waits on T-043, because five documents quote the
coverage figure T-043 corrects and rewriting them first would write the wrong number twice.
Everything else is `related`: T-047 and T-045 both edit `DESIGN-RATIONALE.md` and must not run in
the same session, which is a sequencing note rather than a gate (**TASK-WORKFLOW.md** §4 —
*`blocked_by` is expensive*).

**The three open questions this audit raised are answered inside the children that inherit them** —
F-3's owner in [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) §1, the `§n.m`
resolution rule and what an open task owes the deliverables report in
[T-046](T-046-extend-task-py-to-what-it-cannot-see.md) §1, and the README's home in
[T-050](T-050-write-the-repository-readme.md) §1. Each is decided from the reason the rule it
concerns already gives, and each names the alternative it rejects.

**Recommended order, and why**

1. **F-2, F-6, F-13** — the tooling's own honesty, and all three are small. F-2 first: every other
   document quotes its number, so fixing the documents before the arithmetic writes the wrong figure
   twice.
2. **F-1, F-11** — one command plus a ledger reconciliation, and they restore the only evidence the
   rubric has.
3. **F-4, F-9, F-10, F-14, F-15, F-16, F-17, F-19, F-21** — one sweep of stale prose, after F-2 and
   F-1 have settled the numbers it should state.
4. **F-5, F-7, F-18** — the three gaps in `task.py`'s reach, best done together since they touch one
   file.
5. **F-8** — memory, independent of everything above.
6. **F-3** — last, because it needs a decision rather than an edit, and it is the one finding that
   may change `EVALUATION.md`'s structure.
7. **F-12** — [T-050](T-050-write-the-repository-readme.md), best written after T-044 re-measures the
   deck so the repository's two front doors state the same numbers.

**Accepted without action**
- <F-n — reason — date>

**Deviation from the template.** An **Effort** column was added to the findings table, because the
audit was asked to rank by effort as well as severity and a severity alone does not say which
findings are worth batching.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | (no change) | **All twenty-one findings approved by the owner; eight children raised, [T-043](T-043-make-the-gates-coverage-account-provable.md) to [T-050](T-050-write-the-repository-readme.md).** Grouped by the file each edits rather than by theme, because the two largest risks in a fix run of this shape are two tasks contending for one document and a figure corrected in one copy of five. One `blocked_by` edge only — T-045 on T-043 — and a sequencing note where T-045 and T-047 both touch `DESIGN-RATIONALE.md`. **The three open questions are answered rather than handed back**, each from the reason the rule it concerns already gives: the 25 `hard` `judge` rules keep gate status and gain a pass/fail checklist inside the existing fresh-context pass, because §1's ban on scoring them is about **dilution by arithmetic** and not about leaving them unobserved — the alternative demotes the deliverable contract from defect to a point off a score. A `§n.m` reference resolves when `n.m` is a heading **or** `n` is a heading and `m` is an ordinal printed in a numbered list under it — which passes `R7 §5.3` and `DESIGN-SYSTEM §0.8` and fails `DESIGN-SYSTEM §9.4` and `EVALUATION §0`, exactly the live/dead split, so it needs no exception list. And the README is its own task, because T-008's blockers are two *modes* and a README depends on neither. |
| 2026-08-09 | → proposed | **Created. Twenty-one findings, and every gate in the repository is green** — which is the frame the list should be read in: `task.py check --closing`, `check.py`, `ruleset.py`, `check_scaffold.py`, `contract.py` and `audit.py` all pass, and nothing here was found by any of them. **Three findings are about a green run overstating itself.** F-2: the coverage account sums to 112 against 111 owned rules because DS-072 is both `checked` and excused by the ruleset, and the assertion that would have caught it is `if …: pass` with a comment claiming the arithmetic is asserted elsewhere, which it is not. F-3: 25 `hard` rules are declared gates and are `judge`, so nothing emits a verdict for them, and 11 of the 25 — including four of the nine deliverable-contract rules — are named nowhere in `EVALUATION.md`; that is **L-41** at the judgement layer, where T-005's *silent rule fails the run* device has no counterpart. F-1: the seeded-defect deck is four reference-deck revisions stale, so the fixture the rubric was validated against differs from its parent in 601 lines and fails two rules its ledger does not claim — the exact confound `examples/README.md` says it exists to remove. **F-5 is L-39 unswept:** T-037 chased the `§11` references and the `§9.1`–`§9.5` family survived, two of them in `BRIEF.md`'s live prose, and `EVALUATION.md §0` is cited five times and does not exist. 1141 section references, none validated by anything. No fix applied — the working tree is unchanged, and the fixture regenerated during measurement was reverted. |
