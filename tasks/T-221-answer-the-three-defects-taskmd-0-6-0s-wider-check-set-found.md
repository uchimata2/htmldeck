---
id: T-221
title: Answer the three defects taskmd 0.6.0's wider check set found
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-098, T-161, T-163]
work_package: PH3
owner: the project owner
business_value: high
effort: s
created: 2026-08-23
updated: 2026-08-23
deliverables: []
---

# T-221 — Answer the three defects taskmd 0.6.0's wider check set found

## 1. Specify

**Trigger**

taskmd `0.6.0` reached the plugin cache on 2026-08-23. `python tools/tasks/lint.py` ran green
earlier the same session and then reported **`FAILED at taskmd check (exit 1)`, 3 problems**, with
no file in this repository changed between the two runs beyond one prose line in
[`../docs/RELEASE-PHASES.md`](../docs/RELEASE-PHASES.md). **The gate widened; the tree did not
move.** `check` also gained `front-matter value(s)`, `closed record(s)`, `table row(s)` and
`section reference(s)` to what it counts, and `lint.py` now runs `taskmd index` as its first step.

**The three, each verified by hand rather than taken from the checker**

| # | What `check` says | Verified against the file | Class |
| :-- | :--- | :--- | :--- |
| 1 | `CLOSED PARENT T-016 is 'done' with child T-057 still open` | [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) carries `parent: T-016` and `status: proposed`; [T-016](T-016-the-interaction-and-motion-layer.md) is `done` | a real status contradiction |
| 2 | `ABANDONED SLOT tasks/T-003-brief-mode-elicit-the-six-section-prompt.md body line 29 still reads '- <decision — rationale — date>'` | line 45 of [T-003](T-003-brief-mode-elicit-the-six-section-prompt.md), which is `cancelled`; the slot is the template's §3 line and was never filled | record hygiene |
| 3 | `WIDE ROW docs/upstream/harness.md:32 has 3 cells against a 2-column header` | line 32 carries four pipes where lines 28–31 carry three; the third cell's text renders nowhere | **content that exists and is invisible** |

**Why the third one is the interesting one.** It is the exact failure mode this project reported
upstream as `O-T4` in [`../docs/upstream/taskmd.md`](../docs/upstream/taskmd.md), and
[T-161](T-161-decide-whether-to-adopt-the-wide-row-gate-now-that-upstream-ships-one.md) declined to
build the local gate after measuring **307 files and 0 wide rows** on 2026-08-15. The offending row
is `O-C3`, whose own text dates its measurement to 2026-08-20 — **after that sweep** — so this is a
new instance rather than one the sweep missed. **T-161's refusal is not falsified by it.** Adopting
their gate rather than building one was supposed to buy exactly this catch, and it did, five days
later and without a line of code here.

**Scope**

- In: the three findings, and for each, whether it is a defect to fix or a rule to state.
- In: `lint.py` back to exit 0.
- Out: any other check class `0.6.0` added. Nothing else fired, and a class that fires on nothing is
  not evidence about this tree.
- Out: re-deriving `0.6.0`'s full check set from its source. What fired is what is in scope.

**Acceptance criteria**

- [ ] `python tools/tasks/lint.py` exits 0, and the record pastes what it printed.
- [ ] Finding 1 closes on a decision about which of the two records is wrong, not on whichever field
      is cheaper to edit.
- [ ] Finding 3's third cell is either moved somewhere it renders or deleted on purpose, and the
      record says which and why.
- [ ] Whether `docs/upstream/harness.md` was ever sent to anyone carrying that invisible cell is
      stated either way.

**Open questions**

- **Finding 1 — which of T-016 and T-057 is wrong?** My reading: **T-057 is not a child.** It is
  `PH3`, `effort: l`, `blocked_by: [T-214]` and was created after T-016 shipped the layer, which is
  the shape of a later spin-off rather than a part of the umbrella. If that is right the fix is
  `parent: null` plus `related`, and T-016 stays `done`. The alternative — reopening T-016 — makes a
  shipped release's task open again. **Owner answers**, because it is a claim about what the layer
  was meant to contain.
- **Finding 2 — is the placeholder a defect, or is the gate right about a class this project has
  never ruled on?** My reading: fix the one instance, and do not write a rule. One occurrence in 220
  task files does not argue for a convention. **Decidable here** unless the owner disagrees.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Put finding 1's question to the owner before touching either file | An answer in the Log |
| 2 | Recover finding 3's third cell from the file, decide where it belongs, and repair the row | `docs/upstream/harness.md` |
| 3 | Check whether that document was sent, and say so | This record |
| 4 | Clear finding 2's slot in T-003 | `tasks/T-003-brief-mode-elicit-the-six-section-prompt.md` |
| 5 | Re-run `lint.py` and paste the output | This record |

## 3. Implement

**Decisions & assumptions**

- Not started.

**Outputs produced**

- Not started.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| | | Not started. |

**Child fix tasks raised**

- none yet.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-23 | → proposed | **Raised at a session close, by the gate turning red under the session's feet.** The session installed nothing and edited none of the three files; taskmd `0.6.0` arrived in the plugin cache and `lint.py` found what had been there all along. `PH3` by [`../CLAUDE.md`](../CLAUDE.md)'s rule: PH2 has shipped and none of the three is a defect in the published plugin, so size does not put it in PH1. `high` rather than `medium` because a red `lint.py` is the gate every task edit owes, so this blocks the next edit to any task, not only to these. |
