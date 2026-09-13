# htmldeck — working conventions

Read this before doing anything in this folder.

## What loads every turn, and what bounds it

**Tier 1 is what the harness loads without being asked** — a property of the tree, not a list anyone
maintains. Establish it by observation and never from a file's claim about itself: a document that
asserts a load discipline the harness does not implement is worse than one over budget, because the
claim cannot be falsified and content keeps being written on the strength of it. **Tier 2** is what a
skill or workflow document pulls in when work of a kind starts. **Tier 3** is what tier 2 loads one
at a time, for the branch actually taken.

**Observed 2026-08-13:** a session here receives three files unasked — the owner's global
preferences, this file, and the memory index. Method: read what the session was given before its
first tool call, then confirm the tree holds no second `CLAUDE.md`. **This repository owns one of the
three**; the other two are the owner's and outside this bound, and the memory index is `CE-10`'s. The
plugin also writes into an adopter's tier 1, through `skills/htmldeck/SKILL.md`'s description block
and nothing else.

**`.claude/rules/` is tier 2 by path**, observed 2026-09-14 ([T-295](tasks/T-295-complete-t-288s-observation-and-decide-the-move.md) §3): the
harness appends a rule file after a read of a file its `paths:` names. A rule file is content cut
from this one, so it is not a term of the bound below, for the reason a tier-3 document is not.

**The bound: this file stays smaller than the smallest document it defers to that a session enters
at the start of work of a kind** — today `docs/BRIEF.md`, `docs/PUBLISHING.md`,
`tasks/TASK-WORKFLOW.md`, `tasks/README.md`, `.taskmd/config.md` and `docs/AUDIT-METHOD.md`. **That
test is the tier-2 set, ruled by the owner 2026-08-23**
([T-236](tasks/T-236-tier-1-and-the-brief-against-what-they-measure.md)): the list is its enumeration,
a document that meets the test joins it, and it is still not every document this file links to. A
tier-3 document — one opened for a single question *during* work — is not a term:
`docs/RELEASE-PHASES.md`, `docs/RELEASE-HISTORY.md`, `docs/REMEDIATION-ORDER.md`. **Otherwise
splitting content out could never satisfy the bound**, since each split makes a new document smaller
than what it was cut from. Both terms are counted from the tree and **no constant is written
anywhere**, because a number and the arithmetic that justified it have to be edited together and the
number wins by staying put. The inequality says something: once the file you pay for on every turn
costs more than any single document you open on demand, the split has inverted. Measure both terms
with

```bash
python -c "import pathlib;[print(f'{p.stat().st_size:>7}  {p}') for p in map(pathlib.Path,'CLAUDE.md docs/BRIEF.md docs/PUBLISHING.md tasks/TASK-WORKFLOW.md tasks/README.md .taskmd/config.md docs/AUDIT-METHOD.md'.split())]"
```

**Tiers 2 and 3 carry no budget**, and that is deliberate rather than an omission: they are not paid
every turn, so a size limit there measures the wrong cost, and what constrains them is loading one at
a time. It accepts that `docs/BRIEF.md` and `docs/LESSONS.md` grow without limit. A tier-2 document
that starts loading on every turn has become tier 1, and this bound applies to it.

**This file is over its own bound** — 11,413 bytes against `docs/AUDIT-METHOD.md`'s 8,040, measured
2026-09-14 with the command above, so the debt is 3,373. *The floor moved twice on 2026-09-02 and this
sentence was rewritten twice with it: `T-239` gave that file a Method column, and B22 gave it
`PR-82`'s clause. It had fallen to that file from `tasks/TASK-WORKFLOW.md`'s 13,324 when the
2026-08-23 ruling made the audit method a term — three changes in the smaller side, one in the
definition, and never in this file.* The two cuts this bound was written to make
decidable are spent: `CE-01` as
[T-143](tasks/T-143-split-the-release-chronology-out-of-claude-md.md) and `CE-04` as
[T-144](tasks/T-144-give-each-cumulative-rule-one-operative-home.md), both ranked in
[`docs/CONTEXT-AUDIT.md`](docs/CONTEXT-AUDIT.md) §6, and so is the third: `CE-14` in the same table,
carried on 2026-09-14 by [T-295](tasks/T-295-complete-t-288s-observation-and-decide-the-move.md),
which moved the deck and release rules under `.claude/rules/`. What remains has no ranked finding
behind it. That is dated debt and not a rule already met. *This statement has been wrong in both terms four
times — three when the smaller side moved, once when the definition did. **Re-measure both,
never one**, and write it here in the same edit — a figure about this file cannot be corrected
anywhere else, and `tools/docs/figures.py` holds both terms to the fence.*

## What this is

A publishable Claude Code plugin: **single-file HTML presentations that don't look generated**,
plus the prompt structure that briefs them and the critique pass that fixes them.

Grounded in a corpus of real decks, prompts and written style guides from a training programme.
`docs/BRIEF.md` records what that evidence shows and what to build; `reference/` holds the source
prompt — **one 1.2 KB file, and it is a prompt rather than a codebase**: nothing in it is code to
copy or behaviour to verify.

**What exists.** `python tools/deck/check.py <deck>` decides 93 of the 122 rules a gate owns and
names the other 29 with a reason each; `skills/htmldeck/references/build.md` plus `shell/` turn a
reviewed specification into a deck; `skills/htmldeck/references/critique.md` plus
`tools/deck/critique.py` are the review. **The repository is public at
`github.com/uchimata2/htmldeck`, `master` is the published branch, and the current version is
`0.7.0`.**

**When each of those landed, which release carried which fix, and which task found which defect are
[`docs/RELEASE-HISTORY.md`](docs/RELEASE-HISTORY.md)** — tier 3, loaded by nothing. It was this
section until 2026-08-14.

**A phase name is not a version number. `work_package` is the phase, `shipped_in` is the version, and
never write a phase with a `v`** — a task holding `PH3` and `0.2.1` at once is the rule working.
Conflating them nearly shipped a release no adopter could have installed: **L-69**. Which number a
*release* takes is [`docs/PUBLISHING.md`](docs/PUBLISHING.md) §8; which field a *task* carries is
`tasks/TASK-WORKFLOW.md` §3.

**The backlog is four release phases — `PH1` to `PH4`. PH3 is the main line, and `PH4` is the 3D
line, which 1.0.0 does not wait for.**
[`docs/RELEASE-PHASES.md`](docs/RELEASE-PHASES.md) is the decision: what each phase contains, why each
split was needed, and why the line between PH2 and PH3 falls at an effort estimate of `l`.
`tasks/README.md` is the current state, grouped by the same names. **A new task belongs to one
of them**: `PH1` only when a defect in the published plugin reopens it — such a defect is a `PH1`
**phase** task, not a later improvement — `PH4` for 3D work, `PH3` for anything else `l` or `xl`,
**and, since PH2 shipped, for everything else that is not such a defect**, because reopening a shipped
phase is reserved for them. That last clause is why a small task can sit in the phase of the big ones.
A phase that quietly takes work the size of the next one is the failure the first two splits exist to
prevent.

**A task's classification is this project's to make, not its filer's.** A report that arrives as
feedback because a contract behaves as written is still a defect when a published gate fails a deck
for using a class that contract defines. Re-derive the phase and the type from the rules above, and
log why they differ from what arrived.

**Read the brief first** — its "Decisions taken" section overrides anything older in it.

**The objectives are still being shaped.** Research is expected to be able to overturn scope, not
just fill it in. Findings that contradict the brief are surfaced as candidate changes of
direction, not quietly worked around.

## The rules that must survive

**Rules 1 to 5 and 7 are [`.claude/rules/decks.md`](.claude/rules/decks.md)**, with *Voice* and
*Verifying*, and the harness appends that file after a session reads one in a deck tree. **Rule 6
stays here**, because a path-scoped rule arrives after the read that matches it — one read too late
for the rule that forbids reading a deck whole. The numbers did not change, so a citation of rule N
still names one rule.

6. **Look at the rendered deck, and never read one whole.** A deck that validates is not a deck
   that reads well — so *look* means render it and open it, which nothing here replaces. It does
   **not** mean reading the file: every shipped deck is over 300 KB (`python tools/docs/figures.py`
   prints each size), and a question about what is inside one is answered by a tool in `tools/deck/`
   or by a targeted search, never by opening the HTML.

## Working method

1. **No work without a task file** in `tasks/`, from `tasks/_task-template.md`. Tasks are tracked
   with the **taskmd** plugin, and `python tools/tasks/lint.py` is every check a task edit owes.
   `tasks/TASK-WORKFLOW.md` owns this project's conventions and `tasks/TOOLING.md` the commands;
   `.taskmd/config.md` is the schema and outranks any prose about the fields.
2. Lifecycle: `specify → plan → implement → review`.
3. What closes a task is `tasks/TASK-WORKFLOW.md` §7's checklist, which owns that bar.

## Publishing constraints

**The steps of a release, in order, are [`docs/PUBLISHING.md`](docs/PUBLISHING.md) §8.** Do not
re-derive the sequence from the last release's commits; that is what §8 was written to stop. Its step 1
and the humanizing rule are [`.claude/rules/release.md`](.claude/rules/release.md), appended after a
session reads `README.md` or `docs/PUBLISHING.md`; the font-licence rule is `decks.md`'s.

This repository goes to GitHub. Everything written here must be:

- **Free of personal, client and machine data.** The source corpus is training work for real
  named scenarios; **do not copy deck content into this repository.** Patterns, structure and
  measurements only. Any example deck shipped here must be written fresh on a neutral topic.
  **One scoped exception, ruled by the owner 2026-08-13:** the adopting project's D6 deck and its
  two specifications may be copied in and published as an example, because that deliverable is an
  exam exercise rather than a real engagement — **sanitized on the way in**, and the source folder
  is read-only in this matter. The exception is that deck and nothing else; the corpus rule above is
  unchanged. [T-128](tasks/T-128-publish-the-adopter-deck-as-a-worked-example.md) carries it.
- **Committed under the publishing identity**, `uchimata2 <112070643+uchimata2@users.noreply.github.com>`,
  set in this repository's local git config. The personal address was rewritten out of all 121
  commits before the first push and **must not come back** — history is public now, so a single
  commit carrying it cannot be undone the way the first rewrite could. **No co-author trailer**, on
  the same reasoning: this history is uniform without one, and a push makes the exception permanent.
  Ruled by the owner 2026-08-14, after four commits carrying an agent trailer were stripped before
  they went out.
- **Out-of-the-box.** Clone and run, no path editing.
