---
id: T-124
title: An adopter cannot refresh a deck's shell after an upgrade, so every release breaks every deck
type: deliverable
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-085, T-108, T-116]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-13
updated: 2026-08-13
deliverables: []
---

# T-124 — An adopter cannot refresh a deck's shell after an upgrade, so every release breaks every deck

## 1. Specify

**Outcome**
A deck built on an older release can be brought up to the installed shell by running a command,
instead of by rebuilding it or by hand-patching two regions of a 250 KB file.

**The mechanism**

`shell.py check` compares a deck's `COMPONENTS` and `SCRIPT` regions with `shell/components.css` and
`shell/deck.js` **byte for byte**, which is what makes the shared half trustworthy (T-085). The other
edge of that: **any release touching either file makes every existing deck fail**, whether or not the
deck's author did anything.

Measured on 2026-08-13, running the `0.2.3` tooling against this repository's own deck as it stood at
`fa3c439`:

```
COMPONENTS    differs from shell/components.css
SCRIPT        differs from shell/deck.js
STAGE TABLE   STAGES has 8 entries and STAGE_ICON has 7
```

The third is a real defect in that deck and the new gate finding it is the gate working. **The first
two are not defects at all** — they are the deck being one release behind, and there is no command
that fixes them. `shell.py` offers `new`, `icons`, `check` and `parts`; `new` builds an empty deck,
and pointing it at a deck with slides in it is not an upgrade path.

**This is the third release running to do it**, and [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md)
§8.1 exists because of the first two. That section makes the breakage *legible* — it names what newly
fails and the smallest edit — and for `0.2.1` the smallest edit was a command
(`shell.py preflight <deck>`). For a shell change there is no such sentence to write.

**Scope**
- In: a command that replaces a deck's shell regions with the installed ones, leaving the eleven
  per-deck slots untouched, and refusing rather than guessing when a deck's regions cannot be cut.
- In: what it does about a deck whose shell was *deliberately* edited — the case `check` exists to
  catch. Overwriting silently would destroy the evidence of a defect.
- In: whether it reports what it changed, since an adopter has to review a diff in a file they
  cannot read.
- Out: migrating per-deck content across a contract change. `0.2.0`'s `Sources:` field and `0.2.2`'s
  `data-stage` index are authored facts; this is about the half nobody authors.
- Out: the byte-for-byte comparison itself. It is what makes the shared half worth sharing.

**Inputs**
- [`../tools/deck/shell.py`](../tools/deck/shell.py) — `cut`, `fill`, `SLOTS`, `SCRIPT_SLOTS` are
  already the whole mechanism; `new` composes them in the one direction that exists.
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8.1 — the table this would give an answer to.
- [T-085](T-085-the-reference-deck-does-not-carry-the-shell-it-defines.md) — why the comparison is
  byte for byte.

**Acceptance criteria**
- [ ] A deck one release behind passes `shell.py check` after the command and not before.
- [ ] Every per-deck slot survives byte for byte — asserted by cutting the deck before and after and
      comparing the eleven regions, not by reading the output.
- [ ] A deck whose shell was hand-edited is reported rather than silently overwritten.
- [ ] Run against a real deck from an older release, not a fixture built for the test.

**Open questions**
- Does this belong to the adopter as a command, or to the plugin as something the skill runs when it
  notices a version gap — the owner.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised while preparing `0.2.3`'s §8.1 row, which is the third release running that cannot name a smallest edit for a shell change. `PH3` and `m` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — a new capability, not a defect in the published plugin: nothing is wrong, there is simply no command. `high` because the cost falls on every adopter at every release and grows with the number of decks in the wild. |
