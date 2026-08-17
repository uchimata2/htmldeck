---
id: T-124
title: An adopter cannot refresh a deck's shell after an upgrade, so every release breaks every deck
type: deliverable
status: done
phase: review
shipped_in: 0.3.0
parent: null
blocked_by: []
related: [T-085, T-108, T-116, T-036]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - tools/deck/shell.py
  - docs/PUBLISHING.md
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

**It cost this repository on the day after it was raised, and the hand path has a known failure**
[T-036](T-036-the-second-contents-page-for-long-decks.md) changed `shell/components.css` and
`shell/deck.js` on 2026-08-13 and had to push both into three tracked decks. With no command, that
was a throwaway script composing `cut` and `fill` — the same four lines this task is about, written
once and thrown away, which is the argument for having them installed. **And it went wrong**: one of
the three is `examples/reference-deck-seeded-defects.html`, which `seed_defects.py` *generates*, so
writing the shipped component block into it deleted eleven lines of seeded CSS. `shell.py check`
then reported the file clean, because by its own measure it was. **L-77.** So the missing command
costs this project too, and the ad-hoc replacement for it has a failure mode worth naming in the
command's own output.

**Scope**
- In: a command that replaces a deck's shell regions with the installed ones, leaving the eleven
  per-deck slots untouched, and refusing rather than guessing when a deck's regions cannot be cut.
- In: **the skeleton as well as the two named regions.** `check` compares three things against
  `shell/`, not two — the markup outside the regions is the third, and a release can move it.
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
      comparing the eleven regions, not by reading the output. **The command asserts this itself and
      refuses to write when it fails**, rather than leaving it to a test that ran once.
- [ ] A deck whose shell was hand-edited is reported rather than silently overwritten.
- [ ] The report says what changed, per region, in a file the adopter cannot read.
- [ ] It is idempotent — running it twice changes nothing the second time.
- [ ] Run against a real deck from an older release, not a fixture built for the test.
- [ ] The output names the generated-file trap once (**L-77**).

**Open questions**
- ~~Does this belong to the adopter as a command, or to the plugin as something the skill runs when
  it notices a version gap?~~ **Answered 2026-08-13: a command, and the two are not alternatives.**
  Every other shell operation is one — `new`, `icons`, `preflight`, `check` — and `check` is what
  reports the gap, so the fix belongs beside the report. The deciding reason is in the scope above:
  an adopter has to review a change to a 250 KB file they cannot read, and a rewrite that happens
  because the skill noticed something is the opposite of reviewable. **The skill calling the command
  when it notices a version gap stays available and is not foreclosed** — it needs the command to
  exist either way, and it should invoke the same reviewable thing an adopter does.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `sync(html)` — cut the deck, fill the **installed** skeleton with its eleven parts, and refill the script skeleton with the deck's three | the four lines, in `shell.py` |
| 2 | `changes(old, new)` — what moved, per region, with the first difference in each | the report a reader can act on |
| 3 | The guard: cut the result and compare every per-deck part with the original's. Any drift and the command refuses to write | the assertion, inside the command |
| 4 | Wire `sync <deck>` — reports by default, writes on `--write` | the CLI |
| 5 | Self-test fixtures: a stale deck syncs clean, the parts survive, a hand-edited shell is reported, a second run is a no-op, and a deck that is not a shell is refused | `shell.py --self-test` |
| 6 | Run it on a **real deck one release behind** — this repository's own at the `v0.2.2` tag — and check that `shell.py check` fails before and passes after | the evidence |
| 7 | `docs/PUBLISHING.md` §8.1 gains the sentence it has not been able to write for three releases, and the module docstring gains the command | the release procedure |

**Approach decisions**

- **The report is the default and `--write` is the flag, which inverts `icons` and `preflight`.**
  Those two *derive* a region from the deck's own content, so running them is idempotent and
  self-evidently right. This one *overwrites* the deck's shell with a foreign one and cannot tell a
  version gap from a deliberate edit — nothing in the deck records which release built it. Since the
  two cannot be distinguished, every sync is reported before it is applied, which satisfies the
  hand-edited criterion without needing to detect the case at all.
- **The guard lives in the command, not in the test.** A test proves the property held once on one
  fixture; the assertion proves it on the adopter's deck, which is the file that matters and the one
  nobody here will ever see.
- **The skeleton is refreshed too.** `check` compares three things and the scope named two; a command
  that fixed two of three would leave a red run and no next step, which is the state this task exists
  to end.

## 3. Implement

**Decisions & assumptions**

- **The command is four lines, and that is the finding rather than a boast.** `sync` cuts the deck
  into its parts and fills the **installed** `shell/shell.html` with them, refilling the script
  skeleton with the deck's own three declarations. That is the same lossless operation that made
  `shell.html` in the first place, run in the other direction. The mechanism has been sitting in
  this file since T-085 and only ever composed one way — `new` — which is why three releases could
  name no smallest edit for a shell change. Everything else in this task is the guard, the report
  and the words. — 2026-08-13
- **`sync` does not need to know what changed in the release, and must not.** It carries no list of
  versions, no migration table and no notion of *older*: it writes what is installed. A deck from
  any release, or from none, reaches the current shell in one run, and a release that adds a shell
  change adds nothing here. — 2026-08-13
- **The `v0.2.2` deck came out with exactly one problem left, and it is the right one.** Before:
  `COMPONENTS differs`, `SCRIPT differs`, and `STAGE TABLE` — eight stages against seven icons.
  After: `STAGE TABLE` alone. The two shell failures were the deck being a release behind; the third
  is a real defect in that deck's own content, and a shell sync that had fixed it would have been
  overreaching. **The division is the product**, not the byte count. — 2026-08-13
- **The report's closing paragraph names the generated-file trap, unconditionally.** It cannot be
  detected — in an adopter's repository there is no way to know that some other tool writes the file
  — so it is stated once, every time, in the place where someone is about to type `--write`.
  **L-77**, which this project earned the day before. — 2026-08-13

**What was measured**

The real deck one release behind, taken out of git at the `v0.2.2` tag as bytes rather than through
a shell redirect, which would have rewritten its line endings and made every comparison a lie:

```
--- before
  COMPONENTS    differs from shell/components.css
  SCRIPT        differs from shell/deck.js
  STAGE TABLE   STAGES has 8 entries and STAGE_ICON has 7
  3 problem(s).

--- sync
  COMPONENTS   815 lines -> 860 lines
  SCRIPT       686 lines -> 826 lines
  2 region(s) would change; 12 per-deck region(s) untouched. Nothing written.

--- after --write
  STAGE TABLE   STAGES has 8 entries and STAGE_ICON has 7
  1 problem(s).

--- run again
  OK - already carries the installed shell. Nothing to sync.

--- and it still prints
  printed pages: 14 declared, 14 counted, wanted 14 (13 slides + 1 contents sheet) pass
```

Twelve per-deck regions, not eleven: nine top-level slots other than `COMPONENTS` and `SCRIPT`, plus
the three declarations nested inside the script.

**Outputs produced**
- [`tools/deck/shell.py`](../tools/deck/shell.py) — `sync`, `kept`, `changes`, the `sync` command,
  eleven new self-test fixtures, and the docstring
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §8.1 — the `0.2.3` row names a command, and the
  paragraph under the table says what the rule for writing such a row now is
- [`shell/README.md`](../shell/README.md) — `sync` as the other direction of `check`
- [`skills/htmldeck/references/build.md`](../skills/htmldeck/references/build.md) — what to do when
  `shell.py check` reports the two region failures on a deck nobody edited

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| A deck one release behind passes `shell.py check` after the command and not before | **met** | Three problems before, one after — and the one that survives is `STAGE TABLE`, a defect in that deck's own content rather than in the shared half. A sync that had cleared it would have been reaching into the eleven regions it exists to protect. Also asserted as fixtures, one per region `check` compares, since one real deck is one sample |
| Every per-deck slot survives byte for byte, asserted by cutting before and after — **and the command asserts it itself** | **met** | `kept()` flattens the twelve per-deck regions and the command compares them across the sync; any drift and it prints `REFUSING`, writes nothing, and says the defect is in `shell.py` rather than in the deck. The self-test asserts the same on the reference deck, which has something in every region — a fresh skeleton would have passed it vacuously |
| A deck whose shell was hand-edited is reported rather than silently overwritten | **met** | Every sync is reported before it is applied, which settles the case without detecting it — and it cannot be detected: nothing in a deck records which release built it, so a version gap and a deliberate edit are the same bytes. The report says so in as many words |
| The report says what changed, per region | **met** | Region, line count before and after, and the first difference with both sides — `COMPONENTS 815 lines -> 860 lines`, `first at line 486`. Enough to tell the shell moving from an edit of one's own being reverted, which is the judgement no program here can make for the adopter |
| Idempotent | **met** | The second run prints `OK - already carries the installed shell. Nothing to sync.` and returns 0. Asserted as a fixture too: `sync(sync(x)) == sync(x)`, and `sync(reference-deck) == reference-deck` exactly, which is the round-trip the whole tool rests on |
| Run against a real deck from an older release, not a fixture built for the test | **met** | This repository's own deck at the `v0.2.2` tag, extracted as bytes rather than through a shell redirect. It still prints 14 correct pages after the sync, so the upgrade is a deck that works and not just a deck that passes |
| The output names the generated-file trap once (**L-77**) | **met** | In the closing paragraph of the report, unconditionally, because it cannot be detected from the file |
| *(added)* A file that is not a shell is refused rather than guessed at | **met** | `NotAShell` names the missing anchor and the command exits saying it will not guess. This is `sync`'s worst failure mode — a partial cut would write the shell into the wrong offsets of a 250 KB file — so it is a fixture rather than an inference from `cut` |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → done | **Seven criteria met and one added, and the command is four lines.** `cut` and `fill` have been in `shell.py` since T-085 and were only ever composed one way; `sync` composes them the other way, which is why three releases could name no smallest edit while the mechanism sat in the file. Everything else in the task is the guard, the report and the words. **The result worth keeping is the division**: the `v0.2.2` deck went from three problems to one, and the one that survived is a defect in that deck's own content. A sync that had cleared it would have been reaching into the regions it exists to protect. The added criterion is the refusal — a partial cut writing the shell into the wrong offsets of a 250 KB file is this command's worst failure, so it is a fixture and not an inference from `cut`. §8.1's `0.2.3` row now names a command, and the paragraph under the table says that naming one is the rule for a shell change from here. |
| 2026-08-13 | → in_progress |  Nothing in the plan changed under implementation, which is worth one row because it is unusual here: the seven steps ran in order and the two arguable decisions — report by default, guard inside the command — both held on contact. The one thing the plan did not anticipate is the shape of the answer on the real deck. Three problems became one rather than none, because `STAGE TABLE` is per-deck content; that is `sync` behaving correctly and it is now the headline of §4 rather than a caveat in it. |
| 2026-08-13 | → planned | Seven steps, and the one decision worth arguing is that **the report is the default and `--write` is the flag**, which inverts how `icons` and `preflight` behave. Those derive a region from the deck's own content; this one overwrites the deck's shell with a foreign one, and nothing in a deck records which release built it, so a version gap and a deliberate edit are the same bytes. Reporting every time satisfies the hand-edited criterion without having to detect the case. Two things also moved into the command from where a plan would normally put them: the per-deck-slots assertion, because it has to hold on the adopter's file rather than on a fixture here, and the skeleton, because `check` compares three regions and a command fixing two of them leaves a red run with no next step. |
| 2026-08-13 | → specified | **The open question answered — a command, and the skill-runs-it alternative is not an alternative.** `check` reports the gap, so the fix belongs beside the report; and the scope's own reason decides it, since an adopter has to review a change to a file they cannot read and a rewrite triggered by the skill noticing something is the opposite of reviewable. The skill may still call it. §1 also gained evidence the task did not have when it was raised: **the gap bit this repository the next day.** T-036 changed both shell files and pushed them into three decks with a throwaway script, and one of the three was a *generated* fixture, so the sync deleted eleven lines of seeded CSS and `shell.py check` called the result clean (**L-77**). Four criteria added from that — the report says what changed, the command asserts the per-deck slots survive rather than leaving it to a test, it is idempotent, and its output names the generated-file trap once. |
| 2026-08-13 | → proposed | Raised while preparing `0.2.3`'s §8.1 row, which is the third release running that cannot name a smallest edit for a shell change. `PH3` and `m` by [`../CLAUDE.md`](../CLAUDE.md)'s rule — a new capability, not a defect in the published plugin: nothing is wrong, there is simply no command. `high` because the cost falls on every adopter at every release and grows with the number of decks in the wild. |
