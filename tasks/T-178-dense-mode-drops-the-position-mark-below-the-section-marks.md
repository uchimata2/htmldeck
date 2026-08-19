---
id: T-178
title: In dense mode the current-position mark is half the size of the section marks, and the ring is gone
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-035, T-114]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-18
updated: 2026-08-19
deliverables:
  - shell/components.css
  - tools/deck/longdeck.py
  - tools/deck/rulerstrip.py
  - docs/lessons/L-123.md
---

# T-178 — In dense mode the current-position mark is half the size of the section marks, and the ring is gone

## 1. Specify

**Outcome**
Past the ruler's capacity bound, *where am I* is still the loudest thing on the ruler. Today it is
one of the quietest, and the ruler's whole reason for existing degrades exactly at the length that
made it necessary.

**The mechanism, measured 2026-08-18**
Rendered in real Chrome, offline, at 1920x1234, on a throwaway 25-slide deck built by splicing
twelve minimal slides into `examples/reference-deck.html`. Both themes, `data-ticks="dot"`, which
is the shipped default:

| Deck length | Mode | What marks the current slide | Rendered width |
| :--- | :--- | :--- | ---: |
| 13 slides | normal | `.ruler-ring` around the lit dot | **30 px** |
| 25 slides | dense | the lit dot alone, `7 du` | **7 px** |

In the same dense row a **section** mark renders at **14 px** — `.ruler[data-dense]` shrinks
`li:not([data-section])` and leaves the seven section cells at their full `14 du`. So past the bound
the mark that *changes* is half the width of the eleven marks that do not, and hue is the only
property left telling them apart.

**Why the two rules that produce it are each defensible**
Neither is a mistake on its own, which is why no review caught the pair:

- `.ruler[data-dense] .ruler-ring{display:none}` — the cells stop being uniform in dense mode and a
  30-unit ring would cover its neighbours. True.
- `.ruler[data-ticks="dot"] .ruler-ticks li[data-lit] button::before{background:var(--accent)}` sets
  colour and deliberately **not** size, so a lit slide cannot be misread as a stage start. Also
  true, and the CSS says so in its own comment.

Together they leave dense mode with no size channel for position at all: the ring carried it, the
ring is gone, and the replacement was explicitly forbidden from growing.

**Scope**
- In: how the current position reads in `[data-dense]`, both tick styles, both themes.
- Out: the capacity bound itself (16, `rulerAvailableDu()` — that is T-114's and is correct), and
  the decision to drop targets past the bound.

**The constraint any answer has to clear**
The size channel is spoken for: size means *section versus slide* and DS-216 forbids inventing a
third encoding of position. So the answer is a treatment that is neither a bigger dot nor a new
element — a ring sized to the dense cell, a bracket, or an underline the label already implies.
Whichever it is, it has to survive the `0.5` stage hand-over (DS-071), where a design unit renders
at `0.506` CSS px.

**Acceptance criteria**
- [x] At 25 slides, the current-position mark is the most prominent mark on the ruler, in both
      themes, and a person says so from a render rather than a measurement.
- [x] Position stays distinguishable from a stage start — the two encodings do not merge.
- [x] The treatment survives the 0.5 scale floor; the rendered size is stated.
- [x] Both tick styles (`dot`, `bar`) covered, since the theme parameter must not fork the
      component (CLAUDE.md rule 4).
- [x] `check_all.py`, `tasks/lint.py` and `docs/figures.py` clean.

**Open questions**
- Which treatment — the project owner, from a rendered strip of two or three candidates, not from
  prose. This is the same shape of question `chrome_row.py` refuses to answer for the mark floor.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Build a repeatable long-deck fixture rather than a hand-spliced throwaway — the fixture this was found with lived in a scratch directory and dies with the session | a tool or a checked-in fixture |
| 2 | Render two or three candidate treatments at 17, 25 and 43 slides, both themes, both tick styles | a strip to look at |
| 3 | Owner rules | a decision in §3 |
| 4 | Build it in `shell/`, sync the three shipped decks, regenerate the seeded-defects deck (L-77) | shell, css |
| 5 | Gates, then `figures.py` last because a shell change moves every deck's byte size | green |

**What reading the code added to the five steps, 2026-08-19.** None of it changes their order; each is a
constraint a step has to satisfy and would otherwise discover late.

- **Step 1 has a registration cost.** `check_all.py` discovers every tracked tool under `tools/` with
  `git ls-files` and fails the run on any it cannot classify — that is the *unclassified* state, and it
  is deliberately what a new checker nobody wired looks like. A fixture builder is not a gate, so it
  goes in `NOT_RUN` **with its reason**, beside `render.py` and `chrome_row.py`. Forgetting this turns
  step 5 red for a reason that has nothing to do with the ruler.
- **Step 1 needs no manifest surgery.** `manifest()` in [`shell/deck.js`](../shell/deck.js) derives
  every entry from the `.slide` sections themselves — `data-stage`, `data-name`, `.bottom-line` — so
  splicing sections is the whole of it. There is no second list to keep in step, which is L-08 already
  paid for.
- **Step 2's candidates all reuse one element.** `.ruler-ring` exists in every deck and is only
  `display:none` past the bound, and `placeRing()` positions it by **measuring the current tick**
  rather than by pitch arithmetic — written that way precisely so it stays correct where the cells
  stop being uniform. So a dense treatment built on the ring inherits working positioning and the
  translate-not-redraw behaviour, and adds no element, which is what §1's constraint asks for.
- **Step 2 cannot crop.** `render.py shots` passes Chrome `--screenshot`, which captures the whole
  **window**; there is no clip and no image library here (L-07). So the strip is assembled by loading
  the real PNGs into a contact-sheet page and screenshotting that — the pixels stay the real deck's,
  cropped by the browser rather than simulated in one.
- **Step 2's numbers come from the DOM, not from the picture.** §1's acceptance criterion asks for the
  rendered size to be *stated*; that is a `getBoundingClientRect` read in the same run, not something
  measured off a screenshot.

## 3. Implement

**Decisions & assumptions**

- **The treatment is the capsule — the owner's pick, 2026-08-19, from the rendered strip.** Offered
  the baseline and three candidates at 1920x1234 and at the 0.5 hand-over, in both themes and both
  tick styles, they chose the ring reshaped to the dense cell: `10 x 30 du`, a `--rule` outline in
  `--accent`, cornered with `--radius`. What decided it was the floor rather than the wide render,
  where all three read: 30 du is **15.2 CSS px** at `k=0.506`, against the caret's 7 du at 3.5 and
  the underline's 3 du at 1.5. The two quieter candidates are legible at the default size and
  effectively gone at the smallest stage the deck supports.
- **It reuses `.ruler-ring` and adds no element**, which is §1's constraint met rather than worked
  around. Three things come free with that: `placeRing()` already positions it by **measuring the
  current tick** instead of computing a pitch — written that way for exactly this degraded mode,
  where the cells are not uniform — it already translates rather than being redrawn, so the eye
  follows one object, and DS-218's stop control and DS-143's reduced-motion collapse already reach
  it.
- **The rule is not scoped to a tick style, unlike the ring rule above it.** `bar` never received the
  ring at all, so a dense rule written the same way would have left half the component with the
  defect (CLAUDE.md rule 4). Equal specificity plus later source order is what lets one declaration
  serve both, and the rendered proof is the `bar` strip.
- **`border-radius:var(--radius)` rather than the `calc(5*var(--du))` the shape needs.** DS-010
  failed the literal, correctly: a theme that changed its corners would have left this one behind.
  The rendering is identical — 14 du of corner on a 10 du box overflows, so CSS scales every radius
  by `10/28` and lands on exactly 5.
- **The lit mark is untouched.** Size on the ruler still means section-versus-slide, so DS-216 is
  satisfied by construction rather than by argument: `7x7` lit against `14x14` section, unchanged at
  every length and both scales measured.

**Outputs produced**
- `shell/components.css` — `.ruler[data-dense] .ruler-ring` reshapes instead of disappearing.
- `tools/deck/longdeck.py` — splices a deck to any slide count, holding the stage set fixed so the
  section-mark count does not move with length. Registered in `check_all.py`'s `NOT_RUN`.
- `tools/deck/rulerstrip.py` — renders the candidates side by side and reports what each mark
  measures. Also in `NOT_RUN`.
- The three shipped decks synced and the seeded-defects fixture regenerated (L-77).
- [`docs/lessons/L-123.md`](../docs/lessons/L-123.md) — the two measurement defects this hit.

**Two defects found in the instrument, both before anything was built, both L-123**
- A DOM rectangle cannot crop a `--screenshot`: the capture is laid out differently from what
  `--dump-dom` reports, in the same invocation. Replaced by finding the box in the image.
- `getComputedStyle` is pre-transform and `getBoundingClientRect` is post-transform. Dividing both
  by the stage scale reported every mark at double size at the floor, and was invisible at `k=0.99`.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| At 25 slides, the current-position mark is the most prominent mark on the ruler, in both themes, and a person says so from a render rather than a measurement | **pass** | The owner chose it from the strip, which is the person and the render this criterion asks for. Confirmed again after the build at 43 slides, where it is the only mark on the row that is not a dot |
| Position stays distinguishable from a stage start — the two encodings do not merge | **pass** | Nothing about any mark changed: `7x7` lit, `14x14` section, `4x4` plain, at 13, 25 and 43 slides and at both scales. The capsule is drawn *around* the mark, so size still answers only section-versus-slide |
| The treatment survives the 0.5 scale floor; the rendered size is stated | **pass** | At `k=0.506`, `30 du` renders at **15.2 CSS px** and the outline at `--rule`. Looked at, in both themes, in `dot` and in `bar`. **The first version of this number was double** and the measurement bug that produced it is L-123 |
| Both tick styles (`dot`, `bar`) covered, since the theme parameter must not fork the component | **pass** | One declaration, scoped to neither. Rendered in `bar` at the wide size and at the floor. Worth recording: in `bar` the baseline defect was always milder — the lit bar is `6x20` against a `3x26` section bar, so it was wider if shorter. The dot style is where the defect bit, and one rule fixed both |
| `check_all.py`, `tasks/lint.py` and `docs/figures.py` clean | **pass** | `0 failure(s), 0 unclassified, 0 stale` over 44 tracked tools. `figures.py` needed seven byte figures updated across three documents, which is the shell change moving every deck's size exactly as §2 step 5 predicted |

**Child fix tasks raised**
- none.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-18 | → proposed | Found by [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md)'s post-build look, doing the half that had never been done: the chrome row **in dark mode**, at 13 slides and at 25. The defect is not dark-specific and shows in both themes, which is the part worth keeping — it had been rendered in light at 25 during T-114 step 10 and read as *a compact mode* rather than as a loss, because nothing put the two lengths side by side. `contrast.py` passes it, and correctly: every pair clears its ratio. The failure is one of **rank**, not of contrast, and no gate here owns rank (**L-05**). Not a tag blocker for the release T-114 ships in — the two rules that produce it both predate T-114 and neither moved — but this release lowers the capacity bound 17 → 16, so one more deck length falls into dense mode than before, and that is why it is filed now rather than noticed later. |
| 2026-08-19 | (no change) | **The owner confirmed §1's open question keeps its stated method: a rendered strip first, then the pick.** Offered the alternative of choosing from a written description of the three candidates, they declined it. So the next step is to build two or three treatments — a ring sized to the dense cell, a bracket, an underline — render a 25-slide deck in Chrome offline in both themes, and put the strip in front of them. Recorded here so the question is not re-asked as prose by a later session; the answer is that this one cannot be answered as prose. |
| 2026-08-19 | in_progress → done | **Built the capsule, chosen by the owner from a rendered strip.** The instrument is the deliverable that outlives the fix: `longdeck.py` makes the long-deck fixture a command rather than a scratch file that dies with the session, and `rulerstrip.py` renders the candidates and reports what each mark measures. Two measurement defects were found and fixed inside the instrument before the treatment was built - a DOM rectangle cannot crop a Chrome capture, and `getComputedStyle` is pre-transform where `getBoundingClientRect` is post - and both were invisible at the wide window and obvious at the 0.5 floor, which is **L-123**. The fix itself is one declaration: the dense ring reshapes to the cell instead of disappearing, scoped to neither tick style so `bar` is covered by the same rule that covers `dot`. |
