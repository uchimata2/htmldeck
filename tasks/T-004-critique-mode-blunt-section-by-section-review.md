---
id: T-004
title: Critique mode — blunt section-by-section review
type: deliverable
status: done
phase: review
parent: null
blocked_by: [T-014, T-020]
related: [T-002, T-005]
work_package: v0.1
owner: maintainer
created: 2026-08-04
updated: 2026-08-09
deliverables:
  - skills/htmldeck/references/critique.md
  - tools/deck/critique.py
---

# T-004 — Critique mode — blunt section-by-section review

## 1. Specify

**Outcome**
A mode that reviews a deck slide by slide, bottom line up front, with no diplomatic padding.

**Why this one**
The most useful artifact in the corpus is a critique, not a deck. It caught a structural gap in the argument, a two-column format that only landed on one side, a "Venn diagram" whose sets did not overlap, a metaphor used four times, a typo on the most important slide, and generator branding left in a corner. This is the part users cannot do for their own work.

**Scope**

- In: **both report formats**, which [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md)
  ruled are one mode over two inputs — the **specification review** at pipeline stage 5, and the
  **design audit** at stage 7 and whenever a user points at a deck.
- In: **the mechanical half of the report, assembled rather than retyped.** `check.py --json`
  already emits the rows, the coverage account, the figure ledger and which halves ran; a reviewer
  that re-derives those by reading is a reviewer that gets a count wrong (**L-08**). What this mode
  adds is *which* finding matters, which is the half no program has.
- In: **the hard-judge checklist as a worksheet.** `ruleset.py --gates` prints 25 `hard` rules that
  no mechanical gate can reach, and [`EVALUATION.md`](../docs/EVALUATION.md) §1.1 requires one
  `pass` / `fail` / written excusal each — **a rule in none of those three states fails the run.**
  This mode is where those verdicts are produced.
- In: **the source-vs-source contradiction pass.** An acceptance criterion below requires it and
  nothing implements it: `content.py` reconciles deck-against-source (`FIG-1`, `FIG-2`) and
  deck-against-itself (`FIG-3`), and no check compares two sources with each other. A deck inherits
  its sources' disagreements, so the gap is real rather than notional.
- In: **the four outcomes**, which are not interchangeable — PASS, CAP, STALL, OSCILLATION, each
  reporting something different, and OSCILLATION reporting it into
  [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §2 rather than at the deck.
- In: the plugin wiring — `SKILL.md`'s critique section and the two `pipeline.md` rows that still
  record the report formats as unfixed.
- Out: **applying fixes.** Settled 2026-08-07: the user-invoked mode reports and nothing else. A
  reviewer that edits its own subject cannot be re-run to prove the fix landed.
- Out: **counting.** [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) owns it and closed
  having built it. This mode consumes the count.
- Out: **restating what another document owns** — [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §6's
  twelve anti-patterns and [`EVALUATION.md`](../docs/EVALUATION.md)'s anchors are cited, never
  copied. T-014 recorded that as the assumption to revisit here, and it survives revisiting: a check
  and the standard it tests cannot be two documents.
- Out: **numbers reaching the user.** [`EVALUATION.md`](../docs/EVALUATION.md) §8.2 is settled — a
  dimension at 0 or 1 reaches the user as a finding *naming the dimension*. Scores exist inside the
  loop and never in the report.
- Out: **deciding the ruleset's own open questions.** DS-045's two readings and DS-219's *never*
  against its own reason are the owner's; a critique that settles them is legislating.

**Inputs**
- `docs/EVALUATION.md` — the dimensions, the threshold, §6's loop and its four outcomes, §1.1's
  two gate halves, §8's decisions on who scores and what the user sees
- `docs/DESIGN-SYSTEM.md` §6 — the twelve anti-patterns, cited as `X-nn`
- `docs/DESIGN-RATIONALE.md` §2 — where an OSCILLATION finding is recorded
- `tools/deck/check.py --json`, `tools/deck/ruleset.py --gates`, `tools/deck/content.py` — the
  mechanical half, already built
- `examples/reference-deck-seeded-defects.html` — ten known defects, one per dimension, with a
  published ledger of what a review ought to find
- `skills/htmldeck/references/pipeline.md` — stages 5 and 7, which are this mode

**Acceptance criteria**
- [ ] Opens with a verdict, then grades each slide
- [ ] Names specific defects with the slide they are on — no general advice
- [ ] Run against a deck with known defects and found them
- [ ] Voice stays direct; no compliment sandwich
- [ ] **When sources are supplied, reconciles the deck against them** — and reconciles the sources
      against each other, because a deck inherits their disagreements
- [ ] Run against a deck built from sources that contradict each other, and found the contradiction
- [ ] States plainly when it reviewed the deck alone, so a clean report is not read as "the content
      is right"
- [ ] **Both formats exist and are distinguishable** — the specification review as
      `ID · Severity · Slide · Finding · Fix` with an *"Open — needs a decision"* section and counts;
      the design audit as verdict, coverage table, findings citing the rule or anti-pattern, then an
      explicit keep-versus-rebuild split
- [ ] **Every one of the 25 hard-judge rules gets `pass`, `fail`, or an excusal in writing**, and a
      rule in none of those three states fails the run
- [ ] **The report says which passes ran** — auto, render, per-slide, whole-deck, and whether sources
      were supplied — and names the dimensions no mechanical check reached
- [ ] **No score reaches the report.** A dimension at 0 or 1 appears as a finding naming it
- [ ] The four outcomes are distinguishable in the output, and OSCILLATION names the two rules in
      tension rather than proposing a third fix

**The second class of finding**

The corpus critique's findings are all inside one deck. `docs/BRIEF.md` § *The critique pass* records
a second class, from a five-document set audited before its deck was built: figures correct where
written and wrong where quoted, a summary contradicting the table above it, a count drifted from the
model it described. Each document had passed its own review. **All of them were found by counting,
not reading** — so this mode needs a counting pass, not only a reading pass.

The cheap technique that worked: one table of every figure in the material, its origin, and every
place it is reused.

**Open questions**
- ~~Should critique be able to apply its own fixes, or only report?~~ **Answered 2026-08-07 by the
  owner: report only, when the user invokes it as a mode.** Inside the convergence loop the fixes
  are the build step's, as [`EVALUATION.md`](../docs/EVALUATION.md) §6.2 already has them, with the
  fix ledger keeping them attributable. The reason to hold the line at the user-invoked mode is
  evidence, not purity: a reviewer that edits its own subject cannot be re-run to prove the fix
  landed, and two reports of the same deck stop being comparable.
- ~~Does the counting pass belong here or in the build check (T-005)? They overlap. Likely: T-005
  gates automatically, critique explains and prioritises.~~ **Answered 2026-08-07 by the owner:
  the hypothesis was right — [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) counts, this
  mode explains and prioritises.** Counting is deterministic and has to *gate*, which is what T-005
  is; its three figure criteria already own it. What a count cannot produce is which wrong number
  matters, and that is this mode's half.

## 2. Plan

**The shape follows T-002's, and for the same reason.** A reviewer has a mechanical half that must
not be retyped and a judgement half that is the whole point. Steps 1–3 assemble the first so step 4
can be about the second.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Build the source-vs-source pass — the acceptance criterion nothing implements. Two sources naming the same quantity with different values is a finding **about the material**, before any deck exists | `FIG-4`, in `tools/deck/content.py` |
| 2 | Build the report assembler: the coverage table, which passes ran, the figure ledger, the hard-judge worksheet with every rule unanswered, and the dimensions no check reached — **all derived, none stored** (**L-08**) | `critique.py`, under `tools/deck/` |
| 3 | Make it refuse to report on an incomplete worksheet: a hard-judge rule left blank fails the run, exactly as a silent mechanical rule does. Self-test on fixtures whose answers are known (**L-04**) | the same tool |
| 4 | Write the mode: two formats, the four outcomes, the voice, what to do with a finding the gate already made | `critique.md`, under `skills/htmldeck/references/` |
| 5 | Wire it: `SKILL.md`'s critique section and the two `pipeline.md` rows recording the formats as unfixed | edits, `check_scaffold.py` green |
| 6 | **Run it against the seeded-defect deck**, whose ten defects are published with a ledger, and against the good deck. A review that cannot tell them apart is not a review | the two reports, and what each found |
| 7 | Run it against a contradicted source set, and show the contradiction reported | the run, in §3 |
| 8 | Close: `LESSONS.md`, §3 and §4, then `index` and `check --closing` | a closed task |

**Approach decisions**

- **The tool assembles; it never judges.** — Every row it prints is derived from a file that already
  decided something. The hard-judge worksheet ships **unanswered** and the tool fails if it is
  handed back incomplete, which is the one thing a program can enforce about a judgement. — 2026-08-09
- **`FIG-4` goes in `content.py`, not in a new tool.** — That file owns figure reconciliation and
  already parses both sides; a second parser for the same corpus is the second home this repository
  keeps removing. It adds a row to the gate's account, which is correct: source-vs-source is
  deterministic and belongs to the count, per the 2026-08-07 ruling. — 2026-08-09
- **The report never prints a number that is a score.** — Counts of findings are facts about the
  report; dimension scores are the loop's internals. `EVALUATION.md` §8.2 is settled and the tool
  enforces it by never being given the scores at all. — 2026-08-09
- **A finding the mechanical gate already made is not repeated as a finding.** — It is cited in the
  coverage line instead. The reviewer's value is the 25 judge rules and the five dimensions no check
  reaches; repeating `check.py` pads a report nobody then reads to the end. — 2026-08-09

## 3. Implement

**Decisions & assumptions**

- **`FIG-4` is a reading list, not a gate row — and that is a deviation from §2, taken on
  measurement.** The plan said it lands in `content.py` as a fourth gate row. Three thresholds were
  tried against two real pairs: a restatement that *is* a contradiction (*busiest single day* at
  31,900 in a table against 30,400 in a summary) and a pair that is *not* (*mean round utilisation,
  off-peak* at 71% against *peak* at 88%). **Set equality of the labels misses the true pair**,
  because a restatement rephrases. **Jaccard at 0.6 misses it as well, and so does 0.5.** Every
  threshold loose enough to catch the true pair catches the false one, because what separates them
  is that *peak* and *off-peak* are contrastive — semantics, not counting. So the deterministic half
  stops at *same unit, four shared words, different values*, and a person decides. That is the
  2026-08-07 ruling applied rather than worked around. — 2026-08-09
- **The threshold was measured on two corpora, and the second one is why it is not trusted
  further** (**L-45**). At four shared words: `examples/sort-window/sources` gives **0** candidates
  and is clean; `examples/sources` gives **10** and is also clean, so all ten are false; the
  deliberately contradicted copy gives **1**, the planted pair and only it. Ten false candidates on
  a clean corpus is the honest rate, recorded in `content.py` beside the constant rather than tuned
  away. — 2026-08-09
- **The worksheet ships unanswered and the tool refuses an incomplete one.** `EVALUATION.md` §1.1
  says a rule in none of the three states fails the run, and that is the one thing a program can
  enforce about a judgement. It also refuses a `fail` or an `excused` with no reason written beside
  it, because an excusal with no reason is the row the section was written to remove. — 2026-08-09
- **The self-test reports to stderr, unlike its siblings.** `--worksheet` writes an artifact a
  reviewer redirects into a file; twelve lines of provenance at the top of that file is provenance
  in the product. — 2026-08-09
- **The tool is never given the scores.** `EVALUATION.md` §8.2 is settled, and the surest way to
  keep a number out of a report is for the reporter not to have it. A self-test fixture asserts the
  spine prints no `n/24` or `n/16`. — 2026-08-09

**What the mode found, run against both decks with the same procedure**

The discriminating test: `examples/reference-deck-seeded-defects.html` carries one deliberate
defect per dimension, `examples/reference-deck.html` is its parent with none, and they differ by
exactly ten edits.

| Dim | Seeded defect | Found by | Where |
| :--- | :--- | :--- | :--- |
| **S1** Claim | headline becomes "Wait times" | **DS-090** | worksheet |
| **S2** Evidence | projection restated as observed fact | **DS-102**, **DS-099** | worksheet |
| **S3** Encoding | network diagram becomes four cards and arrows | **DS-116**, **DS-123** | worksheet |
| **S4** Density | the deciding sentence moved behind the click | **DS-161**, **DS-162** | worksheet |
| **S5** Craft | type at 11 units, a panel off its track | **DS-035** | mechanical gate |
| **S6** Motion | a looping ambient pulse | **DS-142**, **DS-141**; **DS-150** | gate, then worksheet |
| **D1** Spine | slides reordered | the stage order read off the spine — `0,3,3,3,3,2,2,1,4,4,4,5,5` against the parent's `0,1,2,2,3,3,4,4,4,5,5` | **no rule; the reviewer** |
| **D2** Pacing | one slide split into three | **DS-084**, **DS-201** | worksheet |
| **D3** Close | the ask becomes a recap and a thank-you | **DS-085** | worksheet |
| **D4** Consistency | the reserve restated as $2.2M | **FIG-1** — 2 unsourced figures of 84, both of them the $2.2M | content half |

**Ten of ten, and the two that needed something other than the worksheet are the point.** D1 is
found by a person reading the spine, and no rule reaches it. D4 is invisible without sources: run
presentation-only, the seeded deck reports a clean content half, which is exactly the false pass the
*say which half ran* rule exists to prevent.

**One thing the run exposed that the ledger does not claim.** With sources supplied the seeded deck
reports **FIG-3 ninety times**, and **thirty of those rows are collateral from the D2 seed** — the
duplicated small multiple puts every figure on three near-identical slides. A pacing defect can bury
a consistency defect inside the figure ledger, which is the sharpest argument yet for *which wrong
number matters* being the reviewer's call and not the count's.

**The caveat, stated rather than left to be inferred.** The reviewer had read the published defect
ledger earlier in the same session, so this is not a blind run. What it does establish without
blindness: the same procedure over the parent deck produces **0** mechanical failures and no
worksheet failure, so the two decks are distinguishable by the mode rather than by memory.

**Outputs produced**
- `tools/deck/critique.py` — the spine, the worksheet, the answer check; 12 self-test fixtures
- `skills/htmldeck/references/critique.md` — both formats, the four outcomes, the voice
- `FIG-4` in `tools/deck/content.py` — the source-vs-source pass, with its measurement beside it
- `SKILL.md` and `pipeline.md` — the mode is loaded rather than described as unfixed

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Opens with a verdict, then grades each slide | **met** | `critique.md` §3.2 fixes the order — verdict first in two or three sentences, then coverage, then findings by severity |
| Names specific defects with the slide they are on — no general advice | **met** | The rule is written into both formats and the eleven worksheet failures in §3 each name a slide or the deck |
| Run against a deck with known defects and found them | **met** | Ten of ten dimensions, §3's table. **Not a blind run** — the caveat is in §3, and the parent-deck control is what carries the claim instead |
| Voice stays direct; no compliment sandwich | **met** | `critique.md` §6, and it names the opposite rule for the deck's own voice so the register is not carried across |
| When sources are supplied, reconciles the deck against them and the sources against each other | **met** | `FIG-1` to `FIG-3` were T-005's; `FIG-4` is new and is the source-against-source half |
| Run against a deck built from sources that contradict each other, and found the contradiction | **met** | A contradicted copy of the sort-window sources; `FIG-4` reported the planted pair and only it, against 0 candidates on the same set uncontradicted |
| States plainly when it reviewed the deck alone | **met** | The spine prints `content half NO - presentation-only, and a clean report here is not "the content is right"`, and §3's D4 row is what that sentence is protecting against |
| Both formats exist and are distinguishable | **met** | `critique.md` §3.1 and §3.2 — different columns, different dimensions scored, and §3.1 names the four it may not touch |
| Every one of the 25 hard-judge rules gets pass, fail, or an excusal in writing | **met** | `critique.py --answers` refuses an incomplete sheet; a `fail` or `excused` with no reason beside it is refused too |
| The report says which passes ran and names the dimensions no check reached | **met** | Both are sections of the spine, and the five blind dimensions are listed by name |
| No score reaches the report | **met** | The tool is never given them; a self-test fixture asserts no `n/24` or `n/16` reaches the output |
| The four outcomes are distinguishable, and OSCILLATION names the two rules | **met** | `critique.md` §5, with OSCILLATION reported into `DESIGN-RATIONALE.md` §2 rather than at the deck |

**Child fix tasks raised**
- none

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-11 | (no change) | **N-4 and N-6, from the first external deck**, routed here by [T-092](T-092-product-feedback-from-the-first-external-deck.md) as needs against a task that built exactly what it specified. N-4: a green build reads as a finished deck, and nothing in the run asks the X-08 question - critique mode exists and an adopter finishing a deck did not reach for it, because the gate had just said `0 failures` and there is nothing in the build's own output to say what that does not cover. N-6: DS-091's six-word cap pulls an author toward the allusive headline, which is the X-08 failure itself, and only the cap is checkable. The pair is one need read twice: **the checkable rule is the one that gets obeyed**, and where a checkable rule and a judged one point in opposite directions the deck goes where the check points. Recorded, not reopened. |
| 2026-08-09 | → done | **Critique mode exists, and the seeded-defect deck is what says so: ten of ten dimensions found, against a parent deck the same procedure clears.** §3 has the table. **The deviation worth reading is `FIG-4`.** §2 planned it as a fourth gate row and the measurement refused: no threshold separates a restatement that contradicts from a qualified pair that does not, because *peak* and *off-peak* are contrastive rather than merely similar. It ships as a reading list, which is the 2026-08-07 ruling — counting gates, judgement explains — applied rather than worked around. **And L-45 earned its keep twice over**: at four shared words the first corpus gives zero false candidates and the second gives ten, so the number is recorded with its measured error rate instead of being tuned to whichever deck was open. **Two findings the ledger does not claim:** a pacing defect buries a consistency defect in the figure ledger — thirty of the seeded deck's ninety `FIG-3` rows are collateral from the duplicated slide — and D1 Spine is reached by no rule at all, only by a person reading the stage order. |
| 2026-08-09 | → planned | **§1 and §2 written; the specify phase found one criterion nothing implements.** *Reconciles the sources against each other* has been an acceptance criterion since 2026-08-05 and `content.py` does not do it: `FIG-1` and `FIG-2` compare the deck with its sources, `FIG-3` compares the deck with itself, and **no check compares two sources**. The 2026-08-07 ruling sends counting to [T-005](T-005-build-check-the-gate-the-deck-must-pass.md), which closed without it, so the pass is built here as `FIG-4` and lands in `content.py` where the other three live. The rest of the plan is T-002's shape: assemble the mechanical half so the mode can be about the judgement half, and **ship the hard-judge worksheet unanswered**, because a rule left blank failing the run is the one thing a program can enforce about a judgement. |
| 2026-08-09 | (no change) | **[T-005](T-005-build-check-the-gate-the-deck-must-pass.md) closed, and the report this mode consumes now exists.** `python tools/deck/check.py <deck> --json` emits the rows, the **coverage account** (owned, checked, failing, excused with a reason each, silent), the **figure ledger** this mode prioritises, which halves ran, and the five dimensions the gate is blind to. **Two things that bear on this mode's own scope.** The gate decides 77 of 111 owned rules and names the other 34 - so a critique that repeats a mechanical finding is repeating one the build already had, and the useful half is the 43 `judge` rules plus S1, S2, S4, D1 and D4. And **two rules are open questions for the owner** - DS-045's two readings, DS-219's *never* against its own reason - which a critique should not decide either. |
| 2026-08-07 | (no change) | **Both open questions answered by the owner; §1 now has none.** *Report, do not fix* — the user-invoked mode reports and nothing else, while the loop's fixes stay with the build step under [`EVALUATION.md`](../docs/EVALUATION.md) §6.2. *Counting belongs to [T-005](T-005-build-check-the-gate-the-deck-must-pass.md)* — this mode consumes the count and says which wrong figure matters. **The second answer removes work from here and adds a dependency**: the counting pass in §1 above is no longer this mode's to build, so what it needs from T-005 is the figure ledger in a form it can cite — which is one more reason this mode follows the check rather than preceding it. **The `related` edge this implies is now written on both files** — it existed in [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md)'s reasoning for the build order and in neither task's front-matter, and `related` is asymmetric, so it has to be stated twice or the task that needs the context cannot see it. |
| 2026-08-07 | (no change) | **[T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) ruled: this mode takes two input types, and it is not split into two modes.** The **specification review** runs before any HTML exists and the **design audit** after the build; both are critiques over different inputs, and two modes would duplicate the reporting machinery for that one difference. **The scope growth is real and it is the cheap half.** T-020 §3.3 maps six of the ten dimensions onto a slide-by-slide spec — S1, S2, D1, D2, D3 and D4's source-reconciliation half — **three of them among the five no mechanical check can reach.** The two report formats are R1 §14's, not inventions: spec review as `ID · Severity · Slide · Finding · Fix` with Major/Minor/Note, then *"Open — needs a decision"*, then counts; design audit as headline verdict, coverage table, findings with the principle violated, then an explicit keep-vs-rebuild split. |
| 2026-08-07 | (no change) | **Blocked on [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md), added by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md).** T-020 decides whether the **specification review** — the second critique format R1 §14 proves, run before any HTML exists — belongs to this mode or becomes one of its own. That is a doubling of scope, not a detail: §1 above reviews a built deck only, and every acceptance criterion is written against a rendered artifact. A mode specified for one format and then handed two is respecified. |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-05 | (no change) | Added the cross-document class of finding and the counting pass, after a source-document audit found nine defects that five per-document reviews had all passed. Evidence in `docs/BRIEF.md`. |
| 2026-08-06 | (no change) | Owner answered BRIEF open question 6 — sources are supplied, so the cross-document reconciliation added above is now a **standing** part of this mode rather than a conditional one. Two further inputs landed: R3 §6's 12 anti-patterns are directly usable as named defect classes, and R2 §11 gives this mode a testable disclosure check — close every panel and read the deck; if a slide stops making its argument, the tier split is wrong. R4 §2 found the critique format has **zero prior art**, so R1 §14's severity scheme is the only source for it. |
| 2026-08-06 | (no change) | **T-014 closed.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) **§6 owns the twelve anti-patterns and the named defect classes; this mode consumes them and must not restate them** — a check and the standard it tests cannot be two documents. Kept there deliberately, and T-014 recorded it as the assumption to revisit if this task disagrees when planned. M3–M6, M8, M9 and M11 were **deferred to here** as the report's format. The severity scheme (M2) stays in the design system as shared vocabulary. §11 conditions 15 and 23 are explicitly **not machine-checkable** and belong to this mode. *(Corrected 2026-08-09 by [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md): **`DESIGN-SYSTEM.md` §11 never existed** — the document has ended at §9 in every commit, and which rules "15 and 23" meant is unrecoverable. The sentence is left standing because it is what was believed at the time; what this mode actually inherits is every rule whose new **`Reach`** column reads `—`, which is machine-readable and cannot go stale the same way.)* |
| 2026-08-06 | (no change) | **This mode is now the reporting face of a defined evaluator, not a free-standing review.** [`docs/EVALUATION.md`](../docs/EVALUATION.md) supplies the dimensions, anchors, threshold and the four stop outcomes; the design system supplies `DS-nnn` IDs so a finding can cite a rule and a fix can be verified against it. **Three consequences:** findings carry a rule ID and a dimension score, not just prose; the report must state **which passes ran** (auto / render / per-slide / whole-deck), since the whole-deck pass is where cross-slide defects live; and the four outcomes are **not interchangeable** — PASS, CAP, STALL and OSCILLATION need different reports, and OSCILLATION is a finding about the *ruleset* that belongs in `DESIGN-RATIONALE.md` §2. |
