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

**The bound: this file stays smaller than the smallest document it defers to** — `docs/BRIEF.md`,
`docs/PUBLISHING.md`, `tasks/TASK-WORKFLOW.md`, `tasks/README.md`, `.taskmd/config.md`. **Those five
are the tier-2 set and the comparison is against tier 2**, which is what makes the list closed rather
than every document this file links to. A tier-3 document — one opened for a single question, never
to start work of a kind — is not a term: `docs/RELEASE-PHASES.md` was never in the list and
`docs/RELEASE-HISTORY.md` is not either. **Otherwise splitting content out could never satisfy the
bound**, since each split makes a new document smaller than what it was cut from. Both terms
are counted from the tree and **no constant is written anywhere**, because a number and the
arithmetic that justified it have to be edited together and the number wins by staying put. The
inequality says something: once the file you pay for on every turn costs more than any single
document you open on demand, the split has inverted. Measure both terms with

```bash
python -c "import pathlib;[print(f'{p.stat().st_size:>7}  {p}') for p in map(pathlib.Path,'CLAUDE.md docs/BRIEF.md docs/PUBLISHING.md tasks/TASK-WORKFLOW.md tasks/README.md .taskmd/config.md'.split())]"
```

**Tiers 2 and 3 carry no budget**, and that is deliberate rather than an omission: they are not paid
every turn, so a size limit there measures the wrong cost, and what constrains them is loading one at
a time. It accepts that `docs/BRIEF.md` and `docs/LESSONS.md` grow without limit. A tier-2 document
that starts loading on every turn has become tier 1, and this bound applies to it.

**This file is still over its own bound** — 15,226 bytes against `tasks/TASK-WORKFLOW.md`'s 11,925,
measured 2026-08-18 with the command above. That day's cuts took it **19,035 → 15,208, −20.1%**,
closing 57% of the debt before later edits added back: `CE-01` as
[T-143](tasks/T-143-split-the-release-chronology-out-of-claude-md.md) and `CE-04` as
[T-144](tasks/T-144-give-each-cumulative-rule-one-operative-home.md), both ranked in
[`docs/CONTEXT-AUDIT.md`](docs/CONTEXT-AUDIT.md) §6. **Those were the two cuts this bound was written
to make decidable, and both are spent** — what remains has no ranked finding behind it. That is dated
debt and not a rule already met. *This statement has now been wrong in both terms twice: it read
18,807 against `.taskmd/config.md`'s 14,087 when the smaller side had changed hands the same day, and
15,182 against 11,579 after a later session moved both and recorded the new pair in a task record
instead of here. **Re-measure both, never one**, and write it here in the same edit — a figure about
this file cannot be corrected anywhere else.*

## What this is

A publishable Claude Code plugin: **single-file HTML presentations that don't look generated**,
plus the prompt structure that briefs them and the critique pass that fixes them.

Grounded in a corpus of real decks, prompts and written style guides from a training programme.
`docs/BRIEF.md` records what that evidence shows and what to build; `reference/` holds the source
prompt — **one 1.2 KB file, and it is a prompt rather than a codebase**: nothing in it is code to
copy or behaviour to verify.

**What exists.** `python tools/deck/check.py <deck>` decides 84 of the 114 rules a gate owns and
names the other 30 with a reason each; `skills/htmldeck/references/build.md` plus `shell/` turn a
reviewed specification into a deck; `skills/htmldeck/references/critique.md` plus
`tools/deck/critique.py` are the review. **The repository is public at
`github.com/uchimata2/htmldeck`, `master` is the published branch, and the current version is
`0.4.0`.**

**When each of those landed, which release carried which fix, and which task found which defect are
[`docs/RELEASE-HISTORY.md`](docs/RELEASE-HISTORY.md)** — tier 3, loaded by nothing. It was this
section until 2026-08-14.

**A phase name is not a version number. `work_package` is the phase, `shipped_in` is the version, and
never write a phase with a `v`** — a task holding `PH3` and `0.2.1` at once is the rule working.
Conflating them nearly shipped a release no adopter could have installed: **L-69**. Which number a
*release* takes is [`docs/PUBLISHING.md`](docs/PUBLISHING.md) §8; which field a *task* carries is
`tasks/TASK-WORKFLOW.md` §3.

**The backlog is three release phases — `PH1`, `PH2` and `PH3`, and PH3 is the main line.**
[`docs/RELEASE-PHASES.md`](docs/RELEASE-PHASES.md) is the decision: what each phase contains, why the
second split was needed, and why the line between the last two falls at an effort estimate of `l`.
`tasks/README.md` is the current state, grouped by the same three names. **A new task belongs to one
of them**: `PH1` only when a defect in the published plugin reopens it — such a defect is a `PH1`
**phase** task, not a later improvement — `PH3` for anything `l` or `xl`, **and, since PH2 shipped,
for everything else that is not such a defect**, because reopening a shipped phase is reserved for
them. That last clause is why a small task can sit in the phase of the big ones. A phase that quietly
takes work the size of the next one is the failure both splits exist to prevent.

**A task's classification is this project's to make, not its filer's.** A report that arrives as
feedback because a contract behaves as written is still a defect when a published gate fails a deck
for using a class that contract defines. Re-derive the phase and the type from the rules above, and
log why they differ from what arrived.

**Read the brief first** — its "Decisions taken" section overrides anything older in it.

**The objectives are still being shaped.** Research is expected to be able to overturn scope, not
just fill it in. Findings that contradict the brief are surfaced as candidate changes of
direction, not quietly worked around.

## The rules that must survive

1. **Self-contained or it doesn't ship.** One `.html` that renders correctly with the network
   disabled. Every deck in the source corpus failed this — 2–7 external references each, mostly
   web fonts.
   *Measured and settled 2026-08-06:* this is no longer the main technical problem. A full
   12-slide deck with three embedded faces, icons, a motion library and SVG diagrams is **192 KB
   with zero external references** (`docs/research/R5-assets-and-licences.md`). Embedding is
   cheap, so `portable` is the default and the only shipping mode. A `linked` (CDN) mode exists
   **for the authoring loop only**; a deck delivered that way is a defect, and the critique pass
   says so.
2. **Portability is the constraint, not restraint.** No installation, no special privileges — the
   recipient double-clicks the file. It must render **glitch-free in recent Chrome/Edge**; other
   browsers degrade gracefully and mobile is secondary. Within that envelope, richness is wanted:
   interaction, animation and 3D. There is no JavaScript budget. The corpus habit of 1–3 script
   tags describes past work, not this.
3. **Use whatever renders best.** SVG, `<canvas>` and WebGL are all permitted, for diagrams
   included. Still never raster images, and never an *external* library — rule 1 settles that.
   When SVG is as good, prefer it: it scales, themes and diffs.
4. **One theme, every layer parametric.** Ship one fully-resolved look, not several and not a
   per-topic palette. Every value that could differ between themes is a token. Variety comes later,
   from a tool that generates new templates — design for it now, do not build it yet.
5. **Printing is optional.** A mode the user can force on, never a constraint on the design.
6. **Look at the rendered deck, and never read one whole.** A deck that validates is not a deck
   that reads well — so *look* means render it and open it, which nothing here replaces. It does
   **not** mean reading the file: the three shipped decks are 810,746 bytes, and a question about
   what is inside one is answered by a tool in `tools/deck/` or by a targeted search, never by
   opening the HTML.
7. **Critique is a first-class mode**, not a footnote. It is what turns a first draft into
   something worth presenting, and it is the part users cannot do for their own work.

## Voice

The critique mode is blunt on purpose — bottom line up front, then section by section, no
diplomatic padding. A review that opens with three compliments is one nobody acts on. This is a
deliberate choice carried from the corpus, where the harshest review was the most useful
artifact in it.

That applies to the critique output. The **decks** themselves stay respectful, positive and
professional, and avoid the terminology that marks text as machine-written — ship that list and
enforce it at build time rather than hoping.

## Working method

1. **No work without a task file** in `tasks/`, from `tasks/_task-template.md`. Tasks are tracked
   with the **taskmd** plugin, and `python tools/tasks/lint.py` is every check a task edit owes.
   `tasks/TASK-WORKFLOW.md` owns this project's conventions and `tasks/TOOLING.md` the commands;
   `.taskmd/config.md` is the schema and outranks any prose about the fields.
2. Lifecycle: `specify → plan → implement → review`.
3. What closes a task is `tasks/TASK-WORKFLOW.md` §7's checklist, which owns that bar.

## Publishing constraints

**The steps of a release, in order, are [`docs/PUBLISHING.md`](docs/PUBLISHING.md) §8.** Do not
re-derive the sequence from the last release's commits; that is what §8 was written to stop. **Step 1
is one command** — `python tools/check_all.py` — which discovers every checker a clone receives and
every deck this repository ships, and ends with a partition: each **ran**, **was skipped with a
stated reason**, or **failed**. A tool in none of those three fails the run. What it replaced, and
what its first run found that a hand-kept list could not, are §8 as well.

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
- **Font-licence aware.** If fonts are embedded, only ones whose licence permits redistribution.
  Record the licence next to each.
- **Humanized where a human reads it.** **No release ships until the human-facing text has been
  through the humanizer** — every release, not the first. The test is *what a stranger reads before
  installing anything*: today `README.md` and the repository description. **Plugin files are not
  human-facing and must stay AI-optimized** — the skill, this file, tool docstrings, commit messages
  and the task record — and a humanizer pass over them is a defect, not a courtesy. Deck copy is
  DS-106's, gated by `check.py`. The covered-set test, the exclusions and the owner's verbatim
  exception: [`docs/PUBLISHING.md`](docs/PUBLISHING.md), which is the rule and outlives any task.
  The first release's pass is recorded in
  [T-056](tasks/T-056-humanize-the-human-facing-documents-before-publishing.md); **every release
  after it runs the rule again.**

## Verifying

Test the generator on a **real 12-slide deck with diagrams**, not a three-slide toy — the corpus
decks are the target case, and that is the size where layout and pacing problems appear. State
results as what was actually produced, not as "works".

**12 is the floor, not the target.** Only the contents page has been built and printed above 13 —
at 17, 25 and 43 — and what is still known to bite above it is the ruler, which degrades to dense
mode past 16 and then marks where you are more quietly than it marks anything else
([T-178](tasks/T-178-dense-mode-drops-the-position-mark-below-the-section-marks.md)). Treat a long deck as
**untested territory** rather than as a longer version of a tested one, and say which length a
result was measured at. How the target moved, and off what evidence, is
[`docs/RELEASE-HISTORY.md`](docs/RELEASE-HISTORY.md) §4.

**And print it. One thing here can read the paper, and it reads two numbers.**
`tools/deck/printgeom.py` reads the card rectangles out of the printed PDF and asserts `PRINT-2` *no
two cards intersect* and `PRINT-3` *no card reaches the footnote*, on any deck it is pointed at,
standard library only. **It is two numbers and nothing wider**, and the fault it was written for
lives only in paged layout, which no screen measurement reaches (**L-76**). Whether the page reads as
a compact mode rather than as damage is still a person's, which is the 2026-08-08 ruling on DS-222 to
DS-226 and is untouched. Rule 6 is not satisfied by a screen render at any length, nor by a green
`PRINT-2`.
