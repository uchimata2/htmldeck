# Context audit — htmldeck

**This is part 2 of [T-130](../tasks/T-130-audit-the-context-economy-of-an-agent-driven-repository.md).**
Part 1 is [`research/R8-context-economy-for-coding-agents.md`](research/R8-context-economy-for-coding-agents.md)
— the method, the rubric, the technique catalogue, and every finding that applies to any repository.
This document applies that method here and ranks what it found. **It implements nothing.** The owner
reviews the ranking, and the top of it becomes child tasks then.

**Two subjects, reported separately** (§2 and §3): this repository's own development workflow, and
`skills/htmldeck/` as loaded into an adopting project's context.

## 0. How this was measured

| | |
| :--- | :--- |
| **Measured on** | 2026-08-13, on the working tree at `4c18c87` |
| **Representative unit of work** | **One task carried from `proposed` to `done`** — the only unit this project has. Its mandatory read path is the same for every task, so the figure generalises instead of describing one file |
| **Instrument** | Throwaway scripts outside the repository. Sizes came off the filesystem; gate output was captured to a file and the file measured. **Nothing was read to find out how big it is** |
| **Token figures** | Estimated as **bytes ÷ 4** and labelled `~tokens` everywhere. No tokeniser ships here and adding one would be a dependency (**L-07**). The estimate never separates two findings that a byte count does not already separate |
| **Line figures** | `(Get-Content file).Count`, not `Measure-Object -Line`, which omits blank lines |

**Inventory figures below are measurements. Every gain is a band** — `XL`/`L`/`M`/`S` as defined in
`R8-context-economy-for-coding-agents.md` §5, read against the surface it names.

---

## 1. The answer in one paragraph

A session here pays about **6,900 estimated tokens before anything happens** and about **20,000 more
if it reads the specification and the lessons file, which the working rules tell it to do**. The
single largest avoidable item is not a document at all: the board is read whole, at 33,676 bytes,
because the tracker's own query commands do not resolve in an agent shell — they answer the same
question in **1,901 bytes**. The three cheapest fixes are all `xs` and none of them deletes anything.
The three largest are all `F1` splits of documents that are 52%, 61% and 81% appendix by weight.

*Two of those three landed on 2026-08-14 — `CE-05` and `CE-06`, as
[T-145](../tasks/T-145-move-brief-mds-release-phases-to-its-own-document.md) and
[T-146](../tasks/T-146-one-file-per-lesson-with-a-generated-index.md) — and **neither saved what its
band promised**. The first moved 92,894 bytes to a document opened on demand; the second moved none
at all and bought a gate instead. `CE-09` is the third and is still open. A share-of-file figure
says where the weight is, not what removing it is worth.*

---

## 2. Subject 1 — this repository's development workflow

### 2.1 Surface A — the load path

What enters context unasked, per session, before any work.

| Item | Bytes | ~tokens | Tier |
| :--- | ---: | ---: | :--- |
| Global working preferences (`~/.claude/CLAUDE.md`) | 5,869 | 1,467 | 1 |
| [`CLAUDE.md`](../CLAUDE.md) — this project | 15,630 | 3,908 | 1 |
| The memory index (35 memories, one line each) | 6,134 | 1,534 | 1 |
| **Tier 1 total** | **27,633** | **~6,908** | |
| The skill-description block — 55 skills on this machine | 20,941 | 5,235 | 1, harness-supplied |
| **Tier 1 including the skill block** | **48,574** | **~12,143** | |
| A recalled memory, mean of 34 | 1,889 | 472 | on recall |
| A handoff, mean of 47 archived | 4,932 | 1,233 | once, at resume |
| [`.taskmd/config.md`](../.taskmd/config.md) | 14,087 | 3,522 | 2 |

**In lines**, for comparison with the tier-1 bound the owner's other project sets: global 92 +
project 207 + memory index 39 = **338 lines**. That project's tier 1 is one file of 144 lines, bounded
by a relation rather than a constant — `R8-context-economy-for-coding-agents.md` §2.1.

*Re-measured 2026-08-13 at T-134's close, which moved the only figure here this repository owns:
[`../CLAUDE.md`](../CLAUDE.md) is **18,642 bytes / 249 lines** — 15,630 at the audit and 15,952 before
T-134 wrote the tier section, so it had drifted 322 bytes in a day, which is why §6.2 opens with
*re-measure*. Tier 1 is **30,645 bytes / ~7,661 tokens / 380 lines**, holding the other two files at
their audit figures. The model, the membership rule and the bound now live in `../CLAUDE.md` itself,
which is also over that bound by 4,555 bytes and says so.*

**Tool schemas are already deferred** — roughly 100 tool names are listed without their schemas, and
a schema loads on request. That is the single largest saving available on this surface and the
harness already takes it. No finding.

### 2.2 Surface B — the read path for one unit of work

| Document | Bytes | ~tokens | Needed for one task? |
| :--- | ---: | ---: | :--- |
| ~~[`docs/LESSONS.md`](LESSONS.md)~~ | ~~152,444~~ | ~~38,111~~ | ~~One entry of 81, cited as `L-nn`~~ **split 2026-08-14 by [T-146](../tasks/T-146-one-file-per-lesson-with-a-generated-index.md): the entry is its own file and this path is a 12,258-byte index** |
| [`docs/BRIEF.md`](BRIEF.md) | 108,163 | 27,041 | "Read the brief first" — 61% of it is one appendix |
| [`docs/DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) | 75,295 | 18,824 | Deck work only |
| [`docs/DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) | 62,463 | 15,616 | Rarely |
| [`tasks/README.md`](../tasks/README.md) | 33,676 | 8,419 | The board — 134 rows |
| [`docs/COMPONENT-CONTRACT.md`](COMPONENT-CONTRACT.md) | 26,947 | 6,737 | Deck work only |
| [`docs/EVALUATION.md`](EVALUATION.md) | 26,784 | 6,696 | Rarely |
| [`docs/PUBLISHING.md`](PUBLISHING.md) | 23,173 | 5,793 | Releases |
| [`docs/THEME-CONTRACT.md`](THEME-CONTRACT.md) | 21,663 | 5,416 | Deck work only |
| ~~[`tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md)~~ | ~~21,374~~ | ~~5,344~~ | ~~Every task — 52% of it is §6~~ **§6 moved out 2026-08-14 by [T-147](../tasks/T-147-one-workflow-file-per-lifecycle-phase.md); it read 23,210 with §6 at 55.3% that day, and the file is now 11,407** |
| The task file itself, median of 130 | 12,528 | 3,132 | Yes |
| **The mandatory set** (lessons + brief + board + workflow + the task) | **328,185** | **~82,046** | |

**The mandatory set is 41% of a 200k window before the work starts.** That is the growth the task was
raised about, and it is measured rather than felt.

**Where the weight sits inside the three biggest.**

| Document | Largest section | Bytes | Share |
| :--- | :--- | ---: | ---: |
| ~~`docs/BRIEF.md`~~ | ~~*Release phases* — 112 rows, 68 struck through~~ **moved out 2026-08-14 by [T-145](../tasks/T-145-move-brief-mds-release-phases-to-its-own-document.md); it read 92,894 / 69% over 134 rows on the day it went, and `BRIEF.md` is now 42,485 bytes** | ~~66,461~~ | ~~**61%**~~ |
| ~~`docs/LESSONS.md`~~ | ~~81 entries, mean 1,873 bytes~~ **split out 2026-08-14 by T-146; it read 89 entries, mean 1,859, 167,043 bytes on the day it went** | ~~151,751~~ | ~~**>99%**~~ |
| ~~`tasks/TASK-WORKFLOW.md`~~ | ~~§6 *The tooling*~~ **split out 2026-08-14 by T-147; it read 12,836 / 55.3% on the day it went** | ~~11,026~~ | ~~**52%**~~ |
| `CLAUDE.md` | *What this is* — release chronology | 6,980 | **45%** |

### 2.3 Surface C — tool output on a green run

| Command | Bytes | ~tokens | Lines | Seconds |
| :--- | ---: | ---: | ---: | ---: |
| `python tools/deck/check.py <deck>` | **17,391** | **4,348** | 169 | 16.7 |
| `python tools/check_all.py` — the whole release gate | 8,233 | 2,058 | 130 | **154** |
| `python tools/tasks/lint.py` | 1,073 | 268 | 18 | 1.4 |
| `taskmd list --open` | 1,901 | 475 | 17 | 0.1 |
| `taskmd context T-130` | 790 | 198 | 15 | 0.1 |
| `taskmd list --open --limit 1` | 123 | 31 | 1 | 0.1 |

**One gate on one deck prints more than the entire release gate over the whole repository.**
`check_all.py` suppresses its children's output unless `--verbose` is passed, which is the technique
already adopted, one altitude up, by the tool that needed it most.

### 2.4 Surface D — write volume

| | Count | Bytes | ~tokens |
| :--- | ---: | ---: | ---: |
| Task files | 130 | 1,997,073 | 499,268 |
| — open | 17 | 151,296 | 37,824 |
| — closed | 113 | 1,845,777 | 461,444 |
| Median task file | | 12,528 | 3,132 |
| Largest task file | | 53,488 | 13,372 |
| All markdown in the tree | 221 | 3,191,730 | 797,932 |
| `tools/**/*.py` | 36 | 921,624 | 230,406 |
| — of which docstrings | | 277,092 | **30%** |
| `examples/*.html` | 3 | 810,746 | 202,686 |

**92% of the task record is closed tasks, and that costs nothing** — a closed file is read only when
its id is cited. Recorded as a negative result, because the number invites the opposite conclusion.

**One example deck is 200k+ estimated tokens of HTML.** Reading one whole would end a session's
runway on its own.

### 2.5 Surface E — workflow and tooling

- **The gate split is already right.** `lint.py` at 1.4 s is what a task edit owes; `check_all.py` at
  154 s is what a release owes. Nothing per-task runs the 154-second gate.
- **Delegation is not used, and the cheaper substitute is the house style.** This session's inventory
  ran as scripts rather than as reading or as sub-agents, which is F4 applied to the audit itself.
- **The handover is a real cost and mostly a correct one**: a mean archived handoff is 4,932 bytes,
  read once, and it replaces re-deriving the state. Its one measured failure is CE-08.

---

## 3. Subject 2 — the plugin as an adopter loads it

| Item | Bytes | ~tokens | When it loads |
| :--- | ---: | ---: | :--- |
| The skill description in front-matter | 472 | 118 | **Every session, for every adopter** |
| [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) | 5,206 | 1,302 | On activation |
| `references/build.md` | 12,144 | 3,036 | Build mode |
| `references/pipeline.md` | 10,809 | 2,702 | On demand |
| `references/critique.md` | 7,470 | 1,868 | Critique mode |
| `references/artifacts.md` | 5,984 | 1,496 | On demand |
| **Total if everything loaded** | **41,613** | **10,403** | Never all at once |
| `shell/` — what a build reaches for | 114,931 | 28,733 | During a build |

**This is already three-stage progressive disclosure and it measures well.** Discovery costs 472
bytes; activation costs 5,206; a build adds one 12 KB reference. An adopter who never builds a deck
pays 118 estimated tokens for having the plugin installed. **No finding against the skill's own
shape** — it is the best-tiered artifact in the repository, and it is the newest.

**One thing is unmeasured and is recorded as such**: how much of `shell/`'s 114,931 bytes a build
actually pulls into context. Closing it needs an instrumented build, which is deferred (§4, T19-class
work), not assumed.

---

## 4. Screening the technique catalogue

Every technique in `R8-context-economy-for-coding-agents.md` §7, screened against this project. **The
three verdicts partition the catalogue: 9 adopted, 5 rejected, 7 deferred, summing to 21.**

**And the partition is not a coverage claim.** It summed correctly at 19 while two techniques were
missing from the catalogue entirely — T20 and T21, both added 2026-08-13 after a reader asked whether
one specific tool had been checked. It had not. The gap is the research step's, not the screening's,
and [T-136](../tasks/T-136-re-run-the-external-research-with-a-recorded-search-record.md) re-runs it
with a search record. Rows T20 and T21 below are screened on what is known now and are provisional
until that task lands.

| # | Technique | Verdict | Why |
| :--- | :--- | :--- | :--- |
| T1 | Right-altitude system prompts | **adopted** | CE-01, CE-11 |
| T2 | Just-in-time retrieval | **adopted** | CE-05, CE-06, CE-09 |
| T3 | Progressive disclosure, three stages | **adopted** | Already in force in `skills/htmldeck/` (§3); extended to the docs by CE-05, CE-06 |
| T4 | Tool-set curation | **adopted** | CE-07 |
| T5 | Deferred tool schemas | **adopted** | Already in force, harness-side. No work |
| T6 | Tool-result clearing | **deferred** | Harness behaviour, not the repository's to set. Closed by a harness setting the owner controls |
| T7 | Compaction | **deferred** | Same. Closed by nothing this repository can change |
| T8 | Structured note-taking / external memory | **adopted** | Already in force: the task record and the handoff *are* this, and the four-store routing rule is stricter than the technique |
| T9 | Sub-agent delegation | **rejected** | Collides with the session rule that the Agent tool is not called unless the user asks, and F4's deterministic-script route is cheaper for the read-heavy work here — this audit's own inventory is the demonstration |
| T10 | Scoped requests over broad retrieval | **adopted** | CE-13 |
| T11 | Prompt caching | **rejected** | Collides with what a repository controls: file contents, not prompt assembly order |
| T12 | Diffs, not whole files | **adopted** | Already in force — edits are targeted by default |
| T13 | Module summaries | **deferred** | Would suit `tools/` (921 KB) and `shell/` (115 KB). Closed by deciding where the summary lives and what keeps it true; an untrue summary lies cheaply, which is worse than the cost it saves |
| T14 | Minification for agent input | **rejected** | Collides with F4's own limit — *simplify wherever no human reads them*. Every artifact here is read by a human too: the decks are deliverables and the record is the project's memory |
| T15 | Adaptive context pruning | **deferred** | Harness-side. Closed by the harness exposing it |
| T16 | Model routing | **rejected** | Collides with the audit's axis: it moves cost, not runway |
| T17 | Planner → implementer → reviewer | **adopted** | Already in force as `specify → plan → implement → review` |
| T18 | Fresh context per checklist item | **deferred** | Would suit the variant and seeded-defect suites. Closed by deciding whether per-item isolation is worth losing cross-item learning |
| T19 | Evidence quoted forward | **deferred** | The strongest untaken idea here. Closed by measuring how much of a `review` phase's reading duplicates what `implement` already had — unmeasured, so no band is written |
| T20 | Generation restraint — a decision ladder | **deferred** | Two constraints pull opposite ways and neither settles it. **For the tooling** it may fit: standard-library-only is already a rung of that ladder (**L-07**). **For the decks it fights the brief** — rule 2 wants richness, interaction, animation and 3D, so a minimalism rule pointed at deck output is aimed at the wrong artifact. And its own instructions are a permanent load-path cost, which an audit ranking by load path has to count against it. Closed by deciding whether it can be scoped to `tools/` alone, and by measuring its own listing cost against the write volume it removes |
| T21 | Semantic index over the repository | **rejected** | Collides with two rules at once. **L-07** and the out-of-the-box constraint: this repository ships standard library only and must clone and run, so an index service or embedding library is a dependency it does not take. And the index would be a machine-local artifact that no clone receives — the same property that made `taskmd check` refuse a link to the git-ignored settings file. The corpus is also small enough that naming files works: the read path is a dozen documents, not a codebase |

---

## 5. The family walk

**All five families were walked. ~~Each yielded at least one finding~~ — four did — and each also
produced a negative worth recording.** *`F3`'s single finding was withdrawn on 2026-08-14 when it was
re-measured ([T-150](../tasks/T-150-relocate-the-research-prose-in-the-two-docstring-outliers.md),
**L-92**), so the family that is hardest to draw a line in produced a rejection and nothing else. That
is a result about F3, not a gap in the walk.*

| Family | Findings | The negative result |
| :--- | :--- | :--- |
| **F1** — what loads, and when | CE-01, CE-05, CE-06, CE-09, CE-11 | `skills/htmldeck/` needs nothing: it is already three-stage (§3) |
| **F2** — redundancy and contradiction | CE-04, CE-08, CE-10 | **No contradicting pair was found.** The record's cross-references are unusually consistent, which three reference checkers plausibly explain |
| **F3** — prose not doing work | ~~CE-12 (two outliers only)~~ **none** | **The general sweep is rejected** (§5.1), and on 2026-08-14 the one finding that survived it was withdrawn: **its outliers were a measurement error**, not prose (§6.1). F3 yielded nothing here |
| **F4** — model work that should be deterministic | CE-02, CE-13 | Tool schemas and the gate chain are already deterministic; `lint.py` already solves the locating problem CE-02 reuses |
| **F5** — tool and workflow economics | CE-03, CE-07 | `check_all.py` already suppresses child output by default, and the per-task/per-release gate split is already correct |

### 5.1 The F3 rejection, recorded

**Rejected: a sweep over the record's rationale prose — tool docstrings at ~~30%~~ **16.3%** of
`tools/**/*.py`, and task log rows.** It cannot name what the prose would stop deciding. Every sample
checked carried a reason a future reader needs: why a rule exists, what it cost to learn, what was
rejected and why, what would close an excusal. That is the test in
`R8-context-economy-for-coding-agents.md` §4.1, and this sweep fails it.

~~**What survives is CE-12**, two files whose docstring share is so far outside the distribution that
the question is worth asking about them specifically — and even there the change is relocation, not
deletion.~~

**Nothing survives it. The carve-out was a measurement error and was withdrawn on 2026-08-14**
([T-150](../tasks/T-150-relocate-the-research-prose-in-the-two-docstring-outliers.md)). The corrected
figure above is the same correction: **30% counted every triple-quoted string token**, and the two
"outliers" hold their payloads that way. The rejection is unaffected and is stronger — the sweep it
declined is half the size it was declined at, and it now has no exception. **L-92.**

---

## 6. The ranked findings

Gain per unit of effort, risk as a veto. **`any`-marked findings are stated in full in
[`research/R8-context-economy-for-coding-agents.md`](research/R8-context-economy-for-coding-agents.md)
§8 and are not restated here** — one numbering space, one statement per finding.

**Before working one of these, read §6.2.** It is what a session implementing a finding owes beyond
the finding itself, and four closures showed that none of it is obvious from the row.

| Rank | ID | Surface / Family | What | Gain | Effort | Risk | Stated in |
| ---: | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| ~~1~~ | **CE-02** | B / F4 | Expose the tracker's `list` and `context` so the board is not read whole — **done, and the band held while the multiple was understated** | `L` | `xs` | none | R8 §8 |
| ~~2~~ | **CE-03** | C / F5 | A quiet mode for the deck gate's green run — **done; 345 bytes against 17,581, and the default proved unchanged** | `L` | `xs` | stated | R8 §8 |
| ~~3~~ | **CE-07** | A / F5 | Enable skills per project, not globally — **done, and the band was wrong** | ~~`L`~~ **`S`** | `xs` | stated | R8 §8 |
| ~~4~~ | **CE-13** | B / F4 | Write down that a deck is never read whole — **done, inside rule 6 rather than as a new rule; the numbers are cited about 130 times** | *bimodal* | `xs` | none | §6.1 |
| 5 | **CE-01** | A / F1 | Split the release chronology out of `CLAUDE.md` | `L` | `s` | stated | R8 §8 |
| ~~6~~ | **CE-11** | A / F1 | Adopt the tier model and a relation-bound tier 1 — **done, and the file is over the bound the day it was set, so it is written as dated debt** | *enabler* | `s` | none | §6.1 |
| ~~7~~ | **CE-05** | B / F1 | Move `BRIEF.md`'s *Release phases* to its own document — **done; `BRIEF.md` 134,596 → 42,485, and the shape the row proposed was refused with a measurement** | `XL` | `m` | stated | R8 §8 |
| ~~8~~ | **CE-06** | B / F1 | One file per lesson, plus a generated index — **done, and the band was wrong: no bytes were saved.** What it bought was 983 citations a gate now resolves | ~~`XL`~~ **`S`, plus an unbanded gain the row never named** | `m`–`l` | stated | R8 §8 |
| ~~9~~ | **CE-09** | B / F1 | One workflow file per lifecycle phase — **done, and the shape was refused**: §6 was extracted whole and the rest left alone, because everything but §6 is 10,374 bytes together | `L` | `m` | stated | §6.1 |
| 10 | **CE-04** | A+B / F2 | One operative home per cumulative rule | `M` | `xs` each | stated | R8 §8 |
| 11 | **CE-08** | A / F2 | A measured figure gets a durable home | `S` | `xs` | none | R8 §8 |
| 12 | **CE-10** | A / F2 | Prune the memory index of spent entries | `S` | `xs` | stated | §6.1 |
| ~~13~~ | **CE-12** | B / F3 | ~~Two docstring outliers~~ — **withdrawn 2026-08-14: there are no docstring outliers.** The figures counted triple-quoted string tokens, and in those files the strings are the tools' payloads | ~~`M`~~ **none** | `s` | ~~stated~~ — the stated risk was never reached | §6.1 |

**CE-13's gain is bimodal, which is why it ranks above larger bands**: it saves nothing on most
sessions and saves a whole session's runway on the one that would otherwise open a deck.

### 6.1 Findings whose subject is this repository

#### CE-09 — The workflow document is half tooling history

| | |
| :--- | :--- |
| **Surface / Family** | B / F1 |
| **Finding** | [`tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) is 22,190 bytes and §6 *The tooling* is **11,842 of them, 53%** — most of it the history of which checker resolved what, which upstream release changed it, and why one advisory is expected forever. A session at `plan` needs §2, which is 1,291 bytes. *Measured at 21,374 / 11,026 / 52% when this was written; **T-131 added 816 bytes to §6 the same day**, which is the finding describing itself — the section grows because every tooling change lands in it* |
| **Change** | One file per lifecycle phase, following `R8-context-economy-for-coding-agents.md` §9, P2: preflight, do, do-not, close. **Section numbers must survive** — the document itself records that a dozen task records cite it at §2 through §6.2 and that renumbering silently falsifies all of them |
| **Gain** | `L` on the read path of every task |
| **Effort** | `m` |
| **Risk** | `§n` citations from a dozen task records, which `refcheck.py` resolves. A split that keeps the numbers keeps the citations; one that does not breaks twelve records at once, and the checker will say so |
| **Applies to** | `this project` |
| **Source** | local precedent — `R8-context-economy-for-coding-agents.md` §9, P2 |

#### CE-10 — The memory index carries entries that say they are spent

| | |
| :--- | :--- |
| **Surface / Family** | A / F2 |
| **Finding** | The memory index is 6,134 bytes over 39 lines and is tier 1. Several of its 35 entries mark themselves superseded in their own hook text — *"its WP1 scheduling advice is spent"*, *"Its ask-first half is superseded"* — so the index pays for them every session while telling the reader not to use them |
| **Change** | Prune what is spent, and move anything still true but project-shaped into the repository, where it is shared rather than private. This is the owner's action, not a repository change |
| **Gain** | `S` on the load path |
| **Effort** | `xs` |
| **Risk** | Deleting a memory that the repository does not in fact record. Mitigated by checking each against `docs/LESSONS.md` before removal |
| **Applies to** | `this project` |
| **Source** | this audit |

#### CE-11 — There is no tier model here, and the project that has one is the owner's

| | |
| :--- | :--- |
| **Surface / Family** | A / F1 |
| **Finding** | Nothing states what this project's always-loaded set is, what bounds it, or where the boundary between always-loaded and read-on-demand falls. Tier 1 measures **338 lines across three files**; the owner's other project settled this in its own audit and bounds tier 1 as a **relation** to the flat alternative it replaced, with no number written anywhere |
| **Change** | Adopt the tier model and the relation-bound: state the membership rule — *what the harness loads without being asked* — name the tiers, and bound tier 1 against something counted from the same tree. **It is an enabler**: CE-01 and CE-04 are the cuts it makes decidable, and it should land before them so the cuts are not chosen to fit a number nobody agreed |
| **Gain** | Not banded — it saves nothing by itself and decides what the others may cut |
| **Effort** | `s` |
| **Risk** | `none` |
| **Applies to** | `this project` |
| **Source** | local precedent — `R8-context-economy-for-coding-agents.md` §2.1 |

#### CE-12 — ~~Two files where docstrings are most of the file~~ — **withdrawn, the measurement was of the wrong unit**

**Withdrawn 2026-08-14 by
[T-150](../tasks/T-150-relocate-the-research-prose-in-the-two-docstring-outliers.md), which ran the
full lifecycle and cancelled on the premise.** The row is kept whole below, struck where it is wrong,
because a finding that reached five documents is worth being able to trace.

**Every figure in it counts triple-quoted `STRING` tokens, not docstrings.** Measured by AST role
over the same 38 files:

| File | This row says | **Docstrings by AST role** | Rank of 38 |
| :--- | ---: | ---: | :--- |
| `tools/portability/build_probes.py` | 85%, 52,408 B | **3.2%, 1,949 B** | **38th — the lowest in the tree** |
| `tools/deck/print_variants.py` | 58% | **15.3%, 2,780 B** | 26th |
| `tools/deck/audit.py` | 36%, 52,230 B | **11.6%, 16,465 B** | 30th |
| `tools/**/*.py` overall | 30% | **16.3%** | — |

The named files hold their payloads as triple-quoted constants — `PROBE_JS`, `PROBE_HTML`,
`PROBE_3D_HTML`, `PRINT_PROBE_HTML`, `PAGINATED`, `REFLOW`. **That text is what the tools write out,
so the change this row proposes would break them.** One true claim survives and is worth nothing:
`audit.py` does hold the largest single docstring block, at 11.6% of itself. **L-92** is the rule.

| | |
| :--- | :--- |
| **Surface / Family** | B / F3 |
| **Finding** | ~~Docstrings are 30% of `tools/**/*.py`, which is this project's deliberate style and is **not** a finding (§5.1). Two files sit far outside that: `tools/portability/build_probes.py` is **85%** docstring (52,408 of 61,484 bytes) and `tools/deck/print_variants.py` is **58%**. `tools/deck/audit.py` is 36% but is the largest file in the tree at 141,896 bytes, so its 52,230 bytes of docstring is the biggest single block~~ — the clause about §5.1 is right, the figure in it is not, and the outliers are not outliers |
| **Change** | ~~For those files only, ask what the prose decides. Where it is a research record rather than a rule for the next editor, **relocate it to `docs/research/`** and leave a pointer. Deletion is not the change~~ — there is no prose to relocate |
| **Gain** | ~~`M` on the read path when those files are edited, which is rare~~ **none** |
| **Effort** | ~~`s`~~ — nothing was built; the measurement that withdrew it was three throwaway scripts |
| **Risk** | ~~These are the files whose behaviour is least obvious, which is plausibly *why* they carry the most explanation. A relocation that makes a probe's reasoning unfindable costs more than it saves~~ — **this risk was never reached.** It presumes the explanation is there, and it is 1,949 bytes |
| **Applies to** | `this project` |
| **Source** | this audit |

#### CE-13 — Nothing says a deck is never read whole

| | |
| :--- | :--- |
| **Surface / Family** | B / F4 |
| **Finding** | The three example decks are **810,746 bytes, ~202,686 estimated tokens**. Rule 6 requires looking at a rendered deck, and the repository already ships tools that answer questions about one without loading it — `tools/deck/check.py`, `tools/deck/printgeom.py` and others under `tools/deck/`. **No document says the HTML must not be read into context**, and one accidental whole-file read ends a session |
| **Change** | One line in the working rules: a deck is queried by the tools or by targeted search, never opened whole; looking at it means rendering it |
| **Gain** | Nothing on most sessions; a whole session's runway on the one that would have opened a deck |
| **Effort** | `xs` |
| **Risk** | `none` |
| **Applies to** | `this project` |
| **Source** | this audit |

### 6.2 Working one of these — what to check, what to report, and where each thing goes

Written 2026-08-13 after `CE-02`, `CE-03`, `CE-13` and one raised defect were implemented in one
session. **None of the four cost what the row said it would, and all four produced something the row
did not predict** — so this is the part of an audit task that is not in the audit task.

**What to check, beyond the finding**

1. **Re-measure before you claim a saving, and again after.** Every figure in this document is dated
   and the subjects grow: the board was 33,676 bytes when `CE-02` was written and 36,813 five
   closures later. A ratio computed against a stale denominator is not a measurement.
2. **Measure the thing a session actually does, not the thing the row compares.** `CE-02` compared
   the whole board against a full listing — 17.7×. The question a session asks is *what next*, which
   is 389×. The row understated its own finding by twenty times.
3. **Capture the before-state first when a criterion says *unchanged*.** Once the edit is in there is
   no instrument left (`CE-03`).
4. **Prove which component failed before naming one.** A symptom measured in your environment is not
   evidence about whose defect it is (**L-87**), and a local workaround that sidesteps the broken
   mechanism will keep working while the attribution stays wrong.
5. **Check a throwaway scan against a case whose answer you know**, before reading its output as a
   finding (**L-86**).
6. **Assert what a change must never do.** Not review it — assert it, in a self-test that runs on
   every invocation, with a synthetic fixture rather than the current state of a tracked file
   (**L-78**, **L-85**).

**What to report — everything seen, filtered by nobody**

The value of an observation is the receiving project's call, not the reporter's. Record the rows that
look marginal, the ones with no obvious action, and **the assumptions worth double-checking** —
including the ones your own result rests on. There is no cost to a row nobody acts on.

**Where each thing goes**

| What you found | Where it goes |
| :--- | :--- |
| A saving in this repository | a `CE-nn` here, or a task if it is already ranked |
| Something belonging to the handoff skill, taskmd, or the harness | that owner's document under [`upstream/`](upstream), stamped *implementation*, **never ranked or banded** (`R8` §6). §7 is the pointer and the rules |
| An owner with no document yet | a **new document** under [`upstream/`](upstream), and a subsection in §7 pointing at it. `O-C1` was misfiled because the only homes available were wrong ones |
| Anything noticed that is not token efficiency | §8, the byproduct register |
| A rule that outlives the task | [`LESSONS.md`](LESSONS.md), as `L-nn`, and cited from the task rather than restated in it |
| What the *method* taught, for the skill that packages it | [T-137](../tasks/T-137-package-the-context-economy-method-as-a-skill.md) §1 — it is the only place that survives the sessions |
| A correction to a row already written | in the row, marked, with the old value kept. `CE-07`'s band and `O-T2`'s owner are both corrections and both still legible |

**What a closure owes the record.** The task's §3 and §4, a
[`RELEASE-PHASES.md`](RELEASE-PHASES.md) row folded to two cells (above the PH3 table), the
execution-order table renumbered, `shipped_in` set, and
any figure this document states that your change moved — `CE-09`'s moved because `CE-02`'s fix added
to the very section `CE-09` measures. *The row was written into `BRIEF.md` until 2026-08-14, when
`CE-05` moved that section out; the obligation is unchanged and the file is not.*

---

## 7. Upstream — observed here, reported for their owner, implemented there

**The register now lives in one document per owner, under [`upstream/`](upstream).** It was assembled
here and handed over there; this section is the pointer and the rules, not a second copy of the rows
(**L-13**). Extracted 2026-08-13 by
[T-141](../tasks/T-141-extract-the-upstream-register-into-one-document-per-owner.md), because a
recipient should not have to read an audit of somebody else's repository to find the paragraphs
addressed to them.

**The rules travel with the rows and are restated in each document:** no observation carries a
priority, because that is a guess about someone else's project; the value of an observation is the
receiving project's call, so nothing is withheld for looking marginal; and every row is stamped
*audit* — written during T-130, with that owner's backlog read first — or *implementation*, added
after findings were built, **with no backlog re-read**. An *implementation* row says *this was
observed*, never *this is not already known*.

**A new owner gets a new document.** The register began with a subsection for each tool this
repository uses, which quietly assumed every outside defect belongs to one of them; `O-C1` belongs to
neither, and the missing home is why it was first filed against the wrong project (**L-87**).

**Nothing has been sent, and nothing is sent until the audit's findings are worked and their fixes
land.** Ruled by the owner 2026-08-13. The documents are **a register that is still filling**, not a
report waiting on a courier: every finding still to be implemented is a session that may add rows,
and four out of four implementations so far have. Sending early would mean sending three times.
**So a session that finds something adds it to the owner's document and stops there** — the handover
is one deliberate act, later, and not a step in anyone's task.

### 7.1 The handoff skill

**[`upstream/handoff-skill.md`](upstream/handoff-skill.md)** — `O-H1` to `O-H6`. Backlog read for the
*audit* rows: the six open issues on the public repository (`#60`, `#57`, `#55`, `#54`, `#53`, `#8`)
plus `PROJECT_BOARD.md`. `O-H4` carries the patch applied to the installed copy here, written out so
it can reach the repository it belongs in.

### 7.2 The taskmd plugin

**[`upstream/taskmd.md`](upstream/taskmd.md)** — `O-T1` to `O-T6`. Backlog read for the *audit* rows:
138 task files, the 8 then open, and every closed title touching context, size or output. `O-T2` is
the corrected row — it would have sent them after a defect that turned out to be the harness's, and
it is kept with the error visible.

### 7.3 The harness

**[`upstream/harness.md`](upstream/harness.md)** — `O-C1`, `O-C2`. No backlog was available to read.
Both rows were measured on one machine and the document says so before it says anything else.

---

## 8. Byproduct register

**Not token efficiency. Never ranked, never banded, never a `CE-nn`.** Seen while looking for
something else.

| | File | What was seen |
| :--- | :--- | :--- |
| **BP-1** | [`tools/deck/check.py`](../tools/deck/check.py) | Given a directory instead of a deck file it raises an unhandled `PermissionError` traceback (14 lines) rather than printing usage. Reproduced with `python tools/deck/check.py examples/sort-window` |
| **BP-2** | `.handoff/` (gitignored) | Five successive handoffs carried "the release gate takes 7–11 minutes"; measured 154 seconds. **Nothing tracked in the repository states a run time**, so no committed document is wrong — the figure had no durable home at all, which is CE-08 |
| **BP-3** | [`docs/RELEASE-PHASES.md`](RELEASE-PHASES.md) | *Release phases* is 112 rows of which **68 are struck through**. Correct by the section's own convention; recorded because it is the weight behind CE-05. **134 rows and 76 struck when CE-05 was worked on 2026-08-14** — the count that grew is the finding, and it moved out of `BRIEF.md` into its own document that day |
| **BP-4** | [`tools/portability/build_probes.py`](../tools/portability/build_probes.py) | ~~85% docstring — the highest ratio in the tree by a wide margin, and the file is 61,484 bytes. Feeds CE-12~~ **Wrong, and corrected 2026-08-14: 3.2% docstring, the *lowest* ratio in the tree.** 85% is its share of triple-quoted string tokens, which in this file are the four probe payloads. The file is 61,484 bytes and that part was right. **A byproduct that fed a finding, and carried the same error into it** — §6.1, **L-92** |
| **BP-5** | The plugin cache | Seven copies of this plugin's skill description exist on this machine, one per cached version. A machine-level accumulation, not a repository fact, and `lint.py` already assumes it by globbing for the newest |

---

## 9. Candidate child tasks, and what the owner picked

Seven candidates were put up in ranked order with **none raised**, the cut-off left to the owner.
**Reviewed 2026-08-13: the top four were accepted and raised the same day.**

**The cut-off moved again on 2026-08-14, and one of the two additions was never on this list.** With
`CE-11`'s bound set and [`../CLAUDE.md`](../CLAUDE.md) reporting itself 4,555 bytes over it, the owner
raised both cuts that bound was written to make decidable:
[T-143](../tasks/T-143-split-the-release-chronology-out-of-claude-md.md) for `CE-01`, the fifth
candidate, and [T-144](../tasks/T-144-give-each-cumulative-rule-one-operative-home.md) for `CE-04`,
which ranked tenth in §6 and was never put up here. **A debt statement in tier 1 naming a finding is
what turned the citation into a task** — the enabler's stated purpose, arriving one day later than
the enabler.

**Later the same day the cut-off went to all of them: every finding in §6 now has a task**, and the
six raised last carry a scope limit rather than a place in the order —
[T-145](../tasks/T-145-move-brief-mds-release-phases-to-its-own-document.md) (`CE-05`),
[T-146](../tasks/T-146-one-file-per-lesson-with-a-generated-index.md) (`CE-06`),
[T-147](../tasks/T-147-one-workflow-file-per-lifecycle-phase.md) (`CE-09`),
[T-148](../tasks/T-148-give-a-measured-figure-a-durable-home.md) (`CE-08`),
[T-149](../tasks/T-149-prune-the-memory-index-of-spent-entries.md) (`CE-10`) and
[T-150](../tasks/T-150-relocate-the-research-prose-in-the-two-docstring-outliers.md) (`CE-12`) go to
`specify → plan` and stop, so that each is decided rather than assumed. **`cancelled` is the honest
outcome for any of them and keeps the file** (`../tasks/TASK-WORKFLOW.md` §3.1). Four of the six were
never candidates at all — this list stopped being the record of what is raised, and
[`RELEASE-PHASES.md`](RELEASE-PHASES.md) is where every one of them now has a row.

**The `specify → plan` limit was lifted by the owner on 2026-08-14**, before any of the six was
worked: they run the full lifecycle. The reason the limit existed still stands and is recorded above
— it is `cancelled` that the pass makes available, not a smaller amount of work.

**Four of the six closed the same day, and `cancelled` was used once.** T-145, T-146 and T-147 were
implemented; **T-150 was withdrawn** — and not for the *not worth it* the limit was written to catch.
`CE-12`'s figures had counted the wrong unit, so there was nothing left to weigh (§6.1, **L-92**).
**The safeguard was never the thing that saved it: the measurement was.** A pass that had stopped at
`plan` would have reasoned about the finding's stated risk and, on the row as written, most likely
approved a change that deletes two tools' payloads.

**T-148 and T-149 left that batch within the hour**, on the argument that a decision pass is for work
whose worth is in doubt: both are `xs`, both have their instance measured in this document, and both
have their mechanism already present, so the pass would cost what the work costs. They run the
ordinary lifecycle in their turn. **The same review raised
[T-151](../tasks/T-151-generate-the-finding-to-task-listing-instead-of-keeping-it-by-hand.md), which
is not a finding** — `CE-nn` closed at thirteen. Answering *which finding is which task* had just
been done by hand out of six sources, including this section, and the copy it produced was stale at
the next closure; T-151 makes that listing derived, and is the local proof of the requirement written
into [T-137](../tasks/T-137-package-the-context-economy-method-as-a-skill.md) the same day.

| Candidate | From | Effort | Why it is where it is | Outcome |
| :--- | :--- | :---: | :--- | :--- |
| Expose `taskmd list` and `context` through a wrapper beside `tools/tasks/lint.py` | CE-02 | `xs` | Largest measured saving per unit of effort in the audit, no risk, and the locating problem is already solved in a file that ships | **[T-131](../tasks/T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md)** |
| Add a quiet mode to `tools/deck/check.py` | CE-03 | `xs` | 4,348 estimated tokens per green invocation, several per deck session | **[T-132](../tasks/T-132-give-the-deck-gate-a-quiet-mode-for-its-green-run.md)** |
| Write down that a deck is never read whole | CE-13 | `xs` | One line, and it removes a failure that costs an entire session | **[T-133](../tasks/T-133-write-down-that-a-deck-is-never-read-whole.md)** |
| State the tier model and bound tier 1 as a relation | CE-11 | `s` | The enabler. It should land before CE-01 and CE-04 so those cuts are decided rather than negotiated | **[T-134](../tasks/T-134-state-the-tier-model-and-bound-tier-1-as-a-relation.md)** |
| Split the release chronology out of `CLAUDE.md` | CE-01 | `s` | 45% of a tier-1 file, paid every turn | **[T-143](../tasks/T-143-split-the-release-chronology-out-of-claude-md.md)** |
| Move `BRIEF.md`'s *Release phases* to its own document | CE-05 | `m` | 61% of the document new sessions are told to read first. **Carries a named collision**: the `DUPLICATE INDEX` advisory is excused by file name and would follow the content | **[T-145](../tasks/T-145-move-brief-mds-release-phases-to-its-own-document.md)** |
| One file per lesson, with a generated index | CE-06 | `m`–`l` | The largest read-path document in the repository, needed one entry at a time | **[T-146](../tasks/T-146-one-file-per-lesson-with-a-generated-index.md)** |

**CE-05's collision was ruled at the same review: the excusal moves with the content, inside the same
task.** [`../tasks/TOOLING.md`](../tasks/TOOLING.md) §1 excuses the `DUPLICATE INDEX` advisory *by file name* — it was `tasks/TASK-WORKFLOW.md` §6 until T-147 moved it — and the
advisory is believable everywhere else precisely because that excusal is narrow. Splitting the move
from the excusal would leave the advisory firing correctly against a document no rule covers, in the
window between two tasks — which is the state the excusal exists to prevent.

**CE-07 closed the same day at a quarter of its band, and the correction is the useful part.**
[T-135](../tasks/T-135-cut-the-load-path-this-project-cannot-use.md) bought **~800 tokens of a 7,300
token listing over two restarts**, then stopped moving. A per-skill override reaches built-in and
user skills; plugin-supplied ones are governed by whatever enables the plugin, and those plugins are
not installed here. `L` was an honest reading of the block's size and a careless one of its
addressable share — **a gain band is a claim about reachable saving, and this one was not.** One
experiment would decide the rest and it is the owner's, because it touches every project they work in.

**How it became a task at all:** It was ranked as the owner's
machine on the reasoning that the plugins supplying most skills are not installed on disk, so no
setting could reach them. The configuration schema says otherwise: the listing override keys on the
**skill's name**, not on its delivery, and it is honoured at project scope in a file this repository
already keeps out of git. The correction is recorded in
[`research/R8-context-economy-for-coding-agents.md`](research/R8-context-economy-for-coding-agents.md)
§8, under CE-07, because the lesson is portable and larger than the finding.

**CE-10 stands as not repository work** — pruning the memory index is the owner's memory, and is
named here so it is not mistaken for a task.
