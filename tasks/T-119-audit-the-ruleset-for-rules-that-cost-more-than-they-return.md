---
id: T-119
title: Audit the ruleset for rules that cost more to satisfy than they return
type: audit
status: proposed
phase: specify
parent: null
blocked_by: []
related: [T-054, T-113, T-114, T-115]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-13
updated: 2026-08-13
deliverables:
  - docs/DESIGN-SYSTEM.md
  - docs/DESIGN-RATIONALE.md
---

# T-119 — Audit the ruleset for rules that cost more to satisfy than they return

## 1. Specify

**Outcome**
Every rule in [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) has been tested against one question —
**does satisfying this make a deck better, or only different?** — and the ones that fail are deleted,
merged or narrowed, with the reason recorded. 165 rules, and the count is not the point: an
unexamined rule is a cost paid on every deck forever.

**The concern is real, and there are three kinds of evidence for it already**

**1. Dead legislation — a rule governing something that does not exist.** **DS-146** and **DS-147**
both regulate chart behaviour: *charts draw in once, never re-animate on back-navigation*, *count-up
on headline statistics, one emphasis pulse*. There is no chart component:

```
grep -c -i "chart" shell/components.css   →  0
```

Two rules, fully argued, with no possible subject. They cost nothing to satisfy and something to
read, and they made [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md)'s
question unanswerable as asked.

**2. Over-broad scope — a rule that reaches past its own reason.** **DS-138** requires a popover to
drop *below* its control. Its reason is stated and good: tier-two content a reader is reading must
fit on the stage. Its **scope** is any popover at all, so on 2026-08-12 it blocked a two-item chrome
control menu — not tier two, not content, not read — and
[T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) now has to argue an exemption
into the rule before it can write a line of code. **The rule is right and its scope is wrong**, which
is the expensive combination: it does not look like a defect, so it gets obeyed.

**3. Rules never exercised on any deck.** `check.py` partitions its jurisdiction and reports
**27 excused here** against 84 checked. A rule excused on every deck this project has ever built has
never changed anything, and there is no evidence either way about whether it should exist.

**What the audit is not**
**Not a campaign to make decks easier to build.** A rule that is expensive *and* earns it stays —
DS-001, DS-106 and the disclosure rules are all costly and all load-bearing. The test is not cost, it
is **cost against observed return**.

**The three-part test each rule faces**

1. **Subject.** Does anything in a real deck fall under it? A rule with no possible subject is dead.
2. **Effect.** Has it ever changed a deck — caught something, or shaped a build? A rule that has never
   fired is unverified, not proven.
3. **Scope fit.** Does its wording reach exactly as far as its reason? A rule whose scope exceeds its
   rationale is narrowed to the rationale, not deleted.

A rule failing **1** is deleted. Failing **2** is either given an instrument or demoted to
`guidance`. Failing **3** is narrowed. Passing all three is left alone and **said to have been
examined**, which is most of the value — an audited ruleset is one a later reader can trust.

**Scope**
- In: all 165 rules, each with a verdict and a one-line reason.
- In: the three named candidates above, decided rather than listed.
- In: **the deletions, merges and narrowings themselves**, with
  [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) recording what was removed and why — a rule
  deleted without a record is one that gets re-invented.
- In: whether the count itself is a problem. 165 rules is a lot to hold, and merging near-duplicates
  may be worth more than deleting weak ones.
- Out: **hard rules that gate portability.** DS-001 through DS-009 are the product; they are examined
  like everything else but the bar for changing them is the owner's, not this task's.
- Out: adding rules. This audit removes and narrows; anything it finds missing is raised as its own
  task.
- Out: **the validation tolerance question**, which is a different thing and mostly already answered —
  see below.

**The tolerance question, and why it is not in scope**
Raised by the owner 2026-08-13: a review-and-fix loop that demands 100% compliance can run forever on
an unforeseen contradiction. **Most of that machinery already exists.**
[`EVALUATION.md`](../docs/EVALUATION.md) §0 states *"the score is a stopping rule, not a quality
claim"*; §1 makes `hard` rules gates that are **never scored** and scores only `default` and
`guidance`, which is exactly the territory a deck may depart from with a reason; **DS-000** is the
override clause; §5 sets the threshold. What genuinely does not exist is **detection of a
contradiction between two `hard` rules**, and **a defined point at which the loop stops and asks a
person**. Those are worth a task and this is not it.

**Inputs**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the 165 rows.
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — why each is what it is, which is where
  test 3 is decided.
- [`tools/deck/check.py`](../tools/deck/check.py) — the partition, and the 27 excused-here rules that
  are test 2's starting list.
- [T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md) — per-clause coverage. **Read
  together**: a rule whose only checked clause is trivial can pass test 2 while its real content has
  never fired.

**Acceptance criteria**
- [ ] Every rule has a verdict against all three tests, with a one-line reason.
- [ ] DS-146, DS-147 and DS-138 are each decided, not deferred.
- [ ] Every deletion, merge and narrowing is recorded in `DESIGN-RATIONALE.md` with what it cost and
      what it bought.
- [ ] The reference decks still pass after the changes, and any rule whose removal changes a deck is
      reported — that is evidence the rule was load-bearing and the removal was wrong.
- [ ] `ruleset.py --counts` and `--gates` still partition, and the documents state the new numbers.
- [ ] A statement of how many rules were examined and left alone, since that is the audit's main
      product.

**Open questions**
- Whether a rule that passes test 1 and 3 but fails test 2 should be demoted or instrumented.
  Decided per rule, from whether an instrument is cheap.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Extract the 27 excused-here rules — test 2's candidate list | the starting set |
| 2 | Test 1 across all 165: does a subject exist in any real deck | the dead list |
| 3 | Test 3 across all 165: scope against stated rationale | the over-broad list |
| 4 | Decide DS-146, DS-147, DS-138 first, as the worked examples | three decisions |
| 5 | Apply deletions, merges, narrowings; record each | ruleset, rationale |
| 6 | Re-run both reference decks; report any that changed | the load-bearing check |
| 7 | Restate the counts | `--counts`, `--gates`, README |

## 3. Implement

**Decisions & assumptions**
-

**Outputs produced**
-

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
|  |  |  |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-13 | → proposed | Raised by the owner, asking whether rules exist that make a deck harder to build without making it better. They do, and three kinds were already on the record before the question was asked: dead legislation (DS-146, DS-147 govern a component that does not exist), over-broad scope (DS-138 blocked a chrome menu its rationale never meant to reach), and 27 rules excused on every deck ever built. Scoped as a three-part test rather than a cull, because the audit's main product is the rules it examines and keeps. |
