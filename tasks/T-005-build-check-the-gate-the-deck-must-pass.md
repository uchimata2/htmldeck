---
id: T-005
title: Build check — the gate the deck must pass
type: deliverable
status: done
phase: review
parent: null
blocked_by: []
related: [T-001, T-002, T-004, T-007, T-016, T-018, T-021, T-032, T-034, T-037, T-038]
work_package: WP3
owner: maintainer
created: 2026-08-04
updated: 2026-08-09
deliverables:
  - tools/deck/check.py
  - tools/deck/ruleset.py
  - tools/deck/content.py
  - tools/deck/printpages.py
  - tools/deck/static_variants.py
  - tools/deck/content_variants.py
  - examples/sources/README.md
---

# T-005 — Build check — the gate the deck must pass

## 1. Specify

**Outcome**
One check library with two entry points — called per batch and whole-deck by the pipeline, and
exposed as a standalone command taking any HTML file — that returns a pass/fail verdict **per
`DS-nnn` rule ID**, **declares which of the rules it owns it did not check and why**, and, when
sources are supplied, reconciles every figure on a slide against them and against itself. A deck
that passes it is not a good deck; it is a deck carrying no defect this gate was built to see, and
the gate is the thing that has to say so.

**Why this one**
Cheap to build, and it converts several house rules from hopes into failures.

**Scope**

- In: the **109 rules [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) labels `auto` or `render`** —
  65 and 44. That table is the jurisdiction, and the count is what the gate has to account for.
  *(**111**, 66 and 45, when this was built — see the superseded note under the table below. The
  scope is the `Check` column, not the number, which is why the number moving did not move it.)*
- In: **the coverage declaration itself.** An owned rule that is neither checked nor excused in
  writing is the defect class this task exists to end (**L-36**), so the account of all 109 — **111
  as built** — is a deliverable, not a line in a report.
- In: the content half — the figure ledger
  [`artifacts.md`](../skills/htmldeck/references/artifacts.md) already specifies (*Figure · Value ·
  Origin · Used on*), **emitted as an output** rather than kept internal, plus the three
  reconciliation checks over it.
- In: the report format [T-004](T-004-critique-mode-blunt-section-by-section-review.md) consumes.
- Out: **fixing anything.** The gate reports; the build step fixes, and
  [`EVALUATION.md`](../docs/EVALUATION.md) §6.2 keeps the fix ledger. Settled 2026-08-07 and
  restated here because it is the boundary most likely to erode: a gate that edits what it is
  measuring cannot be trusted to have measured it.
- Out: scoring. `hard` rules are gates and are never scored ([`EVALUATION.md`](../docs/EVALUATION.md)
  §1), so this check contributes nothing to a total.
- Out: the 43 `judge` rules and the five evaluation dimensions this gate is structurally blind to —
  **S1 Claim, S2 Evidence, S4 Density, D1 Spine, D4 Consistency**, proven blind against the
  seeded-defect deck. [T-004](T-004-critique-mode-blunt-section-by-section-review.md) owns them.
- Out: `prefers-reduced-motion`, the 3D class and the second never-quiescent animation — none of
  them exists until [T-016](T-016-the-interaction-and-motion-layer.md) lands. A re-entry, named
  in *Known re-entries* below rather than left to be discovered.

**Inputs**

- [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) — the rule table, read **by ID and by `Check`
  value**. This is the scope. It does **not** yet say which rules no check can reach — that is
  [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md), and the coverage
  criterion is sequenced against it.
- [`examples/reference-deck.html`](../examples/reference-deck.html) — must pass.
- [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html) —
  must fail, per seeded defect, and `examples/README.md` carries the ledger of what was seeded.
- `tools/deck/` as it stands: `audit.py` (four stages, `render_data` / `render_verdicts` already
  split so a suite can ask the same code that gates the real deck), `contract.py`, `contrast.py`,
  `render.py`, and the three variant suites.
- [`EVALUATION.md`](../docs/EVALUATION.md) §1, §2, §6.3 — the gate runs **first** in the pipeline,
  and re-runs whole-deck **every** iteration, because a fix routinely reintroduces what an earlier
  one removed.
- [`pipeline.md`](../skills/htmldeck/references/pipeline.md) stages 2 and 6 — where the ledger is
  built and where the per-batch run already belongs.

**Where the gate actually stands — measured 2026-08-08, not estimated**

| | Count | How it was counted |
| :--- | ---: | :--- |
| Rules owned (`auto` + `render`) | **109** | `Check` column of every `DS-nnn` row |
| Emit a verdict on a live run | **41** | rule IDs in `audit.py` output, less the not-gated tail |
| Excused, with the reason printed | **4** | DS-033, DS-061, DS-065, DS-072 |
| **Silent — no verdict, no reason** | **64** | 35 `auto`, 29 `render` |
| Demonstrated failing on purpose | **14** | `deliverable_variants.py` 7/7 + `contract_variants.py` 7/7 |
| Content half | **0** | nothing under `tools/` reads a source document |

> **Every row above is superseded as of 2026-08-09 and none of it should be carried across.**
> [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) added two rules and
> corrected seven verdicts, so **rules owned is 111**, `Reach: yes` with `Check` in {`auto`,
> `render`} is **107**, and `audit.py` emits **39** verdicts rather than 40. **DS-080, DS-082,
> DS-111 and DS-143 moved from *claimed* to *silent*** — each had a verdict citing it that tested
> something else. Re-derive the table from the ruleset before planning; the counts are what this
> task's own criteria are written against, and a hand-carried one is indistinguishable from a
> correct one.

The 64 is the number that sizes this task, and it is **not** the "five rules with no implementation"
the 2026-08-07 log row recorded — that row counted the five [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md)
happened to trip over, not the jurisdiction. Reproduce the table before trusting it; it is a
count over a document and a program output, and both move.

**Known re-entries** — accepted costs, not oversights:

1. *The token-layer criterion* — "fails on a theme value hard-coded outside the token layer" cannot
   be built before [T-007](T-007-define-the-parametric-theme-layer.md) exists.
   [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) §3 took this deliberately:
   one criterion of roughly thirty-three, cheaper to re-enter for than to delay the whole gate.
2. *Motion and 3D* — [T-016](T-016-the-interaction-and-motion-layer.md) adds a second
   never-quiescent animation, so **DS-221**'s pin-motion-off-before-capture gains a second subject
   and the render gate gains one more thing to hold still before it measures.

**Acceptance criteria**

*Presentation — always run*
- [ ] Fails on any external reference
- [ ] Fails on banned terminology
- [ ] Fails on a `<section>` with no heading
- [ ] Checks contrast against WCAG AA
- [ ] Fails when the deck does not render glitch-free **from `file://`** in the target browser —
      the restricted-origin failures (ES modules, `fetch`, XHR, some WebGL texture paths) are the
      likeliest way a rich deck ships broken. See T-017
- [ ] Fails on a console error or unhandled rejection on load or during navigation
- [ ] Fails on a theme value hard-coded outside the token layer — see T-007
- [ ] *Opt-in only:* when the user has asked for a printable deck, fails if disclosure content is
      dropped or slides clip. Not run otherwise — printing is a mode, not a gate. **Owner,
      2026-08-07: the print path does earn its row, opt-in only** — inherited from
      [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md), which deferred the call
      here. The row asserts [R7](../docs/research/R7-printable-mode.md) §4's three rules — **which
      have IDs since [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md):
      DS-222** the print stylesheet asserts the view it wants including `display`, **DS-223** a
      slide stays a containing block for its own overlays, **DS-224** entrance animations are
      disabled for print — **and the page count**, because the measured failure is silent: thirteen
      blank pages, which nothing on the presentation list above can see. **The page count is
      `n` + 1 for `n` slides, and has been since
      [T-034](T-034-a-contents-page-for-the-printed-deck.md) added the contents page on
      2026-08-08** — `DESIGN-SYSTEM.md` §5.4 was amended by the owner to match, and the row now
      asserts **five** rules rather than three: **DS-225** the contents page is generated rather
      than authored and is placed *first* (last would re-break the trailing-page selector), and
      **DS-226** printed type has a floor in points rather than design units. The `n` + 1 count is
      what makes the off-by-one visible in either direction: `n` means the contents page never
      rendered, `n` + 2 means the trailing blank page is back
- [ ] Proven **failing** on each class before being trusted

*Content — run when source documents are supplied*
- [ ] Fails when a figure on a slide appears in no source
- [ ] Fails when a figure on a slide disagrees with the source it came from
- [ ] Fails when the same figure appears twice in the deck with different values
- [ ] Proven **failing** on each of those three before being trusted

*Coverage — the gate accounts for its own jurisdiction*
- [ ] **Every one of the 109 owned rules is in exactly one of three states at run time**: checked,
      excused with a written reason, or failing. A rule in none of them is itself a failure of the
      run — this is **L-36**'s second instance made impossible rather than found again
- [ ] The account is **derived from the ruleset when the gate runs**, never a list kept by hand. A
      hand-kept list is a stored copy of a derivable fact and drifts on the first amendment
      (**L-08**): DS-225 and DS-226 were added on 2026-08-08 and must appear in the account without
      anyone editing the gate
- [ ] The gate **fails on *nothing measured*** and never passes on it — the case
      [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) found, where stage 3
      reported `NO RESULT` and `render.py measure` emitted a tolerance verdict computed from 16
      values while the run stayed green
- [ ] Adding a rule to `DESIGN-SYSTEM.md` with no implementation makes the gate **say so**, and
      shipping one that silently does nothing is demonstrated to be impossible

*Honesty*
- [ ] The output states which half ran. "Presentation-only" is a legitimate result; reported as a
      clean pass, it is a false one
- [ ] The banned-terminology check **states that it is necessary and not sufficient** and never
      reports a clean pass as "reads as human-written" (**X-10**)
- [ ] The report names the dimensions the gate is structurally blind to — **S1, S2, S4, D1, D4** —
      so a clean run cannot be read as a good deck (**L-05**, **DS-191**)
- [ ] Ships with a self-test on a case whose answer is known, and the self-test is part of the
      deliverable, not a one-off

**Why the content half exists**

A deck can pass every presentation check and still put a wrong number in front of a board. The
evidence is in `docs/BRIEF.md` § *The critique pass*: a five-document set where every document
passed its own review, and the figure that reached the board's decision cell was wrong in eight
places. Nothing on this task's presentation list would have caught it.

**Open questions**

- ~~Does this task close all 64 silent rules, or ship the account and close a defined subset?~~
  **Answered 2026-08-08 by the owner: the account, then triage.** The coverage declaration is built
  first; the silent rules labelled `hard` are then closed, and **every rule left silent is excused in
  writing, one reason per rule, each excusal a candidate task rather than a shrug.** The gate ships
  honest about what it covers instead of dishonest about covering 109. What this rules out is
  closing all 64 now, which would front-load 29 `render` rules behind a browser harness before
  [T-002](T-002-build-mode-the-self-contained-deck-generator.md) exists to feed it any deck but the
  two in `examples/`. **The triage line is where this task's scope will drift**, so it is stated as
  a rule and not an intention: a rule leaves the silent list by being checked or by being excused in
  writing, and by no third route.
- ~~Where does "not machine-checkable" live, given that §11 never existed?~~ **Answered 2026-08-08 by the
  owner: per rule, in the ruleset** — a rule no check can reach says so in its own row, on
  [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md)'s precedent. **Raised as
  [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) rather than done here**, a
  finding not being repaired where it is found: it amends the ruleset, this task builds a check, and
  they are different deliverables. T-037 is `related`, **not** blocking — this §1 already assumes the
  field exists, so landing it later leaves this spec incomplete rather than wrong, which is
  [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md)'s test for whether an edge
  gates. What the coverage criterion inherits: until T-037 lands, *derived from the ruleset* has
  nothing to derive the excusals from, so that criterion is the one to sequence against it.
  The finding, kept because it is the reason T-037 exists: two of this task's log rows and part of
  its scope were written against `DESIGN-SYSTEM.md` **§11**, a list of 26 — later 33 — numbered
  conditions that named which ones no check could reach. **That section was never committed.**
  Established from git on 2026-08-08: the document has ended at §9 in all 13 commits of its life,
  including the one that closed [T-014](T-014-synthesise-research-into-the-design-system-reference.md)
  recording §11 as delivered. So *"conditions 22 and 30 are not machine-checkable"* has never pointed
  at anything, and the numbering is **not reconstructible** — DS-063, the one condition
  [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) translated by hand, is the 31st hard
  rule and not the 17th. `check` cannot see any of this: it validates links and paths, not section
  references. The carve-out survives **only as print statements inside `audit.py`**.
- ~~Does the opt-in print row become an automated check, or stay a human procedure?~~ **Answered
  2026-08-08 by the owner: automate the page count, and only that.** `print_variants.py` builds the
  three variants and self-tests, but it emits **no DS-222–226 verdict**, and the `n` + 1 count is
  asserted by a person printing and looking. The count is the silent failure the criterion was
  written for — thirteen blank pages, which nothing on the presentation list can see — and it is
  cheap: headless print-to-PDF, then enough PDF reading to count pages, and no more. **What stays
  human is the part a person is better at**: *"disclosure content dropped, slides clip"* stays with
  the print that CLAUDE.md rule 6 requires regardless, so the gate gains a check without the project
  gaining a claim it cannot support.
- ~~Is the check a separate command, or always part of build?~~ **Answered 2026-08-07 by the owner:
  both — one library, two entry points.** Called per batch and whole-deck by the pipeline
  ([`pipeline.md`](../skills/htmldeck/references/pipeline.md) stage 6 already requires the per-batch
  run), **and** exposed as a standalone command that takes any HTML file. The standalone half is not
  a convenience: the *proven failing* criteria below run against
  [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html),
  a deck this plugin did not build, and [T-004](T-004-critique-mode-blunt-section-by-section-review.md)
  reviews decks it did not build either. `tools/deck/audit.py` is already both shapes.
- ~~Does the content half need the sources parsed, or is "the user pastes them in" enough?~~
  **Answered 2026-08-07 by the owner: read the files at the paths supplied in question 2.** That is
  where [`pipeline.md`](../skills/htmldeck/references/pipeline.md) stage 2 already builds the figure
  ledger — every figure, its origin, every place it is reused. Reconciliation needs an **origin per
  figure**, and a pasted blob has no path, so *"appears in no source"* degrades to string matching —
  which is the class of defect the content half exists to catch. Pasting stays legitimate as a
  fallback for a source that is not a file; it is not the contract.
- **Inherited and answered:** the print row, from
  [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) — see the opt-in criterion
  above.

## 2. Plan

**Re-derived 2026-08-09, before planning, as the note above the table requires.** The jurisdiction is
**111** rules (66 `auto`, 45 `render`), **85** of them `hard`. **44** are cited by a verdict today;
**4** are excused in the ruleset by their `Reach` value; **64 are silent — 44 `hard` and 20
`default`.** The 64 is the same number the 2026-08-08 row recorded and it is not the same 64: four
rules left the checked set when T-038 removed verdicts that cited them, and two arrived with the
rules it added. **DS-072 is checked *and* excused in the ruleset**, which is a contradiction this
task resolves rather than inherits.

The answered question sets the order — **the account first, then triage** — so steps 1–3 make the
gate honest about a jurisdiction it barely covers, and only then does step 4 start closing it.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | Parse the ruleset into records — id, label, `Check`, `Reach`, reason — reading `Reach` as a leading token with free text after it. Self-test on known rows, on the `—`-is-a-value trap, and on duplicate IDs | `tools/deck/ruleset.py` |
| 2 | Make the three verdict producers return rows rather than only print them, and **give `contrast.py`'s failures a rule ID** — §7 says its criterion numbers *are* the IDs, so they cite **1.4.3** instead of a colour-pair label | `audit.py`, `contrast.py` |
| 3 | Build the gate. It composes the stages, **derives the account at run time** from the ruleset, and fails when any owned rule is in none of the three states, when a verdict measured nothing, and when a deferral names a rule that is actually checked — a stale excusal is the same defect as a missing one | `tools/deck/check.py` |
| 4 | Add the load-time error capture the criteria ask for: a hook injected **in `<head>`**, before the deck's own script, catching `error`, `unhandledrejection` and `console.error` on load and across navigation. A probe appended to `</body>` cannot see a load-time failure, which is the `file://` restricted-origin class the criterion names | `check.py` probe |
| 5 | **Triage the 44 silent `hard` rules, one at a time.** Build the check where the rule's own subject is decidable from the file or the render; **excuse it in writing where it is not**, naming what would close it. T-038's discriminator governs every new verdict: the thing measured is the thing cited, or it does not ship | ~20 new verdicts, and a deferral register |
| 6 | The 20 silent `default` rules are **excused in writing**, not checked — the answered question closes `hard` first, and a rule leaves the silent list by being checked or excused and by no third route | deferral register |
| 7 | Write a source set for the reference deck's own topic, fresh and neutral, so the content half has a real case rather than a fixture that agrees with itself by construction | `examples/sources/` |
| 8 | The content half: extract every figure with its label and slide, emit the **Figure · Value · Origin · Used on** ledger `artifacts.md` specifies, and run the three reconciliation checks over it | `tools/deck/content.py` |
| 9 | Prove the content half fails on each of its three classes, by the method the other two suites use — seed one break at a time into a copy, assert the edit matched, require the gate to object | `tools/deck/content_variants.py` |
| 10 | The print page count: headless print-to-PDF, count pages, assert **`n` + 1**. Opt-in, and it emits no DS-222–226 verdict — the owner's answer automates the count and only the count | `tools/deck/printpages.py` |
| 11 | Prove the new presentation checks fail, extending the existing suites rather than starting a third | `deliverable_variants.py` and a new static suite |
| 12 | The report: human text plus **JSON for [T-004](T-004-critique-mode-blunt-section-by-section-review.md)**, carrying which half ran, the account, the ledger, and the blind-dimension statement | `check.py --json` |
| 13 | Retire `audit.py`'s *"Not gated here, and why"* tail, which the ruleset's `Reach` column now supersedes and contradicts | `contract.py` |
| 14 | Point the docs at the gate — `pipeline.md` stage 6, `EVALUATION.md` §2, and the counts both carry | docs |

## 3. Implement

### Where the gate stands now — measured 2026-08-09

| | Before | After | How it was counted |
| :--- | ---: | ---: | :--- |
| Rules owned (`auto` + `render`) | 111 | **111** | `ruleset.py`, from the `Check` column |
| Checked — a verdict naming that rule | 44 | **79** | rule IDs in `check.py`'s row list |
| Excused **in the ruleset** by `Reach` | 4 | **4** | DS-042, DS-072, DS-210, DS-211 |
| Excused **in the gate**, in writing | 0 | **29** | `check.DEFERRED`, one reason each |
| **Silent — no verdict, no reason** | **64** | **0** | owned − checked − excused |
| Demonstrated failing on purpose | 14 | **34** | four suites: 7 + 7 + 3 + 17 |
| Content half | 0 | **3 checks + the ledger** | `content.py` |

**The 64 did not become 64 checks, and it was never going to.** The owner's answer was *the account,
then triage*: 33 rules gained a real check, and the other 31 gained a written reason and a named
condition that would close it. The distinction the account enforces is that **there is no third
state** — a rule cannot be quietly absent, because absence is what fails the run.

### Decisions & assumptions

- **The account is checked in both directions — 2026-08-09.** A rule nothing decided fails the run,
  and so does an excusal for a rule that **is** decided. Only the first is the famous failure; the
  second is the one that rots quietly, because a stale note reads exactly like a live one. The
  self-test seeds both.
- **A rule leaves the silent list by being checked or excused, and the excusal has to be an
  argument — 2026-08-09.** `check.py`'s self-test refuses a reason under 40 characters, and it fired
  during the build: three print rules had been excused with *"See DS-222 — the same ruling"*, which
  is a cross-reference and not a reason. All three were written out.
- **Where a rule and the reference deck disagreed, neither was assumed right — 2026-08-09.** Two
  cases, both excused with the argument on both sides and handed to the owner: **DS-045**, whose two
  readings disagree about a pattern twelve slides use and this gate's own DS-203 check depends on;
  and **DS-219**, which says *never* while its stated reason says *no neutral does both* — and the
  deck's marks are the accent, which clears both criteria. Deciding either unilaterally would have
  been a ruleset amendment made by whoever happened to be writing a check.
- **Where a rule's subject is a reading of the content, the check was not built — 2026-08-09.**
  DS-041, DS-101, DS-117, DS-120, DS-149, DS-209, DS-026. Each is excused with what it would take,
  and in four of them the **measurement exists and is reported** — the missing part is the
  threshold, and inventing one is how a gate starts lying (**L-38**, and T-038's whole subject).
- **The content checks carry their own IDs, `FIG-1` to `FIG-3` — 2026-08-09.** DS-102 is the rule in
  the neighbourhood and it is `judge`: a program can compare a slide's number to a file's, and it
  cannot decide whether a figure is fabricated. Citing DS-102 would have been T-038's defect
  re-committed in a new file, three days after it was swept out of the old one.
- **The sources are written, not generated — 2026-08-09.** A source set derived from the deck agrees
  with it by construction and proves nothing. `examples/sources/` is three documents written as the
  model the deck's figures are outputs of, and the first run against them found a real mismatch in
  the *reader*, not the deck: sources were being read line by line, so a wrapped `16\nstations` was
  not in the file at all.
- **`audit.py`'s "Not gated here, and why" tail is retired — 2026-08-09.** It listed four rules and
  only one of them was a reachability statement; the rest were *checked in another stage*, which is
  a fact about how the gate is arranged today. DS-065 in particular is no longer unchecked at all —
  T-021 reworded the rule so it could be false, and the check that rewording made possible is built.
- **Three defects in the reference deck were found and NOT fixed here — 2026-08-09.** §1 puts fixing
  out, and the reason is restated there as the boundary most likely to erode. They went to
  [T-040](T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md), which fixed them.

### Outputs produced

- [`tools/deck/check.py`](../tools/deck/check.py) — the gate, the account, the excusal register, the
  JSON report
- [`tools/deck/ruleset.py`](../tools/deck/ruleset.py) — the ruleset as data, so no list is kept by
  hand
- [`tools/deck/content.py`](../tools/deck/content.py) — the figure ledger and its three
  reconciliations
- [`tools/deck/printpages.py`](../tools/deck/printpages.py) — the printed page count
- [`tools/deck/static_variants.py`](../tools/deck/static_variants.py) ·
  [`tools/deck/content_variants.py`](../tools/deck/content_variants.py) — 18 more seeded defects
- [`tools/deck/audit.py`](../tools/deck/audit.py) — 22 static and 11 rendered verdicts added
- [`tools/deck/contrast.py`](../tools/deck/contrast.py) — verdicts citing §7's criterion numbers, and
  DS-013 and DS-027
- [`examples/sources/`](../examples/sources/README.md) — the source set the content half reconciles
  against
- [`docs/EVALUATION.md`](../docs/EVALUATION.md) ·
  [`skills/htmldeck/references/pipeline.md`](../skills/htmldeck/references/pipeline.md) — both now
  point at the command

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Fails on any external reference | **met** | DS-001, and DS-002 for the CDN case; `cdn-reference` variant caught |
| Fails on banned terminology | **met** | DS-106, unchanged from before this task |
| Fails on a `<section>` with no heading | **met, in substance** | DS-080 fails a slide that is not a `<section>` (`slide-is-not-a-section` caught) and DS-091 decides its headline. *No heading at all* is the intersection and no separate row asserts it |
| Checks contrast against WCAG AA | **met** | 1.4.3 and 1.4.11 now cite the criterion numbers rather than a colour-pair label, in both themes, with the evaluated-pair count in the verdict |
| Fails when the deck does not render glitch-free from `file://` | **met** | DS-005 fails a deck that calls `fetch`, XHR or a dynamic import, which is the restricted-origin class; `script-reads-a-file` caught. DS-006 covers the module-specifier case |
| Fails on a console error or unhandled rejection | **not met** | The load-time hook was planned as step 4 and is **not built**. `render_data` returning nothing already fails the run, so a deck that throws hard is caught; one that logs an error and carries on is not. The smallest remaining gap, and named |
| Fails on a theme value hard-coded outside the token layer | **met, for colour** | DS-010; `colour-outside-the-tokens` caught. The rule's wider subject — any value that could differ between themes — needs [T-007](T-007-define-the-parametric-theme-layer.md), which §1 named as a known re-entry |
| *Opt-in:* the print row, and the page count | **met** | `--print-pages`: 13 declared, 13 counted, wanted 13. DS-222–226 emit no verdict, per the owner's ruling, and are excused in writing |
| Proven failing on each class before being trusted | **met** | 32 seeded defects across four suites, all caught. **Two were missed on the first run and both were real gaps** — DS-141 could not see a duration held in a token, and DS-092's sentence splitter cut `$5.6M` in half |
| Fails when a figure appears in no source | **met** | FIG-1; `figure-in-no-source` caught |
| Fails when a figure disagrees with its source | **met** | FIG-2; `figure-disagrees-with-source` caught |
| Fails when one figure has two values in the deck | **met, with a stated limit** | FIG-3; `same-figure-two-values` caught. **Restricted to different slides**, because A-07 draws the same diagram twice with one edge changed — a before/after slide is one subject with two values by design |
| Proven failing on each of those three | **met** | `content_variants.py`, 3 of 3 |
| Every owned rule is checked, excused in writing, or failing | **met** | `SILENT 0` of 111. The run fails if that number is not zero |
| The account is derived from the ruleset at run time | **met** | `ruleset.py` parses `DESIGN-SYSTEM.md` on every run; DS-227 and DS-228, added yesterday, appear in the account with nobody having edited the gate |
| The gate fails on *nothing measured* | **met** | A `NO RESULT` render is a `FAIL` row, not a skipped stage; DS-130 now fails on a null; every count-based verdict carries its denominator, so `0 of 0` is visible |
| Adding a rule with no implementation makes the gate say so | **met** | It lands in `silent` and the run goes red. Demonstrated in reverse throughout the build: the count fell 64 → 2 → 0 as checks landed |
| The output states which half ran | **met** | `content half: NOT RUN — no sources supplied. A presentation-only run is a legitimate result and is not a clean one`, and the same for the page count |
| The banned-terminology check says it is not sufficient | **met** | The closing block names DS-106 as the sharpest case and DS-107 as the reason |
| The report names the blind dimensions | **met** | S1, S2, S4, D1, D4, on every run |
| Ships with a self-test that is part of the deliverable | **met** | Five self-tests run before any verdict: `ruleset`, `render`, `contrast`, `contract`, `content`, plus the gate's own. **The gate's fired during the build** and refused to run over a three-word excusal |
| The report format T-004 consumes | **met** | `--json`: rows, the full account, the ledger, the notes, and the blind list. 88 rows on the reference deck |

**Child fix tasks raised**
- [T-040](T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md) — **done.** The three
  defects the new checks found in the reference deck: two sentences over DS-092's 20-word cap, and
  a sprite icon nothing used.

**The two questions raised here were settled the same day — 2026-08-09**

The owner delegated both. Each was decided **for the reason the rule already gives**, which is the
only ground available when a rule and a conforming deck disagree: the wording moves to match the
argument, not the other way round. Both rules gained a real check, so the account went **77 → 79
checked and 31 → 29 excused**, and the rationale for each is in
[`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) §5.7.

- **DS-045 — the narrow reading.** *Never style the bare `b` element selector.* A rule on the
  element reaches every `<b>` in the deck; a scoped one cannot leak, and the scope is the fix the
  harm describes. `.bottom-line b` stays. Checked, and `styled-bare-b` proves it fails.
- **DS-219 — the clause, with two numbers rather than an exemption.** A label may sit on a mark when
  that mark's own pair is **measured**: ≥ 3:1 against the ground and ≥ 4.5:1 under the text. The
  deck's three labelled accent bars measure **6.5:1 on both**, so the blanket ban was forbidding
  something its own mechanism permits. **The amended rule is stricter in the direction the ban never
  looked**: `mark-too-pale-to-clear-the-ground` seeds a washed-out bar with a dark, perfectly
  legible label — DS-215 passes, the slide looks fine, and only DS-219 objects.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-09 | (no change) | **Both open questions settled, by the owner's delegation, and both rules gained a check rather than an exemption.** DS-045 takes the narrow reading and DS-219 gains the two measurements its own reason implies. **Neither was decided on taste:** a rule and a conforming deck disagreeing means the wording has drifted from the argument, and the argument is what survives. DS-219 is now *stricter* than the ban it replaced - it catches a mark too pale to clear the ground, which *never set text on a mark* never looked at because it assumed nobody would try. Account: **79 checked, 29 excused, 0 silent**, and the seeded-defect count is 34. |
| 2026-08-09 | → done | **Silent went from 64 to 0, and that is the deliverable — not the 33 new checks.** 77 of 111 rules are decided and the other 34 are named with a reason and a closing condition, derived from the ruleset every run. **The self-tests earned their place twice on the way:** the gate refused to run over an excusal written as *"See DS-222"* rather than as an argument, and the new variant suite caught **two of its own checks unable to see their own seeded defect** — DS-141 could not read a duration held in a token, which is where DS-033 requires every duration to live, and DS-092's sentence splitter cut `$5.6M` in half so a 28-word sentence read as three short ones. Both were green before the suite existed. **One criterion is not met and is named rather than reworded:** the console-error hook was planned and not built, so a deck that logs an error and carries on passes. **Three genuine defects in the reference deck** went to [T-040](T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md) rather than being fixed here. **Two ruleset questions are the owner's** — DS-045's two readings and DS-219's *never* against its own reason — and both are excused with the argument on each side rather than settled by whoever was writing a check. |
| 2026-08-09 | → in_progress | Planned in 14 steps after re-deriving the jurisdiction, which the note above §2 required and which mattered: the 64 silent rules are **not the same 64** the 2026-08-08 row counted. Four left the checked set when T-038 removed verdicts citing rules they did not test, and two arrived with the rules it added. |
| 2026-08-09 | (no change) | **[T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) closed, and it moved the numbers this task plans against — re-derive, do not carry them.** Two rules were added, **DS-227** (closed at load) and **DS-228** (one panel open at a time), so **rules owned is 111** and the count to account for is **107**, not 105. Yesterday's row said *plan against 105*; that number is one day old and already superseded, which is the behaviour the criterion's *derived from the ruleset* wording exists to survive. **The gate's claimed coverage shrank as well as grew.** T-038 swept all 40 verdicts and found seven wrong; four rules — **DS-080, DS-082, DS-111, DS-143** — had a verdict citing them that tested something else, and now have none. All four keep `Reach: yes`, so **the coverage declaration owes each of them a checked-or-excused line**, and this task inherits four gaps that were previously invisible because they read as covered. **DS-137 and DS-161 are no longer a trap for the coverage count** — they are `judge`, the gate has stopped claiming them, and no naive count can score them as covered any more. The *"Not gated here, and why"* tail is still this task's to retire, and `contrast.py`'s failures still carry a pair label rather than §7's criterion number, which is the same defect one file over. |
| 2026-08-09 | (no change) | **[T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) closed, and the one coupling this task was sequenced against is discharged.** The *derived from the ruleset* coverage criterion now has something to derive from: [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) carries a **`Reach`** column on all **158** rule rows, and a program that has never heard of an individual rule can compute **the number this task must account for: 105** — `Reach: yes` with `Check` in {`auto`, `render`}. **Plan against 105, not 109.** The other four of the 109 are excused *in the ruleset, with their reasons*, and are not this task's to close: DS-042 `never`, DS-072, DS-210 and DS-211 `off-gate`. **Three consequences worth having before planning.** (1) The gate's own excuse list is now redundant and contradicted — `audit.py`'s *"Not gated here, and why"* tail conflates *checked in another stage* with *cannot be checked*, which is why only one of its four entries moved to the ruleset; making the gate derive its account from `Reach` is what retires it, and that is this task's work. (2) `Reach` deliberately says **nothing about which part of the gate checks a rule** — a rule decided statically rather than at render is still `yes` — so the coverage account must not encode stage, or the ruleset goes stale on the next refactor. (3) [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) is open against a defect this task will otherwise inherit: the gate emits verdicts for two `judge` rules, one of them under an ID whose rule it does not test, so a naive coverage count would score them as covered. `related` gains T-037 and T-038. |
| 2026-08-08 | (no change) | **Correction, from git rather than from reading: §11 was never committed.** Yesterday's row and this task's §1 both said [T-022](T-022-split-the-design-system-from-its-rationale.md) replaced the numbered conditions with `DS-nnn` IDs and §11 went with the renumbering. That was wrong. `docs/DESIGN-SYSTEM.md` has ended at **§9 in all 13 commits of its life**, created that way by the very commit that closed [T-014](T-014-synthesise-research-into-the-design-system-reference.md) recording *"§11 — 26 numbered conditions"* as **met**. Nothing was deleted; the section was never written. The practical consequence for this task is that *"conditions 22 and 30 are not machine-checkable"* was never recoverable, and now provably is not: had the conditions been the hard rules in document order, condition 17 would be the 17th, and DS-063 — the one mapping [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) made by hand — is the **31st**. [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) writes the two off explicitly rather than leaving a search for someone to re-run. **Two counts confirmed while checking this**, because they are close enough to be mistaken for each other: this task owns **109** `auto`+`render` rules, and there are also **109** rules labelled `hard` — different sets, overlapping in 84. The triage decision's *"close the silent rules labelled `hard`"* means that 84, not the 109. |
| 2026-08-08 | → specified | **Three questions answered by the owner, and §1 is accepted.** *(1) The account, then triage* — the coverage declaration is built first, the silent `hard` rules are closed, and everything still silent is **excused in writing, one reason per rule**, each excusal a candidate task. A rule leaves the silent list by being checked or by being excused, and by no third route; that line is where this task's scope will drift, so it is written as a rule. Closing all 64 now was rejected as front-loading 29 `render` rules behind a browser harness before [T-002](T-002-build-mode-the-self-contained-deck-generator.md) can feed it anything but the two decks in `examples/`. *(2) The unreachable-rule carve-out belongs per rule in the ruleset* — **raised as [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md), not fixed here**, because it amends the ruleset while this task builds a check. `related`, not blocking: this §1 assumes the field, so landing T-037 later leaves the spec incomplete rather than wrong. The one coupling to sequence against it is the *derived from the ruleset* criterion, which until then has no excusals to derive. *(3) The print row automates the page count and nothing else* — the `n` + 1 count is the silent failure (thirteen blank pages, invisible to every presentation check) and is cheap; *disclosure dropped, slides clip* stays with the human print CLAUDE.md rule 6 requires anyway, so the gate gains a check without the project gaining a claim it cannot support. |
| 2026-08-08 | (no change) | **`specify` worked: scope, inputs and a coverage account added, and the gate's real position measured rather than described.** §1 had no scope boundary and no input list at all, which is why it could grow in both directions across four log rows without anything registering. Both are now written, with *fixing* and the 43 `judge` rules explicitly out. **The measurement is the finding: this task owns 109 rules (65 `auto`, 44 `render`); 41 emit a verdict, 4 are excused with the reason printed, and 64 are silent — no verdict and no stated reason.** The 2026-08-07 row below records "five rules with no implementation", which counted what [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) tripped over, not the jurisdiction; the row stands as written and this one supersedes its number. Four **coverage** criteria added, turning L-36 from a defect to be found again into one the gate cannot ship — every owned rule checked, excused in writing, or failing, derived from the ruleset at run time rather than from a hand-kept list (**L-08**). Three criteria added under *Honesty* for X-10 and the five blind dimensions. **A stale anchor found and not silently repaired:** two rows below cite `DESIGN-SYSTEM.md` **§11**, the 26- then 33-condition list this task was written to consume — [T-022](T-022-split-the-design-system-from-its-rationale.md) replaced it with `DS-nnn` IDs and **the document now ends at §9**, so "conditions 22 and 30 are not machine-checkable" points at nothing and the carve-out survives only as print statements in `audit.py`. `check` validates links and paths, not section references, which is how it went unseen. Raised as an open question with a recommendation rather than fixed here, because where that carve-out lives is a ruleset decision. **Three open questions for the owner, each with a recommendation; status stays `proposed` until they are answered.** |
| 2026-08-08 | (no change) | **The print row's three rules now have IDs, and its page count has an expiry date.** [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) adopted the paginated stylesheet in the reference deck and carried R7 §4's rules into the ruleset as **DS-222, DS-223 and DS-224** — the criterion described them in prose, which was correct when nothing else named them and is now a second copy. It also added three `render` rules to this task's scope; the counts in the 2026-08-06 row below are historical and were right when written. **The page count is the part to watch**: it is `n` pages for `n` slides today, and [T-034](T-034-a-contents-page-for-the-printed-deck.md) would make it `n` + 1 by putting a generated contents page in front — a printed page that is not a slide, which is exactly the kind of change a gate asserting a count discovers by failing. `related` gains T-032 and T-034. |
| 2026-08-07 | (no change) | **Three questions answered by the owner, and one of them was inherited.** *Both entry points* — one library, called per batch and whole-deck by the pipeline and exposed as a standalone command, because two of this task's own criteria and all of [T-004](T-004-critique-mode-blunt-section-by-section-review.md) run against decks this plugin did not build. *Sources are read from their paths*, at pipeline stage 2 where the figure ledger is built; pasting is the fallback, not the contract. *The print row is earned, opt-in only* — [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) closed having deliberately deferred that call here, and it is now taken: [R7](../docs/research/R7-printable-mode.md) §4's three rules plus the page count. **Scope moved in both directions today.** It grew by the print row and by the figure ledger, which [T-004](T-004-critique-mode-blunt-section-by-section-review.md)'s counting-pass answer routes here — this task counts, that one prioritises, so the ledger has to be an output this check *emits*, not an internal. It did not grow by the fix loop: fixes stay with the build step. **`related` gains [T-004](T-004-critique-mode-blunt-section-by-section-review.md)**, written on both files: that mode consumes this check's report and its ledger, an edge [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) used to order the two and neither file recorded. |
| 2026-08-07 | (no change) | **[T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) closed and handed this task a second variants suite and a refactor it should build on.** `audit.py` now splits `render_data(deck)` (the browser half) from `render_verdicts(data)` (pure, no browser), so a suite can seed a break, take one measurement, and ask **the same code that gates the real deck** rather than a copy of it — that split is the shape this task's gate wants, and it is already done. [`tools/deck/deliverable_variants.py`](../tools/deck/deliverable_variants.py) covers DS-202/203/205/216/217, 7 of 7 caught; with `contract_variants.py` that is **14 rules demonstrated failing on purpose**, against 36 checks still never shown to fail individually. Two findings bear directly on this task's criteria: **five rules labelled `auto` and `render` had no implementation at all** (L-36's second instance), so *"the gate checks what it says it checks"* needs to be a criterion here and not an assumption; and **the gate was driving the deck through chrome a design rule required deleting**, which made stage 3 report `NO RESULT` and made `render.py measure` emit a tolerance verdict computed from 16 values. A gate must fail on *nothing measured*, never pass on it. |
| 2026-08-07 | (no change) | **[T-021](T-021-the-reflow-view-and-the-resolution-contract.md) closed and handed this task the resolution-contract checks built rather than specified**, so what remains here is absorption, not authorship — the pattern [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) §4 flagged as **L-32** for four tasks at once. What arrived: [`tools/deck/contract.py`](../tools/deck/contract.py) gating twelve of the fourteen §2.4 / §2.5 rules, stage 4 of `audit.py` (33 checks → 43), and [`tools/deck/contract_variants.py`](../tools/deck/contract_variants.py). **The variants file is the part worth reading before writing this task's criteria**: it broke each rule on purpose and caught **three of the new checks measuring nothing**, which is a stronger form of this task's own *"fails on a seeded-defect deck"* criterion than a fixture alone gives. Also relevant to the criterion about theme values: DS-065 was found **unenforceable as written** and reworded, so a check for it is not owed. |
| 2026-08-07 | (no change) | **Unblocked by [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) — the `blocked_by` on T-002 was false.** This check runs on an HTML file, and two exist: [`examples/reference-deck.html`](../examples/reference-deck.html) and [`examples/reference-deck-seeded-defects.html`](../examples/reference-deck-seeded-defects.html), the second of which is precisely the *proven **failing** on each class* fixture the criteria above demand. `tools/deck/` already runs 30 checks against both. **Nothing here waits on build mode**, and the edge was gating a task already a third built — the exact case the audit was raised to find. T-002 becomes `related`, alongside T-018 (whether the print path earns a row) and T-021 (which hands conditions 13–19 over). |
| 2026-08-06 | (no change) | **A working measurement layer now exists**, built by [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) and committed as `tools/deck/audit.py`, `tools/deck/render.py` and `tools/deck/contrast.py`. It runs 30 checks against `DS-nnn` IDs in real Chrome, offline, and it found six defects in the reference deck that looking at it had not — including type below DS-035's own floor and a headline over DS-091's word cap. **This task now hardens and completes that layer rather than starting one**; the gap is L-04 self-tests on the render path, the `judge` boundary, and a report format T-004 can consume. Two findings constrain it: an infinite animation makes a headless capture non-deterministic unless motion is pinned off, and content spilling a grid track is invisible to element-bounds checks (**L-26**). |
| 2026-08-04 | → proposed | Seeded from `docs/BRIEF.md` when the project folder was prepared. |
| 2026-08-05 | (no change) | Acceptance criteria split into presentation and content halves, plus an honesty criterion, after a source-document audit showed the presentation list cannot catch a wrong figure. Evidence in `docs/BRIEF.md`. |
| 2026-08-06 | (no change) | Added disclosure-layer and token-layer criteria after the owner identified progressive disclosure as their signature technique and chose a parametric single theme. |
| 2026-08-06 | (no change) | Corrected: print demoted from hard gate to opt-in mode, and the keyboard/hover criteria dropped, after the owner ruled that printing overrides nothing and that rich interaction is wanted. Replaced by `file://` render and console-error gates. |
| 2026-08-06 | (no change) | Owner answered BRIEF open question 6: **the check has two halves.** The content half reconciles every figure against the supplied sources and against itself; the presentation half runs regardless. When sources are absent the check runs presentation-only and **says which half it ran** — that requirement is now load-bearing rather than advisory. Also: "every `<section>` has a heading" becomes semantic — the heading must be a claim, not a label (R2 P-01) — and R2 §9 gives the accessibility floor as testable numbers. |
| 2026-08-06 | (no change) | **T-014 closed.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) **§11 states the hard rules as 26 numbered testable conditions**, written for this task to consume without reading the whole reference. Five corpus rules were deferred here as mechanics: K2, K3, K4, K6, K7. **Two constraints on what this check may claim:** X-10 — the banned-terminology check is necessary and not sufficient and must say so, never reporting a clean pass as "reads as human-written"; and conditions 15 and 23 are not machine-checkable, listed so they are not silently dropped. *(**§11 never existed** — see the 2026-08-08 correction row above. Left standing as what was believed; the live equivalent is the `Reach` column.)* |
| 2026-08-06 | (no change) | **Seven new conditions — [`DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) §11 items 13–19, the resolution contract.** Renumbering note: the behavioural half is now 20–30 and the content half 31–33; the two not machine-checkable are **22 and 30**. **Condition 17 is the one to build first** — render the deck at 3840×2000 and at 1280×634 and diff up to a uniform scale factor. It is cheap and it catches the entire accidental-breakpoint class in one pass, which is the defect that produced "broken slides on my own monitor". Also new: a design-unit type floor (nothing under 18, body ≥ 24) that is measured in stage units, not rendered pixels. *(**§11 never existed** — see the 2026-08-08 correction row above. The seven conditions are real and shipped as DS-060 to DS-076; only the numbering was imaginary.)* |
| 2026-08-06 | (no change) | **Scope is now enumerable rather than described.** [`docs/DESIGN-SYSTEM.md`](../docs/DESIGN-SYSTEM.md) gives every rule a `DS-nnn` ID and a `Check` value: **this task owns the 59 `auto` rules and the 32 `render` rules**; the 36 `judge` rules belong to the evaluator. [`docs/EVALUATION.md`](../docs/EVALUATION.md) §1 fixes the contract: **`hard` rules are gates and are never scored**, so this check reports pass/fail per rule ID and never contributes to a total. §2 puts it first in the pipeline, because a judgement pass on a deck with external references is wasted. §6.3 adds a requirement this task would not otherwise have: the auto gate **re-runs on the whole deck every iteration**, since a fix routinely reintroduces what an earlier one removed. |
