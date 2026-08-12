# htmldeck — working conventions

Read this before doing anything in this folder.

## What this is

A publishable Claude Code plugin: **single-file HTML presentations that don't look generated**,
plus the prompt structure that briefs them and the critique pass that fixes them.

Grounded in a corpus of real decks, prompts and written style guides from a training programme.
`docs/BRIEF.md` records what that evidence shows and what to build; `reference/` holds the source
prompt — **one 1.2 KB file, and it is a prompt rather than a codebase**: nothing in it is code to
copy or behaviour to verify. It was described as working prior art until 2026-08-09, which it never
was. **Status: the research is complete; the plugin scaffold exists and runs its own pipeline**
(`.claude-plugin/`, `skills/htmldeck/`), **and as of 2026-08-09 the build check, the theme contract,
the component contract, the editorial split rule and build mode are all built** — `python
tools/deck/check.py <deck>` decides 84 of the 115 rules a gate owns and names the other 31 with a
reason each, `skills/htmldeck/references/build.md` plus `shell/` turn a reviewed specification into a
deck, and `skills/htmldeck/references/critique.md` plus `tools/deck/critique.py` are the review.
**`examples/sort-window/` is the first deck nobody authored by hand.** The humanizer rule landed
2026-08-09 as `docs/PUBLISHING.md`, and **PH1 shipped the same day as `0.1.0`**: the repository is
public at `github.com/uchimata2/htmldeck`, released and **now at `0.2.2`** after six PH1 patches,
with `master` as the published branch. **PH2 shipped 2026-08-11 as `0.2.0`** carrying
[T-086](tasks/T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md) and
[T-087](tasks/T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md), and
**the phase stays open behind it**: T-036 keeps the `PH2` label by the owner's decision, so a
shipped release and an open phase are not a contradiction here. T-080 kept it too until it closed on
2026-08-12.

**A phase name is not a version number, and conflating the two nearly shipped a release nobody could
install.** The backlog calls a defect in the published plugin PH1 work, which is a *phase*; the
record then wrote the next such release as `v0.1.6`, which as a *version* is lower than the published
`0.2.0`. Plugin updates compare versions, so that tag would have reached no adopter at all. **Patches
take the next patch number on the published line** — `0.2.1`, `0.2.2` — whatever phase the tasks in
them belong to. Settled 2026-08-11, at the release it would have broken.

**The phases were called `v0.1`, `v0.2` and `v0.3` until 2026-08-12 and are now `PH1`, `PH2` and
`PH3`** — same three phases, renamed because a label shaped like a version gets read as one, which is
what the paragraph above is about. The rule the rename makes visible: **`work_package` is the phase,
`shipped_in` is the version**, and a task can hold `PH3` and `0.2.1` at once without contradiction.
Never write a phase with a `v`. **T-099.**

**PH3 is the main line now, but PH1 has reopened eight times**: a defect in the published plugin is
a `PH1` **phase** task, not a later improvement. **`0.2.2` shipped four of them 2026-08-12** —
[T-101](tasks/T-101-theme-py-self-test-fails-for-every-plugin-install.md),
[T-102](tasks/T-102-data-stage-is-an-index-and-the-contract-does-not-say-so.md),
[T-103](tasks/T-103-build-md-drops-ds-105s-link-clause-for-a-single-source-slide.md) and
[T-105](tasks/T-105-fig-pos-neg-caution-are-vocabulary-so-a-real-deck-fails-for-using-them.md), all
four from the adopting project. **`0.2.1` shipped three on 2026-08-11** —
[T-090](tasks/T-090-spec5-cannot-parse-a-descriptive-slide-label.md),
[T-091](tasks/T-091-build-md-documents-icons-set-as-a-single-pair.md) and
[T-094](tasks/T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md). T-090 and T-091 were
the first ever **raised from outside this repository**, hit on the
published `0.2.0` by the first adopting project and moved here from the `PH3` they arrived labelled
with; T-094 is the project's own, found while rendering a deck to look at it. **T-105 is the first
this phase took over its filer's own classification**: it arrived as feedback because the contract
behaves as written, and a published gate that fails a deck for using a class the contract defines is
a defect in the check whatever the report calls it. **The fifth
was the first nobody reported** — `v0.1.5` carried
[T-083](tasks/T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md) and
[T-085](tasks/T-085-the-reference-deck-does-not-carry-the-shell-it-defines.md), both found by running
[`docs/PUBLISHING.md`](docs/PUBLISHING.md) §8's gate list rather than by an adopter — which is the
argument for having written that list down. Read the brief first — its "Decisions taken" section overrides anything older
in it.

**The backlog is three release phases, all set by the owner: `PH1` and `PH2` on 2026-08-09, and
`PH3` split off PH2 on 2026-08-10.** PH1 is a working plugin someone can install — build mode,
critique mode, the humanizer pass, publish — and nothing else, and it has shipped. PH2 is the
dependencies and every minor and moderate fix; PH3 is the bigger tasks and the new capabilities,
and **the line between those two falls at an effort estimate of `l`**. `docs/BRIEF.md` *Release
phases* is the decision and says what each contains; `tasks/README.md` is the current state, grouped
by the same three names. **A new task belongs to one of them**: PH1 only when a defect in the
published plugin reopens it, PH3 for anything `l` or `xl` — **and, since PH2 shipped, for
everything else that is not such a defect**, because reopening a shipped phase is reserved for them.
That last clause is why a small task can sit in the phase of the big ones; T-089, T-092 and T-093 are
all there against their size. A phase that quietly takes work the size of the next one is the failure
both splits exist to prevent.

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
6. **Look at the rendered deck.** A deck that validates is not a deck that reads well.
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
   with the **taskmd** plugin: `taskmd check` validates the record, `taskmd index` regenerates it,
   and `python tools/docs/refcheck.py` validates every reference in every document.
   `tasks/TASK-WORKFLOW.md` owns this project's own task conventions and how to invoke all three;
   `.taskmd/config.md` is the schema and outranks any prose about the fields.
2. Lifecycle: `specify → plan → implement → review`.
3. A task is `done` only when its deliverables exist, its log is current, and any deck it
   produced has been **opened and looked at** — offline.

## Publishing constraints

**The steps of a release, in order, are [`docs/PUBLISHING.md`](docs/PUBLISHING.md) §8.** Do not
re-derive the sequence from the last release's commits; that is what §8 was written to stop. **Step 1
is one command** — `python tools/check_all.py` — which discovers every checker a clone receives and
every deck this repository ships, and ends with a partition: each **ran**, **was skipped with a
stated reason**, or **failed**. A tool in none of those three fails the run. It replaced a
hand-kept list of sixteen commands on 2026-08-13 (**T-096**); that list had missed three red checks
the day it was written, and its first replacement run found three suites nobody had wired and a
printed page count no gate reached.

This repository goes to GitHub. Everything written here must be:

- **Free of personal, client and machine data.** The source corpus is training work for real
  named scenarios; **do not copy deck content into this repository.** Patterns, structure and
  measurements only. Any example deck shipped here must be written fresh on a neutral topic.
- **Committed under the publishing identity**, `uchimata2 <112070643+uchimata2@users.noreply.github.com>`,
  set in this repository's local git config. The personal address was rewritten out of all 121
  commits before the first push and **must not come back** — history is public now, so a single
  commit carrying it cannot be undone the way the first rewrite could.
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

**12 is the floor, not the target, and the target moved on 2026-08-13.** The first adopting project
presented a 13-slide deck and reported the constraint as the problem: the material needed far more
room than 12 slides, a peer presented **43**, and the next deck from the same sources will be much
longer. **Nothing here has ever been built or measured above 13.** What is already known to bite
above it: the printed contents page collides at 13
([T-116](tasks/T-116-the-printed-contents-page-collides-at-thirteen-entries.md)), a second contents
sheet does not exist ([T-036](tasks/T-036-the-second-contents-page-for-long-decks.md)), and the
ruler degrades to dense mode once the slide count passes a capacity the controls' width decides
([T-114](tasks/T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md)). Treat a long deck as
**untested territory** rather than as a longer version of a tested one, and say which length a
result was measured at.
