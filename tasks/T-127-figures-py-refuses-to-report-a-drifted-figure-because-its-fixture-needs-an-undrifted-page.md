---
id: T-127
title: Stop figures.py refusing to report a drifted figure because its own fixture needs an undrifted page
type: fix
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-088, T-126]
work_package: PH3
owner: the project owner
business_value: medium
effort: xs
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - tools/docs/figures.py
---

# T-127 — Stop figures.py refusing to report a drifted figure because its own fixture needs an undrifted page

## 1. Specify

**Outcome**
`python tools/docs/figures.py` reports a stale figure as a stale figure. Today, when the drifted
figure is one of the three in `examples/README.md` that fixture 9 seeds against, the tool exits 1
with `SELF-TEST FAILED: … the tool itself is wrong; anything below means nothing` — a verdict about
the code, printed when the code is right and the page is what moved.

**What was seen, and where**
Found 2026-08-13 during [T-125](T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md),
where a shell change grew both shipped decks and moved four pasted figures. Measured by putting one
stale figure back and running the tool:

```
exit 1
SELF-TEST FAILED: the rounded size was re-seeded as 252 and no row reported it. That is the
state this task was raised from - a figure about a named file, inside the unanchored bucket,
wrong and unwatched. Got: [('258', 'claims 258 KB of examples/sort-window/sort-window.html,
which is 260'), ('264 284', ...
```

Fixture 9 seeds `252` over the page's **correct** size. When the page is already stale that string
is not there, nothing is seeded, no row reports it, and the fixture — written by
[T-088](T-088-a-figure-in-a-sentence-naming-no-field-goes-stale-unwatched.md) to exit loudly rather
than seed nothing — takes the tool down.

**Why it is worth fixing even though it announces itself**
The failure message carries the real drift in its `Got:` list, so the maintainer is not blind; that
is how the four figures were repaired the day this was found. What it costs is the verdict. A gate
that exits 1 saying *the tool itself is wrong* teaches the reader to distrust the message, and
`check_all.py` cannot tell this apart from a genuinely broken checker.

**This is L-78, in a second tool, found the same day as the first.** `shell.py` asserted the state
of a tracked deck and deadlocked its own `sync`
([T-126](T-126-shell-py-refuses-every-command-while-a-tracked-deck-is-behind-the-shell.md)); this
one depends on the state of a tracked page to build a fixture. Two tools, one substitution — the
repository's current contents standing in for a property of the code.

**Scope**
- In: fixture 9's setup, so a page that has drifted does not disable the tool.
- In: whatever keeps T-088's guarantee intact — the fixture must still fail loudly if the page
  stops carrying a figure of that shape, which is the thing it was built to prevent.
- Out: the refuse-on-failed-self-test behaviour (**L-04**), and every other fixture.
- Out: the volatile-block report, which is separate and already reports rather than fails.

**Inputs**
- `tools/docs/figures.py` — fixture 9 and the seeding helper.
- [T-088](T-088-a-figure-in-a-sentence-naming-no-field-goes-stale-unwatched.md) §4 — why the
  fixture seeds the page's real wording, and why it exits loudly.
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-78**, the rule this instance belongs to.

**Acceptance criteria**
- [ ] With a figure in `examples/README.md` deliberately stale, the tool reports it as stale and the
      self-test passes
- [ ] The fixture still fails if the page stops carrying a figure of the shape it seeds
- [ ] Seeding is shown to fail on a broken detector, not just to pass on a working one (**L-04**)

**Open questions**
- **Seed against the page's stated value rather than its computed one, or seed into a copy the
  fixture writes itself?** The second is what T-126 chose for `shell.py` and is the more general
  answer; the first is one line and keeps the fixture bound to the real page, which is what T-088
  wanted. Whoever takes this decides it from the fixture's own reason.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 |  |  |
| 2 |  |  |

## 3. Implement

**Decisions & assumptions**
- <decision — rationale — date>

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised, not taken. It did not block — the failure message names the drifted figures, so the four were repaired from it — and the fix turns on a question T-088 already answered once, which makes it the owner's to re-open rather than mine to settle inside another task (**L-37**). |
