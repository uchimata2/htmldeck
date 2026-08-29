# Remediation order — the 47 tasks, batched for unattended sessions

**Tier 3. Loaded by nothing**; opened when a session asks *what do I work next*. It is a schedule,
not a decision: what each task does is its own record, and this file never restates one.

Written 2026-08-29, after the pre-release audit's triage (cycle 40) and the ClaimAI adopter triage
([T-225](../tasks/T-225-triage-the-claimai-adopter-report.md)) put 49 tasks on the board at once.
**[T-057](../tasks/T-057-the-3d-class-the-frame-rate-figure-and-ds-140s-fifth-motion.md) is out of
scope by the owner's instruction** — the 3D visual is deferred, not scheduled here. That leaves 47
tasks plus [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md)'s two remaining
cycles.

**A batch keeps its membership whether or not its tasks are closed — this is a schedule, not a board.** How many are still open is [`../tasks/README.md`](../tasks/README.md)'s answer and never this file's, so nothing here carries a count that decays. **B1 and B2 landed 2026-08-29.**

---

## 1. The three rules that decide the order

Everything below follows from these. They are stated first because a batch that violates one costs
more than it saves.

1. **An instrument is fixed before anything it measures.** Three were producing wrong answers when
   this file was written — `density.py write` wrote invalid markup, `render.py motion` reported a
   working motion as dead, and the scaffold gate read nought of the skill's eighteen commands. Work
   verified against a lying instrument has to be verified again. **All three were fixed in B1 on
   2026-08-29**, which is what makes wave 2 onwards worth running; the rule stands for whatever the
   later batches find.
2. **A rule changes before any document that counts it.** Sixteen open tasks state a figure that a
   rule change moves — rule totals, `auto`/`judge` splits, coverage counts. Fix the documents first
   and every one of them moves twice. **This is why every documentation task is in the last third**,
   including the ones ranked `High`.
3. **A deck is rebuilt once.** Five tracked decks are gated byte-for-byte. Every task that changes
   the shell, a theme, a rule's check or a generator invalidates them, so the deck work sits after
   all of it and the rebuild happens in one batch.

**The release is cut after all forty-seven**, ruled by the owner 2026-08-29. So no finding
needs a deferral reason, cycle 41 re-reads a settled tree, and the eighteen `PH1` tasks are
worked where this order puts them rather than pulled forward — which is the whole reason the
corollary below is affordable.

**The corollary nobody likes:** the `High` and `critical` bands do **not** run first. Severity
measures the audience's cost; this order measures rework. Where they disagree, a `critical`
documentation fix waits behind a `medium` instrument fix, because the instrument decides whether the
documentation fix can be verified at all.

---

## 2. The batches

Each batch is one unattended session: one subject area, no file conflicts inside it, and no decision
that is still the owner's. **A batch ends at a commit.** Six batches carried a question when this
file was written; all eight questions were ruled the same day and §3 holds the answers, so no batch
is blocked.

### Wave 1 — the instruments (nothing downstream is trustworthy until these land)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B1** — landed 2026-08-29 | [T-254](../tasks/T-254-density-py-write-corrupts-every-self-closing-svg-tag.md), [T-255](../tasks/T-255-render-py-motion-seeks-past-the-delay.md), [T-231](../tasks/T-231-two-packaging-checks-have-no-subject-at-all.md), **+[T-272](../tasks/T-272-render-py-motion-enumerates-a-different-animation-set-across-runs.md)** | `s`·4 | Three instruments that answer wrongly today. `density.py write` is refused outright by the adopter's launcher and is the tool `DS-239` makes necessary; `render.py motion` prints a verdict about its own seek as a finding about the deck; the scaffold gate has read nothing since 2026-08-20. Files are disjoint: `density.py`, `render.py`, `check_scaffold.py`. **`T-272` was found while closing `T-255` and absorbed into the batch under §4** — the same instrument enumerating a different animation set across runs of one unchanged deck |
| **B2** — landed 2026-08-29 | [T-261](../tasks/T-261-ds-035-measures-a-text-run-through-its-transform.md) | `s` | **Alone, because it changes what every geometry rule measures.** The probe must be pinned for `DS-035` and unpinned for `DS-140`, `DS-142` and `DS-218`, so it is a split rather than a flag, and its blast radius wants its own gate run. **The split is in time rather than in a flag**: the probe reads its motion facts, pins, then measures. T-209's *identical both ways* was re-derived and does not generalise — two geometry rows move on a deck whose entrance moves the axis |
| **B3** | [T-246](../tasks/T-246-two-docs-instruments-misdescribe-their-own-behaviour.md) | `s` | `figures.py`'s `bind()` decides every pasted figure in the tree, and sixteen later tasks paste figures. Fixing what it actually pairs before they run is the difference between one sweep and two |

### Wave 2 — rules and checks (they move the counts, so they precede every document)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B4** | [T-243](../tasks/T-243-five-checks-bound-on-a-name-rather-than-on-structure.md), [T-230](../tasks/T-230-the-resolution-contract-samples-four-slides-by-fixed-index.md) | `m`,`s` | Five checks re-bound on structure, plus the adopter's `DS-229` and `DS-239` records. **Needs B1** — `T-243`'s `DS-239` half is unverifiable while `density.py write` corrupts what it writes |
| **B5** | [T-263](../tasks/T-263-ds-217-fails-on-any-deck-past-eighteen-sections.md), [T-262](../tasks/T-262-ds-092-counts-a-sources-box-as-prose.md), [T-264](../tasks/T-264-ds-141s-request-licence-has-nowhere-to-put-its-number.md) | `s`·3 | Three rules that a correct deck cannot satisfy. Independent of each other; all three change `audit.py` and a rule row. **`T-264`'s question is ruled** — §3 |
| **B6** | [T-256](../tasks/T-256-ds-219-cannot-see-a-painted-svg-ancestor.md), [T-260](../tasks/T-260-ds-244-tests-proximity-where-it-means-obstruction.md) | `m`·2 | The two rules whose *scope* is in question rather than their code. **Both questions are ruled** (§3). Held together because both re-open what a rule measures and both are gated by `T-204`'s calibration precedent |
| **B7** | [T-229](../tasks/T-229-ds-106s-check-omits-a-word-the-rule-names.md), [T-242](../tasks/T-242-the-contracts-against-the-checkers-that-decide-them.md) | `s`,`m` | Deriving a check from its rule row, and reconciling the two contracts with their checkers. Both are *derive rather than restate* work and share the idiom |
| **B8** | [T-265](../tasks/T-265-ds-110-cannot-tell-a-rasterised-diagram-from-a-drawing.md), [T-266](../tasks/T-266-a-deck-cannot-name-a-repeated-figure-treatment-once.md), [T-270](../tasks/T-270-two-rules-whose-escape-hatch-teaches-the-wrong-habit.md) | `s`·3 | The three rule **decisions**. Grouped because each is a `DS-000` ruleset change with a stated reason, and one session can hold that frame once. **All three are ruled** (§3), so the session writes the change rather than deciding it |

### Wave 3 — the product (shell, tools, themes)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B9** | [T-232](../tasks/T-232-two-entrance-motions-do-not-collapse-for-print.md), [T-268](../tasks/T-268-three-chrome-and-timing-defects-in-deck-js.md) | `s`·2 | The shell: the print block's entrance collapse, and three chrome and timing defects the presenter reported. `components.css` and `deck.js`, and both end in a print or a look |
| **B10** | [T-269](../tasks/T-269-three-build-path-defects-the-adopter-worked-around.md), [T-245](../tasks/T-245-seven-tool-defects-in-tools-deck.md) | `s`,`m` | Ten small defects across the build path and the deck tools. Each carries its own reproduction, so the batch is ten independent seeded proofs |
| **B11** | [T-228](../tasks/T-228-the-second-theme-fails-the-contract-it-demonstrates.md), [T-244](../tasks/T-244-the-gates-own-coverage-account.md) | `s`,`m` | The theme validation step, and deriving the gate's clause-level account. **`T-244` must follow every rule change above** — it derives what the gate decides, and a table derived before the rules settle is derived twice |

### Wave 4 — the decks (rebuilt once, after everything above)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B12** | [T-233](../tasks/T-233-a-shipped-deck-carries-eleven-copies-of-one-source.md), [T-248](../tasks/T-248-four-content-errors-in-three-shipped-decks.md), [T-247](../tasks/T-247-the-portfolio-generators-documents-against-the-deck.md) | `s`,`m`,`s` | Every change that invalidates a deck has landed, so the five tracked decks are rebuilt **once** here. Ten dead quick-view payloads removed, four content errors corrected against their source models, and the generator's documents reconciled |
| **B13** | [T-257](../tasks/T-257-ds-218-passes-the-shipped-example-vacuously.md), [T-226](../tasks/T-226-a-shipped-deck-is-in-neither-human-facing-document.md) | `s`·2 | The example's own defects: a rule it passes vacuously, and a deck missing from both human-facing documents. **`T-257`'s question is ruled** — §3 |

### Wave 5 — new capability

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B14** | [T-259](../tasks/T-259-nothing-prints-what-a-slide-actually-contains.md), [T-258](../tasks/T-258-the-gate-passes-copy-its-own-reader-calls-difficult.md) | `m`·2 | Two printers that report rather than gate, built against a tree whose rules have settled. `T-259` first: the fact printer is what a later verdict would rest on |
| **B15** | [T-267](../tasks/T-267-render-py-cannot-capture-a-decks-interactive-states.md), [T-271](../tasks/T-271-a-quick-view-scoped-to-a-document-section.md) | `m`·2 | Interactive capture, and the per-section quick view. **`T-271` stays deferred past the release** by §3's ruling, so B15 is `T-267` alone unless the owner reschedules it |

### Wave 6 — documentation and counts (last, because every figure depends on everything above)

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B16** | [T-227](../tasks/T-227-the-front-pages-adoption-route-names-a-variable-the-skill-removed.md), [T-235](../tasks/T-235-the-skills-documents-against-the-tools-they-describe.md) | `s`·2 | What an adopter receives. **`T-235` needs B1** — its proof is vacuous while the scaffold gate reads nothing. `T-227` carries the adopter's launcher record and settles what `$HTMLDECK` resolves to |
| **B17** | [T-234](../tasks/T-234-the-front-pages-own-figures-and-claims.md), [T-236](../tasks/T-236-tier-1-and-the-brief-against-what-they-measure.md), [T-220](../tasks/T-220-derive-the-release-chronologys-task-count-instead-of-typing-it.md) | `s`,`m`,`s` | The front page, tier 1 and the brief — every figure in them re-derived against a tree that has stopped moving |
| **B18** | [T-240](../tasks/T-240-the-evaluation-document-against-itself-and-the-code.md), [T-241](../tasks/T-241-the-design-system-and-the-rationale-against-what-shipped.md) | `m`,`s` | The evaluation and the ruleset's rationale. **`T-241` needs B6** — `PR-97`'s unresolved conflict is `DS-219`'s, and `T-256` is what settles it |
| **B19** | [T-237](../tasks/T-237-the-release-machinery-and-its-record.md), [T-238](../tasks/T-238-the-trackers-own-rules-against-its-own-records.md) | `m`,`s` | The release documents against the releases that ran, and the tracker's own rules |
| **B20** | [T-249](../tasks/T-249-the-two-prior-audits-registers.md), [T-250](../tasks/T-250-two-lessons-state-a-figure-and-two-link-to-a-dead-anchor.md), [T-251](../tasks/T-251-a-research-note-and-a-memory-entry-describe-a-state-that-changed.md), [T-252](../tasks/T-252-the-ignore-rules-come-from-three-files-and-one-ships.md) | `s`·4 | Four small record repairs: the prior audit registers, four lessons, a research note and a memory entry, and the ignore rules |
| **B21** | [T-239](../tasks/T-239-the-audits-own-record-against-what-it-did.md) | `s` | The audit's own plan and ledger, reconciled **after** the remedies exist rather than before — the same reason cycle 41 waits |

### Wave 7 — the batch, and the audit's close

| Batch | Tasks | Eff | Why here |
| :--- | :--- | :--- | :--- |
| **B22** | [T-253](../tasks/T-253-the-low-findings-batch.md) | `l` | **Last of the remediation.** Forty-nine `Low` findings, many of them in documents waves 4 to 6 rewrite. Running it earlier means fixing a line and then rewriting the paragraph around it |
| **B23** | [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md) cycle 41 | — | Re-read cycles 1, 3 and 5 plus every cycle a remedy touched. **This is where the audit's own damage shows**, and it cannot run before the remedies exist |
| **B24** | [T-219](../tasks/T-219-pre-release-audit-of-the-whole-repository.md) cycle 42 | — | Phase 2: predicted against measured, per finding. It has to name at least one prediction the measurement refused, or it was not run honestly |

---

## 3. The eight rulings — answered 2026-08-29, before B1

Six batches carried a question that was the owner's rather than a session's. **All eight are ruled
and none of them stops a batch.** Each was put with its recommendation and the owner took the
recommendation in every case, so the column below is the ruling rather than a proposal.

**Each is reversible on the owner's word, and the task that implements it records it as a `DS-000`
change with the stated reason** — which is the ordinary route for a ruleset change, not an exception
bought by the authority in §5.

| Batch | Task | The question | **Ruled** |
| :--- | :--- | :--- | :--- |
| B5 | `T-264` | A per-deck motion band the theme contract names, or a `DS-010` exemption for a duration inside a `--motion-long` rule? | **The band.** It keeps the value where a generator can find it, which is the argument `DS-013` rests on |
| B6 | `T-256` | Once the ground walk is fixed, does `DS-219` keep its force, or does `DESIGN-RATIONALE.md` §5.7's doubt retire it? | **Fix the walk, keep the rule, re-measure.** The doubt is about over-firing, and a corrected walk is the only thing that can settle whether it still does |
| B6 | `T-260` | Does `DS-244`'s new shape comparison **gate** or **report**? | **Report, calibrate, then decide** — `T-204`'s own precedent, which took text-against-line to report at 16 firings for 1 real defect |
| B8 | `T-265` | Does `DS-110` narrow by where a raster sits? | **The record's weaker form**, not its primary: allow one that is not inside `.body` and carries no `role="img"` naming data |
| B8 | `T-266` | Reserve a deck-local class prefix so a deck can name a repeated figure treatment once? | **Yes.** `DS-229` keeps its real job — stopping a deck redefining a *component* — and stops policing figure internals no contract can anticipate |
| B8 | `T-270` | Accept only the two narrow halves of `DS-100` and `DS-202`, rejecting *make the rule reviewable* and *replace the sentence count*? | **Yes**, for the reasons in `T-225` §3 |
| B13 | `T-257` | Is a control one click inside a shut menu genuinely disqualifying? | **Yes, keep the rule** — and fix the example by giving it one looping motion, so it passes for a reason |
| B15 | `T-271` | Build the per-section quick view now, or keep it deferred past the release? | **Keep it deferred.** It is the only record asking for a new component and it competes with nothing else |

---

## 4. What an unattended session may do

Ruled by the owner 2026-08-29, in the same pass as §3. **These are standing authorities for this
programme of work, not general ones**: they are scoped to the 47 tasks in §2 and expire when B24
closes.

| May | Bound |
| :--- | :--- |
| **Commit and push each batch** | Per task where the task is the unit, and push at the end of the batch — the same shape every audit cycle used |
| **Amend a `DESIGN-SYSTEM.md` rule row** | Only where the task calls for it, with `DS-000`'s stated reason, and marked reversible. §3's eight are already ruled; a *ninth* rule question is not covered and stops the batch |
| **Rebuild and commit the five tracked decks** | They are gated byte-for-byte, so every rebuild is a reviewable diff. Rebuild in B12 where it can be done once; earlier, only where a task's own proof needs it |
| **Absorb what a batch finds** | **A small fix in place is made in place.** Anything with potential impact on other work becomes a task — **and that task is added to the running batch and worked in it**, rather than filed for later. A batch is elastic: it finishes what it started and what it found |

**The one thing a session may not do is look.** `CLAUDE.md` rule 6 is a person, and three of this
audit's findings were passed by every machine and caught by an eye. So:

- a task owing a look does **everything measurable**, records the look as **owed** — naming the deck,
  the slide and what to look for — and **closes**;
- the owed looks accumulate as a queue, and the owner runs **one looking pass** over it;
- **that pass happens before the release is cut**, which is what keeps rule 6 true rather than
  merely deferred. B12, B13 and B9 are the batches that will owe most of it.

---

## 5. What this order costs if it is wrong

**The risk is concentrated in wave 2.** If a rule decision in B6 or B8 comes back the other way, the
documents in wave 6 move again — which is the rework this order exists to avoid, arriving through
the one door it cannot close. That is why the questions in §3 are asked before B4 rather than when
each batch reaches them.

**The cheapest thing a reader can do with this file is disbelieve §2's dependencies and check them.**
Three are stated as hard and the rest are economics: `T-235` after `T-231`, `T-243` after `T-254`,
`T-241` after `T-256`. Everything else is *this saves a second pass*, and a session that finds a
better order should take it and say so here.
