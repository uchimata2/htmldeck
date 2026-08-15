---
id: T-163
title: Correct the coverage claim that carried the wide-row refusal
type: admin
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-161, T-160, T-157, T-139]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-15
updated: 2026-08-15
deliverables: []
---

# T-163 — Correct the coverage claim that carried the wide-row refusal

## 1. Specify

**Outcome**
[`../tools/docs/refcheck.py`](../tools/docs/refcheck.py)'s module docstring states a reversing
condition that **can occur**, and the closed record of
[T-161](T-161-decide-whether-to-adopt-the-wide-row-gate-now-that-upstream-ships-one.md) no longer
asserts, in three places, a fact upstream has disproved. The refusal itself is untouched.

**Why this exists**
T-161 declined to build a wide-row checker here and wrote the refusal into `refcheck.py` with the one
thing that would reverse it: *`taskmd check` reads tasks and the documents it resolves — not `skills/`
or `examples/`. A wide row there is invisible to both tools.* taskmd corrected that on the report
thread, commit `5cf121b`:

> `check` does not read only tasks and the documents they resolve. It reads every Markdown document a
> clone would receive — the whole tree, excluding nested taskmd projects and anything `git ls-files
> --cached --others --exclude-standard` would not send.

**A refusal whose stated trigger cannot fire is worse than one with no trigger at all.** T-161's whole
purpose was that the third asking of this question starts from an answer rather than from the
argument; it now starts from a condition nobody can trip, which reads as *permanent* rather than as
*decided on evidence*.

**Measured here 2026-08-15, rather than taken on their word**
One probe document was written into `examples/` and an identical one into `skills/`, each carrying a
markdown link to a file that does not exist **and** a three-cell row under a two-column header.
`taskmd check` was run and the probes deleted. It reported **both** as `BROKEN LINK`, naming each tree,
and read 316 documents where a clean run of the same command reads 315. The probe paths are not
written here because check 2 of `refcheck.py` resolves a repo-relative pointer inside a fenced block,
and a deleted probe is exactly the dead pointer that check exists to catch — the same reason
[T-161](T-161-decide-whether-to-adopt-the-wide-row-gate-now-that-upstream-ships-one.md) §4 recorded its
scanner's method rather than its output.

Both trees are covered. Their correction is right and `refcheck.py` is wrong.

**The second finding, which the correction did not carry**
The same probe's **wide row was not reported**. The installed skill is `0.5.0`, `v0.5.0` is upstream's
latest release, and the installed source carries no wide-row rule — the gate is on their master,
unreleased, as it was when T-161 was written. So the docstring's *once that release lands this
repository gets it free* is a promise about an unreleased version, and **the class is ungated here
today**. That is not a reason to build one — the measurement behind the refusal is 0 wide rows in 307
files — but a docstring that reads as though the cover is already in place is the same defect as the
one being fixed, one tense away.

**Scope**
- In: `refcheck.py`'s docstring — the coverage sentence, its tense, and the replacement trigger
- In: T-161's three repetitions of the false premise — §1's open question, §3's third decision, §4's
  second review row — **annotated where they stand**, dated, with the original left legible. A closed
  record that is silently rewritten teaches the next reader that closed records are edited invisibly
- Out: **re-opening the refusal.** Upstream's point is that it stands on *better* ground than it was
  given, since the hole it hedged against does not exist
- Out: building the checker, and pinning taskmd's version — both out in T-161, both unchanged
- Out: [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md). Checked 2026-08-15: the register
  carries no copy of the claim, so the correction lands in two files, not three
- Out: a register row for upstream adopting **L-103** as their `T-151`. It is credited on their thread
  and it is their backlog; a row here would be an observation about their record, which the register
  is not for

**Inputs**
- The correction: [`taskmd#1 (comment)`](https://github.com/uchimata2/taskmd/issues/1#issuecomment-5302496417)
- [T-161](T-161-decide-whether-to-adopt-the-wide-row-gate-now-that-upstream-ships-one.md) — the
  refusal, its measurement, and the three places the premise appears
- [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py) — the operative home of the decision
- [`../docs/lessons/L-103.md`](../docs/lessons/L-103.md) — the fixture lesson upstream took

**Acceptance criteria**
- [ ] `refcheck.py` states no condition that cannot occur, and its coverage sentence matches the
      measurement above
- [ ] The replacement trigger names something that **can** happen, so the decision stays falsifiable
- [ ] The docstring separates what the installed taskmd does **today** from what upstream's master will
      do when released
- [ ] T-161's three repetitions are annotated rather than rewritten, each dated and pointing here
- [ ] The measurement is reproducible from this record alone — the probe is thrown away, so the method
      is written down, as T-161 did for its scanner
- [ ] `python tools/tasks/lint.py` green

**Open questions**
- **What replaces the trigger?** Recommend: **the lint chain stops running `taskmd check`** — then the
  class is genuinely ungated here and the narrow thing is the fallback — kept alongside the standing
  one, *a wide row that appears anyway*, which the corrected coverage makes upstream's alarm rather
  than a blind spot. Decided at implement; not handed back.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Rewrite the last two paragraphs of `refcheck.py`'s docstring: coverage as measured, the tense split between installed `0.5.0` and upstream master, the replacement trigger, the GFM trap kept | The decision, falsifiable again, in the file that owns it |
| 2 | Annotate T-161 §1, §3 and §4 where each states the false premise, dated and pointing here, original legible | A closed record that shows its correction instead of hiding it |
| 3 | Add the Log row to T-161 recording the correction after close | The status history says why the record changed |
| 4 | Gates, commit | `python tools/tasks/lint.py`, one commit |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

**Outputs produced**
- `...`

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-15 | → proposed | Raised from taskmd's correction on the report thread, commit `5cf121b`: `check` reads **every** Markdown document a clone would receive, not tasks and the documents they resolve. That voids the reversing condition T-161 put in `refcheck.py`'s docstring one day earlier. **Reproduced here before accepting it** — a probe seeded into `skills/` and `examples/` was reported by the installed `0.5.0`, and the same probe's wide row was not, because the gate is still unreleased upstream. The refusal stands; the trigger under it does not. `xs`, `admin`, `PH3`. |
