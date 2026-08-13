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

---

## 7. Upstream — observed here, reported for their owner, implemented there

**Both backlogs were read before anything below was written.** Neither is this repository's to edit,
and neither observation carries a priority — that is a guess about someone else's project.

### 7.1 The handoff skill

**Backlog read:** the six open issues on the public repository (`#60` standalone reconcile, `#57` doc
fixes, `#55` ad-hoc snapshot exit reminder, `#54` install verification, `#53` config validation, `#8`
pickup intelligence with multiple archives), plus `PROJECT_BOARD.md`.

| | Observation |
| :--- | :--- |
| **O-H1** | **A measured figure propagated through five successive handoffs and was wrong by 3×.** A release-gate run time appeared in five consecutive handoff files here; measuring it returned 154 seconds against the 7–11 minutes being carried. The core's own golden rule — *the handoff points, it does not store* — already forbids this, and the failure is that a **number** does not look like the kind of fact the rule is about. **Where it might land:** the create flow's pre-write checklist already scans for secrets; measured figures are a second category with the same shape — value in the handoff, no durable home, copied forward untested. `#53` and `#57` are the nearest open items and neither covers it |
| **O-H2** | **There is no retention rule for archived handoffs.** This repository has **47** archived files, mean 4,932 bytes; they are gitignored here so they cost a clone nothing, but in another adopting repository the archives are tracked and sit in the tree agents glob. `#8` is adjacent — it is about *pickup* when several exist, not about how many accumulate |
| **O-H3** | **A confirmation, not a finding.** The spine-plus-one-branch design measurably works. This audit's own session loaded the core and `flows/resume.md` and never touched `flows/create.md` or the tracker binding — **about 13 KB present, ~13 KB not paid.** It is also the design the owner's task tracker explicitly copied when it settled its own tier model |

### 7.2 The taskmd plugin

**Backlog read:** 138 task files, 8 open (`T-005`, `T-085`, `T-093`, `T-108`, `T-130`, `T-131`,
`T-135`, `T-138` — **all theirs**), plus every closed title touching context, size or output. *Their*
`T-015`, `T-028` and `T-048` already did this work upstream.

| | Observation |
| :--- | :--- |
| **O-T1** | **Nothing to propose about tiering — they did it first, and this project should follow them.** Their `T-028` established the membership rule, the three tiers, and the budget-as-a-relation, and rejected both the alternatives an outsider would arrive with. That is CE-11's source, and the direction of travel is upstream→here |
| **O-T2** | **The command surface is unreachable in an agent shell, and that is what causes this audit's largest read-path cost.** `taskmd list --open` answers in 1,901 bytes what reading the generated index costs 33,676 — **17.7×** — and `context` answers one task in 790. Because the bare command does not resolve, every adopter re-derives a `PYTHONPATH` locator; this repository's lives in `tools/tasks/lint.py`, globbing the version directory so a plugin update does not break it silently. **Where it might land:** their `T-085` (*install the published plugin on a machine that has never seen it*, in progress) is the natural home, and their closed `T-073` (*correct the command surface local context still states*) is the adjacent precedent |
| **O-T3** | **A generated index grows without bound and has no cheap form.** 134 rows, 33,676 bytes here. Their `T-087` let `list` filter on a field the index shows, which is the same problem approached from the query side. Stated as an observation only: the index is for people, and the fix may simply be that agents should never read it — which is what O-T2 makes possible |

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
