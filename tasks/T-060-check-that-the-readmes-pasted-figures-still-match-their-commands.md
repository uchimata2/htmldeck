---
id: T-060
title: Check that the README's pasted figures still match the commands that produced them
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-050, T-056, T-067]
work_package: PH2
shipped_in: 0.1.4
owner: the project owner
business_value: high
effort: m
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - tools/docs/figures.py
---

# T-060 — Check that the README's pasted figures still match the commands that produced them

## 1. Specify

**Outcome**
A check that runs each command `README.md` prints and compares its output to the block underneath it,
so a figure that has gone stale is a red run rather than something a reader finds. **The figures are
correct as of 2026-08-09** — [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md)
re-derived all of them. What does not exist is anything that keeps them that way.

**Why this one**
Raised by T-056, which found **six figures already wrong** before it edited anything: build mode and
critique mode grew the ruleset on 2026-08-09, and nothing re-derived the README afterwards. 161 rule
rows were 163, 115 hard rules were 117, 24 judge rules were 25. The README had also started
**contradicting itself** — its prose said the judgement half is 25 rules while a fenced block three
sections above printed 24. Every gate stayed green throughout and was right to: no gate owns a number
printed in prose in a document that is not a deck (**L-52**).

The obligation to re-derive now exists in [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §6, in
writing and unchecked. This repository's own position is that a rule with nothing behind it is a
claim, so the state this task ends is the one `check.py`'s account exists to make impossible
elsewhere.

**One figure is structurally unstable and needs a decision, not just a check.** The block from
`python tools/docs/refcheck.py` counts **every document pointer in the repository**, so it moves
whenever any document is edited — including edits to the README itself. It went 968 → 980 → 992 → 995
within T-056's single session. A check comparing it byte-for-byte would fail on almost every
documentation commit, which is a check nobody keeps.

*The command named here was `tools/tasks/task.py check` until 2026-08-10; that tool was retired by
[T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) and the figure now
comes from `refcheck.py`. The instability is unchanged — it was never a property of the tool.*

**Measured on the live document, 2026-08-10.** The two `ruleset.py` blocks still match their commands
exactly; the `refcheck.py` block does not, and all three of its numbers have moved — 1035 → 1041,
493 → 496, 1191 → 1196. **That is the whole task in one observation**: the figures that describe a
*decision* stay put for months, and the figures that count the *repository* are stale within a day.
They are two kinds of number and a single rule cannot hold both.

**Scope**
- In: a check that maps each fenced block in `README.md` to the command that produces it, runs it, and
  compares.
- In: a decision on the pointer-count block above — the candidates are dropping the volatile line from
  the pasted excerpt, comparing only its stable prefix, or regenerating the block in place rather than
  asserting it.
- In: the same treatment for figures stated in **prose**, which is where two of the six stale ones were
  and where the self-contradiction lived.
- Out: `examples/README.md` and the other document READMEs, unless the same mechanism reaches them for
  free.
- Out: deck figures, which are DS-102's and already gated.
- Out: re-deriving today's figures, which T-056 did.

**Inputs**
- [`../docs/PUBLISHING.md`](../docs/PUBLISHING.md) §6 — the obligation this would enforce, and the
  list of commands behind the blocks.
- [`../docs/LESSONS.md`](../docs/LESSONS.md) **L-52**, the finding; **L-03** on why the figures are
  pasted at all; **L-05** on what a check that cannot fail is worth.
- [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) §3, which lists all six stale
  figures with the command that re-derives each.

**Acceptance criteria**
- [ ] Every fenced block in `README.md` is either bound to a command and compared, or **listed as
      unbound with a reason** — the same partition `check.py` already requires of itself
- [ ] The check fails when a figure is stale, demonstrated against a deliberately staled copy rather
      than asserted
- [ ] The pointer-count block no longer produces a false failure on an unrelated documentation edit,
      **and its drift is still reported** — a figure nobody can be told has moved is a figure that
      rots quietly, which is the state this task exists to end
- [ ] Figures stated in prose are covered, or excluded in writing with what would close the exclusion
- [ ] The blocks are **excerpts** and are compared as such: `ruleset.py --counts` prints far more
      than the three lines the README pastes, so a whole-output equality test would fail on every
      block and prove nothing

**Open questions**
- **Settled 2026-08-10 — its own tool, `tools/docs/figures.py`, because it removes a manual step
  rather than adding a command.** [`PUBLISHING.md`](../docs/PUBLISHING.md) §6 already instructs a
  human to run five commands and *"diff each against its command"* by eye. That instruction is the
  thing being replaced, so the count of commands a person runs does not go up. It sits beside
  `refcheck.py` in `tools/docs/` because both check documents rather than decks; putting it in
  `check_scaffold.py` would make the package checker read prose, and `taskmd check` belongs to
  another project entirely.
- **Settled 2026-08-10 — a figure is either `compared` or `volatile`, and volatile has to be
  declared in writing with what makes it volatile.** Compared figures fail the run on any drift;
  volatile figures are **reported with their old and new values and do not fail it**. This is
  [T-067](T-067-the-published-upgrade-instructions-do-not-upgrade.md) §4's third candidate — *a figure that
  does not count its own source* — reached from the other side: rather than trying to make the
  number stable, the check states which numbers are not. It takes neither of the other two.
  A **tolerance** would be a band with no rule behind it, which this repository rejects everywhere
  else (**L-38**). **Release-time-only re-derivation** is what `PUBLISHING.md` §6 already is, in
  writing and unchecked — the exact state that let six figures go stale, so repeating it in code
  would answer nothing.

  The split is not a convenience. Every one of T-056's six stale figures was a **ruleset count** —
  163, 117, 25 — and every one of those is `compared`, so all six would have been red the afternoon
  they broke. Nothing is weakened by excusing the three numbers that count the repository.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Bind blocks to commands by the document's own shape — an unlabelled fence immediately after a ```bash fence is that command's output — and enumerate every fence, so an unbound one is a named gap rather than a silence. | The binding pass in `tools/docs/figures.py`, and a printed partition over every fence in `README.md` |
| 2 | Compare each bound block as an **excerpt**: run the command once, and require every pasted line to appear in its output, in order. Whole-output equality is wrong here and would fail on all five. | The comparison pass, and a `compared` verdict per bound block |
| 3 | Add the `volatile` declaration — a span the run reports as drifted instead of failing on — keyed to the block and carrying its written reason. Report old → new so the release pass has the values to paste. | The declaration table and its report line |
| 4 | Extend the partition to **prose figures**: extract every numeral and spelled-out number from the README's prose, and require each to be matched against a bound command's output or declared with a reason. Derived from the document, never from a hand-kept list of what to look for (**L-54**). | The prose pass, and a declaration entry per excluded figure |
| 5 | Self-test on staled copies — one per failure mode: a changed compared figure, a changed volatile figure, a new undeclared fence, a new undeclared prose number. | Four fixtures in `self_test()` |
| 6 | Run it against the live README, fix whatever it legitimately finds, and rewrite `PUBLISHING.md` §6 to name the command instead of instructing a human to diff by eye. | A green run, the corrected README, and §6 pointing at the tool |

**Shape of the deliverable, decided**

**The tool runs the commands rather than reading recorded outputs.** A fixture holding a copy of what
`ruleset.py` printed last time is a second copy of the fact, and it goes stale in the direction that
produces false confidence (**L-13**, **L-52**).

*Rejected: parsing the README for figures and checking them against the ruleset document directly.*
It skips the subprocess and is much faster. It also checks something different from what the README
claims — the README says *this is what this command prints*, and a reader who runs the command is
comparing against the command, not against the document the command reads.

**Output paths**
- `tools/docs/figures.py`

## 3. Implement

**Decisions & assumptions**
- **The runnable set is an allowlist, not a convenience.** The page also prints `git clone`,
  `/plugin install` and `claude plugin update`. A tool that executed whatever a document told it to
  would run those the first time somebody edited the README, so only `python tools/…` is executed
  and everything else is a declared exclusion.
- **Command outputs are cached for the process.** Not an optimisation: `check.py` drives real
  headless Chrome, and the self-test audits the document six times over. Uncached, the first
  complete run **timed out at two minutes without reporting anything** — a check nobody waits for
  (**L-40**). Cached, the whole thing is 20 s.
- **Three of eight prose figures were passing against a coincidence, and it took looking at what
  they matched to see it.** `163` was matching `DS-163`, `113` matched `DS-113`, `221` matched
  `DS-221` — rule IDs, not the figures. The verdict said `compared` and was false. The boundary now
  rejects a preceding letter or hyphen, all eight bind to the right line, and **fixture 5 fails on
  a numeral matched only by a rule ID**. A check that compares a coincidence is worse than one that
  says nothing (**L-36**, **L-44**).
- **A dead fixture, caught by the lesson written an hour earlier.** The volatile-block fixture
  hardcoded `1041` while the README said `1035`, so its `replace` matched nothing, staled nothing
  and passed. Both fixtures now **derive** their target line from the document and exit if they
  cannot find one (**L-54**, **L-55**).
- **Prose coverage is numerals only**, and the spelled-out numbers are excluded in writing rather
  than by silence. Of the 60 numbers in the README's prose, 50 are words like *"one project"* and
  *"two days"*; requiring a declaration for each would be 60 entries of noise and a check nobody
  keeps. **Every one of T-056's stale prose figures was a numeral.** What would close the exclusion:
  a spelled-out figure going stale, which has not happened yet.
- **The drifted volatile block is left as it is.** Re-pasting it now would be stale by the commit
  that pastes it — the count moved 1041 → 1043 → 1044 during this task alone, from this task's own
  edits. That is the treadmill [T-067](T-067-the-published-upgrade-instructions-do-not-upgrade.md)
  §4 identified, and declining to run on it is the decision, not an omission.

**Outputs produced**
- [`tools/docs/figures.py`](../tools/docs/figures.py) — the check, with five fixtures.
- [`docs/PUBLISHING.md`](../docs/PUBLISHING.md) §6 — rewritten to name the command instead of
  telling a person to diff five outputs by eye.

**Checked by being used.** On the live document, 17 fences and 9 prose numerals, partitioned:

```
  fenced blocks          prose numerals
    command        5       compared       8
    compared       4       excluded       1
    volatile       1       total          9
    excluded       7
    total         17   = every fence, so the account is a partition

0 stale figure(s) - 1 volatile block(s) drifted, which is reported rather than failed
```

**Six defects were put back, one at a time**, and each produced its own diagnosis (**L-55**: the
exit status is the same for all of them, so only the message distinguishes them):

```
comparison always succeeds        SELF-TEST FAILED: a compared figure was moved ('owned by a gate 113') and the run stayed green
the volatile split removed        SELF-TEST FAILED: the live README does not pass its own check - line 150 ...
drift computed but not reported   SELF-TEST FAILED: a moved pointer count was neither failed nor reported ...
undeclared fence treated as excluded  SELF-TEST FAILED: a fenced block bound to nothing passed ...
undeclared prose numeral accepted     SELF-TEST FAILED: a prose numeral no command prints was accepted
the word boundary loosened        SELF-TEST FAILED: a prose numeral matched only by a rule ID (DS-107) was reported as compared
```

**The second one is the empirical case for the split.** Remove the volatile declaration and the
**live README fails today** — not hypothetically, on this commit. That is the check nobody would
have kept.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every fence is bound and compared, or listed as unbound with a reason | **met** | 17 fences: 5 command, 4 compared, 1 volatile, 7 excluded, 0 undeclared, and the total is printed as a partition. An undeclared fence fails the run — fixture 3 |
| The check fails on a stale figure, demonstrated against a staled copy rather than asserted | **met** | Six defects put back one at a time, each with its own message. The compared-figure fixture derives its target from the document, so it cannot go stale the way the first draft's did |
| The pointer-count block no longer produces a false failure, and its drift is still reported | **met** | Declared `volatile`; the live run reports `1035 → 1044` and exits 0. Fixture 2 fails if it ever fails the run, fixture C if the drift stops being reported |
| Figures stated in prose are covered, or excluded in writing with what would close the exclusion | **met** | 8 of 9 numerals bound to a command's output, 1 excluded with what would close it. Spelled-out numbers are excluded as a class, in writing, with the closing condition stated |
| The blocks are compared as excerpts | **met** | `ruleset.py --counts` prints ~20 lines against the README's 3. Every pasted line must appear in the run, in order; whole-output equality would have failed all five |

**Two things this leaves undone, stated rather than buried.**

**A prose numeral is bound to the corpus, not to a field.** `25` is confirmed to appear as
`gated by judgement (judge) 25` — but the check only knows the number occurs somewhere in the union
of the bound commands' output. If the README said *"the judgement half is 81 rules"*, `81` appears
in `checked 81` and the run would stay green. It catches a figure that has gone stale, which is the
defect class T-056 found; it would not catch a figure moved to the wrong sentence. Closing that
needs a field-level binding, and that is a task, not a tweak.

**Nothing here checks the sentence around the figure.** The README's *"all three are fixed"* went
false with every figure on the page correct
([T-067](T-067-the-published-upgrade-instructions-do-not-upgrade.md) review). The tool prints that
limitation on every run rather than leaving a reader to infer coverage it does not have (**L-05**).

**Child fix tasks raised**
- **[T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md)** — bind a prose figure
  to the field that produces it, so a correct number in the wrong sentence fails. Carries the first
  gap above.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-10 | → done | Specify, plan, implement and review in one pass. `tools/docs/figures.py` partitions all 17 fences and 9 prose numerals; `PUBLISHING.md` §6 now names the command instead of asking a person to diff five outputs by eye. All five criteria met. **Three prose figures were passing against rule IDs** (`163` vs `DS-163`, `113` vs `DS-113`, `221` vs `DS-221`) and one fixture was dead because it quoted a figure instead of deriving it — both found by looking at what the check matched rather than at whether it was green (**L-55**). The residual numeral-to-corpus binding is carried by [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md). |
| 2026-08-09 | → proposed | Raised by [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md), which re-derived the README's figures and found **six already stale** and one place where the document contradicted itself. **PH2, not PH1:** the figures are correct today, so a first release is not blocked by the absence of a check that keeps them correct — holding publication for it would be exactly the failure the release split exists to prevent. Carries one finding that shapes the work before it starts: the `task.py check` block counts every pointer in the repository and therefore moves on almost every documentation commit, so a naive byte-comparison would fail constantly and be turned off within a week. |
