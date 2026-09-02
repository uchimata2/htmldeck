---
id: T-293
title: The second context-economy run's three Low findings, in one pass
type: fix
status: done
phase: review
parent: T-287
blocked_by: []
related: [T-286, T-132]
work_package: PH3
owner: the project owner
business_value: low
effort: xs
finding: CE-19
created: 2026-09-02
updated: 2026-09-02
shipped_in: unreleased
deliverables: []
---

# T-293 — The second context-economy run's three Low findings, in one pass

## 1. Specify

**Outcome**
Three `Low` findings from [`../docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) §6.3 closed in one
pass, each `xs`. The front matter binds `CE-19`; `CE-20` and `CE-21` are batched here because
`findings.py` binds one id per task, and their rows in §6.3 name this task.

- **`CE-19`** — `tools/deck/check.py` prints **29,980 bytes** on a green run by default, up from
  17,391 on 2026-08-13, against **398** under `--quiet`. L-153's rule — quiet when stdout is not a
  terminal, the account on a terminal, everything on a red run — was applied to four document tools
  and not to the tool that prints most. Apply it; the self-test already asserts a red run is never
  swallowed.
- **`CE-20`** — five entries in the memory index duplicate a rule that has a home in `CLAUDE.md` or
  the owner's global preferences: the two publishing rules, the trailer rule, the PowerShell command
  rule, and the incoming-labels rule. About 930 of 9,014 bytes, paid every turn. Prune at the next
  consolidate pass; the test is the *memory with a repository home is spent* entry's own.
- **`CE-21`** — `refcheck.py` and `findings.py --check` print 384 and 62 bytes green inside every
  lint; `T-286` §3 named them. Apply L-153's one line.

**Scope**
- In: the three above. Out: any verdict, any rule.

**Inputs**
- `../docs/CONTEXT-AUDIT.md` §6.3, `../docs/lessons/L-153.md`

**Acceptance criteria**
- [ ] `check.py` on a green deck, piped, prints its one line; at a terminal, the account; red prints everything — self-test asserts all three.
- [ ] The memory index is smaller by the five entries and no fact lost its only home.
- [ ] `lint.py`'s green run, piped, is smaller than 1,976 bytes by the two tools' lines.

**Open questions**
- none

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | `check.py`: `quiet_wanted` as in the four tools | one line; 29,980 → **327** bytes piped |
| 2 | Assert the three readings the criterion names, not only the red one it already had | four assertions: terminal, pipe, and each flag winning |
| 3 | Memory index: apply the test the row **names**, per facet, before removing anything | five is **two**; three kept, and one of them is named a keeper inside the test entry |
| 4 | Move the two to `spent/`, repoint the inbound link, read the index back | 9,014 → 8,795 bytes |
| 5 | `refcheck.py`, `findings.py`: one line green when piped | `findings.py` already was; `refcheck.py` 384 → 79 |
| 6 | The tool added to the chain this same batch gets the rule now, not as a later finding | `shipped.py`, `lint.py`'s fifth step |

## 3. Implement

**Decisions & assumptions**
- **`CE-19` is one line and the band held with room.** `check.py` already had `--quiet` and a `report()` that prints everything on a red run whatever the mode; what it lacked was the default coming from `isatty`. A piped green run of the reference deck is **327 bytes** against 29,980, and against the 398 the row predicted — the row measured `--quiet` on a deck whose notes were longer — 2026-09-02
- **The self-test owes the two readings that decide a *green* run.** The red case was already asserted with a seeded failure; a default that silently stopped depending on `isatty` is exactly what nothing would notice, so a terminal, a pipe, and each flag winning are all asserted now — 2026-09-02
- **`CE-20`'s five are two, and this is the finding to read before trusting a count.** The row names the *memory with a repository home is spent* entry as its test; that test is **per facet**, and three of the five have a facet no tier-1 file holds — the publishing entry's method, fleet state and taskmd no-rewrite ruling; the PowerShell entry's `start ""` failure and its reverse, which cost four stray files in a repository root; and the trailer entry, **which the test entry names as a keeper, by id**. Absorption was verified by searching the two homes rather than from recollection, as that entry requires. 930 bytes is 219 ([L-159](../docs/lessons/L-159.md)) — 2026-09-02
- **Spent entries are moved, not deleted**, and the one inbound `[[link]]` was repointed at the document that now owns the rule rather than left dangling — both are the test entry's own instructions — 2026-09-02
- **The index header was repaired in the same pass.** It promised *the account of the seven entries moved to `spent/`* as *the last line below*, and there was no such line; the count decays every time the folder grows, and `spent/` answers both. The count is deleted and the rule stated instead — `T-236`'s rule, applied to a tier-1 file — 2026-09-02
- **`CE-21` was half done before it was raised.** `findings.py --check`'s 62 bytes **are** the one line, so nothing was owed there and nothing was changed; `refcheck.py` went 384 → 79. Said here because a row closed with *both applied* would misrepresent what the tool did — 2026-09-02
- **`shipped.py` got the rule on the day it was written.** It joined `lint.py` earlier in this same batch printing five lines green, which is how `CE-19` and `CE-21` were born. Fixing it now rather than raising it is the remediation order's §4 — 2026-09-02
- **The full gate caught what neither Low predicted, and it is the interesting half.** `figures.py`'s self-test runs the README's own pasted commands and requires their output lines to appear. It runs them through a **pipe** — so the moment `check.py` and `refcheck.py` adopted L-153, the page's two pasted accounts became ten and two absent lines, and the release gate went red on a documentation page nobody had edited. **The page is right and the instrument was reading the wrong form**: a README documents what a person at a terminal sees. `run()` now adds `--report` for exactly the tools that have the rule, and **which tools those are is read from their source** — the presence of `quiet_wanted` — so a tool adopting it tomorrow needs no edit here and one dropping it stops being asked. `refcheck.py` also had to stop treating `--report` as a mistyped command: its guard now filters the two flags and still prints the docstring for anything else — 2026-09-02

**What it bought, measured**
- `check.py`, piped, green: **29,980 → 327 bytes**.
- `lint.py`, piped, green: **2,091 → 1,737 bytes**. Against the row's 1,976 baseline the arithmetic is 1,976 − 305 for `refcheck.py` + 66 for a fifth step the row predates. **About 1,500 of what remains is taskmd's own advisory account** — upstream, and §1's *Out: any verdict, any rule*.
- The memory index: **9,014 → 8,795 bytes**, paid on every turn of every session here.

**Outputs produced**
- [`tools/deck/check.py`](../tools/deck/check.py) — `quiet_wanted`, and four self-test assertions
- [`tools/docs/refcheck.py`](../tools/docs/refcheck.py) — `quiet_wanted`, `emit`, a one-line green form, and a guard that reads the two flags as flags
- [`tools/docs/figures.py`](../tools/docs/figures.py) — `has_quiet_default`, and `run()` asking a quiet-defaulted tool for the form the README documents
- `tools/tasks/shipped.py` — the same, on the day it was added
- The agent memory index and two entries moved to `spent/` — machine-local, and it reaches no clone
- [`docs/lessons/L-159.md`](../docs/lessons/L-159.md) and the regenerated index
- [`docs/CONTEXT-AUDIT.md`](../docs/CONTEXT-AUDIT.md) — the three rows closed, with both numbers on `CE-20`'s

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| `check.py` green piped prints its one line; at a terminal the account; red prints everything — self-test asserts all three | met | 327 bytes piped. The red assertion was already there with a seeded failure; the terminal and pipe readings and both flags are asserted now |
| the memory index is smaller by the five entries and no fact lost its only home | **met, against the number rather than with it** | Two, not five. The second clause is what refuses the first: three of the five have a facet no tier-1 file holds, and one is named a keeper inside the row's own stated test. §3 and `L-159` |
| `lint.py`'s green run, piped, is smaller than 1,976 bytes by the two tools' lines | met | 1,737. `findings.py` was already one line, so the saving is `refcheck.py`'s 305, less 66 for a fifth step raised after the row was written |

**Child fix tasks raised**
- none. Two things were found here and fixed here, under the remediation order's §4: `shipped.py`'s five green lines, and `figures.py` reading a piped tool where the README documents a terminal one. Both are small and in place. What is left in the green lint is taskmd's own advisory account, and §1 puts it out of scope.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-09-02 | → proposed | Raised by `T-287`: the run's Lows, batched as the audit method asks. `PH3`. |
| 2026-09-02 | proposed → done | B19. Three Lows, and the third had its count refuted by its own stated test: `CE-20`'s **five** entries are **two** once *spent* is read per facet as the entry it cites defines it, and one of the three kept is named a keeper by id inside that entry ([L-159](../docs/lessons/L-159.md)). `CE-19` is one line and 29,980 → 327 bytes. Half of `CE-21` was already done and the row says so. **The full gate found the third thing**: a quiet default makes a README's pasted account absent, because `figures.py` reads through a pipe and the page documents a terminal — the instrument now asks for the account, and which tools it asks is read from their source. |
