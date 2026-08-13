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

**Tool schemas are already deferred** — roughly 100 tool names are listed without their schemas, and
a schema loads on request. That is the single largest saving available on this surface and the
harness already takes it. No finding.

### 2.2 Surface B — the read path for one unit of work

| Document | Bytes | ~tokens | Needed for one task? |
| :--- | ---: | ---: | :--- |
| [`docs/LESSONS.md`](LESSONS.md) | 152,444 | 38,111 | One entry of 81, cited as `L-nn` |
| [`docs/BRIEF.md`](BRIEF.md) | 108,163 | 27,041 | "Read the brief first" — 61% of it is one appendix |
| [`docs/DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) | 75,295 | 18,824 | Deck work only |
| [`docs/DESIGN-RATIONALE.md`](DESIGN-RATIONALE.md) | 62,463 | 15,616 | Rarely |
| [`tasks/README.md`](../tasks/README.md) | 33,676 | 8,419 | The board — 134 rows |
| [`docs/COMPONENT-CONTRACT.md`](COMPONENT-CONTRACT.md) | 26,947 | 6,737 | Deck work only |
| [`docs/EVALUATION.md`](EVALUATION.md) | 26,784 | 6,696 | Rarely |
| [`docs/PUBLISHING.md`](PUBLISHING.md) | 23,173 | 5,793 | Releases |
| [`docs/THEME-CONTRACT.md`](THEME-CONTRACT.md) | 21,663 | 5,416 | Deck work only |
| [`tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md) | 21,374 | 5,344 | Every task — 52% of it is §6 |
| The task file itself, median of 130 | 12,528 | 3,132 | Yes |
| **The mandatory set** (lessons + brief + board + workflow + the task) | **328,185** | **~82,046** | |

**The mandatory set is 41% of a 200k window before the work starts.** That is the growth the task was
raised about, and it is measured rather than felt.

**Where the weight sits inside the three biggest.**

| Document | Largest section | Bytes | Share |
| :--- | :--- | ---: | ---: |
| `docs/BRIEF.md` | *Release phases* — 112 rows, 68 struck through | 66,461 | **61%** |
| `docs/LESSONS.md` | 81 entries, mean 1,873 bytes | 151,751 | **>99%** |
| `tasks/TASK-WORKFLOW.md` | §6 *The tooling* | 11,026 | **52%** |
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

**All five families were walked. Each yielded at least one finding, and each also produced a negative
worth recording.**

| Family | Findings | The negative result |
| :--- | :--- | :--- |
| **F1** — what loads, and when | CE-01, CE-05, CE-06, CE-09, CE-11 | `skills/htmldeck/` needs nothing: it is already three-stage (§3) |
| **F2** — redundancy and contradiction | CE-04, CE-08, CE-10 | **No contradicting pair was found.** The record's cross-references are unusually consistent, which three reference checkers plausibly explain |
| **F3** — prose not doing work | CE-12 (two outliers only) | **The general sweep is rejected** — see §5.1 |
| **F4** — model work that should be deterministic | CE-02, CE-13 | Tool schemas and the gate chain are already deterministic; `lint.py` already solves the locating problem CE-02 reuses |
| **F5** — tool and workflow economics | CE-03, CE-07 | `check_all.py` already suppresses child output by default, and the per-task/per-release gate split is already correct |

### 5.1 The F3 rejection, recorded

**Rejected: a sweep over the record's rationale prose — tool docstrings at 30% of `tools/**/*.py`, and
task log rows.** It cannot name what the prose would stop deciding. Every sample checked carried a
reason a future reader needs: why a rule exists, what it cost to learn, what was rejected and why,
what would close an excusal. That is the test in `R8-context-economy-for-coding-agents.md` §4.1, and
this sweep fails it.

**What survives is CE-12**, two files whose docstring share is so far outside the distribution that
the question is worth asking about them specifically — and even there the change is relocation, not
deletion.

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
| 6 | **CE-11** | A / F1 | Adopt the tier model and a relation-bound tier 1 | *enabler* | `s` | none | §6.1 |
| 7 | **CE-05** | B / F1 | Move `BRIEF.md`'s *Release phases* to its own document | `XL` | `m` | stated | R8 §8 |
| 8 | **CE-06** | B / F1 | One file per lesson, plus a generated index | `XL` | `m`–`l` | stated | R8 §8 |
| 9 | **CE-09** | B / F1 | One workflow file per lifecycle phase | `L` | `m` | stated | §6.1 |
| 10 | **CE-04** | A+B / F2 | One operative home per cumulative rule | `M` | `xs` each | stated | R8 §8 |
| 11 | **CE-08** | A / F2 | A measured figure gets a durable home | `S` | `xs` | none | R8 §8 |
| 12 | **CE-10** | A / F2 | Prune the memory index of spent entries | `S` | `xs` | stated | §6.1 |
| 13 | **CE-12** | B / F3 | Two docstring outliers | `M` | `s` | stated | §6.1 |

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

#### CE-12 — Two files where docstrings are most of the file

| | |
| :--- | :--- |
| **Surface / Family** | B / F3 |
| **Finding** | Docstrings are 30% of `tools/**/*.py`, which is this project's deliberate style and is **not** a finding (§5.1). Two files sit far outside that: `tools/portability/build_probes.py` is **85%** docstring (52,408 of 61,484 bytes) and `tools/deck/print_variants.py` is **58%**. `tools/deck/audit.py` is 36% but is the largest file in the tree at 141,896 bytes, so its 52,230 bytes of docstring is the biggest single block |
| **Change** | For those files only, ask what the prose decides. Where it is a research record rather than a rule for the next editor, **relocate it to `docs/research/`** and leave a pointer. Deletion is not the change |
| **Gain** | `M` on the read path when those files are edited, which is rare |
| **Effort** | `s` |
| **Risk** | These are the files whose behaviour is least obvious, which is plausibly *why* they carry the most explanation. A relocation that makes a probe's reasoning unfindable costs more than it saves |
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
| Something belonging to the handoff skill, taskmd, or the harness | §7, under that owner, stamped *implementation*, **never ranked or banded** (`R8` §6) |
| An owner §7 has no subsection for | a **new subsection**. `O-C1` was misfiled because the only homes available were wrong ones |
| Anything noticed that is not token efficiency | §8, the byproduct register |
| A rule that outlives the task | [`LESSONS.md`](LESSONS.md), as `L-nn`, and cited from the task rather than restated in it |
| What the *method* taught, for the skill that packages it | [T-137](../tasks/T-137-package-the-context-economy-method-as-a-skill.md) §1 — it is the only place that survives the sessions |
| A correction to a row already written | in the row, marked, with the old value kept. `CE-07`'s band and `O-T2`'s owner are both corrections and both still legible |

**What a closure owes the record.** The task's §3 and §4, a `BRIEF.md` row folded to two cells
(*Release phases*, above the PH3 table), the execution-order table renumbered, `shipped_in` set, and
any figure this document states that your change moved — `CE-09`'s moved because `CE-02`'s fix added
to the very section `CE-09` measures.

---

## 7. Upstream — observed here, reported for their owner, implemented there

**Neither project is this repository's to edit, and no observation carries a priority** — that is a
guess about someone else's project, and the value of an observation is the owner's to judge, not
ours. Everything seen is recorded; nothing is withheld for looking marginal.

**Two vintages, and they are not equally checked.** The rows marked **audit** were written during
T-130, with both backlogs read first. The rows marked **implementation** were added by
[T-140](../tasks/T-140-correct-and-extend-the-upstream-register-from-what-implementing-the-audit-found.md)
after four findings were built, **and no backlog was re-read for them** — building a thing sees what
auditing it does not, but it also sees it without the owner's context. Read an *implementation* row
as *this was observed*, never as *this is not already known or already decided*.

**§7.3 exists because one row had the wrong owner.** The register was built with a home for the
handoff skill and one for taskmd, which quietly assumed every outside defect belongs to one of the
two tools this repository uses. `O-C1` belongs to neither.

### 7.1 The handoff skill

**Backlog read:** the six open issues on the public repository (`#60` standalone reconcile, `#57` doc
fixes, `#55` ad-hoc snapshot exit reminder, `#54` install verification, `#53` config validation, `#8`
pickup intelligence with multiple archives), plus `PROJECT_BOARD.md`.

| | Observation |
| :--- | :--- |
| **O-H1** *audit* | **A measured figure propagated through five successive handoffs and was wrong by 3×.** A release-gate run time appeared in five consecutive handoff files here; measuring it returned 154 seconds against the 7–11 minutes being carried. The core's own golden rule — *the handoff points, it does not store* — already forbids this, and the failure is that a **number** does not look like the kind of fact the rule is about. **Where it might land:** the create flow's pre-write checklist already scans for secrets; measured figures are a second category with the same shape — value in the handoff, no durable home, copied forward untested. `#53` and `#57` are the nearest open items and neither covers it |
| **O-H2** *audit* | **There is no retention rule for archived handoffs.** This repository has **47** archived files, mean 4,932 bytes; they are gitignored here so they cost a clone nothing, but in another adopting repository the archives are tracked and sit in the tree agents glob. `#8` is adjacent — it is about *pickup* when several exist, not about how many accumulate. *Datum added 2026-08-13: 49* |
| **O-H3** *audit* | **A confirmation, not a finding.** The spine-plus-one-branch design measurably works. This audit's own session loaded the core and `flows/resume.md` and never touched `flows/create.md` or the tracker binding — **about 13 KB present, ~13 KB not paid.** It is also the design the owner's task tracker explicitly copied when it settled its own tier model. *Confirmed a second time 2026-08-13 by the session that resumed this work: core plus one flow, `flows/create.md` never opened* |
| **O-H4** *implementation* | **A mode word followed by a qualifier routes to the opposite mode.** The spine's §4 says trailing text that is *just* a mode word selects that mode, and that **otherwise the whole argument is the subject of a handoff to create**. A user typed `resume, full lifecycle` — a mode word plus a qualifier about how to work — which by the letter of the rule selects **Create** and records *"resume, full lifecycle"* as the next session's task. Resume was obviously meant, and Resume was run. The rule reads as though the alternative to a bare mode word is a sentence describing future work, but `<mode> <qualifier>` is ordinary phrasing and lands on the wrong side of it. **Where it might land:** §4's *Explicit invocation and its argument*, and the same section's ambiguity rule already prefers the non-mutating path, which points the same way |
| **O-H5** *implementation* | **A handoff that states a board count is storing a derived fact, and the one consumed here was already stale.** It read *22 open, 115 closed*; the tracker said 23 active before this session changed anything. Harmless once, and the same class as `O-H1` — the golden rule *the handoff points, it does not store* is broken by counts and figures without looking as though it is, because a count feels like state rather than like a fact with a home. A pointer to the command that answers it costs one line and cannot go stale |
| **O-H6** *implementation* | **`reconcile_targets` is a hand-kept list, and the §3a sweep went outside it.** This project declares `tasks/, docs/BRIEF.md`. Closing four tasks made statements stale in `docs/CONTEXT-AUDIT.md` and `docs/LESSONS.md` as well, and both were reconciled because the session had touched them — which is the *fallback* rule, not the declared one. A declared list is subject to exactly the staleness it exists to prevent, and this repository's own release gate treats a hand-kept list as a defect class in its own right. **Where it might land:** §0's key description, or §3a's closing test — possibly as *the declared targets are a floor, never a ceiling*, which is what actually happened here |

### 7.2 The taskmd plugin

**Backlog read:** 138 task files, 8 open (`T-005`, `T-085`, `T-093`, `T-108`, `T-130`, `T-131`,
`T-135`, `T-138` — **all theirs**), plus every closed title touching context, size or output. *Their*
`T-015`, `T-028` and `T-048` already did this work upstream.

| | Observation |
| :--- | :--- |
| **O-T1** *audit* | **Nothing to propose about tiering — they did it first, and this project should follow them.** Their `T-028` established the membership rule, the three tiers, and the budget-as-a-relation, and rejected both the alternatives an outsider would arrive with. That is CE-11's source, and the direction of travel is upstream→here |
| **O-T2** *audit, corrected* | **The command surface is unreachable in an agent shell, and that is what causes this audit's largest read-path cost — but the defect is not taskmd's.** The saving is real and larger than first stated: `list --open` answers in 2,451 bytes what reading the generated index costs 36,813, and `list --open --limit 1` — the form that actually answers *what next* — answers in **94 bytes, 389×** (2026-08-13, after T-131). **The cause was measured in T-140 and it is the harness**, not the packaging: taskmd ships `bin/taskmd`, the launcher runs correctly when invoked directly, and the harness does emit its directory into the shell snapshot — where the `PATH` line is truncated mid-value. That is `O-C1`, and this row previously pointed at *their* `T-085` (*install the published plugin on a machine that has never seen it*), which would have been a hunt for a defect that is not there. **What is left for taskmd** is a smaller and still real question: the design comment in `bin/taskmd` states the `PATH` mechanism as given — *no install step, no PYTHONPATH to set, no path to a cache directory anyone has to know* — and one environment breaks it silently, so a documented fallback for *the command is not on PATH* may be worth having. Every adopter otherwise re-derives a locator, and re-deriving it is error-prone: this repository's globbed the version directory and **sorted it as text**, which would have selected `0.5.0` over `0.10.0` at the next bump (**L-85**) |
| **O-T3** *audit* | **A generated index grows without bound and has no cheap form.** 134 rows, 33,676 bytes here. Their `T-087` let `list` filter on a field the index shows, which is the same problem approached from the query side. Stated as an observation only: the index is for people, and the fix may simply be that agents should never read it — which is what O-T2 makes possible. *Datum added 2026-08-13: five task closures in one session took it to 139 rows and 36,813 bytes, **+9.3% in a day**, while `list --open` moved from 1,901 to 2,451. The index grows with the whole board; the query grows only with what is open* |
| **O-T4** *implementation* | **A markdown table row with more cells than its header loses the excess silently, and nothing in a markdown-native tracker can see it.** Two rows of a document here carried a whole paragraph in a third cell against a two-column header; GitHub-flavoured markdown drops it, so the text existed in the file and rendered nowhere, for weeks, with `check` green ([T-139](../tasks/T-139-two-rows-in-brief-md-carry-a-cell-the-table-cannot-render.md)). `check` already reads documents and resolves markdown links, so it is the only tool in the neighbourhood — **and this repository decided against building the equivalent gate for itself**, on the grounds that a cell past the header is not a broken pointer and a checker for two rows would outlive the fault. Recorded because that trade may come out differently for a tool whose whole subject is markdown records, and because the failure mode is invisible by construction: the only instrument is counting cells against the header |
| **O-T5** *implementation* | **`--help` on a subcommand prints the top-level usage, so the options cannot be discovered from the CLI.** `python -m taskmd list --help` and `... context --help` both print `usage: taskmd {check,context,index,list} [args] [--root PATH]` and nothing else (0.5.0). `--open`, `--closed`, `--limit`, `--json` and the `--<field> V` form are in `SKILL.md` and in `cli.py`'s module docstring; an agent that has the command but not the skill file has to read the source. This is a context-economy point as well as a usability one — it is the case where a caller reads a file to learn what a flag is called |
| **O-T6** *implementation* | **A field the project requires at a status transition has no gate, and three tasks closed without it.** This project's convention is that `shipped_in` is set when a task closes; `check` validates the *value* of a declared field but nothing ties a field's presence to a status. 113 of 138 files carried it and three closed tasks did not, found by hand. The adjacent case is already filed as **their** `T-063` — an open task at `specified` or later declaring no deliverable — which is the same shape: *this field becomes required at this point in the lifecycle*. Recorded as one observation rather than two because the general form may be cheaper than either instance |

### 7.3 The harness

**Backlog read: none.** There is no backlog here to read, and this section exists because one
observation had nowhere else to go. Everything below is *implementation* vintage and was measured on
one machine — Windows 11, Git Bash and PowerShell 7 — which is one data point about a surface that
almost certainly varies.

| | Observation |
| :--- | :--- |
| **O-C1** *implementation* | **The shell snapshot's `PATH` line is truncated mid-value, and it silently removes every plugin's `bin/` directory.** Measured 2026-08-13: the snapshot's `export PATH='…'` line is **5,551 characters, 67 entries, and ends mid-path with no closing quote**; the shell that sources it has **37 entries and zero plugin `bin/` directories**, so 30 entries were lost including all three from the plugin cache. **20 of the 67 are session-scoped `local-agent-mode-sessions/<id>/<id>/rpm/plugin_<id>/bin` paths of about 200 characters each**, which is where the length comes from. Nothing reports the failure: a plugin's command simply does not exist, which reads as a broken install. It cost this repository a wrapper, an upstream observation filed against the wrong project, and — through the locator that wrapper needs — a latent version-ordering defect (**L-85**). **Two directions worth considering, neither ours to choose:** shorten what goes in, since twenty session-scoped entries dominate the line; and fail loudly rather than truncate, since a `PATH` that cannot be written whole is worth an error |
| **O-C2** *implementation* | **PowerShell gets no plugin `bin/` at all, by a different route.** `Get-Command taskmd` does not resolve and `$env:PATH` contains no `plugins` entry, on the same machine and in the same session where the Bash snapshot at least *contained* the directory before losing it. So the two shells this environment offers disagree about what commands exist, and neither offers the plugin's. Recorded separately from `O-C1` because the mechanism is not the same and a fix for one need not fix the other |

---

## 8. Byproduct register

**Not token efficiency. Never ranked, never banded, never a `CE-nn`.** Seen while looking for
something else.

| | File | What was seen |
| :--- | :--- | :--- |
| **BP-1** | [`tools/deck/check.py`](../tools/deck/check.py) | Given a directory instead of a deck file it raises an unhandled `PermissionError` traceback (14 lines) rather than printing usage. Reproduced with `python tools/deck/check.py examples/sort-window` |
| **BP-2** | `.handoff/` (gitignored) | Five successive handoffs carried "the release gate takes 7–11 minutes"; measured 154 seconds. **Nothing tracked in the repository states a run time**, so no committed document is wrong — the figure had no durable home at all, which is CE-08 |
| **BP-3** | [`docs/BRIEF.md`](BRIEF.md) | *Release phases* is 112 rows of which **68 are struck through**. Correct by the section's own convention; recorded because it is the weight behind CE-05 |
| **BP-4** | `tools/portability/build_probes.py` | 85% docstring — the highest ratio in the tree by a wide margin, and the file is 61,484 bytes. Feeds CE-12 |
| **BP-5** | The plugin cache | Seven copies of this plugin's skill description exist on this machine, one per cached version. A machine-level accumulation, not a repository fact, and `lint.py` already assumes it by globbing for the newest |

---

## 9. Candidate child tasks, and what the owner picked

Seven candidates were put up in ranked order with **none raised**, the cut-off left to the owner.
**Reviewed 2026-08-13: the top four were accepted and raised the same day.** The remaining three
stand as candidates and are not tasks.

| Candidate | From | Effort | Why it is where it is | Outcome |
| :--- | :--- | :---: | :--- | :--- |
| Expose `taskmd list` and `context` through a wrapper beside `tools/tasks/lint.py` | CE-02 | `xs` | Largest measured saving per unit of effort in the audit, no risk, and the locating problem is already solved in a file that ships | **[T-131](../tasks/T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md)** |
| Add a quiet mode to `tools/deck/check.py` | CE-03 | `xs` | 4,348 estimated tokens per green invocation, several per deck session | **[T-132](../tasks/T-132-give-the-deck-gate-a-quiet-mode-for-its-green-run.md)** |
| Write down that a deck is never read whole | CE-13 | `xs` | One line, and it removes a failure that costs an entire session | **[T-133](../tasks/T-133-write-down-that-a-deck-is-never-read-whole.md)** |
| State the tier model and bound tier 1 as a relation | CE-11 | `s` | The enabler. It should land before CE-01 and CE-04 so those cuts are decided rather than negotiated | **[T-134](../tasks/T-134-state-the-tier-model-and-bound-tier-1-as-a-relation.md)** |
| Split the release chronology out of `CLAUDE.md` | CE-01 | `s` | 45% of a tier-1 file, paid every turn | candidate |
| Move `BRIEF.md`'s *Release phases* to its own document | CE-05 | `m` | 61% of the document new sessions are told to read first. **Carries a named collision**: the `DUPLICATE INDEX` advisory is excused by file name and would follow the content | candidate |
| One file per lesson, with a generated index | CE-06 | `m`–`l` | The largest read-path document in the repository, needed one entry at a time | candidate |

**CE-05's collision was ruled at the same review: the excusal moves with the content, inside the same
task.** `tasks/TASK-WORKFLOW.md` §6 excuses the `DUPLICATE INDEX` advisory *by file name*, and the
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
