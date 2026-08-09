# Build mode

Load this at stage 6, once the slide-by-slide specification has been reviewed. It is **how a deck
gets written**; what makes a deck good is `${CLAUDE_PLUGIN_ROOT}/docs/DESIGN-SYSTEM.md`'s job and
nothing here repeats it.

**The input is a reviewed `<slug>.slides.md`, not a brief.** Seven fields per slide are already
decided. This stage composes them; it does not invent narrative.

---

## 1. Start from the shell, never from a blank file or another deck

Roughly 170 KB of every deck is the same deck — three embedded faces, the shared component block,
the script, the chrome, the reading view. It is not authored, it is assembled:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py new <slug>.html \
    --title "<the deck's name>" --subtitle "<one line: who, when, and any illustrative-subject note>"
```

That writes a deck with the shell in place and no slides. **Do not copy
`${CLAUDE_PLUGIN_ROOT}/examples/reference-deck.html` and edit it** — it is the structural reference,
and a copy carries twelve slides of someone else's content plus a `<style id="slides">` composition
written for them.

Then set the argument's stages, which the ruler and the printed contents page both render. They come
from the outline in `<slug>.foundation.md`, and they are declared in the deck's own script — the
three `var` lines at the top, `DECK`, `STAGES` and `STAGE_ICON`. Every stage icon must exist in
`${CLAUDE_PLUGIN_ROOT}/shell/icons.svg`; look at the set before choosing:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py icons --sheet <somewhere>.svg
```

**Never draw an icon** (DS-112). If the set has nothing for a concept, use the nearest one that is
honest rather than invent path data.

## 2. Write the slides, in batches of three

Three slides, then the loop in §3, then the next three. **Batching is not about scoring** — it is
that components are built once and reused, so a defect found in batch one is fixed once rather than
in twelve places.

Per slide, the parts and their attributes are `${CLAUDE_PLUGIN_ROOT}/docs/COMPONENT-CONTRACT.md`
§3.2–§3.8, and `component.py check` decides them. Read it before the first slide. Three things it
will not tell you, because they are this stage's judgement:

- **The `<style id="slides">` block is yours to write and it is the only CSS you write.** Composition
  goes there — a ledger's tracks, a stat's split, a closing slab. **The shared component block is not
  yours**: adding a rule to it is caught by `shell.py check`, and it means a second deck will inherit
  a layout written for this one.
- **Every value that could differ between themes is a token.** No colour, length, duration or easing
  curve outside the theme region; `theme.py check` fails one and names it under DS-010.
- **Tier two is a decision, not a leftover.** Every `.disc` declares its kind in `data-disc` —
  `derivation` · `scope` · `condition` · `instances`, and no fifth (DS-230). If what is behind the
  click is none of those four, it belongs on the slide or nowhere. A bottom line may never depend on
  a figure that lives only behind the click (DS-231).

Sync the sprite whenever a batch introduced an icon — it keeps DS-113 true by construction:

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py icons <slug>.html --set <concept>=<lucide-name>
```

## 3. The per-batch loop

Run all five on the batch. The first two are cheap and catch the expensive mistakes.

```
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/shell.py check <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/component.py check <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/theme.py check <slug>.html
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/check.py <slug>.html [--sources <dir>]
python ${CLAUDE_PLUGIN_ROOT}/tools/deck/render.py shots <slug>.html --out <dir>
```

Then score **S3 Encoding · S5 Craft · S6 Motion** on the batch's slides, per
`${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md`. **And look at the shots.** A deck that passes every
check can still be a deck nobody can read; that is why the render step is in the loop and not at the
end.

**Batch loops do not count against the iteration cap.** The cap is 3 and it counts whole-deck
rounds — a four-batch deck counting batch loops would exhaust it before the deck existed.

## 4. When the specification cannot be built

A slide that will not fit the stage, or that a `hard` rule fails on, cannot be built as written.
**Resolve it here.** This stage holds implementation authority above the detailed specification, and
returning the decision to a user who cannot picture the outcome is not an option — nor is shipping a
non-conformant slide, nor looping on one.

Two obligations come with that authority, and the first is the one under pressure to produce a deck:

1. **Write the deviation back into the artifact it contradicts** — `<slug>.slides.md`, and
   `<slug>.foundation.md` too when the outline moved. Those files exist to be what a reader opens
   when the deck turns out wrong, which they are not if they record only the intent.
2. **Tell the user at delivery, as brief bullet points.** One line each, no rationale per item.

**This is not the exit for everything.** `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §6.1 keeps its
two: **STALL** — a design decision wearing a finding's clothes — escalates, and **OSCILLATION** —
two rules genuinely in tension — stops and names them. Deviation authority is for what this stage
*can* resolve.

## 5. Delivery

Stop when `${CLAUDE_PLUGIN_ROOT}/docs/EVALUATION.md` §5 says the deck is done, not when it feels
finished. Then hand over:

- **The deck and both specification files**, in the delivery directory, per
  `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/artifacts.md`.
- **The deviation bullets** from §4, if there were any.
- **What printing does and does not do** — three sentences, and
  `${CLAUDE_PLUGIN_ROOT}/skills/htmldeck/references/pipeline.md` has them. Say them once, at
  handover, never on the deck's own surface.
- **Which half was checked.** A run with no sources is presentation-only and has to say so; a
  presentation-only check presented as a clean pass is a false one. If such a run needed a figure, it
  ships marked as a placeholder for the author to replace, or it does not ship.

**A clean gate is not a good deck.** Five of the ten dimensions are invisible to every check above,
so the run is not over when the tools go quiet.
