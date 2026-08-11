---
id: T-056
title: Humanize the human-facing documents before publishing
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-050, T-052, T-042]
work_package: PH1
shipped_in: 0.1.0
owner: the project owner
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - docs/PUBLISHING.md
  - README.md
---

# T-056 — Humanize the human-facing documents before publishing

*Adapted from `T-079` in the **taskmd** project, 2026-08-09, at the owner's request — the same rule
is wanted across every repository that gets published. What carried over unchanged is the owner's
exception, quoted verbatim below, and the shape of the deliverable: **a standing rule, not a pass
over today's tree**. What changed is recorded under [Where this differs from
T-079](#where-this-differs-from-t-079), because a task copied without its differences named is a
task that will be worked against the wrong repository.*

## 1. Specify

**Outcome**
A standing rule, at a home that publication reaches, saying which text gets humanized and under what
exception — plus one use of it on real text, because a rule nobody has run is a claim. **The rule is
the deliverable, not a sweep**: a sweep covers the files that exist on the day it runs, and every
document written afterwards is uncovered.

**Raised to a deployment rule by the owner, 2026-08-09.** *"No release can be published without
humanizing human-facing information. Plugin files are not human facing and must be kept AI
optimized."* Two consequences, and neither is cosmetic:

- **It binds every release, not this one.** A `blocked_by` edge on
  [T-008](T-008-package-document-and-publish.md) is spent the moment T-008 closes, so the edge
  cannot carry a standing rule and was never going to. The constraint now lives in
  [`CLAUDE.md`](../CLAUDE.md) *Publishing constraints*, beside the three rules of the same kind, and
  the edge stays as the gate on the **first** release.
- **The agent-facing exclusion is a rule, not a scope note.** It was already listed under *Out*
  below as a boundary this task would not cross. The owner has made it a positive requirement:
  plugin files **must be kept** AI-optimized, so a humanizer pass over `SKILL.md` is now a defect
  rather than merely out of scope, and this task's job includes saying so where a later reader
  looks.

What that leaves for this task is the **detail and the use**: the covered-set test, the verbatim
exception, the DS-106 boundary, and one run against real text. The decision itself is taken.

**Why this one**
Every document here was drafted in an agent session, and the tell is uniform prose rather than any
one sentence. A reader who bounces off the README never reaches the plugin. This repository already
holds *decks* to that standard — DS-106 bans five categories of terminology and `check.py` gates it —
and holds its own documents to nothing.

**The exception, as given by the owner on 2026-08-09 — verbatim**

> When humanizing docs: preserve tables, code blocks, heading hierarchy, and **Label:** value
> bullets. Skip patterns 15, 16, 18. Apply the rest.

The three skipped patterns are numbered sections of the skill, and they are named here as well as
numbered so the instruction survives the skill being renumbered — **verified against the installed
copy**, `humanizer@humanizer` **2.9.1**, where they are **15 Overuse of Boldface**, **16
Inline-Header Vertical Lists** and **18 Emojis**. Each is load-bearing in a technical document: this
project's prose carries its decisions in bolded labels and its rules in inline-header lists, and
stripping them would flatten the structure that makes a document skimmable rather than remove a tell.

**Scope**
- In: the rule, written where publication reaches it.
- In: what the rule covers, stated as a test rather than a list — *what a stranger reads before they
  have installed anything*. Today that is [`README.md`](../README.md) and any repository or
  marketplace description; a list would go stale the first time a document is added, and silently.
- In: one application of the rule to text that exists today, as the evidence it works.
- Out: **everything agent-facing** — [`CLAUDE.md`](../CLAUDE.md),
  [`skills/htmldeck/SKILL.md`](../skills/htmldeck/SKILL.md) and its `references/`, and the tool
  docstrings. The owner's words: keep them efficient for AI parsing. The compression that reads as
  machine-written is the feature there, and `SKILL.md` is under a byte budget on purpose.
- Out: commit messages, for the same reason.
- Out: task files. Fifty-odd records of work already done are an audit trail; rewriting their prose
  edits the history rather than the product.
- Out: **the ruleset and the research notes** — `docs/DESIGN-SYSTEM.md`, `docs/DESIGN-RATIONALE.md`,
  `docs/EVALUATION.md`, `docs/LESSONS.md`, `docs/research/`. A stranger does not read them before
  installing, they are cited by ID from code, and their density is what makes them usable.
- Out: **deck copy**, which DS-106 and DS-107 already govern and `check.py` already gates. Two
  instruments over one text would disagree, and the gated one wins.
- Out: anything the humanizer would have to invent a fact to improve. **Every figure in the README
  is pasted from a run** ([T-050](T-050-write-the-repository-readme.md)), so a rewrite that rounds,
  rephrases or re-derives one is a defect and not a style improvement.

**Inputs**
- The installed skill: `humanizer@humanizer` 2.9.1, from the `blader/humanizer` marketplace.
  **Not currently enabled for this project** — see the open question below.
- [`CLAUDE.md`](../CLAUDE.md) *Publishing constraints*, where the other publish-time rules live, and
  *Voice*, which already states the machine-written-terminology position for decks.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §3.3 — DS-106 and DS-107, the deck-side rule
  this one sits beside without overlapping.
- The owner's exception of 2026-08-09, quoted verbatim above.

**Acceptance criteria**
- [ ] The rule exists in one home, states what it covers and what it excludes, and carries the
      exception verbatim
- [ ] ~~`CLAUDE.md` gains a pointer to it~~ — **done ahead of this task, 2026-08-09**, when the owner
      raised it to a deployment rule. What remains is that the pointer still resolves to the written
      rule once it exists, and that the summary in `CLAUDE.md` and the rule do not disagree
- [ ] **The rule binds releases, not this release** — stated so that closing T-008 does not retire it,
      and so a second release is covered by the same words
- [ ] **Keeping plugin files AI-optimized is written as a requirement**, not only as this task's
      *Out* list, since the owner made it one
- [ ] The rule's covered set is stated as a test a future document can be held against, not as a
      list of today's files
- [ ] The rule says how it relates to DS-106, so a later reader does not apply both to one text
- [ ] The rule has been **used** on real text, with the before and after both recorded
- [ ] Every figure and every code block in the touched text is byte-identical afterwards, checked
      rather than assumed
- [ ] Nothing agent-facing is rewritten, and `check_scaffold.py` still passes

**Open questions**
- ~~**Is the humanizer skill to be enabled for this project, or run from the other one?**~~
  **Answered 2026-08-09 by inspection: it runs here.** `humanizer:humanizer` is listed in this
  project's session, so nothing had to be enabled and no cross-project run was needed. The installed
  copy was re-verified rather than trusted from the record above — `plugin.json` reads **2.9.1**, and
  the four numbered sections this task depends on are **14 Em Dashes (and En Dashes): Cut Them**, **15
  Overuse of Boldface**, **16 Inline-Header Vertical Lists** and **18 Emojis**. The record and the
  installed skill agree, which is what makes the verbatim exception safe to carry into a rule that
  will outlive this task.
- ~~**Which documents count as human-facing?**~~ **Answered by the owner, 2026-08-09** (on T-079,
  and it transfers): the README definitely, and any repository description. Everything agent-facing
  is explicitly out, because it should stay efficient for AI parsing.
- ~~**Does pattern 14 apply — cutting em dashes?**~~ **Answered by the owner, 2026-08-09: yes.**
  Worth recording that the skill offers an escape and it is not being taken: its *Voice Calibration*
  section says a supplied writing sample outranks §14, so this repository's existing prose could
  have been handed over as a sample to keep its em dashes. The answer forecloses that, and the rule
  must say so, because the next person to read §14 will find that escape too.

## Where this differs from T-079

Four differences, each of which changes what the task does rather than only what it names.

| | taskmd T-079 | here |
| :--- | :--- | :--- |
| **The README** | Does not exist; T-006 step 5 writes it, so T-079 is scoped *away* from it to avoid writing one document twice | **Exists**, written from a clean clone by [T-050](T-050-write-the-repository-readme.md). It is the primary subject, and the ordering problem does not arise |
| **A rule already governs machine-written prose** | No analogue | **DS-106 and DS-107 do, for decks, and `check.py` gates DS-106.** The new rule must say where its jurisdiction ends, or two instruments end up over one text |
| **Where the rule lives** | A `PUBLISHING.md` under `docs/`, pointed to from tier 1 | No such file here. The same shape is the leading candidate, on this project's own precedent — `SKILL.md` keeps substance in `references/` for exactly this reason — but it is step 1, not a decision taken in advance |
| **What must survive verbatim** | Tables, code blocks, headings, label bullets | Those, **plus every figure in the README**, each of which is pasted from a run and re-derived by `ruleset.py --counts` rather than typed |

The publish task is **[T-008](T-008-package-document-and-publish.md)** here, not T-006, and this task
gates it on the same reasoning T-079 used: after publishing, the first impression has been made.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 0 | ~~Settle whether the constraint binds at all~~ — **taken by the owner, 2026-08-09**, and already in `CLAUDE.md` *Publishing constraints* | The bullet, and this row as its record |
| 1 | Answer the enablement question, then settle where the rule's **detail** lives against the cost of `CLAUDE.md` being read every turn | The decision and its rejections, in §3 |
| 2 | Write the rule: the covered set as a test, the exclusions with the owner's reason, the exception verbatim, the DS-106 boundary, and the *Voice Calibration* escape that is not being taken | `PUBLISHING.md` under `docs/`, or wherever step 1 lands it |
| 3 | Add the pointer from `CLAUDE.md`, and measure what it costs there | The edited section, and the character count before and after |
| 4 | Use the rule on real text: draft the repository description a stranger reads, run the skill's draft / audit / final loop on it, and record all three | The before, the audit answers, and the final text, in §3 |
| 5 | Run the rule over `README.md` and record the verdict per section, **including the sections it changes nothing in** | A verdict list, in §4 |
| 6 | Prove the figures survived: re-derive every count the README states and diff the code blocks | The output of `ruleset.py --counts` against the edited README |
| 7 | Point T-008's publication step at where the drafted description lives | The edited T-008 |
| 8 | `task.py index`, `task.py check --closing`, `check_scaffold.py` | The output of each |

**Step 4 is what makes this a task rather than a note**, and **step 6 is what makes it safe.** A rule
written and never run is the unverified claim this project exists to avoid (**L-05**); a humanizer
pass over a document whose every figure is evidence is how a correct number quietly becomes a
plausible one (**L-03**).

**Decisions — shape**

- **The rule is written as a test, not as a list of files.** A list goes stale the first time a
  document is added, and it would go stale silently. *Rejected: enumerating `README.md` and the
  description.* This project has already paid for that once — `reconcile_targets` in
  [`.handoff/config.md`](../.handoff/config.md) is an enumeration, and the audit
  ([T-042](T-042-audit-the-whole-repository-against-itself.md)) is what found what it had stopped
  covering.

**Not in this plan:** rewriting the ruleset or the research notes, which are out of scope above; and
enabling the humanizer skill repository-wide, which is a tooling decision the owner takes once for
every project rather than inside this task.

## 3. Implement

**Decisions & assumptions**

- **The skill runs in this project; nothing had to be enabled — 2026-08-09.** `humanizer:humanizer`
  is listed in this project's session. The installed copy was re-verified rather than trusted:
  `plugin.json` reads **2.9.1**, and §14, §15, §16 and §18 carry the headings the exception depends
  on. The one question that could have stopped the task dead cost one command.

- **The rule's detail lives in `docs/PUBLISHING.md`, and `CLAUDE.md` points at it — 2026-08-09.**
  `CLAUDE.md` is read every turn of every session, so 7 496 bytes of covered-set test, exclusion
  table and verbatim exception cannot live there; the pointer costs **145 bytes** (6 505 → 6 650),
  which is the whole trade. *Rejected: inlining it in `CLAUDE.md`*, which is that cost 50× over for
  a document consulted at release time. *Rejected: leaving the detail in this task file* — a task
  reaches `done` and a standing rule must outlive it, which is the same spent-edge failure §1
  already identified for `blocked_by`, one level up. *Rejected: `docs/DESIGN-SYSTEM.md`* — that
  ruleset is deck-scoped, every entry carries a `DS-nnn` ID with a gate and a reach verdict, and a
  repository-prose rule there would be an ID no check could ever own in a document whose entire
  argument is that every ID has an owner.

- **`CLAUDE.md`'s pointer was repointed from the task to the rule — 2026-08-09.** It named
  [T-008](T-008-package-document-and-publish.md)'s blocker, T-056, as where the detail lived. That
  reproduced the defect §1 diagnosed: the standing rule would have pointed at a closed task. It now
  points at `docs/PUBLISHING.md` for the rule and keeps T-056 as the gate on the **first** release
  only.

- **§14 applies inside table cells; the exception protects the table, not the prose in it —
  2026-08-09.** Four of the README's 24 em dashes sat in table cells. Reading *preserve tables* as
  exempting cell text would leave §14's closing scan unable to come out clean, and §14 is written as
  a hard constraint with exactly that scan. Every row, column and fact survives; four separators
  became a full stop, a colon and a semicolon. **No fenced block was touched at all** — the 20
  remaining em dashes were all in prose, which the region diff below confirms independently.

- **One factual correction, made deliberately and not by the humanizer — 2026-08-09.** The lede
  said *"the mode that writes a deck for you is not [built]"* and pointed at *What does not exist
  yet*, a section [T-004](T-004-critique-mode-blunt-section-by-section-review.md) had already
  rewritten to say the opposite. The front door contradicted its own backlog section. Corrected to
  name all four working parts. **Recorded here as content work rather than as a humanizer change**,
  because the skill's rule 3 forbids it inventing or altering a fact, and a pass that quietly fixed
  a claim would make the before/after record useless as evidence.

- **The humanizer bullet was removed from *What does not exist yet* — 2026-08-09.** It read *"the
  human-facing text has not been through the humanizer"*, which this task makes false. Left in
  place, the first document the rule covers would state the opposite of its own outcome.

**Step 4 — the repository description, all three stages recorded**

*Draft, written straight and not pre-degraded:*

> A Claude Code plugin for building single-file HTML presentations that don't look generated — self-contained decks that open offline with no installation, backed by a 161-rule design system, a build check that accounts for every rule it cannot reach, and a blunt critique pass.

*Audit, the skill's two questions:*

- **What makes it obviously AI generated?** The em dash bolting an appositive onto the main clause
  (§14). The four-item pile-up after *backed by*, which is the rule-of-three habit with one more
  bolted on (§10). *Backed by* is promotional framing rather than a statement of what is there (§4).
  And it is one 44-word sentence with no rhythm, which is the even mid-length cadence §7's guidance
  names as the giveaway.
- **Does the rewrite state any fact not in the source?** No, but the draft did: it says **161** rules,
  which was the README's figure and was **already stale** when the draft was written. The correct
  figure is 163 rows. Caught by step 6, not by the audit, which is the argument for step 6 existing.

*Final:*

> Single-file HTML presentations that don't look generated. One .html you double-click, and it opens with the network off. A Claude Code plugin: a 163-rule design system, a build check that names every rule it cannot reach, and a critique pass that is blunt on purpose.

No em or en dashes, no curly quotes, 231 characters, inside GitHub's 350-character limit. **T-008
takes it from here**, per step 7.

**Step 6 — what re-deriving the figures actually found**

The README's figures were **stale before this task touched them**, which is what step 6 was written
to catch and the reason the plan refused to trust the diff. Build mode and critique mode added rules
to the ruleset on 2026-08-09 and nothing re-derived the README afterwards:

| Block or claim | Stated | Re-derived | Command |
| :--- | ---: | ---: | :--- |
| `ruleset.py --counts`, rows | 161 | **163** | `python tools/deck/ruleset.py --counts` |
| `ruleset.py --counts`, declared | 162 | **164** | same |
| `ruleset.py --gates`, hard | 115 | **117** | `python tools/deck/ruleset.py --gates` |
| `ruleset.py --gates`, mechanical | 86 | **87** | same |
| `ruleset.py --gates`, judge | 24 | **25** | same |
| *What is actually here*, "161 rules" | 161 | **163** | `ruleset.py --counts` |
| `task.py check`, pointers | 968 | **992**, and 491 section refs | `python tools/tasks/task.py check` |
| `check.py` account partition | 113/81/0/4/28/0 | unchanged | `python tools/deck/check.py examples/reference-deck.html` |
| `check_scaffold.py` | 10 of 10 | unchanged | `python tools/plugin/check_scaffold.py` |
| Reference deck, 221 KB | 221 KB | 225 922 B = **220.6 KB** | `os.path.getsize` |
| Sort-window deck, 212 KB | 212 KB | 217 050 B = **212.0 KB** | same |

**One of these was an internal contradiction, not just staleness.** The prose said *"The judgement
half is 25 `hard` rules"* while the `--gates` block three sections above printed **24**. The prose
was right and the block was behind; both now read 25 from the same run.

Both deck sizes survive: 220.6 KB rounds to the stated 221, and 212.0 is exact.

**Outputs produced**
- `docs/PUBLISHING.md`
- `README.md`
- `CLAUDE.md` (the pointer only, repointed from the task to the rule)
- `tasks/T-008-package-document-and-publish.md` (step 7)

## 4. Review

**Step 5 — the verdict per section of `README.md`, including the ones nothing changed in**

| Section | Verdict | What the pass found |
| :--- | :--- | :--- |
| Lede | **changed** | Em dash into a rule-of-three tail (§14, §10). Separately, and not as a humanizer change, the claim that the deck-writing mode is unbuilt was **false** and pointed at a section saying so |
| *What is actually here* | **changed, minimally** | Three em dashes inside table cells became a full stop and two colons. Every row, column and fact kept. The `161` figure was corrected under step 6, not here |
| *Run it* | **changed** | Five em dashes. Two aphorism-shaped openers rewritten: *"The account is the point"* became an instruction that says what to do, and the em-dash parenthetical around *with what would close the excusal* became real parentheses. **All five fenced blocks untouched by this pass** |
| *The reference deck* | **changed** | Em dash after a link, and one aphorism formula (§32): *"a rubric that has never been tested is a rubric that passes everything"* became the concrete claim it gestures at. All eleven figures kept |
| *The deck nobody authored by hand* | **changed** | Two em dashes, one of them attaching the deck's own title. The title itself is a proper name and was not touched, per the skill's *secondhand text* guidance |
| *Reviewing a deck* | **changed** | Two em dashes bracketing the five dimension names, now parentheses. The staccato *"run over the parent, none"* was **kept**: it is a real contrast, not manufactured drama (§31) |
| *What does not exist yet* | **changed** | Three em dashes, one aphorism (*"a README describing the plan is not a README"*), and one bullet deleted for being made false by this task. The PH1 contents were **stale**, still naming build and critique mode as outstanding |
| *Where to go next* | **changed, minimally** | One em dash in a table cell became a semicolon. Table otherwise identical |
| *Licence* | **changed, minimally** | One em dash after **MIT**. The OFL paragraph was read and **left alone**: it is specific, correctly hedged, and carries no tell |
| Fenced blocks, all 13 | **unchanged by the pass** | Proven by a region diff, not asserted. Three were later corrected under step 6 as a separate, recorded pass |

**Nothing in the OFL paragraph or the Marnfield/Riverbend disclaimers was rewritten.** Both are the
*specific, hard-to-fabricate detail* the skill's detection guidance says to preserve, and flattening
them would have removed the strongest human signal on the page.

**Acceptance criteria**

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The rule exists in one home, states what it covers and what it excludes, and carries the exception verbatim | **met** | `docs/PUBLISHING.md`, §1–§3 and §5. The exception is block-quoted, unedited |
| ~~`CLAUDE.md` gains a pointer~~; the pointer still resolves and does not disagree | **met** | Repointed from T-056 to `docs/PUBLISHING.md`, which is the stronger form: the old pointer would have resolved to a closed task. `task.py check` resolves it |
| The rule binds releases, not this release | **met** | `PUBLISHING.md` §1, which states why the `blocked_by` edge could never have carried it |
| Keeping plugin files AI-optimized is written as a requirement | **met** | `PUBLISHING.md` §1 and §3, as a defect rather than a scope note. §7 applies it to `PUBLISHING.md` itself |
| The covered set is a test, not a list of today's files | **met** | `PUBLISHING.md` §2, with the question stated first and today's two answers under it, plus a worked case for a document that does not exist yet |
| The rule says how it relates to DS-106 | **met** | `PUBLISHING.md` §4, a four-row table of jurisdiction, instrument, failure mode and scope, ending with the tie-break |
| The rule has been used on real text, before and after recorded | **met** | Twice. The repository description with all three stages in §3; `README.md` with a per-section verdict above |
| Every figure and every code block in the touched text is byte-identical afterwards, **checked** | **met, and it caught something** | The humanizer pass left all 13 fenced blocks byte-identical, proven by a region diff. Re-deriving then found **six figures that were already wrong before this task**, corrected in a second, separately recorded pass |
| Nothing agent-facing is rewritten, and `check_scaffold.py` still passes | **met** | The only agent-facing edit is 145 bytes of pointer in `CLAUDE.md`, which is a reference change, not prose. `check_scaffold.py`: 10 of 10, SKILL.md 5 206 of 8 192 bytes, untouched |

**Child fix tasks raised**
- **[T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md)** — the six
  stale figures were corrected in place, but nothing keeps them correct. The obligation to re-derive
  now exists in `PUBLISHING.md` §6, unchecked, which is the state this repository treats as a claim.
  Raised to **PH2**: the figures are right today, so a first release is not blocked by it. The
  general finding is **L-52** in [`../docs/LESSONS.md`](../docs/LESSONS.md).

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **The rule is written, and running it found the README was already wrong.** `docs/PUBLISHING.md` carries the covered-set test, the exclusions, the verbatim exception and the DS-106 boundary; `CLAUDE.md` was **repointed from this task to that document**, because a standing rule pointing at a task that closes is the spent-edge failure §1 diagnosed one level up. The pass itself cut all 24 em dashes and three aphorism formulas from `README.md` and left every fenced block byte-identical, proven by a region diff. **Then step 6 earned its place**: six figures were stale *before* this task touched them, because build mode and critique mode grew the ruleset the same day and nothing re-derived the README afterwards — 161 rows are 163, 115 hard rules are 117, and the prose already contradicted its own `--gates` block on whether the judgement half is 24 rules or 25. One claim was outright false: the lede said the deck-writing mode was unbuilt while pointing at a section [T-004](T-004-critique-mode-blunt-section-by-section-review.md) had already rewritten to say the opposite. Corrected as content work and recorded separately from the humanizer pass, since the skill may not alter a fact and a pass that quietly fixed one would make the evidence worthless. **The repository description is drafted, audited and final** in §3, and [T-008](T-008-package-document-and-publish.md) now carries a criterion that copying it is required and retyping it at the console is a failure. |
| 2026-08-09 | → in_progress | **The file was ahead of its status, and the open question cost one command.** §1 was complete and accepted, §2 carried a full eight-step plan, and the front-matter still read `proposed` / `specify` — so the status was behind the file rather than §1 being unfinished. The one thing that could have stopped the task dead is answered: `humanizer:humanizer` is listed in this project's session, nothing had to be enabled, and the installed copy was re-verified at **2.9.1** with §14, §15, §16 and §18 carrying the headings the owner's exception names. `deliverables:` declared, which §6.2 of the workflow requires from `specified` onward and which this file owed. |
| 2026-08-09 | (no change) | **The subject grew: `README.md` gained three sections this session and none has been through the humanizer.** [T-002](T-002-build-mode-the-self-contained-deck-generator.md) added *The deck nobody authored by hand*; [T-004](T-004-critique-mode-blunt-section-by-section-review.md) added *Reviewing a deck* and rewrote *What does not exist yet*, which had become a heading over a positive statement once the two modes landed. **Step 5's verdict list therefore covers more than it did when the plan was written**, and step 6 matters more than it did: two of the three new sections paste figures from a run — the pointer and section counts, and the seeded-deck result — and one quotes deck sizes in binary KB against a byte count, which is the convention both READMEs use. **One inconsistency in this file to settle in the specify phase rather than trip over:** the front-matter reads `proposed` / `specify` while §2 already carries an eight-step plan, so either §1 has an open question worth naming or the status is behind the file. |
| 2026-08-09 | (no change) | **Raised to a deployment rule by the owner** — *"no release can be published without humanizing human-facing information; plugin files are not human facing and must be kept AI optimized."* The important half is that it binds **every** release: a `blocked_by` edge on [T-008](T-008-package-document-and-publish.md) is spent when T-008 closes, so the constraint could never have lived there and now sits in [`CLAUDE.md`](../CLAUDE.md) *Publishing constraints* beside the three rules of its kind. The edge stays as the gate on the first release. The second half turns this task's *Out* list into a positive requirement: a humanizer pass over `SKILL.md` is now a **defect**, not merely out of scope. Step 3 was therefore done ahead of the task and step 0 records it; what is left here is the detail and one use of it, which is what the task was always for. |
| 2026-08-09 | → proposed | Adapted from `T-079` in the **taskmd** project at the owner's request, who wants the rule applied across every repository that gets published. The owner's exception is carried **verbatim** and its three pattern numbers were **re-verified against the installed skill** rather than trusted from the copy — `humanizer@humanizer` 2.9.1 does have 15 Overuse of Boldface, 16 Inline-Header Vertical Lists and 18 Emojis, and 14 is the em-dash rule with the *Voice Calibration* escape. Four differences from the source are named in their own section rather than absorbed: **the README already exists here**, so it is the subject rather than something to route around; **DS-106 already governs machine-written terminology for decks and is gated**, so the new rule has to state where its jurisdiction ends; there is no `PUBLISHING.md` under `docs/` to write into; and **every figure in this README is pasted from a run**, which makes "preserve code blocks" a stronger obligation than it was in the source. Made a blocker on [T-008](T-008-package-document-and-publish.md) on the source's reasoning: after publishing, the first impression has been made. |
