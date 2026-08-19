---
id: T-187
title: Open DS-140's closed motion vocabulary into a style guide, keeping the rules that protect behaviour
type: decision
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-057, T-112, T-016]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-19
updated: 2026-08-19
deliverables: []
---

# T-187 — Open DS-140's closed motion vocabulary into a style guide, keeping the rules that protect behaviour

## 1. Specify

**Outcome**
DS-140 stops being an allow-list. A motion that follows the project's motion principles is
admissible whether or not it carries one of four names, and the four names survive as a **suggested
starter set**. The rules that protect observable behaviour — the duration cap, print, reduced
motion, the stop control — stay `hard` and unchanged. What replaces the closure is a written motion
style guide the critique pass can argue from and a person can extend.

**The owner's ruling, recorded 2026-08-19**
Asked whether the wobble in [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md)
is a fifth motion or an exemption, the owner rejected the frame of the question:

> *"Please don't limit the animation to a specific 'allow list'. Any animation, that aligned with the
> rules can be implemented. I prefer a list of suggested animation to add to enrich the document for
> highlighting, or emphasizing content. Some principles, but not complete rules:*
> 1. *Keep animation gentle.*
> 2. *Add significant animation when it is specifically requested.*
> 3. *Ease in/out is the preferred default for almost everything.*
> 4. *Sequence length might default to 300-500ms. It can be longer, if it's for illustration or upon request.*
> 5. *Add 1-1 animation to the content of each page, but if there's no room for that, skip it.*
> 6. *Don't design the page driven by the animation itself, only if its topic is about motion,
>    transition, animation, or specifically requested. Or, later, when the selected theme for the deck
>    is an animation-rich or 3D style.*
> 7. *...and so on. These are not hard rules, more like a style guide. And can be adjusted, refined,
>    extended."*

Put a second time with the blast radius stated, the owner chose **open the list, keep the safety
rules** over opening it fully, over adding a fifth name, and over writing the guide while leaving the
rule contradicting it.

**Two of the six principles are already rules, and that is the finding that makes this tractable**
Principles 3 and 4 restate **DS-141** as amended by T-016 — eased rather than linear, entries and
transitions inside 500 ms. So the guide does not replace DS-141; it agrees with it. What is genuinely
new is principle 6, which no rule states: *the page is not designed around its own animation*.

**The blast radius, measured 2026-08-19**
DS-140's closure is load-bearing for six rules and one self-test. Each has to be re-derived, not
merely re-worded, because each currently reasons *from* the closure:

| Cites the closure | What it reasons from today | What it needs once the list opens |
| :--- | :--- | :--- |
| DS-141 | a duration over 500 ms is admitted only when DS-140 names the motion | a stated exception condition that does not depend on a name |
| DS-146 | a chart draw-in must be Rise, because a stroke-dash draw "would add one to a vocabulary DS-140 fixes at four" | the rule's own reason, restated without the count |
| DS-218 | `Current` is infinite, therefore a stop control | unchanged in force; the trigger becomes *any* looping motion, which it already says |
| DS-221, DS-224 | pin motion off before capture / for print | unchanged; they name DS-140 as the source of looping and of pre-animation state, not as a limit |
| DS-230 | copies DS-140's closure as the precedent for its own closed list of four editorial kinds | **decide explicitly** whether that precedent survives. Opening DS-140 does not open DS-230, and the borrowed argument must not be read as opened by inheritance |
| DS-238 | "DS-140's vocabulary ... binds unchanged at 100" | reworded; density still never admits a non-conformant motion, but conformance stops meaning *named* |
| `audit.py` self-test | asserts the DS-140 row reports a verdict at all — the T-051 fault, absence read as conformance | the row becomes a principles check; the self-test must still fail loudly when it returns nothing |

**Scope**
- In: amending DS-140 from a closed vocabulary to a suggested set plus admission principles, with the
  reason stated per DS-000.
- In: the six dependent rules above, each re-derived rather than patched.
- In: a written motion style guide — the owner's principles, extended where the ruleset already
  implies one, and marked as guidance rather than as gates.
- In: what `check.py` and `audit.py` can still decide once names stop being the test, and saying
  plainly which motion judgements move from `auto` to `judge`.
- In: principle 6 as a new rule or as guidance — argued either way, not assumed.
- Out: **building any new motion.** T-057's 3D visual is the first consumer, not part of this.
- Out: DS-230's editorial vocabulary. It borrowed DS-140's argument; whether it keeps it is a
  decision this task records and does not take on DS-230's behalf.
- Out: the density default. [T-188](T-188-raise-the-shipped-motion-density-default-to-100.md) carries it.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §5.2 — DS-140, DS-141, DS-146, DS-218, DS-221,
  DS-224, DS-230, DS-237, DS-238.
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §4 — the argument that a named vocabulary
  is what stops animation becoming decoration. **This is the argument being overturned**, so the task
  answers it rather than ignoring it.
- [`docs/COMPONENT-CONTRACT.md`](../docs/COMPONENT-CONTRACT.md) §3.8 — what a motion declares to be
  part of the layer rather than beside it.
- [T-016](T-016-the-interaction-and-motion-layer.md) §1 — the exemption case the owner has now
  superseded with a wider ruling.

**Acceptance criteria**
- [ ] DS-140 states a suggested set and an admission test, with DS-000's stated reason, and no
      sentence in the ruleset still asserts a count of four motions.
- [ ] Each of the six dependent rules is re-derived, and the table above is filled in with what each
      became — including DS-230's precedent decided explicitly either way.
- [ ] The motion style guide exists, is reachable from the brief, and is marked guidance.
- [ ] Every rule that protects observable behaviour is still `hard` and still fails a deck that
      breaks it: a proof for each of the 500 ms cap, print, reduced motion, and the stop control,
      run against a seeded defect rather than asserted.
- [ ] `audit.py`'s DS-140 self-test still fails loudly when the row returns nothing.
- [ ] `python tools/check_all.py` green; the rule count in `CLAUDE.md` re-measured rather than
      carried forward.

**Open questions**
- Does DS-230's closed editorial vocabulary keep the argument it borrowed? Owner, once the amended
  DS-140 is written and the borrowing can be read in its new form.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- none yet

**Outputs produced**
- none yet

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none yet

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-19 | → proposed | Created from the owner's ruling of the same day, taken while resuming a handoff whose whole purpose was to put four open questions to them. It supersedes T-057's open question rather than answering it: asked to choose between a fifth motion and an exemption, the owner rejected the allow-list itself. Raised as its own task because DS-140's closure is cited by six rules and one self-test, so this is a ruleset change under DS-000 and not an edit to one row. |
