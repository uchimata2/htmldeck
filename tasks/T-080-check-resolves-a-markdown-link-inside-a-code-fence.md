---
id: T-080
title: taskmd check resolves a markdown link inside a code fence, so pasted output cannot be quoted
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-063, T-073, T-079]
work_package: PH2
shipped_in: 0.2.2
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-10
updated: 2026-08-12
deliverables:
  - tools/docs/refcheck.py
---

# T-080 — taskmd check resolves a markdown link inside a code fence, so pasted output cannot be quoted

## 1. Specify

**Outcome**
A task file can paste the output of `taskmd index` without the check treating the pasted row's
link as one of its own. As with [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md)
the change is upstream's, so the outcome here is a decided behaviour and a proposal carrying it,
delivered the same way.

**Why this one**
**This project states results as what was actually produced**, so pasted tool output is everywhere
in the task record — and `taskmd index` emits markdown links by construction, one per row. Quoting a
board row therefore puts a bracketed id followed by a parenthesised filename inside a fence, and
`check` resolves it as a live link.

**What it cost, 2026-08-10.** Drafting T-079's proposal, a row was pasted as evidence with the
filename abridged to an ellipsis. The run went red:

```
BROKEN LINK   tasks/T-079-the-boards-dependency-columns-list-closed-tasks.md -> …

1 problem(s) over 78 task(s)
```

The fix was to paste a *resolvable* link instead. **That is the part worth fixing: the checker did
not find a defect, it edited the evidence.** A quotation that has to be adjusted to satisfy a link
checker is no longer a quotation, and the adjustment is invisible to whoever reads it later.

**Why this is not the same ask as `refcheck`'s.** [`refcheck.py`](../tools/docs/refcheck.py)
deliberately reads inside fences — *every repo-relative `.md` path written in prose or printed by a
tool* — and that has caught real defects, so **blanket fence-skipping is the wrong proposal** and
this project would not want it. The narrow claim is about **link syntax**: a bracketed label with a
parenthesised target renders, inside a fence or a code span, as literal characters — nobody can
follow it and it cannot be broken. A bare path in a fence is a different thing and may stay checked.

**Scope**
- In: markdown-link syntax inside fenced code blocks, in `check`'s link resolution.
- In: **inline code spans, which behave the same** — measured, not assumed. Writing this task
  reproduced the defect three more times in one run, every one of them a link-shaped example wrapped
  in backticks in prose. **A task describing the defect could not be written without committing it**,
  which is the strongest statement of it available and is why the examples above are now paraphrased
  rather than shown.
- In: the proposal, delivered as a task in taskmd's tracker the way T-079's was — same maintainer,
  and the two pair naturally.
- Out: bare paths inside fences, and any change to `refcheck.py`, which wants them.

**Inputs**
- [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md) §3 — the fence that triggered it
  and the channel the proposal goes through.
- [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md) — the five earlier proposals, and the
  house format for one.

**Acceptance criteria**
- [ ] The behaviour is decided and written down, including that inline spans were left alone and why.
- [ ] The proposal is delivered upstream and named here.
- [ ] A task file in this repository can quote a `taskmd index` row verbatim, abridged filename and
      all, and `python tools/tasks/lint.py` stays green.
- [ ] If upstream declines, the workaround is written down where a task author will meet it —
      `TASK-WORKFLOW.md`, not this file.

**Open questions**
- none.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Reproduce against the current source, and check whether inline spans behave the same | this file §1, **done 2026-08-10** |
| 2 | Write the proposal | taskmd's own **T-112**, **done 2026-08-10** |
| 3 | Deliver it as a task in taskmd's tracker | **done 2026-08-10** |
| 4 | Make the same change in `refcheck.py`, holding the boundary §3 measured | `tools/docs/refcheck.py`, **done 2026-08-12** |
| 5 | Write the rule where a task author meets it | `TASK-WORKFLOW.md` §6.1, **done 2026-08-12** |

## 3. Implement

**Decisions & assumptions**
- **Argue it from taskmd's own T-092, not from this project's practice** — 2026-08-10. T-092 decided
  that a bare path in prose is not a reference, separating a pointer from *a path merely being
  discussed*, and its acceptance criteria demanded that a false-positive boundary be **proven rather
  than asserted**. Link syntax inside a fence is that same boundary one syntax over, so the ask is
  consistency with a decision they have already taken rather than a new rule from an adopter. The
  mechanism confirms it was never decided: `LINK.finditer` runs over the whole file text with no
  notion of a fence.
- **Do not ask for blanket fence-skipping** — 2026-08-10, as scoped. Bare paths inside fences stay
  checked upstream and here: `refcheck.py` reads them deliberately and has caught real defects, so
  the two tools disagree about paths on purpose and only agree about link syntax.

- **Inline code spans were brought in, not left alone** — 2026-08-10, and §1's acceptance criterion
  still asks for the opposite because it was written before the measurement. Writing this task
  reproduced the defect three more times in one run, every one a link-shaped example wrapped in
  backticks in prose. A span and a fence are code for the same reason, so a rule that separated them
  would need a second justification and has none.
- **The rule goes in `TASK-WORKFLOW.md` §6.1 whether or not upstream declined** — 2026-08-12. §1's
  last criterion made that conditional on a refusal, which was the wrong trigger: the fact a task
  author needs is *what may be quoted*, and it is now the same sentence for both checkers. It sits
  beside the `§`-in-code paragraph it generalises.

**Outputs produced**
- The proposal, delivered as **T-112**, *Stop check resolving a link that is displayed rather than
  navigable*, in taskmd's own tracker — same channel as T-079's, left for the maintainer to index.
  Named by id and title rather than by path, since the file is in another repository.
- [`../tools/docs/refcheck.py`](../tools/docs/refcheck.py) — `links_in` and `pointers_in`, the two
  call sites they replace, and four self-test assertions.
- [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md) §6.1 — two paragraphs: what may now be quoted, and the bare
  path that is still checked.

**Upstream is finished, measured against the installed 0.4.0 rather than read off a release note.**
Their T-112 is `done` and its own review records fixtures for the fence, the span, a live link either
side of the fence, and a document quoting a whole `index` run. Reproduced here, one fixture per row,
each written into this file and taken out again:

```
taskmd skill: 0.4.0
  no fixture                 exit 0  0 broken link(s)   <- baseline
  inside a fence             exit 0  0 broken link(s)   <- NOT reported
  inside an inline span      exit 0  0 broken link(s)   <- NOT reported
  a real link, outside both  exit 1  1 broken link(s)   <- reported
```

**The target is `T-041-no-such-file-anywhere.md` and not the abridged form this task first used.**
Their T-112 records that a target ending in `...` **resolves on Windows**, so a fixture built that
way passes before the fix and proves nothing — which is what the first attempt at this measurement
did on 2026-08-11.

**What is left is `refcheck.py`, and it is the same two holes plus one behaviour that must survive.**
The identical four fixtures:

```
  link syntax in a fence     exit 1  REPORTED     <- the defect
  link syntax in a span      exit 1  REPORTED     <- the defect
  a BARE path in a fence     exit 1  REPORTED     <- CORRECT, and §1 says keep it
  a real link, outside both  exit 1  REPORTED     <- CORRECT
```

So the change is narrow and its boundary is already measured: stop resolving **link syntax** inside a
fence or a span, and leave everything else exactly as it is. §1's *Out: bare paths inside fences* is
the third row, and it stays out.

**The demonstration, and it is this file.** A real `taskmd index` row, pasted verbatim except for the
filename, which is abridged the way a quotation abridges:

```
| [T-041](T-041-implement-the-nine-glitch-free-…md) | Implement the nine glitch-free conditions R6 defined and nothing adopted | `PH3` | `proposed` | `specify` | - | - | T-005, T-016, T-019, T-042, T-097 |
```

Before the change, that block alone turned the run red — the checker did not find a defect, it
required the evidence to be edited:

```
FAIL - 1 problem(s):

  BROKEN LINK  tasks\T-080-check-resolves-a-markdown-link-inside-a-code-fence.md -> T-041-implement-the-nine-glitch-free-…md
```

After it, the same block is quoted and the chain is green. **The row above is the acceptance
criterion, kept rather than described.**

**The change is one call site each, and two functions that say which is which.** `links_in` runs
check 1 over `strip_code(text)` — the same helper the section scan already used, so nothing new
decides what code is. `pointers_in` runs check 2 over `strip_front_matter(text)` and **not** over
`strip_code`, which is where the two deliberately disagree. Both are named so the self-test can
assert the path `cmd_check` actually takes; asserting `LINK` and `POINTER` directly would have
tested two patterns that merely happen to be used the right way today.

**The self-test is load-bearing, and that was measured rather than trusted.** Four new assertions,
one per row of the table above. Two mutations against them:

```
MUTATION 1 caught: SELF-TEST FAILED: link syntax inside a fence was resolved - it renders as the characters t
MUTATION 2 caught: SELF-TEST FAILED: a bare path printed into a fence was skipped - that is a tool's own outp
```

Mutation 1 reverts the fix; mutation 2 applies it to check 2 as well, which is the over-correction
§1 scoped out. Neither survives.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| The behaviour is decided and written down, including that inline spans were left alone and why | met, **the other way** | Spans were **not** left alone — they were brought in, on a measurement §1's Scope already records and this criterion predates. The criterion is met by the decision going the opposite way, written up in §3. Left as first drafted rather than corrected in place: a criterion edited to match the outcome cannot fail. |
| The proposal is delivered upstream and named here | met | taskmd's **T-112**, `done`, shipped in their 0.4.0 and still correct on 0.5.0 — the fixture in §3 is a real index row and `taskmd check` passed 98 tasks over it today. |
| A task file can quote a `taskmd index` row verbatim, abridged filename and all, and `lint.py` stays green | met | §3 holds the row. Red before the change, green after; both runs pasted there. |
| If upstream declines, the workaround is written down in `TASK-WORKFLOW.md` | met, **unconditionally** | Upstream accepted, so the condition never fired. The rule went in anyway — §3 says why the trigger was wrong. |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-12 | → done | **Closed on this project's own half.** `refcheck.py` stops resolving link syntax inside a fence or a span and keeps resolving a bare path in either, which is the boundary the four fixtures had already drawn — so the implementation decided nothing the measurement had not. The change is two named functions and one call site each; the reason they are named is that the self-test then asserts what `cmd_check` runs rather than two regexes that happen to be used the right way. **Both mutations of that self-test were caught** (§3), including the over-correction of stripping code from check 2, which is the one way this fix could have taken a real check with it. Verified against **taskmd 0.5.0**, installed the same day: the fixture in §3 is a live index row and `check` passed 98 tasks over it. The generic half went to `TASK-WORKFLOW.md` §6.1 beside the `§`-in-code paragraph it generalises, and it went there unconditionally — §1 had made that conditional on upstream declining, which was the wrong trigger for a fact about what may be quoted. Generalised as **L-70**: a checker that forces a quotation to be edited has stopped checking and started writing. |
| 2026-08-11 | (implement) | **Upstream is done and the remaining work is measured, not guessed.** Four fixtures against taskmd 0.4.0 and the same four against `refcheck.py`, printed in §3: taskmd resolves neither a fenced link nor a spanned one and still catches a live broken link; `refcheck.py` reports all four, and the one it is **right** to report is the bare path. So the change is *stop resolving link syntax inside a fence or a span*, and nothing else — the boundary §1 argued for, now with both sides of it observed. The first attempt at this measurement used an abridged target ending in an ellipsis, which their T-112 records as **resolving on Windows**: a fixture that passes before the fix. |
| 2026-08-11 | (implement) | **Upstream shipped it in 0.4.0, and the same defect is now this project's own.** The release note does not mention T-112, so it was tested rather than read: a real `taskmd index` row with an abridged filename, pasted into a fence in this file, and `taskmd check` passed 94 tasks over it. **`refcheck.py` failed the same line** — `BROKEN LINK ... -> T-041-implement-the-nine-glitch-free-…md`. §1 scoped `refcheck.py` out on the ground that it *wants* paths inside fences, which is true of **bare paths** and not of link syntax; §1's own narrow claim draws exactly that line. So the fixture is reverted for now and the task stays open on a deliverable that moved from upstream's tool to this one. Not folded into the release being cut the same hour: a patch shipping three adopter-facing fixes should not also carry a checker change discovered mid-sequence. |
| 2026-08-10 | (implement) | **Not fixed in 0.3.0, measured rather than assumed.** [T-081](T-081-the-installed-taskmd-is-two-minor-versions-behind.md) installed the current release and reproduced this against it: a fenced block in a task file carrying link syntax with an abridged target turns the run red, as before. Upstream's T-112 is still `proposed` — **their T-111, this task's sibling, is `done` and shipped in the same release**, so the pair has separated and only one is outstanding. Nothing to do here; the workaround stands. |
| 2026-08-10 | (implement) | **Received upstream**, with T-111 — taskmd informed, reindexed, project updated. Their decision is not known here and is not assumed. Until it lands, the workaround stands and is written where a task author meets it: paraphrase link syntax, or paste a target that really resolves. |
| 2026-08-10 | → in_progress | **Delivered as taskmd's T-112**, the same channel as T-079. Reading their source first moved the argument onto their own T-092, which had already separated a pointer from a path being discussed and had asked for false-positive boundaries to be proven — so this is a gap in enforcement of a settled rule, not a request for a new one. Their repository is green on this today only because no task there quotes an index row; the defect belongs to whoever pastes the tool's own output, which is this project's method. One consequence found while writing: `links += 1` runs on every match, so the count their T-095 added to the summary is inflated by strings nobody can follow. Open on their side; nothing outstanding here. |
| 2026-08-10 | → proposed | Raised on the owner's word after the defect turned a run red while T-079's own proposal was being drafted. `medium` because this project pastes tool output as a matter of method and `index` output carries a link per row, so it recurs rather than being one bad afternoon; `xs` because the change is upstream's and the ask is narrow. Kept out of T-079 deliberately: that task is scoped to `index`, and one task carrying two unrelated upstream defects is harder to close than two carrying one each. |
| 2026-08-13 | (no change) | **Shipped in `0.2.2`.** `shipped_in` read `unreleased` until this sweep: the closing commit `9bc2bbf` is contained in `v0.2.2`, which is what the field holds (TASK-WORKFLOW.md §3). Found by reconciling the board after the `0.2.3` release rather than by a check - nothing validates the field against the tags. |
