---
id: T-306
title: Wire an icon-first source item in quickview.py, and make shell.py sync name a stale chrome tail
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-299, T-269]
work_package: PH1
shipped_in: unreleased
owner: the project owner
business_value: medium
effort: s
created: 2026-09-13
updated: 2026-09-14
deliverables: [tools/deck/quickview.py, tools/deck/shell.py]
---

# T-306 — Wire an icon-first source item in quickview.py, and make shell.py sync name a stale chrome tail

## 1. Specify

**Outcome**
Two build-path tools stop reporting a state that is false. Today `quickview.py`'s item pattern fixes
the id before the icon, so a `.sources-item` whose icon comes first is invisible to `wire` and `plan`
and is reported as uncited. And `shell.py sync` ends by counting regions (`tools/deck/shell.py`
`:1265`) and never runs or names `tail` (`:198`), so a deck whose chrome tail is a release behind is
reported fully up to date.

**From the adopter report** [`03`](../docs/adopter-reports/nextep/2026-09-06-quickview-cannot-wire-an-icon-first-source-item.md), [`15`](../docs/adopter-reports/nextep/2026-09-08-shell-sync-is-silent-about-a-stale-chrome-tail.md).

**Re-run in triage, 2026-09-13, on this tree.** `item_pattern()` matched the id-first ordering and
returned no match for the icon-first one. `15` was confirmed from source.

**Scope**
- In: the two optional groups of the item pattern made order-independent, the record's own alternation
- In: one line at the end of `sync` naming `shell.py tail <deck>`, the way `sync` already names
  `shell.py tokens --write` for undeclared tokens
- Out: anything the records above do not name. The report is a closed one-way hand-over, so a
  question this task cannot answer is settled here rather than asked

**Inputs**
- the two records above, each with its command, its version and its own proposed fix
- [T-299](T-299-triage-the-nextep-adopter-report.md) section 3

**Acceptance criteria**
- [ ] records `03` and `15` are each closed with the remedy measured, or deferred with the reason
      recorded in this task
- [ ] each fix is proved by seeding the defect and watching it fire, in both directions (**L-125**)
- [ ] `python tools/tasks/lint.py` and `python tools/check_all.py` green, run separately

**Open questions**
- None. Each record carries its evidence and a proposed fix; the proposal is a hypothesis to measure
  before committing to it.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Run `shell.py sync` and `tail` on a copy of the reference deck whose `Motion` sits outside the menu, before any change | the before half of `15` |
| 2 | Add an icon-first fixture to `quickview.py`'s self-test and watch it fail; then make `ITEM_HEAD` accept either order and watch it pass | `03`, both directions |
| 3 | `shell.py`: compare the tail read-only in `sync` and name `tail` when it is behind, with a fixture for each answer; re-run step 1 | `15`, both directions |
| 4 | `lint.py`, then the full `check_all.py`, run separately | the gate |

## 3. Implement

**Decisions & assumptions**
- `ITEM_HEAD` takes record `03`'s own alternation, unchanged. — 2026-09-14
- `sync` compares the tail read-only and names `tail` only when the tail is behind, the way it names
  `tokens --write` only when a token is missing. That is record `15`'s second fix. Its first, a line
  printed every time, would be noise on every current deck. — 2026-09-14
- The line is printed on the `OK - … Nothing to sync.` path too, and that path is where this tree
  showed the defect. Record `15`'s deck also had shared regions to change. A deck current in those
  regions and behind in the tail got `OK` and nothing else. — 2026-09-14
- The exit code does not change. It stays about the regions a sync writes, so no script that reads
  it changes, and a deck that rewords its tail on purpose is not failed by `sync`. — 2026-09-14
- `03` is measured on the self-test fixture rather than by `quickview.py plan` on a deck. `plan`
  reaches the item through the same `item_pattern` the fixture calls. — 2026-09-14

**Evidence**, on this tree:

| Probe | Before | After |
| :--- | :--- | :--- |
| `quickview.py` self-test, a glyph-first item | `SELF-TEST FAILED: an item whose kind glyph comes before its identifier does not match` | passes, and wiring keeps the glyph before the identifier |
| `shell.py sync` on a copy of the reference deck with `Motion` moved outside the menu | `OK - … already carries the installed shell. Nothing to sync.` and nothing more, while `tail` on the same copy reported `` `Motion` would move inside the menu (DS-218)`` | the same `OK` line, then a `CHROME_TAIL` row naming `shell.py tail <deck> --write`; exit 0 |
| `shell.py sync` on the reference deck | not run | `OK`, no `CHROME_TAIL` row |
| `shell.py` self-test with `tail_behind` seeded to answer no, then yes | not applicable, the function is new | each seed fails exactly one of the two new fixtures |

**Outputs produced**
- `tools/deck/quickview.py`: `ITEM_HEAD` in either order, and a glyph-first fixture
- `tools/deck/shell.py`: `tail_behind`, which `sync` reports, and a fixture for each answer

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Records `03` and `15` closed with the remedy measured, or deferred | met | Both measured before and after on this tree. The table in section 3 |
| Each fix proved by seeding the defect and watching it fire, in both directions | met | `03`: the fixture fails on the old pattern and passes on the new one. `15`: `sync` is silent before and names `tail` after, and each seed of `tail_behind` fails one fixture |
| `lint.py` and `check_all.py` green, run separately | met | Run in that order on the tree this task's commit carries. The counts are in the pull request |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-13 | -> proposed | Raised by T-299 from Nextep records `03` and `15`. `PH1`: an adopter met both in the published `0.7.0`. `15` arrived as `friction` and is ruled a defect, because the tool reports a deck up to date when it is not. |
| 2026-09-14 | -> in_progress | Section 1 was complete from triage and needed no change. Planned, and started after `/compact` in the session that closed `T-310`, as the compact arm of `T-290`. |
| 2026-09-14 | in_progress -> done | `ITEM_HEAD` accepts either order, and `sync` names a chrome tail that is behind. Each is measured in both directions. |
