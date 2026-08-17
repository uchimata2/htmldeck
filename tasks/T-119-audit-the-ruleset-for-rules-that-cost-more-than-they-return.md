---
id: T-119
title: Audit the ruleset for rules that cost more to satisfy than they return
type: audit
status: done
phase: review
shipped_in: unreleased
parent: null
blocked_by: []
related: [T-054, T-113, T-114, T-115]
work_package: PH3
owner: the project owner
business_value: high
effort: l
created: 2026-08-13
updated: 2026-08-17
deliverables:
  - docs/RULESET-AUDIT.md
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

**1. Dead legislation — a rule governing something that does not exist.** ~~**DS-146** and
**DS-147**~~ — **withdrawn 2026-08-17 as the first act of this audit, because the evidence was wrong
and the way it was wrong is the finding.** The claim was that both regulate chart behaviour with no
possible subject, on this probe:

```
grep -c -i "chart" shell/components.css   →  0
```

The count is still 0 and it decides nothing. **Both rules govern behaviour, and behaviour is not in
the stylesheet.** `shell/deck.js:410` carries DS-146 by name — *charts and entrances draw in once,
never on the way back* — and `shell/deck.js:825` carries DS-147's `countUp()`, both shipped in all
three decks. The subject is there too: `examples/reference-deck.html` holds a hand-authored line
chart, `<polyline>` twice under an `aria-label` naming it, which is what **DS-122** requires a chart
to be — *no chart library, hand-written SVG* — so a `.chart` class in `components.css` is the one
form the ruleset forbids. **The probe looked for the rule's subject where the rule had banned it
from being.**

Nothing about the concern falls with it. What falls is the assumption that a rule's subject can be
found by a name-shaped search, and that is now a constraint on the audit's own method (test 1
below). **The class stands and its named instances do not**, which is a result rather than a
retraction: two rules that looked dead are alive and gated, and the audit still owes 165 verdicts.
[T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md)'s question is
answerable as asked — DS-122 already answers most of it.

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

1. **Subject.** Could anything a deck is allowed to contain fall under it? A rule with no *possible*
   subject is dead — **possible, not present**, because a prohibition is satisfied vacuously by every
   deck that obeys it and that is the rule working, not the rule sleeping. **Probe the mechanism the
   rule names, never a name that sounds like the rule**: kind 1's two withdrawn instances above were
   both found alive in the file the rule's verb points at, after a search of the file its noun
   suggested returned zero.
2. **Effect.** Has it ever changed a deck — caught something, or shaped a build? A rule that has never
   fired is unverified, not proven.
3. **Scope fit.** Does its wording reach exactly as far as its reason? A rule whose scope exceeds its
   rationale is narrowed to the rationale, not deleted.

A rule failing **1** is deleted. Failing **2** is either given an instrument or demoted to
`guidance`. Failing **3** is narrowed. Passing all three is left alone and **said to have been
examined**, which is most of the value — an audited ruleset is one a later reader can trust.

**Scope**
- In: all 165 rules, each with a verdict and a one-line reason.
- In: the three named candidates above, decided rather than listed. **Two of the three are decided in
  §1 already** — DS-146 and DS-147 pass test 1, on the mechanism rather than on the name — which
  leaves DS-138's scope as the only one still open.
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

**Where the verdicts live: a new `RULESET-AUDIT.md`, under `docs/`.** 165 rows with three verdicts
each is the audit's main product and it is read once by whoever asks whether a rule was examined —
tier 3, loaded by nothing, on `docs/CONTEXT-AUDIT.md`'s precedent. `DESIGN-RATIONALE.md` takes only
what the acceptance criteria send it: **what was deleted, merged or narrowed, and why**. Putting the
165 rows there instead would bury eleven changes in a table nobody finishes.

**The instrument for each test, named before the work rather than after it.**

| Test | What decides it | What it cannot decide |
| :--- | :--- | :--- |
| **1 Subject** | The rule's own verb, probed in the file that implements it — `shell/`, the three shipped decks. §1's withdrawal is the method's own worked example | Nothing much: *possible* subject is a low bar and almost every rule clears it. Expect very few deaths |
| **2 Effect** | `check.py`'s coverage account, which partitions the 115 gated rules per run into **checked / excused in the rules / excused here**; plus the documented record — a rule an amendment or a defect is named against has fired | Whether a *checked* rule has ever come out `FAIL`. The gate reports today's verdict, not its history, and `examples/reference-deck-seeded-defects.html` seeds **five** defects, so it proves five rules and is silent on the rest |
| **3 Scope fit** | The rule text against its own stated reason, in the rule or in `DESIGN-RATIONALE.md` | Anything mechanical. This is the reading test and it is the expensive one |

**Test 2's honest ceiling is stated here so the review cannot be surprised by it.** A rule that no
instrument has ever seen fire is recorded **unverified**, which §1 already rules is the correct
outcome rather than a gap — *a rule that has never fired is unverified, not proven*. The audit does
not manufacture evidence by seeding a defect per rule; that is a bigger task than this one and it is
[T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md)'s neighbourhood.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Take the partition from a live run — 165 rows, 115 gated, checked / excused-here / excused-in-rules — rather than from any figure written down | test 2's candidate set, re-derived |
| 2 | Test 1 across all 165, probing the verb and not the noun | the dead list |
| 3 | Test 2 across all 165 from step 1's partition plus the documented record | the never-fired list |
| 4 | Test 3 across all 165: wording against stated reason | the over-broad list |
| 5 | Decide DS-138 — the one named candidate §1 leaves open | one decision |
| 6 | Write `docs/RULESET-AUDIT.md`: every rule, three verdicts, one-line reason | the audit's main product |
| 7 | Apply the deletions, merges and narrowings to `DESIGN-SYSTEM.md`; record each in `DESIGN-RATIONALE.md` with what it cost and what it bought | ruleset, rationale |
| 8 | Re-run the gate on all three shipped decks; any deck that changes verdict is evidence the rule was load-bearing and the change was wrong | the load-bearing check |
| 9 | Restate the counts — `ruleset.py --counts`, `--gates`, and every document quoting 165 | the figures, corrected together |

**Step 9 is where this task can falsify published numerals**, the way a shell change falsifies deck
sizes. `python tools/docs/figures.py` names them; correct them last, after the ruleset settles.

## 3. Implement

**Decisions & assumptions**

- **The audit was raised to remove rules and removed none.** Every one of the 165 cleared test 1,
  because *possible subject* is a low bar and this ruleset does not legislate for things a deck
  cannot contain. What it found instead is **rules nothing could apply** — a different defect with a
  much cheaper fix, and the reason the result is four changes rather than a cull.
- **The open question is answered the same way for all fourteen: instrument, never demote.** §1 left
  it per rule, *from whether an instrument is cheap*. An instrument existed for every one — naming an
  id in a rubric dimension, or reclassifying to `judge` so the hard-judge checklist takes it — so
  nothing was demoted and no rule lost its label.
- **`Check` and `Reach` are not independent, and DS-042 is where that shows.** The ruleset's preamble
  defends `auto` + `never` as a coherent pair and it is coherent: a program could decide *boxes that
  read as a set are siblings* if something told it which boxes read as a set. **Coherent was doing
  the work that useful should have been doing** — the pair describes a `hard` rule handed to a
  mechanism that cannot decide it in principle, which is a rule nothing will ever apply. The preamble
  keeps the pair and now says no row carries it.
- **The thirteen uninstrumented rules were found by intersecting instruments, not by reading rules.**
  A first pass counted citations outside the ruleset and returned nine, which was wrong in both
  directions: it missed rules the rubric covers by **range** (`DS-041 to DS-049`) and it flagged
  rules the build pipeline names. The instrument that holds is *`judge`, minus `hard`, minus every id
  `EVALUATION.md` names or ranges, minus every id `skills/` names*. **A rule goes missing by being
  numbered between two ranges**, and no reading of that rule can catch it.
- **`docs/RULESET-AUDIT.md` is a dated snapshot and its generator is not shipped.** The script that
  produced it reads a template from outside the tree, so a clone could not run it — and a tool a
  clone receives that cannot run fails `check_all.py` by that command's own partition. The finding
  it would recompute is pinned in the document instead, with the one-expression recipe written out
  so anyone can re-run it by hand. **Recomputing it live was tried and is the trap**: the fix removes
  the finding, so a live count reports 0 and the audit erases its own result.
- **Nine documents quoted the partition this task moved, and one command found all of them.**
  `python tools/docs/figures.py` went red on the first run after DS-042 changed hands and stayed red
  through four rounds of correction, each naming the next document. Not one was found by looking.

**Outputs produced**

- [`docs/RULESET-AUDIT.md`](../docs/RULESET-AUDIT.md) — **new.** The examination: 165 rows, three
  verdicts and a reason each, the four changes, the thirteen orphans, and what the audit could not do.
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-042 reclassified, DS-041 split, DS-138
  narrowed, DS-007 moved to §8; the `auto`+`never` preamble reconciled; a pointer to the audit.
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §6.0 — the record: each change with what
  it cost and what it bought, and the two findings deliberately not acted on.
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — twelve rule ids added across S1, S4 and S5, and the
  range-gap mechanism written down where the dimension lists are.
- [`skills/htmldeck/references/pipeline.md`](../skills/htmldeck/references/pipeline.md) — stage 5
  names DS-213, whose pair DS-212 was already named at stage 4.
- [`tools/deck/check.py`](../tools/deck/check.py) — DS-041's deferral no longer cites a `Reach: never`
  that does not exist, and its closing condition is now a check to write rather than a ruleset review.
- Nine documents corrected for the moved partition: `CLAUDE.md`, `README.md`,
  [`examples/README.md`](../examples/README.md), [`docs/BRIEF.md`](../docs/BRIEF.md),
  `docs/EVALUATION.md`, [`docs/PUBLISHING.md`](../docs/PUBLISHING.md), `pipeline.md`,
  [`critique.md`](../skills/htmldeck/references/critique.md) and
  [`tools/deck/critique.py`](../tools/deck/critique.py).

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :--- | :--- |
| Every rule has a verdict against all three tests, with a one-line reason | **met** | [`docs/RULESET-AUDIT.md`](../docs/RULESET-AUDIT.md) §5. 165 rows, and the ID / Label / Check / Reach columns are read out of `DESIGN-SYSTEM.md` rather than retyped, so the table cannot disagree with the ruleset about what a rule is |
| DS-146, DS-147 and DS-138 are each decided, not deferred | **met** | DS-146 and DS-147 in §1 and audit §2 — **both alive**, and the claim that they were dead is withdrawn with the reason it was wrong. DS-138 narrowed to tier two |
| Every deletion, merge and narrowing recorded in `DESIGN-RATIONALE.md` with what it cost and what it bought | **met** | [§6.0](../docs/DESIGN-RATIONALE.md). Four changes, each with both halves; plus the two findings recorded and deliberately not acted on, which is the same discipline pointed the other way |
| The reference decks still pass, and any rule whose removal changes a deck is reported | **met, and the weaker half of it** | All three shipped decks: 0 failures, partition intact at 84 + 3 + 27 = 114. **Nothing was removed**, so the criterion's real test — does a deck notice — never ran. A ruleset audit that deletes nothing cannot produce that evidence |
| `--counts` and `--gates` still partition, and the documents state the new numbers | **met** | `owned 114 = 69 auto + 45 render`; `119 hard = 88 mechanical + 26 judge + 5 checker-binding`. Nine documents corrected and `python tools/docs/figures.py` is clean — it is what found every one of them |
| A statement of how many rules were examined and left alone | **met** | **165 examined, 161 left exactly as they were**, first line of the audit. Stated beside a second figure on purpose: 16 rules failed a test and only 4 moved, and reading those two counts as one is the error the document warns about |

**The open question is closed.** *Whether a rule failing test 2 should be demoted or instrumented* —
**instrumented, all fourteen**, because an instrument was cheap for every one. Demotion was never
reached.

**What a later reader should distrust here.** Test 2 asks whether a rule has an instrument by
searching the instruments for its id, so a rule applied by something that never names it would read
as an orphan. The thirteen were each read against the rubric's dimensions before being called that;
**the 161 that passed were not read that way**, and the audit says so in its own §6.

**Child fix tasks raised**
- **none, and one thing is owed.** DS-041's narrowed clause — alignment produced by a shared track
  rather than by absolute offsets — is decidable and no check decides it yet. It is not raised as a
  task because the project already tracks that kind of debt where the gate can see it:
  [`tools/deck/check.py`](../tools/deck/check.py)'s `DEFERRED` entry for DS-041 now carries it as its
  closing condition, which is the same mechanism that carried the request this task just answered.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-17 | → done | **165 examined, 161 untouched, 4 changed, nothing deleted.** The task was raised to remove rules and the honest result is that it found almost none worth removing — what it found instead is **thirteen rules no instrument could apply**, plus DS-042, which was `hard` and assigned to a gate under the ruleset's only `Reach: never`. The remedy for all fourteen is an instrument rather than a demotion, and for the thirteen it is five edits naming them in `EVALUATION.md` and the pipeline. **The mechanism is the part that outlives this**: the rubric names rules in ranges, `DS-034 to DS-037` stops one short of `DS-041 to DS-049`, and a rule numbered in the gap is invisible to every reading of itself (**L-116** is the audit's other trap, met live: the generated document recomputed the thirteen after fixing them and printed 0). DS-138 was narrowed off T-114's blocked chrome menu, DS-041 split against DS-042 on a review `check.py` had asked for by name, and DS-007 moved to the section that already claimed to hold its kind. **Nine documents quoted the partition this moved and `figures.py` found every one** — none was found by looking. Closed with one criterion **met only in its weaker half** and saying so: nothing was removed, so *does a deck notice a removal* never ran. |
| 2026-08-17 | → planned | The plan gained a home for the verdicts — `docs/RULESET-AUDIT.md`, tier 3 — and, ahead of the steps, **a table naming what decides each test and what it cannot decide**. That second column is the plan's real work: test 2 has an honest ceiling, because `check.py` reports today's verdict rather than its history and the seeded-defects fixture seeds **five** defects, so no instrument here can tell a checked rule that has caught something from one that has always passed vacuously. Written down before the audit rather than discovered at review, so `unverified` reads as the specified outcome it is. Nine steps, and step 9 is a numeral correction this task can trigger the way a shell change does. |
| 2026-08-17 | → specified | §1 was already written; what specifying it cost was checking its own evidence, and **the first of the three kinds did not survive**. DS-146 and DS-147 were called dead legislation on `grep -c -i "chart" shell/components.css → 0`; the count is right and it answers a question nobody asked. Both rules govern behaviour and both are implemented by name in `shell/deck.js` — 410 for DS-146, 825 for DS-147 — shipped in all three decks, over a real hand-authored line chart in the reference deck that **DS-122 requires to be exactly that**. So the probe searched the stylesheet for a component the ruleset forbids. Kind 1 keeps its class and loses both instances, test 1 is reworded to *possible* subject with the probe constraint attached, and DS-138 is the only named candidate still open. |
| 2026-08-13 | → proposed | Raised by the owner, asking whether rules exist that make a deck harder to build without making it better. They do, and three kinds were already on the record before the question was asked: dead legislation (DS-146, DS-147 govern a component that does not exist), over-broad scope (DS-138 blocked a chrome menu its rationale never meant to reach), and 27 rules excused on every deck ever built. Scoped as a three-part test rather than a cull, because the audit's main product is the rules it examines and keeps. |
