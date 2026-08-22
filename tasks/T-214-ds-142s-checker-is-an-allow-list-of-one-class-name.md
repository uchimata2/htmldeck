---
id: T-214
title: DS-142's checker is an allow-list of one class name, and T-187 left it behind
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-187, T-057, T-005, T-202, T-105]
work_package: PH1
owner: the project owner
business_value: high
effort: m
created: 2026-08-22
updated: 2026-08-22
deliverables: []
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

**Open questions**
- **What is the declaration called, and where does it sit?** `--motion-subject: live | static` on the
  rule that starts the motion is the shape that matches `--motion-kind` and `--motion-long`, and
  `data-`-attributes are the shape that matches `data-disc` and `data-scale`. The three existing
  instances split two to one in favour of a custom property for *motion* facts and an attribute for
  *editorial* ones, which argues for the property. **Decide during specify from that precedent
  rather than asking** — it is a naming question the rule's own reason settles.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- <path>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-22 | → proposed | **Raised while restating T-057's DS-140 criterion, and it is not what that restatement was looking for.** T-057's criterion asked for a ruling the owner dissolved on 2026-08-19, so the question was which rule now decides whether a 3D wobble is admissible. The answer is that DS-140's admission test admits it and **DS-142's checker rejects it**, on a class name — so the criterion was blocked by a rule nobody had asked. `PH1` because a published gate fails a deck for a design choice the ruleset permits, which is `CLAUDE.md`'s stated case for reopening it; `m` because the fix is one probe branch, one declaration and two seeded variants, and `high` because it gates [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) and reaches an adopter with no 3D at all. |
