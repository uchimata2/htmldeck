# Task index — htmldeck

Generated from each task's front-matter. **Do not hand-edit** between the markers below.

```
taskmd index            # regenerate this file
taskmd context T-001    # everything needed to start a task
taskmd check            # validate
```

Working method: [`../CLAUDE.md`](../CLAUDE.md). Specification: [`../docs/BRIEF.md`](../docs/BRIEF.md).
Schema, statuses and lifecycle: [`TASK-WORKFLOW.md`](TASK-WORKFLOW.md). Carried lessons:
[`../docs/LESSONS.md`](../docs/LESSONS.md).

**The open backlog is three release phases, and the `Work Package` column below carries them.**
**PH1** is what a first working release needs and nothing else, and it has shipped; **PH2** is the
dependencies and every minor and moderate fix; **PH3** is the bigger tasks and the new capabilities,
everything estimated `l` or `xl`. What is in each and why is in
[`../docs/BRIEF.md`](../docs/BRIEF.md) *Release phases* — that section is the decision, this page is
the current state of it. **Closed tasks keep the `WP1`–`WP3` packages they were worked under**;
those were phases of the research and design work and rewriting them would be rewriting what
happened.

**A phase is not a version, and the `Shipped In` column is the version.** The three phases were named
`v0.1`, `v0.2` and `v0.3` until 2026-08-12, which made them unreadable next to the releases they were
not: `PH3` work shipping in `0.2.1` is the rule working, since a release takes the next patch number
on the published line whatever phase its tasks belong to. `Shipped In` is the release in which a
task's work first reached an installed copy, derived from the first tag containing the commit that
closed it — `unreleased` where that has not happened yet. **T-099**, and **L-69** for what the old
names cost.

<!-- taskmd:index - generated, do not edit by hand -->

## Active

| ID | Title | Work Package | Shipped In | Status | Phase | Parent | Children | Related |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [T-041](T-041-implement-the-nine-glitch-free-conditions.md) | Implement the nine glitch-free conditions R6 defined and nothing adopted | `PH3` | - | `proposed` | `specify` | - | - | T-005, T-016, T-019, T-042, T-097, T-111, T-112 |
| [T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md) | Record which clauses of a rule the gate decides, not only which rules it reaches | `PH3` | - | `proposed` | `specify` | T-053 | - | T-005, T-037, T-043, T-051, T-119 |
| [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) | The 3D visual class, the frame-rate figure, and DS-140's fifth motion | `PH3` | - | `proposed` | `specify` | T-016 | - | T-007, T-016, T-019, T-033, T-111, T-112, T-113 |
| [T-097](T-097-ds-004s-excusal-says-degrade-gracefully-is-unobservable-and-ds-009-gave-it-an-instrument.md) | DS-004's excusal says degrading gracefully is unobservable, and DS-009 gave half of it an instrument | `PH3` | - | `proposed` | `specify` | - | - | T-017, T-019, T-041 |
| [T-109](T-109-one-source-reference-component-rendered-in-three-places.md) | One source-reference component, typed by what the source is, rendered in three places | `PH3` | - | `proposed` | `specify` | - | - | T-069, T-070, T-103, T-106, T-108, T-110, T-115, T-117, T-118 |
| [T-110](T-110-the-quick-view-styles-a-source-as-deck-copy-not-as-a-document.md) | The quick view styles a source as deck copy, not as a document | `PH3` | - | `proposed` | `specify` | - | - | T-070, T-106, T-107, T-109, T-121, T-122 |
| [T-111](T-111-a-named-slide-transition-chosen-per-deck.md) | A named slide transition, chosen per deck, with slide and immediate as the shipping pair | `PH3` | - | `proposed` | `specify` | - | - | T-016, T-041, T-057, T-112 |
| [T-112](T-112-motion-density-and-the-split-between-content-and-affordance-motion.md) | Motion density, and the split between content motion and affordance motion | `PH3` | - | `proposed` | `specify` | - | - | T-016, T-041, T-057, T-111, T-113, T-114 |
| [T-113](T-113-evaluate-an-embeddable-chart-library-against-hand-authored-svg.md) | Evaluate an embeddable chart library against hand-authored SVG, and settle where each is used | `PH3` | - | `proposed` | `specify` | - | - | T-057, T-112, T-119 |
| [T-114](T-114-the-chrome-row-layout-the-pager-deserves-the-corner.md) | The chrome row layout — give the pager the corner, and decide what happens to Read and Motion | `PH3` | - | `proposed` | `specify` | - | - | T-035, T-036, T-112, T-115, T-119 |
| [T-115](T-115-the-specification-can-assert-a-layout-the-shell-cannot-honour.md) | A specification can assert a layout the shell cannot honour, and nothing reads the two together | `PH3` | - | `proposed` | `specify` | - | - | T-109, T-114, T-117, T-118, T-119 |
| [T-117](T-117-the-decision-diamond-has-no-label-slot-and-diagrams-sit-off-the-text-grid.md) | The decision diamond has no label slot, and diagrams sit off the text grid | `PH3` | - | `proposed` | `specify` | - | - | T-016, T-109, T-115 |
| [T-118](T-118-a-style-must-mean-the-same-thing-in-the-reading-view.md) | A style that carries meaning on a slide must carry the same meaning in the reading view | `PH3` | - | `proposed` | `specify` | - | - | T-070, T-109, T-115 |
| [T-119](T-119-audit-the-ruleset-for-rules-that-cost-more-than-they-return.md) | Audit the ruleset for rules that cost more to satisfy than they return | `PH3` | - | `proposed` | `specify` | - | - | T-054, T-113, T-114, T-115 |
| [T-121](T-121-the-quick-view-renderer-flattens-nested-lists-and-drops-indented-code.md) | The quick-view renderer flattens nested lists and renders indented code as paragraphs | `PH3` | - | `proposed` | `specify` | - | - | T-070, T-107, T-110 |
| [T-128](T-128-publish-the-adopter-deck-as-a-worked-example.md) | Publish the adopting project's D6 deck as a third worked example, sanitized on the way in | `PH3` | - | `proposed` | `specify` | - | - | T-085, T-123, T-124, T-125, T-129, T-130 |
| [T-131](T-131-expose-the-trackers-query-commands-so-the-board-is-not-read-whole.md) | Expose the tracker's query commands so the board is not read whole | `PH3` | - | `proposed` | `specify` | T-130 | - | T-130 |
| [T-132](T-132-give-the-deck-gate-a-quiet-mode-for-its-green-run.md) | Give the deck gate a quiet mode for its green run | `PH3` | - | `proposed` | `specify` | T-130 | - | T-130 |
| [T-133](T-133-write-down-that-a-deck-is-never-read-whole.md) | Write down that a deck is never read whole | `PH3` | - | `proposed` | `specify` | T-130 | - | T-130, T-134 |
| [T-134](T-134-state-the-tier-model-and-bound-tier-1-as-a-relation.md) | State the tier model and bound tier 1 as a relation | `PH3` | - | `proposed` | `specify` | T-130 | - | T-130, T-133 |

## Closed

| ID | Title | Work Package | Shipped In | Status | Phase | Parent | Children | Related |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [T-001](T-001-decide-the-font-strategy-embedded-subsets-or-a-syste.md) | Decide the font strategy: embedded subsets or a system stack | `WP2` | `0.1.0` | `done` | `review` | - | - | T-005, T-013, T-024 |
| [T-002](T-002-build-mode-the-self-contained-deck-generator.md) | Build mode — the self-contained deck generator | `PH1` | `0.1.0` | `done` | `review` | - | - | T-003, T-004, T-005, T-006, T-007, T-015, T-016, T-017, T-018, T-020, T-021, T-023, T-024, T-026, T-027, T-028 |
| [T-003](T-003-brief-mode-elicit-the-six-section-prompt.md) | Brief mode — elicit the six-section prompt | `WP3` | `0.1.0` | `cancelled` | `specify` | - | - | T-002, T-015, T-020, T-027, T-089 |
| [T-004](T-004-critique-mode-blunt-section-by-section-review.md) | Critique mode — blunt section-by-section review | `PH1` | `0.1.0` | `done` | `review` | - | - | T-002, T-005, T-020, T-022, T-023, T-026, T-042, T-047, T-048, T-092 |
| [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) | Build check — the gate the deck must pass | `WP3` | `0.1.0` | `done` | `review` | - | T-040 | T-001, T-002, T-004, T-007, T-016, T-017, T-018, T-019, T-021, T-022, T-023, T-025, T-027, T-028, T-032, T-034, T-036, T-037, T-038, T-039, T-041, T-042, T-043, T-047, T-048, T-050, T-051, T-053, T-054, T-055, T-058 |
| [T-006](T-006-decide-the-chart-strategy.md) | Decide the chart strategy | `WP2` | `0.1.0` | `done` | `review` | - | - | T-002, T-013, T-016, T-017, T-024 |
| [T-007](T-007-define-the-parametric-theme-layer.md) | Define the parametric theme layer | `WP2` | `0.1.0` | `done` | `review` | - | - | T-002, T-005, T-016, T-021, T-024, T-057, T-059 |
| [T-008](T-008-package-document-and-publish.md) | Package, document and publish | `PH1` | `0.1.1` | `done` | `review` | - | - | T-030, T-042, T-050, T-061, T-064, T-078 |
| [T-009](T-009-analyse-the-corpus-extract-my-deck-conventions.md) | Analyse the corpus — extract the deck conventions already in use | `WP1` | `0.1.0` | `done` | `review` | - | - | T-012, T-014 |
| [T-010](T-010-research-external-deck-design-and-ux-principles.md) | Research external deck-design and presentation UX principles | `WP1` | `0.1.0` | `done` | `review` | - | - | T-014 |
| [T-011](T-011-research-exemplary-decks-and-why-they-work.md) | Research exemplary decks and what makes them work | `WP1` | `0.1.0` | `done` | `review` | - | - | T-014 |
| [T-012](T-012-research-existing-html-deck-skills-and-libraries.md) | Research existing HTML-deck skills, plugins and libraries to build on | `WP1` | `0.1.0` | `done` | `review` | - | - | T-009, T-014, T-015 |
| [T-013](T-013-research-offline-safe-assets-and-licences.md) | Research offline-safe assets — icons, illustration, fonts, diagram tooling | `WP1` | `0.1.0` | `done` | `review` | - | - | T-001, T-006, T-014, T-017 |
| [T-014](T-014-synthesise-research-into-the-design-system-reference.md) | Synthesise the research into the htmldeck design-system reference | `WP1` | `0.1.0` | `done` | `review` | - | T-022 | T-009, T-010, T-011, T-012, T-013, T-020, T-021, T-023, T-024, T-025, T-037, T-038, T-039, T-047, T-049 |
| [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md) | Plugin scaffold and the two-question interface | `WP2` | `0.1.0` | `done` | `review` | - | - | T-002, T-003, T-012, T-020, T-027, T-050, T-061 |
| [T-016](T-016-the-interaction-and-motion-layer.md) | The interaction and motion layer | `PH1` | `0.1.0` | `done` | `review` | - | T-057 | T-002, T-005, T-006, T-007, T-017, T-021, T-024, T-032, T-035, T-041, T-057, T-058, T-069, T-092, T-104, T-111, T-112, T-117 |
| [T-017](T-017-define-the-portability-contract.md) | Define the portability contract — what "opens anywhere and works" actually permits | `WP1` | `0.1.0` | `done` | `review` | - | - | T-002, T-005, T-006, T-013, T-016, T-018, T-019, T-049, T-097 |
| [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) | Measure the printable mode — what printing a deck from `file://` actually costs | `WP1` | `0.1.0` | `done` | `review` | - | - | T-002, T-005, T-017, T-021, T-029, T-032, T-034 |
| [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) | Build the capability preflight every deck ships with | `PH3` | `0.2.1` | `done` | `review` | - | - | T-005, T-017, T-041, T-057, T-070, T-093, T-094, T-097 |
| [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) | Model the authoring pipeline, not just the three modes | `WP1` | `0.1.0` | `done` | `review` | - | - | T-002, T-003, T-004, T-014, T-015, T-022, T-023, T-026, T-027, T-030 |
| [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) | Build the reflow view and enforce the resolution contract | `WP2` | `0.1.0` | `done` | `review` | - | - | T-002, T-005, T-007, T-014, T-016, T-018, T-024, T-025, T-028, T-032, T-037, T-039, T-083 |
| [T-022](T-022-split-the-design-system-from-its-rationale.md) | Split the operative ruleset from its rationale, and give every rule an ID | `WP1` | `0.1.0` | `done` | `review` | T-014 | - | T-004, T-005, T-020, T-023, T-025, T-037, T-039 |
| [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) | Define the deck evaluation rubric and the convergence loop that uses it | `WP1` | `0.1.0` | `done` | `review` | - | T-026 | T-002, T-004, T-005, T-014, T-020, T-022, T-024, T-025, T-044, T-048 |
| [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) | Build the reference deck by hand and find out whether the ruleset works | `WP2` | `0.1.0` | `done` | `review` | - | T-025 | T-001, T-002, T-006, T-007, T-014, T-016, T-021, T-023, T-026, T-027, T-028, T-040, T-044, T-050, T-052 |
| [T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md) | Reconcile the thirteen ruleset findings the reference deck produced | `WP2` | `0.1.0` | `done` | `review` | T-024 | - | T-005, T-014, T-021, T-022, T-023, T-027, T-028, T-033, T-047 |
| [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) | Settle who scores a deck, and whether the score reaches the user | `WP2` | `0.1.0` | `done` | `review` | T-023 | T-029 | T-002, T-004, T-020, T-024, T-048 |
| [T-027](T-027-specify-the-slide-deliverable-and-the-outline-contract.md) | Specify the slide deliverable and the outline contract, and the rules the owner's deck review implies | `WP2` | `0.1.0` | `done` | `review` | - | T-028 | T-002, T-003, T-005, T-015, T-020, T-024, T-025, T-033, T-035, T-048 |
| [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) | Retrofit the reference deck to the deliverable contract and thin its chrome | `WP2` | `0.1.0` | `done` | `review` | T-027 | - | T-002, T-005, T-021, T-024, T-025, T-030, T-032, T-033, T-035, T-040, T-044, T-045, T-052 |
| [T-029](T-029-stop-the-deliverable-exemption-silently-dropping-pointers.md) | Stop the deliverable exemption silently dropping pointers from the check | - | `0.1.0` | `done` | `review` | T-026 | - | T-018, T-031, T-046 |
| [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) | Audit the dependency edges across the open backlog and propose a build order | - | `0.1.0` | `done` | `review` | - | - | T-008, T-020, T-028, T-031 |
| [T-031](T-031-stop-the-index-blocks-column-listing-closed-tasks.md) | Stop the index `Blocks` column listing closed downstream tasks | - | `0.1.0` | `done` | `review` | - | - | T-029, T-030, T-046, T-079 |
| [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) | Adopt the paginated print mode in the reference deck, and decide whether print carries tier two | `WP2` | `0.1.0` | `done` | `review` | - | - | T-005, T-016, T-018, T-021, T-028, T-034, T-044 |
| [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md) | Reconcile DS-131 with the chrome budget it now contradicts | `WP2` | `0.1.0` | `done` | `review` | - | - | T-025, T-027, T-028, T-035, T-037, T-057 |
| [T-034](T-034-a-contents-page-for-the-printed-deck.md) | Add a contents page to the printed deck | `WP2` | `0.1.0` | `done` | `review` | - | T-036 | T-005, T-018, T-032, T-035, T-036, T-044, T-108, T-116, T-123, T-125 |
| [T-035](T-035-the-ruler-navigator.md) | Replace the stage ribbon with a ruler navigator, and rescope the chrome budget it breaks | `WP2` | `0.1.0` | `done` | `review` | - | - | T-016, T-027, T-028, T-033, T-034, T-044, T-102, T-108, T-114 |
| [T-036](T-036-the-second-contents-page-for-long-decks.md) | Continue the contents page onto a second sheet for decks past the measured bound | `PH2` | `unreleased` | `done` | `review` | T-034 | - | T-005, T-034, T-042, T-084, T-108, T-114, T-116, T-123, T-124, T-125 |
| [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) | Record in the ruleset itself which rules no check can reach | `WP2` | `0.1.0` | `done` | `review` | - | T-039 | T-005, T-014, T-021, T-022, T-033, T-038, T-042, T-043, T-045, T-046, T-048, T-053, T-054 |
| [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) | Stop the gate reporting judge rules, and one verdict under the wrong rule ID | `WP3` | `0.1.0` | `done` | `review` | - | - | T-005, T-014, T-037, T-043, T-051, T-053, T-055 |
| [T-039](T-039-finish-the-record-t-037-left-in-the-wrong-places.md) | Finish the record T-037 left in the wrong places | `WP2` | `0.1.0` | `done` | `review` | T-037 | - | T-005, T-014, T-021, T-022, T-042, T-046 |
| [T-040](T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md) | Fix the three reference-deck defects the completed gate found | `WP3` | `0.1.0` | `done` | `review` | T-005 | - | T-024, T-028, T-044, T-052 |
| [T-042](T-042-audit-the-whole-repository-against-itself.md) | Audit the repository against itself — stale claims, unreachable rules, and unchecked references | - | `0.1.0` | `done` | `review` | - | T-043, T-044, T-045, T-046, T-047, T-048, T-049, T-050 | T-004, T-005, T-008, T-036, T-037, T-039, T-041, T-056 |
| [T-043](T-043-make-the-gates-coverage-account-provable.md) | Make the gate's coverage account provable, and derive the counts the documents state | - | `0.1.0` | `done` | `review` | T-042 | - | T-005, T-037, T-038, T-051, T-054 |
| [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) | Restore the seeded-defect fixture, and re-measure everything examples/README claims | - | `0.1.0` | `done` | `review` | T-042 | T-051 | T-023, T-024, T-028, T-032, T-034, T-035, T-040, T-045, T-052 |
| [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | Sweep the nine stale claims the audit found across the live documents | - | `0.1.0` | `done` | `review` | T-042 | - | T-028, T-037, T-044, T-046, T-047 |
| [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) | Extend task.py to the three things it cannot currently see | - | `0.1.0` | `done` | `review` | T-042 | - | T-029, T-031, T-037, T-039, T-045, T-062 |
| [T-047](T-047-give-the-rationale-conflicts-their-own-id-namespace.md) | Give the rationale's conflicts their own ID namespace, and fix the mis-citation it has already caused | - | `0.1.0` | `done` | `review` | T-042 | - | T-004, T-005, T-014, T-025, T-045 |
| [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) | Gate the twenty-five hard rules only a judgement pass can reach | `WP2` | `0.1.0` | `done` | `review` | T-042 | T-052 | T-004, T-005, T-023, T-026, T-027, T-037 |
| [T-049](T-049-reconcile-the-session-memory-with-the-research.md) | Reconcile the session memory with what the research settled and the owner last said | - | `0.1.0` | `done` | `review` | T-042 | - | T-014, T-017 |
| [T-050](T-050-write-the-repository-readme.md) | Write the repository README — what exists, what does not, and how to run it | `final` | `0.1.0` | `done` | `review` | T-042 | - | T-005, T-008, T-015, T-024, T-056, T-060 |
| [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) | A check whose subject is absent must not report a pass | - | `0.1.0` | `done` | `review` | T-044 | - | T-005, T-038, T-043, T-053, T-054, T-065, T-066, T-075, T-090 |
| [T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md) | Settle the two hard-judge failures the checklist's first run found in the reference deck | - | `0.1.0` | `done` | `review` | T-048 | - | T-024, T-028, T-040, T-044, T-056 |
| [T-053](T-053-enforce-the-headline-ds-091-requires.md) | Enforce the headline DS-091 requires, and excuse the fragment count no check can reach | - | `0.1.0` | `done` | `review` | - | T-054, T-055 | T-005, T-037, T-038, T-051 |
| [T-055](T-055-a-variant-that-leaves-malformed-markup.md) | Close the slide-is-not-a-section variant's open tag, so it tests the tag and not parser repair | `PH2` | `0.1.5` | `done` | `review` | T-053 | - | T-005, T-038 |
| [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) | Humanize the human-facing documents before publishing | `PH1` | `0.1.0` | `done` | `review` | - | - | T-042, T-050, T-052, T-060, T-067, T-078 |
| [T-058](T-058-the-seeded-defect-generator-reports-edits-that-never-matched.md) | The seeded-defect generator reports edits that never matched | `PH2` | `0.1.5` | `done` | `review` | - | - | T-005, T-016 |
| [T-059](T-059-theme-swap-overwrites-its-input-when-o-is-omitted.md) | Theme swap overwrites its input when -o is omitted | `PH2` | `0.1.4` | `done` | `review` | - | - | T-007, T-101 |
| [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md) | Check that the README's pasted figures still match the commands that produced them | `PH2` | `0.1.4` | `done` | `review` | - | - | T-050, T-056, T-067, T-068, T-077, T-088 |
| [T-061](T-061-the-scaffold-check-passed-a-manifest-the-installer-rejects.md) | The scaffold check passed a manifest the installer rejects | `PH1` | `0.1.1` | `done` | `review` | - | - | T-008, T-015, T-062, T-064, T-067 |
| [T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) | Retire the pre-split task tool and repoint what points at it | `PH2` | `0.1.2` | `done` | `review` | - | - | T-046, T-061, T-063, T-073, T-079, T-081 |
| [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md) | Improvements to propose upstream to taskmd | `PH2` | `0.1.2` | `done` | `review` | - | - | T-062, T-073, T-079, T-080, T-098 |
| [T-064](T-064-the-tools-crash-when-the-deck-is-on-another-drive.md) | The tools crash when the deck is on a different drive from the plugin | `PH1` | `0.1.2` | `done` | `review` | - | - | T-008, T-061, T-065, T-101 |
| [T-065](T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md) | Four rules still fail a deck for not having their subject | `PH1` | `0.1.2` | `done` | `review` | - | - | T-051, T-064, T-066, T-075, T-090 |
| [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) | Make the absent-subject rule a fixture instead of a sweep | `PH1` | `0.1.3` | `done` | `review` | - | - | T-051, T-065, T-075, T-090, T-095 |
| [T-067](T-067-the-published-upgrade-instructions-do-not-upgrade.md) | The published upgrade instructions do not upgrade anything | `PH1` | `0.1.4` | `done` | `review` | - | - | T-056, T-060, T-061 |
| [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) | Bind a prose figure to the field that produces it, not to the whole output | `PH2` | `0.2.0` | `done` | `review` | - | - | T-060, T-088 |
| [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) | Extend the provenance mark to multiple sources, and decide where deck-wide sources go | `PH2` | `0.1.4` | `done` | `review` | - | - | T-016, T-070, T-072, T-084, T-085, T-089, T-092, T-093, T-103, T-109 |
| [T-070](T-070-the-quick-view-for-a-source-document.md) | The quick view — a source document rendered inside the deck | `PH3` | `0.2.1` | `done` | `review` | - | - | T-019, T-069, T-071, T-092, T-103, T-106, T-107, T-109, T-110, T-118, T-121, T-122 |
| [T-071](T-071-the-intermediate-specifications-carry-their-references.md) | The intermediate specifications carry the sources they rest on | `PH2` | `0.1.5` | `done` | `review` | - | - | T-070, T-082, T-083, T-085, T-086 |
| [T-072](T-072-a-corrupted-comment-opener-in-shell-components-css.md) | A corrupted comment opener in shell/components.css would swallow the rule beneath it | - | `0.2.1` | `cancelled` | `specify` | - | - | T-069, T-089 |
| [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md) | Decide whether to keep refcheck now that upstream has ruled on bare paths | `PH2` | `0.1.5` | `done` | `review` | - | - | T-062, T-063, T-074, T-077, T-079, T-080, T-081 |
| [T-074](T-074-the-documented-render-command-does-not-exist.md) | The documented render command does not exist, and the tools write into their own install | `PH1` | `0.1.4` | `done` | `review` | - | - | T-073, T-094, T-101 |
| [T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md) | DS-064 probes for the reference deck's own class names, and contract.py is outside the fixture | `PH1` | `0.1.4` | `done` | `review` | - | - | T-051, T-065, T-066, T-076, T-083, T-095, T-101 |
| [T-076](T-076-a-verdict-producer-that-exits-instead-of-reporting.md) | A verdict producer that exits the process instead of reporting a row | `PH2` | `0.1.5` | `done` | `review` | - | - | T-075 |
| [T-077](T-077-report-a-figure-exclusion-that-outlived-its-numeral.md) | Report a figure exclusion that outlived the numeral it was written for | `PH2` | `0.1.5` | `done` | `review` | - | - | T-060, T-073, T-088 |
| [T-078](T-078-write-down-the-release-sequence.md) | Write down the release sequence, which lives only in four task logs | `PH2` | `0.1.5` | `done` | `review` | - | - | T-008, T-056, T-084, T-085, T-096, T-099 |
| [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md) | The board's dependency columns list closed tasks, so open rows read as blocked | `PH2` | `0.1.5` | `done` | `review` | - | - | T-031, T-062, T-063, T-073, T-080, T-081 |
| [T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md) | taskmd check resolves a markdown link inside a code fence, so pasted output cannot be quoted | `PH2` | `0.2.2` | `done` | `review` | - | - | T-063, T-073, T-079, T-081, T-098 |
| [T-081](T-081-the-installed-taskmd-is-two-minor-versions-behind.md) | The installed taskmd is two minor versions behind, so the gates run rules that have been superseded | `PH2` | `0.1.5` | `done` | `review` | - | - | T-062, T-073, T-079, T-080 |
| [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) | The worked example's figure ledger omits figures that reach slides, so the ledger cannot be the authority it is treated as | `PH2` | `0.2.0` | `done` | `review` | - | - | T-071, T-086, T-087, T-088, T-092 |
| [T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md) | The generated example deck fails a hard rule and nothing recorded it | `PH1` | `0.1.5` | `done` | `review` | - | - | T-021, T-071, T-075, T-084, T-085, T-096 |
| [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md) | The contents-bound fixture counts a deck that no longer exists, and has been red since the day the deck changed | `PH2` | `0.1.5` | `done` | `review` | - | - | T-036, T-069, T-078, T-083, T-096, T-116, T-123 |
| [T-085](T-085-the-reference-deck-does-not-carry-the-shell-it-defines.md) | The reference deck does not carry the shell it defines, and its sprite is out of sync | `PH1` | `0.1.5` | `done` | `review` | - | - | T-069, T-071, T-078, T-083, T-124, T-128, T-129 |
| [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md) | Check that every figure ledger row appears on the slides its Used on names | `PH2` | `0.2.0` | `done` | `review` | - | - | T-071, T-082, T-087, T-090 |
| [T-087](T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md) | Sweep the reference deck's figure ledger for the pattern T-082 found | `PH2` | `0.2.0` | `done` | `review` | - | - | T-082, T-086 |
| [T-088](T-088-a-figure-in-a-sentence-naming-no-field-goes-stale-unwatched.md) | A figure in a sentence that names no field goes stale unwatched, and two just did | `PH3` | `0.2.1` | `done` | `review` | - | - | T-060, T-068, T-077, T-082, T-092, T-127, T-129 |
| [T-089](T-089-a-withdrawn-task-was-deleted-rather-than-cancelled.md) | A task withdrawn on a false premise was deleted rather than cancelled, and no rule said which | `PH3` | `0.2.1` | `done` | `review` | - | - | T-003, T-069, T-072 |
| [T-090](T-090-spec5-cannot-parse-a-descriptive-slide-label.md) | SPEC-5 reports NO SUBJECT on a fully built deck whose slides carry a descriptive aria-label | `PH1` | `0.2.1` | `done` | `review` | - | - | T-051, T-065, T-066, T-086, T-091, T-101, T-102 |
| [T-091](T-091-build-md-documents-icons-set-as-a-single-pair.md) | build.md documents shell.py icons --set as a single pair, and it takes one comma-separated argument | `PH1` | `0.2.1` | `done` | `review` | - | - | T-090 |
| [T-092](T-092-product-feedback-from-the-first-external-deck.md) | Product feedback from the first external deck — six needs, all against tasks that already exist | `PH3` | `0.2.1` | `done` | `review` | - | - | T-004, T-016, T-069, T-070, T-082, T-088, T-099, T-100, T-103, T-104, T-105 |
| [T-093](T-093-ds-005s-check-bans-the-one-esm-route-r6-measured-as-working.md) | DS-005's check bans the one ESM route R6 measured as working | `PH3` | `0.2.1` | `done` | `review` | - | - | T-019, T-069, T-095 |
| [T-094](T-094-render-py-shots-out-with-a-relative-path-writes-nothing.md) | render.py shots --out with a relative path writes nothing and says FAILED | `PH1` | `0.2.1` | `done` | `review` | - | - | T-019, T-074 |
| [T-095](T-095-static-variants-builds-its-static-half-from-a-hand-kept-list.md) | static_variants builds its static half from a hand-kept list, so a new producer is outside the suite | `PH3` | `unreleased` | `done` | `review` | - | - | T-066, T-075, T-093, T-096 |
| [T-096](T-096-one-command-that-runs-every-checker-and-says-what-it-skipped.md) | One command that runs every checker under tools/ and reports what it skipped, with a reason | `PH3` | `0.2.3` | `done` | `review` | - | - | T-078, T-083, T-084, T-095, T-120, T-130 |
| [T-098](T-098-check-reports-briefs-phase-tables-as-a-second-index.md) | taskmd check reports BRIEF.md's phase tables as a second index, and will on every run | `PH3` | `0.2.3` | `done` | `review` | - | - | T-063, T-080, T-099 |
| [T-099](T-099-rename-the-release-phases-so-they-cannot-be-read-as-versions.md) | Rename the release phases to PH1-PH3 and record which version shipped each task | `PH3` | `0.2.2` | `done` | `review` | - | - | T-078, T-092, T-098 |
| [T-100](T-100-a-release-adds-a-required-part-and-conforming-decks-fail-silently.md) | A release adds a required part, and every conforming deck becomes non-conforming in silence | `PH3` | `0.2.2` | `done` | `review` | - | - | T-092 |
| [T-101](T-101-theme-py-self-test-fails-for-every-plugin-install.md) | theme.py exits on its own self-test for every plugin install, so no adopter can run it | `PH1` | `0.2.2` | `done` | `review` | - | - | T-059, T-064, T-074, T-075, T-090, T-102, T-126 |
| [T-102](T-102-data-stage-is-an-index-and-the-contract-does-not-say-so.md) | data-stage is an index into STAGES, the contract does not say so, and component.py passes a name | `PH1` | `0.2.2` | `done` | `review` | - | - | T-035, T-090, T-101 |
| [T-103](T-103-build-md-drops-ds-105s-link-clause-for-a-single-source-slide.md) | build.md drops DS-105's link clause for a single-source slide, so the mark does not read as provenance | `PH1` | `0.2.2` | `done` | `review` | - | - | T-069, T-070, T-092, T-109 |
| [T-104](T-104-an-svg-marker-defined-in-one-slide-does-not-paint-in-another.md) | An SVG marker defined in one slide does not paint in another, and four gates stay silent about it | `PH3` | `0.2.2` | `done` | `review` | - | - | T-016, T-092 |
| [T-105](T-105-fig-pos-neg-caution-are-vocabulary-so-a-real-deck-fails-for-using-them.md) | The figure's pos, neg and caution roles are vocabulary, so the first deck to use them fails component.py | `PH1` | `0.2.2` | `done` | `review` | - | - | T-092 |
| [T-106](T-106-the-quick-view-sheet-is-sized-to-the-prose-measure.md) | The quick-view sheet is sized to the prose measure, so a source's tables are crushed | `PH1` | `0.2.3` | `done` | `review` | - | - | T-070, T-109, T-110 |
| [T-107](T-107-quickviews-markdown-renderer-drops-thematic-breaks.md) | quickview.py's Markdown renderer drops thematic breaks, shipping "---" as body text | `PH1` | `0.2.3` | `done` | `review` | - | - | T-070, T-110, T-121, T-122 |
| [T-108](T-108-a-deck-has-no-back-matter-stage-so-the-colophon-is-labelled-with-the-last-argument-stage.md) | A deck has no back-matter stage, so the colophon is labelled with the last argument stage | `PH1` | `0.2.3` | `done` | `review` | - | - | T-034, T-035, T-036, T-109, T-124 |
| [T-116](T-116-the-printed-contents-page-collides-at-thirteen-entries.md) | The printed contents page collides at thirteen entries, well below its measured bound | `PH1` | `0.2.3` | `done` | `review` | - | - | T-034, T-036, T-084, T-120, T-123, T-124, T-125 |
| [T-120](T-120-printpages-standalone-defaults-the-slide-count-to-a-hardcoded-twelve.md) | printpages.py's own entry point defaults the slide count to a hardcoded 12, so it fails a correct deck | `PH1` | `0.2.3` | `done` | `review` | - | - | T-096, T-116 |
| [T-122](T-122-the-quick-views-contracted-article-is-never-created-so-seventeen-rules-are-dead.md) | The quick view's contracted `.qv-doc` article is never created, so seventeen style rules are dead | `PH1` | `0.2.3` | `done` | `review` | - | - | T-070, T-107, T-110 |
| [T-123](T-123-nothing-can-see-a-print-only-layout-fault.md) | Nothing can see a print-only layout fault, and one reached two shipped decks | `PH3` | `unreleased` | `done` | `review` | - | - | T-034, T-036, T-084, T-116, T-128 |
| [T-124](T-124-an-adopter-cannot-refresh-a-decks-shell-after-an-upgrade.md) | An adopter cannot refresh a deck's shell after an upgrade, so every release breaks every deck | `PH3` | `unreleased` | `done` | `review` | - | - | T-036, T-085, T-108, T-116, T-126, T-128 |
| [T-125](T-125-a-split-contents-page-still-clamps-its-descriptions-to-one-line.md) | Decide whether a split contents page should take a further sheet rather than clamp every description to one line | `PH3` | `unreleased` | `done` | `review` | - | - | T-034, T-036, T-116, T-126, T-128 |
| [T-126](T-126-shell-py-refuses-every-command-while-a-tracked-deck-is-behind-the-shell.md) | Stop shell.py refusing every command while a tracked deck is behind the shell | `PH3` | `unreleased` | `done` | `review` | - | - | T-101, T-124, T-125, T-127 |
| [T-127](T-127-figures-py-refuses-to-report-a-drifted-figure-because-its-fixture-needs-an-undrifted-page.md) | Stop figures.py refusing to report a drifted figure because its own fixture needs an undrifted page | `PH3` | `unreleased` | `done` | `review` | - | - | T-088, T-126, T-129 |
| [T-129](T-129-the-reference-decks-figures-in-examples-readme-are-unwatched-and-two-are-wrong.md) | The reference deck's figures in examples/README.md are bound to nothing, and two of them are wrong on the published page | `PH3` | `unreleased` | `done` | `review` | - | - | T-085, T-088, T-127, T-128 |
| [T-130](T-130-audit-the-context-economy-of-an-agent-driven-repository.md) | Audit the context economy of an agent-driven repository, and rank the savings | `PH3` | - | `done` | `review` | - | T-131, T-132, T-133, T-134 | T-096, T-128, T-131, T-132, T-133, T-134 |

<!-- taskmd:end -->
