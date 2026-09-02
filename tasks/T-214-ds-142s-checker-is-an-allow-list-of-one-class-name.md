---
id: T-214
title: DS-142's checker is an allow-list of one class name, and T-187 left it behind
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-187, T-057, T-005, T-202, T-105]
work_package: PH1
owner: the project owner
business_value: high
effort: m
created: 2026-08-22
updated: 2026-08-22
shipped_in: 0.6.0
deliverables: [docs/lessons/L-130.md]
---

# T-214 — DS-142's checker is an allow-list of one class name, and T-187 left it behind

## 1. Specify

**Outcome**
`audit.py` decides [DS-142](../docs/DESIGN-SYSTEM.md) from whether a looping motion's subject is
static content, rather than from whether the element carries the class `.current`. A deck running a
looping motion DS-140 admits passes the gate; a deck running an ambient glow on static content still
fails it.

**Why this one**
**A published gate fails a deck for a design choice the ruleset permits.** DS-140 was a closed
vocabulary of four until 2026-08-21, and while it was, *the one sanctioned looping motion* and *the
element with class `.current`* were the same set — so implementing DS-142 as a class test was
correct and cost nothing. [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md) opened the
vocabulary on the owner's ruling that **any animation aligned with the rules is admissible**, and
every rule that reasoned from the closure was re-derived: DS-141's waiver became a declared licence,
DS-146 was re-argued from DS-243, DS-218 was restated on *looping* rather than on `Current`, and
DS-230's closure was kept in its own terms. **`audit.py`'s DS-142 branch was not**, and it is the
one place the closure survives as executable code.

The test today is [`tools/deck/audit.py`](../tools/deck/audit.py), in the probe that decides DS-140,
DS-142 and DS-218:

```js
if (!all[j].classList.contains('current')) out.ambient.push(row);
```

Anything whose computed `animationIterationCount` is `infinite` and whose element does not carry
`.current` is reported as ambient, and DS-142 is a `hard`/`auto` prohibition, so the deck fails.

**This is L-39 again, and this instance is sharper than the usual one.** The comment directly above
that line was rewritten by T-187 and now reads *"what decides the rows below is whether a looping
thing is a flow or static content, which was always the actual test"*. **It is not what the line
below it does.** So the file carries a claim that the re-derivation happened, three lines above the
code that shows it did not — which is worse than an un-revisited comment, because a reader checking
whether T-187 reached here finds a sentence saying yes.

**It is an allow-list of one, which is the shape the owner rejected one rule along.** The ruling was
*"please don't limit the animation to a specific 'allow list'"*. DS-140's list of four went; DS-142's
list of one did not, and a list of one is not a smaller version of the problem.

**Latent, not live, and that is why it needs a task rather than a hotfix.** No deck in this
repository runs an infinite animation outside `.current`, so every gate run is green and will stay
green until somebody builds one. The first deck to meet it is
[T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)'s 3D visual, whose
oscillation *is* the depth encoding and is therefore infinite by construction — which is how this
was found, rather than by a gate run.

**Why `PH1`, and there is a named precedent.**
[T-105](T-105-fig-pos-neg-caution-are-vocabulary-so-a-real-deck-fails-for-using-them.md) is the
same defect one contract along - `.fig .pos`, `.neg` and `.caution` were classified so that a real
deck had to choose between drawing a loss in red and passing the gate - and [T-120](T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md) cites it as
*a shipped gate failing a conforming deck is a defect in the check*. `CLAUDE.md` states the case
this is: *a report that arrives as feedback because a contract behaves as written is still a defect
when a published gate fails a deck for using a class that contract defines.* The gate is published at
`0.5.1`, the class is the one DS-140's admission test defines, and an adopter meets this with no 3D
at all — any looping motion they write that is not a dashed flow.

**Scope**
- In: the DS-142 branch of the probe, re-derived so the subject rather than the class name decides
  it.
- In: **the declaration a motion makes about its own subject**, on the idiom the ruleset already
  uses three times — DS-237's `--motion-kind`, DS-141's `--motion-long`, DS-230's `data-disc`: the
  artifact states the claim and the tool reads it back rather than inferring it. `.current` stops
  being special and becomes the first thing that declares.
- In: **both directions seeded** — a looping motion that declares a live subject must pass, and an
  ambient glow on static content must still fail. A check only ever seen in one direction is
  **L-36** or **L-129** depending on which direction is missing, and this one has never been seen to
  pass on anything but `.current`.
- In: DS-142's row amended to say what decides it, and DS-140's admission test amended to **name
  DS-142**, which it does not today.
- Out: **DS-142's force.** *No continuous ambient glow, pulse or drift on static content* is not
  weakened, re-scoped or made `judge`. What changes is how the instrument finds its subject.
- Out: the 3D visual itself, which is T-057. This task must not need one to be finished — the
  seeded variants are its subject, not a deck.
- Out: DS-218's control, which already binds on *looping* and was restated by T-187.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.2 — DS-142, DS-140's admission test,
  DS-237, DS-141, DS-218, DS-238's list of what binds at density 100 (which already names DS-142).
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the probe, the `ambient` row, and the comment
  that claims the re-derivation.
- [`docs/MOTION-GUIDE.md`](../docs/MOTION-GUIDE.md) §3 — the admission test as written for a person,
  which omits DS-142 in the same way.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8 — where a declaration on a
  motion is registered.
- [T-187](T-187-open-the-motion-vocabulary-into-a-style-guide.md) — what was re-derived and what the
  ruling was. [T-202](T-202-amend-ds-122-into-a-threshold-and-bind-its-check-on-structure.md) — the
  precedent for replacing a name-matching check with one bound on structure (**L-125**).

**Acceptance criteria**
- [ ] DS-142 fails an ambient glow on static content, on a seeded variant, exactly as it does today
- [ ] DS-142 **passes** a looping motion that declares a live subject, on a seeded variant — the
      direction that has never been observed on anything but `.current`
- [ ] `.current` passes by declaring, not by being named in the checker; no class name decides a
      verdict
- [ ] The reference deck and the other three shipped decks still pass, with no change to their
      verdicts
- [ ] DS-140's admission test names DS-142, in `DESIGN-SYSTEM.md` and in `MOTION-GUIDE.md` §3
- [ ] The comment in `audit.py` describes what the code does

**Settled during specify**
- **The declaration is `--motion-subject: live | static`, a custom property on the rule that starts
  the motion.** Decided 2026-08-22 from the precedent the open question names, without asking. The
  three existing instances split two to one — a custom property carries *motion* facts
  (`--motion-kind`, `--motion-long`), an attribute carries *editorial* ones (`data-disc`,
  `data-scale`) — and a motion's subject is a motion fact. It also lands where a reader already
  looks: `.current` declares `--motion-kind:affordance;--motion-long:loop` on one rule
  ([`shell/components.css`](../shell/components.css)), and this is a third token on that same line.
- **Both values are meaningful, so the closed pair is not one value plus a violation.** `static` is
  the honest declaration for a *non-looping* motion on static content — DS-147's emphasis pulse is
  exactly that — so the property describes any motion's subject and DS-142 binds only where the
  motion also loops. That is what makes absence a defect in DS-237's shape rather than a default.

**Verified during specify, and it is worse than the task assumed**
- **`static_variants.py` carries no DS-142 seed in either direction.** Grepped 2026-08-22: the file
  seeds DS-140 (`motion-outside-its-band`) and DS-218 (`motion-stop-shut-inside-the-menu`) and
  nothing for DS-142. So the row has never been observed to fire *or* to pass on any input — it is
  **L-36 and L-129 at once**, not just the L-129 the task was raised on. Its green on four shipped
  decks is the absence of a subject, which is the same reading T-051 was raised for.
- **`run_must_pass` already exists** and is the harness the second criterion needs — added by T-041
  for GF-7, the other check whose pass had never been seen. This task adds the second user of it
  rather than a mechanism.

## 2. Plan

**The one finding that shapes every step below: a custom property inherits, and the checker reads
computed style.** DS-237's `--motion-kind` and DS-141's `--motion-long` are read out of the **CSS
source text** by regex on the rule body, so inheritance never reaches them. DS-142 is decided by the
live probe on `getComputedStyle`, which is a different instrument on the same idiom — and there an
element that declares nothing inherits its ancestor's value. A glow nested inside `.current` would
read `live` and be exempted. **That is the same defect one shape along: an allow-list of one class
becomes an exemption one subtree wide**, which is what the scope forbids. So the property is
**registered non-inheriting** — `@property{inherits:false}` — and the guard sits at the exact point
the measurement is taken rather than in a rule about where authors may write the token. Step 5 is
what proves it, and it is not optional.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Register `--motion-subject` with `inherits:false`, and declare `--motion-subject:live` on `.current` beside its two existing motion tokens | `shell/components.css` |
| 2 | Re-derive the probe's DS-142 branch: ambient unless the element's own `--motion-subject` computes to `live`. **Correct the comment above it**, which claims a re-derivation the code below it never had | `tools/deck/audit.py` |
| 3 | Seed the fail direction — an infinite glow on static content, which must still fail DS-142 exactly as today | `tools/deck/static_variants.py`, `RENDER_VARIANTS` |
| 4 | Seed the pass direction — an infinite motion on an element that is **not** `.current`, declaring `live`, which must pass | `tools/deck/static_variants.py`, a new `RENDER_PASS_VARIANTS` run through `run_must_pass` |
| 5 | Seed the inheritance direction — an infinite glow **nested inside `.current`**, which must fail. This is the seed that proves step 1's registration and that no subtree is exempt | `tools/deck/static_variants.py`, `RENDER_VARIANTS` |
| 6 | Amend DS-142's row to say what decides it, make DS-140's admission test name DS-142, and register the declaration where a component declares things | `docs/DESIGN-SYSTEM.md`, `docs/MOTION-GUIDE.md` §3, `docs/COMPONENT-CONTRACT.md` §3.8 |
| 7 | Prove the three seeds **red before the fix**, then green after, and the four shipped decks' verdicts unchanged | run output recorded in §3 |

**Step 4 needs a new list and one line of wiring**, because `run_must_pass` exists but has exactly
one caller — `GF_PASS_VARIANTS` against `glitchfree_failures`. The rendered half has no pass
direction at all today. That is the mechanism T-041 built being used a second time, not a new one.

**Order matters between 3-5 and 1-2.** Seed first and run them against the *unfixed* checker; a
seed written after the fix proves only that the fix agrees with itself (**L-125**). *Corrected
during implement: this step said watch all three **fail**, and only one of them can. Seeds 3 and 5
are caught before the fix and after it — they are regression guards, and the nested seed's evidence
is that its ambient **count** falls from 2 to 1 rather than that its verdict flips. Only seed 4 is
red-then-green. Writing it as three would have made two seeds look like proof they are not, which is
the same over-claim **L-129** names one level up.*

## 3. Implement

**Decisions & assumptions**
- **`--motion-subject: live | static`, a custom property on the rule that starts the motion** —
  settled at specify from the two-to-one precedent, not asked. 2026-08-22.
- **The property is registered `@property{syntax:"*";inherits:false}`, and that is the whole of what
  makes the fix smaller than the defect** — 2026-08-22. `--motion-kind` and `--motion-long` are read
  by a regex over the CSS source, so inheritance never reaches them; DS-142 is decided by a live
  probe on `getComputedStyle`, where a custom property inherits. Copying the idiom without its
  instrument would have traded an allow-list of one class name for an exemption one subtree wide.
  Kept as **L-130**.
- **Every seed declares `--motion-kind:affordance`** — 2026-08-22. A glow on a headline is not an
  affordance and the claim is false, but DS-237 checks that a kind is declared and DS-243/DS-150
  judge whether the claim is true. Declaring `content` would gate the seed on `--m-on` and demand an
  `--m-rank`, breaking DS-238 and DS-239 alongside DS-142 and proving nothing about any of the three.
- **The comment in `shell/components.css` was written long and then cut to four lines** —
  2026-08-22. It ships inside every deck: the first draft cost **1,198 bytes in each of four decks**
  and moved nine pasted figures. The argument lives in DS-142's row and in `audit.py`, neither of
  which ships.
- **`shell.py sync --write` is wrong on `reference-deck-seeded-defects.html`** — 2026-08-22. That
  deck is *derived* from the reference deck and carries seeded CSS in the same region, so syncing it
  silently dropped eleven lines. It is regenerated with `tools/examples/seed_defects.py`, and the
  gate caught it.

**Outputs produced**
- [`shell/components.css`](../shell/components.css) — the registration and `.current`'s declaration
- [`tools/deck/audit.py`](../tools/deck/audit.py) — the re-derived probe branch, and the comment
  corrected to describe what the code does
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) — three seeds and
  `RENDER_PASS_VARIANTS`, the rendered half's first pass direction
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-142's row, and DS-140's admission test
- [`docs/MOTION-GUIDE.md`](../docs/MOTION-GUIDE.md) §3, [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8
- [`docs/lessons/L-130.md`](../docs/lessons/L-130.md)
- The four shipped decks, re-synced to the new component block

**Verification**

Red before green, on the three seeds, `RENDER_VARIANTS` and `RENDER_PASS_VARIANTS`:

| Seed | Before the fix | After |
| :--- | :--- | :--- |
| `ambient-glow-on-static-content` | CAUGHT, 12 ambient | CAUGHT, 12 ambient |
| `ambient-glow-inheriting-a-live-subject` | CAUGHT, **2** ambient — `seedspin`, `seedglow` | CAUGHT, **1** — `seedglow` |
| `looping-motion-declaring-a-live-subject` | **DID NOT PASS**, 1 ambient — the defect | **PASSED**, 0 ambient |

The middle row is the evidence for the registration: the declaring parent stopped being ambient and
its undeclared child did not, so inheritance carries no exemption.

`python tools/check_all.py` — **35 ran, 2 skipped with a stated reason, 0 failed, 270 s.** The four
shipped decks' verdicts are unchanged.

**Looked at** (CLAUDE.md rule 6): `render.py shots examples/reference-deck.html 1,8` — slide 8 is the
only slide carrying `.current`. The dashed flow, its arrowhead, the ruler and the chrome row all
render as before; motion is pinned off in a capture, as `render.py` documents.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| DS-142 fails an ambient glow on static content, on a seeded variant, exactly as today | met | `ambient-glow-on-static-content`, 12 ambient rows before and after |
| DS-142 **passes** a looping motion that declares a live subject | met | `looping-motion-declaring-a-live-subject` — DID NOT PASS before, PASSED after. The rendered half had no pass direction at all until this task |
| `.current` passes by declaring, not by being named; no class name decides a verdict | met | `classList.contains('current')` is gone from `audit.py`; `.current` carries `--motion-subject:live` |
| The reference deck and the other three shipped decks still pass, verdicts unchanged | met | `check_all.py` green, 35 ran / 0 failed. All four re-synced to the new component block |
| DS-140's admission test names DS-142, in `DESIGN-SYSTEM.md` and `MOTION-GUIDE.md` §3 | met | Both amended |
| The comment in `audit.py` describes what the code does | met | Rewritten, and it now records that the old comment claimed T-187's re-derivation three lines above code that had not had it (**L-39**) |

**Child fix tasks raised**
- none

**What this task found that it was not looking for**
- **DS-142 had no seed in either direction**, so its green on four shipped decks was the absence of a
  subject rather than a verdict — **L-36** and **L-129** at once, where the task was raised on L-129
  alone.
- **The declaration idiom does not carry its guarantees across instruments.** Kept as **L-130**; it
  is the finding that decided the shape of the fix rather than a note beside it.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | (shipped) | **Shipped in `0.6.0`.** The release note carries `docs/PUBLISHING.md` §8.1's row for this version, which names what an adopter must change and the smallest edit that satisfies it. |
| 2026-08-22 | → done | **Closed the same day it was raised.** The fix is one probe branch, one registered property, one declaration and three seeds; what took the time was the registration, without which the fix would have been wider than the defect (**L-130**). `check_all.py` green at 35 ran / 0 failed, and slide 8 looked at. Unblocks [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md), whose 3D oscillation is infinite by construction and was the deck this rule would have failed. |
| 2026-08-22 | → proposed | **Raised while restating T-057's DS-140 criterion, and it is not what that restatement was looking for.** T-057's criterion asked for a ruling the owner dissolved on 2026-08-19, so the question was which rule now decides whether a 3D wobble is admissible. The answer is that DS-140's admission test admits it and **DS-142's checker rejects it**, on a class name — so the criterion was blocked by a rule nobody had asked. `PH1` because a published gate fails a deck for a design choice the ruleset permits, which is `CLAUDE.md`'s stated case for reopening it; `m` because the fix is one probe branch, one declaration and two seeded variants, and `high` because it gates [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) and reaches an adopter with no 3D at all. |
