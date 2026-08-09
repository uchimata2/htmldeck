# htmldeck — working conventions

Read this before doing anything in this folder.

## What this is

A publishable Claude Code plugin: **single-file HTML presentations that don't look generated**,
plus the prompt structure that briefs them and the critique pass that fixes them.

Grounded in a corpus of real decks, prompts and written style guides from a training programme.
`docs/BRIEF.md` records what that evidence shows and what to build; `reference/` holds the source
prompt. **Status: the research is complete; the plugin scaffold exists and runs its own pipeline**
(`.claude-plugin/`, `skills/htmldeck/`), **and as of 2026-08-09 the build check, the theme contract,
the component contract, the editorial split rule and build mode are all built** — `python
tools/deck/check.py <deck>` decides 81 of the 113 rules a gate owns and names the other 32 with a
reason each, `skills/htmldeck/references/build.md` plus `shell/` turn a reviewed specification into a
deck, and `skills/htmldeck/references/critique.md` plus `tools/deck/critique.py` are the review.
**`examples/sort-window/` is the first deck nobody authored by hand.** What v0.1 still needs is the
humanizer pass and publication. Read the brief first — its "Decisions taken" section overrides
anything older in it.

**The backlog is two release phases, set 2026-08-09 by the owner: `v0.1` and `v0.2`.** v0.1 is a
working plugin someone can install — build mode, critique mode, the humanizer pass, publish — and
nothing else; v0.2 carries everything already known and deliberately not held for. `docs/BRIEF.md`
*Release phases* is the decision and says what each contains; `tasks/README.md` is the current
state, grouped by the same two names. **A new task belongs to one of them**, and putting work in
v0.1 that a first release does not need is the failure this split exists to prevent.

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

1. **No work without a task file** in `tasks/`, from `tasks/_templates/task-template.md`.
2. Lifecycle: `specify → plan → implement → review`.
3. A task is `done` only when its deliverables exist, its log is current, and any deck it
   produced has been **opened and looked at** — offline.

## Publishing constraints

This repository goes to GitHub. Everything written here must be:

- **Free of personal, client and machine data.** The source corpus is training work for real
  named scenarios; **do not copy deck content into this repository.** Patterns, structure and
  measurements only. Any example deck shipped here must be written fresh on a neutral topic.
- **Out-of-the-box.** Clone and run, no path editing.
- **Font-licence aware.** If fonts are embedded, only ones whose licence permits redistribution.
  Record the licence next to each.
- **Humanized where a human reads it.** **No release ships until the human-facing text has been
  through the humanizer** — every release, not the first. The test is *what a stranger reads before
  installing anything*: today `README.md` and the repository description. **Plugin files are not
  human-facing and must stay AI-optimized** — the skill, this file, tool docstrings, commit messages
  and the task record — and a humanizer pass over them is a defect, not a courtesy. Deck copy is
  DS-106's, gated by `check.py`. Detail and the owner's exception:
  [T-056](tasks/T-056-humanize-the-human-facing-documents-before-publishing.md), which gates
  publication until it lands.

## Verifying

Test the generator on a **real 12-slide deck with diagrams**, not a three-slide toy — the corpus
decks are the target case, and that is the size where layout and pacing problems appear. State
results as what was actually produced, not as "works".
