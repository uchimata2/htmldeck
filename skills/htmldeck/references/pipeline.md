# The run shape

Load this at the start of every build run. It is the sequence, the hand-offs and the two gates —
nothing about what a good deck looks like, which is
`${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md`'s job.

```
governing idea ─→ requirements ─→ foundation spec (carries the outline) ─→ OUTLINE SIGN-OFF
    └─→ slide-by-slide spec ─→ spec review ─→ DETAILED-SPEC SIGN-OFF
        └─→ build, in batches ─→ build review ─→ owner review ─→ fix
```

**Two of the four reviews happen before any HTML exists, and that is the point.** Six of the ten
rubric dimensions are checkable against a specification — S1 Claim, S2 Evidence, D1 Spine, D2
Pacing, D3 Close, and the source-reconciliation half of D4 — and three of those are among the five
no mechanical check can reach. The most expensive defects are catchable at the cheapest moment.

**Each gate immediately follows the artifact it gates and immediately precedes the expansion of
it.** A slide cut at the outline costs three fields; the same slide cut after the specification
costs seven fields times every slide around it, and after the build it costs HTML.

---

## The two rules that hold across every stage

1. **The specification files are always written.** Both of them, on every run, including one where
   the user declines both gates. A file costs the user nothing until they open it, and it is the
   only trace of what was decided when the deck later turns out wrong. See `artifacts.md`.
2. **The gates are optional and independently so.** Both, one, or neither — whatever the user asked
   for. Unprompted, both are on. **Never ask which**; asking would be a third question, and the
   promise this plugin is built on is two.

---

## Stage 1 — Governing idea

**In:** the two answers, plus anything the user pointed at.
**Out:** one sentence, written before anything else. It becomes the first line of the foundation
spec.

Not a gate, and not shown to the user on its own. It costs one sentence and it is what stops the
deck acquiring six things it is about.

## Stage 2 — Requirements

**In:** the two answers, plus any supplied sources.
**Out:** six sections, filled in — never asked for, section by section or at all.

| Section | Filled from |
| :--- | :--- |
| **Role** | Who the author is being. Inferred from the topic and the audience. |
| **Context** | What happened before this deck; where the content came from. The sources, if any. |
| **Goal** | One sentence, transformational not descriptive. The governing idea, restated as an outcome. |
| **Requirements** | What the audience must believe or do afterwards. |
| **Format** | Single-file HTML; the length from question 1; respectful, positive, professional. |
| **Resources** | The source documents from question 2, by path. Empty is a legitimate state. |

**When sources are supplied, read them here.** Every figure that will reach a slide has to come from
one, and the reconciliation table — every figure, its origin, every place it is reused — is built at
this stage, not at review time.

**When they are not, the run is presentation-only, and that changes what a figure may do.** A
presentation-only run **may not invent a number and let it read as measured.** Any figure it needs
is either marked on the slide as a placeholder the author must replace, or it does not ship. Record
which in the foundation spec and say it again when the deck is delivered — an unmarked invented
figure is the S2 Evidence failure, and it is the one a presentation-only run cannot catch for
itself, because there is nothing to check it against.

## Stage 3 — Foundation spec

**In:** the governing idea and the requirements.
**Out:** the foundation spec on disk, including its **outline** section. Template in `artifacts.md`.

**It is a selection sheet, not a design document.** One theme is already fully resolved, so the
per-deck content is: the governing idea, the narrative spine, the archetypes and elements this deck
selects, and any per-deck additions to the quality bar. **It cites
`${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md`; it never restates it.**

The outline names, per slide and at minimum: **archetype · title · bottom line** (DS-211). The
bottom line in the outline is the same sentence that ships on the slide — not a paraphrase of it.
Load `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md` §3.2 for the thirteen archetypes and §3.4 for
what a bottom line owes the audience.

## Gate 1 — Outline sign-off

**Show:** the outline section only — the governing idea, the spine, and the per-slide
archetype · title · bottom line. Not the whole foundation spec, and not the reasoning.

**Ask for:** cuts, additions, reordering, and any bottom line that is wrong. This is the cheap place
to lose a slide, and losing one here is a success, not a setback.

**Declined:** proceed straight to stage 4. The foundation spec is written either way.

## Stage 4 — Slide-by-slide specification

**In:** the signed-off outline.
**Out:** the slide-by-slide specification on disk. Template in `artifacts.md`.

Seven fields per slide: **structure · text · visuals · animations · interactive elements · title ·
bottom line**. Expanded from the outline **page by page, never in one pass** (DS-212) — the
one-pass version reads like a list of slides rather than an argument, and it is where the spine
quietly breaks.

## Stage 5 — Specification review

**In:** the slide-by-slide specification.
**Out:** findings as `ID · Severity · Slide · Finding · Fix`, with Major/Minor/Note, then
**"Open — needs a decision"**, then counts.

**This is critique mode's first format**, not a mode of its own — load
`${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/critique.md`. It scores what a specification can
carry: **S1 Claim · S2 Evidence · D1 Spine · D2 Pacing · D3 Close · D4 source-reconciliation.**
It does not score S3 Encoding, S4 Density, S5 Craft, S6 Motion or D4's visual half — those need a
rendered artifact and are the build review's.

Blunt, bottom line up front, no diplomatic padding. **This is the critique voice; the deck's own
voice is the opposite** and stays respectful, positive and professional.

## Gate 2 — Detailed-spec sign-off

**Show:** the review's findings and, first, its **"Open — needs a decision"** items. Those are the
reason this gate is here.

**Ask for:** a decision on each open item, and on anything the review marked Major that the user
would rather leave. Not approval of the specification as a whole — that is what the outline gate
already covered, and asking twice teaches the user to wave both through.

**Declined:** apply the review's own fixes, record the open decisions in the specification file as
open, and proceed. **Do not guess an open decision closed** — write it down as unresolved so the
file says what was never settled.

## Stage 6 — Build, in batches

**In:** the reviewed slide-by-slide specification. **Not a brief.**
**Out:** the deck.

**Load `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/build.md`** — how the deck is assembled,
what this stage may decide for itself, and the loop below stated in commands.

Build a few slides, run the cheap loop on them, then continue. Batching is not about scoring — it
is that interaction patterns are built once and reused, so **a component defect found in batch one
is fixed once instead of in twelve places**.

**Per batch:** the automatic checks, the render check, and S3 · S5 · S6 on the batch.
**Batch loops are not measurement rounds and do not count against the iteration cap** — the cap is
3 and it counts whole-deck rounds; a four-batch deck counting batch loops would exhaust it before
the deck existed.

## Stage 7 — Build review, then the owner

**In:** the whole deck.
**Out:** a converged deck, then the user's own review.

The whole-deck measurement round is `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §6, including the
fresh-context judgement pass. **It runs before the user sees the deck, not after** — the corpus pipeline puts the machine
review second and the human third.

**The user is shown the outcome and the findings, never the numbers.** A dimension at 0 or 1 reaches
them as a finding naming the dimension.

### Handing it over — say what printing does and does not do

The deck prints. **Say so once, with its two limits, when you hand the deck over** — a printable
mode whose limits are discovered on paper is worse than one that states them, and the person who
needs to hear it is the one *about to* print, not the one holding the pages. Not on the deck's own
surface: that would be print-only chrome on the stage.

Three sentences, no more:

- **It prints as slides — one per page**, at the deck's own 16:9 page size rather than A4. The
  print dialog's layout controls will be greyed out, because here the page shape is the design.
- **Everything behind a disclosure control stays on screen.** The panels are overlays on a fixed
  slide, so they cannot open onto paper without covering what they explain; the control is hidden
  in print too rather than advertising detail the page cannot reach. Read those on screen.
- **Turn headers and footers off in the print dialog.** Chrome's default prints the file's full
  local path across the foot of every page — someone else's directory layout on paper. It is not
  reachable from CSS, so it can only be warned about.

---

## What this scaffold does not build

Each stage above names what it produces; several of them are thin until the task that owns them
lands. Stated so a run is not mistaken for a finished plugin:

| Stage | Owned by | Until then |
| :--- | :--- | :--- |
| 5 · spec review, 7 · build review | ~~Critique mode~~ — **built 2026-08-09.** `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/critique.md` fixes both report formats, and `python ${CLAUDE_PLUGIN_ROOT}/tools/deck/critique.py <deck>` assembles the half a program can. | — |
| 6 · build | ~~Build mode~~ — **built 2026-08-09.** `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/build.md` is the stage, and `${CLAUDE_PLUGIN_ROOT}/shell/` plus `python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py` are what a deck is assembled from. | — |
| 6 · per-batch automatic checks | ~~The build check~~ — **built 2026-08-09.** `python ${CLAUDE_PLUGIN_ROOT}/tools/deck/check.py <deck> [--sources <dir>] [--print-pages] [--json]` gates 82 of the 113 rules the ruleset puts in its jurisdiction and **names every one of the other 31, with a reason**. | — |
| 6 · tokens, components, motion | The theme and interaction layers | `${CLAUDE_PLUGIN_ROOT}/examples/reference-deck.html` carries a working first instance of both, and `${CLAUDE_PLUGIN_ROOT}/shell/` is that instance with the content cut out. |
