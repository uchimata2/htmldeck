---
id: T-127
title: Stop figures.py refusing to report a drifted figure because its own fixture needs an undrifted page
type: fix
status: done
phase: review
shipped_in: unreleased
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
- ~~**Seed against the page's stated value rather than its computed one, or seed into a copy the
  fixture writes itself?**~~ **Decided 2026-08-13 from the fixture's own reason: against the page's
  stated value, located by the sentence's *shape*.** T-088 built this fixture to prove that *this
  page's way of stating a property binds* — a claim about the wording, not about the number. So the
  fixture needs a sentence of that shape and does not need it to be right, and the seed is found by
  matching the shape and moving whatever number is there. **It is the pattern fixtures 1 and 2 in
  the same file already use** — *the line is found, its first number is moved, and the fixture
  refuses to run if it could not find one* — so this is bringing one fixture into line with its
  neighbours rather than inventing a rule. A copy the fixture writes itself, T-126's answer, is the
  more general fix and is wrong here: the thing under test is a real page's phrasing, and a fixture
  that writes its own page would test a phrasing nobody publishes.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Find both claim shapes by regex — `**N KB in one file**, N bytes` and `N hand-written SVG figures` — and refuse loudly if either shape has left the page | the seed, derived |
| 2 | Seed **every** claim of those shapes one at a time, not the two the deck happens to own, and require a `STALE` row naming each moved value | the fixture |
| 3 | Prove it on a drifted page: put a stale figure back and require the tool to *report* it and the self-test to pass | the evidence |
| 4 | Prove the seeding fails on a broken detector, not only that it passes on a working one (**L-04**) | the evidence |

## 3. Implement

**Decisions & assumptions**
- 2026-08-13 — **the seed is found by shape and taken from the page, not from `artifact_facts()`.**
  Decided from the fixture's own reason: T-088 built it to prove *this page's wording binds*, which
  is a claim about phrasing and not about the number being right.
- 2026-08-13 — **it seeds every claim of either shape the page binds, not the two the deck owns.**
  Naming the deck's own figures was the coupling; matching the shape costs nothing.
- 2026-08-13 — **it seeds only claims the page actually binds**, and reports rather than asserts the
  ones it does not. A claim of the right shape bound to nothing is a real defect — it is
  [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) —
  but asserting it here would put the tool straight back where this task found it: down, blaming
  itself, for something the page did.

**Two defects underneath the first, both found by measuring rather than by reading**

1. **`compared` is not the test for *bound*.** The first rebuild collected the bound values from
   `compared` rows only. A figure that has drifted reports as `STALE`, so it dropped out of its own
   shape on exactly the day it went wrong, and the fixture then refused for want of a shape the page
   still carried. That is this task's own defect one level further in. The filter is now
   `compared` **or** `STALE`: binding is the question, correctness is not.
2. **A fixed delta is not a wrong value.** The seeded page said `252`, the seed added 8, and 260 is
   the right answer — so nothing reported it and the fixture failed on a figure it had accidentally
   corrected. The seed is now chosen against the set of values the accounts print, and the fixture
   refuses if no candidate is genuinely wrong.

Neither was visible in the code. Both appeared the first time a real drift was put on the page,
which is plan step 3 and the reason it is a step rather than a check at the end.

**Outputs produced**
- `tools/docs/figures.py`, fixture 9 rebuilt: two shape regexes, a seed derived from the page, a
  seed proven wrong before it is asserted, and a loud refusal if either shape stops being bound.

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| With a figure in `examples/README.md` deliberately stale, the tool reports it as stale and the self-test passes | met | Seeded `**252 KB in one file**, 257 235 bytes`. The run prints two `STALE` rows naming the drift and exits 1 **as a gate failure about the page** — `SELF-TEST FAILED: … the tool itself is wrong` is gone |
| The fixture still fails if the page stops carrying a figure of the shape it seeds | met | The guard fired for real during the work, naming the bound values it could see: `Bound values found: ['12', 'six']` |
| Seeding is shown to fail on a broken detector, not just to pass on a working one (**L-04**) | met | The artifact comparison was changed to emit `compared` where it emits `STALE`; the fixture caught it and exited. Restored, and the run is green |

**Child fix tasks raised**
- [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) —
  the reference deck's figures on `examples/README.md` are bound to nothing and two are wrong on the
  published page. Found by this task's rebuilt fixture refusing on a claim the page does not bind.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | (no change) | **The fix was silently thrown away between the proof and the commit, and the run afterwards looked like confirmation.** Undoing the deliberate break with `git checkout -- tools/docs/figures.py` restored the file from the index, discarding the whole uncommitted rebuild with it; the confirming run printed `0 stale figure(s)` and exited 0, which the *original* fixture also does on a clean page. Caught by `git status` showing the file unmodified while staging. Reapplied, and both proofs re-run with the break reversed by writing the saved text back and asserting the bytes match. **L-80.** |
| 2026-08-13 | → specified, → planned, → done | Fixture 9 now finds its seed by the sentence's **shape** and takes the number from the page, so a drifted page is reported rather than blamed on the tool. Two further defects appeared underneath it, both only once a real drift was on the page: `compared` was used as the test for *bound*, which drops a figure out of its own shape the day it goes wrong; and a fixed delta landed the seed on the correct value. Proven in both directions — a drifted page reports `STALE`, and a detector broken on purpose is caught. **It also found a live one**: the reference deck's figures on `examples/README.md` are bound to nothing and understate the shipped deck by 12 KB, raised as [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) rather than fixed here. |
| 2026-08-13 | → proposed | Raised, not taken. It did not block — the failure message names the drifted figures, so the four were repaired from it — and the fix turns on a question T-088 already answered once, which makes it the owner's to re-open rather than mine to settle inside another task (**L-37**). |
