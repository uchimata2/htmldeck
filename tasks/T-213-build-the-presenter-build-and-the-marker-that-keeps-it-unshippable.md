---
id: T-213
title: Build the presenter build, and the marker that keeps it unshippable
type: deliverable
status: done
phase: review
parent: T-211
blocked_by: []
related: [T-211]
work_package: PH3
owner: the project owner
business_value: medium
effort: l
created: 2026-08-21
updated: 2026-08-22
shipped_in: unreleased
deliverables: [tools/deck/presenter.py, docs/lessons/L-132.md]
---

# T-213 — Build the presenter build, and the marker that keeps it unshippable

## 1. Specify

**Outcome**
A specification carrying speaker notes produces **two** artifacts: the deck that ships, with no
notes in it, and a **presenter build** that carries them and cannot pass a gate. Today neither
exists; [T-211](T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md) scoped them and
explicitly did not build them.

**What T-211 settled, and what it left**
Settled: notes never ship; DS-088 is unchanged and governs the shipped deck; the presenter build is
a second artifact from the same specification; its safety property is that it carries a marker
DS-088's own check fails on, so **the only build that can pass a gate is the one with no notes in
it**. Left: all of the mechanism. The scope is T-211 §3 and this task does not re-derive it.

**Why it is `l` rather than `m`**
It touches a build path, the shell, the component contract and a gate at once, and it introduces a
second output artifact where the repository has always had one. Each of those is small; the
combination is not, and the one-file promise is the thing being qualified.

**Scope**
- In: the presenter build — how notes are authored in the specification, how the build emits them,
  and what the presenter sees.
- In: the marker, and proving by seeded defect that a presenter build cannot pass `check.py`.
- In: the component-contract row for however the notes are carried.
- Out: changing DS-088. T-211 settled that it stands.
- Out: PDF export, the other half of `docs/BRIEF.md` open question 4, which the owner left deferred
  on 2026-08-21.

**Inputs**
- [T-211](T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md) §3 — the scope, and the
  privacy argument the marker exists to enforce.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-088 and its restated reason.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) — where the notes region's row goes.

**Acceptance criteria**
- [ ] One specification produces both artifacts, and the shipped one is byte-identical to what the
      same specification produces with no notes authored.
- [ ] A presenter build **fails** `python tools/deck/check.py`, proved by seeding one and running it.
- [ ] The shipped build passes every gate it passes today.
- [ ] The presenter build is still one self-contained file that opens by double-clicking, because a
      presenter is a recipient too.
- [ ] `python tools/check_all.py` green.

**Settled during specify, 2026-08-22**

- **The presenter build carries the whole deck and the notes.** The open question's own text argued
  it and nothing found here argues back: a presenter presents *from* it, so a file carrying notes
  and no slides is a sidecar with extra steps — the arrangement T-211 already rejected. The cost the
  question named is real and is answered below, not waived: it looks almost exactly like the
  shipping file, so the marker has to be loud to a **person** as well as to the gate.

- **The marker already exists, and building a new one would have been the defect.** DS-088's check
  is `"speaker-note" not in h and 'class="notes' not in h` ([`audit.py`](../tools/deck/audit.py)).
  So a note carried in `class="speaker-note"` **is** the marker: the artifact fails DS-088 because
  it contains notes, not because it contains a flag that says it contains notes. Inventing a
  separate `data-presenter` token would have created a second thing to keep in sync with the first,
  and a presenter build that lost its flag would pass — which is the whole safety property gone.
  **Nothing new is added to the ruleset or to any checker.**

- **The shipped deck is byte-identical because the notes path never touches it.** Criterion 1 asks
  for identity with what the same specification produces with no notes authored. The cheap way to
  satisfy it is to build one deck and strip notes out; the honest way is to **never put them in**.
  So the build is unchanged, and the presenter build is **derived from the built deck** by injecting
  notes into a copy — `presenter.py <deck> <slides>`. Identity then holds by construction and there
  is nothing to compare, which is the same shape `seed_defects.py` uses to derive its fixture and
  `fps.py` uses to instrument one.

- **A note is authored as a tenth field.** `- **Notes.**` in `<slug>.slides.md`, optional per slide,
  alongside the nine that
  [`artifacts.md`](../skills/htmldeck/references/artifacts.md) defines. Optional is the difference
  that matters: a required field would put an empty `Notes.` on every slide of every deck, and the
  first deck to ship would carry the string `Notes` into a specification nobody wanted it in.

**What the gate cannot reach, and what to do about it**
**The gate protects the file; it cannot protect the send.** A presenter build that never runs
through `check.py` is just a file with the deck's name and one extra panel, and the failure mode is
a person attaching the wrong one. Two things answer that, and both are in scope because the
criterion *a presenter is a recipient too* already puts the human in the design: the presenter build
is named `<slug>-presenter.html` rather than `<slug>.html`, and it carries a **persistent banner**
naming what it is and why it must not be sent. Neither is a substitute for the gate — they are for
the case the gate is never run in.

## 2. Plan

**The one decision the plan rests on: nothing on the shipping path changes.** Every step below adds
a derivation beside the build rather than a branch inside it. That is what makes criterion 1 true
without a comparison, and it is also what keeps this `l` task from touching the gate at all.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Add `Notes` as an optional tenth slide field, and say it never renders into the shipped deck | [`skills/htmldeck/references/artifacts.md`](../skills/htmldeck/references/artifacts.md), and its *Nine fields per slide* line |
| 2 | Build `presenter.py`: read the built deck and the slides specification, parse `Notes` per slide, inject a notes panel plus a banner into a **copy**, write `<slug>-presenter.html`. Standard library only (**L-07**) | `tools/deck/presenter.py` |
| 3 | The panel follows the deck's own `[data-current]` rather than counting clicks, so it cannot drift from the slide on screen and survives a chrome redesign — the lesson `audit.py`'s `goTo` records | in `presenter.py` |
| 4 | Register the notes region in the component contract, marked as **presenter-only** so no deck author reads it as shippable | [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) |
| 5 | Prove the safety property: generate a presenter build from the reference deck and run `check.py` on it. It must **fail DS-088**, and the shipped deck must still pass | recorded in §3 |
| 6 | Prove the identity property: the shipped deck is unchanged, by hash, across the whole task | recorded in §3 |
| 7 | Declare `presenter.py` in `check_all.py`'s `NOT_RUN`, and **stage it before the gate runs** (`PUBLISHING.md` §8 step 1) | [`tools/check_all.py`](../tools/check_all.py) |
| 8 | Author a note on one slide of the reference deck's specification, so the field has a worked instance rather than only a definition | [`examples/`](../examples) — specification only, never the deck |

**Step 5 is the acceptance criterion and not a smoke test.** T-211 §4 rests the entire scope on
*the only build that can pass a gate is the one with no notes in it*, and that sentence has never
been executed. Until step 5 runs it is a claim about a checker, which is **L-36** in the shape this
repository keeps meeting.

**What is deliberately not built:** any change to `check.py`, `audit.py`, DS-088, or the shell. If
a step turns out to need one, that is a finding about the design and gets reported rather than
absorbed.

## 3. Implement

**Decisions & assumptions**
- **The marker is `class="speaker-note"`, which is DS-088's own check string** — 2026-08-22. Nothing
  was added to the ruleset or to any checker. A separate `data-presenter` flag would have been a
  second object with the same job, removable on its own, and a build that lost it would pass while
  still carrying every note. Kept as **L-132**.
- **The presenter build is derived from the built deck, so criterion 1 needs no comparison** —
  2026-08-22. Verified by hash rather than argued: `examples/sort-window/sort-window.html` is
  `756d0350…` before this task and `756d0350…` after it.
- **`Notes` is optional, and it is the only optional field** — 2026-08-22. A required one would put
  an empty `Notes.` on every slide of every deck and carry the word into specifications nobody
  wanted it in. Absent and empty are the same answer.
- **The panel follows `[data-current]` through a `MutationObserver`** — 2026-08-22, rather than
  counting clicks. Anything keeping its own idea of position drifts the first time the ruler is
  used, which is the fault `audit.py`'s `goTo` helper records.
- **`*-presenter.html` is `.gitignore`d** — 2026-08-22. `check_all.py` fails any tracked `.html` it
  has no `DECKS` entry for, so a committed presenter build goes red. Ignoring it makes *never commit
  one* structural instead of remembered, which is the same argument as the marker one line up.

**The defect found by running the gate, and it changed the build**
The first presenter build failed **three** rules — DS-088 as designed, plus **DS-033** (a `34vh` in
the panel) and **DS-010** (17 raw lengths in the injected chrome, taking the deck's literal count
from 51 to 68). Every verdict was correct and the safety property held. **It is still wrong**: a
maintainer meeting three failures cannot see which one is the design, and the shortest path to a
quiet gate is deleting the notes. The chrome was rewritten on the deck's own tokens and `max-height`
moved from `vh` to a percentage, which on a fixed element resolves against the viewport and is not
what DS-033 bans. **A deliberate failure has to be the only failure.** Kept as **L-132**.

*Two smaller things, both caught by the tool's own self-test or by looking:* `max-height:40%` broke
the `%`-format template until it was doubled, and the banner printed a literal script-style escape
across the top of the deck because HTML does not parse them. The second was invisible to every
check and visible in the first screenshot.

**Outputs produced**
- [`tools/deck/presenter.py`](../tools/deck/presenter.py) — the derivation, standard library only
- [`skills/htmldeck/references/artifacts.md`](../skills/htmldeck/references/artifacts.md) — the
  optional tenth field, and what it must never do
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.7a — the presenter panel, marked
  as the one region a conforming deck must not contain
- [`tools/check_all.py`](../tools/check_all.py) — the `NOT_RUN` entry
- [`.gitignore`](../.gitignore) — `*-presenter.html`
- [`docs/lessons/L-132.md`](../docs/lessons/L-132.md)
- [`examples/sort-window/sort-window.slides.md`](../examples/sort-window/sort-window.slides.md) — a
  worked note on slide 3, so the field has an instance and not only a definition

**Verification**

| What | Result |
| :--- | :--- |
| `check.py` on the presenter build | **1 failure: DS-088** — and nothing else |
| `check.py` on the shipped deck | **0 failures**, unchanged |
| `sort-window.html` hash, before and after the whole task | `756d03504a6ffd2c` → `756d03504a6ffd2c` |
| `presenter.py` self-test | passes — parse, wrap-over-lines, empty-field, escaping, missing anchor |
| `python tools/check_all.py` | **0 failures**, 30 tools not run each with what it is instead |

**Looked at** (CLAUDE.md rule 6): rendered slide 3 of the presenter build. The banner reads across
the top, the panel carries the slide number, the slide name and the authored note, and the deck
below it is unchanged. That render is what caught the escape defect above.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| One specification produces both artifacts, and the shipped one is byte-identical to what the same specification produces with no notes authored | met | Identity holds **by construction**: the notes path derives a copy and never touches the build. Verified by hash across the whole task, `756d03504a6ffd2c` unchanged |
| A presenter build **fails** `check.py`, proved by seeding one and running it | met | Generated from `sort-window.html` and run: **1 failure, DS-088**. T-211 §4's central sentence had never been executed before this |
| The shipped build passes every gate it passes today | met | `check.py` on `sort-window.html`: 0 failures. `check_all.py`: 0 failures |
| The presenter build is still one self-contained file that opens by double-clicking | met | Injected inline, no external reference added; 308 KB against the deck's 306 KB |
| `python tools/check_all.py` green | met | 0 failures, 0 unclassified, 0 stale |

**Child fix tasks raised**
- none

**What this task found that it was not looking for**
- **The marker already existed.** Building one would have been the defect — DS-088's check string is
  the marker, and a flag beside the notes could be removed on its own. **L-132**.
- **A deliberate failure must be the only failure**, or a maintainer tidying the noise is one edit
  from deleting the notes. Same lesson, second half.

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | → done | **The presenter build exists and T-211 §4's central sentence has now been executed.** *The only build that can pass a gate is the one with no notes in it* was a claim about a checker for a day; it is a run with a verdict now — 1 failure, DS-088, on a build generated from a shipped deck. Nothing was added to the ruleset, no checker changed, and the shipped deck is byte-identical by construction rather than by comparison. The open question was settled from its own argument during specify, not asked. **L-132** is the finding: make the forbidden thing its own marker, and make it the only failure. |
| 2026-08-21 | → proposed | Raised by [T-211](T-211-scope-speaker-notes-and-decide-what-ds-088-becomes.md), which scoped speaker notes and ruled that DS-088 stands unchanged because it governs the **shipped** deck. `PH3`, `l`: a build path, the shell, the contract and a gate at once, and a second output artifact where there has always been one. |
