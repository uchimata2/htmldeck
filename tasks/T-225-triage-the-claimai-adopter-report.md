---
id: T-225
title: Triage the ClaimAI adopter report and decide each of its twenty-seven findings
type: analysis
status: done
phase: review
parent: null
blocked_by: []
related: [T-063]
work_package: PH3
owner: the project owner
business_value: high
effort: m
created: 2026-08-28
updated: 2026-08-29
deliverables: []
---

# T-225 — Triage the ClaimAI adopter report and decide each of its twenty-seven findings

## 1. Specify

**Outcome**
Every finding in [`docs/adopter-reports/claimai/`](../docs/adopter-reports/claimai/README.md) has a
decision against it — accepted and raised as a fix, accepted and deferred, or rejected with a reason.
Nothing in the set is left unjudged. This task produces the judgement; the fixes it accepts become
tasks of their own.

**Where it came from**

An outside project used htmldeck to build a twenty-five slide executive board presentation, under a
deadline, as the deliverable of a formal training exam. It ran from 2026-08-23 to 2026-08-28, kept 84
task records, and shipped. Twenty-seven findings came out of that work and were staged as they were
found rather than written up afterwards.

**The deck was presented and judged good.** That is the frame for the whole set: these are the places
where a tool that produced a good result made reaching it harder than it needed to be. The report's
own covering note puts the goal as *not to limit but to support such results*.

**Nobody is waiting for an answer.** The project that produced this is closed. There is no thread, no
deadline and no reply expected — the set is a one-way hand-over, written to stand alone. Take what is
useful and discard the rest, including any record judged wrong.

**What makes this set worth the time**

- **It is evidence, not opinion.** Every record carries the command and its output, the source line,
  or the verdict the tool itself printed. The staging project's standing rule was that a claim about
  a tool's behaviour without one is a guess.
- **It is not one-sided.** Six rules are named as having caught real faults — `DS-091`, `DS-143`,
  `DS-215`, `DS-236`, `DS-239` and `DS-202` — inside the records that criticise others. `022` says
  plainly that `DS-244` improved the slide three times while being wrong.
- **It reports what the gate cannot see.** The four records with the highest value here are the ones
  where `check` was green and something was wrong anyway: `025`, `026`, `016` and `017`.

**Four things worth knowing before reading**

1. **The deck fails four rules permanently** — `DS-110`, `DS-217`, `DS-218`, `DS-219` — and has since
   the build. An author who cannot ever reach zero stops reading the gate, and that is the cost
   behind several of these records rather than the rules themselves.
   [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md) is the
   sharpest of them: `DS-219` is unsatisfiable for a whole class of correct diagrams, and
   `docs/DESIGN-RATIONALE.md` §5.7 already records this repository's own doubt about the rule.
2. **`DS-244` is reported twice, deliberately, from opposite directions.**
   [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md)
   says it is too blind;
   [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) says it is too
   strict. Read together they say the rule tests proximity where it means obstruction — which neither
   record says alone. **Triage them as a pair, not separately.**
3. **One finding is a note about this repository's own examples.**
   [`018`](../docs/adopter-reports/claimai/018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md)
   shows `portfolio-review` passing `DS-218` with `0 looping` — the rule never fires, so the example
   models a control placement that is safe only for want of a subject. The adopter's first reading was
   that the example contradicted the rule, and running the gate on the example is what corrected it.
   **An example that satisfies a rule vacuously is worth finding elsewhere in the set of four.**
4. **`density.py write` is currently refused outright by that project's launcher**, because it
   corrupts self-closing SVG tags —
   [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md).
   It is the tool `DS-239` makes necessary, so the rule and the broken writer compound: see
   [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md).
   That pair is the one place in the set where a rule and a defect together produce an adopter
   editing generated markup by hand.

**Scope**
- In: all twenty-seven records; one decision each; a fix task for every accepted finding.
- Out: fixing anything here. A triage that turns into an implementation stops being a triage, and
  three of these records touch rules rather than code.
- Out: replying to the adopter. There is no channel and none is expected.

**Inputs**
- [`docs/adopter-reports/claimai/README.md`](../docs/adopter-reports/claimai/README.md) — the covering
  note, the index and four suggested themes
- The twenty-seven records beside it
- `docs/DESIGN-SYSTEM.md` and `docs/DESIGN-RATIONALE.md` — the rules under discussion, and §5.7, which
  already doubts `DS-219`

**Acceptance criteria**
- [ ] Every one of the twenty-seven records carries a decision: accepted and raised, accepted and deferred, or rejected with a reason
- [ ] `013` and `022` are decided together, as one question about what `DS-244` is testing
- [ ] Each accepted finding names the task that will do it
- [ ] Each rejected finding says why, in a sentence an adopter would accept — the records are evidence-led, so a rejection needs a reason of the same kind
- [ ] The four permanently-failing rules are looked at as a group, and the outcome says whether a deck failing four rules by design is acceptable
- [ ] `Version seen` is checked before any record is actioned: fourteen were stamped rather than re-run, so a finding may already be fixed

**Open questions**
- None for the adopter — the report is closed and expects nothing. Every open question here is this
  repository's own.

## 2. Plan

Four passes, in this order, and the order is the point.

| # | Step | Output |
| :-- | :--- | :--- |
| 1 | **Verify before actioning.** `Version seen` is `0.6.0` on all twenty-seven and fourteen were stamped rather than re-run, so re-run the checkable ones against this tree | section 3's verification table |
| 2 | **Look for a home before raising one.** The pre-release audit closed its triage the same day; a record whose class already has a task is merged into it | three merges |
| 3 | Decide each remaining record — accepted and raised, accepted and deferred, or rejected with a reason | section 3's decision table |
| 4 | Decide the two questions the set poses as questions: the four permanently-failing rules as a group, and `013`/`022` as one | section 3, below the table |

## 3. Implement

**Decisions & assumptions**

- **Nothing was actioned on the report's word.** Seven claims were re-run against this tree before
  any record was decided, chosen as the ones a fix would depend on. **All seven hold on `0.6.0`.**
  — 2026-08-29

| Record | Re-run | Result |
| :--- | :--- | :--- |
| [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) | `set_var` at `tools/deck/density.py` `:179` | `tag[:-1] + ...` — the self-closing branch is unchanged |
| [`017`](../docs/adopter-reports/claimai/017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md) | `render.py` `:597` and `:602` | both seek expressions unchanged, and they still disagree |
| [`008`](../docs/adopter-reports/claimai/008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md) | `grep -c "ctrlKey\|metaKey\|altKey" shell/deck.js` | **0** — no modifier guard anywhere in the file |
| [`009`](../docs/adopter-reports/claimai/009-the-sources-box-does-not-dismiss-on-an-outside-click.md) | `closest('.sources')` in `shell/deck.js` | absent; the More menu's listener is still the only one |
| [`003`](../docs/adopter-reports/claimai/003-reading-view-never-unwraps-a-provenance-row.md) | `.doc .sources-item` in `shell/components.css` | absent; the box is unwrapped and the item is not |
| [`004`](../docs/adopter-reports/claimai/004-spec-py-cannot-read-a-sources-field-that-carries-a-section.md) | `slugs()` at `tools/deck/spec.py` `:103` | still splits on `[,;]` |
| [`018`](../docs/adopter-reports/claimai/018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md) | `check.py` on `examples/portfolio-review/` | `DS-218 ... False (present: True, 0 looping) pass` — reproduced exactly |

- **Three records were merged rather than raised, and that is what waiting for the audit bought.**
  [`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md) and [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md) are `DS-229` and `DS-239` bound on selector text and on a derived set — which is
  the class [T-243](T-243-five-checks-bound-on-a-name-rather-than-on-structure.md) already owns, `PR-44` naming `DS-239` by name. [`027`](../docs/adopter-reports/claimai/027-the-tools-are-unreachable-when-htmldeck-is-installed-as-a-plugin.md) is the plugin cache and what
  `$HTMLDECK` resolves to, which is `PR-07`'s root and [T-227](T-227-the-front-pages-adoption-route-names-a-variable-the-skill-removed.md)'s. **Three of twenty-seven cost nothing
  to place.** — 2026-08-29

- **One record refutes a conclusion the audit recorded as settled, and it is the most valuable thing
  in the set.** [`006`](../docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md) shows `DS-035` reading `0 du` on three display-size headings, because the
  probe scales font size by the screen CTM and a `scaleY(0)` entrance with `fill-mode:both` puts the
  determinant at zero. [T-209](T-209-six-more-probes-measure-a-page-whose-entrance-never-ran.md)
  left `audit.PROBE` unpinned and wrote its reason into the file: *its geometry rows were measured
  both ways on the portfolio deck and are identical, so pinning buys nothing here*. **That was one
  deck**, whose entrances do not move the axis `DS-035` reads. The comment states a one-deck
  measurement as a general property, which is the failure T-217 recorded a lesson about six days
  earlier. [T-261](T-261-ds-035-measures-a-text-run-through-its-transform.md) carries it, and the design problem underneath is real: one probe cannot be both
  pinned for a geometry rule and unpinned for three rules that read `animationIterationCount`.
  — 2026-08-29

- **`013` and `022` are decided together, as section 1 required, and the answer is neither of them
  alone.** [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md) says `DS-244` is too blind — it never compares a label to the shape it labels, the
  commonest defect in a hand-built figure. [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) says it is too strict — it refuses a cross-fade in
  place because it does not read `opacity`. **Read together they say the rule tests proximity of two
  text runs where it means obstruction**, which is a single statement neither record makes alone.
  [T-260](T-260-ds-244-tests-proximity-where-it-means-obstruction.md) takes both, and it carries a constraint: [T-204](T-204-an-instrument-for-mark-collisions.md)
  measured text-against-line at 16 firings for 1 real defect and made it report rather than gate, on
  T-115's precedent. That calibration is a term in the decision and must not be reversed by
  inattention. — 2026-08-29

- **The four permanently-failing rules, decided as a group: no, a deck failing four rules by design
  is not acceptable — and three of the four are the gate's fault rather than the deck's.**
  `DS-217` is unsatisfiable past eighteen sections because sub-pixel rounding defeats a clustering
  test ([T-263](T-263-ds-217-fails-on-any-deck-past-eighteen-sections.md)). `DS-219` is unsatisfiable for a whole class of correct diagrams, and
  [`DESIGN-RATIONALE.md`](../docs/DESIGN-RATIONALE.md) section 5.7 already doubts it in this
  repository's own words ([T-256](T-256-ds-219-cannot-see-a-painted-svg-ancestor.md)). `DS-218` is failed by a deck that copied the chrome of a shipped
  example which passes the same rule vacuously ([T-257](T-257-ds-218-passes-the-shipped-example-vacuously.md)). **Only `DS-110` is the deck genuinely
  choosing to break a rule**, and that one is a rule change the owner decides ([T-265](T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md)). After these
  four tasks a deck of this shape should fail **at most one** rule, by an explicit decision rather
  than by exhaustion. The cost the report names — *an author who cannot ever reach zero stops
  reading the gate* — is the reason this is a group and not four unrelated rows. — 2026-08-29

- **Three proposals are recommended against, and the reasons are recorded here because there is no
  channel to send them.** [`023`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md)'s second option, *make `DS-100` reviewable rather than fatal* —
  `hard` is what the corpus measured and *reviewable* is how a rule quietly stops being enforced;
  its first option, extending the existing source-question exemption, is accepted instead. [`024`](../docs/adopter-reports/claimai/024-ds-202-refuses-a-two-sentence-bottom-line-the-author-chose.md)'s
  first option, replacing `DS-202`'s sentence count with a word or clause cap — that trades a crisp
  rule for a fuzzy one, and the record itself says the rule caught **eight** bottom lines restating
  their headline; its second option, saying the reason in the failure, is accepted instead. [`011`](../docs/adopter-reports/claimai/011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md)'s
  primary form, allowing any raster in a `front` or `back` section — broader than the argument
  supports; the record's own weaker alternative is closer to the real test and is what [T-265](T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md)
  recommends. **All three records anticipated the disagreement and none of them asks to drop a
  rule**, which is why all three are still worth acting on. — 2026-08-29

- **Nothing here was rejected outright.** Twenty-four records are raised, three are merged, and one
  — [`001`](../docs/adopter-reports/claimai/001-per-section-quick-view.md) — is accepted and **deferred** rather than rejected: it is the only record asking for a
  new component, and deferring it is a scheduling decision rather than a judgement on the case.
  — 2026-08-29

**Outputs produced**

- Eighteen child tasks, `T-254` to `T-271`, listed in section 4.
- Three merges: two `In:` lines and an input on [T-243](T-243-five-checks-bound-on-a-name-rather-than-on-structure.md), one of each on [T-227](T-227-the-front-pages-adoption-route-names-a-variable-the-skill-removed.md).

## 4. Review

| Acceptance criterion | Result | Note |
| :--- | :---: | :--- |
| Every one of the twenty-seven carries a decision | **met** | The table below. 24 accepted and raised, 3 accepted and merged, 1 of the 24 deferred rather than scheduled. None rejected outright; three proposals within accepted records are recommended against, with reasons in section 3 |
| `013` and `022` are decided together, as one question about what `DS-244` is testing | **met** | [T-260](T-260-ds-244-tests-proximity-where-it-means-obstruction.md). The joint statement — proximity where it means obstruction — is in neither record alone |
| Each accepted finding names the task that will do it | **met** | The table below, and every task names its records back |
| Each rejected finding says why, in a sentence an adopter would accept | **met, and narrower than section 1 expected** | Nothing was rejected. Three *proposals inside* accepted records are recommended against and each carries an evidence-shaped reason, which is the bar section 1 set |
| The four permanently-failing rules are looked at as a group, and the outcome says whether a deck failing four rules by design is acceptable | **met** | **No.** Three of the four are the gate's fault; only `DS-110` is a rule the deck chose to break. Section 3 carries the argument |
| `Version seen` is checked before any record is actioned | **met** | Seven re-run against this tree, all seven hold. The table in section 3 |

**The triage**

| Record | Task | Decision | What it is | Phase, effort |
| :--- | :--- | :--- | :--- | :--- |
| [`015`](../docs/adopter-reports/claimai/015-density-py-write-corrupts-a-self-closing-svg-tag.md) | [T-254](T-254-density-py-write-corrupts-every-self-closing-svg-tag.md) | accepted, raised | Fix set_var's self-closing tag insertion, and have write verify what it wrote | `PH1`, `s` |
| [`017`](../docs/adopter-reports/claimai/017-render-py-motion-seeks-a-fraction-of-duration-and-ignores-the-delay.md) | [T-255](T-255-render-py-motion-seeks-past-the-delay.md) | accepted, raised | Add the delay in the report branch and drop the subtraction in the capture branch | `PH1`, `s` |
| [`019`](../docs/adopter-reports/claimai/019-ds-219-cannot-see-a-painted-svg-ancestor.md) | [T-256](T-256-ds-219-cannot-see-a-painted-svg-ancestor.md) | accepted, raised | Walk the full ancestor chain for DS-219's ground, and settle the doubt the rationale records | `PH1`, `m` |
| [`018`](../docs/adopter-reports/claimai/018-ds-218-passes-the-shipped-example-only-because-it-has-no-looping-motion.md) | [T-257](T-257-ds-218-passes-the-shipped-example-vacuously.md) | accepted, raised | Make portfolio-review pass DS-218 for a reason, and say why a control is not persistent | `PH1`, `s` |
| [`025`](../docs/adopter-reports/claimai/025-the-gate-passes-copy-its-own-reader-calls-difficult.md) | [T-258](T-258-the-gate-passes-copy-its-own-reader-calls-difficult.md) | accepted, raised | Report a readability measurement over drawn slide copy, and name the hardest lines | `PH3`, `m` |
| [`026`](../docs/adopter-reports/claimai/026-nothing-prints-what-a-slide-actually-contains.md) | [T-259](T-259-nothing-prints-what-a-slide-actually-contains.md) | accepted, raised | Ship a per-slide fact printer, so a specification and its deck stop drifting silently | `PH3`, `m` |
| [`013`](../docs/adopter-reports/claimai/013-ds-244-sees-label-over-label-but-not-label-over-shape.md), [`022`](../docs/adopter-reports/claimai/022-ds-244-refuses-a-cross-fade-in-place.md) | [T-260](T-260-ds-244-tests-proximity-where-it-means-obstruction.md) | accepted, raised | Decide what DS-244 measures, from the two findings that contradict each other | `PH1`, `m` |
| [`006`](../docs/adopter-reports/claimai/006-ds-035-measures-text-through-its-transform.md) | [T-261](T-261-ds-035-measures-a-text-run-through-its-transform.md) | accepted, raised | Re-derive whether audit.PROBE can stay unpinned, on a deck whose entrance moves the axis | `PH1`, `s` |
| [`012`](../docs/adopter-reports/claimai/012-ds-092-counts-a-sources-box-as-prose.md) | [T-262](T-262-ds-092-counts-a-sources-box-as-prose.md) | accepted, raised | Exclude provenance from DS-092's paragraph half, and give any source ceiling its own rule | `PH1`, `s` |
| [`002`](../docs/adopter-reports/claimai/002-ruler-scale-claim-breaks-past-eighteen-sections.md) | [T-263](T-263-ds-217-fails-on-any-deck-past-eighteen-sections.md) | accepted, raised | Give regularScale a tolerance, so a long deck can satisfy DS-217 | `PH1`, `s` |
| [`005`](../docs/adopter-reports/claimai/005-a-deck-cannot-express-an-author-requested-duration.md) | [T-264](T-264-ds-141s-request-licence-has-nowhere-to-put-its-number.md) | accepted, raised | Give a licensed long motion somewhere to state its duration | `PH1`, `s` |
| [`011`](../docs/adopter-reports/claimai/011-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md) | [T-265](T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md) | accepted, raised | Decide whether DS-110 narrows by where a raster sits | `PH3`, `s` |
| [`014`](../docs/adopter-reports/claimai/014-a-deck-cannot-name-a-repeated-figure-treatment-once.md) | [T-266](T-266-a-deck-cannot-name-a-repeated-figure-treatment-once.md) | accepted, raised | Say what to do when a class fails DS-229, and decide whether a deck gets a local prefix | `PH3`, `s` |
| [`016`](../docs/adopter-reports/claimai/016-render-py-cannot-capture-a-decks-interactive-states.md) | [T-267](T-267-render-py-cannot-capture-a-decks-interactive-states.md) | accepted, raised | Give render.py a capture path for a deck's disclosed states | `PH3`, `m` |
| [`008`](../docs/adopter-reports/claimai/008-single-letter-shortcuts-swallow-ctrl-r-and-every-other-browser-chord.md), [`009`](../docs/adopter-reports/claimai/009-the-sources-box-does-not-dismiss-on-an-outside-click.md), [`010`](../docs/adopter-reports/claimai/010-data-played-lands-at-transition-start-so-an-entrance-plays-under-the-outgoing-slide.md) | [T-268](T-268-three-chrome-and-timing-defects-in-deck-js.md) | accepted, raised | Guard the single-letter shortcuts, dismiss the sources box, and land data-played on arrival | `PH1`, `s` |
| [`003`](../docs/adopter-reports/claimai/003-reading-view-never-unwraps-a-provenance-row.md), [`004`](../docs/adopter-reports/claimai/004-spec-py-cannot-read-a-sources-field-that-carries-a-section.md), [`007`](../docs/adopter-reports/claimai/007-quickview-leaves-bold-unconverted-across-a-line-break.md) | [T-269](T-269-three-build-path-defects-the-adopter-worked-around.md) | accepted, raised | Unwrap a provenance row, read a rich Sources field, and convert bold across a line break | `PH1`, `s` |
| [`023`](../docs/adopter-reports/claimai/023-ds-100-fires-on-any-question-mark-meeting-a-tag.md), [`024`](../docs/adopter-reports/claimai/024-ds-202-refuses-a-two-sentence-bottom-line-the-author-chose.md) | [T-270](T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md) | accepted, raised | Decide what DS-100 and DS-202 should measure, and say the reason in each failure | `PH3`, `s` |
| [`001`](../docs/adopter-reports/claimai/001-per-section-quick-view.md) | [T-271](T-271-a-quick-view-scoped-to-a-document-section.md) | accepted, raised | Decide whether a slide can open a quick view scoped to the section it argues from | `PH3`, `m` |
| [`020`](../docs/adopter-reports/claimai/020-ds-229-keys-motion-rows-to-exact-selector-text.md) | [T-243](T-243-five-checks-bound-on-a-name-rather-than-on-structure.md) | accepted, **merged** | That task already owns the class; the record is an extra `In:` line on it, not a second task | — |
| [`021`](../docs/adopter-reports/claimai/021-ds-239-re-derives-m-rank-so-removing-one-motion-invalidates-the-rest.md) | [T-243](T-243-five-checks-bound-on-a-name-rather-than-on-structure.md) | accepted, **merged** | That task already owns the class; the record is an extra `In:` line on it, not a second task | — |
| [`027`](../docs/adopter-reports/claimai/027-the-tools-are-unreachable-when-htmldeck-is-installed-as-a-plugin.md) | [T-227](T-227-the-front-pages-adoption-route-names-a-variable-the-skill-removed.md) | accepted, **merged** | That task already owns the class; the record is an extra `In:` line on it, not a second task | — |

**Child fix tasks raised**

- Eighteen: `T-254` through `T-271`. Seven `PH1` records carry ten of the twenty-seven findings
  between them, because a defect an adopter met in the published `0.6.0` is `CLAUDE.md`'s one
  condition for reopening the phase.

**The order the child tasks are worked in is [`../docs/REMEDIATION-ORDER.md`](../docs/REMEDIATION-ORDER.md)**, written 2026-08-29 once cycle 40 and T-225 put 49 tasks on the board at once. It batches 47 of them for unattended sessions, carries the owner's eight rulings and the standing authority a session works under, and puts cycles 41 and 42 at the end where they belong. **It is a schedule and never a second statement of what a task does.**

**What this triage found that it was not looking for**

- **The audit and the adopter report agree on a class neither could have named alone.** The audit's
  `PR-44` and `PR-70` are checks bound on a name or emptied of their subject; the report's `020`,
  `021` and `018` are the same shape met from outside. **`018` is the sharper one**: a shipped
  example passing a rule vacuously is the absent-subject defect (**L-57**) in the one artifact an
  adopter is told to copy.
- **A report written without access to this repository's reasoning arrived at a doubt this
  repository had already written down.** `019` and `DESIGN-RATIONALE.md` section 5.7 are independent,
  and that is what makes the pair worth acting on rather than either alone.

## Log

| Date | Status change | Note |
| :--- | :--- | :--- |
| 2026-08-29 | → done | **Twenty-seven records, eighteen tasks, three merges, nothing rejected.** Run after the pre-release audit's own triage closed, which is what made three records free: `020` and `021` are `DS-229` and `DS-239` bound on selector text and on a derived set, so they merged into `T-243`, whose `PR-44` already names `DS-239`; `027` is the plugin cache and `$HTMLDECK`, so it merged into `T-227`. **Seven claims were re-run before anything was decided and all seven hold on `0.6.0`** — the report's `Version seen` was stamped rather than re-run on fourteen of them, and `018`'s evidence reproduced to the character. **The most valuable record refutes the audit**: `006` shows `DS-035` reading 0 du through a `scaleY(0)` entrance, where `T-209` left `audit.PROBE` unpinned on a measurement taken on one deck and wrote it into the file as a general property. `T-261` carries it. **The four permanently-failing rules are answered as a group and the answer is no**: three of `DS-110`, `DS-217`, `DS-218` and `DS-219` are the gate's fault, and only `DS-110` is a rule the deck chose to break. **`013` and `022` are decided as one question** and the answer is in neither alone — `DS-244` tests proximity where it means obstruction. Three proposals inside accepted records are recommended against, with reasons recorded here because the report is a closed one-way hand-over and there is nowhere to send them. |
| 2026-08-29 | (no change) | **The eighteen are `parent: null`, `related: [T-225]`, and the gate is what settled it.** Written as children first, `taskmd check` refused the tree: *CLOSED PARENT T-225 is 'done' with children T-254 ... still open*. That refusal is right and the fix is not to hold this task open — section 1 says the deliverable is the judgement and that *the fixes it accepts become tasks of their own*, so a triage that stays open until every judgement is executed conflates deciding with doing. **The precedent is the owner's ruling of 2026-08-23** on `T-057` and `T-016`, recorded in [T-221](T-221-answer-the-three-defects-taskmd-0-6-0s-wider-check-set-found.md): a record created by another and worked separately is a spin-off rather than a part. Same shape, same disposition. |
| 2026-08-28 | → proposed | Created when the adopter report was handed over. The report was collected during the project rather than written up afterwards, and every claim in it was verified against `0.6.0` before it was staged. Nothing is expected in return. |
