---
id: T-074
title: The documented render command does not exist, and the tools write into their own install
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-073]
work_package: PH1
shipped_in: 0.1.4
owner: the project owner
business_value: high
effort: m
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - skills/htmldeck/references/build.md
  - tools/deck/render.py
  - tools/deck/paths.py
  - tools/plugin/check_scaffold.py
---

# T-074 — The documented render command does not exist, and the tools write into their own install

## 1. Specify

**Outcome**
Every command the skill tells a build to run is a command the tool accepts, proven on every run rather
than by someone hitting the traceback. And the shots that command produces land in the project being
built, not inside the installed plugin.

**The report**
From another project, 2026-08-10, building a twelve-slide executive deck end to end on the published
`v0.1.3`. [`skills/htmldeck/references/build.md:75`](../skills/htmldeck/references/build.md) gives the
per-batch render step as `render.py shots <slug>.html --out <dir>`. Run as written it crashes with
`ValueError: invalid literal for int() with base 10: '--out'`. Their words on why it is worth more
than a typo: the per-batch render *"is the only instrument that reaches"* the evaluation dimensions no
automatic check covers, so the failure lands *"at exactly the moment it is supposed to start
looking, and the cheapest wrong response is to skip the render and trust the checks that passed."*
Running it anyway found **seven geometry defects every automatic check had passed**.

**Reproduced by reading the parser, 2026-08-10.**
[`tools/deck/render.py:361`](../tools/deck/render.py) is `which = [int(x) for x in argv[2].split(",")]`,
so the third argument is a comma-separated list of 0-based slide indices and `--out` reaches `int()`.
There is no `--out`, and no output argument of any kind. The module docstring at
[`render.py:19`](../tools/deck/render.py) already shows the working form, so **the two disagree inside
one repository** and neither is gated.

**The defect underneath is where the output goes.** `render.py:40` is
`OUT = os.path.join(ROOT, ".assets-cache", "deck")` with `ROOT` derived from `__file__`. Invoked the
way `build.md` invokes it — `${CLAUDE_PLUGIN_ROOT}/tools/deck/render.py` — `ROOT` **is the installed
plugin**, so an adopter's shots are written into the plugin cache rather than into the deck's own
project: a directory that is not theirs, is not in their repository, and a reinstall erases. The same
anchor is in [`printpages.py:41`](../tools/deck/printpages.py), [`theme.py:39`](../tools/deck/theme.py)
and [`contract.py:352`](../tools/deck/contract.py), all three reachable from `build.md` or
[`critique.md`](../skills/htmldeck/references/critique.md). The `--out` in the documentation is
therefore not a hallucinated flag so much as **the flag the pipeline needed and nobody built**, which
is why deleting it from the prose is the smaller half of this fix.

**Why nothing caught it**
[`refcheck.py`](../tools/docs/refcheck.py) validates repo-relative paths and `<document> §n`
references, `taskmd check` validates the task record and markdown links, and `figures.py` validates
quoted measurements. **No gate reads a documented command and asks the tool whether it would accept
it.** The skill's references carry 13 such invocations; one is wrong and the other twelve are correct
by luck rather than by construction. The instance is one line of `build.md`; the missing rule is that
**a documented invocation is a claim like any other** and belongs to a gate.

**Scope**
- In: `render.py` gains a real output argument, defaulting to today's location so nothing that works
  now changes, and `build.md:75` becomes true as written.
- In: **an output root an adopter can point at their own project**, applied to the tools an adopter
  actually runs — `render.py`, `printpages.py`, `theme.py`, `contract.py`. The variants and probe
  scripts are development-only and stay anchored to the repository.
- In: **a gate over documented invocations.** Every `${CLAUDE_PLUGIN_ROOT}/tools/**.py` command line
  in `skills/htmldeck/**` is parsed and offered to the tool it names, and one the tool would reject
  fails the run. It decides all 13, not the one that was reported.
- In: a fixture that fails before the fix (**L-04**) — the pre-fix `build.md` line is the fixture.
- Out: the invocations in `docs/` and `tasks/`, which are development commands run from the
  repository root where `ROOT` is already right. If the gate can cover them free, it may; they are
  not what this task is for.
- Out: DS-064, which the same report raised and which is [T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md).

**Inputs**
- `skills/htmldeck/references/build.md`, `skills/htmldeck/references/critique.md`
- `tools/deck/render.py`, `tools/docs/refcheck.py`

**Acceptance criteria**
- [ ] The command at `build.md:75` runs, copied verbatim, against a deck outside this repository
- [ ] Shots from a plugin-root invocation land in the target project, not in the plugin install
- [ ] Today's invocation with no output argument still writes where it writes now
- [ ] A seeded wrong flag in a documented command fails the gate, shown before the fix
- [ ] All 13 documented invocations are decided by the gate, and a 14th added anywhere in
      `skills/htmldeck/**` is decided without editing a list by hand
- [ ] `render.py`'s docstring and `build.md` say the same thing, and the gate is what holds them together

**Open questions**
- **Which release?** This is a defect in the published `v0.1.3`, so `PH1` and a patch. The output-root
  half is larger than a patch usually carries, and splitting it would ship a correct sentence over a
  tool that still writes into its own install. Recommended: one patch, both halves — the owner's call.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | The gate first, failing on the shipped `build.md` | The failing run |
| 2 | Give `render.py` the output argument, default unchanged | `tools/deck/render.py` |
| 3 | Apply the same root to `printpages.py`, `theme.py`, `contract.py` | Those three |
| 4 | Correct `build.md:75`; confirm the gate goes green for the right reason | `build.md`, the green run |
| 5 | Run the full gate set, and the reference deck end to end | The measurements |

## 3. Implement

**Decisions & assumptions**

- **The output root follows the deck, and the rule is the deck's nearest `.git` ancestor — 2026-08-10.**
  `paths.output_root` is the one home for it, beside `display_path`, because both answer *where is
  this path, relative to what* and both exist because the tool's own directory was the wrong answer.
  A deck inside this repository resolves to this repository, so **every path that worked before is
  unmoved** and the development suites keep `render.OUT`; a deck in someone else's project resolves
  to theirs; a deck under no repository falls back to its own directory, never to the tool's. Both
  ends are asserted in `paths.self_test` against the tool's own location rather than a literal, so
  the fixture still means something in a clone somewhere else.

- **The probe was the worst of the four writes, and it is not in the task's scope as written.**
  `make_probe` writes a **whole copy of the deck** — an adopter's content, their client's content —
  into the installed package. The scope named shots, PDFs and themed decks; the copy is the same
  defect and was fixed with them rather than left for a second patch.

- **`printpages.self_test` now uses `tempfile`.** It wrote a two-page PDF into the tool's own
  directory to prove its reader could count pages. That is a self-test that fails on any read-only
  install, and the platform's temporary directory is where a temporary file belongs.

- **The command gate lives in `check_scaffold.py`, not in `refcheck.py` as the task said.** The
  deliverable list is corrected. `refcheck.py` decides whether a *pointer* resolves;
  `check_scaffold.py` decides whether the shipped **package** is sound, and a documented invocation
  is a fact about the package. It also already had the fixture harness this needed. Check 7 reads
  only inside fenced blocks — which is exactly where checks 4 and 5 deliberately do not look, so
  until now the one part of a skill file meant to be executed verbatim was the part nothing read.

- **The check decides three things and says which three.** The tool exists; the subcommand exists;
  every flag exists — each as a **whole string literal** in that tool's source. It does not decide
  that the tool would accept the whole line: positional arity, flag order, and whether a flag is
  valid for a given subcommand are beyond a static read, and running the line for real would launch
  Chrome. All four defects this family has produced were a flag or a subcommand the tool had never
  heard of, which is the shape it does decide.

- **Its own first version passed the defect it was built for, and that is why it tokenises.** The
  check searched the raw source for the flag between quotes. Seeded against a `render.py` with
  `--out` removed, it went green: `'--out'` was still in the file, **in a comment quoting the
  traceback the missing flag produces** — a comment this task had written. `literals()` now walks
  `tokenize`, keeps `STRING` tokens, drops triple-quoted ones, and matches whole values, so a
  mention is no longer an implementation (**L-36**). The fixture *a flag mentioned in a comment is
  not a flag the tool has* is that failure, kept.

- **The README's pasted `14 of 14` was caught by `figures.py`, not by me.** Five new fixtures made
  it 19, and the figure check refused its own self-test until the README matched. That is the gate
  working exactly as T-060 intended, on the first change that moved one of its numbers.

**Outputs produced**
- [`tools/deck/paths.py`](../tools/deck/paths.py) — `output_root`, and two assertions for it
- [`tools/deck/render.py`](../tools/deck/render.py) — `out_dir`, `--out` parsed before the slide
  list, `make_probe`/`measure`/`cmd_shots`/`cmd_measure` writing under the deck
- [`tools/deck/printpages.py`](../tools/deck/printpages.py),
  [`tools/deck/theme.py`](../tools/deck/theme.py),
  [`tools/deck/contract.py`](../tools/deck/contract.py) — the same root for the PDF, the themed copy
  and `contract.json`
- [`tools/plugin/check_scaffold.py`](../tools/plugin/check_scaffold.py) — check 7, `literals`, five
  fixtures
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md), [`README.md`](../README.md),
  [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-58**

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The command at `build.md:75` runs, copied verbatim, against a deck outside this repository | **met** | A copy of the reference deck in a scratch directory: `render.py shots my-deck.html --out <dir>` rendered all 13 slides; `... 0,4 --out <dir>` rendered two. Both printed the destination given |
| Shots from a plugin-root invocation land in the target project | **met** | Invoked by absolute path from outside the repository, with no `--out`, the run wrote to `<the deck's directory>/.assets-cache/deck` |
| Today's invocation with no output argument still writes where it writes now | **met** | Every suite and gate in the repository ran unchanged, all writing to `.assets-cache/` at the repository root |
| A seeded wrong flag fails the gate, shown before the fix | **met** | With `"--out"` renamed in `render.py`: `UNKNOWN FLAG skills/htmldeck/references/build.md: --out is documented for tools/deck/render.py, which has no such literal`. Restored, the run is clean |
| All 13 documented invocations decided, and a 14th decided without editing a list | **met** | The check reads every fenced block of every `.md` under `skills/`, so a new command is decided by being written |
| `render.py`'s docstring and `build.md` say the same thing, held together by the gate | **met** | Both now show the `--out` form; the docstring's examples are checked by nothing, but the prose the skill loads is |
| Every other gate still green | **met** | Reference deck `113 / 82 / 0 / 4 / 27`, `0 failure(s)`, unchanged · seeded deck `4 failure(s)` unchanged · `static 24 of 24` · `contract 8 of 8` · `content 3 of 3` · `deliverable 7 of 7` · `critique 12 of 12` · `check_scaffold 19 of 19` · `taskmd` · `refcheck` · `figures 0 stale` |
| The deck opened and looked at (**L-01**) | **met** | Slide 5 of the relocated render, from a directory outside the repository, examined offline: ledger rows, icons, the disclosure control, the multi-source mark, counter and bottom line all correct |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | **Shipped in `v0.1.4`. Both halves in one patch, on the owner's call, and the second is the one that mattered.** The flag now exists and the documented line runs verbatim; underneath it, every tool that writes anything anchored that write to its own `__file__`, so an adopter running the documented pipeline put screenshots, PDFs, themed decks **and a full copy of their deck** inside the installed package. `paths.output_root` follows the deck instead, and every path inside this repository is unmoved because a deck here resolves to here. The rule-level half is check 7: a documented invocation is a claim, and it was the only kind this package made that nothing decided. **The check's own first version passed the defect it was built for** — the flag was still in `render.py`, in a comment quoting the traceback — which is why it tokenises and matches whole literals, and which is kept as a fixture. Generalised as **L-58**. |
| 2026-08-10 | → in_progress | Started after [T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md), the other half of the same report, closed. |
| 2026-08-10 | → proposed | **Reported from another project against the published `v0.1.3`, and reproduced by reading the parser rather than by running it.** `argv[2]` is parsed as a slide list, so the documented `--out` reaches `int()`; `render.py`'s own docstring already shows the working form, so the repository contradicts itself in two files and neither is gated. **The larger finding is underneath the flag**: `OUT` is anchored to `__file__`, so every adopter running the documented pipeline writes shots, PDFs and themed decks into the installed plugin. That makes `--out` the flag the pipeline needed rather than a flag that never existed, and it is why the fix is not a prose edit. `PH1` because the broken command is the one that closes the visual gate, and the reporter names the cheap wrong response — skip the render, trust the checks — as the likely one. |
