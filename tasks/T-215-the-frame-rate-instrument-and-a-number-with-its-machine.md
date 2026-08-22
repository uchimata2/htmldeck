---
id: T-215
title: The frame-rate instrument, and a number with the machine it was measured on
type: deliverable
status: done
phase: review
parent: T-057
blocked_by: []
related: [T-057, T-185, T-016]
work_package: PH3
owner: the project owner
business_value: medium
effort: m
created: 2026-08-22
updated: 2026-08-22
shipped_in: 0.6.0
deliverables: [tools/deck/fps.py, docs/lessons/L-131.md]
---

# T-215 — The frame-rate instrument, and a number with the machine it was measured on

## 1. Specify

**Outcome**
A way to measure the frame rate a deck actually holds, and one recorded figure produced with it:
the number, the deck and slide it was taken on, and **the machine it was measured on stated beside
it**. No deck in this repository has ever had its frame rate measured on any machine.

**Why it is its own task**
Split out of [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) on
2026-08-22. T-057's own §1 calls itself *"three deliverables wearing one title"* and its plan step 1
says this one is **"independent of the rest, and the only one of the three that measures what
already exists"**. The third deliverable — the DS-140 amendment — was dissolved by the owner's
ruling of 2026-08-19, so T-057 was two things rather than three, and this is the half that needs no
3D visual, no ruleset change and no new component.

**It is the same argument T-016 used to create T-057.** T-016 split at `PH1` so a release would
ship; this splits so a measurement that can be taken today stops waiting behind an `xl` that cannot
start. T-057 has sat `proposed` since 2026-08-09 and this half was never the reason.

**Scope**
- In: an instrument that reports frames produced over a stated interval, on a real deck, with the
  heaviest slide on screen.
- In: one recorded figure, with **the machine named beside it** — that pairing is the deliverable,
  not the number alone.
- In: a stated home for the figure, so a later measurement on another machine adds a row rather
  than overwriting one. A single number with no machine is the thing this task exists to avoid.
- Out: **a gate.** Nothing here fails a deck. A frame-rate threshold is a claim about hardware this
  project does not have a corpus for, and inventing one from a single machine is exactly the
  reasoning **L-05** and the *scope warning* in
  [`docs/upstream/harness.md`](../docs/upstream/harness.md) both refuse.
- Out: the 3D visual, which stays in T-057 and is the case that would make the figure interesting
  rather than the case that makes it measurable.
- Out: any change to `render.py motion`, which seeks rather than plays and is settled (T-185).

**Inputs**
- [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) §1 — the criterion
  this inherits verbatim, and the scope sentence it is cut from.
- [T-185](T-185-no-instrument-here-can-watch-an-animation-play.md) — **the constraint that shapes this
  task.** `render.py motion` seeks the timeline and the computed style follows exactly, which makes
  every intermediate state measurable. What it explicitly **cannot** reach is *playback at a frame
  rate*, because headless produces no frames: a CSS animation's clock there is frame production
  rather than time (**L-26**). So this measurement cannot be taken by the headless harness that
  takes every other measurement in this repository.
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — where a measured figure is recorded, and the
  one-render-per-stage cost model.

**Acceptance criteria**
- [ ] Frame rate held on a real 12-slide deck with the heaviest slide on screen; **number stated,
      and the machine it was measured on stated with it** — inherited verbatim from T-057
- [ ] The instrument runs somewhere a person can repeat it, and what it needs is written down
- [ ] The figure's home takes a second row for a second machine without contradicting the first
- [ ] Nothing this task adds can fail a deck

**Settled during specify**
- **The owner will run it, in Chrome or Edge on the development machine.** Asked and answered
  2026-08-22, which is the one question this task could not settle for itself. So the instrument is
  built to be handed over and run by a person, and its output carries its **own** provenance —
  browser, platform, core count, display refresh and GPU renderer, read by the page at the moment of
  measurement — rather than inheriting the harness's, which is not the thing running it.
- **The heaviest slide is derived at run time, and it is not a proxy.** The open question offered a
  count of animated elements as *probably the right proxy*; it can be the exact thing instead. The
  instrument already runs inside the deck in a real browser, so it walks every slide and counts the
  elements whose computed `animation-name` is not `none`. Nothing is parsed and nothing is guessed.
  **T-057 then re-measures and adds a row** rather than rewriting this one, which is the second half
  of the open question answered as it proposed.
- **Naming the machine is capability, never identity — and that is a constraint this task inherits
  rather than invents.** `CLAUDE.md`'s publishing rule requires this repository to be free of
  personal and **machine** data, and this task's whole point is that a number without its machine is
  worthless. Both hold at once: what makes the figure interpretable is the **class of hardware** —
  OS, browser and version, core count, display refresh, GPU renderer — and none of that is a
  hostname, a user name, a serial or a path. `docs/upstream/harness.md` already publishes *one
  machine — Windows 11, Git Bash and PowerShell 7* on exactly this reading. The instrument collects
  nothing else, so the rule is kept by what it does not gather rather than by remembering to redact.
- **The figure's home is `docs/EVALUATION.md`.** Named in Inputs, and it is the document that already
  separates what the gate decides from what it cannot reach. `docs/upstream/harness.md` was
  considered and rejected: it is a register of observations addressed to a vendor, not a place this
  project records its own measurements.

**Why the number needs a second number beside it**
A frame rate is bounded by the display, so *58 fps* means nothing until you know whether the ceiling
was 60 or 144. The instrument therefore measures the **refresh ceiling** on the same machine in the
same run, and the figure is recorded as *held against ceiling*. Without it the first row would invite
exactly the comparison across machines that this task's `Out: a gate` clause refuses.

## 2. Plan

**The instrument is a tool that prepares a deck and a person who runs it**, because no other split
works: the measurement needs frames, frames need a real window, and a real window needs somebody
looking at it (T-185, **L-26**). So `fps.py` does everything that can be automated — inject, pick the
slide, count, gather provenance, format the row — and the person supplies the one thing the harness
cannot, which is a machine that draws.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `fps.py <deck>`: copy the deck, inject a measuring overlay before `</body>`, write it to the deck's own assets cache and open it. Standard library only (**L-07**) | `tools/deck/fps.py` |
| 2 | The overlay measures the **refresh ceiling** first, on an idle frame burst, before any slide is shown — the ceiling is a property of the display, and measuring it while the deck animates would fold the two numbers together | in `fps.py` |
| 3 | It walks every slide counting elements whose computed `animation-name` is not `none`, picks the heaviest, and drives the deck there through its own `next`/`prev` controls — never by assuming an index, which is how `audit.py`'s helper survived a chrome redesign | in `fps.py` |
| 4 | It counts `requestAnimationFrame` callbacks over a stated interval on that slide, then shows a result card with the figure, the ceiling, the slide, the animated-element count and the machine's **capability** fields — and a pre-formatted table row to paste | in `fps.py` |
| 5 | Declare the tool in `check_all.py`'s `NOT_RUN` with what it is instead, and **stage it before the gate runs**, since `check_all` discovers tracked files only (`PUBLISHING.md` §8 step 1) | `tools/check_all.py` |
| 6 | Give the figure a home that takes one row per measurement — deck, slide, held, ceiling, machine, date | `docs/EVALUATION.md` |
| 7 | Hand the command to the owner, record the row they return, and close | §3, §4 |

**Nothing here can fail a deck**, which is the scope's one prohibition. `fps.py` is not in the gate,
is not called by `check.py`, and prints a measurement rather than a verdict. Step 5 is what keeps
that true *and* keeps `check_all` green, which otherwise fails any tracked tool no table names.

**The one acceptance criterion this task cannot close on its own is the first**, and that was known
when it was raised. If the owner's reading does not arrive, it is recorded `not met` with the reason
and the instrument still ships — §2 of `TASK-WORKFLOW.md` says that closes a task honestly, and a
number invented next to a machine nobody ran is the single outcome this task exists to prevent.

## 3. Implement

**Decisions & assumptions**
- **The instrument is a preparer plus a person, and the split is forced rather than chosen** —
  2026-08-22. `fps.py` injects, weighs, drives, counts and formats; the person supplies a window
  that draws. Nothing else divides the work, because frames need a real foreground window.
- **The heaviest slide is counted in the browser, not parsed from CSS** — 2026-08-22. The overlay is
  already running inside the deck, so it reads computed `animation-name` per element per slide. This
  is the same move T-214 made one rule along: bind on what is true at run time, never on a name.
- **The refresh ceiling is measured first, before any slide is shown** — 2026-08-22. It is a property
  of the display; measuring it while the deck animates folds two numbers into one and neither
  survives.
- **`fps.py` is declared in `check_all.py`'s `NOT_RUN` and staged before the gate ran** — 2026-08-22.
  `check_all` discovers *tracked* files, so an unstaged new tool is invisible to it and a staged one
  with no entry fails the run as `UNCLASSIFIED`. Both halves are `PUBLISHING.md` §8 step 1.
- **The machine is recorded as capability and never as identity** — 2026-08-22. OS, browser, cores,
  memory, screen, refresh, GPU renderer; no hostname, user, path or account. That is how this task's
  *state the machine* and `CLAUDE.md`'s *no machine data* hold at once, and `fps.py` keeps it by not
  collecting the rest.

**A defect found in this tool by checking it, and worth more than the tool**
Opening the instrumented deck in a hidden preview pane to check the overlay for script errors: the
card rendered, the script ran clean, `requestAnimationFrame` **never fired once**, and the page sat
on *Measuring the display's refresh ceiling…* indefinitely. **A stall is indistinguishable from a
slow machine**, and it is the reading most likely to be written down as a number. The overlay now
carries a watchdog that reports *No frames* with what causes it. This is T-185's finding arriving
through a second door — and it is also the proof that the instrument cannot be satisfied by the
harness, a background tab or a preview pane, which is the property that makes its output worth
recording at all.

**The first real reading found two defects, and only a real reading could have**
The owner ran it and returned *slide 1, 5 animated, 144.0 held, 144 ceiling*. The **numbers are
sound and the subject is wrong**, which is the failure mode this task exists to prevent wearing its
most convincing face — a plausible figure, correctly measured, of the wrong thing.

- **The walk.** `.rise` is declared `.slide[data-played] .rise`, so a slide nobody has visited has no
  animation to count. `weigh()` ran from a standing start, saw motion on the opening slide and zero
  on the other twelve, and picked slide 1 — **every time, on any deck**, while printing a count that
  reads as a derivation. Fixed by walking the deck before weighing. Verified headlessly: the walk
  reports 5, 5, 6, 5, 5, 5, 8, 6, 7, 7, 5, 3, 5 across thirteen slides.
- **The axis.** Ranking on total animated elements is wrong for a *sustained* measurement. An entry
  animation is over 340 ms in and costs nothing across a six-second window; only a **looping** one
  costs for the whole interval. On the counts above, ranking by total picks slide 7 and ranking by
  looping picks **slide 8**, the only slide in the deck carrying an infinite animation — `Current`,
  which is the thing worth measuring.
- **Consequence for the record:** the returned row is not entered. It measured an idle page, which
  is a true statement about slide 1 and not the criterion.

The card now names both counts and says so plainly when a slide has nothing looping, so *144 of 144*
can never again be read as a loaded deck holding its frame rate when it is an idle one.

**Outputs produced**
- [`tools/deck/fps.py`](../tools/deck/fps.py) — the instrument, standard library only (**L-07**)
- [`tools/check_all.py`](../tools/check_all.py) — the `NOT_RUN` entry saying what it is instead
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) §6.3 — the figure's home, one row per measurement

**Verification**
- `fps.py` self-test passes: the overlay lands, the anchor is replaced rather than duplicated,
  `--seconds` and `--slide` reach the page, and a file with no `</body>` is refused rather than
  silently returned unchanged.
- Built against the reference deck: 314 KB out, overlay present, no console errors on load.
- `python tools/check_all.py` green with the tool staged and declared.

**The reading, and the two defects between it and the first attempt**
Three runs on the owner's machine produced one row. **None of the three was a bad measurement** —
each counted frames correctly, and each of the first two counted them on the wrong subject.

| Run | What came back | What was wrong |
| :--- | :--- | :--- |
| 1 | slide 1, 5 animated, 144.0 / 144 | The count ran before the walk, and `.rise` only exists on a played slide. Slide 1 wins on every deck |
| 2 | slide 8, `6 · 1 looping`, 144.1 / 144 | Right slide. But *6 animated* invites the reader to find six moving things and see one, and the deck column named the slide because `deck.js` rewrites `document.title` on navigation |
| 3 | recorded | — |

**The owner found the second one by looking at the deck and counting**, which is `CLAUDE.md` rule 6
doing exactly what it is for: the gate was green, the self-test passed, the number was right, and the
label was wrong in a way only a person watching the slide could see.

**The figure:** **144.1 fps held against a 144 fps ceiling**, reference deck slide 8, one looping
animation and five finished entrances, Windows 11 / Chrome 151 / 16 cores / RTX 4070, 2026-08-22.
Recorded in [`docs/EVALUATION.md`](../docs/EVALUATION.md) §6.3, which takes a row per machine.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Frame rate held on a real 12-slide deck, heaviest slide, **number and machine stated together** | met | **144.1 held against a 144 ceiling**, reference deck slide 8, 1 looping + 5 entry, on Windows 11 / Chrome 151 / 16 cores / RTX 4070. `docs/EVALUATION.md` §6.3. Took three runs, and the first two were the instrument's fault |
| The instrument runs somewhere a person can repeat it, and what it needs is written down | met | `python tools/deck/fps.py <deck>`; the docstring states what it needs and why nothing here can substitute |
| The figure's home takes a second row for a second machine without contradicting the first | met | `docs/EVALUATION.md` §6.3 — a table keyed by date, deck, slide and machine |
| Nothing this task adds can fail a deck | met | `fps.py` is in `check_all.py`'s `NOT_RUN`, is called by no gate, and prints a measurement rather than a verdict |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-22 | → done | **The figure exists, and this repository has never had one before.** 144.1 against a 144 ceiling on the reference deck's slide 8, with the machine beside it. All four criteria met. **Three runs, two of them defects in the instrument rather than in the deck**, and the second was caught by the owner counting animations on screen against what the card claimed - a green gate, a passing self-test and a correct number, with the label wrong. Kept as **L-131**. The baseline this leaves is what [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)'s 3D visual gets measured against, on this machine, as a second row. |
| 2026-08-22 | (still in_progress) | **The first reading found two defects in the instrument and was not recorded.** The walk and the ranking axis were both wrong, and each independently guaranteed the wrong slide: `.rise` only exists on a played slide, and entry animations are finished before a six-second window starts. Both fixed and verified headlessly — the ranking now picks slide 8, the deck's only looping motion. **A correctly measured number about the wrong subject is the outcome this task was raised to prevent**, and it took a real machine to surface it: no self-test would have, because the logic was internally consistent. Re-run owed. |
| 2026-08-22 | → in_progress | **Instrument built; the reading is the only thing outstanding.** Both open questions settled at specify - the owner runs it in Chrome or Edge on the development machine, and the heaviest slide is counted at run time rather than proxied. Three of four criteria met. Held open rather than closed `not met`, because the owner's answer has arrived and only the number has not; closing now would make a one-command wait look like a limit of the task. |
| 2026-08-22 | → proposed | **Split out of [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) while restating that task's dissolved DS-140 criterion.** T-057 was three deliverables wearing one title, the third went with the owner's 2026-08-19 ruling, and its own plan calls this half independent and the only one measuring something that already exists. `m` rather than `l` because there is no visual to build and no rule to change; `PH3` because it is not a defect in the published plugin. **The constraint carried over from T-185 is the whole shape of it**: headless produces no frames, so this is the first measurement here that cannot be taken by the harness. |
