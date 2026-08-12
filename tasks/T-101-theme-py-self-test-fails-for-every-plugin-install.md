---
id: T-101
title: theme.py exits on its own self-test for every plugin install, so no adopter can run it
type: fix
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-059, T-064, T-074, T-075, T-090]
work_package: PH1
owner: the project owner
business_value: high
effort: s
created: 2026-08-12
updated: 2026-08-12
deliverables:
  - tools/deck/theme.py
---

# T-101 — theme.py exits on its own self-test for every plugin install, so no adopter can run it

## 1. Specify

**Where this came from.** The adopting project, building and re-authoring a twelve-slide deck. It is
`Report 2` in that project's own defect report, **written 2026-08-11 and never filed until today** —
the adopter recorded an upstream id for it, the id turned out to belong to an unrelated task, and a
reconciliation on 2026-08-12 found there had never been a task here at all. So this is the first time
it has been seen upstream, and the delay is the adopter's, not anyone's here.

**What happens.** Run from an installed plugin, `theme.py` refuses to report anything:

```
python <plugin-root>/tools/deck/theme.py check <any-deck>.html

SELF-TEST FAILED: the default destination is not under .assets-cache/deck/themed, where
THEME-CONTRACT.md §1 says a themed copy belongs -
'<plugin-root>/examples/.assets-cache/deck/themed/reference-deck-lattice.html'
```

The self-test runs before the command, so **no verdict is produced for any deck**. Run from a git
clone of this repository the same command works and produces nine verdicts on the same deck.

## The cause

`destination()` builds on `paths.output_root(deck)`, which walks up from the **deck** to the nearest
ancestor holding a `.git` and falls back to the deck's own directory when there is none. That is
correct, and it is the `T-074` fix working as intended: an adopter's themed copy lands in the
adopter's project rather than in the package cache.

The self-test then asserts that answer equals the module constant `OUT`, which is anchored on the
tool's own `ROOT`:

| Where htmldeck runs from | `output_root(reference-deck)` | `OUT` | Self-test |
| :--- | :--- | :--- | :--- |
| A git checkout | `<repo>` — the `.git` is found | `<repo>` | **passes** |
| An installed plugin | `<root>/examples` — no `.git` above it | `<root>` | **fails** |

So the assertion holds only when the tool sits inside a repository. Everyone who installs htmldeck
the documented way gets the failing branch; the maintainer, working from a clone, gets the passing
one.

**Verified both ways on one machine, same command, same deck**, at 0.2.0 and again at 0.2.1, and the
two lines are unchanged on `master`:

```
python <plugin-cache>/tools/deck/theme.py check <deck>.html   # SELF-TEST FAILED
python <clone>/tools/deck/theme.py check <deck>.html          # runs, 9 verdicts
```

**Still present at `master`.** The self-test compares `os.path.realpath(default)`'s directory against
`os.path.realpath(OUT)`, and `OUT` is still `os.path.join(ROOT, ".assets-cache", "deck", "themed")`.

**The fourth of one family, and the family is the point.** `build.md`'s `--out`, `DS-064`'s probe for
the reference deck's class names, `SPEC-5`'s slide pattern, and this. Each encodes the reference
environment as though it were the contract; here it is done in a self-test, which is the one place
where the encoding also blocks the tool.

**Why the self-test is right to exist.** It is not the assertion that is wrong. `T-059` is why it is
there — a default destination that overwrote its input cost a recovery — and the guard should stay.
What it must not do is assume the destination is anchored on the tool.

**Scope**
- In: making the self-test's expectation depend on the same input `destination()` depends on, so it
  passes wherever htmldeck is installed and still fails if `T-059`'s defect returns.
- In: a case that would have caught this — the self-test run against a deck outside any repository.
- Out: changing `paths.output_root()` or `destination()`. Both are correct and are `T-074`'s fix.
- Out: the adopter's workaround. Running from a clone works and is what they have been doing.

**Acceptance criteria**
- [ ] `theme.py check` produces verdicts when run from an installed plugin, on a deck outside any
      repository
- [ ] The `T-059` guard still fails when the default destination is the input deck
- [ ] A test covers the installed-plugin case specifically, so this cannot regress silently

**Open questions**
- none.

## 2. Plan

**Phase: `PH1`.** A defect in the published plugin, hit by an adopter on `0.2.0` and still present
on `0.2.1`. The task arrived carrying `work_package: none`, so the phase was derived here from
`CLAUDE.md`'s rule rather than inherited.

| # | Step | Where |
| :--- | :--- | :--- |
| 1 | Make the constant relative, so it cannot name a project at all | `OUT` → `THEMED` |
| 2 | Derive the self-test's expectation from the same deck `destination()` is given | `self_test` |
| 3 | Add the installed case: a deck with no repository above it | `self_test` |
| 4 | Keep `T-059`'s guard exercised, unchanged | `self_test` |
| 5 | Reproduce the adopter's run against a plugin layout with no `.git`, before and after | outside the repo |

**Why not fix the constant alone.** Deleting the assertion would pass everywhere and check nothing;
pointing `OUT` at the deck would make the constant a function of an argument it does not take. The
expectation has to come from the same input as the answer, which is what step 2 says.

## 3. Implement

**The constant is gone.** `OUT` was `os.path.join(ROOT, ".assets-cache", "deck", "themed")` and is
now `THEMED`, the relative fragment, joined onto `paths.output_root(deck)` by `destination()` and
onto `ROOT` only where the self-test wants a scratch path inside this repository. A relative
constant cannot assert which project it belongs to, which is the class of defect
[`paths.py`](../tools/deck/paths.py)'s docstring already names.

**The assertion now reads the deck.** For each of two decks — the reference deck, and one under the
system temp directory with no repository above it — the expectation is
`os.path.join(paths.output_root(where), THEMED)`, and the destination's directory must equal it.
Neither path is created: `destination()` decides and reads nothing, which is what lets the installed
case be constructed on any machine.

**And the placement T-074 exists for is asserted directly**: the outside deck's destination must not
sit under this tool's `ROOT`. That is the half a purely relative comparison would not catch, and it
is the failure an adopter actually suffers — their deck copied into the package cache.

**One thing outside the acceptance criteria, fixed and reported here.** The `usage:` line printed
the same `ROOT`-anchored path, so a `theme.py` with no arguments told an adopter their themed copy
goes into the plugin's own directory. It now names the relative path and says *under the deck's own
project*. Same defect, second place, one line.

## 4. Review

| Criterion | Verdict | Evidence |
| :--- | :--- | :--- |
| `theme.py check` produces verdicts from an installed plugin, on a deck outside any repository | **met** | The tools copied to a directory with no `.git`, a deck beside it: nine verdicts, `DS-011` through `DS-010`, where the same command on `master` exited on the self-test |
| The `T-059` guard still fails when the default destination is the input deck | **met** | `out = deck` re-seeded in that copy: `SELF-TEST FAILED: the default destination is the input deck` |
| A test covers the installed-plugin case, so this cannot regress silently | **met** | The `outside` case. Re-seeding `themed = os.path.join(ROOT, THEMED)` **in a clone** — where the old assertion passed — now fails the self-test |

**The regression test is the point of the third row.** The old assertion could only fail for people
who were not going to run it, so the maintainer's clone was the one environment in which it was
silent. The new one fails in a clone, which is where it will be run.

**Verified in a clone as well**, unchanged: nine verdicts on `examples/reference-deck.html`.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → proposed | Filed from the adopting project's defect report, `Report 2`. **Written there on 2026-08-11 and believed filed here ever since**; a reconciliation of every upstream id that project records found no task for it, which is how a defect that blocks a tool for every adopter sat unreported for a day. Re-verified on `master` before filing rather than trusted from the write-up. |
| 2026-08-12 | → done | Phase derived as `PH1` — the task arrived with `work_package: none`. Fixed, and the `usage:` line carried the same defect and was fixed with it. Reproduced against a plugin layout with no `.git` before and after, and the new case was shown to fail from a clone with the defect re-seeded, which is the environment the old assertion could never fail in. |
