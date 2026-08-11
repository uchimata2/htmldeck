---
id: T-038
title: Stop the gate reporting judge rules, and one verdict under the wrong rule ID
type: fix
status: done
phase: review
parent: null
blocked_by: []
related: [T-005, T-014, T-037]
work_package: WP3
shipped_in: 0.1.0
owner: maintainer
created: 2026-08-09
updated: 2026-08-12
deliverables:
  - tools/deck/audit.py
  - docs/DESIGN-SYSTEM.md
  - docs/DESIGN-RATIONALE.md
  - docs/LESSONS.md
  - docs/EVALUATION.md
---

# T-038 — Stop the gate reporting judge rules, and one verdict under the wrong rule ID

## 1. Specify

**Outcome**
Every verdict `tools/deck/audit.py` emits cites a rule that the ruleset says a check may decide, and
cites the rule it is actually testing. Where the gate is measuring a *proxy* for a rule rather than
the rule, either the rule gains an ID for the proxy or the gate stops claiming it.

**Why this one**
Found while populating [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md)'s
`Reach` column, which forced a row-by-row reading of what the gate claims against what the ruleset
says. Two rules labelled `judge` — the evaluator's territory, explicitly *"judgement"* — are gated
mechanically, and one of the two reports under an ID whose rule it does not test.

**The two, with the evidence**

| | Ruleset says | `audit.py` emits |
| :--- | :--- | :--- |
| **DS-137** | *"Two simultaneous interactions need a **defined precedence rule**."* `hard` / `judge` | `panels open at once: <n>`, passing when `<= 1` (`audit.py` ~line 428) |
| **DS-161** | *"**Closed, the slide still makes its point.**"* `hard` / `judge` | `panels closed by default: <n> open`, passing when `0` (`audit.py` ~line 426) |

DS-137 is the milder case: at most one panel open is *evidence of* a precedence rule for one
interaction pair, not the rule, which is about precedence in general. **DS-161 is the real defect.**
Its rule is a judgement about whether the argument survives with everything closed; *"panels are
closed at load"* is a **precondition** of asking that question and is not the question. The check is
worth keeping — it is just not DS-161, and the source comment says as much, reading
`// DS-160/161 - closed by default` while DS-160 is *"Two tiers, never three."* So the comment names
a third rule that is also not what is being measured.

**Scope**
- In: the two verdicts above — decide for each whether the rule's `Check` value is wrong, the gate
  should stop claiming it, or a new rule ID is owed for the mechanical fact.
- In: a sweep of the rest of `audit.py`'s verdicts for the same mismatch, since two were found
  without looking for them.
- In: whatever `Reach` values the outcome implies, written into the ruleset.
- Out: **building any new check.** This task corrects what existing verdicts claim.
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) owns coverage.
- Out: the `judge` rules' own home — `docs/EVALUATION.md` is unaffected either way.
- Out: `audit.py`'s *"Not gated here, and why"* tail, which
  [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) found conflates *"checked
  in another stage"* with *"cannot be checked"*. Same file, different defect, and it belongs with
  T-005's coverage work.

**Inputs**
- `tools/deck/audit.py` — the verdict list, and the `// DS-160/161` comment above the probe.
- [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-137, DS-160, DS-161, and the `Check` and
  `Reach` column definitions.
- [`EVALUATION.md`](../docs/EVALUATION.md) §1 — `judge` rules are scored, not gated, which is the
  boundary being crossed.

**Acceptance criteria**
- [ ] Every verdict `audit.py` emits names a rule whose `Check` value permits a check to decide it
- [ ] No verdict cites a rule it does not test; where a proxy is being measured, the thing measured
      and the rule cited are the same thing, or the proxy has its own ID
- [ ] The DS-160/161 comment names the rule actually being probed
- [ ] The rest of the verdict list is swept for the same mismatch, and the count found is stated —
      including if it is zero
- [ ] Whatever changes, `audit.py` still reports **0 mechanical failures** on
      `examples/reference-deck.html`, or the new failure is a real defect and is written down as one
- [ ] Any rule whose `Check` value changes gets its `Reach` value reviewed in the same edit, so the
      two columns cannot disagree

**Open questions**
- **Does *"closed by default"* deserve its own rule ID, or is it already DS-073's inverse? — owner.
  *Recommended: give it its own ID*, and the owner indicated support for this reading on
  2026-08-09; it is recorded as the recommendation rather than as the answer, because the rule's
  actual wording is this task's work and not a thing to settle in a sentence.**

  The objection to inventing a rule so a check has somewhere to live is real, but it does not apply
  here, and the distinction is worth stating because it will come up again. **It is backwards when
  the check is the reason the rule exists.** Here the rule is load-bearing and simply was never
  written down: *on the stage, every disclosure panel is closed at load* is a **precondition that
  two other rules already depend on**. DS-161 asks whether the slide still makes its point with
  everything closed — a question with no content unless closed-at-load is guaranteed. DS-073
  requires the reflow view to render every panel **open** and inlined, which is only a meaningful
  contrast against a stage that starts closed. So two rules lean on a fact the ruleset never
  states, and the check that happens to exist is evidence the fact matters, not the motive.

  DS-073's inverse is the tempting shortcut and it is not sufficient: DS-073 governs the **reflow
  view**, and a rule about a different rendering cannot carry an obligation on the stage by
  negation. Reading it that way would leave the stage's behaviour derivable only by someone who
  notices the inversion — which is the class of unstated dependency this whole task is about.

  What this implies for the rest of the task: DS-161 keeps its judgement and stays `judge`, the new
  rule takes the mechanical fact as `hard` / `auto` / `Reach: yes`, and `audit.py`'s existing probe
  moves to it unchanged — a re-pointing rather than new work, which is what keeps this inside §1's
  *"out: building any new check"*.

  **Answered 2026-08-09 — its own ID, and the wording is `DS-227`:** *on the stage, every disclosure
  panel is closed at load.* `hard` / `auto` / `Reach: yes`, filed in §5.3 beside the rules that lean
  on it. The reasoning above is unchanged and is the reason; what the phase owed was the sentence.

**The sibling decision the answer forces — DS-137.** The same three outcomes apply, and the answer
is the same shape with a different label. *At most one panel open at a time* is a **defined
precedence rule for one interaction pair**; DS-137 requires that a precedence rule exist and does
not supply one, so the two are not the same claim and the gate cannot cite DS-137 for it. It becomes
**`DS-228`** — *at most one disclosure panel is open at a time* — and it is `default`, not `hard`,
because a slide genuinely arguing two details side by side is a coherent design that DS-000 lets a
recorded reason license, and `default` is the label DS-169 already gives to more than one
interaction on a slide. DS-137 keeps its `judge` value and the gate stops claiming it.

**The sweep needs a discriminator, or criteria 2 and 4 cannot be checked.** Nearly every verdict
here decides *part* of its rule, and calling that a defect would condemn the whole gate. The test
applied is **subject identity, not completeness**:

- **A mismatch** — the thing measured is not what the cited rule is about, so a conforming deck can
  fail the check or the ID is named with nothing testing it. DS-161 (a precondition, not the
  judgement), DS-137 (evidence of a rule, not the rule).
- **Not a mismatch** — the check decides one clause of the cited rule and is silent on the rest.
  Passing is evidence for the rule and failing is a real violation of it, which is what a partial
  check owes. DS-091 measures headline length and not the fragment count; DS-203 measures type size
  and not the whole of prominence.

## 2. Plan

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Sweep all 40 verdicts `audit.py` emits — 13 static, 27 rendered — against the discriminator in §1, and record every one, so a *not a mismatch* verdict is visible rather than merely absent | The sweep table in §3, and the count criterion 4 asks for |
| 2 | Write **DS-227** and **DS-228** into `DESIGN-SYSTEM.md` §5.3, both with `Check` and `Reach` filled, and the *why* into `DESIGN-RATIONALE.md` as §5.6 — the ruleset states the rule, the rationale carries the argument | Two rows in §5.3; a new §5.6 |
| 3 | Re-point the two named verdicts in `audit.py`: DS-161 → DS-227, DS-137 → DS-228, and rewrite the `// DS-160/161` comment to name what the three probe lines actually measure | `tools/deck/audit.py` |
| 4 | Fix whatever else step 1 found, cheapest honest fix per finding: re-cite where a correct rule exists, drop the verdict where no rule owns the measurement, repair the assertion where the verdict tests nothing | `tools/deck/audit.py` |
| 5 | Derive the `Reach: yes` ∧ `Check ∈ {auto, render}` count before and after, since criterion 6 pairs the columns and T-005 plans against that number | The two numbers, stated in §4 and in the log for T-005 |
| 6 | Re-run the gate: `audit.py` on the reference deck, both variant suites, `contents_bound` and `chrome_row`, and `task.py check --closing` | 0 mechanical failures, or a written-down defect |
| 7 | Record the reusable half in `LESSONS.md` — L-36's inverse, a check with no rule rather than a rule with no check | **L-41** |

## 3. Implement

### The sweep — 40 verdicts, 7 wrong

`audit.py` emitted **40** verdicts: 13 static and 27 rendered. Every one was read against its rule
under §1's discriminator. **Seven were wrong**, in four shapes. The two the task was opened for are
the first two; the other five were found by the sweep §1 put in scope precisely because those two
had been found without looking.

| Verdict, as it stood | Shape of the defect | Fixed by |
| :--- | :--- | :--- |
| **DS-161** — `panels closed by default: n open` | **A precondition standing in for its rule.** DS-161 asks whether the slide still makes its point closed; whether the panels *are* closed is the condition under which that question is asked. Also `judge`. | Re-pointed to the new **DS-227** |
| **DS-137** — `panels open at once: n` | **Evidence of a rule reported as the rule.** DS-137 requires a *defined precedence rule*; one-panel-at-a-time is one such rule for one interaction pair. The particular asserted as the general. Also `judge`. | Re-pointed to the new **DS-228** |
| **DS-080/081/082** — `sections: n`, pass at `>= 6` | **Two IDs cited by a check that cannot fail for them.** Only DS-081 is tested. DS-080 is about the *element type* and the probe counts `.slide` whatever the tag; DS-082's *past 12 needs a recorded reason* is not in the file at all. | Now cites **DS-081** alone, and reads `slides:` — the old label was the DS-080 claim in a word |
| **DS-111** — `inline SVG figures: n`, pass at `> 0` | **Existence measured, form cited.** DS-111 governs what a diagram is *made of* and explicitly permits `<canvas>` and WebGL, so the check **fails a conforming all-canvas deck** and passes a deck whose other figures are card grids. | **Verdict dropped**, count still printed as a measurement. No rule in the ruleset requires a deck to carry a figure, and inventing one so the check has a home is the error §1 argues against |
| **DS-143** — `reduced motion keeps the dashes` | **The wrong state measured.** DS-143 is about what survives `prefers-reduced-motion`; `render_data` takes one render in the **default** state, so a deck dropping the dasharray under the media feature passes. | Re-cited to **DS-140**, whose `Current` is *dasharray 7 6* — which is what the measurement actually decides |
| **DS-076** — `position preserved…: 'name'` | **An assertion that could not be false.** It passed on `bool(backOnSlide)`: any deck with a current slide after returning. The rule says *preserved in both directions* and nothing compared the two ends. | Probe records `leftFrom`; the verdict now requires the two to be equal |
| **DS-130** — `current slide's disclosure reachable: None` | **Nothing measured, reported as a pass.** Taken at the top of the probe, so it landed on slide 1, which has no disclosure control — `null`, and the predicate was `is not False`. **L-36** inside the instrument. | Measured on slide 5, which has one; the predicate is now `is True`, so a null fails |

**The other 33 are correctly cited and most are partial**, which §1's discriminator admits: they
decide one clause of their rule, so passing is evidence for it and failing is a real violation. Four
were close enough to be worth naming, and each was kept deliberately:

- **DS-168** enforces the 24 CSS px branch and not the spacing exception, so a deck conforming via
  the exception would fail. Kept: the subject measured *is* the rule's subject, and no deck here
  uses the exception. Named so the next one is not surprised.
- **DS-032** hard-codes the string `Open Font License`, which fails a face under any other
  redistributable licence. Same subject, narrower than the rule.
- **DS-203** compares computed font size, and prominence is size, weight, colour and position.
  One-sided: it cannot confirm the rank, and anything larger than the bottom line is a real breach.
- **DS-070** tests that the control *works*, not that it is persistent, visible and keyboard-operable.

**Two more sit outside `audit.py` and were not touched**, because §1's inputs name `audit.py` and
its verdict list. Recorded so the sweep's edge is visible rather than implied:

- `contrast.py`'s failures are labelled `contrast/<pair>` and cite **no rule ID**. §7 says its
  criterion numbers *are* the IDs, so 1.4.3 is the citation owed.
- `contract.py` emits a **DS-072** verdict and lists DS-072 in the same run's *"Not gated here, and
  why"* tail, which is a contradiction inside one file — and that tail is explicitly out of scope in
  §1 and belongs with [T-005](T-005-build-check-the-gate-the-deck-must-pass.md).

**Decisions & assumptions**

- **Two new rules rather than one, and the split is by kind — 2026-08-09.** *Closed at load* is an
  initial condition two rules lean on; *one open at a time* is a precedence behaviour under
  interaction. They are separately violable and separately measured, so folding them into one ID
  would put the gate back where it started, with a verdict citing part of a rule.
- **DS-228 is `default`, DS-227 is `hard` — 2026-08-09.** A panel open at load has no defensible
  other side. Two panels open together does have one, so it is a DS-000 departure with a reason.
- **The DS-076 and DS-130 repairs are corrections, not new checks — 2026-08-09.** §1 rules out
  *building* a check. Both verdicts already existed and already named the right rule; each was made
  to test what it names. The verdict count did not grow, no second render was added, and the
  alternative — deleting two verdicts that were one line from being true — would have cost coverage
  to respect the letter of a scope line.
- **DS-143's real check is not built, and that is a coverage gap, not a fix — 2026-08-09.** Deciding
  it needs a second render under `prefers-reduced-motion`, which is new-check work and T-005's.
- **`EVALUATION.md` was updated, against §1's line that it is unaffected — 2026-08-09.** That line
  scopes out the *judge rules'* home, and it holds: nothing about DS-137 or DS-161 changed there. But
  every count in that document is derived from the ruleset, and this task added two rules, so leaving
  them would have made a stale number staler. Re-deriving found the `render` count had **already
  drifted by six** before this task — 39 recorded against 45 actual.
- **The `Reach` column did not move for any existing rule — 2026-08-09.** No existing rule's `Check`
  value changed, so criterion 6's pairing had nothing to review; the two new rules carry both columns
  from the start. What did move is the **count**, which is criterion 6 read in the other direction.

**Outputs produced**
- [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — DS-227 and DS-228 in §5.3
- [`docs/DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) — §5.6, why both rules exist and why one
  is `hard` and the other `default`
- [`tools/deck/audit.py`](../tools/deck/audit.py) — seven verdicts corrected, two probe measurements
  moved or added, three comments rewritten to name what is measured
- [`docs/LESSONS.md`](../docs/LESSONS.md) — **L-41**, L-36's inverse
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) — the derived counts re-derived and re-dated

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every verdict names a rule whose `Check` value permits a check to decide it | **met** | The only two `judge` citations were DS-137 and DS-161; both are gone. The 39 remaining verdicts cite rules whose `Check` is `auto` or `render` — checked against the ruleset row by row in §3's sweep |
| No verdict cites a rule it does not test; a measured proxy either matches the rule or has its own ID | **met** | Seven corrected, listed in §3 with the shape of each. Two proxies earned IDs (DS-227, DS-228); one had no rule to earn and the verdict was dropped (DS-111); two were re-cited to the rule they do test (DS-081, DS-140); two were made to test what they already named (DS-076, DS-130) |
| The DS-160/161 comment names the rule actually being probed | **met** | `audit.py` now reads *DS-227 — every panel closed at load. DS-228 — at most one open at a time… DS-138 — the open one drops below its control*, and says what the old comment got wrong |
| The rest of the verdict list is swept, and the count found is stated | **met** | **40 verdicts swept, 5 findings beyond the two named** — DS-080/082, DS-111, DS-143, DS-076, DS-130. The 33 correct ones are stated as correct, with the four closest calls named and the reason each was kept |
| `audit.py` still reports 0 mechanical failures on the reference deck | **met** | `0 mechanical failure(s): none`, all four stages. Both variant suites still catch every seeded defect: deliverable 7/7, contract 7/7 |
| Any rule whose `Check` value changes gets its `Reach` reviewed in the same edit | **met, vacuously — and the count moved anyway** | No existing rule's `Check` changed. The two added rules carry `auto`/`yes` and `render`/`yes`. **Derived from the ruleset: `Reach: yes` with `Check` in {`auto`, `render`} went 105 → 107, and the owned total 109 → 111** |

**Child fix tasks raised**
- none. The three gaps this opened are **coverage**, which
  [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) owns and must now account for: **DS-080**,
  **DS-082** and **DS-111** lost a claimed check that never tested them, and **DS-143** lost one that
  measured the wrong state. All four keep `Reach: yes`, so the coverage declaration owes each of them
  a checked-or-excused line. Raising separate tasks would split one account across five files.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | → done | **Six of the six criteria met, and the sweep found more than twice what the task was opened for.** Two verdicts were known wrong; **seven of forty were**, in four shapes, and **none had ever failed** — the deck is conformant, so nothing in a green run separated a check that holds from one that cannot fire. Two of the five new findings are not citation errors at all but assertions that could not be false: **DS-076** passed if any slide was current after returning from the reflow view, and **DS-130** measured a slide with no disclosure control, reported `null`, and passed on `is not False`. Both were repaired rather than deleted — they already named the right rule and were one line from testing it — and the reasoning for treating that as correction rather than as the new-check work §1 excludes is in §3. **`EVALUATION.md` was touched despite §1 saying it is unaffected**: that line scopes out the judge rules' home and still holds, but the document's counts are derived from the ruleset this task changed, and re-deriving them found the `render` figure had **already drifted by six** before today. The number T-005 plans against is **107**, up from 105, and its file now says so in both §1 and its log. |
| 2026-08-09 | → review | Gate green on the reference deck at all four stages, and the two suites still catch every seeded defect — the check that the corrections did not quietly disarm anything. **No deck was built or looked at**: this task changed a ruleset and a measuring tool, and the reference deck is unmodified, so CLAUDE.md's *open it and look* bar has nothing to bind to here. What replaces it is the gate's own output on the unmodified deck, which is the artifact this task was actually changing. |
| 2026-08-09 | → in_progress | Plan written. Seven steps, and **two of them are not obviously in this task's scope until the reason is stated.** Step 1 records the *not a mismatch* verdicts as well as the mismatches, because criterion 4 asks for a count and a count with no rejected candidates beside it cannot be audited — it reads identically whether the sweep was strict or lazy. Step 5 derives the ruleset count twice; criterion 6 pairs `Check` with `Reach`, and adding two rules moves the number [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) plans against even though no existing rule's `Check` value changes, which is the case the criterion was written for read in the other direction. |
| 2026-08-09 | → specified | **The open question is answered and the phase's remaining work was the sentence, not the decision.** *Closed at load* becomes **DS-227**, `hard` / `auto` / `Reach: yes`. Answering it forced a **sibling decision the question had not asked for**: DS-137's verdict is the same defect in a milder form, and leaving it while fixing DS-161 would close this task with one of its two named rules untouched. It becomes **DS-228**, `default` rather than `hard` — a slide arguing two details side by side is a design DS-000 lets a reason license, and DS-169 already treats more than one interaction per slide that way. The specify phase also added the **discriminator** the sweep runs on: subject identity, not completeness. Without it criterion 2 condemns every partial check in the gate, which is most of them, and criterion 4's count means nothing. |
| 2026-08-09 | (no change) | **The owner sequenced this ahead of [T-005](T-005-build-check-the-gate-the-deck-must-pass.md), and the reason is worth keeping because it works in one direction only.** T-005's coverage account asserts a number derived from the ruleset — **105** when this was written, being `Reach: yes` with `Check` in {`auto`, `render`}. This task's last acceptance criterion requires any rule whose `Check` value changes to have its `Reach` reviewed in the same edit, so **landing this can move that number**. Running T-005 first would have it build an account that counts DS-137 and DS-161 as covered, one of them under an ID whose rule the gate does not test, and then need re-deriving anyway. Recorded here rather than only in the handoff: a handoff is consumed once, and this ordering has a reason that outlives it. Whoever plans T-005 should **re-derive the count after this task closes** rather than carrying 105 across. |
| 2026-08-09 | → proposed | **Raised from [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md)'s implement, and deliberately not fixed there.** Populating the `Reach` column forces a row-by-row comparison of what the ruleset says a rule is against what the gate claims about it, and that comparison found two `judge` rules being gated mechanically — **DS-137** and **DS-161** — with DS-161's verdict measuring *"panels closed at load"*, which is a precondition of its rule rather than its rule. The source comment above the probe reads `// DS-160/161 - closed by default` and DS-160 is *"Two tiers, never three"*, so it names a third rule that is also not what is measured. **Both were found without looking for them**, which is why §1 puts a sweep of the remaining verdicts in scope. Not fixed in T-037 because re-labelling a rule and editing the gate are both outside that task's scope, and it would have meant changing the column it was in the middle of populating on the strength of its own reading. |
