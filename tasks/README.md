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
**v0.1** is what a first working release needs and nothing else, and it has shipped; **v0.2** is the
dependencies and every minor and moderate fix; **v0.3** is the bigger tasks and the new capabilities,
everything estimated `l` or `xl`. What is in each and why is in
[`../docs/BRIEF.md`](../docs/BRIEF.md) *Release phases* — that section is the decision, this page is
the current state of it. **Closed tasks keep the `WP1`–`WP3` packages they were worked under**;
those were phases of the research and design work and rewriting them would be rewriting what
happened.

<!-- taskmd:index - generated, do not edit by hand -->

## Active

| ID | Title | Work Package | Status | Phase | Parent | Children | Blocks | Related |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [T-019](T-019-build-the-capability-preflight-the-deck-ships-wit.md) | Build the capability preflight every deck ships with | `v0.3` | `proposed` | `specify` | - | - | - | T-005, T-017, T-041, T-057, T-070 |
| [T-036](T-036-the-second-contents-page-for-long-decks.md) | Continue the contents page onto a second sheet for decks past the measured bound | `v0.2` | `proposed` | `specify` | T-034 | - | - | T-005, T-034, T-042, T-084 |
| [T-041](T-041-implement-the-nine-glitch-free-conditions.md) | Implement the nine glitch-free conditions R6 defined and nothing adopted | `v0.3` | `proposed` | `specify` | - | - | - | T-005, T-016, T-019, T-042 |
| [T-054](T-054-record-which-clauses-of-a-rule-the-gate-decides.md) | Record which clauses of a rule the gate decides, not only which rules it reaches | `v0.3` | `proposed` | `specify` | T-053 | - | - | T-005, T-037, T-043, T-051 |
| [T-057](T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) | The 3D visual class, the frame-rate figure, and DS-140's fifth motion | `v0.3` | `proposed` | `specify` | T-016 | - | - | T-007, T-016, T-019, T-033 |
| [T-070](T-070-the-quick-view-for-a-source-document.md) | The quick view — a source document rendered inside the deck | `v0.3` | `proposed` | `specify` | - | - | - | T-019, T-069, T-071 |
| [T-080](T-080-check-resolves-a-markdown-link-inside-a-code-fence.md) | taskmd check resolves a markdown link inside a code fence, so pasted output cannot be quoted | `v0.2` | `in_progress` | `implement` | - | - | - | T-063, T-073, T-079, T-081 |

## Closed

| ID | Title | Work Package | Status | Phase | Parent | Children | Blocks | Related |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [T-001](T-001-decide-the-font-strategy-embedded-subsets-or-a-syste.md) | Decide the font strategy: embedded subsets or a system stack | `WP2` | `done` | `review` | - | - | - | T-005, T-013, T-024 |
| [T-002](T-002-build-mode-the-self-contained-deck-generator.md) | Build mode — the self-contained deck generator | `v0.1` | `done` | `review` | - | - | T-019 | T-003, T-004, T-005, T-006, T-007, T-015, T-016, T-017, T-018, T-020, T-021, T-023, T-024, T-026, T-027, T-028 |
| [T-003](T-003-brief-mode-elicit-the-six-section-prompt.md) | Brief mode — elicit the six-section prompt | `WP3` | `cancelled` | `specify` | - | - | - | T-002, T-015, T-020, T-027 |
| [T-004](T-004-critique-mode-blunt-section-by-section-review.md) | Critique mode — blunt section-by-section review | `v0.1` | `done` | `review` | - | - | - | T-002, T-005, T-020, T-022, T-023, T-026, T-042, T-047, T-048 |
| [T-005](T-005-build-check-the-gate-the-deck-must-pass.md) | Build check — the gate the deck must pass | `WP3` | `done` | `review` | - | T-040 | - | T-001, T-002, T-004, T-007, T-016, T-017, T-018, T-019, T-021, T-022, T-023, T-025, T-027, T-028, T-032, T-034, T-036, T-037, T-038, T-039, T-041, T-042, T-043, T-047, T-048, T-050, T-051, T-053, T-054, T-055, T-058 |
| [T-006](T-006-decide-the-chart-strategy.md) | Decide the chart strategy | `WP2` | `done` | `review` | - | - | - | T-002, T-013, T-016, T-017, T-024 |
| [T-007](T-007-define-the-parametric-theme-layer.md) | Define the parametric theme layer | `WP2` | `done` | `review` | - | - | - | T-002, T-005, T-016, T-021, T-024, T-057, T-059 |
| [T-008](T-008-package-document-and-publish.md) | Package, document and publish | `v0.1` | `done` | `review` | - | - | - | T-030, T-042, T-050, T-061, T-064, T-078 |
| [T-009](T-009-analyse-the-corpus-extract-my-deck-conventions.md) | Analyse the corpus — extract the deck conventions already in use | `WP1` | `done` | `review` | - | - | - | T-012, T-014 |
| [T-010](T-010-research-external-deck-design-and-ux-principles.md) | Research external deck-design and presentation UX principles | `WP1` | `done` | `review` | - | - | - | T-014 |
| [T-011](T-011-research-exemplary-decks-and-why-they-work.md) | Research exemplary decks and what makes them work | `WP1` | `done` | `review` | - | - | - | T-014 |
| [T-012](T-012-research-existing-html-deck-skills-and-libraries.md) | Research existing HTML-deck skills, plugins and libraries to build on | `WP1` | `done` | `review` | - | - | - | T-009, T-014, T-015 |
| [T-013](T-013-research-offline-safe-assets-and-licences.md) | Research offline-safe assets — icons, illustration, fonts, diagram tooling | `WP1` | `done` | `review` | - | - | - | T-001, T-006, T-014, T-017 |
| [T-014](T-014-synthesise-research-into-the-design-system-reference.md) | Synthesise the research into the htmldeck design-system reference | `WP1` | `done` | `review` | - | T-022 | - | T-009, T-010, T-011, T-012, T-013, T-020, T-021, T-023, T-024, T-025, T-037, T-038, T-039, T-047, T-049 |
| [T-015](T-015-plugin-scaffold-and-the-two-question-interface.md) | Plugin scaffold and the two-question interface | `WP2` | `done` | `review` | - | - | - | T-002, T-003, T-012, T-020, T-027, T-050, T-061 |
| [T-016](T-016-the-interaction-and-motion-layer.md) | The interaction and motion layer | `v0.1` | `done` | `review` | - | T-057 | - | T-002, T-005, T-006, T-007, T-017, T-021, T-024, T-032, T-035, T-041, T-057, T-058, T-069 |
| [T-017](T-017-define-the-portability-contract.md) | Define the portability contract — what "opens anywhere and works" actually permits | `WP1` | `done` | `review` | - | - | - | T-002, T-005, T-006, T-013, T-016, T-018, T-019, T-049 |
| [T-018](T-018-measure-the-printable-mode-what-printing-from-fi.md) | Measure the printable mode — what printing a deck from `file://` actually costs | `WP1` | `done` | `review` | - | - | - | T-002, T-005, T-017, T-021, T-029, T-032, T-034 |
| [T-020](T-020-model-the-authoring-pipeline-not-just-the-modes.md) | Model the authoring pipeline, not just the three modes | `WP1` | `done` | `review` | - | - | - | T-002, T-003, T-004, T-014, T-015, T-022, T-023, T-026, T-027, T-030 |
| [T-021](T-021-the-reflow-view-and-the-resolution-contract.md) | Build the reflow view and enforce the resolution contract | `WP2` | `done` | `review` | - | - | - | T-002, T-005, T-007, T-014, T-016, T-018, T-024, T-025, T-028, T-032, T-037, T-039, T-083 |
| [T-022](T-022-split-the-design-system-from-its-rationale.md) | Split the operative ruleset from its rationale, and give every rule an ID | `WP1` | `done` | `review` | T-014 | - | - | T-004, T-005, T-020, T-023, T-025, T-037, T-039 |
| [T-023](T-023-the-deck-evaluation-rubric-and-convergence-loop.md) | Define the deck evaluation rubric and the convergence loop that uses it | `WP1` | `done` | `review` | - | T-026 | - | T-002, T-004, T-005, T-014, T-020, T-022, T-024, T-025, T-044, T-048 |
| [T-024](T-024-build-the-reference-deck-and-validate-the-ruleset.md) | Build the reference deck by hand and find out whether the ruleset works | `WP2` | `done` | `review` | - | T-025 | - | T-001, T-002, T-006, T-007, T-014, T-016, T-021, T-023, T-026, T-027, T-028, T-040, T-044, T-050, T-052 |
| [T-025](T-025-reconcile-the-thirteen-ruleset-findings-from-the-reference-deck.md) | Reconcile the thirteen ruleset findings the reference deck produced | `WP2` | `done` | `review` | T-024 | - | - | T-005, T-014, T-021, T-022, T-023, T-027, T-028, T-033, T-047 |
| [T-026](T-026-settle-who-scores-a-deck-and-whether-the-score-is-shown.md) | Settle who scores a deck, and whether the score reaches the user | `WP2` | `done` | `review` | T-023 | T-029 | - | T-002, T-004, T-020, T-024, T-048 |
| [T-027](T-027-specify-the-slide-deliverable-and-the-outline-contract.md) | Specify the slide deliverable and the outline contract, and the rules the owner's deck review implies | `WP2` | `done` | `review` | - | T-028 | - | T-002, T-003, T-005, T-015, T-020, T-024, T-025, T-033, T-035, T-048 |
| [T-028](T-028-rewrite-the-reference-deck-to-the-deliverable-contract.md) | Retrofit the reference deck to the deliverable contract and thin its chrome | `WP2` | `done` | `review` | T-027 | - | - | T-002, T-005, T-021, T-024, T-025, T-030, T-032, T-033, T-035, T-040, T-044, T-045, T-052 |
| [T-029](T-029-stop-the-deliverable-exemption-silently-dropping-pointers.md) | Stop the deliverable exemption silently dropping pointers from the check | - | `done` | `review` | T-026 | - | - | T-018, T-031, T-046 |
| [T-030](T-030-audit-the-backlog-edges-and-propose-a-build-order.md) | Audit the dependency edges across the open backlog and propose a build order | - | `done` | `review` | - | - | - | T-008, T-020, T-028, T-031 |
| [T-031](T-031-stop-the-index-blocks-column-listing-closed-tasks.md) | Stop the index `Blocks` column listing closed downstream tasks | - | `done` | `review` | - | - | - | T-029, T-030, T-046, T-079 |
| [T-032](T-032-adopt-the-paginated-print-mode-in-the-reference-deck.md) | Adopt the paginated print mode in the reference deck, and decide whether print carries tier two | `WP2` | `done` | `review` | - | - | - | T-005, T-016, T-018, T-021, T-028, T-034, T-044 |
| [T-033](T-033-reconcile-ds-131-with-the-chrome-budget.md) | Reconcile DS-131 with the chrome budget it now contradicts | `WP2` | `done` | `review` | - | - | - | T-025, T-027, T-028, T-035, T-037, T-057 |
| [T-034](T-034-a-contents-page-for-the-printed-deck.md) | Add a contents page to the printed deck | `WP2` | `done` | `review` | - | T-036 | - | T-005, T-018, T-032, T-035, T-036, T-044 |
| [T-035](T-035-the-ruler-navigator.md) | Replace the stage ribbon with a ruler navigator, and rescope the chrome budget it breaks | `WP2` | `done` | `review` | - | - | - | T-016, T-027, T-028, T-033, T-034, T-044 |
| [T-037](T-037-record-in-the-ruleset-which-rules-no-check-can-reach.md) | Record in the ruleset itself which rules no check can reach | `WP2` | `done` | `review` | - | T-039 | - | T-005, T-014, T-021, T-022, T-033, T-038, T-042, T-043, T-045, T-046, T-048, T-053, T-054 |
| [T-038](T-038-the-gate-emits-verdicts-for-judge-rules-and-one-wrong-id.md) | Stop the gate reporting judge rules, and one verdict under the wrong rule ID | `WP3` | `done` | `review` | - | - | - | T-005, T-014, T-037, T-043, T-051, T-053, T-055 |
| [T-039](T-039-finish-the-record-t-037-left-in-the-wrong-places.md) | Finish the record T-037 left in the wrong places | `WP2` | `done` | `review` | T-037 | - | - | T-005, T-014, T-021, T-022, T-042, T-046 |
| [T-040](T-040-fix-the-three-reference-deck-defects-the-new-gate-found.md) | Fix the three reference-deck defects the completed gate found | `WP3` | `done` | `review` | T-005 | - | - | T-024, T-028, T-044, T-052 |
| [T-042](T-042-audit-the-whole-repository-against-itself.md) | Audit the repository against itself — stale claims, unreachable rules, and unchecked references | - | `done` | `review` | - | T-043, T-044, T-045, T-046, T-047, T-048, T-049, T-050 | - | T-004, T-005, T-008, T-036, T-037, T-039, T-041, T-056 |
| [T-043](T-043-make-the-gates-coverage-account-provable.md) | Make the gate's coverage account provable, and derive the counts the documents state | - | `done` | `review` | T-042 | - | - | T-005, T-037, T-038, T-051, T-054 |
| [T-044](T-044-restore-the-seeded-defect-fixture-and-its-claims.md) | Restore the seeded-defect fixture, and re-measure everything examples/README claims | - | `done` | `review` | T-042 | T-051 | - | T-023, T-024, T-028, T-032, T-034, T-035, T-040, T-045, T-052 |
| [T-045](T-045-sweep-the-stale-claims-across-the-live-documents.md) | Sweep the nine stale claims the audit found across the live documents | - | `done` | `review` | T-042 | - | - | T-028, T-037, T-044, T-046, T-047 |
| [T-046](T-046-extend-task-py-to-what-it-cannot-see.md) | Extend task.py to the three things it cannot currently see | - | `done` | `review` | T-042 | - | - | T-029, T-031, T-037, T-039, T-045, T-062 |
| [T-047](T-047-give-the-rationale-conflicts-their-own-id-namespace.md) | Give the rationale's conflicts their own ID namespace, and fix the mis-citation it has already caused | - | `done` | `review` | T-042 | - | - | T-004, T-005, T-014, T-025, T-045 |
| [T-048](T-048-gate-the-hard-rules-only-judgement-can-reach.md) | Gate the twenty-five hard rules only a judgement pass can reach | `WP2` | `done` | `review` | T-042 | T-052 | - | T-004, T-005, T-023, T-026, T-027, T-037 |
| [T-049](T-049-reconcile-the-session-memory-with-the-research.md) | Reconcile the session memory with what the research settled and the owner last said | - | `done` | `review` | T-042 | - | - | T-014, T-017 |
| [T-050](T-050-write-the-repository-readme.md) | Write the repository README — what exists, what does not, and how to run it | `final` | `done` | `review` | T-042 | - | - | T-005, T-008, T-015, T-024, T-056, T-060 |
| [T-051](T-051-a-check-with-no-subject-must-not-report-a-pass.md) | A check whose subject is absent must not report a pass | - | `done` | `review` | T-044 | - | - | T-005, T-038, T-043, T-053, T-054, T-065, T-066, T-075 |
| [T-052](T-052-two-hard-judge-failures-in-the-reference-deck.md) | Settle the two hard-judge failures the checklist's first run found in the reference deck | - | `done` | `review` | T-048 | - | - | T-024, T-028, T-040, T-044, T-056 |
| [T-053](T-053-enforce-the-headline-ds-091-requires.md) | Enforce the headline DS-091 requires, and excuse the fragment count no check can reach | - | `done` | `review` | - | T-054, T-055 | - | T-005, T-037, T-038, T-051 |
| [T-055](T-055-a-variant-that-leaves-malformed-markup.md) | Close the slide-is-not-a-section variant's open tag, so it tests the tag and not parser repair | `v0.2` | `done` | `review` | T-053 | - | - | T-005, T-038 |
| [T-056](T-056-humanize-the-human-facing-documents-before-publishing.md) | Humanize the human-facing documents before publishing | `v0.1` | `done` | `review` | - | - | - | T-042, T-050, T-052, T-060, T-067, T-078 |
| [T-058](T-058-the-seeded-defect-generator-reports-edits-that-never-matched.md) | The seeded-defect generator reports edits that never matched | `v0.2` | `done` | `review` | - | - | - | T-005, T-016 |
| [T-059](T-059-theme-swap-overwrites-its-input-when-o-is-omitted.md) | Theme swap overwrites its input when -o is omitted | `v0.2` | `done` | `review` | - | - | - | T-007 |
| [T-060](T-060-check-that-the-readmes-pasted-figures-still-match-their-commands.md) | Check that the README's pasted figures still match the commands that produced them | `v0.2` | `done` | `review` | - | - | - | T-050, T-056, T-067, T-068, T-077 |
| [T-061](T-061-the-scaffold-check-passed-a-manifest-the-installer-rejects.md) | The scaffold check passed a manifest the installer rejects | `v0.1` | `done` | `review` | - | - | - | T-008, T-015, T-062, T-064, T-067 |
| [T-062](T-062-retire-the-pre-split-task-tool-and-repoint-what-points-at-it.md) | Retire the pre-split task tool and repoint what points at it | `v0.2` | `done` | `review` | - | - | - | T-046, T-061, T-063, T-073, T-079, T-081 |
| [T-063](T-063-improvements-to-propose-upstream-to-taskmd.md) | Improvements to propose upstream to taskmd | `v0.2` | `done` | `review` | - | - | - | T-062, T-073, T-079, T-080 |
| [T-064](T-064-the-tools-crash-when-the-deck-is-on-another-drive.md) | The tools crash when the deck is on a different drive from the plugin | `v0.1` | `done` | `review` | - | - | - | T-008, T-061, T-065 |
| [T-065](T-065-four-rules-still-fail-a-deck-for-not-having-their-subject.md) | Four rules still fail a deck for not having their subject | `v0.1` | `done` | `review` | - | - | - | T-051, T-064, T-066, T-075 |
| [T-066](T-066-make-the-absent-subject-rule-a-fixture-instead-of-a-sweep.md) | Make the absent-subject rule a fixture instead of a sweep | `v0.1` | `done` | `review` | - | - | - | T-051, T-065, T-075 |
| [T-067](T-067-the-published-upgrade-instructions-do-not-upgrade.md) | The published upgrade instructions do not upgrade anything | `v0.1` | `done` | `review` | - | - | - | T-056, T-060, T-061 |
| [T-068](T-068-bind-a-prose-figure-to-a-field-not-to-the-whole-output.md) | Bind a prose figure to the field that produces it, not to the whole output | `v0.2` | `done` | `review` | - | - | - | T-060 |
| [T-069](T-069-extend-the-provenance-mark-to-multiple-sources.md) | Extend the provenance mark to multiple sources, and decide where deck-wide sources go | `v0.2` | `done` | `review` | - | - | T-070 | T-016, T-070, T-084, T-085 |
| [T-071](T-071-the-intermediate-specifications-carry-their-references.md) | The intermediate specifications carry the sources they rest on | `v0.2` | `done` | `review` | - | - | - | T-070, T-082, T-083, T-085, T-086 |
| [T-073](T-073-decide-whether-to-keep-refcheck-now-that-upstream-has-ruled.md) | Decide whether to keep refcheck now that upstream has ruled on bare paths | `v0.2` | `done` | `review` | - | - | - | T-062, T-063, T-074, T-077, T-079, T-080, T-081 |
| [T-074](T-074-the-documented-render-command-does-not-exist.md) | The documented render command does not exist, and the tools write into their own install | `v0.1` | `done` | `review` | - | - | - | T-073 |
| [T-075](T-075-ds-064-probes-for-the-reference-decks-own-class-names.md) | DS-064 probes for the reference deck's own class names, and contract.py is outside the fixture | `v0.1` | `done` | `review` | - | - | - | T-051, T-065, T-066, T-076, T-083 |
| [T-076](T-076-a-verdict-producer-that-exits-instead-of-reporting.md) | A verdict producer that exits the process instead of reporting a row | `v0.2` | `done` | `review` | - | - | - | T-075 |
| [T-077](T-077-report-a-figure-exclusion-that-outlived-its-numeral.md) | Report a figure exclusion that outlived the numeral it was written for | `v0.2` | `done` | `review` | - | - | - | T-060, T-073 |
| [T-078](T-078-write-down-the-release-sequence.md) | Write down the release sequence, which lives only in four task logs | `v0.2` | `done` | `review` | - | - | - | T-008, T-056, T-084, T-085 |
| [T-079](T-079-the-boards-dependency-columns-list-closed-tasks.md) | The board's dependency columns list closed tasks, so open rows read as blocked | `v0.2` | `done` | `review` | - | - | - | T-031, T-062, T-063, T-073, T-080, T-081 |
| [T-081](T-081-the-installed-taskmd-is-two-minor-versions-behind.md) | The installed taskmd is two minor versions behind, so the gates run rules that have been superseded | `v0.2` | `done` | `review` | - | - | - | T-062, T-073, T-079, T-080 |
| [T-082](T-082-the-worked-examples-figure-ledger-omits-figures-that-reach-slides.md) | The worked example's figure ledger omits figures that reach slides, so the ledger cannot be the authority it is treated as | `v0.2` | `done` | `review` | - | - | - | T-071, T-086, T-087 |
| [T-083](T-083-the-generated-example-deck-fails-a-hard-rule-and-nothing-recorded-it.md) | The generated example deck fails a hard rule and nothing recorded it | `v0.1` | `done` | `review` | - | - | - | T-021, T-071, T-075, T-084, T-085 |
| [T-084](T-084-the-contents-bound-fixture-counts-a-deck-that-no-longer-exists.md) | The contents-bound fixture counts a deck that no longer exists, and has been red since the day the deck changed | `v0.2` | `done` | `review` | - | - | - | T-036, T-069, T-078, T-083 |
| [T-085](T-085-the-reference-deck-does-not-carry-the-shell-it-defines.md) | The reference deck does not carry the shell it defines, and its sprite is out of sync | `v0.1` | `done` | `review` | - | - | - | T-069, T-071, T-078, T-083 |
| [T-086](T-086-check-that-every-ledger-row-appears-on-the-slides-its-used-on-names.md) | Check that every figure ledger row appears on the slides its Used on names | `v0.2` | `done` | `review` | - | - | - | T-071, T-082, T-087 |
| [T-087](T-087-sweep-the-reference-decks-figure-ledger-for-the-pattern-t-082-found.md) | Sweep the reference deck's figure ledger for the pattern T-082 found | `v0.2` | `done` | `review` | - | - | - | T-082, T-086 |

<!-- taskmd:end -->
