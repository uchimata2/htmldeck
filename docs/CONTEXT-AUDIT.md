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
at all and bought a gate instead. The third, `CE-09`, closed the same day with its shape refused. A
share-of-file figure says where the weight is, not what removing it is worth.*

***All thirteen findings had closed tasks by the end of 2026-08-14.** The paragraph above is what the
audit predicted; what it actually bought is
[T-153](../tasks/T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md)'s subject,
and `python tools/docs/findings.py` is the current state rather than any count written here.*

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

*Re-measured again 2026-08-14 after T-143 and T-144: `../CLAUDE.md` is **14,917 bytes**, down from
19,035 — **−21.6%**, and still 3,338 over a bound whose smaller term is now `../tasks/TASK-WORKFLOW.md`
at 11,579 rather than `.taskmd/config.md`. Tier 1 is **~26,900 bytes**, holding the other two files at
their audit figures. Three re-measurements of one figure in two days, each one moving it: this is what
§6.2's first rule is about.*

*Re-measured a fourth time 2026-08-14, in passing during T-138: [`../CLAUDE.md`](../CLAUDE.md) is
**15,208 bytes** against [`../tasks/TASK-WORKFLOW.md`](../tasks/TASK-WORKFLOW.md)'s **11,925** — so the
line above is stale in **both** terms, which is the failure `../CLAUDE.md` records having made twice
itself. Both terms are re-measured together or neither is; the operative statement of the debt is in
`../CLAUDE.md` and this is a dated observation of it, not a second home for it.*

**Tool schemas are already deferred** — roughly 100 tool names are listed without their schemas, and
a schema loads on request. That is the single largest saving available on this surface and the
harness already takes it. No finding.

**The capability-listing mechanism, and the three null results — `CE-07`'s evidence.** *Moved here
from `R8` §8 on 2026-08-14 by
[T-138](../tasks/T-138-make-the-portable-half-agent-agnostic.md). It is a measurement of one machine
and one harness, so the portable half now states the shape and this is where the mechanism lives.*

The audit first reported the listing as untouchable, reasoning that the plugins supplying most entries
were not installed anywhere on disk, so no plugin-enable setting could reach them. **True and
irrelevant.** The configuration schema exposes a **per-skill listing override keyed on the skill's
*name***, which does not care where the skill is served from, plus a switch that stops cloud
connectors being fetched at all, and a budget fraction capping what the whole listing may cost.

Then measuring the correction produced a second one. **Two restarts and three measurements moved ~800
tokens of a 7,300-token listing, and then stopped.** What that established is a boundary, not a
saving:

- **the per-skill override reaches the skills the harness itself and the user provide**; skills a
  plugin supplies are governed by whatever enables the plugin, and where those plugins are not
  installed locally, no file on this machine names them;
- **the connector switch was accepted at every scope tried and inert at all of them**, including the
  user scope that was supposed to be the decisive test.

**Three mechanisms, three scopes, three null results** — which is why `CE-07`'s controller is
`harness` rather than a low band. The cost is visible in the accounting, attributable to a named
source, and not addressable by the project that pays it. T-135 is the task; **L-82** and **L-83** are
the general halves.

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
| ~~`CLAUDE.md`~~ | ~~*What this is* — release chronology~~ **moved out 2026-08-14 by [T-143](../tasks/T-143-split-the-release-chronology-out-of-claude-md.md) to `RELEASE-HISTORY.md`; the file went 19,035 → 15,416 bytes and its largest section is now the same heading at 3,760 / 24.4%, holding rules rather than dates** | ~~6,980~~ | ~~**45%**~~ |

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
three verdicts partition the catalogue: 12 adopted, 10 rejected, 13 deferred, summing to 35.**

**Re-screened in full 2026-08-14** by
[T-136](../tasks/T-136-re-run-the-external-research-with-a-recorded-search-record.md), which re-ran the
research under the coverage rule and took the catalogue from 21 to 35. **Every row was re-derived, not
only the new ones** — a row screened against a thin catalogue was screened against a different
denominator. No verdict on the original 21 changed; four rows gained a measurement, which is a
different thing and is marked in each.

**And the partition is still not a coverage claim.** It summed correctly at 19 while two techniques
were missing entirely, and it summed correctly at 21 while fourteen were. Both times the arithmetic
was right and the catalogue was short. `R8` §7.1 is the search record that replaces the reassurance the
sum was never giving, and `R8` §10's fifth limit now carries the measured size of the gap.

*The rows below are no longer provisional: T20 and T21 are confirmed, and both are now screened
against an independent measurement rather than an argument.*

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
| T20 | Generation restraint — a decision ladder | **deferred** | Two constraints pull opposite ways and neither settles it. **For the tooling** it may fit: standard-library-only is already a rung of that ladder (**L-07**). **For the decks it fights the brief** — rule 2 wants richness, interaction, animation and 3D, so a minimalism rule pointed at deck output is aimed at the wrong artifact. And its own instructions are a permanent load-path cost, which an audit ranking by load path has to count against it. **The evidence to close this now exists** (`R8` §7): an 80-task benchmark measures −10.3% cost, about four times below the advertised figure, **concentrated on big builds and zero where little was going to be written**. That sharpens the closing condition rather than settling it — scope it to `tools/`, where the ladder's rungs are already rules, and weigh its permanent listing cost against a saving this repository's write volume may not be large enough to earn |
| T21 | Semantic index over the repository | **rejected** | Collides with two rules at once. **L-07** and the out-of-the-box constraint: this repository ships standard library only and must clone and run, so an index service or embedding library is a dependency it does not take. And the index would be a machine-local artifact that no clone receives — the same property that made `taskmd check` refuse a link to the git-ignored settings file. The corpus is also small enough that naming files works: the read path is a dozen documents, not a codebase. **Measured 2026-08-14 and the rejection holds on its own terms**: the reported gains — about +12.5% accuracy, ~40% fewer tokens — are stated *for large heterogeneous corpora*, and lexical search is reported to win on small plain-text ones. This corpus is the second kind, so the technique is not merely unaffordable here, it is aimed elsewhere |
| T22 | Code execution over tool calls | **rejected** | Collides with what a repository controls — the same constraint that rejected T11. This project ships documents, a skill and standard-library tools; it does not assemble the agent's tool layer and publishes no MCP server, so there is no surface here to apply it to. Nothing about it is wrong; it is addressed to whoever owns the tool layer |
| T23 | On-demand tool retrieval | **adopted** | Already in force, harness-side — deferred tool schemas are fetched by query in this very session. No work, and it is listed separately from T5 because they are different mechanisms: T5 defers the *schema* behind a visible name, this one defers the name too |
| T24 | Token-oriented serialization | **deferred** | The only uniform, tabular payload a session reads here is the board listing, and CE-02's fix already replaced reading it with asking it — so the candidate payload shrank before the format could be applied to it. Closed by a machine-read payload large and uniform enough to pay for a notation no other reader knows |
| T25 | A compression proxy in the path | **rejected** | Collides with the out-of-the-box constraint, exactly as T21 does: a component between agent and model is not something a clone receives, and this repository cannot ship one. It is also lossy by construction, which the record — the project's memory — is the wrong corpus for |
| T26 | Server-side context editing | **deferred** | Harness- and API-side. This repository controls file contents, not the API call. Closed by the harness exposing it as a setting, at which point it costs this project nothing to take. It is the one clearing technique that does not collide with T11, which is why it is listed apart from T6 |
| T27 | Symbol-level retrieval | **rejected** | Collides with **L-07** and out-of-the-box — a language server per language is a dependency this repository does not take — and with the corpus: the read path is Markdown prose, which has no symbol graph. `tools/` is the one place it would apply, and is also the place a standard-library route exists (see T28) |
| T28 | A ranked repository map on a token budget | **deferred** | **The strongest new candidate.** It would suit `tools/` (921 KB) and `shell/` (115 KB), the same two T13 names, and unlike T27 there is a route that takes no dependency: Python's own `ast` is standard library, so a ranked map of the tool set is buildable within **L-07**. Closed by measuring how much of a session's read path is actually `tools/` — unmeasured, so no band is written, on T19's precedent |
| T29 | Whole-repository packing with a token report | **rejected** | Collides with the audit's own axis: packing the repository into one file maximizes load, which is the thing being reduced. **The measurement half is already in force** — `R8` §3's *measure with a program* step is a throwaway script that does exactly the token-report part, without the packing |
| T30 | Deterministic enforcement instead of instruction | **adopted** | Already in force and it is the general statement of the F4 family: `check.py`, `tools/tasks/lint.py` and `check_all.py` are rules that left the prompt for a gate. The reported compliance gap — 70–90% for a prompt rule against 100% for an enforced one — is the argument this project already made from the other direction, and it is why a rule that can be checked belongs in a checker |
| T31 | Session telemetry as the instrument | **deferred** | It closes `R8` §10's first limit, which until now read as an impossibility. It costs no repository dependency — the collector is the owner's machine, not a clone's — so this is the owner's setting to enable, not this project's to ship. Closed by enabling the export and pointing it somewhere |
| T32 | Addressable recall | **deferred** | Harness-side, like T6 and T15. Closed by the harness exposing it. Worth the row because it is the one form of clearing that leaves a handle behind, which is the objection to T6 |
| T33 | A curated entry index for machine readers | **adopted** | Already in force, and it names what this repository was doing without the name: `CLAUDE.md` is the root layer, the tier-2 set is the base layer, and `tasks/README.md` is the index. **The tier discipline in `CLAUDE.md` is stricter than the convention**, because it establishes membership by observation rather than by a file's claim about itself |
| T34 | A capped reasoning budget | **deferred** | Harness-side, and a session setting rather than a repository one. Closed by the harness exposing a per-task cap. Nothing here can set it |
| T35 | Version-pinned documentation retrieval | **rejected** | Collides with **L-07** twice over: it is an external service in the loop, and this repository has no third-party dependencies whose documentation it would otherwise carry. The technique solves a problem standard-library-only does not have |

### 4.1 The finding question, answered

**The re-run produced no new `CE-nn`, and that is a result rather than an omission.** It is written
here because [T-153](../tasks/T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md)
was blocked on the answer: phase 2 prices a ranking, and a ranking about to change should not be
priced.

**Why none, stated so it can be argued with.** The findings rest on the inventory — steps 1–4, which
measure this repository — and not on the catalogue, which is why re-running step 5 can leave the
ranking untouched without that being suspicious. Fourteen techniques arrived; **ten of them are
addressed to somebody else** — the harness, the API, or whoever assembles the tool layer — and land as
deferrals and rejections naming the constraint, which is what those verdicts are for. Of the four that
could bear on this repository, three are already in force under a different name (T23, T30, T33) and
the fourth, **T28, is the one real candidate and is unmeasured**. On T19's precedent an unmeasured
candidate gets a deferral with a closing condition, not a band — a `CE-nn` invented for it would carry
a gain estimate with nothing behind it.

**What did change is smaller and worth having**: two rejections that rested on argument now rest on a
measurement (T20, T21), one limit of the method turned out to be a choice rather than an impossibility
(`R8` §10, first limit), and one candidate got a route that does not break **L-07** (T28).

**One thing the re-run found is about this document rather than about the repository.** The partition
above — *12 adopted, 10 rejected, 13 deferred, summing to 35* — is a part-of-whole claim in prose, in
two documents, checked by nobody: `tools/docs/figures.py` binds such claims only through a declared
`ACCOUNTS` entry, and there is no command that counts these rows. The sum was wrong-by-omission twice
already and no gate said so. That is
[T-156](../tasks/T-156-make-the-screening-partition-a-figure-a-checker-can-count.md), raised rather
than fixed here because building it is not re-running research.

**Closed 2026-08-15 by [T-156](../tasks/T-156-make-the-screening-partition-a-figure-a-checker-can-count.md),
and the paragraph above is kept as the state it closed from.** `tools/docs/screening.py` counts
exactly those rows in exactly those two documents, and prints the three counts, the sentence it
checks, the catalogue size and `0 disagreements`. **`PR-91` guessed the class might be wider than
this one paragraph, and the sweep refused that**: reading both audit registers for a stated gap whose
remedy had since shipped returned §4.1 alone — §10.4 and §10.3's *text a reader follows and no checker
reads* already carry their own closure notes, which is how this one was found missing.

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
| ~~5~~ | **CE-01** | A / F1 | Split the release chronology out of `CLAUDE.md` — **done; 19,035 → 15,416, and the row's own 6,980 was never the saving.** 3,619 bytes were narrative and the rest was fourteen rules that stayed, which is what *the extraction is the work* means once it is counted | ~~`L`~~ **`M`** | `s` | stated | R8 §8 |
| ~~6~~ | **CE-11** | A / F1 | Adopt the tier model and a relation-bound tier 1 — **done, and the file is over the bound the day it was set, so it is written as dated debt** | *enabler* | `s` | none | §6.1 |
| ~~7~~ | **CE-05** | B / F1 | Move `BRIEF.md`'s *Release phases* to its own document — **done; `BRIEF.md` 134,596 → 42,485, and the shape the row proposed was refused with a measurement** | `XL` | `m` | stated | R8 §8 |
| ~~8~~ | **CE-06** | B / F1 | One file per lesson, plus a generated index — **done, and the band was wrong: no bytes were saved.** What it bought was 983 citations a gate now resolves | ~~`XL`~~ **`S`, plus an unbanded gain the row never named** | `m`–`l` | stated | R8 §8 |
| ~~9~~ | **CE-09** | B / F1 | One workflow file per lifecycle phase — **done, and the shape was refused**: §6 was extracted whole and the rest left alone, because everything but §6 is 10,374 bytes together | `L` | `m` | stated | §6.1 |
| ~~10~~ | **CE-04** | A+B / F2 | One operative home per cumulative rule — **done, and the band held: 596 bytes off tier 1 for one rule.** The row undercounted its own homes by one, and the sixth was written the same morning by `CE-01`'s task. **The document that governs the behaviour was the only one not stating it** | `M` | `xs` each | stated | R8 §8 |
| ~~11~~ | **CE-08** | A / F2 | A measured figure gets a durable home — **done, and the shape was refused**: the figure now has no home at all. The decision it drove was coarser than the number, so `PUBLISHING.md` §8 states *minutes, background it* and `check_all.py` prints its own seconds (**L-95**) | `S` | `xs` | none | R8 §8 |
| ~~12~~ | **CE-10** | A / F2 | Prune the memory index of spent entries — **done, and the band held: 6,706 → 5,818, −13.2% of a file loaded on every turn.** Six of the seven entries removed were duplicating `../CLAUDE.md`, so the fact was charged twice per turn | `S` | `xs` | stated | §6.1 |
| ~~13~~ | **CE-12** | B / F3 | ~~Two docstring outliers~~ — **withdrawn 2026-08-14: there are no docstring outliers.** The figures counted triple-quoted string tokens, and in those files the strings are the tools' payloads | ~~`M`~~ **none** | `s` | ~~stated~~ — the stated risk was never reached | §6.1 |
| 14 | **CE-14** | A / F1 | Move the rules that bind only deck or release work under path-scoped rules — about 4,500 of `CLAUDE.md`'s 15,581 bytes, and rule 6 stays. **Still open, and the risk cell was right to name addressability.** `T-288` measured it and closed `not met` without moving anything: the mechanism is real on this harness — one `path_glob_match` in 1,814 logged instruction loads — but a rule file added mid-session does not fire, so no session can take the reading on itself. It also found two things this row does not hold: `.claude/` is untracked in a repository that publishes, and the sibling project declined the same move. `T-295` carries the decision | `L` on tier 1, `M` on the start context | `s` | stated | §6.3 |
| ~~15~~ | **CE-15** | B / F1 | `TOOLING.md` §1 is 18,461 of 26,408 bytes and every pointer to it costs the whole — **done 2026-09-02, and the band is real but conditional in a way this row did not say.** Nothing was deleted, so a session that reads §1 whole still pays all of it. What changed is that no pointer sends it there: fourteen numbered subsections of 262 to 3,440 bytes, and the four live pointers now each name the one rule they meant. The saving belongs to the pointer, not to the file, and a row stating a gain against a file size cannot see that distinction | `M` | `s` | none | §6.3 |
| 16 | **CE-16** | E / F5 | A session boundary re-pays the start context and the read path at the write rate; the session-per-task rhythm buys continuity, not tokens — **a measurement first, because it collides with a settled rhythm** | `L` (estimated) | `m` | stated | §6.3 |
| ~~17~~ | **CE-17** | A / F1 | Sixty skills offered every turn, five of them this repository's; the app's store is outside `CE-07`'s reach — **done 2026-09-02, and the band is unspendable from here.** The counts re-derive exactly — 5 this repository's, 41 others, and 15 built-ins against the row's 14 — but **the row's account of where the 41 live is wrong**: 40 of them are on no disk in this profile, and the one that is sits in `~/.claude/skills`. They are account-level, and this CLI has no settings key to disable a skill by name. So the gain is real and the controller is the account's own interface | `M` on the start context | `xs` | none | §6.3 |
| 18 | **CE-18** | E / F5 | The docs gate is 81% one render — seconds, not tokens | *time* | `s` | stated | §6.3 |
| ~~19~~ | **CE-19** | C / F5 | The deck gate's green default prints 29,980 bytes, up 72%; L-153 was not applied to it — **done 2026-09-02, and the band held with room.** One line: the default now comes from `isatty` rather than from the flag. A piped green run of the reference deck is **327 bytes**, not the 398 the row predicted from `--quiet`, because the deck line and the two notes are all that survive. The self-test asserts all three readings — terminal, pipe, and each flag winning — rather than only the red run it already covered | `M` | `xs` | none | §6.3 |
| ~~20~~ | **CE-20** | A / F2 | Five memory-index entries duplicate a rule with a home — **done 2026-09-02, and the band did not hold: five is two, and 930 bytes is 219.** The row named the right test and was counted by a coarser one. The test is **per facet** — spent means *every* facet superseded or absorbed, and a cross-project facet is neither — and three of the five have one: the publishing entry carries the method, the fleet state and taskmd's no-rewrite ruling; the PowerShell entry carries a failure mode no tier-1 file states; and the trailer entry **is named as a keeper, by id, inside the entry this row cites as its test**. The index is 9,014 → 8,795 bytes, the two spent entries are in `spent/` rather than deleted, and the one inbound link was repointed at the document that now owns the rule ([L-159](lessons/L-159.md)) | `S` | `xs` | none | §6.3 |
| ~~21~~ | **CE-21** | C / F5 | `refcheck.py` and `findings.py` print 446 bytes green inside every lint — **done 2026-09-02, and half of it was already done.** `findings.py --check`'s 62 bytes **are** the one line L-153 asks for, so only `refcheck.py` had a change to make: 384 → 79. A third tool joined the chain the same day and got the rule at once rather than as a later finding — `shipped.py`, `lint.py`'s fifth step. The green lint is 1,737 bytes against the row's 1,976 baseline, and about 1,500 of what remains is taskmd's own advisory account, which is upstream and outside this | `S` | `xs` | none | §6.3 |
| 22 | **CE-22** | D / F3 | Output at five times the input rate was a quarter of the session's weighted spend, and the record forms are the mechanism — **collides with the project's record policy; reported, not tasked** | *bimodal* | — | stated | §6.3 |

**Rows 14 to 22 are the second run's** — [T-287](../tasks/T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md),
2026-09-02, ranked within that run; §6.3 states them and §11 measures them.

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
| **Controller** | `project` - The repository's own files and tools |
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
| **Controller** | `user` - The store belongs to the person running the agent, not to the repository. Actionable today, and no clone inherits the result |
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
| **Controller** | `project` - The repository's own files and tools |
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
| **Controller** | `project` - The repository's own files and tools |
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
| **Controller** | `project` - The repository's own files and tools |
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

**And there is a phase after the last closure.** `R8` §3.1 — the method's phase 2, steps 12–16, added
2026-08-14 — runs **once, after the raised work is implemented**, and this section is the per-closure
half of it rather than a substitute. It pairs every band against what it actually bought, prices what
the remedies cost, feeds the method's own rubric, and writes standing policy into the documents that
already govern. **It is closer than this said.** *Until 2026-08-14 this read "not due here yet: §9's listing still has
open tasks", and that sentence expired the same day —* **every finding in §6 now has a closed task**,
which `python tools/docs/findings.py` reports in 1,317 bytes. **Phase 2 has now run — 2026-08-14, by
[T-153](../tasks/T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md), and §10 is
its report.** It runs once, so this section is the per-closure half of a phase that is finished rather
than a phase that is coming. *Everything from here to the end of this paragraph is the account of what
it was waiting on, kept because it is the argument that set the moment:* what phase 2 still waited on
was not the
ranking but the two repairs to the method itself,
[T-136](../tasks/T-136-re-run-the-external-research-with-a-recorded-search-record.md)
and [T-138](../tasks/T-138-make-the-portable-half-agent-agnostic.md): the first re-runs the external
research with a recorded search record and can still raise a finding, so phase 2 taken before it would
price a ranking that is about to change. **T-136 closed 2026-08-14 and raised none** — §4.1 is the
answer and the argument for it — so **only T-138 is left between here and phase 2.** **The remaining execution order is ordinary backlog and does
not gate it** — that was never the condition, and reading it as one
would park phase 2 behind eighteen tasks it has nothing to do with.

**What a closure owes the record.** The task's §3 and §4, a
[`RELEASE-PHASES.md`](RELEASE-PHASES.md) row folded to two cells (above the PH3 table), the
execution-order table renumbered, `shipped_in` set, **§6's rank cell struck through** — and
`finding: CE-nn` in the task's front matter, which is what makes the rest of this sentence checkable
rather than owed. `python tools/tasks/lint.py` fails the closure that skips either, in both
directions. Also
any figure this document states that your change moved — `CE-09`'s moved because `CE-02`'s fix added
to the very section `CE-09` measures. *The row was written into `BRIEF.md` until 2026-08-14, when
`CE-05` moved that section out; the obligation is unchanged and the file is not.*

---

### 6.3 The second run — what a session accumulates by working

**[T-287](../tasks/T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md), 2026-09-02.** The
rows `CE-14` to `CE-22` in the table above are this run's; §11 is how they were measured and what the
measurement says on its own. The ranks continue the first run's numbering because `findings.py` reads
one table, and they rank within this run only. **Every `Change` cell is a hypothesis** — §10.2's
sentence is the standing verdict on this method's forecasts, and nothing here is exempt from it.

#### CE-14 — Rules that bind only deck or release work are paid on every turn of every session

| | |
| :--- | :--- |
| **Surface / Family** | A / F1 |
| **Finding** | `CLAUDE.md` is 15,581 bytes. Its *rules that must survive* (2,556), *Voice* (540) and *Verifying* (1,568) bind deck work; the humanizer and corpus rules in *Publishing constraints* (part of 3,107) bind a release. About **4,500 bytes, 29%**, bind work that most sessions here never do, and the harness documents a mechanism for exactly this: `.claude/rules/*.md` with `paths:` front matter loads when a matching file is read, not at launch. The repository's tier model calls that tier 3 and does not use it |
| **Change** | Two rule files scoped to the deck trees and to the release documents; the paragraphs deleted at the source. **Rule 6 stays**: a rule that fires when a deck is read cannot forbid reading the deck |
| **Gain** | `L` on tier 1 (about 4,500 of 15,581); `M` on the start context (about 1,100 of 70,788 estimated tokens). Both stated because the second is what a session pays |
| **Effort** | `s` |
| **Risk** | stated — addressability: the desktop harness is not the one the document describes, and what loads is established by observation, never by a document's claim. The task measures first |
| **Applies to** | `this project` |
| **Controller** | `project`, with one `harness` question the task answers first |
| **Source** | this audit; the harness's own documentation for the mechanism |

#### CE-15 — One section of the tooling document is ten rules, and every pointer to it costs all ten

| | |
| :--- | :--- |
| **Surface / Family** | B / F1 |
| **Finding** | `tasks/TOOLING.md` §1 is **18,461 of the file's 26,408 bytes** and holds the gate order, the no-edit rule, `--docs`, the quiet line, the render workers, the bulk-edit rule, `lint.py`, `query.py`, the board question, `refcheck.py` and `findings.py`. The handoff pointed at `§1` for one rule and this session read all of it — 15% of everything the resume read from the project's own homes |
| **Change** | Numbered subsections, one rule each; every `§1` pointer re-pointed |
| **Gain** | `M` on the read path — a resume that needs one rule reads about a tenth of what it reads today |
| **Effort** | `s` |
| **Risk** | `none` — `refcheck.py` resolves `§n` pointers, so a missed one fails the lint |
| **Applies to** | `this project` |
| **Controller** | `project` |
| **Source** | this audit |

#### CE-16 — A session boundary costs about as much as thirty turns of carried context

| | |
| :--- | :--- |
| **Surface / Family** | E / F5 |
| **Finding** | From this session's transcript (§11.2): a new session pays its start context at the cache-write rate — 70,788 tokens, weighted ×2 — and its resume read path the same way, about 25,000 tokens more. That is roughly **190,000 weighted tokens per boundary**. Continuing instead costs the carried context at the read rate: at 140,000 tokens, about 14,000 weighted per turn, and about 7,000 more per turn than a fresh session would pay. **A restart pays back after about 27 turns at the smaller context.** The per-task rhythm — one session, one handoff, one task — pays a boundary per task, and B17 paid three |
| **Change** | **A hypothesis with a collision.** Continue across a batch's tasks, compact between them, hand off at the batch. It collides with `REMEDIATION-ORDER.md` §4's rhythm, `AUDIT-METHOD.md`'s cycle-as-session-boundary, and the owner's handoff discipline — the ecoctx method's fourth refusal applies, so the child task measures one batch both ways and the owner decides |
| **Gain** | `L` on a batch's total spend — **estimated from one session, with the weights stated once in §11.2** |
| **Effort** | `m` — the measurement, not the change |
| **Risk** | stated — what a compaction loses is a re-read later, and it is counted against the compaction in the task |
| **Applies to** | `this project` |
| **Controller** | `user` |
| **Source** | this audit; the harness's cost page for the cache mechanics |

#### CE-17 — Sixty skills are offered on every turn and five of them are this repository's

| | |
| :--- | :--- |
| **Surface / Family** | A / F1 |
| **Finding** | The catalogue this session received: **60 skills, 15,024 bytes of name and description, about 3,800 estimated tokens per turn**, 5.3% of the start context. Five serve this repository; 41 are installed by the desktop app in the user's roaming profile and 14 are the harness's built-ins. `CE-07` scoped the `~/.claude` plugins per project and reached none of these |
| **Change** | Find whether the app's store scopes or disables per skill; disable what no project on the machine uses; record the boundary where it cannot |
| **Gain** | `M` on the start context |
| **Effort** | `xs` |
| **Risk** | `none` |
| **Applies to** | `this project`'s sessions |
| **Controller** | `user` — the change lands outside the repository and no clone inherits it |
| **Source** | this audit |

**Re-measured 2026-09-02 by [T-291](../tasks/T-291-measure-whether-the-desktop-apps-skill-catalogue-can-be-scoped-per-project.md), and the counts held while the mechanism did not.** The catalogue arrived as **61** entries, not
60: 5 this repository's, 15 harness built-ins where the row says 14, and the same **41** in
between. *Installed by the desktop app in the user's roaming profile* is the half that fails —
searching the whole user profile finds a directory for exactly **one** of the 41, in
`~/.claude/skills`, and none for the rest at any depth. They are delivered with the account, and
`ListSkills` reports each with its own `enabled` flag, so per-skill scoping **exists** and is the
account interface's. **Nothing on this machine can reach it**: the CLI binary carries
`enabledPlugins` and `disabledMcpjsonServers` and knows none of `disabledSkills`,
`enabledSkills`, `allowedSkills`, `deniedSkills` or `skillSettings`. The byte figure is left at
the row's own measurement rather than restated — re-deriving it means transcribing the
catalogue, which is the thing being measured.

#### CE-18 — The documents gate is four fifths one render

| | |
| :--- | :--- |
| **Surface / Family** | E / F5 |
| **Finding** | `check_all.py --docs` spent **22.5 of 27.6 s** (81.4%) in `figures.py`, which resolves the README's coverage account by running `check.py` on the reference deck. `T-285` §3 measured the same thing as 37.6 of 45 s an hour earlier on a slower machine and named it for this audit |
| **Change** | Bind the account to what `check.py` reads rather than to a render, or skip that one binding under `--docs` with a printed reason. **L-152 bounds the hypothesis**: bound or deleted, never refreshed, so a cached figure is not a candidate |
| **Gain** | none in tokens — the run prints one line either way; about 22 s per documentation commit |
| **Effort** | `s` |
| **Risk** | stated — a binding that stops being live |
| **Applies to** | `this project` |
| **Controller** | `project` |
| **Source** | `T-285` §3, confirmed here |

**The mechanism is refuted, and the finding stands. Measured 2026-09-02 by [T-292](../tasks/T-292-the-docs-gate-is-four-fifths-one-render.md):**
the coverage account is **not** what runs `check.py`. Empty `ACCOUNTS` and the run still
happens, because [`../README.md`](../README.md) pastes that command's output in a fence and
`figures.py` compares the paste against a live one — the account is a second reader of a run
that happens anyway. So both changes this row proposes save **nothing**, and rebinding the
account would trade a live binding for a weaker one to buy no seconds. `figures.py` alone is
**33.2 s**, of which `check.py` is **28.7 s** and the five other commands 4 s together. The
remedy the measurement points at is a different one, and it removes a guarantee from the front
page rather than moving a binding: [T-296](../tasks/T-296-the-readmes-deck-gate-fence-is-what-the-docs-gate-pays-for.md).

#### CE-19 — The deck gate's green default grew 72% and L-153 was not applied to it

| | |
| :--- | :--- |
| **Surface / Family** | C / F5 |
| **Finding** | `check.py` on the reference deck prints **29,980 bytes** green by default, against 17,391 on 2026-08-13 and **398** under `--quiet`. `T-286` gave four document tools the rule that quiet is the non-terminal default; the tool that prints most still needs the flag remembered, and `build.md` remembers it in one place |
| **Change** | `quiet_wanted` as in the four tools; the self-test already asserts a red run is never swallowed |
| **Gain** | `M` on surface C for any session that runs the gate by hand without the flag; `S` where `build.md` is followed |
| **Effort** | `xs` |
| **Risk** | `none` |
| **Applies to** | `this project` |
| **Controller** | `project` |
| **Source** | this audit |

#### CE-20 — Five memory-index entries duplicate a rule that has a home

| | |
| :--- | :--- |
| **Surface / Family** | A / F2 |
| **Finding** | The index is 47 entries, 9,014 bytes, mean 186 per line, under the harness's 200-line / 25 KB load limit. Five entries restate a rule that `CLAUDE.md` or the owner's global preferences already state: the publishing identity, the trailer rule, the cross-repository rule, the PowerShell command rule, the incoming-labels rule — about **930 bytes**, paid every turn twice over. `CE-10`'s mechanism, recurring: the memory was written before the rule got its home |
| **Change** | Prune at the next consolidate pass; the *memory with a repository home is spent* entry is the test |
| **Gain** | `S` |
| **Effort** | `xs` |
| **Risk** | `none` |
| **Applies to** | `this project`'s sessions |
| **Controller** | `user` |
| **Source** | this audit |

#### CE-21 — Two document tools still print their green account inside every lint

| | |
| :--- | :--- |
| **Surface / Family** | C / F5 |
| **Finding** | `refcheck.py` prints 384 bytes and `findings.py --check` 62 on a green run, inside `lint.py`'s 1,976. `T-286` §3 named both for this audit |
| **Change** | L-153's one line |
| **Gain** | `S` |
| **Effort** | `xs` |
| **Risk** | `none` |
| **Applies to** | `this project` |
| **Controller** | `project` |
| **Source** | `T-286` §3 |

#### CE-22 — The session's own writing is a quarter of what it pays, and the record forms are why

| | |
| :--- | :--- |
| **Surface / Family** | D / F3 |
| **Finding** | Output tokens weigh five times an input token. At the fourteenth call this session had written 22,020 of them — **25% of its weighted spend**, more than the whole carried context. The forms are the mechanism: a task's §3 runs 3–4 KB of decisions, a register row 2,186 bytes on average over 159 rows, a lesson 1.5–2 KB, a handoff 6–7 KB — and every one of them is read again by the next session as surface B |
| **Change** | **None proposed here.** The forms are the project's settled policy — records are the durable homes, L-153's own argument that a report is read forever by an agent applies to them, and the F3 test is *does it decide anything future*, which most of a decisions section does. Reported for the owner as the ecoctx method's fourth refusal requires; the one lever that does not collide is the resume side: read the section a pointer names and not the file |
| **Gain** | *bimodal* — bytes not written now against bytes not read later, and a decision not recorded against a decision re-litigated |
| **Effort** | — |
| **Risk** | stated — a shorter record costs a fact its only home |
| **Applies to** | `this project` |
| **Controller** | `project` — and the owner's, since it is policy |
| **Source** | this audit |


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

**Two of the three were sent on 2026-08-14; the third has no route and says so.** *The route, ruled by
the owner that day:* one issue on the receiving project's own repository —
[`uchimata2/handoff-skill#75`](https://github.com/uchimata2/handoff-skill/issues/75) and
[`uchimata2/taskmd#1`](https://github.com/uchimata2/taskmd/issues/1). It was chosen over committing a
file into each receiving repository and over a direct handover with no outward act, on one property:
*what came back* needs somewhere to land, and only a thread has one. **The response is recorded as
handed over rather than waited for** — a reply is the receiving project's business, so the sending
completed here instead of parking on an answer.
[`upstream/harness.md`](upstream/harness.md) was **not** sent: its owner is a vendor, no channel was
found that accepts an observation carrying no priority, and the document records that, plus what would
change it. Each document carries its own handover record; this paragraph is the summary, not the
register.

**The route is retired for anything found after 2026-08-15, and the register with it.** Ruled by the
owner that day, on the cost of the one thread that ran to completion: **34 KB of issue comments here
and upstream, and 111 KB of task records in this repository, for four local tasks of which none
changed a line of behaviour.** Three of the four were prose about prose — deliver the register,
correct the register, correct the correction. What replaces it, for every project the owner holds:
**a defect found in one of their repositories is fixed in that repository, as a branch with a failing
test and a three-line pull request**, because all of them are cloned side by side on the owner's
machine and a diff describes itself. A finding is reported rather than fixed only when it breaks a
gate or destroys data; a claim about another tool's behaviour travels with the command that proves it,
which is the same command that usually produces the fix; and a report gets **one** reply, with a
correction as a one-line comment rather than a section. **The operative statement is the owner's
global working preferences, which are machine-local and outside this clone** — this paragraph is this
repository's copy of the ruling, not a second authority, and the practice binds every project rather
than this one (**L-13** applies to the rule as much as to the rows). Raised and implemented by
[T-164](../tasks/T-164-retire-the-cross-repo-register-in-favour-of-a-branch.md).

**What the two sent registers become.** History, not a live practice. Their rows were delivered, their
threads answered, and the documents stay exactly as they are — the correction record they promised is
still owed on the terms they were sent under. `O-T4`'s value is the reason the retirement is not a
verdict that the exchange was worthless: it found a defect that had silently destroyed a task record
for six days. **The rule is not stop reporting; it is report by patch, prove behaviour by running it,
and cap the prose.**

*The hold, ruled by the owner 2026-08-13 and now spent:* nothing was to go until the audit's findings
were worked and their fixes landed, because the documents were **a register still filling** rather
than a report waiting on a courier — every finding still to be implemented was a session that might
add rows, and four out of four implementations did. Sending early would have meant sending three
times. **The registers stopped filling on 2026-08-14**: phase 2 closed and added no rows to any of the
three, which is that argument coming good rather than a lucky outcome — it held that a review of what
the findings actually bought is the session most likely to add rows.
[T-157](../tasks/T-157-hand-the-upstream-registers-to-their-owners.md) was the sending act.

**A send transforms the document, so diff the whole delivered artifact against the source and account
for every difference.** Added 2026-08-15 by
[T-160](../tasks/T-160-correct-the-three-errors-the-recipients-found-in-the-delivered-registers.md),
which is what the first send cost. A register is written for here and delivered elsewhere, so it needs
changing on the way out — links absolute, the sender-facing banner replaced — and **the transformation
is broader than its intent every time it is written narrowly.** The first one matched every blockquote
instead of the first and destroyed a quotation. The check that missed it compared the observation rows
byte for byte, which was the thing feared and not the thing changed: **L-102**. Three expected
differences and one unexplained is a fifteen-line diff, and it is the whole guard.

**A session that finds something still adds it to the owner's document and stops there.** Sending
ended the wait, not the filling. **A row added after a document's handover date is unsent, and nothing
needs to mark it so** — the record carries a date, the row carries a position, and the two answer the
question between them. Do not open a second thread and do not chase the first; a register that has
been sent once can be sent again, by the same one deliberate act, when there is enough to justify it.

*What is spent, kept in one line so the argument is findable and does not have to be re-run:* the
2026-08-13 hold set a condition and no moment; the owner set the moment on 2026-08-14 — after phase 2,
before [T-137](../tasks/T-137-package-the-context-economy-method-as-a-skill.md) — with phase 2
deliberately **inside** the hold, because
[T-153](../tasks/T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md) reviews the
method against what it bought and is therefore the session most likely to add rows. The act was given a
task file because a scheduled act has nowhere to record who was told, by what route, and what came
back — **the rows were the input and the responses were homeless.** All of it happened.

### 7.1 The handoff skill

**[`upstream/handoff-skill.md`](upstream/handoff-skill.md)** — `O-H1` to `O-H7`. Backlog read for the
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
| **BP-2** | `.handoff/` (gitignored) | Five successive handoffs carried "the release gate takes 7–11 minutes"; measured 154 seconds. **Nothing tracked in the repository states a run time**, so no committed document is wrong — the figure had no durable home at all, which is CE-08. **Closed 2026-08-14 by [T-148](../tasks/T-148-give-a-measured-figure-a-durable-home.md), and it still states none**: the run measured 164 s that day, the command prints its own seconds now, and `PUBLISHING.md` §8 carries the decision instead of the number (**L-95**). The 6% between two real readings against the 300% the carried figure was wrong by is the whole argument |
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
task.** [`../tasks/TOOLING.md`](../tasks/TOOLING.md) §1.12 excuses the `DUPLICATE INDEX` advisory *by file name* — it was `tasks/TASK-WORKFLOW.md` §6 until T-147 moved it — and the
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

**Phase 2 is done — 2026-08-14, and §10 is its report.** *The rest of this section is the record of
how it came to be scheduled, kept because the reasoning outlived the wait.* It closed with seven
acceptance criteria met and one `not met`, which is
[T-158](../tasks/T-158-measure-the-tier-1-bound-instead-of-remembering-it.md).

**This repository owes itself a phase 2, and the listing emptied on 2026-08-14.** The method gained
one that day (`R8` §3.1) and it runs after the raised work is implemented. **All thirteen findings now
have closed tasks** — T-148, T-149 and T-152 closed in the same session, and
`python tools/docs/findings.py` is what says so rather than a count kept here.

*This paragraph said phase 2 waited on "the open tasks in the execution order" and would "sit blocked
behind six". Both figures are spent, and the first was too wide:* the execution order holds ordinary
backlog that has nothing to do with the audit. **What phase 2 actually waits on is
[T-136](../tasks/T-136-re-run-the-external-research-with-a-recorded-search-record.md)
and [T-138](../tasks/T-138-make-the-portable-half-agent-agnostic.md)** — the two repairs to `R8`, one
of which can still raise a finding. It is blocked behind **two**, both `next` or adjacent to it.
**Raised the same day as [T-153](../tasks/T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md)**,
at the owner's direction, on the argument that raised T-152 the day before: a remainder nothing
schedules is a remainder that depends on this paragraph being re-read. It carries the two `blocked_by`
edges, so it sorts last and changes nothing about what to work on next.

**CE-10 stands as not repository work** — pruning the memory index is the owner's memory, and is
named here so it is not mistaken for a task.

**Both of the owner's 2026-08-14 additions closed the same day, and neither cost what the row said.**
T-143 cut `CE-01` and T-144 cut `CE-04`, taking `../CLAUDE.md` from **19,035 to 14,821 bytes, −22.1%**
— 57% of the debt the bound reports, and it is still over. `CE-01`'s 6,980 was never available: 3,619
of it was narrative and the rest was rules that had to stay in tier 1, which prices *the extraction is
the work* for the first time. `CE-04`'s band held, and the row undercounted its own homes by one —
**the sixth copy was written the same morning by `CE-01`'s task**, in the pass raised to remove
copies, which is the finding's mechanism rather than anyone's oversight. Both went to
[T-137](../tasks/T-137-package-the-context-economy-method-as-a-skill.md) §1 as a fourth table.

**`CE-04` has a second task against it after closing, and that is the band working rather than a
reopening.** Its band is `xs` **per rule** and T-144 took one rule, so the finding closes while the
work does not: [T-152](../tasks/T-152-give-look-at-the-rendered-deck-one-operative-home.md) carries
*look at the rendered deck*, raised 2026-08-14 rather than left as a remainder inside a closed task.
**A per-item band is the one shape where a closed row is not a finished subject** — worth reading as
a rule for the ranking. *This said nothing in the table marked per-item bands, and that was wrong:
`CE-04`'s Effort cell has read `xs` **each** since the row was written. The marker was there and
nothing read it.* `tools/docs/findings.py` reads it now, and a closed row with open work is a failure
for every finding whose band is not per item ([T-151](../tasks/T-151-generate-the-finding-to-task-listing-instead-of-keeping-it-by-hand.md)).

**What the pair changed about the enabler.** `CE-11`'s bound compares tier 1 against a set that was
never written down, and the omission matters in one direction: a document split out of tier 1 is
smaller than tier 1, so counting tier 3 would ratchet the bound down with every remedy it prompts and
**no split could ever satisfy it**. The set is now stated as tier 2 in `../CLAUDE.md`, which is what
`RELEASE-PHASES.md`'s exclusion had always assumed.

---

## 10. Phase 2 — what the ranking was worth

`R8` §3.1 steps 12 and 13, run once on 2026-08-14 after the last raised task closed, by
[T-153](../tasks/T-153-run-the-audit-methods-phase-2-over-this-repositorys-own-audit.md). **This
section grades the audit above it. It raises nothing** — `CE-nn` closed at thirteen, and anything
found here is an ordinary task. What the *method* learned is in `R8`; what this repository learned is
here.

Read from §3 and §4 of the fourteen closed records — **80,721 bytes, not the 210,783 those records
are whole.** `python tools/docs/findings.py` supplies each band and outcome; the *bought* column is
the part no tool holds.

### 10.1 Every finding, predicted against measured

Bands are as ranked. Where a band was corrected before implementation, both values are shown, because
a correction that erases its predecessor teaches the next audit nothing.

| Finding | Band | What it measurably bought | Verdict |
| :--- | :--- | :--- | :--- |
| `CE-03` | L / xs | green run **17,581 → 345 bytes, 51×**; the failing path byte-identical at 18,253 | **held** |
| `CE-10` | S / xs | memory index **6,706 → 5,818, −888 bytes, −13.2%**, 38 → 32 entries, paid every turn | **held** |
| `CE-02` | L / xs | `list --open --limit 1` — the literal *what next* — **94 bytes against a 36,559-byte board, 389×** | **understated ~22×.** The row compared the whole board against a full listing, 17.7×. No session asks that question |
| `CE-01` | M / s | `CLAUDE.md` **19,035 → 15,416, −3,619, −19.0%** | **48% short.** The row measured the chronology at 6,980 bytes; 3,619 was narrative and the rest was rules that had to stay. *The extraction is the work*, priced |
| `CE-07` | ~~L~~ → S / xs | skill listing **7.3k → 6.5k, −800 tokens, once**; deferred MCP schemas unmoved at 50.4k through two restarts | **band corrected during implementation.** `L` assumed the whole block was addressable; what is reachable *from a repository* is `S` |
| `CE-06` | S / m–l | **not a byte.** 167,043 in one file became 169,361 in 89 plus a 12,258-byte index | **the 81× was never claimed** — it assumed a whole-file read nothing here performs. What was bought is a one-call fetch, a question that could not be asked, and 983 citations a gate now resolves |
| `CE-05` | XL / m | `BRIEF.md` **134,596 → 42,485**; 92,894 bytes moved, none saved | **shape refused on a measurement.** The row proposed extracting only completed rows; PH3 is 52,894 of the section and gains one per closure, so that cuts 40,000 once and rebuilds the finding on a timer |
| `CE-09` | L / m | `TASK-WORKFLOW.md` **23,210 → 11,407**; 12,829 bytes moved, none saved. `TOOLING.md` is **15,281 — larger than the section it received** | **shape refused on a measurement.** Four files, one per phase, would give a session at `plan` several small files instead of one already small: everything but §6 is 10,374 bytes together |
| `CE-08` | S / xs | the gate measured at **164 s** against a carried *7–11 minutes* — **300% wrong**, while two real readings differ by 6% | **band held, shape refused.** The row said *give the figure a home*; the work ensured **no document holds it** |
| `CE-04` | M / xs **each** | `CLAUDE.md` **15,416 → 14,917** (T-144), then **15,182 → 15,034** (T-152); five operative statements to two, then three to one | **held, and undercounted its own subject.** Six homes, not five — **the sixth was written the same morning by `CE-01`'s task**, in the pass raised to remove copies |
| `CE-11` | enabler / s | `CLAUDE.md` **15,952 → 18,642, +2,690 bytes** on tier 1; over its own new bound by 4,555 on the day it was set | **a cost, correctly predicted as an enabler.** It priced itself in its own record |
| `CE-13` | bimodal / xs | `CLAUDE.md` **15,630 → 15,952, +322 bytes, +4 lines** on tier 1 | **a cost, and the trade was argued rather than absorbed**: paid every turn against one session saved once |
| `CE-12` | none / s | nothing, and the premise was false | **withdrawn, and that is a result.** The instrument counted triple-quoted **tokens**, not docstrings: 85% → **3.2%**, 36% → 11.6%, 30% → **16.3%** — wrong by up to 27× |

**Two of thirteen held as written.** Four were wrong about magnitude, three about shape, one about its
premise, two were costs by design, and one undercounted the subject it was measuring. **This is the
single most useful table the audit produced**, and none of it was available at ranking time.

### 10.2 The one sentence the pattern reduces to

**A finding says where the weight is. It does not know what removing it is worth.** T-147 wrote that
after `CE-05`, `CE-06` and `CE-09` each had a shape refused in three consecutive tasks, and it holds
across all thirteen: every row that was wrong was wrong about the *value or form of the remedy*, never
about the location of the cost. The audit's inventory was sound. Its forecasting was not, and it was
not close.

**The corollary, which is why this is not a complaint about estimating.** Four rows were refused by
the measurement taken *while implementing them* — `CE-12`'s premise, `CE-05`'s and `CE-09`'s shapes,
`CE-08`'s direction. A ranking that had been believed rather than re-measured would have deleted two
tools' payloads (`CE-12`), rebuilt `CE-05` on a timer, and split one small document into four smaller
ones. **The rank was useful; obeying it would have done damage.**

### 10.3 What the remedies cost

**The load path ended 2.7% smaller than the audit found it, after a peak 21.8% above it.**

| `CLAUDE.md` | Bytes | |
| :--- | ---: | :--- |
| At the audit, 2026-08-13 | 15,630 | what `CE-01`, `CE-04`, `CE-11` and `CE-13` were ranked against |
| Peak, before `CE-01`'s task | 19,035 | `CE-11` +2,690 and `CE-13` +322 are 3,012 of the 3,405 |
| After `CE-01` and `CE-04` | 14,917 | −4,118, −21.6%, closing 57% of the debt |
| **Now, 2026-08-14** | **15,208** | later edits added back |
| **Net across the whole audit** | **−422** | **−2.7%** |

**The audit's own remedies are most of the growth it then had to cut.** `CE-11` wrote the tier model
into the file it governs — 2,690 bytes onto the surface being measured — and `CE-13` added 322 more.
That is `R8` step 16's warning, *an audit that closes by writing governance into the file it just cut
has undone itself*, committed by this audit **before step 16 existed to name it**. Both records priced
it honestly at the time, which is the only reason it is legible now.

**Every structural remedy grew the repository.** The load path is what shrank.

| Remedy | Off the load path | Onto disk |
| :--- | ---: | :--- |
| `CE-01` | −3,619 | `RELEASE-HISTORY.md`, **10,012** — new |
| `CE-04` | −499, then −148 | `PUBLISHING.md` +945, `TASK-WORKFLOW.md` +172, then +346 more |
| `CE-05` | −92,111 from `BRIEF.md` | `RELEASE-PHASES.md`, **116,655** — new, and it gains a row per closure |
| `CE-06` | 0 | `docs/lessons/` **197,557** over 99 files, plus a **13,669** index, from 167,043 in one |
| `CE-09` | −11,803 | `TOOLING.md`, **15,281** — new, and larger than what it received |

**Three remedies left a gate that runs on every release** — `query.py` (`CE-02`), `--quiet`
(`CE-03`), `lessons.py` (`CE-06`) — plus elapsed-time reporting (`CE-08`). None is free. `lessons.py`
is the one that pays for itself: it found a defect class **invisible to every gate in the repository**
before it existed, and caught an unallocated citation quoted into its own task record hours later.

**A withdrawal is not free either.** `CE-12` saved nothing and cost three throwaway instruments, five
corrections in this document, one in T-130 §3, one in `R8` §4.1, plus `L-92` and a note in T-137. It
was **rank 13 of 13 — the cheapest row to have got wrong, and the last anyone would have re-measured.**

**One remedy manufactured work of another family, and it did so inside the pass raised to prevent
it.** `CE-01`'s task wrote a sixth copy of `CE-04`'s rule into `RELEASE-HISTORY.md` while moving the
chronology — an `F2` duplicate created by the sibling task, hours before the survey that caught it.
Nobody acted incorrectly; **a rule with no declared home is copied by whoever needs it next** is the
mechanism, and this is it operating on the audit's own remedies.

**What no row forecast, and no row could have.** Eight defects surfaced in passing, none of them token
economy: a version comparison sorting `0.10.0` below `0.5.0`; five permission rules naming a rotated
server id and matching nothing; three dangling links in the memory store, one a typo for an entry that
exists; dangling `L-nn` citations, unseen by anything; link **labels** that state a wrong path beside
a working target; bare `§n` cross-references left behind by an extraction; a survey that missed a copy
in the very file being cut; and an untracked new tool reported as `STALE`. **Six of the eight are the
same shape — text a reader follows and no checker reads.**

*Worked as [T-159](../tasks/T-159-gate-the-text-a-reader-follows-and-no-checker-reads.md), closed
2026-08-17, and **one of the six turned out to be arithmetic**: a link label naming a file the link
does not open is now `refcheck.py`'s check 4. One was already gated by `lessons.py` by the time the
classification reached it, three are irreducibly a reader's, and the sixth is refused on a
measurement — the obvious rule would fire 1,195 times to catch three instances
([`../tasks/TOOLING.md`](../tasks/TOOLING.md) §2.1). The sentence above still stands as what phase 2
found; what it could not say is how much of the class a checker can take, and the answer is one
sixth.*

*One figure to reconcile rather than repeat: §9 states the pair took `CLAUDE.md` to **14,821**, and
T-144's own record measures **14,917** the same day. 96 bytes apart, both dated, neither reproducible
now. Recorded as a disagreement rather than resolved — which is what `L-97` asks for.*

### 10.4 Standing policy — one rule, and it collides

`R8` §3.1 step 16. **Almost everything this run learned belongs to the method, not to this project**,
and it went to `R8` §3, §5, §6 and §6.3 rather than here. That is the step working: an audit is a
guest, and a guest that leaves ten new house rules has misread what it was for.

**One policy is local, and it is the smallest one imaginable: the tier-1 bound should be measured by
something, not remembered by someone.**

- **Governing document:** [`../CLAUDE.md`](../CLAUDE.md), *What loads every turn* — it states both
  figures, carries the command that produces them, and already rules that they are re-measured
  together.
- **Verdict: extends.** It does not change the bound, the comparison set, or which document owns the
  number. It makes the existing *re-measure both, never one* enforced instead of remembered.
- **Price on the load path: it must be zero**, which is what makes this hard rather than obvious.

**The evidence that it is needed is in this document.** §10.3 measures tier 1 at **15,208** against a
figure that was **15,034** when T-152 closed — 174 bytes of drift that nothing reported. `CLAUDE.md`'s
own debt statement says it *has now been wrong in both terms twice*. And `tools/docs/figures.py`
reports the two figures as **unanchored** — *in a sentence naming no field*, among 413 others. **The
one number in this repository that governs what every session pays is checked by nobody**, which is
`CE-08`'s finding — a measured figure with no owner drifts — reappearing on the audit's own governance
rule.

**The collision, reported rather than resolved.** The mechanism that would catch it is `figures.py`,
which compares a stated figure against **pasted command output** in the same document. Two ways to
get there, and each breaks a rule this project has already settled:

| Route | What it breaks |
| :--- | :--- |
| Paste the command's output into `CLAUDE.md` | `R8` step 16's own second constraint — **an audit that closes by writing governance into the file it just cut has undone itself.** The paste lands on surface A, paid every turn, in the file `CE-01` and `CE-04` were raised to shrink |
| Move the two figures to a document that can be gated | `CLAUDE.md`'s explicit ruling: *a figure about this file cannot be corrected anywhere else* — written after a session recorded the pair in a task record instead, which is how the statement came to be wrong twice |

**Both rules are the project's own and both are right.** Step 16 says the project's rule stands and
the collision goes to the owner, so it does — this section is the report, and the third route
(`figures.py` learns to run a command from a document that pastes no output) is a change to a tool
rather than a policy, which is a task and not a ruling.

**What phase 2 therefore leaves that re-measures without being asked: nothing yet, and that is
recorded rather than papered over.** *Review this annually* is the failure mode step 16 names by name,
and a policy nobody can implement without the owner picking a side is not better. The obligation is
open and it is one decision wide.

**Closed 2026-08-15 by [T-158](../tasks/T-158-measure-the-tier-1-bound-instead-of-remembering-it.md),
and the paragraph above is kept as the state it closed from.** The owner took the third route on
2026-08-14 — neither settled rule yields — so `figures.py` learned to run a fenced command that pastes
no output and hold the page to it. Both figures are now compared on every run of `check_all.py`, at a
cost to `CLAUDE.md` of **zero bytes**: the page already carried the command.

**One thing the collision hid, found only by implementing it.** The mechanism could not simply be
pointed at this page. `figures.py` binds a figure by making its sentence name the label a command
printed, and against a document that keeps its own corrections that rule leaves the first term
unwatched *and* reports the record sentence beside it as stale — one silence and one false alarm, on
the two sentences the page is most careful about. The comparison had to invert: **every measured term
must be written**, rather than every written numeral measured. That is **L-104**, and it is the part of
this section that generalises beyond the one number.

---

## 11. The second run — what a session accumulates by working

**[T-287](../tasks/T-287-audit-what-a-session-pays-per-turn-and-why-it-grows.md), measured
2026-09-02 on the working tree at `807d2db`**, the commit that landed `T-285` and `T-286`, so the
gate figures below are after those two cuts and count their saving once. The findings are `CE-14` to
`CE-22` in §6's table and §6.3. **Inventory figures here are measurements; every gain in §6.3 is a
band.** The conversion is the one §0 states, bytes ÷ 4, labelled an estimate.

| | |
| :--- | :--- |
| **Representative unit** | the resume of this session itself — a handoff read to its first edit — and B17's three tasks plus this one for write volume; chosen before the measurement, as the method requires |
| **Instruments** | three throwaway scripts outside the repository: sizes off the filesystem; every gate run in sequence on the frozen tree with its output captured to a file and the file measured; and the harness's own transcript of this session, read for the token fields of every API call |
| **Grade C, decided** | the transcript is **an instrument for the session it reads and nothing wider**, and every figure it yields says so — the task's first open question, its recommendation adopted |
| **Weights, stated once** | an input token 1; a cache read 0.1; a cache write 2; an output token 5 — the harness's `explain-usage` skill's, applied uniformly. *Weighted* below always means these |

### 11.1 The inventories

**A — the load path.** The first API call of this session carried **70,788 tokens** before any work:
39,315 read from a cache shared with other sessions — the system prompt and the tool schemas, the
harness's — and 31,471 written fresh for this session. Of the fresh part, the repository's tier 1 is
**30,084 bytes, about 7,500 tokens**: `CLAUDE.md` 15,581, the owner's global preferences 5,489, the
memory index 9,014. The skill catalogue is 15,024 bytes, about 3,800 tokens (`CE-17`). The remaining
20,000 or so are environment, git state, the invoked skill's text and the harness's own reminders,
and cannot be decomposed from outside the harness. **So the repository controls about a tenth of the
start context, and every further tier-1 cut has that tenth as its ceiling.** This is a result rather
than a finding: it says what the first run's remedies were bounded by while they were being banded.

**B — the read path.** This resume opened sixteen files and read **123,684 of their 306,038 bytes**
before its first edit, about 30,900 estimated tokens. By owner: the handoff skill's own spine, flow
and config 35,311 (28.5%); the audit method's skill and first reference 17,443 (14.1%); the project's
homes 70,930 (57.4%), of which `TOOLING.md` §1 was 18,461 (`CE-15`), the register's §0–§2 and §6
14,748, the task 8,014, `AUDIT-METHOD.md` 6,438, the handoff 6,197. The harness capped one result —
the 26,526-byte spine arrived as a 2 KB preview and a file — so what entered was nearer 99,000 bytes,
and the transcript agrees: the context grew from 70,788 to 97,762 tokens across the eight calls that
did the reading.

**C — tool output on a green run**, the frozen tree, in sequence, stdout and stderr together.

| Command | Bytes | Seconds | Note |
| :--- | ---: | ---: | :--- |
| `python tools/tasks/lint.py` | 1,976 | 4.1 | `T-286` measured 1,969; the difference is a date |
| `python tools/check_all.py` | **89** | 226 | 8,233 on 2026-08-13; the full gate, one line |
| `python tools/check_all.py --docs` | 129 | 27.7 | 7 ran, 35 skipped with a reason |
| `python tools/check_all.py --docs --report` | 27,537 | 27.8 | `figures.py` 22.5 s of it (`CE-18`) |
| `python tools/docs/figures.py` / `--report` | 131 / 3,547 | 21.6 | |
| `python tools/docs/refcheck.py` | 384 | 2.0 | `CE-21` |
| `python tools/docs/findings.py --check` / bare | 62 / 1,332 | 0.1 | `CE-21` |
| `python tools/docs/chronology.py` | 94 | 0.1 | |
| `python tools/docs/cycles.py` | 5,931 | 0.1 | **exit 1** while `T-284` is open; not a gate |
| `python tools/tasks/query.py list --open` / `context T-287` | 1,909 / 876 | 0.2 | 18 open tasks |
| `python tools/deck/check.py examples/reference-deck.html` / `--quiet` | **29,980** / 398 | 18.7 | 17,391 on 2026-08-13 (`CE-19`) |
| `python tools/examples/seed_defects.py --check` | 1,200 | 0.1 | |

**`T-286`'s prediction held on every tool it touched**: the four green runs that printed 74 KB across
B17 print 89, 129, 131 and 94 bytes now. The full gate took 226 s on this machine against 211 and
332 s in the previous session, which is the machine and not the tree.

**D — write volume.** Nine commits since 2026-08-31 carried 4,920 bytes of message and +1,680 / −292
lines; the most-churned files were `check_all.py` (372 lines) and `chronology.py` (311). B17's task
files closed at 9,763, 9,740 and 11,908 bytes; `T-285` and `T-286` at 12,948 and 11,473; this task
opened at 8,014. Three handoffs in two days: 6,170, 7,367 and 6,197 bytes. The board is 70,662 bytes
over 287 tasks, median 11,721; the pre-release register is 353,983 bytes, 288,021 of it §3's 159 rows
at a mean of 2,186; all markdown in the tree is 651 files and 7.1 MB. **The first run's negative
result stands**: closed records cost nothing until cited. What this surface costs is `CE-22`.

**E — workflow.** The gate split is right and now quiet; the docs mode is one render (`CE-18`); the
session rhythm is `CE-16`; and the harness offers three mechanisms this project does not use — path-
scoped rules (`CE-14`), subagents for read-heavy work, and a `PostToolUse` hook that rewrites a
tool's output before it enters context. The last two are screened in §11.3.

### 11.2 Why it grows — the per-turn model, from one transcript

Fourteen API calls into this session the context stood at 137,904 tokens. Summed over those calls:
1,095 input, 98,507 cache-written, 1,288,603 cache-read, 22,020 output. Weighted: **fresh content
198,109 (45%), the session's own output 110,100 (25%), carried context 128,860 (30%)**, 437,069 in
all. The per-call growth was between 1,063 and 13,341 tokens, and the two largest steps were a batch
of four document reads and one fetched documentation page.

**Every token that enters the context at call *t* of an *N*-call session is paid about 2 + 0.1 × (N − t)
times its size.** Written at 2 once, read at 0.1 on every later call. So the bytes that enter
earliest cost most: at forty calls, a read at call 5 costs 5.5 times its size and one at call 35
costs 2.5. **The resume read path compounds like tier 1 for the rest of the session**, which is why a
30,000-token resume is the dearest thing a session does after its own writing, and why `CE-15`'s
read-path saving is banded on what a session pays and not on file size. The carried term overtakes
the fresh term once the context exceeds about twenty times what a call adds — for this session, at
about the fourteenth call. **A cache miss** — an hour idle on a subscription, a plugin toggled, a tool
list rebuilt — re-writes the whole context at 2, which at 130,000 tokens costs what twenty calls of
carrying it cost. The *exponential* the owner felt is a quadratic: per-call cost is linear in the
context, and the sum over a session is not.

**What the instrument cannot say**: it reads one session, it attributes a call's fresh tokens to the
tool results before it in proportion to their size, and it does not see thinking separately from
output. A first version counted each API call once per content block and reported 36 calls for 14;
the dedup is by message id, and the figures above are after it.

### 11.3 The catalogue, second pass — search record and screening

**Three axes, as the method names them, thirteen searches and three page fetches.** Axis **A**
(ideas): rounds of four, one and one searches; the third added nothing the first two had not, so A
stopped there. Axis **B** (named tools, by name): five rounds, each adding — `rtk`, `context-mode`,
`ccusage`; `headroom`, `caveman`, `CBM`; `pxpipe`, `ponytail`, `codebase-memory-mcp`; `mem0`,
`serena`; `squeez`, `graphify` — **and it was stopped while still adding**, at the session's budget,
which is stated here rather than dressed as saturation. Axis **C** (the harness's own documentation):
the context-window, costs and memory pages fetched whole, and two searches; five rounds, the fifth
adding the compaction layers. **Named tools were looked for by name** on axis B throughout.

**Screened**, against the constraints this project has already settled:

| Technique | Verdict | Why |
| :--- | :--- | :--- |
| Path-scoped `.claude/rules/` | **adopted** as `CE-14` | the harness documents it; the repository's tier model asked for it |
| Quiet by `isatty` on every tool | adopted, extended to the deck gate as `CE-19` | already the house rule, L-153 |
| Compaction between tasks instead of a session boundary | **deferred** to `CE-16`'s measurement | collides with a settled rhythm; the owner decides on numbers |
| Subagents for read-heavy exploration | deferred | this run found no read that a summary would have served — the resume needs the rule, not a summary of it; re-screen when a task's read path is a deck specification |
| `PostToolUse` hook rewriting tool output | **rejected** | a hook that edits what a gate printed collides with L-05's *say which half you checked*; the tools already decide their own green output, which is the same saving with the tool as the owner |
| Shell-output compressors (`rtk`, `headroom`, `squeez`) | rejected | a proxy between the gate and the reader is a second author of the evidence; L-153 solved the case that mattered at the source |
| Rendering context as images (`pxpipe`) | rejected | lossy on exact strings by its own README, and every figure here is an exact string |
| Output-style compressors (`caveman`, `ponytail`) | rejected | the record forms are policy (`CE-22`); the reply style is already the owner's structured style |
| Code-graph and memory servers (`CBM`, `codebase-memory-mcp`, `mem0`, `serena`) | rejected | vendor figures measure compression against whole-repo grep; this tree's questions are answered by its own tools in under 2 KB |
| `ENABLE_TOOL_SEARCH`, tool deferral | accepted as already in force | this session's Notion tools arrived as names only; the browser and artifact schemas did not, and that is the harness's |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, `/autocompact` | deferred | no session here has compacted; `CE-16`'s task is where a threshold would be chosen |
| Block-level HTML comments in `CLAUDE.md` are stripped before injection | noted, not adopted | maintainer notes at zero cost; the project keeps its notes as rules with reasons, and a comment nobody loads is a fact with no home |
| Move instructions from `CLAUDE.md` to skills | rejected | the plugin's skill is the adopter's, not this repository's; `CE-14` is the same move by a mechanism that fires on the tree |

**The research changed two findings**: `CE-14` exists because the harness's mechanism was found on
axis C, and `CE-16`'s arithmetic uses the harness's cache lifetimes. Nothing on axis B survived
screening, and that is a result.

### 11.4 Upstream — observed here, for their owners

Each entry says whether the owner's backlog was read, and each carries this project's labels, not
theirs.

- **The handoff skill** (the owner's `Handoff`). The always-loaded spine is 26,526 bytes and the
  resume flow 6,219; a resume pays 35 KB for about 3 KB of steps it follows. The skill already loads
  spine-plus-one-flow (P6); the spine is the remaining weight. **Backlog not read.** By the owner's
  cross-repository rule this is fix-or-drop, never a report: a candidate pull request from a session
  in that repository, measured there first.
- **The ecoctx skill** (the owner's). The method cost this run 31 KB across its body and two
  references, loaded one at a time as designed; its instrument for surface A cannot see inside the
  harness's shared prefix, and its search record cannot be made complete — both stated in the skill.
  Two things it could add: the transcript instrument as a named grade, and the per-byte cost line
  in §11.2, which is the mechanism behind its own *only tier 1 gets a budget* rule. **Backlog not
  read.**
- **The harness.** Two of three documentation pages fetched with a prompt asking for a list came
  back whole, at 10–12 thousand tokens each; the third, larger still, was capped to a 2 KB preview
  and a file, which saved more than any finding here. The cap is the right default and the prompt is
  not honoured on that site; this project has no channel for it and none is proposed.

### 11.5 Phase 2 — recorded after the remedies exist

*Not yet run.* [T-294](../tasks/T-294-grade-the-second-context-economy-runs-bands-after-its-remedies-land.md)
is raised and blocked on the six children; it grades every band above and the model in §11.2, and
names at least one prediction the measurement refused. §10.2's sentence stands until then.

### 11.6 Byproducts, second run

Recorded, never ranked.

- `python tools/docs/cycles.py` exits 1 on every run while `T-284` is open, printing 5,931 bytes —
  known, and the reason is in `check_all.py`.
- `docs/PRE-RELEASE-AUDIT.md` §3 is 288,021 bytes over 159 rows; nothing reads it whole, and the
  task's own statement that a row is one or two kilobytes was right about the mean and silent about
  the 5,732-byte maximum.
- The full gate ran 226 s here against 211 and 332 s the previous day on the same tree — the
  machine's drift is larger than any tool's share, so a timing is read against its own run's ranking.
- The transcript instrument's first version over-counted calls by content block; a scan owes a
  known-good case before its output is a finding, which the method already says and this run
  re-learned.
